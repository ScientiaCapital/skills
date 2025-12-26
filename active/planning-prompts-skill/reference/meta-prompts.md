# Meta-Prompts Reference

Comprehensive reference for creating Claude-to-Claude prompts and multi-stage workflows. Outputs are structured with XML and metadata for efficient parsing by subsequent prompts.

---

## Folder Structure

```
.prompts/
├── 001-auth-research/
│   ├── completed/
│   │   └── 001-auth-research.md    # Prompt (archived after run)
│   ├── auth-research.md            # Full output (XML for Claude)
│   └── SUMMARY.md                  # Executive summary (for human)
├── 002-auth-plan/
│   ├── completed/
│   │   └── 002-auth-plan.md
│   ├── auth-plan.md
│   └── SUMMARY.md
├── 003-auth-implement/
│   ├── completed/
│   │   └── 003-auth-implement.md
│   └── SUMMARY.md                  # Do prompts create code elsewhere
```

---

## Intake Gate

<first_action>
IF no context provided (skill invoked without description):
-> IMMEDIATELY ask:

- header: "Purpose"
- question: "What is the purpose of this prompt?"
- options:
  - "Do" - Execute a task, produce an artifact
  - "Plan" - Create an approach, roadmap, or strategy
  - "Research" - Gather information or understand something
  - "Refine" - Improve an existing research or plan output

After selection, ask: "Describe what you want to accomplish"
</first_action>

<purpose_inference>
If context was provided, infer purpose from keywords:
- `implement`, `build`, `create`, `fix`, `add`, `refactor` -> Do
- `plan`, `roadmap`, `approach`, `strategy`, `decide`, `phases` -> Plan
- `research`, `understand`, `learn`, `gather`, `analyze`, `explore` -> Research
- `refine`, `improve`, `deepen`, `expand`, `iterate`, `update` -> Refine
</purpose_inference>

<chain_detection>
Scan `.prompts/*/` for existing `*-research.md` and `*-plan.md` files.

If found:
1. List them: "Found existing files: auth-research.md (in 001-auth-research/), stripe-plan.md (in 005-stripe-plan/)"
2. Ask: "Should this prompt reference any existing research or plans?"
3. Match by topic keyword when possible (e.g., "auth plan" -> suggest auth-research.md)
</chain_detection>

<decision_gate>
After gathering context:

- header: "Ready"
- question: "Ready to create the prompt?"
- options:
  - "Proceed" - Create the prompt with current context
  - "Ask more questions" - I have more details to clarify
  - "Let me add context" - I want to provide additional information

Loop until "Proceed" selected.
</decision_gate>

---

## Research Prompts

<purpose>
Gather information that planning or implementation prompts will consume.
</purpose>

