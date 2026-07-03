# Tim's Skills Library

87 production-ready skills for Claude Code and Claude Desktop. Engineering, GTM, sales automation, BDR pipeline automation, and trading.

## How to Use This Folder

When working in this folder, Claude should:
1. Read SKILLS_INDEX.md first to see what's available
2. Only load the specific SKILL.md file(s) needed for the current task
3. Keep context lean - don't load all skills at once

## Folder Structure

```
skills/
├── CLAUDE.md               # You're reading this
├── README.md               # Quick start + skill catalog
├── SKILLS_INDEX.md         # Detailed skill documentation (87 skills)
├── DEPENDENCY_GRAPH.md     # Visual skill relationships
├── PLANNING.md             # Current sprint (P14)
├── BACKLOG.md              # Future work
├── ARCHIVE.md              # Completed sprints
├── active/                 # 80 trigger-activated skills (4 live-automation names lack the -skill suffix: nooks-autopilot, sdr-dial-lists, sdr-call-coaching, epiphan-call-playbook)
├── stable/                 # 2 always-loaded core skills
├── dist/                   # 86 zip files for Claude Desktop (gitignored; scripts/rebuild-zips.sh)
├── scripts/
│   ├── deploy.sh           # Deploy to ~/.claude/skills/
│   ├── rebuild-zips.sh     # Rebuild dist/*.zip
│   ├── test-skills.sh      # Integration tests (537 checks, T1-T9)
│   ├── test-outcomes.sh    # Infrastructure tests (T10-T14)
│   ├── log-skill-usage.sh  # PostToolUse hook target (activations)
│   ├── log-outcome.sh      # PostToolUse hook target (outcomes)
│   ├── log-feedback.sh     # Feedback logger
│   ├── validate-outcome.sh # Outcome schema validator
│   ├── outcome-report.sh   # Outcome analytics CLI
│   ├── variant-assigner.sh # Deterministic A/B variant assignment
│   ├── skill-analytics-report.sh  # Usage reporting
│   ├── skill-health-report.sh     # Skill health CLI ($0 cost)
│   └── hooks/              # SessionStart + workflow hooks
├── templates/              # Skill starter templates
└── .claude/
    ├── settings.json       # Hooks config (PreToolUse, PostToolUse, Stop)
    ├── settings.local.json # Permissions + observer hooks
    ├── agents/             # skill-health-observer.md, observer-lite.md, observer-full.md
    ├── commands/           # skill-feedback.md, skill-health.md + 8 workflow commands
    ├── observers/          # QUALITY.md, ARCH.md, ALERTS.md, SKILL_HEALTH.md
    ├── rules/              # coding.md
    └── SKILL_TEST_MATRIX.md  # Activation test results
```

## Self-Improvement Infrastructure (P12)

Autoresearch-style framework for skill outcome tracking, health scoring, and A/B variant testing.

**Outcome Logging:** Pilot skills write sidecar JSON to `~/.claude/skill-analytics/last-outcome-{skill-name}.json`. A PostToolUse hook auto-captures these into `~/.claude/skill-analytics/outcomes.jsonl`. Schema: `{ts, skill, version, variant, status, runtime_ms, metrics{}, error, session_id}`. 90-day rotation.

**Feedback:** `/skill-feedback <skill> <status> <notes>` — manual outcome recording for any skill. Writes to both `outcomes.jsonl` and `feedback.jsonl`.

**Health Observer:** `/skill-health` spawns a Haiku agent to score per-skill health (success rate, consistency, data volume). `/skill-health --quick` runs bash-only report ($0). Output: `.claude/observers/SKILL_HEALTH.md`. Morning pipeline nudges if report >7 days stale.

**A/B Variants:** Optional `variants` key in `config.json`. Deterministic hash-based assignment via `scripts/variant-assigner.sh`. Pilot: `cold-email-sequence-generator-skill` (control vs concise). Outcomes track variant for per-variant analysis.

