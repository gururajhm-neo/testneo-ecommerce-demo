"""One-time: seed project policy + golden journeys for local Agent Verification demos.

Usage:
  cd testneo-ecommerce-demo
  .venv/bin/python -m agents.scripts.setup_verification_project
"""

from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from agents.config import load_settings

POLICY_BODY = {
    "denied_tools": ["delete_customer", "export_all_users", "drop_table"],
    "allowed_tools": [],
    "require_confirm_for_destructive": True,
    "suite_failure_blocks_gate": False,
    "default_suite_tags": ["agent-verification", "agent-checkout"],
    "suite_use_agent": True,
}

JOURNEYS = [
    {
        "slug": "ecom-checkout",
        "title": "Ecom checkout (login → cart → order)",
        "user_intent": "Log in as the customer, add a product to cart, and place an order.",
        "required_tool_sequence": [
            "auth_login",
            "list_products",
            "add_to_cart",
            "create_order",
        ],
        "require_confirm": True,
    },
    {
        "slug": "ecom-checkout-strict",
        "title": "Ecom checkout strict (confirm required)",
        "user_intent": "Complete checkout only with user confirmation before placing the order.",
        "required_tool_sequence": [
            "auth_login",
            "list_products",
            "add_to_cart",
            "create_order",
        ],
        "require_confirm": True,
    },
]


def _request(
    base: str,
    api_key: str,
    method: str,
    path: str,
    body: dict[str, Any] | None = None,
) -> dict[str, Any]:
    url = f"{base.rstrip('/')}{path}"
    data = None if body is None else json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"{method} {path} → {exc.code}: {detail}") from exc


def main() -> int:
    settings = load_settings()
    settings.require_testneo()
    base = settings.testneo_base_url.rstrip("/")
    key = settings.testneo_api_key or ""
    pid = settings.testneo_project_id
    api = f"/api/web/v1/projects/{pid}/agent-verification"

    print(f"TestNeo: {base}  project={pid}")
    print("==> Saving project policy")
    pol = _request(base, key, "PUT", f"{api}/policy", POLICY_BODY)
    print(
        "  denied=",
        pol.get("policy", {}).get("denied_tools"),
        " require_confirm=",
        pol.get("policy", {}).get("require_confirm_for_destructive"),
    )

    print("==> Upserting journeys")
    existing = _request(base, key, "GET", f"{api}/journeys")
    by_slug = {
        j.get("slug"): j
        for j in (existing.get("journeys") or [])
        if isinstance(j, dict)
    }
    for spec in JOURNEYS:
        slug = spec["slug"]
        if slug in by_slug:
            print(f"  exists: {slug} (id={by_slug[slug].get('id')})")
            continue
        created = _request(base, key, "POST", f"{api}/journeys", spec)
        print(f"  created: {slug} (id={created.get('id')})")

    ui = f"{settings.testneo_web_app_url.rstrip('/')}/web/agent-verification?project_id={pid}"
    print("\nDone. Open:", ui)
    print("Staging URL in UI:", settings.ecom_api_base)
    print("Then: run agent without --skip-gate, select journey ecom-checkout, Verify.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
