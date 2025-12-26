# Project Plans Reference

Comprehensive reference for creating hierarchical project plans: briefs, roadmaps, phases, and context handoffs.

---

## Create Brief

<purpose>
The brief captures human vision. It's the ONLY human-focused document. Everything else is Claude-executable.
</purpose>

<greenfield_template>
```markdown
# [Project Name]

**One-liner**: [What this is in one sentence]

## Problem

[What problem does this solve? Why does it need to exist?
2-3 sentences max.]

## Success Criteria

How we know it worked:

- [ ] [Measurable outcome 1]
- [ ] [Measurable outcome 2]
- [ ] [Measurable outcome 3]

## Constraints

[Any hard constraints: tech stack, timeline, budget, dependencies]

- [Constraint 1]
- [Constraint 2]

## Out of Scope

What we're NOT building (prevents scope creep):

- [Not doing X]
- [Not doing Y]
```
</greenfield_template>

<brownfield_template>
After shipping v1.0, update BRIEF.md to include current state:

```markdown
# [Project Name]

## Current State (Updated: YYYY-MM-DD)

**Shipped:** v[X.Y] [Name] (YYYY-MM-DD)
**Status:** [Production / Beta / Internal / Live with users]
**Users:** [If known: "~500 downloads, 50 DAU" or "Internal use only"]
**Feedback:** [Key themes from user feedback]
**Codebase:**
- [X,XXX] lines of [primary language]
- [Key tech stack: framework, platform, deployment target]

**Known Issues:**
- [Issue 1 from v1.x that needs addressing]
- [Or "None" if clean slate]

## v[Next] Goals

**Vision:** [What's the goal for this next iteration?]

**Motivation:**
- [Why this work matters now]
- [User feedback driving it]

**Scope (v[X.Y]):**
- [Feature/improvement 1]
- [Feature/improvement 2]

**Success Criteria:**
- [ ] [Measurable outcome 1]
- [ ] [Measurable outcome 2]

**Out of Scope:**
- [Not doing X in this version]

---

<details>
<summary>Original Vision (v1.0 - Archived)</summary>
[Original brief content with checkboxes marked [x] for achieved]
</details>
```
</brownfield_template>

<guidelines>
- Keep under 50 lines
- Success criteria must be measurable/verifiable
- Out of scope prevents "while we're at it" creep
- This is the ONLY human-focused document
</guidelines>

---

## Create Roadmap

<purpose>
Define phases of implementation. Each phase is a coherent chunk of work that delivers value.
</purpose>

<process>
1. Check if brief exists: `cat .planning/BRIEF.md`
2. If no brief, ask: "No brief found. Create one first, or proceed with roadmap?"
3. Identify 3-6 phases based on the brief
4. Present phase breakdown for confirmation
5. Create structure: `mkdir -p .planning/phases`
6. Write ROADMAP.md
7. Create phase directories: `mkdir -p .planning/phases/01-{name}`
</process>

<roadmap_template>
```markdown
# Roadmap: [Project Name]

## Overview

[One paragraph describing the journey from start to finish]

## Phases

- [ ] **Phase 1: [Name]** - [One-line description]
- [ ] **Phase 2: [Name]** - [One-line description]
- [ ] **Phase 3: [Name]** - [One-line description]
- [ ] **Phase 4: [Name]** - [One-line description]

## Phase Details

### Phase 1: [Name]
**Goal**: [What this phase delivers]
**Depends on**: Nothing (first phase)
**Plans**: [Number of plans, e.g., "3 plans" or "TBD"]

Plans:
- [ ] 01-01: [Brief description of first plan]
- [ ] 01-02: [Brief description of second plan]
- [ ] 01-03: [Brief description of third plan]

### Phase 2: [Name]
**Goal**: [What this phase delivers]
**Depends on**: Phase 1
**Plans**: [Number of plans]

Plans:
- [ ] 02-01: [Brief description]

## Progress

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. [Name] | 0/3 | Not started | - |
| 2. [Name] | 0/1 | Not started | - |
```
</roadmap_template>

