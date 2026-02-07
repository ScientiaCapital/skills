# Context Engineering for Agent Teams

> Adapted from Anthropic's context engineering patterns for multi-agent coordination.

---

## Core Principle: Context Is Finite

Each Claude agent has a fixed context window. In a team setting, this means:

- **Don't duplicate context across agents.** Agent 1 doesn't need Agent 2's task details.
- **Don't front-load the entire codebase.** Each agent should only see files relevant to its task.
- **Plan context budgets.** A well-scoped WORKTREE_TASK.md uses ~500-1000 tokens. The rest is for the agent to read code and work.

### Context Budget Per Agent

| Content | Typical Tokens | Notes |
|---------|---------------|-------|
| WORKTREE_TASK.md | 500-1000 | Task description, contract, boundaries |
| Relevant source files | 2000-8000 | Agent reads as needed |
| Test files | 1000-3000 | For verification |
| Working memory | Remaining | Agent's internal reasoning |

**Rule:** Keep WORKTREE_TASK.md under 1000 tokens. If it's longer, the task is too complex for one agent.

---

## External Progress Tracking

Agents have no persistent memory between turns (within a session they do, but not across sessions). Track progress externally:

### File-Based State

```
worktree-root/
├── WORKTREE_TASK.md      # Agent's briefing (written by team lead)
├── .agent-status          # Simple status flag: STARTING | IN_PROGRESS | DONE | ERROR
├── CONTRACT.md            # Shared interfaces (optional, for multi-agent contracts)
└── ... (normal project files)
```

### Git-Based State

Git commits are the most reliable state tracking mechanism:
- Each commit is a checkpoint of agent progress
- `git log --oneline branch-name -5` gives quick progress overview
- Commit messages serve as agent "status updates"

### Status File Protocol

Agents should update `.agent-status` at key milestones:

```bash
# Agent startup
echo "STARTING: Reading task and checking environment" > .agent-status

# Agent working
echo "IN_PROGRESS: Implementing auth endpoints (3/5 done)" > .agent-status

# Agent done
echo "DONE: All endpoints implemented and tested" > .agent-status

# Agent error
echo "ERROR: Cannot install dependencies - missing native module" > .agent-status
```

---

## Delegation Patterns

### Pattern 1: Fan-Out (Most Common)

Team lead decomposes task → spawns N agents → waits → merges.

```
Lead: "Build auth system"
  ├─→ Agent 1: "Build API endpoints" (independent)
  ├─→ Agent 2: "Build UI components" (independent)
  └─→ Agent 3: "Write integration tests" (depends on 1 & 2)
```

**Execution:** Spawn agents 1 and 2 in parallel. Spawn agent 3 after 1 and 2 complete.

### Pattern 2: Pipeline

Output of Agent 1 feeds into Agent 2.

```
Agent 1: Write tests → push branch
Agent 2: Pull Agent 1's branch → implement until tests pass
```

**Execution:** Sequential. Agent 2 starts after Agent 1 pushes.

### Pattern 3: Contract-First

Team lead writes shared contract → all agents implement against it.

```
Lead: Write CONTRACT.md with API types
  ├─→ Agent 1: Implement server (matches contract)
  └─→ Agent 2: Implement client (matches contract)
```

**Execution:** Parallel after contract is written.

---

## Context Window Management

### Signs of Context Bloat

An agent's context is bloated if:
- It starts re-reading files it already read
- Responses become slow or repetitive
- It loses track of what it was doing
- It asks questions that are answered in WORKTREE_TASK.md

### Prevention Strategies

1. **Narrow file boundaries** — Tell agents exactly which directories to work in. "Work in `src/api/auth/`. Do NOT explore other directories."

2. **Pre-read files for the agent** — In WORKTREE_TASK.md, include key code snippets the agent will need instead of making it search:
   ```markdown
   ## Existing Code You'll Need
   The user model is at `src/models/user.ts`:
   ```typescript
   interface User { id: string; email: string; role: 'admin' | 'user' }
   ```
   ```

3. **One task per agent** — Never give an agent multiple unrelated tasks. "Build auth AND fix the dashboard layout" should be two agents.

4. **Limit reference material** — Link to docs sparingly. If an agent needs a library's API, include the 5 relevant methods, not the whole documentation.

---

## Team Lead Context Management

The team lead (orchestrating Claude) also has finite context. Strategies:

1. **Use the JSON roadmap** — Externalize the team plan to a structured format instead of holding it in memory.

2. **Check progress incrementally** — Don't read all agent branches at once. Check one at a time:
   ```bash
   git log --oneline feature/auth-api -3
   ```

3. **Delegate monitoring to shell commands** — Use `for` loops and `git log` instead of manually tracking each agent.

4. **Summarize, don't replay** — When reporting team status to the user, summarize ("Agent 1 completed 3 commits, Agent 2 is still working") rather than showing all details.

---

## Anti-Patterns

| Anti-Pattern | Why It Fails | Better Approach |
|-------------|-------------|-----------------|
| Sharing full codebase context with every agent | Context bloat, agents confused by irrelevant code | Narrow file boundaries per agent |
| Verbal contracts ("Agent 1, just make sure it works with Agent 2") | Agents can't communicate | Written CONTRACT.md with types |
| No verification steps | Agent may produce broken code | Explicit test commands in task |
| Spawning 5+ agents on 8GB RAM | Memory thrashing, all agents slow | Max 3 agents, monitor pressure |
| Having agents read each other's code | Cross-contamination, context waste | Strict file boundaries |
| Over-detailed WORKTREE_TASK.md (2000+ tokens) | Buries the actual task in noise | Keep under 1000 tokens |

---

## Further Reading

- Anthropic Blog: "Building Effective Agents" — delegation and tool-use patterns
- Anthropic Blog: "Context Engineering" — managing context as a resource
- `../SKILL.md` — main skill reference with workflows
- `worktree-integration.md` — infrastructure coordination
