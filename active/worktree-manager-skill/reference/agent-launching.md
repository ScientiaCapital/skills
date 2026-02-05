# Agent Launching Reference

## Required Defaults

**CRITICAL**: These settings MUST be used when launching agents in worktrees:

- **Terminal**: Configurable (Ghostty recommended, iTerm2 for notifications)
- **Model**: Opus 4.5 (`--model opus` or full ID `claude-opus-4-5-20251101`)
- **Flags**: `--dangerously-skip-permissions` (required for autonomous operation)

## Terminal Selection Guide

| Use Case | Terminal | Why |
|----------|----------|-----|
| Quick dev work | Ghostty | Fast, clean UI |
| Parallel with notifications | iTerm2 | Numbered tabs + idle alerts |
| Background autonomous | tmux | Detached, resumable |
| CI/automation | tmux | Headless operation |

## Standard Launch Command

```bash
# Short form (recommended)
ghostty --title="[1] project - branch" -e "cd {worktree_path} && claude --model opus --dangerously-skip-permissions"

# Full model ID (for pinning to specific version)
ghostty --title="[1] project - branch" -e "cd {worktree_path} && claude --model claude-opus-4-5-20251101 --dangerously-skip-permissions"
```

## Terminal-Specific Commands

### Ghostty (Recommended for Quick Work)

```bash
# Create a temp script for reliable execution
TEMP_SCRIPT=$(mktemp /tmp/worktree-launch.XXXXXX.sh)
TAB_NUM=$(cat /tmp/worktree-tab-counter 2>/dev/null || echo 1)
cat > "$TEMP_SCRIPT" << SCRIPT
#!/bin/bash
cd '$WORKTREE_PATH'
exec claude --model opus --dangerously-skip-permissions
SCRIPT
chmod +x "$TEMP_SCRIPT"
open -na "Ghostty.app" --args --title="[$TAB_NUM] $PROJECT - $BRANCH" -e "$TEMP_SCRIPT"
```

### iTerm2 (Recommended for Parallel Sessions)

```bash
TAB_NUM=$(cat /tmp/worktree-tab-counter 2>/dev/null || echo 1)
osascript <<EOF
tell application "iTerm2"
    activate
    create window with default profile
    tell current session of current window
        set name to "[$TAB_NUM] $PROJECT - $BRANCH"
        write text "cd '$WORKTREE_PATH' && claude --model opus --dangerously-skip-permissions"
    end tell
end tell
EOF
```

### macOS Terminal.app

```bash
osascript -e 'tell application "Terminal" to do script "cd '"$WORKTREE_PATH"' && claude --model opus --dangerously-skip-permissions"'
```

### tmux (For Background/Autonomous Work)

```bash
tmux new-session -d -s "wt-$PROJECT-$BRANCH_SLUG" -c "$WORKTREE_PATH" \
  "bash -c 'claude --model opus --dangerously-skip-permissions'"
```

## Numbered Tabs (Boris Cherny Workflow)

For parallel development, use numbered tabs to track multiple sessions:

### How It Works

1. A counter file at `/tmp/worktree-tab-counter` tracks the next tab number
2. Each launch increments the counter and uses `[$N]` prefix
3. Counter resets on system reboot (file lives in `/tmp/`)
4. Manual reset: `rm /tmp/worktree-tab-counter`

### Tab Naming Convention

```
[1] project-name - feature/branch
[2] project-name - fix/other-branch
[3] another-project - main
```

### Manual Tab Number Management

```bash
# Check current tab number
cat /tmp/worktree-tab-counter

# Reset to start at 1
rm /tmp/worktree-tab-counter

# Set specific number
echo "5" > /tmp/worktree-tab-counter
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

## Model Options

| Option | When to Use |
|--------|-------------|
| `--model opus` | Default choice, always gets latest Opus 4.5 |
| `--model claude-opus-4-5-20251101` | Pin to specific version for reproducibility |

## Why These Defaults Matter

| Setting | Reason |
|---------|--------|
| Terminal auto-detect | Launches in whatever terminal you're using |
| Opus 4.5 | Most capable model for autonomous work |
| `--dangerously-skip-permissions` | Required for autonomous file operations |
| Numbered tabs | Track multiple parallel sessions (Boris workflow) |
