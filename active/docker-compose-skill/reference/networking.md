# Networking

## Port Mapping

### Basic port mapping
```yaml
ports:
  - "8080:80"        # host:container
  - "5432:5432"      # Same port
  - "127.0.0.1:3000:3000"  # Bind to localhost only
```

### Port ranges
```yaml
ports:
  - "8000-8005:8000-8005"
```

### Dynamic host port
```yaml
ports:
  - "5432"  # Random host port -> container 5432
```

Check assigned port: `docker compose port service_name 5432`

## Custom Networks

### Default network
All services share a default network automatically:
```yaml
# Services can reach each other by service name
# app can connect to db via: postgres://db:5432
```

### Named networks
```yaml
services:
  app:
    networks:
      - frontend
      - backend

  db:
    networks:
      - backend

  nginx:
    networks:
      - frontend

networks:
  frontend:
  backend:
```

### External networks
```yaml
networks:
  shared:
    external: true
    name: my-external-network
```

## Volumes

### Named volumes (persistent)
```yaml
services:
  db:
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:  # Persists across restarts
```

### Bind mounts (development)
```yaml
services:
  app:
    volumes:
      - ./src:/app/src        # Source code
      - ./config:/app/config  # Config files
```

### Anonymous volumes (preserve node_modules)
```yaml
services:
  app:
    volumes:
      - .:/app                 # Mount everything
      - /app/node_modules      # But keep container's node_modules
```

### Read-only mounts
```yaml
volumes:
  - ./config:/app/config:ro
```

### Volume with driver options
```yaml
volumes:
  db_data:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /data/postgres
```

## Service Discovery

Services communicate using service names:

```yaml
services:
  app:
    environment:
      DATABASE_URL: postgresql://user:pass@db:5432/mydb
      REDIS_URL: redis://redis:6379
      #                    ↑ service name
```

### DNS aliases
```yaml
services:
  db:
    networks:
      backend:
        aliases:
          - database
          - postgres
```

## Exposing vs Publishing

```yaml
services:
  db:
    expose:
      - "5432"    # Only accessible to other containers
    ports:
      - "5432:5432"  # Accessible from host
```

## Host Network Mode

```yaml
services:
  app:
    network_mode: host  # Use host's network directly
```

Note: Ports configuration is ignored in host mode.

## Container Network Mode

```yaml
services:
  sidecar:
    network_mode: "service:app"  # Share network with app
```

## Common Port Conflicts

| Port | Common Users |
|------|-------------|
| 3000 | Node.js apps, Rails |
| 5432 | PostgreSQL |
| 6379 | Redis |
| 8080 | Various web servers |
| 80/443 | Nginx, Apache |

**Solution:** Use different host ports:
```yaml
ports:
  - "5433:5432"  # Use 5433 on host
```
