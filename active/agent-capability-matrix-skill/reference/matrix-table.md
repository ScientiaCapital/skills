# Full Agent Capability Matrix

## Built-in Claude Code Agents

| Agent | subagent_type | Tools | Best For | Model |
|-------|---------------|-------|----------|-------|
| Explore | `Explore` | Glob, Grep, Read, LS, WebSearch | Fast codebase search | haiku |
| Plan | `Plan` | All read-only | Architecture design | opus |
| general-purpose | `general-purpose` | All tools | Any multi-step task | sonnet |

## Plugin Agents

| Agent | subagent_type | Focus | Model |
|-------|---------------|-------|-------|
| code-reviewer | `feature-dev:code-reviewer` | Bug/quality review | haiku |
| code-explorer | `feature-dev:code-explorer` | Deep code analysis | sonnet |
| code-architect | `feature-dev:code-architect` | Feature design | sonnet |
| code-simplifier | `code-simplifier:code-simplifier` | Simplify code | sonnet |
| pr-code-reviewer | `pr-review-toolkit:code-reviewer` | PR review | haiku |
| silent-failure-hunter | `pr-review-toolkit:silent-failure-hunter` | Error handling review | sonnet |
| pr-test-analyzer | `pr-review-toolkit:pr-test-analyzer` | Test coverage review | sonnet |
| type-design-analyzer | `pr-review-toolkit:type-design-analyzer` | Type design review | sonnet |
| comment-analyzer | `pr-review-toolkit:comment-analyzer` | Comment accuracy | haiku |
| superpowers-reviewer | `superpowers:code-reviewer` | Plan adherence review | sonnet |

## Skills (Trigger-Activated)

| Skill | Category | Triggers |
|-------|----------|----------|
| workflow-orchestrator | Core | "start day", "end day" |
| project-context | Core | "load context", "save context" |
| workflow-enforcer-skill | Core | Automatic |
| extension-authoring | Dev Tools | "create skill", "create hook" |
| debug-like-expert | Dev Tools | "debug systematically" |
| planning-prompts | Dev Tools | "create plan", "meta-prompt" |
| worktree-manager | Dev Tools | "create worktree" |
| agent-teams | Dev Tools | "set up agent team" |
| subagent-teams | Dev Tools | "subagent team", "fan out" |
| git-workflow | Dev Tools | "commit", "PR" |
| testing | Dev Tools | "write tests", "TDD" |
| api-design | Dev Tools | "design API" |
| security | Dev Tools | "security audit" |
| api-testing | Dev Tools | "postman", "API testing" |
| docker-compose | Dev Tools | "docker compose" |
| langgraph-agents | Infrastructure | "LangGraph agent" |
| groq-inference | Infrastructure | "groq", "fast inference" |
| openrouter | Infrastructure | "openrouter", "deepseek" |
| voice-ai | Infrastructure | "voice agent", "Deepgram" |
| unsloth-training | Infrastructure | "train with GRPO" |
| runpod-deployment | Infrastructure | "deploy to RunPod" |
| supabase-sql | Infrastructure | "fix SQL", "RLS" |
| stripe-stack | Infrastructure | "stripe", "payments" |
| gtm-pricing | Business | "GTM strategy", "pricing" |
| research | Business | "research company" |
| sales-revenue | Business | "cold email", "pipeline" |
| crm-integration | Business | "Close CRM", "HubSpot" |
| content-marketing | Business | "content strategy" |
| data-analysis | Business | "analyze data", "dashboard" |
| trading-signals | Business | "fibonacci", "elliott wave" |
| business-model-canvas | Strategy | "business model canvas" |
| blue-ocean-strategy | Strategy | "blue ocean", "ERRC" |
| cost-metering | Core | "cost check", "budget" |
| portfolio-artifact | Core | "capture metrics", "weekly summary" |
| agent-capability-matrix | Dev Tools | "which agent", "route task" |
| miro | Dev Tools | "miro board", "whiteboard" |
