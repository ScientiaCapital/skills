---
name: "prospect-research-to-cadence"
description: "End-to-end prospect research pipeline: Apollo enrichment → personalized email + call scripts → draft review → Apollo sequence load. Eliminates manual research bottleneck. Use when: 'research prospect', 'prospect [company]', 'build cadence for', 'outreach for [company]', 'research-to-cadence', 'enrich and sequence', 'new prospect batch'."
---

<objective>
Automate the full prospect research → outreach pipeline. Takes a company name, domain, or contact and produces enriched firmographics, personalized multi-touch email sequences, call scripts with MEDDIC hooks, and optionally loads contacts into Apollo sequences — all in one workflow. Draft + approve mode: research and drafts are generated, then paused for Tim's approval before loading sequences.
</objective>

<quick_start>
**Single prospect:**
"research prospect Baylor University" → enriches org + decision-makers → drafts personalized outreach → presents for approval → loads to Apollo sequence

**Batch mode:**
"build cadence for these 5 companies: [list]" → runs pipeline for each → presents batch draft → loads approved contacts

**Trigger phrases:**
- "research prospect [company/domain]"
- "build cadence for [company]"
- "outreach for [company]"
- "research-to-cadence [company]"
- "enrich and sequence [list]"
- "new prospect batch"
</quick_start>

<success_criteria>
- Company enriched with firmographics, tech stack, news, and Epiphan use case angle
- 3-5 ATL decision-maker contacts identified per approved title patterns (VP/Director/Dean/Chief/Provost = economic buyers; Managers flagged as GRAY for manual review)
- Personalized 3-touch email sequence drafted per contact
- Call script with MEDDIC discovery hooks generated
- Draft presented for Tim's approval BEFORE any sequence loading
- On approval: contacts created in Apollo + added to specified sequence
- Golden Rules exclusions enforced (no customers, no channel, no product-usage contacts)
</success_criteria>

<workflow>

## Pipeline Stages

```
INPUT                    RESEARCH                 DRAFT                    APPROVE              LOAD
─────────────────────────────────────────────────────────────────────────────────────────────────────
Company/Domain    →  Apollo Org Enrich     →  Email Sequences    →  Tim Reviews     →  Apollo Sequence
                  →  Apollo People Search  →  Call Scripts       →  Approves/Edits  →  Contact Create
                  →  Epiphan CRM Check     →  ICP Score          →                  →  Add to Cadence
                  →  Web Research          →  Pain Hypothesis    →                  →
```

## Stage 1: Research (Tools Used)

### 1a. Company Intelligence
Use these MCP tools in parallel:

| Tool | Purpose | Key Data |
|------|---------|----------|
| `apollo_organizations_enrich` | Firmographics | Industry, size, revenue, tech stack |
| `apollo_organizations_job_postings` | Hiring signals | AV/IT roles = buying signal |
| `hubspot_search_companies` | Existing relationship check | Deals, lifecycle stage |
| `crm_search_customers` | Epiphan CRM customer match | Device count, orders, channel flag |
| `analytics_search_by_email` | Device registration lookup | Registered devices by contact email |
| Web search | Recent news | Funding, expansion, leadership changes |

### 1a-bis. Clay Enrichment (Waterfall)
For companies/contacts where Apollo data is incomplete (missing phone, tech stack, or funding data):

| Tool | Purpose | Key Data |
|------|---------|----------|
| `find-and-enrich-contacts-at-company` (Clay) | Deep contact enrichment | Phone waterfall, social profiles, employment history |
| `add-contact-data-points` (Clay) | Append missing data points | Phone verification, org chart depth |
| `find-and-enrich-company` (Clay) | Company intelligence | Technographics, hiring signals, funding |

Clay acts as a **waterfall fallback** — it aggregates 50+ data providers. Use it when Apollo returns incomplete results, especially for phone numbers.

### 1b. Golden Rules Filter
**STOP and skip if ANY of these are true:**
- `lifecyclestage = 'customer'` in HubSpot
- `first_conversion` contains 'Pearl', 'setup', 'Connect', 'signup'
- Company `device_count >= 1` in Epiphan CRM
- `engagement_overview` contains product usage
- `is_channel = true`
- `hubspot_owner_id` IN ('82625923', '423155215', '190030668') — AEs: Lex Evans, Ron Epstein, Phillip Sandler
  → **90-Day Stale Exception:** If `hs_lastmodifieddate` > 90 days ago → SURFACE as `STALE AE LEAD` with ATL/BTL tier + deal value. Tim reviews to re-engage, push to demo, or help close.
  → Ron Epstein: all leads. Lex & Phil: NA only. <90 days → still exclude.

