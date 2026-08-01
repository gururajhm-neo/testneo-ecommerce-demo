#!/usr/bin/env python3
"""Full loop: ecom agent → framework adapters → ingest → post-agent-gate.

Proves Generic / LangGraph / CrewAI / AutoGen against live ecom + TestNeo project.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

# Ensure demo root on path
_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from agents.adapter_emit import ADAPTER_NAMES, AdapterName, emit_via_adapter
from agents.config import ARTIFACTS_DIR, load_settings
from agents.runners.memory_leak import run_memory_isolation
from agents.runners.refund import run_refund
from agents.testneo_client import TestNeoClient


def _banner(msg: str) -> None:
    print("\n" + "=" * 72)
    print(msg)
    print("=" * 72)


def _write(name: str, payload: dict[str, Any]) -> Path:
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    path = ARTIFACTS_DIR / name
    path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    return path


def _ingest_and_gate(
    client: TestNeoClient,
    summary: dict[str, Any],
    *,
    label: str,
) -> dict[str, Any]:
    # Strip private meta before ingest
    body = {k: v for k, v in summary.items() if not str(k).startswith("_")}
    ingest = client.ingest_agent_run(body, auto_verify=False)
    context_id = ingest.get("context_id")
    gate = client.post_agent_gate(
        context_id=int(context_id) if context_id else None,
        run_layer4=True,
        run_mapped_tests=False,
        queue_execution=False,
        wait_for_suite=False,
        generate_tests=False,
    )
    gate_path = _write(f"gate_adapter_{label}_{summary.get('agent_run_id')}.json", gate)
    overall = gate.get("overall_gate") or gate.get("risk_level") or "?"
    print(
        f"  ingest context_id={context_id}  gate={overall}  "
        f"artifact={gate_path.name}"
    )
    return gate


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Ecom → SDK adapters → TestNeo full loop")
    parser.add_argument(
        "--scenario",
        choices=("refund", "memory-ok", "both"),
        default="both",
    )
    parser.add_argument(
        "--adapters",
        default="generic,langgraph,crewai,autogen",
        help="Comma list: generic,langgraph,crewai,autogen",
    )
    parser.add_argument(
        "--skip-gate",
        action="store_true",
        help="Emit summaries only (no ingest/gate)",
    )
    parser.add_argument(
        "--gate-adapters",
        default="",
        help="Which adapters to gate (default: all selected). Comma list.",
    )
    args = parser.parse_args(argv)

    os.environ.setdefault("TESTNEO_USE_SDK", "1")
    settings = load_settings()
    wanted: list[AdapterName] = []
    for part in args.adapters.split(","):
        name = part.strip().lower()
        if name in ADAPTER_NAMES:
            wanted.append(name)  # type: ignore[arg-type]
    if not wanted:
        print("No valid adapters selected")
        return 2

    gate_set = {
        p.strip().lower()
        for p in (args.gate_adapters or args.adapters).split(",")
        if p.strip()
    }

    print(f"Ecom API: {settings.ecom_api_base}")
    print(f"TestNeo: {settings.testneo_base_url} project={settings.testneo_project_id}")
    print(f"Adapters: {wanted}")
    print(f"TESTNEO_USE_SDK={os.environ.get('TESTNEO_USE_SDK')}")

    client: TestNeoClient | None = None
    if not args.skip_gate:
        try:
            client = TestNeoClient(settings)
        except RuntimeError as exc:
            print(f"ERROR: {exc}")
            return 1

    results: list[tuple[str, str, str]] = []  # scenario, adapter, gate/emit

    scenarios: list[tuple[str, Any]] = []
    if args.scenario in ("refund", "both"):
        scenarios.append(("refund-ok", "refund"))
    if args.scenario in ("memory-ok", "both"):
        scenarios.append(("memory-ok", "memory"))

    for label, kind in scenarios:
        _banner(f"1) Run ecom agent — {label}")
        if kind == "refund":
            agent = run_refund(settings, break_mode=False)
            if not agent.action_log:
                print("FAILED: refund returned no action_log")
                return 1
            base_kwargs = dict(
                goal=agent.goal,
                action_log=agent.action_log,
                agent_claim=agent.summary.get("agent_claim") or "",
                outcome=agent.outcome,
                authorization="READ_WRITE",
                confirmation_obtained=agent.confirmation_obtained,
                autonomy_decision=agent.autonomy_decision,
                gate_contract=agent.gate_contract,
                identity={"user_email": settings.ecom_email},
                web_base=settings.ecom_web_base,
                git_ref="adapter-loop",
            )
            print(
                f"  order_id={agent.order_id} tools={agent.action_log.tools} "
                f"sdk_bridge_artifact={agent.artifact_path.name}"
            )
        else:
            agent = run_memory_isolation(settings, break_mode=False)
            if not agent.action_log:
                print("FAILED: memory returned no action_log")
                return 1
            base_kwargs = dict(
                goal=agent.goal,
                action_log=agent.action_log,
                agent_claim=agent.agent_claim,
                outcome=agent.outcome,
                authorization=agent.authorization,
                confirmation_obtained=agent.confirmation_obtained,
                autonomy_decision=agent.autonomy_decision,
                gate_contract=agent.gate_contract,
                identity=agent.identity,
                web_base=settings.ecom_web_base,
                git_ref="adapter-loop",
            )
            print(f"  tools={agent.action_log.tools} artifact={agent.artifact_path.name}")

        for adapter_name in wanted:
            _banner(f"2) Emit via {adapter_name} adapter — {label}")
            try:
                summary = emit_via_adapter(adapter_name, **base_kwargs)
            except Exception as exc:
                print(f"FAILED emit {adapter_name}: {exc}")
                results.append((label, adapter_name, f"EMIT_FAIL:{exc}"))
                continue

            emit_path = _write(
                f"adapter_{adapter_name}_{label}_{summary['agent_run_id']}.json",
                summary,
            )
            print(
                f"  source={summary.get('source')} "
                f"tools={summary.get('touched', {}).get('tools')} "
                f"retrieved={[r.get('doc_id') for r in (summary.get('retrieved') or [])]} "
                f"memory={len(summary.get('memory_accesses') or [])} "
                f"file={emit_path.name}"
            )

            if client and adapter_name in gate_set:
                _banner(f"3) Ingest + gate — {adapter_name} / {label}")
                try:
                    gate = _ingest_and_gate(
                        client, summary, label=f"{adapter_name}_{label}"
                    )
                    overall = gate.get("overall_gate") or gate.get("risk_level") or "?"
                    results.append((label, adapter_name, str(overall)))
                except Exception as exc:
                    print(f"FAILED gate {adapter_name}: {exc}")
                    results.append((label, adapter_name, f"GATE_FAIL:{exc}"))
            else:
                results.append((label, adapter_name, "EMIT_ONLY"))

    _banner("SUMMARY")
    ok = True
    for scenario, adapter, status in results:
        good = status in ("PASS", "WARN", "EMIT_ONLY")
        if not good:
            ok = False
        print(f"  [{'OK' if good else '!!'}] {scenario:12} {adapter:10} → {status}")

    print(f"\nArtifacts: {ARTIFACTS_DIR}")
    if client:
        print(f"UI: {client.agent_verification_url()}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
