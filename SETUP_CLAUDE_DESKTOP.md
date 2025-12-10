# Setup Instructions for Claude Desktop

Run this command to open your Claude Desktop config:

```bash
open ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

Then add `"/Users/tmkipper/Desktop/tk_projects/skills"` to your filesystem server's `args` array.

It should look something like this:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@anthropic-ai/mcp-filesystem",
        "/Users/tmkipper/Desktop/tk_projects",
        "/Users/tmkipper/Desktop/tk_projects/skills"
      ]
    }
    // ... your other servers
  }
}
```

**Note:** If you already have `/Users/tmkipper/Desktop/tk_projects` in there, you're good - the skills folder is inside it and already accessible!

## After Editing

1. Save the file
2. Quit Claude Desktop completely (Cmd+Q)
3. Reopen Claude Desktop

## Test It Works

In Claude Desktop, ask:
> "Read the file at ~/Desktop/tk_projects/skills/SKILLS_INDEX.md"

If it works, you're all set!

---

## Tonight's TODO

1. Unzip your .skill files into the matching folders:
   - `trading-signals-skill.skill` → `skills/active/trading-signals-skill/`
   - `sales-outreach-skill.skill` → `skills/active/sales-outreach-skill/`
   - `runpod-deployment-skill.skill` → `skills/active/runpod-deployment-skill/`

2. The unzip command:
   ```bash
   cd ~/Desktop/tk_projects/skills/active
   unzip ~/path/to/trading-signals-skill.skill -d trading-signals-skill/
   unzip ~/path/to/sales-outreach-skill.skill -d sales-outreach-skill/
   unzip ~/path/to/runpod-deployment-skill.skill -d runpod-deployment-skill/
   ```
