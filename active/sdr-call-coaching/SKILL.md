---
name: sdr-call-coaching
description: Weekly SDR call-coaching loop for Tim (Sr. BDR coaching Edgar Marroquin + Vasil Ivanov). Pulls each SDR's real connected Nooks dials (recordingUrl) + external Clari calls from the report week, scores every coachable call against a 4-dimension rubric (Orlob discovery, opener + take-control, Epiphan spec accuracy, MEDDIC capture), and outputs a per-SDR coaching card (score, 2 wins, 2 fixes, verbatim quotes, recording links) + a team trend. Read-only everywhere except the final Slack DM to Tim and an optional coaching-notes Gmail draft. Built to run Friday ~11 AM CST so Tim reviews before the 5:30 PM KPI report.
---

<objective>
Run Tim's weekly SDR call-coaching loop (Fridays ~11 AM CST, before the 5:30 PM KPI report): pull each SDR's real connected Nooks dials (recordingUrl required) + external Clari calls for the report week, score every coachable call 0-3 on four equally-weighted dimensions (Orlob discovery, opener + take-control, Epiphan spec accuracy, MEDDIC capture), and hand Tim a per-SDR coaching card — composite score, 2 wins, 2 fixes with verbatim quotes, one drill, recording links — plus a week-over-week trend and team roll-up. This task COACHES (qualitative); the weekly KPI report MEASURES. Read-only everywhere except the Slack DM to Tim + optional Gmail draft.
</objective>

<quick_start>
**Trigger:** "SDR call coaching", "coaching cards", "score SDR calls", "review Edgar's/Vasil's calls" — or the Friday ~11 AM CST scheduled run.

**Flow:** Gates (Nooks + Clari read-only, technical-accuracy, privacy/scope) → Step 1 pull coachable calls per SDR (Nooks connects >=30s with recording; Clari external-only) → Step 2 score each deep-scored call on the 4-dimension rubric (cap 6 per SDR) → Step 3 build per-SDR coaching cards (2 wins, 2 fixes, spec correction, drill, best-call callout) → Step 4 week-over-week trend via outputs/sdr_coaching_prev.json → Step 5 team roll-up → deliver (HTML, Gmail draft to Tim, Slack DM to Tim).
</quick_start>

<success_criteria>
- Every deep-scored call has four 0-3 scores with one-line justifications + short verbatim quotes; composite normalized 0-100 with GREEN/YELLOW/RED badge; spec-accuracy 0-1 force-flags "SPEC FIX".
- Spec claims judged only against live-verified facts (search_product_catalog / search_product_knowledge); unverifiable moments marked "unverified — flag for Tim," never called errors.
- Each SDR card has: header stats + trend arrow, per-call rows with recording links, TOP 2 WINS + TOP 2 FIXES with quotes, one spec correction if any, ONE DRILL, best-call callout, live-review candidates.
- Vasil zero-coachable weeks render "NEW · ramping" — never zeros or RED; holiday weeks post a short no-connects DM and skip the draft.
- Privacy held: output goes only to Tim (Slack DM + Gmail draft); nothing sent to SDRs, Victor, HubSpot, or prospects. Only allowed writes: create_draft, slack_send_message, local HTML + sdr_coaching_prev.json.
</success_criteria>

<core_content>

# SDR Call-Coaching Loop (v1, 2026-06-17)

Schedule: Fridays ~11:00 AM CST. Automated run — Tim is NOT present. Execute autonomously, make reasonable choices, note them in the output. When in doubt, produce the coaching cards. This task COACHES the SDRs; the weekly-kpi-report MEASURES them. Do not duplicate the scorecard math here — this is qualitative call review.

PURPOSE: Transfer Tim's calling skill to the new SDRs by scoring their actual recorded calls the way Tim would, every week, and handing each SDR 2 wins + 2 fixes grounded in their own verbatim quotes.

