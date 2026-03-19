---
name: morning-brief
description: "Daily briefing with calendar, CRM priority dial list, deal momentum summary, and Gmail drafts for each lead."
schedule: "0 7 30 * * 1-5"
timezone: "America/New_York"
---

# Morning Brief Skill

<objective>
Generate Tim's daily briefing (Monday-Friday 7:30 AM) with calendar, HubSpot hot leads for dialing, deal momentum scores, recent Clari call summaries, and personalized Gmail drafts for each priority dial list contact. Integrate health metrics from callable-lead-count. Skip leads in Supabase cooldown. Output single-page HTML brief for quick review before 50+ daily dials.
</objective>

<quick_start>
**Trigger:** M-F 7:30 AM ET (after callable-lead-count at 7:25 AM)  
**Manual Trigger:** "Show morning brief" or "Today's dial list"  
**Dependencies:** Requires HubSpot (portal 21530819), Google Calendar, Clari, Supabase (disposition check)  
**Output:** Single-page HTML brief with calendar, dial list (20 ATL contacts), deal momentum, call summaries, draft emails
</quick_start>

<success_criteria>
- [ ] Pull Tim's calendar for today (meetings, breaks, focus blocks)
- [ ] Pull 15-20 hot leads from HubSpot (ATL-first sort, high engagement)
- [ ] Filter: skip leads in Supabase cooldown (disposition_cooldown_until > NOW)
- [ ] Enrich each lead: company, title, last touch, recent activity
- [ ] Fetch deal momentum scores for leads (from deal-momentum-analyzer or calculated)
- [ ] Check Clari for calls from last 7 days (summaries, key takeaways)
- [ ] Create Gmail draft for each lead (using prospect-refresh templates or custom)
- [ ] Output: HTML brief with calendar, dial list, deal pipeline, call highlights, drafts ready
- [ ] Report: dial target (15-20 ATL), meeting blocks, deal momentum trends
</success_criteria>

<workflow>

## Stage 1: Pull Tim's Calendar for Today

**MCP Tool:** `gcal_list_events`

```
calendarId: "primary"
timeMin: TODAY 00:00:00
timeMax: TODAY 23:59:59
timeZone: "America/New_York"
condenseEventDetails: true
```

**Extract and Display:**
- All meetings with times, attendees, duration
- Focus blocks or "Do Not Disturb" blocks
- Lunch/break time
- Available dial windows (gaps between meetings)

**Calendar Output:**
```
## Today's Calendar

09:00 - 09:30  | All Hands (Zoom)
09:30 - 10:30  | [AVAILABLE FOR DIALS] 60 min
10:30 - 11:15  | 1:1 with Manager
11:15 - 12:00  | [AVAILABLE FOR DIALS] 45 min
12:00 - 13:00  | LUNCH
13:00 - 14:30  | [AVAILABLE FOR DIALS] 90 min
14:30 - 15:00  | Clari Call Review
15:00 - 16:00  | [AVAILABLE FOR DIALS] 60 min
16:00 - 17:00  | Admin / Wrap-up
```

**Dial Window Summary:** Total 255 min = 4.25 hours available for dials (target 50 dials at ~5 min/dial)

---

## Stage 2: Pull Hot Leads from HubSpot

**MCP Tool:** `search_crm_objects` (HubSpot)

```
objectType: "contacts"
filterGroups: [{
  filters: [
    { propertyName: "phone", operator: "HAS_PROPERTY" },
    { propertyName: "hs_lead_status", operator: "IN", values: ["Qualified Lead", "Sales Qualified Lead"] },
    { propertyName: "hs_analytics_num_page_views", operator: "GTE", value: "3" }
  ]
}]
properties: [
  "firstname", "lastname", "email", "phone", "jobtitle", "company",
  "custom_atl_btl_tier", "custom_prospect_vertical", "hs_analytics_num_page_views",
  "hubspot_owner_id", "hs_lastmodifieddate", "createdate", "custom_last_touch",
  "lifecyclestage", "custom_deal_momentum_score"
]
sorts: [{
  propertyName: "custom_atl_btl_tier",
  direction: "ASCENDING"  # ATL first
}]
limit: 50
```

