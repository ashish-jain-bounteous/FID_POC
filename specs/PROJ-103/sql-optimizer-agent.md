# Action Spec: SQL Optimizer Agent (Persona: Finops & Devops) - PROJ-103

**Agent:** `sql-optimizer-agent`  ·  Persona: Finops & Devops  ·  Pipeline stage: 4 - Quality/FinOps
**Ticket:** PROJ-103: Optimize LOAD_FCT_TRADES stored procedure for faster nightly load
**Verdict / severity:** FEATURE / P3   (from Triage)
**Routing status:** ROUTED
**Action status:** PLANNED (awaiting approval)
**Master spec:** `specs/PROJ-103/PROJ-103.md`   ·   **Ticket approval:** PENDING SME APPROVAL
**This action-spec status:** AWAITING SME REVIEW   ·   **Date:** 2026-06-18T06:41:00Z

---

## Purpose of this action spec
This document states, for review before execution, exactly what SQL Optimizer Agent (Persona: Finops & Devops)
will do for PROJ-103. Per the spec-first / SME-approval rule
(`docs/SPEC-002-spec-first-gate.md`), no action listed below is performed until
this spec is approved at the SME gate. It exists so any action this agent takes
is reviewable in isolation, separate from the master spec.

## Agent role
Scans the code and optimizes SQL for Snowflake execution by simulating and providing optimized parameters.

## Planned action for PROJ-103
Simulate the MERGE-based load and the FCT_TRADES(TRADE_ID) clustering vs Search Optimization, and recommend the Snowflake parameters (warehouse size, which lookup aid). Read-only analysis.

## Inputs
Master spec specs/PROJ-103/PROJ-103.md; tickets/PROJ-103.json; relevant source under snowflake/ and control_m/.

## Output artifact(s)
Optimization report with recommended parameters; edits no source.

## Objects in scope (from Triage)
| Object | Type | Path | This ticket's interaction |
|--------|------|------|---------------------------|
| `LOAD_FCT_TRADES` | proc | `snowflake/procs/load_fct_trades.sql` | in scope for this ticket |
| `FCT_TRADES` | table | `snowflake/ddl/fct_trades.sql` | in scope for this ticket |
| `STG_TRADES` | table | `snowflake/staging/stg_trades.sql` | in scope for this ticket |
| `CTM_LOAD_FCT_TRADES` | job | `control_m/CTM_LOAD_FCT_TRADES.json` | in scope for this ticket |

## Proposed changes / operations (for review)
| # | File | Operation |
|---|------|-----------|
_None: this agent produces an analysis/report, no source changes._
<!-- Use "_None: this agent produces no source/file changes for this ticket._" if not routed. -->

## Guardrails / standards
**This agent is propose/report-only for this ticket**; it produces an analysis/report artifact and edits no source files.

## Review checklist
- [ ] Action matches the ticket scope and verdict (FEATURE/P3).
- [ ] No change outside the objects-in-scope list above.
- [ ] Consistent with the master spec `specs/PROJ-103/PROJ-103.md`.
- [ ] Standards hook satisfied (if this agent writes `.sql`/`.py`).
- [ ] Open questions / risks surfaced to the SME.

## Approval
- SME: __________   status: pending   date: ______
