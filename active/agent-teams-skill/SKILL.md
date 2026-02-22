---
name: "agent-teams"
description: "Orchestrate teams of parallel Claude Code sessions working on the same codebase. Handles task decomposition, agent coordination, context isolation, and merge strategies. Builds on worktree-manager for infrastructure."
---

<objective>
Coordinate teams of 2-3 Claude Code agents working in parallel on the same codebase. Each agent runs in its own terminal, its own git worktree, and its own context window. The team lead (you, the orchestrating Claude) decomposes work, spawns agents with focused prompts, monitors progress, and coordinates merges.

**Key principle:** Each agent is a fresh Claude session with zero shared memory. All coordination happens through files (WORKTREE_TASK.md, shared contracts) and git (branches, PRs). There is no runtime communication between agents.
</objective>

<quick_start>
**Set the environment variable (one-time):**
```bash
export AGENT_TEAMS_MAX=3  # M1/8GB safe default
```

**Spawn a 2-agent team:**
```
"Set up a team: Agent 1 builds the API endpoints, Agent 2 builds the React components.
They share this contract: POST /api/tasks returns { id, title, status }."
```

**What happens:**
1. Team lead creates 2 worktrees via worktree-manager
2. Writes WORKTREE_TASK.md with focused prompt + contract to each
3. Launches each agent in its own Ghostty terminal
4. Agents work independently, team lead monitors and merges
</quick_start>

<success_criteria>
A team session is successful when:
- Each agent completes its assigned task in its worktree
- No merge conflicts between agent branches (or conflicts are trivially resolvable)
- Each agent's context stays focused (no bloat, no re-reading unrelated code)
- All agent work passes the project's test suite after merge
- Total wall-clock time is less than sequential execution would take
</success_criteria>

<setup>

## Prerequisites

**Required skill:** [worktree-manager](../worktree-manager-skill/SKILL.md) — agent-teams delegates ALL worktree creation, port allocation, and terminal launching to worktree-manager. Install it first.

**Recommended:** Project has a `.claude/` directory with CLAUDE.md (dev commands, conventions). If the project also has `.claude/agents/` with custom subagents or `.claude/settings.json` with hooks/permissions, these are automatically propagated to each agent's worktree.

**Environment check:**
```bash
# Agent teams config
echo "Max agents: ${AGENT_TEAMS_MAX:-3}"

# Worktree manager available?
ls ~/.claude/skills/worktree-manager/ 2>/dev/null && echo "worktree-manager: OK" || echo "worktree-manager: MISSING"

# Running agents (approximate)
pgrep -f "claude.*--model" | wc -l | xargs echo "Active Claude processes:"

# Memory pressure
vm_stat | grep "Pages free" | awk '{print "Free pages:", $3}'
```

<current_state>
Active agents:
!`pgrep -f "claude.*--model" 2>/dev/null | wc -l | tr -d ' '` Claude processes running

Worktree registry:
!`cat ~/.claude/worktree-registry.json 2>/dev/null | jq -r '.worktrees[] | select(.status == "active") | "\(.project)/\(.branch)"' | head -5`

Memory:
!`memory_pressure 2>/dev/null | head -1 || echo "Unknown"`

Git status:
!`git status --short --branch 2>/dev/null | head -3`
</current_state>

### Hardware Constraints (M1/8GB)

| Resource | Budget | Per Agent | System Reserved |
|----------|--------|-----------|-----------------|
| RAM | 8 GB | ~1.5 GB | 2 GB |
| CPU cores | 8 | Shared | — |
| Max agents | 3 | — | — |

**Rule of thumb:** If `memory_pressure` reports "WARN" or higher, reduce to 2 agents.

</setup>

<when_to_use>

## When to Use Agent Teams

**Use when:**
- Task naturally decomposes into 2-3 independent work streams
- Each stream touches different files (low conflict risk)
- Wall-clock speed matters more than token efficiency
- You have clear contracts between components (API shape, shared types)

**Don't use when:**
- Task is tightly coupled (every change touches the same files)
- You're on battery with <30% charge (agents drain power fast)
- Memory pressure is already high (check `memory_pressure`)
- The codebase has no tests (merging blind is risky)

**Decision heuristic:**
```
Can I describe each agent's task in <50 words?
  YES → Good candidate for agent teams
  NO  → Break it down more, or do it sequentially
```

**Lightweight alternative:** For tasks where agents DON'T need file isolation (different files, read-only, reviews), use [subagent-teams](../subagent-teams-skill/SKILL.md) instead. It uses Claude's native Task tool for in-session parallel agents — faster startup, no worktrees needed. See also the **Native Teams API** section below.

</when_to_use>

