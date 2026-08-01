"""Full-loop adapter emit — ActionLog → framework adapters → agent_run_summary.v1.

Proves Generic / LangGraph / CrewAI / AutoGen adapters against the real ecom
tool trace (same evidence the gate needs: tools + retrieval + confirm + contract).
"""

from __future__ import annotations

import sys
import uuid
from pathlib import Path
from typing import Any, Literal

# Prefer sibling monorepo SDK (Documents/testneo-api next to this demo)
_SDK_SRC = (
    Path(__file__).resolve().parents[2] / "testneo-api" / "packages" / "testneo-agent-sdk" / "src"
)
_SDK_SRC_ALT = (
    Path(__file__).resolve().parents[1].parent.parent
    / "testneo-api"
    / "packages"
    / "testneo-agent-sdk"
    / "src"
)
for _p in (_SDK_SRC, _SDK_SRC_ALT):
    if _p.is_dir() and str(_p) not in sys.path:
        sys.path.insert(0, str(_p))
        break

from agents.action_log import ActionLog  # noqa: E402

AdapterName = Literal["generic", "langgraph", "crewai", "autogen"]
ADAPTER_NAMES: tuple[AdapterName, ...] = ("generic", "langgraph", "crewai", "autogen")


def _attach_shared_evidence(
    run: Any,
    *,
    action_log: ActionLog,
    authorization: str,
    confirmation_obtained: bool,
    autonomy_decision: str,
    gate_contract: dict[str, Any] | None,
    identity: dict[str, Any] | None,
    web_base: str | None,
    git_ref: str | None,
) -> None:
    """RAG / memory / confirm / gate — frameworks rarely put these in tool traces."""
    run.authorization(authorization)
    run.autonomy(autonomy_decision)
    if confirmation_obtained:
        run.confirmation(True)
    if identity:
        from testneo_agent.events import EventType, InternalEvent

        run.emit(
            InternalEvent(
                type=EventType.RUN_STARTED,
                run_id=run.agent_run_id,
                payload={"identity": dict(identity)},
            )
        )
    for api in action_log.api_calls:
        run.observe_api(
            str(api.get("method") or "GET"),
            str(api.get("path") or "/"),
            status=api.get("status"),
            url=web_base,
        )
    for hit in action_log.retrieved:
        if not hit.get("doc_id"):
            continue
        run.retrieval(
            doc_id=str(hit["doc_id"]),
            snippet=hit.get("snippet") or hit.get("text"),
            score=hit.get("score"),
            chunk_id=hit.get("chunk_id"),
            source=hit.get("source"),
            query=(hit.get("metadata") or {}).get("query")
            if isinstance(hit.get("metadata"), dict)
            else None,
            metadata=dict(hit.get("metadata") or {}),
            emit_action=False,
        )
    for access in action_log.memory_accesses:
        op = str(access.get("op") or "read").lower()
        kwargs = {
            "user_id": access.get("user_id"),
            "keys": access.get("keys") or [],
            "scope": access.get("scope") or "user",
            "tenant_id": access.get("tenant_id"),
            "session_id": access.get("session_id"),
            "values_preview": access.get("values_preview") or [],
        }
        if op == "write":
            run.memory_write(**kwargs)
        else:
            run.memory_read(**kwargs)
    if gate_contract:
        run.set_gate_contract(gate_contract)
    if git_ref:
        data = {"git_ref": git_ref}
        # Stash on summary via identity/metadata after finish (see emit_via_adapter)


def _tool_dicts(action_log: ActionLog) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for a in action_log.actions:
        out.append(
            {
                "tool": a.get("tool"),
                "name": a.get("tool"),
                "operation": a.get("operation") or "EXECUTE",
                "target": a.get("target"),
                "arguments": dict(a.get("arguments") or {}),
                "args": dict(a.get("arguments") or {}),
                "result": a.get("result") or "SUCCESS",
                "result_summary": a.get("result_summary"),
                "sequence": a.get("sequence"),
                "call_id": f"call-{a.get('sequence') or uuid.uuid4().hex[:8]}",
            }
        )
    return out


def _langgraph_events(action_log: ActionLog) -> list[dict[str, Any]]:
    """Tool stream events only — retrieval attached via shared evidence (avoid dup docs)."""
    events: list[dict[str, Any]] = []
    for a in action_log.actions:
        rid = f"lg-{a.get('sequence')}"
        events.append(
            {
                "event": "on_tool_start",
                "name": a.get("tool"),
                "run_id": rid,
                "data": {"input": dict(a.get("arguments") or {})},
            }
        )
        events.append(
            {
                "event": "on_tool_end",
                "name": a.get("tool"),
                "run_id": rid,
                "data": {"output": a.get("result_summary") or a.get("result") or "OK"},
            }
        )
    return events


