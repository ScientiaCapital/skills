# Demo Execution Playbook — Vertical-Specific Demo Flows

> Extracted from SKILL.md — content preserved verbatim.

#### **Higher Ed (90 ICP Score)**
*Vertical DNA: Multi-room capture, automated publishing, integration w/ learning platforms, admin dashboards*

**Demo Arc:**
1. **RECAP:** "You capture lectures in 3+ lecture halls, publish to Kaltura/Panopto/YuJa, and need one-click scheduling."
2. **AGENDA:** Show Pearl-2 multi-room setup → Epiphan Connect cloud mgmt → CMS auto-sync → room scheduler interface
3. **SHOW VALUE:**
   - Pearl-2 in Room A + Room B → Live switch/record both simultaneously
   - Hit REC → Auto-publishes to Kaltura/Panopto with metadata (course, instructor, timestamp)
   - Click "Schedule Room" in Connect dashboard → Pearl turns on, streams, records on your time
   - Compare: Manual Extron + Crestron (3 vendors, tech support fragmentation) vs. Epiphan one platform
4. **SUMMARIZE:** "One box per room, one cloud platform, zero manual steps—your faculty just teaches."
5. **NEXT STEPS:** Pilot 2 classrooms (Week 1), then phase 3-5 more

**Key Questions During Demo:**
- "How many simultaneous recordings do you need?" (→ Pearl-Nexus or multi-Pearl scaling)
- "Which LMS owns your content?" (→ integration path validation)
- "Who's your technical troubleshooter?" (→ MEDDIC User Champion ID)

**Competitive Displacement:**
- vs. Extron SMP: "Extron SMP was discontinued; you'll have no vendor support. Pearl-2 is actively developed."
- vs. Blackmagic ATEM + recorder: "Blackmagic requires a control room operator; Pearl auto-records without crew."
- vs. Crestron: "Crestron is AV control, not capture-to-cloud. You'd need separate recorder + cloud stack."

---

#### **Courts/Legal (85 ICP Score)**
*Vertical DNA: Compliance archival, failover reliability, secure streaming, multi-camera courtroom capture, audit trail*

**Demo Arc:**
1. **RECAP:** "You need tamper-proof recording, 99.9% uptime, secure playback for judges/attorneys, and chain-of-custody compliance."
2. **AGENDA:** Pearl-2 multi-camera courtroom → Dual recording (local SSD + cloud via SRT) → Failover behavior → Secure streaming with audit logs
3. **SHOW VALUE:**
   - 3 Pearl Mini cameras (judge, defendant, gallery) → Synchronized multi-view record
   - Show local .MP4 on SSD + simultaneous cloud backup (SRT protocol, encrypted)
   - Simulate network failure → Pearl stays recording locally, cloud re-syncs when connectivity returns
   - Attorney logs in (HTTPS, 2FA in Connect) → Video plays, access logged with timestamp and IP
   - Legal holds / audit export → CSV of who watched what, when
4. **SUMMARIZE:** "Your recordings are redundant, compliant, and legally defensible—no questions about tampering or authenticity."
5. **NEXT STEPS:** Pilot one courtroom, validate compliance checklist, then scale to 5+ courts

**Key Questions During Demo:**
- "What's your uptime SLA?" (→ Dual-recording rationale)
- "Who audits access?" (→ Compliance role = MEDDIC EB)
- "Do you currently use Matrox or Teradek?" (→ Competitive displacement)

**Competitive Displacement:**
- vs. Matrox (exited market): "Matrox has no vendor support or updates. Pearl is actively maintained for legal compliance."
- vs. Teradek: "Teradek is cloud-first only; if your cloud goes down, you lose recordings. Pearl has local failover."
- vs. vMix: "vMix requires a PC operator; Pearl records unattended and is hardened for 24/7 compliance use."

---

#### **Corporate AV / Meeting Rooms (80 ICP Score)**
*Vertical DNA: Meeting room capture, NDI/SRT streaming, multi-site standardization, easy ops*

