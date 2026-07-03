---
name: demo-execution-playbook
id: demo-execution-playbook
version: 1.0
author: Epiphan Sales Engineering
description: Structured demo execution framework for AEs to drive deals forward with vertical-specific flows, live coaching, and post-demo scoring
roles:
  - Account Executive
  - Sales Engineer
products:
  - Pearl-2
  - Pearl Mini
  - Pearl Nano
  - Pearl Nexus
  - EC20 PTZ
  - Epiphan Connect
triggers:
  - "demo playbook"
  - "demo flow for"
  - "how should I demo to"
  - "demo checklist"
  - "live demo prep"
  - "what to show"
  - "demo execution"
dependencies:
  - epiphan-ai-mcp-guide
  - meddic-call-prep-auto
  - challenger-sale
keywords:
  - demo execution
  - vertical-specific
  - MEDDIC
  - live demo coaching
  - objection handling
  - post-demo scorecard
---

# Demo Execution Playbook

<objective>
Enable Phil Sandler and Lex Evans to execute high-confidence, vertical-specific product demos that:
- Uncover and validate MEDDIC gaps (Economic Buyer, Decision Criteria, Decision Process, Identify Pain)
- Map features to prospect-stated pain points (40/60 talk-listen ratio)
- Position Epiphan competitively against Extron, Blackmagic, Crestron, vMix, Teradek
- Generate next-step commitments with measurable confidence lift
- Create repeatable, scoring-based demo success metrics
</objective>

<quick_start>
**Invoke with:** `demo playbook [company name]` or `how should I demo to [vertical]`

**Returns:** 
1. Pre-demo checklist (5 min)
2. Vertical-specific demo flow (10 min prep)
3. Live demo coaching card (1-screen reference)
4. Post-demo scorecard template

**Time to ready:** 15 minutes from trigger
</quick_start>

<success_criteria>
- MEDDIC Economic Buyer attends demo
- Prospect verbalizes pain within first 3 minutes
- AE achieves 40% talk / 60% prospect talk ratio
- Demo focused on 2-3 core capabilities (not feature dump)
- Next step agreed before meeting ends
- Post-demo scorecard completed same day
- Demo confidence score improves by +2 points (1-10 scale)
</success_criteria>

<core_content>

## Workflow (Staged)

### Stage 1: Pre-Demo Intel Gathering (Parallel MCP Calls)

Collect deal context, attendees, prior discovery, and competitive intelligence.

**Call Set:**
1. `hubspot_get_deal(dealId)` → Stage, amount, notes, close date
2. `hubspot_search_contacts(q=company_name)` → Contact list, titles, roles
3. `clari_search_calls(attendeeEmail=prospect_email)` → Discovery calls recorded
4. `ask_agent(question="What pain points and competitive context?")` → CRM memory
5. `apollo_organizations_enrich(domain=company_domain)` → Company size, tech stack, industry

**Output Map:**
- Deal stage → Demo urgency (Proposal = polish; Negotiation = competitive)
- Contact titles → MEDDIC role assignment (CEO/CTO = EB; Manager = User Champion; ITOps = Blocker)
- Call summaries → Pain recap (what Clari flagged as key objections/needs)
- Tech stack → Integration readiness (CMS, streaming protocol, architecture fit)
- Vertical → Demo path selection (see Stage 2)

---

### Stage 2: Vertical-Specific Demo Flow Selection

Match prospect vertical to pre-built demo sequence. Each path prioritizes Epiphan's fit.

| Vertical | ICP | Demo Focus |
|----------|-----|------------|
| Higher Ed | 90 | Pearl-2 multi-room + Epiphan Connect + CMS auto-sync (Kaltura/Panopto/YuJa) |
| Courts/Legal | 85 | Dual recording (local SSD + SRT cloud), failover, secure playback, audit trail |
| Corporate AV | 80 | Pearl Mini NDI/RTMP hybrid meetings, multi-site Connect dashboard |
| Government | 80 | On-prem recording/streaming, RTMP/SRT, no-cloud-required option |
| Healthcare | 75 | HIPAA-friendly multi-camera capture, LMS role-based access, audit logs |
| Houses of Worship | 70 | One-button YouTube/Facebook streaming, volunteer-proof operation |
| K-12 | 65 | One-button classroom REC, LMS auto-publish, district Connect dashboard |

