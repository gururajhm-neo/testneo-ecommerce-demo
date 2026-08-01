# Demo walkthrough — Ecom + CrewAI/deterministic agents + TestNeo

**One repo. One story.** This app is the customer ecom. Agents call its APIs. TestNeo gates the run and optionally re-runs your product suite.

**Audience:** customer demos, internal FAANG-style release assurance.

**Runtime:** `AGENT_RUNTIME=deterministic` (default, reliable). Optional `crewai` narrator.

---

## Prerequisites (5 min)

| # | Check |
|---|--------|
| 1 | Ecom: `./start_all.sh` → UI http://127.0.0.1:3001 API http://127.0.0.1:9000/health |
| 2 | Login works: `john@test.com` / `john123` |
| 3 | TestNeo web API on `:8001`, UI on `:5173` |
| 4 | `cp agents/.env.example agents/.env` — set `TESTNEO_API_KEY`, `TESTNEO_PROJECT_ID` |
| 5 | Local Agent online if you want suite execution on agent |
| 6 | (Once) Tag 5–15 goldens: `agent-verification`, `agent-checkout`, `agent-refund` |

---

## Live script (~20 min)

### Act 0 — Product under test (2 min)

1. Open http://127.0.0.1:3001 — “this is the customer store.”
2. Show API docs http://127.0.0.1:9000/docs — cart, orders, refunds.

### Act 1 — Existing suite (3 min)

1. TestNeo → Test Runner → run a tagged checkout/API test.
2. Open **Running Executions** (`/test-runner/executions`) — live links.

*Say:* “Product suite already exists. Agents don’t replace it.”

### Act 2 — Good agent (5 min)

```bash
./agents/scripts/demo_e2e.sh
# or:
python -m agents.scripts.run_demo_e2e --scenario checkout --seed
```

1. Show `agents/artifacts/checkout_latest.json` — real `actions[]` against `/cart`, `/orders`.
2. Agent Verification UI → ingested run → **Post-agent gate** → PASS.
3. If suite mapped: open live execution links.

*Say:* “CrewAI-compatible agent used real ecom tools. Gate agrees.”

### Act 3 — Bad refund agent (5 min)

```bash
python -m agents.scripts.run_demo_e2e --scenario refund-break --seed --skip-suite
```

1. Summary retrieves `policy_refund_v1_expired`, `confirmation_obtained=false`.
2. Gate → Layer 4 **BLOCK** (forbidden doc / grounding / confirm).

*Say:* “Tools may succeed. Release still BLOCKs. Success ≠ correct.”

### Act 4 — Memory isolation (3 min)

```bash
python -m agents.scripts.run_demo_e2e --scenario memory --skip-suite
```

1. Agent claims order token from **another user’s** memory.
2. Layer 4 **BLOCK** on unexpected/forbidden user + token.

### Act 5 — Close (2 min)

1. One slide: **App suite + agent evidence + Layer 4 + optional PR risk**.
2. Optional: MCP `testneo_sync_code_structure` + PR validation on this repo.

---

## Expected outcomes cheat sheet

| Run | overall_gate (typical) |
|-----|------------------------|
| checkout-ok | PASS (or WARN if suite missing tags) |
| refund-break | **BLOCK** |
| memory-break | **BLOCK** |

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Ecom health fails | `./start_backend.sh` |
| No eligible refund order | `python -m agents.scripts.seed_demo_state` |
| Ingest 401 | Check `TESTNEO_API_KEY` / project ownership |
| Suite empty | Tag tests; set `SUITE_TAGS`; Local Agent online |
| Executions page empty | Use trailing `/executions/` API (fixed in TestNeo); hard-refresh |

---

## What we are / are not using

| Component | Choice |
|-----------|--------|
| Demo agent tools | Deterministic HTTP (default) + optional **CrewAI** narrator |
| Not used as customer agent | LangGraph (TestNeo may use LangGraph **internally** for NLP codegen) |
| Verification | TestNeo post-agent-gate (framework-agnostic) |

## Customer emit → push (share this)

How a real customer wires their agent to TestNeo (REST, MCP, n8n, curl, adapters):

**Canon doc (TestNeo monorepo):**  
`/home/gururaj/Documents/testneo-api/docs/product/AGENT_RUN_SUMMARY_INTEGRATION_BIBLE.md`

**Copy-paste sample:**  
`/home/gururaj/Documents/testneo-api/examples/agent-run-ingest-sample/`
