# Trading Integration Plan: Unified Portfolio Management

**Owner:** Tim Kipper
**Date:** 2026-03-13
**Status:** Architecture Design
**DA Audit Score:** 7/10 (architecture sound, execution gaps flagged below)

---

## Executive Summary

Connect **trading-signals** (analysis) + **ibkr-api-skill** (execution) + **theta-room** (full-stack trading) + **swaggy-stacks** (monitoring/backtesting) into a unified system for managing 4 accounts:

| Account | Platform | Access Level | Purpose | DA Status |
|---------|----------|-------------|---------|-----------|
| Roth IRA | IBKR | Full API (ib_async) | Long-term, IRA-safe strategies | ⚠️ Verify IRA rules in IBKR account agreement |
| Personal Brokerage | IBKR | Full API (ib_async) | Active trading, options | ✅ Standard |
| THK Enterprises | IBKR (upcoming) | Full API (ib_async) | Business account | ❌ Account not yet created — Phase 4+ |
| Personal Trading | Robinhood | CSV export only | Monitor only, trade manually | ❌ SnapTrade blocked — CSV fallback only |

---

## DA Audit: Critical Blockers (Resolve Before Starting)

> **These 5 items must be resolved before writing any integration code.**

### BLOCKER 1: ib_insync vs NautilusTrader Event Loop Conflict
- **Problem:** Both theta-room and thetaroom use `ib_insync` AND `nautilus_trader[ib]` — they both try to own the asyncio event loop
- **Evidence:** theta-room's nautilus-integration.md contract explicitly states this conflict
- **Decision needed:** Use ib_insync OR NautilusTrader, not both
- **Recommendation:** Use **ib_insync** for Phase 1-3 (more mature, fewer deps). Migrate to NautilusTrader in Phase 5+ if needed
- **Action:** Remove `nautilus_trader` from requirements.txt, delete any nautilus stubs
- **Timeline:** 1 day

### BLOCKER 2: Missing ib_insync Dependency in swaggy-stacks
- **Problem:** `swaggy-stacks/backend/requirements.txt` does NOT list `ib_insync`
- **Evidence:** Broker adapter imports it via lazy loading, but pip install won't include it
- **Action:** Add `ib_insync>=10.0.0` to swaggy-stacks requirements.txt
- **Timeline:** 2 hours

### BLOCKER 3: Robinhood Integration Not Viable via API
- **Problem:** SnapTrade has limited/discontinued Robinhood support. RH actively blocks third-party API access
- **Evidence:** Robinhood ToS prohibits API access; SnapTrade RH connector unreliable
- **Decision:** Use CSV export from Robinhood web app (free, zero risk, manual)
- **Action:** Remove `rh_poller.py` from Phase 1. Add manual CSV import step instead
- **Timeline:** Update plan only (saves 3+ days)

### BLOCKER 4: Cowork Scheduled Tasks File Access & Notifications
- **Problem:** Cowork tasks run in sandboxed sessions. They may NOT have access to `~/Desktop/tk_projects/` or `osascript` for desktop notifications
- **Decision:** Use **Supabase** for portfolio data storage instead of local JSON files. Use **Discord + Gmail** for alerts (skip osascript)
- **Action:** Set up Supabase table for portfolio snapshots. Rewrite alert_router to use HTTP webhooks only
- **Timeline:** 3-5 days

### BLOCKER 5: IBKR Broker Adapter Never Tested with Live IB Gateway
- **Problem:** Both theta-room and swaggy-stacks have IBKR adapters but they've only been tested with synthetic data
- **Evidence:** theta-room defaults to `paper=True`, has blocking `asyncio.sleep()` calls that will cause latency issues
- **Action:** Install IB Gateway on Mac → connect paper trading (port 7497) → run test script → verify positions/orders work
- **Timeline:** 3-5 days

---

## Current State Assessment

### What Actually Exists (DA-Verified)

