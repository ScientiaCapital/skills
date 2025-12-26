#!/bin/bash
# Deploy all skills to ~/.claude/skills/
# Run: ./scripts/deploy.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"
DEPLOY_DIR="$HOME/.claude/skills"

echo "=== Skills Deployment ==="
echo "Source: $REPO_DIR"
echo "Target: $DEPLOY_DIR"
echo ""

# Create target if needed
mkdir -p "$DEPLOY_DIR"

# Deploy active skills
echo "Deploying active skills..."
for skill in "$REPO_DIR"/active/*/; do
    name=$(basename "$skill")
    rm -rf "$DEPLOY_DIR/$name"
    cp -r "$skill" "$DEPLOY_DIR/"
    echo "  ✓ $name"
done

# Deploy stable skills
echo "Deploying stable skills..."
for skill in "$REPO_DIR"/stable/*/; do
    name=$(basename "$skill")
    rm -rf "$DEPLOY_DIR/$name"
    cp -r "$skill" "$DEPLOY_DIR/"
    echo "  ✓ $name"
done

echo ""
echo "✅ Deployed $(ls -1 "$DEPLOY_DIR" | grep -v README | wc -l | tr -d ' ') skills to $DEPLOY_DIR"
