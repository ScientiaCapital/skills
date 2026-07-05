# Patch: prospect-research-to-cadence-skill

**Score:** trigger=5 tool_integration=3 output_contract=4 failure_handling=3 maintainability=4 (sum=19/25)

**Highest-leverage single change (M effort):** Consolidate Stage 1b Golden Rules + 1c ATL/BTL + CRM dedupe lookups into a single qualify_lead call and add a check_my_copy brand gate on drafted touches
**Expected impact:** Cuts MCP round-trips, removes classification drift, stops off-brand/unverified copy reaching the approval screen

## Description

**Before:**
> End-to-end prospect research pipeline: Apollo enrichment → personalized email + call scripts → draft review → Apollo sequence load. Eliminates manual research bottleneck. Use when: 'research prospect', 'prospect [company]', 'build cadence for', 'outreach for [company]', 'research-to-cadence', 'enrich and sequence', 'new prospect batch'.

*(trigger_quality > 3 — no description rewrite proposed)*

## Findings & fixes

### [HIGH] tool_integration
- **Evidence** (line 58-60): "| `crm_search_customers` | Epiphan CRM customer match |...| `analytics_search_by_email` | Device registration lookup |"
- **Issue:** Wires crm_search_customers + hubspot_search + analytics_search_by_email + an in-line ATL/BTL classifier (110-118) to reconstruct what qualify_lead returns in one call. qualify_lead is the named source of truth and is not called.
- **Fix:** Call qualify_lead as the single Golden-Rules + ATL/BTL + dedupe gate; keep manual CRM lookups only for enrichment fields it does not return.

### [HIGH] tool_integration
- **Evidence** (line 144-154): "Load `reference/email-templates.md` for templates. Customize with: ... Lead with THEIR problem, not Epiphan features"
- **Issue:** Generates 3-touch email sequences + MEDDIC call scripts (customer-facing) with no search_product_knowledge spec check and no get_writing_style/check_my_copy brand gate.
- **Fix:** Add a spec-verification read and a check_my_copy pass on drafted touches before Stage 2 presentation.

### [LOW] tool_integration
- **Evidence** (line 62): "| Web search | Recent news | Funding, expansion, leadership changes |"
- **Issue:** Generic web search where an Epiphan-native intel path may exist (house rule 4).
- **Fix:** Prefer Epiphan CRM/intel tools for covered signals; web search only for gaps.

### [LOW] output_contract
- **Evidence** (line 205-206): "Present draft to Tim using AskUserQuestion tool ... Options: "Approve & Load", "Edit first", "Skip this prospect""
- **Issue:** Strong draft-first + explicit approval gate before Apollo load — good. Minor: approved draft is not persisted for audit.
- **Fix:** Persist the approved deliverable block to a run log.

## Missing tool references

- qualify_lead
- search_product_knowledge
- search_product_catalog
- get_writing_style
- check_my_copy

## Self-healing gap (see specs/self-healing-template.md)

Sidecar status buckets + an approval halt exist, but no retry->degrade ladder for Apollo people_match/enrich failures and no run log at ~/.claude/skill-runs/prospect-research-to-cadence.jsonl. Phone-miss path is skip/flag (line 123) — reasonable but not generalized.

## Overlap candidates (flag only — no removal)

- prospect-refresh
- sequence-load
- cold-email-sequence-generator-skill
- meddic-call-prep-auto-skill
- sales-revenue-skill