## Identifiers (verified 2026-06-17)
- Tim Kipper (Sr. BDR, reviewer): HubSpot owner_id `87486452`; Nooks user `UdhD9yeRfOXij75iD0Oy9F1b25P2`; Slack DM `U0AAJUZH2PK`; email tkipper@epiphan.com.
- Edgar Marroquin (SDR): HubSpot owner_id `93367782`; Nooks user `U2iWVwWG83OYhm3XR0mvGd9gWDV2`; email emarroquin@epiphan.com.
- Vasil Ivanov (SDR): HubSpot owner_id `93782443`; Nooks user `1BUM3d2fZuhsbFttl5UOKEOPuMG3`; email vivanov@epiphan.com. Onboarded 2026-06-11 — likely few/no connected calls early. If zero coachable calls, render "NEW · ramping — no coachable calls this week," NOT zeros or RED.
- HubSpot portal 21530819. Contact link: https://app.hubspot.com/contacts/21530819/contact/{contactId} (Nooks prospect.crmId = HubSpot contact_id).

## Report window
Monday 00:00 to Friday 23:59 America/Chicago of the current week. Compute dynamically via bash `date` — never hardcode dates. Coaching covers Mon-Fri of THIS week.

=== GATES (run before producing any card) ===

NOOKS = READ-ONLY. Nooks MCP server id `8c1d2738-2529-4248-b268-342859275d11`. Use ONLY read tools: listCalls, getCall, listCallDispositions, listProspects, getMe. Do NOT call any Nooks write tool. Every Nooks call needs USER_GOAL="Generate Tim's weekly SDR call-coaching cards" plus a per-call REASON.

CLARI = READ-ONLY. Use clari_search_calls + clari_get_call (Epiphan AI MCP). No writes.

TECHNICAL-ACCURACY GATE (non-negotiable): the rubric scores whether the SDR stated Epiphan specs correctly. To judge that, YOU must know the correct spec. Before flagging any spec as right or wrong, verify it live via Epiphan AI `search_product_catalog` (short product names: Pearl-2, Pearl Mini, Pearl Nano, Pearl Nexus, EC20 PTZ, Epiphan Connect, Unify, Edge) or `search_product_knowledge` (integration/topic: Panopto, Kaltura, YuJa, Echo360, Opencast, RTMP/S, SRT, HLS, NDI, RTSP). Confirm competitor claims before scoring them (Extron SMP discontinued; Matrox exited the market). Never assert a spec from memory in a coaching note. If you cannot verify, mark the spec moment "unverified — flag for Tim to confirm," do not call it an error.

PRIVACY/SCOPE GATE: This is internal coaching for Tim only. Do not send anything to the SDRs directly, to Victor, to HubSpot, or to the prospect. Output goes to Tim's Slack DM + an optional Gmail draft addressed to Tim.

Default to `Epiphan Ai` MCP namespace; fall back to `Epiphan CRM` only for tools present there.

=== STEP 1: PULL COACHABLE CALLS PER SDR ===

Run the SAME logic for Edgar then Vasil.

SOURCE A — Nooks connected dials (PRIMARY for cold-call coaching).
- listCalls: filter_owner_id={SDR Nooks user id}, filter_time_gte/filter_time_lte bounding the report week, include=["prospect","callDisposition"], page_size=50, page via links.next until exhausted.
- A call is COACHABLE only if it cleared a human conversation. Keep a call when ALL of:
  a) callDisposition.callOutcome IN ("Connect","Meeting") — i.e. disposition name in {Connected, Follow Up (call back another day), Meeting Booked, No Interest, Using Competitor, Referral, Send Email}. Drop No Answer / Left voicemail / Left live message / Busy / Wrong number / No Longer at Company.
  b) duration >= 30 seconds (a real exchange, not a 4-second pickup-hangup).
  c) recordingUrl is non-null (must be reviewable). If a Connect has duration>=30 but recordingUrl is null, list it in a "Connected but no recording — disposition/recording hygiene" line, do NOT score it.
- For each coachable call capture: call id, prospect name/title/account, prospect.crmId (→ HubSpot link), email domain (vertical signal), disposition name, duration, recordingUrl, time.
- Known disposition ids: Connected `14a81f79-6d14-4b37-9277-e2ae88618aca`; Follow Up `6155389e-9bc2-4c99-8218-dc95561de424`; Meeting Booked `c1210028-7405-4f1e-81f0-90bbf1921c53`. Use live names only; never invent.

