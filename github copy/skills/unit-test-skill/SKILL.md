---
name: unit-test-skill
description: "Creates unit test cases based on the spec and code. [STUB - placeholder agent, not yet implemented]"
---

> Reusable skill (COPILOT-002). This is the source-of-truth procedure for the `unit-test-agent` agent on the GitHub Copilot side, called by `.github/agents/unit-test-agent.md`. Note that `.github/skills/` isn't a Copilot auto-discovery location, so open and follow this file when you act as this agent. Cross-platform source: `.claude/agents/unit-test-agent.md`.

# Unit Test Agent (Persona: Test Engineer) - STUB

> Pipeline stage: **3 - Test**
> Source description (agents.json): *"Creates unit test cases based on the spec and code."*

Status: placeholder. This agent is registered in the Jarvis framework, but its
behavior isn't implemented yet. When you invoke it, it should explain what it would
do and return a structured "NOT IMPLEMENTED" result so the orchestrator can
continue and log the step.

## Role
Author unit tests covering the changed logic and the defect's reproduction case.

## Inputs
- Spec + changed code

## Outputs
- Unit test files / test SQL under `tests/` covering the change

## Standards
Any `.sql`/`.py` you write is checked by the standards hook (`.claude/hooks/sql_standards.py`).

## TODO (to implement this agent)
- [ ] Define the concrete procedure steps for "Author unit tests covering the changed logic and the defect's reproduction case."
- [ ] Specify the exact output artifact path/format
- [ ] Add self-check expectations against PROJ-101 / PROJ-102
- [ ] Remove the STUB markers from the frontmatter description and this heading

## Output discipline (OPTIM-001)
Return a compact result: one status line, at most ~6 short bullets of what you would do, and the output artifact path. No essays; don't restate the ticket or spec. Aim for under ~150 words.
