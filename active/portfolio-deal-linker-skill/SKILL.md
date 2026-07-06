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
- Apply the CLAUDE.md Golden Rules lead-qualification gates (customers, channel partners, product-only engagers, geo). For the AE-owned exclusion, use the canonical owner list there (Lex Evans `82625923`, Ron Epstein `423155215`, Phillip Sandler `190030668`) — this is a **90-day stale exception, not a hard exclude**: if last activity on an AE-owned deal is >90 days old (Ron Epstein: all leads; Lex Evans/Phillip Sandler: North America only), surface it as a `STALE AE LEAD` in the portfolio run rather than dropping it.

**last-run.json missing/corrupt recovery:** Before querying, read `~/.claude/portfolio/last-run.json`. If the file is missing, unparseable, or its `last_run_ts` is not a valid timestamp:
1. Default the incremental window to a trailing 24 hours (`now - 24h`) instead of guessing or failing.
2. Mark this run's outcome sidecar `status` as `"partial"` and add `"degraded_window":"missing_last_run_json"` (or `"corrupt_last_run_json"`) to `metrics` so the gap is visible downstream.
3. Proceed with the scan using the 24h fallback window — never crash the run or silently assume a wider/narrower window.
4. On successful completion, (re)write `~/.claude/portfolio/last-run.json` with the current run timestamp so the next run recovers a normal incremental window.

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
| Activity history exists | meddic-call-prep-auto | `ask_agent` — query activity timeline for company |
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

## Stage 5: Comp Plan Attainment Tracker

Calculate daily progress against Tim's 2026 BDR comp plan targets.

### Current Month Targets
ALWAYS resolve targets for the CURRENT month from the Monthly Target Lookup table below (never hardcode a month). Since June 2026 Tim is on full quota: 24 deals/mo, $714K pipeline/mo; H2 revenue targets rise monthly. Stretch = 126%+ of target (1.5x accelerator). Daily run rate = monthly target / business days in month.

### Calculation Logic
1. Query HubSpot for deals created this month where Tim is owner (87486452) or collaborator
2. Sum `amount` for pipeline generated
3. Sum `amount` where `dealstage` = 'closedwon' for revenue
4. Calculate:
   - **Pipeline attainment %** = total pipeline / monthly target × 100
   - **Revenue attainment %** = total closed-won / monthly target × 100  
   - **Deal count attainment %** = deals created / monthly target × 100
   - **Accelerator zone**: <100% = base, 100-110% = 1.0x, 111-125% = 1.25x, 126%+ = 1.5x
   - **Days remaining** = business days left in month
   - **Required daily run rate** = (target - achieved) / days remaining

### Output Format (append to daily portfolio report)
```
📊 COMP PLAN TRACKER — {Month YYYY} ({Phase from lookup table})
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Pipeline:  $XXX,XXX / ${month pipeline target}  (XX% — Zone: BASE/1.0x/1.25x/1.5x)
Revenue:   $XX,XXX / ${month revenue target}   (XX% — Zone: BASE/1.0x/1.25x/1.5x)
Deals:     X / {month deal target}             (XX%)
Days left: X business days
Gap to stretch: $XXX,XXX pipeline | $XX,XXX revenue | X deals
Daily run rate needed: $X,XXX pipeline | $X,XXX revenue
```

### Monthly Target Lookup (for future months)
| Month | Deals | Pipeline | Revenue | Phase |
|-------|-------|----------|---------|-------|
| March | 12 | $357K | $125K | Ramp 50% |
| April | 16 | $464K | $163K | Ramp 65% |
| May | 20 | $607K | $212K | Ramp 85% |
| June | 24 | $714K | $250K | Full (H1) |
| July | 24 | $714K | $475K | Full (H2) |
| August | 24 | $714K | $475K | Full (H2) |
| September | 24 | $714K | $500K | Full (H2) |
| October | 24 | $714K | $525K | Full (H2) |
| November | 24 | $714K | $550K | Full (H2) |
| December | 24 | $714K | $600K | Full (H2) |

Dynamically select targets based on current month.

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
- **Gmail MCP:** search_threads (check draft/sent history for attribution)
- `qualify_lead` — dedupe when matching attributed contacts against already-qualified leads

## Sibling Skills Referenced
- `portfolio-artifact-skill` — Base metrics capture, weekly digest format, executive summary template
- `deal-momentum-analyzer-skill` — Recovery attribution (deals flagged RED/YELLOW that closed-won)
- `prospect-research-to-cadence-skill` — Origination attribution (Apollo sequence enrollment)
- `meddic-call-prep-auto-skill` — Influence attribution (call prep generated for deal)
- `hubspot-revops-skill` — HubSpot query patterns, deal stage definitions

## Failure Handling
If `hubspot_search_deals` fails (timeout, rate limit, auth error): retry once with backoff, then skip the stage and mark the run `"partial"` rather than aborting the whole workflow — downstream stages (attribution, metrics) should still run on whatever deals were already fetched, if any. Append one line per run to `~/.claude/skill-runs/portfolio-deal-linker.jsonl` (`{ts, status, deals_seen, degraded_window, error}`) so incremental-window and retry failures are visible across runs, not just in the latest sidecar.

## Emit Outcome Sidecar

As the final step, write to `~/.claude/skill-analytics/last-outcome-portfolio-deal-linker.json`:
```json
{"ts":"[UTC ISO8601]","skill":"portfolio-deal-linker","version":"1.0.0","variant":"default",
 "status":"[success|partial|error]","runtime_ms":[estimated ms from start],
 "metrics":{"deals_linked":[n],"skills_attributed":[n],"revenue_tracked_usd":[n],"degraded_window":"[none|missing_last_run_json|corrupt_last_run_json]"},
 "error":null,"session_id":"[YYYY-MM-DD]"}
```
Use status "partial" if some stages failed but results were produced, or if the last-run.json fallback window was used. Use "error" only if no output was generated.
</dependencies>
