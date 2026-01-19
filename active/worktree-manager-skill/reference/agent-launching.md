# Agent Launching Reference

## Required Defaults

**CRITICAL**: These settings MUST be used when launching agents in worktrees:

- **Terminal**: Ghostty (ALWAYS use Ghostty)
- **Model**: Opus 4.5 (`claude-opus-4-5-20251101` or shorthand `opus`)
- **Flags**: `--dangerously-skip-permissions` (required for autonomous operation)

## Standard Launch Command

```bash
ghostty -e "cd {worktree_path} && claude --model claude-opus-4-5-20251101 --dangerously-skip-permissions"
```

## Terminal-Specific Commands

### Ghostty (Recommended)

```bash
# Create a temp script for reliable execution
TEMP_SCRIPT=$(mktemp /tmp/worktree-launch.XXXXXX.sh)
cat > "$TEMP_SCRIPT" << SCRIPT
#!/bin/bash
cd '$WORKTREE_PATH'
exec claude --model claude-opus-4-5-20251101 --dangerously-skip-permissions
SCRIPT
chmod +x "$TEMP_SCRIPT"
open -na "Ghostty.app" --args -e "$TEMP_SCRIPT"
```

### macOS Terminal.app

```bash
osascript -e 'tell application "Terminal" to do script "cd '"$WORKTREE_PATH"' && claude --model claude-opus-4-5-20251101 --dangerously-skip-permissions"'
```

### iTerm2

```bash
osascript -e 'tell application "iTerm2" to create window with default profile' \
  -e 'tell application "iTerm2" to tell current session of current window to write text "cd '"$WORKTREE_PATH"' && claude --model claude-opus-4-5-20251101 --dangerously-skip-permissions"'
```

### tmux

```bash
tmux new-session -d -s "wt-$PROJECT-$BRANCH_SLUG" -c "$WORKTREE_PATH" \
  "bash -c 'claude --model claude-opus-4-5-20251101 --dangerously-skip-permissions'"
```

## WORKTREE_TASK.md Auto-Loading

Each worktree should have a `WORKTREE_TASK.md` file at its root. When an agent launches, it automatically reads this file to understand its task.

### Template

```markdown
# Worktree Task: [branch-name]

**Project:** [project-name]
**Branch:** [branch]
**Ports:** [port1], [port2]
**Created:** [timestamp]

---

## Your Task

[Detailed task description with specific deliverables]

## Acceptance Criteria

- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

## Context

[Any relevant context, links to docs, or constraints]

## When Done

1. Commit your changes with conventional commit message
2. Run tests: `npm run test` or equivalent
3. Update this file to check off completed criteria
4. Notify: Task complete, ready for code review
```

### Creating WORKTREE_TASK.md

```bash
cat > "$WORKTREE_PATH/WORKTREE_TASK.md" << 'EOF'
# Worktree Task: feature/auth

**Project:** my-project
**Branch:** feature/auth
**Ports:** 8100, 8101
**Created:** 2025-12-30T10:00:00Z

---

## Your Task

Implement OAuth login with Google and GitHub providers.

## Acceptance Criteria

- [ ] Google OAuth working
- [ ] GitHub OAuth working
- [ ] Session persists across page refresh
- [ ] Logout clears session

## When Done

1. Commit with `feat(auth): add OAuth login`
2. Run `npm run test`
3. Ready for code review
EOF
```

## Why These Defaults Matter

| Setting | Reason |
|---------|--------|
| Ghostty | Required terminal for agent launching |
| Opus 4.5 | Most capable model for autonomous work |
| `--dangerously-skip-permissions` | Required for autonomous file operations |
