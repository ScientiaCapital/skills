# IBKR Trading Patterns

## Table of Contents
1. [Order Types](#order-types)
2. [IRA-Safe Order Validation](#ira-safe-order-validation)
3. [Multi-Account Order Routing](#multi-account-order-routing)
4. [Options Order Flow](#options-order-flow)
5. [Position Sizing](#position-sizing)

---

## Order Types

### Basic Orders via ib_async
```python
from ib_async import IB, Stock, Option, Order, LimitOrder, MarketOrder, StopOrder

# Stock contract
aapl = Stock('AAPL', 'SMART', 'USD')

# Market order
market_order = MarketOrder('BUY', 100)

# Limit order
limit_order = LimitOrder('BUY', 100, limitPrice=175.50)

# Stop order
stop_order = StopOrder('SELL', 100, stopPrice=170.00)

# Bracket order (entry + take-profit + stop-loss)
bracket = ib.bracketOrder(
    action='BUY',
    quantity=100,
    limitPrice=175.50,
    takeProfitPrice=185.00,
    stopLossPrice=170.00
)
```

### Advanced Order Types
```python
# Trailing stop (percentage)
from ib_async import Order
trailing_stop = Order(
    action='SELL',
    orderType='TRAIL',
    totalQuantity=100,
    trailingPercent=5.0,  # 5% trailing stop
)

# Adaptive algo (IBKR smart routing)
adaptive_order = Order(
    action='BUY',
    orderType='LMT',
    totalQuantity=100,
    lmtPrice=175.50,
    algoStrategy='Adaptive',
    algoParams=[{'tag': 'adaptivePriority', 'value': 'Normal'}],
)

# TWAP (Time-Weighted Average Price)
twap_order = Order(
    action='BUY',
    orderType='LMT',
    totalQuantity=1000,
    lmtPrice=175.50,
    algoStrategy='Twap',
    algoParams=[
        {'tag': 'startTime', 'value': '09:30:00 US/Eastern'},
        {'tag': 'endTime', 'value': '16:00:00 US/Eastern'},
    ],
)
```

---

## IRA-Safe Order Validation

### Pre-Order Validation
```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class AccountRules:
    """Trading rules by account type."""
    can_short: bool
    can_use_margin: bool
    can_borrow_currency: bool
    can_trade_mlps: bool
    futures_margin_multiplier: float

ACCOUNT_RULES = {
    'IRA': AccountRules(
        can_short=False,
        can_use_margin=False,
        can_borrow_currency=False,
        can_trade_mlps=False,
        futures_margin_multiplier=2.0,
    ),
    'Individual': AccountRules(
        can_short=True,
        can_use_margin=True,
        can_borrow_currency=True,
        can_trade_mlps=True,
        futures_margin_multiplier=1.0,
    ),
    'Business': AccountRules(
        can_short=True,
        can_use_margin=True,
        can_borrow_currency=True,
        can_trade_mlps=True,
        futures_margin_multiplier=1.0,
    ),
}

def validate_order_for_account(
    action: str,
    contract,
    account_type: str,
    quantity: float,
) -> tuple[bool, Optional[str]]:
    """
    Validate order against account-type restrictions.
    Returns (is_valid, rejection_reason).
    """
    rules = ACCOUNT_RULES.get(account_type)
    if not rules:
        return False, f"Unknown account type: {account_type}"

    # Check short selling
    if action == 'SELL' and quantity < 0 and not rules.can_short:
        return False, f"Short selling not allowed in {account_type} accounts"

    # Check MLP restriction
    if hasattr(contract, 'secType') and contract.secType == 'STK':
        # Would need MLP lookup table
        pass

    return True, None
```

---

## Multi-Account Order Routing

### Route Order to Specific Account
```python
async def place_order_on_account(
    ib: IB,
    account_id: str,
    contract,
    order: Order,
    account_type: str = 'Individual',
    dry_run: bool = True,
) -> Optional[dict]:
    """
    Place order on specific account with validation.
    Set dry_run=True for paper verification without execution.
    """
    # Validate against account rules
    is_valid, reason = validate_order_for_account(
        order.action, contract, account_type, order.totalQuantity
    )
    if not is_valid:
        return {'status': 'REJECTED', 'reason': reason}

    # Set account on order
    order.account = account_id

    if dry_run:
        # Use whatIf to simulate without executing
        what_if = await ib.whatIfOrderAsync(contract, order)
        return {
            'status': 'SIMULATED',
            'init_margin_change': what_if.initMarginChange,
            'maint_margin_change': what_if.maintMarginChange,
            'equity_with_loan': what_if.equityWithLoanValue,
            'commission': what_if.commission,
        }

    # Place live order
    trade = ib.placeOrder(contract, order)
    return {
        'status': 'SUBMITTED',
        'order_id': trade.order.orderId,
        'trade': trade,
    }
```

### Cross-Account Rebalance
```python
async def rebalance_across_accounts(
    ib: IB,
    target_allocations: dict[str, dict[str, float]],
    accounts: dict[str, str],  # {account_id: account_type}
) -> list[dict]:
    """
    Generate rebalance orders across multiple accounts.
    target_allocations: {account_id: {symbol: target_pct}}
    """
    orders = []

    for acct_id, targets in target_allocations.items():
        acct_type = accounts[acct_id]

        # Get current positions
        positions = [p for p in ib.positions() if p.account == acct_id]

        # Get account NAV
        summary = [s for s in ib.accountSummary()
                   if s.account == acct_id and s.tag == 'NetLiquidation']
        nav = float(summary[0].value) if summary else 0

        for symbol, target_pct in targets.items():
            target_value = nav * target_pct

            # Find current position
            current_pos = next(
                (p for p in positions if p.contract.symbol == symbol), None
            )
            current_qty = current_pos.position if current_pos else 0

            # Get current price (simplified)
            contract = Stock(symbol, 'SMART', 'USD')
            [ticker] = await ib.reqTickersAsync(contract)
            price = ticker.marketPrice()

            if price and price > 0:
                target_qty = int(target_value / price)
                delta = target_qty - current_qty

                if abs(delta) > 0:
                    action = 'BUY' if delta > 0 else 'SELL'
                    order_info = {
                        'account': acct_id,
                        'account_type': acct_type,
                        'symbol': symbol,
                        'action': action,
                        'quantity': abs(delta),
                        'current_qty': current_qty,
                        'target_qty': target_qty,
                    }

                    # Validate before adding
                    is_valid, reason = validate_order_for_account(
                        action, contract, acct_type, delta
                    )
                    order_info['valid'] = is_valid
                    order_info['rejection_reason'] = reason
                    orders.append(order_info)

    return orders
```

---

## Options Order Flow

### Options Contract Construction
```python
from ib_async import Option

# Single option
aapl_call = Option('AAPL', '20260320', 180, 'C', 'SMART')

# Request option chain
chains = await ib.reqSecDefOptParamsAsync(
    underlyingSymbol='AAPL',
    futFopExchange='',
    underlyingSecType='STK',
    underlyingConId=265598,  # AAPL conId
)

# Filter for specific expiry and strikes
for chain in chains:
    if chain.exchange == 'SMART':
        expirations = chain.expirations  # List of date strings
        strikes = chain.strikes          # List of strike prices
```

### Spread Orders
```python
from ib_async import Contract, ComboLeg, Order

# Vertical spread (bull call)
combo = Contract()
combo.symbol = 'AAPL'
combo.secType = 'BAG'
combo.currency = 'USD'
combo.exchange = 'SMART'

# Buy lower strike call, sell higher strike call
combo.comboLegs = [
    ComboLeg(conId=long_call_conid, ratio=1, action='BUY', exchange='SMART'),
    ComboLeg(conId=short_call_conid, ratio=1, action='SELL', exchange='SMART'),
]

# Net debit order for the spread
spread_order = LimitOrder('BUY', 1, limitPrice=2.50)
```

---

## Position Sizing

### Risk-Based Position Sizing
```python
def calculate_position_size(
    account_nav: float,
    entry_price: float,
    stop_price: float,
    risk_pct: float = 0.02,  # 2% max risk per trade
    account_type: str = 'Individual',
) -> dict:
    """
    Calculate position size based on risk management rules.
    Integrates with trading-signals-skill risk parameters.
    """
    # Max risk amount
    risk_amount = account_nav * risk_pct

    # Per-share risk
    per_share_risk = abs(entry_price - stop_price)

    if per_share_risk <= 0:
        return {'error': 'Stop price must differ from entry'}

    # Raw position size
    raw_qty = int(risk_amount / per_share_risk)

    # IRA adjustment: no margin, so check cash available
    max_by_cash = int(account_nav / entry_price) if account_type == 'IRA' else raw_qty * 2

    final_qty = min(raw_qty, max_by_cash)

    return {
        'quantity': final_qty,
        'risk_amount': final_qty * per_share_risk,
        'risk_pct_actual': (final_qty * per_share_risk) / account_nav,
        'position_value': final_qty * entry_price,
        'position_pct_of_nav': (final_qty * entry_price) / account_nav,
        'account_type': account_type,
        'margin_adjusted': account_type == 'IRA',
    }
```
