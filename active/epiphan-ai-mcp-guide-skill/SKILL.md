---
name: epiphan-ai-mcp-guide
description: Epiphan AI MCP tool picker — which tool answers which question across HubSpot CRM (read + admin-scoped writes + static lists), legacy CRM orders, Pearl device analytics, Clari calls, qualify_lead, enrich_contact, curated query_dataset/weekly_brief reports, and Semrush/GA4/GAds marketing intel. Use when: "which Epiphan tool for X", "look up a customer", "sales brief", "qualify a lead", "find the AV/IT director", "pull pipeline", "weekly sales tracker", "tool seems missing / wrong namespace".
---

# Epiphan AI — MCP Tools Guide

<objective>
Day-one reference for the Epiphan AI MCP toolset — which tool answers which question across CRM sales
data, device analytics, HubSpot CRM (read + admin-scoped writes), Clari call recordings, contact
enrichment, lead qualification, curated analytics datasets, and marketing intel (Semrush/GA4/GAds).
Use it to pick the right tool fast, know its defaults and caveats, and avoid the wrong namespace.
</objective>

<quick_start>
1. **Start with `ask_agent`** — natural language handles most questions (revenue, calls, products, pricing).
2. **Direct lookups** → the "All Available Tools" table below (e.g. `sales_brief` for a customer, `weekly_brief` for the tracker, `qualify_lead` for inbound, `query_dataset` for repeatable numbers).
3. **Namespace:** default to **`Epiphan Ai`**, not the `Epiphan CRM` subset (see Namespaces section).
4. **Deeper reference in this skill's folders:**
   - `resources/` — per-domain tool guides: `crm-tools.md`, `sales-tools.md`, `enrichment-tools.md`, `product-tools.md`, `marketing-tools.md`
   - `reference/` — `tool-examples.md` (worked examples) and `verticals.md` (5-vertical persona pack)
5. Customer-facing assets → defer to the `epiphan-brand-assets` skill (separate Epiphan Brand MCP).
</quick_start>

Epiphan AI gives you access to CRM sales data, device analytics, HubSpot CRM, call recordings, contact enrichment, lead qualification, and marketing analytics — all through natural language.

## What You Can Do

### Sales & Revenue

**Ask anything about sales data.** Revenue, customers, products, trends — from 2010 to today. All currencies auto-converted to USD.

> "Top 10 customers by revenue in 2025"
> "Monthly sales trend for Pearl Mini last 2 years"
> "Compare Q1 vs Q2 by region"
> "Which products have declining sales?"
> "Pearl Nano vs Pearl Mini revenue comparison"
> "New customers acquired in 2025"
> "Customers who haven't ordered in 6 months"
> "Average order value by customer segment"
> "80/20 analysis — who are the customers driving 80% of revenue?"

### Customer Deep Dive

**Get a complete picture of any customer in one shot.** Just say the name — fuzzy matching handles misspellings.

> "Sales brief for B&H Photo"
> "Tell me everything about Stanford University"
> "Customer brief for University of Toronto"

Returns: company info, 12-month revenue, top products, open deals, key contacts, recent notes.

**Look up specific orders or history:**

> "Show B&H Photo order history"
> "Find order PO-2024-1234"
> "All orders for customer ID 5678 in 2024"

### Call Prep & Handoffs

**Before a call — get fully prepared:**

> "Sales brief for MIT"
> "Search Clari for calls with mit.edu in the last 90 days"
> "Show engagement timeline for MIT — last 6 months"
> "What's the deal pipeline for MIT?"

**After a call — hand off to AE:**

> "Create AE handoff for MIT, contact: john.smith@mit.edu"

Generates: bottom line summary, pre-call tasks for AE, aggregated intel from CRM + devices + Clari calls + HubSpot engagement. Optionally creates a HubSpot note.

