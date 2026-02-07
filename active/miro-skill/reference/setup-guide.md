# Miro Setup Guide

## Prerequisites

- Miro account (free or paid)
- Claude Code CLI installed
- Internet access for MCP authentication

## MCP Server Installation

### Add the Miro MCP Server
```bash
claude mcp add --transport http miro https://mcp.miro.com
```

### Authenticate
In a Claude Code session:
```
/mcp auth
```

Follow the browser OAuth flow to grant Claude access to your Miro workspace.

### Verify Connection
```
/mcp status
```
Should show `miro` as connected.

## AI Plugin (Optional)

The `miroapp/miro-ai` plugin adds higher-level capabilities on top of the MCP tools.

### Install
1. Go to Miro Marketplace
2. Search for "miro-ai" by miroapp
3. Click Install
4. Authorize for your workspace

### Plugin Capabilities
| Capability | Description |
|-----------|-------------|
| Browse | Navigate and read board contents |
| Diagram | Create diagrams from text descriptions |
| Doc | Generate documentation from board content |
| Table | Create structured tables from data |
| Summarize | Condense board sections into summaries |

## Workspace Configuration

### Board Organization
Recommended folder structure in Miro:
```
My Boards/
├── Strategy/          # GTM, pricing, competitive
├── Architecture/      # System design, data flow
├── Sprints/          # Sprint boards, retrospectives
└── Research/         # Market research, user interviews
```

### Team Settings
- Enable "Anyone with link can view" for shared boards
- Set default board permissions to "Can edit" for team members
- Enable board templates for recurring board types

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Not authenticated" | Re-run `/mcp auth` |
| "Board not found" | Check board ID with `get_boards` |
| "Permission denied" | Verify board sharing settings |
| MCP server not listed | Re-run `claude mcp add` command |
| Stale OAuth token | Remove and re-add MCP server |
