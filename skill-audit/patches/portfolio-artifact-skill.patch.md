# Patch: portfolio-artifact-skill

**Score:** trigger=4 tool_integration=4 output_contract=3 failure_handling=3 maintainability=5 (sum=19/25)

**Highest-leverage single change (M effort):** Make the deliverable a real HTML Artifact for the weekly/exec summary (or rename the skill), and flag missing cost/git data instead of defaulting to 0
**Expected impact:** Name matches output, and reports stop silently under-reporting on days with missing source files

## Description

**Before:**
> Auto-extract GTME metrics from work sessions. Lines shipped, bugs fixed, PRs merged, cost per feature. Weekly digests and executive summaries. Use when: capture metrics, portfolio report, what did I ship, weekly summary.

*(trigger_quality > 3 — no description rewrite proposed)*

## Findings & fixes

### [MED] output_contract
- **Evidence** (line 2,82): "name: "portfolio-artifact" ... echo "{\"date\":\"$DATE\",...}" >> ~/.claude/portfolio/daily-metrics.jsonl"
- **Issue:** Skill is named 'artifact' and success criteria mention 'artifacts_generated', yet all outputs are Markdown templates + a JSONL file — no actual Artifact/HTML deliverable or delivery mechanism defined.
- **Fix:** Render the weekly/exec summary as an HTML Artifact (matching the name) or rename to portfolio-metrics; declare the delivery target explicitly.

### [LOW] trigger_quality
- **Evidence** (line 32-35): "<triggers>
- "capture metrics", "portfolio report", "what did I ship"
- "weekly summary", "executive summary", "sprint report""
- **Issue:** Good explicit triggers, but 'weekly summary'/'executive summary' collide with weekly-kpi-report-skill and business-pulse-skill; 'cost per feature' overlaps cost-metering-skill.
- **Fix:** Scope triggers to engineering/dev-session metrics to disambiguate from GTM KPI reporting.

### [LOW] failure_handling
- **Evidence** (line 80): "COST=$(cat ~/.claude/daily-cost.json 2>/dev/null | jq '.spent // 0')"
- **Issue:** Bash uses 2>/dev/null and // 0 defaults so a missing cost file degrades to 0 silently — a $0 day looks real.
- **Fix:** Emit a 'cost_data_missing' flag in the metric row when daily-cost.json is absent.

### [LOW] maintainability
- **Evidence** (line 186): "**Deep dive:** See `reference/metrics-guide.md`, `reference/report-templates.md`"
- **Issue:** Compact (198 lines) with clean progressive disclosure; no drifting hardcoded values. Strength.
- **Fix:** None.

## Self-healing gap (see specs/self-healing-template.md)

Silent-default bash (|| echo 0, // 0) degrades missing inputs to zero with no alert or run log; no retry ladder and no ~/.claude/skill-runs entry — a failed git/gh/jq call produces a plausible-but-wrong metric row rather than a flagged partial.

## Overlap candidates (flag only — no removal)

- weekly-kpi-report-skill
- cost-metering-skill
- business-pulse-skill
- executive-dashboard-generator
