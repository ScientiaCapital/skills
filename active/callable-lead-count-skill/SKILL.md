---
name: callable-lead-count
description: "Daily callable-lead inventory health check with ATL/BTL/GRAY/NEVER breakdown and ATL Runway metric for Tim's 50+ dials/day target. Alerts when total callable < 50 or ATL < 15. Use when: 'show callable leads', 'lead inventory check', 'how many callable leads', 'ATL runway', 'callable count', or the 7:25 AM scheduled run feeding morning-brief."
schedule: "0 7 25 * * 1-5"
timezone: "America/New_York"
---

# Callable Lead Count Skill

<objective>
Generate daily inventory of callable prospects (contacts with phone numbers) in HubSpot. Apply Golden Rules filtering. Classify by ATL/BTL tier. Calculate ATL Runway metric (days of ATL dials at 15/day target). Alert if daily inventory falls below 50 or ATL inventory below 15. Support morning brief and dial-list priority-setting.
</objective>

<quick_start>
**Trigger:** M-F 7:25 AM ET (daily, before morning-brief at 7:30 AM)  
**Manual Trigger:** "Show callable leads", "Lead inventory check", "how many callable leads", "ATL runway", "callable count"  
**Dependencies:** Requires HubSpot portal 21530819 access; `qualify_lead` (Epiphan AI) for dedupe + tiering  
**Output:** Callable lead count by tier, ATL Runway days, health alerts, delivered via Slack DM on the scheduled run
</quick_start>

<success_criteria>
- [ ] Query HubSpot for contacts with phone != null
- [ ] Gate every candidate through `qualify_lead` (dedupe + Golden Rules + power_level) per `skill-audit/specs/suppression-spec.md` — do not re-derive Golden Rules or ATL/BTL from local keyword lists
- [ ] Classify each by ATL/BTL tier sourced from `qualify_lead`'s `power_level` (taxonomy defined once in CLAUDE.md § ATL/BTL Classification, not restated here)
- [ ] Count totals: ATL, GRAY, BTL, NEVER (for awareness)
- [ ] Calculate ATL Runway = ATL count ÷ 15 dials/day = X days of inventory
- [ ] Calculate total Runway = total callable count ÷ 50 dials/day = X days
- [ ] Alert if ATL < 15 (⚠️ warning)
- [ ] Alert if total < 50 (🚨 critical)
- [ ] Alert if NEVER ATL > 0 (🔍 review, remove from sequences)
- [ ] Output: Summary stats + detailed table + trend vs previous day
</success_criteria>

<workflow>

## Stage 1: Query HubSpot for Callable Contacts

**MCP Tool:** `search_crm_objects` (HubSpot)

```
objectType: "contacts"
filterGroups: [{
  filters: [
    { propertyName: "phone", operator: "HAS_PROPERTY" }
  ]
}]
properties: [
  "firstname",
  "lastname",
  "email",
  "phone",
  "jobtitle",
  "company",
  "hs_lead_status",
  "hubspot_owner_id",
  "hs_analytics_num_page_views",
  "custom_atl_btl_tier",
  "custom_prospect_vertical",
  "lifecyclestage",
  "createdate"
]
limit: 100
```

**Pagination:** Loop through all results (may be 200+ contacts)

**Output:** Full contact list with all properties (no filtering yet)

---

## Stage 2: qualify_lead Gate (Golden Rules + Dedupe)

**MCP Tool:** `qualify_lead` (Epiphan AI)

Call `qualify_lead` on every contact from Stage 1 immediately after the pull — this is Gate A per `skill-audit/specs/suppression-spec.md`, and it must run before any ATL/BTL tiering. `qualify_lead` returns `category` (ideal_mql/warm/nurture/junk), `power_level` (atl/gray/btl/unknown), region, and a junk/duplicate flag, so it replaces both the hand-rolled Golden Rules keyword matching and the missing dedupe step (multi-record contacts at the same account previously double-counted inventory).

**Drop from the callable pool if:**
- `qualify_lead` flags the record as duplicate or `category == junk`
- Any Golden Rule from CLAUDE.md § Golden Rules — Lead Qualification Gates applies (customer, channel partner, product-only engager, AE-owned with <90d activity) — `qualify_lead` reflects these; treat CLAUDE.md as the source of truth on disagreement
- Lead status in exclusion list: Unqualified, Opted Out, Bad Fit
- Phone number invalid

**Retention logic:** keep contacts `qualify_lead` doesn't drop, prioritizing hs_lead_status in Subscriber/Qualified Lead/Inbound Lead/Marketing Qualified Lead/Sales Qualified Lead, prospects created in the last 90 days, and contacts with hs_analytics_num_page_views > 0.

**Fallback (only if `qualify_lead` is unreachable):** apply the Golden Rules checklist directly from CLAUDE.md rather than a locally maintained keyword list, and flag the run as degraded (no dedupe) in the outcome sidecar.

**Output:** Deduped, Golden-Rules-filtered callable list (typically 50-70% of input).

---

### Stage S — Suppression Gate

