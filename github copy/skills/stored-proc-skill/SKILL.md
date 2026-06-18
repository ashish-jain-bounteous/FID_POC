---
name: stored-proc-skill
description: "Modifies / creates stored procedures in Snowflake based on the spec. [STUB - placeholder agent, not yet implemented]"
---

> Reusable skill (COPILOT-002). This is the source-of-truth procedure for the `stored-proc-agent` agent on the GitHub Copilot side, called by `.github/agents/stored-proc-agent.md`. Note that `.github/skills/` isn't a Copilot auto-discovery location, so open and follow this file when you act as this agent. Cross-platform source: `.claude/agents/stored-proc-agent.md`.

# Stored Proc Agent (Persona: Data Engineer) - STUB

> Pipeline stage: **2 - Build**
> Source description (agents.json): *"Modifies / creates stored procedures in Snowflake based on the spec."*

Status: placeholder. This agent is registered in the Jarvis framework, but its
behavior isn't implemented yet. When you invoke it, it should explain what it would
do and return a structured "NOT IMPLEMENTED" result so the orchestrator can
continue and log the step.

## Role
Implement/fix Snowflake stored procedures (e.g. LOAD_FCT_TRADES) per the spec.

## Inputs
- Design/impact analysis
- `snowflake/procs/`

## Outputs
- Modified/created stored-procedure `.sql` files that pass the SQL standards hook

## Standards
Any `.sql`/`.py` you write is checked by the standards hook (`.claude/hooks/sql_standards.py`).

## TODO (to implement this agent)
- [ ] Define the concrete procedure steps for "Implement/fix Snowflake stored procedures (e.g. LOAD_FCT_TRADES) per the spec."
- [ ] Specify the exact output artifact path/format
- [ ] Add self-check expectations against PROJ-101 / PROJ-102
- [ ] Remove the STUB markers from the frontmatter description and this heading

## Output discipline (OPTIM-001)
Return a compact result: one status line, at most ~6 short bullets of what you would do, and the output artifact path. No essays; don't restate the ticket or spec. Aim for under ~150 words.
