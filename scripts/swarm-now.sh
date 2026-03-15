#!/usr/bin/env bash
# =============================================================================
# swarm-now.sh — Quick manual trigger for agent swarm
# =============================================================================
# Shortcut to launch agents RIGHT NOW without waiting for the schedule.
# Usage:
#   ./swarm-now.sh          # Launch 2 agents on next projects in rotation
#   ./swarm-now.sh 4        # Launch 4 agents (full day's worth)
#   ./swarm-now.sh 1 chamba # Launch 1 agent on a specific project
# =============================================================================

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
COUNT="${1:-2}"

if [[ -n "${2:-}" ]]; then
  # Specific project override
  PROJECT="$2"
  PROJECT_PATH="$HOME/Desktop/tk_projects/$PROJECT"

  if [[ ! -d "$PROJECT_PATH" ]]; then
    echo "❌ Project not found: $PROJECT_PATH"
    exit 1
  fi

  echo "🚀 Launching agent for: $PROJECT"
  ghostty \
    --title="🤖 Agent: $PROJECT" \
    -e bash -c "
      cd '$PROJECT_PATH' && \
      echo '🤖 Manual Agent Launch: $PROJECT' && \
      claude --model opus --dangerously-skip-permissions
    " &
  echo "✅ Agent launched in Ghostty"
else
  # Use rotation
  bash "$SCRIPT_DIR/agent-swarm-launcher.sh" --count "$COUNT" --block "$(date +%H | awk '{print ($1<12)?"am":"pm"}')"
fi
