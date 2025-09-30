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

## 🚀 Features
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

## 🛠️ Architecture
The system consists of:

### Core Components
- **OpenAI Agent**: Main agent that orchestrates MCP server interactions
- **MCP Servers**: Specialized servers providing specific tool capabilities
- **MCPServerStdio**: Standard I/O interface for MCP server communication

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

### Python Packages
```bash
pip install openai-agents python-dotenv
```

### Node.js Dependencies
```bash
npm install -g @modelcontextprotocol/server-filesystem
npm install -g @modelcontextprotocol/server-playwright
npm install -g @modelcontextprotocol/server-brave-search
npx playwright install
```

---

## ⚙️ Setup

### 1. Environment Variables
Create a `.env` file in the project root:
```env
# OpenAI (required)
OPENAI_API_KEY=sk-...

# Brave Search (optional)
BRAVE_SEARCH_API_KEY=your_brave_search_api_key
```

### 2. Install Dependencies
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install Python packages
pip install -U openai-agents python-dotenv

# Install Node.js MCP servers
npm install -g @modelcontextprotocol/server-filesystem
npm install -g @modelcontextprotocol/server-playwright
npm install -g @modelcontextprotocol/server-brave-search

# Install Playwright browsers
npx playwright install
```

### 3. Run the Demo
```bash
# Start Jupyter notebook
jupyter notebook mcp_agents_demo.ipynb
```

---

## 📖 Usage Examples

### Basic MCP Server Setup
```python
from agents import Agent, Runner
from agents.mcp import MCPServerStdio

# Filesystem MCP Server
filesystem_server = MCPServerStdio(
    "npx", 
    ["@modelcontextprotocol/server-filesystem", "/path/to/sandbox"]
)

# Playwright MCP Server
playwright_server = MCPServerStdio(
    "npx",
    ["@modelcontextprotocol/server-playwright"]
)
```

### Agent with MCP Tools
```python
# Create agent with MCP servers
agent = Agent(
    name="MCP Assistant",
    instructions="Use available MCP tools to help with tasks",
    mcp_servers=[filesystem_server, playwright_server]
)

# Run the agent
result = await Runner.run(agent, "Read the file and summarize its content")
```

---

## 🔧 Configuration

### MCP Server Parameters
- **Filesystem Server**: Requires a sandbox directory path
- **Playwright Server**: No additional configuration needed
- **Brave Search Server**: Requires API key in environment variables

### Agent Configuration
- **Model Selection**: Uses OpenAI's latest models by default
- **Tool Access**: Agents can access all tools from connected MCP servers
- **Concurrency**: Multiple MCP servers can run simultaneously

---

## 🐛 Troubleshooting

### Common Issues
1. **Node.js not found**: Ensure Node.js is installed and `npx` is in PATH
2. **MCP server fails to start**: Check server installation and permissions
3. **Playwright browsers missing**: Run `npx playwright install`
4. **API key errors**: Verify environment variables are properly set

### Debug Mode
Enable debug logging for MCP servers:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## 📚 Resources and Further Exploration

### Official Documentation
- [OpenAI Agents SDK Documentation](https://platform.openai.com/docs/agents)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [MCP Server Documentation](https://github.com/modelcontextprotocol/servers)

### Community Resources
- [MCP Server Examples](https://github.com/modelcontextprotocol/servers/tree/main/src)
- [OpenAI Agents Cookbook](https://cookbook.openai.com/)
- [MCP Integration Patterns](https://modelcontextprotocol.io/docs/integration)

### Related Projects
- [Deep Research with Google Search](../Deep_Research_w_Google_Search/)
- [Job Application Agents](../Job_Application_Agents/)

---

## 🤝 Contributing
This project is part of the OpenAI SDK Lab. Feel free to explore, modify, and extend the MCP server implementations for your specific use cases.

---

*Last updated: September 2025*
