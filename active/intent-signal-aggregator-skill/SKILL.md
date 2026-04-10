---
name: intent-signal-aggregator-skill
description: Monitor buyer intent signals across the web including job postings, tech changes, funding rounds, and leadership changes. Alerts when prospects show buying signals and prioritizes "hot" accounts. Use for timing-based prospecting.
---

# Intent Signal Aggregator

<objective>
Monitor buyer intent signals across the web — job postings, tech changes, funding rounds, and leadership changes — to identify when prospects are in-market. Aggregates signals from multiple sources, scores account "heat," and alerts on high-intent accounts so you can time outreach for maximum impact.
</objective>

<quick_start>
**Trigger:** "track intent signals for [company/account list]" or "which accounts are showing buying signals?"
**Output:** Prioritized intent signal report with hot accounts, signal tracking, and recommended actions
</quick_start>

<success_criteria>
- [ ] Signals categorized by urgency (high/medium/low intent)
- [ ] Each account scored with intent score and evidence
- [ ] Recommended actions and talking points provided per hot account
- [ ] Weekly digest with hottest accounts and watch list
</success_criteria>

<workflow>

## Stage G — Golden Rules Gate (apply before scoring any account)

Before surfacing any company or contact in the intent report, disqualify records matching:

1. **Customers:** `lifecyclestage = customer` OR `device_count >= 1` → **EXCLUDE** (they already own Epiphan gear)
2. **Channel Partners:** `is_channel = true` → **EXCLUDE**
3. **AE-Owned:** `hubspot_owner_id` IN `[82625923 (Lex), 423155215 (Ron), 190030668 (Phil)]`
   - If last activity **< 90 days** → **EXCLUDE** (AE actively working it)
   - If last activity **≥ 90 days** → **SURFACE** as `STALE AE LEAD` with intent score, signal evidence, and recommended action (Tim decides)
4. **Geo Gate:** Non-USA/Canada → **EXCLUDE** unless explicitly requested

Check HubSpot via `mcp__claude_ai_Epiphan_Ai__hubspot_search_companies` or `mcp__claude_ai_Epiphan_Ai__hubspot_search_contacts` before including any account. If found as customer/channel partner → skip silently.

---

### Stage S — Suppression Gate

Before including any contact in outreach or dial output:
- **EXCLUDE** if `bdr_suppression_until` IS SET AND `bdr_suppression_until` > TODAY
- **INCLUDE** if `bdr_suppression_until` IS NOT SET (never suppressed)
- **INCLUDE** if `bdr_suppression_until` < TODAY (cooling period expired)

HubSpot filter: `propertyName: "bdr_suppression_until", operator: "NOT_HAS_PROPERTY"` OR `operator: "LT", value: TODAY_ISO`
Reference: `lead-suppression-spec` (bdr_suppressed, bdr_suppression_reason, bdr_suppression_until)

---

## Instructions

You are an expert at identifying buyer intent signals that indicate a company is in-market for solutions like yours. Your mission is to aggregate signals from multiple sources and alert on "hot" accounts showing strong buying intent — filtering to qualified net-new prospects only.

### Intent Signals

**High-Intent Signals** (Act Within Days):
- Posted job listing for role that uses your product
- Raised funding (Series A/B/C)
- Key executive just joined
- Mentioned your category in job description
- Attending/speaking at relevant conference

**Medium-Intent Signals** (Act Within Weeks):
- Hiring in relevant department (3+ roles)
- Announced partnership related to your space
- Published content about problem you solve
- Tech stack changes visible
- Company reaching certain growth milestone

**Low-Intent Signals** (Nurture, Monitor):
- General company growth (headcount up)
- New market expansion
- Product launch in adjacent space
- Following your company on LinkedIn
- Downloading your content

### Output Format

```markdown
# Intent Signal Report

**Report Period**: [Date Range]
**Accounts Monitored**: [X] companies
**High-Intent Signals**: [X] accounts
**Medium-Intent Signals**: [X] accounts

---

## 🔥 HOT ACCOUNTS (High Intent)

### #1: [Company Name] - 🔴 URGENT

**Intent Score**: 95/100

**Signals Detected**:
1. **Posted 5 job listings** for [relevant role] (2 days ago)
   - Source: LinkedIn Jobs
   - Evidence: JD mentions "[technology you integrate with]"
   - Why it matters: They're scaling the team that uses your product

2. **Announced $25M Series B** (1 week ago)
   - Source: TechCrunch
   - Lead Investor: [VC Name]
   - Why it matters: Fresh capital = budget for new tools

3. **New VP of [Department] joined** (3 weeks ago)
   - Name: [Person Name]
   - Previous Company: [Company] (your customer!)
   - Why it matters: New execs bring new vendors

**Recommended Action**: Reach out THIS WEEK
**Contact**: [Decision Maker Name], [Title]
**Talking Point**: "Congrats on the Series B! With 5 new [role] hires, I imagine [pain point]..."

---

## 📊 Signal Tracking

**By Signal Type**:
| Signal | # Accounts | Avg Days to Reach Out | Win Rate |
|--------|-----------|----------------------|----------|
| Funding | 15 | 3-5 days | 18% |
| Hiring | 28 | 7 days | 12% |
| Leadership Change | 12 | 14 days | 22% |
| Tech Stack | 8 | 21 days | 15% |

**Best Signals**: Leadership changes + Hiring = 35% win rate

---

## 🎯 Weekly Digest

**This Week's Hottest Accounts**:
1. [Company] - Raised $X, hiring Y roles
2. [Company] - New CTO, expanding team
3. [Company] - Posted job mentioning your category

**Next Week's Watch List**:
- [Company] - Series B expected
- [Company] - Conference attendance
- [Company] - Tech migration underway

```

Remember: Intent signals are about TIMING. Same prospect, different time = different outcome!

## Emit Outcome Sidecar

As the final step, write to `~/.claude/skill-analytics/last-outcome-intent-signal-aggregator.json`:
```json
{"ts":"[UTC ISO8601]","skill":"intent-signal-aggregator","version":"1.0.0","variant":"default",
 "status":"[success|partial|error]","runtime_ms":[estimated ms from start],
 "metrics":{"accounts_scanned":[n],"signals_detected":[n],"hot_accounts":[n],"signal_types":{"funding":[n],"hiring":[n],"leadership":[n],"tech_stack":[n]}},
 "error":null,"session_id":"[YYYY-MM-DD]"}
```
Use status "partial" if some stages failed but results were produced. Use "error" only if no output was generated.

</workflow>
