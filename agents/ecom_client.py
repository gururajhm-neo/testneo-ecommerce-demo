"""Typed HTTP client for the ecom FastAPI under test.

All agent tools go through this client so actions[], touched.api, and errors
are recorded consistently for AgentRunSummary emission.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Optional

import httpx

from agents.action_log import ActionLog


DEFAULT_SHIPPING = {
    "street": "100 Market Street",
    "city": "San Francisco",
    "state": "CA",
    "postal_code": "94105",
    "country": "US",
}


@dataclass
class EcomClient:
    base_url: str
    action_log: ActionLog = field(default_factory=ActionLog)
    timeout: float = 30.0
    _token: Optional[str] = field(default=None, repr=False)
    _user: dict[str, Any] = field(default_factory=dict, repr=False)
    _client: httpx.Client = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self._client = httpx.Client(base_url=self.base_url.rstrip("/"), timeout=self.timeout)

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> "EcomClient":
        return self

    def __exit__(self, *exc: Any) -> None:
        self.close()

    @property
    def user_id(self) -> Optional[int]:
        uid = self._user.get("id")
        return int(uid) if uid is not None else None

    @property
    def headers(self) -> dict[str, str]:
        if not self._token:
            return {"Content-Type": "application/json"}
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._token}",
        }

    def _request(
        self,
        method: str,
        path: str,
        *,
        tool: str,
        operation: str = "EXECUTE",
        json_body: Any = None,
        auth: bool = True,
    ) -> Any:
        headers = self.headers if auth else {"Content-Type": "application/json"}
        if not auth:
            headers = {"Content-Type": "application/json"}
        elif self._token:
            headers = self.headers
        else:
            headers = {"Content-Type": "application/json"}

        url_path = path if path.startswith("/") else f"/{path}"
        try:
            resp = self._client.request(
                method.upper(),
                url_path,
                headers=headers,
                json=json_body,
            )
            detail = None
            try:
                payload = resp.json() if resp.content else None
            except Exception:
                payload = {"raw": resp.text[:500]}
            if resp.is_success:
                summary = _short(payload)
                # Persist bearer for TestNeo prove-after-write on later authenticated GETs
                if tool == "auth_login" and isinstance(payload, dict) and payload.get("access_token"):
                    summary = f"access_token={payload['access_token']} keys={list(payload.keys())[:8]}"
                self.action_log.record(
                    tool=tool,
                    operation=operation,
                    target=url_path,
                    result="SUCCESS",
                    arguments=json_body if isinstance(json_body, dict) else {"body": json_body},
                    result_summary=summary,
                    api={"method": method.upper(), "path": url_path, "status": resp.status_code},
                )
                return payload
            detail = payload.get("detail") if isinstance(payload, dict) else resp.text
            self.action_log.record(
                tool=tool,
                operation=operation,
                target=url_path,
                result="FAILURE",
                arguments=json_body if isinstance(json_body, dict) else {"body": json_body},
                result_summary=str(detail)[:400],
                api={"method": method.upper(), "path": url_path, "status": resp.status_code},
                error=f"HTTP {resp.status_code}: {detail}",
            )
            raise EcomApiError(resp.status_code, str(detail), path=url_path)
        except EcomApiError:
            raise
        except Exception as exc:
            self.action_log.record(
                tool=tool,
                operation=operation,
                target=url_path,
                result="FAILURE",
                arguments=json_body if isinstance(json_body, dict) else {},
                result_summary=str(exc)[:400],
                api={"method": method.upper(), "path": url_path, "status": 0},
                error=str(exc),
            )
            raise

    def health(self) -> Any:
        return self._request("GET", "/health", tool="health_check", operation="READ", auth=False)

    def login(self, email: str, password: str) -> dict[str, Any]:
        data = self._request(
            "POST",
            "/auth/login",
            tool="auth_login",
            operation="EXECUTE",
            json_body={"email": email, "password": password},
            auth=False,
        )
        self._token = data["access_token"]
        self._user = data.get("user") or {}
        return data

    def list_products(self, limit: int = 20) -> list[dict[str, Any]]:
        data = self._request(
            "GET",
            f"/products?limit={limit}",
            tool="list_products",
            operation="READ",
            auth=False,
        )
        if isinstance(data, dict):
            return list(data.get("products") or data.get("items") or [])
        return list(data or [])

    def clear_cart(self) -> None:
        try:
            self._request("DELETE", "/cart", tool="clear_cart", operation="DELETE")
        except EcomApiError:
            # empty cart is fine
            pass

    def add_to_cart(self, product_id: int, quantity: int = 1) -> Any:
        return self._request(
            "POST",
            "/cart",
            tool="add_to_cart",
            operation="WRITE",
            json_body={"product_id": product_id, "quantity": quantity},
        )

    def get_cart(self) -> dict[str, Any]:
        data = self._request("GET", "/cart", tool="get_cart", operation="READ")
        return data if isinstance(data, dict) else {"items": data}

    def create_order(
        self,
        *,
        shipping_address: dict[str, Any] | None = None,
        payment_method: str = "credit_card",
        shipping_method: str = "standard",
    ) -> dict[str, Any]:
        cart = self.get_cart()
        items = cart.get("items") or []
        if not items:
            raise EcomApiError(400, "Cart is empty", path="/orders")
        order_items = [
            {
                "product_id": int(it["product_id"]),
                "quantity": int(it["quantity"]),
                "selected_options": it.get("selected_options"),
            }
            for it in items
        ]
        body = {
            "items": order_items,
            "payment_method": payment_method,
            "shipping_method": shipping_method,
            "shipping_address": shipping_address or DEFAULT_SHIPPING,
            "billing_address": shipping_address or DEFAULT_SHIPPING,
            "customer_notes": "agent-demo order",
        }
        return self._request(
            "POST",
            "/orders",
            tool="create_order",
            operation="WRITE",
            json_body=body,
        )

    def list_orders(self, limit: int = 20) -> list[dict[str, Any]]:
        data = self._request(
            "GET",
            f"/orders?limit={limit}",
            tool="list_orders",
            operation="READ",
        )
        return list(data or [])

    def get_order(self, order_id: int) -> dict[str, Any]:
        return self._request(
            "GET",
            f"/orders/{order_id}",
            tool="get_order",
            operation="READ",
        )

    def create_refund(
        self,
        order_id: int,
        amount: float,
        reason: str = "customer_change_mind",
        description: str | None = None,
    ) -> dict[str, Any]:
        return self._request(
            "POST",
            "/refunds",
            tool="create_refund",
            operation="WRITE",
            json_body={
                "order_id": order_id,
                "amount": amount,
                "reason": reason,
                "description": description or "Agent-requested refund",
            },
        )

    def me(self) -> dict[str, Any]:
        return self._request("GET", "/users/me", tool="get_profile", operation="READ")


class EcomApiError(RuntimeError):
    def __init__(self, status_code: int, detail: str, *, path: str = "") -> None:
        self.status_code = status_code
        self.detail = detail
        self.path = path
        super().__init__(f"Ecom API {status_code} {path}: {detail}")


def _short(payload: Any, n: int = 240) -> str:
    if payload is None:
        return "ok"
    if isinstance(payload, dict):
        keys = list(payload.keys())[:8]
        if "id" in payload:
            return f"id={payload.get('id')} keys={keys}"
        return f"keys={keys}"
    if isinstance(payload, list):
        return f"list[{len(payload)}]"
    return str(payload)[:n]
