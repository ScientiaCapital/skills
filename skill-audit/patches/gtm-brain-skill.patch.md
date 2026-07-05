# Patch: gtm-brain-skill

**Score:** trigger=5 tool_integration=4 output_contract=4 failure_handling=3 maintainability=3 (sum=19/25)

**Highest-leverage single change (S effort):** Route contact tier/vertical through qualify_lead (power_level) instead of re-deriving ATL/BTL from CLAUDE.md keywords
**Expected impact:** Graph tiers stay consistent with the rest of the BDR stack; eliminates a second drifting classifier

## Description

**Before:**
> Relationship intelligence graph for GTM work. Reads and writes Contact/Account/Deal/Outcome nodes in Neo4j Aura. Syncs contacts/accounts from HubSpot MCP and imports call outcomes from Nooks MCP automatically. Surfaces what messaging, sequences, and personas worked across verticals. Use when: relationship graph, gtm brain, log outcome, what worked with, account map, sync from hubspot, import nooks calls, contact history, sequence performance.

*(trigger_quality > 3 — no description rewrite proposed)*

## Findings & fixes

### [MED] tool_integration
- **Evidence** (line 245-251): "### Step 2 — Classify ATL/BTL from title
Apply the ATL/BTL Classification from CLAUDE.md:
- Match title against Universal ATL Keywords -> `ATL`"
- **Issue:** ATL/BTL tier is re-derived by keyword matching from CLAUDE.md instead of calling qualify_lead, whose power_level (atl/btl/unknown) is the house source of truth. Two classifiers will drift.
- **Fix:** In Stage 6 Step 2, call qualify_lead and read power_level; fall back to keyword match only when power_level=unknown.

### [MED] failure_handling
- **Evidence** (line 332): "Process all calls in the batch. Report: N calls imported, breakdown by result (X positive / Y neutral / Z negative)."
- **Issue:** Stage 7 batch loop has no per-item failure/skip/retry; one missing hubspotContactId or Aura timeout aborts with no run log.
- **Fix:** Add per-call try/skip with a failure tally and a run-log line to ~/.claude/skill-runs/gtm-brain.jsonl.

### [MED] maintainability
- **Evidence** (line 344-345): ""skill": "gtm-brain",
  "version": "1.0.0","
- **Issue:** Sidecar hardcodes version 1.0.0 but frontmatter is version "1.1.0" (line 4) — version drift mislabels outcome analytics.
- **Fix:** Emit the frontmatter version or reference a single VERSION constant.

### [LOW] trigger_quality
- **Evidence** (line 3): "description: "...Use when: relationship graph, gtm brain, log outcome, what worked with, account map, sync from hubspot, import nooks calls, contact history, sequence performance.""
- **Issue:** Strong enumerated trigger list; specific and pushy.
- **Fix:** None.

### [LOW] tool_integration
- **Evidence** (line 254): "Use `mcp__claude_ai_Epiphan_Ai__qualify_lead` or infer from company name/domain:"
- **Issue:** qualify_lead offered only as optional vertical-inference path, not as the authority gate before writing a Contact node.
- **Fix:** Make qualify_lead the default enrichment call for any contact written via Stage 6/7.

### [LOW] maintainability
- **Evidence** (line 300): "Use Tim's Nooks user ID `87486452`."
- **Issue:** Nooks user id and Aura URL hardcoded inline mid-stage.
- **Fix:** Declare owner id + instance host once in config.json and reference it.

## Missing tool references

- qualify_lead (for power_level authority on contact writes)

## Self-healing gap (see specs/self-healing-template.md)

No failure definition for the HubSpot/Nooks sync loops, no retry->degrade->alert ladder beyond the ping-retry note (line 80), and no run log to ~/.claude/skill-runs/gtm-brain.jsonl — only a single end-of-session sidecar written even on partial batch failure.

## Overlap candidates (flag only — no removal)

- nooks-autopilot
- meddic-call-prep-auto-skill
- morning-brief-skill
