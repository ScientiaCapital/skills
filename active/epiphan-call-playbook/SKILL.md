---
name: epiphan-call-playbook
description: Canonical Epiphan cold + discovery CALL playbook for Tim's BDR/SDR team (Tim, Edgar, Vasil). The phone-call sibling to sdr-email-sms-playbook. Covers the opener, the live discovery flow (Orlob-applied per vertical), objection handling, spec-accurate talking points by product, and the close/next-step. Every spec verified via Epiphan AI search_product_catalog / search_product_knowledge. Use when prepping or making cold calls, writing or reviewing call scripts, coaching reps, building dial-list talking points, or when the sdr-call-coaching task needs the canonical "what good sounds like" reference. Trigger on: call script, cold call, discovery call, opener, objection handling, talking points, what to say on the phone, dial list talking points, SDR coaching reference, Pearl/EC20/Nexus pitch on a call.
---

<objective>
Serve as the canonical reference for what a good Epiphan phone call sounds like, for Tim's BDR/SDR team (Tim, Edgar, Vasil). Covers the opener (permission-based / pattern-interrupt / trigger-based), the Challenger teach by vertical, the live Orlob 5-step discovery flow, objection handling (Voss labels + calibrated questions), the close/next-step, and a Verified Spec Bank of product/competitor facts confirmed via Epiphan AI. The sdr-dial-lists task sources talking points from here; the sdr-call-coaching task scores calls against the standards defined here.
</objective>

<quick_start>
**Trigger:** prepping or making cold calls, writing/reviewing call scripts, coaching reps, building dial-list talking points — "call script", "cold call", "discovery call", "opener", "objection handling", "talking points", "what to say on the phone".

**Call map:** OPEN (Section 1: audit/trigger, 1 sentence + question) → TEACH (Section 2: vertical-tailored Challenger insight) → DISCOVER (Section 3: problem → cause → impact → future state → MEDDIC woven in) → HANDLE objections (Section 4: label first, then teach) → CLOSE (Section 5: specific booked next step).

**Spec claims:** state only what's in the Verified Spec Bank (Section 6); anything else, verify live via `search_product_catalog` / `search_product_knowledge` before saying it.
</quick_start>

<success_criteria>
- Every product/competitor claim made on a call matches the Verified Spec Bank or was verified live first — zero confidently-stated wrong specs (the technical-accuracy gate is non-negotiable).
- Openers follow the coached rules: name + Epiphan in the first sentence, one sentence then a question, no "How are you today?".
- Discovery reaches a business problem / suffering metric and at least one root cause the buyer owns — not just a symptom.
- Every call closes to an explicit, specific next step (booked time via the discovery-call link), never "I'll send some info."
- Calls meet the 4-dimension coaching standard in Section 7 (discovery, opener + take control, spec accuracy, MEDDIC capture) that sdr-call-coaching scores against.
</success_criteria>

<core_content>

# Epiphan Call Playbook (v1, 2026-06-17)

The canonical reference for what a good Epiphan phone call sounds like. Sibling to `sdr-email-sms-playbook` (email/SMS) — this one is the PHONE. Use it to make calls, coach Edgar + Vasil, and source talking points for dial lists. The `sdr-call-coaching` task scores calls against the standards defined here.

## Non-negotiable: technical-accuracy gate
Every product/competitor claim in this playbook was verified via Epiphan AI on 2026-06-17. Before quoting any spec, price, or competitive claim that is NOT in the "Verified spec bank" below, look it up live (`search_product_catalog` for SKUs/pricing/short names, `search_product_knowledge` for technical/integration). A confidently-stated wrong spec on a real prospect call is the worst outcome — it costs credibility and the meeting. When unsure, say "let me confirm the exact number and send it right after this call." Zero tolerance for invented capabilities.

## Frameworks in play
- **Challenger** (Teach → Tailor → Take Control): lead with an insight that reframes their problem, tailor to their vertical, control the next step.
- **Never Split the Difference** (Voss): tactical empathy, labels ("It sounds like…"), calibrated questions ("How do you currently…?"), the accusation audit on a cold open.
- **Orlob 5-step discovery**: business problem → cause analysis → negative impact → future state → close. See `orlob-discovery-framework` + its `references/epiphan-root-causes.md` for the per-vertical root causes this playbook maps to.

