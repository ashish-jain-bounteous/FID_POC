# Jarvis — Data Engineering Agentic Delivery Framework

A Claude Code–native agentic framework built from `agents.json` (Sheet3 of
*Fid Data GenAI usecases.xlsx*). It takes a Jira ticket for a Snowflake data
platform and drives it through a pipeline of 18 specialized agents, coordinated
by a master orchestrator (**Jarvis**). Full design: [`docs/SPEC.md`](docs/SPEC.md).

## What's here

```
.claude/
  agents/          18 sub-agents — triage-agent (built) + 17 structured stubs
  skills/jarvis/         /jarvis <TICKET-ID> orchestrator
  skills/spec-template/  /spec-template <TICKET> [agent] — canonical spec scaffolder
  hooks/           sql_standards.py — SQL/code standards (PostToolUse)
  settings.json    registers the hook on Write|Edit
snowflake/         hard-coded star schema (DIM_/FCT_), proc, view
tickets/           mock Jira tickets (Triage input + output)
control_m/         mock Control-M job definition
runtime/           pipeline-runlog.jsonl (audit, generated at run time)
docs/SPEC.md       approved specification
```

## Run it

```
/jarvis PROJ-101      # defect  -> Triage = ISSUE/P2, routes to fix/test/review
/jarvis PROJ-102      # feature -> Triage = FEATURE/P3, routes via Design first
```

Jarvis runs the **Triage Agent** first (fully implemented): it classifies the
ticket as ISSUE vs FEATURE, discovers impacted Snowflake/Control-M objects,
assigns severity, recommends the downstream agent route, and writes the analysis
back into the ticket's `triage` block. The 17 downstream agents are structured
stubs that report "NOT IMPLEMENTED — would do X"; Jarvis still walks and logs the
full route.

> Note: a newly added sub-agent type becomes invocable in a **new** Claude Code
> session (agents are discovered at startup). The Triage analysis for the two
> sample tickets has already been generated and written into `tickets/*.json`.

## Standards hook

Any `.sql`/`.py` file written or edited is checked by
`.claude/hooks/sql_standards.py`: approved object prefixes
(`DIM_/FCT_/STG_/VW_/HUB_/LNK_/SAT_/SEQ_`), `UPPER_SNAKE_CASE`, required header
block (`-- Object:/Owner:/Ticket:`), no `SELECT *`, no hard-coded secrets.
Violations block the write (exit 2) and are fed back to the agent to self-correct.

## Agent roster

See [`docs/SPEC.md` §4](docs/SPEC.md) for the full agent → persona → pipeline-stage
mapping (Intake → Analysis → Build → Test → Quality/FinOps → Review/Governance).
