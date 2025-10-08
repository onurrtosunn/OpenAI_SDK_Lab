from mcp.server.fastmcp import FastMCP
from typing import List, Dict, Any
import asyncio

try:
    from duckduckgo_search import DDGS
except Exception:  # pragma: no cover
    DDGS = None  # type: ignore


mcp = FastMCP("search_server")


@mcp.tool()
async def web_search(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """Perform a free web search using DuckDuckGo.

    Args:
        query: Search query string.
        max_results: Maximum number of results to return (default 5).

    Returns:
        List of results with keys: title, href, body.
    """
    if DDGS is None:
        raise RuntimeError(
            "duckduckgo-search is required. Install with: uv add duckduckgo-search"
        )

    loop = asyncio.get_running_loop()

    def _search_sync() -> List[Dict[str, Any]]:
        with DDGS() as ddgs:
            return list(ddgs.text(query, max_results=max_results))

    results = await loop.run_in_executor(None, _search_sync)
    # Normalize keys to a consistent schema
    normalized: List[Dict[str, Any]] = []
    for item in results:
        normalized.append(
            {
                "title": item.get("title"),
                "href": item.get("href") or item.get("link"),
                "body": item.get("body") or item.get("snippet"),
            }
        )
    return normalized


if __name__ == "__main__":
    mcp.run(transport="stdio")