**Optional `ebStrategy` block** — when provided, it's appended to the handoff note as an "Economic Buyer Strategy" section AND written to the deal's `eb_intel` custom properties:
- `ebTitleHypothesis` — hypothesized EB title (e.g. "VP Academic Affairs")
- `ebPriorityHypothesis` — which EB priority the pain maps to
- `championActivationStatus` — `exploring | activated | pursuing`
- `doubleUpfrontSeeded` — boolean
- `knownEvalSteps` — string array (e.g. IT security review, faculty pilot)

Omit `ebStrategy` and the handoff is unchanged (backward-compatible). HubSpot writes are admin-scoped.

### BDR Call Activity & Coaching

> "How many calls did Tim make today?"
> "Dials to connect ratio for the BDR team this week"
> "Total talk time by rep this month"
> "Who did rhaynes call yesterday?"
> "Any booked demos from calls this week?"
> "Rep leaderboard for the last 30 days"

**Clari call intelligence:**

> "Summarize Clari calls about Nexus products"
> "Get summary for call ID 12345"
> "Search Clari for calls with competitor mentions"

### Task Briefs (Sales Rep Accountability)

**See overdue + upcoming HubSpot tasks per rep.** Highlights "follow up on sales related support ticket" tasks (auto-created from CS_Tickets pipeline) — most commonly missed.

> "Task brief for Tim"
> "Show overdue tasks for Lex Evans"
> "Team task brief"

Returns: overdue / due-today / upcoming with deal context.

### AE Drift Detection

**Find contacts and deals that drifted away from a rep.** Useful for handoff tracking and pipeline hygiene — surfaces records currently owned by other AEs where the target rep had recent engagement.

> "What drifted away from Phillip in the last 7 days?"
> "AE drift check for Lex"

`days` lookback: min 1, **max 30**, default 7.

### Lead Qualification

**Qualify inbound leads automatically.** Detects junk, classifies against ICP, routes to region, drafts outreach email.

> "Qualify lead 12345"
> "Is contact 67890 a good lead?"
> "Classify and write email for HubSpot contact 11111"

Returns: category (ideal_mql / warm_lead / nurture / junk), confidence score, region (NA/EMEA/APAC), `power_level` (atl / btl / unknown — above/below the line buyer authority), suggested email draft.

**`writeToHubSpot` defaults to `false`** — `qualify_lead` is a dry run unless you pass `writeToHubSpot: true`, which then updates the lifecycle stage + creates a qualification note. Writing is admin-scoped (Tim / Victor).

`powerLevelOverride` (`atl` | `btl` | `unknown`) — override the title-based ATL/BTL classifier when you know the contact's real authority. Sticky on the contact: later classifier runs won't downgrade it.

### Contact Enrichment

**Find phone numbers and emails for prospects.**

> "Find contact info for John Smith at Stanford"
> "Enrich contact: Sarah Johnson at Microsoft"
> "Look up email for this person"

3-tier lookup: cached data (instant) → HubSpot DB (instant) → Clay API (30-90s for new contacts). Provide LinkedIn URL for best accuracy.

### Company Identification

**Match spoken or misspelled company names.** Great after sales calls when you're not sure about the spelling.

> "Who is be an age photo?" → finds B&H Photo
> "Identify company: samsun" → finds Samsung
> "Match this company: standford univeristy"

Returns best matches from CRM + HubSpot with confidence scores.

### Device Analytics (Pearl Fleet)

**Pearl device registrations, usage, and fleet analysis.** Data synced daily from production.

> "How many Pearl devices does MIT have?"
> "Find all devices registered by john@mit.edu"
> "Devices registered in Germany with high idle rate"
> "Show idle devices over 90 days for education vertical"
> "Universities with most device registrations"
> "Registration trends by country last 12 months"
> "Devices active per day — last 30 days"
> "Most active Pearl devices by usage"

**Cross-data (devices + revenue):**

> "Customers with registered devices but no orders in 2024"
> "Correlation between device count and order value"
> "Which accounts have devices but no open deal?"

### HubSpot CRM

**Contacts, companies, deals — search and lookup.**

