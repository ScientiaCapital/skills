# IBKR Connection Patterns

## Table of Contents
1. [IB Gateway Setup](#ib-gateway-setup)
2. [ib_async Connection](#ib_async-connection)
3. [Multi-Account Queries](#multi-account-queries)
4. [Session Management](#session-management)
5. [Error Handling](#error-handling)
6. [Client Portal API Auth](#client-portal-api-auth)

---

## IB Gateway Setup

### Prerequisites
```bash
# Install IB Gateway (lightweight, headless — preferred over TWS for automation)
# Download from: https://www.interactivebrokers.com/en/trading/ibgateway-stable.php

# Verify Java 8+
java -version
```

### Configuration
1. Launch IB Gateway → Login with IBKR credentials
2. Configure → Settings → API:
   - Enable ActiveX and Socket Clients
   - Socket port: `7496` (live) or `7497` (paper)
   - Allow connections from localhost only
   - Read-Only API: Enable for portfolio-only queries
3. Master Client ID: Set to `0` for primary connection

---

## ib_async Connection

### Basic Connection
```python
import asyncio
from ib_async import IB, Stock, util

async def connect_ib() -> IB:
    """Connect to IB Gateway with retry logic."""
    ib = IB()

    # Connection params
    host = '127.0.0.1'
    port = 7496        # 7497 for paper trading
    client_id = 1      # Unique per concurrent connection

    try:
        await ib.connectAsync(host, port, clientId=client_id)
        print(f"Connected. Server version: {ib.client.serverVersion()}")
        return ib
    except Exception as e:
        print(f"Connection failed: {e}")
        raise

async def main():
    ib = await connect_ib()
    try:
        # Your logic here
        accounts = ib.managedAccounts()
        print(f"Linked accounts: {accounts}")
    finally:
        ib.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
```

### Connection with Auto-Reconnect
```python
from ib_async import IB
import asyncio

class IBConnection:
    """Managed IBKR connection with auto-reconnect."""

    def __init__(
        self,
        host: str = '127.0.0.1',
        port: int = 7496,
        client_id: int = 1,
        max_retries: int = 5,
        retry_delay: float = 3.0
    ):
        self.host = host
        self.port = port
        self.client_id = client_id
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.ib = IB()

        # Register disconnect handler
        self.ib.disconnectedEvent += self._on_disconnect

    async def connect(self) -> IB:
        """Connect with retry logic."""
        for attempt in range(self.max_retries):
            try:
                await self.ib.connectAsync(
                    self.host, self.port,
                    clientId=self.client_id,
                    timeout=10
                )
                return self.ib
            except Exception as e:
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(self.retry_delay * (attempt + 1))
                else:
                    raise ConnectionError(
                        f"Failed after {self.max_retries} attempts: {e}"
                    )

    def _on_disconnect(self):
        """Handle unexpected disconnection."""
        print("WARNING: Disconnected from IB Gateway")
        # Could trigger auto-reconnect here

    async def disconnect(self):
        """Clean disconnect."""
        if self.ib.isConnected():
            self.ib.disconnect()
```

---

## Multi-Account Queries

### List All Linked Accounts
```python
async def get_all_accounts(ib: IB) -> dict[str, str]:
    """
    Get all linked accounts with their types.
    Returns: {'U1234567': 'Individual', 'U7654321': 'IRA', ...}
    """
    accounts = ib.managedAccounts()

    account_info = {}
    for acct in accounts:
        # Request account type via account summary
        tags = await ib.accountSummaryAsync(acct)
        for tag in tags:
            if tag.tag == 'AccountType':
                account_info[acct] = tag.value
                break

    return account_info
```

### Query Positions Across All Accounts
```python
async def get_all_positions(ib: IB) -> dict[str, list]:
    """Get positions grouped by account."""
    positions = ib.positions()

    by_account: dict[str, list] = {}
    for pos in positions:
        acct = pos.account
        if acct not in by_account:
            by_account[acct] = []
        by_account[acct].append({
            'symbol': pos.contract.symbol,
            'quantity': pos.position,
            'avg_cost': pos.avgCost,
            'contract': pos.contract,
        })

    return by_account
```

### Account Summary (All Accounts)
```python
async def get_account_summaries(ib: IB) -> dict[str, dict]:
    """Get key financial metrics for all linked accounts."""
    summary_tags = [
        'NetLiquidation',
        'TotalCashValue',
        'BuyingPower',
        'GrossPositionValue',
        'MaintMarginReq',
        'AvailableFunds',
        'ExcessLiquidity',
    ]

    summaries = {}
    for item in ib.accountSummary():
        acct = item.account
        if acct not in summaries:
            summaries[acct] = {}
        if item.tag in summary_tags:
            summaries[acct][item.tag] = float(item.value)

    return summaries
```

---

## Session Management

### Keep-Alive (Client Portal API)
```python
import httpx
import asyncio

async def keep_session_alive(base_url: str = "https://localhost:5000/v1/api"):
    """Ping Client Portal API every 5 min to prevent 6-min timeout."""
    while True:
        try:
            async with httpx.AsyncClient(verify=False) as client:
                resp = await client.post(f"{base_url}/tickle")
                if resp.status_code != 200:
                    print(f"Session ping failed: {resp.status_code}")
        except Exception as e:
            print(f"Keep-alive error: {e}")
        await asyncio.sleep(300)  # 5 minutes
```

### Session Exclusivity Warning
```
CRITICAL: Only ONE active brokerage session per IBKR username.
- Logging in via TWS/Gateway on another device = disconnects current session
- Logging in via web/mobile = disconnects API session
- Solution: Dedicate one machine to API access
```

---

## Error Handling

### Common Error Codes
```python
IBKR_ERRORS = {
    200: "No security definition found",
    201: "Order rejected — check IRA restrictions",
    202: "Order cancelled",
    300: "Socket connection dropped — reconnect",
    502: "Couldn't connect to TWS — is IB Gateway running?",
    504: "Not connected — call connect() first",
    1100: "Connectivity between IB and TWS lost",
    1101: "Connectivity restored (data lost)",
    1102: "Connectivity restored (data maintained)",
    2104: "Market data farm connection OK",
    2106: "HMDS data farm connection OK",
    2158: "Sec-def data farm connection OK",
}

def handle_error(req_id: int, error_code: int, error_string: str):
    """Route IBKR errors to appropriate handler."""
    if error_code in (1100, 300, 502):
        # Connection issues — trigger reconnect
        raise ConnectionError(f"IBKR connection error {error_code}: {error_string}")
    elif error_code == 201:
        # Order rejected — likely IRA restriction
        raise ValueError(f"Order rejected (check IRA rules): {error_string}")
    elif error_code >= 2100:
        # Informational messages
        print(f"IBKR info [{error_code}]: {error_string}")
    else:
        print(f"IBKR error [{error_code}]: {error_string}")
```

---

## Client Portal API Auth

### OAuth 2.0 Flow (JWT Client Assertion)
```python
import jwt
import time
import httpx

async def get_cp_access_token(
    client_id: str,
    private_key_path: str,
    token_url: str = "https://api.ibkr.com/v1/api/oauth/token"
) -> str:
    """
    Get Client Portal API access token using OAuth 2.0
    with private key JWT assertion (RFC 7521/7523).
    """
    # Load private key
    with open(private_key_path, 'r') as f:
        private_key = f.read()

    # Create JWT assertion
    now = int(time.time())
    claims = {
        'iss': client_id,
        'sub': client_id,
        'aud': token_url,
        'exp': now + 300,  # 5 min expiry
        'iat': now,
    }

    assertion = jwt.encode(claims, private_key, algorithm='RS256')

    # Exchange for access token
    async with httpx.AsyncClient() as client:
        resp = await client.post(token_url, data={
            'grant_type': 'client_credentials',
            'client_assertion_type': 'urn:ietf:params:oauth:client-assertion-type:jwt-bearer',
            'client_assertion': assertion,
        })
        resp.raise_for_status()
        return resp.json()['access_token']
```

### Session Duration
- Access tokens: Up to 24 hours (reset at midnight NY/Zug/HK)
- Inactivity timeout: 6 minutes without requests
- Must call `/tickle` endpoint every 5 minutes to maintain session
