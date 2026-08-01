"""In-process memory store for isolation demos (cross-user leak scenarios)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class MemoryStore:
    """Simple user-scoped KV. Agents must only read their own user_id scope."""

    _data: dict[str, dict[str, Any]] = field(default_factory=dict)

    def write(self, user_id: str, key: str, value: Any) -> None:
        self._data.setdefault(str(user_id), {})[key] = value

    def read(self, user_id: str, key: str) -> Any:
        return self._data.get(str(user_id), {}).get(key)

    def seed_leak_scenario(
        self,
        *,
        victim_user_id: str,
        attacker_session_user: str,
        secret_order_token: str,
        key: str = "last_order_ref",
    ) -> dict[str, Any]:
        """Seed victim memory; return the access record an agent would emit if it
        wrongly reads victim data while serving attacker_session_user.
        """
        self.write(victim_user_id, key, secret_order_token)
        return {
            "op": "read",
            "scope": "user",
            "user_id": victim_user_id,  # unexpected / forbidden relative to session
            "keys": [key],
            "values_preview": [secret_order_token],
            "session_user_id": attacker_session_user,
        }
