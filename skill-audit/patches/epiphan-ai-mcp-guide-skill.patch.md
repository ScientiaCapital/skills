# Patch: epiphan-ai-mcp-guide-skill

**Score:** trigger=3 tool_integration=5 output_contract=4 failure_handling=3 maintainability=4 (sum=19/25)

**Highest-leverage single change (S effort):** Add an enumerated 'Use when:' trigger list to the frontmatter description
**Expected impact:** Raises activation recall so Claude reaches for the guide on tool-selection questions instead of guessing a namespace

## Description

**Before:**
> Reference for Epiphan AI MCP tools — CRM, sales intel, device analytics, lead qualification, marketing (Semrush/GA4/GAds).

**After (proposed):**
> Epiphan AI MCP tool picker: which tool answers which question across HubSpot CRM (read + admin writes + static lists), legacy CRM orders, Pearl device analytics, Clari calls, qualify_lead, enrich_contact, curated query_dataset/weekly_brief reports, and Semrush/GA4/GAds marketing intel. Use when: which Epiphan tool, look up a customer, sales brief, qualify a lead, find the AV/IT director, pull pipeline, weekly sales tracker, wrong namespace / tool missing.

## Findings & fixes

### [MED] trigger_quality
- **Evidence** (line 3): "description: Reference for Epiphan AI MCP tools — CRM, sales intel, device analytics, lead qualification, marketing (Semrush/GA4/GAds)."
- **Issue:** Reference-style description with no 'Use when:' phrases; a discoverability skill that is itself hard to trigger. Lower recall than sibling skills.
- **Fix:** Add enumerated triggers so it surfaces on 'which tool for X', 'how do I look up a customer', 'find the AV director'.

### [MED] failure_handling
- **Evidence** (line 354): "If a tool seems "missing," you're probably on `Epiphan CRM` — switch to `Epiphan Ai`."
- **Issue:** Namespace-fallback guidance exists, but as a reference guide there is no defined behavior when a tool returns 403 (non-allowlisted write) or a rate-limit — caveats are listed but not turned into a recovery step.
- **Fix:** Add a 'when a write 403s / rate-limits' recovery note (fall back to read + surface to Tim/Victor).

### [LOW] tool_integration
- **Evidence** (line 356-358): "Before drafting any customer-facing asset ... defer to the **`epiphan-brand-assets`** skill, which drives the brand tools (`get_brand_asset_kit`, `check_my_copy`, ...)"
- **Issue:** Correctly enforces the brand gate and product-spec sourcing (search_product_catalog) — exemplary; noting as strength.
- **Fix:** None.

### [LOW] tool_integration
- **Evidence** (line 366): "- **`qualify_lead` is a dry run by default** — pass `writeToHubSpot: true` to update lifecycle + create the note (admin-scoped)."
- **Issue:** Documents qualify_lead dry-run default and admin-scope caveats accurately — reinforces house rule 3.
- **Fix:** None.

### [LOW] maintainability
- **Evidence** (line 255): "> "BDR activity for owner_ids 87486452, 423155215 last 7 days""
- **Issue:** Owner ids appear inline in examples; low drift risk since illustrative, but no single declared roster.
- **Fix:** Reference the canonical owner-id roster (CLAUDE.md / nooks-autopilot config) instead of loose inline ids.

## Self-healing gap (see specs/self-healing-template.md)

As a reference skill it has no run loop, but it also defines no recovery ladder for the failure modes it documents (403 non-allowlist write, per-record rate limit, wrong namespace) beyond prose caveats; no run log applies.

## Overlap candidates (flag only — no removal)

- hubspot-revops-skill
- crm-integration-skill