SOURCE B — Clari external calls (for longer discovery/demo conversations).
- clari_search_calls: repEmail={SDR email}, daysBack=10, limit=50.
- KEEP ONLY calls with a genuine external prospect: at least one address in `participants[]` whose domain is NOT @epiphan.com. DROP every internal call (BDR/SDR Sync, Reinforcement Session, Sales Marketing Monthly, any all-@epiphan.com roster). This filter is mandatory — Clari records internal Zoom meetings and scoring those is worthless.
- For each surviving call: clari_get_call with includeTranscript=true. Capture summary, transcript, participants, review_url (https://copilot.clari.com/call/{id}).

Note on volume: Nooks cold dials and Clari external calls measure different surfaces. A cold-call week may have many Nooks coachable calls and zero Clari externals — that is normal, present it as such.

Per-SDR coachable inventory = Source A (scored individually) + Source B (scored individually). Cap deep transcript scoring at the 6 highest-value calls per SDR (rank: Meeting Booked > longest Connect/Follow-Up > others). List the rest as "additional connects (not deep-scored)" with links so Tim can spot-check.

=== STEP 2: SCORE EACH CALL — THE RUBRIC ===

For each deep-scored call, fetch the recording/transcript and score the FOUR dimensions 0-3. Weight all four equally (Tim's choice). If a call is a pure cold-open that never reached discovery (e.g. a 35-second "not interested" hang), score what applies and mark the rest "n/a — call ended early," do not penalize discovery on a call that never got there.

For each dimension, give a 0-3 score AND a one-line justification with a SHORT verbatim quote from the call (≤15 words). Quotes make the coaching real — always include at least one quote per win and per fix.

Dimension 1 — DISCOVERY QUALITY (Orlob). Reference Skill: orlob-discovery-framework (and references/epiphan-root-causes.md for the SDR's vertical). Score:
- 3 = peeled past surface to a business problem / suffering metric, asked calibrated/open diagnostic questions, surfaced a root cause the buyer owns.
- 2 = asked good open questions but stayed at symptom level, no metric.
- 1 = mostly pitched, one token question.
- 0 = pure feature dump, no discovery.
Coaching tie-in: name the specific Orlob move they missed (e.g. "cause analysis — never asked what's driving the AV-staffing crunch").

Dimension 2 — OPENER + TAKE CONTROL (Challenger + Never Split the Difference). Reference Skills: challenger-sale, never-split-the-difference. Score:
- 3 = human, non-scripted opener that earned the next 30 seconds (pattern interrupt / label / honest "cold call" framing), and the SDR explicitly controlled the next step (booked time or a clear specific follow-up).
- 2 = decent opener OR clear next step, not both.
- 1 = robotic/AI-sounding opener, vague next step ("I'll send some info").
- 0 = no opener structure, prospect drove the whole call, no next step.
Coaching tie-in: quote the opener verbatim; if weak, give Tim a one-line rewrite suggestion in the SDR's words.

Dimension 3 — SPEC ACCURACY (Epiphan technical correctness). Clears the TECHNICAL-ACCURACY GATE. Score:
- 3 = every Epiphan/competitor claim stated correctly (verify each via search_product_catalog / search_product_knowledge).
- 2 = mostly correct, one vague-but-not-wrong claim.
- 1 = one clear factual error (wrong spec, wrong integration, stale competitor claim).
- 0 = multiple spec errors or invented capabilities.
- n/a = no product/spec claims made on the call.
Coaching tie-in: for any error, state the WRONG thing the SDR said + the VERIFIED correct fact (with the product name you looked up). This is the highest-stakes dimension — a confidently-stated wrong spec on a real prospect call must always surface.

Dimension 4 — MEDDIC CAPTURE. Did the SDR surface any of: Metric, Economic Buyer (or a path to them), Decision Criteria, Decision Process, Identify Pain, Champion? Score:
- 3 = captured 3+ MEDDIC elements, including pain + a buyer/champion thread.
- 2 = captured pain + one other element.
- 1 = pain only, or one element.
- 0 = none.
Coaching tie-in: name the single highest-value MEDDIC element they could have gotten and didn't (usually Economic Buyer or a quantified Metric).

Per-call composite = sum of the applicable dimensions, normalized to a 0-100 scale (sum / (3 × number_of_applicable_dimensions) × 100). Badge: GREEN >=70, YELLOW 45-69, RED <45. A spec-accuracy score of 0 or 1 force-flags the call as "SPEC FIX" regardless of composite.

=== STEP 3: BUILD THE PER-SDR COACHING CARD ===

For each SDR, produce a card with:
- Header: SDR name · # coachable calls this week (Nooks connects / Clari externals) · # deep-scored · week's avg composite + trend arrow vs last week (see Step 4).
- Per deep-scored call, a compact row: Prospect (HubSpot link) | Account + vertical | Disposition | Duration | the four 0-3 scores | composite badge | recording link (Nooks .wav or Clari review_url).
- THE COACHING SUMMARY (the point of the whole task): per SDR, synthesize across their calls:
  - TOP 2 WINS — what they did well this week, each with a verbatim quote + which call.
  - TOP 2 FIXES — the two highest-leverage things to change next week, each with: the pattern, a verbatim quote showing it, and a concrete "try this instead" in plain language (think like an electrical engineer explaining to a high-schooler — signal-flow analogy or before/after line where it helps).
  - ONE SPEC CORRECTION if any spec error surfaced this week (verified fact).
  - ONE DRILL — a single rep-able exercise for the week (e.g. "On every connect, ask one calibrated 'how do you currently handle...' before mentioning Pearl").
- BEST CALL OF THE WEEK callout (highest composite) — Tim can share it as a positive model.
- Coaching candidates for live review: the 1-2 calls Tim should actually listen to (longest Connect/Follow-Up or any Meeting Booked), with direct recording links.

Edgar example anchor (real, week of Jun 8): the Adrian Bisek / SFU thread — a 502s connect → callback, then 175s → Meeting Booked — is exactly the kind of discovery-to-demo sequence to surface and score as a model if it recurs.

=== STEP 4: WEEK-OVER-WEEK TREND ===
- Read prior week's per-SDR composite + fix list from outputs/sdr_coaching_prev.json if present.
- Compute trend arrow per SDR (↑/↓/→ vs last week's avg composite). Note whether last week's FIXES improved (did the pattern recur?). "Last week's fix was X — this week it recurred on N calls / improved" is the single most valuable coaching line; always include it when a prior file exists.
- Overwrite outputs/sdr_coaching_prev.json with this week's per-SDR avg composite + the two fixes, so next week can check follow-through.

=== STEP 5: TEAM ROLL-UP ===
- Edgar vs Vasil side-by-side: coachable-call counts, avg composite, common fix theme.
- Team-level pattern: the ONE thing both SDRs (or the team) should drill next week.
- If Vasil is still ramping, frame his section as developmental, not comparative.

=== DELIVERY ===
1. Single HTML report saved to ${CLAUDE_OUTPUTS_DIR:-./outputs/} named `sdr_coaching_cards_<YYYY-MM-DD>.html`: per-SDR cards, color-coded badges, embedded recording links, team roll-up. Present via mcp__cowork__present_files.
2. Gmail DRAFT to tkipper@epiphan.com (create_draft), subject "SDR Coaching Cards — week of [Mon date]", full HTML as body. Draft only — Tim decides what to share with each SDR.
3. Slack DM to Tim U0AAJUZH2PK (slack_send_message), bullet format (Tim's preference): per-SDR one-liner (X coachable calls, avg composite + trend, the #1 fix), any SPEC FIX flag (always surface these), the team drill, and a link line "Full cards + recordings in the email draft + HTML." If a SPEC FIX exists, lead with it.
4. End the chat run with a 4-bullet summary + a one-line GTME Lens (GTM Motion: ramps SDRs faster → more qualified demos to Phil/Lex; Operational Leverage: replaces ad-hoc manual call review with a weekly automated coaching pass, cutting Tim's review time and standardizing "what good sounds like" across interchangeable SDRs).

WRITE actions allowed this run: ONLY create_draft (Gmail) and slack_send_message (Slack) and writing the local HTML + sdr_coaching_prev.json. Everything else (Nooks, Clari, Epiphan CRM/ask_agent, search_product_*) is READ-ONLY.

=== EDGE CASES ===
- Vasil zero coachable calls → "NEW · ramping" card, no badge, no RED; still produce Edgar's card.
- Both SDRs zero coachable calls (holiday week) → post a short "no coachable connects this week" Slack DM + skip the email draft.
- A Clari call that is borderline internal/external (e.g. a partner @reseller.com) → keep it, label "partner call," score opener+control + spec, mark discovery/MEDDIC n/a if not a prospect.
- Recording URL present but transcript/audio unfetchable → score from the Clari summary + disposition context, label "scored from summary (audio unavailable)."
- If clari_get_call transcript is very large, summarize-as-you-go; do not dump full transcripts into the report.

</core_content>
