# Tim's Skills Library

47 production-ready skills for Claude Code and Claude Desktop. Engineering, GTM, sales automation, and trading.

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
├── SKILLS_INDEX.md         # Detailed skill documentation (47 skills)
├── DEPENDENCY_GRAPH.md     # Visual skill relationships
├── PLANNING.md             # Current sprint (P9)
├── BACKLOG.md              # Future work
├── ARCHIVE.md              # Completed sprints
├── active/                 # 45 trigger-activated skills
├── stable/                 # 2 always-loaded core skills
├── dist/                   # 47 zip files for Claude Desktop
├── scripts/
│   ├── deploy.sh           # Deploy to ~/.claude/skills/
│   ├── rebuild-zips.sh     # Rebuild dist/*.zip
│   ├── test-skills.sh      # Integration tests (323 checks)
│   ├── log-skill-usage.sh  # PostToolUse hook target
│   ├── skill-analytics-report.sh  # Usage reporting
│   └── hooks/              # SessionStart + workflow hooks
├── templates/              # Skill starter templates
└── .claude/
    ├── settings.json       # Hooks config (PreToolUse, PostToolUse, Stop)
    ├── settings.local.json # Permissions + observer hooks
    ├── observers/          # QUALITY.md, ARCH.md, ALERTS.md
    ├── rules/              # coding.md
    └── SKILL_TEST_MATRIX.md  # Activation test results
```

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
