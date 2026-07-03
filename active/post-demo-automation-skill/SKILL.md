---
name: "post-demo-automation"
title: "Post-Demo Automation"
description: "Automates post-demo follow-up sequence for Epiphan AEs: demo recap emails, internal debrief notes, meeting scheduling, stakeholder expansion, and 5-touch momentum plans."
owner: "Phil Sandler, Lex Evans (Epiphan Video Account Executives)"
slack_channel: "#epiphan-ae"
category: "Sales Automation"
version: "1.0"
status: "production"
trigger_phrases:
  - "post-demo [company]"
  - "demo follow-up [company]"
  - "follow up after [company] demo"
  - "send demo recap"
  - "what's next after [company] demo"
  - "demo debrief [company]"
---

<objective>

## Objective

Automate the post-demo sequence for Epiphan Account Executives to maximize deal momentum. Within 2 hours of demo completion, generate:
- **Demo recap email** (Challenger-style, vertical-specific template)
- **Internal HubSpot debrief note** (MEDDIC scorecard, competitive intel, next-step flagging)
- **Calendar event or check-in plan** (scheduled meeting or 3-day follow-up)
- **Stakeholder expansion research** (if single-threaded)
- **5-touch momentum maintenance sequence** (Day 0, 3, 7, 14, escalation)

Reduces manual work, ensures consistent follow-up quality, and flags at-risk deals early.

</objective>

<quick_start>

## Quick Start

1. **After demo ends**, say: "post-demo Acme Corp" or "demo debrief Acme"
2. **Provide demo details** (optional but faster): Who attended, key takeaways, any objections
3. **Skill collects data** via Clari (recording), HubSpot (deal/contacts), Google Calendar
4. **Within 30 seconds**, you get:
   - Gmail draft (recap email ready to customize & send)
   - HubSpot note (internal summary with MEDDIC update)
   - Calendar invite draft (if next meeting confirmed) OR Day +3 check-in email
   - Stakeholder expansion plan (LinkedIn research, loop-in email draft)
   - 5-touch sequence outline (Day 0, 3, 7, 14, escalation triggers)
5. **Review & send** — all outputs are drafts; you customize tone and timing

</quick_start>

<success_criteria>

## Success Criteria

- ✅ Demo recap email sent within 2 hours of demo end
- ✅ HubSpot deal note logged with MEDDIC update + competitive status
- ✅ Next meeting scheduled (or 3-day check-in drafted)
- ✅ Single-threaded deals flagged; stakeholder research drafted
- ✅ All 5 action items (recap, note, meeting, stakeholder, momentum) completed
- ✅ Deal stage advanced if demo was successful
- ✅ At-risk flags (no EB, unresolved objections, competitor) surfaced to AE
- ✅ BDR escalation auto-triggered on Day 14 if no response

</success_criteria>

## Workflow: 5-Stage Post-Demo Automation

### Stage 1: Data Collection (Parallel Calls)
Execute in parallel to minimize latency:

1. **Clari Call Intelligence**
   - `clari_search_calls` — find demo recording (last 24h, attendee email)
   - `clari_get_call_summary` — extract: key conversation points, objections raised, questions asked, action items discussed, buyer sentiment
   
2. **HubSpot Deal Context**
   - `hubspot_get_deal` — deal name, amount, stage, close date, notes, associated contacts
   - `hubspot_search_contacts` — all attendees + their titles, engagement score
   
3. **Calendar & Activity**
   - `get_upcoming_meetings` — check if next meeting already scheduled (next 30 days)
   - `ask_agent` — full activity timeline (calls, emails, notes) last 7 days for context
   
4. **Output:** Structured data object with demo metadata, attendees, deal stage, sentiment

### Stage 2: Demo Recap Email (Challenger-Style)
Generate Gmail draft with vertical-specific template:

**Email structure:**
- **Subject line:** "Quick recap: [Company] demo + next steps" or "Thoughts on [Product] for [Company]"
- **Opener (2 lines):** Gratitude + curiosity ("Thanks for your time on the call. A few thoughts from my side...")
- **Key takeaways (3 bullets max):** Use Challenger Sale "Teach" angle — one insight they may not have considered
- **Their action items:** Summarize what THEY committed to (review ROI, check with IT, etc.)
- **Our action items:** What YOU'RE doing (send case study, schedule follow-up, etc.)
- **Next step:** Specific date/time proposed ("Let's reconvene Tuesday at 2pm to discuss...")
- **Resource:** Vertical-specific (Higher Ed: CMS integration guide; Courts: compliance case study; Gov: security datasheet)

