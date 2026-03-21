#!/bin/bash
# Outcome Schema Validator — validates outcomes.jsonl entries
# Part of P12: Autoresearch Self-Improving Skills Framework
# Usage: ./scripts/validate-outcome.sh [--file <path>] [--sample] [--quiet]

set -e

OUTCOME_DIR="$HOME/.claude/skill-analytics"
DEFAULT_FILE="$OUTCOME_DIR/outcomes.jsonl"

FILE=""
SAMPLE=false
QUIET=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        --file)   FILE="$2"; shift 2 ;;
        --sample) SAMPLE=true; shift ;;
        --quiet)  QUIET=true; shift ;;
        -h|--help)
            echo "Usage: $0 [--file <path>] [--sample] [--quiet]"
            echo "  --file <path>  Validate specific file (default: $DEFAULT_FILE)"
            echo "  --sample       Generate and validate a sample outcome"
            echo "  --quiet        Only output errors"
            exit 0
            ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

# Require jq for validation
if ! command -v jq &>/dev/null; then
    echo "ERROR: jq is required for validation" >&2
    exit 1
fi

PASS=0
FAIL=0
ERRORS=()

validate_line() {
    local line="$1"
    local line_num="$2"

    # Must be valid JSON
    if ! echo "$line" | jq empty 2>/dev/null; then
        ERRORS+=("Line $line_num: invalid JSON")
        FAIL=$((FAIL + 1))
        return
    fi

    # Required field: ts (string, non-empty)
    local ts
    ts=$(echo "$line" | jq -r '.ts // empty' 2>/dev/null)
    if [ -z "$ts" ]; then
        ERRORS+=("Line $line_num: missing required field 'ts'")
        FAIL=$((FAIL + 1))
        return
    fi

    # Required field: skill (string, non-empty)
    local skill
    skill=$(echo "$line" | jq -r '.skill // empty' 2>/dev/null)
    if [ -z "$skill" ]; then
        ERRORS+=("Line $line_num: missing required field 'skill'")
        FAIL=$((FAIL + 1))
        return
    fi

    # Required field: status (enum)
    local status
    status=$(echo "$line" | jq -r '.status // empty' 2>/dev/null)
    case "$status" in
        success|partial|error) ;;
        "")
            ERRORS+=("Line $line_num: missing required field 'status'")
            FAIL=$((FAIL + 1))
            return
            ;;
        *)
            ERRORS+=("Line $line_num: invalid status '$status' (must be success|partial|error)")
            FAIL=$((FAIL + 1))
            return
            ;;
    esac

    # Optional: metrics must be object if present
    local metrics_type
    metrics_type=$(echo "$line" | jq -r '.metrics | type' 2>/dev/null)
    if [ "$metrics_type" != "null" ] && [ "$metrics_type" != "object" ]; then
        ERRORS+=("Line $line_num: 'metrics' must be an object, got $metrics_type")
        FAIL=$((FAIL + 1))
        return
    fi

    # Optional: runtime_ms must be number if present
    local runtime_type
    runtime_type=$(echo "$line" | jq -r '.runtime_ms | type' 2>/dev/null)
    if [ "$runtime_type" != "null" ] && [ "$runtime_type" != "number" ]; then
        ERRORS+=("Line $line_num: 'runtime_ms' must be a number, got $runtime_type")
        FAIL=$((FAIL + 1))
        return
    fi

    PASS=$((PASS + 1))
}

# Sample mode: generate and validate a test outcome
if $SAMPLE; then
    SAMPLE_DIR=$(mktemp -d)
    SAMPLE_FILE="$SAMPLE_DIR/sample-outcomes.jsonl"

    cat > "$SAMPLE_FILE" << 'SAMPLE_EOF'
{"ts":"2026-03-21T14:00:00Z","skill":"prospect-enrich","version":"1.1.0","variant":"default","status":"success","runtime_ms":45000,"metrics":{"contacts_processed":42,"phones_found":18,"atl_count":12},"session_id":"sample-001"}
{"ts":"2026-03-21T14:30:00Z","skill":"morning-brief","version":"1.0.0","variant":"default","status":"success","runtime_ms":30000,"metrics":{"dial_list_count":15,"deals_scored":8,"drafts_created":15},"session_id":"sample-002"}
{"ts":"2026-03-21T15:00:00Z","skill":"cold-email-sequence-generator","version":"1.1.0","variant":"concise","status":"partial","runtime_ms":20000,"metrics":{"sequences_created":1,"emails_generated":5},"error":null,"session_id":"sample-003"}
SAMPLE_EOF

    FILE="$SAMPLE_FILE"
    $QUIET || echo "=== Validating sample outcomes ==="
fi

# Determine input file
[ -z "$FILE" ] && FILE="$DEFAULT_FILE"

if [ ! -f "$FILE" ] || [ ! -s "$FILE" ]; then
    echo "No outcomes file found at: $FILE"
    echo "Run skills with outcome emit or use /skill-feedback to generate data."
    exit 0
fi

$QUIET || echo "=== Outcome Schema Validation ==="
$QUIET || echo "File: $FILE"
$QUIET || echo ""

# Validate each line
LINE_NUM=0
while IFS= read -r line; do
    LINE_NUM=$((LINE_NUM + 1))
    [ -z "$line" ] && continue
    validate_line "$line" "$LINE_NUM"
done < "$FILE"

# Report
TOTAL=$((PASS + FAIL))
if [ $FAIL -eq 0 ]; then
    echo "PASS: $TOTAL/$TOTAL outcomes valid"
    # Clean up sample temp dir
    [ -n "${SAMPLE_DIR:-}" ] && rm -rf "$SAMPLE_DIR"
    exit 0
else
    echo "FAIL: $FAIL/$TOTAL outcomes invalid"
    echo ""
    for err in "${ERRORS[@]}"; do
        echo "  - $err"
    done
    [ -n "${SAMPLE_DIR:-}" ] && rm -rf "$SAMPLE_DIR"
    exit 1
fi
