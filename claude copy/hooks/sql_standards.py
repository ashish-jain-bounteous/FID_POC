#!/usr/bin/env python3
"""PostToolUse hook: enforce simple SQL / Python standards.

Runs after Write|Edit. Reads the hook payload from stdin (JSON), inspects the
target file, and checks .sql / .py files against the project standards. On a
hard violation it exits 2 with a message on stderr so the agent self-corrects;
warnings are advisory (exit 0 with a note). Non-.sql/.py files are ignored.

This is how the framework "applies simple standards and instructions that run
after the described agents (including Triage)".
"""
import json
import os
import re
import sys

APPROVED_PREFIXES = ("DIM_", "FCT_", "STG_", "VW_", "HUB_", "LNK_", "SAT_", "SEQ_")
CREATE_OBJECT_RE = re.compile(
    r"CREATE\s+(?:OR\s+REPLACE\s+)?(?:TABLE|VIEW)\s+([A-Z0-9_\.\"]+)", re.IGNORECASE
)
SECRET_RE = re.compile(
    r"(password|passwd|secret|api[_-]?key|aws_secret|private_key)\s*[:=]\s*['\"][^'\"]+['\"]",
    re.IGNORECASE,
)


def read_payload():
    try:
        return json.load(sys.stdin)
    except Exception:
        return {}


def target_path(payload):
    ti = payload.get("tool_input") or {}
    return ti.get("file_path") or ti.get("path") or ""


def object_short_name(qualified):
    name = qualified.strip().strip('"')
    if "." in name:
        name = name.split(".")[-1].strip('"')
    return name.upper()


def check_sql(text):
    errors, warnings = [], []

    # 1. approved object prefixes on CREATE TABLE/VIEW
    for m in CREATE_OBJECT_RE.finditer(text):
        short = object_short_name(m.group(1))
        if not short.startswith(APPROVED_PREFIXES):
            errors.append(
                f"object '{short}' must use an approved prefix "
                f"({', '.join(APPROVED_PREFIXES)})"
            )

    # 2. ban SELECT *
    if re.search(r"SELECT\s+\*", text, re.IGNORECASE):
        errors.append("`SELECT *` is not allowed; list columns explicitly")

    # 3. required header block
    for tag in ("-- Object:", "-- Owner:", "-- Ticket:"):
        if tag not in text:
            errors.append(f"missing required header line '{tag}'")

    # 4. UPPER_SNAKE_CASE for created object names
    for m in CREATE_OBJECT_RE.finditer(text):
        short = object_short_name(m.group(1))
        if not re.fullmatch(r"[A-Z0-9_]+", short):
            warnings.append(f"object '{short}' should be UPPER_SNAKE_CASE")

    # 5. secrets
    if SECRET_RE.search(text):
        errors.append("possible hard-coded credential/secret detected")

    return errors, warnings


def check_python(text):
    errors, warnings = [], []
    stripped = text.lstrip()
    if not (stripped.startswith('"""') or stripped.startswith("'''")):
        warnings.append("module is missing a docstring")
    if re.search(r"^\s*print\(", text, re.MULTILINE):
        warnings.append("debug `print(` found; prefer logging")
    if SECRET_RE.search(text):
        errors.append("possible hard-coded credential/secret detected")
    return errors, warnings


def main():
    payload = read_payload()
    path = target_path(payload)
    if not path or not os.path.exists(path):
        sys.exit(0)

    ext = os.path.splitext(path)[1].lower()
    if ext not in (".sql", ".py"):
        sys.exit(0)

    try:
        with open(path, "r", encoding="utf-8") as fh:
            text = fh.read()
    except Exception:
        sys.exit(0)

    errors, warnings = check_sql(text) if ext == ".sql" else check_python(text)

    label = os.path.basename(path)
    if warnings:
        sys.stderr.write(
            "[sql_standards] WARNINGS in %s:\n  - %s\n"
            % (label, "\n  - ".join(warnings))
        )
    if errors:
        sys.stderr.write(
            "[sql_standards] STANDARDS VIOLATION in %s - please fix:\n  - %s\n"
            % (label, "\n  - ".join(errors))
        )
        sys.exit(2)  # non-zero blocks and feeds the message back to the agent

    sys.exit(0)


if __name__ == "__main__":
    main()