**Important:** Sidecar paths MUST stay outside the repo directory (`~/.claude/skill-analytics/`) — the PreToolUse observer hook bypasses writes to external paths.

---

## HubSpot Configuration

- **Portal ID:** `21530819`
- **Contact Record URL format:** `https://app.hubspot.com/contacts/21530819/record/0-1/{contactId}`
- **Company Record URL format:** `https://app.hubspot.com/contacts/21530819/record/0-2/{companyId}`
- **Deal Record URL format:** `https://app.hubspot.com/contacts/21530819/record/0-3/{dealId}`

Always use portal ID `21530819` when generating HubSpot links. Never use `4366444`.

## Email & Draft Staging

- **Default send-from:** `tkipper@epiphan.com`
- **Gmail Draft Workflow:** When building call lists, ALWAYS create Gmail drafts via `gmail_create_draft` for every lead. Tim's workflow: call → open draft → review/edit → send.
- **Never use:** robert@epiphan.com or any other sender

## Golden Rules — Lead Qualification Gates

These apply to ALL BDR skills that touch contacts (enrichment, outreach, call lists, sequences):

1. **Customers:** `lifecyclestage = 'customer'` or `device_count >= 1` → **EXCLUDE**
2. **Channel Partners:** `is_channel = true` → **EXCLUDE**
3. **Product-only Engagers:** `first_conversion` contains setup forms (not demo/pricing) → **EXCLUDE**
4. **AE-Owned Contacts (90-Day Stale Exception):**
   - `hubspot_owner_id` IN `82625923` (Lex Evans), `423155215` (Ron Epstein), `190030668` (Phillip Sandler)
   - **If last activity > 90 days ago** → **SURFACE** to Tim as `STALE AE LEAD`. Show ATL/BTL tier, deal value, recommended action (re-engage, push to demo, or help close). Tim decides.
   - **Ron Epstein (423155215):** 90-day stale rule applies to ALL his leads
   - **Lex Evans (82625923) & Phillip Sandler (190030668):** 90-day stale rule applies to **North America only** (USA/Canada). Non-NA contacts with <90 day activity → still exclude.
   - **If last activity < 90 days** → **EXCLUDE** (AE actively working)
5. **Geo:** USA/Canada only (unless specified)

> **Updated 2026-03-21:** Changed AE-owned from hard-exclude to 90-day stale exception. Tim Kipper (BDR) can review and re-engage stale AE leads to push toward demo or closed-won.

---

## For Individual Projects

To use a skill in another project, either:

1. **Symlink** (recommended):
   ```bash
   ln -s ~/Desktop/tk_projects/skills/active/skill-name ./skills/
   ```

2. **Reference in project's CLAUDE.md**:
   ```markdown
   ## Skills
   - See `~/Desktop/tk_projects/skills/active/skill-name/SKILL.md`
   ```

3. **Copy the `.zip`** directly into project

## Available Skills

See SKILLS_INDEX.md for the complete list.

---

## ATL / BTL Decision-Maker Classification — Epiphan Video
**Last Updated: 2026-03-17** | **Approved by: Tim Kipper** | **Version: 1.0**

> **Core Principle:** ATL = the person who can sign a purchase order or approve budget for AV/video equipment. If they need someone else's approval to spend, they're BTL. "Manager" is NOT automatically ATL — it depends on whether they hold P&L / budget authority.

### Universal ATL Title Keywords (Cross-Vertical — Budget Authority)
Chief (CIO, CTO, CFO, COO) • Vice President (VP, AVP, SVP, EVP) • President • Provost • Vice Provost •
Superintendent • Director (of IT, Technology, Facilities, Academic Technology, Procurement, Materials Mgmt,
Medical Education, Court Administration) • Dean • Court Administrator • Clerk of Court (Federal) •
City Manager • County Manager • Senior Pastor • Executive Pastor

