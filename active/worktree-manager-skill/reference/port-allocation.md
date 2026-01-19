# Port Allocation Reference

## Port Pool Rules

- **Global pool**: 8100-8199 (100 ports total)
- **Per worktree**: 2 ports allocated (for API + frontend patterns)
- **Globally unique**: Ports are tracked globally to avoid conflicts across projects
- **Check before use**: Always verify port isn't in use by system: `lsof -i :<port>`
- **Max worktrees**: With 100-port pool and 2 ports each, max ~50 concurrent worktrees

## Manual Port Allocation

### Step 1: Get Currently Allocated Ports

```bash
ALLOCATED=$(cat ~/.claude/worktree-registry.json | jq -r '.portPool.allocated[]' | sort -n)
echo "Currently allocated: $ALLOCATED"
```

### Step 2: Find First Available Port

```bash
for PORT in $(seq 8100 8199); do
  # Check if in registry
  if ! echo "$ALLOCATED" | grep -q "^${PORT}$"; then
    # Check if in use by system
    if ! lsof -i :"$PORT" &>/dev/null; then
      echo "Available: $PORT"
      break
    fi
  fi
done
```

### Step 3: Add to Allocated Pool

```bash
TMP=$(mktemp)
jq '.portPool.allocated += [8100] | .portPool.allocated |= unique | .portPool.allocated |= sort_by(.)' \
  ~/.claude/worktree-registry.json > "$TMP" && mv "$TMP" ~/.claude/worktree-registry.json
```

## Using the allocate-ports.sh Script

```bash
# Allocate 2 ports
~/.claude/skills/worktree-manager/scripts/allocate-ports.sh 2
# Returns: 8100 8101 (space-separated)

# The script automatically updates the registry
```

## Port Conflict Resolution

### Check What's Using a Port

```bash
lsof -i :8100
# Shows process using port 8100
```

### Kill Process on Port

```bash
lsof -ti:8100 | xargs kill -9
```

### Find System Ports to Avoid

```bash
# Common ports to avoid (usually in use)
# 3000 - React dev server default
# 5432 - PostgreSQL
# 5173 - Vite dev server default
# 8080 - Common web server port

# Our pool (8100-8199) avoids these conflicts
```
