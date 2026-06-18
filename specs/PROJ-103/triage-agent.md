# Action Spec: Triage Agent (Persona: Product Owner) - PROJ-103

**Agent:** `triage-agent`  ·  Persona: Product Owner  ·  Pipeline stage: 0 - Intake
**Ticket:** PROJ-103: Optimize LOAD_FCT_TRADES stored procedure for faster nightly load
**Verdict / severity:** FEATURE / P3   (from Triage)
**Routing status:** ROUTED (intake)
**Action status:** COMPLETED
**Master spec:** `specs/PROJ-103/PROJ-103.md`   ·   **Ticket approval:** PENDING SME APPROVAL
**This action-spec status:** AWAITING SME REVIEW   ·   **Date:** 2026-06-18T06:41:00Z

---

## Purpose of this action spec
This document states, for review before execution, exactly what Triage Agent (Persona: Product Owner)
will do for PROJ-103. Per the spec-first / SME-approval rule
(`docs/SPEC-002-spec-first-gate.md`), no action listed below is performed until
this spec is approved at the SME gate. It exists so any action this agent takes
is reviewable in isolation, separate from the master spec.

## Agent role
Triages a Jira ticket for the Snowflake data platform. Classifies it as a genuine ISSUE (defect) or a FEATURE (new/enhancement work), discovers the impacted Snowflake/Control-M objects, assigns severity, recommends the downstream agents to run, and writes the full analysis back into the ticket JSON. Use this first for any incoming ticket.

## Planned action for PROJ-103
Classified the ticket FEATURE/P3, confirmed the optimization scope (no output change), and routed design, sql-optimizer, stored-proc, code-review. Analysis written to the ticket triage block.

## Inputs
Master spec specs/PROJ-103/PROJ-103.md; tickets/PROJ-103.json; relevant source under snowflake/ and control_m/.

## Output artifact(s)
Updated tickets/PROJ-103.json triage block (done).

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
| 1 | `tickets/PROJ-103.json` | Write the triage block (done). |
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
