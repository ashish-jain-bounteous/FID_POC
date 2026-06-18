---
name: regression-test-skill
description: "Identifies all unit test cases for that code and updates the catalog for the future regression suite. [STUB - placeholder agent, not yet implemented]"
---

> Reusable skill (COPILOT-002). This is the source-of-truth procedure for the `regression-test-agent` agent on the GitHub Copilot side, called by `.github/agents/regression-test-agent.md`. Note that `.github/skills/` isn't a Copilot auto-discovery location, so open and follow this file when you act as this agent. Cross-platform source: `.claude/agents/regression-test-agent.md`.

# Regression Test Agent (Persona: Test Engineer) - STUB

> Pipeline stage: **3 - Test**
> Source description (agents.json): *"Identifies all unit test cases for that code and updates the catalog for the future regression suite."*

Status: placeholder. This agent is registered in the Jarvis framework, but its
behavior isn't implemented yet. When you invoke it, it should explain what it would
do and return a structured "NOT IMPLEMENTED" result so the orchestrator can
continue and log the step.

## Role
Identify the relevant existing tests and register them in the regression catalog.

## Inputs
- Changed objects
- Existing tests under `tests/`

## Outputs
- Updated regression catalog (`tests/regression-catalog.json`) referencing the relevant tests

## Standards
Any `.sql`/`.py` you write is checked by the standards hook (`.claude/hooks/sql_standards.py`).

## TODO (to implement this agent)
- [ ] Define the concrete procedure steps for "Identify the relevant existing tests and register them in the regression catalog."
- [ ] Specify the exact output artifact path/format
- [ ] Add self-check expectations against PROJ-101 / PROJ-102
- [ ] Remove the STUB markers from the frontmatter description and this heading

## Output discipline (OPTIM-001)
Return a compact result: one status line, at most ~6 short bullets of what you would do, and the output artifact path. No essays; don't restate the ticket or spec. Aim for under ~150 words.