<phase_naming>
Use `XX-kebab-case-name` format:
- `01-foundation`
- `02-authentication`
- `03-core-features`
- `04-polish`

Numbers ensure ordering. Names describe content.
</phase_naming>

<anti_patterns>
- Don't add time estimates
- Don't create Gantt charts
- Don't add resource allocation
- Don't include risk matrices
- Don't plan more than 6 phases (scope creep)

Phases are buckets of work, not project management artifacts.
</anti_patterns>

---

## Plan Phase

<purpose>
Create the executable prompt for a phase. PLAN.md IS the prompt - it contains everything Claude needs to execute.
</purpose>

<plan_template>
```markdown
---
phase: XX-name
type: execute
---

<objective>
[What this phase accomplishes - from roadmap phase goal]

Purpose: [Why this matters for the project]
Output: [What artifacts will be created]
</objective>

<context>
@.planning/BRIEF.md
@.planning/ROADMAP.md
[If research exists:]
@.planning/phases/XX-name/FINDINGS.md
[Relevant source files:]
@src/path/to/relevant.ts
</context>

<tasks>

<task type="auto">
  <name>Task 1: [Action-oriented name]</name>
  <files>path/to/file.ext, another/file.ext</files>
  <action>[Specific implementation - what to do, how to do it, what to avoid and WHY]</action>
  <verify>[Command or check to prove it worked]</verify>
  <done>[Measurable acceptance criteria]</done>
</task>

<task type="auto">
  <name>Task 2: [Action-oriented name]</name>
  <files>path/to/file.ext</files>
  <action>[Specific implementation]</action>
  <verify>[Command or check]</verify>
  <done>[Acceptance criteria]</done>
</task>

</tasks>

<verification>
Before declaring phase complete:
- [ ] [Specific test command]
- [ ] [Build/type check passes]
- [ ] [Behavior verification]
</verification>

<success_criteria>
- All tasks completed
- All verification checks pass
- No errors or warnings introduced
- [Phase-specific criteria]
</success_criteria>

<output>
After completion, create `.planning/phases/XX-name/{phase}-{plan}-SUMMARY.md`
</output>
```
</plan_template>

<task_anatomy>
Every task has four required fields:

**files**: Exact file paths that will be created or modified.
- Good: `src/app/api/auth/login/route.ts`, `prisma/schema.prisma`
- Bad: "the auth files", "relevant components"

**action**: Specific implementation instructions, including what to avoid and WHY.
- Good: "Create POST endpoint that accepts {email, password}, validates using bcrypt against User table, returns JWT in httpOnly cookie with 15-min expiry. Use jose library (not jsonwebtoken - CommonJS issues with Next.js Edge runtime)."
- Bad: "Add authentication", "Make login work"

**verify**: How to prove the task is complete.
- Good: `npm test` passes, `curl -X POST /api/auth/login` returns 200
- Bad: "It works", "Looks good"

**done**: Acceptance criteria - the measurable state of completion.
- Good: "Valid credentials return 200 + JWT cookie, invalid credentials return 401"
- Bad: "Authentication is complete"
</task_anatomy>

---

## Checkpoints

<checkpoint_types>

### checkpoint:human-verify (Most Common)
Human confirms Claude's automated work.

```xml
<task type="checkpoint:human-verify" gate="blocking">
  <what-built>[What Claude automated]</what-built>
  <how-to-verify>
    1. Run: npm run dev
    2. Visit: http://localhost:3000/dashboard
    3. Test: [specific interactions]
    4. Confirm: [expected behaviors]
  </how-to-verify>
  <resume-signal>Type "approved" or describe issues</resume-signal>
</task>
```

Use for: Visual UI checks, interactive flows, accessibility testing.

### checkpoint:decision
Human makes implementation choice.

