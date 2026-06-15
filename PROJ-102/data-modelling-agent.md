# Action Spec: Data Modelling Agent — PROJ-102

**Agent:** `data-modelling-agent`  ·  Persona: Data modeller  ·  Pipeline stage: 1 — Analysis
**Ticket:** PROJ-102 — Add SETTLEMENT_DATE to FCT_TRADES and expose it in VW_DAILY_POSITIONS
**Verdict / severity:** FEATURE / P3   (from Triage)
**Routing status:** ROUTED (step 2 of the recommended route)
**Action status:** PLANNED
**Master spec:** `specs/PROJ-102/PROJ-102.md`   ·   **Ticket approval:** PENDING SME APPROVAL
**This action-spec status:** AWAITING SME REVIEW   ·   **Date:** 2026-06-12T09:39:32Z

---

## Purpose of this action spec
This document states — **for review before execution** — exactly what Data Modelling Agent
will do for PROJ-102. Per the spec-first / SME-approval rule
(`docs/SPEC-002-spec-first-gate.md`), no action listed below is performed until
this spec is approved at the SME gate. It exists so any action this agent takes
is reviewable in isolation, separate from the master spec.

## Agent role
Produce/update the logical & physical data model (dimensional star and/or Data Vault hubs/links/satellites) for the change.

## Planned action for PROJ-102
Model the new attribute on the fact grain:
- Add `SETTLEMENT_DATE` to FCT_TRADES.
- **Open modelling question:** store as a raw `DATE`, or add `SETTLEMENT_DATE_KEY` FK to DIM_DATE for star-schema consistency with TRADE_DATE_KEY. Recommend and document the choice.

## Inputs
Design spec; existing DDL under snowflake/ddl/

## Output artifact(s)
Updated model DDL / model notes (DIM_/FCT_/HUB_/LNK_/SAT_)

## Objects in scope (from Triage)
| Object | Type | Path | This ticket's interaction |
|--------|------|------|---------------------------|
| `ANALYTICS.MART.FCT_TRADES` | table | `snowflake/ddl/fct_trades.sql` | New SETTLEMENT_DATE column to be added |
| `ANALYTICS.MART.LOAD_FCT_TRADES` | proc | `snowflake/procs/load_fct_trades.sql` | Must populate SETTLEMENT_DATE (T+2) |
| `ANALYTICS.MART.VW_DAILY_POSITIONS` | view | `snowflake/views/vw_daily_positions.sql` | Must expose settlement date downstream |

## Proposed changes / operations (for review)
| # | File | Operation |
|---|------|-----------|
| 1 | snowflake/ddl/fct_trades.sql | Model SETTLEMENT_DATE attribute (DATE vs DIM_DATE FK) — proposed model note/DDL, pending design. |

## Guardrails / standards
**This agent writes source/model files.** Every `.sql`/`.py` it touches is validated by the PostToolUse standards hook (`.claude/hooks/sql_standards.py`): approved object prefixes (DIM_/FCT_/STG_/VW_/HUB_/LNK_/SAT_), UPPER_SNAKE_CASE identifiers, required header block, no `SELECT *`, no hard-coded secrets.

## Review checklist
- [ ] Action matches the ticket scope and verdict (FEATURE/P3).
- [ ] No change outside the objects-in-scope list above.
- [ ] Consistent with the master spec `specs/PROJ-102/PROJ-102.md`.
- [ ] Standards hook satisfied (if this agent writes `.sql`/`.py`).
- [ ] Open questions / risks surfaced to the SME.

## Approval
- SME: __________   status: pending   date: ______
