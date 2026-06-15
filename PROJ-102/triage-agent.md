# Action Spec: Triage Agent — PROJ-102

**Agent:** `triage-agent`  ·  Persona: Product Owner  ·  Pipeline stage: 0 — Intake
**Ticket:** PROJ-102 — Add SETTLEMENT_DATE to FCT_TRADES and expose it in VW_DAILY_POSITIONS
**Verdict / severity:** FEATURE / P3   (from Triage)
**Routing status:** ALWAYS-RUN (intake step, ran before the route)
**Action status:** COMPLETED
**Master spec:** `specs/PROJ-102/PROJ-102.md`   ·   **Ticket approval:** PENDING SME APPROVAL
**This action-spec status:** AWAITING SME REVIEW   ·   **Date:** 2026-06-12T09:39:32Z

---

## Purpose of this action spec
This document states — **for review before execution** — exactly what Triage Agent
will do for PROJ-102. Per the spec-first / SME-approval rule
(`docs/SPEC-002-spec-first-gate.md`), no action listed below is performed until
this spec is approved at the SME gate. It exists so any action this agent takes
is reviewable in isolation, separate from the master spec.

## Agent role
Classify a ticket as ISSUE vs FEATURE, discover impacted objects, assign severity, recommend the downstream route, and write the analysis back into the ticket JSON.

## Planned action for PROJ-102
- Classified the ticket **FEATURE / P3** (confidence 0.95).
- Discovered impacted objects: FCT_TRADES, LOAD_FCT_TRADES, VW_DAILY_POSITIONS.
- Recommended the schema-feature route (design → data-modelling → impact → sql → stored-proc → unit-test → code-review → governance-security).
- Wrote the `triage` block back into `tickets/PROJ-102.json`.

## Inputs
tickets/PROJ-102.json; snowflake/**; control_m/**

## Output artifact(s)
Updated `triage` block in tickets/PROJ-102.json

## Objects in scope (from Triage)
| Object | Type | Path | This ticket's interaction |
|--------|------|------|---------------------------|
| `ANALYTICS.MART.FCT_TRADES` | table | `snowflake/ddl/fct_trades.sql` | New SETTLEMENT_DATE column to be added |
| `ANALYTICS.MART.LOAD_FCT_TRADES` | proc | `snowflake/procs/load_fct_trades.sql` | Must populate SETTLEMENT_DATE (T+2) |
| `ANALYTICS.MART.VW_DAILY_POSITIONS` | view | `snowflake/views/vw_daily_positions.sql` | Must expose settlement date downstream |

## Proposed changes / operations (for review)
| # | File | Operation |
|---|------|-----------|
| 1 | tickets/PROJ-102.json | Set the `triage` object (verdict, severity, impacted_objects, recommended_agents). |

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
