"""Build agent_run_summary.v1 payloads (framework-agnostic contract for TestNeo)."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any

from agents.action_log import ActionLog

CONTRACT = "agent_run_summary.v1"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def build_summary(
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
    """Emit a validated-shape summary dict (no pydantic dependency on TestNeo)."""
    if outcome not in ("success", "failure", "unknown"):
        outcome = "unknown"
    urls = list(action_log.urls)
    if web_base and web_base not in urls:
        urls.insert(0, web_base.rstrip("/") + "/")

    summary: dict[str, Any] = {
        "contract_version": CONTRACT,
        "source": source,
        "agent_run_id": agent_run_id or f"ecom-{uuid.uuid4().hex[:12]}",
        "goal": goal,
        "outcome": outcome,
        "agent_claim": agent_claim,
        "touched": {
            "urls": urls,
            "api": list(action_log.api_calls),
            "tools": action_log.tools,
            "ui_actions": [],
        },
        "actions": list(action_log.actions),
        "retrieved": list(action_log.retrieved),
        "memory_accesses": list(action_log.memory_accesses),
        "errors": list(action_log.errors),
        "started_at": started_at or _now(),
        "ended_at": ended_at or _now(),
        "authorization": authorization,
        "confirmation_obtained": bool(confirmation_obtained),
        "autonomy_decision": autonomy_decision,
        "final_action": action_log.final_action,
        "output": output or agent_claim,
    }
    if identity:
        summary["identity"] = identity
    if gate_contract:
        summary["gate_contract"] = gate_contract
    return summary
