# Copilot Instructions - Jarvis Data-Engineering Delivery Framework

These are the custom instructions for GitHub Copilot in this repo. This codebase runs on both Claude Code (`.claude/`) and GitHub Copilot (`.github/`), so apply these rules whenever you're working here.

## What we're building
This is an agentic delivery framework for a Snowflake data platform. When a Jira ticket comes in, it flows through 18 specialized agents coordinated by Jarvis. The pipeline goes: Triage, Design (spec), SME approval gate, Analysis, Build, Test, Quality/FinOps, Review, and Governance. See `docs/SPEC.md` for the full design.

## The spec-first and SME-approval rule
Here's the core principle: nothing gets implemented without an approved spec. The spec lists every single proposed change. Check `docs/SPEC-002-spec-first-gate.md` for details.

For any ticket, the design-agent writes a master spec to `specs/<TICKET>/<TICKET>.md` that includes every file, exact change, rationale, impacted objects, test plan, and rollback steps.

The pipeline halts until an SME approves it. You'll know it's approved when the ticket's `approval` block flips to `approved`. Nothing builds, tests, or reviews until then. This applies to both issues and features.

Use `/spec-template <TICKET>` or `/spec-template <TICKET> <agent>` to scaffold a new spec.

## How to work as an agent
The 18 agents live in `.github/agents/` (one `.md` file per agent, like `triage-agent` or `design-agent`). To act as an agent, open its file. Each agent file is thin because the real work lives in the skill at `.github/skills/<name>-skill/SKILL.md` (so `triage-agent` follows the `triage-skill` skill). Open that skill and follow the procedure there.

To run the full pipeline, use `/jarvis <TICKET>`. This gives you a guided walkthrough since Copilot doesn't support programmatic sub-agent dispatch. Jarvis handles each stage inline and tells you which agent to use next.

Specs for tickets go in `specs/<TICKET>/`. The master spec is `specs/<TICKET>/<TICKET>.md`. Individual agent action specs are `specs/<TICKET>/<agent>.md`.

## SQL and Python standards
Every `.sql` and `.py` file needs to follow these rules. They're checked at commit time by `.github/scripts/check_standards.py`, so violations will block your commit.

For SQL:
- Object names must start with one of these: `DIM_`, `FCT_`, `STG_`, `VW_`, `HUB_`, `LNK_`, `SAT_`, or `SEQ_`
- Use `UPPER_SNAKE_CASE` for all identifiers
- Include a header block with `-- Object:`, `-- Owner:`, and `-- Ticket:`
- Always list columns explicitly, never use `SELECT *`
- No hard-coded secrets, passwords, or API keys

Check `.github/instructions/` for more details. If you get violations, fix them instead of suppressing them.

## Where to find what
These folders are shared between Claude Code and GitHub Copilot.

- `tickets/` holds Jira tickets, both input and output
- `specs/` has all the implementation specs, including master specs and per-agent action specs
- `evals/` has per-agent evaluation definitions
- `runtime/` contains pipeline logs and evaluation logs generated during execution
- `snowflake/` has DDL, stored procedures, views, and the star schema
- `control_m/` has scheduler job definitions
- `docs/SPEC.md` and `docs/SPEC-002-spec-first-gate.md` describe the overall design and the approval gate

## Copilot limitations compared to Claude Code
Copilot works differently in a few ways:

- Copilot can't automatically dispatch to sub-agents, so Jarvis is a guided procedure. See `.github/COPILOT.md`.
- Standards checking is advisory when you generate code, but actually enforced at commit time via CI.
- The automatic eval runner at `evals/run_jarvis_eval.py` only works in Claude. For Copilot, use the `evals/*.json` files as your rubric instead.
