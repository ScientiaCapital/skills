# Daily Trading Workflow

Automate your daily trading prep using Claude's two scheduling systems. The goal: by market open, you already know the regime, key levels, and watchlist — no manual scanning needed.

## Two-Tier Scheduling

Claude offers two ways to schedule recurring work. Use both — they serve different purposes.

### Desktop Scheduled Tasks (Persistent)

- Survive restarts and session closures
- Spawn a fresh Claude session each run
- macOS and Windows support
- Catch-up logic: missed runs execute on next launch (7-day lookback)
- Live at `~/.claude/scheduled-tasks/<name>/SKILL.md`
- No expiry — run until you delete them

### /loop + CronCreate (Session-Scoped)

- Run inside your current terminal session
- Fire between turns (while Claude is idle)
- Any cron expression via CronCreate, or simple interval via `/loop`
- 3-day auto-expiry — they disappear if not refreshed
- Max 50 concurrent tasks per session
- Any platform (macOS, Linux, Windows, SSH)

**When to use which:** Desktop tasks for prep that should run whether or not you're at the terminal. /loop for monitoring that only matters while you're actively trading.

## Four Time Anchors

A trading day has four natural checkpoints. Each maps to a scheduling mechanism.

### Pre-Market (4:00 AM ET) -- Desktop Scheduled Task

Run overnight analysis before you wake up. By the time you check your phone, the report is waiting.

**What it does:**
- Overnight gaps scan: futures (ES, NQ, YM) vs previous close
- Global market summary: Asia close, Europe mid-session
- Key levels from previous session (Fibonacci retracements, support/resistance)
- Regime check: Markov state + VIX level + any overnight shifts
- News/earnings calendar for the day
- Watchlist generation based on overnight movers

**CronCreate equivalent:** `0 4 * * 1-5` (weekdays only)

### Market Open (9:25 AM ET) -- Desktop Scheduled Task

Five minutes before the bell. Fresh data hits — update everything.

**What it does:**
- Turtle System 1/2 breakout check (20-day, 55-day Donchian channels)
- Options flow scanner: unusual volume, smart money bets, large block trades
- Regime detection update with pre-market data
- Position review: Greeks snapshot, delta exposure, theta decay overnight
- Opening gap analysis: fade or follow based on gap size and regime

**CronCreate equivalent:** `25 9 * * 1-5`

### Intraday Monitoring -- /loop (Session-Scoped)

These run while your terminal is open during trading hours. Close the terminal and they stop — which is exactly what you want for active monitoring.

```
/loop 5m check my open positions for stop hits and delta drift
/loop 15m scan for unusual options flow on my watchlist
/loop 30m update regime detection with latest data
```

**Why different intervals:** Position stops need fast checks (5m). Options flow patterns take time to develop (15m). Regime shifts are slow-moving — checking every 30 minutes is plenty. More frequent just adds noise.

### EOD Review (4:00 PM ET) -- Desktop Scheduled Task

Market close wrap-up. Runs whether you remember or not.

**What it does:**
- P&L reconciliation: actual vs expected, slippage analysis
- Regime state update with closing data
- Next-day watchlist generation (scans for setups forming)
- Position roll/close recommendations: flag anything with DTE < 21
- Portfolio Greeks summary: net delta, gamma exposure, theta earned today

**CronCreate equivalent:** `0 16 * * 1-5`

## Desktop Scheduled Task Templates

Drop these into `~/.claude/scheduled-tasks/<name>/SKILL.md` to activate.

### Template 1: Pre-Market Analysis

```markdown
---
name: pre-market-analysis
description: Daily pre-market trading prep — runs at 4:00 AM ET weekdays
---
Load the trading-signals skill. Run pre-market analysis:
1. Check overnight futures (ES, NQ, YM) for gaps > 0.5%
2. Pull previous session's high/low/close for SPY, QQQ, IWM
3. Calculate Fibonacci retracement levels from yesterday's range
4. Run Markov regime detection on SPY, QQQ, BTC using latest data
5. Check today's earnings calendar and economic releases
6. Scan watchlist for unusual pre-market volume (> 2x average)
7. Write summary to ~/trading/daily/YYYY-MM-DD-premarket.md
```

### Template 2: Market Open Scanner