Full demo arcs (RECAP / AGENDA / SHOW VALUE / SUMMARIZE / NEXT STEPS), key questions to ask during each demo, and per-vertical competitive displacement lines: see [reference/vertical-demo-flows.md](reference/vertical-demo-flows.md).

---

### Stage 3: RECAP-AGENDA-SHOW VALUE-SUMMARIZE-NEXT STEPS Framework

This is your demo skeleton. Follow it for every vertical. It ensures you validate pain, stay on track, and never do a feature dump.

**RECAP (2 min):**
- "Based on our calls with [BDR name] and [previous call with attendee], you told us you need [pain point 1], [pain point 2], and [pain point 3]. Is that still accurate?"
- Wait for confirmation. This is not rhetorical—if they disagree, adjust your demo path.
- **Why:** MEDDIC-heavy. You're validating Pain and Identifying Buyer (are they nodding? Do they care?).

**AGENDA (1 min):**
- "Today I want to show you three things: [Feature A related to pain 1], [Feature B related to pain 2], [Feature C related to pain 3]. Then we'll talk about next steps. Sound good?"
- Sets boundary. No derails. Manages expectations.
- **Why:** Challenger Sale. You're teaching and taking control.

**SHOW VALUE (8-10 min):**
- Alternate between showing and asking (40/60 rule).
- Feature → "Here's how we solve [pain]: [show feature]" → "How does that compare to your current setup?" → Listen.
- Don't say "features." Say outcomes: "Instead of 3 technicians managing 10 rooms, one IT person manages all of Epiphan Connect."
- **Traffic Light System** (see Stage 4 below).

**SUMMARIZE (2 min):**
- "So we've shown you: [Feature A recap + benefit], [Feature B recap + benefit], [Feature C recap + benefit]. Does that address your top three needs?"
- Confirm. Get head nods.
- **Why:** Close the loop. MEDDIC Decision Criteria validation.

**NEXT STEPS (1 min):**
- "Based on what we showed, I think the best path forward is a [2-week pilot] in [department/location], starting [date]. You'll [specific outcome]. Agree?"
- Don't ask "Do you have questions?" (vague). Ask "Should we pilot Tuesday or Wednesday?" (binary close).
- MEDDIC Decision Process lock-in.

**Total Demo Time: 15-20 minutes. Then discussion/Q&A.**

---

### Stage 4: Live Demo Coaching—The Traffic Light System

Use this during the demo to sense engagement and adapt in real-time.

**GREEN (Engaged, asking questions, leaning forward):**
- Keep going. Don't pause to explain every detail—they're following.
- Invite more: "Should I show you how [related feature] works, or move to [next pain point]?"
- Let them drive the pace.

**YELLOW (Quiet, checking phone, polite but not engaged):**
- Pause demo. Don't keep talking.
- Ask a question: "Does this solve the [specific pain] we mentioned, or should I show you something different?"
- Get them back in the conversation. If they say "not quite," pivot to a different demo path.

**RED (Objections, skepticism, "That won't work because..." or visible frustration):**
- Stop demo immediately.
- Use LAER (Listen-Acknowledge-Explore-Respond):
  - **Listen:** Let them finish. Don't interrupt.
  - **Acknowledge:** "I hear you. That's a fair concern."
  - **Explore:** "Tell me more about [concern]. What does your current setup do?" (Dig into the real issue.)
  - **Respond:** Address the root concern. Go back to demo if needed.
- Example: 
  - Prospect says: "Our IT won't allow any cloud stuff."
  - You: "I hear you. IT security is critical. Let me ask—is it cloud per se, or data residency that's the concern?"
  - Prospect: "We have HIPAA requirements. Data can't leave our servers."
  - You: "Perfect. Pearl actually has on-prem recording + optional on-prem Epiphan Connect. Let me show you that setup instead." (Pivot to on-prem flow.)

**Questions to Ask DURING Demo (to maintain 40/60 ratio):**
1. "How does that compare to what you're doing today?"
2. "Would [feature] work with your [system/LMS]?"
3. "If we could solve [pain], what's your next step?"
4. "Who on your team needs to validate this?" (→ Uncover MEDDIC blockers.)
5. "Does this address [pain point from discovery]?"
6. "What's your timeline to make a decision?"

