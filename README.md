# Skills Library

39 production-ready Claude Code skills. AI-native engineering, GTM, and business ops.

## Quick Start

### Claude Desktop
1. Download `.zip` from `dist/`
2. Settings → Skills → Drag to upload

### Claude Code CLI
```bash
./scripts/deploy.sh
```

## Skills (39)

### Core (5)
| Skill | What It Does |
|-------|-------------|
| **workflow-orchestrator** | Full-day workflow + cost tracking + 70-agent catalog |
| **cost-metering** | API cost tracking, budget alerts, optimization |
| **portfolio-artifact** | Engineering metrics capture, report templates |
| **project-context** | Session continuity across conversations |
| **workflow-enforcer-skill** | Automatic agent routing + discipline enforcement |

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

### Business (9)
| Skill | What It Does |
|-------|-------------|
| **gtm-pricing** | GTM strategy, pricing, opportunity evaluation |
| **research** | Market and technical research |
| **sales-revenue** | Sales outreach, discovery, RevOps |
| **crm-integration** | Close CRM, HubSpot, Salesforce |
| **hubspot-revops** | HubSpot SQL analytics, lead scoring, pipeline forecasting |
| **content-marketing** | B2B content strategy |
| **data-analysis** | Executive data analysis and dashboards |
| **trading-signals** | Technical analysis for trading systems |
| **miro** | Miro boards for strategy, architecture, sprints |

### Strategy (2)
| Skill | What It Does |
|-------|-------------|
| **business-model-canvas** | 9-block business model design |
| **blue-ocean-strategy** | Blue ocean market differentiation |

## Project Structure

```
skills/
├── active/              # 37 trigger-activated skills
├── stable/              # 2 always-loaded core skills
├── dist/                # Zip files for Claude Desktop
├── scripts/
│   ├── deploy.sh        # Deploy to ~/.claude/skills/
│   └── rebuild-zips.sh  # Rebuild dist/*.zip
├── templates/           # Skill starter templates
├── .claude/             # Project config + test matrix
├── SKILLS_INDEX.md      # Detailed skill documentation
├── DEPENDENCY_GRAPH.md  # Visual skill relationships
├── PLANNING.md          # Current sprint
├── BACKLOG.md           # Future work
├── ARCHIVE.md           # Completed sprints
└── README.md            # This file
```

## Architecture

Skills use **progressive disclosure** to minimize token usage:

1. **L0:** YAML frontmatter — loads at startup for activation matching
2. **L1:** SKILL.md content — loads when skill triggers
3. **L2:** reference/*.md — loads only when deep-dive needed

## Scripts

```bash
# Deploy all skills to Claude Code
./scripts/deploy.sh

# Rebuild all zip files after changes
./scripts/rebuild-zips.sh

# Run integration tests (8 checks per skill)
./scripts/test-skills.sh [--verbose] [--skill <name>]

# View skill usage analytics
./scripts/skill-analytics-report.sh [--days N] [--all]
```

## Principles

- **AI-native** — Built for Claude, not ported from elsewhere
- **Progressive loading** — Lean context, maximum capability
- **Battle-tested** — Extracted from production projects

## License

MIT
