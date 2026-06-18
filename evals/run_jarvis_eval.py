#!/usr/bin/env python3
"""EVALS-002 — inline evaluation runner invoked by /jarvis Stage 6.

For each agent that executed in a /jarvis run, run the with-skill vs
without-skill A/B (skill-creator methodology) using that agent's
evals/<TICKET>/<agent>_eval.json definition:

  * with-skill arm  : `claude -p ...`                         (project skills available)
  * baseline arm    : `claude -p ... --disable-slash-commands` (all skills disabled)
  * grade each arm  : a headless `claude -p` grader scores the transcript
                      against the eval's `expectations`.

It prints a final results table to the terminal, writes a detailed log
(INFO + EXCEPTION lines), a structured JSON results file, and appends one
summary line per agent to runtime/eval-runlog.jsonl.

Design rules (per spec EVALS-002):
  * NON-BLOCKING: every per-agent / per-arm failure is caught, logged as an
    EXCEPTION, recorded as status=error, and the run continues. Exit code is
    always 0 so it can never abort the /jarvis pipeline.
  * READ-ONLY executors: Write/Edit/NotebookEdit are disallowed and the system
    prompt instructs the executor to describe (not create) its artifact, so an
    eval run never mutates the repo.

Usage:
  python evals/run_jarvis_eval.py --ticket PROJ-101 \
         --agents triage-agent,design-agent,impact-analysis-agent,... \
         [--runs-per-query 1] [--timeout 180] [--model sonnet] [--dry-run]
"""
import argparse
import datetime
import json
import subprocess
import sys
import traceback
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent          # evals/ -> repo root
EVAL_DIR = REPO / "evals"
OUT_DIR_DEFAULT = REPO / "runtime" / "eval"
RUNLOG = REPO / "runtime" / "eval-runlog.jsonl"

EXEC_SYS = ("Evaluation mode: you are being evaluated. Work READ-ONLY: do not "
            "create, edit, or delete any file. Describe precisely the artifact "
            "and changes you would produce for this ticket.")


def _utc_iso() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _utc_stamp() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")


class Log:
    """Detailed INFO/EXCEPTION logger -> file + (optionally) stderr."""

    def __init__(self, path: Path, echo: bool = False):
        self.path = path
        self.echo = echo
        path.parent.mkdir(parents=True, exist_ok=True)
        self.fh = path.open("w")

    def _write(self, level: str, msg: str):
        line = f"{_utc_iso()} {level:<9} {msg}"
        self.fh.write(line + "\n")
        self.fh.flush()
        if self.echo:
            sys.stderr.write(line + "\n")

    def info(self, msg: str):
        self._write("INFO", msg)

    def exception(self, msg: str):
        self._write("EXCEPTION", msg)

    def close(self):
        self.fh.close()


# ---------------------------------------------------------------------------
# claude -p arms
# ---------------------------------------------------------------------------
def _claude(prompt, *, with_skill, model, timeout, executor):
    """Run a single headless claude -p call; return its `result` text."""
    cmd = ["claude", "-p", prompt, "--model", model, "--output-format", "json"]
    if executor:
        cmd += ["--add-dir", str(REPO),
                "--permission-mode", "bypassPermissions",
                "--disallowedTools", "Write", "Edit", "NotebookEdit",
                "--append-system-prompt", EXEC_SYS]
    else:  # grader needs no tools
        cmd += ["--disallowedTools", "Write", "Edit", "Bash", "Read", "Grep", "Glob"]
    if not with_skill:
        cmd.append("--disable-slash-commands")
    proc = subprocess.run(cmd, capture_output=True, text=True,
                          timeout=timeout, cwd=str(REPO))
    if proc.returncode != 0:
        raise RuntimeError(f"claude exited {proc.returncode}: {proc.stderr.strip()[:300]}")
    return json.loads(proc.stdout).get("result", "")


