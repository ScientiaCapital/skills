# Nooks Signals v1 — Epiphan (paste-ready)
**Owner:** Tim Kipper | **Date:** 2026-06-13 | **Scope:** Additive — fill the 2 open Premium slots + add Free signals. Do NOT touch the 8 Basic signals or the existing "CMS Usage/Panopto" Premium.

## Why this build
- Premium = the only tier with **complex multi-source LLM search**, and it's sitting at **1/3 used**.
- Basic is **maxed (8/8)** with 4 "Prior Convo" re-engagement variants — leave it alone.
- Free = **no LLM, filter-based, abundant** — never competes for Basic budget, so max it out.
- Strongest "why now" Epiphan owns (not yet a signal): **Matrox exited the capture market** + **Extron SMP discontinued** = *forced* replacement (2026 Higher Ed AV Survey: 36+ P0 accounts).

## Tier budget after this build
| Tier | Limit | Used after build |
|---|---|---|
| Premium | 3 | 3/3 (Panopto existing + 2 new below) |
| Basic | 8 | 8/8 (unchanged) |
| Free | abundant | +6 |

---

# PREMIUM #2 — "Legacy Capture HW (Matrox/Extron SMP)" 🔥
**Click path:** Create signal → **Start from scratch** → **Account signal** → Type: *Uses Competitor / Tech Usage* (closest available) → Category: **Hot Account Signals** → paste Description + prompt → Save.

**Description:**
`Account runs discontinued/EOL capture hardware (Matrox, Extron SMP, Mediasite, Seneca). Forced-replacement window — strongest "why now."`

**LLM prompt:**
```
Determine whether this organization currently operates — or recently standardized on — video
capture or lecture-capture hardware that is now end-of-life, discontinued, or from a vendor that
exited the capture market. Look specifically for:
- Matrox capture cards/appliances (Matrox exited the dedicated capture market — unsupported going forward)
- Extron SMP series recorders (SMP 111/351/etc. — discontinued by Extron)
- Sonic Foundry Mediasite capture appliances (legacy; modernization candidates)
- Seneca lecture-capture systems / aging custom capture PCs used as recorders

Search: IT/AV "standards" or "supported equipment" pages, classroom/room technology docs, job
postings naming these products, RFPs and bid documents, public procurement records, AV community
forum posts, and case studies.

Return TRUE only with concrete evidence — name the specific product detected and cite the source.
This is highest priority because the replacement is forced (vendor exited / discontinued the line),
not discretionary. Prioritize higher-education, government/court, and AV-heavy organizations.
```

---

# PREMIUM #3 — "Competing Capture/Production Tech"
**Click path:** Create signal → **Start from scratch** → **Account signal** → Type: *Uses Competitor / Tech Usage* → Category: **Account Insights** *(switch to Hot Account if you want it weighted as urgency)* → paste → Save.

**Description:**
`Competing capture/switching/streaming tech in use + the Epiphan displacement angle (incl. software/PC capture + Windows fragility).`

**LLM prompt:**
```
Identify whether this organization uses video capture, live-production, or streaming technology
that competes with Epiphan, and classify the displacement angle. Look for:
- Hardware switchers/encoders: Blackmagic Design ATEM, NewTek/Vizrt TriCaster, AJA, Matrox, Magewell
- Software/PC capture & production: OBS, vMix, Wirecast, or a custom Windows PC acting as the
  recorder/encoder — flag any mention of Windows updates breaking recordings, "patch Tuesday"
  disruption, or recorder-reliability problems (strongest pain angle)
- Lecture-capture / video CMS: Kaltura, Echo360, YuJa, Mediasite, Opencast (Epiphan hardware feeds
  these as a remote recorder, so this is fit + displacement of their capture layer)

Search job postings, AV/IT documentation, room standards, case studies, social posts, forums.
Return TRUE with: the specific tech detected, the source, and a one-line displacement angle, e.g.
"OBS on a Windows PC for lecture capture → Pearl one-touch/reliability pitch" or
"ATEM + laptop rig → Pearl Mini all-in-one." Exclude orgs already standardized on Epiphan Pearl
with no competing capture layer.
```

**No overlap, by design:** existing Premium = *video-CMS platform (Panopto)* · #2 = *dead/discontinued capture hardware* (Hot, forced) · #3 = *all other live competing tech* (insight/angle).

---

# FREE LAYER (no LLM — add/activate; zero Basic-budget cost)

| # | Signal | Target | Category | Config |
|---|---|---|---|---|
| F1 | **ICP Org Match** | Account | 🎯 ICP Fit | Industry = Higher Ed, Gov/Municipal, Legal/Courts, Healthcare, Religious Orgs, Broadcast/Media, Events/Hospitality + employee-size band |
| F2 | **Has Relevant Job Titles** | Account/Prospect | 🎯 ICP Fit | Titles from `nooks-personas-v2.md`: AV Director, Media Services Director, Classroom Technology Manager, Lecture Capture Administrator, Panopto Administrator, Broadcast Engineer, Worship Tech Director, Court Technology Coordinator, … |
| F3 | **New Leadership Hire — AV/IT/Media** | Account/Prospect | 🔥 Hot | Finalize your existing **(draft)**; scope to AV/Media/IT director titles, last 90 days |
| F4 | **>10% Headcount Growth** | Account | 🔥 Hot | Free template as-is (expansion → new facilities → capture need) |
| F5 | **Hiring for AV/Video/Streaming Roles** | Account | Account Insights | "Hiring for X/Y/Z Roles"; X/Y/Z = AV Technician, Video Engineer, Streaming Specialist, Lecture Capture, Media Operations |
| F6 | **Mentions Streaming/Lecture-Capture/Hybrid in JD** | Account | Account Insights | "Mentions X/Y/Z in JD"; keywords = lecture capture, livestream, hybrid/HyFlex, Panopto, Kaltura, broadcast, video production |

---

# RANK ORDER (drag only the NEW signals in; leave existing relative order)
1. Legacy Capture HW (Matrox/Extron SMP) — Premium 🔥 *(new)*
2. CMS Usage / Panopto — Premium *(existing)*
3. New Leadership Hire — AV/IT/Media — Free 🔥 *(finalize draft)*
4. >10% Headcount Growth — Free 🔥 *(new)*
5. Competing Capture/Production Tech — Premium *(new)*
6. *(existing Basic re-engagement signals keep current order)*
7. ICP Org Match / Has Relevant Job Titles — Free 🎯 *(new)*
8. Hiring for AV roles / Mentions … in JD — Free Insights *(new)*

---

# VERIFY (Nooks **Preview** pane → Select accounts → **Run**)
Ground-truth from the Higher Ed survey:
- **Legacy Capture HW must FIRE:** Northwestern (Matrox), Santa Clara (Pearl+Matrox+Extron SMP), Tennessee State (Extron+Matrox), Humber College (Matrox), U of Alaska (Extron SMP), Notre Dame (Extron+Seneca+PC).
- **Competing Tech must FIRE:** CUNY (custom PC), U of Toronto (custom PC), Boise State (PC), Calgary Board of Education (Blackmagic).
- **CMS/Panopto** must FIRE on Panopto/Kaltura users.
- **False-positive check:** Pearl-only accounts (~42) must NOT fire EOL/Competing-Tech.
- After 1 week of dials: re-check hit-rate; tighten any prompt that over/under-fires.
