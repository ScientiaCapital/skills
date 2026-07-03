#!/usr/bin/env python3
# SDR Dial Lists engine — classify, dedupe, derive state, rank, build top-50 per SDR + ASCII notes.
import sys, re, json
sys.path.insert(0,'/sessions/great-zen-curie/mnt/epiphan-mcp-guide')
sys.path.insert(0,'/sessions/great-zen-curie/mnt/outputs/data')
import data_raw as D
import areacodes as AC

TODAY="2026-06-18"
BOOK_URL="meetings.hubspot.com/timkipper/discovery-call"
STUDY="study-app-flax.vercel.app/killer-questions"

# ---------- vertical classification ----------
HE_INDS={"higher_education","higher education","education_management","education management","primary/secondary education"}
LE_INDS={"entertainment","events_services","events services","media_production","media production","performing arts"}
# Out-of-scope industries we must DROP per scope lock (broadcast PBS, film/post, online media)
OOS_INDS={"broadcast media","motion pictures and film","online media","research"}

def vertical(ind, company, title):
    i=(ind or "").lower().strip()
    if i in HE_INDS: return "Higher Ed"
    if i in LE_INDS: return "Live Events"
    return None  # out of scope

ICP={"Higher Ed":90,"Live Events":85}

# ---------- ATL / BTL classification (from persona intel) ----------
# ATL = Manager/Director/Head of AV, Media Services, Classroom/Instructional/Academic Technology,
#       Online/Digital Learning (Panopto admin), or senior production/ops leadership in Live Events.
# BTL = Coordinator/Technologist/Specialist/Engineer/Technician booking layer.
ATL_RE=re.compile(r"\b(director|dir\.|head|chief|vp|vice president|avp|a\.v\.p|executive director|exec dir|manager|mgr|supervisor|associate director|assoc dir|cto|cio|founder|owner|president)\b",re.I)
BTL_RE=re.compile(r"\b(coordinator|technologist|specialist|technician|analyst|engineer|support|producer|operator|lead\b)",re.I)
# Strong ATL AV/media titles = top of book (44% progression)
TOPATL_RE=re.compile(r"(av|a/v|audio.?visual|media services|media production|classroom tech|classroom service|learning space|instructional tech|academic tech|educational media|media systems|media support|media and information|digital classroom|video.{0,3}production|video & network|production services|production director|technical director|broadcast operations|head of technology)",re.I)
PANOPTO_ADMIN_RE=re.compile(r"(online learning|digital learning|academic technolog|instructional design|teaching and learning|ed ?tech|distance|ecampus)",re.I)
# Pure-IT (deprioritize per intel: IT-first cold motion stalls without active AV project)
PUREIT_RE=re.compile(r"(it |information technology|infrastructure|service desk|systems|network|security|enterprise software|enterprise systems|service management|identity|application manager|data )",re.I)

# ---------- HARD EXCLUDE: gatekeeper / off-persona titles (Tim 2026-06-19) ----------
# These titles are dropped entirely BEFORE ranking. Per Tim's YTD evidence:
#  - IT C-suite, IT VP/Director, Network, Security, Service Desk = gatekeepers, slow deals
#    with security/IT review, zero hardware ownership.
#  - Faculty (Lecturer, Professor, Instructor, Adjunct) = zero deals YTD.
#  - Pure C-suite at non-AV vendors (CinemaCloudWorks CTO, Telestream CTO) = partner-talk,
#    not outbound dial.
# Domain exemption: if the account has an OPEN AV-tagged deal (passed in via
# AV_DEAL_DOMAINS), exclusion is bypassed — IT may legitimately own the project.
HARD_EXCLUDE_TITLE_RE = re.compile(
    r"\b("
    # C-suite IT (no Pearl ownership at this altitude)
    r"cio|cto|chief information officer|chief technology officer|chief technical officer|"
    r"chief digital officer|chief security officer|ciso|"
    # VP / Sr Dir of IT (gatekeeper layer)
    r"vp information technology|vice president information technology|vp of information technology|"
    r"vp it|vp of it|vp, it|svp it|svp information technology|"
    r"sr director of it|senior director of it|sr dir of it|"
    r"vp infrastructure|vp network|vp security|"
    # Director of IT/Information Technology (without AV ownership)
    r"director of it|director of information technology|director, information technology|"
    r"director it|it director|director of infrastructure|director, infrastructure|"
    r"director of distributed systems|director of computing|executive director of it|"
    r"executive director, it|exec director of it|director of it services|"
    # Network
    r"network engineer|network analyst|network architect|network administrator|"
    r"network director|director of network|director, network|network operations|"
    r"network manager|head of network|sr network|senior network|network technician|"
    r"director of network operations|"
    # Security
    r"information security|it security|cybersecurity|cyber security|"
    r"security analyst|security engineer|security manager|director of security|"
    r"director, security|director of information security|infosec|"
    # Service desk / help desk
    r"service desk|help desk|helpdesk|it support|it service|"
    # Systems (administrator, NOT 'media systems' which is AV)
    r"systems administrator|sysadmin|systems engineer iii|"
    # Faculty / academic (zero deals YTD)
    r"lecturer|professor|adjunct|instructor in|teaching assistant|"
    r"dean|provost|department chair|"
    # IT project mgmt
    r"it project manager|director of it project|"
    # Library systems
    r"library it|head of library it|library systems|"
    r")\b",
    re.I,
)