### Universal BTL Title Keywords (No Budget Authority)
Technician • Specialist • Coordinator • Support • Administrator (Systems/Network/Database) •
Engineer (AV/Network/Systems) • Operator • Instructor/Professor/Faculty •
Designer (Learning/Instructional/Graphic) • Assistant • Clerk (non-Court Admin) •
Volunteer • Intern • Student • Resident • Help Desk

### NEVER ATL (Regardless of Vertical)
Warehouse Manager • Network Manager • Systems Administrator • AV Technician •
Graphic Design Instructor • Program Administrator • Web Designer •
Classroom Support • Lab Coordinator • Maintenance • Building Engineer •
Multimedia Services Manager • Video Production Specialist • Streaming Crew

### Gray Zone — Requires Manual Review
- **Manager (AV/Facilities/IT)** — ATL only if reports to Director+ AND has delegated budget authority >$25K
- **Department Chair** — ATL at small institutions; BTL at large universities
- **Director of Educational Technology** — depends on reporting line (Provost = ATL; IT VP = maybe BTL)
- **Program Director** — ATL only if department-level budget holder; BTL if coordination role

### Vertical-Specific ATL Patterns

**Higher Ed (ICP 90):** CIO • VP of IT • AVP for IT • Provost • VP Academic Affairs • Vice Provost Teaching & Learning • Director of Academic/Instructional Technology • Director of IT Services • Dean • CTO

**Courts/Legal (ICP 85):** Clerk of Court • Court Administrator • Director of Court Administration • Court Executive Director • Chief Judge • Director of Finance & Administration

**Government (ICP 80):** City Manager • Deputy City Manager • IT Director/CIO • Director of Procurement • County Administrator • Director of Finance

**Corporate AV (ICP 80):** VP of Facilities • VP of IT/CIO • VP of Corporate Communications • VP of Operations • Director of Facilities Operations • Director of IT Infrastructure • Director of Corporate Events • Procurement Director

**Healthcare (ICP 75):** CFO • CIO • COO • VP of Operations • Hospital Administrator • Director of Materials Management • Surgical Services Director • Director of Medical Education

**Houses of Worship (ICP 70):** Senior Pastor • Executive Pastor • Church Board/Elders • Finance Committee Chair • Building/Facilities Committee Chair

**K-12 (ICP 65):** Superintendent • CTO/Director of Technology Services • Director of Instructional Technology • Business/Finance Director • Assistant Superintendent of Operations • Building Principal (<$10K)

### Full Reference
See `atl-btl-classification-draft.html` in skills folder for complete vertical breakdowns with BTL lists, gray zone rules, and examples.

### ATL/BTL Remediation Backlog (from 2026-03-17 Audit)
See `atl-btl-audit-report.html` for full findings. 7 issues across 20 tasks and 5 skills.

**Phase 1 — This Week (by 2026-03-21): ✅ COMPLETED 2026-03-17**
- [x] Patch `phone-verification-waterfall/SKILL.md` — Added ATL/BTL Classification Gate (Stage 1), NEVER ATL filter, ATL-first sorting (Stage 5), tier badges + counts in output
- [x] Patch `prospect-research-to-cadence/SKILL.md` — Stage 1c: replaced "Manager of AV/IT/Media" with ATL-only title patterns; added ATL/BTL Classification subsection with full 16-item BTL list, 14-item NEVER ATL list, $25K Gray Zone gate
- [x] Patch `sales-revenue/SKILL.md` — Added ATL/BTL Gate (Pre-Sequence) with full keyword lists (ATL 10, GRAY w/$25K threshold, BTL 16, NEVER 14); updated ENRICHER agent row for ATL-first discovery

