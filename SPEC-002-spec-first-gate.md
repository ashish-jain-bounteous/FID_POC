# SPEC-002 — Mandatory Spec-First + SME Approval Gate

**Status:** APPROVED by SME (2026-06-10) — implemented (Changes 1–6 applied)
**Author:** Claude (Jarvis framework)
**Date:** 2026-06-10
**Supersedes/extends:** `docs/SPEC.md`
**Driver:** SME rule — *"Always generate specs first before implementing any
agents and get approval from SME. Without specs, nothing should be done. Specs
should mention all the proposed changes."*

---

## 1. Problem

In the current framework the spec-producing agent (`design-agent`) only runs for
**FEATURE** tickets, and all downstream agents are stubs that write nothing. So a
ticket can move through the pipeline (e.g. PROJ-101) with **no spec** and no
approval gate. This violates the SME rule.

## 2. Goal

Make the framework — and my own development of it — **spec-first and
SME-gated**: every change must be described in a spec that lists *all* proposed
changes, and an SME must approve that spec before any implementation/build runs.

This policy operates at **two levels**:
- **A. Framework runtime** — the Jarvis pipeline must produce a spec and pause
  for SME approval before any build/test/quality/review agent acts.
- **B. Development** — when I implement or modify any agent/hook/model, I first
  write an implementation spec and get SME approval.

---

## 3. Proposed changes (ALL of them)

### Change 1 — Jarvis orchestrator gains a mandatory Spec + Approval gate
**File:** `.claude/skills/jarvis/SKILL.md`
- Insert a new **Stage 0.5: Spec** immediately after Triage and **before every
  other agent**, for **ALL verdicts** (ISSUE and FEATURE alike).
- Jarvis invokes the spec agent (`design-agent`) to write `specs/<TICKET>/<TICKET>.md`.
- Insert a new **Stage 0.6: SME Approval** — Jarvis **HALTS** and presents the
  spec to the SME. No build/test/quality/review/governance agent may run until
  the SME records approval.
- Jarvis reads an approval status; if `pending` or `rejected`, it stops with a
  clear message and logs `APPROVAL_PENDING` / `APPROVAL_REJECTED`.
- Only on `approved` does Jarvis walk the remaining route.

### Change 2 — `design-agent` promoted from stub to the Spec Author (implemented)
**File:** `.claude/agents/design-agent.md`
- Fully implement it as the **spec author** for any ticket (not just features).
- It reads the ticket + Triage block, inspects impacted objects, and writes
  `specs/<TICKET>/<TICKET>.md` using the template in §4 — listing **every** proposed
  change (file, exact change, rationale), impacted objects, test plan, rollback,
  and an **Approvals** section left for the SME.
- It must NOT modify any source/model files — it only proposes.
- (This `design-agent` implementation is itself covered by this spec; per the
  rule it is built only after SME approval of SPEC-002.)

### Change 3 — Triage routing always puts the spec step first
**File:** `.claude/agents/triage-agent.md`
- Update the routing rules so `design-agent` is **always** the first entry in
  `recommended_agents`, regardless of ISSUE vs FEATURE.
- Re-run Triage on existing tickets so their `recommended_agents` reflect this.

### Change 4 — Approval tracking
**File:** ticket JSON (`tickets/<id>.json`) — add an `approval` block:
```json
"approval": { "spec": "specs/PROJ-101/PROJ-101.md", "status": "pending",
              "approved_by": null, "approved_at": null, "notes": null }
```
- `status` ∈ `pending | approved | rejected`. Jarvis honors it as the hard gate.
- The SME (human) flips it to `approved` (in this Claude Code context, via a
  confirmation that I record) to unlock the rest of the pipeline.

### Change 5 — Update `docs/SPEC.md`
- Document the new mandatory Spec + SME-Approval gate in the orchestration
  section and acceptance criteria.

### Change 6 — Development working principle (no file; behavioral)
- For any future agent/hook/model work, I will write an implementation spec
  (under `docs/` or `specs/`) and obtain SME approval **before** coding.

---

## 4. Spec template (what `specs/<TICKET>/<TICKET>.md` must contain)

```
# Spec: <TICKET> — <summary>
- Verdict / severity (from Triage)
- Objective
- Proposed changes (table): | # | file | change | rationale |
  ...must list ALL files and ALL changes...
- Impacted objects (from Triage/impact analysis)
- Test plan (unit + regression)
- Rollback plan
- Risks / open questions
- Approvals:  SME: __________  status: pending  date: ____
```

A spec is **incomplete** (and must not be approved) if any proposed change to a
file is omitted.

---

## 5. Resulting pipeline (after this spec is approved & implemented)

```
Triage  ->  Spec (design-agent writes specs/<id>/<id>.md)  ->  [SME APPROVAL GATE]
        -> (only if approved) -> Impact/Lineage -> Build -> Test -> Quality -> Review/Gov
```

For PROJ-101 specifically: Triage already done → next a real `specs/PROJ-101/PROJ-101.md`
listing the `LOAD_FCT_TRADES` `IS_CURRENT` fix + duplicate-cleanup + tests →
SME approves → then (and only then) the fix agents run.

---

## 6. Out of scope (this change)
- Implementing the other 16 stub agents (separate, each spec-gated).
- Live Jira/Snowflake/Control-M connectivity.

## 7. Acceptance criteria
- [ ] Jarvis halts after writing the spec and does not run build agents without
      `approval.status == approved`.
- [ ] `design-agent` writes a complete `specs/<id>/<id>.md` for ISSUE and FEATURE.
- [ ] Triage routes `design-agent` first for all verdicts.
- [ ] `docs/SPEC.md` documents the gate.
- [ ] No implementation occurs before SME approval (this very spec included).

---

## 8. SME decision
Approve this SPEC-002 to let me implement Changes 1–6. Until approved, I will
not modify the orchestrator, agents, hooks, or models.
```
