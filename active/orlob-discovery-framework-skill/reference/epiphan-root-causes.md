# Epiphan Root Causes by Vertical

For use in discovery (Step 2: Cause Analysis). Each vertical lists the underlying causes
Epiphan products actually fix — not symptoms. Symptoms are what the buyer says first
("our recordings are inconsistent"); root causes are what's driving it ("one AV tech
supports 50+ rooms, so nobody's there when a capture fails"). Use the cause matched to
what the buyer said, then confirm it back with a calibrated question.

**Epiphan products:** Pearl-2, Pearl Mini, Pearl Nano, Pearl Nexus, EC20 PTZ Camera,
Epiphan Connect, Unify, Edge.

**Core problems Epiphan solves:** lecture capture complexity, multi-source AV switching,
unreliable software encoders, scaling live production for remote viewers.

---

## Higher Ed (ICP 90)

Symptoms buyers report: "recordings are inconsistent," "faculty won't use the system,"
"we can't keep up with room support."

Root causes:
- **AV-staffing crunch** — one tech supports 50+ rooms, so failures go unattended and
  nobody's on-site when a capture drops.
- **Faculty abandonment** — recording systems are too complex, so faculty stop using them
  → students miss content and usage rates fall below 50%.
- **LMS integration gaps** — capture doesn't flow cleanly into Echo360 / Panopto / YuJa /
  Kaltura / Opencast, so recordings need manual handling to publish.
- **Room diversity** — HDMI, SDI, VGA, and USB sources across the same fleet mean no single
  workflow works everywhere, driving one-off setups per room.
- **IT ticket volume** — AV failures generate a steady stream of tickets that IT can't
  scale to absorb.

Cause-analysis line: "What's driving the AV-staffing crunch — is it headcount, room count,
or the number of different source types your one tech has to know?"

---

## Courts/Legal (ICP 85)

Symptoms buyers report: "our streams drop during proceedings," "we can't rely on the
recording for the record," "the old system is end-of-life."

Root causes:
- **Chain-of-custody requirements** — recorded proceedings must be provably intact and
  attributable, which ad-hoc software encoders can't guarantee.
- **Multi-camera/multi-source sync** — evidentiary quality requires the judge, witness,
  and exhibit feeds to stay in sync; drift breaks the record.
- **Unreliable streaming to remote attendees** — remote participants drop or desync,
  jeopardizing a proceeding that must be accessible.
- **Legacy Extron SMP EOL** — installed base is end-of-life with no clean upgrade path,
  forcing a forced-migration decision.
- **Court reporter + audio sync failures** — audio and the reporter's record fall out of
  alignment, undermining the certified transcript.

Cause-analysis line: "When a stream drops mid-proceeding, what's the actual failure —
the encoder, the network, or the source switch?"

---

## Government (ICP 80)

Symptoms buyers report: "public can't reliably watch council meetings," "we're failing
ADA," "each department runs its own AV."

Root causes:
- **Budget cycles tied to fiscal year** — purchases must land in a fiscal window, so
  timing (not just fit) drives the decision.
- **Procurement through contract vehicles** — buying must route through approved vehicles
  (cooperative contracts, GSA, state contracts), shaping the decision process.
- **Council/board meeting streaming to the public** — public-meeting streams must be
  reliable and on-record, and outages are politically visible.
- **ADA compliance** — captioning and recording obligations aren't optional; gaps are a
  legal exposure.
- **Multi-department coordination** — shared AV infrastructure across departments creates
  no clear owner and inconsistent setups.

Cause-analysis line: "What has to be true in the procurement process — is this coming off
an existing contract vehicle, or does it need its own line in next year's budget?"

---

## Healthcare (ICP 75)

Symptoms buyers report: "OR turnover is too slow," "we can't document CME," "surgical
recordings are hit or miss."

Root causes:
- **Surgical suite recording for training + credentialing** — procedures must be captured
  reliably for teaching and credentialing, and a missed capture can't be re-shot.
- **OR turnover time** — complex setup between cases delays the schedule; every minute of
  setup is a delayed case.
- **HIPAA considerations** — patient-visible content must be handled compliantly, so any
  workflow that leaks PHI is a non-starter.