def _autogen_messages(action_log: ActionLog, *, goal: str, claim: str) -> list[dict[str, Any]]:
    msgs: list[dict[str, Any]] = [{"role": "user", "content": goal}]
    tool_calls = []
    tool_results = []
    for a in action_log.actions:
        cid = f"call-{a.get('sequence')}"
        tool_calls.append(
            {
                "id": cid,
                "function": {
                    "name": a.get("tool"),
                    "arguments": dict(a.get("arguments") or {}),
                },
            }
        )
        tool_results.append(
            {
                "role": "tool",
                "name": a.get("tool"),
                "tool_call_id": cid,
                "content": a.get("result_summary") or a.get("result") or "OK",
            }
        )
    if tool_calls:
        msgs.append({"role": "assistant", "content": "", "tool_calls": tool_calls})
        msgs.extend(tool_results)
    msgs.append({"role": "assistant", "content": claim})
    return msgs


def emit_via_adapter(
    adapter_name: AdapterName,
    *,
    goal: str,
    action_log: ActionLog,
    agent_claim: str,
    outcome: str = "success",
    authorization: str = "READ_WRITE",
    confirmation_obtained: bool = False,
    autonomy_decision: str = "proceed",
    gate_contract: dict[str, Any] | None = None,
    identity: dict[str, Any] | None = None,
    web_base: str | None = None,
    git_ref: str | None = "adapter-loop",
    agent_run_id: str | None = None,
) -> dict[str, Any]:
    """Build summary through a real framework adapter (no HTTP ingest here)."""
    from testneo_agent import Config, TestNeo
    from testneo_agent.adapters import (
        AutoGenAdapter,
        CrewAIAdapter,
        GenericAdapter,
        LangGraphAdapter,
    )

    cfg = Config(auto_ingest=False, strict=True, agent_name="ecom-adapter-loop")
    sdk = TestNeo(cfg)
    run_id = agent_run_id or f"ecom-{adapter_name}-{uuid.uuid4().hex[:10]}"

    with sdk.run(
        goal=goal,
        agent_run_id=run_id,
        source=adapter_name if adapter_name != "generic" else "custom",
        auto_ingest=False,
        framework=adapter_name,
    ) as run:
        _attach_shared_evidence(
            run,
            action_log=action_log,
            authorization=authorization,
            confirmation_obtained=confirmation_obtained,
            autonomy_decision=autonomy_decision,
            gate_contract=gate_contract,
            identity=identity,
            web_base=web_base,
            git_ref=git_ref,
        )

        if adapter_name == "generic":
            adapter = GenericAdapter()
            adapter.bind(run)
            adapter.ingest_events(_tool_dicts(action_log))
            adapter.finish(agent_claim)
        elif adapter_name == "langgraph":
            adapter = LangGraphAdapter()
            adapter.bind(run)
            for ev in _langgraph_events(action_log):
                adapter.on_native_event(ev)
            adapter.finish({"content": agent_claim})
        elif adapter_name == "crewai":
            adapter = CrewAIAdapter()
            adapter.bind(run)
            adapter.from_kickoff(
                tool_calls=_tool_dicts(action_log),
                final_output=agent_claim,
            )
        elif adapter_name == "autogen":
            adapter = AutoGenAdapter()
            adapter.bind(run)
            adapter.ingest_messages(
                _autogen_messages(action_log, goal=goal, claim=agent_claim)
            )
        else:
            raise ValueError(f"unknown adapter: {adapter_name}")

        result = run.finish(outcome=outcome, claim=agent_claim, ingest=False)

    if not result.summary:
        raise RuntimeError(f"{adapter_name} adapter failed: {result.error}")

    data = result.summary.model_dump(mode="json")
    if identity:
        data["identity"] = {**(data.get("identity") or {}), **identity}
    if git_ref:
        data["git_ref"] = git_ref
    data["_emit_meta"] = {
        "adapter": adapter_name,
        "path": "framework_adapter",
    }
    return data


def emit_all_adapters(
    *,
    goal: str,
    action_log: ActionLog,
    agent_claim: str,
    adapters: tuple[AdapterName, ...] = ADAPTER_NAMES,
    **kwargs: Any,
) -> dict[AdapterName, dict[str, Any]]:
    out: dict[AdapterName, dict[str, Any]] = {}
    for name in adapters:
        out[name] = emit_via_adapter(
            name,
            goal=goal,
            action_log=action_log,
            agent_claim=agent_claim,
            **kwargs,
        )
    return out
