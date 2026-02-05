---
name: "docker-compose-skill"
description: "Local dev environments with Docker Compose - multi-service setups, databases, hot reload, debugging. Use when: docker compose, local dev, postgres container, redis local, dev environment."
---

# Docker Compose Skill

Local development environments using Docker Compose for multi-service setups.

## Quick Start

### Common Services

| Service | Image | Default Port |
|---------|-------|--------------|
| PostgreSQL | `postgres:16-alpine` | 5432 |
| Redis | `redis:7-alpine` | 6379 |
| MongoDB | `mongo:7` | 27017 |
| MySQL | `mysql:8` | 3306 |

### Basic compose.yml

```yaml
services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: ${DB_USER:-app}
      POSTGRES_PASSWORD: ${DB_PASSWORD:-secret}
      POSTGRES_DB: ${DB_NAME:-app_dev}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER:-app}"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

## Essential Commands

```bash
# Start services (detached)
docker compose up -d

# Start with logs visible
docker compose up

# View logs
docker compose logs -f [service]

# Shell into container
docker compose exec db psql -U app

# Stop and remove containers
docker compose down

# Stop and remove volumes (full reset)
docker compose down -v

# Rebuild without cache
docker compose build --no-cache
```

## Environment Variables

Create `.env` file in project root:

```bash
# .env
DB_USER=app
DB_PASSWORD=secret
DB_NAME=myapp_dev
REDIS_URL=redis://localhost:6379
```

Reference in compose.yml:
```yaml
environment:
  POSTGRES_USER: ${DB_USER:-app}
```

## Health Checks

Always add health checks for service dependencies:

```yaml
services:
  db:
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER:-app}"]
      interval: 5s
      timeout: 5s
      retries: 5

  app:
    depends_on:
      db:
        condition: service_healthy
```

## Hot Reload Setup

Mount source code for development:

```yaml
services:
  app:
    build: .
    volumes:
      - .:/app                    # Source code
      - /app/node_modules         # Preserve node_modules
    environment:
      - NODE_ENV=development
```

## Profiles for Optional Services

```yaml
services:
  mailhog:
    image: mailhog/mailhog
    profiles: ["mail"]
    ports:
      - "8025:8025"

# Start with: docker compose --profile mail up
```

## Reference Files

- `reference/compose-patterns.md` - Common compose file patterns
- `reference/services.md` - Database, cache, queue service configs
- `reference/networking.md` - Ports, networks, volumes
- `reference/dev-workflow.md` - Development workflow commands