- **Simulation lab recording** — med-ed sim labs need multi-source capture for debrief.
- **CME credit documentation** — continuing-education credit requires documented,
  retrievable recordings.

Cause-analysis line: "What's eating the OR turnover time on the AV side — is it cabling,
source switching, or getting the recording started and closed out?"

---

## Corporate AV (ICP 80)

Symptoms buyers report: "all-hands quality is inconsistent," "hybrid meetings are
unreliable," "we're locked into a vendor."

Root causes:
- **All-hands / town hall production quality** — leadership visibility events must look
  professional; a bad stream is seen company-wide.
- **Multi-site hybrid meeting reliability** — hybrid meetings across sites drop or desync,
  eroding trust in the format.
- **IT infrastructure compatibility** — must fit existing NDI / SRT / Teams / Zoom
  plumbing rather than forcing a parallel stack.
- **AV staff turnover** — institutional knowledge leaves with the operator, so workflows
  that require an expert break when that person does.
- **Vendor lock-in** — proprietary systems trap the org and inflate switching costs.

Cause-analysis line: "When a hybrid all-hands goes sideways, where does it break —
the encode, the integration with Teams/Zoom, or the person running it that day?"

---

## Houses of Worship (ICP 70)

Symptoms buyers report: "the stream fails during service," "we only have volunteers,"
"the archive looks bad."

Root causes:
- **Weekend service reliability** — one shot, no retakes; a failure during service is
  visible to the entire congregation and can't be redone.
- **Volunteer-operated** — you can't require AV expertise, so anything needing an expert
  will fail when the volunteer rotation changes.
- **Multi-campus live streaming** — sending service to multiple campuses reliably is
  beyond a single-encoder setup.
- **Archive quality for on-demand replays** — the recorded archive must be watchable for
  people catching up later.
- **Budget approval through finance committee or elders** — the decision process runs
  through a committee, not one buyer.

Cause-analysis line: "If the volunteer running the stream on Sunday is different every
week, what happens when the regular person isn't there?"

---

## K-12 (ICP 65)

Symptoms buyers report: "teachers won't adopt it," "the board wants to see ROI," "every
building runs different gear."

Root causes:
- **Superintendent/board visibility into ROI** — leadership needs to see that classroom
  tech is being used and is worth the spend.
- **Teacher adoption** — it has to be zero-training; anything a teacher has to learn won't
  get used.
- **Device diversity across the district** — mixed gear building-to-building means no
  single supportable standard.
- **Classroom AV budgets tied to bond measures** — funding is episodic and tied to bonds,
  shaping timing and scope.
- **Athletic/event recording alongside academics** — the same system is expected to cover
  games and events, not just classrooms.

Cause-analysis line: "For teachers to actually use this, how much training can you realistically
ask them to do — because whatever's above that number, they won't."

---

## Products that map to each root cause

| Root cause | Recommended Epiphan product(s) |
|---|---|
| Room diversity / mixed HDMI-SDI-VGA-USB sources | Pearl Mini, Pearl-2 (multi-input capture/switch) |
| Faculty/teacher abandonment (needs zero-training) | Pearl Nano, Edge (simple, set-and-forget) |
| AV-staffing crunch / one tech, many rooms | Pearl Nano fleet + Edge (remote management at scale) |
| LMS integration gaps (Echo360/Panopto/etc.) | Pearl family (RTMP/RTSP/HLS out to LMS) |
| Multi-camera / multi-source sync (evidentiary) | Pearl-2, Pearl Nexus (multi-channel sync) |
| Unreliable software encoders | Any Pearl (hardware encoder reliability) |
| Legacy Extron SMP EOL replacement | Pearl-2, Pearl Nexus (drop-in upgrade path) |
| Multi-site / multi-campus live streaming | Pearl Nexus, Epiphan Connect (scale to remote viewers) |
| Hybrid meeting / Teams-Zoom integration | Epiphan Connect (pulls isolated feeds into Teams/Zoom) |
| PTZ camera capture in rooms/ORs/sanctuaries | EC20 PTZ Camera |
| Multi-source live production for events | Unify (production/switching), Pearl-2 |
| Scaling live production for remote viewers | Epiphan Connect, Pearl Nexus |
