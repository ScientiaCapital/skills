# Patch: call-recording-analyzer-skill

**Score:** trigger=5 tool_integration=2 output_contract=2 failure_handling=4 maintainability=3 (sum=16/25)

**Highest-leverage single change (M effort):** Add the spec-verification gate before battlecard mapping and wire a concrete delivery (Gmail draft/saved HTML) + downstream feed write.
**Expected impact:** Stops stale-battlecard scoring and turns the scorecard into a durable artifact instead of ephemeral terminal text.

## Description

**Before:**
> Gong/Chorus-style call transcript analysis using Clari data. Scores calls against MEDDIC framework, flags missed discovery questions, surfaces competitor mentions, extracts action items, and identifies coaching moments. Feeds deal-momentum-analyzer and morning-brief with call quality signals. Use when: 'analyze call', 'call review', 'score my call', 'what did I miss', 'call coaching', 'review transcript', 'Clari analysis', 'call scorecard', 'how did my call go', 'review my last call with [company]'.

*(trigger_quality > 3 — no description rewrite proposed)*

## Findings & fixes

### [HIGH] tool_integration
- **Evidence** (line 170-171): "### Competitive Intelligence Extraction
Scan for: Extron, Blackmagic, Crestron, vMix, Matrox, Teradek, Kaltura, Panopto, YuJa, Echo360"
- **Issue:** Competitor mentions 'mapped to battlecard responses' (line 35) with no live spec/competitor verification gate — violates house rule 1. Unlike sdr-call-coaching, scores MEDDIC and emits competitor rebuttals without calling search_product_catalog/knowledge, so it can score a rep 'correct' against a stale battlecard.
- **Fix:** Add the non-negotiable technical-accuracy gate before mapping any competitor mention to a battlecard response.

### [HIGH] output_contract
- **Evidence** (line 173-198): "## Stage 4: Output Format ... CALL SCORECARD: [Company Name]"
- **Issue:** Deps list gmail_create_draft (line 219) but output contract defines only a terminal ASCII scorecard — no delivery wired (no draft/Slack/HTML); 'feed to downstream skills' (202-213) has no concrete write.
- **Fix:** Define the actual delivery (Gmail draft or saved HTML) and specify how the deal-momentum-analyzer/morning-brief feed is written.

### [MED] tool_integration
- **Evidence** (line 66): "| clari_get_call_summary | AI summary, key moments, action items, sentiment |"
- **Issue:** Uses clari_get_call_summary, but sibling sdr-call-coaching (same Clari surface, verified 2026-06-17) uses clari_get_call with includeTranscript=true — possible stale/nonexistent tool name and inconsistent Clari access pattern.
- **Fix:** Reconcile against the live Clari tool set; standardize on clari_search_calls + clari_get_call.

### [MED] tool_integration
- **Evidence** (line 80-83): "**Pre-Flight Golden Rules Check:** - If contact.lifecyclestage = 'customer' -> Skip. - If hubspot_owner_id IN ('82625923', '423155215', '190030668') AND Tim is NOT collaborator -> Skip."
- **Issue:** Suppression/ownership check via raw HubSpot reads, not gated through qualify_lead (house rule 3).
- **Fix:** Route the pre-flight check through qualify_lead where available.

### [LOW] maintainability
- **Evidence** (line 82): "- If hubspot_owner_id IN ('82625923', '423155215', '190030668')"
- **Issue:** AE owner IDs hardcoded inline (drift risk vs CLAUDE.md canonical list).
- **Fix:** Reference CLAUDE.md Golden Rules rather than re-listing the IDs.

## Missing tool references

- search_product_catalog
- search_product_knowledge
- qualify_lead
- create_draft

## Self-healing gap (see specs/self-healing-template.md)

Has outcome sidecar with partial/error (229-236) but no retry->degrade->alert->halt ladder for Clari misses, no run log to ~/.claude/skill-runs, and no defined behavior when the downstream feed (deal-momentum-analyzer) target is unavailable.

## Overlap candidates (flag only — no removal)

- sdr-call-coaching
- meeting-intelligence-system-skill
- meddic-call-prep-auto
- deal-momentum-analyzer-skill