# AV-deal domain exemption set. Populate from HubSpot before each build run via
# hubspot_search_deals filtered to open deals with AV/Pearl/Nexus/EC20 keywords.
# Empty by default = strict exclude. Override-safe so a known IT-owner with an open
# Pearl project (rare) isn't dropped.
AV_DEAL_DOMAINS = set()  # e.g. {"uiuc.edu", "umb.edu", "brooklynpubliclibrary.org"}

# Generic over-vague Director / Coordinator at non-AV firms — drop unless they have an
# AV/Media/Production/Broadcast keyword in their title.
GENERIC_DIRECTOR_RE = re.compile(r"^\s*(director|managing director|associate director|assistant director|coordinator|lead project coordinator)\s*$", re.I)
AV_KEYWORD_RE = re.compile(r"(av|a/v|audio.?visual|media|broadcast|production|video|classroom|instructional|academic tech|learning|panopto|kaltura|encore|nexus|pearl)", re.I)

def hard_exclude(title, domain=""):
    """Return True if title is hard-excluded (gatekeeper / faculty / generic). Domain
    exemption: known AV-deal domains bypass the IT/network filter."""
    t = (title or "").strip()
    if not t:
        return True  # blank titles never make the queue
    dom = (domain or "").lower().strip()
    # Domain exemption only protects from IT/network filter — not from faculty/generic.
    if HARD_EXCLUDE_TITLE_RE.search(t):
        if dom and dom in AV_DEAL_DOMAINS:
            return False  # IT owner of an open AV project — allowed through
        return True
    # Generic Director/Coordinator with no AV-related keyword anywhere in the title.
    if GENERIC_DIRECTOR_RE.search(t) and not AV_KEYWORD_RE.search(t):
        return True
    return False

def power(title):
    t=(title or "")
    is_atl = bool(ATL_RE.search(t))
    is_btl = bool(BTL_RE.search(t))
    # Director/Manager beats the BTL keyword if both present (e.g. "Manager ... Engineer")
    if is_atl: return "ATL"
    if is_btl: return "BTL"
    return "BTL"  # default unknown -> BTL booking layer

def title_score(title, vert):
    """Persona-intel conversion weight. Higher = better."""
    t=(title or "")
    s=0
    if TOPATL_RE.search(t): s+=50          # the title that converts (AV/Media Manager-Director)
    if PANOPTO_ADMIN_RE.search(t): s+=30   # Panopto-admin ATL (Discovery-stall fix)
    if ATL_RE.search(t): s+=20
    if PUREIT_RE.search(t) and not TOPATL_RE.search(t): s-=12  # pure IT, no AV title -> dead-end risk
    if BTL_RE.search(t) and not ATL_RE.search(t): s-=4
    return s

# ---------- build unified records ----------
def mkrec(row, source):
    cid,fn,ln,title,company,phone,email,state_raw,ind,dom,last_act=row[:11]
    # derive state from phone area code; fall back to state_raw if it's a 2-letter or known
    ph_state=AC.state_from_phone(phone)
    is_ca=AC.is_ca(phone)
    # choose displayed state: prefer phone-derived (reliable); else cleaned raw
    st=ph_state
    raw=(state_raw or "").strip()
    if not st:
        # raw may be full name; keep if looks like a US state / province
        st=raw if raw and raw.lower() not in ("select your state","") else ""
    country = "CA" if is_ca else ("US" if ph_state else ("CA" if raw.lower() in ("ontario","quebec","alberta","british columbia","manitoba","saskatchewan","nova scotia","new brunswick","newfoundland") else "US"))
    vert=vertical(ind,company,title)
    return {
      "cid":cid,"name":f"{fn} {ln}".strip(),"fn":fn,"ln":ln,"title":title,"company":company,
      "phone":phone,"email":email,"state":st,"phone_state":ph_state,"state_raw":raw,
      "country":country,"industry":ind,"domain":dom,"last_act":last_act,
      "vertical":vert,"power":power(title),"tscore":title_score(title,vert),"source":source,
    }

def clean(rows):
    out=[]
    for r in rows:
        if r[0] in ("171969999999",): continue
        t=(r[3] or "").lower()
        if t=="placeholder" or "dup" in (r[4] or "").lower() or r[1]=="Ben": continue
        if r[2] in ("Goodwin2","Stavrou2","Wallace2"): continue  # explicit dup guards
        out.append(r)
    return out

