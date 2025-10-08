from mcp.server.fastmcp import FastMCP
from typing import Optional, Dict, Any
import httpx


mcp = FastMCP("fetch_server")


@mcp.tool()
async def fetch_text(url: str, timeout_seconds: int = 15, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """Fetch a URL and return status and text content.

    Args:
        url: The URL to fetch
        timeout_seconds: Request timeout in seconds (default 15)
        headers: Optional HTTP headers
    Returns:
        {"url", "status", "content", "encoding"}
    """
    async with httpx.AsyncClient(follow_redirects=True, timeout=timeout_seconds, headers=headers) as client:
        resp = await client.get(url)
        return {
            "url": str(resp.url),
            "status": resp.status_code,
            "content": resp.text,
            "encoding": resp.encoding,
        }


@mcp.tool()
async def fetch_json(url: str, timeout_seconds: int = 15, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """Fetch a URL and parse JSON.

    Returns:
        {"url", "status", "json"}
    """
    async with httpx.AsyncClient(follow_redirects=True, timeout=timeout_seconds, headers=headers) as client:
        resp = await client.get(url)
        data = resp.json()
        return {
            "url": str(resp.url),
            "status": resp.status_code,
            "json": data,
        }


if __name__ == "__main__":
    mcp.run(transport="stdio")