| Component | Project | Verified Status | DA Notes |
|-----------|---------|----------------|----------|
| IBKR broker adapter | theta-room | ⚠️ Paper-only tested | Has blocking sleep() calls, needs async fix |
| IBKR broker adapter | swaggy-stacks | ⚠️ Missing dependency | ib_insync not in requirements.txt |
| Alpaca broker | Both projects | ✅ Tested (synthetic) | Working with synthetic data |
| Signal generation (7-layer) | theta-room | ✅ Exists | Tested with synthetic data only |
| Signal generation (multi-source) | swaggy-stacks | ✅ Exists | RSI, MACD, BB, LLM, Markov |
| Risk management | swaggy-stacks | ✅ Exists | Position sizing, loss limits, Greeks |
| Celery task system | swaggy-stacks | ✅ Exists | Market data, trading, analysis, notifications |
| Prometheus + Grafana | swaggy-stacks | ⚠️ Config exists | Dashboards are JSON configs — deployment status unknown |
| NautilusTrader | theta-room/thetaroom | ❌ Not wired | In requirements but never imported. Event loop conflict with ib_insync |
| Sentiment pipeline | signal-siphon | ✅ MVP deployed | Live at signal-siphon-scientia-capital.vercel.app |
| Trading-signals skill | skills/active/ | ✅ Stable | Analysis-only, no execution capability |
| IBKR API skill | skills/active/ | ✅ New | Connection patterns, IRA validation, reference docs |
| Robinhood integration | Any project | ❌ Not viable | No official API. SnapTrade unreliable. CSV only |

### What's Missing (The Gaps)

1. **Unified account view** — No single dashboard showing IBKR (2-3 accounts) + RH positions together
2. **Signal → Execution pipeline** — trading-signals skill produces analysis but can't execute
3. **Cross-account risk management** — No aggregate portfolio Greeks, no cross-account exposure limits
4. **Robinhood data ingestion** — CSV export only (manual), no real-time API
5. **Alert system** — No unified alerts across Gmail + Discord
6. **Scheduled monitoring** — No automated pre-market/intraday/EOD checks that span all accounts
7. **IRA compliance gate** — swaggy-stacks IBKR adapter doesn't enforce IRA restrictions
8. **Account routing** — No logic to route signals to the right account based on strategy type

---

## Integration Architecture

### Layer 1: Data Ingestion (Cron — runs on your Mac)

```
┌─────────────────────────────────────────────────────────┐
│  CRON JOBS (launchd on macOS, every 5-30 min)           │
│                                                         │
│  ibkr_poller.py ─── IB Gateway ─── 2-3 accounts        │
│    ├── positions, balances, Greeks, P&L                 │
│    ├── open orders, execution reports                   │
│    └── market data (watchlist quotes)                   │
│    └── OUTPUT → Supabase portfolio_snapshots table      │
│                                                         │
│  market_scanner.py ─── Alpaca (free tier) ─── data      │
│    ├── VIX, sector ETFs, regime indicators              │
│    ├── unusual options volume                           │
│    └── earnings calendar                                │
│    └── OUTPUT → Supabase market_data table              │
│                                                         │
│  rh_csv_import.py ─── manual CSV from RH web ─── daily │
│    ├── positions, balances (manual export)              │
│    └── OUTPUT → Supabase rh_positions table             │
│                                                         │
│  ⚠️ DA NOTE: Use Supabase instead of local JSON files  │
│     so Cowork scheduled tasks can access the data       │
└─────────────────────────────────────────────────────────┘
```

### Layer 2: Analysis & Signals (Cowork Scheduled Tasks)

```
┌─────────────────────────────────────────────────────────┐
│  COWORK SCHEDULED TASKS (created ✅)                    │
│                                                         │
│  PRE-MARKET (6:00 AM CT / 7:00 AM ET) ✅ Created       │
│    ├── Load overnight data from Supabase                │
│    ├── Run Markov regime detection                      │
│    ├── Scan for gaps, pre-market movers                 │
│    ├── Check all open positions against stops           │
│    ├── Generate watchlist for the day                   │
│    └── Alert: regime changes, gap-ups/downs on holdings │
│                                                         │
│  MARKET HOURS (every 30 min, 8:30-2:30 CT) ✅ Created  │
│    ├── Position P&L check (all accounts)               │
│    ├── Greeks snapshot (theta decay, delta drift)       │
│    ├── Options flow scan (unusual volume)               │
│    ├── Stop-loss validation                            │
│    └── Alert: P&L threshold breaches, Greeks extremes   │
│                                                         │
│  EOD (3:15 PM CT / 4:15 PM ET) ✅ Created              │
│    ├── Daily P&L summary (all accounts)                │
│    ├── Positions that need attention (roll/close)       │
│    ├── Tomorrow's earnings on holdings                  │
│    ├── Weekly theta decay projection                   │
│    └── Alert: EOD summary to all channels              │
│                                                         │
│  WEEKLY (Friday 4:30 PM CT) — TODO: Create             │
│    ├── Portfolio performance vs benchmarks              │
│    ├── Greeks rebalancing recommendations               │
│    ├── Regime trend analysis (weekly view)              │
│    └── Account-specific reports (IRA vs Personal)       │
└─────────────────────────────────────────────────────────┘
```

