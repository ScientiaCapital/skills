# End Day Protocol

Comprehensive end-of-day procedures including security sweeps, context preservation, and cost tracking.

## Security Sweep (Mandatory)

### Automated Security Scan
```bash
#!/bin/bash
# end-day-security-sweep.sh

echo "=== End Day Security Sweep ==="
echo "Time: $(date -Iseconds)"

# Initialize results
SECURITY_PASSED=true
ISSUES=()

# 1. Secrets Detection
echo -e "\n[1/5] Scanning for secrets..."
gitleaks detect --source . --verbose --report-path=.security/gitleaks-$(date +%Y%m%d).json

if [ $? -ne 0 ]; then
    SECURITY_PASSED=false
    ISSUES+=("Secrets detected in code")
    
    # Show details
    jq '.Issues[] | {file: .File, secret: .Secret[0:20], line: .StartLine}' .security/gitleaks-*.json | tail -5
fi

# 2. Git History Check
echo -e "\n[2/5] Checking git history..."
SECRETS_IN_HISTORY=$(git log -p -10 | grep -E "(password|secret|api[_-]?key|token)[ ]*=[ ]*['\"]" | wc -l)

if [ "$SECRETS_IN_HISTORY" -gt 0 ]; then
    SECURITY_PASSED=false
    ISSUES+=("$SECRETS_IN_HISTORY potential secrets in recent commits")
fi

# 3. Dependency Vulnerabilities
echo -e "\n[3/5] Checking dependencies..."
if [ -f "package.json" ]; then
    npm audit --audit-level=critical --json > .security/npm-audit-$(date +%Y%m%d).json
    CRITICAL=$(jq '.metadata.vulnerabilities.critical' .security/npm-audit-*.json)
    HIGH=$(jq '.metadata.vulnerabilities.high' .security/npm-audit-*.json)
    
    if [ "$CRITICAL" -gt 0 ]; then
        SECURITY_PASSED=false
        ISSUES+=("$CRITICAL critical npm vulnerabilities")
    fi
elif [ -f "requirements.txt" ] || [ -f "pyproject.toml" ]; then
    pip-audit --format json > .security/pip-audit-$(date +%Y%m%d).json
    VULNS=$(jq '.vulnerabilities | length' .security/pip-audit-*.json)
    
    if [ "$VULNS" -gt 0 ]; then
        SECURITY_PASSED=false
        ISSUES+=("$VULNS Python dependency vulnerabilities")
    fi
fi

# 4. Environment Files
echo -e "\n[4/5] Checking environment files..."
ENV_ISSUES=$(grep -r "API_KEY\|SECRET\|PASSWORD\|TOKEN" --include="*.env*" . 2>/dev/null | grep -v ".env.example" | wc -l)

if [ "$ENV_ISSUES" -gt 0 ]; then
    echo "⚠️  WARNING: $ENV_ISSUES potential secrets in .env files"
    echo "   Ensure these are in .gitignore!"
    
    # Check if they're ignored
    for env_file in $(find . -name "*.env*" -not -name "*.example"); do
        if ! git check-ignore "$env_file" > /dev/null 2>&1; then
            SECURITY_PASSED=false
            ISSUES+=("$env_file not in .gitignore")
        fi
    done
fi

# 5. File Permissions
echo -e "\n[5/5] Checking file permissions..."
WORLD_WRITABLE=$(find . -type f -perm -002 -not -path "./.git/*" 2>/dev/null | wc -l)

if [ "$WORLD_WRITABLE" -gt 0 ]; then
    ISSUES+=("$WORLD_WRITABLE world-writable files detected")
fi

# Report
echo -e "\n=== Security Sweep Results ==="
if [ "$SECURITY_PASSED" = true ]; then
    echo "✅ ALL SECURITY CHECKS PASSED"
    echo "Safe to commit changes."
else
    echo "❌ SECURITY ISSUES DETECTED"
    echo ""
    printf '%s\n' "${ISSUES[@]}"
    echo ""
    echo "⛔ BLOCKING COMMITS until resolved"
    exit 1
fi
```

