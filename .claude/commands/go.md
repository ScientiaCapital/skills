---
description: "Quick start — deps check, git state, last commits. 30 seconds."
argument-hint: ""
allowed-tools: Read, Bash, Glob
---

# /go — Quick Start

! `echo "=== $(basename $(pwd)) ==="`
! `git status --short 2>/dev/null | head -5`
! `git log --oneline -5 2>/dev/null`

## Instructions

1. Show the output above (git status + recent commits)
2. Check environment health (10 seconds max):
   - `package.json` exists but no `node_modules`? → say "Run `./init.sh`"
   - `requirements.txt` exists but no `.venv`? → say "Run `./init.sh`"
   - `.env.local` or `.env` missing? → say which env file is needed
3. Read `CLAUDE.md` silently for project context
4. Say: "Ready. What are we working on?"

That's it. No observers, no sprint plan, no ceremony. Just context and go.
