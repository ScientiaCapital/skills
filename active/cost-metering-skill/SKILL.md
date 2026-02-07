---
name: "cost-metering"
description: "Track and manage API costs across sessions. Budget alerts, model routing for cost optimization, spend reports. Use when: cost check, budget status, how much spent, optimize costs, cost tracking."
---

<objective>
Track Claude API costs across sessions with budget alerts, model routing optimization, and spend reporting. Integrates with workflow-orchestrator's cost gate for automated budget enforcement.
</objective>

<quick_start>
**Check current spend:**
```bash
cat ~/.claude/daily-cost.json 2>/dev/null || echo "No tracking yet"
```

**Initialize tracking:**
```bash
mkdir -p ~/.claude
echo '{"date":"'$(date +%Y-%m-%d)'","spent":0,"budget_monthly":100,"budget_daily":5}' > ~/.claude/daily-cost.json
```
</quick_start>

<triggers>
- "cost check", "budget status", "how much spent"
- "optimize costs", "cost tracking", "budget alert"
- "model routing", "cheaper model", "cost report"
</triggers>

---

## Model Rates (Current)

| Model | Input/1M tokens | Output/1M tokens | Typical Use |
|-------|----------------|-------------------|-------------|
| Claude Opus 4 | $15.00 | $75.00 | Architecture, complex reasoning |
| Claude Sonnet 4.5 | $3.00 | $15.00 | Code generation, standard tasks |
| Claude Haiku 4.5 | $0.25 | $1.25 | Search, classification, simple |
| DeepSeek V3 | $0.27 | $1.10 | Bulk processing |
| GROQ Llama 3.3 70B | $0.59 | $0.79 | Fast inference |
| Voyage Embeddings | $0.10 | — | Embeddings |

---

## Budget Configuration

### ~/.claude/daily-cost.json
```json
{
  "date": "2026-02-07",
  "spent": 2.40,
  "budget_monthly": 100,
  "budget_daily": 5,
  "alerts": {
    "info": 0.5,
    "warn": 0.8,
    "block": 0.95
  }
}
```

### Alert Thresholds

| Threshold | % Budget | Action |
|-----------|----------|--------|
| **Info** | 50% | Display: "50% of monthly budget used" |
| **Warn** | 80% | Yellow alert: "⚠️ 80% budget — consider model downgrade" |
| **Block** | 95% | Red alert: "🛑 95% budget — require explicit override to continue" |

---

## Cost Optimization Strategies

### 1. Model Routing (biggest impact)

| Task | Expensive | Optimized | Savings |
|------|-----------|-----------|---------|
| File search | Sonnet ($3/1M) | Haiku ($0.25/1M) | 92% |
| Code review | Sonnet ($3/1M) | Haiku ($0.25/1M) | 92% |
| Classification | Sonnet ($3/1M) | Haiku ($0.25/1M) | 92% |
| Bulk processing | Sonnet ($3/1M) | DeepSeek ($0.27/1M) | 91% |

**Rule:** If the task doesn't generate code, use Haiku. If it doesn't need Claude, use DeepSeek.

### 2. Context Management

- Keep SKILL.md files under 200 lines (progressive disclosure)
- Load reference files only when needed
- Use `Explore` agent with `haiku` model for codebase search
- Avoid reading entire files — use Grep to find specific lines

### 3. Task Batching

- Group related searches into one Explore agent call
- Use parallel subagents (haiku) instead of serial sonnet calls
- Combine file reads when possible

---

## Tracking Commands

### Daily Spend Check
```bash
cat ~/.claude/daily-cost.json | jq '{date, spent, remaining: (.budget_daily - .spent), pct: ((.spent / .budget_monthly) * 100 | floor)}'
```

### Weekly Report
```bash
# Aggregate daily logs
cat ~/.claude/cost-log.jsonl | jq -s 'group_by(.phase) | map({phase: .[0].phase, total: (map(.est_cost) | add), count: length})'
```

### Monthly Summary
```bash
cat ~/.claude/cost-log.jsonl | jq -s '{
  total: (map(.est_cost) | add),
  by_model: (group_by(.model) | map({model: .[0].model, cost: (map(.est_cost) | add)})),
  by_phase: (group_by(.phase) | map({phase: .[0].phase, cost: (map(.est_cost) | add)}))
}'
```

---

## Integration Points

| System | How |
|--------|-----|
| workflow-orchestrator | Cost gate checks budget before workflows |
| subagent-teams | Model selection uses cost tiers |
| agent-capability-matrix | Includes model recommendations |
| portfolio-artifact | Reports cost-per-feature metrics |
| End Day protocol | Logs daily costs, updates MTD |
| TaskCreate/TaskUpdate | Zero API cost — local UI tool for progress tracking |
| TeamCreate/SendMessage | Zero API cost — local coordination (but spawned agents incur model costs) |

---

## Storage

```
~/.claude/
├── daily-cost.json          # Current day's budget + spend
├── cost-log.jsonl           # Append-only operation log
└── portfolio/
    └── daily-metrics.jsonl  # Includes cost-per-feature
```

**Deep dive:** See `reference/cost-tracking-guide.md`, `reference/budget-templates.md`
