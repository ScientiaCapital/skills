# Tim's Skills Library

This folder contains reusable skill packages for Claude Desktop and Claude Code.

## How to Use This Folder

When working in this folder, Claude should:
1. Read SKILLS_INDEX.md first to see what's available
2. Only load the specific SKILL.md file(s) needed for the current task
3. Keep context lean - don't load all skills at once

## Folder Structure

```
skills/
├── CLAUDE.md               # You're reading this
├── README.md               # Quick start + skill catalog
├── SKILLS_INDEX.md         # Detailed skill documentation
├── DEPENDENCY_GRAPH.md     # Visual skill relationships
├── PLANNING.md             # Current sprint
├── BACKLOG.md              # Future work
├── ARCHIVE.md              # Completed sprints
├── active/                 # Trigger-activated skills
├── stable/                 # Always-loaded core skills
├── dist/                   # Zip files for Claude Desktop
├── scripts/
│   ├── deploy.sh           # Deploy to ~/.claude/skills/
│   └── rebuild-zips.sh     # Rebuild dist/*.zip
├── templates/              # Skill starter templates
└── .claude/
    └── SKILL_TEST_MATRIX.md  # Activation test results
```

## For Individual Projects

To use a skill in another project, either:

1. **Symlink** (recommended):
   ```bash
   ln -s ~/Desktop/tk_projects/skills/active/skill-name ./skills/
   ```

2. **Reference in project's CLAUDE.md**:
   ```markdown
   ## Skills
   - See `~/Desktop/tk_projects/skills/active/skill-name/SKILL.md`
   ```

3. **Copy the `.zip`** directly into project

## Available Skills

See SKILLS_INDEX.md for the complete list.
