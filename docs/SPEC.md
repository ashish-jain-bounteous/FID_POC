# Jarvis — Data Engineering Agentic Delivery Framework

**Status:** DRAFT — awaiting human approval
**Source of agents:** `agents.json` (Sheet3 of *Fid Data GenAI usecases.xlsx*)
**Date:** 2026-06-10

---

## 1. Purpose

Build a **Claude Code–native** agentic framework that takes a Jira ticket
(defect or feature) for a Snowflake data platform and drives it through a
delivery pipeline of specialized agents — from triage to design, build, test,
quality, and governance — coordinated by a master orchestrator named **Jarvis**.

This iteration delivers:

1. A **fully implemented Triage Agent** (per its `agents.json` description).
2. **Structured-stub placeholders** for the other 17 agents.
3. A **Jarvis orchestrator** that routes a ticket through the pipeline.
4. **Hooks** that enforce simple SQL/code standards after agents run.
5. **Hard-coded Snowflake star-schema models** and **mock Jira tickets** as the
   working data the agents operate on.

---

## 2. Confirmed decisions (from requirements Q&A)

| Decision | Choice |
|----------|--------|
| Runtime | **Claude Code native** — `.claude/agents`, `.claude/skills`, hooks in `settings.json` |
| Orchestration | **Master orchestrator (Jarvis)** routes the pipeline |
| Triage input source | **Mock Jira tickets as local JSON** (`tickets/*.json`) |
| Snowflake models | **Small star schema** (Fidelity/finance trades domain) |
| Hooks | **SQL/code standards** enforcement (PostToolUse on Write/Edit) |
| Triage output | **Full analysis + routing** (verdict, impacted objects, recommended agents, writes back to ticket) |
| Placeholders | **Structured stubs** (full frontmatter + role/inputs/outputs + TODO body) |

---

## 3. Directory layout (to be created)

```
new_agents_fidelity/
├── agents.json                       # existing — source of truth for agent list
├── docs/
│   └── SPEC.md                       # this file
├── .claude/
│   ├── settings.json                 # registers the SQL/code-standards hook
│   ├── agents/                       # 18 sub-agents (1 built, 17 stubs) + jarvis
│   │   ├── triage-agent.md           # FULLY IMPLEMENTED
│   │   ├── design-agent.md           # stub
│   │   ├── data-product-agent.md     # stub
│   │   ├── data-modelling-agent.md   # stub
│   │   ├── lineage-agent.md          # stub
│   │   ├── impact-analysis-agent.md  # stub
│   │   ├── sql-agent.md              # stub
│   │   ├── python-agent.md           # stub
│   │   ├── stored-proc-agent.md      # stub
│   │   ├── scheduler-agent.md        # stub
│   │   ├── code-refactor-agent.md    # stub
│   │   ├── unit-test-agent.md        # stub
│   │   ├── regression-test-agent.md  # stub
│   │   ├── sql-optimizer-agent.md    # stub
│   │   ├── sonar-remediation-agent.md# stub
│   │   ├── code-quality-agent.md     # stub
│   │   ├── code-review-agent.md      # stub
│   │   └── governance-security-agent.md # stub
│   ├── skills/
│   │   └── jarvis/
│   │       └── SKILL.md              # /jarvis orchestrator (drives the pipeline)
│   └── hooks/
│       └── sql_standards.py          # PostToolUse standards checker
├── snowflake/                        # hard-coded models the agents operate on
│   ├── ddl/
│   │   ├── dim_account.sql
│   │   ├── dim_security.sql
│   │   ├── dim_date.sql
│   │   └── fct_trades.sql
│   ├── procs/
│   │   └── load_fct_trades.sql
│   └── views/
│       └── vw_daily_positions.sql
├── tickets/                          # mock Jira (Triage input/output)
│   ├── PROJ-101.json                 # a DEFECT (issue) example
│   └── PROJ-102.json                 # a FEATURE example
└── runtime/
    └── pipeline-runlog.jsonl         # created at run time (audit of agent runs)
```

---

## 4. Agent roster & persona mapping

All 18 agents from `agents.json`, grouped by the pipeline stage Jarvis uses:

