#!/bin/bash
# Feedback Logger — appends feedback to feedback.jsonl
# Part of P12: Autoresearch Self-Improving Skills Framework
# Usage: echo '{"ts":"...","skill":"...","status":"...","notes":"..."}' | bash scripts/log-feedback.sh

set -e

FEEDBACK_DIR="$HOME/.claude/skill-analytics"
FEEDBACK_FILE="$FEEDBACK_DIR/feedback.jsonl"

mkdir -p "$FEEDBACK_DIR"

# Read feedback JSON from stdin
INPUT=$(cat)

# Validate required fields
if command -v jq &>/dev/null; then
    if ! echo "$INPUT" | jq -e '.skill and .status' >/dev/null 2>&1; then
        echo "feedback-logger: missing required fields (skill, status)" >&2
        exit 1
    fi
else
    if ! echo "$INPUT" | grep -q '"skill"' || ! echo "$INPUT" | grep -q '"status"'; then
        echo "feedback-logger: missing required fields (skill, status)" >&2
        exit 1
    fi
fi

# Append feedback (atomic if flock available)
if command -v flock &>/dev/null; then
    flock "$FEEDBACK_FILE.lock" bash -c "echo '$INPUT' >> '$FEEDBACK_FILE'"
else
    echo "$INPUT" >> "$FEEDBACK_FILE"
fi

# 90-day rotation (same pattern as log-outcome.sh)
LINE_COUNT=$(wc -l < "$FEEDBACK_FILE" 2>/dev/null | tr -d ' ')
if [ "${LINE_COUNT:-0}" -gt 500 ]; then
    if date -v-90d +%Y-%m-%dT &>/dev/null 2>&1; then
        CUTOFF=$(date -v-90d +%Y-%m-%dT00:00:00Z)
    else
        CUTOFF=$(date -d '90 days ago' +%Y-%m-%dT00:00:00Z)
    fi

    ARCHIVE="$FEEDBACK_DIR/feedback-archive-$(date +%Y).jsonl"
    TEMP_FILE="$FEEDBACK_FILE.tmp"

    if command -v jq &>/dev/null; then
        jq -c "select(.ts < \"$CUTOFF\")" "$FEEDBACK_FILE" >> "$ARCHIVE" 2>/dev/null || true
        jq -c "select(.ts >= \"$CUTOFF\")" "$FEEDBACK_FILE" > "$TEMP_FILE" 2>/dev/null || true
        mv "$TEMP_FILE" "$FEEDBACK_FILE"
    fi
fi
