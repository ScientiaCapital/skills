# Skills Index

> Last updated: 2026-02-05
> Total skills: 30 (2 stable, 28 active)

## Architecture

**Progressive Disclosure** - Skills load in layers to minimize token usage:
- **Level 1:** YAML frontmatter (loads at startup for activation)
- **Level 2:** SKILL.md content (loads when skill activates)
- **Level 3:** reference/*.md files (loads only when needed)

---

## Quick Lookup

| Need to... | Use Skill | Category |
|------------|-----------|----------|
| Author skills, hooks, commands, subagents | [extension-authoring](#extension-authoring-skill) | Dev Tools |
| Systematic expert debugging | [debug-like-expert](#debug-like-expert-skill) | Dev Tools |
| Create project plans, meta-prompts | [planning-prompts](#planning-prompts-skill) | Dev Tools |
| Manage git worktrees for parallel dev | [worktree-manager](#worktree-manager-skill) | Dev Tools |
| Conventional commits, PR templates | [git-workflow](#git-workflow-skill) | Dev Tools |
| Write tests, TDD, test coverage | [testing](#testing-skill) | Dev Tools |
| Design REST/GraphQL APIs | [api-design](#api-design-skill) | Dev Tools |
| Auth, secrets, OWASP, security audit | [security](#security-skill) | Dev Tools |
| Test APIs with Postman/Bruno | [api-testing](#api-testing-skill) | Dev Tools |
| Local dev with Docker Compose | [docker-compose](#docker-compose-skill) | Dev Tools |
| Fine-tune LLMs with GRPO/SFT | [unsloth-training](#unsloth-training-skill) | Infrastructure |
| Build multi-agent LangGraph systems | [langgraph-agents](#langgraph-agents-skill) | Infrastructure |
| Deploy to RunPod GPU serverless | [runpod-deployment](#runpod-deployment-skill) | Infrastructure |
| Fast GROQ API inference | [groq-inference](#groq-inference-skill) | Infrastructure |
| Route to Chinese LLMs via OpenRouter | [openrouter](#openrouter-skill) | Infrastructure |
| Build voice AI agents | [voice-ai](#voice-ai-skill) | Infrastructure |
| Clean Supabase SQL migrations | [supabase-sql](#supabase-sql-skill) | Infrastructure |
| Stripe payments + webhooks | [stripe-stack](#stripe-stack-skill) | Infrastructure |
| CRM integration (Close, HubSpot, Salesforce) | [crm-integration](#crm-integration-skill) | Business |
| GTM strategy, pricing, opportunity eval | [gtm-pricing](#gtm-pricing-skill) | Business |
| Market + technical research | [research](#research-skill) | Business |
| Sales outreach, discovery, RevOps | [sales-revenue](#sales-revenue-skill) | Business |
| B2B content marketing | [content-marketing](#content-marketing-skill) | Business |
| Executive data analysis, dashboards | [data-analysis](#data-analysis-skill) | Business |
| Trading signals, technical analysis | [trading-signals](#trading-signals-skill) | Business |
| Design business models (9 blocks) | [business-model-canvas](#business-model-canvas-skill) | Strategy |
| Blue ocean market differentiation | [blue-ocean-strategy](#blue-ocean-strategy-skill) | Strategy |
| Track project context across sessions | [project-context](#project-context-skill) | Core |
| Enforce workflow discipline | [workflow-enforcer](#workflow-enforcer) | Core |
| Orchestrate full-day workflows with cost tracking | [workflow-orchestrator](#workflow-orchestrator-skill) | Core |

---

## Stable Skills (Battle-Tested)

### workflow-enforcer
**Location:** `stable/workflow-enforcer/`

Enforces workflow discipline across ALL projects. Ensures Claude checks for specialized agents, announces usage, and creates TodoWrite todos.

**Triggers:** Automatic on all sessions

---

### project-context-skill
**Location:** `stable/project-context-skill/`

Maintains project context and progress tracking across Claude sessions.

**Triggers:** "load project context", "save context", "end session"

---

## Active Skills by Category

### Core

#### workflow-orchestrator-skill
**Location:** `active/workflow-orchestrator-skill/`

Comprehensive workflow orchestration for full-day Claude sessions with cost tracking, model routing, and team coordination.

**Key Features:**
- **5 Workflow Phases:** START DAY → RESEARCH → FEATURE DEVELOPMENT → DEBUG → END DAY
- **Cost Optimization:** Intelligent model routing (Claude/DeepSeek/GROQ/Ollama) based on budget
- **Parallel Execution:** Git worktree management with isolated environments
- **70+ Agent Catalog:** Smart routing to specialized agents based on task type
- **Security Gates:** Automated security scanning before commits

**Reference Files (8):**
- `reference/start-day-protocol.md` - Session initialization, context loading
- `reference/research-workflow.md` - Systematic research with cost optimization  
- `reference/feature-development.md` - Multi-phase development with quality gates
- `reference/debug-methodology.md` - Evidence-based debugging
- `reference/end-day-protocol.md` - Security sweeps, context preservation
- `reference/cost-tracking.md` - Model pricing, budget management
- `reference/agent-routing.md` - Complete 70+ agent catalog
- `reference/rollback-recovery.md` - Rollback strategies and recovery

**Templates (4):**
- `templates/PROJECT_CONTEXT.md` - Dynamic context generation
- `templates/RESEARCH.md` - Research documentation format
- `templates/daily-cost.json` - Cost tracking data structure
- `templates/worktree-registry.json` - Worktree management registry

**Triggers:** "start day", "end day", "orchestrate workflow", "track costs", "route agent"

---

### Dev Tools

#### extension-authoring-skill
**Location:** `active/extension-authoring-skill/`

Comprehensive guide for authoring Claude Code extensions: skills, hooks, slash commands, and subagents.

**Reference Files:**
- `reference/skills.md` - SKILL.md authoring patterns
- `reference/hooks.md` - Event-driven automation
- `reference/commands.md` - Slash command YAML configs
- `reference/subagents.md` - Specialized agent creation

**Triggers:** "create skill", "create hook", "slash command", "subagent"

---

#### debug-like-expert-skill
**Location:** `active/debug-like-expert-skill/`

Systematic debugging with evidence gathering and hypothesis testing.

**Methodology:** Observe -> Hypothesize -> Test -> Verify

**Triggers:** "debug systematically", "root cause analysis", "expert debugging"

---

#### planning-prompts-skill
**Location:** `active/planning-prompts-skill/`

Hierarchical project planning and meta-prompt creation for Claude-to-Claude workflows.

**Reference Files:**
- `reference/plans.md` - Project planning patterns
- `reference/meta-prompts.md` - Prompt chaining techniques

**Triggers:** "create plan", "meta-prompt", "project planning", "prompt chaining"

---

#### worktree-manager-skill
**Location:** `active/worktree-manager-skill/`

Git worktree automation for parallel development with Claude agents.

**Features:** Ghostty terminal, 3 concurrent worktrees, M1/8GB optimized

**Triggers:** "create worktree", "parallel development", "cleanup worktrees"

---

#### git-workflow-skill
**Location:** `active/git-workflow-skill/`

Git workflow conventions: conventional commits, semantic branch naming, PR templates, and merge strategies.

**Key Patterns:**
- Conventional commits (feat/fix/docs/etc.)
- Branch naming: `<type>/<ticket>-<description>`
- PR templates with checklist
- Squash merge for features, merge commit for releases

**Reference Files:**
- `reference/commit-examples.md` - Detailed commit message examples

**Triggers:** "commit", "PR", "branch naming", "git workflow", "conventional commits"

---

#### testing-skill
**Location:** `active/testing-skill/`

Comprehensive testing skill covering TDD workflow, test pyramid, mocking patterns, and coverage strategies.

**Reference Files (4):**
- `reference/unit-testing.md` - Unit test patterns, mocking, fixtures
- `reference/integration-testing.md` - API tests, database tests, E2E
- `reference/test-organization.md` - File structure, naming conventions
- `reference/coverage-strategies.md` - Coverage targets, what to test

**Key Concepts:**
- TDD: Red-Green-Refactor cycle
- Test Pyramid: Unit (70%) → Integration (20%) → E2E (10%)
- Mock external services, not your own code

**Triggers:** "write tests", "TDD", "test coverage", "unit test", "integration test", "mocking"

---

#### api-design-skill
**Location:** `active/api-design-skill/`

REST and GraphQL API design patterns for consistent, maintainable APIs.

**Reference Files (5):**
- `reference/rest-patterns.md` - Resource design, CRUD operations
- `reference/error-handling.md` - Error response format, status codes
- `reference/pagination.md` - Cursor vs offset, implementation
- `reference/versioning.md` - URL versioning, deprecation strategy
- `reference/documentation.md` - OpenAPI spec, README patterns

**Key Patterns:**
- RESTful naming conventions (plural nouns, kebab-case)
- Consistent error response format with request ID
- Cursor-based pagination for real-time data
- URL path versioning (/api/v1/, /api/v2/)

**Triggers:** "design API", "REST endpoints", "error responses", "pagination", "API versioning"

---

#### security-skill
**Location:** `active/security-skill/`

Application security patterns for web applications.

**Reference Files (5):**
- `reference/auth-patterns.md` - JWT, OAuth, session management
- `reference/secrets-management.md` - Environment variables, rotation
- `reference/input-validation.md` - Zod schemas, sanitization
- `reference/rls-policies.md` - Supabase Row Level Security
- `reference/owasp-top-10.md` - Vulnerability checklist

**Key Areas:**
- Authentication: JWT (short-lived) + refresh tokens
- Secrets: Never in code, validate at startup
- Input: Validate with Zod, sanitize HTML with DOMPurify
- SQL: Always use parameterized queries
- XSS: React auto-escapes, use CSP headers

**Triggers:** "auth", "JWT", "secrets", "API keys", "SQL injection", "XSS", "CSRF", "RLS", "security audit"

---

#### api-testing-skill
**Location:** `active/api-testing-skill/`

Tool-based API testing with Postman and Bruno. Covers collections, environments, test assertions, and CI/CD integration.

**Reference Files (5):**
- `reference/postman-patterns.md` - Collections, scripting, monitors
- `reference/bruno-patterns.md` - .bru files, git-native workflow
- `reference/test-design.md` - Coverage strategies, edge cases
- `reference/data-management.md` - Fixtures, dynamic data, cleanup
- `reference/ci-integration.md` - Newman, GitHub Actions, reporting

**Key Patterns:**
- Postman: Cloud sync, mock servers, team collaboration
- Bruno: Git-native .bru files, open source, offline-first
- Test assertions for status, body, schema, headers
- Environment management for local/staging/production

**Triggers:** "postman", "bruno", "API testing", "test API endpoint", "API collection", "endpoint validation"

---

#### docker-compose-skill
**Location:** `active/docker-compose-skill/`

Local development environments using Docker Compose for multi-service setups.

**Reference Files (4):**
- `reference/compose-patterns.md` - Service definitions, health checks, profiles
- `reference/services.md` - Database, cache, queue, search services
- `reference/networking.md` - Ports, networks, volumes
- `reference/dev-workflow.md` - Commands for logs, exec, rebuild

**Quick Services:**
| Service | Image | Port |
|---------|-------|------|
| PostgreSQL | `postgres:16-alpine` | 5432 |
| Redis | `redis:7-alpine` | 6379 |
| MongoDB | `mongo:7` | 27017 |
| MySQL | `mysql:8` | 3306 |

**Triggers:** "docker compose", "local dev", "postgres container", "redis local", "dev environment"

---

### Infrastructure

#### runpod-deployment-skill
**Location:** `active/runpod-deployment-skill/`

Expert-level RunPod deployment patterns for GPU serverless workloads.

**Reference Files (7):**
- `reference/serverless-workers.md` - Handler patterns, streaming
- `reference/pod-management.md` - Pod lifecycle, SSH, volumes
- `reference/cost-optimization.md` - GPU selection, spot instances
- `reference/monitoring.md` - Health checks, logging
- `reference/model-deployment.md` - LLM, embedding, vision patterns
- `reference/templates.md` - Dockerfiles, CI/CD
- `templates/runpod-worker.py` - Production handler template

**M1 Mac Note:** Uses GitHub Actions for x86 builds

**Triggers:** "deploy to RunPod", "GPU serverless", "vLLM endpoint", "scale to zero"

---

#### voice-ai-skill
**Location:** `active/voice-ai-skill/`

Production voice AI agents with ultra-low latency (<500ms). VozLux-tested.

| Component | Provider | Latency |
|-----------|----------|---------|
| STT | Deepgram Nova-3 | ~150ms |
| LLM | GROQ llama-3.1-8b | ~220ms |
| TTS | Cartesia Sonic-2 | ~90ms |
| Telephony | Twilio Media Streams | Realtime |

**Reference Files (6):** deepgram-setup, cartesia-tts, groq-voice-llm, twilio-webhooks, latency-optimization, voice-prompts

**Triggers:** "voice agent", "Twilio", "Deepgram", "Cartesia", "STT", "TTS"

---

#### groq-inference-skill
**Location:** `active/groq-inference-skill/`

Ultra-fast LLM inference with GROQ API. Chat, vision, audio, tool use.

| Capability | Models |
|------------|--------|
| Chat | llama-3.3-70b-versatile, llama-3.1-8b-instant |
| Vision | llama-4-scout-17b |
| STT | whisper-large-v3 |
| TTS | playai-tts |
| Tool Use | compound-beta |

**Triggers:** "groq", "fast inference", "whisper", "compound beta"

---

#### openrouter-skill
**Location:** `active/openrouter-skill/`

Orchestrate Chinese LLMs (DeepSeek, Qwen, Yi, Moonshot) through OpenRouter's unified API with LangChain/LangGraph integration.

| Model | Best For | Cost ($/1M) |
|-------|----------|-------------|
| deepseek-chat | General reasoning | $0.27/$1.10 |
| deepseek-coder | Code generation | $0.14/$0.28 |
| qwen-2-vl-72b | Vision, charts | $0.40/$0.40 |
| qwen-2.5-7b | Fast, cheap tasks | $0.09/$0.09 |
| qwq-32b | Deep reasoning | $0.15/$0.40 |

**Reference Files (7):**
- `reference/models-catalog.md` - Complete model listing with capabilities
- `reference/routing-strategies.md` - Auto, provider, and custom routing
- `reference/langchain-integration.md` - LangChain/LangGraph patterns
- `reference/cost-optimization.md` - Budget management and caching
- `reference/tool-calling.md` - Function calling patterns
- `reference/multimodal.md` - Vision, PDF, audio support
- `reference/observability.md` - Monitoring and tracing

**Triggers:** "openrouter", "chinese llm", "deepseek", "qwen", "moonshot", "model routing", "auto router"

---

#### langgraph-agents-skill
**Location:** `active/langgraph-agents-skill/`

Multi-agent systems with LangGraph. NO OPENAI.

| Pattern | Use When |
|---------|----------|
| Supervisor | Centralized routing |
| Swarm | Peer-to-peer handoffs |
| Master Orchestrator | Complex workflows |
| Functional API | Simpler decorator-based workflows |
| Deep Agents | Production framework with backends |
| HITL/Interrupts | Human approval gates |
| MCP Integration | Standardized tool protocols |

**Reference Files (10):** state-schemas, orchestration-patterns, context-engineering, cost-optimization, base-agent-architecture, tools-organization, functional-api, deep-agents, mcp-integration, streaming-patterns

**Triggers:** "LangGraph agent", "multi-agent", "supervisor pattern", "functional API", "deep agents", "MCP tools", "human in the loop"

---

#### unsloth-training-skill
**Location:** `active/unsloth-training-skill/`

Fine-tune LLMs with Unsloth using GRPO (reinforcement learning) or SFT (supervised fine-tuning).

| Method | Use When | Data Needed |
|--------|----------|-------------|
| GRPO | Improving reasoning, aligning behavior | Prompts + verifiable answers |
| SFT | Teaching formats, domain knowledge | Input/output pairs |

**Reference Files (4):**
- `references/reward-design.md` - Reward function patterns and testing
- `references/domain-examples.md` - Voice AI, Sales Agent, Support examples
- `references/hyperparameters.md` - GRPOConfig complete reference
- `references/troubleshooting.md` - Common issues and fixes

**Reference Code:**
- `reference/grpo/basic_grpo.py` - Minimal working GRPO example
- `reference/sft/sales_extractor_training.py` - Complete SFT script

**Triggers:** "train with GRPO", "fine-tune model", "create reward functions", "SFT training", "Unsloth", "export to GGUF"

---

#### supabase-sql-skill
**Location:** `active/supabase-sql-skill/`

Clean SQL migrations for Supabase: typo fixes, idempotency, RLS patterns.

**Triggers:** "fix SQL", "clean migration", "RLS policy"

---

#### stripe-stack-skill
**Location:** `active/stripe-stack-skill/`

Production Stripe integration for Next.js + Supabase. Extracted from NetZero Suite (netzero-bot, solarappraisal-ai, fieldvault-ai, solarvoice-ai).

**Key Patterns:**
- Database-backed webhook idempotency (NOT in-memory)
- Lazy Stripe client initialization
- Environment variable price IDs (test→live switching)

**Reference Files (4):**
- `references/webhook-patterns.md` - Idempotency, event handling
- `references/pricing-models.md` - Plans vs Credits vs Usage-based
- `references/environment-vars.md` - Standard conventions
- `references/common-errors.md` - Troubleshooting guide

**Workflows (5):**
- `workflows/setup-new-project.md` - Fresh Stripe integration
- `workflows/add-webhook-handler.md` - Add to existing project
- `workflows/implement-subscriptions.md` - Subscription billing
- `workflows/add-credit-system.md` - Pay-as-you-go credits
- `workflows/go-live-checklist.md` - Test → Production

**Templates (6):**
- `templates/webhook-handler-nextjs.ts` - Complete webhook handler
- `templates/stripe-client.ts` - Lazy client factory
- `templates/plans-config.ts` - Type-safe plan definitions
- `templates/idempotency-migration.sql` - Supabase migration
- `templates/webhook-handler.test.ts` - Vitest/Jest tests
- `templates/env-example.txt` - Environment template

**GitHub:** https://github.com/ScientiaCapital/stripe-stack (private)

**Triggers:** "stripe", "payments", "billing", "subscription", "webhook", "checkout"

---

### Business

#### crm-integration-skill
**Location:** `active/crm-integration-skill/`

Unified CRM integration patterns for Close CRM, HubSpot, and Salesforce.

| CRM | Auth | Best For |
|-----|------|----------|
| Close | API Key | SMB sales, simplicity (daily driver) |
| HubSpot | OAuth 2.0 | Marketing + Sales alignment |
| Salesforce | JWT Bearer | Enterprise, complex workflows |

**Reference Files:**
- `reference/close-deep-dive.md` - Query language, Smart Views, automation

**Triggers:** "Close CRM", "HubSpot", "Salesforce", "CRM API", "lead sync", "deal sync"

---

#### gtm-pricing-skill
**Location:** `active/gtm-pricing-skill/`

Comprehensive GTM strategy, pricing models, and opportunity evaluation.

**Reference Files:**
- `reference/gtm.md` - ICP, positioning, messaging
- `reference/pricing.md` - Models, packaging, psychology
- `reference/opportunity.md` - Deal evaluation, unit economics

**Triggers:** "GTM strategy", "pricing", "ICP", "evaluate opportunity"

---

#### research-skill
**Location:** `active/research-skill/`

Market and technical research framework.

**Reference Files:**
- `reference/market.md` - Company profiles, competitive intel
- `reference/technical.md` - Framework evaluation, API assessment

**Triggers:** "research company", "competitive analysis", "evaluate framework"

---

#### sales-revenue-skill
**Location:** `active/sales-revenue-skill/`

B2B sales: outreach, discovery, and revenue operations.

**Reference Files:**
- `reference/outreach.md` - Cold email, lead scoring
- `reference/discovery.md` - SPIN, MEDDIC, demo flow
- `reference/revenue-ops.md` - Pipeline, CAC, LTV, forecasting

**Triggers:** "cold email", "discovery call", "pipeline analysis", "MEDDIC"

---

#### content-marketing-skill
**Location:** `active/content-marketing-skill/`

B2B content strategy for demand generation and thought leadership.

**Triggers:** "content strategy", "LinkedIn post", "blog SEO", "case study"

---

#### data-analysis-skill
**Location:** `active/data-analysis-skill/`

Executive-grade data analysis for VC, PE, angels, and founders.

**Reference Files (4):** chart-gallery, saas-metrics, streamlit-patterns, data-wrangling

**Triggers:** "analyze data", "dashboard", "investor presentation", "SaaS metrics"

---

#### trading-signals-skill
**Location:** `active/trading-signals-skill/`

Technical analysis for quantitative trading systems.

| Methodology | Coverage |
|-------------|----------|
| Elliott Wave | Wave rules, targets |
| Turtle Trading | Donchian, ATR sizing |
| Fibonacci | Golden pocket, confluence |
| Wyckoff | Phase detection, VSA |
| Markov Regime | 7-state transitions |

**Reference Files (8):** elliott-wave, turtle-trading, fibonacci, wyckoff, markov-regime, pattern-recognition, swarm-consensus, chinese-llm-stack

**Triggers:** "fibonacci levels", "elliott wave", "wyckoff", "trading signals"

---

### Strategy

#### business-model-canvas-skill
**Location:** `active/business-model-canvas-skill/`

Business model design using Alexander Osterwalder's 9 building blocks framework.

| Block | Focus |
|-------|-------|
| Customer Segments | Who are we serving? |
| Value Propositions | What value do we deliver? |
| Channels | How do we reach customers? |
| Customer Relationships | How do we engage? |
| Revenue Streams | How do we make money? |
| Key Resources | What do we need? |
| Key Activities | What must we do? |
| Key Partnerships | Who helps us? |
| Cost Structure | What does it cost? |

**Key Features:**
- Canvas generation algorithm
- Validation checklist for each block
- Canvas health metrics (viability scoring)
- Example sessions with real scenarios

**Triggers:** "business model canvas", "value proposition", "customer segments", "revenue model", "startup canvas"

---

#### blue-ocean-strategy-skill
**Location:** `active/blue-ocean-strategy-skill/`

Blue Ocean Strategy (Chan Kim & Renée Mauborgne) for creating uncontested market space.

| Framework | Purpose |
|-----------|---------|
| ERRC Grid | Eliminate, Reduce, Raise, Create |
| Strategy Canvas | Value curves vs competitors |
| Six Paths | Alternative market exploration |
| Blue Ocean Index | Opportunity scoring (0-100) |

**Key Concepts:**
- Value Innovation (differentiation + low cost)
- Three tiers of noncustomers
- Red Ocean vs Blue Ocean comparison

**Classic Examples:**
- Cirque du Soleil (eliminated animal shows, created artistic elements)
- Southwest Airlines (eliminated meals, created point-to-point)
- Yellow Tail Wine (eliminated complexity, created easy drinking)

**Triggers:** "blue ocean", "ERRC framework", "strategy canvas", "value innovation", "market differentiation"

---

## Folder Structure

```
skills/
├── active/                    # 28 active skills
│   ├── api-design-skill/
│   ├── api-testing-skill/
│   ├── docker-compose-skill/
│   ├── blue-ocean-strategy-skill/
│   ├── business-model-canvas-skill/
│   ├── content-marketing-skill/
│   ├── crm-integration-skill/
│   ├── data-analysis-skill/
│   ├── debug-like-expert-skill/
│   ├── extension-authoring-skill/
│   ├── git-workflow-skill/
│   ├── groq-inference-skill/
│   ├── gtm-pricing-skill/
│   ├── langgraph-agents-skill/
│   ├── openrouter-skill/
│   ├── planning-prompts-skill/
│   ├── research-skill/
│   ├── runpod-deployment-skill/
│   ├── sales-revenue-skill/
│   ├── security-skill/
│   ├── stripe-stack-skill/
│   ├── supabase-sql-skill/
│   ├── testing-skill/
│   ├── trading-signals-skill/
│   ├── unsloth-training-skill/
│   ├── voice-ai-skill/
│   ├── workflow-orchestrator-skill/
│   └── worktree-manager-skill/
├── stable/                    # 2 stable skills
│   ├── project-context-skill/
│   └── workflow-enforcer/
├── dist/                      # Zips for Claude Desktop
├── scripts/
│   ├── deploy.sh              # Deploy to ~/.claude/skills/
│   └── rebuild-zips.sh        # Rebuild dist/*.zip
├── templates/
│   └── SKILL_TEMPLATE.md
├── CLAUDE.md
├── README.md
└── SKILLS_INDEX.md            # This file
```

---

## Scripts

```bash
# Deploy all skills to ~/.claude/skills/
./scripts/deploy.sh

# Rebuild all zip files in dist/
./scripts/rebuild-zips.sh
```

---

## Consolidation History

On 2025-12-25, 14 skills were consolidated into 5 comprehensive skills:

| New Skill | Merged From |
|-----------|-------------|
| extension-authoring | create-agent-skills, create-hooks, create-slash-commands, create-subagents |
| gtm-pricing | gtm-strategy, pricing-strategy, opportunity-evaluator |
| planning-prompts | create-meta-prompts, create-plans |
| research | market-research, technical-research |
| sales-revenue | sales-outreach, revenue-ops, demo-discovery |

This reduced the library from 31 to 17 skills with no functionality loss.

On 2026-01-01, 4 skills were audited and restructured to XML format (<500 lines each):

| Skill | Before | After | Changes |
|-------|--------|-------|---------|
| runpod-deployment-skill | 1172 lines | 451 lines | Full XML structure, reference files |
| crm-integration-skill | 788 lines | 489 lines | Updated with Context7 SDK patterns |
| voice-ai-skill | 652 lines | 493 lines | Deepgram v5 SDK, Cartesia Sonic-2 |
| gtm-pricing-skill | 510 lines | 496 lines | Trimmed integration notes |
