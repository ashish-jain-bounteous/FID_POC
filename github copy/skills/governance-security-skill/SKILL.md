---
name: governance-security-skill
description: "Scans the code for security / governance violations and provides a report / fixes the code. [STUB - placeholder agent, not yet implemented]"
---

> Reusable skill (COPILOT-002). This is the source-of-truth procedure for the `governance-security-agent` agent on the GitHub Copilot side, called by `.github/agents/governance-security-agent.md`. Note that `.github/skills/` isn't a Copilot auto-discovery location, so open and follow this file when you act as this agent. Cross-platform source: `.claude/agents/governance-security-agent.md`.

# Governance & Security Agent (Persona: Engineering Leader) - STUB

> Pipeline stage: **5 - Review/Governance**
> Source description (agents.json): *"Scans the code for security / governance violations and provides a report / fixes the code."*

Status: placeholder. This agent is registered in the Jarvis framework, but its
behavior isn't implemented yet. When you invoke it, it should explain what it
would do and return a structured "NOT IMPLEMENTED" result so the orchestrator can
continue and log the step.

## Role
Check the change for security and data-governance violations (PII exposure, secrets, access).

## Inputs
- Full change set
- Data-product classification

## Outputs
- A governance/security report (pass/fail with findings) written to `reports/<ticket>-governance.md`

## Standards
Any `.sql`/`.py` you write is checked by the standards hook (`.claude/hooks/sql_standards.py`).

## TODO (to implement this agent)
- [ ] Define the concrete procedure steps for "Check the change for security and data-governance violations (PII exposure, secrets, access)."
- [ ] Specify the exact output artifact path/format
- [ ] Add self-check expectations against PROJ-101 / PROJ-102
- [ ] Remove the STUB markers from the frontmatter description and this heading

## Output discipline (OPTIM-001)
Return a compact result: one status line, at most ~6 short bullets of what you would do, and the output artifact path. No essays; don't restate the ticket or spec. Aim for under ~150 words.