> "Search HubSpot for contacts at stanford.edu"
> "Find deals with 'Nexus' in the name"
> "Show open deals for company ID 12345"
> "HubSpot company details for domain mit.edu"
> "What's the pipeline summary?"
> "Stalled deals over 30 days"

### Competitive & Market Intel (Marketing Tools)

**Semrush SEO:**

> "Semrush domain overview for vaddio.com"
> "Compare organic keywords: epiphan.com vs crestron.com"
> "What questions do people ask about lecture capture?"
> "Who are epiphan.com's organic search competitors?"
> "Backlinks to epiphan.com — top referring domains"
> "Keyword difficulty for 'lecture capture software'"

**Google Analytics:**

> "Top landing pages this month by sessions"
> "Conversion rate by traffic source last 30 days"
> "Compare organic vs paid traffic trends"

**Google Ads:**

> "Campaign performance last 30 days"
> "Ad creatives for the Pearl campaign"
> "Which ads have the best conversion rate?"

### Product Knowledge

**Ask about Epiphan products — pricing, specs, features, comparisons, troubleshooting.**

> "What's the price of Pearl Mini?"
> "How much does Epiphan Edge cost for 10 devices?"
> "Does Pearl-2 support 4K? Is there an extra cost?"
> "How do I set up Pearl Mini with Panopto?"
> "What's the difference between Pearl Nexus and Pearl Mini?"
> "Which encoder is best for NDI workflows?"

Uses structured product catalog (instant) + RAG from tech support docs for deep technical questions. Live CRM prices for pricing queries.

### Clari Call Search (by Name)

**Find calls by company name, contact name, or topic** — not just by email.

> "How did the Tufts University call go with Jesse Anderson?"
> "Find calls about Old Dominion"
> "What was discussed on the Stanford call last week?"
> "Summarize Lex Evans' calls this month"

Searches the `clari_calls` table in PostgreSQL (7K+ calls with AI summaries, action items, competitor mentions).

### Stripe Cloud Usage

**Epiphan Cloud (Connect/Unify) usage tracking and renewal alerts.**

> "Which customers are approaching their usage contract limits?"
> "Show Stripe usage for PLI"
> "Cloud usage growth signals — who's increasing?"
> "Churn risk: customers with declining usage"

### Curated Analytics Datasets (Weekly Tracker / Repeating Reports)

**Parameterized analytics with deterministic SQL** — built for recurring reports (Cowork weekly sales tracker, BDR digests). Bypass `ask_agent` when you need consistent numbers.

5 datasets, common filters + group_by:

| Dataset | What | Example |
|---------|------|---------|
| `revenue` | CRM orders, USD-converted, `order_type_id < 30` | "Booked revenue MTD/QTD/YTD" |
| `deals_closed` | HubSpot won/lost in date range | "Won deals last week, by outcome" |
| `pipeline_open` | HubSpot active pipeline (excludes closed) | "Open pipeline by AE × stage" |
| `contacts_created` | New HubSpot contacts with lifecycle/source | "New leads by lifecycle this week" |
| `rep_activity` | BDR/AE engagements (emails, calls, tasks, meetings, notes) | "Tim + Ron activity last 7 days" |

> "Use query_dataset: revenue from 2025-11-01 to 2026-04-29 by month"
> "Open pipeline matrix — AE × stage for default sales pipeline"
> "Won/lost deals last week, split by outcome"
> "New contacts last week broken down by lifecycle and source"
> "BDR activity for owner_ids 87486452, 423155215 last 7 days" (illustrative — see the canonical owner-id roster in `nooks-autopilot`/CLAUDE.md rather than hardcoding ids)

`group_by` supports cross-product matrix (e.g. `["owner","stage"]`), period grain (`period_day` / `period_week` / `period_month` / `period_quarter` / `period_year`), and dimensional breakdown (`owner` / `stage` / `outcome` / `country` / `lifecycle` / `source` / `pipeline`). `format=csv` returns an embedded CSV file (Claude Desktop attaches it). Custom HubSpot lifecycle stage IDs are normalized to MQL/SAL/SQL/Customer/Junk/Declined/Nurture labels.

