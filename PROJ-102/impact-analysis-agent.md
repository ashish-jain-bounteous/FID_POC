# Action Spec: Impact Analysis Agent — PROJ-102

**Agent:** `impact-analysis-agent`  ·  Persona: Product Owner  ·  Pipeline stage: 1 — Analysis
**Ticket:** PROJ-102 — Add SETTLEMENT_DATE to FCT_TRADES and expose it in VW_DAILY_POSITIONS
**Verdict / severity:** FEATURE / P3   (from Triage)
**Routing status:** ROUTED (step 3 of the recommended route)
**Action status:** PLANNED
**Master spec:** `specs/PROJ-102/PROJ-102.md`   ·   **Ticket approval:** PENDING SME APPROVAL
**This action-spec status:** AWAITING SME REVIEW   ·   **Date:** 2026-06-12T09:39:32Z

---

## Purpose of this action spec
This document states — **for review before execution** — exactly what Impact Analysis Agent
will do for PROJ-102. Per the spec-first / SME-approval rule
(`docs/SPEC-002-spec-first-gate.md`), no action listed below is performed until
this spec is approved at the SME gate. It exists so any action this agent takes
is reviewable in isolation, separate from the master spec.

## Agent role
Determine everything affected by the change, both upstream (backward) and downstream (forward).

## Planned action for PROJ-102
Forward/backward impact of adding a nullable→populated column:
- **Backward:** STG_TRADES (does it carry settlement date or is T+2 derived?), DIM_DATE (if FK chosen).
- **Forward:** VW_DAILY_POSITIONS and any consumers — additive column, assess `SELECT`-list and GROUP BY impact and backfill of historical rows.

## Inputs
Impacted objects from Triage; snowflake/**, control_m/**, referencing views/procs

## Output artifact(s)
reports/PROJ-102-impact.md

## Objects in scope (from Triage)
| Object | Type | Path | This ticket's interaction |
|--------|------|------|---------------------------|
| `ANALYTICS.MART.FCT_TRADES` | table | `snowflake/ddl/fct_trades.sql` | New SETTLEMENT_DATE column to be added |
| `ANALYTICS.MART.LOAD_FCT_TRADES` | proc | `snowflake/procs/load_fct_trades.sql` | Must populate SETTLEMENT_DATE (T+2) |
| `ANALYTICS.MART.VW_DAILY_POSITIONS` | view | `snowflake/views/vw_daily_positions.sql` | Must expose settlement date downstream |

## Proposed changes / operations (for review)
_Read-only analysis — emits `reports/PROJ-102-impact.md`; edits no source files._

## Guardrails / standards
**This agent is propose/report-only for this ticket** — it produces an analysis/report artifact and edits no source files. (Triage/Design write JSON/Markdown only.)

## Review checklist
- [ ] Action matches the ticket scope and verdict (FEATURE/P3).
- [ ] No change outside the objects-in-scope list above.
- [ ] Consistent with the master spec `specs/PROJ-102/PROJ-102.md`.
- [ ] Standards hook satisfied (if this agent writes `.sql`/`.py`).
- [ ] Open questions / risks surfaced to the SME.

## Approval
- SME: __________   status: pending   date: ______