owned=[mkrec(r,"owned") for r in clean(D.EDGAR_OWNED)]
GF_ALL = clean(D.GREENFIELD) + clean(getattr(D,"GREENFIELD_US_ADD",[]))
gf=[mkrec(r,"greenfield") for r in GF_ALL]

# drop out-of-scope verticals (broadcast/film/online media)
def in_scope(r): return r["vertical"] in ("Higher Ed","Live Events")
owned_scope=[r for r in owned if in_scope(r)]
owned_oos=[r for r in owned if not in_scope(r)]
gf_scope=[r for r in gf if in_scope(r)]

print("=== SCOPE FILTER ===")
print(f"Edgar owned: {len(owned)} -> in-scope {len(owned_scope)}, dropped OOS {len(owned_oos)}")
for r in owned_oos: print(f"  DROP(OOS) {r['name']} | {r['company']} | {r['industry']}")
print(f"Greenfield: {len(gf)} -> in-scope {len(gf_scope)}")

# dedupe greenfield by cid and by (lastname+domain) and drop anything already in owned
owned_cids={r["cid"] for r in owned}
seen=set(); gf_dedup=[]
for r in sorted(gf_scope,key=lambda x:(-x["tscore"],x["last_act"]),reverse=False):
    key=(r["ln"].lower(),r["domain"].lower())
    if r["cid"] in owned_cids or r["cid"] in seen or key in seen: continue
    seen.add(r["cid"]); seen.add(key); gf_dedup.append(r)
print(f"Greenfield after dedupe: {len(gf_dedup)}")

# ---------- ranking ----------
def rank_key(r):
    # Tier: callbacks(0) > owned ATL(1) > owned BTL(2) > greenfield(3)
    if r["source"]=="owned":
        tier = 1 if r["power"]=="ATL" else 2
    else:
        tier = 3
    # US-weight: US ahead of CA (Tim's instruction)
    us = 0 if r["country"]=="US" else 1
    # within tier: US first, then ICP desc, then title_score desc, then ATL>BTL, then recency desc
    return (tier, us, -ICP.get(r["vertical"],0), -r["tscore"], 0 if r["power"]=="ATL" else 1, _negdate(r["last_act"]))

def _negdate(d):
    # for DESC recency: invert string date
    return tuple(-int(x) for x in d.split("-"))

owned_ranked=sorted(owned_scope,key=rank_key)
gf_ranked=sorted(gf_dedup,key=rank_key)

# ---------- assemble per SDR ----------
# Edgar: owned first, then greenfield fill to 50. Vasil: all greenfield (ramping), ATL-first.
CAP=50

# Split greenfield between the two SDRs so they never overlap.
# Edgar gets the fill he needs after owned; Vasil gets a US-weighted ATL-first slice from the rest.
edgar=list(owned_ranked)
need_edgar=CAP-len(edgar)
edgar_fill=gf_ranked[:max(0,need_edgar)]
rest=gf_ranked[max(0,need_edgar):]
for r in edgar_fill: r["fill"]=True
edgar=edgar+edgar_fill

# Vasil: from 'rest', US-FIRST (Tim's instruction), then ATL-first, then ICP/title/recency (ramping rule).
# US weighting dominates so his queue is US-majority; CA only fills the tail if US runs out.
def vasil_key(r):
    us=0 if r["country"]=="US" else 1
    return (us, 0 if r["power"]=="ATL" else 1, -ICP.get(r["vertical"],0), -r["tscore"], _negdate(r["last_act"]))
vasil=sorted(rest,key=vasil_key)[:CAP]
for r in vasil: r["fill"]=True

print("\n=== QUEUE SIZES ===")
print(f"Edgar: {len(edgar)} (owned {len(owned_ranked)} + fill {len(edgar_fill)})")
print(f"Vasil: {len(vasil)} (all greenfield, ramping)")
us_e=sum(1 for r in edgar if r['country']=='US'); us_v=sum(1 for r in vasil if r['country']=='US')
print(f"US weighting -> Edgar {us_e}/{len(edgar)} US, Vasil {us_v}/{len(vasil)} US")

# vertical + power mix
from collections import Counter
def mix(q,label):
    print(f"\n{label} vertical: {dict(Counter(r['vertical'] for r in q))}")
    print(f"{label} power: {dict(Counter(r['power'] for r in q))}")
    print(f"{label} country: {dict(Counter(r['country'] for r in q))}")
mix(edgar,"Edgar"); mix(vasil,"Vasil")

# Save assembled queues
out={"date":TODAY,"edgar":edgar,"vasil":vasil,"owned_oos":owned_oos}
json.dump(out,open('/sessions/great-zen-curie/mnt/outputs/data/queues.json','w'),indent=1)
print("\nSaved queues.json")
