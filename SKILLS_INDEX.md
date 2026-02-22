# Skills Index

> Last updated: 2026-02-22
> Total skills: 39 (2 stable, 37 active)
> See [DEPENDENCY_GRAPH.md](./DEPENDENCY_GRAPH.md) for visual skill relationships
> **100% config.json coverage** — All 39 skills have `config.json` with version tracking

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
| Orchestrate parallel Claude Code sessions | [agent-teams](#agent-teams-skill) | Dev Tools |
| Orchestrate in-session Task tool subagents | [subagent-teams](#subagent-teams-skill) | Dev Tools |
| Map task types to best agent/skill | [agent-capability-matrix](#agent-capability-matrix-skill) | Dev Tools |
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
| Create visual Miro boards | [miro](#miro-skill) | Business |
| HubSpot SQL analytics, lead scoring, forecasting | [hubspot-revops](#hubspot-revops-skill) | Business |
| Design business models (9 blocks) | [business-model-canvas](#business-model-canvas-skill) | Strategy |
| Blue ocean market differentiation | [blue-ocean-strategy](#blue-ocean-strategy-skill) | Strategy |
| Track and manage API costs | [cost-metering](#cost-metering-skill) | Core |
| Auto-extract GTME metrics from sessions | [portfolio-artifact](#portfolio-artifact-skill) | Core |
| Track project context across sessions | [project-context](#project-context-skill) | Core |
| Auto-diagnose and repair broken skills | [heal-skill](#heal-skill) | Dev Tools |
| Enterprise SaaS frontend (Tailwind v4, shadcn, Next.js) | [frontend-ui](#frontend-ui-skill) | Dev Tools |
| Enforce workflow discipline | [workflow-enforcer-skill](#workflow-enforcer-skill) | Core |
| Orchestrate full-day workflows with cost tracking | [workflow-orchestrator](#workflow-orchestrator-skill) | Core |

---

## Stable Skills (Battle-Tested)

### workflow-enforcer-skill
**Location:** `stable/workflow-enforcer-skill/`

Enforces workflow discipline across ALL projects. Ensures Claude checks for specialized agents, announces usage, and creates TaskCreate tasks (preferred) or TodoWrite todos for multi-step work.

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
**Location:** `active/workflow-orchestrator-skill/` | **Version:** 2.0.0

Dual-team workflow orchestration with Builder + Observer concurrent teams, cost tracking, model routing, security gates, and devil's advocate pattern.

**Key Features:**
- **Dual-Team Architecture:** Builder team ships fast, Observer team watches for drift/debt/gaps
- **Devil's Advocate:** Adversarial roles on both teams prevent groupthink
- **Contract-First Development:** Define endpoints + scope boundaries before any code
- **Observer BLOCKER Gate:** Phase transitions blocked if active Observer findings
- **5 Workflow Phases:** START DAY → RESEARCH → FEATURE DEVELOPMENT → DEBUG → END DAY
- **Native Agent Teams:** Experimental support for DAG tasks, peer messaging, TeammateIdle hooks
- **Cost Optimization:** Intelligent model routing; Observers use Haiku for routine checks
- **Security Gates:** Automated scanning + Observer findings before commits

**Reference Files (11):**
- `reference/start-day-protocol.md` - Session initialization, context loading
- `reference/research-workflow.md` - Systematic research with cost optimization
- `reference/feature-development.md` - Multi-phase development with quality gates
- `reference/debug-methodology.md` - Evidence-based debugging
- `reference/end-day-protocol.md` - Security sweeps, context preservation
- `reference/cost-tracking.md` - Model pricing, budget management
- `reference/agent-routing.md` - Complete 70+ agent catalog
- `reference/rollback-recovery.md` - Rollback strategies and recovery
- `reference/dual-team-architecture.md` - Full Builder + Observer team spec
- `reference/observer-patterns.md` - 7 drift detection patterns with commands
- `reference/devils-advocate.md` - Adversarial prompt templates and protocol

**Templates (6):**
- `templates/PROJECT_CONTEXT.md` - Dynamic context generation
- `templates/RESEARCH.md` - Research documentation format
- `templates/daily-cost.json` - Cost tracking data structure
- `templates/worktree-registry.json` - Worktree management registry
- `templates/OBSERVER_QUALITY.md` - Code Quality Observer report template
- `templates/OBSERVER_ARCH.md` - Architecture Observer report template

**Triggers:** "start day", "end day", "orchestrate workflow", "track costs", "route agent", "dual team", "observer team", "builder team", "spawn observers", "devil's advocate"

---

#### cost-metering-skill
**Location:** `active/cost-metering-skill/` | **Version:** 1.1.0

Track and manage Claude API costs across sessions with budget alerts and optimization strategies.

**Key Features:**
- Model rate cards (Opus/Sonnet/Haiku per 1M tokens)
- Daily/monthly budget tracking with alert thresholds (50%/80%/95%)
- Cost optimization: model routing, context management, task batching
- Integration with workflow-orchestrator cost gate
- Zero-cost tools: TaskCreate/TaskUpdate, TeamCreate/SendMessage (local UI, not API calls)

**Reference Files (2):**
- `reference/cost-tracking-guide.md` - Data formats, tracking methods, reporting queries
- `reference/budget-templates.md` - Budget tiers (Hobby/Pro/Enterprise), monthly calculator

**Triggers:** "cost check", "budget status", "how much spent", "optimize costs"

---

#### portfolio-artifact-skill
**Location:** `active/portfolio-artifact-skill/`

Auto-extract engineering metrics from work sessions for portfolio reporting.

**Key Features:**
- Per-session metrics: lines shipped, bugs fixed, PRs merged, cost per feature
- 3 report templates: executive summary, weekly digest, sprint report
- Auto-capture from git log, diff stats, test results
- Storage at `~/.claude/portfolio/YYYY-MM-DD.json`

**Reference Files (2):**
- `reference/metrics-guide.md` - What to capture, how to measure impact
- `reference/report-templates.md` - Executive summary, weekly digest, sprint report templates

**Triggers:** "capture metrics", "portfolio report", "what did I ship", "weekly summary"

---

### Dev Tools

#### extension-authoring-skill
**Location:** `active/extension-authoring-skill/` | **Version:** 1.1.0

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
**Location:** `active/worktree-manager-skill/` | **Version:** 1.1.0

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

#### agent-teams-skill
**Location:** `active/agent-teams-skill/` | **Version:** 1.1.0

Orchestrate teams of 2-3 parallel Claude Code sessions working on the same codebase. Handles task decomposition, agent coordination via WORKTREE_TASK.md, context isolation, and merge strategies. Includes Native Teams API alternative (TeamCreate + SendMessage) for lightweight coordination.

**Depends on:** worktree-manager-skill (infrastructure layer)

**Team Patterns:**
| Pattern | Agents | Execution |
|---------|--------|-----------|
| Feature Parallel | 2-3 | Parallel |
| Frontend/Backend | 2 | Parallel |
| Test/Implement | 2 | Sequential |
| Review/Refactor | 2 | Sequential |

**Reference Files (3):**
- `reference/context-engineering.md` - Context isolation, delegation patterns
- `reference/worktree-integration.md` - Port allocation, terminal strategies
- `reference/prompt-templates.md` - Spawn prompts for 4 team patterns

**Triggers:** "set up agent team", "parallel development", "coordinate Claude sessions", "team of agents", "spawn agents", "agent coordination"

---

#### subagent-teams-skill
**Location:** `active/subagent-teams-skill/`

Orchestrate in-session Task tool subagents for parallel work without terminal overhead. Documents TaskCreate/TaskUpdate for native progress rendering, TeamCreate + SendMessage for team coordination, and complete Task tool parameter reference.

**Depends on:** extension-authoring-skill, agent-teams-skill

**Team Patterns:**
| Pattern | Agents | Use Case |
|---------|--------|----------|
| Research Team | 3 Explore | Broad codebase investigation |
| Implement Team | architect → builders → reviewer | Multi-component features |
| Review Team | 3 reviewers | Parallel code review |
| Explore Team | 3 search strategies | Find unknown code locations |
| Doc Team | N updaters | Independent file updates |

**Reference Files (3):**
- `reference/task-tool-guide.md` - Subagent types, parameters, parallel execution
- `reference/team-patterns.md` - 5 reusable team compositions with cost estimates
- `reference/prompt-templates.md` - Spawn prompts per pattern

**Triggers:** "subagent team", "Task tool team", "in-session parallel", "fan-out subagents"

---

#### agent-capability-matrix-skill
**Location:** `active/agent-capability-matrix-skill/`

Map task types to best agent, skill, fallback, and model tier. 70+ agents cataloged.

**Key Features:**
- Full task→agent mapping across 5 categories (includes progress tracking + team coordination)
- Decision flowchart for agent selection
- Model tier guide (Haiku→search, Sonnet→code, Opus→architecture, TaskCreate→free)
- Cost impact per strategy

**Reference Files (2):**
- `reference/matrix-table.md` - Complete agent listing (built-in, plugin, custom skills)
- `reference/selection-flowchart.md` - Decision tree + cost impact table

**Triggers:** "which agent", "route task", "agent for this", "capability matrix"

---

#### heal-skill
**Location:** `active/heal-skill/`

Auto-diagnose and repair broken skills. Validates YAML frontmatter, XML sections, config.json schema, and cross-skill dependencies.

**Key Features:**
- 3-layer diagnostic engine: Structural → Content → Integration
- 16 automated checks with severity levels
- Auto-fix protocol with preview, confirm, apply workflow
- Health scoring per skill and library-wide

**Reference Files (2):**
- `reference/validation-rules.md` - Complete check reference (S1-S10, C1-C6, I1-I5)
- `reference/known-issues.md` - GitHub issue patterns and library audit findings

**Triggers:** "/heal-skill", "fix broken skill", "skill health check", "validate skills"

---

#### frontend-ui-skill
**Location:** `active/frontend-ui-skill/` | **Version:** 1.0.0

Enterprise SaaS frontend patterns with Tailwind CSS v4, shadcn/ui (2026), Next.js 15+ App Router or Vite SPA, and React 19.

**Key Features:**
- Tailwind v4 CSS-first configuration (@theme, @theme inline, OKLCH, container queries)
- shadcn/ui 2026 patterns (data-slot, no forwardRef, tw-animate-css)
- Server/Client Component architecture with boundary optimization
- **Vite SPA support:** React Router v7, TanStack Router, client-only patterns
- Enterprise SaaS UI: dashboards, pricing pages, data tables, role-based UI
- Accessibility (WCAG 2.1 AA): keyboard, focus management, ARIA, contrast
- Forms: React Hook Form + Zod + shadcn Form + Server Actions
- Performance: Core Web Vitals targets, code splitting, image/font optimization

**Integrates with:** testing-skill, api-design-skill, security-skill, stripe-stack-skill

**Reference Files (10):**
- `reference/tailwind-v4-setup.md` - Complete v4 setup, migration from v3
- `reference/shadcn-setup.md` - shadcn + Tailwind v4 configuration
- `reference/component-patterns.md` - Compound, cva, polymorphic, data-slot
- `reference/saas-dashboard.md` - Dashboard layouts, KPI cards, charts, RBAC
- `reference/saas-pricing-checkout.md` - Pricing pages, Stripe UI, conversion
- `reference/accessibility-checklist.md` - WCAG 2.1 AA per-component patterns
- `reference/form-patterns.md` - Multi-step, file upload, optimistic updates
- `reference/performance-optimization.md` - Core Web Vitals, Lighthouse CI
- `reference/vite-react-setup.md` - Vite + React 19 SPA project setup
- `reference/spa-routing.md` - React Router v7, TanStack Router, migration table

**Templates (7):**
- `templates/nextjs-tailwind-v4-setup.css` - Complete globals.css with design tokens
- `templates/component-with-variants.tsx` - cva + data-slot + React 19 props
- `templates/dashboard-layout.tsx` - Sidebar + header + responsive layout
- `templates/form-with-server-action.tsx` - RHF + Zod + Server Action
- `templates/pricing-page.tsx` - 3-tier pricing with toggle and comparison
- `templates/vite-react-config.ts` - Vite config with Tailwind v4, aliases, chunks
- `templates/spa-app-layout.tsx` - SPA layout with React Router + code splitting

**Triggers:** "React component", "Next.js page", "frontend UI", "Tailwind", "shadcn", "accessibility", "a11y", "responsive design", "form validation", "server component", "client component", "design system", "dark mode", "SaaS UI", "dashboard", "pricing page", "enterprise UI", "data table", "landing page", "Vite", "React Router", "SPA", "single page app"

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

#### miro-skill
**Location:** `active/miro-skill/`

Visual collaboration boards for strategy, architecture, and sprint planning via Miro MCP + AI plugin.

**Setup:** `claude mcp add --transport http miro https://mcp.miro.com` → `/mcp auth`

**Workflows:**
| Workflow | Use Case |
|----------|----------|
| Strategy Board → Tech Spec | GTM planning, product strategy |
| Architecture → Code Scaffold | System design, data flow |
| Sprint Board → Tasks | Sprint planning, capacity tracking |
| Competitive Analysis → GTM Playbook | Market positioning |

**Reference Files (4):**
- `reference/setup-guide.md` - MCP + plugin installation
- `reference/board-workflows.md` - Strategy → execution workflows
- `reference/mcp-tools-reference.md` - All Miro MCP tools with examples
- `reference/prompt-templates.md` - GTM board prompts

**Triggers:** "miro board", "visual diagram", "strategy canvas", "whiteboard"

---

#### hubspot-revops-skill
**Location:** `active/hubspot-revops-skill/`

Revenue analytics infrastructure on HubSpot API + SQL data warehouse. Bridges CRM data → analytics → intelligence products.

**Key Features:**
- SQL warehouse query templates (ICP, pipeline velocity, competitive, forecast)
- ML lead scoring with GradientBoostingClassifier
- Clay MCP → HubSpot enrichment writeback
- Competitive intelligence extraction and alerting

**Depends on:** crm-integration-skill (base CRUD patterns)

**Use Cases:**

| # | Use Case | Output |
|---|----------|--------|
| 1 | ICP Validation | Segment conversion rates |
| 2 | Lead Scoring | Win probability per lead (ML) |
| 3 | Competitive Intel | Win/loss matrix by competitor |
| 4 | Activity Analysis | Activity→outcome correlation |
| 5 | Pipeline Forecast | Weighted revenue forecast |

**Reference Files (4):**
- `reference/api-guide.md` - HubSpot API auth, SDK, CRUD, batch operations
- `reference/sql-analytics.md` - SQL templates for 5 use cases + dialect notes
- `reference/enrichment-pipelines.md` - Clay writeback, ML scoring, automation
- `reference/architecture.md` - System diagram, deployment options, cost tiers

**Triggers:** "hubspot analytics", "revops dashboard", "lead scoring", "pipeline forecast", "ICP analysis", "hubspot SQL"

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
├── active/                    # 37 active skills
│   ├── agent-capability-matrix-skill/
│   ├── agent-teams-skill/
│   ├── api-design-skill/
│   ├── api-testing-skill/
│   ├── blue-ocean-strategy-skill/
│   ├── business-model-canvas-skill/
│   ├── content-marketing-skill/
│   ├── cost-metering-skill/
│   ├── crm-integration-skill/
│   ├── data-analysis-skill/
│   ├── debug-like-expert-skill/
│   ├── docker-compose-skill/
│   ├── extension-authoring-skill/
│   ├── frontend-ui-skill/
│   ├── git-workflow-skill/
│   ├── groq-inference-skill/
│   ├── heal-skill/
│   ├── gtm-pricing-skill/
│   ├── hubspot-revops-skill/
│   ├── langgraph-agents-skill/
│   ├── miro-skill/
│   ├── openrouter-skill/
│   ├── planning-prompts-skill/
│   ├── portfolio-artifact-skill/
│   ├── research-skill/
│   ├── runpod-deployment-skill/
│   ├── sales-revenue-skill/
│   ├── security-skill/
│   ├── stripe-stack-skill/
│   ├── subagent-teams-skill/
│   ├── supabase-sql-skill/
│   ├── testing-skill/
│   ├── trading-signals-skill/
│   ├── unsloth-training-skill/
│   ├── voice-ai-skill/
│   ├── workflow-orchestrator-skill/
│   └── worktree-manager-skill/
├── stable/                    # 2 stable skills
│   ├── project-context-skill/
│   └── workflow-enforcer-skill/
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

# Run integration tests (8 checks per skill)
./scripts/test-skills.sh [--verbose] [--skill <name>]

# View skill usage analytics (last 7 days)
./scripts/skill-analytics-report.sh [--days N] [--all]
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
