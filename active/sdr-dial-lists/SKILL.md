---
name: sdr-dial-lists
description: Daily SDR dial-list builder for Edgar Marroquin + Vasil Ivanov (Tim's SDRs). Builds each SDR their own ranked callable queue every weekday morning — HubSpot-owned contacts first, callback-owed prospects from Nooks, vertical-matched cold ATL/BTL — each row carrying spec-accurate talking points + calibrated discovery questions sourced from the epiphan-call-playbook skill. The dial-list sibling to Tim's morning-brief; same engine, run for the SDRs. Read-only except per-SDR Slack DM + an optional HTML/XLSX artifact. Use when the user says "build SDR dial lists", "Edgar's call list", "Vasil's dial queue", "feed the SDRs", "SDR morning queue".
---

<objective>
Build Edgar's and Vasil's daily dial queues every weekday morning (~7:30 AM CST, after Tim's morning-brief) — a ranked, vertical-segmented, callable queue per SDR: callback-owed Nooks prospects first, then HubSpot-owned ATL contacts, then top BTL/Champions, with vertical-matched greenfield fill when owned inventory is thin. Every row carries spec-accurate talking points + calibrated discovery questions sourced from the epiphan-call-playbook skill, so the SDRs walk in knowing exactly whom to call and what to say. Read-only everywhere except per-SDR Slack DMs + the local HTML/XLSX artifact.
</objective>

<quick_start>
**Trigger:** "build SDR dial lists", "Edgar's call list", "Vasil's dial queue", "feed the SDRs", "SDR morning queue" — or the weekday-morning scheduled run.

**Flow:** Gates (Nooks read-only, suppression, technical accuracy) → Step 1 pull each SDR's owned + callback inventory → Step 2 greenfield fill if thin → Step 3 rank (callbacks > ATL > BTL, ICP score DESC, cap ~40) → Step 4 attach playbook talking points + discovery questions → Step 5 deliver (HTML with Edgar/Vasil tabs, optional XLSX, Slack DM each SDR + team summary to Tim).

**Resources in this skill directory:**
- `reference/` — persona intel (`tim_persona_intel.md`, `ae_persona_intel.md`, `SOURCES.md`) for tone/voice and AE-routing context.
- `scripts/` — list-building helpers (`build_lists.py`, `build_deliverables.py`, `build_notes.py`, `data_raw.py`).
</quick_start>

<success_criteria>
- Both SDRs receive a ranked queue (cap ~40 rows each); Vasil's thin inventory is filled with labeled "ramping fill" greenfield — never an empty queue or RED.
- All gates enforced: Nooks read-only with USER_GOAL + per-call REASON; suppression gate applied (bdr_suppressed, do_not_call, hs_email_optout, AE-owned <90 days); every talking point spec-accurate per the epiphan-call-playbook Verified Spec Bank or live-verified.
- Every row has: rank, contact details + HubSpot deep link, tier badge, opener cue, teach line, 1-2 verified talking points, 2-3 calibrated discovery questions, existing-customer flag where applicable.
- Delivery complete: HTML artifact, per-SDR Slack DM, Tim's team-summary DM, 4-bullet run summary + GTME Lens.
- Only allowed writes performed: slack_send_message + local HTML/XLSX. No sequence or dialer pushes.
</success_criteria>

<core_content>

# SDR Dial Lists (v1, 2026-06-17)

Schedule: Mon-Fri ~7:30 AM CST (after Tim's 7:10 morning-brief). Automated run — Tim is NOT present. Execute autonomously; when in doubt, produce the lists. This builds Edgar's and Vasil's daily dial queues the same way Tim's morning-brief builds his — so the SDRs walk in with a ranked list and know exactly what to say on each call.

PURPOSE: Give each SDR a vertical-segmented, spec-accurate callable queue every morning, so they are interchangeable-by-vertical and ramp fast. Talking points + discovery questions come from the canonical `epiphan-call-playbook` skill (not invented per-run).

## Identifiers (verified 2026-06-17)
- Tim Kipper (Sr. BDR, owner of this report): HubSpot owner_id `87486452`; Slack DM `U0AAJUZH2PK`.
- Edgar Marroquin (SDR): HubSpot owner_id `93367782`; Nooks user `U2iWVwWG83OYhm3XR0mvGd9gWDV2`; email emarroquin@epiphan.com.
- Vasil Ivanov (SDR): HubSpot owner_id `93782443`; Nooks user `1BUM3d2fZuhsbFttl5UOKEOPuMG3`; email vivanov@epiphan.com. Onboarded 2026-06-11 — if he has few owned contacts, fill more of his queue from vertical-matched greenfield (see Step 2) and label it "ramping fill."
- HubSpot portal 21530819. Contact link: https://app.hubspot.com/contacts/21530819/contact/{contactId}.
- Slack DM targets: confirm each SDR's Slack user via slack_search_users by email at run time (do not hardcode SDR Slack IDs). Always also DM Tim (U0AAJUZH2PK) the team summary.

## Report window
Today = the day this fires (bash `date`). Build each SDR's queue for TODAY's dialing.

=== GATES (run before assembling any list) — identical discipline to Tim's morning-brief ===

NOOKS = READ-ONLY. Server `8c1d2738-2529-4248-b268-342859275d11`. Read tools only: listCalls, listTasks, listSequenceStates, listProspects, getMe. USER_GOAL="Build Edgar + Vasil daily dial lists" + per-call REASON on every Nooks call.

SUPPRESSION GATE: enforce the same lead-suppression rules as the morning brief — drop any contact where bdr_suppressed=true, do_not_call=true, hs_email_optout=true, or AE-owned <90 days. HubSpot is the single source of truth. (If a dedicated suppression spec/skill is installed, use it; else use the available HubSpot fields.)

TECHNICAL-ACCURACY GATE (non-negotiable): every talking point on every row must be spec-accurate. Source talking points + discovery questions from the `epiphan-call-playbook` skill, which is itself spec-verified. For any product/competitor claim NOT already in that playbook's Verified Spec Bank, verify live via `search_product_catalog` / `search_product_knowledge` before putting it on a row. Never invent specs. Zero tolerance.

Default to `Epiphan Ai` MCP namespace; fall back to `Epiphan CRM` only for tools present there.

=== STEP 1: PULL EACH SDR'S OWNED + CALLBACK INVENTORY ===
Run for Edgar, then Vasil.

A) HubSpot-owned callable contacts — `hubspot_search_contacts` with hubspot_owner_id={SDR owner_id}, filtered to callable lifecycle stages (lead, MQL, SQL, opportunity contact — not customer-closed, not suppressed). Capture: contactId, name, title, company, phone, email, vertical signal (email domain + company), hs_lead_status, last activity.

B) Nooks callback-owed prospects — listCalls filter_owner_id={SDR Nooks user id}, prior 3 business days, include=["prospect","callDisposition"]. Surface prospects with disposition "Follow Up (call back another day)", "Connected" (no meeting), or "Send Email". These rank ABOVE never-touched cold contacts. Capture prospect.crmId (→ HubSpot contact), name, account, call time, what was said if available.

=== STEP 2: FILL GAPS WITH VERTICAL-MATCHED GREENFIELD (if owned inventory is thin) ===
If an SDR's callable owned+callback inventory is < 25 for the day, fill up to ~40 total with vertical-matched cold contacts. Prefer the existing `vertical-list-builder` skill if installed (it already does HubSpot-first + Apollo greenfield + Clay phone enrichment + ATL/BTL classification per vertical). Otherwise pull cold ATL/BTL contacts from HubSpot in the SDR's assigned verticals. Label these rows "greenfield fill." For Vasil (ramping), lean more on this fill and bias toward higher-ICP verticals (Higher Ed 90, Live Events 85, Courts/Legal 85).

=== STEP 3: RANK EACH SDR'S QUEUE ===
Golden rules (same as morning-brief):
1. Callback-owed prospects first (a prospect spoken to who owes a callback outranks any cold ATL of the same vertical).
2. Then ATL (above-the-line decision-makers) by ICP vertical score.
3. Then top 2-3 BTL/Champions.
Sort within tiers by: ICP vertical score DESC (Higher Ed 90, Live Events 85, Courts/Legal 85, Government 80, Corporate AV 80, Healthcare 75, Houses of Worship 70, K-12 65), then recency of signal.
Cap at ~40 callable rows per SDR for the day.

=== STEP 4: ATTACH TALKING POINTS + DISCOVERY QUESTIONS (from the playbook) ===
For EACH row, pull from the `epiphan-call-playbook` skill, matched to the contact's vertical + role:
- OPENER cue: which opener fits (permission-based / pattern-interrupt / trigger-based if a trigger exists).
- TEACH: the 1-line vertical-tailored Challenger insight for that vertical.
- 1-2 SPEC-ACCURATE TALKING POINTS for that vertical/role (from the Verified Spec Bank — e.g. Higher Ed → Pearl Nexus 3-channel CMS-integrated lecture capture + EC20 Panopto-certified; Live Events → Pearl-2 6-channel + SRT/NDI reliability vs software encoders).
- 2-3 CALIBRATED DISCOVERY QUESTIONS for that vertical (from the playbook's discovery flow / orlob-discovery-framework).
- If the contact's company shows an existing Pearl/Cloud relationship (quick analytics_search_by_email or domain check), flag "existing customer — expansion angle, route to CSM/AE if hot," do not treat as cold.
All talking points must clear the technical-accuracy gate.

=== STEP 5: DELIVERY ===
1. ONE HTML file per run to ${CLAUDE_OUTPUTS_DIR:-./outputs/} named `sdr_dial_lists_<YYYY-MM-DD>.html` with two tabs: "Edgar" and "Vasil." Each row: rank, name, title, company, ICP vertical badge, phone (tel: click-to-call), email (mailto:), LinkedIn, HubSpot deep link, tier (Callback / ATL / BTL / Greenfield fill), opener cue, teach line, talking points, discovery questions, existing-customer flag. Present via mcp__cowork__present_files.
2. Optional XLSX (`sdr_dial_lists_<YYYY-MM-DD>.xlsx`, openpyxl, Arial, HubSpot-orange #FF7A59 header): Summary + Edgar + Vasil sheets, zero formula errors.
3. Slack DM to EACH SDR (resolve via slack_search_users by email): "Morning [Name] — your dial queue is ready: N calls today, top vertical [X]. Top 3: [name/company/one-line why]. Full list + talking points in the attached HTML." Keep it short, bullet format.
4. Slack DM to Tim (U0AAJUZH2PK): team one-liner — Edgar N calls / Vasil N calls, callback-owed counts, any thin-inventory or ramping-fill flags, link to the HTML.
5. End the chat run with a 4-bullet summary + a one-line GTME Lens (GTM Motion: keeps both SDRs in front of qualified, vertical-matched buyers daily → more demos to Phil/Lex; Operational Leverage: eliminates each SDR hand-building their own list every morning and guarantees spec-accurate talking points, cutting ramp time and making reps interchangeable by vertical).

WRITE actions allowed: ONLY slack_send_message (Slack) + writing the local HTML/XLSX. Everything else (Nooks, HubSpot/Epiphan CRM, search_product_*, analytics) is READ-ONLY. This task does NOT push to sequences or dialers — it produces the queue + talking points; the SDRs dial from Nooks.

=== EDGE CASES ===
- Vasil thin/zero owned inventory → fill from greenfield, label "ramping fill," never render an empty queue or RED.
- A referenced skill (vertical-list-builder, epiphan-call-playbook, suppression spec) not installed this run → note the gap in output, fall back to HubSpot-direct pulls + live spec verification, continue.
- If owned inventory is large, still cap at ~40 and note how many were held back.
- Weekend/holiday fire → if no business day, post a short "no dialing day" note and skip.

</core_content>
