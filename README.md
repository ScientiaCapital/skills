# Skills Library

47 production-ready Claude Code skills. AI-native engineering, GTM, sales automation, and trading.

## Quick Start

### Claude Desktop
1. Download `.zip` from `dist/`
2. Settings → Skills → Drag to upload

### Claude Code CLI
```bash
./scripts/deploy.sh
```

## Skills (47)

### Core (5)
| Skill | What It Does |
|-------|-------------|
| **workflow-orchestrator** | Dual-team workflow + cost tracking + agent orchestration |
| **cost-metering** | API cost tracking, budget alerts, model routing |
| **portfolio-artifact** | Engineering metrics capture, report templates |
| **project-context** | Session continuity across conversations |
| **workflow-enforcer** | Automatic agent routing + discipline enforcement |

### Dev Tools (15)
| Skill | What It Does |
|-------|-------------|
| **extension-authoring** | Author skills, hooks, slash commands, subagents |
| **debug-like-expert** | Systematic debugging with hypothesis testing |
| **planning-prompts** | Project planning and meta-prompt creation |
| **worktree-manager** | Git worktree automation for parallel dev |
| **agent-teams** | Orchestrate parallel Claude Code sessions |
| **subagent-teams** | In-session Task tool subagent orchestration |
| **agent-capability-matrix** | Task→agent mapping, 70+ agents cataloged |
| **git-workflow** | Conventional commits, PR templates, merge strategies |
| **testing** | TDD, test pyramid, mocking, coverage strategies |
| **api-design** | REST/GraphQL API design patterns |
| **security** | Auth, secrets, OWASP, RLS, security audit |
| **api-testing** | API testing with Postman and Bruno |
| **docker-compose** | Local dev environments with Docker Compose |
| **frontend-ui** | Enterprise SaaS frontend: Tailwind v4, shadcn/ui, Next.js |
| **heal-skill** | Auto-diagnose and repair broken skills |

### Infrastructure (8)
| Skill | What It Does |
|-------|-------------|
| **langgraph-agents** | Multi-agent LangGraph systems |
| **groq-inference** | Ultra-fast GROQ API: chat, vision, audio, tools |
| **openrouter** | Chinese LLMs (DeepSeek, Qwen) via OpenRouter |
| **voice-ai** | Production voice agents: Deepgram + Cartesia + Twilio |
| **unsloth-training** | Fine-tune LLMs with GRPO/SFT |
| **runpod-deployment** | GPU serverless deployment patterns |
| **supabase-sql** | Clean SQL migrations for Supabase |
| **stripe-stack** | Stripe payments + webhooks for Next.js |

### Business — GTM & Sales (10)
| Skill | What It Does |
|-------|-------------|
| **gtm-pricing** | GTM strategy, pricing, opportunity evaluation |
| **research** | Market and technical research |
| **sales-revenue** | Sales outreach, discovery, RevOps |
| **crm-integration** | Close CRM, HubSpot, Salesforce patterns |
| **hubspot-revops** | HubSpot SQL analytics, lead scoring, pipeline forecasting |
| **content-marketing** | B2B content strategy |
| **data-analysis** | Executive data analysis and dashboards |
| **miro** | Miro boards for strategy, architecture, sprints |
| **prospect-research-to-cadence** | Apollo research → outreach → sequence automation |
| **phone-verification-waterfall** | Golden Rules filtering + Clay waterfall enrichment |

### Business — Sales Workflow Automation (4)
| Skill | What It Does |
|-------|-------------|
| **meddic-call-prep-auto** | Auto-generate MEDDIC call prep from CRM + Apollo data |
| **deal-momentum-analyzer** | Score deal velocity, predict close vs stall |
| **portfolio-deal-linker** | Link engineering output to revenue impact |
| **trading-alert-scheduler** | Daily pre-market digest with regime detection |

### Business — Trading & Brokerage (2)
| Skill | What It Does |
|-------|-------------|
| **trading-signals** | 5 TA methodologies, 25+ options strategies, regime detection |
| **ibkr-api** | Interactive Brokers API: portfolio, trades, multi-account |

### Strategy (3)
| Skill | What It Does |
|-------|-------------|
| **business-model-canvas** | 9-block business model design |
| **blue-ocean-strategy** | Blue ocean market differentiation |
| **jobs-to-be-done** | JTBD + ODI analysis for sales discovery and strategy |

## Project Structure

```
skills/
├── active/              # 45 trigger-activated skills
├── stable/              # 2 always-loaded core skills
├── dist/                # 47 zip files for Claude Desktop
├── scripts/
│   ├── deploy.sh           # Deploy to ~/.claude/skills/
│   ├── rebuild-zips.sh     # Rebuild dist/*.zip
│   ├── test-skills.sh      # Integration tests (323 checks)
│   ├── log-skill-usage.sh  # PostToolUse hook target
│   ├── skill-analytics-report.sh  # Usage reporting
│   └── hooks/              # SessionStart + workflow hooks
├── templates/           # Skill starter templates
├── .claude/             # Project config, observers, test matrix
├── SKILLS_INDEX.md      # Detailed skill documentation
├── DEPENDENCY_GRAPH.md  # Visual skill relationships
├── PLANNING.md          # Current sprint
├── BACKLOG.md           # Future work
├── ARCHIVE.md           # Completed sprints
└── README.md            # This file
```

## Architecture

Skills use **progressive disclosure** to minimize token usage:

1. **Level 1:** YAML frontmatter — loads at startup for activation matching
2. **Level 2:** SKILL.md content — loads when skill triggers
3. **Level 3:** reference/*.md — loads only when deep-dive needed

## Scripts

```bash
# Deploy all skills to Claude Code
./scripts/deploy.sh

# Rebuild all zip files after changes
./scripts/rebuild-zips.sh

# Run integration tests (323 checks across 46 skills)
./scripts/test-skills.sh [--verbose] [--skill <name>]

# View skill usage analytics
./scripts/skill-analytics-report.sh [--days N] [--all]
```

## MCP Integrations

Skills connect to these MCP servers for live data:

| Server | Tools | Used By |
|--------|-------|---------|
| **Epiphan CRM** | 14 tools (HubSpot, CRM, analytics) | crm-integration, hubspot-revops |
| **Apollo.io** | 15 tools (enrich, search, sequences) | prospect-research, phone-verification |
| **Clay** | 13 tools (waterfall enrichment) | phone-verification, crm-integration |
| **Gmail** | 7 tools (drafts, search, read) | prospect-research, meddic-call-prep |
| **Google Calendar** | 9 tools (events, free time) | meddic-call-prep, deal-momentum |
| **IBKR** | 11 tools (portfolio, trades, margin) | ibkr-api, trading-alert-scheduler |

## Principles

- **AI-native** — Built for Claude, not ported from elsewhere
- **Progressive loading** — Lean context, maximum capability
- **Battle-tested** — Extracted from production BDR workflows

## License

MIT