### Raw SQL Export

**Escape hatch when curated datasets aren't enough.** `export_query_csv` runs a read-only SQL SELECT and returns the result as a CSV file (embedded resource).

> "Export this query as CSV: SELECT ... FROM crm_orders WHERE ..."

Same SQL safety as `execute_sql` (SELECT/WITH only, no writes). Hard cap 50 000 rows.

### Data Visualization

**Generate Economist-style charts from any data.**

> "Create a bar chart of top 10 customers by revenue"
> "Line chart: monthly revenue trend 2023-2025"
> "Pie chart of revenue by region"

Always provide the data (JSON/table) alongside the request.

## All Available Tools

| Tool | What it does |
|------|-------------|
| `ask_agent` | Ask any CRM/analytics question in natural language |
| `sales_brief` | Complete customer briefing in one call |
| `ae_handoff` | BDR→AE handoff package with HubSpot note |
| `qualify_lead` | Lead qualification: junk detection, ICP scoring, email draft |
| `identify_company` | Fuzzy match company names across CRM + HubSpot |
| `enrich_contact` | Find phone + email via Clay |
| `activity_get_timeline` | Engagement history (calls, emails, notes, meetings) |
| `clari_search_calls` | Search recorded sales calls |
| `clari_get_call` | Full call details + optional transcript |
| `clari_get_call_summary` | Quick call summary + action items |
| `hubspot_search_companies` | Find HubSpot companies |
| `hubspot_get_company` | Company details by ID |
| `hubspot_search_contacts` | Find HubSpot contacts |
| `hubspot_get_contact` | Contact details by ID |
| `hubspot_find_contacts_by_role` | **Role discovery** — "who is the AV/IT Director at northeastern.edu". Keyed on email domain (ignores dirty company names). Params: `domain`, `titles[]` (optional; defaults to higher-ed AV/IT preset), `limit`. Unions HubSpot + Clay-enriched contacts, decision-makers first. Read-only. Use this for list-building instead of enrich_contact (which needs a known name) |
| `hubspot_search_deals` | Find HubSpot deals |
| `hubspot_get_deal` | Deal details by ID |
| `crm_get_customer` | Legacy CRM customer by ID |
| `crm_search_customers` | Search legacy CRM customers |
| `crm_get_order` | Order details (fuzzy search) |
| `crm_get_customer_orders` | Customer order history |
| `analytics_get_device` | Pearl device lookup by serial |
| `analytics_search_by_email` | All devices by registrant email |
| `search_product_catalog` | Product pricing, specs, features, competitors (catalog + CRM prices + RAG) |
| `search_product_knowledge` | Deep tech support RAG (troubleshooting, setup, firmware) |
| `task_brief` | Overdue + upcoming HubSpot tasks per rep (or team) |
| `ae_drift_detect` | Contacts/deals reassigned away from a rep (last N days) |
| `query_dataset` | Curated parameterized analytics: revenue, deals_closed, pipeline_open, contacts_created, rep_activity |
| `weekly_brief` | One-shot weekly sales tracker — bundles 9 `query_dataset` calls. Params: `week_ending`, `ae_names`, `bdr_owner_ids`, `fiscal_year_start`, `target_annual_revenue`, `pipelines`. Defaults: FY2026, Tim+Ron, $19.5M target |
| `export_query_csv` | Raw read-only SQL → CSV file (escape hatch when curated datasets aren't enough) |
| `generate_image` | Data charts and infographics |
| `get_upcoming_meetings` | Calendar check |

### HubSpot Write Tools (admin-scoped: Tim / Victor)

These mutate HubSpot. Restricted to an allowlist — others get a 403. Rate-limited: 1,000 writes / 5 min per user (bulk-friendly), 4 / 5 min per record.

**Recovery when a write 403s or rate-limits:** don't retry the write blind. Fall back to the read-only equivalent (`hubspot_search_*` / `hubspot_get_*`) to keep answering the question, then surface the failure to Tim / Victor (the admin-scoped operators) so they can run or approve the write.

| Tool | What it does |
|------|-------------|
| `hubspot_create_contact` | Create contact. Idempotent — dedupes by email (returns existing on match). Entry stages only (lead/MQL/SQL/Cold Lead/SAL); accepts `associateCompanyId` |
| `hubspot_create_company` | Create company. Dedup is **domain-first**: any existing company on the same registrable domain (eTLD+1 — `www.carleton.ca`, `cunet.carleton.ca` and `carleton.ca` all match) is flagged as the same institution (`needsReview:true`, `matchType:"domain"`), since that's the reliable key for dirty higher-ed names. Falls back to fuzzy company-name match on other domains. Reuse a candidate's `companyId`, or pass `confirmDespiteSimilar:true` to force-create a genuinely distinct org |
| `hubspot_create_deal` | Create deal. No dedup — pass `pipelineId` + `dealstage` (from `hubspot_deal_stages`) |
| `hubspot_update_contact` | Update fields on an **existing** contact (e.g. add a missing phone). Identify by `contactId` **or** `email`. Patches only the fields you pass: `phone`, `mobilephone`, `jobtitle`, `firstName`, `lastName`, `company`, `website`. Owner → use `hubspot_update_contact_owner`; lifecycle → `hubspot_set_lifecycle_stage` |
| `hubspot_update_company` | Update fields on an **existing** company. Identify by `companyId` **or** `domain` (ambiguous domain → returns candidates, pass `companyId`). Patches only passed fields: `name`, `city`, `country`, `state`, `industry`, `phone`, `website` |
| `hubspot_update_contact_owner` | Set contact owner. Validates `ownerId` against `hubspot_owners` |
| `hubspot_set_lifecycle_stage` | Set lifecycle stage. Accepts ID, label, or alias (SAL/MQL/Cold Lead) — resolved + validated |
| `hubspot_create_contact_note` | Create note on a contact (optionally on deal/company). HTML body, script tags stripped |
| `hubspot_create_contact_task` | Create task on a contact. ISO 8601 due date, validated `ownerId`. **`taskType`: `CALL` / `EMAIL` / `TODO`** (default TODO) — pass `CALL` for dial/follow-up-call tasks (Nooks call lists) so they land as real Call tasks. No HubSpot connector needed |
| `hubspot_update_contact_note` | Edit an existing note's body by `noteId`. HTML, script tags stripped + spacing normalized. **Guardrail:** only notes our integration created, or ones newer than ~7 days, can be edited — older human-authored notes are protected (`Forbidden`). HubSpot keeps per-property history as a backstop |
| `hubspot_update_contact_task` | Edit an existing task by `taskId`. Any subset of `subject` / `body` / `dueDate` / `status` / `ownerId` / `taskType` / `priority`; omitted fields unchanged. **`status: COMPLETED`** marks it done. Same age/ownership guardrail as note updates |

### HubSpot Static Lists (admin-scoped)

Push a BDR segment to a HubSpot **static (MANUAL)** list instead of CSV/Sheets import. Created list names are stamped with an **`[AI] `** prefix so humans can spot agent-managed lists in the UI.

| Tool | What it does |
|------|-------------|
| `hubspot_search_lists` | Read. Find lists by `query` (substring) or exact `name` (case-insensitive). Returns `listId` (ILS), `name`, `processingType`, `size`. `objectType`: contacts/companies/deals |
| `hubspot_list_members` | Read. List a list's members + their contact fields (name/email/company/jobtitle/phone) with per-member **gap flags** (blank jobtitle/phone) + summary. `gapsOnly: true` returns just the members needing enrichment. Use with `enrich_contact` to **fill only the gaps** (e.g. what the HubSpot/Breeze agent left partially filled) — saves Clay credits, doesn't re-enrich complete contacts. Works on any list |
| `hubspot_create_list` | Create a MANUAL list. Idempotent — dedupes by name (forced `[AI] ` prefix). Optional `recordIds` seed (max 5,000, auto-chunked ≤500/request). Reuses an existing agent-owned list; on a name clash with a **human-made** list it returns the ID but **refuses to seed** (`LIST_NOT_AGENT_OWNED`) |
| `hubspot_update_list_membership` | Add/remove records (`add`/`remove`, combined max 5,000, auto-chunked into ≤500/request). **Only on lists the agent created itself** — refuses any other list (`LIST_NOT_AGENT_OWNED`) and non-MANUAL lists (`LIST_NOT_MANUAL`). Natively idempotent (already-member / non-member IDs reported as `missing`); a mid-batch failure returns `PARTIAL_FAILURE` with what landed — just re-run |

**Why the ownership lock:** a static-list membership can be a HubSpot *workflow enrollment trigger*. The agent can only mutate lists it created — so it can never inject members into a human-curated list that might fire a campaign. Lists created here are immediately queryable by the official HubSpot connector via `hs_crm_search.ilsListIds`.

**Note:** Stripe Cloud usage queries (renewals/growth/churn) go through `ask_agent` — there's no dedicated MCP tool. Just ask in natural language.

## Namespaces — default to `Epiphan Ai`

Two MCP connections may show up:

- **`Epiphan Ai`** — the full toolset above. **Default to this.**
- **`Epiphan CRM`** — a subset. Missing, among others: `hubspot_get_contact`, `crm_get_customer_orders`, `get_upcoming_meetings`, `weekly_brief`, `hubspot_search_contacts`, and the `collaborator_owner_id` filter on `hubspot_search_deals`.

If a tool seems "missing," you're probably on `Epiphan CRM` — switch to `Epiphan Ai`. (`hubspot_search_contacts` exists — it just isn't exposed on the CRM subset.)

