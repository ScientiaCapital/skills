#!/bin/bash
# Outcome Sweeper — user-level SessionStart hook
# Ingests any pending skill outcome sidecars into outcomes.jsonl, regardless
# of which session/project/tool wrote them. Complements scripts/log-outcome.sh
# (project-scoped PostToolUse hook), which only fires inside the skills repo.
# Source of truth: tk_projects/skills/scripts/sweep-outcomes.sh
# Deployed copy:   ~/.claude/scripts/sweep-outcomes.sh
# Part of P14: analytics capture repair.

OUTCOME_DIR="$HOME/.claude/skill-analytics"
OUTCOMES_FILE="$OUTCOME_DIR/outcomes.jsonl"
SIDECAR_GLOB="$OUTCOME_DIR/last-outcome-*.json"

command -v jq &>/dev/null || exit 0
mkdir -p "$OUTCOME_DIR"

NOW=$(date +%s)
SWEPT=0

for f in $SIDECAR_GLOB; do
    [ -f "$f" ] || continue

    # Skip files modified within the last 5s — may still be mid-write
    MTIME=$(stat -f %m "$f" 2>/dev/null || stat -c %Y "$f" 2>/dev/null || echo 0)
    [ $((NOW - MTIME)) -lt 5 ] && continue

    # Validate required fields + status enum; drop invalid sidecars
    if ! jq -e '.ts and .skill and (.status | IN("success","partial","error"))' "$f" >/dev/null 2>&1; then
        echo "sweep-outcomes: invalid sidecar dropped: $f" >&2
        rm -f "$f"
        continue
    fi

    # Compact to a single JSONL line and append under lock
    LINE=$(jq -c . "$f" 2>/dev/null) || continue
    if command -v flock &>/dev/null; then
        flock "$OUTCOMES_FILE.lock" sh -c 'printf "%s\n" "$1" >> "$2"' _ "$LINE" "$OUTCOMES_FILE"
    else
        printf '%s\n' "$LINE" >> "$OUTCOMES_FILE"
    fi
    rm -f "$f"
    SWEPT=$((SWEPT + 1))
done

# 90-day rotation once file exceeds 500 lines (same policy as log-outcome.sh)
LINE_COUNT=$(wc -l < "$OUTCOMES_FILE" 2>/dev/null | tr -d ' ')
if [ "${LINE_COUNT:-0}" -gt 500 ]; then
    if date -v-90d +%Y-%m-%d &>/dev/null; then
        CUTOFF=$(date -v-90d +%Y-%m-%dT00:00:00Z)
    else
        CUTOFF=$(date -d '90 days ago' +%Y-%m-%dT00:00:00Z)
    fi
    ARCHIVE="$OUTCOME_DIR/outcomes-archive-$(date +%Y).jsonl"
    TEMP_FILE="$OUTCOMES_FILE.tmp"
    jq -c "select(.ts < \"$CUTOFF\")" "$OUTCOMES_FILE" >> "$ARCHIVE" 2>/dev/null || true
    jq -c "select(.ts >= \"$CUTOFF\")" "$OUTCOMES_FILE" > "$TEMP_FILE" 2>/dev/null && mv "$TEMP_FILE" "$OUTCOMES_FILE"
fi

[ "$SWEPT" -gt 0 ] && echo "sweep-outcomes: ingested $SWEPT sidecar(s) into outcomes.jsonl" >&2
exit 0
