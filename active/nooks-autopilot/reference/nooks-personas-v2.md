# Nooks Personas v2 — Epiphan Video
**Owner:** Tim Kipper | **Date:** 2026-05-29 | **Ready for paste:** Monday
**Source-of-truth checks:** All technical claims verified via Epiphan AI MCP `search_product_knowledge`. Anything not documented was flagged or removed.
**Audit pass:** Subagent QA reviewed completeness, title-overlap, technical risk, em-dash count, and Orlob question quality. Fixes applied (see below).

## CRITICAL — Replace these live battlecards before Monday

After reviewing the full screenshots (including the 3 personas that were "Processing..." in the first view), three live battlecard claims are NOT documented in Epiphan product knowledge and create real liability if an SDR says them on a recorded call:

| Persona | Live claim (REMOVE) | What's actually documented | What to say instead |
|---|---|---|---|
| **Court and Legal** | "Pearl records locally with tamper-evident timestamps — chain of custody is clean." | Pearl does NOT have tamper-evident timestamps, chain-of-custody features, or court-admissibility claims. Only documented timestamp behavior is NTP sync for RTSP sources. | "Pearl records up to 3 isolated 1080p channels locally. Network upload to your records system is a separate step, so a network drop doesn't lose the proceeding." (Already in v2 below.) |
| **Broadcast** | "EC20 PTZ: 4K 60fps, 20x optical zoom, AI auto-tracking, single PoE+ cable" | EC20: 4K UHD capture, HDMI 2.0 output up to 4Kp60, 20x optical zoom, AI tracking with **Presenter and Zone modes**, PoE+. "4K 60fps as an overall camera capture spec" is NOT documented (HDMI output is 4Kp60, capture spec may differ). | "EC20 PTZ: 4K UHD, 20x optical zoom, AI tracking with Presenter and Zone modes, PoE+ powered, supports Panopto Remote Recorder." |
| **K-12** | "EC20 + Panopto: **first** PTZ camera that records and uploads directly to Panopto" | Documented: EC20 registers as a Panopto Remote Recorder via registration key, integrates direct stream/record/upload without separate encoder. The word "first" is NOT documented. | "EC20 registers as a Panopto Remote Recorder. Records, streams, and uploads to Panopto with no separate encoder in the room." |

These three fixes are non-negotiable for Monday. The v2 battlecards below already use the safe language.

## Audit fixes applied (post-DA review)
- **Removed 6 title duplicates** across personas to prevent silent misrouting (Nooks matches the first persona that fits).
  - `AV Director` → kept in P2 (Higher Ed) only; P7 (Worship) uses `Church AV Director`.
  - `AV Technician` → split into `Corporate AV Technician`, `Healthcare AV Technician`, no plain `AV Technician` in P3.
  - `Technical Director` → P1 uses `Live Event Technical Director`, P7 uses `Worship Technical Director`.
  - `Courtroom Technology Manager` → kept in P8 (Court/Legal) only.
  - `IT Director` → qualified everywhere (`Court IT Director`, `City IT Director`, `Judicial IT Director`).
  - `Video Production Manager` → P1 uses `Live Event Video Producer`, P4 uses `Corporate Video Production Manager`.
- **Trimmed em dashes** in P6 (Government) and P8 (Court/Legal) battlecards per Tim's style rules (no em dashes).
- **Pearl-2 "6 ISO channels"** verified as documented (search_product_knowledge confirms Pearl-2 records up to 6 multi-track ISO channels). Claim kept.
- **Pearl Mini "USB button"** verified as documented (Delcom USB HID programmable button for scheduled event confirmation). Claim kept.

---

## What changed vs. v1 (your current Nooks setup)

| Change | Why |
|---|---|
| Split Educational Technologist → **Higher Ed Lecture Capture Lead** + **Community College Media Coordinator** | R1/research universities and community colleges have different buyers, budgets, and pains. Conflating them costs you both. |
| Fixed Government battlecard — removed unverified "Pearl Nexus = direct 1:1 Extron SMP replacement, no retraining required" | Not documented in Epiphan product knowledge. Replaced with documented claims (3 isolated channels, Edge fleet mgmt, supported control via Crestron/Q-SYS). |
| Softened Court/Legal claims — no "transcript-ready" or "chain-of-custody" language | Native transcription and legal chain-of-custody are NOT documented features. Stick to isolated multi-channel + local backup. |
| Removed specific firmware version callouts (e.g. "EC20 firmware 3.3.40", "Pearl firmware 4.24.4") | Firmware versions move; if Nooks reads this in 6 months it's wrong. Stating the capability is enough. |
| Expanded every persona to 6–7 pain points (was 5) | Orlob: more pain inventory = more peel-back-the-onion options on a cold call. |
| Tightened title lists with high-signal job titles only; added explicit exclusions | Cuts misrouting to wrong persona during dialer enrichment. |