| Stage | Agent | Persona | Status |
|-------|-------|---------|--------|
| 0 · Intake | **Triage Agent** | Product Owner | **Built** |
| 1 · Analysis | Design Agent | Product Owner | stub |
| 1 · Analysis | Data Product Agent | Product Owner | stub |
| 1 · Analysis | Lineage Agent | Product Owner | stub |
| 1 · Analysis | Impact Analysis Agent | Product Owner | stub |
| 1 · Analysis | Data modelling Agent | Data modeller | stub |
| 2 · Build | SQL Agent | Data Engineer | stub |
| 2 · Build | Python Agent | Data Engineer | stub |
| 2 · Build | Stored Proc Agent | Data Engineer | stub |
| 2 · Build | Scheduler Agent | Data Engineer | stub |
| 2 · Build | Code Refactor Agent | Data Engineer | stub |
| 3 · Test | Unit Test Agent | Test Engineer | stub |
| 3 · Test | Regression Test Agent | Test Engineer | stub |
| 4 · Quality/FinOps | SQL Optimizer Agent | Finops & Devops | stub |
| 4 · Quality/FinOps | Sonar Remediation Agent | Finops & Devops | stub |
| 4 · Quality/FinOps | Code Quality Agent | Finops & Devops | stub |
| 5 · Review/Gov | Code Review Agent | Engineering Leader | stub |
| 5 · Review/Gov | Governance & Security Agent | Engineering Leader | stub |

---

## 5. Triage Agent (full design)

**Persona:** Product Owner
**Description (source):** *"Checks if the raised defect is an issue / feature and
lists the impacted objects and/or updates the story with the analysis."*

**Sub-agent frontmatter**
- `name: triage-agent`
- `tools: Read, Grep, Glob, Edit, Write, Bash`
- `model: sonnet`

**Inputs**
- A ticket id (e.g. `PROJ-101`) → reads `tickets/PROJ-101.json`.
- Read access to `snowflake/**` to discover impacted objects by keyword/name match.

**Process**
1. Read the ticket (summary, description, type, reporter, components).
2. **Classify** as `ISSUE` (genuine defect) or `FEATURE` (new/enhancement work)
   with a short rationale and a confidence score (0–1).
3. **Discover impacted objects**: scan `snowflake/**` (and referenced job/code
   names) for tables, procs, views, and Control-M/Korous jobs named or implied
   by the ticket. Produce a typed list `{type, name, path, why}`.
4. **Assess severity** (`P1..P4`) from keywords (duplicates, data loss, prod down…).
5. **Recommend downstream agents** (routing list) based on verdict + impacted
   object types — e.g. an ISSUE touching a proc → `impact-analysis`, `stored-proc`,
   `unit-test`, `code-review`; a FEATURE → `design` first.
6. **Write analysis back** into the ticket JSON under a `triage` block
   (verdict, confidence, severity, impacted_objects, recommended_agents,
   analyzed_at, notes), so the "story is updated with the analysis".

**Output contract** (`tickets/<id>.json` → `triage` object):
```json
{
  "triage": {
    "verdict": "ISSUE",
    "confidence": 0.86,
    "severity": "P2",
    "rationale": "Duplicate rows indicate a load-logic defect, not new scope.",
    "impacted_objects": [
      {"type": "table", "name": "FCT_TRADES", "path": "snowflake/ddl/fct_trades.sql", "why": "named in summary"},
      {"type": "proc",  "name": "LOAD_FCT_TRADES", "path": "snowflake/procs/load_fct_trades.sql", "why": "loads the impacted table"}
    ],
    "recommended_agents": ["impact-analysis-agent","stored-proc-agent","unit-test-agent","code-review-agent"],
    "analyzed_at": "<timestamp>",
    "analyzed_by": "triage-agent"
  }
}
```

---

## 6. Jarvis orchestrator (`/jarvis <TICKET-ID>`)

A **skill** invoked from the main thread (which has the Agent tool, so it can
call sub-agents in sequence). Flow:

1. Validate the ticket id and load `tickets/<id>.json`.
2. Invoke **triage-agent**; read back the `triage` block.
3. **Spec (MANDATORY, all verdicts):** invoke **design-agent** to write
   `specs/<id>/<id>.md` listing ALL proposed changes. If no spec is written, STOP.
4. **SME APPROVAL GATE (hard stop):** halt and present the spec; set/read the
   ticket `approval` block. No Analysis/Build/Test/Quality/Review agent runs
   until `approval.status == "approved"`. See `docs/SPEC-002-spec-first-gate.md`.
