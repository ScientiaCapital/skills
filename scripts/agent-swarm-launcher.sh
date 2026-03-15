#!/usr/bin/env bash
# =============================================================================
# agent-swarm-launcher.sh — Autonomous Claude Code Agent Swarm
# =============================================================================
# Launches N Claude Opus 4.6 agents in Ghostty terminals, each working on a
# different project from Tim's portfolio. Reads PLANNING.md/BACKLOG.md and
# autonomously builds the next priority item.
#
# Usage:
#   ./agent-swarm-launcher.sh [--count N] [--block am|pm] [--dry-run]
#
# Requires:
#   - Ghostty installed
#   - claude CLI (Claude Code) installed
#   - Projects in ~/Desktop/tk_projects/
# =============================================================================

set -euo pipefail

# --- Configuration -----------------------------------------------------------
PROJECTS_DIR="$HOME/Desktop/tk_projects"
STATE_FILE="$HOME/.claude/rotation-state.json"
AGENT_LOG_DIR="$HOME/.claude/agent-logs"
AGENT_COUNT="${1:-2}"      # Default: 2 agents per block
BLOCK="${2:-auto}"          # am, pm, or auto-detect
DRY_RUN="${3:-false}"
MAX_MEMORY_PERCENT=75       # Don't launch if memory > 75% used
# Ensure claude CLI is in PATH (installed at ~/.local/bin on Tim's machine)
export PATH="$HOME/.local/bin:$HOME/.npm-global/bin:/opt/homebrew/bin:/usr/local/bin:$PATH"
CLAUDE_CMD="claude --model opus --dangerously-skip-permissions"
# Ghostty is an .app on macOS — need to use `open` to launch it
GHOSTTY_CMD="open -na /Applications/Ghostty.app --args"

# --- Parse flags -------------------------------------------------------------
while [[ $# -gt 0 ]]; do
  case $1 in
    --count) AGENT_COUNT="$2"; shift 2 ;;
    --block) BLOCK="$2"; shift 2 ;;
    --dry-run) DRY_RUN=true; shift ;;
    *) shift ;;
  esac
done

# --- Auto-detect block -------------------------------------------------------
if [[ "$BLOCK" == "auto" ]]; then
  HOUR=$(date +%H)
  if [[ $HOUR -lt 12 ]]; then
    BLOCK="am"
  else
    BLOCK="pm"
  fi
fi

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║  🤖 Agent Swarm Launcher — $BLOCK block ($AGENT_COUNT agents)     ║"
echo "║  $(date '+%Y-%m-%d %H:%M %Z')                                    ║"
echo "╚══════════════════════════════════════════════════════════════╝"

# --- Ensure directories exist ------------------------------------------------
mkdir -p "$AGENT_LOG_DIR"
mkdir -p "$(dirname "$STATE_FILE")"

