# MCP Agents Implementation

## 📌 Overview
This project demonstrates **Model Context Protocol (MCP) integration with OpenAI Agents SDK** to enable specialized tool usage through multiple MCP servers.  
It showcases how to configure and run OpenAI Agents with MCP servers for filesystem operations, web scraping, and more.

The system is designed to showcase:
- **MCP Server Integration** - Connect multiple MCP servers to OpenAI Agents
- **Specialized Tool Usage** - Filesystem operations, web scraping with Playwright
- **Multi-Server Architecture** - Simultaneous use of different MCP servers
- **Agent Workflow Visualization** with `graphviz`

---

##  Features
- **Multiple MCP Servers**  
  - `Filesystem MCP Server` → File and directory operations  
  - `Playwright/Browser MCP Server` → Web scraping and browser automation  
  - `Brave Search MCP Server` → Web search capabilities
- **OpenAI Agent Integration**  
  - Seamless connection between OpenAI Agents and MCP servers  
  - Tool-based communication and execution  
  - Real-time interaction with external systems
- **Comprehensive Demo**  
  - Interactive Jupyter notebook with step-by-step examples  
  - Practical use cases for each MCP server  
  - Error handling and debugging examples

---

## Architecture
The system consists of:

### MCP Servers Used
1. **Filesystem MCP Server** (`npx @modelcontextprotocol/server-filesystem`)
   - File reading, writing, and directory operations
   - Path manipulation and file system queries

2. **Playwright/Browser MCP Server** (`npx @modelcontextprotocol/server-playwright`)
   - Web page navigation and interaction
   - HTML content extraction and scraping
   - Browser automation capabilities

3. **Brave Search MCP Server** (`npx @modelcontextprotocol/server-brave-search`)
   - Web search functionality
   - Search result processing and formatting

---
## 📋 Requirements
- **Python 3.10+**
- **OpenAI API key** (for agents)
- **Node.js and npm** (for MCP servers)
- **Playwright browsers** (for web scraping)
- **Brave Search API key** (optional, for search functionality)

## Configuration

### MCP Server Parameters
- **Filesystem Server**: Requires a sandbox directory path
- **Playwright Server**: No additional configuration needed
- **Brave Search Server**: Requires API key in environment variables

### Agent Configuration
- **Model Selection**: Uses OpenAI's latest models by default
- **Tool Access**: Agents can access all tools from connected MCP servers
- **Concurrency**: Multiple MCP servers can run simultaneously


---
### Related Projects
- [Deep Research with Google Search](../Deep_Research_w_Google_Search/)
- [Job Application Agents](../Job_Application_Agents/)

---
