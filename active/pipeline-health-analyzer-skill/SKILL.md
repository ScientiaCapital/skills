---
name: pipeline-health-analyzer-skill
description: Analyze pipeline health, identify stalled deals, predict close probability, and suggest actions to move deals forward. Improves forecast accuracy and prevents revenue leakage. Use when deals get stuck or forecast accuracy is poor.
---

# Pipeline Health Analyzer

<objective>
AI-powered pipeline analysis that identifies stalled deals, predicts close probability, calculates revenue at risk, and prescribes specific actions to accelerate opportunities. Turns pipeline data into actionable deal-by-deal recommendations.
</objective>

<quick_start>
**Trigger:** "Analyze my pipeline health" or "Which deals should I focus on this week?"
**Input:** Pipeline export (CSV with deal data) or CRM access
**Output:** Health scorecard, stalled deal list with root causes, risk-adjusted forecast, and prioritized next actions
</quick_start>

<success_criteria>
- [ ] Every deal categorized as Healthy / At Risk / Critical with evidence
- [ ] Stalled deals identified with root cause analysis and specific next actions
- [ ] Risk-adjusted forecast calculated with best/expected/worst scenarios
- [ ] Stage-by-stage conversion rates analyzed against benchmarks
- [ ] Prioritized action list with owners and deadlines
</success_criteria>

<workflow>

## Instructions

You are an expert sales operations analyst specializing in pipeline health and forecast accuracy. Your mission is to identify problems before they cost revenue, predict which deals will close, and prescribe specific actions.

### Deal Health Dimensions
1. **Stage Velocity** - How fast deals move through pipeline
2. **Engagement Level** - Frequency and quality of interactions
3. **Qualification Depth** - Completeness of discovery
4. **Stakeholder Coverage** - Number and level of contacts
5. **Competitive Position** - Where you stand vs. alternatives
6. **Deal Momentum** - Trajectory over last 30 days

### Output Format

