# Action Spec: Triage Agent — PROJ-101

**Agent:** `triage-agent`  ·  Persona: Product Owner  ·  Pipeline stage: 0 — Intake
**Ticket:** PROJ-101 — FCT_TRADES shows duplicate trades for some accounts after nightly load
**Verdict / severity:** ISSUE / P2   (from Triage)
**Routing status:** ALWAYS-RUN (intake step, ran before the route)
**Action status:** COMPLETED
**Master spec:** `specs/PROJ-101/PROJ-101.md`   ·   **Ticket approval:** APPROVED BY SME (2026-06-10T11:36:05Z)
**This action-spec status:** AWAITING SME REVIEW   ·   **Date:** 2026-06-12T09:39:32Z

---

## Purpose of this action spec
This document states — **for review before execution** — exactly what Triage Agent
will do for PROJ-101. Per the spec-first / SME-approval rule
(`docs/SPEC-002-spec-first-gate.md`), no action listed below is performed until
this spec is approved at the SME gate. It exists so any action this agent takes
is reviewable in isolation, separate from the master spec.

## Agent role
Classify a ticket as ISSUE vs FEATURE, discover impacted objects, assign severity, recommend the downstream route, and write the analysis back into the ticket JSON.

## Planned action for PROJ-101
- Classified the ticket **ISSUE / P2** (confidence 0.97).
- Discovered impacted objects: FCT_TRADES, LOAD_FCT_TRADES, DIM_ACCOUNT, VW_DAILY_POSITIONS, CTM_LOAD_FCT_TRADES.
- Recommended the downstream route (design → impact → lineage → stored-proc → unit-test → regression-test → code-review).
- Wrote the `triage` block back into `tickets/PROJ-101.json`.

## Inputs
tickets/PROJ-101.json; snowflake/**; control_m/**

## Output artifact(s)
Updated `triage` block in tickets/PROJ-101.json

## Objects in scope (from Triage)
| Object | Type | Path | This ticket's interaction |
|--------|------|------|---------------------------|
| `ANALYTICS.MART.LOAD_FCT_TRADES` | proc | `snowflake/procs/load_fct_trades.sql` | Root-cause object — join predicate + dedup guard |
| `ANALYTICS.MART.FCT_TRADES` | table | `snowflake/ddl/fct_trades.sql` | Fact table receiving the duplicates; UNIQUE(TRADE_ID) added |
| `ANALYTICS.MART.DIM_ACCOUNT` | table | `snowflake/ddl/dim_account.sql` | SCD-2 dimension joined without IS_CURRENT (read-only) |
| `ANALYTICS.MART.VW_DAILY_POSITIONS` | view | `snowflake/views/vw_daily_positions.sql` | Downstream consumer double-counting positions |
| `CTM_LOAD_FCT_TRADES` | job | `control_m/CTM_LOAD_FCT_TRADES.json` | Nightly job; one-time dedup sequencing condition |

## Proposed changes / operations (for review)
| # | File | Operation |
|---|------|-----------|
| 1 | tickets/PROJ-101.json | Set the `triage` object (verdict, severity, impacted_objects, recommended_agents). |

## Guardrails / standards
**This agent is propose/report-only for this ticket** — it produces an analysis/report artifact and edits no source files. (Triage/Design write JSON/Markdown only.)

## Review checklist
- [ ] Action matches the ticket scope and verdict (ISSUE/P2).
- [ ] No change outside the objects-in-scope list above.
- [ ] Consistent with the master spec `specs/PROJ-101/PROJ-101.md`.
- [ ] Standards hook satisfied (if this agent writes `.sql`/`.py`).
- [ ] Open questions / risks surfaced to the SME.

## Approval
- SME: __________   status: pending   date: ______