### Layer 3: Execution & Routing (Manual Approval + Auto-Execute)

```
┌─────────────────────────────────────────────────────────┐
│  SIGNAL → ACCOUNT ROUTER                                │
│                                                         │
│  Signal from trading-signals skill                      │
│    │                                                    │
│    ├── Is it IRA-safe? ──── YES ──→ Route to Roth IRA  │
│    │   (no shorts, no margin,       (conservative)      │
│    │    no naked calls, no MLPs)                        │
│    │                                                    │
│    ├── Is it options/active? ──→ Route to Personal IBKR │
│    │   (all strategies allowed)     (aggressive)        │
│    │                                                    │
│    ├── Is it business? ────────→ Route to THK account   │
│    │   (business expense,           (when ready)        │
│    │    hedging, treasury)                              │
│    │                                                    │
│    └── Is it RH-only? ────────→ Alert only (no execute) │
│        (manual trade on app)                            │
│                                                         │
│  APPROVAL MODES:                                       │
│    ├── Paper trading: Auto-execute (no approval)        │
│    ├── Live < $500: Auto-execute with notification      │
│    ├── Live > $500: Discord + email alert, wait for OK  │
│    └── IRA trades: Always require manual approval       │
│                                                         │
│  ⚠️ DA NOTE: IRA restrictions need verification against │
│     actual IBKR IRA account agreement (15 min task)     │
└─────────────────────────────────────────────────────────┘
```

### Layer 4: Alert Distribution

```
┌─────────────────────────────────────────────────────────┐
│  ALERT ROUTER (by severity)                             │
│                                                         │
│  🔴 CRITICAL (immediate — all channels)                │
│    ├── Portfolio drawdown > 5%                          │
│    ├── VIX spike > 35 (regime override)                 │
│    ├── Margin call warning                              │
│    ├── Stop-loss triggered                              │
│    └── → Gmail + Discord                                │
│                                                         │
│  🟡 WARNING (within 5 min)                             │
│    ├── Position P&L > -3% intraday                     │
│    ├── Greeks drift (delta > 0.7 or vega > threshold)  │
│    ├── Options approaching expiry (< 7 DTE)            │
│    └── → Discord                                        │
│                                                         │
│  🟢 INFO (batched, next scheduled check)               │
│    ├── New signal generated (confluence > 0.7)          │
│    ├── Regime change detected                          │
│    ├── Earnings on holdings (next 5 days)              │
│    └── → Discord only                                   │
│                                                         │
│  📊 REPORT (scheduled)                                 │
│    ├── Pre-market brief                                │
│    ├── EOD summary                                     │
│    ├── Weekly report                                   │
│    └── → Gmail (formatted) + Discord (summary)         │
│                                                         │
│  ⚠️ DA NOTE: Desktop notifications (osascript) removed │
│     — Cowork sandbox cannot access macOS notifications. │
│     Discord + Gmail are reliable from sandbox.          │
└─────────────────────────────────────────────────────────┘
```

---

## Manipulation Detection

### Regime Anomaly Detection
- **VIX/SPX divergence** — VIX dropping while SPX drops = artificial suppression
  - ⚠️ DA: VIX data via `yfinance` (free) — add `yf.download("^VIX")` to market_scanner.py
- **Volume/price divergence** — price moving on thin volume = manipulation risk
  - ✅ Implementable with Alpaca free data
- **After-hours gap analysis** — overnight futures manipulation detection
  - ✅ Implementable with Alpaca extended hours data
