---
name: "workflow-orchestrator"
description: "Dual-team project workflow — Builder + Observer teams, cost tracking, parallel execution, security gates, agent orchestration. Use when: start day, begin session, status check, new feature, build, implement, end day, wrap up, debug, investigate, dual team, observer team, builder team, spawn observers, devil's advocate."
---

<objective>
Dual-team project workflow system providing Builder + Observer concurrent teams, cost tracking, parallel execution via git worktrees, security gates, and intelligent agent orchestration. Every session runs two teams: Builders ship features fast, Observers watch for drift, debt, and scope creep. Each team has a devil's advocate role. Manages complete development lifecycle from session start to end-of-day with mandatory Observer reports, security sweeps, and context preservation.
</objective>

<quick_start>
**Start session:**
```bash
pwd && git status && git log --oneline -5
cat PROJECT_CONTEXT.md 2>/dev/null
```
→ Auto-spawns Observer team (non-negotiable)

**Feature development:** Contract → Builder Team → Observer monitors → Security gate → Ship

**End session:**
1. Observer final report
2. Security sweep: `gitleaks detect --source .`
3. Update `PROJECT_CONTEXT.md`
4. Log costs to `costs/daily-YYYY-MM-DD.json`
</quick_start>

<success_criteria>
Workflow is successful when:
- Context scan completed at session start
- Observer team spawned and monitoring (non-negotiable)
- Contract defined before any feature implementation
- Observer BLOCKER gate checked before phase transitions
- Security sweep passes before any commits
- Cost tracking updated (daily.json, mtd.json)
- Observer final report generated at end of day
- PROJECT_CONTEXT.md updated at session end
- All security gates passed before shipping
</success_criteria>

<triggers>

- **Session Management:** "start day", "begin session", "what's the status", "end day", "wrap up", "done for today"
- **Feature Development:** "new feature", "build", "implement"
- **Dual-Team:** "dual team", "observer team", "builder team", "spawn observers", "devil's advocate"
- **Debugging:** "debug", "investigate", "why is this broken"
- **Research:** "research", "evaluate", "should we use"

---

## DUAL-TEAM ARCHITECTURE

Every session runs two concurrent teams under the Orchestrator:

```
              ORCHESTRATOR
              ┌────┴────┐
        BUILDER TEAM   OBSERVER TEAM
        (ships fast)   (watches quality)
        ├ Lead Builder  ├ Code Quality (haiku)
        ├ Builder(s)    └ Architecture (sonnet)
        └ Devil's Adv.    └─ (Devil's Advocate)
```

**Observer team is non-negotiable.** It always runs, even for "small" changes.

- **Builders** optimize for velocity — ship features via worktrees or subagents
- **Observers** optimize for correctness — detect drift, debt, gaps, scope creep
- **Devil's advocate** on each team prevents groupthink and blind spots

Observers write findings to `.claude/OBSERVER_*.md` with severity levels:
- 🔴 BLOCKER — stop work, fix immediately
- 🟡 WARNING — fix before merge or log
- 🔵 INFO — backlog

**Deep dive:** See `reference/dual-team-architecture.md`

---

## START DAY

### Pre-Flight Checks
```bash
git status --short | head -5
[ -f package.json ] && [ ! -d node_modules ] && echo "Run npm install"
[ -f requirements.txt ] && [ ! -d .venv ] && echo "Run pip install"
[ -f .env.example ] && [ ! -f .env ] && echo "Copy .env.example to .env"
```

### Context Scan (Mandatory)
```bash
pwd && git status && git log --oneline -5
cat PROJECT_CONTEXT.md 2>/dev/null || echo "No context file"
cat CLAUDE.md 2>/dev/null
cat PLANNING.md 2>/dev/null
```

### Observer Team Spawn (Automatic)
Spawn Observer team concurrent with standup:
- Code Quality Observer (haiku) — tech debt, test gaps, imports
- Architecture Observer (sonnet) — contract drift, scope creep, design violations

```bash
# Detect Native Agent Teams support
if [ "${CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS}" = "1" ]; then
  echo "Native Agent Teams enabled — using DAG task system"
  # Use TeamCreate + SendMessage for Observer coordination
else
  echo "Native Agent Teams not enabled — falling back to manual worktree spawn"
  # Use subagent-teams-skill Task tool pattern
fi
```

### Sprint Plan
Include Observer BLOCKER gate in sprint plan — no phase transitions if active BLOCKERs in `.claude/OBSERVER_ALERTS.md`.

### Output Format
```markdown
## Session Start: [PROJECT_NAME]
### Completed (Last Session)
- [x] Task 1
### In Progress
| Task | Branch/Worktree | Status |
|------|-----------------|--------|
| API endpoint | feature/api | 70% |
### Observer Status
- Team: ACTIVE (Code Quality + Architecture)
- Active blockers: 0
### Today's Priority Queue
1. [BUILDER] Feature implementation
2. [OBSERVER] Continuous monitoring
### Cost Context
- Today: $0.00 | MTD: $12.34 | Budget: $100
```

