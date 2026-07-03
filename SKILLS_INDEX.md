# Skills Index

> Last updated: 2026-07-03
> Total skills: 82 (2 stable, 80 active)
> See [DEPENDENCY_GRAPH.md](./DEPENDENCY_GRAPH.md) for visual skill relationships
> **100% config.json coverage** — All 86 skills have `config.json` with version tracking
> **Naming note:** `nooks-autopilot`, `sdr-dial-lists`, `sdr-call-coaching`, and `epiphan-call-playbook` deliberately omit the `-skill` suffix — they are live-automation names (P14 harvest exceptions to the kebab-case `-skill` convention).

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
| Expert trading partner: Options, Stocks, Crypto, Commodities, VIX, Forex | [trading-signals](#trading-signals-skill) | Business |
| IBKR portfolio, trades, multi-account management | [ibkr-api](#ibkr-api-skill) | Business |
| Create visual Miro boards | [miro](#miro-skill) | Business |
| HubSpot SQL analytics, lead scoring, forecasting | [hubspot-revops](#hubspot-revops-skill) | Business |
| Apollo research → outreach → sequence load | [prospect-research-to-cadence](#prospect-research-to-cadence-skill) | Business |
| Always have verified phones for dials | [phone-verification-waterfall](#phone-verification-waterfall-skill) | Business |
| Auto-generate MEDDIC call prep briefs | [meddic-call-prep-auto](#meddic-call-prep-auto-skill) | Business |
| Deal health scoring + next-best-action (scheduled daily) | [deal-momentum-analyzer](#deal-momentum-analyzer-skill) | Business |
| AE handoff brief: MEDDIC + call history + demo flow | [ae-handoff-brief](#ae-handoff-brief-skill) | Business |
| Call transcript analysis: MEDDIC scoring + coaching | [call-recording-analyzer](#call-recording-analyzer-skill) | Business |
| Identify + recover stalled/dead deals, clean pipeline | [dead-deal-recovery](#dead-deal-recovery-skill) | Business |
| Auto-link closed deals to GTME portfolio evidence | [portfolio-deal-linker](#portfolio-deal-linker-skill) | Business |
| Pre-market trading digest — watchlist + IBKR positions | [trading-alert-scheduler](#trading-alert-scheduler-skill) | Business |
| Design business models (9 blocks) | [business-model-canvas](#business-model-canvas-skill) | Strategy |
| Blue ocean market differentiation | [blue-ocean-strategy](#blue-ocean-strategy-skill) | Strategy |
| Jobs To Be Done + ODI analysis | [jobs-to-be-done](#jobs-to-be-done-skill) | Strategy |
| Challenger Sale methodology (Teach-Tailor-Take Control) | [challenger-sale](#challenger-sale-skill) | Strategy |
| FBI negotiation (tactical empathy, calibrated questions) | [never-split-the-difference](#never-split-the-difference-skill) | Strategy |
| Track and manage API costs | [cost-metering](#cost-metering-skill) | Core |
| Auto-extract GTME metrics from sessions | [portfolio-artifact](#portfolio-artifact-skill) | Core |
| Track project context across sessions | [project-context](#project-context-skill) | Core |
| Auto-diagnose and repair broken skills | [heal-skill](#heal-skill) | Dev Tools |
| Enterprise SaaS frontend (Tailwind v4, shadcn, Next.js) | [frontend-ui](#frontend-ui-skill) | Dev Tools |
| Enforce workflow discipline | [workflow-enforcer-skill](#workflow-enforcer-skill) | Core |
| Orchestrate full-day workflows with cost tracking | [workflow-orchestrator](#workflow-orchestrator-skill) | Core |
| Daily callable lead inventory + ATL runway | [callable-lead-count](#callable-lead-count-skill) | BDR Automation |
| Morning briefing: calendar + dials + deals + drafts | [morning-brief](#morning-brief-skill) | BDR Automation |
| Daily phoneless contact enrichment (Apollo + Clay) | [prospect-enrich](#prospect-enrich-skill) | BDR Automation |
| Weekly net-new ICP prospect search | [prospect-refresh](#prospect-refresh-skill) | BDR Automation |
| Auto-load prospects into Apollo sequences | [sequence-load](#sequence-load-skill) | BDR Automation |
| Find internal champions at target accounts | [champion-identifier](#champion-identifier-skill) | Sales Intelligence |
| 7-14 cold email sequences with A/B testing | [cold-email-sequence-generator](#cold-email-sequence-generator-skill) | Sales Intelligence |
| Multi-source contact info extraction | [contact-hunter](#contact-hunter-skill) | Sales Intelligence |
| Professional email templates by scenario | [email-template-generator](#email-template-generator-skill) | Sales Intelligence |
| Score inbound leads by ICP + intent + urgency | [inbound-lead-qualifier](#inbound-lead-qualifier-skill) | Sales Intelligence |
| Monitor buyer intent signals across the web | [intent-signal-aggregator](#intent-signal-aggregator-skill) | Sales Intelligence |
| LinkedIn prospect list building + tracking | [linkedin-sales-navigator-alt](#linkedin-sales-navigator-alt-skill) | Sales Intelligence |
| Find 100+ companies matching best customers | [lookalike-customer-finder](#lookalike-customer-finder-skill) | Sales Intelligence |
| Extract decisions/actions from meeting transcripts | [meeting-intelligence-system](#meeting-intelligence-system-skill) | Sales Intelligence |
| Personalized first lines for 100s of prospects | [personalization-at-scale](#personalization-at-scale-skill) | Sales Intelligence |
| Forecast accuracy + stall prediction for pipeline | [pipeline-health-analyzer](#pipeline-health-analyzer-skill) | Sales Intelligence |
| Implement MEDDIC/BANT/Sandler/Challenger/SPIN | [sales-methodology-implementer](#sales-methodology-implementer-skill) | Sales Intelligence |
| 30+ LinkedIn posts for prospect attraction | [social-selling-content-generator](#social-selling-content-generator-skill) | Sales Intelligence |
| Firm-wide sales pulse: revenue pace + pipeline + coaching | [business-pulse](#business-pulse-skill) | Sales Enablement |
| MEDDIC close plans with 0-100 confidence score | [close-plan-generator](#close-plan-generator-skill) | Sales Enablement |
| Vertical discovery questions from cost-of-inaction calculator | [cost-discovery-coach](#cost-discovery-coach-skill) | Sales Enablement |
| Vertical demo flows + LAER objection handling | [demo-execution-playbook](#demo-execution-playbook-skill) | Sales Enablement |
| Day-one Epiphan AI + CRM/Clari MCP reference | [epiphan-ai-mcp-guide](#epiphan-ai-mcp-guide-skill) | Sales Enablement |
| Find greenfield Pearl/EC20 opportunities | [greenfield-pearl-tracker](#greenfield-pearl-tracker-skill) | Sales Enablement |
| Cold/discovery call playbook: openers, objections, spec bank | [epiphan-call-playbook](#epiphan-call-playbook) | Sales Enablement |
| Post-demo follow-up: recap, debrief, 5-touch momentum plan | [post-demo-automation](#post-demo-automation-skill) | Sales Automation |
| Higher-Ed SDR pod tiered daily dial queue | [he-dial-queue](#he-dial-queue-skill) | BDR Automation |
| Autonomous lead hunt → Nooks sequences → warm replies | [nooks-autopilot](#nooks-autopilot) | BDR Automation |
| Daily ranked dial lists for Edgar + Vasil | [sdr-dial-lists](#sdr-dial-lists) | BDR Automation |
| Weekly SDR call scoring + coaching cards | [sdr-call-coaching](#sdr-call-coaching) | BDR Automation |

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
**Location:** `active/langgraph-agents-skill/` | **Version:** 2.0.0

Multi-agent systems with LangGraph. NO OPENAI.

| Pattern | Use When |
|---------|----------|
| Supervisor | Centralized routing |
| Swarm | Peer-to-peer handoffs |
| Handoff | Sequential pipelines |
| Router | Classify-and-dispatch |
| Skills | Progressive disclosure |
| Master Orchestrator | Complex workflows |
| Functional API | Simpler decorator-based workflows |
| Deep Agents | Production framework with backends |
| HITL/Interrupts | Human approval gates |
| MCP Integration | Standardized tool protocols |
| Guardrails | PII, budget, safety controls |

**Reference Files (14):** state-schemas, orchestration-patterns, context-engineering, cost-optimization, base-agent-architecture, tools-organization, functional-api, deep-agents, mcp-integration, streaming-patterns, guardrails, testing-patterns, observability, deployment-patterns

**Triggers:** "LangGraph agent", "multi-agent", "supervisor pattern", "functional API", "deep agents", "MCP tools", "human in the loop", "guardrails", "durable execution", "time travel", "agent handoff", "swarm", "StateGraph", "checkpointer", "interrupt", "agent testing", "LangSmith", "observability", "LangGraph deploy", "create_react_agent"

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
**Location:** `active/trading-signals-skill/` | **Version:** 2.1.0

Expert trading partner across all major asset classes. Combines 5 TA methodologies, 25+ options strategies, regime detection, sentiment analysis, risk management, daily workflow automation, and backtesting patterns.

| Domain | Coverage |
|--------|----------|
| Options | 25+ strategies, full Greeks (1st+2nd order), IV surface, GEX, flow scanner, Zero DTE, Wheel |
| Stocks/ETFs | Sector rotation, scanner, Kelly allocation, earnings plays |
| Crypto/Bitcoin | On-chain metrics, halving supercycle, Markov 7-state regime, composite operator |
| Commodities | Gold/Silver (COT, real rates), Oil (EIA, OPEC, contango) |
| VIX/Volatility | IV rank, term structure, crisis thresholds, regime integration |
| Forex | Carry trade, rate differentials, COT, central bank policy |
| Risk Management | Position sizing, Greeks gates, drawdown, strategy-aware classification, fail-safe closure |
| Sentiment | Social filtering, multi-model consensus, circuit breaker, noise detection |
| Daily Workflow | Pre-market, market-open, intraday /loop, EOD review via scheduled tasks |
| Backtesting | Walk-forward, Monte Carlo, ensemble, combinatorial alpha discovery |

**Reference Files (18):** elliott-wave, turtle-trading, fibonacci (+ GEX fusion), wyckoff (+ composite operator), markov-regime, pattern-recognition, swarm-consensus, chinese-llm-stack, options-trading (+ flow scanner), options-strategies (+ Zero DTE, Wheel), commodities, vix-volatility, forex, equities, sentiment-signals (+ circuit breaker), risk-management (+ fail-safe), daily-trading-workflow, backtesting-patterns

**Triggers:** "options greeks", "iron condor", "credit spread", "VIX", "gold silver oil", "forex", "bitcoin crypto", "position sizing", "IV rank", "daily prep", "pre-market", "backtest", "zero DTE", "options flow", + all v1.0 triggers

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

#### prospect-research-to-cadence-skill
**Location:** `active/prospect-research-to-cadence-skill/` | **Version:** 1.0.0

End-to-end prospect research pipeline: Apollo enrichment → personalized email + call scripts → draft review → Apollo sequence load. Draft+approve mode ensures Tim reviews before contacts are loaded.

**Key Features:**
- Apollo org enrichment + people search in parallel
- Golden Rules filter (excludes customers, channel, product-usage contacts)
- ICP scoring by vertical (Higher Ed 90, Courts 85, Gov 80, Corp AV 80, etc.)
- 3-touch personalized email sequence generation
- MEDDIC-structured call scripts with discovery hooks
- Draft → Tim approval → Apollo sequence auto-load

**Depends on:** sales-revenue-skill, hubspot-revops-skill, research-skill

**MCP Tools:** Apollo (orgs + people + sequences), Epiphan CRM (HubSpot + identify), Gmail (drafts)

**Reference Files:**
- `reference/email-templates.md` - Vertical-specific email templates (Higher Ed, Courts, Corporate AV)

**Triggers:** "research prospect", "build cadence for", "outreach for", "research-to-cadence", "enrich and sequence"

**Impact:** 90 min/day saved | ~$12K/mo revenue lift

---

#### meddic-call-prep-auto-skill
**Location:** `active/meddic-call-prep-auto-skill/` | **Version:** 1.0.0

Auto-generate MEDDIC-structured call prep scripts by pulling HubSpot deal + contact data, Apollo enrichment, Clari call history, and Google Calendar context. Complete brief in 60 seconds.

**Key Features:**
- Calendar-aware: "prep my next call" reads upcoming meetings automatically
- Clari integration: pulls prior call summaries + objections + commitments
- Attendee-to-MEDDIC role mapping (EB, Champion, User, Coach)
- MEDDIC scorecard with ✅/⚠️/❌ per dimension
- Competitive displacement angle identification
- Demo-specific addon flow (RECAP → AGENDA → SHOW VALUE → SUMMARIZE → NEXT STEPS)
- 3 personalized discovery questions generated from enrichment

**Depends on:** sales-revenue-skill, prospect-research-to-cadence-skill, hubspot-revops-skill

**MCP Tools:** Google Calendar, Epiphan CRM (HubSpot + Clari), Apollo (enrichment)

**Triggers:** "call prep", "prep me for", "demo prep", "discovery prep", "meddic brief", "prep my next call"

**Impact:** 45 min/day saved | eliminates 15-20 min demo prep per call

---

#### deal-momentum-analyzer-skill
**Location:** `active/deal-momentum-analyzer-skill/` | **Version:** 1.0.0

Deal health scoring + next-best-action engine. Scores every open deal on 6 momentum signals (days in stage, activity recency, stakeholder breadth, call momentum, MEDDIC completeness, close date integrity). Runs daily at 7am CST via scheduled task.

**Key Features:**
- 6-signal momentum scoring (0-100) with GREEN/YELLOW/RED classification
- Next-best-action engine: prescribes specific recovery actions per deal
- Auto-drafts re-engagement emails for RED deals via Gmail
- Trend tracking: compares to previous run
- Integrates into SOD/morning brief workflow
- Scheduled daily at 7am CST (weekdays)

**Depends on:** hubspot-revops-skill, sales-revenue-skill, meddic-call-prep-auto-skill, portfolio-artifact-skill

**MCP Tools:** Epiphan CRM (HubSpot deals + Clari calls), Apollo (multi-threading), Gmail (draft emails), Google Calendar (check-in booking)

**Scheduled Task:** `deal-momentum-daily` — runs weekdays at 7:00 AM CST

**Triggers:** "deal health", "deal momentum", "pipeline review", "stalled deals", "morning brief", "SOD"

**Impact:** $18K/mo from recovered pipeline | 5-10% stalled deal recovery rate

---

#### phone-verification-waterfall-skill
**Location:** `active/phone-verification-waterfall-skill/` | **Version:** 1.0.0

Ensures Tim always has 50+ verified-phone leads for daily dials. Uses Apollo → Clay waterfall enrichment, applies Golden Rules filter, outputs ICP-scored callable queue. Scheduled Monday 6:15 AM.

**Key Features:**
- Apollo people_match + enrichment for phone verification
- Clay find-and-enrich + add-contact-data-points for waterfall backup
- Golden Rules filter (excludes customers, channel, product-usage contacts)
- ICP scoring by vertical
- Callable lead queue ranked by propensity and ICP fit
- Scheduled Monday 6:15 AM CST

**Depends on:** prospect-research-to-cadence, hubspot-revops, sales-revenue

**MCP Tools:** Epiphan CRM (hubspot_search_contacts), Apollo (people_match), Clay (find-and-enrich-contacts-at-company, add-contact-data-points)

**Scheduled Task:** `phone-verification-waterfall` — runs Mondays at 6:15 AM CST

**Triggers:** "verify phones", "phone waterfall", "callable leads", "who can I call", "dial list", "enrich phones"

**Impact:** 50+ verified leads per week | eliminates cold-calling dead ends

---

#### portfolio-deal-linker-skill
**Location:** `active/portfolio-deal-linker-skill/` | **Version:** 1.0.0

Auto-attributes closed HubSpot deals to the skills and automations that influenced them. Builds living GTME portfolio evidence for Tim's VP Business Development transition — revenue influenced, time saved, automation coverage, cost per deal.

**Key Features:**
- Detects newly closed deals daily (won + lost)
- Multi-touch attribution: primary (first touch), assist (middle), recovery (stalled → won)
- Aggregates rolling 30-day metrics: revenue influenced, deals recovered, time saved, automation coverage
- Generates monthly GTME Evidence Report with VP BD transition narrative
- Links to prospect-research-to-cadence (origination), meddic-call-prep-auto (influence), deal-momentum-analyzer (recovery)

**Depends on:** portfolio-artifact-skill, deal-momentum-analyzer-skill, prospect-research-to-cadence-skill, meddic-call-prep-auto-skill, hubspot-revops-skill

**MCP Tools:** Epiphan CRM (HubSpot deals + Clari), Apollo (sequence history), Gmail (outreach history)

**Scheduled Task:** `portfolio-deal-linker-daily` — runs weekdays at 7:07 AM CST

**Triggers:** "portfolio update", "deal closed", "gtme evidence", "what did I influence", "career evidence", "transition tracker"

**Impact:** Career-critical for VP BD transition — auto-builds evidence of revenue influenced, operational leverage, and systems thinking

---

#### ibkr-api-skill
**Location:** `active/ibkr-api-skill/` | **Version:** 1.0.0

Interactive Brokers API integration for portfolio management, account queries, and trade execution across multiple account types (Roth IRA, personal brokerage, business).

**Key Features:**
- TWS API via ib_async (recommended) or Client Portal REST API
- Multi-account management (Roth IRA restrictions enforced)
- IBKR MCP Server installed (ArjunDivecha/ibkr-mcp-server)
- 11 MCP tools: get_portfolio, get_account_summary, switch_account, place_order, etc.

**Reference Files (2):** connection-patterns, trading-patterns

**Triggers:** "IBKR", "Interactive Brokers", "IB Gateway", "TWS API", "ib_async", "portfolio positions", "account balances", "place trades"

---

#### trading-alert-scheduler-skill
**Location:** `active/trading-alert-scheduler-skill/` | **Version:** 1.0.0

Daily pre-market trading digest. Scans watchlist tickers for regime changes, technical setups, and options flow anomalies. Checks IBKR positions for risk/expiry/Greeks health. Delivers one prioritized action list — no intraday distractions during 50-call BDR days.

**Key Features:**
- Markov 7-state regime detection on SPY
- 5-methodology confluence scoring per ticker (Elliott Wave, Wyckoff, Fibonacci, Turtle, Markov)
- Only surfaces actionable setups (confluence ≥ 0.4)
- IBKR position health: expiry, delta, margin, concentration alerts
- Editable watchlist via `reference/watchlist.json`
- Scannable in under 3 minutes

**Depends on:** trading-signals-skill, ibkr-api-skill

**Tools:** Web Search (market data, news, options flow), IBKR API (positions, P&L, margin)

**Scheduled Task:** `trading-alert-daily` — runs weekdays at 7:09 AM CST

**Triggers:** "market digest", "trading alerts", "pre-market scan", "watchlist check", "what's setting up", "check my positions"

**Impact:** 30 min/day saved + fewer missed setups from not watching screens

---

### BDR Automation (Daily Pipeline)

#### prospect-enrich-skill
**Location:** `active/prospect-enrich-skill/` | **Version:** 1.1.0

Mon-Fri 6:00 AM — Daily batch enrichment of phoneless HubSpot contacts using Apollo + Clay. DEMO REQUEST tier (hand-raisers) enriched first, then ATL-first priority. Golden Rules + ATL/BTL Classification Gate. AE-owned contact exclusion.

**Key Features:**
- DEMO REQUEST tier: contacts with first_conversion containing demo/pricing keywords — highest priority
- ATL/BTL/GRAY/NEVER classification before enrichment (saves Apollo credits)
- AE owner exclusion (IDs 82625923, 423155215)
- Apollo → Clay waterfall for phone misses
- Branded HTML report with Epiphan colors

**Depends on:** hubspot-revops-skill
**Feeds into:** phone-verification-waterfall-skill, prospect-refresh-skill

**Scheduled Task:** `prospect-enrich` — Mon-Fri 6:00 AM ET

**Triggers:** "run prospect enrich", "enrich phoneless contacts"

---

#### prospect-refresh-skill
**Location:** `active/prospect-refresh-skill/` | **Version:** 1.0.0

Monday 6:30 AM — Weekly net-new prospect search across all 7 ICP verticals using Apollo People API. Deduplicates against HubSpot. Creates personalized Gmail drafts for each prospect with vertical-specific templates.

**Key Features:**
- 7 ICP verticals: Higher Ed (90), Courts (85), Gov (80), Corporate AV (80), Healthcare (75), HoW (70), K-12 (65)
- ATL-first targeting with seniority filters
- HubSpot dedup (email + company + name fuzzy match)
- 6 vertical-specific email templates
- Gmail draft creation (one per prospect, DO NOT SEND)
- HTML report with sortable columns + HubSpot/Apollo links

**Depends on:** prospect-enrich-skill, hubspot-revops-skill
**Feeds into:** sequence-load-skill

**Scheduled Task:** `prospect-refresh` — Monday 6:30 AM ET

**Triggers:** "run prospect refresh", "search new ICP prospects"

---

#### sequence-load-skill
**Location:** `active/sequence-load-skill/` | **Version:** 1.0.0

Monday 7:15 AM — Auto-load net-new prospects from prospect-refresh into Apollo outreach sequences. Validates Golden Rules, confirms phone numbers, checks for duplicate enrollments.

**Key Features:**
- Reads prospect-refresh HTML output for batch enrollment
- Dedup against HubSpot + Apollo (avoid re-enrollment)
- Maps prospects to vertical-specific Apollo sequences (BDR_HigherEd_1, etc.)
- Creates Apollo contacts if new, syncs to HubSpot
- Enrollment report with per-sequence breakdown

**Depends on:** prospect-refresh-skill
**Feeds into:** callable-lead-count-skill, morning-brief-skill

**Scheduled Task:** `sequence-load` — Monday 7:15 AM ET

**Triggers:** "load prospects into sequences", "enroll new leads"

---

#### callable-lead-count-skill
**Location:** `active/callable-lead-count-skill/` | **Version:** 1.0.0

M-F 7:25 AM — Daily callable lead inventory with ATL/BTL breakdown. Calculates ATL Runway metric (days of ATL dials at 15/day target). Alerts if inventory falls below thresholds.

**Key Features:**
- Full ATL/BTL/GRAY/NEVER classification of callable contacts
- ATL Runway = ATL count ÷ 15 dials/day
- Alert thresholds: ATL < 15 (⚠️), total < 50 (🚨), NEVER > 0 (🔍)
- Day-over-day trend tracking
- Top companies by lead density
- JSON output for morning-brief integration

**Depends on:** hubspot-revops-skill
**Feeds into:** morning-brief-skill

**Scheduled Task:** `callable-lead-count` — M-F 7:25 AM ET

**Triggers:** "show callable leads", "lead inventory check", "ATL runway"

---

#### morning-brief-skill
**Location:** `active/morning-brief-skill/` | **Version:** 1.0.0

M-F 7:30 AM — Tim's daily briefing: calendar, HubSpot hot leads, deal momentum, Clari call summaries, and Gmail drafts for each priority lead. Single-page HTML brief for quick review before 50+ daily dials.

**Key Features:**
- Calendar integration: meetings, focus blocks, available dial windows
- 15-20 hot leads sorted ATL-first with deal + activity enrichment
- Supabase cooldown filter (skip leads in disposition cooldown)
- Deal momentum scores per associated deal
- Clari call summaries (last 7 days)
- Gmail draft per lead (3 templates: High Momentum, New Lead, Warm Lead)
- Branded HTML brief with sections: Calendar, Dial List, Pipeline, Call Highlights, Health Metrics, Tasks

**Depends on:** callable-lead-count-skill, deal-momentum-analyzer-skill, hubspot-revops-skill

**Scheduled Task:** `morning-brief` — M-F 7:30 AM ET

**Triggers:** "show morning brief", "today's dial list", "morning brief"

---

#### he-dial-queue-skill
**Location:** `active/he-dial-queue-skill/` | **Version:** 1.1.0

Builds the Higher-Ed SDR pod's daily tiered dial queue (Tier 1/2/3) from the existing HubSpot pool with Golden Rules + AE-ownership + deal-association suppression, emits a Nooks-ready Google Sheet, and monitors inventory with a capped Apollo top-up gate.

**Depends on:** phone-verification-waterfall-skill
**Integrates with:** phone-verification-waterfall-skill, morning-brief-skill, callable-lead-count-skill, nooks-autopilot

**Triggers:** "build HE dial queue", "refresh pod dial list", "higher-ed dial queue", "daily dial queue", "tier callable leads", "nooks dial list"

---

#### nooks-autopilot
**Location:** `active/nooks-autopilot/` | **Version:** 1.0.0

> Naming exception: no `-skill` suffix — live-automation name.

Autonomous BDR/SDR team that hunts leads to a warm reply: sources from HubSpot [AI] lists, qualifies (Golden Rules + Suppression + ATL/BTL + persona match), routes each lead to the right Nooks sequence by play, and (shadow-first) enrolls + monitors for replies to hand each rep a warm contact and their next-best 5 to call.

**Depends on:** sequence-load-skill
**Integrates with:** sequence-load-skill, prospect-research-to-cadence-skill, prospect-enrich-skill, phone-verification-waterfall-skill, morning-brief-skill

**Triggers:** "run nooks autopilot", "autonomous BDR run", "hunt leads", "enroll into nooks sequences", "shadow enroll", "autopilot dry run", "check for replies", "warm handoffs"

---

#### sdr-dial-lists
**Location:** `active/sdr-dial-lists/` | **Version:** 1.0.0

> Naming exception: no `-skill` suffix — live-automation name.

Daily SDR dial-list builder for Edgar Marroquin + Vasil Ivanov. Builds each SDR a ranked callable queue every weekday morning with spec-accurate talking points and calibrated discovery questions sourced from epiphan-call-playbook. Read-only except per-SDR Slack DM + optional HTML/XLSX artifact.

**Depends on:** epiphan-call-playbook
**Integrates with:** epiphan-call-playbook, sdr-call-coaching, nooks-autopilot

**Triggers:** "build SDR dial lists", "Edgar's call list", "Vasil's dial queue", "feed the SDRs", "SDR morning queue"

---

#### sdr-call-coaching
**Location:** `active/sdr-call-coaching/` | **Version:** 1.0.0

> Naming exception: no `-skill` suffix — live-automation name.

Weekly SDR call-coaching loop for Tim (coaching Edgar Marroquin + Vasil Ivanov). Pulls real connected Nooks dials + external Clari calls, scores every coachable call against a 4-dimension rubric (Orlob discovery, opener + take-control, Epiphan spec accuracy, MEDDIC capture), and outputs per-SDR coaching cards + a team trend. Read-only except Slack DM to Tim + optional Gmail draft. Runs Fridays ~11 AM CST.

**Depends on:** epiphan-call-playbook
**Integrates with:** epiphan-call-playbook, sdr-dial-lists, nooks-autopilot

**Triggers:** "SDR call coaching", "coaching cards", "score SDR calls", "review Edgar's calls", "review Vasil's calls", "weekly call review"

---

### Sales Enablement (P14 Harvest)

#### epiphan-ai-mcp-guide-skill
**Location:** `active/epiphan-ai-mcp-guide-skill/` | **Version:** 1.0.0

Day-one reference for the Epiphan AI + CRM/Clari MCP toolset, golden defaults, caveats, and the 5-vertical persona pack.

**Integrates with:** business-pulse-skill, greenfield-pearl-tracker-skill, blue-ocean-strategy-skill, morning-brief-skill, sales-revenue-skill

**Triggers:** "epiphan mcp", "epiphan ai tools", "crm tools", "which epiphan tool", "sdr onboarding", "weekly brief", "query dataset", "clari calls"

---

#### business-pulse-skill
**Location:** `active/business-pulse-skill/` | **Version:** 1.0.0

Live firm-wide sales pulse (revenue vs pace, pipeline, won/lost, BDR activity) with coaching takeaways, from the Epiphan AI MCP.

**Depends on:** epiphan-ai-mcp-guide-skill
**Integrates with:** epiphan-ai-mcp-guide-skill, pipeline-health-analyzer-skill, sales-revenue-skill, morning-brief-skill

**Triggers:** "business pulse", "how are we doing", "pipeline health", "revenue pace", "weekly numbers", "standup brief", "sales snapshot"

---

#### close-plan-generator-skill
**Location:** `active/close-plan-generator-skill/` | **Version:** 1.0.0

Generates comprehensive close plans for Epiphan Video deals: MEDDIC stakeholder mapping, decision process, competitive position, reverse-engineered close timeline, risk register, this-week actions, mutual action plan, and a 0-100 close confidence score.

**Depends on:** epiphan-ai-mcp-guide-skill
**Integrates with:** deal-momentum-analyzer-skill, meddic-call-prep-auto-skill, ae-handoff-brief-skill, epiphan-ai-mcp-guide-skill

**Triggers:** "close plan", "build close plan", "close strategy", "closing plan", "deal close checklist", "how do I close", "what's blocking"

---

#### cost-discovery-coach-skill
**Location:** `active/cost-discovery-coach-skill/` | **Version:** 1.0.0

Turns the cost-of-inaction calculator's inputs into tight, spec-true discovery questions per vertical (JTBD job + Never-Split calibrated question + Challenger insight).

**Depends on:** epiphan-ai-mcp-guide-skill
**Integrates with:** jobs-to-be-done-skill, never-split-the-difference-skill, challenger-sale-skill, epiphan-ai-mcp-guide-skill, greenfield-pearl-tracker-skill

**Triggers:** "discovery questions", "how to ask", "calculator discovery", "cost of inaction questions", "sdr call prep", "what do I ask"

---

#### demo-execution-playbook-skill
**Location:** `active/demo-execution-playbook-skill/` | **Version:** 1.0.0

Structured demo execution framework for Epiphan AEs: vertical-specific demo flows, RECAP-AGENDA-SHOW VALUE-SUMMARIZE-NEXT STEPS skeleton, Traffic Light live coaching, LAER objection handling, competitive displacement scripts, and post-demo scorecard.

**Depends on:** epiphan-ai-mcp-guide-skill, meddic-call-prep-auto-skill, challenger-sale-skill
**Integrates with:** epiphan-ai-mcp-guide-skill, meddic-call-prep-auto-skill, challenger-sale-skill, ae-handoff-brief-skill, call-recording-analyzer-skill

**Triggers:** "demo playbook", "demo flow for", "how should I demo to", "demo checklist", "live demo prep", "demo execution", "post-demo scorecard"

---

#### greenfield-pearl-tracker-skill
**Location:** `active/greenfield-pearl-tracker-skill/` | **Version:** 1.0.0

Find and track greenfield Pearl/EC20 opportunities (new-build, remote production, post-NAB broadcast fly-kit/automation) from live CRM + Clari signals.

**Depends on:** epiphan-ai-mcp-guide-skill
**Integrates with:** epiphan-ai-mcp-guide-skill, deal-momentum-analyzer-skill, cost-discovery-coach-skill, blue-ocean-strategy-skill

**Triggers:** "greenfield opportunities", "new build", "fly kit", "remote production", "broadcast deals", "NAB signals", "find new logos"

---

#### epiphan-call-playbook
**Location:** `active/epiphan-call-playbook/` | **Version:** 1.0.0

> Naming exception: no `-skill` suffix — live-automation name.

Canonical Epiphan cold + discovery CALL playbook for Tim's BDR/SDR team (Tim, Edgar, Vasil). Openers, live Orlob discovery flow per vertical, objection handling, spec-accurate talking points by product (Verified Spec Bank), and the close/next-step. Every spec verified via Epiphan AI search_product_catalog / search_product_knowledge.

**Integrates with:** sdr-dial-lists, sdr-call-coaching, nooks-autopilot

**Triggers:** "call script", "cold call", "discovery call", "opener", "objection handling", "talking points", "what to say on the phone"

---

### Sales Automation (P14 Harvest)

#### post-demo-automation-skill
**Location:** `active/post-demo-automation-skill/` | **Version:** 1.0.0

Automates the post-demo follow-up sequence for Epiphan AEs: Challenger-style demo recap emails, internal HubSpot MEDDIC debrief notes, next-meeting scheduling, stakeholder expansion for single-threaded deals, and a 5-touch momentum plan with Day-14 BDR escalation.

**Integrates with:** meddic-call-prep-auto-skill, deal-momentum-analyzer-skill, challenger-sale-skill, never-split-the-difference-skill, close-plan-generator-skill, ae-handoff-brief-skill

**Triggers:** "post-demo", "demo follow-up", "follow up after demo", "send demo recap", "demo debrief", "what's next after demo"

---

### Sales Intelligence (Imported)

#### champion-identifier-skill
**Location:** `active/champion-identifier-skill/` | **Version:** 1.0.0

Analyze LinkedIn profiles in target accounts to identify potential internal champions. Evaluates role, career path, mutual connections, interests, and suggests personalization approach.

**Triggers:** "find champion", "internal champion", "who will champion"

---

#### cold-email-sequence-generator-skill
**Location:** `active/cold-email-sequence-generator-skill/` | **Version:** 1.0.0

Generate personalized cold email sequences (7-14 emails) with A/B test subject lines, follow-up timing, and social proof integration. Multi-touch campaigns optimized for response rates.

**Triggers:** "cold email sequence", "email campaign", "outbound sequence", "lead gen emails"

---

#### contact-hunter-skill
**Location:** `active/contact-hunter-skill/` | **Version:** 1.0.0

Search and extract contact information from multiple sources: names, phone numbers, emails, job titles, LinkedIn profiles. Aggregates and enriches contact data. Complements Apollo/Clay for edge cases.

**Triggers:** "find contact info", "contact hunter", "extract contacts", "who works at"

---

#### email-template-generator-skill
**Location:** `active/email-template-generator-skill/` | **Version:** 1.0.0

Generate professional email templates for sales outreach, customer support, follow-ups, and apologies. Tone-appropriate with subject line variations.

**Triggers:** "email template", "write email", "sales email", "follow-up email"

---

#### inbound-lead-qualifier-skill
**Location:** `active/inbound-lead-qualifier-skill/` | **Version:** 1.0.0

Score inbound leads (form fills, demo requests) by ICP fit, intent, and urgency. Auto-generates qualification questions, routes to right rep, and suggests personalized first touch.

**Triggers:** "qualify inbound", "score lead", "inbound lead", "demo request scoring"

---

#### intent-signal-aggregator-skill
**Location:** `active/intent-signal-aggregator-skill/` | **Version:** 1.0.0

Monitor buyer intent signals: job postings, tech changes, funding rounds, leadership changes. Alerts when prospects show buying signals and prioritizes "hot" accounts.

**Triggers:** "intent signals", "buyer intent", "buying signals", "hot accounts"

---

#### linkedin-sales-navigator-alt-skill
**Location:** `active/linkedin-sales-navigator-alt-skill/` | **Version:** 1.0.0

Build targeted prospect lists by analyzing LinkedIn profiles: job titles, companies, locations, recent activity. Identifies decision-makers, tracks job changes for warm outreach.

**Triggers:** "linkedin prospects", "sales navigator", "decision maker search", "job change alerts"

---

#### lookalike-customer-finder-skill
**Location:** `active/lookalike-customer-finder-skill/` | **Version:** 1.0.0

Input best customers, find 100+ companies matching the profile. Uses firmographic data, tech stack, growth signals, and similarity scoring.

**Triggers:** "lookalike companies", "similar companies", "target account list", "expand to new markets"

---

#### meeting-intelligence-system-skill
**Location:** `active/meeting-intelligence-system-skill/` | **Version:** 1.0.0

Analyze meeting transcripts to extract decisions, action items, blockers, sentiment. Generate structured summaries and follow-up emails.

**Triggers:** "meeting notes", "transcript analysis", "meeting summary", "action items from meeting"

---

#### personalization-at-scale-skill
**Location:** `active/personalization-at-scale-skill/` | **Version:** 1.0.0

Generate unique personalized first lines for 100s of prospects using company news, LinkedIn activity, mutual connections. Saves 10+ hours of manual research per campaign.

**Triggers:** "personalize at scale", "first lines", "personalized outreach", "batch personalization"

---

#### pipeline-health-analyzer-skill
**Location:** `active/pipeline-health-analyzer-skill/` | **Version:** 1.0.0

Analyze pipeline health, identify stalled deals, predict close probability. Forecast accuracy improvement and revenue leakage prevention. Supplements deal-momentum-analyzer with broader pipeline analytics.

**Triggers:** "pipeline health", "forecast accuracy", "deal slippage", "revenue leakage"

---

#### sales-methodology-implementer-skill
**Location:** `active/sales-methodology-implementer-skill/` | **Version:** 1.0.0

Implement MEDDIC, BANT, Sandler, Challenger, SPIN across teams. Framework-specific questions, deal scoring, training materials, certification tracking.

**Triggers:** "sales methodology", "implement MEDDIC", "BANT framework", "Sandler training", "SPIN selling"

---

#### social-selling-content-generator-skill
**Location:** `active/social-selling-content-generator-skill/` | **Version:** 1.0.0

Generate 30+ LinkedIn posts that attract target prospects. Industry insights, thought leadership, engagement prompts, and comment strategies for building personal brand.

**Triggers:** "social selling", "LinkedIn content", "thought leadership posts", "attract prospects"

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

#### jobs-to-be-done-skill
**Location:** `active/jobs-to-be-done-skill/`

Jobs To Be Done analysis using Christensen's theory and Ulwick's Outcome-Driven Innovation (ODI) methodology.

| Component | Purpose |
|-----------|---------|
| Job Statement | [When___], [I want to___], [so I can___] |
| Job Map | 8 universal steps of every job |
| Outcome Statements | Direction + Metric + Object |
| Forces of Progress | Push/Pull/Anxiety/Habit analysis |
| Hiring/Firing | Competitive landscape through job lens |
| Switch Interview | Timeline-based discovery template |
| Opportunity Algorithm | ODI importance vs satisfaction scoring (0-100) |

**Key Features:**
- Dual-mode: Sales discovery AND strategic innovation
- BDR Quick Reference for live discovery calls
- Opportunity scoring (0-100, consistent with Blue Ocean/BMC)
- Worked example: video conferencing for hybrid teams

**Triggers:** "jobs to be done", "JTBD", "ODI", "forces of progress", "outcome statements", "why customers switch"

---

#### challenger-sale-skill
**Location:** `active/challenger-sale-skill/`

The Challenger Sale methodology — Teach-Tailor-Take Control framework for B2B sales. Build commercial insights that reframe customer thinking, tailor messages to stakeholder types, and handle objections with constructive tension.

**Triggers:** `challenger sale`, `commercial teaching`, `constructive tension`, `teach tailor take control`, `insight selling`, `commercial insight`, `challenger rep`

**Integrates with:** jobs-to-be-done, blue-ocean-strategy, business-model-canvas, never-split-the-difference, sales-revenue

---

#### never-split-the-difference-skill
**Location:** `active/never-split-the-difference-skill/`

Chris Voss FBI negotiation framework — tactical empathy, calibrated questions, mirroring, labeling, accusation audits, and the Ackerman bargaining model. Applied to B2B sales, deal negotiation, and business development communication.

**Triggers:** `never split the difference`, `tactical empathy`, `calibrated questions`, `mirroring`, `labeling`, `accusation audit`, `ackerman model`, `chris voss`

**Integrates with:** challenger-sale, jobs-to-be-done, blue-ocean-strategy, business-model-canvas, sales-revenue

---

## Folder Structure

```
skills/
├── active/                    # 80 active skills (partial listing — see Quick Lookup above)
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
│   ├── jobs-to-be-done-skill/
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

#### ae-handoff-brief-skill
**Location:** `active/ae-handoff-brief-skill/` | **Version:** 1.0.0

Auto-generate structured AE handoff briefs when Tim books a demo for Phil Sandler or Lex Evans. Packages MEDDIC scorecard (6 dimensions with gaps flagged), all prior Clari call summaries, competitive landscape, ATL/BTL contact validation, and a vertical-specific demo flow recommendation into a single document scannable in 60 seconds.

**Key Features:**
- Parallel data gather: HubSpot deals, Clari call history (90 days), Apollo enrichment, CRM activity
- MEDDIC scorecard: all 6 dimensions with known intel + explicit gap + AE coaching question
- ATL/BTL validation: flags if no economic buyer is on the demo invite (RED FLAG)
- Vertical-specific demo flow (Higher Ed, Courts, Corporate AV, Government, Healthcare, HoW, K-12)
- Objection forecast based on discovery data
- Delivers: Gmail draft to AE + HubSpot deal note

**Depends on:** deal-momentum-analyzer-skill, meddic-call-prep-auto-skill
**Integrates with:** call-recording-analyzer-skill
**MCP Tools:** Epiphan CRM (HubSpot + Clari), Apollo (enrich_contact), Gmail (create_draft), Google Calendar

**Triggers:** "handoff to Phil", "handoff to Lex", "ae brief", "hand off", "prep handoff", "pass to AE", "demo booked for"

---

#### call-recording-analyzer-skill
**Location:** `active/call-recording-analyzer-skill/` | **Version:** 1.0.0

Gong/Chorus-style call transcript analysis using Clari data. Scores every call against MEDDIC framework (0-100), flags missed discovery questions, extracts competitor mentions, calculates talk-to-listen ratio, identifies coaching moments. Feeds deal-momentum-analyzer Signal 4 and morning-brief.

**Key Features:**
- MEDDIC scoring: 6 dimensions, 100-point scale with STRONG/ADEQUATE/WEAK/MISSED classification
- ATL/BTL validation of all call attendees — flags if no economic buyer on call
- Talk ratio: target prospect 60%+; flags premature pitching
- Question quality: categorizes Open-ended/Calibrated/Closed/Leading/Feature dump
- Competitive intel extraction: Extron, Blackmagic, Kaltura, Panopto, YuJa, Echo360, etc.
- Coaching moments: timestamps + what happened + what to do differently
- Batch mode: "review today's calls" analyzes all same-day calls

**Integrates with:** deal-momentum-analyzer-skill, morning-brief-skill, meddic-call-prep-auto-skill
**MCP Tools:** Epiphan Clari (search_calls, get_call, get_call_summary), Epiphan CRM (HubSpot), Gmail

**Triggers:** "analyze call", "call review", "score my call", "what did I miss", "call coaching", "review my last call", "Clari scorecard"

---

#### dead-deal-recovery-skill
**Location:** `active/dead-deal-recovery-skill/` | **Version:** 1.0.0

Prevent pipeline rot by systematically identifying and triaging stalled/dying deals. Scores every open deal on 5 death signals, classifies as HEALTHY/RECOVERABLE/DEAD, generates 3-touch recovery email campaigns (Day 0 check-in, Day 4 value bomb, Day 10 break-up), and formally disqualifies dead weight with root cause documentation.

**Key Features:**
- 5-signal health scoring: activity recency, champion engagement, close date integrity, MEDDIC completeness, stakeholder breadth
- Root cause mapping: GHOST, NO_CHAMPION, SINGLE_THREADED, BUDGET_STALL, COMPETITOR_WIN, TIMING, UNQUALIFIED
- Recovery campaign: 3 Gmail drafts (tactical empathy, Challenger reframe, no-oriented break-up)
- Disqualification checklist: 7-step protocol before closing any deal as Lost
- Monthly lost deal review: win rate by vertical, loss by root cause, MEDDIC correlation
- Integrates into morning-brief for daily stall threshold alerts

**Depends on:** meddic-call-prep-auto-skill, pipeline-health-analyzer-skill
**Integrates with:** deal-momentum-analyzer-skill, morning-brief-skill, challenger-sale-skill
**MCP Tools:** Epiphan CRM (HubSpot + Clari), Gmail (recovery drafts), Apollo (enrich_contact)

**Triggers:** "dead deals", "stalled deals", "clean pipeline", "pipeline cleanup", "zombie deals", "pipeline hygiene", "deal recovery", "lost deal review"

---

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

---

## P15 Skills (2026-07-03) — 4 skills added (82 → 86)

### New Skills

#### batch-send-drafts-skill
**Location:** `active/batch-send-drafts-skill/` | **Version:** 1.0.0
**Triggers:** "send staged drafts", "flush draft queue", "batch send drafts", "review my drafts"
**Category:** Sales Automation

Review and batch-send staged Gmail BDR outreach drafts. Uses Gmail MCP to list all queued drafts, enriches each with vertical/ATL classification, presents a prioritized review table, and generates one-click Gmail deep links per draft so Tim can flush the queue without hunting through Gmail.

**Integrates with:** morning-brief-skill, cold-email-sequence-generator-skill, nooks-autopilot

---

#### orlob-discovery-framework-skill
**Location:** `active/orlob-discovery-framework-skill/` | **Version:** 1.0.0
**Triggers:** "discovery framework", "orlob discovery", "discovery questions", "cause analysis", "how to run discovery"
**Category:** Sales Methodology

Chris Orlob's 5-step discovery framework (business problem → cause analysis → negative impact → future state → close) applied to Epiphan. Includes per-vertical root causes (`reference/epiphan-root-causes.md`), calibrated question bank, MEDDIC integration points, and the 0-3 scoring rubric used by sdr-call-coaching.

**Integrates with:** epiphan-call-playbook, sdr-call-coaching, sdr-dial-lists, meddic-call-prep-auto-skill

---

#### sdr-email-sms-playbook-skill
**Location:** `active/sdr-email-sms-playbook-skill/` | **Version:** 1.0.0
**Triggers:** "email playbook", "email template", "outreach email", "cold email template", "sms outreach", "5 touch cadence"
**Category:** Sales Outreach

5-touch email/SMS cadence for Epiphan BDR outreach. Email/SMS companion to epiphan-call-playbook (phone). Full templates for Higher Ed, Courts, Government, Healthcare cold outreach; follow-up and break-up patterns; subject line rules; SMS guidelines (2 sentences max).

**Integrates with:** epiphan-call-playbook, cold-email-sequence-generator-skill, nooks-autopilot, batch-send-drafts-skill

---

#### weekly-kpi-report-skill
**Location:** `active/weekly-kpi-report-skill/` | **Version:** 1.0.0
**Schedule:** Fridays 5:30 PM CST (`0 30 17 * * 5`, America/Chicago)
**Triggers:** "weekly kpi report", "kpi report", "sdr metrics", "team scorecard"
**Category:** BDR Analytics

Friday 5:30 PM weekly KPI report for Tim's SDR pod. Pulls Nooks dials/connects + HubSpot meetings-booked and pipeline-created per rep (Tim, Edgar, Vasil), calculates attainment vs weekly targets, outputs GREEN/YELLOW/RED scorecards with week-over-week trend arrows, HTML report, and compact Slack DM to Tim. MEASURES the team; sdr-call-coaching COACHES.

**Integrates with:** sdr-call-coaching, morning-brief-skill, callable-lead-count-skill, nooks-autopilot
