# Action Spec: {{AGENT_TITLE}} - {{TICKET}}

**Agent:** `{{AGENT_SLUG}}`  ·  Persona: {{PERSONA}}  ·  Pipeline stage: {{STAGE}}
**Ticket:** {{TICKET}}: {{SUMMARY}}
**Verdict / severity:** {{VERDICT}} / {{SEVERITY}}   (from Triage)
**Routing status:** {{ROUTING_STATUS}}
**Action status:** {{ACTION_STATUS}}
**Master spec:** `specs/{{TICKET}}/{{TICKET}}.md`   ·   **Ticket approval:** {{TICKET_APPROVAL}}
**This action-spec status:** AWAITING SME REVIEW   ·   **Date:** {{UTC_ISO8601}}

---

## Purpose of this action spec
This document states, for review before execution, exactly what {{AGENT_TITLE}}
will do for {{TICKET}}. Per the spec-first / SME-approval rule
(`docs/SPEC-002-spec-first-gate.md`), no action listed below is performed until
this spec is approved at the SME gate. It exists so any action this agent takes
is reviewable in isolation, separate from the master spec.

## Agent role
<one line: this agent's responsibility, from agents.json>

## Planned action for {{TICKET}}
<what this agent will actually do for this ticket. If Triage did not route it,
state "Triage did not route {{AGENT_TITLE}} for {{TICKET}}. No action will be
taken." and add the conditional `_If it were routed, it would: ..._`>

## Inputs
<artifacts this agent reads: master spec, ticket JSON, source files>

## Output artifact(s)
<files this agent writes, or "report only, edits no source">

## Objects in scope (from Triage)
| Object | Type | Path | This ticket's interaction |
|--------|------|------|---------------------------|
| `ANALYTICS.MART.<OBJ>` | proc/table/view/job | `<path>` | <interaction> |

## Proposed changes / operations (for review)
| # | File | Operation |
|---|------|-----------|
| 1 | `<path>` | <operation> |
<!-- Use "_None: this agent produces no source/file changes for this ticket._" if not routed. -->

## Guardrails / standards
<If this agent writes `.sql`/`.py`: "**This agent writes source/model files.**
Every `.sql`/`.py` it touches is validated by the PostToolUse standards hook
(`.claude/hooks/sql_standards.py`): approved object prefixes
(DIM_/FCT_/STG_/VW_/HUB_/LNK_/SAT_), UPPER_SNAKE_CASE identifiers, required
header block, no `SELECT *`, no hard-coded secrets."  ·  If propose/report-only:
"**This agent is propose/report-only for this ticket**; it produces an
analysis/report artifact and edits no source files.">

## Review checklist
- [ ] Action matches the ticket scope and verdict ({{VERDICT}}/{{SEVERITY}}).
- [ ] No change outside the objects-in-scope list above.
- [ ] Consistent with the master spec `specs/{{TICKET}}/{{TICKET}}.md`.
- [ ] Standards hook satisfied (if this agent writes `.sql`/`.py`).
- [ ] Open questions / risks surfaced to the SME.

## Approval
- SME: __________   status: pending   date: ______
