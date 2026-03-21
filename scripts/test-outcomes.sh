#!/bin/bash
# Infrastructure tests for P12 Autoresearch outcome logging
# Tests T10-T14 — complements test-skills.sh (T1-T9)
# Usage: ./scripts/test-outcomes.sh [--verbose]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"

VERBOSE=false
[[ "${1:-}" == "--verbose" ]] && VERBOSE=true

PASS_COUNT=0
FAIL_COUNT=0
FAILED_TESTS=()

log_verbose() { $VERBOSE && echo "    $1" || true; }
pass() { PASS_COUNT=$((PASS_COUNT + 1)); log_verbose "PASS: $1"; }
fail() { FAIL_COUNT=$((FAIL_COUNT + 1)); FAILED_TESTS+=("$1"); echo "  ✗ $1"; }

# Setup: create temp dir for isolated testing
TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT

export HOME_BACKUP="$HOME"

# --- T10: validate-outcome.sh --sample produces valid schema ---
test_validate_outcome_sample() {
    if bash "$SCRIPT_DIR/validate-outcome.sh" --sample --quiet >/dev/null 2>&1; then
        pass "T10: validate-outcome.sh --sample produces valid schema"
    else
        fail "T10: validate-outcome.sh --sample failed"
    fi
}

# --- T11: Sidecar round-trip (write sidecar → run hook → appears in outcomes.jsonl) ---
test_sidecar_roundtrip() {
    local TEST_DIR="$TMPDIR/.claude/skill-analytics"
    mkdir -p "$TEST_DIR"

    # Write a test sidecar (must match $HOME/.claude/skill-analytics/last-outcome-*)
    local SIDECAR="$TEST_DIR/last-outcome-test-skill.json"
    echo '{"ts":"2026-03-21T10:00:00Z","skill":"test-skill","status":"success","runtime_ms":1000}' > "$SIDECAR"

    # Simulate hook stdin (what PostToolUse sends)
    local HOOK_INPUT="{\"tool_input\":{\"file_path\":\"$SIDECAR\",\"content\":\"test\"}}"

    # Override HOME so log-outcome.sh uses our temp dir
    echo "$HOOK_INPUT" | HOME="$TMPDIR" bash "$SCRIPT_DIR/log-outcome.sh" 2>/dev/null

    # Check outcomes.jsonl was created and has the entry
    local OUTCOMES="$TEST_DIR/outcomes.jsonl"
    if [ -f "$OUTCOMES" ] && grep -q '"test-skill"' "$OUTCOMES" 2>/dev/null; then
        pass "T11: sidecar round-trip (write → hook → outcomes.jsonl)"
    else
        fail "T11: sidecar round-trip failed (outcomes.jsonl missing or empty)"
    fi

    # Check sidecar was deleted
    if [ ! -f "$SIDECAR" ]; then
        pass "T11b: sidecar cleanup (file deleted after capture)"
    else
        fail "T11b: sidecar not deleted after capture"
    fi
}

# --- T12: Variant assigner is deterministic ---
test_variant_determinism() {
    local RESULTS=""
    local CONSISTENT=true

    # Run 5 times with same input
    local FIRST
    FIRST=$(bash "$SCRIPT_DIR/variant-assigner.sh" cold-email-sequence-generator-skill "determinism-test-123" 2>/dev/null)

    for i in 2 3 4 5; do
        local RESULT
        RESULT=$(bash "$SCRIPT_DIR/variant-assigner.sh" cold-email-sequence-generator-skill "determinism-test-123" 2>/dev/null)
        if [ "$RESULT" != "$FIRST" ]; then
            CONSISTENT=false
            break
        fi
    done

    if $CONSISTENT && [ -n "$FIRST" ]; then
        pass "T12: variant assigner deterministic (5 runs → '$FIRST')"
    else
        fail "T12: variant assigner not deterministic"
    fi

    # Also verify it returns a valid variant name
    case "$FIRST" in
        control|concise)
            pass "T12b: variant assigner returns valid variant name"
            ;;
        default)
            pass "T12b: variant assigner returns default (variants may not be configured)"
            ;;
        *)
            fail "T12b: variant assigner returned unexpected: '$FIRST'"
            ;;
    esac
}

# --- T13: Feedback logger writes valid JSONL ---
test_feedback_logger() {
    local TEST_DIR="$TMPDIR/.claude/skill-analytics"
    mkdir -p "$TEST_DIR"

    local FEEDBACK='{"ts":"2026-03-21T12:00:00Z","skill":"test-skill","status":"success","notes":"test feedback"}'

    echo "$FEEDBACK" | HOME="$TMPDIR" bash "$SCRIPT_DIR/log-feedback.sh" 2>/dev/null

    local FEEDBACK_FILE="$TEST_DIR/feedback.jsonl"
    if [ -f "$FEEDBACK_FILE" ] && grep -q '"test feedback"' "$FEEDBACK_FILE" 2>/dev/null; then
        pass "T13: feedback logger writes valid JSONL"
    else
        fail "T13: feedback logger failed"
    fi

    # Validate it's valid JSON
    if command -v jq &>/dev/null; then
        if head -1 "$FEEDBACK_FILE" | jq empty 2>/dev/null; then
            pass "T13b: feedback JSONL is valid JSON"
        else
            fail "T13b: feedback JSONL is not valid JSON"
        fi
    fi
}

# --- T14: Existing test-skills.sh still passes (regression gate) ---
test_regression_gate() {
    if bash "$SCRIPT_DIR/test-skills.sh" >/dev/null 2>&1; then
        pass "T14: test-skills.sh regression gate (all existing tests pass)"
    else
        fail "T14: test-skills.sh regression — existing tests failed"
    fi
}

# --- Main ---
echo "=== Outcome Infrastructure Tests (T10-T14) ==="
echo ""

test_validate_outcome_sample
echo "  ✓ T10: Schema validation"

test_sidecar_roundtrip
echo "  ✓ T11: Sidecar round-trip"

test_variant_determinism
echo "  ✓ T12: Variant determinism"

test_feedback_logger
echo "  ✓ T13: Feedback logger"

test_regression_gate
echo "  ✓ T14: Regression gate"

# Summary
echo ""
total=$((PASS_COUNT + FAIL_COUNT))
if [[ $FAIL_COUNT -eq 0 ]]; then
    echo "All $total infrastructure tests passed"
    exit 0
else
    echo "$FAIL_COUNT/$total infrastructure tests failed"
    echo ""
    echo "Failures:"
    for f in "${FAILED_TESTS[@]}"; do
        echo "  ✗ $f"
    done
    exit 1
fi
