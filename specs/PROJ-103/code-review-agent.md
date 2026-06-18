# Action Spec: Code Review Agent (Persona: Engineering Leader) - PROJ-103

**Agent:** `code-review-agent`  ·  Persona: Engineering Leader  ·  Pipeline stage: 5 - Review/Governance
**Ticket:** PROJ-103: Optimize LOAD_FCT_TRADES stored procedure for faster nightly load
**Verdict / severity:** FEATURE / P3   (from Triage)
**Routing status:** ROUTED
**Action status:** PLANNED (awaiting approval)
**Master spec:** `specs/PROJ-103/PROJ-103.md`   ·   **Ticket approval:** PENDING SME APPROVAL
**This action-spec status:** AWAITING SME REVIEW   ·   **Date:** 2026-06-18T06:41:00Z

---

## Purpose of this action spec
This document states, for review before execution, exactly what Code Review Agent (Persona: Engineering Leader)
will do for PROJ-103. Per the spec-first / SME-approval rule
(`docs/SPEC-002-spec-first-gate.md`), no action listed below is performed until
this spec is approved at the SME gate. It exists so any action this agent takes
is reviewable in isolation, separate from the master spec.

## Agent role
Reviews the code against standards / best practices and provides a report / fixes the code.

## Planned action for PROJ-103
Review the optimization against the master spec and standards, confirm output is byte-for-byte identical, check for scope creep, and produce a verdict.

## Inputs
Master spec specs/PROJ-103/PROJ-103.md; tickets/PROJ-103.json; relevant source under snowflake/ and control_m/.

## Output artifact(s)
Review verdict (report); edits no source.

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