- **Dark pool percentage** — if dark pool volume > 45% of total, flag it
  - ❌ DA: Dark pool data requires paid feeds ($100+/month). Use Alpaca detailed trades as rough proxy, or defer this feature

### Position Protection
- **Trailing stops auto-tighten** when regime shifts to "distribution" or "bear volatile"
- **Greeks drift alerts** — if portfolio delta swings > 20% intraday, something's wrong
- **Correlation breakdown** — if normally correlated positions diverge, flag for review
  - ⚠️ DA: Requires historical correlation baseline stored in Supabase. Weekly recalculation task needed
- **Earnings surprise buffer** — auto-widen stops 48 hrs before earnings on holdings

### Market Structure Alerts
- **Circuit breaker proximity** — alert if any major index approaches -7% intraday
- **Options expiration pinning** — detect max-pain gravitational pull on holdings
  - ⚠️ DA: Max-pain calculation implementable. Real-time pinning detection is complex — start with EOD max-pain check
- **Sector rotation speed** — if sector leadership changes in < 3 days, flag regime shift
- **Bond/equity correlation flip** — if traditional correlations break, alert immediately

---

## Implementation Roadmap (DA-Adjusted: 7-8 Weeks Realistic)

### Phase 0: Blockers (Week 1) ← NEW — DO THIS FIRST
**Goal:** Resolve the 5 critical blockers before any integration work

- [ ] **BLOCKER 1:** Choose ib_insync over NautilusTrader. Remove nautilus_trader from requirements.txt (1 day)
- [ ] **BLOCKER 2:** Add `ib_insync>=10.0.0` to swaggy-stacks requirements.txt (2 hours)
- [ ] **BLOCKER 3:** Remove SnapTrade/rh_poller from plan. Robinhood = CSV only (update plan, 4 hours)
- [ ] **BLOCKER 4:** Set up Supabase tables for portfolio data instead of local JSON (2-3 days)
  - Tables: `portfolio_snapshots`, `market_data`, `signals`, `alerts`
- [ ] **BLOCKER 5:** Install IB Gateway on Mac. Test IBKR adapter with paper trading port 7497 (3-5 days)
  - Fix blocking `asyncio.sleep()` calls in theta-room's adapter
  - Verify `managedAccounts()` returns both Roth IRA and Personal
- [ ] Set up Discord server + webhook URL (2 hours)
- [ ] Verify Tim's IBKR IRA account restrictions (log in → Account Settings, 15 min)

### Phase 1: Data Flow (Week 2-3)
**Goal:** Get all account data flowing into Supabase

- [ ] Create `ibkr_poller.py` — ib_insync → Supabase (positions, balances, Greeks, P&L)
- [ ] Create `market_scanner.py` — Alpaca free tier → Supabase (VIX, sectors, options flow)
- [ ] Create `rh_csv_import.py` — manual CSV → Supabase (RH positions, run as needed)
- [ ] Create `alert_router.py` — Discord webhook + Gmail API distribution
- [ ] Create launchd plists for cron jobs (every 15 min during market hours)
- [ ] Verify: all account data visible in Supabase, alerts firing to Discord
- [ ] **Test for 1 week** before moving to Phase 2

### Phase 2: Monitoring (Week 4-5)
**Goal:** Automated checks catch market changes before you do

- [ ] Update Cowork scheduled tasks to read from Supabase (not local files)
- [ ] Wire pre-market brief to use live Supabase data
- [ ] Wire intraday monitor to use live Supabase data
- [ ] Wire EOD summary to use live Supabase data
- [ ] Create weekly report task (Friday 4:30 PM CT)
- [ ] Add VIX/regime monitoring to market_scanner.py
- [ ] Test alert flow end-to-end (trigger → Gmail + Discord)
- [ ] **Test for 1 week** before moving to Phase 3

### Phase 3: Signal Integration (Week 6-7)
**Goal:** Trading-signals skill connects to live data and routes to accounts

- [ ] Update trading-signals skill reference docs to consume Supabase snapshots
- [ ] Build signal → account router (IRA-safe check, size check)
- [ ] Wire theta-room's IBKR broker adapter for paper execution
- [ ] Wire swaggy-stacks' signal generator for additional confluence
- [ ] Add IRA compliance gate to ibkr-api-skill
- [ ] Test: signal → routed to correct account → paper executed
- [ ] **Paper trade for 2 weeks** before Phase 4

