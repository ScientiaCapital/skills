# Skills Index

> Last updated: 2025-12-23
> Total skills: 10 (2 stable, 8 active)

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

## Folder Structure

```
skills/
├── active/                              # Skills being developed (8)
│   ├── trading-signals-skill/
│   ├── sales-outreach-skill/
│   ├── runpod-deployment-skill/
│   ├── langgraph-agents-skill/
│   ├── supabase-sql-skill/
│   ├── market-research-skill/
│   ├── technical-research-skill/
│   └── opportunity-evaluator-skill/
├── stable/                              # Production-ready skills (2)
│   ├── workflow-enforcer/
│   └── project-context-skill/
├── templates/
│   └── SKILL_TEMPLATE.md
├── CLAUDE.md
└── SKILLS_INDEX.md                      # This file

~/.claude/skills/                        # Global symlinks
├── workflow-enforcer -> .../stable/workflow-enforcer
└── project-context-skill -> .../stable/project-context-skill
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
