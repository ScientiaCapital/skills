#!/usr/bin/env python3
# Build ASCII Nooks/HubSpot notes per contact, spec-accurate, from the call playbook + study-app killer-questions.
import json, re
q=json.load(open('/sessions/great-zen-curie/mnt/outputs/data/queues.json'))
BOOK="meetings.hubspot.com/timkipper/discovery-call"
STUDY="study-app-flax.vercel.app/killer-questions"

# ---------- discovery (study-app killer-questions, canonical 3-step) ----------
DISCO={
"Higher Ed":[
 "What's the biggest challenge with lecture capture and classroom recording right now that, if it's still broken a year from now, would really hurt faculty adoption or student access?",
 "What's happening on campus that's making reliable capture across all your rooms such a priority this year? (and where it fits: what's your MediaSite / Seneca / Echo360 exit plan?)",
 "If every room just recorded and published to your CMS or LMS without IT touching it, what would that free your AV team up to do?",
],
"Live Events":[
 "What's the biggest risk in your live production workflow right now that, if it went wrong on a major show, would really damage the client relationship or your reputation?",
 "What's driving the pressure to make every stream rock-solid right now?",
 "If you never had to worry about a dropped feed or a failed multi-camera switch mid-event, what bigger work could your team take on?",
],
}

# ---------- teach (Challenger, 1-line vertical) ----------
TEACH={
"Higher Ed":"On most campuses the real cost isn't the gear, it's that recording still needs an AV person physically in the room to press start, so faculty just stop recording.",
"Live Events":"The pattern we see is software encoders like vMix or OBS crashing under sustained load mid-event, and every event still needs a skilled operator on-site, which caps how many you can run at once.",
}

# ---------- openers ----------
def opener(r):
    sr=r['power']; t=r['title'].lower()
    senior = bool(re.search(r"(vp|vice president|chief|cio|cto|avp|director|head|executive|dean)",t))
    if senior:
        return ("Pattern-interrupt (senior): \"Hi "+r['fn']+", Tim's team at Epiphan. This is a sales call, "
                "but a quick and relevant one if you run video capture or streaming for "
                +("your campus" if r['vertical']=="Higher Ed" else "your productions")+". Worth 30 seconds?\"")
    return ("Permission: \"Hey "+r['fn']+", it's [SDR] with Epiphan Video. I know I'm calling out of the blue, "
            "can I take 30 seconds to tell you why, and you can tell me to buzz off if it's not relevant?\"")

# ---------- talking points (VERIFIED spec bank only) ----------
# Verified 2026-06-18 via Epiphan AI search_product_knowledge. EC20 uses DOCUMENTED phrasing
# (native Panopto Remote Recorder integration) -- not the unconfirmed 'world-first certified' claim.
TP={
"Higher Ed":[
 "Pearl Nexus: 1RU rackmount, up to 3 simultaneous 1080p30 channels; registers as a Panopto / Kaltura / YuJa remote recorder for hands-off lecture capture (inputs incl. NDI|HX, not full NDI).",
 "EC20 PTZ: 4K AI auto-tracking camera with native Panopto Remote Recorder integration, records direct to Panopto with no separate encoder; managed via Epiphan Edge.",
 "Epiphan Edge: monitor, update firmware, and remote-access every Pearl and EC20 across all campus rooms from one dashboard, no truck-roll per room.",
],
"Live Events":[
 "Pearl-2: up to 6 simultaneous 1080p30 channels for record/stream, live-switch up to 5, multi-streams to 50+ endpoints. Dedicated hardware, not a laptop that crashes under load.",
 "Inputs: HDMI, SDI, RTSP, SRT, full NDI and NDI|HX, web graphics; SRT for rock-solid feeds over unmanaged networks.",
 "Epiphan Edge: manage every encoder across venues/sites from one dashboard instead of sending an operator to each location.",
]
}

# ---------- multithread logic ----------
# Build per-account contact maps to name the ATL to thread up to / BTL champions to pull in.
from collections import defaultdict
ALL = {"edgar":q['edgar'],"vasil":q['vasil']}
def account_map(rows):
    m=defaultdict(list)
    for r in rows: m[r['company']].append(r)
    return m

