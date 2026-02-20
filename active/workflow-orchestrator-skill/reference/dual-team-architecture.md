# Dual-Team Architecture

> Reference for workflow-orchestrator v2.0.0
> The full specification for Builder + Observer concurrent team pattern.

---

## Overview

Every development session runs two concurrent agent teams under one Orchestrator:

```
                    ┌─────────────────────┐
                    │    ORCHESTRATOR      │
                    │  (workflow-orchestr) │
                    └──────────┬──────────┘
                               │
              ┌────────────────┴────────────────┐
              ▼                                 ▼
    ┌──────────────────┐              ┌──────────────────┐
    │   BUILDER TEAM   │              │  OBSERVER TEAM   │
    │  (ships features)│              │ (watches quality)│
    │                  │              │                  │
    │ • Lead Builder   │              │ • Code Quality   │
    │ • Builder(s)     │              │ • Architecture   │
    │ • Devil's Adv.   │              │   (Devil's Adv.) │
    └──────────────────┘              └──────────────────┘
```

**Key principle:** Observer team is non-negotiable. It always runs, even for "small" changes. Builders optimize for velocity; Observers optimize for correctness. The tension between them produces better code.

---

## Team Compositions

### Builder Team (1-3 agents)

| Role | Model | Responsibility |
|------|-------|----------------|
| Lead Builder | sonnet | Architecture decisions, merges, scope enforcement |
| Builder Agent(s) | sonnet | Feature implementation in isolated worktrees |
| Devil's Advocate | sonnet | Challenges assumptions, finds failure modes (rotated among builders) |

**Spawn:** Via `agent-teams-skill` (worktree sessions) or `subagent-teams-skill` (Task tool subagents)

### Observer Team (2 agents, always active)

