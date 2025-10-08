from mcp.server.fastmcp import FastMCP
from typing import Optional
from datetime import datetime


mcp = FastMCP("push_server")


@mcp.tool()
async def send_notification(title: str, body: str, recipient: Optional[str] = None) -> str:
    """Send a notification (no-op demo). Returns a receipt string.

    Args:
        title: Short title of the notification
        body: Message body
        recipient: Optional recipient identifier (email/user-id/etc.)
    """
    timestamp = datetime.utcnow().isoformat() + "Z"
    # In a real implementation, integrate with a push/email/SMS provider here.
    return f"notified:{recipient or 'default'}:{timestamp}:{title}"


if __name__ == "__main__":
    mcp.run(transport="stdio")


