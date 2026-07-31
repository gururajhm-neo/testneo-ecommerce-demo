"""Local policy knowledge base (simulates the agent's RAG — not TestNeo's vector DB)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from agents.config import POLICIES_DIR


@dataclass(frozen=True)
class PolicyDoc:
    doc_id: str
    title: str
    path: Path

    def read(self) -> str:
        return self.path.read_text(encoding="utf-8")


DOCS = {
    "policy_refund_v2": PolicyDoc(
        doc_id="policy_refund_v2",
        title="Refund policy v2",
        path=POLICIES_DIR / "refund_v2.md",
    ),
    "policy_refund_v1_expired": PolicyDoc(
        doc_id="policy_refund_v1_expired",
        title="Refund policy v1 (expired)",
        path=POLICIES_DIR / "refund_v1_expired.md",
    ),
}


def search_policy(query: str, *, prefer_expired: bool = False) -> dict[str, Any]:
    """Deterministic 'retrieval' for demos.

    prefer_expired=True simulates a bad RAG hit (Layer 4 should BLOCK when
    gate contracts forbid expired docs / require v2 grounding).
    """
    q = (query or "").lower()
    if prefer_expired or "expired" in q or "v1" in q:
        doc = DOCS["policy_refund_v1_expired"]
        score = 0.91
    else:
        doc = DOCS["policy_refund_v2"]
        score = 0.88
    body = doc.read()
    snippet = body.strip().split("\n\n")[0][:400]
    return {
        "doc_id": doc.doc_id,
        "chunk_id": "c1",
        "source": str(doc.path.name),
        "score": score,
        "snippet": snippet,
        "metadata": {"title": doc.title, "query": query},
    }
