---
name: "portfolio-deal-linker"
description: "Auto-update GTME portfolio when HubSpot deals close. Links deal outcomes (won/lost, revenue, cycle time) to the skills, automations, and outreach that influenced them — building VP BD transition evidence automatically. Runs daily at 7am CST or on-demand. Use when: 'portfolio update', 'deal closed', 'link deal to portfolio', 'gtme evidence', 'what did I influence', 'career evidence', 'transition tracker'."
---

<objective>
Automatically connect closed HubSpot deals to the skills, automations, and outreach actions that contributed to them. Builds a living GTME portfolio that proves Tim's operational leverage — time saved, revenue influenced, cost-per-deal, and automation ROI. This is career-critical evidence for the VP Business Development transition.
</objective>

<quick_start>
**Daily automated run (7am CST):**
Checks for deals closed since last run → attributes to skills/actions → updates portfolio

**On-demand:**
"portfolio update" → runs full attribution scan now
"what did I influence this month" → generates monthly impact report
"gtme evidence" → formats portfolio for interview/review context

**Trigger phrases:**
- "portfolio update" / "deal closed"
- "link deal to portfolio" / "gtme evidence"
- "what did I influence" / "career evidence"
- "transition tracker" / "show my impact"
</quick_start>

<success_criteria>
- Every closed-won deal attributed to originating skill/workflow within 24 hours
- Revenue influenced tracked with clear attribution chain
- Time-saved metrics aggregated weekly (skills that eliminated manual work)
- Portfolio evidence formatted for VP BD transition narrative
- Monthly executive summary auto-generated
- Zero missed attributions on deals Tim touched
</success_criteria>

<workflow>

## Architecture

```
SCHEDULED (7am CST)           ATTRIBUTION                 PORTFOLIO UPDATE
──────────────────────────────────────────────────────────────────────────────
HubSpot: recently closed  →  Match deal to skill that  →  Update portfolio.jsonl
deals (won + lost)        →  originated/influenced it  →  Update weekly digest
                          →  Calculate metrics         →  Update GTME narrative
                          →  Compare to manual baseline →  Career evidence file
```

## Stage 1: Detect Newly Closed Deals

Use `hubspot_search_deals` with filters:
- `dealstage` IN ('closedwon', 'closedlost')
- `closedate` >= last run timestamp (stored in `~/.claude/portfolio/last-run.json`)
- Exclude channel deals (`is_channel = true`) and owned by IDs '82625923', '423155215'

For each deal, pull:
| Field | Purpose |
|-------|---------|
| `dealname` | Identification |
| `amount` | Revenue attribution |
| `closedate` | Cycle time calculation |
| `createdate` | Pipeline velocity |
| `dealstage` | Won vs lost |
| `hubspot_owner_id` | Tim's deals only |
| Associated contacts | Who was engaged |
| Associated company | Company match |
| Deal notes/activity | Attribution signals |

## Stage 2: Skill Attribution Engine

For each closed deal, determine which skills/automations contributed:

### Attribution Signals

| Signal | Skill Attributed | How to Detect |
|--------|-----------------|---------------|
| Contact was loaded via Apollo sequence | prospect-research-to-cadence | Apollo `emailer_campaigns_search` — check if contact was in a sequence |
| MEDDIC call prep was generated | meddic-call-prep-auto | Check if company appears in call prep logs |
| Deal was flagged by momentum analyzer | deal-momentum-analyzer | Check if deal appeared in RED/YELLOW actions |
| Contact enriched via Apollo | prospect-research-to-cadence | Apollo contact create date vs deal create date |
| Outreach email was drafted | prospect-research-to-cadence | Gmail draft history for contact email |
| Clari call exists | meddic-call-prep-auto | `clari_search_calls` for company |
| Manual prospecting (no automation match) | Tim (manual) | Fallback — still counts for portfolio |

### Attribution Model
```
PRIMARY attribution (100% credit):
  → Skill that ORIGINATED the deal (first touch)

ASSIST attribution (shared credit):
  → Skills that INFLUENCED the deal (middle touches)
  → E.g., prospect-research found the contact, meddic-call-prep prepped the demo,
    deal-momentum flagged it when stalling

RECOVERY attribution:
  → If deal-momentum-analyzer flagged deal as RED/YELLOW
    AND deal subsequently closed-won
  → This is "recovered revenue" — strongest GTME evidence
```

## Stage 3: Calculate Portfolio Metrics

### Per-Deal Metrics
| Metric | Formula | Why It Matters |
|--------|---------|---------------|
| Cycle time | `closedate - createdate` | Pipeline velocity |
| Revenue | `amount` | Direct impact |
| Cost to close | Estimated from skill usage costs | Efficiency |
| Automation touches | Count of skill attributions | Leverage |
| Manual vs automated | % of deal lifecycle automated | Transition evidence |

