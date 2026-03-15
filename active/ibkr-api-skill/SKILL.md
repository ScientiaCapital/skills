---
name: ibkr-api-skill
description: Interactive Brokers (IBKR) API integration for portfolio management, account queries, and trade execution across multiple account types (Roth IRA, personal brokerage, business). Use when the user mentions IBKR, Interactive Brokers, IB Gateway, TWS API, Client Portal API, brokerage API, portfolio positions, account balances, placing trades via API, multi-account trading, IRA trading restrictions, or wants to build/debug code that connects to Interactive Brokers. Also triggers on "ib_async", "ib_insync", "ibapi", or any IBKR endpoint reference.
---

# IBKR API Skill

Expert guide for building Python integrations with Interactive Brokers across multiple account types.

## Quick Decision: Which API?

| Criterion | TWS API (Recommended) | Client Portal REST API |
|-----------|----------------------|----------------------|
| **Best for** | Automated trading, portfolio mgmt | Web dashboards, light usage |
| **Auth** | Local login via TWS/IB Gateway | OAuth 2.0 JWT |
| **Performance** | Async, low latency, high throughput | REST, slower |
| **Data quality** | Tick-by-tick available | Level 1 only |
| **Multi-account** | All accounts simultaneously | Per-request |
| **Infrastructure** | Local Java app (port 7496/7497) | HTTPS REST calls |
| **Python library** | ib_async (recommended) | requests + OAuth |
| **Cost** | Free | Free |

**Default recommendation**: TWS API via **ib_async** library for all programmatic work.

## Account Architecture

Tim's setup: Roth IRA + Personal Brokerage + THK Enterprises (future business account)

- All linked under single IBKR username/password
- Single API session accesses all linked accounts
- Use `reqLinkedAccounts()` to enumerate account IDs
- Specify account ID per order placement
- Market data subscriptions charged once across all linked accounts
- **One active session per username** — connecting elsewhere closes current session

### IRA-Specific Restrictions (Critical)

| Restriction | Impact |
|-------------|--------|
| No short selling | `placeOrder()` will reject short orders |
| No margin borrowing | Cash-only (no debit balances) |
| No foreign currency borrowing | Must execute FX trade first |
| Futures margin 2x higher | Position sizing affected |
| MLPs/UBTI prohibited | Filter these from IRA order flow |
| Withdrawals USD only | Informational |

## Core API Operations

### Read Operations (Safe — use for all account types)

```python
# Key TWS API functions for portfolio queries
reqLinkedAccounts()        # List all account IDs
reqAccountSummary()        # Balances, buying power, equity (all accounts)
reqPositions()             # Current positions (up to 50 sub-accounts)
reqPositionsMulti()        # Per-account positions (>50 sub-accounts)
reqAccountUpdates()        # Stream account + position data (single account)
reqMktData()               # Real-time Level 1 market data
reqHistoricalData()        # Historical price data
```

### Write Operations (Use with caution — respect IRA restrictions)

```python
placeOrder(account_id, contract, order)  # Place order on specific account
cancelOrder(order_id)                     # Cancel pending order
reqGlobalCancel()                         # Cancel all open orders
```

### Client Portal REST Endpoints (Alternative)

```
GET  /iserver/accounts                        # List accounts
GET  /iserver/account/{id}/positions          # Positions
GET  /iserver/account/{id}/summary            # Balances
POST /iserver/account/{id}/orders             # Place order
GET  /market/candle                           # Historical candles
```

## Python Library: ib_async

**Install**: `pip install ib_async`

