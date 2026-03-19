#!/usr/bin/env python3
"""Generate Tim's Daily Operations Guide PDF."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether
)
from reportlab.platypus.flowables import HRFlowable
from datetime import datetime
import os

# Epiphan brand colors
DARK = HexColor("#1a1a2e")
PRIMARY = HexColor("#0f3460")
ACCENT = HexColor("#e94560")
LIGHT_BG = HexColor("#f0f4f8")
WHITE = white
GRAY = HexColor("#6b7280")
LIGHT_GRAY = HexColor("#e5e7eb")
GREEN = HexColor("#059669")
YELLOW = HexColor("#d97706")
RED = HexColor("#dc2626")
BLUE = HexColor("#2563eb")

OUTPUT = os.path.expanduser("~/Desktop/Tim_Daily_Operations_Guide.pdf")
TODAY = datetime.now().strftime("%B %d, %Y")

def build_styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        'CoverTitle', parent=styles['Title'],
        fontSize=28, textColor=WHITE, alignment=TA_CENTER,
        spaceAfter=6, fontName='Helvetica-Bold'
    ))
    styles.add(ParagraphStyle(
        'CoverSub', parent=styles['Normal'],
        fontSize=14, textColor=HexColor("#94a3b8"), alignment=TA_CENTER,
        spaceAfter=4
    ))
    styles.add(ParagraphStyle(
        'SectionHead', parent=styles['Heading1'],
        fontSize=18, textColor=PRIMARY, fontName='Helvetica-Bold',
        spaceBefore=16, spaceAfter=8,
        borderWidth=0, borderColor=ACCENT, borderPadding=4,
    ))
    styles.add(ParagraphStyle(
        'SubHead', parent=styles['Heading2'],
        fontSize=13, textColor=DARK, fontName='Helvetica-Bold',
        spaceBefore=10, spaceAfter=4
    ))
    styles.add(ParagraphStyle(
        'Body', parent=styles['Normal'],
        fontSize=9, textColor=DARK, leading=13
    ))
    styles.add(ParagraphStyle(
        'BodySmall', parent=styles['Normal'],
        fontSize=8, textColor=GRAY, leading=11
    ))
    styles.add(ParagraphStyle(
        'Trigger', parent=styles['Normal'],
        fontSize=8, textColor=PRIMARY, fontName='Courier',
        leading=11, leftIndent=12
    ))
    styles.add(ParagraphStyle(
        'AccentText', parent=styles['Normal'],
        fontSize=10, textColor=ACCENT, fontName='Helvetica-Bold'
    ))
    styles.add(ParagraphStyle(
        'TableHeader', parent=styles['Normal'],
        fontSize=8, textColor=WHITE, fontName='Helvetica-Bold',
        alignment=TA_CENTER
    ))
    styles.add(ParagraphStyle(
        'TableCell', parent=styles['Normal'],
        fontSize=8, textColor=DARK, leading=10
    ))
    styles.add(ParagraphStyle(
        'TableCellCenter', parent=styles['Normal'],
        fontSize=8, textColor=DARK, leading=10, alignment=TA_CENTER
    ))
    return styles

def make_table(headers, rows, col_widths=None):
    """Create a styled table."""
    s = build_styles()
    header_row = [Paragraph(h, s['TableHeader']) for h in headers]
    data = [header_row]
    for row in rows:
        data.append([Paragraph(str(c), s['TableCell']) for c in row])

    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('BACKGROUND', (0, 1), (-1, -1), WHITE),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, LIGHT_BG]),
        ('GRID', (0, 0), (-1, -1), 0.5, LIGHT_GRAY),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    return t

def hr():
    return HRFlowable(width="100%", thickness=1, color=LIGHT_GRAY, spaceAfter=6, spaceBefore=6)

def page1_cover(story, s):
    """Cover + Quick Start"""
    story.append(Spacer(1, 1.5*inch))

    # Title block with background
    story.append(Paragraph("Tim's Daily Operations Guide", s['CoverTitle']))
    story.append(Paragraph("BDR Playbook  |  Epiphan Video", s['CoverSub']))
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph(f"Generated: {TODAY}  |  67 Skills  |  7 MCP Servers  |  90+ Tools", s['CoverSub']))
    story.append(Spacer(1, 0.5*inch))

    story.append(hr())
    story.append(Paragraph("Quick Start", s['SectionHead']))
    story.append(Paragraph('Say <b>"morning brief"</b> to start your day. This runs the full pipeline:', s['Body']))
    story.append(Spacer(1, 6))

    quick_data = [
        ["Command", "What It Does"],
        ['<font color="#e94560"><b>"morning brief"</b></font>', "Run all morning workflows (deal momentum + portfolio + trading + dial list)"],
        ['"deal momentum"', "Score pipeline, flag RED/YELLOW deals"],
        ['"portfolio update"', "Attribute closed deals to skills/automations"],
        ['"market digest"', "Pre-market scan + IBKR positions"],
        ['"prep me for [Company]"', "Auto-generate MEDDIC call prep brief"],
        ['"prospect [Company]"', "End-to-end research + cadence generation"],
    ]
    t = Table(quick_data, colWidths=[2.2*inch, 4.3*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BACKGROUND', (0, 1), (-1, -1), WHITE),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, LIGHT_BG]),
        ('GRID', (0, 0), (-1, -1), 0.5, LIGHT_GRAY),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("<b>March 2026 Targets (Ramp 50%):</b> 12 deals | $357K pipeline | $125K revenue | 50+ daily dials", s['AccentText']))

def page2_timeline(story, s):
    """Morning Workflow Timeline"""
    story.append(PageBreak())
    story.append(Paragraph("Morning Workflow Timeline", s['SectionHead']))

    story.append(Paragraph("<b>MONDAY (Full Automation Chain)</b>", s['SubHead']))
    mon_data = [
        ["Time", "Skill", "What Happens"],
        ["06:00", "prospect-enrich", "Phoneless contacts -> Apollo/Clay enrichment (DEMO REQUEST first)"],
        ["06:15", "phone-waterfall", "Verify phones -> callable queue"],
        ["06:30", "prospect-refresh", "Net-new ICP search (7 verticals) + Gmail drafts"],
        ["07:00", "deal-momentum", "Score deals, flag RED/YELLOW, draft recovery emails"],
        ["07:00", "portfolio-linker", "Link closed deals -> GTME evidence"],
        ["07:00", "trading-alerts", "Pre-market scan + IBKR positions"],
        ["07:15", "sequence-load", "Auto-enroll new prospects -> Apollo sequences"],
        ["07:25", "callable-lead-count", "ATL/BTL inventory health check"],
        ["07:30", "morning-brief", "Calendar + dials + deals + drafts briefing"],
    ]
    story.append(make_table(mon_data[0], [r for r in mon_data[1:]], [0.6*inch, 1.5*inch, 4.4*inch]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>DAILY (Tuesday - Friday)</b>", s['SubHead']))
    daily_data = [
        ["Time", "Skill", "What Happens"],
        ["06:00", "prospect-enrich", "Daily phoneless enrichment (DEMO REQUEST + ATL first)"],
        ["07:00", "deal-momentum + portfolio-linker + trading-alerts", "Pipeline + portfolio + market scan"],
        ["07:25", "callable-lead-count", "ATL/BTL inventory + runway metrics"],
        ["07:30", "morning-brief", "Full daily briefing with dial list + drafts"],
    ]
    story.append(make_table(daily_data[0], [r for r in daily_data[1:]], [0.6*inch, 3.2*inch, 2.7*inch]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>ON-DEMAND (Any Time)</b>", s['SubHead']))
    ondemand_data = [
        ["Trigger", "Skill", "Use Case"],
        ['"prep me for [Company]"', "meddic-call-prep-auto", "60-second MEDDIC brief before any call"],
        ['"prospect [Company]"', "prospect-research-to-cadence", "Full research -> email -> sequence pipeline"],
        ['"deal momentum"', "deal-momentum-analyzer", "Re-run pipeline scoring + recovery actions"],
        ['"portfolio report"', "portfolio-artifact", "Weekly GTME metrics capture"],
        ['"market digest"', "trading-alert-scheduler", "Re-run pre-market scan"],
    ]
    story.append(make_table(ondemand_data[0], [r for r in ondemand_data[1:]], [2*inch, 2.2*inch, 2.3*inch]))

def page3_triggers(story, s):
    """Trigger Phrase Quick Reference"""
    story.append(PageBreak())
    story.append(Paragraph("Trigger Phrase Quick Reference", s['SectionHead']))
    story.append(Paragraph("All 67 skills organized by category. Say any trigger phrase to activate.", s['Body']))
    story.append(Spacer(1, 6))

    categories = [
        ("Core (5)", [
            ("workflow-orchestrator", '"start day", "begin session", "status check"'),
            ("cost-metering", '"cost check", "budget status", "how much spent"'),
            ("portfolio-artifact", '"capture metrics", "portfolio report", "what did I ship"'),
            ("project-context", '"load project context", "save context", "end session"'),
            ("workflow-enforcer", "Automatic on all sessions"),
        ]),
        ("BDR Automation (5)", [
            ("prospect-enrich", '"run prospect enrich", "enrich phoneless contacts"'),
            ("prospect-refresh", '"run prospect refresh", "search new ICP prospects"'),
            ("sequence-load", '"load sequences", "enroll new leads"'),
            ("callable-lead-count", '"show callable leads", "ATL runway"'),
            ("morning-brief", '"morning brief", "today\'s dial list"'),
        ]),
        ("Sales Workflow (6)", [
            ("prospect-research-to-cadence", '"research prospect", "prospect [Company]"'),
            ("phone-verification-waterfall", '"verify phones", "callable leads", "dial list"'),
            ("meddic-call-prep-auto", '"call prep", "prep me for [Company]"'),
            ("deal-momentum-analyzer", '"deal health", "pipeline review", "stalled deals"'),
            ("portfolio-deal-linker", '"portfolio update", "deal closed", "gtme evidence"'),
            ("trading-alert-scheduler", '"market digest", "pre-market scan", "trading alerts"'),
        ]),
        ("Sales Intelligence (13)", [
            ("champion-identifier", '"find champion", "internal champion"'),
            ("cold-email-sequence-generator", '"cold email sequence", "email campaign"'),
            ("contact-hunter", '"find contact info", "who works at"'),
            ("email-template-generator", '"email template", "write email"'),
            ("inbound-lead-qualifier", '"qualify inbound", "score lead"'),
            ("intent-signal-aggregator", '"intent signals", "buyer intent"'),
            ("linkedin-sales-navigator-alt", '"linkedin prospects", "sales navigator"'),
            ("lookalike-customer-finder", '"lookalike companies", "target account list"'),
            ("meeting-intelligence-system", '"meeting notes", "transcript analysis"'),
            ("personalization-at-scale", '"personalize at scale", "first lines"'),
            ("pipeline-health-analyzer", '"pipeline health", "forecast accuracy"'),
            ("sales-methodology-implementer", '"sales methodology", "implement MEDDIC"'),
            ("social-selling-content-gen", '"social selling", "LinkedIn content"'),
        ]),
        ("Strategy (5)", [
            ("business-model-canvas", '"business model", "canvas", "value proposition"'),
            ("blue-ocean-strategy", '"blue ocean", "ERRC", "strategy canvas"'),
            ("jobs-to-be-done", '"JTBD", "customer jobs", "outcome driven innovation"'),
            ("challenger-sale", '"challenger sale", "teach tailor take control"'),
            ("never-split-the-difference", '"negotiation", "tactical empathy", "ackerman"'),
        ]),
    ]

    for cat_name, skills in categories:
        story.append(Paragraph(f"<b>{cat_name}</b>", s['SubHead']))
        rows = [[sk, tr] for sk, tr in skills]
        story.append(make_table(["Skill", "Trigger Phrases"], rows, [2.2*inch, 4.3*inch]))
        story.append(Spacer(1, 6))

def page4_5_combos(story, s):
    """Skill Combinations by Use Case"""
    story.append(PageBreak())
    story.append(Paragraph("Skill Combinations by Use Case", s['SectionHead']))
    story.append(Paragraph("Chains of skills that work together for common workflows.", s['Body']))
    story.append(Spacer(1, 8))

    combos = [
        ("Start of Day", '"morning brief"',
         "prospect-enrich -> phone-waterfall -> prospect-refresh -> sequence-load -> callable-lead-count -> morning-brief",
         "Full pipeline: enrichment, verification, search, enrollment, inventory, briefing"),
        ("Prospect a Company", '"prospect [Company]"',
         "prospect-research-to-cadence -> [Apollo + Clay enrichment] -> [Gmail drafts] -> [Apollo sequence]",
         "90 min/day saved. Eliminates manual research bottleneck."),
        ("Call Prep", '"prep me for [Company]"',
         "meddic-call-prep-auto -> [HubSpot + Apollo + Clari + Calendar]",
         "60-second MEDDIC brief with deal context, prior calls, competitive intel"),
        ("Pipeline Review", '"deal momentum"',
         "deal-momentum-analyzer -> [6-signal scoring] -> [Gmail recovery drafts]",
         "Scores every deal, prescribes recovery actions, auto-drafts emails"),
        ("Research + Outreach", '"research prospect" + "cold email sequence"',
         "prospect-research-to-cadence -> cold-email-sequence-generator -> personalization-at-scale",
         "Full research -> 7-14 email sequence -> personalized first lines at scale"),
        ("Trading", '"market digest"',
         "trading-alert-scheduler -> [trading-signals + ibkr-api]",
         "Pre-market scan, regime detection, IBKR position health. 3-min read."),
        ("End of Day", '"portfolio report"',
         "portfolio-artifact -> portfolio-deal-linker -> cost-metering",
         "Capture metrics, link deals to skills, track API costs"),
        ("Strategy Deep Dive", '"JTBD analysis" or "blue ocean"',
         "jobs-to-be-done -> blue-ocean-strategy -> challenger-sale -> never-split-the-difference",
         "Full strategy chain: customer jobs -> market space -> sales methodology -> negotiation"),
        ("Debug", '"debug this"',
         "debug-like-expert -> [hypothesis testing] -> [evidence gathering]",
         "Systematic debugging with methodical investigation protocol"),
        ("Feature Development", '"plan this feature"',
         "planning-prompts -> agent-teams -> worktree-manager -> testing -> git-workflow",
         "Plan -> parallel dev -> isolated worktrees -> TDD -> clean commits"),
    ]

    rows = [[name, trigger, chain, impact] for name, trigger, chain, impact in combos]
    t = make_table(
        ["Use Case", "Trigger", "Chain", "Impact"],
        rows,
        [1.1*inch, 1.4*inch, 2.4*inch, 1.6*inch]
    )
    story.append(t)

    story.append(Spacer(1, 12))
    story.append(Paragraph("<b>Dev Tools (15)</b> + <b>Infrastructure (8)</b>", s['SubHead']))

    dev_rows = [
        ["extension-authoring", "Author skills, hooks, commands, subagents"],
        ["debug-like-expert", "Systematic debugging with hypothesis testing"],
        ["planning-prompts", "Project planning and meta-prompt creation"],
        ["agent-teams", "Orchestrate parallel Claude Code sessions"],
        ["subagent-teams", "In-session Task tool subagent orchestration"],
        ["agent-capability-matrix", "Task -> agent mapping, 70+ agents"],
        ["git-workflow", "Conventional commits, PR templates"],
        ["testing", "TDD, test pyramid, mocking, coverage"],
        ["api-design", "REST/GraphQL API design patterns"],
        ["security", "Auth, secrets, OWASP, RLS"],
        ["api-testing", "API testing with Postman/Bruno"],
        ["docker-compose", "Local dev environments"],
        ["frontend-ui", "Tailwind v4, shadcn/ui, Next.js"],
        ["heal-skill", "Auto-diagnose broken skills"],
        ["worktree-manager", "Git worktree automation"],
    ]
    story.append(make_table(["Skill", "What It Does"], dev_rows, [2*inch, 4.5*inch]))

def page6_mcp(story, s):
    """MCP Tools Available"""
    story.append(PageBreak())
    story.append(Paragraph("MCP Tools Available", s['SectionHead']))
    story.append(Paragraph("7 MCP servers providing 90+ live tools for real-time data.", s['Body']))
    story.append(Spacer(1, 8))

    mcp_data = [
        ["HubSpot", "14", "Deals, contacts, companies, CRM search, analytics, ask_agent", "Sales workflow, pipeline, enrichment"],
        ["Apollo.io", "15", "Enrich, search, contacts, sequences, email accounts", "Prospecting, enrichment, outreach"],
        ["Clay", "13+", "Waterfall enrichment, contact/company search, subroutines", "Phone waterfall, data enrichment"],
        ["Gmail", "7", "Drafts, search, read, labels", "Email drafts, follow-ups"],
        ["Google Calendar", "9", "Events, free time, meeting times", "Call prep, scheduling"],
        ["IBKR", "7", "Portfolio, account summary, margin, short analysis", "Trading, position management"],
        ["Supabase", "20+", "SQL, migrations, edge functions, branches", "Disposition tracking, data storage"],
    ]
    story.append(make_table(
        ["Server", "Tools", "Key Capabilities", "Used For"],
        mcp_data,
        [1*inch, 0.5*inch, 2.8*inch, 2.2*inch]
    ))

    story.append(Spacer(1, 16))
    story.append(Paragraph("Golden Rules Enforcement (Automatic via Hooks)", s['SubHead']))
    story.append(Paragraph("These rules are enforced automatically via PreToolUse hooks on Apollo/Clay calls:", s['Body']))
    story.append(Spacer(1, 4))

    rules_data = [
        ["Rule", "Check", "Action"],
        ["Customer Check", "CRM lookup before enrichment", "DENY if existing customer"],
        ["Device Owner", "device_count >= 1", "DENY enrichment"],
        ["Channel Partner", "is_channel = true", "DENY enrichment"],
        ["AE-Owned", "hubspot_owner_id IN (82625923, 423155215)", "DENY prospecting"],
        ["Product Setup", 'first_conversion ILIKE "%setup%"', "DENY (not sales interest)"],
        ["DEMO REQUEST", 'first_conversion contains "demo", "pricing"', "PRIORITIZE (highest tier)"],
    ]
    story.append(make_table(rules_data[0], rules_data[1:], [1.3*inch, 2.5*inch, 2.7*inch]))

    story.append(Spacer(1, 16))
    story.append(Paragraph("Hooks Configuration", s['SubHead']))
    hooks_data = [
        ["Hook Event", "Trigger", "What It Does"],
        ["SessionStart", "Every session (weekday AM)", "Surface pending morning workflows"],
        ["PreToolUse", "Write/Edit/Bash", "Observer activation check"],
        ["PreToolUse", "Apollo/Clay contacts", "Golden Rules enforcement gate"],
        ["PostToolUse", "Write/Edit", "Scope escalation alert (>5 files)"],
        ["PostToolUse", "Apollo people_match", "Phone waterfall trigger on miss"],
        ["PostToolUse", "Skill", "Log skill usage + workflow results"],
        ["Stop", "Every stop", "Uncommitted files warning"],
    ]
    story.append(make_table(hooks_data[0], hooks_data[1:], [1.2*inch, 2*inch, 3.3*inch]))

def page7_targets(story, s):
    """Daily Targets + ATL/BTL Quick Ref"""
    story.append(PageBreak())
    story.append(Paragraph("Daily Targets + ATL/BTL Quick Reference", s['SectionHead']))

    story.append(Paragraph("<b>March 2026 Ramp Targets (50%)</b>", s['SubHead']))
    targets = [
        ["Metric", "Monthly Target", "Stretch (126%+)", "Daily Run Rate"],
        ["Deals created", "12", "16+ (1.5x accelerator)", "0.6/day"],
        ["Pipeline generated", "$357,000", "$450,000+", "$17,850/day"],
        ["Revenue (closed-won)", "$125,000", "$157,000+", "$6,250/day"],
        ["Daily dials", "50+", "60+", "50/day minimum"],
        ["Connect rate", "8-12%", "15%+", "4-6 connects/day"],
        ["Speed to lead", "<60 min", "<30 min", "Immediate"],
    ]
    story.append(make_table(targets[0], targets[1:], [1.5*inch, 1.5*inch, 1.8*inch, 1.7*inch]))

    story.append(Spacer(1, 12))
    story.append(Paragraph("<b>Accelerator Tiers</b>", s['SubHead']))
    accel = [
        ["Attainment", "Multiplier", "What It Means"],
        ["126%+", "1.5x", "Stretch goal -- ALWAYS target this"],
        ["111-125%", "1.25x", "Strong performance"],
        ["100-110%", "1.0x", "Base attainment"],
        ["<100%", "Base only", "Below quota -- recovery mode"],
    ]
    story.append(make_table(accel[0], accel[1:], [1.5*inch, 1.2*inch, 3.8*inch]))

    story.append(Spacer(1, 12))
    story.append(Paragraph("<b>ATL/BTL Classification Quick Reference</b>", s['SubHead']))
    story.append(Paragraph("ATL = can sign a purchase order. BTL = needs someone else's approval.", s['Body']))
    story.append(Spacer(1, 4))

    atl_data = [
        ["Tier", "Who", "Action"],
        ["DEMO REQUEST", "Any contact with first_conversion: demo, pricing, contact us", "ENRICH FIRST (highest priority)"],
        ["ATL (Budget Authority)", "Chief/C-suite, VP, President, Provost, Director (IT/Tech/Facilities), Dean, Court Admin, City/County Mgr, Sr Pastor", "Enrich second, always prospect"],
        ["GRAY ($25K gate)", "Manager (AV/Facilities/IT), Dept Chair, Dir. Ed Tech, Program Dir.", "Flag for Tim's manual review"],
        ["BTL (No Authority)", "Technician, Specialist, Coordinator, Support, Admin, Engineer, Operator, Instructor, Designer, Assistant, Clerk", "Deprioritize, enrich last"],
        ["NEVER ATL", "Warehouse Mgr, Network Mgr, Sys Admin, AV Tech, Graphic Design Instructor, Program Admin, Web Designer, Lab Coord, Maintenance, Building Eng", "HARD SKIP -- do NOT spend credits"],
    ]
    story.append(make_table(atl_data[0], atl_data[1:], [1.2*inch, 3*inch, 2.3*inch]))

    story.append(Spacer(1, 12))
    story.append(Paragraph("<b>ICP Vertical Scores</b>", s['SubHead']))
    icp_data = [
        ["Vertical", "ICP Score", "Top ATL Titles", "Budget Floor"],
        ["Higher Ed", "90", "CIO, VP IT, Provost, Dean, Dir Academic Tech", ">$50K"],
        ["Courts/Legal", "85", "Clerk of Court, Court Admin, Chief Judge", ">$75K"],
        ["Government", "80", "City Manager, IT Director/CIO, Dir Procurement", ">$100K"],
        ["Corporate AV", "80", "VP Facilities, VP IT/CIO, Dir IT Infrastructure", ">$150K"],
        ["Healthcare", "75", "CFO, CIO, COO, VP Operations, Dir Medical Ed", ">$100K"],
        ["Houses of Worship", "70", "Senior Pastor, Executive Pastor, Finance Chair", ">$25K"],
        ["K-12", "65", "Superintendent, CTO, Dir Instructional Tech", ">$10K"],
    ]
    story.append(make_table(icp_data[0], icp_data[1:], [1.2*inch, 0.8*inch, 2.8*inch, 1.7*inch]))

def page8_chains(story, s):
    """Workflow Chain Diagrams"""
    story.append(PageBreak())
    story.append(Paragraph("Workflow Chain Diagrams", s['SectionHead']))

    story.append(Paragraph("<b>1. BDR Daily Pipeline (Monday Full Chain)</b>", s['SubHead']))
    chain1 = [
        ["Step", "Time", "Skill", "Output"],
        ["1", "06:00", "prospect-enrich", "Phoneless contacts enriched (DEMO REQ -> ATL -> GRAY -> BTL)"],
        ["2", "06:15", "phone-waterfall", "Phones verified via Apollo -> Clay waterfall"],
        ["3", "06:30", "prospect-refresh", "30 net-new ICP prospects + Gmail drafts"],
        ["4", "07:00", "deal-momentum + portfolio-linker + trading-alerts", "Pipeline scored + deals linked + market scanned"],
        ["5", "07:15", "sequence-load", "Prospects auto-enrolled in Apollo sequences"],
        ["6", "07:25", "callable-lead-count", "ATL runway: X days, health alerts"],
        ["7", "07:30", "morning-brief", "HTML brief: calendar + 20 ATL leads + drafts ready"],
    ]
    story.append(make_table(chain1[0], chain1[1:], [0.4*inch, 0.6*inch, 2.5*inch, 3*inch]))
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>2. Automated Deal Flow</b>", s['SubHead']))
    chain2 = [
        ["Stage", "Skill", "MCP Tools Used", "Output"],
        ["Research", "prospect-research-to-cadence", "Apollo, Epiphan CRM, Gmail", "Enriched prospects + email drafts"],
        ["Verify", "phone-verification-waterfall", "Apollo, Clay", "Verified phone queue"],
        ["Prep", "meddic-call-prep-auto", "HubSpot, Apollo, Calendar, Clari", "MEDDIC brief per meeting"],
        ["Score", "deal-momentum-analyzer", "HubSpot, Clari, Apollo, Gmail", "6-signal score per deal"],
        ["Attribute", "portfolio-deal-linker", "HubSpot, Apollo, Gmail", "GTME evidence report"],
    ]
    story.append(make_table(chain2[0], chain2[1:], [0.7*inch, 2.2*inch, 1.8*inch, 1.8*inch]))
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>3. Feature Development Chain</b>", s['SubHead']))
    chain3 = [
        ["Step", "Skill", "Purpose"],
        ["1", "planning-prompts", "Create hierarchical plan, meta-prompts"],
        ["2", "agent-teams / subagent-teams", "Parallel dev in worktrees or subagents"],
        ["3", "worktree-manager", "Isolated git worktrees per feature"],
        ["4", "testing", "TDD: write tests first, then implement"],
        ["5", "security", "Auth, secrets, OWASP audit"],
        ["6", "git-workflow", "Conventional commits, PR creation"],
    ]
    story.append(make_table(chain3[0], chain3[1:], [0.5*inch, 2.5*inch, 3.5*inch]))
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>4. Strategy Chain</b>", s['SubHead']))
    chain4 = [
        ["Step", "Skill", "Framework"],
        ["1", "jobs-to-be-done", "Christensen JTBD + Ulwick ODI -- understand customer jobs"],
        ["2", "blue-ocean-strategy", "ERRC + Strategy Canvas -- find uncontested market space"],
        ["3", "business-model-canvas", "Osterwalder 9 blocks -- design the business model"],
        ["4", "challenger-sale", "Teach-Tailor-Take Control -- execute the sale"],
        ["5", "never-split-the-difference", "Voss FBI negotiation -- close the deal"],
    ]
    story.append(make_table(chain4[0], chain4[1:], [0.5*inch, 2*inch, 4*inch]))

    story.append(Spacer(1, 16))
    story.append(hr())
    story.append(Paragraph(
        f'<i>Generated {TODAY} by Claude Code  |  67 skills  |  github.com/tkipper/skills</i>',
        s['BodySmall']
    ))

def header_footer(canvas_obj, doc):
    """Add header and footer to each page."""
    canvas_obj.saveState()
    page_num = doc.page
    width, height = letter

    # Header bar
    if page_num == 1:
        # Cover page: full dark background
        canvas_obj.setFillColor(DARK)
        canvas_obj.rect(0, 0, width, height, fill=1, stroke=0)
    else:
        # Header stripe
        canvas_obj.setFillColor(PRIMARY)
        canvas_obj.rect(0, height - 28, width, 28, fill=1, stroke=0)
        canvas_obj.setFillColor(WHITE)
        canvas_obj.setFont('Helvetica-Bold', 8)
        canvas_obj.drawString(36, height - 20, "Tim's Daily Operations Guide")
        canvas_obj.drawRightString(width - 36, height - 20, f"Page {page_num}")

        # Footer
        canvas_obj.setFillColor(GRAY)
        canvas_obj.setFont('Helvetica', 7)
        canvas_obj.drawString(36, 20, f"Epiphan Video  |  {TODAY}  |  67 Skills")
        canvas_obj.drawRightString(width - 36, 20, 'Say "morning brief" to start')

        # Accent line
        canvas_obj.setStrokeColor(ACCENT)
        canvas_obj.setLineWidth(2)
        canvas_obj.line(0, height - 29, width, height - 29)

    canvas_obj.restoreState()

def main():
    s = build_styles()

    doc = SimpleDocTemplate(
        OUTPUT,
        pagesize=letter,
        topMargin=0.6*inch,
        bottomMargin=0.5*inch,
        leftMargin=0.5*inch,
        rightMargin=0.5*inch,
    )

    story = []

    # Page 1: Cover + Quick Start
    page1_cover(story, s)

    # Page 2: Morning Workflow Timeline
    page2_timeline(story, s)

    # Page 3: Trigger Phrase Quick Reference
    page3_triggers(story, s)

    # Pages 4-5: Skill Combinations by Use Case
    page4_5_combos(story, s)

    # Page 6: MCP Tools Available
    page6_mcp(story, s)

    # Page 7: Daily Targets + ATL/BTL Quick Ref
    page7_targets(story, s)

    # Page 8: Workflow Chain Diagrams
    page8_chains(story, s)

    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print(f"PDF generated: {OUTPUT}")

if __name__ == "__main__":
    main()
