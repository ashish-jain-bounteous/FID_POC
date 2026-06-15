# Action Spec: Stored Proc Agent — PROJ-102

**Agent:** `stored-proc-agent`  ·  Persona: Data Engineer  ·  Pipeline stage: 2 — Build
**Ticket:** PROJ-102 — Add SETTLEMENT_DATE to FCT_TRADES and expose it in VW_DAILY_POSITIONS
**Verdict / severity:** FEATURE / P3   (from Triage)
**Routing status:** ROUTED (step 5 of the recommended route)
**Action status:** PLANNED
**Master spec:** `specs/PROJ-102/PROJ-102.md`   ·   **Ticket approval:** PENDING SME APPROVAL
**This action-spec status:** AWAITING SME REVIEW   ·   **Date:** 2026-06-12T09:39:32Z

---

## Purpose of this action spec
This document states — **for review before execution** — exactly what Stored Proc Agent
will do for PROJ-102. Per the spec-first / SME-approval rule
(`docs/SPEC-002-spec-first-gate.md`), no action listed below is performed until
this spec is approved at the SME gate. It exists so any action this agent takes
is reviewable in isolation, separate from the master spec.

## Agent role
Implement/fix Snowflake stored procedures (e.g. LOAD_FCT_TRADES) per the spec.

## Planned action for PROJ-102
Populate the new column in the nightly load:
- Compute `SETTLEMENT_DATE` as T+2 from trade date and add it to the INSERT column list and SELECT.
- **Open question:** calendar T+2 vs business-day T+2 (skip weekends/holidays via DIM_DATE/TRADING_DAYS) — flag for SME.

## Inputs
Design/impact analysis; snowflake/procs/

## Output artifact(s)
Modified/created stored-procedure .sql files

## Objects in scope (from Triage)
| Object | Type | Path | This ticket's interaction |
|--------|------|------|---------------------------|
| `ANALYTICS.MART.FCT_TRADES` | table | `snowflake/ddl/fct_trades.sql` | New SETTLEMENT_DATE column to be added |
| `ANALYTICS.MART.LOAD_FCT_TRADES` | proc | `snowflake/procs/load_fct_trades.sql` | Must populate SETTLEMENT_DATE (T+2) |
| `ANALYTICS.MART.VW_DAILY_POSITIONS` | view | `snowflake/views/vw_daily_positions.sql` | Must expose settlement date downstream |

## Proposed changes / operations (for review)
| # | File | Operation |
|---|------|-----------|
| 1 | snowflake/procs/load_fct_trades.sql | Add SETTLEMENT_DATE to INSERT list and compute T+2 in the SELECT. |

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
