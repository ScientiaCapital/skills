# Start Day Protocol

Deep dive into session initialization and context loading procedures.

## Context Scan Components

### 1. Project Detection
```bash
# Get current directory
PROJ_NAME=$(basename $(pwd))

# Detect project type
if [ -f "package.json" ]; then
    echo "Node.js project detected"
    PROJ_TYPE="node"
elif [ -f "pyproject.toml" ] || [ -f "setup.py" ]; then
    echo "Python project detected"
    PROJ_TYPE="python"
elif [ -f "Cargo.toml" ]; then
    echo "Rust project detected"
    PROJ_TYPE="rust"
elif [ -f "go.mod" ]; then
    echo "Go project detected"
    PROJ_TYPE="go"
fi
```

### 2. Git State Analysis
```bash
# Branch info
CURRENT_BRANCH=$(git branch --show-current)
DEFAULT_BRANCH=$(git symbolic-ref refs/remotes/origin/HEAD | sed 's@^refs/remotes/origin/@@')

# Uncommitted changes
UNSTAGED=$(git diff --stat)
STAGED=$(git diff --cached --stat)

# Recent activity
LAST_COMMIT=$(git log -1 --pretty=format:"%h %s (%cr)")
COMMITS_AHEAD=$(git rev-list --count HEAD ^origin/$CURRENT_BRANCH)
```

### 3. Context File Loading Priority
1. **PROJECT_CONTEXT.md** - Session-specific context
2. **CLAUDE.md** - Project rules and patterns
3. **TASK.md** - Current sprint tasks
4. **PLANNING.md** - Roadmap and phases
5. **Backlog.md** - Future work
6. **.taskmaster/docs/prd.txt** - Product requirements

### 4. Worktree Analysis
```bash
# Load registry
REGISTRY=~/.claude/worktree-registry.json
if [ -f "$REGISTRY" ]; then
    # Active worktrees for project
    jq --arg proj "$PROJ_NAME" '.worktrees[] | select(.project == $proj)' "$REGISTRY"
    
    # Port usage
    USED_PORTS=$(jq -r '.worktrees[].ports[]' "$REGISTRY" | sort -n)
    NEXT_PORT=$(echo "$USED_PORTS" | tail -1 | xargs -I{} expr {} + 2)
fi
```

### 5. Cost Context Loading
```bash
# Today's costs
TODAY=$(date +%Y-%m-%d)
TODAY_COST=$(cat costs/daily-$TODAY.json 2>/dev/null | jq '.total' || echo "0")

# Month-to-date
MTD=$(cat costs/mtd.json 2>/dev/null | jq '.total' || echo "0")
BUDGET=$(cat costs/mtd.json 2>/dev/null | jq '.budget' || echo "100")
REMAINING=$(echo "$BUDGET - $MTD" | bc)
PERCENT_USED=$(echo "scale=0; $MTD * 100 / $BUDGET" | bc)

# Average cost per task
AVG_COST=$(cat costs/by-feature.jsonl 2>/dev/null | jq -s 'add/length' || echo "0")
```

## Session Initialization Workflow

### Step 1: Automatic Context Detection
```bash
# Run on every session start
/usr/local/bin/workflow-orchestrator-start-day.sh
```

### Step 2: Priority Queue Generation
```python
def generate_priority_queue():
    """Generate today's task queue with agent assignments."""
    tasks = []
    
    # Load from TASK.md
    current_tasks = parse_task_md()
    
    # Load from recent commits
    recent_work = get_recent_commits(5)
    
    # Analyze blockers
    blockers = find_blockers()
    
    # Smart prioritization
    for task in current_tasks:
        agent = assign_agent(task)
        priority = calculate_priority(task, blockers, recent_work)
        tasks.append({
            'task': task,
            'agent': agent,
            'priority': priority
        })
    
    return sorted(tasks, key=lambda x: x['priority'], reverse=True)
```

### Step 3: Agent Assignment Logic
```python
AGENT_MAPPING = {
    # Keywords to agent mapping
    'debug': 'debug-like-expert',
    'error': 'debugging-toolkit:debugger',
    'test': 'unit-testing:test-automator',
    'api': 'backend-development:backend-architect',
    'frontend': 'frontend-mobile-development:frontend-developer',
    'database': 'database-design:schema-design',
    'deploy': 'deployment-strategies:deployment-engineer',
    'research': 'research-skill',
    'plan': 'planning-prompts-skill',
    'refactor': 'code-refactoring:legacy-modernizer',
    'security': 'full-stack-orchestration:security-auditor',
}

def assign_agent(task_description):
    """Intelligently assign agent based on task description."""
    desc_lower = task_description.lower()
    
    for keyword, agent in AGENT_MAPPING.items():
        if keyword in desc_lower:
            return agent
    
    return 'general-purpose'  # Default
```

## Output Formatting