Exclude suppressed contacts before inventory count and dial queue:
- **EXCLUDE** if `bdr_suppression_until` IS SET AND `bdr_suppression_until` > TODAY
- **INCLUDE** if `bdr_suppression_until` IS NOT SET (never suppressed)
- **INCLUDE** if `bdr_suppression_until` < TODAY (cooling period expired)

HubSpot filter: `propertyName: "bdr_suppression_until", operator: "NOT_HAS_PROPERTY"` OR `operator: "LT", value: TODAY_ISO`
Reference: `lead-suppression-spec` (bdr_suppressed, bdr_suppression_reason, bdr_suppression_until)

---

## Stage 3: Classify by ATL/BTL Tier

**MCP Tool:** `qualify_lead` (Epiphan AI) — same call as Stage 2; source tier from its `power_level` field rather than re-deriving it from a local keyword list.

**Tier mapping (from `qualify_lead` output):**
```
FOR each contact IN filtered_list:
  IF power_level == "atl":
    tier = "ATL"
  ELIF power_level == "gray":
    tier = "GRAY"
    note = "Verify budget authority >$25K via company research"
  ELIF power_level == "btl":
    tier = "BTL"
  ELIF title matches CLAUDE.md's NEVER-ATL list (power_level unresolved):
    tier = "NEVER"
    action = "REVIEW" (may need removal from sequences)
  ELSE:
    tier = "BTL"  # unknown power_level, no NEVER-ATL match — treat conservatively
```

The full ATL / GRAY / BTL / NEVER keyword taxonomy is defined once in **CLAUDE.md § ATL/BTL Decision-Maker Classification** and in `skill-audit/specs/suppression-spec.md` — it is not restated here. If `qualify_lead`'s tier and the CLAUDE.md taxonomy ever disagree for a contact, CLAUDE.md wins and the mismatch should be logged for review (possible `qualify_lead` drift).

**Fallback (only if `qualify_lead` is unreachable):** classify directly against the CLAUDE.md keyword lists rather than a locally cached copy, and flag the run as degraded in the outcome sidecar.

**Output:** Classified callable contacts with tier assignment

---

## Stage 4: Calculate Callable Inventory Metrics

**Count by Tier:**
```
atl_count = count(tier == "ATL")
gray_count = count(tier == "GRAY")
btl_count = count(tier == "BTL")
never_count = count(tier == "NEVER")
total_callable = atl_count + gray_count + btl_count
```

**ATL Runway Metric:**
```
atl_runway_days = ROUND(atl_count / 15, 1)
# Tim's target: 15 ATL dials/day
# Example: 45 ATL contacts = 3 days of ATL inventory
```

**Total Runway Metric:**
```
total_runway_days = ROUND(total_callable / 50, 1)
# Tim's target: 50+ dials/day (mix of ATL, GRAY, BTL)
# Example: 200 callable = 4 days of total inventory
```

**Lead Age Metrics:**
```
avg_days_in_system = AVERAGE(TODAY() - contact.createdate)
recent_engagers = count(hs_analytics_num_page_views > 0)
```

---

## Stage 5: Generate Health Alerts

**Alert Thresholds:**

| Metric | Threshold | Alert Level | Action |
|--------|-----------|------------|--------|
| ATL count | < 15 | ⚠️ Warning | "Increase ATL prospecting (prospect-enrich + prospect-refresh)" |
| Total callable | < 50 | 🚨 Critical | "Insufficient inventory for 50 dials/day—escalate prospecting" |
| NEVER ATL count | > 0 | 🔍 Review | "X contacts in NEVER ATL tier—remove from sequences" |
| ATL Runway | < 2 days | ⚠️ Warning | "Less than 2 days of ATL dials—restock urgently" |

**Alert Output:**
```
✓ ATL inventory: 42 contacts (2.8 days runway)
✓ Total callable: 185 contacts (3.7 days runway)
🔍 NEVER ATL: 2 contacts (remove from sequences)
✓ Health: GREEN (acceptable inventory)
```

**Delivery:** On the 7:25 AM scheduled run there's no one watching chat, so any ⚠️/🚨/🔍 alert must go out, not just render to a transcript. Send via `slack_send_message` to Tim's DM (`U0AAJUZH2PK`), matching the `he-dial-queue` alert pattern. On a manual trigger, the chat response is sufficient and no Slack send is needed.

---

## Stage 6: Output Summary Report

**Format:** Markdown summary + detailed table

**Summary Section:**

```
# Daily Callable Lead Inventory — 2026-03-19

## Health Status
✓ ATL Inventory: 42 contacts (2.8 days)
✓ Total Callable: 185 contacts (3.7 days)
🔍 NEVER ATL: 2 contacts (review)

## Detailed Breakdown
| Tier | Count | % of Total | Runway Days | Status |
|------|-------|-----------|-------------|--------|
| ATL | 42 | 22.7% | 2.8 | ✓ Good |
| GRAY | 65 | 35.1% | 1.3 | ⚠️ Monitor |
| BTL | 78 | 42.2% | 1.6 | ✓ OK |
| **TOTAL** | **185** | **100%** | **3.7** | **✓ GREEN** |

## Trend vs Yesterday
- ATL: +3 (was 39)
- GRAY: -2 (was 67)
- BTL: +5 (was 73)
- Total: +6 (was 179)

## Top Companies by Leads
1. Acme Corp: 12 contacts (5 ATL)
2. State University: 8 contacts (6 ATL)
3. County Courts: 6 contacts (5 ATL)

## Activity Signal
- Recent engagers (>5 page views): 45 contacts
- Avg days in system: 23 days
- New adds (last 7 days): 18 contacts
```