### Manual Security Checklist
```markdown
## Manual Security Review

Before ending the day, verify:

- [ ] No hardcoded credentials in new code
- [ ] API keys are from environment variables
- [ ] Database connection strings are secured
- [ ] No sensitive data in logs
- [ ] Authentication checks on new endpoints
- [ ] Input validation on user inputs
- [ ] SQL injection prevention (parameterized queries)
- [ ] XSS prevention (output encoding)
- [ ] CORS settings appropriate
- [ ] File upload restrictions in place
```

## Context Preservation

### PROJECT_CONTEXT.md Generation
```python
#!/usr/bin/env python3
# generate-context.py

import json
import subprocess
from datetime import datetime
from pathlib import Path

def generate_project_context():
    """Generate comprehensive project context."""
    
    context = {
        'last_updated': datetime.now().isoformat(),
        'session_duration': get_session_duration(),
        'completed_tasks': get_completed_tasks(),
        'in_progress': get_in_progress_tasks(),
        'blockers': get_blockers(),
        'decisions': get_decisions_made(),
        'tomorrow_priorities': analyze_next_priorities(),
        'metrics': gather_session_metrics()
    }
    
    # Generate markdown
    md_content = f"""## Project Context
Last Updated: {context['last_updated']}
Session Duration: {context['session_duration']}

### Completed This Session
{format_task_list(context['completed_tasks'])}

### In Progress
{format_progress_table(context['in_progress'])}

### Blockers
{format_blockers(context['blockers'])}

### Decisions Made
{format_decisions(context['decisions'])}

### Tomorrow's Priorities
{format_priorities(context['tomorrow_priorities'])}

### Session Metrics
- Commits: {context['metrics']['commits']}
- Files Changed: {context['metrics']['files_changed']}
- Tests Added: {context['metrics']['tests_added']}
- Coverage: {context['metrics']['coverage']}%
"""
    
    # Save context
    with open('PROJECT_CONTEXT.md', 'w') as f:
        f.write(md_content)
        
    # Also save JSON for programmatic access
    with open('.claude/context.json', 'w') as f:
        json.dump(context, f, indent=2)
        
def get_completed_tasks():
    """Extract completed tasks from various sources."""
    tasks = []
    
    # From git commits
    commits = subprocess.check_output(
        ['git', 'log', '--oneline', '--since="1 day ago"'],
        text=True
    ).strip().split('\n')
    
    for commit in commits:
        if commit:
            tasks.append({
                'source': 'git',
                'description': commit.split(' ', 1)[1],
                'completed': True
            })
    
    # From TODO file if exists
    if Path('TASK.md').exists():
        # Parse completed tasks
        pass
        
    # From todo system
    if Path('.claude/todos.json').exists():
        with open('.claude/todos.json') as f:
            todos = json.load(f)
            tasks.extend([
                {'source': 'todo', 'description': t['content'], 'completed': True}
                for t in todos if t.get('status') == 'completed'
            ])
    
    return tasks

def format_progress_table(tasks):
    """Format in-progress tasks as markdown table."""
    if not tasks:
        return "_No tasks currently in progress_"
        
    table = "| Task | Branch | Status | Blockers |\n"
    table += "|------|---------|---------|----------|\n"
    
    for task in tasks:
        table += f"| {task['name']} | {task['branch']} | {task['progress']}% | {task['blocker'] or 'None'} |\n"
        
    return table
```

### Smart Context Compression
```python
def compress_context(full_context, max_tokens=2000):
    """Compress context to fit token limits while preserving key info."""
    
    # Priority order for context elements
    priorities = [
        ('blockers', 1.0),          # Always include blockers
        ('in_progress', 0.9),       # Current work is critical
        ('decisions', 0.8),         # Important for continuity
        ('tomorrow_priorities', 0.7), # Next session planning
        ('completed_tasks', 0.5),   # Can be summarized
        ('metrics', 0.3),           # Nice to have
    ]
    
    compressed = {}
    current_tokens = 0
    
    for key, priority in priorities:
        if key not in full_context:
            continue
            
        content = full_context[key]
        tokens = estimate_tokens(content)
        
        if current_tokens + tokens <= max_tokens:
            compressed[key] = content
            current_tokens += tokens
        elif priority >= 0.7:  # High priority - try to summarize
            summary = summarize_content(content, max_tokens - current_tokens)
            compressed[key] = summary
            current_tokens += estimate_tokens(summary)
            
    return compressed
```