```markdown
---
name: market-open-scanner
description: Opening bell analysis — runs at 9:25 AM ET weekdays
---
Load the trading-signals skill. Run market open scan:
1. Check Turtle System 1 (20-day) and System 2 (55-day) breakouts on watchlist
2. Scan options chains for unusual activity: volume > 3x OI, large block trades
3. Update regime detection with current pre-market data
4. Review all open positions: current Greeks, distance to stops, P&L
5. Analyze opening gap: size, direction, regime context (fade vs follow)
6. Generate 3 highest-conviction trade ideas with confluence scores
7. Write summary to ~/trading/daily/YYYY-MM-DD-open.md
```

### Template 3: EOD Portfolio Review

```markdown
---
name: eod-portfolio-review
description: End-of-day portfolio review — runs at 4:00 PM ET weekdays
---
Load the trading-signals skill. Run end-of-day review:
1. Calculate daily P&L across all positions (realized + unrealized)
2. Update Markov regime detection with closing data
3. Flag positions with DTE < 21 for roll or close decision
4. Check portfolio-level Greeks: net delta, total gamma, theta/day
5. Verify no single position exceeds 2% portfolio risk
6. Scan for new setups forming on watchlist (breakout candidates, accumulation phases)
7. Generate next-day watchlist ranked by confluence score
8. Write summary to ~/trading/daily/YYYY-MM-DD-eod.md
```

## MCP Integration for Live Data

The Alpaca MCP server bridges Claude to live market data and order placement. No code needed — Claude talks to the MCP layer in natural language, and the server handles API calls.

**What Alpaca MCP provides:**
- Historical bars (1m to 1M timeframes)
- Live quotes and snapshots
- Account positions and balances
- Order placement (market, limit, stop, bracket)
- Options chain data

**Pattern:** Claude gets data from MCP -> runs analysis using trading-signals skill -> writes report (or places orders if you authorize it).

**Example flow in a scheduled task:**
```
Claude spawns -> loads trading-signals skill -> calls Alpaca MCP for SPY bars
-> calculates Fibonacci levels + regime -> writes ~/trading/daily/report.md
```

This means your 4 AM pre-market task can pull real data, run real analysis, and have a report ready — all without you writing any code.

## Session /loop Examples

### Syntax

```
/loop 5m <prompt>                              # Run every 5 minutes
/loop check positions every 5 minutes          # Natural language interval
/loop 20m /trading-signals check SPY regime    # Chain with another skill
```

Default interval is 10 minutes if you don't specify.

### Common Trading Loops

```
# Position monitoring
/loop 5m check my open positions for stop hits, delta drift > 0.10, and any approaching earnings dates

# Options flow
/loop 15m scan for unusual options flow on SPY, QQQ, AAPL, TSLA — flag volume > 3x open interest

# Regime shifts
/loop 30m update regime detection for SPY and BTC, alert if state transition probability > 40%

# End-of-day reminder
remind me at 3pm to review positions before close
```

### Loop + Skill Chaining

```
# Combine trading-signals with other skills
/loop 20m /trading-signals check SPY regime then /risk-management verify portfolio limits
```

## Important Caveats

**Timing:**
- All times are LOCAL timezone, not UTC — your system clock determines when tasks fire
- Jitter: recurring tasks can run up to 10% late; one-shot tasks can fire ~90 seconds early
- For precision, use :03 or :07 instead of :00 or :30 (avoids the jitter window)

**Session /loop limits:**
- 3-day auto-expiry if not refreshed
- Max 50 concurrent tasks per session
- Session ends = all loops stop (by design)

**Desktop Scheduled Tasks limits:**
- No expiry — run indefinitely until deleted
- Catch up missed runs within 7-day lookback window
- Each run spawns a fresh session (no memory of previous runs unless you write to files)

**Global kill switch:**
- Set `CLAUDE_CODE_DISABLE_CRON=1` to disable all scheduling (both /loop and Desktop tasks)

**Cost awareness:**
- Each scheduled task run consumes API tokens — a 4 AM task that loads trading-signals and calls Alpaca MCP might cost $0.10-0.50 per run
- Four daily tasks at $0.30 average = ~$6/week, ~$25/month
- /loop costs depend on interval and prompt complexity — 5m loops add up fast

## Integration with Other References

- **Regime detection:** `reference/markov-regime.md` — the 4-state and 7-state models that drive strategy selection
- **Turtle breakouts:** `reference/turtle-trading.md` — System 1/2 breakout rules used in market open scan
- **Options flow:** `reference/options-trading.md` — Greeks analysis for position reviews
- **Risk management:** `reference/risk-management.md` — portfolio limits checked in EOD review
- **Fibonacci levels:** `reference/fibonacci.md` — key levels computed in pre-market analysis
