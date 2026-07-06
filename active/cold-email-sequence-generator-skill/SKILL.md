---
name: cold-email-sequence-generator-skill
description: Generate personalized cold email sequences (7-14 emails) with A/B test subject lines, follow-up timing recommendations, and integrated social proof. Creates multi-touch campaigns optimized for response rates. Use when users need outbound email campaigns, sales sequences, or lead generation emails.
---

# Cold Email Sequence Generator

<objective>
Craft personalized, value-driven cold email sequences (5-14 emails) with A/B test subject lines, optimal send timing, social proof integration, and breakup strategy. Produces complete multi-touch campaigns optimized for open and reply rates across any industry or persona.

**Scope note:** this skill is the generic, industry-agnostic template engine (framework, timing, A/B copy structure). For Epiphan-specific BDR sequences that need live spec verification and Nooks/HubSpot enrollment, use `sdr-email-sms-playbook-skill` instead — it shares the same gates below but is scoped to Epiphan's product line and dial-list pipeline. This skill still applies Epiphan's Golden Rules gates whenever the input list is real Epiphan contacts (see Stage 0).
</objective>

<quick_start>
**Trigger:** "Create a cold email sequence for [audience]" or "Write a 7-email sequence for [use case]"
**Input:** Target audience/ICP or contact list, your value proposition, social proof/case studies, sequence length
**Output:** Gmail drafts (one per email, via `mcp__Gmail__create_draft`, send-from `tkipper@epiphan.com`) for a real Epiphan contact list, plus the full sequence doc (subject lines A/B, body copy, timing, personalization variables, performance benchmarks) as the working reference. If the audience is a hypothetical/example persona with no real recipient, return the sequence doc only — there is nothing to draft.
</quick_start>

<variant_support>
This skill supports A/B variants via config.json.
1. Read this skill's `config.json` — check if `variants.enabled` is true
2. If enabled, run: `bash scripts/variant-assigner.sh cold-email-sequence-generator-skill $(date +%s)`
3. Apply the `prompt_suffix` from the assigned variant's definition to modify the workflow
4. Record the variant name in the outcome sidecar (see final stage below)

**Current experiment:** `cold-email-subject-style-001`
- `control`: Standard 7-email framework
- `concise`: 5-email framework, 50-word max per email
</variant_support>

<success_criteria>
- [ ] If the input is a real contact list, every contact survived the `qualify_lead` gate (Stage 0) before any sequence copy was generated
- [ ] Sequence type selected (Classic 7-email, Fast-Track 5, Long-Play 12-14, Event-Based, Re-Engagement)
- [ ] Each email has A/B subject lines, body copy, and clear single CTA
- [ ] Send timing and day/time recommendations included
- [ ] Personalization variables identified with sourcing guidance
- [ ] Social proof integrated (case studies, stats, testimonials)
- [ ] Every Epiphan/competitor product claim used in a step is confirmed via `search_product_knowledge` / `search_product_catalog` — never stated from memory; unverified claims are dropped, not guessed
- [ ] Every filled email string passes `check_my_copy` (Epiphan Brand) before being treated as final
- [ ] Breakup email included as final touch
- [ ] Performance benchmarks provided for optimization
- [ ] For a real contact list, each gated email is staged as a Gmail draft via `mcp__Gmail__create_draft` (send-from `tkipper@epiphan.com`) — not just returned as chat text
</success_criteria>

<workflow>

## Stage 0: Qualify the List (gate)

Run this stage whenever the input is a real Epiphan contact list (has contactIds/emails), before any template is filled in. Skip only when the "audience" is a hypothetical persona with no real recipients — note that explicitly and proceed straight to Sequence Types.

1. For each contact, call `qualify_lead` (dry run — do not pass `writeToHubSpot: true` from this skill). Use the returned `category`, `power_level`, and junk flag as the single source of truth; don't hand-roll Golden Rules keyword tables here (see `skill-audit/specs/suppression-spec.md` for why — dedup/suppression logic drifts when reimplemented per skill).
2. Drop contacts qualify_lead flags as junk, `lifecyclestage = customer`, or channel partner, per CLAUDE.md Golden Rules.
3. AE-owned contacts (Lex Evans, Ron Epstein, Phillip Sandler): apply the 90-day stale exception from CLAUDE.md — only contacts stale >90 days stay eligible; otherwise exclude.
4. Contacts that fail the gate are not sequenced and are not included in the emails-generated count — log the exclusion reason per contact instead of silently dropping it (see outcome sidecar below).
5. Survivors carry forward `power_level` (ATL/BTL/GRAY) so later personalization/CTA intensity can be tiered if useful (optional; the template framework below works regardless).

