---
name: "git-workflow"
description: "Git workflow patterns - conventional commits, branch naming, PR templates, merge strategies. Use when: commit, PR, branch naming, git workflow, conventional commits, semantic versioning."
---

<objective>
Comprehensive git workflow skill covering conventional commits, semantic branch naming, PR templates, and merge strategies. Enforces consistency across all projects to reduce review friction and enable automated changelog generation.

This skill complements worktree-manager-skill (which handles parallel development) by providing the conventions for commits and PRs within those worktrees.
</objective>

<quick_start>
**Conventional Commit format:**

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

**Types:** feat, fix, docs, style, refactor, perf, test, build, ci, chore

**Example:**
```bash
git commit -m "feat(auth): add JWT refresh token rotation

Implements automatic token refresh 5 minutes before expiry.
Closes #123"
```

**Branch naming:** `<type>/<ticket>-<short-description>`
```bash
git checkout -b feat/AUTH-123-refresh-tokens
```
</quick_start>

<success_criteria>
Git workflow is successful when:
- All commits follow conventional commit format
- Branch names follow `<type>/<ticket>-<description>` pattern
- PRs use consistent template with summary, test plan, and checklist
- Merge strategy matches branch type (squash for features, merge for releases)
- Commit history tells a clear story of changes
- No force pushes to main/master without explicit team agreement
</success_criteria>

<conventional_commits>
## Conventional Commits Specification

