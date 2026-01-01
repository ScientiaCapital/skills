# Troubleshooting Reference

## Common Issues

### "Worktree already exists"

```bash
git worktree list
git worktree remove <path> --force
git worktree prune
```

### "Branch already exists"

```bash
# Use existing branch (omit -b flag)
git worktree add <path> <branch>
```

### "Port already in use"

```bash
# Check what's using the port
lsof -i :<port>

# Kill if stale process
lsof -ti:<port> | xargs kill -9

# Or pick different port from pool
```

### Registry Out of Sync

```bash
# Compare registry to actual worktrees
cat ~/.claude/worktree-registry.json | jq '.worktrees[].worktreePath'
find ~/tmp/worktrees -maxdepth 2 -type d

# Remove orphaned entries manually
# See registry-operations.md
```

### Validation Failed

1. Check stderr/logs for error message
2. Common issues:
   - Missing env vars
   - Database not running
   - Wrong port
3. Report to user with details
4. Continue with other worktrees
5. User can fix and re-validate manually

## Package Manager Detection

Detect by checking for lockfiles in priority order:

| File | Package Manager | Install Command |
|------|-----------------|-----------------|
| `bun.lockb` | bun | `bun install` |
| `pnpm-lock.yaml` | pnpm | `pnpm install` |
| `yarn.lock` | yarn | `yarn install` |
| `package-lock.json` | npm | `npm install` |
| `uv.lock` | uv | `uv sync` |
| `pyproject.toml` (no uv.lock) | uv | `uv sync` |
| `requirements.txt` | pip | `pip install -r requirements.txt` |
| `go.mod` | go | `go mod download` |
| `Cargo.toml` | cargo | `cargo build` |

### Detection Script

```bash
cd $WORKTREE_PATH
if [ -f "bun.lockb" ]; then bun install
elif [ -f "pnpm-lock.yaml" ]; then pnpm install
elif [ -f "yarn.lock" ]; then yarn install
elif [ -f "package-lock.json" ]; then npm install
elif [ -f "uv.lock" ]; then uv sync
elif [ -f "pyproject.toml" ]; then uv sync
elif [ -f "requirements.txt" ]; then pip install -r requirements.txt
elif [ -f "go.mod" ]; then go mod download
elif [ -f "Cargo.toml" ]; then cargo build
fi
```

## Dev Server Detection

Look for dev commands in this order:

1. **docker-compose.yml / compose.yml**: `docker-compose up -d` or `docker compose up -d`
2. **package.json scripts**: Look for `dev`, `start:dev`, `serve`
3. **Python with uvicorn**: `uv run uvicorn app.main:app --port $PORT`
4. **Python with Flask**: `flask run --port $PORT`
5. **Go**: `go run .`

**Port injection**: Most servers accept `PORT` env var or `--port` flag