## Sequence Types

1. **Classic Cold Outreach** (7 emails, 2 weeks)
2. **Fast-Track** (5 emails, 1 week)
3. **Long-Play Nurture** (12-14 emails, 4-6 weeks)
4. **Event/Trigger-Based** (3-5 emails, event-specific)
5. **Re-Engagement** (5 emails, revive old leads)

## Email Sequence Framework

| Email # | Role | Goal | Length | CTA Style |
|---------|------|------|--------|-----------|
| 1 | Introduction | Make them aware you exist | 50-100 words | Soft ask (reply, quick question) |
| 2 | Value Proof | Establish credibility | 75-125 words | Specific meeting time |
| 3 | Different Angle | Address alternative pain | 50-75 words | Yes/no question |
| 4 | Social Proof | Show peer validation | 60-90 words | Simple reply |
| 5 | Resource Share | Give before asking | 40-60 words | Soft (let me know if helpful) |
| 6 | Direct Ask | Be straightforward | 30-50 words | Direct meeting request |
| 7 | Breakup | Last attempt + opt-out | 25-40 words | "Should I close your file?" |

## Timing & Sending

| Email # | Day | Time | Expected Open Rate |
|---------|-----|------|--------------------|
| 1 | Day 0 | 10:00 AM | 40-50% |
| 2 | Day 2 | 11:00 AM | 30-40% |
| 3 | Day 4 | 2:00 PM | 25-35% |
| 4 | Day 6 | 10:30 AM | 20-30% |
| 5 | Day 8 | 3:00 PM | 15-25% |
| 6 | Day 10 | 9:00 AM | 12-20% |
| 7 | Day 14 | 4:00 PM | 10-18% |

**Best Practices**: Tuesdays-Thursdays highest open rates. 10-11 AM and 2-3 PM optimal. Avoid Mondays (inbox overload) and Fridays (weekend mode). Send in recipient's local timezone.

## Email Templates

**Verification Gate (applies to every template below):** any bracketed placeholder that resolves to a specific Epiphan product claim, spec, price/warranty figure, or competitor statement (e.g. "[achieve specific outcome]", "How [competitor] handles [challenge]", "[Specific result # with metric]") must be confirmed live via `search_product_knowledge` or `search_product_catalog` before it's filled in — never state a spec or competitor status from memory, they go stale. If verification fails or the tool is unavailable, mark the claim `[unverified — needs spec check]` and drop it from the email rather than guessing.

**Brand Voice Gate (applies to every template below):** once a template is filled in with real copy, run `check_my_copy` (Epiphan Brand) on the full subject + body before treating it as final. Resolve every flag; never carry off-voice copy forward into a draft.

### Email #1: The Introduction
**Subject Lines (A/B Test)**:
- A (Curiosity): `Quick question about [their company]'s [specific challenge]`
- B (Value): `[Quantifiable outcome] for [their company type]`
- C (Personal): `[Name], saw your post about [specific topic]`

```
Hi [First Name],

I noticed [specific observation about their company/role] and thought you might be facing [specific challenge].

We've helped [similar company 1] and [similar company 2] [achieve specific outcome] without [common objection].

Worth a quick 15-minute conversation to see if we can do the same for [their company]?

Best,
[Your Name]

P.S. - [Personalized one-liner based on research]
```

### Email #2: The Value Proof
**Subject**: "How [Similar Company] achieved [specific result]"

```
[First Name],

Following up—wanted to share how this worked for a company like [theirs].

[Similar Company] was [specific situation]. In just [timeframe], they:
- [Specific result #1 with metric]
- [Specific result #2 with metric]
- [Specific result #3 with metric]

The best part? They got started in under [timeframe] without [common objection].

Would [Day] at [Time] work for 15 minutes?

[Your Name]
```

### Email #3: The Different Angle
**Subject**: "Different thought about [their company]"

