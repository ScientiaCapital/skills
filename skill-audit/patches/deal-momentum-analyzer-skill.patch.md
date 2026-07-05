# Patch: deal-momentum-analyzer-skill

**Score:** trigger=4 tool_integration=3 output_contract=4 failure_handling=4 maintainability=3 (sum=18/25)

**Highest-leverage single change (M effort):** Route contact ATL/BTL through qualify_lead instead of inline keyword tables, and reconcile the tool names between workflow and Dependencies.
**Expected impact:** Single source of truth for ATL/EB scoring (Signal 3) and eliminates wrong-tool-call risk on every run.

## Description

**Before:**
> Deal health scoring + next-best-action for every open deal. Pulls HubSpot deals, CRM activity history, and engagement data to flag stalled deals, predict close probability, and recommend specific recovery actions. Runs daily at 7am CST or on-demand. Use when: 'deal health', 'pipeline review', 'stalled deals', 'deal momentum', 'which deals need attention', 'morning brief', 'SOD'.

*(trigger_quality > 3 — no description rewrite proposed)*

## Findings & fixes

### [HIGH] tool_integration
- **Evidence** (line 51): "Use `search_crm_objects` (HubSpot MCP) with **two OR-ed filter groups**"
- **Issue:** Workflow calls `search_crm_objects`, but the Dependencies block (line 320) lists `hubspot_search_deals`/`hubspot_search_companies`/`hubspot_search_contacts` — tool names are inconsistent between body and dependency contract, risking a wrong/hallucinated tool call at runtime.
- **Fix:** Pick one canonical tool name set (the actual Epiphan HubSpot MCP tool) and use it in both the workflow and Dependencies.

### [HIGH] tool_integration
- **Evidence** (line 163-168): "For each deal's associated contacts, classify by title before scoring: - **ATL:** Chief, VP, Director..."
- **Issue:** ATL/BTL classification is done by inline title-keyword matching from memory rather than routing through qualify_lead, the stated ATL/BTL and dedupe source of truth. Two skills can diverge on the same contact.
- **Fix:** Call qualify_lead for each associated contact and consume its ATL/BTL/EB verdict; keep the keyword table only as a documented fallback.

### [MED] trigger_quality
- **Evidence** (line 22): ""pipeline review" / "stalled deals""
- **Issue:** Trigger phrases 'stalled deals' and 'pipeline review' collide with dead-deal-recovery and pipeline-health-analyzer, which claim the same phrases — activation ambiguity across three sibling skills.
- **Fix:** Reserve 'deal momentum'/'which deals need attention' here; hand 'stalled deals'/'clean pipeline' to dead-deal-recovery and 'pipeline health'/'forecast' to pipeline-health-analyzer. Add a disambiguation note in each description.

### [MED] tool_integration
- **Evidence** (line 228): "| No activity > 14 days | Send re-engagement email | `gmail_create_draft` |"
- **Issue:** Re-engagement email drafts are customer-facing output but there is no Epiphan Brand voice gate (get_writing_style/check_my_copy) before draft creation.
- **Fix:** Add a brand-gate step: run check_my_copy on any generated email body before gmail_create_draft.

### [MED] maintainability
- **Evidence** (line 58,85): "hubspot_owner_id` EQ `87486452` ... owner IDs 82625923 Lex Evans, 423155215 Ron Epstein, 190030668 Phillip Sandler"
- **Issue:** Owner IDs are hardcoded inline in multiple places (Stage 1a, 1a-bis) and duplicate values already defined in CLAUDE.md Golden Rules — drift risk when a rep changes.
- **Fix:** Declare owner IDs once at top of the skill (or reference CLAUDE.md) and reuse.

### [LOW] maintainability
- **Evidence** (line 119,124): "### 1c. Pull Activity History ... ### 1c. Pull Contact Engagement"
- **Issue:** Two consecutive sub-stages are both labelled '1c' — copy/paste numbering bug.
- **Fix:** Renumber to 1c and 1d.

## Missing tool references

- qualify_lead
- get_writing_style
- check_my_copy

## Self-healing gap (see specs/self-healing-template.md)

Has an outcome sidecar with success/partial/error and a Clari->HubSpot degrade path (line 117), but no explicit retry->degrade->alert->halt ladder for HubSpot/Gmail failures and no run log to ~/.claude/skill-runs/deal-momentum-analyzer.jsonl — only the analytics sidecar.

## Overlap candidates (flag only — no removal)

- pipeline-health-analyzer-skill
- dead-deal-recovery
- close-plan-generator