**Demo Arc:**
1. **RECAP:** "You have 10+ meeting rooms, need to stream hybrid meetings to offices, and want standardized hardware."
2. **AGENDA:** Pearl Mini in conference room → NDI stream to Zoom/Teams/Cisco → Epiphan Connect multi-site mgmt → Compare to Extron SMP
3. **SHOW VALUE:**
   - Pearl Mini with dual HDMI in (presentation + camera) → Single feed with speaker recognition
   - Output: NDI stream (0-latency, no cloud hop) + RTMP to Zoom bridge + local recording
   - Click 1 button: "Start Meeting" → Everything on
   - Epiphan Connect dashboard: 15 rooms, battery checks, record status, remote reboot if stuck
   - Old setup: Extron SMP + codec + Zoom Rooms = 3 tech touches; Pearl = 1
4. **SUMMARIZE:** "One Pearl per room, one cloud dashboard, your meetings just work—IT spends 10 hours/month not troubleshooting."
5. **NEXT STEPS:** 2-room pilot, measure uptime + IT time saved, roll to 8 more

**Key Questions During Demo:**
- "How many simultaneous hybrid meetings?" (→ NDI bandwidth; Pearl-2 if >3/day)
- "Who's your AV manager?" (→ MEDDIC User Champion)
- "Do you have bandwidth concerns with cloud?" (→ NDI value prop; zero cloud latency)

**Competitive Displacement:**
- vs. Extron SMP (discontinued): "SMP is EOL. Pearl is the upgrade path—better specs, cloud management, active support."
- vs. Blackmagic: "Blackmagic requires a separate streaming operator; Pearl auto-handles NDI/RTMP/recording."
- vs. Crestron DM-MD: "Crestron is routing; doesn't capture or stream. Pearl does both + cloud."

---

#### **Government (80 ICP Score)**
*Vertical DNA: On-prem control, secure streaming, RTMP/SRT protocols, archival, no-cloud-required option*

**Demo Arc:**
1. **RECAP:** "Your security posture requires on-prem recording, FIPS-compliant streaming, and audit-ready archive."
2. **AGENDA:** Pearl-2 recording locally → RTMP/SRT to internal streaming server → Epiphan Connect on-prem option → Fallback failover
3. **SHOW VALUE:**
   - Pearl records to local SSD (no cloud)
   - RTMP/SRT output to your on-prem streaming server (your firewall, your control)
   - Optional: Epiphan Connect on-prem (Docker container, your data center)
   - If network fails, Pearl keeps recording; RTMP auto-reconnects
   - Export to NAS on your network, archive to your server
4. **SUMMARIZE:** "Your Pearl records and streams on your terms—data never leaves your infrastructure."
5. **NEXT STEPS:** Security review (FIPS, NIST), 30-day evaluation, then procurement

**Key Questions During Demo:**
- "Do you have a CISO or InfoSec lead?" (→ MEDDIC EB/Blocker ID)
- "What's your on-prem storage architecture?" (→ NAS, SAN, or archive server path)
- "Is cloud a no-go, or just controlled?" (→ Determines on-prem vs. Epiphan Connect with VPC option)

**Competitive Displacement:**
- vs. Teradek (cloud-only): "Teradek requires AWS/cloud. If your policy forbids it, Pearl is your answer."
- vs. vMix: "vMix needs Windows PC operator and external encoder. Pearl is appliance, no PC needed."
- vs. Blackmagic (requires control room): "Blackmagic needs a control operator; Pearl auto-records, no crew needed."

---

#### **Healthcare (75 ICP Score)**
*Vertical DNA: HIPAA-friendly recording, multi-camera surgical/procedure capture, LMS integration for training, cloud OR on-prem*

**Demo Arc:**
1. **RECAP:** "You record surgical procedures and training sessions, must comply with HIPAA, and integrate with your LMS (Kaltura, Panopto, YuJa)."
2. **AGENDA:** Multi-camera Pearl setup (OR camera + proceduralist camera) → HIPAA-compliant encryption → LMS auto-sync → Access controls
3. **SHOW VALUE:**
   - Pearl-2 with 2-camera input (overhead surgical cam + close-up procedural cam) → Single synchronized MP4
   - All data encrypted at rest (on-prem or cloud with AES-256 option)
   - Publish to Kaltura/Panopto → Only residents + mentors get access (role-based)
   - Access logged for audit: "Dr. Smith viewed Procedure #4521 on 2026-04-10 at 14:23 PST"
4. **SUMMARIZE:** "Your surgical recordings are HIPAA-safe, taught to the right people, and audit-ready for CMS inspections."
5. **NEXT STEPS:** HIPAA legal review (2 weeks), pilot 1 OR, then scale to training library