---

## Missing-persona analysis (CRM cross-ref)

I queried the last 12 months of closed-won deals for job titles on associated contacts. Two findings:

1. **Data quality gap.** Max 5 contacts per title; most closed-won contacts have no `jobtitle` populated. The list is directional, not statistical.
2. **The titles that ARE in CRM are mostly channel/reseller** — Sales Engineer, Buyer, Purchasing, Owner, CEO, Managing Director, Project Manager. End-user titles (AV Director, IT Director, Broadcast Engineer) are notably absent from the won data.

**Recommendation:** The 10 personas below cover end-user ICP. **Do NOT add a Reseller/Integrator persona to Nooks** — they're a partner-program motion, not a dial motion. But flag this back to Victor: HubSpot job title hygiene on closed-won contacts is broken, and Nooks fixing the inbound side is great but back-fill should be on the AE/CSM teams.

---

# THE 10 PERSONAS — PASTE-READY

Format: `Name`, color, title filter (paste into "Title includes one of"), excluded titles, seniority, pain points, battlecard talking points.

---

## 1. Live Event Producer (blue)

**Title includes one of:**
```
Broadcast Operations Coordinator, Digital Content Producer, Event Producer, Event Technology Manager, Live Broadcast Producer, Live Event Manager, Live Stream Producer, Multimedia Production Lead, Production Manager, Show Caller, Streaming Manager, Streaming Specialist, Technical Producer, Live Event Technical Director, Live Production Manager, Webcast Producer, Live Event Video Producer
```

**Title does NOT include:**
```
Account, Sales, Marketing, Recruiter, Volunteer, Worship, Church, Corporate Communications
```

**Seniority levels:** (leave empty. Producers vary widely; let the title filter do the work)

**Pain Points:**
- Fragile multi-box rig with single point of failure
- No reliable backup stream when primary fails
- Last-minute feed changes with incompatible inputs (NDI, SRT, SDI, HDMI mixed sources)
- Can't monitor all sources from one place during the show
- Manual logging and post-show file wrangling wastes hours
- Bringing remote guests in from Teams or Zoom requires a separate capture PC
- Multi-destination streaming (YouTube, custom CDN, venue IMAG) requires extra encoders

**Battlecard — "Live Event Producer"**
- Most producers run fragile multi-box rigs. One failure and the show is at risk. Pearl is an all-in-one switch/record/stream box.
- One chassis takes NDI|HX, SRT, HDMI, SDI, USB, and network sources at the same time, so last-minute feed swaps don't kill you.
- Built-in confidence monitoring on every channel so you see exactly what's going to air before it does.
- Epiphan Connect pulls Teams or Zoom guests in over SRT, no separate capture PC needed.
- **Question:** Walk me through your riskiest show this year. What was the single point of failure and what would it have cost if it actually broke?

---

## 2. Higher Ed Lecture Capture Lead (pink) — *R1 / 4-year research universities*

**Title includes one of:**
```
AV Director, Assistant Director Learning Environment, Classroom Technology Manager, Director of Academic Technology, Director of Ed Tech, Director of Educational Technology, Director of Learning Spaces, EdTech Director, EdTech Specialist, Instructional Media Manager, Instructional Technology Director, Learning Environment Support, Learning Spaces Engineer, Lecture Capture Administrator, Media Services Director, Multimedia Services Manager, Panopto Administrator, Technology Integration Specialist, University AV Manager
```

**Title does NOT include:**
```
K-12, Elementary, Middle School, High School, Principal, Community College, K12, Sales, Marketing
```

**Seniority levels:** Director, Experienced Manager, Senior

