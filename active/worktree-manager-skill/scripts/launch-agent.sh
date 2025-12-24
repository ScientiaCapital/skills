#!/bin/bash
# launch-agent.sh - Launch Claude Code in a new Ghostty terminal for a worktree
#
# Usage: ./launch-agent.sh <worktree-path> [task-description]
#
# Examples:
#   ./launch-agent.sh ~/tmp/worktrees/my-project/feature-auth
#   ./launch-agent.sh ~/tmp/worktrees/my-project/feature-auth "Implement OAuth login"

set -e

WORKTREE_PATH="$1"
TASK="$2"

# Validate input
if [ -z "$WORKTREE_PATH" ]; then
    echo "Error: Worktree path required"
    echo "Usage: $0 <worktree-path> [task-description]"
    exit 1
fi

# Find script directory and config
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CONFIG_FILE="$SCRIPT_DIR/../config.json"

# Load config (with defaults)
if [ -f "$CONFIG_FILE" ] && command -v jq &> /dev/null; then
    TERMINAL=$(jq -r '.terminal // "ghostty"' "$CONFIG_FILE")
    SHELL_CMD=$(jq -r '.shell // "bash"' "$CONFIG_FILE")
    CLAUDE_CMD=$(jq -r '.claudeCommand // "claude --dangerously-skip-permissions"' "$CONFIG_FILE")
else
    TERMINAL="ghostty"
    SHELL_CMD="bash"
    CLAUDE_CMD="claude --dangerously-skip-permissions"
fi

# Note: CLAUDE_CMD defaults to "claude --dangerously-skip-permissions" for autonomous operation
# Users can customize in config.json (e.g., use an alias like "cc")

# Expand ~ in path
WORKTREE_PATH="${WORKTREE_PATH/#\~/$HOME}"

# Convert to absolute path if relative
if [[ "$WORKTREE_PATH" != /* ]]; then
    WORKTREE_PATH="$(pwd)/$WORKTREE_PATH"
fi

# Verify worktree exists
if [ ! -d "$WORKTREE_PATH" ]; then
    echo "Error: Worktree directory does not exist: $WORKTREE_PATH"
    exit 1
fi

# Verify it's a git worktree (has .git file or directory)
if [ ! -e "$WORKTREE_PATH/.git" ]; then
    echo "Error: Not a git worktree: $WORKTREE_PATH"
    exit 1
fi

# Get branch name
BRANCH=$(cd "$WORKTREE_PATH" && git branch --show-current 2>/dev/null || basename "$WORKTREE_PATH")

# Get project name from path
PROJECT=$(basename "$(dirname "$WORKTREE_PATH")")

# Build the command to run in the new terminal
# For fish: use 'and'/'or' instead of '&&'/'||'
if [ "$SHELL_CMD" = "fish" ]; then
    if [ -n "$TASK" ]; then
        INNER_CMD="cd '$WORKTREE_PATH'; and echo 'Worktree: $PROJECT / $BRANCH'; and echo 'Task: $TASK'; and echo ''; and $CLAUDE_CMD"
    else
        INNER_CMD="cd '$WORKTREE_PATH'; and echo 'Worktree: $PROJECT / $BRANCH'; and echo ''; and $CLAUDE_CMD"
    fi
else
    # bash/zsh syntax
    if [ -n "$TASK" ]; then
        INNER_CMD="cd '$WORKTREE_PATH' && echo 'Worktree: $PROJECT / $BRANCH' && echo 'Task: $TASK' && echo '' && $CLAUDE_CMD"
    else
        INNER_CMD="cd '$WORKTREE_PATH' && echo 'Worktree: $PROJECT / $BRANCH' && echo '' && $CLAUDE_CMD"
    fi
fi

# Launch based on terminal type
case "$TERMINAL" in
    ghostty)
        if ! command -v ghostty &> /dev/null && [ ! -d "/Applications/Ghostty.app" ]; then
            echo "Error: Ghostty not found"
            exit 1
        fi
        # Launch Ghostty with the command
        open -na "Ghostty.app" --args -e "$SHELL_CMD" -c "$INNER_CMD"
        ;;

    iterm2|iterm)
        osascript <<EOF
tell application "iTerm2"
    create window with default profile
    tell current session of current window
        write text "cd '$WORKTREE_PATH' && $CLAUDE_CMD"
    end tell
end tell
EOF
        ;;

    tmux)
        if ! command -v tmux &> /dev/null; then
            echo "Error: tmux not found"
            exit 1
        fi
        SESSION_NAME="wt-$PROJECT-$(echo "$BRANCH" | tr '/' '-')"
        tmux new-session -d -s "$SESSION_NAME" -c "$WORKTREE_PATH" "$SHELL_CMD -c '$CLAUDE_CMD'"
        echo "   tmux session: $SESSION_NAME (attach with: tmux attach -t $SESSION_NAME)"
        ;;

    wezterm)
        if ! command -v wezterm &> /dev/null; then
            echo "Error: WezTerm not found"
            exit 1
        fi
        wezterm start --cwd "$WORKTREE_PATH" -- "$SHELL_CMD" -c "$INNER_CMD"
        ;;

    kitty)
        if ! command -v kitty &> /dev/null; then
            echo "Error: Kitty not found"
            exit 1
        fi
        kitty --detach --directory "$WORKTREE_PATH" "$SHELL_CMD" -c "$INNER_CMD"
        ;;

    alacritty)
        if ! command -v alacritty &> /dev/null; then
            echo "Error: Alacritty not found"
            exit 1
        fi
        alacritty --working-directory "$WORKTREE_PATH" -e "$SHELL_CMD" -c "$INNER_CMD" &
        ;;

    *)
        echo "Error: Unknown terminal type: $TERMINAL"
        echo "Supported: ghostty, iterm2, tmux, wezterm, kitty, alacritty"
        exit 1
        ;;
esac

echo "✅ Launched Claude Code agent"
echo "   Terminal: $TERMINAL"
echo "   Project: $PROJECT"
echo "   Branch: $BRANCH"
echo "   Path: $WORKTREE_PATH"
if [ -n "$TASK" ]; then
    echo "   Task: $TASK"
fi
