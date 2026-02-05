#!/bin/bash
# launch-agent.sh - Launch Claude Code in a new terminal for a worktree
# Auto-detects terminal: opens in whatever terminal you started your day with
# Supports numbered tabs for Boris Cherny workflow

set -e

WORKTREE_PATH="$1"
TASK="$2"
OVERRIDE_TERMINAL=""

shift 2 2>/dev/null || true
while [[ $# -gt 0 ]]; do
    case $1 in
        --terminal) OVERRIDE_TERMINAL="$2"; shift 2 ;;
        --reset-tabs) rm -f /tmp/worktree-tab-counter; echo "Tab counter reset"; exit 0 ;;
        *) shift ;;
    esac
done

if [ -z "$WORKTREE_PATH" ]; then
    echo "Usage: $0 <worktree-path> [task] [--terminal <type>] [--reset-tabs]"
    echo ""
    echo "Terminals: ghostty, iterm2, terminal, tmux"
    echo "Options:"
    echo "  --terminal <type>  Override auto-detected terminal"
    echo "  --reset-tabs       Reset tab counter to 1"
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CONFIG_FILE="$SCRIPT_DIR/../config.json"

if [ -f "$CONFIG_FILE" ] && command -v jq &> /dev/null; then
    CONFIG_TERMINAL=$(jq -r '.terminal // "ghostty"' "$CONFIG_FILE")
    SHELL_CMD=$(jq -r '.shell // "bash"' "$CONFIG_FILE")
    CLAUDE_CMD=$(jq -r '.claudeCommand // "claude --model opus --dangerously-skip-permissions"' "$CONFIG_FILE")
    ENABLE_NUMBERED_TABS=$(jq -r '.enableNumberedTabs // true' "$CONFIG_FILE")
else
    CONFIG_TERMINAL="ghostty"
    SHELL_CMD="bash"
    CLAUDE_CMD="claude --model opus --dangerously-skip-permissions"
    ENABLE_NUMBERED_TABS=true
fi

# Tab counter for Boris Cherny workflow (numbered tabs)
TAB_COUNTER_FILE="/tmp/worktree-tab-counter"

get_next_tab_number() {
    if [ "$ENABLE_NUMBERED_TABS" != "true" ]; then
        echo ""
        return
    fi
    if [ -f "$TAB_COUNTER_FILE" ]; then
        NUM=$(cat "$TAB_COUNTER_FILE")
        NUM=$((NUM + 1))
    else
        NUM=1
    fi
    echo "$NUM" > "$TAB_COUNTER_FILE"
    echo "$NUM"
}

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
    echo "Terminal: $TERMINAL (explicit override)"
else
    TERMINAL=$(detect_active_terminal)
    [ "$TERMINAL" != "$CONFIG_TERMINAL" ] && echo "Terminal: $TERMINAL (auto-detected)" || echo "Terminal: $TERMINAL (from config)"
fi

WORKTREE_PATH="${WORKTREE_PATH/#\~/$HOME}"
[[ "$WORKTREE_PATH" != /* ]] && WORKTREE_PATH="$(pwd)/$WORKTREE_PATH"

[ ! -d "$WORKTREE_PATH" ] && echo "Error: Directory not found: $WORKTREE_PATH" && exit 1
[ ! -e "$WORKTREE_PATH/.git" ] && echo "Error: Not a git worktree: $WORKTREE_PATH" && exit 1

BRANCH=$(cd "$WORKTREE_PATH" && git branch --show-current 2>/dev/null || basename "$WORKTREE_PATH")
PROJECT=$(basename "$(dirname "$WORKTREE_PATH")")

# Get tab number for window/tab naming
TAB_NUM=$(get_next_tab_number)
if [ -n "$TAB_NUM" ]; then
    TAB_PREFIX="[$TAB_NUM] "
else
    TAB_PREFIX=""
fi
WINDOW_TITLE="${TAB_PREFIX}${PROJECT} - ${BRANCH}"

case "$TERMINAL" in
    ghostty)
        if [ -d "/Applications/Ghostty.app" ]; then
            TEMP_SCRIPT=$(mktemp /tmp/worktree-launch.XXXXXX.sh)
            cat > "$TEMP_SCRIPT" << SCRIPT
#!/bin/bash
cd '$WORKTREE_PATH'
echo 'Worktree: $PROJECT / $BRANCH'
echo 'Task: $TASK'
echo ''
exec $CLAUDE_CMD
SCRIPT
            chmod +x "$TEMP_SCRIPT"
            # Use --title for window identification (Boris workflow)
            open -na "Ghostty.app" --args --title="$WINDOW_TITLE" -e "$TEMP_SCRIPT"
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
        set name to "$WINDOW_TITLE"
        write text "cd '$WORKTREE_PATH' && echo 'Worktree: $PROJECT / $BRANCH' && echo 'Task: $TASK' && echo '' && $CLAUDE_CMD"
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

echo "Launched Claude Code agent"
echo "   Window: $WINDOW_TITLE"
echo "   Project: $PROJECT | Branch: $BRANCH"
echo "   Path: $WORKTREE_PATH"
[ -n "$TASK" ] && echo "   Task: $TASK"
