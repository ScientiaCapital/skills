# Workflows (Detailed)

## 1. Spawn a Team

**User says:** "Set up a team to build the auth system. Agent 1 does the API, Agent 2 does the UI."

**Team lead does:**

```
STEP 1: DECOMPOSE
─────────────────
Break the request into agent assignments. Each assignment needs:
  - Clear scope (which files/directories)
  - Input contract (what data shapes to expect)
  - Output contract (what to produce)
  - Completion signal (how to know it's done)

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
  - CLAUDE.md — project conventions, dev commands, tech stack
  - .claude/settings.json — PostToolUse hooks (auto-format), permissions
  - .claude/agents/ — custom subagents (build-validator, verify-app, etc.)

STEP 4: WRITE TASK FILES
─────────────────────────
Write WORKTREE_TASK.md to each worktree with:
  - Task description (what to build)
  - File boundaries (what NOT to touch)
  - Contract (shared interfaces)
  - Verification steps (how to self-check)
  - Completion protocol (commit, push, update .agent-status)

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

## 2. Write a WORKTREE_TASK.md

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

## 3. Monitor Team Progress

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

## 4. Merge Agent Work

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

## 5. Async Handoff with @claude Bot

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

## 6. Plan Mode for Complex Decomposition

For non-trivial task decomposition, use Claude Code's plan mode:

```
"Enter plan mode and design the team decomposition for [feature].
Identify file boundaries, contracts, and merge order before spawning agents."
```

Plan mode lets you explore the codebase (read-only) and design the team structure before committing to any worktree creation. This prevents wasted effort from bad decomposition.

## 7. Native Teams API Alternative

For teams that don't need full worktree isolation, Claude Code provides native coordination APIs. These are ideal when agents work on different files or do read-only tasks:

```javascript
// Create a team with shared task list
TeamCreate({ team_name: "feature-sprint" })

// Track progress with native UI (live spinners + checkmarks)
TaskCreate({ subject: "Build API endpoints", activeForm: "Building API endpoints" })
TaskCreate({ subject: "Build UI components", activeForm: "Building UI components" })

// Spawn teammates into the team
Task({ subagent_type: "general-purpose", team_name: "feature-sprint", name: "api-builder", prompt: "..." })
Task({ subagent_type: "general-purpose", team_name: "feature-sprint", name: "ui-builder", prompt: "..." })

// Coordinate via messages (real-time, unlike worktree agents)
SendMessage({ type: "message", recipient: "api-builder", content: "Contract updated: add status field" })

// Shutdown when done
SendMessage({ type: "shutdown_request", recipient: "api-builder" })
SendMessage({ type: "shutdown_request", recipient: "ui-builder" })
```

**When to use native Teams API vs worktrees:**
- Agents edit **different files** → Native Teams API (simpler, faster)
- Agents edit **same files** → Worktrees (git isolation prevents conflicts)
- Agents need **separate terminals / long-running processes** → Worktrees
- Agents need **real-time messaging** → Native Teams API

**DAG task dependencies:** Tasks support `blocks` and `blockedBy` fields for dependency ordering. File locking is used for concurrent task claiming to prevent race conditions.

**Storage paths:**
- Team config: `~/.claude/teams/{name}/config.json`
- Tasks: `~/.claude/tasks/{name}/`

**Keyboard shortcuts:** Use `Shift+Down` to cycle between teammates and `Ctrl+T` to toggle the task list view.

See [subagent-teams](../subagent-teams-skill/SKILL.md) for the complete Task tool reference and team patterns.