**Detailed Callable Table:**

| Contact | Title | Company | Vertical | Phone | Tier | Days in System | Engagement | Sequence |
|---------|-------|---------|----------|-------|------|--------|-----------|----------|
| Jane Smith | Director of IT Services | Acme Corp | Corp AV | ✓ | ATL | 34 | 12 views | BDR_CorporateAV_1 |
| Bob Jones | Manager, IT Infrastructure | State Univ | Higher Ed | ✓ | GRAY | 45 | 3 views | BDR_HigherEd_1 |
| Carol White | AV Technician | Example Inc | Healthcare | ✓ | NEVER | 12 | 1 view | REMOVE |

---

## Stage 7: Integration with Morning Brief

**This skill feeds into morning-brief (7:30 AM):**

- Pass ATL/GRAY/BTL breakdown to morning-brief
- Pass alert flags (⚠️ warning, 🚨 critical, 🔍 review)
- Pass top 15 ATL contacts for priority dial list
- Pass runway metrics for inventory planning

**Output format for morning-brief:**
```json
{
  "atl_count": 42,
  "gray_count": 65,
  "btl_count": 78,
  "never_count": 2,
  "total_callable": 185,
  "atl_runway_days": 2.8,
  "total_runway_days": 3.7,
  "alerts": ["NEVER_ATL_REVIEW"],
  "top_atl_contacts": [
    { "name": "Jane Smith", "company": "Acme", "days_in_system": 34 },
    ...
  ]
}
```

---

## Stage 8: Comparison Metrics (Week-over-Week)

**Optional: Track 7-day trend**

| Date | ATL | GRAY | BTL | Total | ATL Runway | Status |
|------|-----|------|-----|-------|-----------|--------|
| 2026-03-19 | 42 | 65 | 78 | 185 | 2.8 | ✓ |
| 2026-03-18 | 39 | 67 | 73 | 179 | 2.6 | ✓ |
| 2026-03-17 | 35 | 64 | 70 | 169 | 2.3 | ⚠️ |
| 2026-03-16 | 32 | 62 | 68 | 162 | 2.1 | ⚠️ |

**Trend Analysis:**
- ATL growing 3-4/day (good)
- Total growing 6/day (good, at target from prospect-enrich + prospect-refresh)
- Runway stable at 2.8-3.7 days (acceptable; 2+ days is minimum)

</workflow>

---

## Emit Outcome Sidecar

As the final step, write to `~/.claude/skill-analytics/last-outcome-callable-lead-count.json`:
```json
{"ts":"[UTC ISO8601]","skill":"callable-lead-count","version":"1.0.0","variant":"default",
 "status":"[success|partial|error]","runtime_ms":[estimated ms from start],
 "metrics":{"atl_count":[n],"gray_count":[n],"btl_count":[n],"total_callable":[n],"never_atl_flagged":[n],"atl_runway_days":[n]},
 "error":null,"session_id":"[YYYY-MM-DD]"}
```
Use status "partial" if some stages failed but results were produced. Use "error" only if no output was generated. If Stage 2/3 ran in the `qualify_lead`-unreachable fallback mode, use "partial" and note the degraded dedupe/tiering in `error`.

---

<dependencies>
## MCP tools
- **HubSpot:** `search_crm_objects` (Stage 1 pull)
- **Epiphan AI:** `qualify_lead` (Stage 2 dedupe + Golden Rules gate, Stage 3 ATL/BTL tiering)
- **Slack:** `slack_send_message` (Stage 5 alert delivery on the scheduled run)

## Reference, not restated here
- `skill-audit/specs/suppression-spec.md` — `qualify_lead` as the single gate contract (dedupe + Golden Rules + power_level)
- `CLAUDE.md` § Golden Rules — Lead Qualification Gates, and § ATL/BTL Decision-Maker Classification — full keyword taxonomy

## Sibling skills referenced (reuse, don't rebuild)
- `he-dial-queue` — Slack alert delivery pattern
- `sdr-dial-lists`, `morning-brief` — overlapping inventory/consumption; this skill is the health-check source of truth, not a dial-list builder
</dependencies>

---

## Skill Metadata

**Version:** 1.1  
**Last Updated:** 2026-07-06  
**Author:** Tim Kipper  
**Status:** Production  
**Integration:** HubSpot (portal 21530819) + Epiphan AI (`qualify_lead`) + Slack (alert delivery)  
**Tier:** P1 (Core BDR Automation)  
**Triggers:** Scheduled (M-F 7:25 AM) + Manual ("Show callable leads", "lead inventory check", "ATL runway")  
**Dependencies:** Feeds into morning-brief (7:30 AM)