5. Walk the remaining `recommended_agents` (design-agent already ran), invoking
   each sub-agent in turn, passing the ticket id + accumulated context.
6. Append each step to `runtime/pipeline-runlog.jsonl` (agent, ticket, ts, status).
7. Print a final pipeline summary table.

> **Spec-first rule (SME):** nothing is implemented without an approved spec, and
> the spec must enumerate every proposed change. This gate is mandatory for both
> ISSUE and FEATURE tickets.

Since the 17 downstream agents are stubs, in this iteration they return a
structured "NOT IMPLEMENTED — would do X" response; Jarvis still demonstrates the
full routing/logging end-to-end with Triage producing real output.

---

## 7. Hooks — SQL/code standards (PostToolUse)

Registered in `.claude/settings.json` as a **PostToolUse** hook matching
`Write|Edit`. Runs `.claude/hooks/sql_standards.py`, which receives the tool
payload on stdin and checks files ending in `.sql`/`.py`:

**SQL rules**
- Table/view names must use approved prefixes: `DIM_`, `FCT_`, `STG_`, `VW_`,
  `HUB_`, `LNK_`, `SAT_`.
- Identifiers `UPPER_SNAKE_CASE`.
- Ban `SELECT *` in views/procs.
- Require a header comment block (`-- Object:`, `-- Owner:`, `-- Ticket:`).
- No hard-coded credentials/secrets.

**Python rules**
- Require module docstring.
- Ban `print(` debug in committed scripts (warn).
- No hard-coded credentials.

**Behavior:** violations are reported back to the agent (non-zero exit with a
clear message) so the agent self-corrects. Warnings are advisory. This is how
"simple standards run after the described agents (incl. Triage)" is enforced.

---

## 8. Hard-coded Snowflake models (Fidelity trades star schema)

- `DIM_ACCOUNT` — account/customer dimension.
- `DIM_SECURITY` — instrument/security dimension.
- `DIM_DATE` — calendar dimension.
- `FCT_TRADES` — fact table (one row per executed trade), FKs to the dims.
- `LOAD_FCT_TRADES` — stored procedure loading the fact (the proc that the
  PROJ-101 duplicate-trades defect points at).
- `VW_DAILY_POSITIONS` — view aggregating positions per account/security/day.

All written to conform to the standards in §7 (so the hook passes on the seeds).

---

## 9. Mock Jira tickets

- **PROJ-101** — *DEFECT*: "FCT_TRADES shows duplicate trades for some accounts
  after the nightly LOAD_FCT_TRADES run." → Triage should classify **ISSUE**,
  impacted = `FCT_TRADES`, `LOAD_FCT_TRADES`.
- **PROJ-102** — *FEATURE*: "Add SETTLEMENT_DATE to FCT_TRADES and expose it in
  VW_DAILY_POSITIONS." → Triage should classify **FEATURE**, route via Design.

Each ticket: `id, type, summary, description, reporter, components, status`, plus
the `triage` block written by the Triage Agent at run time.

---

## 10. How it will be used

```
/jarvis PROJ-101      # runs the full pipeline; Triage produces real analysis
```
or invoke a single agent directly via the Agent tool, e.g. the Triage Agent on a
ticket id.

---

## 11. Out of scope (this iteration)

- Live Jira / Control-M / Snowflake connectivity (all mocked locally).
- Full implementation of the 17 downstream agents (structured stubs only).
- The "Overall Agent (Jarvis)" notes cells from the sheet beyond what §6 covers.

---

## 12. Acceptance criteria

- [ ] **Spec-first gate (SPEC-002):** Jarvis always runs `design-agent` to write
      `specs/<id>/<id>.md` after Triage and HALTS for SME approval; no build/test/
      quality/review agent runs until `approval.status == "approved"`.
- [ ] `.claude/agents/` contains all 18 agents + `jarvis` wiring; Triage fully built.
- [ ] Running Triage on `PROJ-101` writes a correct `triage` block (ISSUE,
      impacted = FCT_TRADES + LOAD_FCT_TRADES) back to the ticket JSON.
- [ ] Running Triage on `PROJ-102` classifies FEATURE and routes via Design.
- [ ] `/jarvis PROJ-101` walks the pipeline and logs each step to the runlog.
- [ ] Editing a `.sql` file that violates a rule triggers the standards hook.
- [ ] Snowflake seed models and both tickets exist and are internally consistent.
```
