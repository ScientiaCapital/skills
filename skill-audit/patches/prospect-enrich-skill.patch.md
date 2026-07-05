# Patch: prospect-enrich-skill

**Score:** trigger=4 tool_integration=3 output_contract=4 failure_handling=3 maintainability=3 (sum=17/25)

**Highest-leverage single change (M effort):** Gate Stage 3 classification and Stage 1 dedupe through qualify_lead instead of the in-skill keyword list
**Expected impact:** Eliminates ATL/BTL drift across the 6-skill family and stops re-spending credits on already-enriched contacts

## Description

**Before:**
> Mon-Fri 6:00 AM — Daily batch enrichment of phoneless contacts using Apollo + Clay. DEMO REQUEST first, then ATL-first priority. Golden Rules + ATL/BTL Classification Gate. Feeds into phone-waterfall and prospect-refresh.

*(trigger_quality > 3 — no description rewrite proposed)*

## Findings & fixes

### [HIGH] tool_integration
- **Evidence** (line 127-141): "elif title in NEVER_ENRICH:
  tier = "NEVER"  # Hard skip
...
elif title in ATL:"
- **Issue:** ATL/BTL classification is hand-rolled in-skill against CLAUDE.md keyword lists rather than gated through qualify_lead, the named dedupe/ATL-BTL source of truth. Every sibling re-implements the same title matching, guaranteeing drift.
- **Fix:** Route each contact through qualify_lead for ATL/BTL tier + dedupe verdict; keep the local keyword list only as a documented fallback.

### [MED] tool_integration
- **Evidence** (line 149): "**MCP Tool:** `apollo_people_bulk_match` (or `apollo:enrich-lead` skill)"
- **Issue:** No dedupe against prior enrichment before spending Apollo/Clay credits — Stage 1 only filters phone=null, so daily runs re-spend credits on the same misses.
- **Fix:** Add a dedupe gate (qualify_lead or enriched_at check) before Stage 4 to skip recently-enriched contacts.

### [MED] failure_handling
- **Evidence** (line 271): "Use status "partial" if some stages failed but results were produced. Use "error" only if no output was generated."
- **Issue:** Sidecar captures terminal status but there is no retry/degrade ladder for Apollo/Clay failure and no run log to ~/.claude/skill-runs/. Clay credit exhaustion mid-run is undefined.
- **Fix:** Add an 'Apollo fails -> Clay; Clay fails -> Apollo-only partial + alert' ladder plus a per-run append to ~/.claude/skill-runs/prospect-enrich.jsonl.

### [LOW] output_contract
- **Evidence** (line 214): "**Output:** HTML file saved to workspace as `bdr-v3-prospect-enrich-YYYY-MM-DD.html`"
- **Issue:** Workspace HTML with no delivery mechanism, so a 6 AM scheduled run produces an artifact nobody is notified about.
- **Fix:** Name a delivery step (Slack DM link or morning-brief handoff).

## Missing tool references

- qualify_lead
- search_product_catalog / search_product_knowledge (if any customer-facing string generated)

## Self-healing gap (see specs/self-healing-template.md)

Terminal-status sidecar only; lacks retry->degrade->alert ladder for Apollo/Clay credit exhaustion and a durable run log at ~/.claude/skill-runs/prospect-enrich.jsonl. Single-stage failure has no recovery path.

## Overlap candidates (flag only — no removal)

- phone-verification-waterfall
- prospect-refresh
- callable-lead-count-skill