def _grade(transcript, expectations, *, model, timeout):
    rubric = "\n".join(f"- {e}" for e in expectations)
    gp = (
        "You are an evaluation grader. For each expectation decide whether the "
        "AGENT TRANSCRIPT satisfies it. Output ONLY strict JSON, no prose, no code "
        'fences: {"expectations":[{"text":"...","passed":true,"evidence":"..."}]}\n\n'
        f"AGENT TRANSCRIPT:\n{transcript[:12000]}\n\nEXPECTATIONS:\n{rubric}\n"
    )
    raw = _claude(gp, with_skill=False, model=model, timeout=timeout, executor=False)
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("```", 2)[1].lstrip("json").strip().rstrip("`").strip()
    g = json.loads(raw)
    exps = g.get("expectations", [])
    passed = sum(1 for x in exps if x.get("passed"))
    total = len(exps) or 1
    return passed / total, exps


def _arm(eval_obj, with_skill, *, model, timeout):
    """Run one arm (executor + grader), averaged over the eval's test cases."""
    rates, details = [], []
    for case in eval_obj["evals"]:
        transcript = _claude(case["prompt"], with_skill=with_skill,
                             model=model, timeout=timeout, executor=True)
        rate, exps = _grade(transcript, case["expectations"], model=model, timeout=timeout)
        rates.append(rate)
        details.append({"id": case["id"], "pass_rate": rate, "expectations": exps})
    return sum(rates) / len(rates), details


def _verdict(delta, err):
    if err:
        return "ERROR"
    if delta > 0.001:
        return "skill helps"
    if delta < -0.001:
        return "skill hurts"
    return "no lift"


# ---------------------------------------------------------------------------
# per-agent evaluation
# ---------------------------------------------------------------------------
def eval_agent(agent, ticket, *, runs, model, timeout, log, dry):
    res = {"agent": agent, "ticket": ticket, "with_pass": None,
           "base_pass": None, "delta": None, "status": "ok", "errors": [],
           "with_detail": None, "base_detail": None}
    path = EVAL_DIR / ticket / f"{agent}_eval.json"
    try:
        if not path.exists():
            raise FileNotFoundError(f"eval file not found: {path.relative_to(REPO)}")
        obj = json.loads(path.read_text())
        ws = obj.get("with_skill", [])
        log.info(f"{agent} loaded {path.relative_to(REPO)} with_skill={ws} "
                 f"expectations={len(obj['evals'][0]['expectations'])}")

        if dry:  # plumbing test: synthetic numbers, no model calls
            wp = 1.0 if agent == "design-agent" else 0.8
            bp = 0.6 if agent == "design-agent" else 0.8
            res["with_detail"] = res["base_detail"] = [{"id": 1, "note": "dry-run"}]
        else:
            wruns, bruns, wdet, bdet = [], [], None, None
            for i in range(runs):
                try:
                    r, d = _arm(obj, True, model=model, timeout=timeout)
                    wruns.append(r); wdet = d
                except Exception as e:
                    log.exception(f"{agent} arm=with run={i+1} {type(e).__name__}: {e}; continuing")
                    res["errors"].append(f"with:{type(e).__name__}")
                try:
                    r, d = _arm(obj, False, model=model, timeout=timeout)
                    bruns.append(r); bdet = d
                except Exception as e:
                    log.exception(f"{agent} arm=baseline run={i+1} {type(e).__name__}: {e}; continuing")
                    res["errors"].append(f"baseline:{type(e).__name__}")
            wp = sum(wruns) / len(wruns) if wruns else None
            bp = sum(bruns) / len(bruns) if bruns else None
            res["with_detail"], res["base_detail"] = wdet, bdet

        res["with_pass"], res["base_pass"] = wp, bp
        if wp is not None:
            log.info(f"{agent} arm=with     pass={wp:.2f}")
        if bp is not None:
            log.info(f"{agent} arm=baseline pass={bp:.2f}")
        if wp is not None and bp is not None:
            res["delta"] = round(wp - bp, 4)
            log.info(f"{agent} delta={res['delta']:+.2f} verdict={_verdict(res['delta'], False)}")
        if res["errors"]:
            res["status"] = "error"
    except Exception as e:
        res["status"] = "error"
        res["errors"].append(f"{type(e).__name__}: {e}")
        log.exception(f"{agent} {type(e).__name__}: {e}; recorded status=error; continuing")
        log.exception(f"{agent} traceback: {traceback.format_exc().splitlines()[-1]}")
    return res


