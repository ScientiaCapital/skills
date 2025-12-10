# Smart Project Context Loader - Design Document

**Date**: 2025-11-30
**Status**: Approved
**Problem**: Global skill stores project-specific data, causing cross-contamination across 50+ projects

---

## Solution

Separate **instructions** (global skill) from **data** (per-project file).

```
~/.claude/skills/project-context-skill/SKILL.md  →  Instructions only
<project>/.claude/PROJECT_CONTEXT.md             →  Project-specific data
```

---

## Context File Format

```markdown
# <project-name>

**Branch**: main | **Updated**: 2025-11-30 14:32

## Status
<current state in 2-3 lines>

## Today's Focus
1. [ ] Task one
2. [ ] Task two

## Done (This Session)
- (populated on session end)

## Blockers
(none or list)

## Quick Commands
```bash
<common commands for this project>
```

## Tech Stack
<single line: Python 3.11 | FastAPI | PostgreSQL>
```

---

## Lifecycle

### Session Start

1. Detect working directory
2. Load `<pwd>/.claude/PROJECT_CONTEXT.md`
3. Verify against actual state:
   - `git status` - current branch, modified files
   - `git log --oneline -5` - recent commits
4. Flag outdated info (TODO marked done in commits)
5. Display clean, verified context

### No Context Exists

Auto-generate from:
- `.claude/CLAUDE.md` or `CLAUDE.md`
- `git log --oneline -5`
- `git status`
- `package.json` / `requirements.txt`

### Session End

Trigger: user says "done", "end session", or runs `/save-context`

1. Move completed tasks to "Done (This Session)"
2. Update status based on commits made
3. Preserve untouched focus items
4. Clear previous session's done list
5. Write updated PROJECT_CONTEXT.md

---

## Implementation Tasks

1. Rewrite SKILL.md as instruction-only loader
2. Create auto-generation logic (read CLAUDE.md, git state)
3. Add verification logic (cross-check TODOs vs commits)
4. Add session-end update protocol
5. Test on sales-agent and swaggy-stacks projects

---

## Files Changed

| File | Action |
|------|--------|
| `~/.claude/skills/project-context-skill/SKILL.md` | Rewrite (instructions only) |
| `<each-project>/.claude/PROJECT_CONTEXT.md` | Create (auto-generated) |

---

## Success Criteria

- Opening sales-agent shows sales-agent context (not SwaggyStacks)
- Opening swaggy-stacks shows swaggy-stacks context
- New projects auto-generate context on first load
- Stale TODOs flagged when commits show completion
- Session work tracked and persisted
