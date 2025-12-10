# PROJECT_CONTEXT.md Template

Copy this template to `<project-root>/.claude/PROJECT_CONTEXT.md` and fill in.

```markdown
# <project-name>

**Branch**: <current-branch> | **Updated**: <YYYY-MM-DD>

## Status
<2-3 sentences describing current state of project>

## Today's Focus
1. [ ] <task-1>
2. [ ] <task-2>
3. [ ] <task-3>

## Done (This Session)
- <populated when session ends>

## Blockers
- <none or list blockers>

## Quick Commands
```bash
# Development
<common-dev-command>

# Testing
<test-command>

# Build
<build-command>
```

## Tech Stack
<single line, e.g.: Python 3.11 | FastAPI | PostgreSQL | Supabase>

## Key Files
- `<path/to/important/file>` - <what it does>
- `<path/to/config>` - <configuration purpose>

## Notes
<any other context for next session>
```

---

## Example: ThetaRoom

```markdown
# ThetaRoom

**Branch**: feature/confluence-scoring | **Updated**: 2025-12-10

## Status
Implementing multi-methodology confluence detection system. Elliott Wave analyzer complete, working on Wyckoff phase detection.

## Today's Focus
1. [ ] Complete Wyckoff phase state machine
2. [ ] Add Fibonacci golden zone detection
3. [ ] Wire up confluence scoring

## Done (This Session)
- Elliott Wave validation rules implemented
- Added crypto time multiplier (0.6x)

## Blockers
- None

## Quick Commands
```bash
# Development
python -m uvicorn app.main:app --reload

# Testing
pytest tests/ -v

# Build
docker build -t thetaroom .
```

## Tech Stack
Python 3.11 | FastAPI | PostgreSQL | yfinance | CCXT

## Key Files
- `app/analysis/elliott_wave.py` - Wave detection
- `app/analysis/confluence.py` - Multi-method scoring
- `app/config.py` - Trading parameters

## Notes
Using 0.6x time multiplier for crypto (faster cycles than traditional markets)
```

---

## Example: Signal-Siphon

```markdown
# Signal-Siphon

**Branch**: main | **Updated**: 2025-12-10

## Status
Production deployed. Discovery Feed working. Need to configure Supabase redirect URLs for magic link auth.

## Today's Focus
1. [ ] Configure Supabase redirect URLs
2. [ ] Run Twitter scraper pipeline
3. [ ] Test magic link auth flow

## Done (This Session)
- Deployed to Vercel
- Fixed footer styling

## Blockers
- Supabase redirect URLs need manual configuration in dashboard

## Quick Commands
```bash
# Frontend
cd frontend && npm run dev

# Backend pipeline
cd backend && python run_pipeline.py

# Deploy
vercel --prod
```

## Tech Stack
React | TypeScript | Vite | Supabase | Python | Gemini Flash

## Key Files
- `frontend/src/components/Feed/FeedPage.tsx` - Main feed UI
- `backend/run_pipeline.py` - Scraper orchestration
- `backend/analyzer/sentiment_analyzer.py` - Gemini sentiment

## Notes
Turkish blue (#2E5090) theme. Evil eye branding. No mock data in production.
```
