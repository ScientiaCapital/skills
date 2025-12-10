---
name: project-context-skill
description: |
  Maintains project context and progress tracking across Claude Code sessions.
  Activates at session start to load context, and on session end to save progress.
  Keywords: context, session, save, done, end session
---

# Project Context Loader

## On Session Start

Execute immediately when starting work on any project:

### 1. Identify Project
```bash
pwd  # Get current working directory
```

### 2. Load Context
Look for: `<pwd>/.claude/PROJECT_CONTEXT.md`

- **If exists**: Read it, verify against git state, display to user
- **If missing**: Auto-generate from CLAUDE.md, git log, and package files

### 3. Verify Against Git
```bash
git status            # Current branch, modified files
git log --oneline -5  # Recent commits
```

Flag discrepancies:
- TODO marked done in commits? → Move to "Done"
- Branch changed? → Update context
- Stale info? → Remove it

## On Session End

Triggers: "done", "end session", "save context", "/save-context"

1. Review conversation for completed work
2. Update PROJECT_CONTEXT.md:
   - Move completed TODOs to "Done (This Session)"
   - Update Status based on commits made
   - Preserve untouched Focus items
   - Clear previous session's Done list
3. Show user the updated context

## Auto-Generate Context

When no PROJECT_CONTEXT.md exists, create from:

1. `.claude/CLAUDE.md` or `CLAUDE.md` (project docs)
2. `git log --oneline -5` (recent activity)
3. `git status` (current state)
4. `package.json` / `pyproject.toml` / `requirements.txt` (tech stack)

Write to: `<pwd>/.claude/PROJECT_CONTEXT.md`

## Context File Format

See `reference/template.md` for full template with examples.

Quick format:
```markdown
# <project-name>

**Branch**: <branch> | **Updated**: <date>

## Status
<2-3 sentences: current state>

## Today's Focus
1. [ ] <task>
2. [ ] <task>

## Done (This Session)
- <populated on session end>

## Blockers
<none or list>

## Tech Stack
<single line: Python 3.11 | FastAPI | PostgreSQL>
```

## Key Rules

- **Never store project data in this SKILL.md file**
- **Always use `<pwd>/.claude/PROJECT_CONTEXT.md` for project data**
- **One project = one context file (no cross-contamination)**
- **Verify context against git state on every load**
- **Keep context concise and actionable for team pickup**
