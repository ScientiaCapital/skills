---
description: "End of day — verify everything is clean and shipped."
argument-hint: ""
allowed-tools: Read, Bash, Glob
---

# /done — End of Day

## Instructions

1. Check git state:
   ```bash
   git status --short
   git log --oneline -5
   ```

2. If dirty files exist:
   - Show what's uncommitted
   - Ask: "Want me to /ship these or discard?"

3. Quick security check (5 seconds, not a full sweep):
   ```bash
   grep -r "sk-\|AKIA\|ghp_" --include="*.ts" --include="*.py" --include="*.env" . 2>/dev/null | grep -v node_modules | grep -v .git | head -5
   ```

4. Report:
   ```
   ## End of Day: PROJECT_NAME
   | Check | Status |
   |-------|--------|
   | Dirty files | 0 (or list them) |
   | Last commit | message + age |
   | Secrets scan | clean |

   Done. See you tomorrow.
   ```

If everything is clean, just say "All clean. Done for today."

No observer reports. No portfolio metrics. No 6-phase ceremony.
Those are for /end on big feature days.
