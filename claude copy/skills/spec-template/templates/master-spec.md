# Spec: {{TICKET}} - {{SUMMARY}}

**Status:** AWAITING SME APPROVAL
**Verdict / severity:** {{VERDICT}} / {{SEVERITY}}   (from Triage)
**Author:** design-agent   **Date:** {{UTC_ISO8601}}

---

## Objective

<one or two paragraphs: what this change achieves and why. State the root cause
(for an ISSUE) or the capability being added (for a FEATURE). No solution detail
here; that goes in Proposed changes.>

---

## Proposed changes (ALL)

| # | File | Change | Rationale |
|---|------|--------|-----------|
| 1 | `snowflake/procs/<file>.sql` | <exact change, line/identifier level> | <why this change, root-cause linked> |
| 2 | ... | ... | ... |
<!-- Every file that will change should appear here. Omitting one invalidates the spec. -->

---

## Impacted objects

| Object | Type | Path | Impact |
|--------|------|------|--------|
| `ANALYTICS.MART.<OBJ>` | proc/table/view/job | `<path>` | <what changes, or "read-only reference"> |

**Secondary / monitoring objects (no change required):**
- `<OBJECT>`: <why it is in the blast radius but not changed>

---

## Test plan

### Unit tests

| # | Test case | Method | Expected result |
|---|-----------|--------|-----------------|
| U-1 | <name> | <how to set up and run> | <observable pass condition> |

### Regression tests

| # | Test case | Scope |
|---|-----------|-------|
| R-1 | <end-to-end / downstream check> | <objects covered> |

---

## Rollback plan

| # | Change | Rollback action |
|---|--------|-----------------|
| 1 | <change> | <exact revert steps; note any pre-deploy backup required> |

**Pre-deployment requirement:** <backups/snapshots to take before destructive
changes, or "none">.

---

## Risks / open questions

| # | Risk / question | Severity | Owner |
|---|-----------------|----------|-------|
| R1 | <risk, with enough detail for the SME to decide> | High/Med/Low | <team> |

<!-- Use "none" if there are genuinely no open questions. -->

---

## Token budget estimate

Rough heuristic to finish this ticket end to end (not a measurement; varies with
file sizes and model verbosity):
- Remaining routed agents after design: `<N>` x ~3k-6k each
- Orchestration + logging overhead: ~2k-5k
- Already spent (triage + design): ~8k-15k
- **Estimated total to finish: ~`<lo>`k-`<hi>`k tokens** (evaluation excluded;
  add ~150k+ only if run with `--eval`)

---

## Approvals

- SME: __________   status: pending   date: ______