**Filter + Sort Logic:**
1. Phone must exist (callable)
2. Lead status in engaged tiers (Qualified Lead, Sales Qualified)
3. Engagement signal: >3 page views OR recent activity (<7 days)
4. Sort by: custom_atl_btl_tier (ATL > GRAY > BTL)
5. Within tier, sort by: hs_lastmodifieddate DESC (most recent first)

**Trim to top 25 candidates** (will further filter in Stage 3)

---

## Stage 3: Apply Supabase Cooldown Filter

**Check Supabase disposition table for cooldown status**

**Query:** disposition table where contact_id = hubspot_contact_id AND disposition_cooldown_until > NOW()

**Cooldown Rules (per disposition policy):**
- Voicemail left: 24-hour cooldown
- Call declined/busy: 2-hour cooldown (can retry)
- Call connected but wrong person: 24-hour cooldown
- Call connected and scheduled: 7-day cooldown (follow-up call)
- Lead opted out: 30-day cooldown or permanent "Do Not Call"

**Filter Logic:**
```
FOR each contact IN hot_leads_list:
  IF contact_id in supabase disposition AND cooldown_until > NOW():
    SKIP contact
    LOG: "In cooldown until {cooldown_until}"
  ELSE:
    KEEP contact (ready to dial)
```

**Output:** Filtered dial list (typically 15-20 after cooldown filter)

---

## Stage 4: Enrich Leads with Deal + Activity Data

**For each remaining lead, enrich:**

**Step A: Check deal association via HubSpot**

**MCP Tool:** `search_crm_objects` (HubSpot deals)

```
filterGroups: [{
  associatedWith: [{
    objectType: "contacts",
    operator: "EQUAL",
    objectIdValues: [contact_id]
  }]
}]
properties: ["dealname", "dealstage", "amount", "closedate", "custom_deal_momentum_score"]
limit: 5
```

**Output per contact:**
- Associated deals (max 3)
- Deal stage (Negotiation, Qualification, etc.)
- Deal size
- Deal momentum score (if calculated by deal-momentum-analyzer)

**Step B: Check Clari calls (last 7 days)**

**MCP Tool:** `clari_search_calls`

```
attendeeEmail: contact.email
daysBack: 7
limit: 5
```

**Extract:**
- Call date/time
- Duration
- Summary of key topics
- Action items (from AI notes)

**Step C: Get last touch info**

- Pull custom_last_touch field from HubSpot (set by prior activities)
- Alternative: query hs_lastmodifieddate
- Display: "Last touched 3 days ago" or "Last call 2026-03-15"

---

## Stage 5: Calculate Deal Momentum Scores

**MCP Tool:** Epiphan CRM `ask_agent` OR pull from HubSpot custom field

**For each lead's associated deals, calculate momentum:**

**Momentum Scoring Factors:**
1. **Stage Progression:** +3 if moved in last 7 days
2. **Contact Breadth:** +2 if ATL contact involved, +1 per GRAY contact
3. **Activity Cadence:** +2 if >2 activities last 7 days, +1 if 1 activity
4. **Recency:** +2 if activity <2 days ago, +1 if <5 days
5. **Deal Size:** +1 if >$100K

**Momentum Tiers:**
- 10+ = 🔥 Hot (near close, high activity, ATL engaged)
- 7-9 = ✓ Warm (progressing, some ATL involvement)
- 4-6 = ⚬ Cool (early stage, low activity)
- <4 = ❄️ Cold (stalled)

**Output example:**
```
Jane Smith @ Acme Corp
  Deal: "Acme AV Suite" ($250K, Negotiation stage)
  Momentum: 🔥 10/10 (ATL + VP Sales, moved stage 3 days ago)
  Last touch: 2026-03-17 (call with VP)
```

---

## Stage 6: Check Recent Clari Calls

**MCP Tool:** `clari_search_calls`

```
repEmail: "tkipper@epiphan.com"
daysBack: 7
status: "POST_PROCESSING_DONE"
limit: 10
```

**Extract call summaries:**

**MCP Tool:** `clari_get_call_summary` (for each call)

```
callId: call_uuid
# Returns: summary, action_items, key_takeaways, attendees
```

