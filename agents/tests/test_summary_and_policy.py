"""Unit tests for summary + policy KB (no live ecom/TestNeo required)."""

from __future__ import annotations

from agents.action_log import ActionLog
from agents.policy_kb import search_policy
from agents.summary_builder import build_summary


def test_build_summary_shape():
    log = ActionLog()
    log.record(tool="auth_login", operation="EXECUTE", result="SUCCESS")
    log.add_retrieved({"doc_id": "policy_refund_v2", "snippet": "30 days"})
    s = build_summary(
        source="deterministic",
        goal="g",
        action_log=log,
        agent_claim="ok",
        outcome="success",
        confirmation_obtained=True,
    )
    assert s["contract_version"] == "agent_run_summary.v1"
    assert s["actions"][0]["tool"] == "auth_login"
    assert s["retrieved"][0]["doc_id"] == "policy_refund_v2"
    assert s["confirmation_obtained"] is True


def test_policy_prefer_expired():
    hit = search_policy("refund", prefer_expired=True)
    assert hit["doc_id"] == "policy_refund_v1_expired"
    hit2 = search_policy("refund within 30 days", prefer_expired=False)
    assert hit2["doc_id"] == "policy_refund_v2"
