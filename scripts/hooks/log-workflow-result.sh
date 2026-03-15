#!/bin/bash
# Workflow Result Logger — PostToolUse hook for Skill tool
# Tracks last-run timestamps and builds run history

set -uo pipefail

input=$(cat)
STATE_DIR="$HOME/.claude/workflow-runs"
mkdir -p "$STATE_DIR"

SKILL_NAME=$(echo "$input" | grep -o '"skill"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed 's/.*"skill"[[:space:]]*:[[:space:]]*"//' | sed 's/"//')

[ -z "$SKILL_NAME" ] && exit 0

TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
TODAY=$(date +%Y-%m-%d)

case "$SKILL_NAME" in
  deal-momentum*|pipeline-review)
    echo "$TODAY" > "$STATE_DIR/deal-momentum-last.txt"
    echo "{\"skill\":\"deal-momentum\",\"ts\":\"$TS\"}" >> "$STATE_DIR/all-runs.jsonl"
    ;;
  portfolio-deal-linker*|portfolio*update*|gtme*)
    echo "$TODAY" > "$STATE_DIR/portfolio-linker-last.txt"
    echo "{\"skill\":\"portfolio-linker\",\"ts\":\"$TS\"}" >> "$STATE_DIR/all-runs.jsonl"
    ;;
  trading-alert*|market*digest*|pre-market*)
    echo "$TODAY" > "$STATE_DIR/trading-alerts-last.txt"
    echo "{\"skill\":\"trading-alerts\",\"ts\":\"$TS\"}" >> "$STATE_DIR/all-runs.jsonl"
    ;;
  prospect-research*|research-to-cadence*)
    echo "{\"skill\":\"prospect-research\",\"ts\":\"$TS\"}" >> "$STATE_DIR/all-runs.jsonl"
    ;;
  meddic-call-prep*|call-prep*|demo-prep*)
    echo "{\"skill\":\"meddic-call-prep\",\"ts\":\"$TS\"}" >> "$STATE_DIR/all-runs.jsonl"
    ;;
esac
