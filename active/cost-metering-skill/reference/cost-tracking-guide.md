# Cost Tracking Guide

## Data Format

### daily-cost.json (Current Day)
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

### cost-log.jsonl (Append-Only Log)
```json
{"phase":"research","model":"haiku","est_tokens":10000,"est_cost":0.003,"ts":"2026-02-07T10:30:00-05:00"}
{"phase":"feature-build","model":"sonnet","est_tokens":50000,"est_cost":0.15,"ts":"2026-02-07T11:00:00-05:00"}
{"phase":"review","model":"haiku","est_tokens":8000,"est_cost":0.002,"ts":"2026-02-07T11:30:00-05:00"}
```

## Tracking Methods

### Automatic (Recommended)
The workflow-orchestrator cost gate tracks spend automatically when you use the standard workflows (Start Day, Feature Build, End Day).

### Manual Logging
After expensive operations:
```bash
echo '{"phase":"[PHASE]","model":"[MODEL]","est_tokens":[N],"est_cost":[COST],"ts":"'$(date -Iseconds)'"}' >> ~/.claude/cost-log.jsonl
```

### Token Estimation
Most Claude Code sessions use roughly:
- Simple query: 5K-10K tokens
- Code generation: 20K-50K tokens
- Large refactor: 50K-100K tokens
- Full feature build: 100K-300K tokens

## Reporting Queries

### Today's spend
```bash
jq '.spent' ~/.claude/daily-cost.json
```

### This week by model
```bash
cat ~/.claude/cost-log.jsonl | jq -s '
  map(select(.ts >= "'$(date -v-7d +%Y-%m-%d)'"))
  | group_by(.model)
  | map({model: .[0].model, total: (map(.est_cost) | add), ops: length})
'
```

### Cost per phase
```bash
cat ~/.claude/cost-log.jsonl | jq -s '
  group_by(.phase)
  | map({phase: .[0].phase, total: (map(.est_cost) | add), avg: (map(.est_cost) | add / length)})
  | sort_by(-.total)
'
```