**Display format:**
```
## Recent Calls (Last 7 Days)

### 2026-03-18 — State University (45 min)
Attendee: Dr. Janet Lee, Director of Academic Technology
Summary: Discussed hybrid learning infrastructure. Interest in lecture capture.
Takeaway: Promised demo of Epiphan Pearl Nano + Canvas integration
Action Items: [Send demo link by 2026-03-20]

### 2026-03-15 — County Courts (30 min)
Attendee: Tom Miller, Court Administrator
Summary: Current process: manual video setup + USB drives. Pain point: compliance archival.
Takeaway: High interest in automation. Will present to judge committee.
Action Items: [Follow-up after judge meeting, 2026-03-25]
```

**Trends:**
- Top pain points mentioned
- Products/features mentioned most
- Follow-up actions due
- Deals progressed

---

## Stage 7: Create Gmail Drafts for Priority Leads

**For each lead in final dial list (15-20), create Gmail draft:**

**MCP Tool:** `gmail_create_draft`

**Draft Template Strategy:**

**Template A — High Momentum Deal (Momentum 8+):**
```
To: jane@acme.com
Subject: RE: Acme AV Suite Demo — Next Steps

Hi Jane,

Following up on our call with your VP of IT on 3/17—thanks again for the positive feedback on the Pearl Nano demo.

Quick question before we schedule the next phase: Does the Board need to review the budget approval, or can we move forward to contract review?

I have a demo with another client at 2pm today, but I'm free 10-11am or 2-3pm this week to talk through the Canvas integration setup.

Best,
Tim
---
Epiphan Video | BDR
```

**Template B — New ICP Lead (No Prior History):**
```
To: bob@example.com
Subject: Video infrastructure question for Example Inc

Hi Bob,

I was researching Example Inc's recent expansion and noticed your focus on hybrid learning.

Quick question: How are you currently handling lecture recordings—do you capture them today, or is that a gap you're filling?

No sales pitch—just trying to understand the landscape at companies your size.

Best,
Tim
```

**Template C — Warm Lead (Momentum 4-6):**
```
To: carol@company.com
Subject: Checking in on that Epiphan demo

Hi Carol,

We talked about the Pearl Mini setup on 3/12—wanted to see if you had a chance to review the spec sheet I sent.

Any initial questions, or is now a good time for a 15-min call to walk through the install process?

Available today 1-2pm or tomorrow morning.

Best,
Tim
```

**Draft Creation Logic:**
```
FOR each contact IN dial_list:
  IF contact.deal_momentum_score > 8:
    use_template = "A_High_Momentum"
  ELIF contact.last_touch > 7 days ago:
    use_template = "B_New_Lead"
  ELSE:
    use_template = "C_Warm_Lead"
  
  personalize_template(contact, company, last_touch, deal)
  create_gmail_draft(to=contact.email, subject=..., body=...)
```

**DO NOT SEND—leave as draft for Tim's manual review + send-from-draft workflow**

---

## Stage 8: Generate HTML Morning Brief

**Output:** Single-page, printable HTML with:

**Brief Header:**
```
╔═══════════════════════════════════════════════════╗
║         MORNING BRIEF — 2026-03-19 (Wednesday)    ║
║              Tim Kipper, BDR at Epiphan           ║
╚═══════════════════════════════════════════════════╝

DIAL TARGET: 20 ATL/GRAY prospects | AVAILABLE TIME: 4.25 hours (255 min)
MOMENTUM SUMMARY: 3 Hot (8+), 8 Warm (4-6), 9 Cool (<4)
CALLABLE INVENTORY: 185 total | 42 ATL (2.8 days runway)
```

**Section 1: Today's Calendar**
- Visual timeline of meetings + dial windows
- Color coding: meetings = blocked, dials = open, breaks = rest

**Section 2: Priority Dial List (Sortable)**

