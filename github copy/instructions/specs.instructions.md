---
applyTo: "specs/**/*.md"
description: "Canonical spec structure + the spec-first / SME-approval rule."
---

# Spec authoring rules

Specs gate all implementation work (`docs/SPEC-002-spec-first-gate.md`):
nothing is built without an approved spec that lists all proposed changes.
A new spec is written with **Status: AWAITING SME APPROVAL** and must pass the
SME gate before any source or model file is touched.

Use `/spec-template <TICKET> [agent]` to scaffold. Keep the canonical structure:

**Master spec** (`specs/<TICKET>/<TICKET>.md`), sections in order:
`# Spec: <TICKET> - <summary>` → status header → `## Objective` →
`## Proposed changes (ALL)` → `## Impacted objects` → `## Test plan` →
`## Rollback plan` → `## Risks / open questions` → `## Token budget estimate` → `## Approvals`.

**Action spec** (`specs/<TICKET>/<agent>.md`), sections in order:
`# Action Spec: <Agent> - <TICKET>` → header → `## Purpose of this action spec`
→ `## Agent role` → `## Planned action` → `## Inputs` → `## Output artifact(s)` →
`## Objects in scope (from Triage)` → `## Proposed changes / operations` →
`## Guardrails / standards` → `## Review checklist` → `## Approval`.

The **Proposed changes (ALL)** table must list every file that will change;
omitting one invalidates the spec. A spec that's missing or reordering any section is
non-conformant and must not be approved.
