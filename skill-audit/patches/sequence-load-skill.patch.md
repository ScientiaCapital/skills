# Patch: sequence-load-skill

**Score:** trigger=3 tool_integration=3 output_contract=4 failure_handling=3 maintainability=3 (sum=16/25)

**Highest-leverage single change (M effort):** Replace HTML-report scraping with a structured handoff from prospect-refresh and gate the final enrollment decision through qualify_lead
**Expected impact:** Removes the silent-break risk between the two scheduled skills and prevents disqualified leads entering live sequences

## Description

**Before:**
> Monday auto-load of weekly prospect refresh results into Apollo outreach sequences.

**After (proposed):**
> Monday 7:15 AM (and on demand) enrollment of prospect-refresh net-new leads into Apollo sequences: qualify_lead final gate + HubSpot/Apollo dedupe + phone validation -> vertical->sequence mapping -> batch add-to-sequence -> HubSpot contact sync -> enrollment report. Use when: 'load prospects into sequences', 'enroll new leads', 'run sequence load'.

## Findings & fixes

### [HIGH] tool_integration
- **Evidence** (line 97-102): "**Skip if:**
- Email domain matches known customer domain (cross-check crm_customers)
... - Title in NEVER ATL list: Warehouse Manager, Network Manager..."
- **Issue:** Re-implements Golden Rules + NEVER ATL as prose at the enrollment stage instead of gating through qualify_lead. This is the last gate before contacts enter live Apollo sequences, so drift here sequences disqualified leads.
- **Fix:** Call qualify_lead for the final go/no-go before enrollment; treat its verdict as authoritative.

### [MED] tool_integration
- **Evidence** (line 37-43): "**Input Source:** prospect-refresh HTML report + Gmail drafts
**Extract from HTML Report:** ..."
- **Issue:** Consumes upstream state by scraping prospect-refresh's HTML report rather than a structured handoff, so any format change silently breaks this skill.
- **Fix:** Have prospect-refresh emit a structured JSON handoff (or shared HubSpot list) that sequence-load reads.

### [MED] maintainability
- **Evidence** (line 131-139): "| Higher Ed | BDR_HigherEd_OutboundX | [search by name] | ... | K-12 | BDR_K12_OutboundX | [search by name] |"
- **Issue:** Sequence-name patterns and an email_account_id literal ('6633baaece5fbd01c791d7ca', line 200) are hardcoded values that drift on rename/mailbox change.
- **Fix:** Resolve sequence IDs dynamically (already partly done); drop the literal ID; declare vertical->sequence mapping once in config.json.

### [LOW] failure_handling
- **Evidence** (line 223-225): "**Expected Success Rate:** 95%+ (most failures due to email validation) ... - Retry if rate limited"
- **Issue:** Rate-limit retry + per-prospect logging exist, but no halt/alert if the whole batch fails or the email account resolves to none beyond an inline ERROR note (line 199).
- **Fix:** Add explicit alert + halt on Stage 6 email-account failure or sub-threshold batch success.

## Missing tool references

- qualify_lead

## Self-healing gap (see specs/self-healing-template.md)

Per-prospect enrollment logging + rate-limit retry, but no run log at ~/.claude/skill-runs/sequence-load.jsonl and no batch-level degrade/halt/alert beyond an inline ERROR when the email account is missing. Upstream HTML-scrape has no fallback if parsing fails.

## Overlap candidates (flag only — no removal)

- prospect-refresh
- prospect-research-to-cadence
- crm-integration-skill
