# Metrics Guide

## What to Capture

### Git-Based Metrics (Automatic)
| Metric | Command | Notes |
|--------|---------|-------|
| Commits today | `git log --since="today 00:00" --oneline \| wc -l` | Raw count |
| Features shipped | `git log --since="today" --grep="^feat" --oneline \| wc -l` | Conventional commits |
| Bugs fixed | `git log --since="today" --grep="^fix" --oneline \| wc -l` | Conventional commits |
| Lines added | `git diff --stat \| tail -1` | Parse insertions |
| Lines removed | `git diff --stat \| tail -1` | Parse deletions |
| Files changed | `git diff --stat \| tail -1` | Parse file count |
| Tests added | `git diff --stat -- '*.test.*' '*.spec.*' \| wc -l` | Test file changes |

### Cost Metrics (From cost-metering)
| Metric | Source | Notes |
|--------|--------|-------|
| Daily spend | `~/.claude/daily-cost.json` | Updated by cost gate |
| Cost per feature | Total / feat count | Derived |
| Cost per bug fix | Total / fix count | Derived |

### GitHub Metrics (Optional)
| Metric | Command | Notes |
|--------|---------|-------|
| PRs created | `gh pr list --author @me --state all` | Requires gh CLI |
| PRs merged | `gh pr list --author @me --state merged` | Requires gh CLI |
| Issues closed | `gh issue list --assignee @me --state closed` | Requires gh CLI |

## How to Measure Impact

### Quantitative
- Lines shipped per day (productivity)
- Cost per feature (efficiency)
- Bug fix rate (quality)
- Test coverage delta (reliability)

### Qualitative
- Complexity of features built
- Architecture decisions made
- Knowledge areas expanded
- Tools/techniques discovered

## Data Quality

- Use conventional commits (`feat:`, `fix:`, `docs:`) for accurate counting
- Log costs at end of each workflow phase
- Capture metrics daily for trend analysis
- Weekly aggregation smooths out variance