```
Hi [First Name],

I realize [original pain point] might not be top of mind right now.

But what about [alternative pain point]?

Most [their role]s say [common complaint], which is why [mini value prop].

If this hits closer to home, happy to share how [quick win].

[Your Name]

P.S. - If neither is relevant, just let me know and I'll stop!
```

### Email #4: The Social Proof
**Subject**: "[Mutual connection] suggested I reach out" OR "How [competitor] handles [challenge]"

```
[First Name],

I was speaking with [name/title] at [similar company] about [challenge].

Here's what they said after implementing [solution]:
"[Direct quote with specific result]"

Open to a quick call to hear more about what's working in [their industry]?

[Your Name]
```

### Email #5: The Resource Share
**Subject**: "Thought you might find this useful"

```
[First Name],

No ask here—just sharing something helpful:

[Brief description of resource]: [Link]

We created this after hearing [their role]s struggle with [pain point]. Actionable tips even if you never use our product.

Hope it helps!

[Your Name]
```

### Email #6: The Direct Ask
**Subject**: "Let's cut to the chase"

```
[First Name],

Let me be direct: I think we could help [their company] [achieve outcome] based on [observation].

I'd like to show you:
1. [Specific thing #1]
2. [Specific thing #2]
3. [How others in their position use it]

15 minutes. No pressure. How's [specific day/time]?

[Your Name]
[Phone number]
```

### Email #7: The Breakup
**Subject**: "Should I close your file?"

```
[First Name],

I'll assume [topic] isn't a priority right now—totally fine.

I'll close your file unless I hear otherwise. For what it's worth, we see best results when [time-sensitive reason], so if you want to revisit, might be worth a quick chat now.

No worries either way—appreciate your time.

[Your Name]

P.S. - If someone else at [their company] should hear about this, happy to redirect.
```

**Breakup Variations**:
- **FOMO**: "Taking you off the list. FYI—[competitor] just started and is seeing [early result]."
- **Permission**: "Assuming this is: 1) Not relevant, 2) Not priority, 3) Bad timing. Which? If #3, when should I check back?"
- **Referral**: "Clearly I'm not reaching the right person. Should I talk to someone else about [topic]?"

## A/B Testing Strategy

**Test Priority** (in order):
1. **Subject Lines**: Question vs. Statement, Generic vs. Personalized, Short vs. Long
2. **Email Body**: Length (50 vs. 100 words), CTA style (Link vs. Question vs. Time slot)
3. **Send Time**: Morning vs. Afternoon, Tue vs. Wed vs. Thu

**Method**: Send to 100 prospects (50/50 split), wait 48 hours, measure open + reply rates, winner goes to remaining list.

## Performance Benchmarks

| Metric | Good | Great | Exceptional |
|--------|------|-------|-------------|
| Email 1 Open Rate | 35-45% | 45-55% | 55%+ |
| Email 1 Reply Rate | 3-8% | 8-15% | 15%+ |
| Sequence Reply Rate | 8-15% | 15-25% | 25%+ |
| Positive Reply % | 40-50% | 50-70% | 70%+ |
| Meeting Booked % | 1-3% | 3-6% | 6%+ |

## Segmentation

Adjust sequences by **Industry** (swap case studies, use industry terminology), **Company Size** (Startup: ROI focus; Mid-Market: scalability; Enterprise: security/compliance), **Role** (Executive: strategic outcomes; Practitioner: time savings; Technical: architecture/specs), and **Intent** (Hot: shorter/faster; Warm: standard 7-email; Cold: longer nurture).

## Quick-Start Templates

**SaaS Sales**: Question about growth metric → Competitor case study → Alternative pain → Mutual connection → Free benchmark report → 15-min demo → Close file

**Agency/Services**: Recent achievement → Client case study → Quick idea for challenge → Competitor approach → No-strings audit → 15-min call → Bad timing?

**Partnership**: Mutual contact intro → Win-win opportunity → Similar partner example → Partnership program question → Worth exploring?

## Pro Tips

1. **3-Second Rule**: Prospect should understand value in first 3 seconds
2. **One CTA Only**: Don't give multiple options
3. **Mobile-First**: 50%+ opened on mobile; keep scannable
4. **No Attachments**: Use links; attachments trigger spam filters
5. **The P.S. Works**: PostScripts get read; use for secondary CTA
6. **Follow-Up Matters**: 80% of responses come from emails 3-7

## Pre-Launch Checklist

