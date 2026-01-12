#!/bin/bash
# launch-agent.sh - Launch Claude Code in a new terminal for a worktree
# Auto-detects terminal: opens in whatever terminal you started your day with

set -e

WORKTREE_PATH="$1"
TASK="$2"
OVERRIDE_TERMINAL=""

shift 2 2>/dev/null || true
while [[ $# -gt 0 ]]; do
    case $1 in
        --terminal) OVERRIDE_TERMINAL="$2"; shift 2 ;;
        *) shift ;;
    esac
done

if [ -z "$WORKTREE_PATH" ]; then
    echo "Usage: $0 <worktree-path> [task] [--terminal <type>]"
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CONFIG_FILE="$SCRIPT_DIR/../config.json"

if [ -f "$CONFIG_FILE" ] && command -v jq &> /dev/null; then
    CONFIG_TERMINAL=$(jq -r '.terminal // "ghostty"' "$CONFIG_FILE")
    SHELL_CMD=$(jq -r '.shell // "bash"' "$CONFIG_FILE")
    CLAUDE_CMD=$(jq -r '.claudeCommand // "claude --dangerously-skip-permissions"' "$CONFIG_FILE")
else
    CONFIG_TERMINAL="ghostty"
    SHELL_CMD="bash"
    CLAUDE_CMD="claude --dangerously-skip-permissions"
fi

detect_active_terminal() {
    [ -n "$ITERM_SESSION_ID" ] && echo "iterm2" && return
    [ -n "$GHOSTTY_RESOURCES_DIR" ] || [ "$TERM_PROGRAM" = "ghostty" ] && echo "ghostty" && return
    [ -n "$WEZTERM_PANE" ] && echo "wezterm" && return
    [ -n "$KITTY_WINDOW_ID" ] && echo "kitty" && return
    [ "$TERM_PROGRAM" = "Alacritty" ] && echo "alacritty" && return
    [ -n "$TMUX" ] && echo "tmux" && return
    [ "$TERM_PROGRAM" = "Apple_Terminal" ] && echo "terminal" && return
    echo "$CONFIG_TERMINAL"
}

if [ -n "$OVERRIDE_TERMINAL" ]; then
    TERMINAL="$OVERRIDE_TERMINAL"
    echo "🖥️  Terminal: $TERMINAL (explicit override)"
else
    TERMINAL=$(detect_active_terminal)
    [ "$TERMINAL" != "$CONFIG_TERMINAL" ] && echo "🖥️  Terminal: $TERMINAL (auto-detected)" || echo "🖥️  Terminal: $TERMINAL (from config)"
fi

WORKTREE_PATH="${WORKTREE_PATH/#\~/$HOME}"
[[ "$WORKTREE_PATH" != /* ]] && WORKTREE_PATH="$(pwd)/$WORKTREE_PATH"

[ ! -d "$WORKTREE_PATH" ] && echo "Error: Directory not found: $WORKTREE_PATH" && exit 1
[ ! -e "$WORKTREE_PATH/.git" ] && echo "Error: Not a git worktree: $WORKTREE_PATH" && exit 1

BRANCH=$(cd "$WORKTREE_PATH" && git branch --show-current 2>/dev/null || basename "$WORKTREE_PATH")
PROJECT=$(basename "$(dirname "$WORKTREE_PATH")")

case "$TERMINAL" in
    ghostty)
        if [ -d "/Applications/Ghostty.app" ]; then
            TEMP_SCRIPT=$(mktemp /tmp/worktree-launch.XXXXXX.sh)
            cat > "$TEMP_SCRIPT" << SCRIPT
#!/bin/bash
cd '$WORKTREE_PATH'
echo '🌳 Worktree: $PROJECT / $BRANCH'
echo '📋 Task: $TASK'
echo ''
exec $CLAUDE_CMD
SCRIPT
            chmod +x "$TEMP_SCRIPT"
            open -na "Ghostty.app" --args -e "$TEMP_SCRIPT"
            (sleep 5 && rm -f "$TEMP_SCRIPT") &
        else
            echo "Ghostty not found, falling back to Terminal.app"
            osascript -e "tell application \"Terminal\" to do script \"cd '$WORKTREE_PATH' && $CLAUDE_CMD\""
        fi
        ;;
    iterm2|iterm)
        osascript <<EOF
tell application "iTerm2"
    activate
    create window with default profile
    tell current session of current window
        set name to "🌳 $PROJECT / $BRANCH"
        write text "cd '$WORKTREE_PATH' && echo '🌳 Worktree: $PROJECT / $BRANCH' && echo '📋 Task: $TASK' && echo '' && $CLAUDE_CMD"
    end tell
end tell
EOF
        ;;
    terminal|terminal.app|mac)
        osascript -e "tell application \"Terminal\" to do script \"cd '$WORKTREE_PATH' && echo 'Worktree: $PROJECT / $BRANCH' && $CLAUDE_CMD\""
        ;;
    tmux)
        SESSION_NAME="wt-$PROJECT-$(echo "$BRANCH" | tr '/' '-')"
        tmux new-session -d -s "$SESSION_NAME" -c "$WORKTREE_PATH" "$SHELL_CMD -c '$CLAUDE_CMD'"
        echo "   tmux session: $SESSION_NAME"
        ;;
    *) echo "Error: Unknown terminal: $TERMINAL"; exit 1 ;;
esac

echo "✅ Launched Claude Code agent"
echo "   Project: $PROJECT | Branch: $BRANCH"
echo "   Path: $WORKTREE_PATH"
[ -n "$TASK" ] && echo "   Task: $TASK"
