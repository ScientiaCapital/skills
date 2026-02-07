---
name: "agent-capability-matrix"
description: "Map task types to the best agent, skill, model, and fallback. Route any task to the right tool. Use when: which agent, route task, agent for this, best agent, capability matrix."
---

<objective>
Provide a comprehensive mapping from task types to the optimal agent, skill, model tier, and fallback strategy. Eliminates guesswork when choosing which agent to use for a given task.
</objective>

<quick_start>
**Find the right agent:**
1. Identify your task type (debug, review, build, explore, etc.)
2. Look up the primary agent in the matrix below
3. If primary fails, use the fallback
4. Match model tier to task complexity
</quick_start>

<triggers>
- "which agent", "route task", "agent for this", "best agent"
- "capability matrix", "agent selection", "what tool should I use"
- "task routing", "agent routing"
</triggers>

---

## Core Capability Matrix

### Development Tasks

| Task Type | Primary Agent | Fallback | Model | Notes |
|-----------|--------------|----------|-------|-------|
| Debug complex issue | debug-like-expert skill | general-purpose | sonnet | Hypothesis-driven |
| Quick bug fix | general-purpose | — | sonnet | Simple fixes |
| Code review | code-reviewer | feature-dev:code-reviewer | haiku | Pattern matching |
| Architecture design | Plan agent | code-architect | opus | Complex reasoning |
| Feature implementation | general-purpose | feature-dev agents | sonnet | Code generation |
| Refactoring | code-simplifier | general-purpose | sonnet | Preserve behavior |
| Security audit | security skill | general-purpose | sonnet | OWASP patterns |
| Write tests | testing skill | general-purpose | sonnet | TDD workflow |
| API design | api-design skill | general-purpose | sonnet | REST/GraphQL |
| API testing | api-testing skill | general-purpose | haiku | Postman/Bruno |

### Exploration & Research

| Task Type | Primary Agent | Fallback | Model | Notes |
|-----------|--------------|----------|-------|-------|
| Find files by pattern | Glob tool (direct) | Explore agent | — | Fastest |
| Search code content | Grep tool (direct) | Explore agent | — | Fastest |
| Understand codebase area | Explore agent | general-purpose | haiku | Thorough search |
| Deep code analysis | code-explorer | Explore agent | sonnet | Traces execution |
| Research framework/tool | research skill | WebSearch | sonnet | Structured eval |
| Market research | research skill | WebSearch | sonnet | Company profiles |

### Infrastructure & Deployment

| Task Type | Primary Agent | Fallback | Model | Notes |
|-----------|--------------|----------|-------|-------|
| Docker setup | docker-compose skill | general-purpose | sonnet | Local dev |
| GPU deployment | runpod-deployment skill | general-purpose | sonnet | RunPod |
| Database migration | supabase-sql skill | general-purpose | sonnet | Supabase |
| Stripe integration | stripe-stack skill | general-purpose | sonnet | Payments |
| Voice AI pipeline | voice-ai skill | general-purpose | sonnet | Deepgram+Cartesia |
| LangGraph agents | langgraph-agents skill | general-purpose | sonnet | Multi-agent |
| Fast inference | groq-inference skill | general-purpose | sonnet | GROQ API |
| Chinese LLMs | openrouter skill | general-purpose | sonnet | DeepSeek/Qwen |
| LLM fine-tuning | unsloth-training skill | general-purpose | sonnet | GRPO/SFT |

### Business & GTM

| Task Type | Primary Agent | Fallback | Model | Notes |
|-----------|--------------|----------|-------|-------|
| GTM strategy | gtm-pricing skill | general-purpose | sonnet | ICP, positioning |
| Sales outreach | sales-revenue skill | general-purpose | sonnet | Cold email |
| CRM integration | crm-integration skill | general-purpose | sonnet | Close/HubSpot |
| Content marketing | content-marketing skill | general-purpose | sonnet | B2B content |
| Data analysis | data-analysis skill | general-purpose | sonnet | Dashboards |
| Trading signals | trading-signals skill | general-purpose | sonnet | Technical analysis |
| Business model | business-model-canvas skill | general-purpose | sonnet | 9-block canvas |
| Market differentiation | blue-ocean-strategy skill | general-purpose | sonnet | ERRC framework |

### Workflow & Coordination

| Task Type | Primary Agent | Fallback | Model | Notes |
|-----------|--------------|----------|-------|-------|
| Session start/end | workflow-orchestrator skill | — | sonnet | Daily lifecycle |
| Parallel worktree dev | agent-teams skill | worktree-manager skill | sonnet | Full isolation |
| In-session parallel | subagent-teams skill | sequential execution | haiku-sonnet | Task tool |
| Git workflow | git-workflow skill | general-purpose | haiku | Commits, PRs |
| Skill authoring | extension-authoring skill | general-purpose | sonnet | Skills, hooks |
| Project planning | planning-prompts skill | Plan agent | sonnet | Meta-prompts |
| Cost tracking | cost-metering skill | manual tracking | haiku | Budget status |

---

## Decision Flowchart

```
START: What do I need to do?
│
├── Search/Find something?
│   ├── Know the file pattern? → Glob (direct)
│   ├── Know the code pattern? → Grep (direct)
│   └── Need to understand area? → Explore agent (haiku)
│
├── Write/Change code?
│   ├── Simple fix? → general-purpose (sonnet)
│   ├── New feature? → Check if a skill matches → skill or general-purpose (sonnet)
│   ├── Architecture? → Plan agent (opus)
│   └── Parallel build? → subagent-teams or agent-teams
│
├── Review/Validate?
│   ├── Code review? → code-reviewer (haiku)
│   ├── Security? → security skill (sonnet)
│   └── Tests? → testing skill (sonnet)
│
├── Research/Learn?
│   ├── Codebase? → Explore agent (haiku)
│   ├── Framework? → research skill (sonnet)
│   └── Market? → research skill (sonnet)
│
└── Business/GTM?
    └── Check Business section of matrix above
```

---

## Model Tier Guide

| Tier | Model | Cost/1M In | Best For |
|------|-------|-----------|----------|
| **Fast** | Haiku | $0.25 | Search, classify, review, simple tasks |
| **Standard** | Sonnet | $3.00 | Code generation, reasoning, most tasks |
| **Premium** | Opus | $15.00 | Architecture, complex decisions, planning |

**Default to Sonnet** unless:
- Task is search/classify → use Haiku (5x cheaper)
- Task requires deep reasoning → use Opus (5x more capable)

**Deep dive:** See `reference/matrix-table.md`, `reference/selection-flowchart.md`
