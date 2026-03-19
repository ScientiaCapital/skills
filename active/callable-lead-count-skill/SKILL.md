---
name: callable-lead-count
description: "Daily callable lead inventory with ATL/BTL breakdown. Health check for 50+ daily dials."
schedule: "0 7 25 * * 1-5"
timezone: "America/New_York"
---

# Callable Lead Count Skill

<objective>
Generate daily inventory of callable prospects (contacts with phone numbers) in HubSpot. Apply Golden Rules filtering. Classify by ATL/BTL tier. Calculate ATL Runway metric (days of ATL dials at 15/day target). Alert if daily inventory falls below 50 or ATL inventory below 15. Support morning brief and dial-list priority-setting.
</objective>

<quick_start>
**Trigger:** M-F 7:25 AM ET (daily, before morning-brief at 7:30 AM)  
**Manual Trigger:** "Show callable leads" or "Lead inventory check"  
**Dependencies:** Requires HubSpot portal 21530819 access  
**Output:** Callable lead count by tier, ATL Runway days, health alerts
</quick_start>

<success_criteria>
- [ ] Query HubSpot for contacts with phone != null
- [ ] Apply Golden Rules (exclude customers, channel, device owners, product-page engagers)
- [ ] Classify each by ATL/BTL tier (per CLAUDE.md Decision-Maker rules)
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

## Stage 2: Apply Golden Rules Filter

**Golden Rules (Hard Exclusions):**

**Skip contacts if:**
- Email domain matches crm_customers table (customer account)
- Contact tagged "Channel Partner" (hubspot_owner_id = channel owner)
- Contact tagged "Device Owner" or in device-owner list
- Contact tagged "Product Page Engager" (marketing-only engagement)
- Job title contains BTL keywords: Technician, Support, Intern, Volunteer, Operator, Designer (non-director)
- Job title in NEVER ATL list (Warehouse Manager, Network Manager, Systems Admin, AV Tech, Graphic Design Instructor, Program Administrator, Web Designer, Classroom Support, Lab Coordinator, Maintenance, Building Engineer, Multimedia Services Manager, Video Production Specialist, Streaming Crew)
- Lead status in exclusion list: Unqualified, Opted Out, Bad Fit
- Phone number invalid or duplicate

**Retention Logic:**
- Keep contacts with hs_lead_status in: Subscriber, Qualified Lead, Inbound Lead, Marketing Qualified Lead, Sales Qualified Lead
- Keep prospects created in last 90 days
- Keep contacts with hs_analytics_num_page_views > 0 (engagement signal)

**Output:** Filtered callable list (typically 50-70% of input after Golden Rules)

---

## Stage 3: Classify by ATL/BTL Tier

**MCP Tool:** N/A (logic-based classification using jobtitle)

**Apply ATL/BTL Decision-Maker Classification (per CLAUDE.md):**

**ATL Tier (Always Prospect)** — 10 Universal Keywords:
- Chief, CIO, CTO, CFO, COO
- Vice President, VP, AVP, SVP, EVP
- President, Provost, Vice Provost
- Superintendent, Director (IT/Tech/Facilities/Academic Tech/Procurement)
- Dean, Court Administrator, Clerk of Court
- City Manager, County Manager, Senior Pastor, Executive Pastor

**GRAY Tier (Contextual - Budget Authority >$25K):**
- Manager (AV/Facilities/IT) — only if reports to Director+
- Department Chair — context-dependent (small vs large institution)
- Director of Educational Technology — depends on reporting line
- Program Director — only if dept-level budget authority

**BTL Tier (No Budget Authority):**
- Technician, Specialist, Coordinator, Support
- Administrator (Systems/Network/Database)
- Engineer (AV/Network/Systems), Operator
- Instructor, Professor, Faculty, Designer, Assistant
- Clerk (non-Court), Volunteer, Help Desk
- Student, Resident, Intern

**NEVER ATL (Automatic Exclusions):**
- Warehouse Manager, Network Manager, Systems Administrator
- AV Technician, Graphic Design Instructor
- Program Administrator, Web Designer
- Classroom Support, Lab Coordinator, Maintenance
- Building Engineer, Multimedia Services Manager
- Video Production Specialist, Streaming Crew

**Classification Algorithm:**
```
FOR each contact IN filtered_list:
  title = contact.jobtitle.lower()
  
  IF title matches any NEVER_ATL keyword:
    tier = "NEVER"
    action = "REVIEW" (may need removal from sequences)
  
  ELIF title matches any ATL keyword:
    tier = "ATL"
  
  ELIF title matches any GRAY keyword:
    tier = "GRAY"
    note = "Verify budget authority >$25K via company research"
  
  ELSE:
    tier = "BTL"
```

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

## Skill Metadata

**Version:** 1.0  
**Last Updated:** 2026-03-19  
**Author:** Tim Kipper  
**Status:** Production  
**Integration:** HubSpot (portal 21530819)  
**Tier:** P1 (Core BDR Automation)  
**Triggers:** Scheduled (M-F 7:25 AM) + Manual ("Show callable leads")  
**Dependencies:** Feeds into morning-brief (7:30 AM)
