---
description: "Project health snapshot — git, deps, tests, CLAUDE.md"
argument-hint: ""
allowed-tools: Bash, Read, Glob
---

# /status — Project Health Snapshot

! `git status --short 2>/dev/null | head -10`
! `git log --oneline -3 2>/dev/null`

## Instructions

Report this table and nothing else:

| Check | Status |
|-------|--------|
| Branch | `git branch --show-current` |
| Dirty files | count from `git status --short` |
| Last commit | age + message |
| CLAUDE.md | line count, or MISSING |
| init.sh | exists? executable? |
| .claude/rules/ | file count |
| tests/ | exists? |
| node_modules/.venv | installed? |
| .env/.env.local | present? |

If everything is green, say "All good." If issues, list them as bullet points.
