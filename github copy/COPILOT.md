# Using this framework in GitHub Copilot

This repo is dual-platform. The Claude Code config lives in `.claude/`; this
GitHub Copilot mirror lives in `.github/` (plus `.vscode/`). Generated per
`specs/COPILOT-001-copilot-conversion.md`. When you edit an agent or skill, make
the edit in both trees to keep them in sync (see R5 in the spec).

## What's here

| Copilot surface | Path | Purpose |
|-----------------|------|---------|
| **Skills (18)** | `.github/skills/<name>-skill/SKILL.md` | The reusable source-of-truth procedure for each agent (e.g. `triage-skill`). Logic lives here once |
| Agents (18) | `.github/agents/<name>-agent.md` | Thin callers (e.g. `triage-agent`). Open one to act as that agent; it tells the model to open and follow the matching `-skill` |
| Prompts | `.github/prompts/jarvis.prompt.md`, `spec-template.prompt.md` | `/jarvis <TICKET>` and `/spec-template <TICKET> [agent]` |
| Templates | `.github/prompts/templates/` | Canonical master/action spec templates |
| Repo instructions | `.github/copilot-instructions.md` | Always-applied rules (incl. spec-first gate) |
| Path instructions | `.github/instructions/{sql,python,specs}.instructions.md` | Standards + spec structure, scoped by glob |
| Standards gate | `.github/scripts/check_standards.py`, `.pre-commit-config.yaml`, `.github/workflows/standards.yml` | Commit-time + CI enforcement |

## Setup
1. Open the repo in VS Code with GitHub Copilot. `.vscode/settings.json` enables
   prompt files, agents, and instruction discovery.
2. Install the commit-time standards gate:
   ```bash
   pip install pre-commit && pre-commit install
   ```
   The `standards.yml` GitHub Action runs the same check on push/PR.

## How to use
- **Run the pipeline:** open Copilot Chat in **agent** mode and type
  `/jarvis PROJ-101`. Jarvis walks triage → design → SME gate → route → summary.
- **Act as one agent:** open that agent's file (e.g. `.github/agents/triage-agent.md`)
  and have the model follow it, then chat.
- **Scaffold a spec:** `/spec-template PROJ-103` (master) or
  `/spec-template PROJ-103 sql-agent` (action).

## Skills layer (COPILOT-002)
Each agent's procedure lives once in `.github/skills/<name>-skill/SKILL.md` (reusable
source of truth; e.g. `triage-agent` follows `triage-skill`). The agent file is a thin caller that instructs the model to open
and follow that skill. One caveat: `.github/skills/` isn't a Copilot
auto-discovery location, so reuse is by reference (the agent or model reads the
file), not auto-load. To reuse a skill from any context, open or `#`-reference
its `SKILL.md`. (If you want native `/`-invokable reuse, mirror a skill as
`.github/prompts/<agent>.prompt.md`.)

## Fidelity gaps vs Claude Code (accepted in COPILOT-001)
- **R1, no programmatic sub-agent dispatch.** Claude's Jarvis invokes 18
  sub-agents via the Agent tool. Copilot has no equivalent, so `/jarvis` is a
  guided pipeline: it performs each stage inline and tells you which agent
  to switch to. It doesn't auto-spawn agents.
- **R2, standards are commit-time, not real-time.** There's no PostToolUse hook in
  Copilot. The `*.instructions.md` files guide generation; the real block happens
  at pre-commit and CI via `check_standards.py` (which reuses the Claude hook's
  rules). A bad file can exist locally until you try to commit it.
- **R3, inline eval (EVALS-002) doesn't port.** `evals/run_jarvis_eval.py` is a
  with/without-skill A/B that shells out to `claude -p`, so it's Claude-only. Under
  Copilot, use the `evals/<TICKET>/<agent>_eval.json` definitions as the rubric
  for what each agent should produce; run the automated A/B from Claude Code.

The spec-first / SME-approval gate applies on both platforms: no
implementation without an approved spec listing all changes.