| Role | Model | Responsibility |
|------|-------|----------------|
| Code Quality Observer | haiku/sonnet | Tech debt, test gaps, import bloat, silent failures |
| Architecture Observer | sonnet | Contract drift, scope creep, design violations (inherent devil's advocate) |

**Spawn:** Automatically at START DAY, or manually via `workflow-orchestrator`

---

## Devil's Advocate Pattern

Each team has an adversarial role to prevent groupthink:

- **Builder Team:** One builder's prompt includes adversarial instructions — challenge before implementing, verify edge cases before committing
- **Observer Team:** Architecture Observer IS the devil's advocate by default — its entire mandate is to find what's wrong

See `reference/devils-advocate.md` for full prompt templates and escalation protocol.

---

## Contract Definition (Before Code)

Before ANY feature implementation, define the contract:

```markdown
## Feature Contract: [NAME]

### Endpoints / Interfaces
- POST /api/widgets → { id, name, created_at }
- GET /api/widgets/:id → { id, name, items[], created_at }

### Scope Boundaries
- IN SCOPE: CRUD operations, input validation, error responses
- OUT OF SCOPE: caching, pagination, auth (separate PR)

### Success Criteria
- [ ] All endpoints return correct shapes
- [ ] Input validation rejects invalid data
- [ ] Error responses follow API design skill patterns
- [ ] Test coverage ≥ 80%

### Observer Checkpoints
- [ ] Architecture Observer approves contract before coding starts
- [ ] Code Quality Observer runs after each merge to main
```

The contract is the **single source of truth**. Observers measure drift against it.

---

## Observer Monitoring Loop

Observers run concurrently with Builders on a continuous loop:

```
┌─────────────────────────────────────────────┐
│  OBSERVER LOOP (every 5-10 minutes)         │
│                                             │
│  1. Pull latest from builder branches       │
│  2. Run drift detection patterns            │
│  3. Write findings to .claude/OBSERVER_*.md │
│  4. If BLOCKER found → write OBSERVER_ALERTS│
│  5. Orchestrator checks OBSERVER_ALERTS.md  │
│     before allowing next phase gate         │
│                                             │
│  Severity levels:                           │
│  🔴 BLOCKER — stop work, fix immediately    │
│  🟡 WARNING — fix before merge or log       │
│  🔵 INFO    — nice to have, backlog         │
└─────────────────────────────────────────────┘
```

See `reference/observer-patterns.md` for the 7 drift detection patterns.

---

## Skill → Phase Mapping

How skills integrate into the dual-team workflow:

| Phase | Skills Used | Who Runs It |
|-------|------------|-------------|
| START DAY: Context | project-context-skill | Orchestrator |
| START DAY: Observer Spawn | workflow-orchestrator | Orchestrator |
| START DAY: Sprint Plan | planning-prompts-skill | Orchestrator |
| FEATURE: Contract | api-design-skill | Lead Builder |
| FEATURE: Implementation | agent-teams / subagent-teams | Builders |
| FEATURE: Monitoring | workflow-orchestrator | Observers |
| FEATURE: Debug | debug-like-expert-skill | Builder (on failure) |
| FEATURE: Security Gate | security-skill | Orchestrator |
| FEATURE: Tests | testing-skill | Builders + Observers |
| END DAY: Observer Report | workflow-orchestrator | Observers |
| END DAY: Security Sweep | security-skill | Orchestrator |
| END DAY: Metrics | portfolio-artifact-skill, cost-metering-skill | Orchestrator |
| END DAY: Context Save | project-context-skill | Orchestrator |

---

## File Structure for Observer Outputs

Observers write their findings to the project's `.claude/` directory:

```
.claude/
├── OBSERVER_QUALITY.md     # Code Quality Observer findings
├── OBSERVER_ARCH.md        # Architecture Observer findings
├── OBSERVER_ALERTS.md      # Escalated blockers (checked by Orchestrator)
└── OBSERVER_HISTORY/       # Archived reports (per session)
    ├── 2026-02-20-quality.md
    └── 2026-02-20-arch.md
```

Templates for these files: `templates/OBSERVER_QUALITY.md`, `templates/OBSERVER_ARCH.md`

---

## Native Agent Teams Integration

Claude Code v2.1.49+ includes experimental Agent Teams support:

```bash
# Enable experimental Agent Teams
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1

# New: --worktree flag for isolated sessions
claude --worktree  # auto-creates worktree branch
```

### What Native Teams Provides

| Feature | Description | Replaces |
|---------|-------------|----------|
| `TeamCreate` | Creates team with shared task list | Manual worktree coordination |
| `SendMessage` | Peer-to-peer agent messaging | WORKTREE_TASK.md polling |
| `TaskCreate/TaskUpdate` | DAG task system with dependencies | Manual TodoWrite tracking |
| `TeammateIdle` hook | Notifies when agent finishes turn | Manual status checking |
| `TaskCompleted` hook | Fires when task marked done | Manual completion polling |
| `--worktree` CLI flag | Auto-creates worktree branch | Manual `git worktree add` |
| `isolation: "worktree"` | Subagents run in temp worktrees | Manual isolation setup |

### When to Use Native vs Manual

| Scenario | Approach | Why |
|----------|----------|-----|
| Short tasks (<20 min) | Native Agent Teams (Task tool) | Lower overhead, automatic coordination |
| Long tasks (30+ min) | Manual worktree sessions | More isolation, explicit control |
| Mixed workload | Hybrid — Native for Observers, worktrees for Builders | Best of both |

### Skill-Scoped Hooks

Hooks can be defined in SKILL.md frontmatter for automatic Observer triggers:

```yaml
hooks:
  - event: TaskCompleted
    command: "echo 'Observer: checking completed task...'"
  - event: TeammateIdle
    command: "echo 'Observer: teammate idle, running drift check...'"
```

---

## GTME Perspective

The dual-team architecture demonstrates advanced Go-To-Market Engineering capabilities:

1. **Process Engineering** — Systematic quality control built into the development lifecycle, not bolted on after
2. **Parallel Orchestration** — Managing concurrent teams with different objectives (velocity vs correctness)
3. **Adversarial Thinking** — Devil's advocate pattern prevents the "happy path only" trap common in solo development
4. **Cost Awareness** — Observer team uses cheaper models (Haiku) for routine checks, Sonnet only for complex analysis
5. **Measurable Output** — Every session produces Observer reports that quantify technical debt, test coverage deltas, and contract compliance

**Portfolio Value:** This workflow produces auditable artifacts (Observer reports, contract compliance metrics) that demonstrate engineering discipline — directly relevant for roles requiring technical depth + process thinking.

---

## Model Cost Reference (Feb 2026)

| Model | Input/1M | Output/1M | Team Role |
|-------|----------|-----------|-----------|
| Claude Opus 4.6 | $5.00 | $25.00 | Architecture decisions only |
| Claude Sonnet 4.6 | $3.00 | $15.00 | Builders, Lead, complex Observer |
| Claude Haiku 4.5 | $1.00 | $5.00 | Code Quality Observer, simple checks |
| TaskCreate/Update | $0.00 | $0.00 | Progress tracking (free, local UI) |
| TeamCreate/SendMessage | $0.00 | $0.00 | Team coordination (free, local UI) |

**Budget tip:** A typical dual-team session costs ~$2-5 for Builders + ~$0.50-2.00 for Observers (Haiku 4.5 is $1/$5, up from Haiku 3's $0.25/$1.25). The Observer team adds ~20-30% cost but catches issues that would cost 5-10x more to fix later.

---

## See Also

- `reference/observer-patterns.md` — 7 drift detection patterns with commands
- `reference/devils-advocate.md` — Adversarial prompt templates
- `templates/OBSERVER_QUALITY.md` — Code Quality report template
- `templates/OBSERVER_ARCH.md` — Architecture report template
- `active/agent-teams-skill/SKILL.md` — Worktree-based team orchestration
- `active/subagent-teams-skill/SKILL.md` — Task tool subagent teams