# ---------------------------------------------------------------------------
# terminal table
# ---------------------------------------------------------------------------
def _fmt(v):
    return f"{v:.2f}" if isinstance(v, (int, float)) else "  — "


def print_table(ticket, results, log_path, json_path, runs):
    deltas = [r["delta"] for r in results if r["delta"] is not None]
    mean = sum(deltas) / len(deltas) if deltas else 0.0
    errors = sum(1 for r in results if r["status"] == "error")
    width = 64
    print("══ EVALUATION RESULTS — " + ticket + " " + "═" * max(0, width - 24 - len(ticket)))
    print(f"{'agent':<24}{'with':>6}{'base':>7}{'Δ':>8}   verdict")
    for r in results:
        d = r["delta"]
        dstr = f"{d:+.2f}" if d is not None else "  — "
        print(f"{r['agent']:<24}{_fmt(r['with_pass']):>6}{_fmt(r['base_pass']):>7}{dstr:>8}   {_verdict(d, r['status']=='error')}")
    print("─" * width)
    print(f"agents={len(results)}  mean Δ={mean:+.2f}  errors={errors}  runs/query={runs}")
    print(f"log:     {log_path.relative_to(REPO)}")
    print(f"results: {json_path.relative_to(REPO)}")


# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description="Inline /jarvis evaluation runner (EVALS-002)")
    ap.add_argument("--ticket", required=True)
    ap.add_argument("--agents", required=True, help="comma-separated agent slugs that ran this route")
    ap.add_argument("--runs-per-query", type=int, default=1)
    ap.add_argument("--timeout", type=int, default=180)
    ap.add_argument("--model", default="sonnet")
    ap.add_argument("--out-dir", default=str(OUT_DIR_DEFAULT))
    ap.add_argument("--dry-run", action="store_true", help="skip claude calls; synthetic results (plumbing test)")
    ap.add_argument("--verbose", action="store_true", help="also echo log lines to stderr")
    args = ap.parse_args()

    agents = [a.strip() for a in args.agents.split(",") if a.strip()]
    out_dir = Path(args.out_dir)
    stamp = _utc_stamp()
    log_path = out_dir / f"{args.ticket}_{stamp}.log"
    json_path = out_dir / f"{args.ticket}_{stamp}.json"

    log = Log(log_path, echo=args.verbose)
    log.info(f"run start ticket={args.ticket} agents={len(agents)} "
             f"runs_per_query={args.runs_per_query} dry_run={args.dry_run} model={args.model}")

    results = []
    for agent in agents:
        results.append(eval_agent(agent, args.ticket, runs=args.runs_per_query,
                                  model=args.model, timeout=args.timeout, log=log, dry=args.dry_run))

    # structured results + runlog
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(
        {"ticket": args.ticket, "ts": _utc_iso(), "runs_per_query": args.runs_per_query,
         "dry_run": args.dry_run, "results": results}, indent=2) + "\n")
    with RUNLOG.open("a") as f:
        for r in results:
            f.write(json.dumps({
                "ticket": r["ticket"], "agent": r["agent"],
                "with_pass": r["with_pass"], "base_pass": r["base_pass"],
                "delta": r["delta"], "status": r["status"],
                "errors": r["errors"], "runs_per_query": args.runs_per_query,
                "ts": _utc_iso(), "log": str(log_path.relative_to(REPO)),
            }) + "\n")

    errors = sum(1 for r in results if r["status"] == "error")
    deltas = [r["delta"] for r in results if r["delta"] is not None]
    mean = sum(deltas) / len(deltas) if deltas else 0.0
    log.info(f"run complete agents={len(results)} mean_delta={mean:+.4f} errors={errors}")
    log.close()

    print_table(args.ticket, results, log_path, json_path, args.runs_per_query)
    sys.exit(0)  # NON-BLOCKING: never fail the pipeline


if __name__ == "__main__":
    main()