<architecture>

## Architecture

```
┌──────────────────────────────────────────────────┐
│                   TEAM LEAD                       │
│            (this Claude session)                  │
│                                                   │
│  Responsibilities:                                │
│  • Decompose task into agent assignments          │
│  • Create worktrees (via worktree-manager)        │
│  • Write WORKTREE_TASK.md for each agent          │
│  • Monitor progress (git log, file checks)        │
│  • Coordinate merges back to main                 │
└─────────┬───────────────┬───────────────┬────────┘
          │               │               │
    ┌─────▼─────┐   ┌─────▼─────┐   ┌─────▼─────┐
    │  AGENT 1  │   │  AGENT 2  │   │  AGENT 3  │
    │           │   │           │   │           │
    │ Worktree: │   │ Worktree: │   │ Worktree: │
    │ ~/tmp/wt/ │   │ ~/tmp/wt/ │   │ ~/tmp/wt/ │
    │ proj/br-1 │   │ proj/br-2 │   │ proj/br-3 │
    │           │   │           │   │           │
    │ Terminal: │   │ Terminal: │   │ Terminal: │
    │ Ghostty 1 │   │ Ghostty 2 │   │ Ghostty 3 │
    └───────────┘   └───────────┘   └───────────┘
         │               │               │
         └───── git branches ─────────────┘
                     │
               [main branch]
```

### Context Isolation

Each agent is a **completely separate Claude session**. Agents:
- Cannot read each other's context windows
- Cannot send messages to each other
- Share state ONLY through the filesystem and git
- Read their task from `WORKTREE_TASK.md` on startup

### Coordination Through Files

| File | Purpose | Written By | Read By |
|------|---------|------------|---------|
| `WORKTREE_TASK.md` | Agent's assignment + context | Team lead | Agent |
| `CONTRACT.md` | Shared API/interface definitions | Team lead | All agents |
| `.agent-status` | Agent self-reports progress | Agent | Team lead |
| `.claude/CLAUDE.md` | Project conventions, dev commands | Project | Agent (auto-loaded) |
| `.claude/settings.json` | Hooks (auto-format), permissions | Project | Agent (auto-loaded) |
| `.claude/agents/*.md` | Custom subagent definitions | Project | Agent (on dispatch) |
| Git commits | Work product | Agent | Team lead at merge |

</architecture>

<display_modes>

## Display Modes

| Mode | Terminal | How |
|------|----------|-----|
| `in-process` | Any terminal | All teammates in main terminal. `Shift+Down` to cycle, `Ctrl+T` for task list. |
| `split-pane` | tmux or iTerm2 only | Each teammate gets own pane. Click pane to interact. |

Config: `"teammateMode": "auto"` in `~/.claude/settings.json`. CLI: `claude --teammate-mode in-process`. Ghostty requires tmux wrapper for split-pane.

</display_modes>

<workflows>

## Workflows

| Workflow | Purpose |
|----------|---------|
| 1. Spawn a Team | Decompose → JSON roadmap → worktrees → task files → launch → monitor |
| 2. Write WORKTREE_TASK.md | Context, assignment, file boundaries, contract, verification, completion protocol |
| 3. Monitor Progress | `git log` per branch + `.agent-status` checks |
| 4. Merge Agent Work | Merge in planned order, test after each, `--no-ff` |
| 5. Async Handoff | `@claude` bot on GitHub PRs for long-running tasks |
| 6. Plan Mode | Explore codebase read-only before committing to decomposition |
| 7. Native Teams API | `TeamCreate` + `TaskCreate` + `SendMessage` for in-session teams without worktrees |

**Native vs Worktree decision:** Different files → Native Teams API. Same files → Worktrees. Real-time messaging → Native. Long-running processes → Worktrees.

See `reference/workflows-detailed.md` for step-by-step instructions, WORKTREE_TASK.md template, merge protocol, and Native Teams API examples.

</workflows>

<use_cases>

## Team Patterns

### Feature Parallel
2-3 agents build independent features simultaneously. Lowest conflict risk.
**Best for:** Sprint-style parallel feature work.
**See:** `reference/prompt-templates.md#feature-parallel` for spawn prompts.

### Frontend / Backend
One agent builds the API, another builds the UI. Connected by a shared contract.
**Best for:** Full-stack features where API and UI are clearly separable.
**See:** `reference/prompt-templates.md#frontend-backend` for spawn prompts.

### Test / Implement (TDD Pair)
Agent 1 writes tests first, commits and pushes. Agent 2 pulls tests and implements until they pass.
**Best for:** High-quality code where test coverage matters.
**See:** `reference/prompt-templates.md#test-implement` for spawn prompts.