```xml
<task type="checkpoint:decision" gate="blocking">
  <decision>[What's being decided]</decision>
  <context>[Why this decision matters]</context>
  <options>
    <option id="option-a">
      <name>[Option name]</name>
      <pros>[Benefits]</pros>
      <cons>[Tradeoffs]</cons>
    </option>
    <option id="option-b">
      <name>[Option name]</name>
      <pros>[Benefits]</pros>
      <cons>[Tradeoffs]</cons>
    </option>
  </options>
  <resume-signal>Select: option-a or option-b</resume-signal>
</task>
```

Use for: Technology selection, architecture decisions, feature prioritization.

### checkpoint:human-action (Rare)
Action has NO CLI/API and requires human-only interaction.

```xml
<task type="checkpoint:human-action" gate="blocking">
  <action>[Unavoidable manual step]</action>
  <instructions>
    [What Claude already automated]
    [The ONE thing requiring human action]
  </instructions>
  <verification>[What Claude can check afterward]</verification>
  <resume-signal>Type "done" when complete</resume-signal>
</task>
```

Use ONLY for: Email verification links, SMS 2FA codes, manual approvals with no API.

Do NOT use for: Anything with a CLI (Vercel, Stripe, Upstash, Railway, GitHub), builds, tests, file creation.
</checkpoint_types>

<golden_rule>
If Claude CAN automate it via CLI/API, Claude MUST automate it.

**Claude automates:**
- Deployments: `vercel`, `fly deploy`, `railway up`
- Resources: Stripe API, Upstash CLI, Supabase CLI
- Builds/tests: `npm run build`, `npm test`
- File operations: Write tool
- Git operations: `git commit`, `git push`

**Human only does:**
- Visual verification (after Claude builds)
- Decisions (architecture, technology choices)
- Truly unavoidable manual steps (email links, 2FA codes)
</golden_rule>

---

## Scope Estimation

<quality_degradation_curve>
```
Context Usage  |  Quality Level   |  Claude's Mental State
-----------------------------------------------------------
0-30%          |  PEAK           |  "I can be thorough and comprehensive"
30-50%         |  GOOD           |  "Still have room, maintaining quality"
50-70%         |  DEGRADING      |  "Getting tight, need to be efficient"
70%+           |  POOR           |  "Running out, must finish quickly"
```

**The 40-50% inflection point:** This is where quality breaks. Claude sees context mounting and enters "completion mode."
</quality_degradation_curve>

<the_2_3_task_rule>
Each plan should contain 2-3 tasks maximum.

Why this number?
- Task 1 (0-15% context): Fresh context, peak quality
- Task 2 (15-35% context): Still peak zone, quality maintained
- Task 3 (35-50% context): Beginning to feel pressure, natural stopping point
- Task 4+ (50%+ context): DEGRADATION ZONE

**Better to have 10 small, high-quality plans than 3 large, degraded plans.**
</the_2_3_task_rule>

<when_to_split>
**Always split if:**
- More than 3 tasks
- Multiple subsystems (database + API + UI = 3 plans)
- Any task with >5 file modifications
- Checkpoint + implementation work
- Research + implementation

**Consider splitting if:**
- Estimated >5 files modified total
- Complex domains (auth, payments, data modeling)
- Any uncertainty about approach
- Natural semantic boundaries

**Naming convention:**
- `01-01-PLAN.md` - Phase 1, Plan 1
- `01-02-PLAN.md` - Phase 1, Plan 2
- `02-01-PLAN.md` - Phase 2, Plan 1
</when_to_split>

<autonomous_vs_interactive>
**Autonomous Plans (no checkpoints):**
- Contains only `type="auto"` tasks
- No user interaction needed
- Execute via subagent with fresh 200k context
- Impossible to degrade (always starts at 0%)

**Interactive Plans (has checkpoints):**
- Contains `checkpoint:human-verify` or `checkpoint:decision`
- Requires user interaction
- Must execute in main context
- Still target 50% context (2-3 tasks)