**How to Handle "Can You Show Me X?" Derails:**
- Prospect: "Can you show me how it integrates with [system you didn't plan]?"
- You: "Great question. Let's table that for our technical deep-dive next week. For today, I want to make sure we cover the core three things we talked about. [Continue demo.] We'll demo the [system] integration with your IT team. Sound good?"
- **Why:** Stay in control. Don't let them set the agenda. Challenger Sale principle.

---

### Stage 5: Objection Handling Matrix

Top 5 objections by vertical + LAER response templates. Adapt to your prospect.

Full objection matrix with LAER response templates for all five verticals (Higher Ed LMS integration, Courts/Legal Matrox, Corporate AV Zoom Rooms, Government no-cloud, Healthcare/K-12 pricing): see [reference/objection-handling-matrix.md](reference/objection-handling-matrix.md).

---

### Stage 6: Post-Demo Scorecard

Complete this **same day** after every demo. It informs your next step and measures demo effectiveness.

**Template:**

```
DEAL: [Company Name]
DATE: [Demo Date]
ATTENDEES: [Name/Title] (Y/N EB), [Name/Title] (Y/N User Champion)

MEDDIC VALIDATION:
[ ] Pain verified? (Prospect said "Yes, that's our issue" or similar)
[ ] Economic Buyer attended? (Y/N) [Name if Y]
[ ] Decision Criteria clear? (What are they evaluating us on?)
[ ] Decision Process mapped? (Who votes? Timeline?)
[ ] Identify pain—recap the 3 pains you addressed:
    1. ________
    2. ________
    3. ________

DEMO EXECUTION:
[ ] Talk/listen ratio: Estimate % (Target: 40% AE / 60% Prospect)
[ ] Traffic light status: GREEN / YELLOW / RED (Last 5 min: How engaged were they?)
[ ] Features shown: [Feature A, Feature B, Feature C]
[ ] Derails handled? (Y/N) If Y, how?
[ ] Next step agreed? (Y/N) What: ________ When: ________ Owner: ________

COMPETITIVE POSITION:
Before demo, your confidence: __/10
After demo, your confidence: __/10
Delta: +/- __
Why? (vs. Extron, Blackmagic, Teradek, vMix, etc.)

POST-DEMO ACTIONS:
[ ] Send follow-up email (include ROI, integration diagram, references)
[ ] Schedule technical deep-dive (if needed)
[ ] Send legal/compliance brief (if Courts/Gov/Healthcare)
[ ] Introduce to sales engineer / customer success
[ ] Enter next step in HubSpot deal
[ ] Share recording with internal team (if prospect allowed)

NOTES:
[Any surprises, objections, or context for your manager/BDR]
```

**Minimum Completion:** 5 minutes post-demo. Upload to HubSpot deal record.

---

### Stage 7: Competitive Displacement Scripts

Use these word-for-word when prospect mentions competitors. Delivered calmly, never defensive.

Word-for-word scripts for all six competitors (Extron SMP, Blackmagic ATEM, Crestron, vMix, Teradek, Matrox): see [reference/competitive-displacement-scripts.md](reference/competitive-displacement-scripts.md).

---

### Stage 8: Live Demo Coaching Card (1-Screen Reference)

Print this or keep it on your second monitor during the demo.