| # | Name | Title | Company | Phone | Vertical | Tier | Momentum | Last Touch | Deal | Gmail |
|---|------|-------|---------|-------|----------|------|----------|-----------|------|-------|
| 1 | Jane Smith | Dir. IT Services | Acme Corp | [copy] | Corp AV | ATL | 🔥 10 | 3/17 | Acme AV Suite ($250K) | [Open Draft] |
| 2 | Bob Jones | Manager, AV | State Univ | [copy] | Higher Ed | GRAY | ✓ 8 | 3/15 | [None] | [Open Draft] |
| 3 | Carol White | IT Director | County Courts | [copy] | Courts | ATL | 🔥 9 | 3/18 | Courthouse AV ($180K) | [Open Draft] |

**Section 3: Deal Pipeline Overview**

| Deal | Stage | Amount | Momentum | Dial Target | Action |
|------|-------|--------|----------|------------|--------|
| Acme AV Suite | Negotiation | $250K | 🔥 10 | Jane Smith | Send demo by 3/20 |
| State Univ Hybrid | Qualification | $120K | ✓ 8 | Bob Jones + Carol White | Schedule tech call |
| County Courts Archive | Discovery | $180K | ✓ 7 | Carol White | Present to judge committee |

**Section 4: Recent Call Highlights**

```
🔥 HIGH PRIORITY FOLLOW-UPS

▸ 2026-03-18: State University (45 min)
  Dr. Janet Lee promised to present to committee.
  ACTION: Follow-up call scheduled for 2026-03-25
  
▸ 2026-03-15: County Courts (30 min)
  High interest in compliance archival. Manual process is pain.
  ACTION: Send compliance white paper + archive demo
```

**Section 5: Health Metrics**

```
INVENTORY STATUS
✓ ATL Runway: 2.8 days (42 contacts at 15 dials/day) — ACCEPTABLE
✓ Total Runway: 3.7 days (185 contacts at 50 dials/day) — GOOD
⚠️ Trending: +6 leads yesterday (+3.2% day-over-day) — ON TRACK

WEEKLY TARGETS (Tim's Ramp 50% = 12 deals minimum)
Deals Closed YTD: 8
Deals in Pipeline: 12
Dial Pace: 45 dials/day (target 50) — ON TRACK
```

**Section 6: Today's Tasks**

```
□ Execute 50 dials (focus: Top 20 ATL leads)
□ Review + send personalized Gmail drafts (one per lead)
□ Follow-up on 2 Clari action items (State Univ, Courts)
□ Update deal stages after calls
□ Log dispositions in Supabase (for cooldown tracking)
```

---

## Stage 9: Email Brief to Tim

**Optional: Auto-send brief to tkipper@epiphan.com as HTML email OR embed in dashboard**

**Email Format:**
- Subject: "Morning Brief — [DATE] — 20 ATL Prospects Ready"
- Body: HTML brief (styled, clickable draft links)
- Attachments: Dial list CSV for easy copy-paste of phone numbers

**Alternative:** Save brief as HTML file + link from Slack/dashboard

---

## Stage 10: Integration with Supabase Disposition Log

**After Tim completes dials, disposition data flows to Supabase:**

```sql
INSERT INTO disposition (
  contact_id, call_date, outcome, duration_seconds,
  notes, deal_id, next_action, disposition_cooldown_until
) VALUES (...)
```

**Next day's brief automatically excludes contacts in cooldown.**

</workflow>

---

## Skill Dependencies

**Upstream (Required to run first):**
1. prospect-enrich (Monday 6:00 AM) — phoneless enrichment
2. prospect-refresh (Monday 6:30 AM) — net-new ICP search
3. sequence-load (Monday 7:15 AM) — auto-enroll in sequences
4. callable-lead-count (M-F 7:25 AM) — inventory health check

**Downstream (Feeds from this brief):**
- Tim's manual dialing workflow (7:30 AM - 5:00 PM)
- Disposition logging to Supabase (cooldown tracking)
- Deal momentum updates (to deal-momentum-analyzer)

---

## Skill Metadata

**Version:** 1.0  
**Last Updated:** 2026-03-19  
**Author:** Tim Kipper  
**Status:** Production  
**Integration:** HubSpot (21530819) + Google Calendar + Clari + Supabase + Gmail  
**Tier:** P1 (Core BDR Automation)  
**Triggers:** Scheduled (M-F 7:30 AM) + Manual ("Show morning brief")  
**Dependencies:** prospect-enrich → prospect-refresh → sequence-load → callable-lead-count → morning-brief