<template>
```xml
<session_initialization>
Before beginning research, verify today's date:
!`date +%Y-%m-%d`

Use this date when searching for "current" or "latest" information.
</session_initialization>

<research_objective>
Research {topic} to inform {subsequent use}.

Purpose: {What decision/implementation this enables}
Scope: {Boundaries of the research}
Output: {topic}-research.md with structured findings
</research_objective>

<research_scope>
<include>
{What to investigate}
{Specific questions to answer}
</include>

<exclude>
{What's out of scope}
{What to defer to later research}
</exclude>

<sources>
{Priority sources with exact URLs for WebFetch}
Official documentation:
- https://example.com/official-docs

Search queries for WebSearch:
- "{topic} best practices {current_year}"
- "{topic} latest version"
</sources>
</research_scope>

<verification_checklist>
□ Verify ALL known configuration/implementation options
□ Document exact file locations/URLs for each option
□ Verify precedence/hierarchy rules if applicable
□ Confirm syntax and examples from official sources
□ Check for recent updates or changes to documentation
□ Verify negative claims ("X is not possible") with official docs
□ Confirm all primary claims have authoritative sources
</verification_checklist>

<output_structure>
Save to: `.prompts/{num}-{topic}-research/{topic}-research.md`

Structure findings using this XML format:

<research>
  <summary>
    {2-3 paragraph executive summary}
  </summary>

  <findings>
    <finding category="{category}">
      <title>{Finding title}</title>
      <detail>{Detailed explanation}</detail>
      <source>{Where this came from}</source>
      <relevance>{Why this matters}</relevance>
    </finding>
  </findings>

  <recommendations>
    <recommendation priority="high">
      <action>{What to do}</action>
      <rationale>{Why}</rationale>
    </recommendation>
  </recommendations>

  <code_examples>
    {Relevant code patterns, snippets, configurations}
  </code_examples>

  <metadata>
    <confidence level="{high|medium|low}">
      {Why this confidence level}
    </confidence>
    <dependencies>
      {What's needed to proceed}
    </dependencies>
    <open_questions>
      {What couldn't be determined}
    </open_questions>
    <assumptions>
      {What was assumed}
    </assumptions>
    <quality_report>
      <sources_consulted>{URLs}</sources_consulted>
      <claims_verified>{Verified facts}</claims_verified>
      <claims_assumed>{Inferences}</claims_assumed>
    </quality_report>
  </metadata>
</research>
</output_structure>

<incremental_output>
CRITICAL: Write findings incrementally to prevent token limit failures.

1. Create file with skeleton structure
2. Write each finding as you discover it
3. Append code examples as you find them
4. Update metadata at the end

This ensures zero lost work if token limit is hit.
</incremental_output>

<summary_requirements>
Create `.prompts/{num}-{topic}-research/SUMMARY.md`

For research, emphasize key recommendation and decision readiness.
Next step typically: Create plan.
</summary_requirements>
```
</template>

<research_types>

### Technology Research
For understanding tools, libraries, APIs:
```xml
<research_objective>
Research JWT authentication libraries for Node.js.
Purpose: Select library for auth implementation
Scope: Security, performance, maintenance status
</research_objective>

<verification_checklist>
□ Verify all major JWT libraries (jose, jsonwebtoken, passport-jwt)
□ Check npm download trends for adoption metrics
□ Review GitHub security advisories for each library
□ Confirm TypeScript support with examples
</verification_checklist>
```

### Best Practices Research
For understanding patterns and standards:
```xml
<research_objective>
Research authentication security best practices.
Purpose: Inform secure auth implementation
Scope: Current standards, common vulnerabilities, mitigations
</research_objective>

<sources>
Official sources:
- https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html
</sources>
```

### Comparison Research
For evaluating options:
```xml
<research_objective>
Research database options for multi-tenant SaaS.
Purpose: Inform database selection decision
Scope: PostgreSQL, MongoDB, DynamoDB for our use case
</research_objective>

<evaluation_criteria>
- Data isolation requirements
- Expected query patterns
- Scale projections
- Team familiarity
</evaluation_criteria>
```
</research_types>

---

## Plan Prompts

<purpose>
Create approaches, roadmaps, and strategies that implementation prompts will consume.
</purpose>

<template>
```xml
<objective>
Create a {plan type} for {topic}.

Purpose: {What decision/implementation this enables}
Input: {Research or context being used}
Output: {topic}-plan.md with actionable phases/steps
</objective>

<context>
Research findings: @.prompts/{num}-{topic}-research/{topic}-research.md
{Additional context files}
</context>

<planning_requirements>
{What the plan needs to address}
{Constraints to work within}
{Success criteria for the planned outcome}
</planning_requirements>

<output_structure>
Save to: `.prompts/{num}-{topic}-plan/{topic}-plan.md`

Structure the plan using this XML format:

<plan>
  <summary>
    {One paragraph overview of the approach}
  </summary>

  <phases>
    <phase number="1" name="{phase-name}">
      <objective>{What this phase accomplishes}</objective>
      <tasks>
        <task priority="high">{Specific actionable task}</task>
        <task priority="medium">{Another task}</task>
      </tasks>
      <deliverables>
        <deliverable>{What's produced}</deliverable>
      </deliverables>
      <dependencies>{What must exist before this phase}</dependencies>
    </phase>
  </phases>

  <metadata>
    <confidence level="{high|medium|low}">
      {Why this confidence level}
    </confidence>
    <dependencies>
      {External dependencies needed}
    </dependencies>
    <open_questions>
      {Uncertainties that may affect execution}
    </open_questions>
    <assumptions>
      {What was assumed in creating this plan}
    </assumptions>
  </metadata>
</plan>
</output_structure>

<summary_requirements>
Create `.prompts/{num}-{topic}-plan/SUMMARY.md`

For plans, emphasize phase breakdown with objectives and assumptions needing validation.
Next step typically: Execute first phase.
</summary_requirements>
```
</template>

