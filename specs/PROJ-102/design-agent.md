# Action Spec: Design Agent — PROJ-102

**Agent:** `design-agent`  ·  Persona: Product Owner  ·  Pipeline stage: 0.5 — Spec
**Ticket:** PROJ-102 — Add SETTLEMENT_DATE to FCT_TRADES and expose it in VW_DAILY_POSITIONS
**Verdict / severity:** FEATURE / P3   (from Triage)
**Routing status:** ROUTED (step 1 of the recommended route)
**Action status:** PLANNED — spec not yet written
**Master spec:** `specs/PROJ-102/PROJ-102.md`   ·   **Ticket approval:** PENDING SME APPROVAL
**This action-spec status:** AWAITING SME REVIEW   ·   **Date:** 2026-06-12T09:39:32Z

---

## Purpose of this action spec
This document states — **for review before execution** — exactly what Design Agent
will do for PROJ-102. Per the spec-first / SME-approval rule
(`docs/SPEC-002-spec-first-gate.md`), no action listed below is performed until
this spec is approved at the SME gate. It exists so any action this agent takes
is reviewable in isolation, separate from the master spec.

## Agent role
Author the master implementation spec listing EVERY proposed change, impacted objects, test plan and rollback. Proposes only — never edits source.

## Planned action for PROJ-102
Author `specs/PROJ-102/PROJ-102.md` listing every change to add settlement reporting: FCT_TRADES DDL column, T+2 population in LOAD_FCT_TRADES, view exposure, tests, and governance classification. Proposes only.

## Inputs
tickets/PROJ-102.json (triage block); impacted source files

## Output artifact(s)
specs/PROJ-102/PROJ-102.md (master spec)

## Objects in scope (from Triage)
| Object | Type | Path | This ticket's interaction |
|--------|------|------|---------------------------|
| `ANALYTICS.MART.FCT_TRADES` | table | `snowflake/ddl/fct_trades.sql` | New SETTLEMENT_DATE column to be added |
| `ANALYTICS.MART.LOAD_FCT_TRADES` | proc | `snowflake/procs/load_fct_trades.sql` | Must populate SETTLEMENT_DATE (T+2) |
| `ANALYTICS.MART.VW_DAILY_POSITIONS` | view | `snowflake/views/vw_daily_positions.sql` | Must expose settlement date downstream |

## Proposed changes / operations (for review)
| # | File | Operation |
|---|------|-----------|
| 1 | specs/PROJ-102/PROJ-102.md | Create the master implementation spec for the SETTLEMENT_DATE feature. |

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
