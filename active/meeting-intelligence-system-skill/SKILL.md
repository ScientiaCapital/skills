---
name: meeting-intelligence-system-skill
description: Structure and summarize INTERNAL meeting transcripts (standups, planning, retros, 1:1s) into decisions, owned action items, blockers, sentiment, and a draft follow-up email. Use when: "analyze this meeting", "extract action items", "meeting minutes", "summarize this standup/planning/retro", "follow-up email from these notes". NOT for sales/prospect calls — route those to call-recording-analyzer (Clari scorecard) or sdr-call-coaching. Runs the follow-up email through the Epiphan brand-voice gate (check_my_copy/get_writing_style) and stages it via gmail_create_draft — never pasted as raw chat text.
---

# Meeting Intelligence System

<objective>
Analyze **internal** meeting transcripts — standups, planning sessions, retros, 1:1s — to extract decisions, action items, blockers, sentiment, and key discussion points. Generates structured meeting summaries and a brand-gated, drafted follow-up email so nothing falls through the cracks after a meeting.

**Scope note:** this skill owns internal/team meetings, not sales or prospect calls. A sales-call
transcript should go to `call-recording-analyzer` (Clari scorecard) or `sdr-call-coaching` instead —
those skills score talk-track/MEDDIC signals this one doesn't produce.
</objective>

<quick_start>
**Trigger:** "analyze this meeting", "extract action items", "meeting minutes", "summarize this standup/planning/retro", "follow-up email from these notes"
**Not this skill:** sales/prospect call transcripts — see `call-recording-analyzer` or `sdr-call-coaching`
**Output:** Structured meeting summary with decisions, action items table, blockers, sentiment analysis, and a follow-up email drafted via `gmail_create_draft` (after the `check_my_copy` brand gate) — never pasted as inline chat text
</quick_start>

<success_criteria>
- [ ] All decisions extracted with owners and rationale
- [ ] Action items listed with owner, deadline, and priority
- [ ] Blockers and risks identified with mitigation actions
- [ ] Follow-up email drafted, passed through `check_my_copy`, and staged via `gmail_create_draft` (never sent, never left as raw chat text)
- [ ] Transcript confirmed as an internal/team meeting — sales/prospect calls redirected to `call-recording-analyzer` or `sdr-call-coaching`
</success_criteria>

<workflow>

## When to Use This Skill

Activate when the user, for an **internal/team meeting** (standup, planning, retro, 1:1, cross-functional
sync):
- Provides a meeting transcript or recording
- Asks to "analyze this meeting"
- Needs action items extracted from notes
- Wants to generate meeting minutes
- Asks for decisions made in a meeting
- Needs a follow-up email created
- Mentions meeting notes or transcripts
- Asks to "summarize this standup/planning/retro"

**Do NOT activate for sales or prospect call transcripts** — a customer/prospect on the call is the
signal to redirect: send Clari transcripts to `call-recording-analyzer` for the scorecard, or to
`sdr-call-coaching` for coaching feedback. Those skills own MEDDIC/talk-track signal extraction this
one doesn't do.

## Instructions

1. **Extract Meeting Metadata**
   - Identify meeting title/topic
   - Note participants (if mentioned)
   - Determine meeting date/time (if available)
   - Identify meeting type (standup, planning, retrospective, etc.)

2. **Identify Decisions Made**
   - Extract all explicit decisions
   - Note who made each decision (if clear)
   - Include rationale for decisions (if stated)
   - Flag tentative decisions vs. final decisions
   - Note decisions that need follow-up approval

3. **Extract Action Items**
   - List all tasks assigned or volunteered
   - Identify owner for each action item
   - Note deadlines or timeframes mentioned
   - Flag action items without clear owners
   - Prioritize action items (if priority discussed)
   - Note dependencies between action items

4. **Identify Blockers and Risks**
   - Extract mentioned blockers
   - Note risks or concerns raised
   - Identify unresolved issues
   - Flag items needing escalation
   - Note resource constraints mentioned

5. **Analyze Discussion Sentiment**
   - Gauge overall meeting tone (productive, tense, confused, aligned)
   - Identify areas of agreement and disagreement
   - Note team morale indicators
   - Flag conflict or tension points

6. **Extract Key Topics Discussed**
   - Summarize main discussion points
   - Note questions raised
   - Identify topics needing follow-up
   - Highlight important context or background

7. **Generate Follow-Up Communications**
   - Create meeting minutes/summary
   - Draft the action item tracking email body (see Output Format)
   - **Brand Gate (required before staging):** run `check_my_copy` (and `get_writing_style` for voice
     reference) on the drafted body. Fix anything flagged — off-voice copy does not go out.
   - **Stage, don't paste:** once gated, create the email via `gmail_create_draft` (to: participants,
     subject and body from the gated draft). The email lives in Gmail as a draft for review/edit/send —
     it is never emitted as final chat text standing in for delivery.
   - Suggest calendar invites for follow-ups
   - Recommend next steps