### Aggregate Metrics (Rolling 30 days)
| Metric | Formula | Target |
|--------|---------|--------|
| Total revenue influenced | Sum of attributed closed-won deals | Track monthly |
| Deals recovered | Deals flagged RED/YELLOW → closed-won | 5-10% of pipeline |
| Time saved (hours/month) | Sum of skill time-saved estimates × usage count | 30+ hrs/mo |
| Cost per deal | Total automation cost / deals closed | < $5/deal |
| Automation coverage | Deals with ≥1 skill touch / total deals | > 80% |
| Win rate lift | Automated deal win rate vs manual baseline | Track delta |

### GTME Positioning Metrics
| Metric | Narrative | VP BD Relevance |
|--------|-----------|----------------|
| Revenue influenced/month | "I influenced $X in pipeline through automated workflows" | Revenue ownership |
| Hours saved/month | "Built systems that save 30+ hours/month of manual work" | Operational leverage |
| Cost per lead | "Reduced cost-per-qualified-lead from $X to $Y" | Unit economics |
| Recovery rate | "Recovered $18K/month in stalled pipeline through automated detection" | Pipeline management |
| Automation coverage | "80%+ of deals now touch at least one automated workflow" | Systems thinking |

## Stage 4: Update Portfolio Files

### 4a. Append to portfolio.jsonl
```json
{
  "date": "2026-03-15",
  "deal_id": "hs_12345",
  "deal_name": "Baylor University",
  "amount": 45000,
  "outcome": "closedwon",
  "cycle_days": 32,
  "primary_skill": "prospect-research-to-cadence",
  "assist_skills": ["meddic-call-prep-auto", "deal-momentum-analyzer"],
  "recovered": true,
  "recovery_skill": "deal-momentum-analyzer",
  "automation_touches": 5,
  "manual_touches": 3,
  "automation_pct": 0.625
}
```

### 4b. Update Weekly Digest
Append deal to the existing `portfolio-artifact` weekly digest with attribution details.

### 4c. Generate Monthly GTME Evidence Report

```
╔══════════════════════════════════════════════════════════════╗
║  GTME PORTFOLIO — [Month Year]                               ║
║  Tim Kipper | BDR → VP Business Development                  ║
╠══════════════════════════════════════════════════════════════╣

HEADLINE METRICS:
┌─────────────────────────────────────────────────────────────┐
│ Revenue Influenced:  $[XXX,XXX]  (XX deals)                 │
│ Pipeline Recovered:  $[XX,XXX]   (X deals saved from stall) │
│ Time Saved:          [XX] hours  ([X] min/day × [XX] days)  │
│ Automation Coverage: [XX]%       (deals with skill touch)    │
│ Cost per Deal:       $[X.XX]     (automation cost / deals)   │
└─────────────────────────────────────────────────────────────┘

SKILL ATTRIBUTION BREAKDOWN:
| Skill | Deals Influenced | Revenue | Time Saved |
|-------|-----------------|---------|------------|
| prospect-research-to-cadence | XX | $XX,XXX | XX hrs |
| meddic-call-prep-auto | XX | $XX,XXX | XX hrs |
| deal-momentum-analyzer | XX (recovered) | $XX,XXX | XX hrs |

TOP DEALS (with attribution chain):
1. [Deal] — $XX,XXX | Won
   Chain: Apollo enrich → sequence load → call prep → demo → close
   Skills: PRC → MCA → DMA

VP BD TRANSITION NARRATIVE:
"In [Month], I influenced $[X] in revenue through automated GTM systems
I designed and built. These systems saved [X] hours of manual work,
recovered $[X] in stalled pipeline, and achieved [X]% automation
coverage across the deal lifecycle. This demonstrates [operational
leverage / systems thinking / revenue ownership] at VP BD scale."

╚══════════════════════════════════════════════════════════════╝
```

</workflow>

<scheduled_automation>
## Daily 7am CST Run

**Schedule:** Daily at 7:00 AM CST (13:00 UTC), weekdays
**Task name:** "portfolio-deal-linker-daily"
**Flow:**
1. Check HubSpot for deals closed since last run
2. Attribute each deal to originating skills
3. Calculate per-deal and aggregate metrics
4. Append to portfolio.jsonl
5. Update weekly digest if new closed-wons
6. Generate monthly report if month-end

**Integration with EOD:**
When Tim says "EOD", include portfolio attribution summary for any deals closed today.
</scheduled_automation>

<dependencies>
## Required MCP Tools
- **Epiphan CRM MCP:** hubspot_search_deals, hubspot_get_deal, hubspot_search_contacts, hubspot_get_company, ask_agent (activity history for attribution)
- **Apollo MCP:** apollo_emailer_campaigns_search (check sequence enrollment history)
- **Gmail MCP:** gmail_search_messages (check draft/sent history for attribution)

## Sibling Skills Referenced
- `portfolio-artifact-skill` — Base metrics capture, weekly digest format, executive summary template
- `deal-momentum-analyzer-skill` — Recovery attribution (deals flagged RED/YELLOW that closed-won)
- `prospect-research-to-cadence-skill` — Origination attribution (Apollo sequence enrollment)
- `meddic-call-prep-auto-skill` — Influence attribution (call prep generated for deal)
- `hubspot-revops-skill` — HubSpot query patterns, deal stage definitions
</dependencies>
