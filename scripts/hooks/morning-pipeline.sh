#!/bin/bash
# Morning Pipeline Check — SessionStart hook
# Surfaces pending daily workflows on weekday mornings

set -euo pipefail

# Skip weekends (6=Sat, 7=Sun)
DOW=$(date +%u)
[ "$DOW" -gt 5 ] && exit 0

# Skip if afternoon (after 11am local)
HOUR=$(date +%H)
[ "$HOUR" -gt 11 ] && exit 0

STATE_DIR="$HOME/.claude/workflow-runs"
TODAY=$(date +%Y-%m-%d)

LAST_DEAL=$(cat "$STATE_DIR/deal-momentum-last.txt" 2>/dev/null || echo "never")
LAST_PORTFOLIO=$(cat "$STATE_DIR/portfolio-linker-last.txt" 2>/dev/null || echo "never")
LAST_TRADING=$(cat "$STATE_DIR/trading-alerts-last.txt" 2>/dev/null || echo "never")

PENDING=""
[ "$LAST_DEAL" != "$TODAY" ] && PENDING="${PENDING} deal-momentum"
[ "$LAST_PORTFOLIO" != "$TODAY" ] && PENDING="${PENDING} portfolio-linker"
[ "$LAST_TRADING" != "$TODAY" ] && PENDING="${PENDING} trading-alerts"

if [ -n "$PENDING" ]; then
  cat <<EOF
Morning workflows pending:${PENDING}
Say "morning brief" to run all, or invoke individually:
  - "deal momentum" — score pipeline, flag RED/YELLOW deals
  - "portfolio update" — attribute closed deals to skills
  - "market digest" — pre-market scan + IBKR positions
EOF
fi
