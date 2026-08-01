"""Seed cart + delivered order so refund / checkout demos are deterministic."""

from __future__ import annotations

import sys
from pathlib import Path

# Allow `python -m agents.scripts.seed_demo_state` from repo root
REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from agents.config import load_settings
from agents.ecom_client import EcomClient, EcomApiError


def mark_order_delivered(order_id: int) -> None:
    """Update SQLite order status via SQLAlchemy models (admin-equivalent)."""
    sys.path.insert(0, str(REPO_ROOT))
    from database import SessionLocal  # type: ignore
    from models.order import Order, OrderStatus  # type: ignore

    db = SessionLocal()
    try:
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise RuntimeError(f"Order {order_id} not found in DB")
        order.status = OrderStatus.DELIVERED
        db.commit()
        print(f"Marked order #{order_id} as delivered")
    finally:
        db.close()


def main() -> int:
    settings = load_settings()
    print(f"Seeding against {settings.ecom_api_base} as {settings.ecom_email}")
    with EcomClient(settings.ecom_api_base) as client:
        try:
            client.health()
        except Exception as exc:
            print(f"ERROR: ecom API not reachable: {exc}")
            print("Start backend: ./start_backend.sh")
            return 1
        client.login(settings.ecom_email, settings.ecom_password)
        products = client.list_products()
        if not products:
            print("ERROR: no products — run populate_mock_data.py")
            return 1
        pid = int(products[0]["id"])
        client.clear_cart()
        client.add_to_cart(pid, 1)
        try:
            order = client.create_order()
        except EcomApiError as exc:
            print(f"ERROR creating order: {exc}")
            return 1
        oid = int(order["id"])
        print(f"Created order #{oid} total={order.get('total_amount')}")
    mark_order_delivered(oid)
    print("Seed complete — refund demos can use this delivered order.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
