# Coding Rules — skills

## Stack
Markdown skill files, bash scripts; no runtime dependencies

## Rules
- Each skill lives in active/ or stable/ as its own directory with SKILL.md
- SKILL.md must define: trigger phrase, purpose, required context, output format
- Skill names use kebab-case with -skill suffix (e.g. sales-outreach-skill)
- Deploy script: scripts/deploy.sh copies to ~/.claude/skills/
- Rebuild zips script: scripts/rebuild-zips.sh for Claude Desktop dist/
- Update SKILLS_INDEX.md and DEPENDENCY_GRAPH.md when adding a new skill
- Keep context lean — skills must be self-contained and load quickly
