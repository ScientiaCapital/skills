# Skills Index

> Last updated: 2025-12-25
> Total skills: 18 (2 stable, 16 active)

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
| Build multi-agent LangGraph systems | [langgraph-agents](#langgraph-agents-skill) | Infrastructure |
| Deploy to RunPod GPU serverless | [runpod-deployment](#runpod-deployment-skill) | Infrastructure |
| Fast GROQ API inference | [groq-inference](#groq-inference-skill) | Infrastructure |
| Build voice AI agents | [voice-ai](#voice-ai-skill) | Infrastructure |
| Clean Supabase SQL migrations | [supabase-sql](#supabase-sql-skill) | Infrastructure |
| CRM integration (Close, HubSpot, Salesforce) | [crm-integration](#crm-integration-skill) | Business |
| GTM strategy, pricing, opportunity eval | [gtm-pricing](#gtm-pricing-skill) | Business |
| Market + technical research | [research](#research-skill) | Business |
| Sales outreach, discovery, RevOps | [sales-revenue](#sales-revenue-skill) | Business |
| B2B content marketing | [content-marketing](#content-marketing-skill) | Business |
| Executive data analysis, dashboards | [data-analysis](#data-analysis-skill) | Business |
| Trading signals, technical analysis | [trading-signals](#trading-signals-skill) | Business |
| Track project context across sessions | [project-context](#project-context-skill) | Core |
| Enforce workflow discipline | [workflow-enforcer](#workflow-enforcer) | Core |

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
| TTS | Cartesia Sonic-3 | ~90ms |
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

#### langgraph-agents-skill
**Location:** `active/langgraph-agents-skill/`

Multi-agent systems with LangGraph. NO OPENAI.

| Pattern | Use When |
|---------|----------|
| Supervisor | Centralized routing |
| Swarm | Peer-to-peer handoffs |
| Master Orchestrator | Complex workflows |

**Triggers:** "LangGraph agent", "multi-agent", "supervisor pattern"

---

#### supabase-sql-skill
**Location:** `active/supabase-sql-skill/`

Clean SQL migrations for Supabase: typo fixes, idempotency, RLS patterns.

**Triggers:** "fix SQL", "clean migration", "RLS policy"

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

## Folder Structure

```
skills/
├── active/                    # 16 active skills
│   ├── content-marketing-skill/
│   ├── crm-integration-skill/
│   ├── data-analysis-skill/
│   ├── debug-like-expert-skill/
│   ├── extension-authoring-skill/
│   ├── groq-inference-skill/
│   ├── gtm-pricing-skill/
│   ├── langgraph-agents-skill/
│   ├── planning-prompts-skill/
│   ├── research-skill/
│   ├── runpod-deployment-skill/
│   ├── sales-revenue-skill/
│   ├── supabase-sql-skill/
│   ├── trading-signals-skill/
│   ├── voice-ai-skill/
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
