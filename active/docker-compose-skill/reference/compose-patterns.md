# Compose Patterns

## Basic Service Definition

```yaml
services:
  service-name:
    image: image:tag
    container_name: my-service  # Optional, auto-generated if omitted
    ports:
      - "host:container"
    environment:
      KEY: value
    volumes:
      - named_volume:/path
      - ./local:/container/path
```

## Environment Variable Handling

### Inline with defaults
```yaml
environment:
  DB_USER: ${DB_USER:-default_user}
  DB_PASS: ${DB_PASS:?Required variable}  # Fails if not set
```

### From .env file (automatic)
```bash
# .env (loaded automatically)
DB_USER=app
DB_PASS=secret
```

### From env_file
```yaml
services:
  app:
    env_file:
      - .env
      - .env.local  # Overrides .env
```

## Health Checks

### PostgreSQL
```yaml
healthcheck:
  test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER:-postgres}"]
  interval: 5s
  timeout: 5s
  retries: 5
```

### Redis
```yaml
healthcheck:
  test: ["CMD", "redis-cli", "ping"]
  interval: 5s
  timeout: 3s
  retries: 5
```

### MySQL
```yaml
healthcheck:
  test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
  interval: 5s
  timeout: 5s
  retries: 5
```

### HTTP Service
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
  interval: 10s
  timeout: 5s
  retries: 3
  start_period: 30s
```

## Depends On with Conditions

```yaml
services:
  app:
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
      migrations:
        condition: service_completed_successfully
```

## Profiles for Optional Services

```yaml
services:
  # Always starts
  db:
    image: postgres:16-alpine

  # Only with --profile debug
  adminer:
    image: adminer
    profiles: ["debug"]
    ports:
      - "8080:8080"

  # Only with --profile mail
  mailhog:
    image: mailhog/mailhog
    profiles: ["mail"]
```

Usage:
```bash
docker compose up                    # Only required services
docker compose --profile debug up    # Include debug tools
docker compose --profile mail --profile debug up  # Multiple profiles
```

## Multi-Stage Builds

```yaml
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      target: development  # Use specific stage
```

## Extending Services

### Using YAML anchors
```yaml
x-common: &common
  restart: unless-stopped
  logging:
    driver: json-file
    options:
      max-size: "10m"

services:
  app:
    <<: *common
    image: myapp
```

### Using extends (compose v2.20+)
```yaml
# compose.yml
services:
  app:
    extends:
      file: compose.base.yml
      service: base-app
```

## Resource Limits

```yaml
services:
  app:
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
```