<plan_types>

### Implementation Roadmap
For breaking down how to build something:
```xml
<objective>
Create implementation roadmap for user authentication system.
Purpose: Guide phased implementation with clear milestones
Input: Authentication research findings
Output: auth-plan.md with 4-5 implementation phases
</objective>

<planning_requirements>
- Break into independently testable phases
- Each phase builds on previous
- Include testing at each phase
- Consider rollback points
</planning_requirements>
```

### Decision Framework
For choosing between options:
```xml
<objective>
Create decision framework for selecting database technology.
Purpose: Make informed choice between PostgreSQL, MongoDB, and DynamoDB
</objective>

<output_structure>
<decision_framework>
  <options>
    <option name="PostgreSQL">
      <pros>{List}</pros>
      <cons>{List}</cons>
      <fit_score criteria="scalability">8/10</fit_score>
    </option>
  </options>
  <recommendation>
    <choice>{Selected option}</choice>
    <rationale>{Why}</rationale>
    <risks>{What could go wrong}</risks>
  </recommendation>
</decision_framework>
</output_structure>
```

### Process Definition
For defining workflows:
```xml
<objective>
Create deployment process for production releases.
Purpose: Standardize safe, repeatable deployments
</objective>

<output_structure>
<process>
  <steps>
    <step number="1" name="pre-deployment">
      <actions>
        <action>Run full test suite</action>
        <action>Create database backup</action>
      </actions>
      <checklist>
        <item>Tests passing</item>
        <item>Backup verified</item>
      </checklist>
      <rollback>N/A - no changes yet</rollback>
    </step>
  </steps>
</process>
</output_structure>
```
</plan_types>

---

## Do Prompts

<purpose>
Execute tasks and produce artifacts (code, documents, designs).
</purpose>

<template>
```xml
<objective>
{Clear statement of what to build/create/fix}

Purpose: {Why this matters, what it enables}
Output: {What artifact(s) will be produced}
</objective>

<context>
{Referenced research/plan files if chained}
@.prompts/{num}-{topic}-research/{topic}-research.md
@.prompts/{num}-{topic}-plan/{topic}-plan.md

{Project context}
@relevant-files
</context>

<requirements>
{Specific functional requirements}
{Quality requirements}
{Constraints and boundaries}
</requirements>

<implementation>
{Specific approaches or patterns to follow}
{What to avoid and WHY}
{Integration points}
</implementation>

<output>
Create/modify files:
- `./path/to/file.ext` - {description}
</output>

<verification>
Before declaring complete:
- {Specific test or check}
- {How to confirm it works}
- {Edge cases to verify}
</verification>

<summary_requirements>
Create `.prompts/{num}-{topic}-{purpose}/SUMMARY.md`

For Do prompts, include Files Created section with paths and descriptions.
Emphasize what was implemented and test status.
Next step typically: Run tests or execute next phase.
</summary_requirements>

<success_criteria>
{Clear, measurable criteria}
- {Criterion 1}
- {Criterion 2}
- SUMMARY.md created with files list and next step
</success_criteria>
```
</template>

<examples>

### Simple Do
```xml
<objective>
Create a utility function that validates email addresses.
</objective>

<requirements>
- Support standard email format
- Return boolean
- Handle edge cases (empty, null)
</requirements>

<output>
Create: `./src/utils/validate-email.ts`
</output>

<verification>
Test with: valid emails, invalid formats, edge cases
</verification>
```