# --- Initialize rotation state if missing ------------------------------------
if [[ ! -f "$STATE_FILE" ]]; then
  echo "Initializing rotation state..."

  # Discover all projects with CLAUDE.md (these are Claude Code projects)
  PROJECTS=()
  for dir in "$PROJECTS_DIR"/*/; do
    if [[ -f "$dir/CLAUDE.md" ]] || [[ -d "$dir/.claude" ]]; then
      PROJECTS+=("$(basename "$dir")")
    fi
  done

  # Build JSON array
  PROJECTS_JSON=$(printf '%s\n' "${PROJECTS[@]}" | jq -R . | jq -s .)

  cat > "$STATE_FILE" <<EOF
{
  "projects": $PROJECTS_JSON,
  "pointer": 0,
  "last_run": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "last_block": "$BLOCK",
  "history": []
}
EOF
  echo "Found ${#PROJECTS[@]} projects with Claude Code configs."
fi

# --- Read rotation state -----------------------------------------------------
PROJECTS=$(jq -r '.projects[]' "$STATE_FILE")
POINTER=$(jq -r '.pointer' "$STATE_FILE")
TOTAL=$(jq -r '.projects | length' "$STATE_FILE")

if [[ $TOTAL -eq 0 ]]; then
  echo "❌ No projects found in $PROJECTS_DIR with CLAUDE.md or .claude/"
  exit 1
fi

echo "📁 Portfolio: $TOTAL projects | Pointer: $POINTER"

# --- Select projects for this block ------------------------------------------
SELECTED=()
for ((i=0; i<AGENT_COUNT; i++)); do
  IDX=$(( (POINTER + i) % TOTAL ))
  PROJ=$(jq -r ".projects[$IDX]" "$STATE_FILE")
  SELECTED+=("$PROJ")
done

# Advance pointer for next run
NEW_POINTER=$(( (POINTER + AGENT_COUNT) % TOTAL ))

echo ""
echo "📋 Selected for $BLOCK block:"
for proj in "${SELECTED[@]}"; do
  echo "   → $proj"
done
echo ""

# --- Memory check ------------------------------------------------------------
if command -v memory_pressure &>/dev/null; then
  MEM_STATUS=$(memory_pressure 2>/dev/null | head -1 || echo "OK")
  echo "💾 Memory: $MEM_STATUS"
  if echo "$MEM_STATUS" | grep -qi "critical\|warn"; then
    echo "⚠️  High memory pressure — reducing to 1 agent"
    AGENT_COUNT=1
    SELECTED=("${SELECTED[0]}")
  fi
fi

# --- Detect project type and map to skills -----------------------------------
SKILLS_DIR="$HOME/Desktop/tk_projects/skills"

detect_project_skills() {
  local project_path="$1"
  local skills=""

  # FAST detection: only check config files and top-level files, NEVER recursive grep
  # This completes in <1 second per project

  # Python backend (FastAPI, Flask, Django)
  if [[ -f "$project_path/requirements.txt" ]] || [[ -f "$project_path/pyproject.toml" ]] || [[ -f "$project_path/uv.lock" ]]; then
    skills="$skills api-design testing security"
    # Check requirements.txt or pyproject.toml for FastAPI (flat file, instant)
    grep -ql "fastapi" "$project_path/requirements.txt" "$project_path/pyproject.toml" 2>/dev/null && skills="$skills api-design"
  fi

  # Node/React/Next.js frontend — only check package.json (single file)
  if [[ -f "$project_path/package.json" ]]; then
    grep -q '"next"\|"react"' "$project_path/package.json" 2>/dev/null && skills="$skills frontend-ui testing"
    grep -q '"tailwind' "$project_path/package.json" 2>/dev/null && skills="$skills frontend-ui"
  fi

  # Supabase — check for dir or .env files only
  if [[ -d "$project_path/supabase" ]]; then
    skills="$skills supabase-sql security"
  elif [[ -f "$project_path/.env" ]]; then
    grep -q "supabase" "$project_path/.env" 2>/dev/null && skills="$skills supabase-sql security"
  fi

  # Docker — just check for files existing
  [[ -f "$project_path/Dockerfile" ]] || [[ -f "$project_path/docker-compose.yml" ]] || [[ -f "$project_path/docker-compose.yaml" ]] && skills="$skills docker-compose-skill"

  # LangGraph — check requirements/pyproject only
  grep -ql "langgraph" "$project_path/requirements.txt" "$project_path/pyproject.toml" 2>/dev/null && skills="$skills langgraph-agents"

  # RunPod — check requirements/pyproject/Dockerfile only
  grep -ql "runpod" "$project_path/requirements.txt" "$project_path/pyproject.toml" "$project_path/Dockerfile" 2>/dev/null && skills="$skills runpod-deployment"

  # HubSpot — check CLAUDE.md and .env (the two places it'd be mentioned)
  grep -ql -i "hubspot" "$project_path/CLAUDE.md" "$project_path/.env" "$project_path/requirements.txt" "$project_path/package.json" 2>/dev/null && skills="$skills crm-integration hubspot-revops-skill"

  # Voice AI — check requirements/package.json only
  grep -ql "deepgram\|cartesia\|twilio" "$project_path/requirements.txt" "$project_path/pyproject.toml" "$project_path/package.json" 2>/dev/null && skills="$skills voice-ai groq-inference"

  # Trading — check project name and CLAUDE.md
  if echo "$project_path" | grep -qi "trad\|theta\|signal\|finops"; then
    skills="$skills trading-signals data-analysis"
  fi

  # Sales / GTM — check project name and CLAUDE.md
  if echo "$project_path" | grep -qi "sales\|lead\|outreach\|bdr\|prospect"; then
    skills="$skills sales-revenue gtm-pricing"
  fi

  # Deduplicate
  skills=$(echo "$skills" | tr ' ' '\n' | sort -u | tr '\n' ' ')
  echo "$skills"
}

# --- Build the autonomous agent prompt ---------------------------------------
build_agent_prompt() {
  local project="$1"
  local project_path="$PROJECTS_DIR/$project"

  # Detect which skills apply
  local detected_skills
  detected_skills=$(detect_project_skills "$project_path")

  # Build skill-loading instructions
  local skill_instructions=""
  if [[ -n "$detected_skills" ]]; then
    skill_instructions="## Phase 0: Load Skills
Before writing any code, read these skill files for best practices:
"
    for skill in $detected_skills; do
      local skill_path="$SKILLS_DIR/active/$skill/SKILL.md"
      local skill_path_alt="$SKILLS_DIR/stable/$skill/SKILL.md"
      local skill_path_flat="$HOME/.claude/skills/$skill/SKILL.md"
      if [[ -f "$skill_path" ]]; then
        skill_instructions="$skill_instructions- Read: $skill_path
"
      elif [[ -f "$skill_path_alt" ]]; then
        skill_instructions="$skill_instructions- Read: $skill_path_alt
"
      elif [[ -f "$skill_path_flat" ]]; then
        skill_instructions="$skill_instructions- Read: $skill_path_flat
"
      fi
    done
    skill_instructions="$skill_instructions
Apply the patterns and best practices from these skills throughout your work.
"
  fi

  cat <<PROMPT
You are an autonomous Claude Code agent working on project: $project
Detected skills: $detected_skills

$skill_instructions
## Phase 1: Context Load
1. Read CLAUDE.md to understand the project
2. Run: git status && git log --oneline -5
3. Read PLANNING.md or BACKLOG.md to find the highest priority incomplete task
4. If no PLANNING.md exists, read any TODO comments in the codebase

## Phase 2: Build (GOAL: Move toward a monetizable product)
1. Pick the SINGLE highest priority incomplete item
2. IMPORTANT: Every task should move this project closer to being a real product/service
   - If the project lacks a landing page, build one
   - If it lacks auth/payments, add Stripe or usage tracking
   - If it lacks tests, add them
   - If it lacks API docs, generate them
   - If it's feature-complete but undeployed, set up deployment
3. Implement it completely — production-ready code with type hints and error handling
4. Run any available tests (npm test, pytest, bun test, etc.)
5. If tests fail, fix them before proceeding

## Phase 3: Simplify
1. Review what you just built
2. Remove unnecessary complexity, over-engineering, dead code
3. Ensure code is readable by a human

## Phase 4: Review
1. Check the last 3 commits for bugs, security issues, convention violations
2. Run linting if available (eslint, ruff, etc.)
3. Verify no secrets or .env files are staged

## Phase 5: Ship
1. git add the specific files you changed (NOT git add -A)
2. git commit with a clear conventional commit message
3. git push to the current branch
4. Update PLANNING.md to mark the task as completed with today's date

## Phase 6: Report
1. Create/update .agent-status in the project root:
   \`\`\`
   agent: opus-4.6
   block: $BLOCK
   date: $(date +%Y-%m-%d)
   skills_loaded: $detected_skills
   task_completed: [description]
   monetization_progress: [what this moves toward: SaaS, API, service, etc.]
   files_changed: [list]
   tests_passed: [yes/no]
   pushed: [yes/no]
   next_priority: [what's next in PLANNING.md]
   \`\`\`

## Rules
- ONE task per session. Do it well, don't try to do everything.
- MONETIZATION LENS: Every commit should move toward revenue. Ask: "Does this get us closer to charging for this?"
- If the project has no clear next task, run /simplify on the most complex file instead.
- If you encounter a blocker you can't resolve, document it in .agent-status and stop.
- Never modify CLAUDE.md, .claude/, or init.sh files.
- Match the project's existing code style.
- Commit message format: type(scope): description (e.g., feat(api): add retry logic)
PROMPT
}

# --- Launch agents -----------------------------------------------------------
LAUNCHED=0
for proj in "${SELECTED[@]}"; do
  PROJECT_PATH="$PROJECTS_DIR/$proj"
  LOG_FILE="$AGENT_LOG_DIR/${proj}_$(date +%Y%m%d_%H%M).log"

  if [[ ! -d "$PROJECT_PATH" ]]; then
    echo "⚠️  Skipping $proj — directory not found"
    continue
  fi

  # Guard: skip if an agent is already running on this project
  if pgrep -f "claude.*$proj" > /dev/null 2>&1; then
    echo "⚠️  Skipping $proj — agent already running (duplicate protection)"
    continue
  fi

  PROMPT=$(build_agent_prompt "$proj")

  if [[ "$DRY_RUN" == "true" ]]; then
    echo "🔍 [DRY RUN] Would launch agent for: $proj"
    echo "   Path: $PROJECT_PATH"
    echo "   Log:  $LOG_FILE"
    echo ""
    LAUNCHED=$((LAUNCHED + 1))
    continue
  fi

  # Detect skills for this project
  DETECTED_SKILLS=$(detect_project_skills "$PROJECT_PATH")

  echo "🚀 Launching agent for: $proj"
  echo "   Path:   $PROJECT_PATH"
  echo "   Skills: ${DETECTED_SKILLS:-none detected}"
  echo "   Log:    $LOG_FILE"

  # Write prompt to a temp file for the agent to read on launch
  PROMPT_FILE=$(mktemp /tmp/agent-prompt-XXXXXX.md)
  echo "$PROMPT" > "$PROMPT_FILE"

  # Create a launch script (worktree-manager pattern — avoids shell escaping)
  TEMP_SCRIPT=$(mktemp /tmp/agent-launch-XXXXXX.sh)
  cat > "$TEMP_SCRIPT" <<LAUNCH_SCRIPT
#!/bin/bash
export PATH="$HOME/.local/bin:$HOME/.npm-global/bin:/opt/homebrew/bin:/usr/local/bin:\$PATH"
cd '$PROJECT_PATH'
echo '═══════════════════════════════════════'
echo '🤖 Autonomous Agent: $proj'
echo '📅 $(date '+%Y-%m-%d %H:%M')'
echo '🔧 Skills: $DETECTED_SKILLS'
echo '═══════════════════════════════════════'
echo ''
# Pass prompt as positional arg — starts INTERACTIVE session (subscription auth, no API key)
# This is the same pattern worktree-manager uses
exec claude --model opus --dangerously-skip-permissions "\$(cat '$PROMPT_FILE')"
LAUNCH_SCRIPT
  chmod +x "$TEMP_SCRIPT"

  # Launch in Ghostty on macOS (same pattern as worktree-manager)
  open -na "Ghostty.app" --args --title="Agent: $proj" -e "$TEMP_SCRIPT"

  # Cleanup temp files after a delay (agent will have read prompt by then)
  (sleep 10 && rm -f "$TEMP_SCRIPT" "$PROMPT_FILE") &

  LAUNCHED=$((LAUNCHED + 1))

  # Small delay between launches to avoid port conflicts
  sleep 3
done

# --- Update rotation state ---------------------------------------------------
if [[ "$DRY_RUN" != "true" ]]; then
  HISTORY_ENTRY=$(cat <<EOF
{
  "date": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "block": "$BLOCK",
  "projects": $(printf '%s\n' "${SELECTED[@]}" | jq -R . | jq -s .),
  "agents_launched": $LAUNCHED
}
EOF
)

  jq --argjson entry "$HISTORY_ENTRY" --argjson ptr "$NEW_POINTER" '
    .pointer = $ptr |
    .last_run = now | todate |
    .last_block = "'"$BLOCK"'" |
    .history += [$entry] |
    .history = (.history | .[-30:])
  ' "$STATE_FILE" > "${STATE_FILE}.tmp" && mv "${STATE_FILE}.tmp" "$STATE_FILE"
fi

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "✅ Launched $LAUNCHED agents in Ghostty windows"
echo "📊 Next rotation pointer: $NEW_POINTER / $TOTAL"
echo "📝 Logs: $AGENT_LOG_DIR/"
echo "═══════════════════════════════════════════════════════════════"
