"""TestNeo REST client: ingest + post-agent-gate + suite refresh."""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

from agents.config import Settings


class TestNeoClient:
    def __init__(self, settings: Settings) -> None:
        settings.require_testneo()
        self.settings = settings
        self.base = settings.testneo_base_url.rstrip("/")
        self.web = settings.testneo_web_app_url.rstrip("/")
        self.api_key = settings.testneo_api_key or ""
        self.project_id = settings.testneo_project_id

    def _request(
        self,
        method: str,
        path: str,
        *,
        body: dict[str, Any] | None = None,
        timeout: int = 180,
    ) -> Any:
        url = f"{self.base}{path}"
        data = None if body is None else json.dumps(body).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data,
            method=method,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "User-Agent": "testneo-ecommerce-agents/1.0",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                raw = resp.read().decode("utf-8")
                return json.loads(raw) if raw else {}
        except urllib.error.HTTPError as e:
            err = e.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"HTTP {e.code} {path}: {err[:1000]}") from e

    def ingest_agent_run(
        self,
        summary: dict[str, Any],
        *,
        auto_verify: bool = False,
    ) -> dict[str, Any]:
        return self._request(
            "POST",
            f"/api/web/v1/projects/{self.project_id}/unified-contexts/ingest/agent-run",
            body={"summary": summary, "auto_verify": auto_verify},
        )

    def post_agent_gate(
        self,
        *,
        context_id: int | None = None,
        run_layer4: bool = True,
        run_mapped_tests: bool | None = None,
        queue_execution: bool | None = None,
        wait_for_suite: bool | None = None,
        test_tags: list[str] | None = None,
        generate_tests: bool = False,
        suite_use_agent: bool | None = None,
        suite_failure_blocks_gate: bool | None = None,
    ) -> dict[str, Any]:
        s = self.settings
        body: dict[str, Any] = {
            "run_layer4": run_layer4,
            "generate_tests": generate_tests,
            "run_mapped_tests": (
                s.run_mapped_tests if run_mapped_tests is None else run_mapped_tests
            ),
            "queue_execution": (
                s.queue_execution if queue_execution is None else queue_execution
            ),
            "wait_for_suite": (
                s.wait_for_suite if wait_for_suite is None else wait_for_suite
            ),
            "test_tags": test_tags or list(s.suite_tags),
            "suite_use_agent": (
                s.suite_use_agent if suite_use_agent is None else suite_use_agent
            ),
            "suite_failure_blocks_gate": (
                s.suite_failure_blocks_gate
                if suite_failure_blocks_gate is None
                else suite_failure_blocks_gate
            ),
        }
        if context_id is not None:
            body["context_id"] = context_id
        return self._request(
            "POST",
            f"/api/web/v1/projects/{self.project_id}/agent-verification/post-agent-gate",
            body=body,
            timeout=300,
        )

    def refresh_suite(self, gate_verification_id: str) -> dict[str, Any]:
        return self._request(
            "POST",
            f"/api/web/v1/projects/{self.project_id}/agent-verification/refresh-suite",
            body={"gate_verification_id": gate_verification_id},
        )

    def list_ingested_runs(self) -> list[dict[str, Any]]:
        data = self._request(
            "GET",
            f"/api/web/v1/projects/{self.project_id}/agent-verification/ingested-runs",
        )
        if isinstance(data, list):
            return data
        return list(data.get("runs") or data.get("items") or [])

    def execution_url(self, execution_id: str) -> str:
        return f"{self.web}/test-runner/execution/{urllib.parse.quote(execution_id, safe='')}"

    def executions_list_url(self) -> str:
        return f"{self.web}/test-runner/executions"

    def agent_verification_url(self) -> str:
        return f"{self.web}/web/agent-verification?project_id={self.project_id}"

    def poll_suite(
        self,
        gate_verification_id: str,
        *,
        max_attempts: int = 40,
        interval_s: float = 5.0,
    ) -> dict[str, Any]:
        last: dict[str, Any] = {}
        for _ in range(max_attempts):
            last = self.refresh_suite(gate_verification_id)
            exec_block = last.get("execution") or {}
            if exec_block.get("suite_finished") or exec_block.get("status") in (
                "completed",
                "failed",
                "cancelled",
            ):
                return last
            time.sleep(interval_s)
        return last
