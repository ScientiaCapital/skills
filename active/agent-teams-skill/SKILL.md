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

### Compact (Default)
Show team status as a single table:
```
Agent Team Status:
| # | Branch | Task | Status |
|---|--------|------|--------|
| 1 | feature/api | Build REST endpoints | ✅ Complete |
| 2 | feature/ui | Build React components | 🔄 In Progress |
```

### Detailed
Show per-agent context including recent commits and file changes.

### Monitoring
Continuous status with `git log` polling (for long-running teams).

</display_modes>

<workflows>

## Workflows

### 1. Spawn a Team

**User says:** "Set up a team to build the auth system. Agent 1 does the API, Agent 2 does the UI."

**Team lead does:**

```
STEP 1: DECOMPOSE
─────────────────
Break the request into agent assignments. Each assignment needs:
  • Clear scope (which files/directories)
  • Input contract (what data shapes to expect)
  • Output contract (what to produce)
  • Completion signal (how to know it's done)

STEP 2: CREATE JSON ROADMAP
────────────────────────────
Before spawning, create a coordination plan:

{
  "team": "auth-system",
  "agents": [
    {
      "id": 1,
      "branch": "feature/auth-api",
      "task": "Build auth API endpoints",
      "files": ["src/api/auth/", "src/middleware/"],
      "contract": "POST /api/auth/login → { token, user }",
      "done_when": "All endpoints pass tests"
    },
    {
      "id": 2,
      "branch": "feature/auth-ui",
      "task": "Build auth UI components",
      "files": ["src/components/auth/", "src/pages/login.tsx"],
      "contract": "Uses POST /api/auth/login → { token, user }",
      "done_when": "Login page renders and calls API"
    }
  ],
  "merge_order": [1, 2],
  "merge_target": "main"
}

STEP 3: CREATE WORKTREES
─────────────────────────
Use worktree-manager to create each worktree:
  → "create worktree feature/auth-api"
  → "create worktree feature/auth-ui"

worktree-manager automatically copies .claude/ directory to each worktree.
This gives each agent:
  • CLAUDE.md — project conventions, dev commands, tech stack
  • .claude/settings.json — PostToolUse hooks (auto-format), permissions
  • .claude/agents/ — custom subagents (build-validator, verify-app, etc.)

STEP 4: WRITE TASK FILES
─────────────────────────
Write WORKTREE_TASK.md to each worktree with:
  • Task description (what to build)
  • File boundaries (what NOT to touch)
  • Contract (shared interfaces)
  • Verification steps (how to self-check)
  • Completion protocol (commit, push, update .agent-status)

STEP 5: LAUNCH AGENTS
──────────────────────
Via worktree-manager terminal launching.
Each agent opens, reads WORKTREE_TASK.md, and starts working.

STEP 6: MONITOR (optional)
───────────────────────────
Check progress via git:
  git log --oneline feature/auth-api -5
  git log --oneline feature/auth-ui -5
```

### 2. Write a WORKTREE_TASK.md

The task file is the ONLY way to communicate with an agent. Make it count.

**Template:**
```markdown
# Task: [Agent's Assignment]

## Context
[2-3 sentences about what the broader project is doing and where this fits]

## Your Assignment
[Specific, measurable task description]

## File Boundaries
**Work in:** [directories/files this agent owns]
**Do NOT touch:** [directories/files another agent owns]

## Contract
[Shared interfaces, API shapes, type definitions]

## Verification
Before committing, verify:
1. [Specific check, e.g., "tests pass"]
2. [Specific check, e.g., "no type errors"]
3. [Specific check, e.g., "API returns expected shape"]

## When Done
1. Commit all changes with descriptive message
2. Push branch: `git push -u origin [branch]`
3. Write "DONE" to `.agent-status`
```

### 3. Monitor Team Progress

```bash
# Quick check: last commit per agent branch
for branch in feature/auth-api feature/auth-ui; do
  echo "=== $branch ==="
  git log --oneline $branch -3 2>/dev/null || echo "No commits yet"
done

# Check agent status files
for wt in ~/tmp/worktrees/$(basename $(pwd))/*/; do
  echo "$(basename $wt): $(cat $wt/.agent-status 2>/dev/null || echo 'no status')"
done
```

### 4. Merge Agent Work

```
MERGE PROTOCOL:
1. Wait for all agents to report DONE (or timeout)
2. Merge in planned order (API before UI typically)
3. Run full test suite after each merge
4. Resolve any conflicts
5. Clean up worktrees via worktree-manager
```

**Merge commands:**
```bash
git checkout main
git merge feature/auth-api --no-ff -m "feat(auth): API endpoints"
npm test  # or project's test command
git merge feature/auth-ui --no-ff -m "feat(auth): UI components"
npm test
```

### 5. Async Handoff with @claude Bot

For longer-running agent work, use GitHub's `@claude` bot integration:

1. Agent creates PR from worktree branch
2. Add `@claude` comment on PR with instructions
3. Claude bot works asynchronously on the PR
4. You get notified when work is complete

