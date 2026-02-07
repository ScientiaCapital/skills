# Report Templates

## Executive Summary Template

```markdown
## Engineering Impact — Week of [DATE]

**Headline:** [1-sentence impact summary]

| Metric | This Week | Last Week | Trend |
|--------|-----------|-----------|-------|
| Features shipped | [N] | [N] | [↑/↓ %] |
| Bugs fixed | [N] | [N] | [↑/↓ %] |
| Lines shipped | [N] | [N] | [↑/↓ %] |
| Total cost | $[N] | $[N] | [↑/↓ %] |
| Cost/feature | $[N] | $[N] | [↑/↓ %] |

### Key Deliverables
1. **[Feature]:** [Impact in business terms]
2. **[Feature]:** [Impact in business terms]

### Cost Optimization
[What was done to reduce costs — model routing, batching, etc.]

### Next Week
[Top 3 priorities]
```

## Weekly Digest Template

```markdown
## Weekly Digest — [START_DATE] to [END_DATE]

### Summary
- [N] commits across [N] projects
- [N] features shipped, [N] bugs fixed
- $[X] total spend ($[X] per feature)

### By Project
| Project | Commits | Features | Fixes | Cost |
|---------|---------|----------|-------|------|
| [project] | [N] | [N] | [N] | $[N] |

### By Day
| Day | Commits | Lines +/- | Cost |
|-----|---------|-----------|------|
| Mon | [N] | +[N]/-[N] | $[N] |
| Tue | [N] | +[N]/-[N] | $[N] |

### Insights
- Most productive: [day/time pattern]
- Most expensive: [feature and why]
- Optimization opportunity: [suggestion]
```

## Sprint Report Template

```markdown
## Sprint: [NAME] — [START] to [END]

### Velocity
| Metric | Target | Actual |
|--------|--------|--------|
| Story points | [N] | [N] |
| Features | [N] | [N] |
| Budget | $[N] | $[N] |

### Deliverables
| Feature | Status | Cost | Notes |
|---------|--------|------|-------|
| [feat] | ✅ | $[N] | [note] |
| [feat] | ✅ | $[N] | [note] |

### Retrospective
- **What worked:** [insight]
- **What didn't:** [insight]
- **Next sprint:** [adjustment]
```

## Generation Script

```bash
#!/bin/bash
# Generate weekly report from daily metrics
WEEK_START=$(date -v-7d +%Y-%m-%d)
METRICS=~/.claude/portfolio/daily-metrics.jsonl

echo "## Weekly Digest — $WEEK_START to $(date +%Y-%m-%d)"
echo ""
echo "### Summary"

TOTAL=$(cat $METRICS | jq -s "map(select(.date >= \"$WEEK_START\")) | length")
COMMITS=$(cat $METRICS | jq -s "map(select(.date >= \"$WEEK_START\")) | map(.commits) | add")
FEATS=$(cat $METRICS | jq -s "map(select(.date >= \"$WEEK_START\")) | map(.features) | add")
FIXES=$(cat $METRICS | jq -s "map(select(.date >= \"$WEEK_START\")) | map(.fixes) | add")
COST=$(cat $METRICS | jq -s "map(select(.date >= \"$WEEK_START\")) | map(.cost) | add")

echo "- $TOTAL days tracked"
echo "- $COMMITS commits ($FEATS features, $FIXES fixes)"
echo "- \$$COST total spend"
```
