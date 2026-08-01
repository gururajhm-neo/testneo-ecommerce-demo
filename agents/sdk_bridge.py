"""Emit agent_run_summary.v1 via the official TestNeo Agent SDK.

Replays the ecom ActionLog into TestNeoRun events so customers see the same
path LangGraph/CrewAI adapters will use — without changing the verification engine.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

# Prefer editable install; fall back to monorepo packages/ path.
_SDK_SRC = Path(__file__).resolve().parents[2] / "testneo-api" / "packages" / "testneo-agent-sdk" / "src"
# Sibling layout: Documents/testneo-api next to Documents/testneo-ecommerce-demo
_SDK_SRC_ALT = Path(__file__).resolve().parents[2].parent / "testneo-api" / "packages" / "testneo-agent-sdk" / "src"
for _p in (_SDK_SRC_ALT, _SDK_SRC):
    if _p.is_dir() and str(_p) not in sys.path:
        sys.path.insert(0, str(_p))
        break

from agents.action_log import ActionLog  # noqa: E402


def sdk_available() -> bool:
    try:
        import testneo_agent  # noqa: F401

        return True
    except ImportError:
        return False


def build_summary_via_sdk(
    *,
    source: str,
    goal: str,
    action_log: ActionLog,
    agent_claim: str,
    outcome: str = "success",
    authorization: str = "READ_WRITE",
    confirmation_obtained: bool = False,
    autonomy_decision: str = "proceed",
    agent_run_id: str | None = None,
    gate_contract: dict[str, Any] | None = None,
    identity: dict[str, Any] | None = None,
    output: str | None = None,
    started_at: str | None = None,
    ended_at: str | None = None,
    web_base: str | None = None,
) -> dict[str, Any]:
    """Replay ActionLog → TestNeo SDK → summary dict (no ingest)."""
    import uuid

    from testneo_agent import Config, TestNeo

    cfg = Config(auto_ingest=False, strict=False, agent_name="ecom-demo-agent")
    sdk = TestNeo(cfg)
    run_id = agent_run_id or f"ecom-{uuid.uuid4().hex[:12]}"
    with sdk.run(
        goal=goal,
        agent_run_id=run_id,
        source=source,
        auto_ingest=False,
        framework=source,
    ) as run:
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
                    payload={"identity": dict(identity), "source": source},
                )
            )

        for api in action_log.api_calls:
            run.observe_api(
                str(api.get("method") or "GET"),
                str(api.get("path") or "/"),
                status=api.get("status"),
                url=web_base,
            )
        for url in action_log.urls:
            run.observe_api("GET", "/", url=url)

        # Prefer explicit retrieved[] (avoid double search_policy action if already in actions)
        retrieved_ids = {str(r.get("doc_id")) for r in action_log.retrieved if r.get("doc_id")}
        for hit in action_log.retrieved:
            if not hit.get("doc_id"):
                continue
            run.retrieval(
                doc_id=str(hit["doc_id"]),
                snippet=hit.get("snippet") or hit.get("text"),
                score=hit.get("score"),
                chunk_id=hit.get("chunk_id"),
                source=hit.get("source"),
                query=(hit.get("metadata") or {}).get("query") if isinstance(hit.get("metadata"), dict) else None,
                metadata=dict(hit.get("metadata") or {}),
                emit_action=False,  # actions already recorded below
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

        for action in action_log.actions:
            tool = str(action.get("tool") or "")
            # Skip synthetic duplicate if we already emitted retrieval for same doc as tool target
            # Keep all real tools including search_policy_kb from the agent.
            call_id = run.tool_called(
                tool,
                operation=str(action.get("operation") or "EXECUTE"),
                target=action.get("target"),
                arguments=dict(action.get("arguments") or {}),
                sequence=action.get("sequence"),
            )
            result = str(action.get("result") or "SUCCESS").upper()
            if result == "FAILURE":
                run.tool_failed(
                    tool,
                    call_id=call_id,
                    error=action.get("result_summary"),
                )
            else:
                run.tool_completed(
                    tool,
                    call_id=call_id,
                    operation=action.get("operation"),
                    target=action.get("target"),
                    arguments=dict(action.get("arguments") or {}),
                    result=result if result in ("SUCCESS", "UNKNOWN") else "SUCCESS",
                    result_summary=action.get("result_summary"),
                    sequence=action.get("sequence"),
                )

        for err in action_log.errors:
            from testneo_agent.events import EventType, InternalEvent

            run.emit(
                InternalEvent(
                    type=EventType.ERROR,
                    run_id=run.agent_run_id,
                    payload={"message": str(err)},
                )
            )

        if gate_contract:
            run.set_gate_contract(gate_contract)
        run.set_claim(agent_claim)
        result = run.finish(outcome=outcome, claim=agent_claim, ingest=False)

    if not result.summary:
        raise RuntimeError(f"SDK failed to build summary: {result.error}")

    data = result.summary.model_dump(mode="json")
    if output:
        data["output"] = output
    if started_at:
        data["started_at"] = started_at
    if ended_at:
        data["ended_at"] = ended_at
    # Preserve identity email etc.
    if identity:
        data["identity"] = {
            **(data.get("identity") or {}),
            **identity,
        }
    # Ensure retrieved present even if empty actions path
    if retrieved_ids and not data.get("retrieved"):
        data["retrieved"] = list(action_log.retrieved)
    return data