**Use when:**
- Agent task will take >30 minutes
- You want to step away from the terminal
- Task involves iterative PR feedback cycles

**Workflow:**
```bash
# Agent pushes branch and creates PR
gh pr create --title "feat(auth): API endpoints" --body "API implementation"

# You (or the agent) tags @claude on the PR
# @claude "Review this implementation and fix any test failures"

# Claude bot works asynchronously, commits to the branch
# You monitor at https://github.com/<org>/<repo>/pulls
```

### 6. Plan Mode for Complex Decomposition

For non-trivial task decomposition, use Claude Code's plan mode:

```
"Enter plan mode and design the team decomposition for [feature].
Identify file boundaries, contracts, and merge order before spawning agents."
```

Plan mode lets you explore the codebase (read-only) and design the team structure before committing to any worktree creation. This prevents wasted effort from bad decomposition.

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

### Context Engineering for Teams

**Each agent gets minimal, focused context.** This is the #1 factor in agent team success.

1. **Isolate context per agent** — An agent building the API doesn't need to know about React component patterns. Put only relevant information in WORKTREE_TASK.md.

2. **Use external state, not agent memory** — Agents forget everything between sessions. Track progress in files:
   - `.agent-status` — simple status flag
   - Git commits — work product audit trail
   - `WORKTREE_TASK.md` — the "briefing document"

3. **Front-load instructions** — Put the most important information (task, contract, boundaries) at the TOP of WORKTREE_TASK.md. Agents read top-down and may deprioritize content at the bottom.

4. **Keep agent tasks to <50 words** — If you can't describe an agent's task concisely, it's too complex. Break it down further.

### Project Config Inheritance

Each agent inherits the project's `.claude/` directory, which ensures consistency:

**CLAUDE.md inheritance** — Agents auto-load the project's CLAUDE.md on startup, giving them:
- Dev commands (`npm test`, `bun run build`, etc.)
- Code style conventions
- Tech stack context
- File structure documentation

**PostToolUse hooks** — If the project uses auto-formatting hooks (e.g., `bun run format || true` after Write/Edit), every agent runs them too. This prevents style conflicts at merge time.

**Permissions model** — Two approaches for agent safety:
```bash
# Option A: Skip all permissions (faster, less safe)
claude --model opus --dangerously-skip-permissions

# Option B: Explicit allowlist (safer, from .claude/settings.json)
claude --model opus --allowedTools "Bash(npm test),Bash(npm run build),Edit,Write,Read"
```

**Custom subagents** — If the project has `.claude/agents/` (e.g., `verify-app.md`, `build-validator.md`), agents can dispatch them for verification steps:
```markdown
## Verification
1. Run tests: `npm test`
2. Run build validator: dispatch `.claude/agents/build-validator.md`
3. Run verify-app: dispatch `.claude/agents/verify-app.md`
```

### Session Harness Patterns

Adapted from Anthropic's session harness methodology:

1. **Startup protocol** — Each agent should:
   - Read WORKTREE_TASK.md first
   - Check for existing work (`git log`, file listing)
   - Confirm understanding before starting

2. **Verification loops** — Build self-checks into agent tasks:
   ```
   After each major change:
   1. Run tests: npm test
   2. Check types: npx tsc --noEmit
   3. If failing, fix before moving on
   ```

3. **Completion protocol** — Each agent must:
   - Run final verification
   - Commit with descriptive message
   - Push branch
   - Update `.agent-status` to "DONE"

### Contract-First Development

When agents need to integrate, define the contract BEFORE spawning:

```typescript
// CONTRACT: Auth API Shape (shared between agents)
interface AuthResponse {
  token: string;
  user: { id: string; email: string; role: string };
}

// POST /api/auth/login
// Body: { email: string; password: string }
// Response: AuthResponse
```

Write this contract to a `CONTRACT.md` or shared type file that both agents can reference.

### Merge Strategy

1. **Merge order matters** — Merge the "foundation" branch first (usually API/backend), then the "consumer" branch (usually UI/frontend)
2. **Test after each merge** — Don't batch merges. Test incrementally.
3. **Use `--no-ff`** — Preserves branch history for debugging

</best_practices>

<limitations>

## Limitations

### M1/8GB Constraints
- **Max 3 agents** — Beyond this, memory pressure causes thrashing
- **No GPU agents** — All agents are CPU-bound Claude sessions
- **Startup time** — Each agent takes 5-10s to initialize

### Coordination Limits
- **No real-time communication** — Agents can't message each other
- **File conflicts** — If two agents edit the same file, manual resolution needed
- **No shared context** — Each agent starts fresh with only WORKTREE_TASK.md
- **Sequential dependency** — If Agent 2 needs Agent 1's output, Agent 2 must wait

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
| `reference/context-engineering.md` | Designing agent prompts, optimizing context usage, delegation patterns |
| `reference/worktree-integration.md` | Coordinating with worktree-manager, port allocation, terminal strategies |
| `reference/prompt-templates.md` | Need ready-to-use spawn prompts for the 4 team patterns |

</routing>
