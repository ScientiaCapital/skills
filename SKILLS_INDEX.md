# Skills Index

> Last updated: 2025-12-23
> Total skills: 25 (2 stable, 23 active)

## Architecture

**Progressive Disclosure** - Skills load in layers to minimize token usage:
- **Level 1:** YAML frontmatter (loads at startup for activation)
- **Level 2:** SKILL.md content (loads when skill activates)
- **Level 3:** reference/*.md files (loads only when needed)

---

## Quick Lookup

| Need to... | Use Skill | Location |
|------------|-----------|----------|
| Enforce workflow discipline | [workflow-enforcer](#workflow-enforcer) | stable/ |
| Track project context across sessions | [project-context-skill](#project-context-skill) | stable/ |
| Build trading signals, technical analysis | [trading-signals-skill](#trading-signals-skill) | active/ |
| Set up sales automation, cold outreach | [sales-outreach-skill](#sales-outreach-skill) | active/ |
| Deploy models to GPU, RunPod serverless | [runpod-deployment-skill](#runpod-deployment-skill) | active/ |
| Build multi-agent systems, LangGraph orchestration | [langgraph-agents-skill](#langgraph-agents-skill) | active/ |
| Clean SQL migrations for Supabase | [supabase-sql-skill](#supabase-sql-skill) | active/ |
| Research companies, competitive analysis | [market-research-skill](#market-research-skill) | active/ |
| Evaluate frameworks, APIs, LLM providers | [technical-research-skill](#technical-research-skill) | active/ |
| Brainstorm opportunities, evaluate clients | [opportunity-evaluator-skill](#opportunity-evaluator-skill) | active/ |
| Define ICP, positioning, messaging | [gtm-strategy-skill](#gtm-strategy-skill) | active/ |
| Run discovery calls, MEDDIC qualification | [demo-discovery-skill](#demo-discovery-skill) | active/ |
| Pipeline analysis, forecasting, RevOps | [revenue-ops-skill](#revenue-ops-skill) | active/ |
| Content strategy, LinkedIn, blog SEO | [content-marketing-skill](#content-marketing-skill) | active/ |
| Pricing models, packaging, tiering | [pricing-strategy-skill](#pricing-strategy-skill) | active/ |
| Build voice agents (Cartesia, Deepgram, Twilio) | [voice-ai-skill](#voice-ai-skill) | active/ |
| Executive data analysis, dashboards, investor presentations | [data-analysis-skill](#data-analysis-skill) | active/ |
| Manage parallel git worktrees with agents | [worktree-manager-skill](#worktree-manager-skill) | active/ |
| Create hierarchical project plans | [create-plans-skill](#create-plans-skill) | active/ |
| Systematic expert debugging | [debug-like-expert-skill](#debug-like-expert-skill) | active/ |
| Build specialized Claude subagents | [create-subagents-skill](#create-subagents-skill) | active/ |
| Author new Claude skills | [create-agent-skills-skill](#create-agent-skills-skill) | active/ |
| Create automation hooks | [create-hooks-skill](#create-hooks-skill) | active/ |
| Build custom slash commands | [create-slash-commands-skill](#create-slash-commands-skill) | active/ |
| Design meta-prompts for chaining | [create-meta-prompts-skill](#create-meta-prompts-skill) | active/ |

---

## Stable Skills (Battle-Tested)

### workflow-enforcer
**Location:** `./stable/workflow-enforcer/SKILL.md`

**Global:** Symlinked to `~/.claude/skills/`

Enforces workflow discipline across ALL projects. Ensures Claude checks for specialized agents, announces usage, and creates TodoWrite todos.

**Reference Files:**
- `reference/agents-catalog.md` - Full 70+ agent table by category

**Triggers:** Automatic on all sessions, "use the right agent", "follow workflow"

---

### project-context-skill
**Location:** `./stable/project-context-skill/SKILL.md`

**Global:** Symlinked to `~/.claude/skills/`

Maintains project context and progress tracking across Claude sessions. Works in both Claude Code (terminal) and Claude Desktop.

**Reference Files:**
- `reference/template.md` - Full context file template with examples
- `reference/projects-list.md` - All 36 projects with context files (for Claude Desktop)

**Triggers:** "load project context", "save context", "end session", "switch to [project]"

---

## Active Skills (In Development)

### trading-signals-skill
**Location:** `./active/trading-signals-skill/SKILL.md`


Technical analysis patterns for quantitative trading systems.

| Methodology | Coverage |
|-------------|----------|
| Elliott Wave | Wave rules, halving supercycle, target projection |
| Turtle Trading | Donchian breakouts, ATR sizing, pyramiding |
| Fibonacci | Golden pocket, on-chain levels, confluence |
| Wyckoff | Phase detection, VSA, composite operator |
| Markov Regime | 7-state model, transition probabilities |
| Pattern Recognition | Candlestick + chart patterns |
| Swarm Consensus | Multi-LLM voting (NO OpenAI) |

**Reference Files (8):**
- `reference/elliott-wave.md` - Wave rules, halving supercycle, targets
- `reference/turtle-trading.md` - Donchian channels, ATR sizing, crypto adaptation
- `reference/fibonacci.md` - Levels, golden pocket, MVRV zones
- `reference/wyckoff.md` - Phase state machines, VSA
- `reference/markov-regime.md` - State definitions, transitions
- `reference/pattern-recognition.md` - Candlestick + chart patterns
- `reference/swarm-consensus.md` - Multi-LLM voting system
- `reference/chinese-llm-stack.md` - Cost-optimized Chinese LLMs for trading

**Triggers:** "analyze chart", "fibonacci levels", "elliott wave", "wyckoff analysis", "trading signals"

**Projects:** ThetaRoom, swaggy-stacks, alpha-lens

---

### sales-outreach-skill
**Location:** `./active/sales-outreach-skill/SKILL.md`


B2B sales automation patterns for cold outreach and multi-agent sales systems.

| Covers | Projects |
|--------|----------|
| Lead scraping (Playwright) | dealer-scraper |
| 6-agent qualification pipeline | sales-agent |
| Domain warming protocol | cold-reach |
| Email sequences | fieldvault-ai |

**Reference Files:**
- `reference/coperniq-messaging.md` - ICP, templates, SMS sequences
- `reference/domain-warming.md` - Protocol, deliverability checklist
- `reference/agent-architecture.md` - 6-agent system, pipeline code

**Triggers:** "cold email", "lead scoring", "email sequence", "BDR automation", "domain warming"

---

### runpod-deployment-skill
**Location:** `./active/runpod-deployment-skill/SKILL.md`


RunPod serverless and pod deployment patterns for GPU-accelerated AI workloads.

**M1 Mac Note:** Cannot build Docker locally - uses GitHub Actions for x86 builds.

| Covers | Projects |
|--------|----------|
| GPU selection guide | ThetaRoom |
| vLLM serverless setup | sales-agent |
| Cost optimization (scale-to-zero) | Unsloth fine-tuning |
| CI/CD integration (M1 workaround) | - |

**Reference Files:**
- `reference/vllm-setup.md` - Environment vars, models, benchmarks
- `reference/project-configs.md` - ThetaRoom, sales-agent, Unsloth
- `reference/cicd.md` - GitHub Actions, M1 Mac workflow, MCP
- `reference/troubleshooting.md` - Common issues, health checks

**Triggers:** "deploy to RunPod", "GPU serverless", "vLLM endpoint", "A100 deployment", "scale to zero"

---

### langgraph-agents-skill
**Location:** `./active/langgraph-agents-skill/SKILL.md`


Production-tested patterns for multi-agent systems with LangGraph and LangChain. NO OPENAI.

| Pattern | Use When |
|---------|----------|
| Supervisor | Centralized routing, clear hierarchy |
| Swarm | Peer-to-peer, dynamic handoffs |
| Master Orchestrator | Complex workflows, learning systems |

**Reference Files (6):**
- `reference/state-schemas.md` - TypedDict, Annotated reducers, concurrent patterns
- `reference/base-agent-architecture.md` - Multi-provider setup (Anthropic, Groq, Cerebras)
- `reference/tools-organization.md` - Modular tool design, testing patterns
- `reference/orchestration-patterns.md` - Supervisor vs swarm vs master decision matrix
- `reference/context-engineering.md` - Memory compaction, just-in-time loading
- `reference/cost-optimization.md` - Provider routing, caching, token budgets

**Triggers:** "build LangGraph agent", "multi-agent workflow", "supervisor pattern", "StateGraph"

**Projects:** sales-agent, robot-brain, vozlux, fieldvault-ai

---

### supabase-sql-skill
**Location:** `./active/supabase-sql-skill/SKILL.md`


Clean SQL migrations for Supabase. Handles typo fixes, idempotency, RLS policy corrections, and consistent formatting.

| Fixes | Pattern |
|-------|---------|
| Typos | `- ` → `-- ` comment lines |
| Idempotency | `DROP IF EXISTS` before CREATE policy/trigger |
| RLS | Service role `TO service_role` not JWT check |
| Dead code | Remove unused enums when TEXT+CHECK used |
| Formatting | Consistent headers, casing (`NOW()`) |

**Reference Files:**
- `reference/rls-patterns.md` - User-owns, business-scoped, nested access
- `reference/function-patterns.md` - Triggers, atomic ops, batch inserts

**Triggers:** "fix this SQL", "clean migration", "RLS policy", "Supabase schema"

**Projects:** vozlux

---

### market-research-skill
**Location:** `./active/market-research-skill/SKILL.md`


Company research, competitive analysis, and lead enrichment for B2B sales.

| Research Type | Output |
|---------------|--------|
| Company Profile | Structured profile with tech stack |
| Tech Stack Discovery | Software + integrations |
| Competitive Intel | Market position, pricing |
| Leadership Research | Key contacts, changes |
| Pain Signal Detection | Triggers for outreach timing |

**Reference Files:**
- `reference/company-profile-template.md` - Full template with examples
- `reference/tech-stack-discovery.md` - Deep dive on software detection
- `reference/mep-contractor-icp.md` - Coperniq-specific ICP criteria
- `reference/competitive-analysis.md` - Competitor research framework

**Triggers:** "research this company", "analyze competitors", "build company profile", "ICP analysis"

**Pairs with:** sales-outreach-skill (messaging), opportunity-evaluator-skill (deals)

---

### technical-research-skill
**Location:** `./active/technical-research-skill/SKILL.md`


Framework comparisons, API evaluations, and implementation pattern research. NO OpenAI.

| Research Type | Output |
|---------------|--------|
| LLM Comparison | Cost/capability matrix |
| Framework Eval | Feature comparison + recommendation |
| API Assessment | Limits, pricing, DX |
| MCP Discovery | Available servers/tools |

**Reference Files:**
- `reference/framework-comparison.md` - Side-by-side evaluation template
- `reference/llm-evaluation-checklist.md` - Deep LLM provider analysis
- `reference/api-integration-patterns.md` - Common integration approaches
- `reference/mcp-discovery.md` - Finding and evaluating MCP servers

**Triggers:** "evaluate this framework", "compare these tools", "LLM provider comparison", "API assessment"

**Stack:** Claude, DeepSeek, Gemini (NO OpenAI), RunPod, Supabase, Vercel

---

### opportunity-evaluator-skill
**Location:** `./active/opportunity-evaluator-skill/SKILL.md`


General-purpose brainstorming partner for exploring opportunities. Works as a thinking partner, not a judge.

| Angle | Coverage |
|-------|----------|
| Project Ideas | Excitement, fit, effort, learning, alternatives |
| Client/Customer Eval | Fit, red flags, budget, scope, exit |
| Partnerships | Alignment, contribution, upside, track record |

**Reference Files:**
- `reference/client-evaluation-questions.md` - Deep dive on client fit
- `reference/project-viability.md` - Technical/business viability questions
- `reference/partnership-considerations.md` - Collaboration frameworks

**Triggers:** "help me think through this", "brainstorm this opportunity", "evaluate this client"

**Context:** Tim's 25+ years B2B experience lens

---

### gtm-strategy-skill
**Location:** `./active/gtm-strategy-skill/SKILL.md`

Go-to-market strategy development for B2B SaaS and services.

| Covers | Methodology |
|--------|-------------|
| ICP Definition | Jobs-to-be-done, firmographics, technographics |
| Positioning | April Dunford framework (5 components) |
| Messaging | Value hierarchy, personas, objection handling |
| Competitive Intel | Battlecard framework, differentiation |

**Reference Files:**
- `reference/icp-templates.md` - ICP canvas templates

**Triggers:** "define ICP", "positioning statement", "competitive analysis", "GTM strategy"

---

### demo-discovery-skill
**Location:** `./active/demo-discovery-skill/SKILL.md`

Discovery calls, demos, and qualification for B2B sales.

| Framework | Coverage |
|-----------|----------|
| SPIN | Situation, Problem, Implication, Need-Payoff |
| MEDDIC | Metrics, Economic Buyer, Decision Process/Criteria, Pain, Champion |
| Demo Flow | Recap, Agenda, Show Value, Summarize, Next Steps |
| LAER | Listen, Acknowledge, Explore, Respond (objections) |

**Triggers:** "discovery call", "run a demo", "MEDDIC", "qualification", "objection handling"

---

### revenue-ops-skill
**Location:** `./active/revenue-ops-skill/SKILL.md`

Sales metrics, pipeline analysis, and revenue forecasting.

| Metric Type | Coverage |
|-------------|----------|
| Pipeline | Coverage ratio, velocity, weighted pipeline |
| Conversion | Lead→MQL→SQL→Opp→Win funnel |
| Efficiency | CAC, LTV, LTV:CAC, payback period |
| Attribution | First/last touch, linear, U-shaped, W-shaped |

**Triggers:** "pipeline analysis", "forecast", "CAC", "LTV", "win rate", "conversion funnel"

---

### content-marketing-skill
**Location:** `./active/content-marketing-skill/SKILL.md`

B2B content strategy for demand generation and thought leadership.

| Content Type | Funnel Stage |
|--------------|--------------|
| LinkedIn posts | Top (awareness) |
| Blog/SEO | Top-Mid (discovery) |
| Case studies | Mid (consideration) |
| Video/Webinar | Mid-Bottom (decision) |

**Triggers:** "content strategy", "LinkedIn post", "blog SEO", "case study", "thought leadership"

---

### pricing-strategy-skill
**Location:** `./active/pricing-strategy-skill/SKILL.md`

B2B pricing strategy, packaging, and monetization.

| Model | Use Case |
|-------|----------|
| Per-seat | Team tools, collaboration |
| Usage-based | APIs, infrastructure |
| Tiered (Good/Better/Best) | Feature differentiation |
| Hybrid | Enterprise SaaS |

**Triggers:** "pricing strategy", "packaging", "tiering", "value-based pricing", "price increase"

---

### voice-ai-skill
**Location:** `./active/voice-ai-skill/SKILL.md`

Voice AI agents with Cartesia, Deepgram, AssemblyAI, Twilio, ElevenLabs. NO OPENAI.

| Component | Primary | Fallback |
|-----------|---------|----------|
| STT | Deepgram | AssemblyAI |
| TTS | Cartesia | ElevenLabs |
| Telephony | Twilio | - |
| LLM | Claude/DeepSeek | - |

**Triggers:** "voice agent", "voice AI", "Twilio", "Deepgram", "Cartesia", "phone bot"

**Projects:** vozlux, solarvoice-ai, langgraph-voice-agents

---

### data-analysis-skill
**Location:** `./active/data-analysis-skill/SKILL.md`

Executive-grade data analysis for VC, PE, angels, C-suite, and founders.

| Capability | Tools |
|------------|-------|
| Data ingestion | pandas, polars, pdfplumber, python-pptx |
| Wrangling | pandas/polars transforms, DuckDB |
| Visualization | Plotly, Altair, Seaborn (McKinsey/BCG style) |
| Dashboards | Streamlit production patterns |
| SaaS metrics | CAC, LTV, MRR, ARR, NRR, cohort analysis |

**Reference Files (4):**
- `reference/chart-gallery.md` - 20+ executive chart templates
- `reference/saas-metrics.md` - Complete SaaS KPI definitions
- `reference/streamlit-patterns.md` - Production dashboard patterns
- `reference/data-wrangling.md` - Format-specific extraction guides

**Triggers:** "analyze this data", "build a dashboard", "investor presentation", "SaaS metrics", "cohort analysis"

**Differentiator:** GTME who presents findings to C-suite, not just codes behind keyboard.

---

### worktree-manager-skill
**Location:** `./active/worktree-manager-skill/SKILL.md`

Git worktree automation for parallel development with Claude agents. M1/8GB optimized.

| Feature | Configuration |
|---------|---------------|
| Terminal | Ghostty (GPU-accelerated) |
| Max concurrent | 3 worktrees |
| Port range | 8100-8115 |
| Memory warning | 6GB threshold |

**Triggers:** "create worktree", "spin up worktrees", "parallel development", "worktree status", "cleanup worktrees"

**Source:** [Wirasm/worktree-manager-skill](https://github.com/Wirasm/worktree-manager-skill)

---

### create-plans-skill
**Location:** `./active/create-plans-skill/SKILL.md`

Hierarchical project planning where "PLAN.md IS the prompt". Solo developer + Claude workflow.

**Workflow:** Brief → Roadmap → Research → PLAN.md → Execute → Summary

**Features:**
- Domain-aware planning (loads expertise skills)
- Atomic tasks (2-3 per plan to avoid context degradation)
- 5 embedded deviation rules for autonomous execution
- Auto-handoff at 10% context remaining

**Triggers:** "create plan", "project planning", "roadmap", "break down this task", "phase planning"

**Source:** [glittercowboy/taches-cc-resources](https://github.com/glittercowboy/taches-cc-resources)

---

### debug-like-expert-skill
**Location:** `./active/debug-like-expert-skill/SKILL.md`

Systematic debugging with evidence gathering and hypothesis testing. Scientific method approach.

**Methodology:** Observe → Hypothesize → Test → Verify

**Triggers:** "debug systematically", "root cause analysis", "expert debugging", "why is this failing"

**Source:** [glittercowboy/taches-cc-resources](https://github.com/glittercowboy/taches-cc-resources)

---

### create-subagents-skill
**Location:** `./active/create-subagents-skill/SKILL.md`

Builds specialized Claude instances for isolated contexts with optimized system prompts.

**Triggers:** "create subagent", "spawn agent", "specialized Claude", "isolated agent"

**Source:** [glittercowboy/taches-cc-resources](https://github.com/glittercowboy/taches-cc-resources)

---

### create-agent-skills-skill
**Location:** `./active/create-agent-skills-skill/SKILL.md`

Meta-skill for building new skills through natural language description. Includes /heal-skill for self-improvement.

**Skill Types:**
- Task-execution skills (workflows, automation)
- Domain expertise skills (5k-10k+ knowledge bases)

**Triggers:** "create new skill", "build a skill", "skill authoring", "teach Claude to"

**Source:** [glittercowboy/taches-cc-resources](https://github.com/glittercowboy/taches-cc-resources)

---

### create-hooks-skill
**Location:** `./active/create-hooks-skill/SKILL.md`

Event-driven automation for tool calls, session events, and prompt submissions.

**Hook Types:** PreToolUse, PostToolUse, Stop, Prompt-based

**Triggers:** "create hook", "automation trigger", "on tool call", "event-driven"

**Source:** [glittercowboy/taches-cc-resources](https://github.com/glittercowboy/taches-cc-resources)

---

### create-slash-commands-skill
**Location:** `./active/create-slash-commands-skill/SKILL.md`

Command authoring with YAML configs, arguments, and dynamic context loading.

**Triggers:** "create slash command", "new command", "custom command", "/command authoring"

**Source:** [glittercowboy/taches-cc-resources](https://github.com/glittercowboy/taches-cc-resources)

---

### create-meta-prompts-skill
**Location:** `./active/create-meta-prompts-skill/SKILL.md`

Builds prompts with structured outputs for chaining (research.md → plan.md → implement).

**Triggers:** "create meta-prompt", "prompt chaining", "structured prompt", "workflow prompts"

**Source:** [glittercowboy/taches-cc-resources](https://github.com/glittercowboy/taches-cc-resources)

---

## Folder Structure

```
skills/
├── active/                              # Skills being developed (23)
│   ├── trading-signals-skill/
│   ├── sales-outreach-skill/
│   ├── runpod-deployment-skill/
│   ├── langgraph-agents-skill/
│   ├── supabase-sql-skill/
│   ├── market-research-skill/
│   ├── technical-research-skill/
│   ├── opportunity-evaluator-skill/
│   ├── gtm-strategy-skill/
│   ├── demo-discovery-skill/
│   ├── revenue-ops-skill/
│   ├── content-marketing-skill/
│   ├── pricing-strategy-skill/
│   ├── voice-ai-skill/
│   ├── data-analysis-skill/
│   ├── worktree-manager-skill/          # NEW: parallel development
│   ├── create-plans-skill/              # NEW: project planning
│   ├── debug-like-expert-skill/         # NEW: expert debugging
│   ├── create-subagents-skill/          # NEW: subagent builder
│   ├── create-agent-skills-skill/       # NEW: skill authoring
│   ├── create-hooks-skill/              # NEW: automation hooks
│   ├── create-slash-commands-skill/     # NEW: command builder
│   └── create-meta-prompts-skill/       # NEW: prompt chaining
├── stable/                              # Production-ready skills (2)
│   ├── workflow-enforcer/
│   └── project-context-skill/
├── dist/                                # Zips for Claude Desktop (25)
├── templates/
│   └── SKILL_TEMPLATE.md
├── PLANNING.md                          # Sprint tracking
├── BACKLOG.md                           # Priority queue
├── CLAUDE.md
└── SKILLS_INDEX.md                      # This file

~/.claude/skills/                        # Global copies (25 skills)
├── workflow-enforcer/
├── project-context-skill/
├── trading-signals-skill/
├── worktree-manager-skill/              # NEW
├── create-plans-skill/                  # NEW
├── ... (all 25 skills)
└── create-meta-prompts-skill/
```

---

## Adding a New Skill

1. Create folder in `active/` using naming: `skill-name-skill`
2. Add `SKILL.md` with:
   - YAML frontmatter (name, version, description with triggers)
   - Core patterns (~80-100 lines max)
   - Reference file pointers
3. Add `reference/` folder for detailed docs
4. Update this index
5. Move to `stable/` once battle-tested

---

## Skill Relationships

```
trading-signals-skill ──┬──→ runpod-deployment-skill (model serving)
                        │
sales-outreach-skill ───┼──→ langgraph-agents-skill (multi-agent orchestration)
                        │
market-research-skill ──┼──→ opportunity-evaluator-skill (deal evaluation)
                        │
technical-research-skill┘    (technology decisions)

workflow-enforcer ──────────→ All projects (global)
project-context-skill ──────→ All projects (global)
```

## Source Projects

| Project | Skills Extracted |
|---------|-----------------|
| ThetaRoom | Elliott Wave, Fibonacci (golden pocket), Wyckoff, Markov, Pattern Recognition, Swarm Consensus |
| SwaggyStacks | Turtle Trading, Halving Supercycle, 7-state Markov, Combinatorial Backtesting |
| cold-reach | Domain warming, Email sequences |
| sales-agent | 6-agent architecture, Lead scoring, LangGraph state schemas, multi-provider routing |
| robot-brain | Supervisor vs swarm orchestration, handoff mechanisms |
| vozlux | Master orchestrator, context engineering, self-learning patterns |
| dealer-scraper | Lead scraping, company profiling |
| Coperniq | B2B sales patterns, ICP framework |