**Planning guidance:** Group autonomous work together (-> subagent), separate interactive work (-> main context).
</autonomous_vs_interactive>

---

## Handoff

<purpose>
Create context handoff when stopping work. Enables resumption in fresh context with full understanding.
</purpose>

<handoff_template>
Save to `.planning/phases/XX-name/.continue-here-{plan}.md`:

```markdown
# Continue Here: [Phase] [Plan]

## Current State
- **Phase**: [X]/[Total]
- **Plan**: [Y] of [Z] in this phase
- **Last Action**: [What was just completed]
- **Context File**: [This file path]

## Immediate Next Steps
1. [Very specific next action]
2. [Following action]
3. [Then this]

## Context Needed
```bash
# Run these to restore context
cat .planning/BRIEF.md
cat .planning/ROADMAP.md
cat .planning/phases/XX-name/XX-YY-PLAN.md
```

## Key Decisions Made
- [Decision 1]: [Choice and why]
- [Decision 2]: [Choice and why]

## Blockers / Issues
- [Any blocking issues, or "None"]

## Files Modified This Session
- `path/to/file.ts` - [What changed]

## Notes for Next Session
[Anything the next Claude should know]
```
</handoff_template>

<when_to_handoff>
- User says "stopping", "done for now", "taking a break"
- Context at 15% remaining (proactive offer)
- Context at 10% remaining (auto-create)
- Phase or plan complete but more work remains
</when_to_handoff>

---

## Resume

<process>
1. Find handoff: `find . -name ".continue-here*.md" -type f`
2. Read handoff file
3. Present summary: "Found handoff for [phase/plan]. [Summary of state]"
4. Ask: "Resume from here, or start fresh?"
5. If resume: Execute the "Context Needed" commands
6. Present: "Context restored. Ready to [next step from handoff]"
7. Delete handoff file after successful resume
</process>

---

## Transition (Phase Complete)

<process>
1. Verify all tasks in current plan complete
2. Create SUMMARY.md if not exists
3. Update ROADMAP.md progress table
4. Check for next plan in phase or next phase
5. Present options:
   ```
   Phase 1, Plan 2 complete.

   What's next?
   1. Plan 1-3 (continue phase)
   2. Move to Phase 2
   3. Create handoff (stopping)
   4. Other
   ```
</process>

---

## Milestones

<purpose>
Milestones mark shipped versions (v1.0, v1.1, v2.0).
</purpose>

<when_to_mark>
- All phases for version complete
- Ready to ship/deploy
- User says "ship it", "v1.0", "release"
</when_to_mark>

<milestone_actions>
1. Update ROADMAP.md with milestone groupings
2. Collapse completed phases in `<details>` tags
3. Update BRIEF.md with current state
4. Git tag: `git tag -a v1.0 -m "MVP release"`
5. Create MILESTONES.md entry if doesn't exist
</milestone_actions>

<milestone_entry>
```markdown
## v1.0 MVP (YYYY-MM-DD)

**Phases:** 1-4
**Commits:** abc1234...def5678

### Shipped
- [Feature 1]
- [Feature 2]

### Known Issues
- [Issue carried forward]
```
</milestone_entry>

---

## Summary Template

For phase completion, create `{phase}-{plan}-SUMMARY.md`:

```markdown
# Phase [X] Plan [Y]: [Name] Summary

**[Substantive one-liner - what shipped, not "phase complete"]**

## Accomplishments
- [Key outcome 1]
- [Key outcome 2]

## Files Created/Modified
- `path/to/file.ts` - Description
- `path/to/another.ts` - Description

## Decisions Made
[Key decisions and rationale, or "None"]

## Issues Encountered
[Problems and resolutions, or "None"]

## Next Step
[If more plans: "Ready for {phase}-{next-plan}-PLAN.md"]
[If phase complete: "Phase complete, ready for next phase"]
```
