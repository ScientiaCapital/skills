---
name: "dead-deal-recovery"
description: "Identify stalled and dying deals, run structured disqualification or recovery workflows, and clean pipeline of dead weight. Finds deals stuck 60+ days, with no champion, no activity, or overdue close dates and prescribes either a final re-engagement campaign or formal disqualification. Keeps pipeline honest and frees mental bandwidth. Use when: 'dead deals', 'stalled deals', 'clean pipeline', 'pipeline cleanup', 'disqualify deals', 'deal graveyard', 'zombie deals', 'which deals should I kill', 'pipeline hygiene', 'deal recovery', 'win back', 'lost deal review', 'close out stale deals'."
---

<objective>
Prevent pipeline rot by systematically identifying deals that should be recovered or killed. Most BDR pipelines carry 20-30% dead weight: deals that will never close but consume mindshare and inflate forecasts. This skill runs a diagnostic on every open deal, classifies each as RECOVERABLE or DEAD, executes a final re-engagement attempt for recoverable deals, and formally disqualifies the rest. Target: clean 15-20% of stalled pipeline monthly, recover 5-10% of "dead" deals via structured last-chance campaigns.
</objective>

<quick_start>
**Weekly pipeline hygiene:**
"clean pipeline" → scans all open deals → classifies recoverable vs dead → recommends actions

**Specific deal:**
"should I kill the Acme deal?" → analyzes that deal specifically → recommendation

**Recovery campaign:**
"run recovery on stalled deals" → generates re-engagement emails for recoverable deals

**Trigger phrases:**
- "dead deals" / "stalled deals" / "zombie deals"
- "clean pipeline" / "pipeline cleanup" / "pipeline hygiene"
- "disqualify deals" / "which deals should I kill"
- "deal recovery" / "win back" / "lost deal review"
</quick_start>

<success_criteria>
- Every open deal classified: HEALTHY, RECOVERABLE, or DEAD
- Zero deals sitting in pipeline over 90 days without deliberate justification
- Final re-engagement attempt made before ANY disqualification
- Lost reason documented for every disqualified deal
- Pipeline accuracy improves: weighted pipeline reflects reality within 15%
</success_criteria>

<workflow>

## Architecture

```
TRIGGER                 DIAGNOSIS                  TRIAGE                    ACTION
──────────────────────────────────────────────────────────────────────────────────────
"clean pipeline"  →  Pull all open deals   →  Score deal health    →  HEALTHY: monitor
                  →  Activity history       →  Classify H/R/D      →  RECOVERABLE: re-engage
                  →  Contact engagement     →  Identify root cause  →  DEAD: disqualify
                  →  MEDDIC completeness    →  Predict recovery %   →  Gmail drafts
                  →  Close date integrity   →                       →  HubSpot updates
```

## Stage 1: Data Collection

### 1a. Pull All Open Deals
**FilterGroup 1 — Tim is COLLABORATOR:**
- `hs_all_collaborator_owner_ids` CONTAINS_TOKEN `87486452`
- `hs_is_closed` EQ `false`

**FilterGroup 2 — Tim is OWNER:**
- `hubspot_owner_id` EQ `87486452`
- `hs_is_closed` EQ `false`

**Properties:** dealname, dealstage, amount, hubspot_owner_id, hs_lastmodifieddate, closedate, createdate, num_associated_contacts, hs_deal_stage_probability

### 1b. Activity History per Deal
| Tool | Purpose |
|------|---------|
| `ask_agent` | "Show all activity for [company] deals in last 90 days" |
| `hubspot_get_deal` | Deal notes, stage change history |

### 1c. Contact Engagement + Clari Check
| Tool | Purpose |
|------|---------|
| `hubspot_search_contacts` | Email opens, clicks, last engagement date |
| `clari_search_calls` | Calls in last 60 days |
| `clari_get_call_summary` | Last call sentiment |

## Stage 2: Deal Health Diagnosis

Score each deal on 5 death signals (0-20 pts each, 100 total).

### Signal 1: Activity Recency (0-20)
| Last activity | Score |
|--------------|-------|
| < 7 days | 20 |
| 7-14 days | 15 |
| 14-30 days | 8 |
| 30-60 days | 3 |
| 60+ days | 0 — DEAD SIGNAL |

### Signal 2: Champion Engagement (0-20)
| Status | Score |
|--------|-------|
| Active champion responding | 20 |
| Responded in last 14 days | 15 |
| Last response 14-30 days | 8 |
| Ghosting 30+ days | 2 |
| No champion ever identified | 0 |

### Signal 3: Close Date Integrity (0-20)
| Status | Score |
|--------|-------|
| Future, never pushed | 20 |
| Pushed once, still future | 12 |
| Pushed 2+ times | 5 |
| Past (overdue) | 0 — OVERDUE |

### Signal 4: MEDDIC Completeness (0-20)
| Status | Score |
|--------|-------|
| 5-6 dimensions identified | 20 |
| 3-4 dimensions | 12 |
| 1-2 dimensions | 5 |
| 0 dimensions | 0 — UNQUALIFIED |