---

# 1. The Opener (first 20 seconds)

Goal of the opener: earn the next 30 seconds. Not to pitch. A cold call is an interruption — name it, be human, give them a reason to stay.

## 1A. Permission-based opener (default cold open)
> "Hey [Name], it's Tim with Epiphan Video. I know I'm calling you out of the blue — can I take 30 seconds to tell you why, and you can tell me to buzz off if it's not relevant?"

Why it works: the accusation audit ("out of the blue," "tell me to buzz off") disarms the reflexive no. Almost everyone gives you the 30 seconds. Then you EARN the rest with a tailored teach (Section 2).

## 1B. Pattern-interrupt opener (for gatekept / senior titles)
> "Hi [Name], Tim at Epiphan. This is a sales call — but a quick and relevant one if you run video capture or streaming for [their org type]. Worth 30 seconds?"

Honesty as a pattern interrupt. Senior buyers respect that you didn't pretend.

## 1C. Trigger-based opener (registered device, ad click, event, survey)
> "Hi [Name], Tim with Epiphan. I'm reaching out because [specific trigger: your team registered a Pearl / you stopped by our InfoComm booth / you filled out our Higher Ed video survey]. Quick question while I have you…"

A real trigger beats any script. Always lead with the trigger when one exists (the morning brief and dial-list tasks surface these).

## Opener rules (coached)
- No "How are you today?" — it signals telemarketer. Go straight to the audit or trigger.
- Say your name and Epiphan in the first sentence. Never hide it.
- One sentence, then a question. Do not stack three sentences before you let them talk.
- Match pace and tone to how they pick up (mirror). If they're clipped, be clipped.

---

# 2. The Teach (Challenger insight — tailor by vertical)

After the opener earns attention, lead with an INSIGHT, not a feature. The cross-vertical insight that lands almost everywhere:

> "Most teams we talk to are still stitching together three or four tools — an encoder, a switcher, a separate recorder, a streaming box — to do what one Pearl handles out of the box. That stack is usually where the failures and the staffing cost come from."

Then tailor the teach to their world (one line, pick by vertical):
- **Higher Ed (ICP 90):** "On most campuses the real cost isn't the gear — it's that recording still needs an AV person physically in the room to press start, so faculty just stop recording."
- **Live Events / Production (85):** "The pattern we see is software encoders like vMix or OBS crashing under sustained load mid-event — and every event still needs a skilled operator on-site, which caps how many you can run at once."
- **Courts / Legal (85):** "The risk we see in courts is recording systems that fail silently — no alert, nobody notices until the record's already gone."
- **Government / Municipal (80):** "Most municipalities have streaming depend on one IT person being physically present for every public meeting — when they're out, the open-meeting compliance gap opens up."
- **Corporate AV (80):** "Usually IT is custom-configuring every single streaming request, and the security team blocks software encoders on the network — so each town hall becomes its own project."
- **Houses of Worship (70):** "It usually comes down to one volunteer who runs everything Sunday morning — when they don't show, the stream doesn't happen, and that's your homebound congregation and giving."
- **K-12 (65):** "The workflow's usually too many steps for a teacher to bother with, so the capture investment just sits idle."

This is the "tailor" — it proves you understand their problem before you've mentioned a product. Source the deeper root causes from `epiphan-root-causes.md`.

---

# 3. The Discovery Flow (Orlob, applied live)

The point of the call is the meeting, but the meeting gets booked because you found a real problem. Run this flow — it's not linear, follow what they give you.