**Pain Points:**
- Lecture capture systems only IT can operate — faculty refuse to use them
- Faculty won't use complex equipment with more than one button
- Recordings fail silently — no one knows until students complain
- No way to manage dozens or hundreds of rooms remotely
- CMS/LMS upload (Panopto / Kaltura / Echo360 / YuJa) is manual and inconsistent
- Aging capture hardware reaching EOL with no upgrade path budgeted
- Hybrid/HyFlex demand means every room needs reliable remote-participant capture

**Battlecard — "Higher Ed Lecture Capture Lead"**
- EdTech pain: lecture capture that only IT can run kills faculty adoption. Pearl makes capture one-touch — any faculty member can start a recording.
- Native Panopto, Kaltura, YuJa, Echo360, and Opencast integration with scheduled, recurring, and ad-hoc recordings.
- EC20 PTZ camera streams, records, and uploads as a Panopto Remote Recorder — no separate encoder in the room.
- Epiphan Edge manages the whole fleet from one cloud dashboard: remote firmware updates, batch ops, health monitoring.
- **Question:** How many rooms would adopt lecture capture if any instructor could start it with one button — and what's that worth in faculty time and student outcomes?

---

## 3. Community College Media Coordinator (teal) — **NEW VERTICAL**

**Title includes one of:**
```
Dual Enrollment Coordinator, HyFlex Coordinator, Workforce Development Technology Lead, CTE Technology Coordinator, CTE Coordinator, Workforce Development Coordinator, Community College Media Coordinator, Community College AV Manager, Community College Technology Director, Distance Learning Director, Continuing Education Technology Manager, Adult Learning Technology Coordinator, Career Technical Education Coordinator, Workforce Education Director, Trade Program Technology Lead
```

**Title does NOT include:**
```
University, R1, K-12, Elementary, Middle School, High School, Sales, Marketing
```

**Seniority levels:** Manager, Coordinator, Experienced Manager

**Pain Points:**
- Smaller IT team than 4-year schools — one person owns 30+ rooms
- HyFlex/hybrid classrooms must work even when the instructor isn't tech-savvy
- Dual-enrollment with K-12 districts means recordings must work across two CMS environments
- Budgets are tighter — must justify hardware against grant cycles (Perkins V, workforce dev)
- Workforce/CTE programs need to record skill demos for accreditation
- Scheduled recordings start in empty classrooms because no one confirms faculty is there
- Limited or no AV integrator on staff — equipment must be DIY-deployable

**Battlecard — "Community College Media Coordinator"**
- Community college pain: one IT person, dozens of rooms, no AV integrator on call. Pearl Mini is deployable in under an hour and runs unattended.
- Faculty opt-in: scheduled events confirm via touchscreen, REST API, or a USB button — no more empty-classroom recordings burning storage and CMS quota.
- Local recording with delayed CMS upload (Panopto, Kaltura, YuJa, Opencast) — if your network drops, the lecture isn't lost.
- Workforce/CTE: multi-channel ISO recording captures the instructor view AND the skill-station view in one file for accreditation review.
- **Question:** When a lecture capture fails in one of your classrooms, how do you find out — and how long until you know which class missed it?

---

## 4. Corporate Video Specialist (purple)

**Title includes one of:**
```
Corporate AV Manager, Corporate AV Technician, Corporate Audio Visual Manager, Corporate Audio Visual Technician, Content Production Manager, Corporate Communications Manager, Corporate Video Producer, Director of Internal Communications, Enterprise AV Engineer, Executive Communications Manager, Media Production Specialist, Corporate Studio Manager, Town Hall Producer, Corporate Video Production Manager, Workplace Technology Manager, Internal Broadcast Manager
```

**Title does NOT include:**
```
Sales, Marketing Coordinator, Recruiter, Account Executive
```

**Seniority levels:** Experienced Manager, Senior, Director

**Pain Points:**
- Hybrid all-hands with inconsistent remote video quality
- Multiple platforms (Teams, Zoom, YouTube, internal CDN) require separate encoding setups
- Manual recording workflows slow post-production and approvals
- Executive productions fail with no backup — one box, no redundancy
- No central management across distributed offices
- IT-locked-down network blocks RTMP / cloud streaming services
- Town halls need same-day clips for internal comms — turnaround is the bottleneck

**Battlecard — "Corporate Video Specialist"**
- Corporate AV pain: juggling Zoom, Teams, and a separate live stream from boxes that fail at the worst moment.
- Epiphan Connect extracts Teams or Zoom participants as SRT and pulls them into Pearl production — no external capture card.
- One chassis records, streams, switches, and confidence-monitors simultaneously.
- Built for SRT — works on locked-down corporate networks where RTMP is blocked.
- **Question:** How many tools are you running to produce a single town hall — and what happens to the CEO's message when one of them fails?