**OPERATING PRINCIPLE:** Tim is NET-NEW first, but can re-engage STALE AE leads (90+ days inactive) to recover pipeline value.

### Stage S — Suppression Gate

Before including any contact in outreach or dial output:
- **EXCLUDE** if `bdr_suppression_until` IS SET AND `bdr_suppression_until` > TODAY
- **INCLUDE** if `bdr_suppression_until` IS NOT SET (never suppressed)
- **INCLUDE** if `bdr_suppression_until` < TODAY (cooling period expired)

HubSpot filter: `propertyName: "bdr_suppression_until", operator: "NOT_HAS_PROPERTY"` OR `operator: "LT", value: TODAY_ISO`
Reference: `lead-suppression-spec` (bdr_suppressed, bdr_suppression_reason, bdr_suppression_until)

---

### 1c. Contact Discovery
Use `apollo_mixed_people_api_search` with filters:
- **Titles (ATL-only):** VP, Director, Dean, CIO, CTO, CFO, Provost, Superintendent, Court Administrator, City Manager, Senior Pastor
- **Gray Zone Titles (flag for review):** Manager (AV/Facilities/IT) — include ONLY if Apollo confirms reports to Director+ AND has delegated budget >$25K
- **Exclude (NEVER ATL):** Warehouse Manager, Network Manager, Systems Administrator, AV Technician, Graphic Design Instructor, Program Administrator, Web Designer, Classroom Support, Lab Coordinator, Maintenance, Building Engineer, Multimedia Services Manager, Video Production Specialist, Streaming Crew
- **Seniority:** director, vp, c_suite
- **Departments:** IT, engineering, operations, education
- **Limit:** 3-5 contacts per company

For each contact, run `apollo_people_match` to get verified email + phone.

### ATL/BTL Classification (applied to each discovered contact)
Classify each contact using approved title patterns (CLAUDE.md § ATL/BTL Classification v1.0):
- **ATL:** Chief, VP, Director, Dean, Provost, Superintendent, Court Administrator, City Manager, Senior Pastor, Executive Pastor
- **BTL:** Technician, Specialist, Coordinator, Support, Administrator (Systems/Network/Database), Engineer (AV/Network/Systems), Operator, Instructor/Professor/Faculty, Designer, Assistant, Clerk (non-Court Admin), Volunteer, Intern, Student, Resident, Help Desk
- **NEVER ATL:** Warehouse Manager, Network Manager, Systems Administrator, AV Technician, Graphic Design Instructor, Program Administrator, Web Designer, Classroom Support, Lab Coordinator, Maintenance, Building Engineer, Multimedia Services Manager, Video Production Specialist, Streaming Crew
- **GRAY:** Manager (AV/Facilities/IT) — ATL only if reports to Director+ AND has delegated budget >$25K. Flag for Tim's manual review before sequence load

Tag each contact: `atl_btl_tier = 'ATL' | 'BTL' | 'GRAY'`
Only ATL contacts are auto-approved for sequence loading. GRAY contacts require Tim's explicit approval. BTL contacts are deprioritized (included in batch but called last).

For contacts where `apollo_people_match` returns no phone number, fall back to Clay's `find-and-enrich-contacts-at-company` for phone waterfall.

### Phone Verification Priority
**ALWAYS attempt phone verification.** Tim needs 50+ daily dials. Every contact loaded into a sequence MUST have a verified phone number. Priority order: Apollo phone → Clay waterfall → skip if no phone found (flag for manual research).

### 1d. ICP Scoring
Score the prospect using Tim's ICP verticals:

| Vertical | Score |
|----------|-------|
| Higher Ed | 90 |
| Courts/Legal | 85 |
| Government | 80 |
| Corporate AV | 80 |
| Healthcare | 75 |
| Houses of Worship | 70 |
| K-12 | 65 |

Boost +5 for: hiring AV roles, recent facility expansion, CMS mentioned in tech stack
Boost +10 for: Extron/Matrox replacement signal (competitors exited market)

## Stage 2: Draft Outreach

### Email Sequence (3-touch)
Load `reference/email-templates.md` for templates. Customize with:
- **Touch 1 (Day 0):** Pain-forward, reference specific news/signal, single CTA (15-min call)
- **Touch 2 (Day 3):** Value prop with peer social proof (similar vertical), ask different question
- **Touch 3 (Day 7):** Breakup email with resource offer (case study or guide)