### Signal 5: Stakeholder Breadth (0-20)
| Contacts | Score |
|----------|-------|
| 3+ contacts including ATL (economic buyer) | 20 |
| 2+ contacts with ≥1 ATL | 15 |
| 2+ contacts but all BTL | 8 |
| Single-threaded (1 contact only) | 3 |
| 0 active contacts | 0 — ABANDONED |

### Classification
| Total | Class | Action |
|-------|-------|--------|
| 60-100 | HEALTHY | Monitor via deal-momentum-analyzer |
| 30-59 | RECOVERABLE | Run recovery campaign |
| 0-29 | DEAD | Recover in 14 days or disqualify |

### Root Cause Mapping
| Root Cause | Recovery Strategy |
|-----------|-------------------|
| GHOST | Multi-channel blitz: email + call + LinkedIn |
| NO_CHAMPION | Find new contact via Apollo |
| SINGLE_THREADED | Research org chart, find peer or manager |
| BUDGET_STALL | Re-engage at next budget cycle |
| COMPETITOR_WIN | Log intel. Re-engage in 12 months. |
| TIMING | Set calendar reminder for stated timeline |
| UNQUALIFIED | Disqualify immediately |

## Stage 3: Recovery Campaign (3-touch, 10 days)

**Email 1 — Check-In (Day 0):** Tactical empathy. "It's been a while since we connected about [topic]..."

**Email 2 — Value Bomb (Day 4):** Challenger reframe with new case study or vertical insight.

**Email 3 — Break-Up (Day 10):**
```
Subject: Should I close your file?

Hi [First Name], I haven't heard back — one of three things:
1. Timing isn't right (totally understand)
2. You've gone a different direction (helpful to know)
3. You're buried and this fell off the radar

Would it be a terrible idea to reconnect next quarter instead?
```

Create Gmail drafts via `gmail_create_draft` for all 3 touches.

## Stage 4: Disqualification Protocol

Before closing any deal as Lost:
1. ☐ Final recovery email sent (Email 3: Break-Up)
2. ☐ At least one call attempt made
3. ☐ 14-day waiting period after last recovery touch
4. ☐ Root cause identified and documented
5. ☐ Lost reason selected in HubSpot

**HubSpot actions on disqualification:**
- Move deal to "Closed Lost" with reason + notes
- Create follow-up reminder at re-engagement date (if applicable)

## Stage 5: Output Format

```
╔══════════════════════════════════════════════════════════════╗
║  PIPELINE CLEANUP REPORT — [Date]                            ║
║  Open Deals: [X] | Pipeline: $[total]                        ║
╠══════════════════════════════════════════════════════════════╣

🟢 HEALTHY: [X] deals ($[amount]) — no action
🟡 RECOVERABLE: [X] deals ($[amount]) — recovery campaign
🔴 DEAD: [X] deals ($[amount]) — disqualify within 14 days
💀 PIPELINE DEAD WEIGHT: [X]% of deals

🟡 RECOVERABLE — TAKE ACTION THIS WEEK:
1. [Deal] — $[amt] | Root cause: [X] | Recovery plan: [X]
   → Gmail draft created: Yes/No

🔴 DEAD — DISQUALIFY:
2. [Deal] — $[amt] | Evidence: [X] | Learning: [X]

PIPELINE IMPACT:
Before: $[current] | After cleanup: $[cleaned]
╚══════════════════════════════════════════════════════════════╝
```

## Stage 6: Lost Deal Review (Monthly)

Pull all deals closed as Lost in last 30 days and analyze:
1. Win rate by vertical
2. Loss by root cause
3. Loss by pipeline stage
4. MEDDIC correlation with win rate
5. Recovery success rate

</workflow>

<scheduled_automation>
## Recommended Cadence

| Frequency | Action |
|-----------|--------|
| Weekly (Friday) | Full pipeline cleanup scan |
| Daily | Check for deals crossing 60-day stall threshold (via morning-brief) |
| Monthly | Lost deal review + pattern analysis |
| On-demand | "should I kill [deal]" |
</scheduled_automation>

<dependencies>
## Required MCP Tools
- **Epiphan CRM MCP:** hubspot_search_deals, hubspot_get_deal, hubspot_search_contacts, hubspot_search_companies, ask_agent
- **Epiphan Clari MCP:** clari_search_calls, clari_get_call_summary
- **Gmail MCP:** gmail_create_draft
- **Apollo MCP:** enrich_contact (find new contacts for single-threaded deals)

## Sibling Skills Referenced
- `deal-momentum-analyzer` — Shares deal health scoring; dead-deal-recovery goes deeper on RED deals
- `morning-brief` — Daily feed of deals approaching death thresholds
- `meddic-call-prep-auto` — If recovery call needed, generates MEDDIC brief
</dependencies>

## Emit Outcome Sidecar

As the final step, write to `~/.claude/skill-analytics/last-outcome-dead-deal-recovery.json`:
```json
{"ts":"[UTC ISO8601]","skill":"dead-deal-recovery","version":"1.0.0","variant":"default",
 "status":"[success|partial|error]","runtime_ms":[estimated ms from start],
 "metrics":{"deals_scanned":[n],"healthy":[n],"recoverable":[n],"dead":[n],"recovery_drafts_created":[n]},
 "error":null,"session_id":"[YYYY-MM-DD]"}
```
Use status "partial" if some stages failed but results were produced. Use "error" only if no output was generated.
