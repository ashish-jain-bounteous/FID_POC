---
name: lineage-skill
description: "Creates a detailed lineage report of the impacted objects (tables / code / jobs). [STUB - placeholder agent, not yet implemented]"
---

> Reusable skill (COPILOT-002). This is the source-of-truth procedure for the `lineage-agent` agent on the GitHub Copilot side, called by `.github/agents/lineage-agent.md`. Note that `.github/skills/` isn't a Copilot auto-discovery location, so open and follow this file when you act as this agent. Cross-platform source: `.claude/agents/lineage-agent.md`.

# Lineage Agent (Persona: Product Owner) - STUB

> Pipeline stage: **1 - Analysis**
> Source description (agents.json): *"Creates a detailed lineage report of the impacted objects (tables / code / jobs)."*

Status: placeholder. This agent is registered in the Jarvis framework, but its
behavior isn't implemented yet. When you invoke it, it should explain what it
would do and return a structured "NOT IMPLEMENTED" result so the orchestrator can
continue and log the step.

## Role
Trace and document end-to-end lineage for the impacted objects across tables, code and Control-M jobs.

## Inputs
- Impacted objects from Triage
- `snowflake/**` and `control_m/**`

## Outputs
- A lineage report (upstream sources -> object -> downstream consumers) written to `reports/<ticket>-lineage.md`

## Standards
Any `.sql`/`.py` you write is checked by the standards hook (`.claude/hooks/sql_standards.py`).

## TODO (to implement this agent)
- [ ] Define the concrete procedure steps for "Trace and document end-to-end lineage for the impacted objects across tables, code and Control-M jobs."
- [ ] Specify the exact output artifact path/format
- [ ] Add self-check expectations against PROJ-101 / PROJ-102
- [ ] Remove the STUB markers from the frontmatter description and this heading

## Output discipline (OPTIM-001)
Return a compact result: one status line, at most ~6 short bullets of what you would do, and the output artifact path. No essays; don't restate the ticket or spec. Aim for under ~150 words.