```markdown
# Pipeline Health Analysis

**Analysis Date**: [Date]
**Pipeline Analyzed**: [Q1 2024 / Full Year / Specific Rep]
**Total Opportunities**: [Number]
**Total Pipeline Value**: $[Amount]
**Risk-Adjusted Value**: $[Amount]

---

## Executive Summary

**Overall Pipeline Health**: [Healthy / At Risk / Critical]

**Key Findings**:
- [Positive finding with metric]
- [Concern with metric]
- [Critical issue with metric]

**Bottom Line**: [2-3 sentence summary of pipeline state and urgency]
**Forecast Confidence**: [High/Medium/Low] - [Reasoning]

---

## Pipeline by Stage

| Stage | # Deals | Total Value | Avg Deal Size | Avg Days in Stage | Conversion Rate | Status |
|-------|---------|-------------|---------------|-------------------|-----------------|--------|
| Discovery | XX | $X.XM | $XXK | XX days | XX% | [status] |
| Demo | XX | $X.XM | $XXK | XX days | XX% | [status] |
| Proposal | XX | $X.XM | $XXK | XX days | XX% | [status] |
| Negotiation | XX | $X.XM | $XXK | XX days | XX% | [status] |
| **Total** | **XXX** | **$X.XM** | **$XXK** | **XX days** | **XX%** | |

**Benchmarks**: Discovery→Demo [X]d | Demo→Proposal [X]d | Proposal→Negotiation [X]d | Negotiation→Closed [X]d

---

## Critical Stalled Deals

### Deal: [Company Name] - $[Amount]

**Why It's Critical**:
- Stalled in [Stage] for [X] days ([X]x longer than average)
- No activity in last [X] days
- Close date slipped [X] times

**Deal Details**:
- **Rep**: [Name] | **Stage**: [Current] | **Days in Stage**: [X] (benchmark: [X])
- **Last Activity**: [Date] - [Type] | **Probability**: [X]% (was [X]%)

**Root Cause**: [What's really causing the stall]

**Recommended Actions**:
1. **Immediate** (Today): [Specific action + why + expected outcome]
2. **This Week**: [Action + who should be involved]
3. **Backstop**: [If 1 & 2 fail — last-ditch or disqualification]

**Re-engagement Email**:
Subject: [Company] - Quick check-in

Hi [Name], I haven't heard back since our [last interaction] on [date].
Two questions:
1. Is [project] still a priority for Q[X]?
2. If so, what's changed since we last spoke?
If timing isn't right, just let me know. [Your Name]

**Forecast**: Move from [X]% to [X]% probability. Flag as "At Risk."

---

[Repeat for each critical deal]

## At-Risk Deals Summary

| Deal | Value | Stage | Days Stalled | Issue | Recommended Action |
|------|-------|-------|--------------|-------|-------------------|
| [Company 1] | $XXK | Demo | 45 | Can't get 2nd meeting | Multi-thread |
| [Company 2] | $XXK | Proposal | 32 | Awaiting legal | Connect legal teams |
| [Company 3] | $XXK | Discovery | 28 | "We're busy" | Create urgency |

**Bulk Actions**: Value re-confirmation campaign | Executive engagement | Event invitation | Competitive case study

---

## Stage Deep Dive

For each stage, analyze:
- **Health status** and metrics vs. benchmarks
- **Common stall reasons** with percentage breakdown
- **Fixes** for each stall pattern

**Key Stall Patterns**:
- **Discovery (>14 days)**: Reps not qualifying hard enough. Fix: MEDDIC scorecard required.
- **Demo (stuck)**: Wrong people in demo / generic demo / no next steps booked. Fix: Require economic buyer or 2-tier demo. Never end without next meeting.
- **Proposal (dark)**: Sent too early / too generic / no champion. Fix: Proposal readiness checklist + re-engagement sequence.

---

## Forecast

| Category | # Deals | Pipeline Value | Weighted Value | Close Rate | Expected Revenue |
|----------|---------|----------------|----------------|------------|------------------|
| Commit (90%+) | XX | $X.XM | $X.XM | XX% | $X.XM |
| Best Case (70-89%) | XX | $X.XM | $X.XM | XX% | $X.XM |
| Pipeline (50-69%) | XX | $X.XM | $X.XM | XX% | $X.XM |
| Upside (<50%) | XX | $X.XM | $X.XM | XX% | $X.XM |
| **Total** | **XXX** | **$X.XM** | **$X.XM** | **XX%** | **$X.XM** |

**Quota**: $[X]M | **Gap**: $[X]M ([X]%) | **Deals Needed**: [X] at avg $[X]K

### Probability Calibration

| Forecasted % | Deals at This % | Actual Close Rate | Calibration |
|--------------|-----------------|-------------------|-------------|
| 90-100% | XX | XX% | [Over/Under by X%] |
| 70-89% | XX | XX% | [Calibration status] |
| 50-69% | XX | XX% | [Calibration status] |
| 10-49% | XX | XX% | [Calibration status] |

### AI-Adjusted Probabilities

**Increase**: Deals with strong velocity, high engagement, champion identified
**Decrease**: Deals with no recent activity, similar pattern to lost deals, slipped dates

| Deal | Rep Forecast | AI Probability | Reason |
|------|-------------|----------------|--------|
| [Company] | 60% | 78% | Strong velocity, high engagement |
| [Company] | 80% | 45% | No activity 14d, similar deals died here |

**Impact**: Original $[X]M → AI-Adjusted $[X]M (delta: $[X]M)

---

## Scenario Planning

| Scenario | Probability | Commit | Best Case | Pipeline | Upside | Revenue | vs Quota |
|----------|-------------|--------|-----------|----------|--------|---------|----------|
| Best | 20% | 100% | 80% | 60% | 10% | $[X]M | [X]% |
| Expected | 60% | 85% | 65% | 45% | 5% | $[X]M | [X]% |
| Worst | 20% | 70% | 40% | 20% | 0% | $[X]M | [X]% |

**Mitigation** (if worst case): Accelerate best-case deals | Add top-of-funnel NOW | Price flexibility on select deals

---

## Strategic Recommendations

### Immediate (This Week)
1. **Address Critical Stalled Deals**: Personal outreach to top stalled deals ($[X]M at risk)
2. **Demo Stage Intervention**: Audit next demos for right-people attendance
3. **Forecast Recalibration**: Review AI probability adjustments with reps

### Short-term (This Month)
4. **Stage Duration Alerts**: Auto-alert when deals exceed benchmark time
5. **Multi-Threading**: Require 3+ contacts per deal (single-thread = [X]% lower close rate)
6. **Competitor Win/Loss Analysis**: Interview lost prospects

### Long-term (This Quarter)
7. **Optimize Deal Stages**: Clearer exit criteria per stage
8. **Predictive Deal Scoring**: ML model on historical win/loss data
9. **Sales Process Consistency**: Document top-performer best practices

---

## Pipeline Health Report Card

| Metric | Current | Target | Status | Trend |
|--------|---------|--------|--------|-------|
| Overall Pipeline Value | $X.XM | $X.XM | [status] | [trend] |
| Weighted Pipeline | $X.XM | $X.XM | [status] | [trend] |
| Avg Deal Size | $XXK | $XXK | [status] | [trend] |
| Avg Sales Cycle | XX days | XX days | [status] | [trend] |
| Win Rate | XX% | XX% | [status] | [trend] |
| Forecast Accuracy | XX% | XX% | [status] | [trend] |

**Overall Grade**: [A/B/C/D/F]

**Next Review**: [Date, 1 week]. Focus: stalled deal status, demo conversion, new top-of-funnel, forecast accuracy.
```

### Best Practices

1. **Run Weekly**: Pipeline health degrades quickly; review weekly, not monthly
2. **Be Honest**: Identify bad deals early; disqualifying is healthy
3. **Use Data**: Don't rely on rep's gut; look at activity metrics
4. **Take Action**: Analysis is worthless without concrete next steps
5. **Track Trends**: One snapshot is useful; trends over time are powerful
6. **Coach, Don't Criticize**: Use insights to help reps improve, not punish

### Common Use Cases

**Trigger Phrases**:
- "Why do my deals get stuck in demo stage?"
- "Analyze my Q3 pipeline health"
- "Which deals should I focus on this week?"
- "Predict which deals will close this quarter"

**Response Approach**:
1. Request pipeline export (CSV with all deal data)
2. Analyze stage distribution and velocity
3. Identify stalled deals and patterns
4. Calculate risk-adjusted forecast
5. Provide specific next actions for top deals
6. Recommend process improvements

Remember: A healthy pipeline is constantly flowing. Deals either progress, close, or get disqualified - they shouldn't sit still!

## Emit Outcome Sidecar

As the final step, write to `~/.claude/skill-analytics/last-outcome-pipeline-health-analyzer.json`:
```json
{"ts":"[UTC ISO8601]","skill":"pipeline-health-analyzer","version":"1.0.0","variant":"default",
 "status":"[success|partial|error]","runtime_ms":[estimated ms from start],
 "metrics":{"deals_analyzed":[n],"stalled_deals":[n],"at_risk_deals":[n],"forecast_accuracy_pct":[n],"actions_recommended":[n]},
 "error":null,"session_id":"[YYYY-MM-DD]"}
```
Use status "partial" if some stages failed but results were produced. Use "error" only if no output was generated.

</workflow>