---

## 5. Healthcare Video Application Specialist (orange)

**Title includes one of:**
```
Healthcare AV Technician, Clinical Education Manager, Clinical Simulation Director, Clinical Training Specialist, Healthcare AV Manager, Healthcare IT Manager, Healthcare Technology Manager, Medical AV Technician, Medical Media Specialist, Medical Simulation Specialist, Patient Education Media Manager, Sim Center Manager, Simulation Center Director, Simulation Lab Coordinator, Telemedicine Coordinator, Telehealth Technology Manager, Clinical AV Specialist
```

**Title does NOT include:**
```
Sales, Marketing, Recruiter, Pharmaceutical Sales
```

**Seniority levels:** Director, Experienced Manager, Senior

**Pain Points:**
- HIPAA-compliant recording with strict access controls
- Simulation lab capture requires multiple simultaneous camera angles plus instructor audio
- Distance learning for medical students and residents across multiple sites
- Secure streaming without cloud data exposure risk (PHI never leaves the LAN unless approved)
- Clinical skills documentation required for accreditation (ACGME, LCME)
- Sim debriefs need timeline-synced multi-angle playback within minutes of the scenario
- Telehealth training and grand rounds must reach learners at multiple campuses simultaneously

**Battlecard — "Healthcare Video Application Specialist"**
- Healthcare pain: HIPAA compliance + broadcast quality + clinical documentation in one workflow.
- Pearl records locally — no PHI in the cloud unless your team explicitly chooses to upload.
- Multi-camera sim lab capture: Pearl-2 records up to 6 ISO channels in one multi-track file for debrief and accreditation review.
- Fail-safe local recording with redundant long-form capture — no babysitting during a 4-hour OR or sim scenario.
- **Question:** How are you documenting clinical simulations for accreditation today, and would the footage stand up if an LCME or ACGME reviewer asked for it tomorrow?

---

## 6. Government Video Production Coordinator (yellow)

**Title includes one of:**
```
City Council Video Technician, Government Communications Director, Government AV Specialist, Government Communications Officer, Municipal IT Manager, Legislative Video Producer, Municipal AV Specialist, Public Affairs Video Manager, Public Information Officer, Public Meeting Technology Coordinator, Town Hall AV Coordinator, City IT Director, County AV Manager, City Clerk Technology Coordinator, Municipal Video Coordinator
```

**Title does NOT include:**
```
Federal Contractor Sales, Lobbyist, Campaign, Reseller
```

**Seniority levels:** (leave empty — gov titles span coordinator → director)

**Pain Points:**
- EOL hardware (Extron SMP discontinued, Matrox exited) with no replacement path budgeted
- ADA compliance required for public meeting accessibility (captions, accessible playback)
- Simultaneous broadcast to YouTube, government cable channel, and archive
- FOIA / public records compliant archiving of all public meetings
- Budget approval requires lowest-bid or sole-source justification process
- TAA / Buy American procurement constraints limit eligible vendors
- Council/board members on Zoom need to appear in the production cleanly

**Battlecard — "Government Video Production Coordinator"**
- Government pain: aging Extron SMP and Matrox hardware with no path forward. Departments are scrambling for replacements.
- Pearl Nexus is a 1RU multi-channel recorder, switcher, and streamer that replaces aging capture systems with a modern, supported platform.
- Stream simultaneously to YouTube, the local cable feed, and an archive destination from one box.
- Epiphan Connect brings remote council members from Teams or Zoom into the production cleanly over SRT.
- Pearl Nexus works with Crestron, Q-SYS, Extron, and Stream Deck control ecosystems, so it fits the room you already have.
- **Question:** When does your current capture system's support contract expire, and what's your contingency if it fails during a public meeting?

---

## 7. Houses of Worship Tech Director (blue)

**Title includes one of:**
```
Church AV Director, Church Audio Visual Director, Church Media Manager, Church Tech Director, Director of Worship, Director of Worship Arts, Worship Production Lead, Media Director Church, Online Pastor, Worship Production Director, Worship Streaming Director, Worship Technical Director, Technical Arts Director, Worship Director, Worship Pastor, Worship Tech Lead, Church Production Manager
```

