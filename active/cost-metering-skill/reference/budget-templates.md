# Budget Templates

## Hobby/Personal ($50/month)
```json
{
  "budget_monthly": 50,
  "budget_daily": 2,
  "alerts": {"info": 0.5, "warn": 0.7, "block": 0.9},
  "strategy": "Haiku-first. Sonnet only for code generation. No Opus."
}
```

## Professional ($100/month)
```json
{
  "budget_monthly": 100,
  "budget_daily": 5,
  "alerts": {"info": 0.5, "warn": 0.8, "block": 0.95},
  "strategy": "Sonnet default. Haiku for search/review. Opus for architecture."
}
```

## Team/Enterprise ($500/month)
```json
{
  "budget_monthly": 500,
  "budget_daily": 25,
  "alerts": {"info": 0.5, "warn": 0.8, "block": 0.95},
  "strategy": "Sonnet default. Opus when needed. Parallel agents OK."
}
```

## Monthly Budget Calculator

| Activity | Frequency | Model | Est. Cost |
|----------|-----------|-------|-----------|
| Start Day scan | 20/mo | haiku | $0.40 |
| Feature builds | 10/mo | sonnet | $20.00 |
| Code reviews | 15/mo | haiku | $0.30 |
| Research sprints | 5/mo | sonnet | $5.00 |
| Debug sessions | 8/mo | sonnet | $8.00 |
| End Day sweep | 20/mo | haiku | $0.40 |
| **Total** | | | **~$34/mo** |

Most developers spend $30-60/month with Sonnet-default routing.
