# Skills Library

A curated collection of 19 Claude Code skills for software development, business operations, and AI infrastructure.

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

### Core (3 skills)
| Skill | Description |
|-------|-------------|
| **project-context** | Track context across sessions |
| **workflow-enforcer** | Enforce workflow discipline |
| **workflow-orchestrator** | Full-day workflow orchestration with cost tracking |

## Project Structure

```
skills/
├── active/              # 28 skills in development
├── stable/              # 2 battle-tested skills
├── dist/                # Zip files for Claude Desktop
├── scripts/
│   ├── deploy.sh        # Deploy to ~/.claude/skills/
│   └── rebuild-zips.sh
├── templates/           # Skill starter templates
├── DEPENDENCY_GRAPH.md  # Visual skill relationships
├── SKILLS_INDEX.md      # Detailed skill documentation
└── README.md            # This file
```

See [DEPENDENCY_GRAPH.md](./DEPENDENCY_GRAPH.md) for how skills connect and common workflow chains.

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

## Worktree Workflow

This library uses git worktrees for parallel development. The `worktree-manager` skill automates this.

### Quick Commands

```bash
# Create worktree with agent
/worktree create feature/auth

# Check status
/worktree status

# Cleanup merged
/worktree cleanup feature/auth
```

### How It Works

1. Worktrees stored at `~/tmp/worktrees/[project]/[branch-slug]`
2. Ports allocated from pool (8100-8199)
3. Global registry at `~/.claude/worktree-registry.json`
4. Each worktree gets isolated Claude agent

### Constraints

- **Max 3 concurrent** on M1 8GB
- Weekly cleanup recommended
- Run `wt-audit` before creating new worktrees

See `active/worktree-manager-skill/` for full documentation.

## Principles

- **NO OpenAI** - Uses Claude, GROQ, Deepgram, Cartesia
- **Progressive loading** - Minimize context usage
- **Battle-tested patterns** - Extracted from production projects

## License

MIT
