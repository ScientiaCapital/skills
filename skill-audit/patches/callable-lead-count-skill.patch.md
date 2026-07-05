# Patch: callable-lead-count-skill

**Score:** trigger=3 tool_integration=3 output_contract=4 failure_handling=4 maintainability=2 (sum=16/25)

**Highest-leverage single change (M effort):** Swap inline ATL/BTL keyword logic + Golden Rules for a qualify_lead gate and reference CLAUDE.md for the taxonomy
**Expected impact:** Eliminates the duplicated classifier that will drift from CLAUDE.md and adds real dedupe so the inventory count is accurate

## Description

**Before:**
> Daily callable lead inventory with ATL/BTL breakdown. Health check for 50+ daily dials.

**After (proposed):**
> Daily callable-lead inventory health check with ATL/BTL/GRAY/NEVER breakdown and ATL Runway metric for Tim's 50+ dials/day target. Alerts when total callable < 50 or ATL < 15. Use when: 'show callable leads', 'lead inventory check', 'how many callable leads', 'ATL runway', 'callable count', or the 7:25 AM scheduled run feeding morning-brief.

## Findings & fixes

### [HIGH] tool_integration
- **Evidence** (line 106-160): "## Stage 3: Classify by ATL/BTL Tier ... **MCP Tool:** N/A (logic-based classification using jobtitle) ... **Classification Algorithm:** ```FOR each contact IN filtered_list: title = contact.jobtitle.lower() IF title matches any NEVER_ATL keyword:"
- **Issue:** ATL/BTL classification and Golden-Rules filtering are done inline with hardcoded keyword lists instead of gating through qualify_lead (the dedupe/ATL-BTL source of truth); no dedupe step at all, so multi-record contacts double-count inventory.
- **Fix:** Replace Stage 2/3 keyword logic with a qualify_lead pass that returns tier + dedupe; keep the local lists only as a documented fallback.

### [HIGH] maintainability
- **Evidence** (line 112-160): "**NEVER ATL (Automatic Exclusions):** - Warehouse Manager, Network Manager, Systems Administrator - AV Technician, Graphic Design Instructor ... (lines 134-140) — duplicates the identical list in CLAUDE.md § ATL/BTL Classification."
- **Issue:** The full ATL/GRAY/BTL/NEVER keyword taxonomy is copy-pasted from CLAUDE.md; two sources will drift when the classification is updated.
- **Fix:** Reference CLAUDE.md § ATL/BTL Classification (or qualify_lead) as the single source instead of re-listing all keywords inline.

### [MED] trigger_quality
- **Evidence** (line 3): "description: "Daily callable lead inventory with ATL/BTL breakdown. Health check for 50+ daily dials.""
- **Issue:** Description is a summary, not 'pushy' — it enumerates no trigger phrases (the manual phrases 'Show callable leads'/'Lead inventory check' live only in the body at line 15), so activation on natural phrasing is weak.
- **Fix:** Move the trigger phrases into the description; see rewritten_description.

### [LOW] output_contract
- **Evidence** (line 220-294): "## Stage 6: Output Summary Report **Format:** Markdown summary + detailed table ... ## Stage 7: Integration with Morning Brief ... Pass ATL/GRAY/BTL breakdown to morning-brief"
- **Issue:** Output is Markdown to chat + a JSON blob for morning-brief, but no delivery mechanism is specified (no Slack DM, no file artifact) despite being a 7:25 AM scheduled run with no human present.
- **Fix:** Define a delivery channel (Slack DM to Tim U0AAJUZH2PK, matching he-dial-queue) for the scheduled run.

## Missing tool references

- qualify_lead

## Self-healing gap (see specs/self-healing-template.md)

Has an outcome sidecar with success|partial|error semantics (lines 320-327) and a suppression gate, but no retry on HubSpot pagination failure, no alert delivery channel for the unattended scheduled run, and no per-run skill-runs/ log.

## Overlap candidates (flag only — no removal)

- he-dial-queue
- sdr-dial-lists
- morning-brief
