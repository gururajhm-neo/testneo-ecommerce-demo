"""Optional CrewAI annotation layer.

Deterministic runners execute real ecom tools (reliable demos / CI).
When AGENT_RUNTIME=crewai, we optionally ask CrewAI to produce a short
narrative over the already-recorded tool trace — without re-calling tools.
"""

from __future__ import annotations

from typing import Any

from agents.config import Settings


def maybe_annotate_with_crewai(
    summary: dict[str, Any],
    *,
    scenario: str,
    settings: Settings,
) -> dict[str, Any]:
    if not settings.use_crewai:
        return summary
    if not (settings.groq_api_key or settings.openai_api_key):
        summary.setdefault("errors", []).append("crewai_skipped:no_llm_key")
        return summary

    try:
        from crewai import Agent, Crew, LLM, Process, Task
    except ImportError:
        summary.setdefault("errors", []).append("crewai_skipped:not_installed")
        return summary

    # Prefer Groq OpenAI-compatible endpoint (same pattern as demo-agent-checkout)
    if settings.groq_api_key:
        llm = LLM(
            model=settings.crew_llm_model,
            base_url="https://api.groq.com/openai/v1",
            api_key=settings.groq_api_key,
            temperature=0.2,
        )
    else:
        llm = LLM(model="gpt-4o-mini", api_key=settings.openai_api_key, temperature=0.2)

    agent = Agent(
        role="E-commerce assistant narrator",
        goal=f"Summarize the {scenario} tool trace honestly for QA",
        backstory="You narrate what tools already did; you never invent tool results.",
        llm=llm,
        verbose=False,
        allow_delegation=False,
    )
    tools_blob = ", ".join(summary.get("touched", {}).get("tools") or [])
    claim = summary.get("agent_claim") or ""
    task = Task(
        description=(
            f"Scenario={scenario}. Tools already executed: {tools_blob}. "
            f"Existing claim: {claim}. "
            "Reply with one short sentence confirming what happened. "
            "Do not invent new orders or refunds."
        ),
        expected_output="One honest sentence.",
        agent=agent,
    )
    crew = Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=False)
    out = crew.kickoff()
    text = str(out).strip()
    summary["source"] = "crewai"
    summary["output"] = text[:2000]
    # Keep original agent_claim (gate contracts depend on it); attach narrative
    summary.setdefault("errors", [])
    return summary