Based on [conventionalcommits.org](https://www.conventionalcommits.org/)

### Commit Types

| Type | Description | Changelog Section | Version Bump |
|------|-------------|-------------------|--------------|
| feat | New feature | Features | Minor |
| fix | Bug fix | Bug Fixes | Patch |
| docs | Documentation only | - | - |
| style | Formatting, no code change | - | - |
| refactor | Code change, no feature/fix | - | - |
| perf | Performance improvement | Performance | Patch |
| test | Adding/fixing tests | - | - |
| build | Build system changes | - | - |
| ci | CI configuration | - | - |
| chore | Maintenance tasks | - | - |

### Breaking Changes

Add `!` after type or `BREAKING CHANGE:` in footer:

```bash
# Method 1: Bang notation
feat(api)!: change response format to JSON:API

# Method 2: Footer
feat(api): change response format to JSON:API

BREAKING CHANGE: Response structure changed from { data } to { data, meta, links }
```

### Scope Guidelines

Scope is optional but recommended. Use consistent scopes per project:

```
# Good scopes
auth, api, ui, db, config, deps

# Examples
feat(auth): add OAuth2 support
fix(api): handle null response from external service
docs(readme): add installation instructions
```

### Commit Message Structure

```
<type>(<scope>): <subject>
│       │         │
│       │         └─> Summary in present tense, no period, max 50 chars
│       │
│       └─> Component/area affected (optional)
│
└─> Type: feat, fix, docs, style, refactor, perf, test, build, ci, chore

[blank line]
[optional body - explain what and why, not how]
[blank line]
[optional footer(s) - breaking changes, issue references]
```

### Good vs Bad Examples

| Bad | Good | Why |
|-----|------|-----|
| `fixed bug` | `fix(auth): prevent token expiry race condition` | Specific, scoped |
| `updates` | `refactor(api): extract validation middleware` | Describes change |
| `WIP` | `feat(ui): add loading skeleton (WIP)` | Clear intent |
| `misc changes` | `chore: update dependencies to latest versions` | Typed, meaningful |
</conventional_commits>

<branch_naming>
## Branch Naming Conventions

### Pattern

```
<type>/<ticket-id>-<short-description>
```

### Branch Types

| Type | Use For | Example |
|------|---------|---------|
| feat/ | New features | feat/AUTH-123-oauth-login |
| fix/ | Bug fixes | fix/API-456-null-response |
| hotfix/ | Urgent production fixes | hotfix/PROD-789-payment-failure |
| docs/ | Documentation | docs/README-update |
| refactor/ | Code restructuring | refactor/cleanup-legacy-api |
| test/ | Test additions | test/add-auth-integration |
| chore/ | Maintenance | chore/update-deps |
| release/ | Release branches | release/v2.1.0 |

### Naming Rules

1. **Lowercase only** - `feat/auth-login` not `feat/Auth-Login`
2. **Hyphens for spaces** - `fix/null-response` not `fix/null_response`
3. **Include ticket ID** when available - `feat/JIRA-123-description`
4. **Keep short** - 50 chars max including type prefix
5. **Be descriptive** - `feat/user-profile` not `feat/feature1`

### Protected Branches

| Branch | Protection | Merge Strategy |
|--------|------------|----------------|
| main | Require PR + review | Squash merge |
| develop | Require PR | Merge commit |
| release/* | Require PR + CI pass | Merge commit |

### Examples

```bash
# Feature work
git checkout -b feat/PROJ-123-user-authentication

# Bug fix
git checkout -b fix/PROJ-456-login-redirect-loop

# Hotfix (from main)
git checkout main
git checkout -b hotfix/PROJ-789-payment-timeout

# Documentation
git checkout -b docs/api-endpoint-reference

# Chore
git checkout -b chore/upgrade-node-20
```
</branch_naming>

<pr_templates>
## Pull Request Templates

### Standard PR Template

```markdown
## Summary
<!-- 1-3 bullet points describing the change -->
-

## Type of Change
<!-- Check one -->
- [ ] feat: New feature
- [ ] fix: Bug fix
- [ ] docs: Documentation
- [ ] refactor: Code restructuring
- [ ] test: Test coverage
- [ ] chore: Maintenance

## Test Plan
<!-- How did you verify this works? -->
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated (if needed)
- [ ] No console.log or debug code
- [ ] No sensitive data exposed

## Related Issues
<!-- Link related issues -->
Closes #

## Screenshots
<!-- If UI change, add before/after -->
```

### Minimal PR Template (for small changes)

```markdown
## What
<!-- One sentence -->

## Why
<!-- One sentence -->

## Test
<!-- How verified -->

Closes #
```

### Release PR Template

```markdown
## Release v{VERSION}

### Changes Since Last Release
<!-- Auto-generated or manual list -->

### Breaking Changes
<!-- List any breaking changes -->

### Migration Guide
<!-- If breaking changes, how to migrate -->

### Deployment Notes
<!-- Any special deployment steps -->

### Rollback Plan
<!-- How to rollback if issues -->
```
</pr_templates>

<merge_strategies>
## Merge Strategies

### Strategy by Branch Type

| Branch Type | Strategy | Rationale |
|-------------|----------|-----------|
| feat/* | Squash | Clean single commit in main |
| fix/* | Squash | Clean single commit in main |
| hotfix/* | Merge | Preserve hotfix history |
| release/* | Merge | Preserve release commits |
| refactor/* | Squash or Rebase | Depends on commit count |

### Git Commands

```bash
# Squash merge (recommended for features)
git checkout main
git merge --squash feat/my-feature
git commit -m "feat(scope): description"

# Merge commit (for releases)
git checkout main
git merge --no-ff release/v2.0.0

# Rebase (for clean linear history)
git checkout feat/my-feature
git rebase main
git checkout main
git merge feat/my-feature

# Interactive rebase (clean up before PR)
git rebase -i HEAD~5
```

### Squash vs Merge Decision Tree

```
Is this a feature or fix branch?
├── Yes → Squash merge
└── No → Is this a release or hotfix?
    ├── Yes → Merge commit (preserve history)
    └── No → Consider context
```
</merge_strategies>

<commit_hooks>
## Commit Hooks (Optional Enforcement)

### commitlint Configuration

```javascript
// commitlint.config.js
module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [2, 'always', [
      'feat', 'fix', 'docs', 'style', 'refactor',
      'perf', 'test', 'build', 'ci', 'chore'
    ]],
    'scope-case': [2, 'always', 'lowercase'],
    'subject-case': [2, 'always', 'sentence-case'],
    'subject-max-length': [2, 'always', 72],
    'body-max-line-length': [2, 'always', 100],
  }
};
```

### Husky Setup

```bash
# Install
npm install -D husky @commitlint/cli @commitlint/config-conventional

# Initialize
npx husky init

# Add commit-msg hook
echo "npx --no -- commitlint --edit \$1" > .husky/commit-msg
```

### Pre-commit Checks

```bash
# .husky/pre-commit
#!/bin/sh
npm run lint
npm run test -- --run
```
</commit_hooks>

<versioning>
## Semantic Versioning

### Version Format

```
MAJOR.MINOR.PATCH
  │     │     │
  │     │     └─> Bug fixes (fix:)
  │     │
  │     └─> New features (feat:)
  │
  └─> Breaking changes (feat!: or BREAKING CHANGE:)
```

### Version Bump Rules

| Commit Type | Example | Version Change |
|-------------|---------|----------------|
| fix: | fix: null check | 1.0.0 → 1.0.1 |
| feat: | feat: new endpoint | 1.0.1 → 1.1.0 |
| feat!: | feat!: new API format | 1.1.0 → 2.0.0 |

### Automated Versioning

```bash
# Using standard-version
npx standard-version

# Using semantic-release (CI)
npx semantic-release
```
</versioning>

<workflow_examples>
## Complete Workflow Examples

### Feature Development

```bash
# 1. Create feature branch
git checkout main
git pull origin main
git checkout -b feat/PROJ-123-user-profile

# 2. Make commits (conventional format)
git add .
git commit -m "feat(ui): add profile avatar component"
git commit -m "feat(api): add profile update endpoint"
git commit -m "test(profile): add integration tests"

# 3. Rebase if needed
git fetch origin
git rebase origin/main

# 4. Push and create PR
git push -u origin feat/PROJ-123-user-profile
gh pr create --title "feat(profile): add user profile page" \
  --body "## Summary\n- Add profile avatar\n- Add update endpoint\n\nCloses #123"

# 5. After approval, squash merge
gh pr merge --squash
```

### Hotfix Flow

```bash
# 1. Create from main
git checkout main
git pull origin main
git checkout -b hotfix/PROD-456-payment-timeout

# 2. Fix and commit
git commit -m "fix(payment): increase timeout to 30s

Production payments timing out during high load.
Closes PROD-456"

# 3. Push and merge (no squash to preserve hotfix history)
git push -u origin hotfix/PROD-456-payment-timeout
gh pr create --title "hotfix: payment timeout" --body "Emergency fix"
gh pr merge --merge
```

### Release Flow

```bash
# 1. Create release branch
git checkout develop
git checkout -b release/v2.1.0

# 2. Version bump
npm version minor
git commit -am "chore(release): v2.1.0"

# 3. Merge to main
git checkout main
git merge --no-ff release/v2.1.0
git tag v2.1.0

# 4. Back-merge to develop
git checkout develop
git merge release/v2.1.0
```
</workflow_examples>

<checklist>
## Git Workflow Checklist

Before each commit:
- [ ] Commit message follows conventional format
- [ ] Type is accurate (feat/fix/docs/etc.)
- [ ] Scope matches affected component
- [ ] Subject is imperative, present tense
- [ ] Breaking changes marked with `!` or footer

Before creating PR:
- [ ] Branch name follows convention
- [ ] Rebased on latest main/develop
- [ ] All commits are meaningful (squash fixups)
- [ ] PR template filled out completely
- [ ] Related issues linked

Before merging:
- [ ] All CI checks pass
- [ ] Required reviews obtained
- [ ] No merge conflicts
- [ ] Correct merge strategy selected
</checklist>

<references>
For detailed patterns, load the appropriate reference:

| Topic | Reference File | When to Load |
|-------|----------------|--------------|
| Commit message examples | `reference/commit-examples.md` | Need more examples |
| PR template variants | `reference/pr-templates.md` | Project-specific templates |
| Git hooks setup | `reference/git-hooks.md` | Setting up enforcement |

**To load:** Ask for the specific topic or check if context suggests it.
</references>
