# Agent Evaluation Suite (EVALS-001)

Per-agent evaluations for the Jarvis pipeline, with a **with-skill vs
without-skill A/B** that measures how much the project's skills lift each agent's
performance. Built from the approved spec
[`specs/EVALS-001-agent-evaluations.md`](../specs/EVALS-001-agent-evaluations.md).

## Layout

```
evals/
├── README.md            ← this file
├── manifest.json        ← index of all 36 evals (ticket, agent, routed, with_skill)
├── PROJ-101/            ← 18 files: <agent>_eval.json   (ISSUE / P2)
└── PROJ-102/            ← 18 files: <agent>_eval.json   (FEATURE / P3)
```

One eval file per **agent × ticket**. Filenames start with the agent slug.

## Eval file schema

skill-creator's `evals.json` schema plus four additive metadata keys
(`ticket`, `agent`, `routed`, `with_skill`) that the runner ignores but this
suite uses to drive the A/B:

```json
{
  "skill_name": "design-agent",
  "ticket": "PROJ-101",
  "agent": "design-agent",
  "routed": true,
  "with_skill": ["spec-template"],
  "evals": [
    { "id": 1, "prompt": "...", "expected_output": "...",
      "files": ["tickets/PROJ-101.json", "specs/PROJ-101/PROJ-101.md"],
      "expectations": ["verifiable assertion", "..."] }
  ]
}
```

- **`routed`** mirrors the ticket's `triage.recommended_agents`. A routed agent's
  expectations test it performs its action; a non-routed agent's expectations
  test it correctly recognises it is out of scope.
- **`with_skill`** lists the skills enabled in the **with-skill arm only**. Only
  `design-agent` enables a skill (`spec-template`); every other agent is `[]`, so
  its delta documents the lift of repo context vs a bare baseline (expected ≈ 0 —
  itself a useful recorded result).

## How to run the with-skill / without-skill A/B

This is skill-creator's **capability-eval** workflow (executor + grader), not the
`run_eval.py` description-trigger benchmark. Harness lives at:

```
SC=~/.claude/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator
```

For one eval file (e.g. `evals/PROJ-101/design-agent_eval.json`):

1. **Spawn both arms in the same turn** — for each test case, launch two executor
   subagents at once:
   - **with-skill arm** → the skills in `with_skill` are available; save the
     transcript + output under `with_skill/outputs/`.
   - **baseline arm** → no skills available; same prompt; save under
     `without_skill/outputs/`.
   (Driven via the Agent tool / skill-creator's executor; the run dir is a
   temp/`evals/.runs/<ts>/` working directory, not committed.)
2. **Grade** each transcript against the eval's `expectations` with the grader
   agent (`$SC/agents/grader.md`) → `grading.json` (pass/fail + `pass_rate`).
3. **Build the review viewer** (with-skill version placed before its baseline):
   ```bash
   python $SC/eval-viewer/generate_review.py <run-dir> -o evals/.runs/<ts>/review.html
   ```
4. **Read the delta** = with-skill `pass_rate` − baseline `pass_rate`. That is the
   skill-lift for that agent.

Batch form: iterate `manifest.json`, run steps 1–3 per entry, then aggregate the
deltas. Default to a **small `runs-per-query` (e.g. 2–3)** first; scale up only
after a smoke run, since each eval is `2 arms × N runs` of live model calls.

> Smoke test first: run **`design-agent` / PROJ-101** (the one eval with a real
> `with_skill`) end-to-end and confirm the with-skill arm's `pass_rate` ≥ baseline
> before scaling to all 36.

## Notes / caveats

- **16 of 18 agents are stubs** (`triage-agent` and `design-agent` are the only
  implemented ones). Their evals test the structured "NOT IMPLEMENTED — would do
  X" response and routed/non-routed recognition; skill-lift reads ≈ 0 for them by
  design.
- **`run_eval.py` / `run_loop.py`** (`$SC/scripts/`) are a *separate* concern —
  they optimise a skill's *description* for trigger accuracy via `claude -p`, not
  the capability A/B above.
- The eval **definitions** are self-contained and harness-agnostic; only the run
  step depends on the installed skill-creator plugin.
- Rollback: this whole tree is additive — `rm -rf evals/` removes it with no
  source/data impact.