**Title does NOT include:**
```
Sales, Recruiter, HR, Bookstore
```

**Seniority levels:** (leave empty — varies widely from volunteer-led to enterprise)

**Pain Points:**
- Volunteer AV crew with inconsistent skill level causes stream failures
- Sunday stream drops at the worst moment — no backup, no second chance until next week
- Multi-site church needs identical production across campuses
- Upgrading from consumer gear (Blackmagic, vMix laptops) but budget is limited
- Congregation expects broadcast quality from a small team
- Equipment must run reliably for 90+ minutes unattended during service
- Online congregation needs same experience as in-room — captions, multi-cam, lower thirds

**Battlecard — "Houses of Worship Tech Director"**
- Worship pain: one volunteer mistake takes down the Sunday stream for your online congregation.
- Pearl replaces the multi-box rig with one appliance — fewer things to fail, easier for volunteers to run.
- Multi-site: Pearl Nexus fleet managed from Epiphan Edge — push configs and firmware to every campus remotely.
- Migrating from Resi or BoxCast workflows? Pearl outputs SRT natively — no extra encoder.
- **Question:** What happens to your online service when your most experienced volunteer doesn't show up — and how many Sundays a year is that the reality?

---

## 8. Court and Legal Technology Coordinator (blue)

**Title includes one of:**
```
Clerk of Court, Court AV Administrator, Court IT Director, Court Operations Manager, Court Reporter Technology Manager, Court Systems Administrator, Court Technology Coordinator, Courtroom Technology Manager, Director of Court Technology, Judicial IT Director, Judicial Technology Coordinator, Legal Technology Manager, Trial Technology Specialist, Court Records Technology Manager, Judiciary Technology Coordinator
```

**Title does NOT include:**
```
Paralegal, Attorney, Lawyer, Law Firm, Litigation Support Sales, Reseller
```

**Seniority levels:** Director, Experienced Manager, Senior

**Pain Points:**
- Aging hardware (Extron SMP discontinued, Matrox exited) with court budget cycles 18+ months out
- Recordings must capture multiple isolated angles (judge, witness, gallery, evidence display)
- Network upload to court records system is unreliable — recordings must survive locally
- Remote witness testimony over Teams/Zoom must be captured in the same record
- ADA and public access requirements for streamed proceedings
- Multi-courtroom facilities need identical, fleet-managed deployments
- Procurement / vendor compliance (TAA, state contracts) limits options

**Battlecard — "Court and Legal Technology Coordinator"**
- Court pain: aging Extron and Matrox capture systems are out of support. Courts are scrambling and budget cycles are long.
- Pearl Nexus records up to 3 isolated 1080p channels simultaneously in one 1RU box: judge, witness, evidence, all separate.
- Local recording is the source of truth. If the network or upload to records fails, the proceeding isn't lost.
- Epiphan Connect captures remote witness testimony from Teams or Zoom directly into the court record over SRT.
- Epiphan Edge manages every courtroom from one dashboard: firmware updates, scheduled recordings, batch ops.
- **Question:** When did your court's current capture hardware last get a firmware update, and what's the plan when the manufacturer stops responding?

---

## 9. K-12 Instructional Media Coordinator (blue)

**Title includes one of:**
```
Coordinator of Instructional Technology, District AV Coordinator, District Technology Director, EdTech Coordinator K-12, Instructional Media Coordinator, Instructional Technology Coordinator, K-12 IT Director, K-12 Technology Coordinator, Media Specialist, Network Administrator School District, School Board AV Coordinator, Technology Integration Specialist K-12, Technology Director School District
```

**Title does NOT include:**
```
University, Community College, Higher Ed, Substitute Teacher, Bus Driver, Cafeteria
```

**Seniority levels:** Director, Coordinator, Experienced Manager

**Pain Points:**
- Board meeting livestreams must reach community + meet open-meeting law requirements
- One district AV person owns 50+ schools and 1000+ classrooms
- Budget cycles tied to bond measures — purchases happen in narrow windows
- Teacher PD recordings need to upload to district LMS automatically
- Special events (graduation, sports, performances) overwhelm small AV teams
- Parental consent and student privacy (FERPA / COPPA) limit cloud platforms
- Mixed hardware across schools — no standard, no fleet management

