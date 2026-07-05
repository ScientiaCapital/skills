# Patch: meeting-intelligence-system-skill

**Score:** trigger=2 tool_integration=1 output_contract=2 failure_handling=2 maintainability=3 (sum=10/25)

**Highest-leverage single change (M effort):** Re-scope the description to internal-only meetings with enumerated triggers and wire create_draft + brand gate for the follow-up email.
**Expected impact:** Removes trigger collisions with the two Epiphan sales-call skills and makes the follow-up email a real, on-brand draft instead of pasted text.

## Description

**Before:**
> Analyze meeting transcripts to extract decisions, action items, blockers, sentiment, and generate follow-up emails. Use when user provides meeting notes, transcripts, or recordings and needs structured summaries or action tracking.

**After (proposed):**
> Structure and summarize INTERNAL meeting transcripts (standups, planning, retros, 1:1s) into decisions, owned action items, blockers, sentiment, and a draft follow-up email. Use when: 'analyze this meeting', 'extract action items', 'meeting minutes', 'summarize this standup/planning/retro', 'follow-up email from these notes'. NOT for sales/prospect calls — route those to call-recording-analyzer (Clari scorecard) or sdr-call-coaching. Wires create_draft for the follow-up email; runs customer-facing copy through the Epiphan brand-voice gate before send.

## Findings & fixes

### [HIGH] trigger_quality
- **Evidence** (line 3): "description: Analyze meeting transcripts to extract decisions, action items, blockers, sentiment, and generate follow-up emails. Use when user provides meeting notes, transcripts, or recordings and needs structured summaries or action tracking."
- **Issue:** Generic, non-'pushy' description — no enumerated trigger phrases, collides directly with call-recording-analyzer ('review transcript', 'analyze call') and sdr-call-coaching. Nothing scopes it to Epiphan, so it will fire on sales-call transcripts the Epiphan-native skills should own.
- **Fix:** See rewritten_description; scope to internal/non-sales meetings and enumerate trigger phrases.

### [HIGH] tool_integration
- **Evidence** (line 79-82): "7. **Generate Follow-Up Communications** - Create meeting minutes/summary - Draft action item tracking email"
- **Issue:** Zero MCP tools referenced anywhere — no Clari for transcripts, no HubSpot, and 'draft email' with no create_draft (generic manual step where the Gmail tool exists). Violates house rule 4 (Epiphan-native preferred) and draft-first; every input/output is manual copy-paste.
- **Fix:** Wire create_draft for the follow-up email and, for sales meetings, defer transcript pulls to clari_get_call.

### [HIGH] output_contract
- **Evidence** (line 122-142): "## Follow-Up Email Draft
Subject: Action Items from [Meeting Title] - [Date]
Hi team,"
- **Issue:** Produces a team/customer-facing email body inline in markdown with no delivery mechanism (no Gmail draft) and no brand-voice gate (house rule 2: get_writing_style/check_my_copy) before emitting the string.
- **Fix:** Emit via create_draft (draft-first); run any external-facing send through the Epiphan brand-voice check first.

### [MED] failure_handling
- **Evidence** (line 176): "Use status "partial" if some stages failed but results were produced. Use "error" only if no output was generated."
- **Issue:** Only a sidecar exists; no definition of a failed run (transcript unparseable, no owners identifiable), no retry/skip/alert behavior, no run log.
- **Fix:** Define partial/failed conditions and a skip/alert path.

## Missing tool references

- create_draft
- clari_get_call
- get_writing_style
- check_my_copy

## Self-healing gap (see specs/self-healing-template.md)

Only an outcome sidecar (169-176); no failure definition, no retry->degrade->alert->halt ladder, no run log to ~/.claude/skill-runs, and no delivery mechanism to fail on since output is terminal markdown.

## Overlap candidates (flag only — no removal)

- call-recording-analyzer
- sdr-call-coaching
- meddic-call-prep-auto
