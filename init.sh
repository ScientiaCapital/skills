#!/usr/bin/env bash
set -euo pipefail

echo "==> skills init"

echo "==> Deploying skills to ~/.claude/skills/"
bash scripts/deploy.sh

echo "==> Rebuilding dist/*.zip for Claude Desktop"
bash scripts/rebuild-zips.sh

echo "==> Done. Skills deployed to ~/.claude/skills/"
echo "==> See SKILLS_INDEX.md for the complete skill catalog."
