# Prompt Templates for Subagent Teams

## Research Prompts

### Codebase Search
```
Search the codebase for [PATTERN]. Focus on [SCOPE: src/, tests/, config/].

Report for each match:
- File path and line number
- 2-sentence summary of what this code does
- How it relates to [CONTEXT]

Do NOT modify any files. Research only.
```

### Framework Evaluation
```
Research [FRAMEWORK/TOOL] for use in this project.

Evaluate:
1. Does it solve [PROBLEM]?
2. What are the main dependencies?
3. How does it compare to [ALTERNATIVE]?
4. Any security concerns?

Return a GO/NO-GO recommendation with rationale.
```

---

## Build Prompts

### Component Implementation
```
Implement [COMPONENT] in [FILE_PATH].

Requirements:
- [REQUIREMENT 1]
- [REQUIREMENT 2]
- [REQUIREMENT 3]

Follow existing patterns in [EXAMPLE_FILE].
Write code only — do not run tests or modify other files.
```

### Test Implementation
```
Write tests for [FILE_PATH].

Test:
- Happy path for each public method
- Edge cases: [LIST]
- Error handling: [LIST]

Use the testing patterns from [TEST_EXAMPLE].
Write to [TEST_FILE_PATH].
```

---

## Review Prompts

### Security Review
```
Review [FILE_PATH] for security vulnerabilities.

Check for:
- SQL injection
- XSS
- Auth bypass
- Secret exposure
- Input validation gaps

Report only HIGH confidence issues.
Format: file:line — vulnerability — severity — fix suggestion
```

### Code Quality Review
```
Review [FILE_PATH] for code quality issues.

Check for:
- Naming consistency
- Pattern adherence
- Dead code
- Missing error handling
- Performance anti-patterns

Report only issues with confidence > 80%.
Format: file:line — issue — suggestion
```

---

## Explore Prompts

### File Structure
```
Map the file structure of [DIRECTORY].
List all files with their purpose (1 sentence each).
Identify the main entry point and key abstractions.
Do NOT read file contents unless needed to understand purpose.
```

### Dependency Tracing
```
Trace all imports and references to [SYMBOL] in [DIRECTORY].
Show the dependency chain: who calls it, what it calls.
Create a simple dependency list (not a diagram).
```
