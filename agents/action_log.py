"""Ordered action / API / error ledger used to emit agent_run_summary.v1."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ActionLog:
    actions: list[dict[str, Any]] = field(default_factory=list)
    api_calls: list[dict[str, Any]] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    urls: list[str] = field(default_factory=list)
    retrieved: list[dict[str, Any]] = field(default_factory=list)
    memory_accesses: list[dict[str, Any]] = field(default_factory=list)
    _seq: int = 0

    def record(
        self,
        *,
        tool: str,
        operation: str = "EXECUTE",
        target: str | None = None,
        result: str = "SUCCESS",
        arguments: dict[str, Any] | None = None,
        result_summary: str | None = None,
        api: dict[str, Any] | None = None,
        error: str | None = None,
    ) -> None:
        self._seq += 1
        self.actions.append(
            {
                "sequence": self._seq,
                "tool": tool,
                "operation": operation,
                "target": target,
                "result": result,
                "arguments": dict(arguments or {}),
                "result_summary": result_summary,
            }
        )
        if api:
            self.api_calls.append(dict(api))
        if error:
            self.errors.append(error)

    def add_url(self, url: str) -> None:
        if url and url not in self.urls:
            self.urls.append(url)

    def add_retrieved(self, hit: dict[str, Any]) -> None:
        self.retrieved.append(hit)

    def add_memory(self, access: dict[str, Any]) -> None:
        self.memory_accesses.append(access)

    @property
    def tools(self) -> list[str]:
        names: list[str] = []
        for a in self.actions:
            t = a.get("tool")
            if t and t not in names:
                names.append(str(t))
        return names

    @property
    def final_action(self) -> str | None:
        if not self.actions:
            return None
        return str(self.actions[-1].get("tool"))
