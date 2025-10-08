# Facade module to expose the accounts MCP client API under a clearer name
from accounts_client import (
    list_accounts_tools,
    call_accounts_tool,
    read_accounts_resource,
    read_strategy_resource,
    get_accounts_tools_openai,
)

__all__ = [
    "list_accounts_tools",
    "call_accounts_tool",
    "read_accounts_resource",
    "read_strategy_resource",
    "get_accounts_tools_openai",
]


