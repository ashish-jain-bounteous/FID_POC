---
description: "Scaffold a spec in the canonical structure - master spec (specs/<TICKET>/<TICKET>.md) or an agent action spec (specs/<TICKET>/<agent>.md), pre-filled from the ticket's triage block. Usage: /spec-template PROJ-103 [agent-slug]"
mode: agent
tools: ['codebase', 'search', 'editFiles']
---

# spec-template Canonical Spec Scaffolder (GitHub Copilot prompt)

Converted from `.claude/skills/spec-template/SKILL.md` per spec
`specs/COPILOT-001-copilot-conversion.md`. This prompt owns the canonical spec
structure so every spec in the repo is identical in shape.

## Argument
`${input:args:PROJ-103}` = `<TICKET> [agent-slug]`:
- `/spec-template PROJ-103` → scaffold the **master** spec `specs/PROJ-103/PROJ-103.md`.
- `/spec-template PROJ-103 master` → same (explicit).
- `/spec-template PROJ-103 sql-agent` → scaffold the **action** spec for `sql-agent`.

If no ticket id is given, list the tickets in `tickets/` and ask which to use.

## Procedure
1. **Resolve the target path.**
   - No agent / `master` / `design-agent` (master) → `specs/<TICKET>/<TICKET>.md`.
   - An agent slug → `specs/<TICKET>/<agent-slug>.md`. The slug has to be one of the
     18 agents (see `.github/agents/`). Reject anything else.
   - Don't overwrite an existing spec; stop and offer to open it instead.
2. **Create** the `specs/<TICKET>/` folder if needed.
3. **Gather fill values** (read-only): read `tickets/<TICKET>.json` for
   `summary`, the `triage` block (`verdict`, `severity`, `impacted_objects`,
   `recommended_agents`) and the `approval` block; derive routing status for an
   action spec; timestamp via `date -u +%Y-%m-%dT%H:%M:%SZ`.
4. **Read the matching template** under `.github/prompts/templates/`
   (`master-spec.md` or `action-spec.md`), substitute every `{{...}}` placeholder,
   and pre-fill the objects table from `triage.impacted_objects`. Leave genuine
   design content (Objective, Proposed changes, Test plan, Rollback, Risks) as the
   template's guidance for the responsible agent to complete.
5. **Write** the spec file.
6. **Report** the path written, master-vs-action, placeholders filled, and which
   sections still need authoring. The spec carries **Status: AWAITING SME
   APPROVAL** and must pass the SME gate before any implementation.

## Structure contract (do not deviate)
**Master spec sections, in order:** Title (`# Spec: <TICKET> - <summary>`) →
status header → `## Objective` → `## Proposed changes (ALL)` →
`## Impacted objects` → `## Test plan` (Unit + Regression) → `## Rollback plan` →
`## Risks / open questions` → `## Token budget estimate` → `## Approvals`.

**Action spec sections, in order:** Title (`# Action Spec: <Agent> - <TICKET>`) →
header → `## Purpose of this action spec` → `## Agent role` → `## Planned action`
→ `## Inputs` → `## Output artifact(s)` → `## Objects in scope (from Triage)` →
`## Proposed changes / operations` → `## Guardrails / standards` →
`## Review checklist` → `## Approval`.

A spec that's missing or reordering any section is non-conformant and must not be
approved.