**Key Questions During Demo:**
- "Do you have a HIPAA compliance officer?" (→ MEDDIC EB)
- "Which LMS is your single source of truth?" (→ Integration validation)
- "How many simultaneous OR recordings?" (→ Pearl-2 vs. multi-Pearl architecture)

**Competitive Displacement:**
- vs. Teradek: "Teradek cloud-only doesn't meet on-prem HIPAA requirements for some practices. Pearl offers both."
- vs. Blackmagic: "Blackmagic + separate cloud recorder + LMS integration = 3 vendors. Pearl is one unified platform."

---

#### **Houses of Worship (70 ICP Score)**
*Vertical DNA: Live streaming (YouTube/Facebook), multi-camera (altar, choir, audience), easy operation (no tech crew), low latency*

**Demo Arc:**
1. **RECAP:** "You stream Sunday services to YouTube, have 3-4 camera angles, and no dedicated AV person to operate complex gear."
2. **AGENDA:** Pearl Mini 3-camera setup → One-click stream to YouTube/Facebook → RTMP automation → Compare to vMix/OBS complexity
3. **SHOW VALUE:**
   - 3 Pearl cameras (front center, choir, audience side) → One Pearl-2 as router/recorder
   - Pastor or volunteer hits "STREAM" button (literally one button, labeled in big text)
   - Live on YouTube (1080p60) + recorded to Pearl for archives
   - Pause, resume—no dropped frames, no re-buffering
   - Compare: vMix requires PC operator, scene switching, OBS requires technical setup—pastors can't do it
4. **SUMMARIZE:** "Your church streams live every week with zero technical staff, archives everything, and reaches your whole congregation online."
5. **NEXT STEPS:** Try a 1-camera test, then add 3-camera setup for next service

**Key Questions During Demo:**
- "Who operates your current setup?" (→ Identify if volunteer or staff, MEDDIC User Champion)
- "How many YouTube subscribers?" (→ Scale readiness)
- "Do you record for archives?" (→ Validate all-in-one Pearl value prop)

**Competitive Displacement:**
- vs. vMix (PC software): "vMix requires a Windows operator who knows OBS/vMix; Pearl is one button for volunteers."
- vs. Blackmagic (requires control): "Blackmagic needs an AV technician; houses of worship don't have that. Pearl is pastor-proof."

---

#### **K-12 Education (65 ICP Score)**
*Vertical DNA: Classroom recording, easy teacher operation, LMS integration (Kaltura, Panopto, YuJa, Echo360, Opencast), district management*

**Demo Arc:**
1. **RECAP:** "Your teachers record lessons, publish to your LMS, and your district IT wants one management platform for all 50+ classrooms."
2. **AGENDA:** Pearl Mini in classroom → Teacher hits REC → Auto-publishes to Opencast/Echo360 → Epiphan Connect district dashboard
3. **SHOW VALUE:**
   - Pearl Mini mounted above whiteboard (or podium camera + screen share)
   - Teacher walks in, hits big REC button (red button, child-proof interface)
   - Lesson records, automatically publishes to Opencast with metadata (class, date, teacher name)
   - Students access recording in LMS within 2 minutes (Pearl auto-transcodes)
   - IT admin logs into Epiphan Connect → sees 50 classrooms, battery levels, storage, any issues
   - District pivot: Instead of Extron + Crestron + separate recorders in each school, one Pearl per room, one cloud platform
4. **SUMMARIZE:** "Your teachers teach, not troubleshoot. Your IT manages one dashboard instead of 50 different devices. Your students get lessons recorded automatically."
5. **NEXT STEPS:** Pilot 5 classrooms in 1 school, measure teacher adoption + IT time saved, then district rollout

**Key Questions During Demo:**
- "Which LMS is your district standard?" (→ Integration validation)
- "Who's your IT director?" (→ MEDDIC EB/Economic Buyer ID)
- "How many classrooms total?" (→ Scaling architecture)
- "Do teachers have any training now?" (→ User Champion readiness)

**Competitive Displacement:**
- vs. Extron (SMP discontinued): "Extron SMP is EOL. Pearl is your modern upgrade with cloud management."
- vs. Blackmagic: "Blackmagic requires operators; K-12 teachers won't do it. Pearl is one-button recording."
- vs. vMix: "vMix needs Windows PCs in every classroom; Pearl is one appliance, no PC overhead."