**Phase 2 — Next 2 Weeks (by 2026-04-01): ✅ COMPLETED 2026-03-17**
- [x] Add ATL/BTL filter to `bdr-v3-prospect-enrich` scheduled task — Updated prompt with full ATL/BTL Classification Gate (ATL-first enrichment priority, NEVER ENRICH hard skip, tier tagging in notes)
- [x] Add ATL/BTL filter to `bdr-v3-prospect-refresh` scheduled task — Updated prompt with ATL/BTL gate (ATL/GRAY-only Gmail drafts, NEVER PROSPECT hard filter, tier badges in output)
- [x] Patch `meddic-call-prep-auto/SKILL.md` — Stage 2 Economic Buyer: added full ATL/BTL validation with all keyword lists (ATL 10, BTL 16, NEVER 14), $25K Gray Zone gate, EB identification logic, discovery questions for BTL-only calls
- [x] Patch `deal-momentum-analyzer/SKILL.md` — Signal 3 (Stakeholder Breadth): ATL-tier requirement for full 15 points; 6-tier scoring table; penalty flag for deals with 0 ATL contacts; all keyword lists complete

**Phase 3 — Next Month (by 2026-04-17): ✅ COMPLETED 2026-03-17**
- [x] Add ATL coverage metric to `bdr-v3-friday-pipeline` — Updated prompt with ATL Coverage % calculation, 80% target, per-deal ATL/GRAY/BTL breakdown table, ⚠️ flag for deals with 0 ATL, full keyword lists (ATL 10, BTL 16, NEVER 14)
- [x] Add ATL coverage metric to `bdr-v3-friday-sequence-audit` — Updated prompt with ATL Targeting % per sequence, 60% target, NEVER ATL removal alerts, per-sequence ATL/GRAY/BTL table, full keyword lists
- [x] Add ATL/BTL breakdown to `bdr-v3-callable-lead-count` daily health check — Updated prompt with separate ATL/GRAY/BTL/NEVER ATL counts, ATL Runway metric (15 ATL dials/day), alert thresholds (ATL < 15 ⚠️, total < 50 🚨, NEVER ATL > 0 🔍)

---

## Tim's 2026 BDR Comp Plan — PERMANENT REFERENCE

**Role:** BDR/Application Engineer at Epiphan Video
**Base Salary:** $75,000/year ($6,250/mo guaranteed)
**Start Date:** February 2026 (learning month)
**Ramp Schedule:**

| Month | Phase | Deals | Pipeline | Revenue | Earnings |
|-------|-------|-------|----------|---------|----------|
| February | Learning | - | - | - | $6,250 |
| March | Ramp 50% | 12 | $357K | $125K | $6,250 |
| April | Ramp 65% | 16 | $464K | $163K | $6,250 |
| May | Ramp 85% | 20 | $607K | $212K | $6,250 |
| June | Full (H1) | 24 | $714K | $250K | $6,250 |
| July | Full (H2) | 24 | $714K | $475K | $6,250 |
| August | Full (H2) | 24 | $714K | $475K | $6,250 |
| September | Full (H2) | 24 | $714K | $500K | $6,250 |
| October | Full (H2) | 24 | $714K | $525K | $6,250 |
| November | Full (H2) | 24 | $714K | $550K | $6,250 |
| December | Full (H2) | 24 | $714K | $600K | $6,250 |
| **Annual** | | **200** | **$6.0M** | **$4.0M** | **$75,000** |

**Accelerators (Monthly):**
| Attainment vs Quota | Multiplier |
|---------------------|------------|
| 126%+ | 1.5x |
| 111-125% | 1.25x |
| 100-110% | 1.0x |

**OPERATING PRINCIPLE:** Always target stretch goals (126%+ = 1.5x accelerator) as the MINIMUM. Use every skill, connector, and automation available to exceed quota every month.

**March 2026 Targets (Ramp 50%):**
- 12 deals minimum (stretch: 16+ for accelerator)
- $357K pipeline minimum (stretch: $450K+)
- $125K revenue minimum (stretch: $157K+ for 1.25x)
- 50+ daily dials | Connect rate: 8-12% | Speed to lead: <60 min
