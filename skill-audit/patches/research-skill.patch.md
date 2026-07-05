# Patch: research-skill

**Score:** trigger=3 tool_integration=2 output_contract=3 failure_handling=2 maintainability=3 (sum=13/25)

**Highest-leverage single change (M effort):** Insert an Epiphan-native tool order into Part 1 Market Research (identify_company -> sales_brief -> activity_get_timeline -> enrich_contact) ahead of generic web sources
**Expected impact:** Account research uses first-party CRM/device/Clari data instead of guesswork, and stops duplicating qualify_lead

## Description

**Before:**
> Market intelligence, competitive analysis, technical evaluations, and technology decisions. Use when researching companies, analyzing competitors, evaluating frameworks, or making tech stack decisions.

**After (proposed):**
> Structured research reports for GTM and tech decisions: company/competitor profiles, tech-stack discovery, framework/LLM/API evaluations, decision matrices with confidence scores. Use when: research a company before a call, competitive analysis, evaluate a framework or LLM, tech-stack decision, build-vs-buy. For Epiphan account prep prefer sales_brief/identify_company; for lead ICP scoring use qualify_lead.

## Findings & fixes

### [HIGH] tool_integration
- **Evidence** (line 366): "- **Data sources:** LinkedIn, Glassdoor, Indeed, G2, Capterra, Google"
- **Issue:** Company/competitive research points only at generic external sources; never references Epiphan-native sales_brief, identify_company, enrich_contact, hubspot_search_companies, or search_product_catalog — direct 'Epiphan-native preferred' violation for account/competitor prep.
- **Fix:** Add a Market Research tool order: identify_company -> sales_brief -> activity_get_timeline -> enrich_contact, with Semrush via Epiphan AI marketing tools before generic web.

### [MED] tool_integration
- **Evidence** (line 115-116): "Step 5: Synthesize
|__ Generate company profile, score against ICP"
- **Issue:** 'Score against ICP' with no call to qualify_lead, the house ICP/power_level source of truth; scoring re-implemented manually.
- **Fix:** Route the ICP/decision-maker step through qualify_lead + hubspot_find_contacts_by_role.

### [MED] maintainability
- **Evidence** (line 287): "|__ /Users/tmkipper/Desktop/tk_projects/mcp-server-cookbook/"
- **Issue:** Hardcoded absolute path uses wrong username 'tmkipper' (Tim's home is /Users/tmk) — a dead path that silently fails.
- **Fix:** Fix to /Users/tmk/... or make it relative/env-based.

### [LOW] maintainability
- **Evidence** (line 163): "machine: m1_mac"
- **Issue:** Stack constraints assert M1 Mac; Tim's machine is now M4 24GB — drifting hardcoded environment fact.
- **Fix:** Remove specific hardware or point to a single environment reference.

### [LOW] output_contract
- **Evidence** (line 308-310): "research_report:
  title: ""
  type: ""  # market, technical, hybrid"
- **Issue:** Defines a YAML report structure but no delivery target (doc, artifact, HubSpot note).
- **Fix:** Specify where the report is written / handed off.

## Missing tool references

- sales_brief
- identify_company
- enrich_contact
- hubspot_search_companies
- qualify_lead
- search_product_catalog

## Self-healing gap (see specs/self-healing-template.md)

No failure definition, no retry->degrade->alert ladder, and no run log; the confidence field substitutes for failure handling but there is no rule for missing sources beyond labeling confidence 'low'.

## Overlap candidates (flag only — no removal)

- gtm-pricing-skill
- prospect-research-compiler
- prospect-research-to-cadence-skill
- competitor-content-analyzer