## Step 1 — Business problem (the "forest fire" filter)
One open, calibrated question that surfaces a suffering metric:
> "How are you currently handling [capture / streaming / lecture capture] across your [rooms / venues / courtrooms] today?"
> "Where do you tend to lose the most time — capture, switching sources, or getting recordings out the door?" *(Tim's proven line, straight from the email playbook — works live too.)*

## Step 2 — Cause analysis (peel the onion)
Once they name a pain, find the root cause (what Epiphan actually fixes):
> "What's driving that?" / "How often does that happen?" / "When that breaks, who has to drop what they're doing?"
Targeted diagnostics by vertical live in `epiphan-root-causes.md` — use one, matched to what they said.

## Step 3 — Negative impact (quantify, build cost of inaction)
> "When a stream fails during a [game / hearing / service], what does that actually cost you — rescheduling, the client relationship, the staff hours?"
> "If a faculty member stops recording because it's too hard, how many students does that touch?"
Get a number or an implied number. This is what makes the AE call worth booking.

## Step 4 — Future state (only after pain is real)
> "If you could manage every encoder and camera across every site from one dashboard, instead of sending someone to each room — what would that change for your team?"
This plants the Edge/fleet vision without pitching specs.

## Step 5 — Calibrated qualifying (MEDDIC, woven in — never an interrogation)
- **Metric:** captured in Step 3.
- **Economic Buyer:** "Who else would weigh in on a decision like this besides you?"
- **Decision process:** "If you did want to move on something like this, what does that usually look like on your end?"
- **Pain + Champion:** you're talking to a potential champion — gauge their energy.
Capture what you get; don't force all six on a cold call. The AE finishes MEDDIC on the discovery call.

---

# 4. Objection Handling

Use a label or calibrated question first (Voss) — acknowledge before you answer. Never argue. All product facts below are in the Verified spec bank (Section 6).

## 4A. "We're not interested" / "Now's not a good time"
> "Totally fair, and I figured this might be a bad time. [accusation audit] Can I ask one quick thing so I don't waste a future call — are you even the person who'd own video capture if it came up?"
Either you disqualify cleanly or you get a thread. Don't cling.

## 4B. "We already use [vMix / OBS]"
> "Makes sense — a lot of teams start there. [label: it sounds like it's working for you so far.] The pattern we see is that software gets shaky under sustained load and ties you to an operator on-site. When you've had an event run long or scale up, how's that held up?"
Teach the failure mode; let them surface it. (Verify: vMix/OBS are software, Pearl is dedicated hardware — software-instability is the documented root cause.)

## 4C. "We already use Extron"
> "Good — so you know the value of doing this in hardware. Are you on the SMP line? Because Extron discontinued the SMP, so a lot of the campuses we work with are looking at what's next anyway." *(Verify SMP-discontinued status holds before stating; it's the current known status. Do not over-claim beyond it.)*

## 4D. "We don't have budget" / "Not this fiscal year"
> "Understood, and I'm not calling to push a PO this week. [label: sounds like timing's the real constraint, not the need.] When does your next budget cycle open — would it be worth me getting you the info now so you're ready when it does?"
Budget objection on a cold call is usually a timing signal. Convert to a future thread + a reason to take the AE meeting.

## 4E. "Just send me some info"
> "Happy to — and so I send the right thing instead of a brochure dump: are you more focused on capture, streaming, or managing gear across multiple rooms?"
Never just send info. Earn one qualifying answer first, then the info email (use the matching `sdr-email-sms-playbook` template).

## 4F. "How much does it cost?"
> "Fair question. It depends on the configuration and we work through certified AV integrators on pricing, so I don't want to quote you something off. The better use of five minutes is figuring out what you'd actually need — can I ask a couple quick questions?"
Deflect price to discovery + the integrator motion. Don't quote from memory. Pull live from `search_product_catalog` only if you commit to a number.

---

# 5. The Close (take control of the next step)

Always close to a specific next step — a booked time, not "I'll follow up." This is the #1 coached behavior.

## 5A. Direct meeting ask (default)
> "Here's what makes sense: let me get you 20 minutes with one of our solutions folks who can show you [the thing tied to their pain] and put an EC20 in your hands. Do you have time Thursday, or is early next week better?"
Two specific options beat "when are you free?"

## 5B. Calibrated close (if they're hedging)
> "What would have to be true for a 20-minute look to be worth your time?"
Let them tell you the condition, then meet it.

## 5C. Booking mechanics
- AE discovery call (Phil or Lex): https://meetings.hubspot.com/timkipper/discovery-call
- If they'll book live, send the link while on the phone and confirm the calendar invite before you hang up.
- Set the AE up: capture the pain + any MEDDIC in the notes so the `ae_handoff` is clean.

---

# 6. Verified Spec Bank (confirmed 2026-06-17 via Epiphan AI)

State these exactly. If a prospect pushes on a number not here, confirm live before answering.

## Pearl-2
- Up to **six simultaneous 1080p30 channels** for recording/streaming.
- Live switching across **up to five channels** (or a single 4K channel with the 4K add-on). *(Careful: capture/stream = up to 6, live-switch = up to 5. Don't conflate them — a technical buyer will catch it.)*
- Multi-streams to **50+ endpoints** simultaneously. Preconfigured Auto A / Auto B channels.
- Positioning: 6-channel, auditorium-size solution.

## Pearl Mini
- Record, switch, and stream simultaneously. No laptop needed.
- Positioning: portable streaming/recording solution.

## Pearl Nano
- Compact single-channel encoder. (Verify exact specs live before detailed claims.)

## Pearl Nexus
- **1RU rackmount** multi-channel encoder/streamer/recorder, **up to three 1080p30 channels**.
- Inputs: HDMI, SDI, RTSP, SRT, **NDI|HX only** (high-bandwidth NDI NOT supported — important, don't overstate NDI).
- Streams to **10–20 endpoints** simultaneously; up to 3 SRT streams; AES 128/192/256-bit encryption on SRT.
- Integrated with **Kaltura, Panopto, and YuJa** CMSs; registers as a video remote recorder for lecture capture + user auth.
- Positioning: best Pearl for Higher Ed lecture capture at campus scale.
- Warranty talking point: Pearl Nexus 3-year warranty promo — **confirm current terms/value via `search_product_catalog` before quoting** (the email playbook cites $999; verify it's current before you say a number on the phone).

## EC20 PTZ Camera
- 4K AI-tracking PTZ camera.
- **Panopto certified** with native Panopto Remote Recorder integration — records/streams **direct to Panopto with no separate encoder** (world's first Panopto-certified PTZ).
- Fleet-managed via **Epiphan Edge**: monitor health, update firmware, remote web access, managed alongside Pearls from one dashboard.
- Won **Best of Show at ISE 2026 (AV Technology)**. *(Not "Tech & Learning" — that was an earlier draft error.)*
- Differentiator vs Sony/Panasonic standalone PTZ: those need a dedicated PC at each location; EC20 is cloud-managed across sites.

## Epiphan Edge
- Cloud platform for fleet management of existing infrastructure — monitor, configure, control devices across sites from one dashboard.

## CMS integrations (verify per product)
- Panopto, Kaltura, YuJa, Echo360, Opencast.
## Protocols
- RTMP/S, SRT, HLS, NDI (NDI|HX on Nexus), RTSP.

## Competitive (confirm before stating)
- Extron SMP: discontinued (EOL, no upgrade path) — opening for "what's next."
- Matrox: exited the market.
- vMix / OBS: software encoders; documented failure mode is instability under sustained load + operator dependency + corporate-IT security friction.

---

# 7. What "good" sounds like (the coaching standard)

The `sdr-call-coaching` task scores connected calls on these four dimensions, 0–3. This is the bar:
1. **Discovery (Orlob):** reached a business problem / suffering metric and at least one root cause the buyer owns — not just a symptom.
2. **Opener + take control:** human, non-scripted opener that earned the next 30 seconds, AND an explicit specific next step (booked time, not "I'll send info").
3. **Spec accuracy:** every Epiphan/competitor claim correct per the Verified spec bank. Zero confident wrong specs.
4. **MEDDIC capture:** surfaced pain + at least one of Economic Buyer / Metric / Decision process.

Proven models from Tim's own calls (listen for these patterns): the **FreshAV / Daniel Burton** call (393s connect → Meeting Booked) and the **Carleton / Jeremy Whalen** call (74s → Meeting Booked) — tight opener, fast to a real problem, clean close to a booked time.

---

# 8. Quick-glance call map

OPEN (audit/trigger, 1 sentence + question) → TEACH (insight tailored to vertical) → DISCOVER (problem → cause → impact → future state) → HANDLE objections (label first, then teach) → CLOSE (specific booked next step). Keep talk-time balanced — if you're talking more than ~40% on a discovery call, ask another calibrated question.

</core_content>
