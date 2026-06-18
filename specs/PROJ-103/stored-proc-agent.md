# Action Spec: Stored Proc Agent (Persona: Data Engineer) - PROJ-103

**Agent:** `stored-proc-agent`  ·  Persona: Data Engineer  ·  Pipeline stage: 2 - Build
**Ticket:** PROJ-103: Optimize LOAD_FCT_TRADES stored procedure for faster nightly load
**Verdict / severity:** FEATURE / P3   (from Triage)
**Routing status:** ROUTED
**Action status:** PLANNED (awaiting approval)
**Master spec:** `specs/PROJ-103/PROJ-103.md`   ·   **Ticket approval:** PENDING SME APPROVAL
**This action-spec status:** AWAITING SME REVIEW   ·   **Date:** 2026-06-18T06:41:00Z

---

## Purpose of this action spec
This document states, for review before execution, exactly what Stored Proc Agent (Persona: Data Engineer)
will do for PROJ-103. Per the spec-first / SME-approval rule
(`docs/SPEC-002-spec-first-gate.md`), no action listed below is performed until
this spec is approved at the SME gate. It exists so any action this agent takes
is reviewable in isolation, separate from the master spec.

## Agent role
Modifies / creates stored procedures in Snowflake based on the spec.

## Planned action for PROJ-103
Implement change 1 in snowflake/procs/load_fct_trades.sql: the MERGE refactor that replaces the NOT EXISTS anti-join, keeping the IS_CURRENT join and identical output. Reconcile against the current file, which already carries a MERGE version.

## Inputs
Master spec specs/PROJ-103/PROJ-103.md; tickets/PROJ-103.json; relevant source under snowflake/ and control_m/.

## Output artifact(s)
Modified snowflake/procs/load_fct_trades.sql.

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
| 1 | `snowflake/procs/load_fct_trades.sql` | Apply the MERGE refactor (change 1 of the master spec). |
<!-- Use "_None: this agent produces no source/file changes for this ticket._" if not routed. -->

## Guardrails / standards
**This agent writes source/model files.** Every `.sql`/`.py` it touches is validated by the standards hook (`.claude/hooks/sql_standards.py`).

## Review checklist
- [ ] Action matches the ticket scope and verdict (FEATURE/P3).
- [ ] No change outside the objects-in-scope list above.
- [ ] Consistent with the master spec `specs/PROJ-103/PROJ-103.md`.
- [ ] Standards hook satisfied (if this agent writes `.sql`/`.py`).
- [ ] Open questions / risks surfaced to the SME.

## Approval
- SME: __________   status: pending   date: ______