## Output Format

```markdown
# Meeting Summary: [Title]
**Date**: [Date] | **Participants**: [Names]

## 📋 Executive Summary
[2-3 sentence overview of meeting purpose and outcome]

## ✅ Decisions Made
1. **[Decision]**
   - Owner: [Name]
   - Rationale: [Why]
   - Status: Final / Needs approval

## 🎯 Action Items
| Priority | Action | Owner | Deadline | Status |
|----------|--------|-------|----------|--------|
| High | [Task] | [Name] | [Date] | Not started |
| Medium | [Task] | [Name] | [Date] | Not started |

## 🚧 Blockers & Risks
1. **[Blocker]** - [Impact] - Needs: [Action]
2. **[Risk]** - [Mitigation plan]

## 💬 Key Discussion Points
- [Topic 1]: [Summary]
- [Topic 2]: [Summary]

## ❓ Open Questions
1. [Question] - Owner: [Who will answer]

## 📊 Sentiment Analysis
- **Overall Tone**: [productive/tense/etc.]
- **Team Alignment**: [high/medium/low]
- **Concerns Raised**: [Summary]

## 📧 Follow-Up Email — Staged as Gmail Draft

Shown below for review; the actual delivery is a `gmail_create_draft` call made **after** the
`check_my_copy` brand gate passes (see Instructions step 7) — this markdown is a preview, not the
output artifact.

Subject: Action Items from [Meeting Title] - [Date]

Hi team,

Thanks for joining today's [meeting type]. Here are our key outcomes:

**Decisions:**
- [Decision 1]

**Your Action Items:**
[Name]: [Task] by [Date]

**Blockers:**
- [Blocker] - please [action]

Next meeting: [Date/Time]

Best,
[Your name]
```
**Confirm to the user:** "Follow-up email gated and staged as a Gmail draft — review before sending."

## Examples

**User**: "Analyze this standup transcript"
**Response**: Extract blockers mentioned → List action items per person → Flag impediments → Note team velocity concerns → Generate summary with focus on blockers

**User**: "Create action items from this product planning meeting"
**Response**: Identify all decisions (feature prioritization) → Extract action items (design mockups, tech spec) → Assign owners → Set deadlines → Create tracking table → Draft follow-up email

## Best Practices

- Be specific with action items (not vague "look into X")
- Always try to identify owners (flag if unclear)
- Differentiate between decisions and proposals
- Preserve important context for decisions
- Flag action items without deadlines
- Note commitments made by each participant
- Include relevant quotes for controversial decisions
- Use clear, scannable formatting
- Prioritize action items by urgency
- Flag dependencies between tasks
- Generate professional, actionable follow-up emails

## Required MCP Tools
- **Gmail MCP:** `gmail_create_draft` — stages the gated follow-up email (draft-first, never sent directly).
- **Epiphan Brand MCP:** `check_my_copy`, `get_writing_style` — brand-voice gate, required before any
  follow-up email draft is staged (Instructions step 7).

## Failure Handling & Outcome Logging

Follow `skill-audit/specs/self-healing-template.md` for the failure ladder (retry → degrade → alert →
halt) and the three-way status definition:
- **success** — transcript parsed, action items have identifiable owners, follow-up email passed
  `check_my_copy` and was staged via `gmail_create_draft`.
- **partial** — name the degraded stage, e.g. transcript was partially unparseable (garbled audio,
  missing speaker labels) so some action items have no owner, or `check_my_copy`/`get_writing_style`
  was unavailable and the draft was staged with a flagged `[unverified voice]` note instead of being
  silently gated. Never skip staging silently — if `gmail_create_draft` fails, surface the drafted
  text back to the user with an explicit "could not stage as a Gmail draft" alert rather than treating
  chat output as done.
- **error** — no usable output at all (empty/unreadable transcript, or the input turned out to be a
  sales/prospect call and was redirected instead of processed here).

## Emit Outcome Sidecar

As the final step, write to `~/.claude/skill-analytics/last-outcome-meeting-intelligence-system.json`:
```json
{"ts":"[UTC ISO8601]","skill":"meeting-intelligence-system","version":"1.0.0","variant":"default",
 "status":"[success|partial|error]","runtime_ms":[estimated ms from start],
 "metrics":{"meetings_analyzed":[n],"action_items_extracted":[n],"decisions_captured":[n],"drafts_staged":[n]},
 "error":null,"session_id":"[YYYY-MM-DD]"}
```
Use status "partial" if some stages failed but results were produced (name the failing stage per above).
Use "error" only if no output was generated.

</workflow>