### Review / Refactor
Agent 1 refactors code. Agent 2 reviews the refactored code and writes improvement suggestions.
**Best for:** Large refactoring tasks that benefit from a second perspective.
**See:** `reference/prompt-templates.md#review-refactor` for spawn prompts.

</use_cases>

<best_practices>

## Best Practices

- **Isolate context per agent** — only relevant info in WORKTREE_TASK.md, keep tasks to <50 words
- **Use external state** — `.agent-status`, git commits, `WORKTREE_TASK.md` (agents have no shared memory)
- **Front-load instructions** — most important info at TOP of task files
- **Contract-first** — define shared API shapes in `CONTRACT.md` BEFORE spawning agents
- **Merge order matters** — foundation (API) before consumer (UI), test after each, use `--no-ff`
- **Project config inheritance** — `.claude/` dir auto-copied gives agents CLAUDE.md, hooks, permissions, custom subagents
- **Team hooks** — `TeammateIdle` and `TaskCompleted` hooks use exit code 2 to keep working / block completion

See `reference/best-practices-full.md` for context engineering, session harness patterns, permissions model, and hook configuration.

<limitations>

## Limitations

### M1/8GB Constraints
- **Max 3 agents** — Beyond this, memory pressure causes thrashing
- **No GPU agents** — All agents are CPU-bound Claude sessions
- **Startup time** — Each agent takes 5-10s to initialize

### Coordination Limits
- **No real-time communication** — Worktree agents can't message each other (but native Teams API agents can — see Workflow 7)
- **File conflicts** — If two agents edit the same file, manual resolution needed
- **No shared context** — Each agent starts fresh with only WORKTREE_TASK.md
- **Sequential dependency** — If Agent 2 needs Agent 1's output, Agent 2 must wait

### Native Agent Teams Constraints

Known constraints of Claude Code's native agent teams:

| Limitation | Details |
|-----------|---------|
| **No session resumption** | `/resume` does not restore in-process teammates. Only the lead agent resumes. |
| **No nested teams** | Teammates cannot spawn sub-teams. Only one level of team hierarchy. |
| **One team per session** | Clean up current team (TeamDelete) before starting a new one. |
| **Lead is fixed** | Cannot promote teammates or transfer leadership mid-session. |
| **Permissions at spawn** | Teammate permissions set at spawn time. Can adjust per-teammate after creation, not during spawn. |
| **Shutdown can be slow** | Teammates finish their current request before shutting down. Plan for graceful wind-down. |

### What This Skill Is NOT
- **Not a CI/CD pipeline** — Use GitHub Actions for automated testing
- **Not a subagent framework** — Subagents (Claude's built-in Task tool) run within one session. This skill coordinates SEPARATE sessions.
- **Not auto-scaling** — You manually decide team size and assignments

</limitations>

<troubleshooting>

## Troubleshooting

### Agent not reading WORKTREE_TASK.md
**Cause:** Agent started without `--dangerously-skip-permissions` or task file not in worktree root.
**Fix:** Ensure worktree-manager writes the task file to the worktree root directory.

### Merge conflicts between agents
**Cause:** Agents edited overlapping files despite file boundary instructions.
**Fix:**
1. Check if boundaries were clear in WORKTREE_TASK.md
2. Resolve conflicts manually on main
3. Next time, use stricter file boundaries

### Agent runs out of context
**Cause:** Agent's task was too broad, causing it to read too many files.
**Fix:** Break the task into smaller pieces. Each agent should touch <10 files.

### Memory pressure / system slowdown
**Cause:** Too many agents for available RAM.
**Fix:**
1. Reduce to 2 agents
2. Close non-essential applications
3. Check `memory_pressure` before spawning

### Agent completes but work is wrong
**Cause:** Insufficient verification steps in WORKTREE_TASK.md.
**Fix:** Add explicit verification commands:
```markdown
## Verification
1. Run: npm test -- --filter auth
2. Run: npx tsc --noEmit
3. Manually test: curl localhost:8100/api/auth/login
```

</troubleshooting>

<routing>

## Reference Files

Load these on demand when you need deeper guidance:

| Reference | Load When |
|-----------|-----------|
| `reference/workflows-detailed.md` | Step-by-step spawn, monitor, merge, async handoff, Native Teams API |
| `reference/best-practices-full.md` | Context engineering, session harness, contract-first, hooks config |
| `reference/context-engineering.md` | Designing agent prompts, optimizing context usage, delegation patterns |
| `reference/worktree-integration.md` | Coordinating with worktree-manager, port allocation, terminal strategies |
| `reference/prompt-templates.md` | Need ready-to-use spawn prompts for the 4 team patterns |

</routing>
