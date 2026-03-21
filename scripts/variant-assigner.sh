#!/bin/bash
# Deterministic A/B Variant Assigner
# Part of P12: Autoresearch Self-Improving Skills Framework
# Usage: ./scripts/variant-assigner.sh <skill-name> [session-id]
# Returns: variant name (e.g., "control" or "concise")
# If no session-id provided, uses today's date

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"

SKILL_NAME="${1:-}"
SESSION_ID="${2:-$(date +%Y-%m-%d)}"

if [ -z "$SKILL_NAME" ]; then
    echo "Usage: $0 <skill-name> [session-id]" >&2
    exit 1
fi

# Find config.json
CONFIG=""
for dir in "$REPO_DIR/active/$SKILL_NAME" "$REPO_DIR/stable/$SKILL_NAME"; do
    [ -f "$dir/config.json" ] && CONFIG="$dir/config.json" && break
done

if [ -z "$CONFIG" ]; then
    echo "default"
    exit 0
fi

# Check if variants are enabled
if ! command -v jq &>/dev/null; then
    echo "default"
    exit 0
fi

ENABLED=$(jq -r '.variants.enabled // false' "$CONFIG" 2>/dev/null)
if [ "$ENABLED" != "true" ]; then
    echo "default"
    exit 0
fi

# Get active variants and their weights
ACTIVE_VARIANTS=$(jq -r '.variants.active[]' "$CONFIG" 2>/dev/null)
[ -z "$ACTIVE_VARIANTS" ] && { echo "default"; exit 0; }

# Compute deterministic hash
KEY="$SKILL_NAME:$SESSION_ID"
if command -v md5 &>/dev/null; then
    HASH=$(echo -n "$KEY" | md5 -q)
else
    HASH=$(echo -n "$KEY" | md5sum | cut -d' ' -f1)
fi

# Take first 8 hex chars, convert to decimal
HEX_PREFIX="${HASH:0:8}"
HASH_NUM=$((16#$HEX_PREFIX))

# Calculate total weight
TOTAL_WEIGHT=0
for variant in $ACTIVE_VARIANTS; do
    W=$(jq -r ".variants.definitions[\"$variant\"].weight // 50" "$CONFIG" 2>/dev/null)
    TOTAL_WEIGHT=$((TOTAL_WEIGHT + W))
done

# Assign variant based on weighted hash
ROLL=$((HASH_NUM % TOTAL_WEIGHT))
CUMULATIVE=0
for variant in $ACTIVE_VARIANTS; do
    W=$(jq -r ".variants.definitions[\"$variant\"].weight // 50" "$CONFIG" 2>/dev/null)
    CUMULATIVE=$((CUMULATIVE + W))
    if [ "$ROLL" -lt "$CUMULATIVE" ]; then
        echo "$variant"
        exit 0
    fi
done

# Fallback
echo "$ACTIVE_VARIANTS" | head -1
