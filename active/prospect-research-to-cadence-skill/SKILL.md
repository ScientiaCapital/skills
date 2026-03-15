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
- 3-5 decision-maker contacts identified (VP/Director/Dean level = economic buyers)
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
- `hubspot_owner_id` IN ('82625923', '423155215') — These are AEs (Lex Evans, Phil Sanders). Also exclude Ron and Anthony's deals.

**OPERATING PRINCIPLE:** NEVER chase deals or opportunities attached to AEs Lex, Phil, Ron, or Anthony. Tim is NET-NEW only.

### 1c. Contact Discovery
Use `apollo_mixed_people_api_search` with filters:
- **Titles:** VP, Director, Dean, Manager of AV/IT/Media/Instructional Technology
- **Seniority:** director, vp, c_suite
- **Departments:** IT, engineering, operations, education
- **Limit:** 3-5 contacts per company

For each contact, run `apollo_people_match` to get verified email + phone.

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
│ 1. [Name] — [Title]                      │
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
</dependencies>
