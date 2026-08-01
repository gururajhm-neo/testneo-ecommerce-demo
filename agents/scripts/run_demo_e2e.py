"""One-button ecom → agent → ingest → post-agent-gate walkthrough."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from agents.config import ARTIFACTS_DIR, load_settings
from agents.runners.checkout import run_checkout
from agents.runners.memory_leak import run_memory_isolation
from agents.runners.refund import run_refund
from agents.testneo_client import TestNeoClient


def _banner(title: str) -> None:
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


def _print_gate(label: str, gate: dict[str, Any], client: TestNeoClient) -> None:
    overall = gate.get("overall_gate") or gate.get("risk_level")
    print(f"\n[{label}] overall_gate = {overall}")
    for w in (gate.get("why") or [])[:6]:
        print(f"  • {w}")
    layer4 = gate.get("layer4") or {}
    if layer4.get("requested"):
        print(f"  Layer4: {layer4.get('risk_level')}")
        for f in (layer4.get("findings") or [])[:5]:
            print(f"    [{f.get('severity')}] {f.get('title')}")
    execution = gate.get("execution") or {}
    if execution.get("requested"):
        print(
            f"  Suite: status={execution.get('status')} "
            f"finished={execution.get('suite_finished')} "
            f"batch={execution.get('batch_id')}"
        )
        for r in (execution.get("suite_runs") or [])[:8]:
            eid = r.get("execution_id")
            url = client.execution_url(eid) if eid else None
            print(f"    #{r.get('test_case_id')} {r.get('status')} {url or ''}")
    print(f"  UI: {client.agent_verification_url()}")
    print(f"  Executions: {client.executions_list_url()}")


def ingest_and_gate(
    client: TestNeoClient,
    summary: dict[str, Any],
    *,
    label: str,
    run_suite: bool,
) -> dict[str, Any]:
    _banner(f"Ingest + gate — {label}")
    ingest = client.ingest_agent_run(summary, auto_verify=False)
    context_id = ingest.get("context_id")
    print(f"Ingested context_id={context_id} agent_run_id={summary.get('agent_run_id')}")
    gate = client.post_agent_gate(
        context_id=int(context_id) if context_id else None,
        run_layer4=True,
        run_mapped_tests=run_suite,
        queue_execution=run_suite,
        wait_for_suite=False,
        generate_tests=False,
    )
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    out = ARTIFACTS_DIR / f"gate_{label}_{summary.get('agent_run_id')}.json"
    out.write_text(json.dumps(gate, indent=2, default=str), encoding="utf-8")
    _print_gate(label, gate, client)
    return gate


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Ecom CrewAI/deterministic → TestNeo E2E demo")
    parser.add_argument(
        "--scenario",
        choices=("all", "checkout", "refund", "refund-break", "memory", "memory-ok", "checkout-break"),
        default="all",
    )
    parser.add_argument("--skip-gate", action="store_true", help="Emit summaries only")
    parser.add_argument("--skip-suite", action="store_true", help="Gate without product suite")
    parser.add_argument("--seed", action="store_true", help="Seed delivered order first")
    parser.add_argument(
        "--print-emit",
        action="store_true",
        help="Pretty-print full agent_run_summary.v1 JSON (SDK emit) to stdout",
    )
    args = parser.parse_args(argv)

    settings = load_settings()
    print(f"Ecom API: {settings.ecom_api_base}")
    print(f"Runtime: {settings.agent_runtime}  CREW_DEMO_MODE={settings.crew_demo_mode}")
    print(f"TestNeo: {settings.testneo_base_url} project={settings.testneo_project_id}")

    if args.seed:
        from agents.scripts.seed_demo_state import main as seed_main

        rc = seed_main()
        if rc != 0:
            return rc

    client: TestNeoClient | None = None
    if not args.skip_gate:
        try:
            client = TestNeoClient(settings)
        except RuntimeError as exc:
            print(f"ERROR: {exc}")
            return 1

    run_suite = not args.skip_suite

    scenarios: list[tuple[str, Any]] = []
    if args.scenario in ("all", "checkout"):
        scenarios.append(("checkout-ok", lambda: run_checkout(settings, break_mode=False)))
    if args.scenario in ("all", "checkout-break"):
        scenarios.append(("checkout-break", lambda: run_checkout(settings, break_mode=True)))
    if args.scenario in ("all", "refund"):
        scenarios.append(("refund-ok", lambda: run_refund(settings, break_mode=False)))
    if args.scenario in ("all", "refund-break"):
        scenarios.append(("refund-break", lambda: run_refund(settings, break_mode=True)))
    if args.scenario in ("all", "memory"):
        scenarios.append(("memory-break", lambda: run_memory_isolation(settings, break_mode=True)))
    if args.scenario == "memory-ok":
        scenarios.append(("memory-ok", lambda: run_memory_isolation(settings, break_mode=False)))

    # For "all", preferred demo order: checkout ok → refund break → memory
    if args.scenario == "all":
        scenarios = [
            ("checkout-ok", lambda: run_checkout(settings, break_mode=False)),
            ("refund-break", lambda: run_refund(settings, break_mode=True)),
            ("memory-break", lambda: run_memory_isolation(settings, break_mode=True)),
        ]

    results = []
    for label, fn in scenarios:
        _banner(f"Run agent — {label}")
        try:
            result = fn()
        except Exception as exc:
            print(f"FAILED {label}: {exc}")
            return 1
        summary = result.summary
        print(f"claim: {summary.get('agent_claim')}")
        print(f"outcome: {summary.get('outcome')}  artifact: {result.artifact_path}")
        print(
            f"emit: contract={summary.get('contract_version')} "
            f"source={summary.get('source')} "
            f"via_sdk={os.environ.get('TESTNEO_USE_SDK', '1')}"
        )
        print(
            f"  tools={summary.get('touched', {}).get('tools')} "
            f"retrieved={[r.get('doc_id') for r in (summary.get('retrieved') or [])]} "
            f"memory={len(summary.get('memory_accesses') or [])}"
        )
        if args.print_emit:
            _banner(f"SDK emit — {label} — {summary.get('agent_run_id')}")
            print(json.dumps(summary, indent=2, default=str))
        if client:
            gate = ingest_and_gate(client, summary, label=label, run_suite=run_suite and label.startswith("checkout"))
            results.append((label, summary, gate))
        else:
            results.append((label, summary, None))

    _banner("Demo complete")
    for label, summary, gate in results:
        g = (gate or {}).get("overall_gate", "n/a")
        print(f"  {label}: outcome={summary.get('outcome')} gate={g}")
    if client:
        print(f"\nOpen Agent Verification: {client.agent_verification_url()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
