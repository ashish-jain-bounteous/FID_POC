---
applyTo: "**/*.py"
description: "Python standards (mirrors .claude/hooks/sql_standards.py check_python)."
---

# Python standards

When you write or edit any `.py` file, keep these rules in mind:

1. **Module docstring.** Start the module with a `"""triple-quoted"""` docstring
   describing what it does.
2. **No debug `print(`.** Prefer the `logging` module over `print` for runtime
   output.
3. **No hard-coded secrets.** Keep passwords, API keys, and private keys out of source.

These are checked at commit time by `.github/scripts/check_standards.py`
(secrets are a hard error; a missing docstring or `print` are warnings). Match the
style of the existing scripts under `evals/`.