### Standard Session Start Template
```markdown
## Session Start: [PROJECT_NAME]
*Branch: [BRANCH] | Type: [PROJECT_TYPE] | Started: [TIME]*

### Git Status
- Current: [BRANCH] ([COMMITS_AHEAD] ahead)
- Unstaged: [COUNT] files
- Staged: [COUNT] files

### Completed (Last Session)
[List from PROJECT_CONTEXT.md]

### In Progress
[Table with worktree info]

### Blockers
[List from context files]

### Today's Priority Queue
[Numbered list with agent assignments]

### Cost Context
- Today: $[TODAY] | MTD: $[MTD] / $[BUDGET] ([PERCENT]%)
- Remaining budget: $[REMAINING]
- Avg cost/task: $[AVG]

### Available Resources
- Worktrees: [ACTIVE]/4 max
- Ports: [NEXT_PORT] next available
- Memory: [FREE]GB free
```

## Integration Points

### 1. With TodoWrite
Automatically create todos from priority queue:
```javascript
const todos = priorityQueue.map((item, idx) => ({
    id: `day-${idx}`,
    content: item.task,
    status: 'pending',
    priority: item.priority > 8 ? 'high' : 'medium'
}));
```

### 2. With Worktree Manager
Check for stale worktrees:
```bash
# Worktrees older than 7 days
git worktree list --porcelain | while read line; do
    # Parse and check age
done
```

### 3. With Cost Tracking
Alert if approaching budget:
```python
if percent_used > 80:
    print("⚠️ BUDGET ALERT: {}% of monthly budget used".format(percent_used))
if remaining < 10:
    print("🚨 CRITICAL: Only ${} remaining in budget".format(remaining))
```

## Error Handling

### Missing Context Files
```bash
# Graceful fallback
if [ ! -f "PROJECT_CONTEXT.md" ]; then
    echo "No previous context found. Starting fresh session."
    # Initialize with defaults
fi
```

### Git Repository Issues
```bash
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    echo "Not a git repository. Limited context available."
    # Fall back to file-based context only
fi
```

### Cost Tracking Errors
```bash
# Initialize if missing
if [ ! -d "costs" ]; then
    mkdir -p costs
    echo '{"total": 0, "budget": 100}' > costs/mtd.json
fi
```

## Performance Optimizations

### 1. Parallel Context Loading
```bash
# Load all context files in parallel
{
    cat PROJECT_CONTEXT.md 2>/dev/null &
    cat CLAUDE.md 2>/dev/null &
    cat TASK.md 2>/dev/null &
    cat PLANNING.md 2>/dev/null &
    wait
} | process_context
```

### 2. Caching Git Information
```bash
# Cache expensive git operations
GIT_CACHE=~/.claude/git-cache/$PROJ_NAME
mkdir -p "$GIT_CACHE"

# Cache branch info for 5 minutes
if [ ! -f "$GIT_CACHE/branches" ] || [ $(find "$GIT_CACHE/branches" -mmin +5) ]; then
    git branch -r > "$GIT_CACHE/branches"
fi
```

### 3. Smart Worktree Detection
Only scan worktrees if registry indicates active ones:
```bash
ACTIVE_COUNT=$(jq --arg p "$PROJ_NAME" '[.worktrees[] | select(.project == $p)] | length' "$REGISTRY")
if [ "$ACTIVE_COUNT" -gt 0 ]; then
    git worktree list
fi
```

## Security Considerations

### 1. Secrets Detection
```bash
# Quick scan for exposed secrets
grep -r "API_KEY\|SECRET\|PASSWORD" --include="*.env*" . 2>/dev/null | head -5
if [ $? -eq 0 ]; then
    echo "⚠️ WARNING: Potential secrets detected in environment files"
fi
```

### 2. Dependency Audit
```bash
# Quick security check
if [ "$PROJ_TYPE" = "node" ]; then
    npm audit --audit-level=critical 2>/dev/null | grep "found.*vulnerabilities"
elif [ "$PROJ_TYPE" = "python" ]; then
    pip-audit --desc 2>/dev/null | grep "Vulnerability"
fi
```

## Customization Options

### 1. Project-Specific Overrides
```bash
# Check for project-specific start script
if [ -f ".claude/start-day.sh" ]; then
    source .claude/start-day.sh
fi
```

### 2. User Preferences
```bash
# Load user preferences
PREFS=~/.claude/preferences.json
if [ -f "$PREFS" ]; then
    START_DAY_FORMAT=$(jq -r '.start_day_format // "standard"' "$PREFS")
    SHOW_COSTS=$(jq -r '.show_costs // true' "$PREFS")
    AUTO_TODO=$(jq -r '.auto_create_todos // true' "$PREFS")
fi
```

### 3. Team Configurations
```bash
# Team-wide settings
TEAM_CONFIG=/opt/claude/team-config.json
if [ -f "$TEAM_CONFIG" ]; then
    source "$TEAM_CONFIG"
fi
```