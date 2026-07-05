# Patch: dead-deal-recovery-skill

**Score:** trigger=4 tool_integration=3 output_contract=4 failure_handling=4 maintainability=4 (sum=19/25)

**Highest-leverage single change (S effort):** Add a brand-voice gate (check_my_copy) before the three recovery-email gmail_create_draft calls and route Signal 5 ATL/BTL through qualify_lead.
**Expected impact:** Brings outbound copy on-brand and unifies stakeholder scoring with sibling skills at low effort.

## Description

**Before:**
> Identify stalled and dying deals, run structured disqualification or recovery workflows, and clean pipeline of dead weight. Finds deals stuck 60+ days, with no champion, no activity, or overdue close dates and prescribes either a final re-engagement campaign or formal disqualification. Keeps pipeline honest and frees mental bandwidth. Use when: 'dead deals', 'stalled deals', 'clean pipeline', 'pipeline cleanup', 'disqualify deals', 'deal graveyard', 'zombie deals', 'which deals should I kill', 'pipeline hygiene', 'deal recovery', 'win back', 'lost deal review', 'close out stale deals'.

*(trigger_quality > 3 — no description rewrite proposed)*

## Findings & fixes

### [HIGH] tool_integration
- **Evidence** (line 146-156): "**Email 3 — Break-Up (Day 10):**
```
Subject: Should I close your file?"
- **Issue:** Three customer-facing recovery emails are drafted (line 158 gmail_create_draft) with no Epiphan Brand voice gate (get_writing_style/check_my_copy) before draft creation.
- **Fix:** Insert a check_my_copy pass on each of the 3 touch bodies before gmail_create_draft.

### [MED] tool_integration
- **Evidence** (line 117-119): "| 3+ contacts including ATL (economic buyer) | 20 | ... | 2+ contacts but all BTL | 8 |"
- **Issue:** Signal 5 stakeholder breadth relies on ATL/BTL judged inline without calling qualify_lead, the dedupe/ATL-BTL source of truth — can diverge from deal-momentum-analyzer scoring of the same deal.
- **Fix:** Pull ATL/BTL from qualify_lead per contact.

### [MED] tool_integration
- **Evidence** (line 225): "- **Apollo MCP:** enrich_contact (find new contacts for single-threaded deals)"
- **Issue:** Names `enrich_contact` for finding new stakeholders where the Epiphan-native qualify_lead / CRM contact search plus the actual Apollo tool (apollo_mixed_people_api_search) would be preferred; the tool name also does not match Apollo's real tool set.
- **Fix:** Use apollo_mixed_people_api_search and gate discovered contacts through qualify_lead before drafting.

### [LOW] output_contract
- **Evidence** (line 188): "-> Gmail draft created: Yes/No"
- **Issue:** Output reports whether a Gmail draft was created but HubSpot 'Closed Lost' updates in Stage 4 are described as actions without a confirmation/delivery line in the report contract.
- **Fix:** Add a per-deal 'HubSpot updated: Yes/No + lost reason' field to the Stage 5 report.

## Missing tool references

- qualify_lead
- get_writing_style
- check_my_copy
- apollo_mixed_people_api_search

## Self-healing gap (see specs/self-healing-template.md)

Strong on process guardrails (disqualification checklist lines 161-168, outcome sidecar lines 235-241) but has no retry->degrade->alert->halt ladder for tool failures and no run log to ~/.claude/skill-runs/dead-deal-recovery.jsonl beyond the analytics sidecar.

## Overlap candidates (flag only — no removal)

- deal-momentum-analyzer
- pipeline-health-analyzer-skill
