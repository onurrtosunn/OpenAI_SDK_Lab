# Trading Bot (MCP-enabled)

A fully local, end-to-end Model Context Protocol (MCP) demo for a research-and-trade workflow. Uses only free/local MCP servers (search, fetch, memory, market, accounts, push) and standard Python packages.

## Features
- Researcher agent with web search and fetch tools (DuckDuckGo + httpx)
- Trader agent that reads account state and executes trades via MCP
- Local market data fallback with EOD/randoms when Polygon is unavailable
- Local memory store (SQLite) for persistence
- Push notifications stub MCP

## Repository Layout
- `traders.py` – main agent orchestration
- `prompts.py` – researcher/trader instructions and messages
- `tracing.py` – trace helpers (bridge to `tracers.py`)
- `mcp_config.py` – MCP server parameter providers
- `accounts.py` – account domain model (SOLID, typed)
- `accounts_server.py` – MCP server exposing account tools/resources
- `accounts_mcp_client.py` – thin client for accounts MCP
- `market.py` + `market_server.py` – market data utilities and MCP
- `search_server.py` – DuckDuckGo search MCP
- `fetch_server.py` – HTTP fetch MCP (httpx)
- `memory_server.py` – SQLite memory MCP
- `push_server.py` – push notifications stub MCP
- `database.py` – simple persistence helpers for accounts/market/logs
- `4_lab4.ipynb` – notebook demo

## Requirements
- Python 3.11+
- `uv` (recommended) or `pip`

Install deps (recommended):
```bash
uv sync
```

Or add missing packages on-demand:
```bash
uv add duckduckgo-search httpx python-dotenv pydantic
```

## Environment
Optional:
- `POLYGON_API_KEY` and `POLYGON_PLAN` ("paid" | "realtime") to enable Polygon MCP; otherwise EOD/random fallback is used.

Create `.env` (optional):
```bash
POLYGON_API_KEY=your_key
POLYGON_PLAN=paid
```

## Running the MCP Servers (sanity checks)
```bash

uv run search_server.py

```
All should start and block; stop with Ctrl+C.

## Notebook Demo
Open and run `main.ipynb` top-to-bottom. It:
1) Configures MCP servers for trader and researcher
2) Runs a researcher demo
3) Initializes a trader and executes a trading run

If you see connection issues, ensure required deps are installed:
```bash
uv add duckduckgo-search httpx
```

## CLI-style Run (optional)
You can also drive the `Trader` class directly (see `traders.py`). Example skeleton:
```python
import asyncio
from traders import Trader

async def main():
    trader = Trader("Onur")
    await trader.run()

asyncio.run(main())
```

