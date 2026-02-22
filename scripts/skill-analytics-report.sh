#!/bin/bash
# Skill usage analytics report
# Reads ~/.claude/skill-analytics/events.jsonl and produces usage stats
# Usage: ./scripts/skill-analytics-report.sh [--days N] [--all]

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"
LOG_FILE="$HOME/.claude/skill-analytics/events.jsonl"

# Defaults
DAYS=7
ALL_TIME=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        --days)
            DAYS="$2"
            shift 2
            ;;
        --all)
            ALL_TIME=true
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [--days N] [--all]"
            echo "  --days N   Show last N days (default: 7)"
            echo "  --all      Show all time"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Check for log file
if [ ! -f "$LOG_FILE" ] || [ ! -s "$LOG_FILE" ]; then
    echo "=== Skill Usage Analytics ==="
    echo ""
    echo "No events recorded yet."
    echo ""
    echo "Events will appear here after skills are activated via Claude Code."
    echo "Log file: $LOG_FILE"
    exit 0
fi

# Determine date filter
if $ALL_TIME; then
    PERIOD_LABEL="All time"
    CUTOFF_DATE="1970-01-01"
else
    PERIOD_LABEL="Last $DAYS days"
    # macOS date vs GNU date
    if date -v-1d +%Y-%m-%d &>/dev/null 2>&1; then
        CUTOFF_DATE=$(date -v-"${DAYS}d" +%Y-%m-%d)
    else
        CUTOFF_DATE=$(date -d "-${DAYS} days" +%Y-%m-%d)
    fi
fi

# Filter events by date range
# Events have ts field like "2026-02-22T14:30:00Z" — extract date portion
if command -v jq &>/dev/null; then
    FILTERED=$(jq -r "select(.ts >= \"${CUTOFF_DATE}\")" "$LOG_FILE" 2>/dev/null || cat "$LOG_FILE")
    TOTAL=$(echo "$FILTERED" | grep -c '"skill"' 2>/dev/null || echo "0")
else
    # Fallback: grep-based filtering
    FILTERED=$(grep "\"ts\":\"${CUTOFF_DATE}\|$(for i in $(seq 0 "$DAYS"); do
        if date -v-"${i}d" +%Y-%m-%d &>/dev/null 2>&1; then
            date -v-"${i}d" +%Y-%m-%d
        else
            date -d "-${i} days" +%Y-%m-%d
        fi
    done | tr '\n' '\|' | sed 's/|$//')" "$LOG_FILE" 2>/dev/null || echo "")
    TOTAL=$(echo "$FILTERED" | grep -c '"skill"' 2>/dev/null || echo "0")
fi

# Handle zero results after filtering
if [ "$TOTAL" -eq 0 ] || [ -z "$FILTERED" ]; then
    echo "=== Skill Usage Analytics ==="
    echo "Period: $PERIOD_LABEL | Total activations: 0"
    echo ""
    echo "No activations in this period."
    exit 0
fi

echo "=== Skill Usage Analytics ==="
echo "Period: $PERIOD_LABEL | Total activations: $TOTAL"
echo ""

# --- Top Skills ---
echo "TOP SKILLS:"
if command -v jq &>/dev/null; then
    echo "$FILTERED" | jq -r '.skill' 2>/dev/null | sort | uniq -c | sort -rn | head -20 | awk '{printf "  %2d. %-30s (%d activations)\n", NR, $2, $1}'
else
    grep -o '"skill":"[^"]*"' <<< "$FILTERED" | sed 's/"skill":"//;s/"//' | sort | uniq -c | sort -rn | head -20 | awk '{printf "  %2d. %-30s (%d activations)\n", NR, $2, $1}'
fi

echo ""

# --- Daily Breakdown ---
echo "DAILY BREAKDOWN:"
if command -v jq &>/dev/null; then
    echo "$FILTERED" | jq -r '.ts[:10]' 2>/dev/null | sort -r | uniq -c | while read -r count day; do
        printf "  %s: %d activations\n" "$day" "$count"
    done
else
    grep -o '"ts":"[^"]*"' <<< "$FILTERED" | sed 's/"ts":"//;s/T.*//' | sort -r | uniq -c | while read -r count day; do
        printf "  %s: %d activations\n" "$day" "$count"
    done
fi

echo ""

# --- Unused Skills Detection ---
echo "UNUSED SKILLS (0 activations in period):"

# Collect skills that WERE used
if command -v jq &>/dev/null; then
    USED_SKILLS=$(echo "$FILTERED" | jq -r '.skill' 2>/dev/null | sort -u)
else
    USED_SKILLS=$(grep -o '"skill":"[^"]*"' <<< "$FILTERED" | sed 's/"skill":"//;s/"//' | sort -u)
fi

# Discover all known skills from the repo
unused_count=0
for skill_dir in "$REPO_DIR"/active/*/ "$REPO_DIR"/stable/*/; do
    [ -d "$skill_dir" ] || continue
    skill_name=$(basename "$skill_dir")
    # Strip the -skill suffix for matching (users invoke "frontend-ui" not "frontend-ui-skill")
    short_name="${skill_name%-skill}"

    # Check if either the full name or short name appears in used skills
    if ! echo "$USED_SKILLS" | grep -qx "$skill_name" && ! echo "$USED_SKILLS" | grep -qx "$short_name"; then
        echo "  - $short_name"
        unused_count=$((unused_count + 1))
    fi
done

if [ "$unused_count" -eq 0 ]; then
    echo "  (none — all skills were used!)"
fi

echo ""
echo "✅ Log file: $LOG_FILE"
