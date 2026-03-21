---
description: "Record outcome/feedback for a skill run"
argument-hint: "<skill-name> [success|partial|error] [notes]"
allowed-tools: Bash, Read, Write
---

# /skill-feedback — Record Skill Outcome

Record the outcome of a skill run to `outcomes.jsonl` and `feedback.jsonl` for health tracking.

## Instructions

1. Parse `$ARGUMENTS` for: `<skill-name>` `<status>` `<notes...>`
   - If no arguments provided, ask: "Which skill? What was the outcome (success/partial/error)? Any notes?"
   - Status must be one of: `success`, `partial`, `error`

2. Look up the skill's `config.json` to get:
   - `version` field
   - `variants.enabled` — if true, ask which variant was used or default to "default"

3. Build the outcome JSON:
```json
{
  "ts": "[current UTC ISO8601]",
  "skill": "[skill-name]",
  "version": "[from config.json]",
  "variant": "[variant or default]",
  "status": "[success|partial|error]",
  "session_id": "[today YYYY-MM-DD]"
}
```

4. Build the feedback JSON (adds `notes` field):
```json
{
  "ts": "[same ts]",
  "skill": "[skill-name]",
  "version": "[version]",
  "variant": "[variant]",
  "status": "[status]",
  "notes": "[user's notes]",
  "session_id": "[today YYYY-MM-DD]"
}
```

5. Append the outcome to `~/.claude/skill-analytics/outcomes.jsonl`
6. Call `bash scripts/log-feedback.sh` with the feedback JSON piped to stdin
7. Confirm: "Recorded: **[skill]** v[version] ([variant]) = [status]"

## Examples

```
/skill-feedback prospect-enrich success "32 phones found, 12 ATL"
/skill-feedback morning-brief partial "Calendar API timed out, dial list still generated"
/skill-feedback cold-email-sequence-generator error "Apollo rate limit hit"
```