```
╔════════════════════════════════════════════════════════════╗
║               LIVE DEMO COACHING CARD                      ║
╠════════════════════════════════════════════════════════════╣
║ STRUCTURE (15-20 min):                                     ║
║ [✓] RECAP pain (2 min)                                     ║
║ [✓] AGENDA what you'll show (1 min)                        ║
║ [✓] SHOW feature + benefit (8-10 min)                      ║
║ [✓] SUMMARIZE what you showed (2 min)                      ║
║ [✓] NEXT STEPS get commitment (1 min)                      ║
╠════════════════════════════════════════════════════════════╣
║ TRAFFIC LIGHT:                                             ║
║ GREEN = Keep going, invite more questions                  ║
║ YELLOW = Pause, ask re-engagement question                 ║
║ RED = Stop demo, LAER (Listen-Acknowledge-Explore-Respond) ║
╠════════════════════════════════════════════════════════════╣
║ TALK/LISTEN TARGET: 40/60 (You: 40%, Them: 60%)            ║
║ QUESTIONS TO ASK:                                          ║
║   • How does that compare to today?                        ║
║   • Would this work with your [system]?                    ║
║   • If we solved [pain], what's next?                      ║
║   • Who needs to validate this?                            ║
║   • What's your timeline?                                  ║
╠════════════════════════════════════════════════════════════╣
║ FEATURE = BENEFIT RULE:                                    ║
║ Never show a feature without connecting to their pain.     ║
║ "This Pearl-2 records multiple cameras simultaneously      ║
║  [FEATURE]—so instead of hiring 2 operators, you have      ║
║  1 box doing the work [BENEFIT]."                          ║
╠════════════════════════════════════════════════════════════╣
║ DERAIL HANDLER:                                            ║
║ Prospect: "Can you show me [off-agenda thing]?"            ║
║ You: "Great question. Let's table that for a technical     ║
║      deep-dive next week. For today, I want to nail the    ║
║      three core things. [Continue demo.]"                  ║
╠════════════════════════════════════════════════════════════╣
║ RED LIGHT SCRIPT (LAER):                                   ║
║ Listen: "Tell me more."                                    ║
║ Acknowledge: "I hear you. That's a fair point."            ║
║ Explore: "What does your current setup do?"                ║
║ Respond: "Here's how Pearl solves that: [pivot]."          ║
╚════════════════════════════════════════════════════════════╝
```

---

### Stage 9: Dependencies & Integration Points

**Tools you'll use:**

1. **Epiphan CRM MCP:**
   - `hubspot_get_deal()` — Fetch deal stage, MEDDIC notes
   - `hubspot_search_contacts()` — Attendee titles, roles
   - `clari_search_calls()` / `clari_get_call_summary()` — Prior discovery, pain/objections
   - `ask_agent()` — Memory of prior engagements
   - `apollo_organizations_enrich()` — Company tech stack, size, vertical

2. **Clari Call Intelligence:**
   - Auto-populated MEDDIC from recorded discovery calls
   - Objection transcripts (what they said in prior calls)
   - Action items and next steps from last call

3. **MEDDIC Call Prep (skill dependency):**
   - Use before your demo to validate you understand all MEDDIC elements
   - Use after to score MEDDIC coverage

4. **Challenger Sale (skill dependency):**
   - Teach (RECAP + AGENDA = teaching framework)
   - Tailor (vertical-specific flows)
   - Take Control (NEXT STEPS binary close)

5. **AE Handoff Brief (sister skill):**
   - Created by BDR Tim Kipper before handing to you
   - Contains discovery summary, MEDDIC, competitive context
   - Your demo builds on this foundation

---

## How to Invoke This Skill

**Trigger phrases:**
- "demo playbook for [company name]"
- "how should I demo to [vertical]?"
- "demo execution for [deal name]"
- "live demo coaching"
- "demo checklist"
- "post-demo scorecard"

**Invoke steps:**
1. Say: `demo playbook for [company]` or `how should I demo to Higher Ed?`
2. Skill returns: Pre-demo checklist → Vertical-specific flow → Live coaching card → Post-demo template
3. You prep (15 min) → Run demo (15-20 min) → Score (5 min)

---

## Additional Resources

- **Epiphan Product Guide:** See `epiphan-ai-mcp-guide` skill for full product specs
- **MEDDIC Framework:** See `meddic-call-prep-auto` skill for full MEDDIC scoring
- **Challenger Sale:** See `challenger-sale` skill for Teach-Tailor-Take Control deep dives
- **AE Handoff Brief:** See `ae-handoff-brief` skill for BDR handoff structure
- **Call Recording Analyzer:** See `call-recording-analyzer` skill for post-call transcript analysis

---

## Version & Maintenance

**v1.0 — Initial Release (2026-04)**
- 7 vertical-specific demo flows
- RECAP-AGENDA-SHOW VALUE-SUMMARIZE-NEXT STEPS framework
- Traffic Light live coaching system
- Objection handling matrix (5 per vertical)
- Competitive displacement scripts (6 competitors)
- Post-demo scorecard template
- LAER objection handling framework

**Author:** Epiphan Sales Engineering  
**Updated:** 2026-04-10  
**Next Review:** 2026-07-10

---


</core_content>
