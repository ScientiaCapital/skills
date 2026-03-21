#!/bin/bash
# Outcome Analytics Report — reads outcomes.jsonl and produces health stats
# Part of P12: Autoresearch Self-Improving Skills Framework
# Usage: ./scripts/outcome-report.sh [--days N] [--all] [--skill <name>] [--by-variant]

set -e

OUTCOME_DIR="$HOME/.claude/skill-analytics"
LOG_FILE="$OUTCOME_DIR/outcomes.jsonl"

# Defaults
DAYS=7
ALL_TIME=false
SKILL_FILTER=""
BY_VARIANT=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        --days)       DAYS="$2"; shift 2 ;;
        --all)        ALL_TIME=true; shift ;;
        --skill)      SKILL_FILTER="$2"; shift 2 ;;
        --by-variant) BY_VARIANT=true; shift ;;
        -h|--help)
            echo "Usage: $0 [--days N] [--all] [--skill <name>] [--by-variant]"
            echo "  --days N       Show last N days (default: 7)"
            echo "  --all          Show all time"
            echo "  --skill <name> Filter to one skill"
            echo "  --by-variant   Break down results by variant"
            exit 0
            ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

# Require jq
if ! command -v jq &>/dev/null; then
    echo "ERROR: jq is required for outcome reporting" >&2
    exit 1
fi

# Check for log file
if [ ! -f "$LOG_FILE" ] || [ ! -s "$LOG_FILE" ]; then
    echo "=== Outcome Analytics ==="
    echo ""
    echo "No outcomes recorded yet."
    echo "Run pilot skills (prospect-enrich, morning-brief) or use /skill-feedback."
    echo "Log file: $LOG_FILE"
    exit 0
fi

# Determine date filter
if $ALL_TIME; then
    PERIOD_LABEL="All time"
    CUTOFF_DATE="1970-01-01"
else
    PERIOD_LABEL="Last $DAYS days"
    if date -v-1d +%Y-%m-%d &>/dev/null 2>&1; then
        CUTOFF_DATE=$(date -v-"${DAYS}d" +%Y-%m-%d)
    else
        CUTOFF_DATE=$(date -d "-${DAYS} days" +%Y-%m-%d)
    fi
fi

# Filter outcomes
FILTER_EXPR="select(.ts >= \"${CUTOFF_DATE}\")"
[ -n "$SKILL_FILTER" ] && FILTER_EXPR="$FILTER_EXPR | select(.skill == \"$SKILL_FILTER\")"

FILTERED=$(jq -c "$FILTER_EXPR" "$LOG_FILE" 2>/dev/null || echo "")
TOTAL=$(echo "$FILTERED" | grep -c '"skill"' 2>/dev/null || echo "0")

if [ "$TOTAL" -eq 0 ] || [ -z "$FILTERED" ]; then
    echo "=== Outcome Analytics ==="
    echo "Period: $PERIOD_LABEL | Total outcomes: 0"
    [ -n "$SKILL_FILTER" ] && echo "Filter: $SKILL_FILTER"
    echo ""
    echo "No outcomes in this period."
    exit 0
fi

echo "=== Outcome Analytics ==="
echo "Period: $PERIOD_LABEL | Total outcomes: $TOTAL"
[ -n "$SKILL_FILTER" ] && echo "Filter: $SKILL_FILTER"
echo ""

# --- Per-Skill Summary ---
echo "SKILL HEALTH SUMMARY:"
printf "  %-35s %5s %8s %10s %12s\n" "SKILL" "RUNS" "SUCCESS" "AVG_MS" "LAST_RUN"
printf "  %-35s %5s %8s %10s %12s\n" "---" "---" "---" "---" "---"

echo "$FILTERED" | jq -r '.skill' 2>/dev/null | sort -u | while read -r skill; do
    [ -z "$skill" ] && continue
    SKILL_DATA=$(echo "$FILTERED" | jq -c "select(.skill == \"$skill\")")

    RUNS=$(echo "$SKILL_DATA" | grep -c '"skill"' 2>/dev/null || echo "0")
    SUCCESS=$(echo "$SKILL_DATA" | jq -r '.status' 2>/dev/null | grep -c '^success$' || echo "0")
    PARTIAL=$(echo "$SKILL_DATA" | jq -r '.status' 2>/dev/null | grep -c '^partial$' || echo "0")
    RATE=$(( (SUCCESS + PARTIAL) * 100 / RUNS ))

    # Average runtime
    AVG_MS=$(echo "$SKILL_DATA" | jq -r '.runtime_ms // empty' 2>/dev/null | awk '{s+=$1; n++} END {if(n>0) printf "%.0f", s/n; else print "-"}')
    [ -z "$AVG_MS" ] && AVG_MS="-"

    # Last run
    LAST=$(echo "$SKILL_DATA" | jq -r '.ts' 2>/dev/null | sort -r | head -1 | cut -c1-10)

    # Trend: compare last 2 vs previous 2 success rates
    RECENT_RATE=""
    if [ "$RUNS" -ge 4 ]; then
        RECENT_OK=$(echo "$SKILL_DATA" | jq -r '.status' 2>/dev/null | tail -2 | grep -c 'success\|partial' || echo "0")
        OLDER_OK=$(echo "$SKILL_DATA" | jq -r '.status' 2>/dev/null | head -2 | grep -c 'success\|partial' || echo "0")
        if [ "$RECENT_OK" -gt "$OLDER_OK" ]; then
            RECENT_RATE=" ^"
        elif [ "$RECENT_OK" -lt "$OLDER_OK" ]; then
            RECENT_RATE=" v"
        else
            RECENT_RATE=" ="
        fi
    fi

    # Flag blockers
    FLAG=""
    [ "$RATE" -lt 80 ] && FLAG=" [!]"

    printf "  %-35s %5d %7d%% %10s %12s%s%s\n" "$skill" "$RUNS" "$RATE" "$AVG_MS" "$LAST" "$RECENT_RATE" "$FLAG"
done

# --- Variant Breakdown ---
if $BY_VARIANT; then
    echo ""
    echo "VARIANT BREAKDOWN:"
    printf "  %-25s %-15s %5s %8s\n" "SKILL" "VARIANT" "RUNS" "SUCCESS"
    printf "  %-25s %-15s %5s %8s\n" "---" "---" "---" "---"

    echo "$FILTERED" | jq -r '[.skill, (.variant // "default")] | @tsv' 2>/dev/null | sort -u | while IFS=$'\t' read -r skill variant; do
        [ -z "$skill" ] && continue
        V_DATA=$(echo "$FILTERED" | jq -c "select(.skill == \"$skill\" and (.variant // \"default\") == \"$variant\")")
        V_RUNS=$(echo "$V_DATA" | grep -c '"skill"' 2>/dev/null || echo "0")
        V_OK=$(echo "$V_DATA" | jq -r '.status' 2>/dev/null | grep -c 'success\|partial' || echo "0")
        V_RATE=$(( V_OK * 100 / V_RUNS ))
        printf "  %-25s %-15s %5d %7d%%\n" "$skill" "$variant" "$V_RUNS" "$V_RATE"
    done
fi

echo ""
echo "Log file: $LOG_FILE"
echo "Legend: [!] = success rate <80% (BLOCKER) | ^ improving | v degrading | = stable"