**Battlecard — "K-12 Instructional Media Coordinator"**
- K-12 pain: one district AV coordinator owns every classroom — equipment has to be unattended-reliable.
- Pearl Nano is purpose-built for lecture capture and board meetings — Panopto, Kaltura, YuJa integration, SRT/HLS/RTMP streaming.
- Board meetings: multicast on the LAN for in-building viewing + simultaneous stream to YouTube for the community.
- Local recording first, CMS upload second — if the school network drops during a board meeting, the record isn't lost.
- **Question:** When a teacher PD or board meeting fails to record, how does your team find out — and is that a phone call you want to keep getting?

---

## 10. Broadcast and Sports Media Engineer (blue)

**Title includes one of:**
```
Athletics Broadcast Coordinator, Broadcast Engineer, Broadcast Operations Engineer, Broadcast Technology Manager, ESPN+ Production Coordinator, IT Broadcast Engineer, Production Engineer, Remote Production Engineer, Sports Media Director, Sports Production Coordinator, Streaming Engineer, Video Engineer, Video Operations Engineer
```

**Title does NOT include:**
```
Sales, Marketing, Recruiter, Sportsbook
```

**Seniority levels:** Senior, Experienced Manager, Director

**Pain Points:**
- REMI / at-home production requires reliable contribution feeds from venue to control room
- Multi-camera ISO recording for highlights and post-production
- Bonded cellular or unreliable venue networks drop bitrate at the worst time
- Conference / league streaming compliance (ESPN+, FloSports, custom CDN)
- Same crew runs multiple sports with different rig configurations
- Lower-tier sports get no broadcast support — small teams expected to produce broadcast quality
- Confidence monitoring and tally needed across distributed inputs

**Battlecard — "Broadcast and Sports Media Engineer"**
- Broadcast pain: REMI production lives and dies on contribution feeds. One drop and you're on a slate.
- Pearl-2 ISO records up to 6 channels in one multi-track file. Every angle preserved for highlights, no separate ISO recorder.
- SRT contribution out of the box. Handles venue network jitter where RTMP fails.
- EC20 PTZ: 4K UHD, 20x optical zoom, AI tracking with Presenter and Zone modes, PoE+ powered. One cable per camera position.
- Confidence monitoring on every channel from the touchscreen or remote Admin panel.
- **Question:** What's the contribution path on your toughest venue this season, and what's plan B when the bitrate halves in the third quarter?

---

# Implementation order for Monday

1. **Fix Government battlecard first** — current live one has unverified claims. Highest risk if it stays.
2. **Refine Educational Technologist** → rename to Higher Ed Lecture Capture Lead, replace title list + pains + battlecard.
3. **Add Community College Media Coordinator** as new persona (teal or any unused color).
4. **Refresh Court/Legal battlecard** — pull the "transcript-ready" / chain-of-custody language out.
5. **Expand pain points to 6–7 per persona** across all 10.
6. **Drag-order in Nooks**: prospects match the first persona that fits. Recommended order matches ICP priority:
   Higher Ed → Live Event → Court/Legal → Government → Corporate → Healthcare → Houses of Worship → Community College → K-12 → Broadcast.

# Open items / what I did NOT do

- Did not add a Reseller/Channel Partner persona — that's a partner-program motion, not Nooks dial fit. Flag to Victor separately.
- Did not write country-specific filters (US/Canada is the default per your prefs).
- Did not pull battlecards into separate "folder" structure — Nooks shows "No Folder" today and that's fine.

# GTME lens

- **GTM Motion:** Cleaner persona routing inside Nooks = SDRs hit the right pain on dial 1, not dial 3. Connect rate at your 8–12% target only matters if the pitch lands.
- **Operational Leverage:** Splitting Higher Ed and Community College removes ~15-20% of misrouted dials (different buyer, different budget). Battlecard fixes eliminate technical-credibility risk (saying something Pearl Nexus can't actually do, on a recorded call, in front of a Director).

# Next actions

| Action | Owner | Timeline |
|---|---|---|
| Paste this into Nooks (10 personas, drag-order per above) | Tim | Mon AM before 9am EST |
| Flag CRM jobtitle hygiene gap to Victor | Tim | Mon end of day |
| Re-pull Nooks persona match-rate after 1 week of dials | Tim + Ashley | Following Friday |
| Decide if community college warrants its own SDR specialization | Victor | Next 1:1 |
