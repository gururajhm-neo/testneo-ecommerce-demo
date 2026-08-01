# Ecom Agents + TestNeo Agent Verification

**Claim:** Agent tool success ≠ release readiness. This package runs real agents against
**this** ecom app, emits `agent_run_summary.v1`, and gates via TestNeo.

| Runtime | When |
|---------|------|
| **deterministic** (default) | Reliable demos / CI — scripted tool sequences against `:9000` |
| **crewai** | Optional LLM narrator (`AGENT_RUNTIME=crewai` + Groq/OpenAI key) |

Framework for verification is **CrewAI-compatible**; default path does not require an LLM.

## Quick start

```bash
# 1) Ecom up
./start_all.sh

# 2) Configure TestNeo
cp agents/.env.example agents/.env
# set TESTNEO_API_KEY + TESTNEO_PROJECT_ID

# 3) One-button demo
chmod +x agents/scripts/demo_e2e.sh
./agents/scripts/demo_e2e.sh
```

## Scenarios

| Scenario | Expected gate signal |
|----------|----------------------|
| Checkout OK | PASS (behavior + Layer4) |
| Refund BREAK (expired policy, no confirm) | Layer4 **BLOCK** |
| Memory BREAK (cross-user token) | Layer4 **BLOCK** |

## Commands

```bash
# Seed a delivered order for refund demos
python -m agents.scripts.seed_demo_state

# Individual runs
python -m agents.scripts.run_demo_e2e --scenario checkout --skip-gate
python -m agents.scripts.run_demo_e2e --scenario refund-break
python -m agents.scripts.run_demo_e2e --scenario memory --skip-suite

# Unit tests (no servers)
pytest agents/tests -q
```

## TestNeo project prep (once)

1. Environment `base_url` → `http://127.0.0.1:3001` (web) / API tests → `:9000`
2. Tag golden NLP/API cases: `agent-verification`, `agent-checkout`, `agent-refund`
3. Policy: require confirmation for refunds; optional journey `auth → get_order → confirm → refund`
4. Open UI: `/web/agent-verification?project_id=<id>`

## Layout

```text
agents/
  config.py              # env
  ecom_client.py         # HTTP tools + action log
  summary_builder.py     # agent_run_summary.v1
  testneo_client.py      # ingest + post-agent-gate
  policy_kb.py           # local RAG docs
  runners/               # checkout / refund / memory
  scripts/demo_e2e.sh    # one button
  policies/              # refund_v2 + expired v1
  artifacts/             # last summaries + gates
```

See **[DEMO_LOCAL_AGENT_VERIFICATION.md](./DEMO_LOCAL_AGENT_VERIFICATION.md)** — intern/customer **bible** (agents, policy/journey/golden, Edit contracts, golden policies, paste JSON, product suite, **Release Intelligence closed loop**).
See [DEMO_WALKTHROUGH.md](../DEMO_WALKTHROUGH.md) for the older live script.
