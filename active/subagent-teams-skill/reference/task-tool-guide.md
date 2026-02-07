# Task Tool Guide

## Available Subagent Types

| Type | Tools Available | Best For |
|------|----------------|----------|
| `Explore` | Glob, Grep, LS, Read, WebFetch, WebSearch | Fast codebase exploration |
| `general-purpose` | All tools | Multi-step tasks, code changes |
| `Plan` | All except Edit, Write, NotebookEdit | Architecture planning |
| `code-reviewer` | Read-only + analysis tools | Code review |
| `code-explorer` | Read-only + analysis tools | Deep code analysis |
| `code-architect` | Read-only + analysis tools | Feature architecture |

## Parameters Reference

```javascript
{
  // Required
  subagent_type: "Explore",           // Agent type from table above
  prompt: "Search for auth patterns",  // Clear, self-contained task
  description: "Find auth patterns",   // 3-5 word summary

  // Optional
  model: "haiku",                      // haiku | sonnet | opus
  run_in_background: true,             // For parallel execution
  mode: "plan",                        // Permission mode
  max_turns: 10                        // Limit agent iterations
}
```

## Parallel Execution Pattern

To run multiple agents in parallel, include multiple Task tool calls in a single message:

```
Message 1:
  Task(agent1, run_in_background=true)
  Task(agent2, run_in_background=true)
  Task(agent3, run_in_background=true)

Message 2 (after all complete):
  Read output files or check TaskOutput
  Synthesize results
```

## Important Constraints

- Background agents return output files — read them with Read tool
- Agents cannot see each other's context
- Each agent starts fresh (no shared memory)
- Max ~7 parallel agents before context fills up
- Use `resume` parameter to continue a previous agent's work
