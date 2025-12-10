# Skills Index

> Last updated: 2025-12-10

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

---

## Stable Skills (Battle-Tested)

### workflow-enforcer
**Location:** `./stable/workflow-enforcer/SKILL.md`
**Lines:** ~91 (trimmed from 256)
**Global:** Symlinked to `~/.claude/skills/`

Enforces workflow discipline across ALL projects. Ensures Claude checks for specialized agents, announces usage, and creates TodoWrite todos.

**Reference Files:**
- `reference/agents-catalog.md` - Full 70+ agent table by category

**Activates:** Every session start

---

### project-context-skill
**Location:** `./stable/project-context-skill/SKILL.md`
**Lines:** ~80
**Global:** Symlinked to `~/.claude/skills/`

Maintains project context and progress tracking across Claude Code sessions.

**Reference Files:**
- `reference/template.md` - Full context file template with examples

**Keywords:** `context`, `session`, `save`, `done`, `end session`

---

## Active Skills (In Development)

### trading-signals-skill
**Location:** `./active/trading-signals-skill/SKILL.md`
**Lines:** ~105

**Comprehensive technical analysis patterns extracted from ThetaRoom & SwaggyStacks.**

| Methodology | Coverage |
|-------------|----------|
| Elliott Wave | Wave rules, halving supercycle, target projection |
| Turtle Trading | Donchian breakouts, ATR sizing, pyramiding |
| Fibonacci | Golden pocket, on-chain levels, confluence |
| Wyckoff | Phase detection, VSA, composite operator |
| Markov Regime | 7-state model, transition probabilities |
| Pattern Recognition | Candlestick + chart patterns |
| Swarm Consensus | Multi-LLM voting (NO OpenAI) |

**Reference Files (7):**
- `reference/elliott-wave.md` - Wave rules, halving supercycle, targets
- `reference/turtle-trading.md` - Donchian channels, ATR sizing, crypto adaptation
- `reference/fibonacci.md` - Levels, golden pocket, MVRV zones
- `reference/wyckoff.md` - Phase state machines, VSA
- `reference/markov-regime.md` - State definitions, transitions
- `reference/pattern-recognition.md` - Candlestick + chart patterns
- `reference/swarm-consensus.md` - Multi-LLM voting system

**Keywords:** `fibonacci`, `elliott wave`, `wyckoff`, `turtle`, `confluence`, `golden pocket`, `swarm`

**Projects:** ThetaRoom, swaggy-stacks, alpha-lens

---

### sales-outreach-skill
**Location:** `./active/sales-outreach-skill/SKILL.md`
**Lines:** ~99 (trimmed from 289)

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

**Keywords:** `cold outreach`, `lead scoring`, `BDR`, `email sequence`, `ICP`, `domain warming`

---

### runpod-deployment-skill
**Location:** `./active/runpod-deployment-skill/SKILL.md`
**Lines:** ~105

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

**Keywords:** `runpod`, `serverless`, `vllm`, `GPU`, `inference`, `A100`, `H100`, `M1`

---

### langgraph-agents-skill
**Location:** `./active/langgraph-agents-skill/SKILL.md`
**Lines:** ~109

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

**Keywords:** `langgraph`, `langchain`, `agents`, `orchestration`, `swarm`, `supervisor`, `state`, `multi-agent`

**Projects:** sales-agent, robot-brain, vozlux, fieldvault-ai

---

## Folder Structure

```
skills/
├── active/                              # Skills being developed
│   ├── trading-signals-skill/
│   │   ├── SKILL.md                     # ~105 lines
│   │   └── reference/                   # 7 files
│   ├── sales-outreach-skill/
│   │   ├── SKILL.md                     # ~99 lines
│   │   └── reference/                   # 3 files
│   ├── runpod-deployment-skill/
│   │   ├── SKILL.md                     # ~105 lines
│   │   └── reference/                   # 4 files
│   └── langgraph-agents-skill/
│       ├── SKILL.md                     # ~109 lines
│       └── reference/                   # 6 files
├── stable/                              # Production-ready skills
│   ├── workflow-enforcer/
│   │   ├── SKILL.md                     # ~91 lines
│   │   └── reference/                   # 1 file
│   └── project-context-skill/
│       ├── SKILL.md                     # ~80 lines
│       └── reference/                   # 1 file
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
   - YAML frontmatter (name, description with keywords)
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
langgraph-agents-skill ─┘    (state schemas, orchestration patterns)

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