### Context Backup Strategy
```bash
#!/bin/bash
# backup-context.sh

BACKUP_DIR=~/.claude/context-backups
PROJECT_NAME=$(basename $(pwd))
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p "$BACKUP_DIR/$PROJECT_NAME"

# Backup all context files
tar -czf "$BACKUP_DIR/$PROJECT_NAME/context_$DATE.tar.gz" \
    PROJECT_CONTEXT.md \
    CLAUDE.md \
    TASK.md \
    PLANNING.md \
    .claude/context.json \
    .claude/todos.json 2>/dev/null

# Keep only last 7 days of backups
find "$BACKUP_DIR/$PROJECT_NAME" -name "context_*.tar.gz" -mtime +7 -delete

echo "Context backed up to: $BACKUP_DIR/$PROJECT_NAME/context_$DATE.tar.gz"
```

## Cost Tracking

### Daily Cost Aggregation
```python
#!/usr/bin/env python3
# track-daily-costs.py

import json
from datetime import datetime
from pathlib import Path
from collections import defaultdict

class CostTracker:
    """Track and aggregate daily costs."""
    
    def __init__(self):
        self.costs_dir = Path('costs')
        self.costs_dir.mkdir(exist_ok=True)
        
        self.today = datetime.now().strftime('%Y-%m-%d')
        self.daily_file = self.costs_dir / f'daily-{self.today}.json'
        self.mtd_file = self.costs_dir / 'mtd.json'
        self.feature_log = self.costs_dir / 'by-feature.jsonl'
        
    def track_session_costs(self, session_data):
        """Track costs for current session."""
        
        # Calculate costs from session data
        costs = self.calculate_costs(session_data)
        
        # Update daily file
        daily_costs = self.load_daily_costs()
        for category, amount in costs.items():
            daily_costs[category] = daily_costs.get(category, 0) + amount
            
        daily_costs['last_updated'] = datetime.now().isoformat()
        daily_costs['sessions'] = daily_costs.get('sessions', 0) + 1
        
        # Save daily costs
        with open(self.daily_file, 'w') as f:
            json.dump(daily_costs, f, indent=2)
            
        # Update MTD
        self.update_mtd(costs)
        
        # Log feature costs if applicable
        if session_data.get('feature_name'):
            self.log_feature_cost(session_data['feature_name'], costs)
            
        return daily_costs
        
    def calculate_costs(self, session_data):
        """Calculate costs from session metrics."""
        
        costs = defaultdict(float)
        
        # LLM costs
        llm_usage = session_data.get('llm_usage', {})
        for model, tokens in llm_usage.items():
            rate = self.get_model_rate(model)
            costs['llm'] += (tokens / 1000) * rate
            costs[f'llm_{model}'] = (tokens / 1000) * rate
            
        # Compute costs
        compute_hours = session_data.get('compute_hours', 0)
        if compute_hours > 0:
            costs['compute'] = compute_hours * 0.50  # RunPod estimate
            
        # Storage costs (monthly, so prorate)
        storage_gb = session_data.get('storage_gb', 0)
        if storage_gb > 0:
            costs['storage'] = (storage_gb * 0.02) / 30  # Daily portion
            
        # API costs
        api_calls = session_data.get('api_calls', {})
        for api, calls in api_calls.items():
            rate = self.get_api_rate(api)
            costs['api'] += calls * rate
            
        costs['total'] = sum(costs.values())
        
        return dict(costs)
        
    def get_model_rate(self, model):
        """Get cost per 1K tokens for model."""
        rates = {
            'claude-sonnet': 0.003,
            'claude-opus': 0.015,
            'claude-haiku': 0.00025,
            'deepseek-v3': 0.00014,
            'qwen-72b': 0.0002,
            'gpt-4': 0.03,
            'gpt-3.5': 0.001,
        }
        return rates.get(model, 0.001)  # Default rate
        
    def update_mtd(self, session_costs):
        """Update month-to-date totals."""
        
        # Load existing MTD
        if self.mtd_file.exists():
            with open(self.mtd_file) as f:
                mtd = json.load(f)
        else:
            mtd = {
                'month': datetime.now().strftime('%Y-%m'),
                'budget': 100.0,
                'categories': {}
            }
            
        # Update totals
        for category, amount in session_costs.items():
            if category != 'total':
                mtd['categories'][category] = mtd['categories'].get(category, 0) + amount
                
        mtd['total'] = sum(mtd['categories'].values())
        mtd['remaining'] = mtd['budget'] - mtd['total']
        mtd['percent_used'] = (mtd['total'] / mtd['budget']) * 100
        mtd['last_updated'] = datetime.now().isoformat()
        
        # Save MTD
        with open(self.mtd_file, 'w') as f:
            json.dump(mtd, f, indent=2)
            
        # Alert if approaching budget
        if mtd['percent_used'] > 80:
            print(f"⚠️  BUDGET ALERT: {mtd['percent_used']:.1f}% of monthly budget used!")
        if mtd['remaining'] < 10:
            print(f"🚨 CRITICAL: Only ${mtd['remaining']:.2f} remaining in budget!")
            
        return mtd
```