**Vertical-specific angles:**
- **Higher Ed:** CMS integration (Kaltura, Panopto, YuJa, Echo360, Opencast), faculty adoption, lecture capture ROI
- **Courts/Legal:** Courtroom recording compliance, evidence management, accessibility for remote proceedings
- **Government:** Security certifications, FISMA compliance, public records retention
- **Corporate AV:** Enterprise scalability, multi-room control, IT integration (Crestron, Extron comparison)
- **Healthcare:** HIPAA compliance, telemedicine recording, clinical documentation
- **Houses of Worship:** Live streaming, volunteer training, accessibility
- **K-12:** Teacher training efficiency, remote learning, parental engagement

**Tone:** Challenger-style (teach, don't regurgitate; position as peer advisor)

### Stage 3: Internal HubSpot Debrief Note
Create deal note with:

- **Demo outcome:** ✅ Positive / ⚠️ Mixed / ❌ Negative (inferred from sentiment + action items)
- **MEDDIC scorecard update:**
  - Metrics: Did they discuss ROI, budget constraints, or savings targets?
  - Economic buyer: Attended? Engaged? Or still hidden?
  - Decision criteria: What did they prioritize (ease of use, security, integration)?
  - Decision process: Is there a formal evaluation? Timeline? Competitive RFP?
  - Identified pain: What problem are we solving? Is it urgent?
  - Champion: Who's most enthusiastic? Who's skeptical?
- **Competitive intelligence:** Any competitor mentioned? (Extron, Blackmagic, Crestron, vMix, Teradek)
- **Next step:** Scheduled meeting date or "awaiting feedback on [topic]"
- **Confidence rating:** 1-10 based on engagement + MEDDIC health

**Flags (auto-surface to AE):**
- 🚩 No economic buyer attended
- 🚩 No next step agreed
- 🚩 Competitor mentioned
- 🚩 Objection raised but unresolved
- 🚩 Only 1 attendee (single-threaded)

### Stage 4: Next Meeting Scheduler
Conditional logic based on demo outcome:

**Scenario A: Next step agreed** (e.g., "Let's reconvene Tuesday")
- Extract date/time from Clari call or HubSpot notes
- `create_event` — calendar invite (attendees: all demo attendees + AE)
- Title: "[Company] - Follow-up: [Topic]" (e.g., "Acme - Follow-up: ROI Discussion")
- Description: Link to deal in HubSpot + key agenda items from demo

**Scenario B: No next step agreed, but demo was positive**
- Create Gmail draft: "Check-in" email (Day +3)
- Subject: "Any thoughts on the [Product] demo?"
- Tone: Light, non-pushy; offer to schedule a call if helpful

**Scenario C: Objection raised, unresolved**
- Create Gmail draft: "Objection response" email (Day +1)
- Use LAER framework (Listen, Ask, Explore, Respond)
- Example objection: "We're waiting to see if our Extron system can integrate"
- Response: Acknowledge → Ask timeline → Offer to loop in their IT → Share integration guide

**Scenario D: Demo was negative or attendees disengaged**
- Flag for AE review + create "recovery" email draft
- Propose alternate approach or deeper discovery call

### Stage 5: Stakeholder Expansion
If deal is single-threaded (only 1 attendee) OR only 1 attendee was truly engaged:

1. **Research via Apollo:**
   - Identify 2-3 likely stakeholders (CFO/VP Finance if budget/ROI discussed; IT Director if integration discussed; Operations if deployment discussed)
   - Pull titles, emails, LinkedIn profiles
   
2. **Create "loop-in" email draft:**
   - AE sends to champion, asking them to forward/introduce to stakeholder
   - Example: "Hey [Champion], I wanted to loop in [IT Director] since we discussed integrations — could you forward this to them?"
   - Includes short value prop + relevant resource (case study, demo video)
   
3. **LinkedIn outreach talking points:**
   - If champion can't loop them in, prepare LinkedIn request + message for AE
   - "I connected with [Champion] on the [Product] opportunity at [Company]..."

### Stage 6: 5-Touch Momentum Maintenance Sequence
Outline the follow-up cadence (AE decides execution method: Gmail scheduled send, BDR, or calendar reminders):

**Day 0:** Demo recap email (Stage 2 output) — sent within 2 hours

**Day 3:** Check-in email
- "Did you have a chance to review the [resource] I shared?"
- "Any questions on the [key takeaway] we discussed?"
- CTA: "Let's schedule 15 min if helpful"

**Day 7:** Value-add resource
- Send: relevant case study (similar company/vertical), ROI calculator, or peer reference
- Subject: "Thought you'd find this useful from [similar company]..."
- Position as "sharing what similar teams are doing" (Challenger angle)

**Day 14:** Escalation threshold
- If no response by Day 14: escalate to BDR (Tim Kipper)
- BDR emails champion or unknown stakeholders (if found in Stage 5)
- BDR may propose lower-touch option or alternative meeting format

**Escalation triggers:**
- No response after Day 14
- 2+ emails opened but no reply
- Deal stage hasn't advanced
- Competitor confirmed + no differentiation discussed

### Stage 7: Deal Stage Automation
Recommend HubSpot stage advances based on demo outcome + MEDDIC health:

**Successful demo** (positive sentiment + action items + next step agreed):
- Current stage: "Presentation Scheduled" → Recommend advance to: "Decision Maker Bought-In"
- Current stage: "Qualified Lead" → Recommend advance to: "Presentation Scheduled"
- Update properties:
  - `next_step`: [Date + topic of next meeting]
  - `last_demo_date`: [Today's date]
  - `demo_outcome`: "Positive"
  - `demo_attendee_count`: [Number]
  - `economic_buyer_attended`: Yes/No
  - `competitor_mentioned`: [Yes + name] or No

**Unsuccessful or mixed demo** (negative sentiment, objection unresolved, no next step):
- Flag for AE review; do NOT auto-advance
- Recommend recovery action: deeper discovery call, involve specialist, or escalate
- Update properties:
  - `demo_outcome`: "Mixed" or "Negative"
  - `unresolved_objections`: [List]
  - `next_action`: [Recovery recommendation]

**Special flags in HubSpot:**
- Add tag: #post-demo-[date]
- Add tag: #single-threaded (if Stage 5 triggered)
- Add tag: #competitor-[name] (if competitor mentioned in Stage 3)
- Add tag: #needs-follow-up-[date] (for Day 14 escalation threshold)

## Dependencies

### Required MCPs / Tools
- **Clari** (clari_search_calls, clari_get_call_summary) — extract demo recording + sentiment
- **HubSpot** (hubspot_get_deal, hubspot_search_contacts, deal updates) — deal context + contact research
- **Apollo** (for stakeholder expansion research)
- **Gmail** (gmail_create_draft) — compose recap email
- **Google Calendar** (create_event) — schedule next meeting
- **Epiphan CRM MCP** (activity_get_timeline, ask_agent) — full engagement history

### Related Skills (Integration Points)
- **meddic-call-prep-auto** — uses MEDDIC framework for Stage 3 scorecard
- **deal-momentum-analyzer** — references deal health scoring; can hand off high-risk deals
- **challenger-sale** — Teach-Tailor-Take Control framework for recap email (Stage 2)
- **never-split-the-difference** — objection response framing (Stage 4 Scenario C, LAER framework)
- **close-plan-generator** — updates close timeline based on Stage 7 deal stage advancement
- **ae-handoff-brief** — BDR can use for Day 14 escalation (Stage 6)

## Configuration & Customization

### Vertical-Specific Email Templates
Edit the vertical angle in Stage 2 for your use case:
- **Higher Ed:** Emphasize CMS integrations, faculty adoption ROI, lecture capture as institutional asset
- **Courts/Legal:** Highlight courtroom recording compliance, evidence chain-of-custody, remote accessibility
- **Government:** Lead with security (FISMA, FedRAMP), public records retention, audit trails
- **Corporate AV:** Focus on enterprise scalability, IT integration (Crestron/Extron comparison), multi-site rollout
- **Healthcare:** Emphasize HIPAA compliance, telemedicine use cases, clinical documentation efficiency
- **Houses of Worship:** Streaming reliability, volunteer onboarding, accessibility for members with disabilities
- **K-12:** Teacher efficiency, remote learning continuity, parental engagement through videos

### Objection Response Library
Customize LAER responses in Stage 4 Scenario C for common Epiphan objections:
- "We have Extron SMP" → Position Pearl as upgrade (SMP discontinued; Pearl has cloud, AI)
- "Blackmagic is cheaper" → Emphasize integration ecosystem + support
- "Crestron can do this" → Highlight simplicity, no programming required
- "We're evaluating multiple vendors" → Offer POC or ROI calculator

### Momentum Sequence Timing
Adjust Day 3, 7, 14 cadence in Stage 6 based on sales cycle length:
- **Fast cycle (K-12, small Corps):** Day 1, 3, 5, 10
- **Standard cycle (Higher Ed, Mid-market):** Day 0, 3, 7, 14 (default)
- **Long cycle (Gov, Enterprise):** Day 0, 5, 14, 30

## Example Workflows

### Example 1: Higher Ed Demo (Positive)
**Trigger:** "post-demo University of Michigan"

**Stage 1 output:**
- Clari: 45-min demo with CTO (IT), Director of Learning Tech (champion), 1 unknown attendee
- Sentiment: Positive; questions focused on integration timeline + Panopto sync
- HubSpot: Deal $85K, "Presentation Scheduled" stage, close date 60 days
- Calendar: No next meeting scheduled

**Stage 2 (Recap Email):**
- Subject: "Pearl + Panopto integration strategy for UMich"
- Opener: "Thanks for the thoughtful questions on Panopto sync..."
- Takeaway 1: "Pearl's direct API integration cuts transcoding time — your faculty time-to-publish drops from 4 hours to 15 min"
- Takeaway 2: "Kaltura + Echo360 customers report 40% higher lecture upload rate when encoding is automatic"
- Takeaway 3: "Deploy Pearl in one building, expand after faculty sees adoption gains"
- Action items: "You'll loop in IT for network feasibility; I'll send the Panopto integration roadmap"
- Next step: "Let's reconvene Thursday 2pm to discuss phased rollout"

**Stage 3 (HubSpot Note):**
- Outcome: ✅ Positive
- MEDDIC: Metrics (adoption %; time-to-publish), EB (CTO engaged, buying signal on timeline), Decision (Panopto as anchor, needs IT sign-off), Process (60-day eval window), Pain (faculty adoption friction)
- Confidence: 8/10
- Flags: None

**Stage 4:** Create calendar invite for Thursday 2pm

**Stage 5:** Research 1 more stakeholder (Provost for budget sign-off)

**Stage 6 momentum plan:** Day 0 (recap sent); Day 3 (Kaltura case study from similar university); Day 7 (POC timeline proposal); Day 14 (escalation if silent)

---

### Example 2: Corporate AV Demo (Mixed - Competitor Mentioned)
**Trigger:** "demo follow-up TechCorp headquarters"

**Stage 1 output:**
- Clari: 30-min demo with Facilities Manager (not EB), muted AV Integrator (skeptical), Finance passed
- Sentiment: Mixed; questions focused on cost comparison with Crestron
- HubSpot: Deal $150K, "Qualified Lead" stage, close date unknown
- Calendar: No next meeting scheduled

**Stage 2 (Recap Email):**
- Opener: "I caught some interesting pushback on Crestron — wanted to address that directly..."
- Takeaway 1: "Crestron is excellent; Pearl is complementary (no programming, plug-and-play for new campuses)"
- Takeaway 2: "Your AV integrator mentioned integration concerns — Pearl's REST API is documented; many integrators adopt it in 1 sprint"
- Next step: "Let's get your AV integrator and Finance on a 30-min tech deep-dive Thursday"

**Stage 3 (HubSpot Note):**
- Outcome: ⚠️ Mixed
- Flags: 🚩 EB (Finance) didn't attend, 🚩 AV Integrator skeptical, 🚩 Competitor mentioned (Crestron)
- Confidence: 5/10
- Recommendation: "Involve AV integrator in follow-up; offer tech POC to build confidence"

**Stage 4 Scenario C:** Create objection-response email (LAER framework)
- Listen: "I heard concerns about Crestron integration..."
- Ask: "How is your integrator currently handling multi-room control?"
- Explore: "What if integration took 2 weeks instead of months?"
- Respond: Offer tech deep-dive + share REST API docs + peer reference (corporate with similar Crestron setup)

**Stage 5:** Research AV Integrator + Finance owner; draft outreach to champion (Facilities Mgr)

**Stage 6:** Day 3 (AV integrator case study); Day 7 (REST API integration guide); Day 14 (escalate to Tim for BDR re-engagement with Finance)

---

### Example 3: Single-Threaded Demo (One Attendee)
**Trigger:** "post-demo Acme Corp"

**Stage 1 output:**
- Clari: 20-min demo with only one attendee (VP of Communications; technically an EB, but no IT/Finance present)
- HubSpot: Deal $60K, "Presentation Scheduled", close date 45 days
- Contact only: VP Comms; no IT, no Finance, no Ops

**Stage 5 (Stakeholder Expansion) triggered automatically:**
- Apollo research finds: IT Director, CFO, broadcast team lead
- Create draft email for VP Comms: "Could you loop in [IT Director] and [CFO]? I want to make sure we address integration + budget concerns..."
- Create LinkedIn outreach talking points for AE (if VP Comms can't loop them in)

**Stage 6 momentum:** Day 0 (recap to VP Comms); Day 5 (escalate to Tim to call IT Director cold); Day 10 (offer executive business review if VP Comms doesn't expand thread)

---

## Execution Checklist

Before triggering post-demo automation:
- [ ] Demo recording uploaded to Clari (automated if using Epiphan + Clari integration)
- [ ] Company name + attendee emails available (for Clari search)
- [ ] HubSpot deal exists and is linked to attendees (or AE provides deal name)
- [ ] Next step discussed in demo (optimal, but not required)
- [ ] AE has 5-10 min to review drafts before sending (all outputs are customizable drafts, not auto-sent)

After automation completes:
- [ ] Review recap email — customize tone if needed, add personal touch
- [ ] Review HubSpot note — confirm MEDDIC scorecard is accurate
- [ ] Confirm calendar invite (if next meeting scheduled)
- [ ] Review stakeholder list — add/remove based on your knowledge
- [ ] Confirm momentum sequence timing — adjust cadence if needed
- [ ] Send recap email within 2 hours of demo end
- [ ] Log HubSpot note within same day
- [ ] Schedule Day 3 check-in in calendar (as reminder, not attendee invite)

## Troubleshooting

**Problem:** "Clari recording not found"
- **Solution:** Ensure demo was recorded in Clari; check attendee email matches Clari profile. If still missing, manually summarize demo in your request ("demo with CTO and IT Director, discussed integration timeline + ROI").

**Problem:** "HubSpot deal not found"
- **Solution:** Provide company name; skill will search HubSpot. If multiple deals exist, specify which stage (e.g., "Acme deal in Qualified Lead stage").

**Problem:** "No next meeting scheduled — what do I propose?"
- **Solution:** Skill creates Day +3 check-in draft by default. If buyer seems cold, request "recovery email" variant (deeper discovery call or involve specialist).

**Problem:** "Stakeholder expansion returned nobody new"
- **Solution:** Manual Apollo search recommended. Add stakeholders to skill input, or reach out to Tim (BDR) for cold outreach support.

**Problem:** "I want to customize the vertical angle"
- **Solution:** Edit the "Vertical-Specific Email Templates" section above before triggering skill. Or mention your vertical in the request ("post-demo Acme [Higher Ed]") and skill will auto-select template.

## Advanced: Integration with Close Plan Generator

If using **close-plan-generator** skill:
1. After demo automation completes, trigger close plan with deal ID
2. Close plan uses MEDDIC scorecard (from Stage 3) + deal stage advancement (from Stage 7)
3. Close plan proposes milestones for Days 14, 30, 60 (aligns with momentum sequence)
4. AE updates HubSpot with close timeline; post-demo automation references it in Day 7 + Day 14 emails

## Notes for Tim Kipper (BDR)

When AE escalates deal on Day 14:
1. Check HubSpot note for flags (no EB, unresolved objections, competitor)
2. Request from AE: attendee list, demo outcome, objections, and stakeholder expansion results
3. BDR re-engagement strategies:
   - Call IT Director / CFO (if single-threaded)
   - Send peer reference (similar company, same vertical)
   - Propose lower-touch option (30-min async video demo vs. live call)
   - Loop in Epiphan product specialist if technical objections exist
4. Update HubSpot with BDR activity; hand back to AE once champion re-engaged

## Version History

- **v1.0** (April 2026): Initial release with 5-stage automation, vertical templates, MEDDIC integration
- Roadmap: Add Slack notifications for momentum sequence; auto-escalation to BDR calendar; A/B testing on email subject lines