**Deep dive:** See `reference/start-day-protocol.md`

---

## RESEARCH PHASE

**Trigger:** Before ANY feature development involving new frameworks, APIs, or architectural decisions.

### Scan → Evaluate → Decide
1. Check existing solutions in your repos and MCP cookbook
2. Use `research-skill` checklist for framework selection
3. Cost projection before building
4. Create `RESEARCH.md` → `FINDINGS.md` with GO/NO-GO recommendation

⛔ **Gate: Human checkpoint required before proceeding**

**Deep dive:** See `reference/research-workflow.md`

---

## FEATURE DEVELOPMENT

### Phase 0: CONTRACT DEFINITION (Before Code)
```markdown
## Feature Contract: [NAME]
### Endpoints / Interfaces
- POST /api/widgets → { id, name, created_at }
### Scope Boundaries
- IN SCOPE: [list]
- OUT OF SCOPE: [list]
### Observer Checkpoints
- [ ] Architecture Observer approves contract
- [ ] Code Quality Observer runs after each merge
```
⛔ **Gate: Architecture Observer must approve contract before Phase 1**

### Phase 1: BUILDER TEAM SPAWN
```bash
# Option A: Worktree sessions (long tasks, 30+ min)
git worktree add -b feature/api ~/tmp/worktrees/$(basename $(pwd))/api
# Option B: Native Agent Teams (short tasks, <20 min)
# Use TeamCreate + Task tool subagents
# Option C: Hybrid — worktrees for Builders, Task tool for Observers
```

Each builder gets a WORKTREE_TASK.md with:
- Scope boundary (what they CAN and CANNOT touch)
- Contract reference
- Devil's advocate mandate (for one builder per cycle)

### Phase 2: OBSERVER MONITORING (Concurrent)
Observers run parallel to builders on a 5-10 minute loop:
1. Pull latest from builder branches
2. Run 7 drift detection patterns (see `reference/observer-patterns.md`)
3. Write findings to `.claude/OBSERVER_QUALITY.md` and `.claude/OBSERVER_ARCH.md`
4. Escalate BLOCKERs to `.claude/OBSERVER_ALERTS.md`

### Phase 3: SECURITY + QUALITY GATE
```bash
# Security scans
semgrep --config auto .
gitleaks detect --source .
npm audit --audit-level=critical || pip-audit
pytest --cov=src || npm test -- --coverage
```

⛔ **Gate: ALL must pass + no active Observer BLOCKERs**
```python
gate = (
    sast_clean AND
    secrets_found == 0 AND
    critical_vulns == 0 AND
    test_coverage >= 80 AND
    observer_blockers == 0  # NEW: Observer gate
)
```

### Phase 4: SHIP
```bash
git diff main...HEAD
git add . && git commit -m "feat: [description]"
git push
echo '{"feature": "X", "cost": 1.23}' >> costs/by-feature.jsonl
```

**Deep dive:** See `reference/feature-development.md`

---

## DEBUG MODE

**Trigger:** When standard troubleshooting fails or issue is complex.

### Evidence → Hypothesize → Test → Verify
1. **Evidence gathering** — exact error, reproduction steps, expected vs actual
2. **Hypothesis formation** — 3+ hypotheses with evidence for each
3. **Systematic testing** — one variable at a time
4. **Verification** — root cause confirmed before committing fix

### Critical Rules
- ❌ NO DRIVE-BY FIXES — explain WHY before committing
- ❌ NO GUESSING — verify everything
- ✅ Use all tools: MCP servers, web search, extended thinking
- ✅ One variable at a time

**Deep dive:** See `reference/debug-methodology.md`

---

## END DAY

### Phase 1: Observer Final Report (Before Security Sweep)
Observers generate final reports:
- Summary of all findings (resolved + open)
- Metrics: debt items, test coverage delta, contract compliance
- Write to `.claude/OBSERVER_QUALITY.md` and `.claude/OBSERVER_ARCH.md`

⛔ **Gate: Review Observer report before proceeding**

### Phase 2: Security Sweep (Mandatory)
```bash
gitleaks detect --source . --verbose
git log -p | grep -E "(password|secret|api.?key|token)" || echo "Clean"
npm audit --audit-level=critical 2>/dev/null || pip-audit 2>/dev/null
```

⛔ **Gate: ALL must pass before any commits**

### Phase 3: Context + Metrics + Cleanup
```markdown
## PROJECT_CONTEXT.md Update
### Completed This Session
- [x] Feature X
### Observer Summary
- Blockers resolved: N | Warnings logged: N | Debt delta: +/-N
### Tomorrow's Priorities
1. Next task
```

