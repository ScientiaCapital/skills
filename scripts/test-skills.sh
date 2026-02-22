#!/bin/bash
# Integration tests for the skills library
# Usage: ./scripts/test-skills.sh [--verbose] [--skill <name>]
# Options:
#   --verbose    Show detailed output for each test
#   --skill      Test a single skill by name

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"

VERBOSE=false
SINGLE_SKILL=""
PASS_COUNT=0
FAIL_COUNT=0
FAILED_TESTS=()

# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        --verbose) VERBOSE=true; shift ;;
        --skill)   SINGLE_SKILL="$2"; shift 2 ;;
        *)         echo "Unknown option: $1"; exit 1 ;;
    esac
done

# --- Helpers ---

log_verbose() {
    if $VERBOSE; then
        echo "    $1"
    fi
}

pass() {
    PASS_COUNT=$((PASS_COUNT + 1))
    log_verbose "PASS: $1"
}

fail() {
    FAIL_COUNT=$((FAIL_COUNT + 1))
    FAILED_TESTS+=("$1")
    echo "  ✗ $1"
}

# --- Test Functions ---

# T1: Required files exist (SKILL.md, config.json)
test_required_files() {
    local skill_dir="$1" name="$2"
    if [[ ! -f "$skill_dir/SKILL.md" ]]; then
        fail "$name: missing SKILL.md"; return 1
    fi
    if [[ ! -f "$skill_dir/config.json" ]]; then
        fail "$name: missing config.json"; return 1
    fi
    pass "$name: required files exist"
}

# T2: YAML frontmatter parses — first line is ---, has name: and description:
test_yaml_frontmatter() {
    local skill_dir="$1" name="$2"
    local skill_md="$skill_dir/SKILL.md"
    [[ ! -f "$skill_md" ]] && return 0

    local first_line
    first_line=$(head -1 "$skill_md")
    if [[ "$first_line" != "---" ]]; then
        fail "$name: SKILL.md first line is not ---"; return 1
    fi

    # Extract frontmatter (between first and second ---)
    local frontmatter
    frontmatter=$(sed -n '2,/^---$/p' "$skill_md" | sed '$d')

    if ! echo "$frontmatter" | grep -q '^name:'; then
        fail "$name: YAML frontmatter missing name: field"; return 1
    fi
    if ! echo "$frontmatter" | grep -q '^description:'; then
        fail "$name: YAML frontmatter missing description: field"; return 1
    fi
    pass "$name: YAML frontmatter valid"
}

