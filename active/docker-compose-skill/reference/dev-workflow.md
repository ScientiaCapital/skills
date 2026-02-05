# Development Workflow

## Starting Services

```bash
# Start all services in background
docker compose up -d

# Start with logs visible (foreground)
docker compose up

# Start specific services
docker compose up -d db redis

# Start with rebuild
docker compose up -d --build

# Start with fresh containers
docker compose up -d --force-recreate
```

## Viewing Logs

```bash
# All services
docker compose logs

# Follow logs (like tail -f)
docker compose logs -f

# Specific service
docker compose logs -f app

# Last 100 lines
docker compose logs --tail 100 app

# With timestamps
docker compose logs -t app
```

## Executing Commands

```bash
# Run command in running container
docker compose exec db psql -U app

# Run in new container (for one-off tasks)
docker compose run --rm app npm test

# Interactive shell
docker compose exec app sh
docker compose exec app bash

# As root user
docker compose exec -u root app sh
```

## Database Operations

### PostgreSQL
```bash
# Connect to psql
docker compose exec db psql -U app -d app_dev

# Run SQL file
docker compose exec -T db psql -U app -d app_dev < migrations.sql

# Dump database
docker compose exec -T db pg_dump -U app app_dev > backup.sql

# Restore database
docker compose exec -T db psql -U app app_dev < backup.sql
```

### MySQL
```bash
# Connect to mysql
docker compose exec db mysql -u app -psecret app_dev

# Dump database
docker compose exec db mysqldump -u app -psecret app_dev > backup.sql
```

### Redis
```bash
# Redis CLI
docker compose exec redis redis-cli

# Flush all data
docker compose exec redis redis-cli FLUSHALL
```

## Stopping Services

```bash
# Stop containers (preserves data)
docker compose stop

# Stop and remove containers (preserves volumes)
docker compose down

# Stop, remove containers AND volumes (full reset)
docker compose down -v

# Remove everything including images
docker compose down -v --rmi all
```

## Rebuilding

```bash
# Rebuild specific service
docker compose build app

# Rebuild without cache
docker compose build --no-cache app

# Rebuild and restart
docker compose up -d --build app

# Pull latest images
docker compose pull
```

## Status & Debugging

```bash
# List running containers
docker compose ps

# List all containers (including stopped)
docker compose ps -a

# Show resource usage
docker compose top

# Inspect container
docker compose exec app env

# Check service config
docker compose config

# View events
docker compose events
```

## Common Patterns

### Fresh Start
```bash
docker compose down -v && docker compose up -d
```

### Rebuild One Service
```bash
docker compose up -d --build --force-recreate app
```

### Reset Database
```bash
docker compose down -v postgres_data
docker compose up -d db
```

### Watch Mode (compose v2.22+)
```bash
# Auto-rebuild on file changes
docker compose watch
```

### Run Migrations
```bash
docker compose exec app npm run migrate
# or
docker compose run --rm app npm run migrate
```

## Troubleshooting

### Container won't start
```bash
# Check logs
docker compose logs app

# Check config
docker compose config

# Try running interactively
docker compose run --rm app sh
```

### Port already in use
```bash
# Find what's using the port
lsof -i :5432

# Use different host port in compose.yml
ports:
  - "5433:5432"
```

### Volume permission issues
```bash
# Fix ownership
docker compose exec -u root app chown -R node:node /app

# Or in Dockerfile
RUN chown -R node:node /app
USER node
```

### Network issues between services
```bash
# Check network
docker network ls
docker network inspect skills_default

# Verify DNS
docker compose exec app ping db
```

### Out of disk space
```bash
# Clean up
docker system prune -a --volumes
```

## Useful Aliases

Add to `~/.bashrc` or `~/.zshrc`:

```bash
alias dc='docker compose'
alias dcu='docker compose up -d'
alias dcd='docker compose down'
alias dcl='docker compose logs -f'
alias dce='docker compose exec'
alias dcr='docker compose restart'
alias dcps='docker compose ps'
```
