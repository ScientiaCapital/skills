#!/bin/bash
# Outcome Logger — PostToolUse hook for Write tool
# Detects skill outcome sidecar files and appends to outcomes.jsonl
# Sidecar pattern: ~/.claude/skill-analytics/last-outcome-{skill-name}.json
# Part of P12: Autoresearch Self-Improving Skills Framework

set -e

OUTCOME_DIR="$HOME/.claude/skill-analytics"
OUTCOMES_FILE="$OUTCOME_DIR/outcomes.jsonl"
SIDECAR_PREFIX="$OUTCOME_DIR/last-outcome-"

# Read hook stdin
INPUT=$(cat)

# Early-exit: extract file_path and check if it's a sidecar file
if command -v jq &>/dev/null; then
    FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty' 2>/dev/null || echo "")
else
    FILE_PATH=$(echo "$INPUT" | grep -o '"file_path"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed 's/.*"file_path"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/' 2>/dev/null || echo "")
fi

# Exit immediately if not a sidecar file (vast majority of Write calls)
case "$FILE_PATH" in
    "$SIDECAR_PREFIX"*.json) ;;  # Match — continue processing
    *) exit 0 ;;                  # No match — fast exit
esac

# Sidecar file detected — wait briefly for write to complete
sleep 0.1

[ -f "$FILE_PATH" ] || exit 0

# Validate required fields (ts, skill, status)
if command -v jq &>/dev/null; then
    if ! jq -e '.ts and .skill and .status' "$FILE_PATH" >/dev/null 2>&1; then
        echo "outcome-logger: invalid sidecar (missing required fields): $FILE_PATH" >&2
        rm -f "$FILE_PATH"
        exit 0
    fi

    # Validate status enum
    STATUS=$(jq -r '.status' "$FILE_PATH" 2>/dev/null)
    case "$STATUS" in
        success|partial|error) ;;
        *) echo "outcome-logger: invalid status '$STATUS' in $FILE_PATH" >&2; rm -f "$FILE_PATH"; exit 0 ;;
    esac
else
    # Grep fallback: check for required fields
    if ! grep -q '"ts"' "$FILE_PATH" || ! grep -q '"skill"' "$FILE_PATH" || ! grep -q '"status"' "$FILE_PATH"; then
        rm -f "$FILE_PATH"
        exit 0
    fi
fi

# Ensure output directory exists
mkdir -p "$OUTCOME_DIR"

# Append outcome (atomic if flock available)
OUTCOME_LINE=$(cat "$FILE_PATH")
if command -v flock &>/dev/null; then
    flock "$OUTCOMES_FILE.lock" bash -c "echo '$OUTCOME_LINE' >> '$OUTCOMES_FILE'"
else
    echo "$OUTCOME_LINE" >> "$OUTCOMES_FILE"
fi

# Remove the transient sidecar
rm -f "$FILE_PATH"

# 90-day rotation: if file exceeds 500 lines, archive old entries
LINE_COUNT=$(wc -l < "$OUTCOMES_FILE" 2>/dev/null | tr -d ' ')
if [ "${LINE_COUNT:-0}" -gt 500 ]; then
    # Calculate cutoff date (90 days ago)
    if date -v-90d +%Y-%m-%dT &>/dev/null 2>&1; then
        CUTOFF=$(date -v-90d +%Y-%m-%dT00:00:00Z)
    else
        CUTOFF=$(date -d '90 days ago' +%Y-%m-%dT00:00:00Z)
    fi

    ARCHIVE="$OUTCOME_DIR/outcomes-archive-$(date +%Y).jsonl"
    TEMP_FILE="$OUTCOMES_FILE.tmp"

    # Split: old entries to archive, recent entries kept
    if command -v jq &>/dev/null; then
        jq -c "select(.ts < \"$CUTOFF\")" "$OUTCOMES_FILE" >> "$ARCHIVE" 2>/dev/null || true
        jq -c "select(.ts >= \"$CUTOFF\")" "$OUTCOMES_FILE" > "$TEMP_FILE" 2>/dev/null || true
        mv "$TEMP_FILE" "$OUTCOMES_FILE"
    fi
fi
