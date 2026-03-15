# Agent Swarm — Autonomous Build System

Your projects build themselves while you work BDR.

## How It Works

```
  7:00 AM ──→ 2 Ghostty agents spin up (projects A, B)
    ↓           Each reads PLANNING.md → builds → simplifies → reviews → ships
  8:00 AM ──→ You start BDR dials. Agents finishing in background.
    ↓
  1:00 PM ──→ 2 more Ghostty agents spin up (projects C, D)
    ↓           Same workflow: build → simplify → review → ship
  5:00 PM ──→ EOD summary generates automatically
    ↓           Shows what 4 agents accomplished today
  Next day ──→ Rotation advances to next 4 projects
```

## Rotation Math

With ~40 projects at 4/day (weekdays only): **full rotation every 10 business days = 2 weeks**.
Every project gets autonomous attention twice a month.

## Scheduled Tasks (auto-running)

| Task | Schedule | What it does |
|------|----------|-------------|
| `morning-agent-swarm` | 7:00 AM M-F | Launch 2 agents on next rotation projects |
| `afternoon-agent-swarm` | 1:00 PM M-F | Launch 2 more agents on next rotation projects |
| `eod-agent-summary` | 5:00 PM M-F | Generate daily report of agent activity |

## Manual Commands

```bash
# Launch agents RIGHT NOW (next 2 in rotation)
~/Desktop/tk_projects/skills/scripts/swarm-now.sh

# Launch 4 agents at once (full day batch)
~/Desktop/tk_projects/skills/scripts/swarm-now.sh 4

# Launch agent on a SPECIFIC project
~/Desktop/tk_projects/skills/scripts/swarm-now.sh 1 chamba

# Check status between BDR calls
~/Desktop/tk_projects/skills/scripts/agent-status-check.sh

# Dry run (see what would launch without actually launching)
~/Desktop/tk_projects/skills/scripts/agent-swarm-launcher.sh --count 2 --block am --dry-run
```

## What Each Agent Does

1. **Context** — Reads CLAUDE.md, checks git status
2. **Plan** — Reads PLANNING.md, picks top priority task
3. **Build** — Implements the task with production-quality code
4. **Simplify** — Strips over-engineering
5. **Review** — Checks for bugs, security, conventions
6. **Ship** — Commits with conventional message, pushes
7. **Report** — Creates .agent-status file with results

## Key Files

| File | Purpose |
|------|---------|
| `~/.claude/rotation-state.json` | Tracks which projects are next |
| `~/.claude/agent-logs/` | Full logs from each agent session |
| `PROJECT/.agent-status` | Agent's report on what it did |
| `costs/daily-YYYY-MM-DD-agents.md` | EOD summary report |

## Project Requirements

For a project to be included in rotation, it needs:
- `CLAUDE.md` or `.claude/` directory in the project root
- `PLANNING.md` or `BACKLOG.md` with prioritized tasks
- Lives in `~/Desktop/tk_projects/`

## Troubleshooting

**Agents not launching?**
- Ensure Ghostty is running
- Check: `which ghostty` and `which claude`
- Run with `--dry-run` to test without launching

**Wrong projects selected?**
- Check pointer: `jq '.pointer' ~/.claude/rotation-state.json`
- Reset: `jq '.pointer = 0' ~/.claude/rotation-state.json > tmp && mv tmp ~/.claude/rotation-state.json`

**Memory issues?**
- Script auto-reduces to 1 agent if memory pressure is high
- Close Chrome tabs before agent blocks launch
- Max 2 agents on 8GB, 3-4 on 16GB+

## GTME Lens

- **Operational leverage**: 4 projects advance daily with zero manual effort
- **Cost-per-project**: ~$0.50-2.00 in API costs per agent session
- **Portfolio velocity**: Full portfolio rotation every 2 weeks
- **Position as**: "Autonomous engineering pipeline — managed 40 concurrent projects using parallel agent orchestration"