Rules:
- Under 100 words per email
- No "I hope this finds you well"
- Lead with THEIR problem, not Epiphan features
- Reference a specific trigger (job posting, news, tech stack gap)
- CTA = specific time ask ("15 minutes this Thursday?")

### Call Script
Generate MEDDIC-structured call script:
```
OPENER (15 sec): Reference email + trigger signal
PAIN PROBE (60 sec): "What's your current setup for [use case]?"
METRICS: "How are you measuring [quality/uptime/cost]?"
ECONOMIC BUYER: "Who else would need to sign off?"
DECISION CRITERIA: "What would you evaluate?"
CHAMPION TEST: "If this made sense, would you be open to a quick demo?"
```

### Deliverable Format
Present draft as structured output:

```
═══════════════════════════════════════════
PROSPECT RESEARCH: [Company Name]
ICP Score: [XX/100] | Vertical: [vertical]
═══════════════════════════════════════════

COMPANY INTEL:
- Industry: [...]
- Size: [...] employees | Revenue: [...]
- Tech stack: [...]
- Trigger signal: [...]
- Epiphan angle: [...]

CONTACTS (ready for sequence):
┌──────────────────────────────────────────┐
│ 1. [Name] — [Title] [ATL/GRAY/BTL]       │
│    Email: [...] | Phone: [...]           │
│    LinkedIn: [...]                        │
│    Personalization hook: [...]            │
└──────────────────────────────────────────┘

EMAIL SEQUENCE:
Touch 1: [subject] → [body]
Touch 2: [subject] → [body]
Touch 3: [subject] → [body]

CALL SCRIPT:
[MEDDIC-structured script]

═══════════════════════════════════════════
APPROVE? (y/edit/skip)
═══════════════════════════════════════════
```

## Stage 3: Approve
- Present draft to Tim using AskUserQuestion tool
- Options: "Approve & Load", "Edit first", "Skip this prospect"
- If edit: Tim provides changes, re-draft, re-present

## Stage 4: Load to Apollo Sequence
On approval:

1. **Create contacts** in Apollo via `apollo_contacts_create`:
   - first_name, last_name, email, organization_name, title

2. **Find target sequence** via `apollo_emailer_campaigns_search`:
   - Search by sequence name Tim specifies (or default active sequence)

3. **Add to sequence** via `apollo_emailer_campaigns_add_contact_ids`:
   - Pass contact IDs + sequence ID
   - Confirm enrollment count

4. **Optional: Create Gmail draft** via `gmail_create_draft`:
   - For high-ICP prospects (score 80+), also create a direct Gmail draft

</workflow>

<dependencies>
## Required MCP Tools
- **Apollo MCP:** organizations_enrich, organizations_job_postings, mixed_people_api_search, people_match, contacts_create, emailer_campaigns_search, emailer_campaigns_add_contact_ids, email_accounts_index (resolve `send_email_from_email_account_id` when loading contacts into sequences)
- **Clay MCP:** find-and-enrich-contacts-at-company, find-and-enrich-company, add-contact-data-points (waterfall enrichment fallback for phone numbers and deep firmographics)
- **Epiphan CRM MCP:** crm_search_customers, analytics_search_by_email, hubspot_search_companies, hubspot_search_contacts
- **Gmail MCP:** gmail_create_draft (for high-ICP direct outreach)
- **Web Search:** For news, trigger signals

## Sibling Skills Referenced
- `sales-revenue-skill` — Email templates, lead scoring tiers, MEDDIC framework
- `hubspot-revops-skill` — Golden Rules filter logic, HubSpot query patterns
- `research-skill` — Competitive intelligence, firmographic research patterns
- `CLAUDE.md § ATL/BTL Classification v1.0` — Approved title keyword patterns for ATL/BTL/Gray classification (2026-03-17)
</dependencies>

## Emit Outcome Sidecar

As the final step, write to `~/.claude/skill-analytics/last-outcome-prospect-research-to-cadence.json`:
```json
{"ts":"[UTC ISO8601]","skill":"prospect-research-to-cadence","version":"1.0.0","variant":"default",
 "status":"[success|partial|error]","runtime_ms":[estimated ms from start],
 "metrics":{"prospects_researched":[n],"emails_drafted":[n],"sequences_loaded":[n],"atl_count":[n],"icp_avg_score":[n]},
 "error":null,"session_id":"[YYYY-MM-DD]"}
```
Use status "partial" if some stages failed but results were produced. Use "error" only if no output was generated.