Archive observer reports to `.claude/OBSERVER_HISTORY/`, reset for next session.

```bash
# Cost tracking
echo '{"total": 0.47}' >> costs/daily-$(date +%Y-%m-%d).json
# Portfolio metrics
git diff --stat $(git log --since="today 00:00" --format="%H" | tail -1)..HEAD 2>/dev/null
```

**Deep dive:** See `reference/end-day-protocol.md`

---

## COST GATE

### Pre-Flight Budget Check
```bash
COST_FILE=~/.claude/daily-cost.json
SPENT=$(jq '.spent' "$COST_FILE" 2>/dev/null || echo 0)
BUDGET=$(jq '.budget_monthly' "$COST_FILE" 2>/dev/null || echo 100)
echo "MTD: \$$SPENT / \$$BUDGET"
```

| % of Budget | Action |
|-------------|--------|
| < 50% | Proceed normally |
| 50-80% | Cost warning, suggest model downgrade |
| 80-95% | **WARN** — Ask user before proceeding |
| > 95% | **BLOCK** — Require explicit override |

**Deep dive:** See `reference/cost-tracking.md`

---

## ROLLBACK / RECOVERY

- Stash current work → find last known good → selective rollback or full revert → verify tests → investigate root cause
- Use `debug-like-expert-skill` for root cause analysis

**Deep dive:** See `reference/rollback-recovery.md`

---

## SKILL INVOCATION QUICK REFERENCE

| Need | Invoke | Model |
|------|--------|-------|
| Spawn builder team | `agent-teams-skill` or Task tool with `team_name` | sonnet |
| Spawn observer team | Auto at START DAY, or `workflow-orchestrator` | haiku/sonnet |
| Debug a failing test | `debug-like-expert-skill` | sonnet |
| Review code quality | `superpowers:requesting-code-review` | sonnet |
| Run security sweep | `security-skill` | sonnet |
| Track costs | `cost-metering-skill` | haiku |
| Write tests | `testing-skill` | sonnet |
| Design API contract | `api-design-skill` | sonnet |
| Plan architecture | `planning-prompts-skill` | opus |
| Capture metrics | `portfolio-artifact-skill` | haiku |
| Parallel build (worktrees) | `agent-teams-skill` | sonnet |
| Parallel build (in-session) | `subagent-teams-skill` | sonnet |
| Map task → best agent | `agent-capability-matrix-skill` | — |

### Native Agent Teams (Experimental)
```bash
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
claude --worktree  # auto-creates worktree branch
```

Features: DAG task system, peer-to-peer messaging, TeammateIdle/TaskCompleted hooks, shared task lists, `isolation: "worktree"` for subagents.

**Deep dive:** See `reference/agent-routing.md` for complete 70+ agent catalog

---

## PROGRESS RENDERING

Use TaskCreate with `activeForm` for live UI spinners:
```javascript
TaskCreate({ subject: "Plan architecture", activeForm: "Planning architecture" })
TaskUpdate({ taskId: "1", status: "in_progress" })  // → live spinner
TaskUpdate({ taskId: "1", status: "completed" })     // → checkmark
```

Use `addBlockedBy` for phase sequencing. Markdown tables for summaries.

---

## CLAUDE CODE COMMANDS

| Command | Workflow |
|---------|----------|
| `/start-day` | Start Day — context scan, Observer spawn, cost status |
| `/build-feature <name>` | Feature Dev — contract → build → observe → ship |
| `/end-day` | End Day — Observer report, security sweep, context save |
| `/quick-fix <issue>` | Debug — evidence → hypothesis → fix |
| `/cost-check` | Display daily/MTD spend and budget status |

---

## GTME PERSPECTIVE

This dual-team workflow demonstrates advanced GTME capabilities:

1. **Process Engineering** — Quality control built into lifecycle, not bolted on
2. **Parallel Orchestration** — Managing concurrent teams with different objectives
3. **Adversarial Thinking** — Devil's advocate prevents "happy path only" trap
4. **Cost Awareness** — Observers use cheaper models; unit economics thinking
5. **Measurable Output** — Observer reports quantify debt, coverage, compliance

**Portfolio Value:** Produces auditable artifacts demonstrating engineering discipline + process thinking + cost optimization.

## Emit Outcome Sidecar

As the final step, write to `~/.claude/skill-analytics/last-outcome-workflow-orchestrator.json`:
```json
{"ts":"[UTC ISO8601]","skill":"workflow-orchestrator","version":"2.0.0","variant":"default",
 "status":"[success|partial|error]","runtime_ms":[estimated ms from start],
 "metrics":{"workflows_run":[n],"stages_completed":[n],"observers_spawned":[n]},
 "error":null,"session_id":"[YYYY-MM-DD]"}
```
Use status "partial" if some stages failed but results were produced. Use "error" only if no output was generated.