# Known ATL anchors per famous account (for multithread naming even when only 1 in queue)
def multithread(r, amap):
    same=[x for x in amap[r['company']] if x['cid']!=r['cid']]
    atls=[x for x in same if x['power']=="ATL" and re.search(r"(av|media|classroom|instructional|video|production|technical director)",x['title'],re.I)]
    btls=[x for x in same if x['power']=="BTL"]
    if r['power']=="BTL":
        if atls:
            a=atls[0]; return f"You're a booking-layer contact. Thread UP to {a['name']} ({a['title']}) on this same account = the economic buyer. Never run this account on your thread alone."
        return ("BTL booking layer. Thread UP to the AV / Media Services / Instructional Tech Manager or Director "
                "(or Director of Online/Academic Technology = the Panopto admin) before this stalls at Discovery.")
    else:
        # ATL
        if r['company']=="College of Charleston":
            return "ATL. Robert Keller (AV Manager) + Allen Ellis (Dir Video & Network Production) own the AV stack here. Pull in one BTL classroom tech to validate room count."
        if btls:
            b=btls[0]; return f"ATL economic buyer. Pull in {b['name']} ({b['title']}) as hands-on champion to validate the workflow."
        if re.search(r"(it|information technology|infrastructure|enterprise|network|security|systems)",r['title'],re.I) and not re.search(r"(av|media|classroom|instructional)",r['title'],re.I):
            return "ATL on the IT side. Thread ACROSS to whoever owns AV / classroom capture + the Panopto/LMS admin; IT-only deals stall without the AV owner engaged."
        return "ATL. Identify and pull in the hands-on classroom/AV technologist as your champion to validate the room count."

# ---------- why-now ----------
def whynow(r):
    src = "OWNED" if r['source']=="owned" else "GREENFIELD (RAMPING FILL)" if False else "GREENFIELD"
    base = f"Last activity {r['last_act']}."
    if r['source']=="owned":
        return f"Owned, in your book. {base} Re-engage on the open thread."
    if r['vertical']=="Higher Ed" and re.search(r"(it|information technology|infrastructure|enterprise|network|security|systems|application)",r['title'],re.I) and not re.search(r"(av|media|classroom|instructional)",r['title'],re.I):
        return f"Fresh greenfield HE IT leader. {base} Lead with the legacy lecture-capture EOL wedge (MediaSite / Seneca / Echo360 exit plan)."
    return f"Fresh greenfield, active in last 90 days. {base} ATL decision-maker, open cold with the vertical teach."

# ---------- assemble ASCII note ----------
def power_label(r): return "ATL" if r['power']=="ATL" else "BTL"
def src_label(r,ramping):
    if r['source']=="owned": return "OWNED"
    return "GREENFIELD (RAMPING FILL)" if ramping else "GREENFIELD"

def build_note(r, amap, ramping):
    d=DISCO[r['vertical']]; tp=TP[r['vertical']]
    note=[]
    note.append(f"=== {r['name']} · {r['company']} ===")
    note.append(f"{r['vertical']} | {power_label(r)} | {src_label(r,ramping)}")
    note.append("")
    note.append("--- WHY NOW ---")
    note.append(whynow(r))
    note.append("")
    note.append("--- OPENER ---")
    note.append(opener(r))
    note.append("")
    note.append("--- TEACH (Challenger) ---")
    note.append(TEACH[r['vertical']])
    note.append("")
    note.append("--- TALKING POINTS (spec-verified) ---")
    for p in tp: note.append("- "+p)
    note.append("")
    note.append("--- DISCOVERY (study-app killer-questions) ---")
    for i,qq in enumerate(d,1): note.append(f"{i}. {qq}")
    note.append("")
    note.append("--- MULTITHREAD ---")
    note.append(multithread(r,amap))
    note.append("")
    note.append("--- NEXT STEP ---")
    note.append("Book 20-min discovery w/ Phil or Lex:")
    note.append(BOOK)
    note.append("Study: "+STUDY)
    return "\n".join(note)

for who,rows in ALL.items():
    amap=account_map(rows)
    ramping = (who=="vasil")
    for r in rows:
        r['note']=build_note(r,amap,ramping)

json.dump(q,open('/sessions/great-zen-curie/mnt/outputs/data/queues_noted.json','w'),indent=1)
print("Notes built for", len(q['edgar']),"Edgar +",len(q['vasil']),"Vasil")
print("\n----- SAMPLE: Edgar #3 (Robert Keller, AV Manager, CofC) -----\n")
print(q['edgar'][2]['note'])
print("\n----- SAMPLE: Vasil #1 (Sonya Zuker, VP IT) -----\n")
print(q['vasil'][0]['note'])
