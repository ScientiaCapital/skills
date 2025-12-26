#!/bin/bash
# Deploy all skills to ~/.claude/skills/
# Usage: ./scripts/deploy.sh [--symlink]
# Options:
#   --symlink    Create symbolic links instead of copying (for team sharing)

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"
DEPLOY_DIR="$HOME/.claude/skills"
USE_SYMLINKS=false

# Parse arguments
if [[ "$1" == "--symlink" ]]; then
    USE_SYMLINKS=true
fi

echo "=== Skills Deployment ==="
echo "Source: $REPO_DIR"
echo "Target: $DEPLOY_DIR"
if $USE_SYMLINKS; then
    echo "Mode: Symlink (team sharing)"
else
    echo "Mode: Copy (local)"
fi
echo ""

# Create target if needed
mkdir -p "$DEPLOY_DIR"

# Deploy active skills
echo "Deploying active skills..."
for skill in "$REPO_DIR"/active/*/; do
    name=$(basename "$skill")
    target="$DEPLOY_DIR/$name"
    
    # Remove existing deployment
    rm -rf "$target"
    
    if $USE_SYMLINKS; then
        # Create symlink
        ln -s "$skill" "$target"
        echo "  ✓ $name (symlinked)"
    else
        # Copy directory
        cp -r "$skill" "$target"
        echo "  ✓ $name (copied)"
    fi
done

# Deploy stable skills
echo "Deploying stable skills..."
for skill in "$REPO_DIR"/stable/*/; do
    name=$(basename "$skill")
    target="$DEPLOY_DIR/$name"
    
    # Remove existing deployment
    rm -rf "$target"
    
    if $USE_SYMLINKS; then
        # Create symlink
        ln -s "$skill" "$target"
        echo "  ✓ $name (symlinked)"
    else
        # Copy directory
        cp -r "$skill" "$target"
        echo "  ✓ $name (copied)"
    fi
done

# Create a README if using symlinks
if $USE_SYMLINKS; then
    cat > "$DEPLOY_DIR/README.md" << EOF
# Symlinked Skills

These skills are symlinked from: $REPO_DIR

To update skills:
1. Pull latest changes in the source repository
2. Changes will automatically reflect here

To deploy as copies instead:
\`\`\`bash
cd $REPO_DIR
./scripts/deploy.sh
\`\`\`
EOF
    echo ""
    echo "📝 Created README.md with symlink information"
fi

echo ""
echo "✅ Deployed $(ls -1 "$DEPLOY_DIR" | grep -v README | wc -l | tr -d ' ') skills to $DEPLOY_DIR"
