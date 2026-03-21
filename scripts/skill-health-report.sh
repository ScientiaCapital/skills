#!/bin/bash
# Skill Health Report — bash-only CLI (no LLM, $0 cost)
# Part of P12: Autoresearch Self-Improving Skills Framework
# Usage: ./scripts/skill-health-report.sh [--days N] [--blocker-only]

set -e

OUTCOME_DIR="$HOME/.claude/skill-analytics"
OUTCOMES_FILE="$OUTCOME_DIR/outcomes.jsonl"

DAYS=30
BLOCKER_ONLY=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --days)         DAYS="$2"; shift 2 ;;
        --blocker-only) BLOCKER_ONLY=true; shift ;;
        -h|--help)
            echo "Usage: $0 [--days N] [--blocker-only]"
            echo "  --days N         Analysis window (default: 30)"
            echo "  --blocker-only   Only show skills with <80% success"
            exit 0
            ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

if ! command -v jq &>/dev/null; then
    echo "ERROR: jq required" >&2; exit 1
fi

if [ ! -f "$OUTCOMES_FILE" ] || [ ! -s "$OUTCOMES_FILE" ]; then
    echo "=== Skill Health Report ==="
    echo "No outcome data yet. Run pilot skills or use /skill-feedback."
    exit 0
fi

# Date cutoff
if date -v-1d +%Y-%m-%d &>/dev/null 2>&1; then
    CUTOFF=$(date -v-"${DAYS}d" +%Y-%m-%dT00:00:00Z)
else
    CUTOFF=$(date -d "-${DAYS} days" +%Y-%m-%dT00:00:00Z)
fi

echo "=== Skill Health Report (Last $DAYS days) ==="
echo ""
printf "  %-30s %5s %8s %8s %12s\n" "SKILL" "RUNS" "SUCCESS" "HEALTH" "LAST_RUN"
printf "  %-30s %5s %8s %8s %12s\n" "-----" "----" "-------" "------" "--------"

BLOCKER_COUNT=0

# Get unique skills
SKILLS=$(jq -r "select(.ts >= \"$CUTOFF\") | .skill" "$OUTCOMES_FILE" 2>/dev/null | sort -u)

for skill in $SKILLS; do
    [ -z "$skill" ] && continue

    # Extract all statuses for this skill into a temp var
    STATUSES=$(jq -r "select(.ts >= \"$CUTOFF\" and .skill == \"$skill\") | .status" "$OUTCOMES_FILE" 2>/dev/null)
    [ -z "$STATUSES" ] && continue

    RUNS=$(echo "$STATUSES" | wc -l | tr -d '[:space:]')
    SUCCESS=$(echo "$STATUSES" | grep -c '^success$' 2>/dev/null || true)
    PARTIAL=$(echo "$STATUSES" | grep -c '^partial$' 2>/dev/null || true)
    SUCCESS=${SUCCESS:-0}; PARTIAL=${PARTIAL:-0}
    LAST_RUN=$(jq -r "select(.ts >= \"$CUTOFF\" and .skill == \"$skill\") | .ts" "$OUTCOMES_FILE" 2>/dev/null | sort -r | head -1 | cut -c1-10)

    [ "$RUNS" -eq 0 ] && continue

    # Success rate
    RATE=$(( (SUCCESS + PARTIAL) * 100 / RUNS ))

    # Simple health score (success_rate * 0.4 + data_volume * 0.3 + baseline 0.3)
    # Bash can't do float math, so scale by 100
    DATA_VOL=$RUNS
    [ "$DATA_VOL" -gt 20 ] && DATA_VOL=20
    DATA_VOL_SCORE=$(( DATA_VOL * 100 / 20 ))
    HEALTH=$(( (RATE * 40 + DATA_VOL_SCORE * 30 + 30 * 100) / 100 ))

    FLAG=""
    if [ "$RATE" -lt 80 ]; then
        FLAG=" [BLOCKER]"
        BLOCKER_COUNT=$((BLOCKER_COUNT + 1))
    fi

    if $BLOCKER_ONLY && [ "$RATE" -ge 80 ]; then
        continue
    fi

    printf "  %-30s %5d %7d%% %7d%% %12s%s\n" "$skill" "$RUNS" "$RATE" "$HEALTH" "$LAST_RUN" "$FLAG"
done

echo ""
if [ "$BLOCKER_COUNT" -gt 0 ]; then
    echo "BLOCKERs: $BLOCKER_COUNT skill(s) with <80% success rate"
else
    echo "No BLOCKERs. All tracked skills healthy."
fi
echo ""
echo "For full LLM-powered analysis: /skill-health"
echo "Data: $OUTCOMES_FILE"