**Why ib_async over alternatives:**
- Modern successor to ib_insync (original creator's project continued)
- Native asyncio support
- Implements IBKR binary protocol internally (no need for official ibapi)
- Active maintenance (GitHub: ib-api-reloaded/ib_async)

**Alternatives** (use only if ib_async doesn't meet needs):
- `ib_insync` — Legacy, stable but unmaintained since early 2024
- `ibapi` — Official IBKR library, cumbersome event loop

### Reference: Connection Pattern

See `reference/connection-patterns.md` for:
- IB Gateway setup and configuration
- Connection/reconnection handling
- Session timeout management (6-min ping for CP API)
- Multi-account query patterns
- Error handling and rate limit management

### Reference: Trading Patterns

See `reference/trading-patterns.md` for:
- Order types (market, limit, stop, bracket, IB algos)
- IRA-safe order validation
- Multi-account order routing
- Position sizing with account-type awareness
- Greeks-aware options order flow

## Infrastructure Requirements

1. **IB Gateway** (lightweight) or **TWS** (full UI) running locally
2. **Java 8+** installed
3. **API enabled** in TWS/Gateway settings
4. **Ports**: 7496 (live) / 7497 (paper trading)
5. **Credentials**: Stored in OS credential manager (never hardcode)

## Security Best Practices

- Run IB Gateway on localhost only (no internet exposure)
- Use read-only login for portfolio queries when trading not needed
- Store credentials in macOS Keychain / Linux secret-service
- Implement session timeout handling
- Validate market data subscriptions before placing orders
- Log all order attempts with account ID + timestamp

## Cost Structure

| Item | Cost |
|------|------|
| API access | Free |
| Market data | $5-50/month per exchange subscription |
| Trading commissions | Standard IBKR rates (varies by asset) |
| Account minimums | $500 per account |
| Estimated total | ~$1,500 aggregate minimum; $15-50/month data |

## Integration with Trading-Signals Skill

This skill complements the `trading-signals-skill`:
- **trading-signals** → generates signals, confluence scores, regime detection
- **ibkr-api** → executes trades, queries positions, manages accounts
- Pipeline: Signal generation → Position sizing → IRA validation → Order execution

## IBKR MCP Server (Installed)

**ArjunDivecha/ibkr-mcp-server** is installed and configured:
- **Location:** `~/Desktop/tk_projects/ibkr-mcp-server/`
- **Claude Code:** Added to `~/.claude.json` (user scope)
- **Claude Desktop:** Added to `claude_desktop_config.json`
- **Mode:** Paper trading (port 7497), live trading disabled
- **Safety:** Order cap 1,000 shares, confirmation required

### Available MCP Tools

| Tool | Purpose | Account Types |
|------|---------|---------------|
| `get_portfolio` | Positions + P&L | All accounts |
| `get_account_summary` | Balances, margin, buying power | All accounts |
| `switch_account` | Toggle Roth IRA / Personal / THK | Multi-account |
| `get_market_data` | Real-time quotes | N/A |
| `get_historical_data` | Historical OHLCV | N/A |
| `place_order` | Orders with safety checks | All (IRA restrictions enforced) |
| `check_shortable_shares` | Short availability | Personal/Business only |
| `get_margin_requirements` | Margin needs per security | Personal/Business only |
| `get_borrow_rates` | Borrow costs for shorts | Personal/Business only |
| `short_selling_analysis` | Full short analysis package | Personal/Business only |
| `get_connection_status` | IB Gateway health check | N/A |

### To Activate
1. Start IB Gateway → port 7497 (paper) or 7496 (live)
2. Enable API: Config → API → Settings → "ActiveX and Socket Clients"
3. Add 127.0.0.1 to Trusted IPs
4. Restart Claude Code / Claude Desktop

### Other Community MCP Servers
- `code-rabi/interactive-brokers-mcp` — Client Portal REST API
- `xiao81/IBKR-MCP-Server` — TWS API focused
- `Hellek1/ib-mcp` — Read-only via ib_async (safest)

## Multi-Broker Aggregation

For unified view across IBKR + Robinhood:
- **SnapTrade MCP** (`dangelov/mcp-snaptrade`) — Read-only aggregator, 15+ brokerages, OAuth-based (safe)
- **Alpaca MCP** (official) — Alternative broker with production-ready MCP
- Manual CSV import from Robinhood as fallback (ToS-safe)

See `reference/multi-broker-strategy.md` for aggregation patterns.
