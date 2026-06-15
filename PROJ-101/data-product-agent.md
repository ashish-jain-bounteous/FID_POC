# Action Spec: Data Product Agent — PROJ-101

**Agent:** `data-product-agent`  ·  Persona: Product Owner  ·  Pipeline stage: 1 — Analysis
**Ticket:** PROJ-101 — FCT_TRADES shows duplicate trades for some accounts after nightly load
**Verdict / severity:** ISSUE / P2   (from Triage)
**Routing status:** NOT ROUTED for this ticket
**Action status:** NOT ROUTED — no action planned
**Master spec:** `specs/PROJ-101/PROJ-101.md`   ·   **Ticket approval:** APPROVED BY SME (2026-06-10T11:36:05Z)
**This action-spec status:** AWAITING SME REVIEW   ·   **Date:** 2026-06-12T09:39:32Z

---

## Purpose of this action spec
This document states — **for review before execution** — exactly what Data Product Agent
will do for PROJ-101. Per the spec-first / SME-approval rule
(`docs/SPEC-002-spec-first-gate.md`), no action listed below is performed until
this spec is approved at the SME gate. It exists so any action this agent takes
is reviewable in isolation, separate from the master spec.

## Agent role
Capture the data-product metadata contract (owner, domain, SLA, freshness, PII classification, schema contract) for the impacted dataset.

## Planned action for PROJ-101
Triage did not route **Data Product Agent** for PROJ-101. No action will be taken.

_If it were routed, it would: Capture the data-product metadata contract (owner, domain, SLA, freshness, PII classification, schema contract) for the impacted dataset._

## Inputs
Impacted dataset(s) from Triage/Design

## Output artifact(s)
reports/PROJ-101-data-product.md

## Objects in scope (from Triage)
| Object | Type | Path | This ticket's interaction |
|--------|------|------|---------------------------|
| `ANALYTICS.MART.LOAD_FCT_TRADES` | proc | `snowflake/procs/load_fct_trades.sql` | Root-cause object — join predicate + dedup guard |
| `ANALYTICS.MART.FCT_TRADES` | table | `snowflake/ddl/fct_trades.sql` | Fact table receiving the duplicates; UNIQUE(TRADE_ID) added |
| `ANALYTICS.MART.DIM_ACCOUNT` | table | `snowflake/ddl/dim_account.sql` | SCD-2 dimension joined without IS_CURRENT (read-only) |
| `ANALYTICS.MART.VW_DAILY_POSITIONS` | view | `snowflake/views/vw_daily_positions.sql` | Downstream consumer double-counting positions |
| `CTM_LOAD_FCT_TRADES` | job | `control_m/CTM_LOAD_FCT_TRADES.json` | Nightly job; one-time dedup sequencing condition |

## Proposed changes / operations (for review)
_None — this agent produces no source/file changes for this ticket._

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
