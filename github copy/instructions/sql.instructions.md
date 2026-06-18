---
applyTo: "**/*.sql"
description: "SQL standards for the Snowflake data platform (mirrors .claude/hooks/sql_standards.py)."
---

# SQL Standards

When you write or edit SQL files, keep these rules in mind. They're checked at commit time by `.github/scripts/check_standards.py`, so violations will block your commit.

1. Use the right prefix for object names. Start every `CREATE [OR REPLACE] TABLE|VIEW` with one of these: `DIM_`, `FCT_`, `STG_`, `VW_`, `HUB_`, `LNK_`, `SAT_`, or `SEQ_`.

2. Use `UPPER_SNAKE_CASE` for object names (letters, digits, underscores only).

3. Include a header block. Every file needs these comment lines: `-- Object:`, `-- Owner:`, and `-- Ticket:`. A `-- Description:` line is nice to have too.

4. List columns explicitly. Don't use `SELECT *`.

5. No hard-coded secrets. Keep passwords, API keys, and private keys out of source files.

Also, match the style of existing files in `snowflake/`. For SCD-2 dimensions, filter joins to the current row with `AND <dim>.IS_CURRENT = TRUE`. For dedup guards, use NULL-safe `NOT EXISTS (...)` instead of `NOT IN (...)`