### Complex Do
```xml
<objective>
Implement user authentication system with JWT tokens.
Purpose: Enable secure user sessions
Output: Auth middleware, routes, types, and tests
</objective>

<context>
Research: @.prompts/001-auth-research/auth-research.md
Plan: @.prompts/002-auth-plan/auth-plan.md
Existing user model: @src/models/user.ts
</context>

<implementation>
Follow patterns from auth-research.md:
- Use jose library for JWT (not jsonwebtoken - see research)
- Implement refresh rotation per OWASP guidelines
- Store refresh tokens hashed in database

Avoid:
- Storing tokens in localStorage (XSS vulnerable)
- Long-lived access tokens (security risk)
</implementation>

<output>
Create in ./src/auth/:
- `middleware.ts` - JWT validation, refresh logic
- `routes.ts` - Login, logout, refresh endpoints
- `types.ts` - Token payloads, auth types
- `utils.ts` - Token generation, hashing
</output>

<verification>
1. Run test suite: `npm test src/auth`
2. Type check: `npx tsc --noEmit`
3. Manual test: login flow, token refresh, logout
</verification>
```
</examples>

---

## Refine Prompts

<purpose>
Improve existing research or plan outputs.
</purpose>

<template>
```xml
<objective>
Refine {topic}-{type}.md based on {feedback/new requirements}.

Purpose: {Why refinement is needed}
Input: {Existing output to improve}
Output: Updated {topic}-{type}.md with version increment
</objective>

<context>
Current version: @.prompts/{num}-{topic}-{type}/{topic}-{type}.md
{Additional context or feedback}
</context>

<refinement_scope>
<improve>
{What to enhance}
{New information to incorporate}
</improve>

<preserve>
{What to keep unchanged}
{Validated decisions}
</preserve>
</refinement_scope>

<output>
Update: `.prompts/{num}-{topic}-{type}/{topic}-{type}.md`
Archive previous: `.prompts/{num}-{topic}-{type}/archive/{topic}-{type}-v1.md`

Increment version in metadata.
</output>

<summary_requirements>
Create updated SUMMARY.md with:
- Version: "v2 (refined from v1)"
- Changes from Previous section
- Updated Key Findings
</summary_requirements>
```
</template>

---

## Execution Engine

<execution_modes>

### Single Prompt
```
1. Read prompt file contents
2. Spawn Task agent with subagent_type="general-purpose"
3. Include prompt contents + output location
4. Wait for completion
5. Validate output
6. Archive prompt to `completed/` subfolder
7. Report results with next-step options
```

### Sequential Execution
For chained prompts where each depends on previous:
```
1. Build execution queue from dependency order
2. For each prompt:
   a. Read prompt file
   b. Spawn Task agent
   c. Wait for completion
   d. Validate output
   e. If failure -> stop, report, offer recovery
   f. If success -> archive prompt, continue
3. Report consolidated results
```

### Parallel Execution
For independent prompts with no dependencies:
```
1. Read all prompt files
2. CRITICAL: Spawn ALL Task agents in a SINGLE message
3. Wait for all to complete
4. Validate all outputs
5. Archive all prompts
6. Report consolidated results (successes and failures)
```

### Mixed Dependencies
For complex DAGs:
```
1. Analyze dependency graph from @ references
2. Group into execution layers:
   - Layer 1: No dependencies (run parallel)
   - Layer 2: Depends only on layer 1 (run after layer 1)
3. Execute: Parallel within layer, sequential between layers
```
</execution_modes>

<dependency_detection>
Scan prompt contents for `@.prompts/{number}-{topic}/` patterns.

**Inference rules** (if no explicit @ references):
- Research prompts: No dependencies (can parallel)
- Plan prompts: Depend on same-topic research
- Do prompts: Depend on same-topic plan
</dependency_detection>

<validation>
After each prompt completes:
1. **File exists**: Check output file was created
2. **Not empty**: File has content (> 100 chars)
3. **Metadata present** (for research/plan): Check required XML tags
4. **SUMMARY.md exists**: Check created
5. **One-liner is substantive**: Not generic like "Research completed"
</validation>

<archiving>
After successful completion:
```bash
mv .prompts/{num}-{topic}-{purpose}/{num}-{topic}-{purpose}.md \
   .prompts/{num}-{topic}-{purpose}/completed/
```
Output file stays in place (not moved).
</archiving>

---

## Intelligence Rules

