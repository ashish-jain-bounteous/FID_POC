# Action Spec: Regression Test Agent — PROJ-101

**Agent:** `regression-test-agent`  ·  Persona: Test Engineer  ·  Pipeline stage: 3 — Test
**Ticket:** PROJ-101 — FCT_TRADES shows duplicate trades for some accounts after nightly load
**Verdict / severity:** ISSUE / P2   (from Triage)
**Routing status:** ROUTED (step 6 of the recommended route)
**Action status:** PLANNED
**Master spec:** `specs/PROJ-101/PROJ-101.md`   ·   **Ticket approval:** APPROVED BY SME (2026-06-10T11:36:05Z)
**This action-spec status:** AWAITING SME REVIEW   ·   **Date:** 2026-06-12T09:39:32Z

---

## Purpose of this action spec
This document states — **for review before execution** — exactly what Regression Test Agent
will do for PROJ-101. Per the spec-first / SME-approval rule
(`docs/SPEC-002-spec-first-gate.md`), no action listed below is performed until
this spec is approved at the SME gate. It exists so any action this agent takes
is reviewable in isolation, separate from the master spec.

## Agent role
Identify the relevant existing tests and register them in the regression catalog.

## Planned action for PROJ-101
Register PROJ-101 in the regression catalog: changed objects (LOAD_FCT_TRADES, FCT_TRADES, CTM_LOAD_FCT_TRADES), the unit test file, and the regression suite R-1…R-5.

## Inputs
Changed objects; existing tests under tests/

## Output artifact(s)
Updated tests/regression-catalog.json

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
| 1 | tests/regression-catalog.json | Add/refresh the PROJ-101 entry (tests + R-1…R-5 suite). |

## Guardrails / standards
**This agent writes source/model files.** Every `.sql`/`.py` it touches is validated by the PostToolUse standards hook (`.claude/hooks/sql_standards.py`): approved object prefixes (DIM_/FCT_/STG_/VW_/HUB_/LNK_/SAT_), UPPER_SNAKE_CASE identifiers, required header block, no `SELECT *`, no hard-coded secrets.

## Review checklist
- [ ] Action matches the ticket scope and verdict (ISSUE/P2).
- [ ] No change outside the objects-in-scope list above.
- [ ] Consistent with the master spec `specs/PROJ-101/PROJ-101.md`.
- [ ] Standards hook satisfied (if this agent writes `.sql`/`.py`).
- [ ] Open questions / risks surfaced to the SME.

## Approval
- SME: __________   status: pending   date: ______
