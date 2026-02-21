# Tim's Skills Library

This folder contains reusable skill packages for Claude Desktop and Claude Code.

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
├── SKILLS_INDEX.md         # Detailed skill documentation
├── DEPENDENCY_GRAPH.md     # Visual skill relationships
├── PLANNING.md             # Current sprint
├── BACKLOG.md              # Future work
├── ARCHIVE.md              # Completed sprints
├── active/                 # Trigger-activated skills
├── stable/                 # Always-loaded core skills
├── dist/                   # Zip files for Claude Desktop
├── scripts/
│   ├── deploy.sh           # Deploy to ~/.claude/skills/
│   └── rebuild-zips.sh     # Rebuild dist/*.zip
├── templates/              # Skill starter templates
└── .claude/
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

## Dual-Team Daily Workflow

Every development session runs two concurrent agent teams:
- **Builder Team** (1-3 agents): Ships features fast via worktrees
- **Observer Team** (2 agents, always active): Watches for drift, debt, gaps

Each team has a **devil's advocate** role. Observer team is non-negotiable.

See `active/workflow-orchestrator-skill/reference/dual-team-architecture.md` for full spec.

Quick invocation:
- Start day: triggers workflow-orchestrator → spawns Observers automatically
- Feature build: uses agent-teams or subagent-teams → Observers monitor
- End day: Observer final report → security sweep → context save

## Available Skills

See SKILLS_INDEX.md for the complete list.

---

## MANDATORY: Observer Protocol

**You MUST follow this protocol before writing ANY code.** No exceptions. No rationalizing.

### Step 1: Classify Task Scope

| Scope | Criteria | Observer Required |
|-------|----------|-------------------|
| **MINIMAL** | Typos, comments, single config tweak | None |
| **SMALL** | 1-3 files changed, no new dependencies | observer-lite (Haiku) |
| **STANDARD** | 4-10 files, or any new dependency | observer-full (Sonnet) |
| **FULL** | >10 files, new architecture, new patterns | observer-full + feature contract |

### Step 2: Spawn Observer (if SMALL or above)

```
# For SMALL scope:
Task tool -> subagent_type: "observer-lite"
  prompt: "Run quality checks on the skills codebase. Focus on [relevant area]."

# For STANDARD/FULL scope:
Task tool -> subagent_type: "observer-full"
  prompt: "Run full drift detection on skills. The current task is: [describe task]."
```

### Step 3: For FULL scope — Create Feature Contract First

Before coding, create `.claude/contracts/[feature-name].md`:
- Define IN SCOPE and OUT OF SCOPE boundaries
- List success criteria
- Get observer approval before writing code

### Step 4: Verify Observer Ran

Before making your first code change, confirm:
- [ ] `.claude/OBSERVER_QUALITY.md` has a real date (not `_not yet run_`)
- [ ] Scope classification matches the task complexity

**If the PreToolUse hook prints `** OBSERVER NOT ACTIVE **`, STOP and spawn the observer.**

### Scope Escalation Rule

If during work you hit ANY of these triggers, upgrade from Lite to Full:
- **>5 files modified** (the PostToolUse hook will remind you)
- **New dependency added** to package.json or pyproject.toml
- **Task scope expanded** beyond original description

---

## Dual-Team Workflow

This project uses the **TK Dual-Team Daily Workflow**.

### Quality Gates

| Gate | Check | Enforced By |
|------|-------|-------------|
| Pre-code | Observer spawned | PreToolUse hook |
| During code | Scope escalation | PostToolUse hook |
| Pre-merge | No open BLOCKERs | OBSERVER_ALERTS.md |

### Observer Cost Guide

| Observer | Model | Cost | When |
|----------|-------|------|------|
| observer-lite | Haiku 4.5 | ~$0.03-0.05 | SMALL scope |
| observer-full | Sonnet 4.6 | ~$0.50-2.00 | STANDARD/FULL scope |

### Copy-Paste Prompts

**START DAY:** Start day — project is skills. Path: ~/Desktop/tk_projects/skills
**FEATURE BUILD:** Feature build — [FEATURE_NAME]
**END DAY:** End day — project is skills