### Phase 4: Live Trading (Week 8+)
**Goal:** Switch from paper to live with safety rails

- [ ] Switch IB Gateway to live (port 7496)
- [ ] Enable approval modes (auto < $500, manual > $500, always manual for IRA)
- [ ] Add cross-account aggregate risk checks
- [ ] Weekly performance reporting (Cowork scheduled task)
- [ ] Monitor for 2 weeks at small position sizes before scaling up
- [ ] Set up THK Enterprises IBKR account (when ready)

---

## File Structure (New Files Needed)

```
~/Desktop/tk_projects/
├── portfolio-data/                    # NEW — unified data layer
│   ├── pollers/
│   │   ├── ibkr_poller.py            # ib_insync → Supabase snapshots
│   │   ├── rh_csv_import.py          # Manual CSV → Supabase (replaces rh_poller.py)
│   │   └── market_scanner.py         # VIX, regime, options flow → Supabase
│   ├── alerts/
│   │   ├── alert_router.py           # Severity-based distribution
│   │   ├── gmail_sender.py           # Gmail API integration
│   │   └── discord_webhook.py        # Discord webhook POST
│   ├── config.py                     # Account configs, thresholds, Supabase URL
│   ├── requirements.txt              # ib_insync, supabase-py, httpx, yfinance
│   └── launchd/
│       ├── com.tk.ibkr-poller.plist  # Every 15 min market hours
│       └── com.tk.market-scan.plist  # Every 10 min market hours (not 5 — rate limits)
│
├── theta-room/                        # EXISTING — add signal consumer
│   └── backend/
│       ├── brokers/ibkr_broker.py    # Exists ✅ — fix async sleeps
│       └── services/
│           └── signal_consumer.py    # NEW — ingest external signals
│
├── swaggy-stacks/                     # EXISTING — add signal endpoint + fix deps
│   └── backend/
│       ├── requirements.txt          # FIX: add ib_insync>=10.0.0
│       └── app/
│           ├── brokers/ibkr_broker.py # Exists ✅
│           ├── signals/              # NEW directory
│           │   ├── signal_receiver.py # Webhook endpoint
│           │   ├── signal_validator.py # Risk + IRA compliance
│           │   └── account_router.py  # Route to correct account
│           └── tasks/
│               └── signal_processing.py # NEW — Celery periodic check
│
└── skills/active/
    ├── trading-signals-skill/         # EXISTING — add live data hooks
    │   └── reference/
    │       └── live-portfolio.md      # NEW — how to consume Supabase data
    └── ibkr-api-skill/               # EXISTING ✅
```

---

## Scheduled Tasks (Created ✅)

| Task | Schedule | Status |
|------|----------|--------|
| `pre-market-brief` | 6:00 AM CT, Mon-Fri | ✅ Created — next run in 2 days |
| `intraday-monitor` | Every 30 min 8:30 AM - 2:30 PM CT, Mon-Fri | ✅ Created — next run in 2 days |
| `eod-summary` | 3:15 PM CT, Mon-Fri | ✅ Created — next run in 2 days |
| `weekly-report` | Friday 4:30 PM CT | TODO — create next |

> ⚠️ **DA NOTE:** These tasks are created but will read from Supabase (Phase 1 dependency). Until pollers are writing data to Supabase, tasks will report "no data available." This is expected behavior.

---

## Cost Estimate (DA-Verified)

| Component | Monthly Cost | DA Notes |
|-----------|-------------|----------|
| IB Gateway | Free | Runs locally on Mac ✅ |
| IBKR market data | $10-30/month | Shared across linked accounts ✅ |
| ~~SnapTrade~~ | ~~Free~~ | ❌ Removed — RH not supported |
| Discord | Free | Webhook is free ✅ |
| Gmail API | Free | Connected in Cowork ✅ |
| Cowork scheduled tasks | Free | Part of Claude subscription ✅ |
| Supabase | Free tier | 500MB, 50K rows — sufficient for snapshots ✅ |
| LLM costs (analysis) | ~$50-100/month | DeepSeek/Qwen for bulk, Claude for decisions |
| Claude (scheduled tasks) | ~$10-15/month | 3 tasks × 5 days/week × 4 weeks |
| **Total** | **$70-145/month** | Well under $500 threshold ✅ |

