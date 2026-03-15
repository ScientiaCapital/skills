#!/usr/bin/env bash
# =============================================================================
# agent-status-check.sh — Check status of all agent-worked projects
# =============================================================================
# Reads .agent-status files from all projects to show what agents accomplished.
# Run anytime between BDR calls to see progress.
#
# Usage:
#   ./agent-status-check.sh [--today] [--week]
# =============================================================================

set -euo pipefail

PROJECTS_DIR="$HOME/Desktop/tk_projects"
STATE_FILE="$HOME/.claude/rotation-state.json"
TODAY=$(date +%Y-%m-%d)

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║  📊 Agent Swarm Status Dashboard                           ║"
echo "║  $TODAY $(date +%H:%M) CST                                        ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# --- Rotation State ----------------------------------------------------------
if [[ -f "$STATE_FILE" ]]; then
  TOTAL=$(jq -r '.projects | length' "$STATE_FILE")
  POINTER=$(jq -r '.pointer' "$STATE_FILE")
  LAST_RUN=$(jq -r '.last_run' "$STATE_FILE")
  LAST_BLOCK=$(jq -r '.last_block' "$STATE_FILE")

  echo "🔄 Rotation: $POINTER / $TOTAL projects | Last: $LAST_BLOCK @ $LAST_RUN"

  # Show today's history
  TODAY_RUNS=$(jq -r ".history[] | select(.date | startswith(\"$TODAY\")) | \"\(.block): \(.projects | join(\", \"))\"" "$STATE_FILE" 2>/dev/null)
  if [[ -n "$TODAY_RUNS" ]]; then
    echo ""
    echo "📅 Today's runs:"
    echo "$TODAY_RUNS" | while read -r line; do
      echo "   $line"
    done
  fi

  # Show next up
  echo ""
  echo "⏭️  Next up in rotation:"
  for ((i=0; i<4; i++)); do
    IDX=$(( (POINTER + i) % TOTAL ))
    PROJ=$(jq -r ".projects[$IDX]" "$STATE_FILE")
    if [[ $i -lt 2 ]]; then
      echo "   [next AM] $PROJ"
    else
      echo "   [next PM] $PROJ"
    fi
  done
else
  echo "⚠️  No rotation state found. Run agent-swarm-launcher.sh first."
fi

echo ""
echo "─────────────────────────────────────────────────────────────"
echo "📋 Agent Reports (from .agent-status files):"
echo "─────────────────────────────────────────────────────────────"

# --- Scan all projects for .agent-status ------------------------------------
FOUND=0
for dir in "$PROJECTS_DIR"/*/; do
  STATUS_FILE="$dir/.agent-status"
  if [[ -f "$STATUS_FILE" ]]; then
    PROJ=$(basename "$dir")
    # Check if status is from today
    if grep -q "$TODAY" "$STATUS_FILE" 2>/dev/null; then
      FOUND=$((FOUND + 1))
      echo ""
      echo "  🤖 $PROJ"
      sed 's/^/     /' "$STATUS_FILE"
    fi
  fi
done

if [[ $FOUND -eq 0 ]]; then
  echo ""
  echo "  No agent reports from today yet."
fi

# --- Recent git activity across all projects ---------------------------------
echo ""
echo "─────────────────────────────────────────────────────────────"
echo "📝 Recent commits across portfolio (today):"
echo "─────────────────────────────────────────────────────────────"

for dir in "$PROJECTS_DIR"/*/; do
  if [[ -d "$dir/.git" ]]; then
    PROJ=$(basename "$dir")
    COMMITS=$(cd "$dir" && git log --since="today 00:00" --oneline 2>/dev/null | head -3)
    if [[ -n "$COMMITS" ]]; then
      echo ""
      echo "  📁 $PROJ"
      echo "$COMMITS" | while read -r line; do
        echo "     $line"
      done
    fi
  fi
done

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "💡 Tip: Run between BDR calls to check progress"
echo "═══════════════════════════════════════════════════════════════"
