#!/bin/bash
# Rebuild all skill zip files in dist/
# Run: ./scripts/rebuild-zips.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"
DIST_DIR="$REPO_DIR/dist"

echo "=== Rebuilding Skill Zips ==="
echo "Output: $DIST_DIR"
echo ""

mkdir -p "$DIST_DIR"

# Rebuild active skills
for skill in "$REPO_DIR"/active/*/; do
    name=$(basename "$skill")
    zip_file="$DIST_DIR/${name}.zip"
    rm -f "$zip_file"
    (cd "$REPO_DIR/active" && zip -rq "$zip_file" "$name/" -x "*.pyc" -x "*__pycache__*")
    size=$(ls -lh "$zip_file" | awk '{print $5}')
    echo "  ✓ $name.zip ($size)"
done

# Rebuild stable skills
for skill in "$REPO_DIR"/stable/*/; do
    name=$(basename "$skill")
    zip_file="$DIST_DIR/${name}.zip"
    rm -f "$zip_file"
    (cd "$REPO_DIR/stable" && zip -rq "$zip_file" "$name/" -x "*.pyc" -x "*__pycache__*")
    size=$(ls -lh "$zip_file" | awk '{print $5}')
    echo "  ✓ $name.zip ($size)"
done

echo ""
echo "✅ Rebuilt $(ls -1 "$DIST_DIR"/*.zip | wc -l | tr -d ' ') zips in $DIST_DIR"
