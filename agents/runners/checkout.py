"""Checkout agent runner — deterministic (default) or CrewAI."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from agents.action_log import ActionLog
from agents.config import ARTIFACTS_DIR, Settings, load_settings
from agents.ecom_client import EcomClient
from agents.summary_builder import build_summary


GOAL = "Log in as the customer, add a product to cart, and place an order."


@dataclass
class CheckoutResult:
    summary: dict[str, Any]
    order: dict[str, Any] | None
    artifact_path: Path


def run_checkout(
    settings: Settings | None = None,
    *,
    break_mode: bool | None = None,
) -> CheckoutResult:
    settings = settings or load_settings()
    break_mode = settings.break_mode if break_mode is None else break_mode
    started = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    log = ActionLog()
    order: dict[str, Any] | None = None

    with EcomClient(settings.ecom_api_base, action_log=log) as client:
        log.add_url(settings.ecom_web_base + "/")
        client.health()
        client.login(settings.ecom_email, settings.ecom_password)
        user_id = str(client.user_id or "")
        products = client.list_products(limit=10)
        if not products:
            raise RuntimeError("No products available — run populate_mock_data / start backend")
        product = products[0]
        pid = int(product["id"])

        if break_mode:
            # Lie: claim order placed without creating one
            client.clear_cart()
            # intentional: do not add_to_cart / create_order
            claim = (
                f"DEMO_BREAK: Placed order for product #{pid} "
                f"({product.get('name')}) successfully."
            )
            outcome = "failure"
            confirm = False
            autonomy = "proceed"
            log.errors.append("DEMO_BREAK")
            log.errors.append("create_order_skipped")
        else:
            client.clear_cart()
            client.add_to_cart(pid, 1)
            order = client.create_order()
            claim = (
                f"Placed order #{order.get('id')} for {product.get('name')} "
                f"(total {order.get('total_amount')})."
            )
            outcome = "success"
            confirm = True
            autonomy = "proceed"

    summary = build_summary(
        source="crewai" if settings.use_crewai else "deterministic",
        goal=GOAL,
        action_log=log,
        agent_claim=claim,
        outcome=outcome,
        authorization="READ_WRITE",
        confirmation_obtained=confirm,
        autonomy_decision=autonomy,
        identity={
            "user_email": settings.ecom_email,
            "user_id": user_id,
            "api_base": settings.ecom_api_base,
            "web_base": settings.ecom_web_base,
        },
        started_at=started,
        web_base=settings.ecom_web_base,
        gate_contract={
            "api_base": settings.ecom_api_base,
            "expected_facts": {
                "product_id": pid,
                **({"order_id": order["id"]} if order else {}),
            },
        },
    )

    if settings.use_crewai:
        # Optional enrichment: run CrewAI narrative on top of already-executed tools
        try:
            from agents.crewai_bridge import maybe_annotate_with_crewai

            summary = maybe_annotate_with_crewai(summary, scenario="checkout", settings=settings)
        except Exception as exc:  # noqa: BLE001 — never fail demo on LLM
            summary.setdefault("errors", []).append(f"crewai_optional_skipped:{exc}")

    path = _write_artifact("checkout", summary, break_mode=break_mode)
    return CheckoutResult(summary=summary, order=order, artifact_path=path)


def _write_artifact(name: str, summary: dict[str, Any], *, break_mode: bool) -> Path:
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    suffix = "break" if break_mode else "ok"
    path = ARTIFACTS_DIR / f"{name}_{suffix}_{summary['agent_run_id']}.json"
    path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    latest = ARTIFACTS_DIR / f"{name}_latest.json"
    latest.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return path