### Cost Analysis & Reporting
```python
def generate_cost_report():
    """Generate detailed cost analysis report."""
    
    report = f"""# Cost Analysis Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Today's Costs
{generate_daily_summary()}

## Month-to-Date
{generate_mtd_summary()}

## Cost by Category
{generate_category_breakdown()}

## Cost by Feature
{generate_feature_costs()}

## Optimization Opportunities
{analyze_cost_optimization()}

## Projections
{generate_cost_projections()}
"""
    
    with open('costs/cost-report.md', 'w') as f:
        f.write(report)
        
def analyze_cost_optimization():
    """Identify cost optimization opportunities."""
    
    opportunities = []
    
    # Analyze LLM usage
    llm_costs = analyze_llm_usage()
    if llm_costs['claude_percent'] > 70:
        opportunities.append({
            'category': 'LLM Usage',
            'finding': f"Claude usage is {llm_costs['claude_percent']}% of LLM costs",
            'recommendation': "Consider DeepSeek V3 for bulk processing (95% cheaper)",
            'potential_savings': llm_costs['potential_savings']
        })
        
    # Analyze compute patterns
    compute_analysis = analyze_compute_usage()
    if compute_analysis['idle_percent'] > 20:
        opportunities.append({
            'category': 'Compute',
            'finding': f"{compute_analysis['idle_percent']}% of compute time is idle",
            'recommendation': "Implement auto-shutdown for idle resources",
            'potential_savings': compute_analysis['idle_cost']
        })
        
    return format_opportunities(opportunities)
```

## Worktree Management

