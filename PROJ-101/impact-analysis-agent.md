# Action Spec: Impact Analysis Agent — PROJ-101

**Agent:** `impact-analysis-agent`  ·  Persona: Product Owner  ·  Pipeline stage: 1 — Analysis
**Ticket:** PROJ-101 — FCT_TRADES shows duplicate trades for some accounts after nightly load
**Verdict / severity:** ISSUE / P2   (from Triage)
**Routing status:** ROUTED (step 2 of the recommended route)
**Action status:** PLANNED
**Master spec:** `specs/PROJ-101/PROJ-101.md`   ·   **Ticket approval:** APPROVED BY SME (2026-06-10T11:36:05Z)
**This action-spec status:** AWAITING SME REVIEW   ·   **Date:** 2026-06-12T09:39:32Z

---

## Purpose of this action spec
This document states — **for review before execution** — exactly what Impact Analysis Agent
will do for PROJ-101. Per the spec-first / SME-approval rule
(`docs/SPEC-002-spec-first-gate.md`), no action listed below is performed until
this spec is approved at the SME gate. It exists so any action this agent takes
is reviewable in isolation, separate from the master spec.

## Agent role
Determine everything affected by the change, both upstream (backward) and downstream (forward).

## Planned action for PROJ-101
Produce a forward/backward impact report for the duplicate-trades fix:
- **Backward (upstream):** STG_TRADES (source), DIM_ACCOUNT (SCD-2 root cause — multiple IS_CURRENT rows), DIM_SECURITY/DIM_DATE (joined, unaffected).
- **Forward (downstream):** VW_DAILY_POSITIONS (double-counted NET_QUANTITY/NET_AMOUNT), plus any dashboards/extracts reading it.
- Assess blast radius of the one-time DELETE remediation and the new UNIQUE(TRADE_ID) constraint.

## Inputs
Impacted objects from Triage; snowflake/**, control_m/**, referencing views/procs

## Output artifact(s)
reports/PROJ-101-impact.md

## Objects in scope (from Triage)
| Object | Type | Path | This ticket's interaction |
|--------|------|------|---------------------------|
| `ANALYTICS.MART.LOAD_FCT_TRADES` | proc | `snowflake/procs/load_fct_trades.sql` | Root-cause object — join predicate + dedup guard |
| `ANALYTICS.MART.FCT_TRADES` | table | `snowflake/ddl/fct_trades.sql` | Fact table receiving the duplicates; UNIQUE(TRADE_ID) added |
| `ANALYTICS.MART.DIM_ACCOUNT` | table | `snowflake/ddl/dim_account.sql` | SCD-2 dimension joined without IS_CURRENT (read-only) |
| `ANALYTICS.MART.VW_DAILY_POSITIONS` | view | `snowflake/views/vw_daily_positions.sql` | Downstream consumer double-counting positions |
| `CTM_LOAD_FCT_TRADES` | job | `control_m/CTM_LOAD_FCT_TRADES.json` | Nightly job; one-time dedup sequencing condition |

## Proposed changes / operations (for review)
_Read-only analysis — emits `reports/PROJ-101-impact.md`; edits no source files._

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
