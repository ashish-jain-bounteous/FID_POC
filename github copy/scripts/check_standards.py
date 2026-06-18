#!/usr/bin/env python3
"""Standards checker for pre-commit / CI (COPILOT-001).

GitHub Copilot has no PostToolUse hook, so this CLI replaces the real-time gate
with a commit-time / CI gate. It REUSES the exact rule logic from the Claude
hook `.claude/hooks/sql_standards.py` (single source of truth - imported, not
copied), and applies it to a list of files passed as arguments.

Usage:
  python .github/scripts/check_standards.py FILE [FILE ...]
  git diff --name-only --cached -- '*.sql' '*.py' | xargs python .github/scripts/check_standards.py

Exit code: 0 if all clean (warnings allowed), 1 if any .sql/.py file has a hard
violation. Non-.sql/.py files are ignored.
"""
import os
import sys
from pathlib import Path

# Import the rule functions from the Claude hook (keeps rules single-source).
REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / ".claude" / "hooks"))
try:
    from sql_standards import check_sql, check_python  # noqa: E402
except Exception as exc:  # pragma: no cover
    sys.stderr.write(f"[check_standards] cannot import rule logic from "
                     f".claude/hooks/sql_standards.py: {exc}\n")
    sys.exit(1)


def check_file(path: str):
    ext = os.path.splitext(path)[1].lower()
    if ext not in (".sql", ".py") or not os.path.exists(path):
        return [], []
    try:
        text = Path(path).read_text(encoding="utf-8")
    except Exception as exc:
        return [f"could not read file: {exc}"], []
    return (check_sql(text) if ext == ".sql" else check_python(text))


def main(argv):
    if not argv:
        return 0
    had_error = False
    for path in argv:
        errors, warnings = check_file(path)
        label = os.path.basename(path)
        if warnings:
            sys.stderr.write("[check_standards] WARNINGS in %s:\n  - %s\n"
                             % (label, "\n  - ".join(warnings)))
        if errors:
            had_error = True
            sys.stderr.write("[check_standards] STANDARDS VIOLATION in %s:\n  - %s\n"
                             % (label, "\n  - ".join(errors)))
    if had_error:
        sys.stderr.write("[check_standards] commit blocked - fix the violations above.\n")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
