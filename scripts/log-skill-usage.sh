#!/bin/bash
# Log skill activation event for analytics
# Called by PostToolUse hook on Skill matcher

set -e

LOG_DIR="$HOME/.claude/skill-analytics"
LOG_FILE="$LOG_DIR/events.jsonl"

# Read hook stdin
INPUT=$(cat)

# Extract skill name from the input — the hook stdin for Skill tool has a "skill" field
# Try to extract with jq if available, else grep
if command -v jq &>/dev/null; then
    SKILL_NAME=$(echo "$INPUT" | jq -r '.tool_input.skill // .skill // empty' 2>/dev/null || echo "")
else
    SKILL_NAME=$(echo "$INPUT" | grep -o '"skill"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed 's/.*"skill"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/' 2>/dev/null || echo "")
fi

# Skip if no skill name found
[ -z "$SKILL_NAME" ] && exit 0

# Get project name from git or cwd
PROJECT=$(basename "$(git rev-parse --show-toplevel 2>/dev/null || pwd)")
CWD=$(pwd)

# Create log directory
mkdir -p "$LOG_DIR"

# Append event
echo "{\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"skill\":\"$SKILL_NAME\",\"project\":\"$PROJECT\",\"cwd\":\"$CWD\"}" >> "$LOG_FILE"