- [ ] Sender email has good deliverability (SPF, DKIM, DMARC)
- [ ] Email warmed up (sent successful emails recently)
- [ ] List cleaned (no invalid emails)
- [ ] Personalization variables all filled
- [ ] Links tested and tracked
- [ ] CRM integration working
- [ ] A/B tests configured
- [ ] Daily send limits set (avoid spam flags)

## Stage Final: Stage Gmail Drafts (real contact list only)

For a real, `qualify_lead`-gated contact list, do not return the sequence as chat text alone. Once each email has passed both the Verification Gate and the Brand Voice Gate:
1. Call `mcp__Gmail__create_draft` once per gated email, per contact, sender `tkipper@epiphan.com` (never any other sender, per CLAUDE.md).
2. Subject = the winning/primary A/B subject line unless the user asked to draft both variants (then draft both, clearly labeled).
3. Leave send timing as guidance in the accompanying sequence doc — this skill stages drafts, it does not schedule or send them. Tim reviews and sends per his draft → review → send workflow.
4. If a claim couldn't be verified or copy couldn't pass `check_my_copy`, do not draft that email — surface it as skipped with the reason instead.

For a hypothetical/example persona (no real recipient), skip this stage and return the sequence doc only.

## Emit Outcome Sidecar

As the final step, write to `~/.claude/skill-analytics/last-outcome-cold-email-sequence-generator.json`:
```json
{"ts":"[UTC ISO8601]","skill":"cold-email-sequence-generator","version":"1.1.0",
 "variant":"[assigned variant or default]","status":"[success|partial|error]",
 "runtime_ms":[estimated ms from start],
 "metrics":{"sequences_created":1,"emails_generated":[count],"subject_variants_generated":[count],
            "contacts_qualified":[count or null],"contacts_dropped_gate":[count or null],
            "claims_unverified":[count],"drafts_created":[count]},
 "error":null,"session_id":"[YYYY-MM-DD]"}
```

**Status rules:**
- `success` — sequence fully generated; for a real list, every survivor's emails passed both gates and were drafted.
- `partial` — one or more claims failed `search_product_knowledge`/`search_product_catalog` verification (dropped, not guessed), or one or more filled emails failed `check_my_copy` and were skipped rather than drafted. Sequence still emitted for the rest.
- `error` — `qualify_lead` gate left zero eligible contacts, or draft creation failed outright.

Also append one line to `~/.claude/skill-runs/cold-email-sequence-generator.jsonl` (`{ts, status, contacts_in, contacts_qualified, drafts_created, error}`) so a failed/partial run is visible in the run log, not just the analytics sidecar.

</workflow>

<dependencies>
## MCP tools
- `qualify_lead` (Epiphan AI) — Stage 0 list gate; dry run by default, never pass `writeToHubSpot` from this skill.
- `search_product_knowledge` / `search_product_catalog` (Epiphan AI) — required before any Epiphan/competitor product claim is used in a step.
- `check_my_copy` (Epiphan Brand) — required brand-voice gate on every filled email before it's final.
- `mcp__Gmail__create_draft` — stages the gated sequence as Gmail drafts; send-from `tkipper@epiphan.com` only.

## Overlap (flag only — no removal/merge here)
- `sdr-email-sms-playbook-skill` — Epiphan-specific equivalent with the same gates; prefer it for live Epiphan BDR sequences.
- `email-template-generator-skill`, `personalization-at-scale-skill` — related template/personalization tooling; this skill owns the multi-touch sequence framework.
</dependencies>

## Guardrails
- Never skip Stage 0 for a real contact list — no sequence copy is generated for a contact until it survives `qualify_lead`.
- Never state an Epiphan/competitor spec, EOL status, or price/warranty figure from memory — confirm via `search_product_knowledge`/`search_product_catalog` first; unverified claims are dropped, not guessed.
- Never treat a filled email as final, and never draft it, until it has passed `check_my_copy`.
- Never send directly — `mcp__Gmail__create_draft` only, from `tkipper@epiphan.com`, so Tim reviews before send.
- If a gate tool is unavailable, degrade to `partial` status and say so in the sidecar/run log — don't silently fall back to ungated output.

## Skill metadata
**Version:** 1.1.0 · **Author:** Tim Kipper · **Variants:** `cold-email-subject-style-001` (control/concise, see `config.json`)
