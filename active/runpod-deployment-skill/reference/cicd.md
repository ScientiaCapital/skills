# CI/CD Integration

## M1 Mac Workaround (Apple Silicon)

**Problem:** M1/M2 Macs use ARM architecture. RunPod GPUs require x86/amd64 Docker images. You cannot build locally.

**Solution:** Use GitHub Actions to build and push images.

### Workflow

```
M1 Mac                    GitHub Actions              RunPod
   │                            │                        │
   ├──git push──────────────────►                        │
   │                            │                        │
   │                      builds x86 image               │
   │                            │                        │
   │                            ├───docker push──────────►
   │                            │                        │
   │                            ├───runpodctl deploy─────►
   │                            │                        │
   ◄────────────────────────────┤                        │
        deployment complete                              │
```

### Quick Deploy from M1

```bash
# Just push - GitHub handles the rest
git add .
git commit -m "feat: update model handler"
git push origin main

# Watch deployment in GitHub Actions tab
```

**Never run `docker build` locally for RunPod on M1.**

---

## GitHub Actions Deployment

### Full Workflow (Docker Build + Deploy)

```yaml
name: Deploy to RunPod
on:
  push:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest  # x86 runner - builds compatible images
    permissions:
      contents: read
      packages: write

    steps:
      - uses: actions/checkout@v4

      - name: Log in to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and push Docker image (x86)
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:latest
          platforms: linux/amd64  # Force x86 for RunPod GPUs

      - name: Install runpodctl
        run: |
          wget -qO- https://github.com/runpod/runpodctl/releases/latest/download/runpodctl-linux-amd64 -O runpodctl
          chmod +x runpodctl
          sudo mv runpodctl /usr/local/bin/

      - name: Deploy to RunPod
        env:
          RUNPOD_API_KEY: ${{ secrets.RUNPOD_API_KEY }}
        run: |
          runpodctl project deploy \
            --name ${{ github.event.repository.name }} \
            --image ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:latest \
            --gpu-type "NVIDIA RTX A4000"
```

### Simple Workflow (No Docker)

```yaml
name: Deploy to RunPod
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install runpodctl
        run: |
          wget -qO- https://github.com/runpod/runpodctl/releases/latest/download/runpodctl-linux-amd64 -O runpodctl
          chmod +x runpodctl
          sudo mv runpodctl /usr/local/bin/

      - name: Deploy
        env:
          RUNPOD_API_KEY: ${{ secrets.RUNPOD_API_KEY }}
        run: |
          runpodctl project deploy \
            --name ${{ github.event.repository.name }} \
            --gpu-type "NVIDIA RTX A4000"
```

## Deploy Script

```bash
#!/bin/bash
# deploy_to_runpod.sh

set -e

PROJECT_NAME=${1:-"my-project"}
GPU_TYPE=${2:-"NVIDIA RTX A4000"}

echo "Deploying $PROJECT_NAME to RunPod..."

runpodctl project deploy \
  --name "$PROJECT_NAME" \
  --gpu-type "$GPU_TYPE" \
  --min-workers 0 \
  --max-workers 3 \
  --idle-timeout 30

echo "Deployment complete!"
```

## MCP Server Integration

### Claude Desktop Config

```json
{
  "mcpServers": {
    "runpod": {
      "command": "npx",
      "args": ["-y", "@runpod/mcp-server"],
      "env": {
        "RUNPOD_API_KEY": "your-api-key"
      }
    }
  }
}
```

### Natural Language Control

```
"Create a RunPod serverless endpoint for embeddings"
"Deploy my model with GPU A4000 and 8GB RAM"
"Scale the endpoint to handle 1000 requests per minute"
"Show me current GPU usage and costs"
```

## Environment Setup

### Required Secrets (GitHub)

- `RUNPOD_API_KEY` - Your RunPod API key

### Local Development

```bash
export RUNPOD_API_KEY="your-api-key"
pip install runpod
```

## Deployment Checklist

- [ ] RunPod API key configured
- [ ] GPU type selected based on model size
- [ ] min_workers=0 for scale-to-zero
- [ ] idle_timeout set appropriately
- [ ] HF_TOKEN set for gated models
- [ ] Container disk sized for model
