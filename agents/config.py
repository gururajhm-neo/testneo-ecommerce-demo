"""Central configuration for ecom CrewAI / deterministic agents + TestNeo gate.

Load order: process env → agents/.env → repo-root .env
Never commit secrets; use agents/.env.example as the template.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

AGENTS_ROOT = Path(__file__).resolve().parent
REPO_ROOT = AGENTS_ROOT.parent
ARTIFACTS_DIR = AGENTS_ROOT / "artifacts"
POLICIES_DIR = AGENTS_ROOT / "policies"

# Load env files without overriding an already-exported var
load_dotenv(REPO_ROOT / ".env", override=False)
load_dotenv(AGENTS_ROOT / ".env", override=False)


def _env(key: str, default: str | None = None) -> str | None:
    val = os.environ.get(key)
    if val is None or str(val).strip() == "":
        return default
    return str(val).strip()


def _env_bool(key: str, default: bool = False) -> bool:
    raw = _env(key)
    if raw is None:
        return default
    return raw.lower() in ("1", "true", "yes", "on")


def _env_int(key: str, default: int) -> int:
    raw = _env(key)
    if raw is None:
        return default
    return int(raw)


@dataclass(frozen=True)
class Settings:
    """Immutable settings snapshot for one agent/demo run."""

    # Ecom under test
    ecom_api_base: str = "http://127.0.0.1:9000"
    ecom_web_base: str = "http://127.0.0.1:3001"
    ecom_email: str = "john@test.com"
    ecom_password: str = "john123"
    # Second user for memory-isolation demos (seeded moderator — treat as "other")
    ecom_other_email: str = "moderator@ecommerce.com"
    ecom_other_password: str = "moderator123"

    # Agent runtime: deterministic (CI / reliable demo) | crewai (live LLM)
    agent_runtime: str = "deterministic"
    crew_demo_mode: str = "normal"  # normal | break
    crew_llm_model: str = "openai/llama-3.3-70b-versatile"
    groq_api_key: str | None = None
    openai_api_key: str | None = None

    # TestNeo
    testneo_base_url: str = "http://localhost:8001"
    testneo_web_app_url: str = "http://localhost:5173"
    testneo_api_key: str | None = None
    testneo_project_id: int = 0
    suite_tags: tuple[str, ...] = ("agent-verification", "agent-checkout", "agent-refund")
    suite_use_agent: bool = True
    suite_failure_blocks_gate: bool = False
    run_mapped_tests: bool = True
    queue_execution: bool = True
    wait_for_suite: bool = False

    @property
    def break_mode(self) -> bool:
        return self.crew_demo_mode.lower() == "break"

    @property
    def use_crewai(self) -> bool:
        return self.agent_runtime.lower() == "crewai"

    def require_testneo(self) -> None:
        if not self.testneo_api_key:
            raise RuntimeError(
                "TESTNEO_API_KEY is required. Copy agents/.env.example → agents/.env"
            )
        if not self.testneo_project_id:
            raise RuntimeError(
                "TESTNEO_PROJECT_ID is required (your TestNeo project for this ecom demo)."
            )


def load_settings() -> Settings:
    tags_raw = _env("SUITE_TAGS", "agent-verification,agent-checkout,agent-refund") or ""
    tags = tuple(t.strip() for t in tags_raw.split(",") if t.strip())
    return Settings(
        ecom_api_base=(_env("ECOM_API_BASE", "http://127.0.0.1:9000") or "").rstrip("/"),
        ecom_web_base=(_env("ECOM_WEB_BASE", "http://127.0.0.1:3001") or "").rstrip("/"),
        ecom_email=_env("ECOM_EMAIL", "john@test.com") or "john@test.com",
        ecom_password=_env("ECOM_PASSWORD", "john123") or "john123",
        ecom_other_email=_env("ECOM_OTHER_EMAIL", "moderator@ecommerce.com")
        or "moderator@ecommerce.com",
        ecom_other_password=_env("ECOM_OTHER_PASSWORD", "moderator123") or "moderator123",
        agent_runtime=_env("AGENT_RUNTIME", "deterministic") or "deterministic",
        crew_demo_mode=_env("CREW_DEMO_MODE", "normal") or "normal",
        crew_llm_model=_env("CREW_LLM_MODEL", "openai/llama-3.3-70b-versatile")
        or "openai/llama-3.3-70b-versatile",
        groq_api_key=_env("GROQ_API_KEY"),
        openai_api_key=_env("OPENAI_API_KEY"),
        testneo_base_url=(_env("TESTNEO_BASE_URL", "http://localhost:8001") or "").rstrip("/"),
        testneo_web_app_url=(
            _env("TESTNEO_WEB_APP_URL", "http://localhost:5173") or ""
        ).rstrip("/"),
        testneo_api_key=_env("TESTNEO_API_KEY"),
        testneo_project_id=_env_int("TESTNEO_PROJECT_ID", 0),
        suite_tags=tags or ("agent-verification",),
        suite_use_agent=_env_bool("SUITE_USE_AGENT", True),
        suite_failure_blocks_gate=_env_bool("SUITE_FAILURE_BLOCKS_GATE", False),
        run_mapped_tests=_env_bool("RUN_MAPPED_TESTS", True),
        queue_execution=_env_bool("QUEUE_EXECUTION", True),
        wait_for_suite=_env_bool("WAIT_FOR_SUITE", False),
    )