### Cheaper Alternative
- Use only DeepSeek V3 for all analysis ($0.27/1M tokens)
- Use Alpaca free data instead of IBKR market data subscription
- **Cheaper total: $15-30/month**

---

## MCP/Plugin Ecosystem (Available Now)

| Tool | Type | Status | What It Does |
|------|------|--------|-------------|
| Alpaca MCP Server | Official MCP | ✅ Production | Stocks, ETFs, crypto, options trading |
| SnapTrade MCP | Community MCP | ⚠️ Read-only | Multi-broker aggregator (RH support limited) |
| IBKR MCP Servers | Community (9+) | ⚠️ Experimental | Various IBKR integrations on GitHub |
| Anthropic financial-services-plugins | Official Plugin | ✅ Production | Morningstar, FactSet, S&P Global connectors |
| trading-signals skill | Local Skill | ✅ Stable | 5 TA methodologies, 25+ options strategies |
| ibkr-api-skill | Local Skill | ✅ New | Connection patterns, IRA validation |

### Community IBKR MCP Servers (for future evaluation)
1. `code-rabi/interactive-brokers-mcp` — Full trading support
2. `rcontesti/IB_MCP` — FastMCP + IB Web API
3. `xiao81/IBKR-MCP-Server` — Portfolio data + quotes
4. `Hellek1/ib-mcp` — Read-only, ib_async (safest)
5. `ArjunDivecha/ibkr-mcp-server` — Multi-account + short selling
6. `GaoChX/ibkr-mcp-server` — FastMCP 2.0 + StreamableHTTP

> **Recommendation:** Evaluate `Hellek1/ib-mcp` (read-only, uses ib_async) for Claude Desktop natural-language queries after Phase 2 is stable.

---

## DA Audit Summary

### What Passed Audit ✅
- ib_insync recommendation is correct and well-justified
- Multi-account IBKR architecture is accurate
- Signal generation methodologies exist and are tested (synthetic)
- Alpaca broker adapter works
- Cost estimates are realistic ($70-145/month)
- IBKR market data is per-user, shared across accounts
- Architecture layers (ingestion → analysis → routing → alerts) are sound

### What Got Flagged ⚠️
- IRA restrictions not sourced to official IBKR docs (15 min verification needed)
- IBKR adapter has blocking sleep() calls (async fix needed)
- ib_insync missing from swaggy-stacks requirements
- Prometheus/Grafana deployment status unknown
- Signals tested with synthetic data only (no live market validation)
- Correlation breakdown and max-pain detection not yet implemented

### What Was Removed/Changed ❌
- SnapTrade for Robinhood → replaced with CSV export
- Desktop notifications (osascript) → removed, Discord + Gmail only
- Local JSON snapshots → replaced with Supabase
- NautilusTrader → deferred to Phase 5+ (event loop conflict)
- 5-week timeline → extended to 7-8 weeks (realistic for full-time BDR)
- market_scanner every 5 min → changed to every 10 min (rate limits)

### Top 5 Things Tim Must Verify Personally
1. **IBKR IRA account restrictions** — log in → Account Settings → screenshot rules (15 min)
2. **IB Gateway install + paper test** — does `managedAccounts()` return both accounts? (3-5 days)
3. **Fix async sleeps** in theta-room IBKR adapter before any integration (1 day)
4. **Cowork scheduled task reliability** — does pre-market-brief actually fire Monday? (wait and verify)
5. **End-to-end alert test** — trigger a fake CRITICAL alert → verify Gmail + Discord receive it (1 hour)

---

## GTME Lens

| Metric | Value |
|--------|-------|
| **GTM motion enabled** | Automated portfolio intelligence → faster trading decisions → more time for BDR work |
| **Operational leverage** | 3 scheduled tasks replace ~45 min/day of manual market checking |
| **Cost per action** | ~$2.30/day for automated monitoring ($70/month ÷ 30 days) |
| **Portfolio evidence** | Multi-system integration, event-driven architecture, risk management automation |
| **JTBD** | "When markets move fast, I need to know what changed in my positions without manually checking 4 accounts" |
