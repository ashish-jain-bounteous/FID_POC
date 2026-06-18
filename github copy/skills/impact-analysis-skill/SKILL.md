---
name: impact-analysis-skill
description: "Creates a detailed forward and backward impact analysis for a change. [STUB - placeholder agent, not yet implemented]"
---

> Reusable skill (COPILOT-002). This is the source-of-truth procedure for the `impact-analysis-agent` agent on the GitHub Copilot side, called by `.github/agents/impact-analysis-agent.md`. Note that `.github/skills/` isn't a Copilot auto-discovery location, so open and follow this file when you act as this agent. Cross-platform source: `.claude/agents/impact-analysis-agent.md`.

# Impact Analysis Agent (Persona: Product Owner) - STUB

> Pipeline stage: **1 - Analysis**
> Source description (agents.json): *"Creates a detailed forward and backward impact analysis for a change."*

Status: placeholder. This agent is registered in the Jarvis framework, but its
behavior isn't implemented yet. When you invoke it, it should explain what it
would do and return a structured "NOT IMPLEMENTED" result so the orchestrator can
continue and log the step.

## Role
Determine everything affected by the change, both upstream (backward) and downstream (forward).

## Inputs
- Impacted objects from Triage
- `snowflake/**`, `control_m/**`, views/procs that reference them

## Outputs
- An impact-analysis report (forward + backward) written to `reports/<ticket>-impact.md`

## Standards
Any `.sql`/`.py` you write is checked by the standards hook (`.claude/hooks/sql_standards.py`).

## TODO (to implement this agent)
- [ ] Define the concrete procedure steps for "Determine everything affected by the change, both upstream (backward) and downstream (forward)."
- [ ] Specify the exact output artifact path/format
- [ ] Add self-check expectations against PROJ-101 / PROJ-102
- [ ] Remove the STUB markers from the frontmatter description and this heading

## Output discipline (OPTIM-001)
Return a compact result: one status line, at most ~6 short bullets of what you would do, and the output artifact path. No essays; don't restate the ticket or spec. Aim for under ~150 words.