### Cleanup Procedures
```bash
#!/bin/bash
# worktree-cleanup.sh

echo "=== Worktree Cleanup ==="

PROJECT=$(basename $(pwd))
REGISTRY=~/.claude/worktree-registry.json

# List current worktrees
echo "Current worktrees:"
git worktree list

# Check each worktree
git worktree list --porcelain | while read -r line; do
    if [[ $line == worktree* ]]; then
        WORKTREE_PATH=$(echo $line | cut -d' ' -f2)
        BRANCH=$(git -C "$WORKTREE_PATH" branch --show-current 2>/dev/null)
        
        if [ -z "$BRANCH" ]; then
            echo "⚠️  Detached worktree: $WORKTREE_PATH"
            continue
        fi
        
        # Check if branch is merged
        MERGED=$(git branch --merged main | grep "$BRANCH" | wc -l)
        
        if [ "$MERGED" -gt 0 ]; then
            echo "✅ Branch $BRANCH is merged and can be cleaned"
            
            # Remove worktree
            git worktree remove "$WORKTREE_PATH"
            
            # Update registry
            jq --arg path "$WORKTREE_PATH" \
               'del(.worktrees[] | select(.path == $path))' \
               "$REGISTRY" > "$REGISTRY.tmp" && mv "$REGISTRY.tmp" "$REGISTRY"
               
            echo "   Removed worktree: $WORKTREE_PATH"
        else
            echo "⏳ Branch $BRANCH is not merged yet"
            
            # Check age
            AGE_DAYS=$(git -C "$WORKTREE_PATH" log -1 --format=%cr | grep -o '[0-9]\+' | head -1)
            if [ "$AGE_DAYS" -gt 7 ]; then
                echo "   ⚠️  Worktree is $AGE_DAYS days old - consider reviewing"
            fi
        fi
    fi
done

# Clean up registry
echo -e "\nCleaning registry..."
jq '.worktrees |= map(select(.project == "'$PROJECT'"))' "$REGISTRY" > "$REGISTRY.tmp" && mv "$REGISTRY.tmp" "$REGISTRY"

# Port cleanup
echo -e "\nReleasing ports..."
USED_PORTS=$(jq -r '.worktrees[].ports[]' "$REGISTRY" 2>/dev/null | sort -n | uniq)
echo "Ports still in use: ${USED_PORTS:-none}"
```

### Stale Worktree Detection
```python
def detect_stale_worktrees(threshold_days=7):
    """Identify stale worktrees that need attention."""
    
    stale = []
    
    worktrees = get_worktree_info()
    
    for wt in worktrees:
        # Check last commit date
        last_commit = get_last_commit_date(wt['path'])
        age_days = (datetime.now() - last_commit).days
        
        if age_days > threshold_days:
            # Additional checks
            has_uncommitted = check_uncommitted_changes(wt['path'])
            is_behind = check_if_behind_main(wt['branch'])
            has_unpushed = check_unpushed_commits(wt['branch'])
            
            stale.append({
                'path': wt['path'],
                'branch': wt['branch'],
                'age_days': age_days,
                'uncommitted': has_uncommitted,
                'behind_main': is_behind,
                'unpushed': has_unpushed,
                'recommendation': recommend_action(wt, age_days)
            })
            
    return stale

def recommend_action(worktree, age_days):
    """Recommend action for stale worktree."""
    
    if worktree['uncommitted']:
        return "Commit or stash changes"
    elif worktree['unpushed']:
        return "Push commits to remote"
    elif age_days > 14:
        return "Consider archiving or removing"
    elif worktree['behind_main']:
        return "Rebase on latest main"
    else:
        return "Review and merge if ready"
```

## Learning Capture

### Session Learnings Extraction
```python
def capture_session_learnings():
    """Extract and document learnings from session."""
    
    learnings = {
        'patterns': extract_new_patterns(),
        'mistakes': extract_mistakes_made(),
        'tools': extract_useful_tools(),
        'optimizations': extract_optimizations(),
        'decisions': extract_architectural_decisions()
    }
    
    # Update CLAUDE.md with learnings
    update_claude_md(learnings)
    
    # Update skill-specific knowledge
    update_skill_knowledge(learnings)
    
    # Create learning entry
    learning_entry = {
        'date': datetime.now().isoformat(),
        'project': get_project_name(),
        'session_duration': get_session_duration(),
        'key_learnings': format_key_learnings(learnings),
        'applicable_to': identify_applicable_contexts(learnings)
    }
    
    # Append to learning log
    with open('~/.claude/learnings.jsonl', 'a') as f:
        f.write(json.dumps(learning_entry) + '\n')
        
def extract_new_patterns():
    """Identify new coding patterns discovered."""
    
    patterns = []
    
    # From git diff
    diff_analysis = analyze_git_diff()
    for pattern in diff_analysis['new_patterns']:
        patterns.append({
            'type': pattern['type'],
            'description': pattern['description'],
            'example': pattern['code_snippet'],
            'context': pattern['use_case']
        })
        
    return patterns
```

