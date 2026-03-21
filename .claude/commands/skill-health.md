---
description: "Run skill health analysis on outcome data"
argument-hint: "[--quick]"
allowed-tools: Read, Bash, Glob, Write, Agent
---

# /skill-health — Skill Health Analysis

## Instructions

Check `$ARGUMENTS` for the mode:

### Quick mode (`--quick`)
Run the bash-only report (no LLM cost):
```bash
bash scripts/skill-health-report.sh --days 30
```
Show the output directly. Done.

### Full mode (default, no args)
1. Run `bash scripts/skill-health-report.sh --days 30` first for a quick summary
2. Then spawn a `skill-health-observer` agent (defined in `.claude/agents/skill-health-observer.md`) for deep analysis
3. The agent will produce `.claude/observers/SKILL_HEALTH.md` with health scores, gap detection, and recommendations
4. Show the user: "Health report written to `.claude/observers/SKILL_HEALTH.md`" with a summary of findings

### If no outcome data exists
Say: "No outcome data yet. Run pilot skills (prospect-enrich, morning-brief) to generate outcomes, or use `/skill-feedback <skill> <status> <notes>` to log manually."