<extended_thinking_triggers>
Use these phrases to activate deeper reasoning in complex prompts:
- "Thoroughly analyze..."
- "Consider multiple approaches..."
- "Deeply consider the implications..."
- "Explore various solutions before..."
- "Carefully evaluate trade-offs..."

**When to use:** Complex architectural decisions, security-sensitive implementations, trade-off analysis.

**When NOT to use:** Simple tasks, clear single approach, basic CRUD.
</extended_thinking_triggers>

<parallel_tool_calling>
Include for efficient research:
```xml
<efficiency>
For maximum efficiency, invoke all independent tool operations
simultaneously rather than sequentially. Multiple file reads,
searches, and API calls that don't depend on each other should
run in parallel.
</efficiency>
```
</parallel_tool_calling>

<why_explanations>
Always explain why constraints matter:

**Bad:**
```xml
<requirements>
Never store tokens in localStorage.
</requirements>
```

**Good:**
```xml
<requirements>
Never store tokens in localStorage - it's accessible to any
JavaScript on the page, making it vulnerable to XSS attacks.
Use httpOnly cookies instead.
</requirements>
```

This helps the executing Claude make good decisions when facing edge cases.
</why_explanations>

---

## Metadata Guidelines

<structure>
```xml
<metadata>
  <confidence level="{high|medium|low}">
    {Why this confidence level}
  </confidence>
  <dependencies>
    {What's needed to proceed}
  </dependencies>
  <open_questions>
    {What remains uncertain}
  </open_questions>
  <assumptions>
    {What was assumed}
  </assumptions>
</metadata>
```
</structure>

<confidence_levels>
- **high**: Official docs, verified patterns, clear consensus, few unknowns
- **medium**: Mixed sources, some outdated info, minor gaps, reasonable approach
- **low**: Sparse documentation, conflicting info, significant unknowns, best guess
</confidence_levels>

---

## SUMMARY.md Template

```markdown
# {Topic} {Purpose} Summary

**{Substantive one-liner describing outcome}**

## Version
{v1 or "v2 (refined from v1)"}

## Changes from Previous
{Only include if v2+}

## Key Findings
- {Most important finding or action}
- {Second key item}
- {Third key item}

## Files Created
{Only for Do prompts}
- `path/to/file.ts` - Description

## Decisions Needed
{Specific actionable decisions, or "None"}

## Blockers
{External impediments, or "None"}

## Next Step
{Concrete forward action}

---
*Confidence: {High|Medium|Low}*
*Full output: {filename.md}*
```

<one_liner_requirements>
Must be substantive:
- **Good**: "JWT with jose library and httpOnly cookies recommended"
- **Bad**: "Research completed"

- **Good**: "4-phase implementation: types -> JWT core -> refresh -> tests"
- **Bad**: "Plan created"

- **Good**: "JWT middleware complete with 6 files in src/auth/"
- **Bad**: "Implementation finished"
</one_liner_requirements>

---

## Research Pitfalls

<common_mistakes>

### Configuration Scope Assumptions
**Mistake:** Assuming there's only one way to configure something.
**Fix:** Enumerate ALL known configuration scopes (user, project, local, environment).

### "Search for X" Vagueness
**Mistake:** "Search for documentation" without specific URLs.
**Fix:** Provide exact URLs for WebFetch, specific queries for WebSearch.

### Deprecated vs Current Confusion
**Mistake:** Using outdated patterns from old documentation.
**Fix:** Always check changelogs and documentation dates.

### Tool-Specific Variations
**Mistake:** Assuming same behavior across all environments.
**Fix:** Check for Desktop vs Code vs CLI variations.

### Negative Claims Without Verification
**Mistake:** "X is not possible" without checking official docs.
**Fix:** Verify all "not possible" or "only way" claims with authoritative sources.
</common_mistakes>

<quality_assurance>
Before completing research:
- [ ] All enumerated options/components documented with evidence
- [ ] Official documentation cited for critical claims
- [ ] Version numbers and dates included where relevant
- [ ] Distinguished verified facts from assumptions
- [ ] Asked: "What might I have missed?"
</quality_assurance>
