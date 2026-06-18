# Jarvis Plan - PROJ-103 (plan mode)

**Ticket:** PROJ-103 - Optimize LOAD_FCT_TRADES stored procedure for faster nightly load
**Verdict / severity:** FEATURE / P3
**Run:** `.github` guided, plan mode (no source or development changes made)
**Generated:** 2026-06-18T07:02:08Z
**Gate status:** AWAITING SME APPROVAL (no downstream agent has run)

This is a plan only. It describes what the pipeline would do end to end. Nothing
in `snowflake/`, `control_m/`, or `tests/` is changed by producing it.

## 1. Triage (done)
Classified FEATURE / P3. The ask is a performance/cost optimization of the
nightly load with no change to output. Impacted objects:

| Object | Type | Path |
|--------|------|------|
| LOAD_FCT_TRADES | proc | `snowflake/procs/load_fct_trades.sql` |
| FCT_TRADES | table | `snowflake/ddl/fct_trades.sql` |
| STG_TRADES | table | `snowflake/staging/stg_trades.sql` |
| CTM_LOAD_FCT_TRADES | job | `control_m/CTM_LOAD_FCT_TRADES.json` |

Route: design-agent -> sql-optimizer-agent -> stored-proc-agent -> code-review-agent.

## 2. Design (done) - master spec
`specs/PROJ-103/PROJ-103.md` proposes 3 changes (output stays byte-for-byte identical):

| # | File | Change |
|---|------|--------|
| 1 | `snowflake/procs/load_fct_trades.sql` | Replace the `NOT EXISTS` anti-join with a `MERGE ... ON TRADE_ID WHEN NOT MATCHED`. Keep the `IS_CURRENT = TRUE` join. |
| 2 | `snowflake/ddl/fct_trades.sql` | Clustering key or Search Optimization on `FCT_TRADES(TRADE_ID)`. |
| 3 | `control_m/CTM_LOAD_FCT_TRADES.json` | No definition change; post-deploy runtime/warehouse review. |

## 3. Execution plan (route, after approval)

| Stage | Agent | Planned action | Writes source? |
|-------|-------|----------------|----------------|
| done | design-agent | Authored the master spec + 18 action specs. | no (markdown) |
| next | sql-optimizer-agent | Simulate the MERGE load and FCT_TRADES(TRADE_ID) clustering vs Search Optimization; recommend warehouse size and the lookup aid. Read-only analysis. | no (report) |
| then | stored-proc-agent | Apply change 1 in `load_fct_trades.sql` (MERGE refactor). Reconcile against the current file, which already carries a MERGE version. | yes (.sql, standards hook applies) |
| last | code-review-agent | Review against the spec + standards, confirm output is byte-for-byte identical, check scope creep, produce a verdict. | no (report) |

Not routed for this ticket (13 agents): triage covers intake; data-modelling,
lineage, impact-analysis, sql, python, scheduler, code-refactor, unit-test,
regression-test, sonar-remediation, code-quality, data-product, governance-security
take no action. Each has a "not routed" action spec under `specs/PROJ-103/`.

## 4. Token budget estimate
- Remaining routed agents after design (sql-optimizer, stored-proc, code-review): 3 x ~3k-6k = ~9k-18k
- Orchestration + logging overhead: ~3k
- Already spent (triage + design): ~8k-14k
- **Estimated total to finish: ~12k-22k tokens** (evaluation excluded; add ~150k+ only if run with `--eval`)

## 5. Risks
- R1: `load_fct_trades.sql` already carries the MERGE optimization from an earlier run, so development is mostly reconcile + verify, not a from-scratch rewrite.
- R2: Clustering / Search Optimization add storage and maintenance cost; confirm the speedup is worth it.
- R3: Output-equivalence (byte-for-byte) is the acceptance bar and must be proven by the regression test before this is "done".

## 6. Deploy / sequencing
Single proc change plus an optional table optimization. No data remediation, no
schedule change. Order: apply proc (1), apply table optimization (2), review,
then post-deploy warehouse review (3).

## 7. Next step
Pipeline is halted at the SME / human-in-the-loop gate. To proceed:
`approve` (then development runs the route above), optionally `--eval` to also
run the with/without-skill A/B (adds ~150k+ tokens). No changes happen until then.
