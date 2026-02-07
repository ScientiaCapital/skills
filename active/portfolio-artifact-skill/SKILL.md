---
name: "portfolio-artifact"
description: "Auto-extract GTME metrics from work sessions. Lines shipped, bugs fixed, PRs merged, cost per feature. Weekly digests and executive summaries. Use when: capture metrics, portfolio report, what did I ship, weekly summary."
---

<objective>
Automatically extract Go-To-Market Engineer portfolio metrics from development sessions. Captures lines shipped, files changed, bugs fixed, tests added, PRs merged, time saved, and cost per feature. Generates executive summaries and weekly digests.
</objective>

<quick_start>
**Capture today's metrics:**
```bash
# Quick session stats
echo "Commits: $(git log --since='today 00:00' --oneline | wc -l | tr -d ' ')"
echo "Files changed: $(git diff --stat $(git log --since='today 00:00' --format='%H' | tail -1)..HEAD 2>/dev/null | tail -1)"
```

**Generate weekly report:**
```bash
cat ~/.claude/portfolio/daily-metrics.jsonl | jq -s 'map(select(.date >= "'$(date -v-7d +%Y-%m-%d)'"))'
```
</quick_start>

<success_criteria>
- Daily metrics captured automatically via End Day protocol (commits, features, fixes, cost)
- Derived metrics calculated: cost-per-feature, cost-per-bug-fix, lines-per-dollar
- Weekly digest generated with project breakdown and day-by-day trends
- Executive summary ready for stakeholder review with week-over-week comparisons
- Metrics stored persistently at `~/.claude/portfolio/daily-metrics.jsonl`
</success_criteria>

<triggers>
- "capture metrics", "portfolio report", "what did I ship"
- "weekly summary", "executive summary", "sprint report"
- "show impact", "productivity metrics"
</triggers>

---

## Metrics Captured

### Per Session (End Day auto-capture)

| Metric | Source | How |
|--------|--------|-----|
| Commits | `git log --since="today"` | Count |
| Files changed | `git diff --stat` | Count from diff |
| Lines added/removed | `git diff --stat` | Parse +/- |
| Tests added | `git diff --stat -- '*.test.*'` | Count test files |
| PRs created | `gh pr list --author @me` | GitHub CLI |
| Bugs fixed | Commits matching `fix:` | Conventional commits |
| Features shipped | Commits matching `feat:` | Conventional commits |
| Cost | `~/.claude/daily-cost.json` | Daily spend |

### Derived Metrics

| Metric | Formula | Why It Matters |
|--------|---------|---------------|
| Cost per feature | Total cost / feat: commits | Efficiency |
| Cost per bug fix | Total cost / fix: commits | ROI on debugging |
| Lines per dollar | Lines shipped / total cost | Productivity |
| Test coverage delta | Tests added / files changed | Quality signal |

---

## Collection

### Automatic (End Day Protocol)

The workflow-orchestrator End Day protocol calls this automatically:

```bash
#!/bin/bash
# Auto-capture at end of day
DATE=$(date +%Y-%m-%d)
COMMITS=$(git log --since="today 00:00" --oneline 2>/dev/null | wc -l | tr -d ' ')
FEATS=$(git log --since="today 00:00" --oneline --grep="^feat" 2>/dev/null | wc -l | tr -d ' ')
FIXES=$(git log --since="today 00:00" --oneline --grep="^fix" 2>/dev/null | wc -l | tr -d ' ')
COST=$(cat ~/.claude/daily-cost.json 2>/dev/null | jq '.spent // 0')

mkdir -p ~/.claude/portfolio
echo "{\"date\":\"$DATE\",\"commits\":$COMMITS,\"features\":$FEATS,\"fixes\":$FIXES,\"cost\":$COST}" >> ~/.claude/portfolio/daily-metrics.jsonl
```

### Manual (On-Demand)

```bash
# Full session capture with git stats
STAT=$(git diff --stat $(git log --since="today 00:00" --format="%H" | tail -1)..HEAD 2>/dev/null | tail -1)
ADDED=$(echo "$STAT" | grep -oE '[0-9]+ insertion' | grep -oE '[0-9]+' || echo 0)
REMOVED=$(echo "$STAT" | grep -oE '[0-9]+ deletion' | grep -oE '[0-9]+' || echo 0)
echo "Today: +$ADDED/-$REMOVED lines, $COMMITS commits ($FEATS features, $FIXES fixes)"
```

---

## Report Templates

### Executive Summary (C-Suite)

```markdown
## Engineering Impact — Week of [DATE]

**Headline:** Shipped [N] features, fixed [N] bugs across [N] projects

| Metric | This Week | Last Week | Trend |
|--------|-----------|-----------|-------|
| Features shipped | 5 | 3 | ↑ 67% |
| Bugs fixed | 8 | 12 | ↓ 33% |
| Lines shipped | 1,247 | 890 | ↑ 40% |
| Cost | $12.40 | $15.20 | ↓ 18% |
| Cost/feature | $2.48 | $5.07 | ↓ 51% |

**Key Deliverables:**
- [Feature 1]: [Impact]
- [Feature 2]: [Impact]

**Cost Optimization:** Shifted [N] tasks to Haiku, saving $[X] (Y% reduction)
```

### Weekly Digest

```markdown
## Weekly Digest — [DATE RANGE]

### By Project
| Project | Commits | Features | Fixes | Cost |
|---------|---------|----------|-------|------|
| skills-library | 12 | 5 | 2 | $3.40 |
| netzero-bot | 8 | 2 | 4 | $5.20 |

### By Day
| Day | Commits | Lines | Cost |
|-----|---------|-------|------|
| Mon | 5 | +234/-45 | $1.80 |
| Tue | 8 | +567/-123 | $2.40 |
| ... | ... | ... | ... |

### Insights
- Most productive day: Tuesday (567 lines)
- Most expensive feature: [feature] ($X)
- Cheapest bug fix: [fix] ($0.12, Haiku)
```

### Sprint Report

```markdown
## Sprint Report — [SPRINT NAME]

**Duration:** [START] → [END]
**Total Cost:** $[X]

### Deliverables
- [ ] Feature A (shipped, $X)
- [ ] Feature B (shipped, $X)
- [ ] Bug fix C (shipped, $X)

### Velocity
- Story points completed: [N]
- Cost per story point: $[X]
- Average cycle time: [N] hours
```

---

## Storage

```
~/.claude/portfolio/
├── daily-metrics.jsonl      # One JSON line per day
├── weekly-YYYY-WW.md        # Auto-generated weekly digest
└── monthly-YYYY-MM.md       # Auto-generated monthly summary
```

---

## Integration

| System | Integration |
|--------|------------|
| workflow-orchestrator | End Day auto-captures daily metrics |
| cost-metering | Provides cost data for cost-per-feature |
| git-workflow | Conventional commits enable feat/fix counting |
| agent-teams | Tracks multi-agent session costs |

**Deep dive:** See `reference/metrics-guide.md`, `reference/report-templates.md`