# T3: config.json schema — valid JSON with required keys
test_config_schema() {
    local skill_dir="$1" name="$2"
    local config="$skill_dir/config.json"
    [[ ! -f "$config" ]] && return 0

    if ! jq empty "$config" 2>/dev/null; then
        fail "$name: config.json is not valid JSON"; return 1
    fi

    local missing=()
    for key in name version category activation_triggers; do
        if [[ $(jq "has(\"$key\")" "$config") != "true" ]]; then
            missing+=("$key")
        fi
    done

    if [[ ${#missing[@]} -gt 0 ]]; then
        fail "$name: config.json missing keys: ${missing[*]}"; return 1
    fi
    pass "$name: config.json schema valid"
}

# T4: Required XML sections exist in SKILL.md body
test_xml_sections() {
    local skill_dir="$1" name="$2"
    local skill_md="$skill_dir/SKILL.md"
    [[ ! -f "$skill_md" ]] && return 0

    local missing=()
    for section in objective quick_start success_criteria; do
        if ! grep -q "<${section}>" "$skill_md"; then
            missing+=("<${section}>")
        fi
    done

    if [[ ${#missing[@]} -gt 0 ]]; then
        fail "$name: SKILL.md missing XML sections: ${missing[*]}"; return 1
    fi
    pass "$name: XML sections present"
}

# T5: SKILL.md under 500 lines
test_line_count() {
    local skill_dir="$1" name="$2"
    local skill_md="$skill_dir/SKILL.md"
    [[ ! -f "$skill_md" ]] && return 0

    local lines
    lines=$(wc -l < "$skill_md" | tr -d ' ')
    if [[ "$lines" -gt 500 ]]; then
        fail "$name: SKILL.md is $lines lines (max 500)"; return 1
    fi
    pass "$name: SKILL.md line count OK ($lines)"
}

# T6: No circular dependencies (library-wide DFS)
# Uses temp files for state (bash 3.2 compatible — no associative arrays)
test_circular_deps() {
    local tmpdir
    tmpdir=$(mktemp -d)
    local cycle_found=false

    # Build dependency map: one file per skill listing its depends_on
    for skill_dir in "$REPO_DIR"/active/*/ "$REPO_DIR"/stable/*/; do
        [[ ! -d "$skill_dir" ]] && continue
        local sname
        sname=$(basename "$skill_dir")
        local config="$skill_dir/config.json"
        if [[ -f "$config" ]]; then
            jq -r '(.depends_on // [])[]' "$config" 2>/dev/null > "$tmpdir/deps_$sname"
        else
            : > "$tmpdir/deps_$sname"
        fi
        echo "0" > "$tmpdir/vis_$sname"  # 0=unvisited
    done

    # DFS cycle detection using temp file state
    # vis states: 0=unvisited, 1=in-stack, 2=done
    dfs() {
        local node="$1"
        echo "1" > "$tmpdir/vis_$node"  # mark in-stack

        if [[ -f "$tmpdir/deps_$node" ]]; then
            while IFS= read -r dep; do
                [[ -z "$dep" ]] && continue
                local dep_state="0"
                if [[ -f "$tmpdir/vis_$dep" ]]; then
                    dep_state=$(cat "$tmpdir/vis_$dep")
                fi
                if [[ "$dep_state" == "1" ]]; then
                    fail "Circular dependency: $node -> $dep"
                    cycle_found=true
                    return
                fi
                if [[ "$dep_state" == "0" ]]; then
                    dfs "$dep"
                    if $cycle_found; then return; fi
                fi
            done < "$tmpdir/deps_$node"
        fi

        echo "2" > "$tmpdir/vis_$node"  # mark done
    }

    for vis_file in "$tmpdir"/vis_*; do
        [[ ! -f "$vis_file" ]] && continue
        local sname
        sname=$(basename "$vis_file")
        sname="${sname#vis_}"
        if [[ "$(cat "$vis_file")" == "0" ]]; then
            dfs "$sname"
        fi
    done

    rm -rf "$tmpdir"

    if ! $cycle_found; then
        pass "No circular dependencies found"
    fi
}

# T7: All integrates_with refs point to existing skill directories
test_integrates_with() {
    local skill_dir="$1" name="$2"
    local config="$skill_dir/config.json"
    [[ ! -f "$config" ]] && return 0

    local refs
    refs=$(jq -r '(.integrates_with // [])[]' "$config" 2>/dev/null)
    [[ -z "$refs" ]] && { pass "$name: integrates_with (none)"; return 0; }

    local bad=()
    while IFS= read -r ref; do
        if [[ ! -d "$REPO_DIR/active/$ref" ]] && [[ ! -d "$REPO_DIR/stable/$ref" ]]; then
            bad+=("$ref")
        fi
    done <<< "$refs"

    if [[ ${#bad[@]} -gt 0 ]]; then
        fail "$name: integrates_with refs not found: ${bad[*]}"; return 1
    fi
    pass "$name: integrates_with refs valid"
}

# T8: All activation_triggers are non-empty strings
test_activation_triggers() {
    local skill_dir="$1" name="$2"
    local config="$skill_dir/config.json"
    [[ ! -f "$config" ]] && return 0

    local trigger_count
    trigger_count=$(jq '.activation_triggers | length' "$config" 2>/dev/null)
    if [[ "$trigger_count" -eq 0 ]]; then
        fail "$name: activation_triggers is empty"; return 1
    fi

    local empty_count
    empty_count=$(jq '[.activation_triggers[] | select(. == "" or type != "string")] | length' "$config" 2>/dev/null)
    if [[ "$empty_count" -gt 0 ]]; then
        fail "$name: activation_triggers contains $empty_count empty/non-string entries"; return 1
    fi
    pass "$name: activation_triggers valid ($trigger_count triggers)"
}

# --- Run per-skill tests (returns 1 if any test failed) ---

run_skill_tests() {
    local skill_dir="$1"
    local name
    name=$(basename "$skill_dir")
    local skill_ok=true

    test_required_files  "$skill_dir" "$name" || skill_ok=false
    test_yaml_frontmatter "$skill_dir" "$name" || skill_ok=false
    test_config_schema   "$skill_dir" "$name" || skill_ok=false
    test_xml_sections    "$skill_dir" "$name" || skill_ok=false
    test_line_count      "$skill_dir" "$name" || skill_ok=false
    test_integrates_with "$skill_dir" "$name" || skill_ok=false
    test_activation_triggers "$skill_dir" "$name" || skill_ok=false

    $skill_ok
}

# --- Main ---

echo "=== Skills Integration Tests ==="
echo "Repository: $REPO_DIR"
if [[ -n "$SINGLE_SKILL" ]]; then
    echo "Skill filter: $SINGLE_SKILL"
fi
echo ""

# Per-skill tests
skill_count=0

echo "Testing active skills..."
for skill in "$REPO_DIR"/active/*/; do
    [[ ! -d "$skill" ]] && continue
    name=$(basename "$skill")
    if [[ -n "$SINGLE_SKILL" ]] && [[ "$name" != "$SINGLE_SKILL" ]]; then
        continue
    fi
    if run_skill_tests "$skill"; then
        echo "  ✓ $name"
    fi
    skill_count=$((skill_count + 1))
done

echo "Testing stable skills..."
for skill in "$REPO_DIR"/stable/*/; do
    [[ ! -d "$skill" ]] && continue
    name=$(basename "$skill")
    if [[ -n "$SINGLE_SKILL" ]] && [[ "$name" != "$SINGLE_SKILL" ]]; then
        continue
    fi
    if run_skill_tests "$skill"; then
        echo "  ✓ $name"
    fi
    skill_count=$((skill_count + 1))
done

# Library-wide tests
echo ""
echo "Running library-wide tests..."
test_circular_deps
echo "  ✓ Circular dependency check"

# Summary
echo ""
total=$((PASS_COUNT + FAIL_COUNT))
if [[ $FAIL_COUNT -eq 0 ]]; then
    echo "✅ All $total tests passed across $skill_count skills"
    exit 0
else
    echo "❌ $FAIL_COUNT/$total tests failed across $skill_count skills"
    echo ""
    echo "Failures:"
    for f in "${FAILED_TESTS[@]}"; do
        echo "  ✗ $f"
    done
    exit 1
fi
