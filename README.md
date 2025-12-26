# Skills Library

A curated collection of 17 Claude Code skills for software development, business operations, and AI infrastructure.

## Quick Start

### Claude Desktop
1. Download `.zip` files from `dist/` folder
2. Open Claude Desktop -> Settings -> Skills
3. Drag and drop to upload

### Claude Code (Terminal)
```bash
# Deploy all skills to ~/.claude/skills/
./scripts/deploy.sh
```

## Skills by Category

### Dev Tools (4 skills)
| Skill | Description |
|-------|-------------|
| **extension-authoring** | Author skills, hooks, slash commands, subagents |
| **debug-like-expert** | Systematic debugging with hypothesis testing |
| **planning-prompts** | Project planning and meta-prompt creation |
| **worktree-manager** | Git worktree automation for parallel dev |

### Infrastructure (5 skills)
| Skill | Description |
|-------|-------------|
| **runpod-deployment** | GPU serverless deployment patterns |
| **voice-ai** | Production voice agents (Deepgram, Cartesia, Twilio) |
| **groq-inference** | Ultra-fast GROQ API inference |
| **langgraph-agents** | Multi-agent LangGraph systems |
| **supabase-sql** | Clean SQL migrations for Supabase |

### Business (6 skills)
| Skill | Description |
|-------|-------------|
| **gtm-pricing** | GTM strategy, pricing, opportunity evaluation |
| **research** | Market and technical research |
| **sales-revenue** | Sales outreach, discovery, RevOps |
| **content-marketing** | B2B content strategy |
| **data-analysis** | Executive data analysis and dashboards |
| **trading-signals** | Technical analysis for trading systems |

### Core (2 skills)
| Skill | Description |
|-------|-------------|
| **project-context** | Track context across sessions |
| **workflow-enforcer** | Enforce workflow discipline |

## Project Structure

```
skills/
├── active/           # 15 skills in development
├── stable/           # 2 battle-tested skills
├── dist/             # Zip files for Claude Desktop
├── scripts/
│   ├── deploy.sh     # Deploy to ~/.claude/skills/
│   └── rebuild-zips.sh
├── templates/        # Skill starter templates
├── SKILLS_INDEX.md   # Detailed skill documentation
└── README.md         # This file
```

## Scripts

```bash
# Deploy all skills to Claude Code
./scripts/deploy.sh

# Rebuild all zip files after changes
./scripts/rebuild-zips.sh
```

## Skill Architecture

Skills use **progressive disclosure** to minimize token usage:

1. **Level 1:** YAML frontmatter (loads at startup)
2. **Level 2:** SKILL.md content (loads when activated)
3. **Level 3:** reference/*.md files (loads on demand)

## Creating New Skills

```bash
# Copy the template
cp templates/SKILL_TEMPLATE.md active/my-new-skill/SKILL.md

# Add reference docs
mkdir active/my-new-skill/reference/
```

See [SKILLS_INDEX.md](./SKILLS_INDEX.md) for detailed documentation.

## Principles

- **NO OpenAI** - Uses Claude, GROQ, Deepgram, Cartesia
- **Progressive loading** - Minimize context usage
- **Battle-tested patterns** - Extracted from production projects

## License

MIT
