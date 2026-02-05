# System Notifications Reference

Enable notifications to know when Claude agents need attention or complete tasks.

## iTerm2 Notification Setup

### Step 1: Enable Idle Notifications

1. Open iTerm2 → Preferences (Cmd+,)
2. Go to Profiles → Terminal
3. Check "Notification Center" section:
   - Enable **"Send notification when idle"**
   - Set threshold to **30 seconds** (configurable)

This notifies you when a terminal session stops producing output for 30 seconds - typically meaning Claude is waiting for input or has finished.

### Step 2: Enable Bell Notifications (Optional)

In the same Profiles → Terminal section:

- Enable **"Notification Center bell"**
- This triggers on any `\a` (bell) character

### Step 3: Shell Integration (Recommended)

Install iTerm2 shell integration for richer notifications:

```bash
# Add to ~/.zshrc or ~/.bashrc
curl -L https://iterm2.com/shell_integration/bash -o ~/.iterm2_shell_integration.bash
source ~/.iterm2_shell_integration.bash

# Or for zsh:
curl -L https://iterm2.com/shell_integration/zsh -o ~/.iterm2_shell_integration.zsh
source ~/.iterm2_shell_integration.zsh
```

## Manual Attention Functions

Add these to your shell config (`~/.zshrc` or `~/.bashrc`):

```bash
# Request attention with fireworks animation
it2attention() {
    printf "\e]1337;RequestAttention=fireworks\a"
}

# Request attention with bounce
it2bounce() {
    printf "\e]1337;RequestAttention=yes\a"
}

# Clear attention request
it2clear() {
    printf "\e]1337;RequestAttention=no\a"
}

# Notify with custom message (macOS)
notify() {
    local message="${1:-Task complete}"
    osascript -e "display notification \"$message\" with title \"Claude Agent\""
}

# Notify when a command completes
# Usage: long-command; done-notify "Build complete"
done-notify() {
    local status=$?
    local message="${1:-Command finished}"
    if [ $status -eq 0 ]; then
        osascript -e "display notification \"$message\" with title \"Success\""
    else
        osascript -e "display notification \"$message (exit $status)\" with title \"Failed\""
    fi
    return $status
}
```

## Usage with Worktrees

### Notify on Worktree Completion

Add to your worktree agent's task file:

```markdown
## When Done

1. Commit your changes
2. Run: `notify "Worktree task complete: feature/auth"`
3. Or just wait - idle notification will trigger after 30s
```

### Automated Completion Notification

Add to the end of `WORKTREE_TASK.md`:

```markdown
## Completion Signal

When all acceptance criteria are met, run:
```bash
it2attention && notify "Ready for review: $BRANCH"
```
```

## macOS Focus Modes Integration

### Do Not Disturb Awareness

iTerm2 notifications respect macOS Focus modes:

- **Work Focus**: Notifications delivered normally
- **Do Not Disturb**: Notifications silenced, delivered later
- **Personal Focus**: Configure per-app settings

### Focus-Aware Notification Script

```bash
# Check if Focus mode is active before notifying
smart_notify() {
    local message="$1"
    # Check if DND is active (requires macOS 12+)
    local dnd_active=$(defaults read com.apple.controlcenter "NSStatusItem Visible FocusModes" 2>/dev/null)

    if [ "$dnd_active" = "1" ]; then
        # Still notify - macOS handles delivery
        osascript -e "display notification \"$message\" with title \"Claude Agent\""
    else
        # Full attention request
        it2attention
        osascript -e "display notification \"$message\" with title \"Claude Agent\" sound name \"Ping\""
    fi
}
```

## Ghostty Notifications

Ghostty doesn't have built-in idle notifications like iTerm2, but you can:

### Option 1: Use macOS Notifications Directly

```bash
# Add to the end of agent tasks
osascript -e 'display notification "Agent complete" with title "Ghostty"'
```

### Option 2: Terminal Bell

```bash
# Ring the bell (if configured in Ghostty)
echo -e "\a"
```

### Option 3: External Monitoring

```bash
# In another terminal, watch for completion signals
tail -f /tmp/agent-*.log | grep -q "COMPLETE" && notify "Agent done"
```

## tmux Notifications

For detached tmux sessions:

```bash
# Monitor tmux session and notify when idle
tmux_watch() {
    local session="$1"
    local timeout="${2:-60}"

    while true; do
        # Check if session still has activity
        local last_activity=$(tmux display -p -t "$session" '#{session_activity}')
        local now=$(date +%s)
        local idle=$((now - last_activity))

        if [ $idle -gt $timeout ]; then
            notify "tmux session '$session' idle for ${idle}s"
            break
        fi
        sleep 10
    done
}
```

## Notification Summary

| Terminal | Idle Notification | Manual Attention | Best For |
|----------|-------------------|------------------|----------|
| iTerm2 | Built-in (30s configurable) | `it2attention` | Parallel monitored work |
| Ghostty | External script | `osascript` | Quick interactive work |
| tmux | Custom watcher | `osascript` | Background autonomous |
| Terminal.app | None | `osascript` | Basic fallback |
