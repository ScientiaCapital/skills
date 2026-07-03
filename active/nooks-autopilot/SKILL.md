---
name: "nooks-autopilot"
description: "Autonomous BDR/SDR team that hunts leads to a warm reply. Sources from HubSpot [AI] lists, qualifies (Golden Rules + Suppression + ATL/BTL + persona match), routes each lead to the right Nooks sequence by play, and (shadow-first) enrolls + monitors for replies to hand Tim a warm contact. Use when: 'run nooks autopilot', 'autonomous BDR run', 'hunt leads', 'enroll into nooks sequences', 'shadow enroll', 'autopilot dry run', 'check for replies / warm handoffs'."
schedule: "0 5 8 * * 1-5"
timezone: "America/New_York"
---

# Nooks Autopilot — Autonomous BDR/SDR Team

<objective>
Find, hunt, and "almost kill" leads automatically, then hand Tim a warm one. Pull prospects
from the curated HubSpot `[AI]` lists, qualify and persona-match them, route each to the
right **Nooks** sequence by play, and enroll them so Nooks runs the multi-touch cadence
(auto-emails fire; calls + LinkedIn become the owning rep's task list). Monitor enrolled
prospects and, the moment one replies, halt the sequence and surface the warm contact to its owner.

**Per-rep agents.** This runs as a dedicated agent for **each dialing rep** (Tim + the 3 SDRs).
Each rep's run works only that rep's owned leads and produces their **next-best top 5 to call**.
**One owner per lead, no double-dialing:** every worked lead is owned by exactly one rep; a lead
is never enrolled twice or placed in two reps' queues. Unowned source-list leads are assigned to
exactly one rep (whole account → one rep, to keep multi-threading clean) before anything else.

**SHADOW MODE is the default and is ON unless explicitly turned off.** In shadow mode the
skill does everything *except* write to Nooks/HubSpot — it produces an enrollment **plan +
report** so Tim can verify behavior on real leads before a single sequence starts.
</objective>

<quick_start>
**Scheduled:** Weekdays ~8:05 AM ET (after `morning-brief`). **Monitor pass:** also run on each invocation.
**Manual triggers:** "run nooks autopilot", "autopilot shadow run on Live Events list", "check nooks replies / warm handoffs"
**Default mode:** SHADOW (plan + report only, zero writes). Flip with `SHADOW_MODE=false` (Tim only).
**Dependencies:** Epiphan AI + HubSpot + Nooks MCP connectors; `nooks-personas-v2` / `nooks-signals-v1` / `nooks-battlecards-v3` in `reference/`; reuses `sequence-load`, `prospect-research-to-cadence`, `prospect-enrich` patterns.
**Output:** enrollment-plan HTML report + outcome sidecar JSON; in live mode, Nooks enrollments + HubSpot state + warm-handoff tasks.
</quick_start>

<config>
## Locked configuration

**SHADOW_MODE:** `true` (master switch — no Nooks/HubSpot writes while true)
**DAILY_ENROLL_CAP:** 25 (throttle once live; protects deliverability)
**ENROLLMENT GATE (auto):** persona ∈ focus verticals **AND** `power_level == atl` **AND** not junk
**AND** survived Golden Rules / Suppression / dedup. The `qualify_lead` CatBoost **category is NOT a gate**
— it's a *ranking* input (a focus-vertical ATL with a "why now" signal still enrolls even if category=`nurture`;
the classifier under-rates Live Events). GRAY power → hold for Tim's ok; BTL → skip auto-enroll.
**TOP_N_PER_REP:** 5 (each rep's "next best to call" queue size)

**Dialing reps (one owner per lead; Nooks `crmId` == HubSpot `ownerId`; mailbox = auto-email send-as):**
| Rep | Role | HubSpot ownerId / `sdr_owner` | Nooks userId (enroll `owner.id`) | Nooks mailbox id |
|-----|------|------------------------------|----------------------------------|------------------|
| Tim Kipper | Sr. BDR | 87486452 | UdhD9yeRfOXij75iD0Oy9F1b25P2 | ac39509a-8903-480b-a11d-2626a9164086 |
| Edgar Marroquin | SDR | 93367782 | U2iWVwWG83OYhm3XR0mvGd9gWDV2 | c33b9127-762c-401c-ab2f-11bec60485d5 |
| Vasil Ivanov | SDR | 93782443 | 1BUM3d2fZuhsbFttl5UOKEOPuMG3 | e86728fe-1d12-424d-a1ad-7f96d3c4f123 |
| Nyasha Chigwedere | SDR | 94135434 | LGCdlTv6v8dSAiSsoJ7ETWQHVKl1 | ⚠️ none yet — enroll call/LinkedIn-only or hold auto-email until her mailbox is connected |

(Victor Doubrovine — manager, ownerId 153471050 / Nooks D9DElZ5… — is NOT a dialing rep; never assign to him.)

**Ownership key = `sdr_owner`** (HubSpot enum of owner-ids; Victor enabled it and it **translates into
Nooks** as the dial owner). This — NOT `hubspot_owner_id` (often the AE) — is the per-rep ownership field.
A lead "belongs to" the rep in its `sdr_owner`.

**Assignment strategy:** assign by **account** (all of an account's contacts → one rep) to prevent two
reps working the same org and to keep multi-threading owned by one rep. New `sdr_owner`-unset accounts →
round-robin/load-balanced across the 4 reps; if any contact at the account already has an `sdr_owner`,
assign the rest to that same rep. Never overwrite an existing `sdr_owner`. Set `sdr_owner` (live) via
`hubspot_update_contact` — it propagates to Nooks as the owner.

**Focus verticals (v1):** Higher Ed, Community College, Live Events, Corporate. Other personas stay matchable but are deprioritized.

**Source lists (HubSpot) → play:**
| listId | name | play |
|--------|------|------|
| 2618 | `[Leads] Send to AI` | generic (route by persona/vertical) |
| 4807 | `[AI] SDR EDU Hit List` | Higher Ed / Community College |
| 4808 | `[AI] SDR Live Events Hit List` | Live Events |
| 4809 | `[AI] Greenfield HE` | Higher Ed |
| 4810 | `[AI] Greenfield LE` | Live Events |

**State lists (HubSpot, DYNAMIC) — driven by the `epiphan_ai_status` contact property (enum):**
| status value | list |
|---|---|
| `enrolled` | `[Epiphan AI] Enrolled` 4575 |
| `sent` | `[Epiphan AI] Email Sent` 4578 |
| `replied` | `[Epiphan AI] Replied` 4576 (warm) |
| `completed` | (cadence ran out, no reply) |
| `skipped_*` (in_deal, exclusion_list, already_enrolled, safeguard_90d, unreachable, …) | `[Epiphan AI] Blocked` 4577 / suppressed |

**To reflect state:** write `epiphan_ai_status` on the contact (do NOT edit the dynamic list). Related
mirror props: `nooks_active_in_sequence` (bool — double-dial guard), `nooks_sequenced_by` (owning rep),
`nooks_current_sequence_name`, `nooks_current_sequence_step`, `epiphan_ai_last_email_at`.

**Warm signals (Stage 7):** `epiphan_ai_status == replied` (list 4576) OR a Nooks call disposition of
**Meeting Booked** / **Connected** / **Referral**. (Negative: No Interest, No Longer at Company, Wrong number.)

**Routing → Nooks sequence id:**
| play / signal | Nooks sequence | id |
|---|---|---|
| Live Events (4808), Greenfield LE (4810) | Live Events Follow-up | `002d69b2-88c0-400b-a8a0-47164c3e8da8` |
| EDU (4807), Greenfield HE (4809), generic (2618) | General Prospecting | `c22af5df-d130-4311-a168-68078641f47c` |
| job-change signal detected | Job Promotion | `4473cb2f-1a70-498f-9683-74d5daae386e` |
| prior deal lost ~6 months ago | 6-month lost-deal | `af4ad19e-7b4a-4fe9-8911-d989b88a48b7` |

Default when ambiguous → General Prospecting. Signals (job-change, lost-deal) override the list→play default.
</config>

<success_criteria>
- [ ] Read source-list members via `hubspot_list_members` for the configured lists; tag each lead with its source-list play
- [ ] Apply Golden Rules + Suppression Gate; dedup vs `[Epiphan AI] Enrolled` (4575) and `[Epiphan AI] Blocked` (4577)
- [ ] **No double-dial:** exclude any lead already owned by another rep, already `active` in ANY rep's Nooks sequence, or already enrolled. Assign unowned accounts to exactly one rep
- [ ] **One SDR per account:** every contact at an account shares one `sdr_owner`; multi-thread contacts attach to that same rep; flag/consolidate `SPLIT ACCOUNT` conflicts
- [ ] **Per-rep:** produce each rep's next-best **TOP_N_PER_REP** (5) leads to call, from their owned + newly-assigned leads only
- [ ] `qualify_lead` each survivor (category, `power_level` ATL/BTL, region, junk); persona-match to a vertical persona; apply Tim's win-pattern weighting; detect "why now" signal
- [ ] Route each ATL lead to a Nooks sequence id (table above); record the routing reason
- [ ] **SHADOW:** produce the enrollment-plan report; make ZERO Nooks/HubSpot writes. **LIVE:** sync/create Nooks prospect, `createSequenceState`, set `[Epiphan AI] Enrolled`
- [ ] Multi-thread flag: per account, if no Manager/Director-level contact present, flag the missing economic buyer
- [ ] Monitor pass: detect replies on enrolled prospects → `finishSequenceState` → `[Epiphan AI] Replied` + notify Tim
- [ ] Write outcome sidecar JSON
</success_criteria>

<workflow>

## Stage 1 — Source
For each configured source list, call `hubspot_list_members(listId, gapsOnly:false)`. Capture
name, email, jobtitle, company, phone, contactId, plus the per-member gap flags. Tag each
lead with its **play** (from the Source-lists table). Cap the run at `DAILY_ENROLL_CAP` candidates
(highest-intent lists first: Hit Lists → Greenfield → Send-to-AI).

## Stage 2 — Filter (reuse existing logic)
Apply, in order — these mirror `sequence-load` Stage 3 + `prospect-research-to-cadence` Stage 1b:
- **Golden Rules:** skip customers, channel partners, device-owners, contacts owned by active AEs
  (<90 days), and NEVER-ATL titles (Warehouse/Network Manager, Systems Admin, AV Technician,
  Classroom Support, Lab Coordinator, Multimedia Services Manager, Video Production Specialist, etc.).
- **Suppression Gate:** exclude where `bdr_suppression_until` is set and > today.
- **Dedup:** drop anyone already in `[Epiphan AI] Enrolled` (4575) or `[Epiphan AI] Blocked` (4577).

## Stage 2b — Ownership + no-double-dial guard (CRITICAL)
A lead must be worked by exactly one rep and never dialed by two. Enforce, in order:
1. **Already in motion (double-dial guard):** exclude any candidate with `nooks_active_in_sequence == true`
   (fast HubSpot filter; `nooks_sequenced_by` shows which rep). Cross-check authoritatively against Nooks
   `listSequenceStates(filter_state:[active,paused], include:[prospect])` on `prospect.crmId == contactId`.
   Also exclude `epiphan_ai_status ∈ {enrolled, sent, replied}` (already in the AI pipeline).
2. **Existing SDR owner:** read `sdr_owner`.
   - Set to a dialing rep → belongs to that rep's queue only (never another rep's).
   - Set to an AE/non-dialer → leave per Golden Rules (stale-AE exception handled upstream).
   - Unset → eligible for assignment.
3. **Assign unset by account:** group eligible candidates by account/domain; assign the whole account to
   one rep (round-robin/load-balanced; if any contact at the account already has an `sdr_owner`, use that
   rep). **SHADOW:** propose the assignment in the report. **LIVE:** set `sdr_owner` via
   `hubspot_update_contact` (propagates to Nooks). Never overwrite an existing `sdr_owner`.
4. Result: a clean per-rep candidate set with zero cross-rep overlap.

## Stage 2c — DA Audit (always-on AE-pipeline + recent-purchase guard) (CRITICAL)
A **devil's-advocate** pass that must run on **every** candidate account before enrollment — challenge
each one with "is there a reason we should NOT touch this?". Two hard exclusions:
1. **Active AE deal (Lex / Phil):** if the account has an **open deal** owned by or collaborated on by
   **Lex Evans (82625923)** or **Phil Sandler (190030668)** → **EXCLUDE** (do not autopilot-dial an
   account with a live AE opportunity). Surface it as `AE-ACTIVE → coordinate with <AE>`, never enroll.
   Check via `hubspot_search_deals` (owner/collaborator filter, open stages) associated to the account,
   or Epiphan AI `ask_agent` / `sales_brief` for the account's open pipeline.
2. **Recent purchase (last 12 months):** if the account **purchased within the last 12 months**
   (`crm_get_customer_orders` / `query_dataset revenue` / closed-won deal in window) → **EXCLUDE** as a
   recent customer; route to CS/expansion, not cold dial. (Catches recent buyers that a stale
   `lifecyclestage` would miss.)
Run this as a real audit step (optionally via a `devils-advocate` subagent over the candidate list);
log every exclusion with its reason. Also re-applies the standard customer/channel checks as backstop.

## Stage 3 — Qualify + score
- `qualify_lead` (Epiphan AI) → category (ideal_mql/warm/nurture/junk), `power_level` (atl/btl/unknown),
  region, junk flag. Drop junk; nurture → leave for email-only, don't auto-enroll the dial cadence.
- **Persona match** to a v1 vertical persona using the exact title filters in
  `reference/nooks-personas-v2.md` (Live Event Producer, Higher Ed Lecture Capture Lead,
  Community College Media Coordinator, Corporate Video Specialist). Respect each persona's
  "Title does NOT include" exclusions.
- **Win-pattern weighting** (from Tim's + AE conversion data, see `reference/`): boost
  AV/Media Services Manager–Director and Head/Director of Instructional Technology (incl.
  Law/Med variants); down-weight central-IT-only with no AV project and junior specialists.
- **"Why now" signal** per `reference/nooks-signals-v1.md`: legacy-capture-HW EOL (Matrox/Extron
  SMP), competing capture/PC-Windows tech, job-change, recent expansion. For v1, inherit the
  signal from the source-list context (e.g. a Greenfield/EOL-bucketed list) and any obvious
  title/firmographic cue; full detection is v3.
- **Auto-enroll gate (see config):** persona-in-focus + `power_level == atl` + not junk → eligible.
  Category `nurture` does **not** block (it under-rates Live Events). GRAY → hold for Tim; BTL → skip.
- **Priority score** (drives per-rep ranking + the top-5; category is one input, not a gate):
  `score = 0.30·signal_strength + 0.25·ICP_vertical_score + 0.20·win_pattern_weight
          + 0.15·category_rank(ideal_mql=1.0 / warm=0.6 / nurture=0.3) + 0.10·phone_present`.
  Signal strength: legacy-HW-EOL / competing-tech / job-change = high; expansion/hiring = medium; none = low.
  Win-pattern: AV/Media Manager–Director + Head/Dir Instructional Technology = high; central-IT-only / junior = low.

## Stage 4 — Route
Map play → Nooks sequence id (Routing table). A detected job-change or lost-deal signal
overrides the list default. Record `sequence_id`, `sequence_name`, and a one-line `routing_reason`.

## Stage 5 — Enroll (SHADOW-GATED)
**If `SHADOW_MODE == true` (default):** DO NOT call any Nooks/HubSpot write tool. Build the
enrollment plan and emit the report (Stage 8). Each row: lead, persona, signal, ATL/BTL,
phone status, routed sequence + reason, and what *would* happen ("would enroll", "would set
[Epiphan AI] Enrolled").

**If `SHADOW_MODE == false`:** per ATL lead, up to `DAILY_ENROLL_CAP`:
1. Resolve the Nooks prospect: `listSequenceStates`/prospect search by email; the Nooks
   `prospect.crmId` equals the HubSpot contactId. If absent, create the prospect (`syncProspects`/create).
2. `createSequenceState({data:{prospect:{id}, sequence:{id}, owner:{id: <rep Nooks userId>},
   mailbox:{id: <rep mailbox>}, state:"active"}})`. The **`owner`** (rep's Nooks userId, mapped from
   `sdr_owner` via the roster table) makes the cadence + its call/manual tasks land in that rep's queue;
   the **`mailbox`** sends auto-emails from that rep. (Target sequences are `team_editable`, so any owner
   is allowed.)
3. Reflect state on the HubSpot contact: set `epiphan_ai_status = "enrolled"` (drives `[Epiphan AI]
   Enrolled` 4575). The `nooks_active_in_sequence` / `nooks_sequenced_by` / `nooks_current_sequence_name`
   mirrors are maintained by the Nooks↔HubSpot sync — confirm at first live run; write them if the sync lags.
4. Respect the per-rep daily cap; log any failures and continue (graceful degradation).

## Stage 6 — Multi-thread, single-owner (CRITICAL guard)
Multi-threading is only safe if **one SDR owns the entire account**. Never let 2–3 SDRs dial the
same company — that's worse than not multi-threading.
- **Account = atomic ownership unit.** Every contact at an account (grouped by registrable domain)
  carries the **same `sdr_owner`**. When the skill adds a 2nd/3rd contact (multi-thread), that contact
  inherits the account's existing `sdr_owner` — never round-robin a teammate onto an owned account.
- **Conflict detection:** if an account already has contacts with **different** `sdr_owner` values,
  flag it as a `SPLIT ACCOUNT` and consolidate to one rep (default: the rep who owns the most/most-senior
  contact, or who has an active Nooks enrollment there) before enrolling anyone new.
- **Missing economic buyer:** if an account has no Manager/Director-level (ATL) contact in the plan,
  call `hubspot_find_contacts_by_role(domain, titles:[AV/Media/IT Director, Head of Instructional
  Technology])` to surface it — and **attach it to the same `sdr_owner`** as the rest of the account.
  Rationale (evidence): every 2026 single-threaded deal below Manager level lost.

## Stage 7 — Monitor + warm handoff (runs every invocation)
Detect warm prospects via two signals (no email-body parsing needed):
- **Reply:** `epiphan_ai_status == replied` (membership in `[Epiphan AI] Replied` 4576) — the Epiphan AI
  pipeline already detects email replies.
- **Call outcome:** a Nooks call disposition of **Meeting Booked** / **Connected** / **Referral** on the
  prospect (poll `listCalls`/dispositions, or `listSequenceStates(filter_updatedAt_gte: last_run)` for
  states that changed). A `finished` state with none of these = cold-complete (status → `completed`), not warm.

For each warm prospect:
- `finishSequenceState(id)` if still active/paused (halt remaining touches).
- Set `epiphan_ai_status = "replied"` on the contact.
- Notify the **owning rep** (`sdr_owner`): `hubspot_create_contact_task(contactId, ownerId: <sdr_owner>,
  taskType:CALL, subject:"WARM — replied/booked in Nooks", dueDate: today)` and surface in that rep's next `morning-brief`.

## Stage 7b — Per-rep "next best 5 to call"
Prioritize each rep's owned + newly-assigned candidates and surface their **TOP_N_PER_REP** (5).
Rank by: persona-fit + ICP vertical score, "why now" signal strength (EOL/competing-tech/job-change
highest), ATL power level, win-pattern weighting (AV/Media Manager–Director + Instructional Technology
up; central-IT-only/junior down), and phone-present. Each entry: name, title, company, phone, persona,
signal, routed sequence, one-line "why call now". This is the rep's dial list for the block — and it
contains only leads no other rep is working (Stage 2b guarantees it).

## Stage 8 — Report (per rep) + outcome sidecar
Fill **`reference/dial-list-report-template.html`** (self-contained; repeat the `.rep` block per dialing
rep, the `.card` block ×5 for their Next-Best-5, and a `.candidates` row per lead) and write it to the
output dir as `nooks_autopilot_<YYYY-MM-DD>.html`. Mode badge = SHADOW or LIVE. Each rep section shows
their **Next-Best 5 to Call** (ranked by the priority score, with a one-line "why now") + a collapsible
full candidate table (disposition: would-enroll / enrolled / skipped+reason, persona, signal, sequence,
ATL/BTL, phone, multi-thread gaps). Header KPIs: candidates, qualified ATL, planned/enrolled, double-dials
prevented, warm handoffs. Then write
`~/.claude/skill-analytics/last-outcome-nooks-autopilot.json`:
```json
{"ts":"[UTC ISO8601]","skill":"nooks-autopilot","version":"1.0.0","variant":"[shadow|live]",
 "status":"[success|partial|error]","runtime_ms":[ms],
 "metrics":{"candidates":[n],"qualified_atl":[n],"shadow_planned":[n],"enrolled":[n],
            "skipped_golden_rules":[n],"skipped_suppressed":[n],"skipped_dedup":[n],
            "double_dials_prevented":[n],"accounts_assigned":[n],
            "multithread_gaps":[n],"warm_handoffs":[n],
            "per_rep":{"<ownerId>":{"top5":[n],"enrolled":[n],"assigned":[n]}}},
 "error":null,"session_id":"[YYYY-MM-DD]"}
```
</workflow>

<dependencies>
## MCP tools
- **Epiphan AI:** `qualify_lead`, `enrich_contact`, `hubspot_find_contacts_by_role`, `hubspot_search_lists`,
  `hubspot_list_members`, `hubspot_create_contact_task`, (live) the HubSpot write tool that sets the
  `[Epiphan AI]` state property, `identify_company`.
- **Nooks:** `listSequences`, `listSequenceStates`, `createSequenceState`, `finishSequenceState`,
  `listEmails`, `listProspects`/`getProspect`, `getMe`. (Token scopes confirmed: sequence-states:write,
  prospects:write, tasks:write, emails:read.)
- **Apollo/Clay (fallback):** phone waterfall when HubSpot/Epiphan AI lacks a verified phone.

## Sibling skills referenced (reuse, don't rebuild)
- `sequence-load` — enrollment scaffold, Golden Rules, dedup, phone validation, suppression gate.
- `prospect-research-to-cadence` — qualify/score, ATL/BTL classification, ICP scoring, Clay waterfall.
- `prospect-enrich` / `phone-verification-waterfall` — phone enrichment.
- `morning-brief` — surface warm handoffs to Tim.

## Reference data (this skill's `reference/`)
`nooks-personas-v2.md` (title filters per persona), `nooks-signals-v1.md` (why-now triggers),
`nooks-battlecards-v3.md` (killer-Q arcs for v3 content personalization),
`Higher_Ed_Survey_Prospect_Signals_Report.md` (P0/P1 named accounts).
Drive canon: SDR System Map, Prompt Playbook, Sales Stack Guide (the operating model).

## Build-time discovery — RESOLVED (2026-06-19)
1. ✅ **Controlling property = `epiphan_ai_status`** (enum: enrolled/sent/replied/completed/skipped_*).
   Ownership key = **`sdr_owner`** (translates to Nooks owner). Double-dial guard = `nooks_active_in_sequence`.
2. ✅ **Enroll attribution:** `createSequenceState` takes `owner.id` (rep Nooks userId) + `mailbox.id`.
3. ✅ **Warm detection:** `epiphan_ai_status==replied` OR Nooks disposition Meeting Booked/Connected/Referral.

## Remaining confirmations (first live run only)
- Each rep's **Nooks mailbox id** (`listMailboxes` filter by user) for auto-email send-as.
- Whether the Nooks↔HubSpot sync auto-maintains `nooks_active_in_sequence`/`epiphan_ai_status` on a
  Nooks-side enrollment, or this skill must write them.
- **Coordinate with the existing Epiphan AI prospecting agent** (it also sets `epiphan_ai_status` and
  may enroll via Apollo) so a contact isn't worked by both pipelines — treat `epiphan_ai_status ∈
  {enrolled,sent,replied}` and `hs_currently_enrolled_in_prospecting_agent=true` as "hands off".
</dependencies>

## Guardrails
- SHADOW first. Never make a Nooks/HubSpot **write** while `SHADOW_MODE == true`.
- Auto-enroll ATL only; GRAY needs Tim's ok; never auto-enroll BTL.
- Honor the daily cap and the Suppression Gate every run.
- Validate any customer-facing claim via Epiphan AI product search / the Verified spec bank
  before content personalization (v3) — never quote specs from memory.
- The agent only mutates `[AI] `-prefixed lists it owns; state is reflected via contact properties.

## Scheduling
- **Cron:** `schedule` frontmatter `0 5 8 * * 1-5` (sec-min-hour order, matching sibling skills) =
  **weekdays 08:05 America/New_York**, right after `morning-brief`.
- **One run, all reps:** a single daily run produces the report **segmented per rep** (each rep reads their
  own section + Next-Best-5). Simpler than 4 crons and gives every SDR their queue. (Optional later: split
  into per-rep scheduled runs if reps want independent timing.)
- **Monitor pass (Stage 7)** runs on every invocation; optionally add a lighter midday cron
  (`0 0 13 * * 1-5`) so same-day replies/bookings get halted + handed off quickly.

## Skill metadata
**Version:** 1.0 · **Author:** Tim Kipper · **Status:** v1 shadow · **Tier:** P1 (Core BDR Automation)
**Chain:** `prospect-refresh` → `sequence-load` → `morning-brief` → **`nooks-autopilot`**
**Supersedes:** the FastAPI backend autonomous pipeline for the live BDR/SDR motion.