### CLAUDE.md Updates
```python
def update_claude_md(learnings):
    """Update project CLAUDE.md with new learnings."""
    
    # Read existing CLAUDE.md
    claude_md = Path('CLAUDE.md')
    if not claude_md.exists():
        content = "# Project Learnings\n\n"
    else:
        content = claude_md.read_text()
        
    # Add new learnings section
    new_section = f"""
## Session Learnings - {datetime.now().strftime('%Y-%m-%d')}

### New Patterns Discovered
{format_patterns(learnings['patterns'])}

### Mistakes to Avoid
{format_mistakes(learnings['mistakes'])}

### Useful Tools/Commands
{format_tools(learnings['tools'])}

### Performance Optimizations
{format_optimizations(learnings['optimizations'])}

### Architectural Decisions
{format_decisions(learnings['decisions'])}
"""
    
    # Append to file
    content += new_section
    claude_md.write_text(content)
```

## Integration & Automation

### Git Hooks Integration
```bash
#!/bin/bash
# .git/hooks/pre-commit

# Run end-day security sweep
./scripts/end-day-security-sweep.sh

if [ $? -ne 0 ]; then
    echo "❌ Security checks failed. Commit blocked."
    echo "Run './scripts/end-day-security-sweep.sh' for details"
    exit 1
fi

# Generate context if needed
if [ ! -f "PROJECT_CONTEXT.md" ] || [ $(find "PROJECT_CONTEXT.md" -mmin +60) ]; then
    echo "Generating project context..."
    python3 scripts/generate-context.py
    git add PROJECT_CONTEXT.md
fi

echo "✅ Pre-commit checks passed"
```

### Automated End Day Script
```bash
#!/bin/bash
# end-day.sh - Main end day automation

echo "=== Running End Day Protocol ==="
echo "Started: $(date)"

# 1. Security sweep
echo -e "\n[1/6] Security Sweep"
./scripts/end-day-security-sweep.sh || exit 1

# 2. Generate context
echo -e "\n[2/6] Generating Context"
python3 scripts/generate-context.py

# 3. Track costs
echo -e "\n[3/6] Tracking Costs"
python3 scripts/track-daily-costs.py

# 4. Clean worktrees
echo -e "\n[4/6] Cleaning Worktrees"
./scripts/worktree-cleanup.sh

# 5. Capture learnings
echo -e "\n[5/6] Capturing Learnings"
python3 scripts/capture-learnings.py

# 6. Backup context
echo -e "\n[6/6] Backing Up Context"
./scripts/backup-context.sh

# Generate summary
cat << EOF

=== End Day Summary ===
Time: $(date)
Duration: $(get_session_duration)

Security: ✅ Passed
Context: ✅ Saved
Costs: ✅ Tracked (Today: \$$(get_today_cost))
Worktrees: ✅ Cleaned
Learnings: ✅ Captured
Backup: ✅ Complete

Ready to commit and end session.
EOF
```

### Slack/Discord Notification
```python
def send_end_day_summary(webhook_url):
    """Send end day summary to team channel."""
    
    summary = generate_end_day_summary()
    
    payload = {
        'text': f"End Day Summary - {get_project_name()}",
        'attachments': [{
            'color': 'good' if summary['all_passed'] else 'danger',
            'fields': [
                {
                    'title': 'Security',
                    'value': '✅ Passed' if summary['security_passed'] else '❌ Issues found',
                    'short': True
                },
                {
                    'title': 'Tests',
                    'value': f"{summary['tests_passing']}/{summary['tests_total']} passing",
                    'short': True
                },
                {
                    'title': 'Coverage',
                    'value': f"{summary['coverage']}%",
                    'short': True
                },
                {
                    'title': 'Cost Today',
                    'value': f"${summary['cost_today']:.2f}",
                    'short': True
                },
                {
                    'title': 'Completed Tasks',
                    'value': '\n'.join(f"• {task}" for task in summary['completed_tasks']),
                    'short': False
                }
            ],
            'footer': f"Session duration: {summary['duration']}"
        }]
    }
    
    requests.post(webhook_url, json=payload)
```