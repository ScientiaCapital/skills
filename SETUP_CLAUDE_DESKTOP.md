# Setup Instructions for Claude Desktop

Run this command to open your Claude Desktop config:

```bash
open ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

Then add `"/Users/tmk/Desktop/tk_projects/skills"` to your filesystem server's `args` array.

It should look something like this:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@anthropic-ai/mcp-filesystem",
        "/Users/tmk/Desktop/tk_projects",
        "/Users/tmk/Desktop/tk_projects/skills"
      ]
    }
    // ... your other servers
  }
}
```

**Note:** If you already have `/Users/tmk/Desktop/tk_projects` in there, you're good - the skills folder is inside it and already accessible!

## After Editing

1. Save the file
2. Quit Claude Desktop completely (Cmd+Q)
3. Reopen Claude Desktop

## Test It Works

In Claude Desktop, ask:
> "Read the file at ~/Desktop/tk_projects/skills/SKILLS_INDEX.md"

If it works, you're all set!
