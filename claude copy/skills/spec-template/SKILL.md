---
name: spec-template
description: Single source of truth for the Jarvis spec structure. Scaffolds a new spec - the master spec (specs/<TICKET>/<TICKET>.md) or an agent action spec (specs/<TICKET>/<agent>.md) - pre-filled from the ticket's Triage block so every spec follows the same sections. Invoke as "/spec-template <TICKET> [agent-slug]" (e.g. /spec-template PROJ-103, or /spec-template PROJ-103 sql-agent).
---

# spec-template: Canonical Spec Scaffolder

Every spec in this project follows one of two fixed structures. This skill owns
both templates and stamps out a new, correctly-structured spec into the
per-ticket folder `specs/<TICKET>/`. Use it whenever a new spec is needed so no
section is invented, dropped, or reordered.

The two structures:
- **Master spec** → `specs/<TICKET>/<TICKET>.md`, written by `design-agent`.
  Template: `templates/master-spec.md`.
- **Action spec** → `specs/<TICKET>/<agent-slug>.md`, one per downstream agent.
  Template: `templates/action-spec.md`.

## Argument
`<TICKET> [agent-slug]` passed as the skill argument:
- `/spec-template PROJ-103` → scaffold the **master** spec (`PROJ-103/PROJ-103.md`).
- `/spec-template PROJ-103 master` → same as above (explicit).
- `/spec-template PROJ-103 sql-agent` → scaffold the **action** spec for `sql-agent`.

If no ticket id is given, ask which ticket in `tickets/` to scaffold for, or list
them.

## Procedure

1. **Resolve the target path.**
   - No agent / `master` / `design-agent` (master) → `specs/<TICKET>/<TICKET>.md`.
   - An agent slug → `specs/<TICKET>/<agent-slug>.md`. The slug must be one of the
     18 agents in `agents.json` (`triage-agent`, `design-agent`, `sql-agent`,
     `stored-proc-agent`, and so on). Reject anything else.
   - Don't overwrite. If the target file already exists, stop and report it,
     then offer to open it instead. Don't clobber an approved spec.

2. **Create the folder** `specs/<TICKET>/` if it does not exist.

3. **Gather fill values** (read-only):
   - Read `tickets/<TICKET>.json` → `summary`/`title`, and the `triage` block
     (`verdict`, `severity`, `impacted_objects`, `recommended_agents`).
   - Read the `approval` block for `{{TICKET_APPROVAL}}` (e.g.
     `APPROVED BY SME (<ts>)` or `PENDING SME APPROVAL`).
   - For an action spec, derive `{{ROUTING_STATUS}}` / `{{ACTION_STATUS}}` from
     whether the slug is in `recommended_agents`, and pull the agent's persona,
     pipeline stage, and one-line role from `.claude/agents/<slug>.md` /
     `agents.json`.
   - Timestamp `{{UTC_ISO8601}}` from `date -u +%Y-%m-%dT%H:%M:%SZ`.

4. **Read the matching template** under `templates/`, substitute every `{{...}}`
   placeholder, and pre-fill the **Objects in scope** / **Impacted objects** table
   from `triage.impacted_objects`. Leave genuine design content (Objective,
   Proposed changes, Test plan, Rollback, Risks) as the template's guidance
   comments; those are authored by the responsible agent, not invented here.

5. **Write** the file with the Write tool. The standards hook does not apply
   (Markdown only).

6. **Report**: the path written, master-vs-action, the placeholders filled, and
   which sections the responsible agent must now complete. State that the spec
   carries **Status: AWAITING SME APPROVAL** and must pass the SME gate before any
   implementation (`docs/SPEC-002-spec-first-gate.md`).

## Placeholder reference

| Placeholder | Source |
|-------------|--------|
| `{{TICKET}}` | the argument |
| `{{SUMMARY}}` | `tickets/<TICKET>.json` summary/title |
| `{{VERDICT}}` / `{{SEVERITY}}` | `triage.verdict` / `triage.severity` |
| `{{UTC_ISO8601}}` | `date -u +%Y-%m-%dT%H:%M:%SZ` |
| `{{AGENT_TITLE}}` / `{{AGENT_SLUG}}` | agent display name / slug |
| `{{PERSONA}}` / `{{STAGE}}` | `.claude/agents/<slug>.md` header |
| `{{ROUTING_STATUS}}` / `{{ACTION_STATUS}}` | derived from `recommended_agents` |
| `{{TICKET_APPROVAL}}` | `tickets/<TICKET>.json` `approval` block |

## Structure contract (do not deviate)

**Master spec, sections in order:** Title (`# Spec: <TICKET> - <summary>`) →
status header block → `## Objective` → `## Proposed changes (ALL)` →
`## Impacted objects` → `## Test plan` (Unit + Regression) → `## Rollback plan`
→ `## Risks / open questions` → `## Token budget estimate` → `## Approvals`.

**Action spec, sections in order:** Title (`# Action Spec: <Agent> - <TICKET>`)
→ header block → `## Purpose of this action spec` → `## Agent role` →
`## Planned action` → `## Inputs` → `## Output artifact(s)` →
`## Objects in scope (from Triage)` → `## Proposed changes / operations` →
`## Guardrails / standards` → `## Review checklist` → `## Approval`.

A spec missing or reordering any of these sections is non-conformant and must
not be approved. `design-agent` and every downstream agent author their specs to
this contract; this skill is the canonical reference they follow.

## Examples
```
/spec-template PROJ-103                 # new master spec for a new ticket
/spec-template PROJ-103 sql-agent       # sql-agent's action spec
/spec-template PROJ-101 stored-proc-agent
```