## Creating customer-facing assets → use the `epiphan-brand-assets` skill

Brand lives on a **separate** `Epiphan Brand` MCP server (voice, tokens, personas, product positioning, logos, fonts) and has its own dedicated skill. Before drafting any customer-facing asset (email, one-pager, deck, proposal) — and before any external send — defer to the **`epiphan-brand-assets`** skill, which drives the brand tools (`get_brand_asset_kit`, `check_my_copy`, …) end-to-end. Don't hand-roll brand calls from this CRM guide.

## Good to Know

- **Start with `ask_agent`** — it handles most questions including calls, products, revenue. Use specific tools only for direct lookups.
- **Call search works by name** — "how did the Tufts call go?" finds it via company/contact name (not just email).
- **Product questions** — `ask_agent` uses product catalog + RAG. For pricing it pulls live CRM prices.
- **Fuzzy matching works** — don't worry about exact spelling for company names.
- **`qualify_lead` is a dry run by default** — pass `writeToHubSpot: true` to update lifecycle + create the note (admin-scoped).
- **`ae_handoff` with `createNote: true`** — visible to the entire sales team.
- **HubSpot IDs are strings**, CRM IDs are numbers.
- **First `enrich_contact` call** for a new person takes 30-90s (Clay API). Subsequent calls are instant.
- **Clari `clari_get_call`** — skip `includeTranscript` for faster responses.
- **Be specific about time periods** — "2024", "last 6 months", "Q3 2025".
- **Specify metrics** — "revenue", "order count", "average order value".
- **Specify grouping** — "by country", "by month", "by product family".

<success_criteria>
- [ ] The question was routed to the right tool (or `ask_agent`) on the first try, using the tool table + `resources/` guides
- [ ] `Epiphan Ai` namespace used (not the `Epiphan CRM` subset) when a tool seemed "missing"
- [ ] Tool defaults and caveats respected: `qualify_lead` dry-run unless `writeToHubSpot:true`, `ae_drift_detect` max 30 days, HubSpot IDs as strings, write tools admin-scoped (Tim/Victor), `[AI]` list ownership lock
- [ ] Repeating reports used `query_dataset` / `weekly_brief` (deterministic SQL), not ad-hoc `ask_agent`
- [ ] Customer-facing asset requests deferred to the `epiphan-brand-assets` skill, not hand-rolled from this guide
</success_criteria>
