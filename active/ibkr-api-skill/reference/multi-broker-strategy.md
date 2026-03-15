# Multi-Broker Strategy: IBKR + Robinhood

## Table of Contents
1. [Architecture Decision](#architecture-decision)
2. [Robinhood Integration Options](#robinhood-integration-options)
3. [Unified Portfolio View](#unified-portfolio-view)
4. [MCP Server Options](#mcp-server-options)
5. [Recommended Setup](#recommended-setup)

---

## Architecture Decision

### The Reality
- **IBKR**: Official API, production-ready, full trading support
- **Robinhood**: No official stocks/options API. Unofficial libraries violate ToS.

### Decision Matrix

| Approach | IBKR | Robinhood | Risk |
|----------|------|-----------|------|
| Full API both | Official ib_async | robin_stocks (unofficial) | HIGH — RH account suspension |
| API + Read-only | Official ib_async | robin_stocks read-only | MEDIUM — still violates RH ToS |
| API + Aggregator | Official ib_async | SnapTrade OAuth | LOW — officially blessed |
| API + Manual | Official ib_async | CSV export | ZERO — fully compliant |

**Recommendation**: IBKR official API + SnapTrade for Robinhood read-only data.

---

## Robinhood Integration Options

### Option 1: SnapTrade (Recommended — Low Risk)
```
Type: OAuth-based aggregator (read-only)
Security: SOC 2 Type 2 compliant, bank-level encryption
Your credentials: NOT shared with SnapTrade
Capabilities: Positions, balances, order history
Limitations: No trading, no real-time data
MCP Server: dangelov/mcp-snaptrade (GitHub)
```

### Option 2: robin_stocks Library (High Risk)
```
Library: robin_stocks (pip install robin-stocks)
GitHub: jmfernandes/robin_stocks (~2,000 stars)
Capabilities: Full trading, positions, balances, options
Auth: Username + password + 2FA (TOTP)
Risk: ToS violation, account suspension possible
Breakage: 1-3x per year when RH changes endpoints
```

### Option 3: CSV Export (Zero Risk)
```
Method: Account → History → Export All (web app)
Format: CSV with date range selection
Automation: Manual only
Use case: Monthly portfolio snapshots, tax prep
```

### Option 4: Robinhood Crypto API (Official, Crypto Only)
```
Type: Official API (launched 2024)
Scope: Crypto trading ONLY (no stocks/options)
Docs: docs.robinhood.com
Use case: Only if you need programmatic crypto on RH
```

---

## Unified Portfolio View

### Data Model
```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class UnifiedPosition:
    """Cross-broker position representation."""
    broker: str                    # 'IBKR' or 'Robinhood'
    account_id: str
    account_type: str              # 'Roth IRA', 'Individual', 'Business'
    symbol: str
    quantity: float
    avg_cost: float
    current_price: Optional[float]
    market_value: Optional[float]
    unrealized_pnl: Optional[float]
    last_updated: datetime

@dataclass
class UnifiedAccountSummary:
    """Cross-broker account summary."""
    broker: str
    account_id: str
    account_type: str
    net_liquidation: float
    total_cash: float
    buying_power: float
    positions_value: float
    day_pnl: Optional[float]
    last_updated: datetime

def merge_portfolios(
    ibkr_positions: list[UnifiedPosition],
    rh_positions: list[UnifiedPosition],
) -> dict[str, list[UnifiedPosition]]:
    """
    Merge positions from both brokers, grouped by symbol.
    Enables cross-broker concentration analysis.
    """
    merged: dict[str, list[UnifiedPosition]] = {}

    for pos in ibkr_positions + rh_positions:
        if pos.symbol not in merged:
            merged[pos.symbol] = []
        merged[pos.symbol].append(pos)

    return merged
```

---

## MCP Server Options

### For Claude Desktop / Cowork Integration

| Server | Broker | Type | Status | GitHub |
|--------|--------|------|--------|--------|
| interactive-brokers-mcp | IBKR | Full trading | Experimental | code-rabi/interactive-brokers-mcp |
| ib-mcp | IBKR | Read-only | Experimental | Hellek1/ib-mcp |
| ibkr-mcp-server | IBKR | Multi-account | Experimental | ArjunDivecha/ibkr-mcp-server |
| mcp-snaptrade | Multi-broker | Read-only | Stable | dangelov/mcp-snaptrade |
| robinhood-mcp | Robinhood | Read-only | Experimental | verygoodplugins/robinhood-mcp |
| alpaca-mcp-server | Alpaca | Full trading | Production | alpacahq/alpaca-mcp-server |

### Claude Desktop MCP Config Example
```json
{
  "mcpServers": {
    "ibkr": {
      "command": "python",
      "args": ["-m", "ibkr_mcp_server"],
      "env": {
        "IB_HOST": "127.0.0.1",
        "IB_PORT": "7496",
        "IB_CLIENT_ID": "10"
      }
    },
    "snaptrade": {
      "command": "npx",
      "args": ["mcp-snaptrade"],
      "env": {
        "SNAPTRADE_CLIENT_ID": "${SNAPTRADE_CLIENT_ID}",
        "SNAPTRADE_CONSUMER_KEY": "${SNAPTRADE_CONSUMER_KEY}"
      }
    }
  }
}
```

---

## Recommended Setup

### Phase 1: IBKR Only (Immediate)
1. Install IB Gateway on local machine
2. Install ib_async (`pip install ib_async`)
3. Connect to all 3 linked accounts (Roth IRA, Personal, THK Enterprises)
4. Build portfolio dashboard with unified view
5. Integrate with trading-signals-skill for signal → execution pipeline

### Phase 2: Add Robinhood Read-Only (When Ready)
1. Set up SnapTrade account (free tier available)
2. Connect Robinhood via SnapTrade OAuth
3. Pull positions/balances into unified data model
4. OR: Use monthly CSV export as simpler alternative

### Phase 3: MCP Integration (Optional)
1. Evaluate community IBKR MCP servers
2. Consider building custom MCP server wrapping ib_async
3. Add SnapTrade MCP for Robinhood data in Claude Desktop
4. Enables natural language portfolio queries in Cowork

### Cost Comparison

| Component | Monthly Cost |
|-----------|-------------|
| IBKR API | Free |
| IBKR market data | $5-50 |
| SnapTrade (free tier) | Free |
| SnapTrade (paid) | ~$50/mo |
| robin_stocks | Free (but risk) |
| CSV export | Free |
| **Total (recommended)** | **$5-50/mo** |
