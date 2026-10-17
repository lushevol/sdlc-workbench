# MCP Servers: Language Support & Implementation

## Overview

This document explains that **Model Context Protocol (MCP) servers can be built in ANY programming language**, not just Node.js. MCP is a language-agnostic protocol, similar to HTTP.

---

## What is MCP?

**Model Context Protocol (MCP)** is a standardized communication protocol that allows:
- AI assistants (like GitHub Copilot) to access external tools and data sources
- Servers to expose capabilities through a uniform interface
- Different implementations to interoperate seamlessly

**Key Point:** MCP is just a protocol specification - any language that can implement it can create an MCP server.

---

## Requirements for Any MCP Server

Any programming language can build an MCP server if it can:

1. ✅ **Read from stdin and write to stdout** (for stdio transport)
2. ✅ **Parse and generate JSON** (for JSON-RPC messages)
3. ✅ **Implement async I/O** (optional but recommended)
4. ✅ **Follow the MCP protocol specification**

That's it! No specific runtime or language requirement.

---

## Official MCP SDKs

### 1. TypeScript/Node.js (Most Mature)

**Package:** `@modelcontextprotocol/sdk`

**Example:**
```typescript
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';

const server = new McpServer({
  name: "my-nodejs-server",
  version: "1.0.0"
});

server.tool(
  "my_tool",
  "Description of what the tool does",
  { param: z.string() },
  async ({ param }) => {
    return { content: [{ type: "text", text: "Result" }] };
  }
);

const transport = new StdioServerTransport();
await server.connect(transport);
```

**Advantages:**
- ✅ Official, well-maintained SDK
- ✅ Rich type definitions with TypeScript
- ✅ Large ecosystem of libraries
- ✅ Easy NPM distribution with `npx`
- ✅ Most examples and documentation available

**Use Cases:**
- Web API integrations (REST, GraphQL)
- Azure DevOps, GitHub, GitLab integrations
- Database operations
- Cloud service management

---

### 2. Python (Growing Ecosystem)

**Package:** `mcp` (Python MCP SDK)

**Example:**
```python
#!/usr/bin/env python3
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server

# Create server
server = Server("my-python-server")

# Define tools
@server.list_tools()
async def list_tools():
    return [{
        "name": "analyze_data",
        "description": "Analyze a dataset",
        "inputSchema": {
            "type": "object",
            "properties": {
                "data": {"type": "array"},
                "operation": {"type": "string"}
            },
            "required": ["data", "operation"]
        }
    }]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "analyze_data":
        import pandas as pd
        df = pd.DataFrame(arguments["data"])
        result = df.describe().to_json()
        return {"result": result}

# Run server
async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream)

if __name__ == "__main__":
    asyncio.run(main())
```

**Advantages:**
- ✅ Excellent for data science and ML tasks
- ✅ Easy integration with pandas, numpy, sklearn
- ✅ Native JSON support
- ✅ Distribution via pip/PyPI
- ✅ Can use `uvx` or `pipx` for one-click install

**Use Cases:**
- Data analysis and visualization
- Machine learning model inference
- Jupyter notebook execution
- Scientific computing
- File processing and transformations

---

### 3. Go (Community Support)

**Package:** Community implementations available

**Example:**
```go
package main

import (
    "bufio"
    "encoding/json"
    "fmt"
    "os"
)

type Tool struct {
    Name        string `json:"name"`
    Description string `json:"description"`
}

type Request struct {
    JSONRPC string          `json:"jsonrpc"`
    ID      int             `json:"id"`
    Method  string          `json:"method"`
    Params  json.RawMessage `json:"params"`
}

type Response struct {
    JSONRPC string      `json:"jsonrpc"`
    ID      int         `json:"id"`
    Result  interface{} `json:"result"`
}

func main() {
    scanner := bufio.NewScanner(os.Stdin)
    
    for scanner.Scan() {
        var req Request
        json.Unmarshal(scanner.Bytes(), &req)
        
        switch req.Method {
        case "tools/list":
            tools := []Tool{
                {Name: "system_info", Description: "Get system information"},
            }
            sendResponse(req.ID, tools)
        }
    }
}

func sendResponse(id int, result interface{}) {
    resp := Response{JSONRPC: "2.0", ID: id, Result: result}
    json.NewEncoder(os.Stdout).Encode(resp)
}
```

**Advantages:**
- ✅ High performance and low memory footprint
- ✅ Excellent for system-level operations
- ✅ Native concurrency with goroutines
- ✅ Single binary distribution (no runtime needed)
- ✅ Strong typing and compile-time checks

**Use Cases:**
- Kubernetes cluster management
- Docker container operations
- System monitoring and automation
- Network tools
- CLI tool integrations

---

### 4. Rust (Community Support)

**Advantages:**
- ✅ Maximum performance and safety
- ✅ Zero-cost abstractions
- ✅ Memory safety without garbage collection
- ✅ Excellent for performance-critical tools

**Use Cases:**
- High-performance data processing
- Systems programming integrations
- Security-critical operations
- WebAssembly compilation

---

### 5. Java/Kotlin (Enterprise)

**Advantages:**
- ✅ Strong enterprise ecosystem
- ✅ JVM platform maturity
- ✅ Integration with Spring Boot, Hibernate
- ✅ Rich library ecosystem

**Use Cases:**
- Enterprise system integration
- Database operations (JDBC)
- SAP, Oracle, IBM integrations
- Legacy system bridges

---

### 6. .NET/C# (Windows & Azure)

**Advantages:**
- ✅ First-class Windows integration
- ✅ Azure SDK native support
- ✅ Active Directory, PowerShell integration
- ✅ Strong typing and modern language features

**Use Cases:**
- Azure resource management
- Windows system administration
- Active Directory operations
- Office 365 integrations

---

### 7. Shell Scripts (Quick & Simple)

**Example:**
```bash
#!/bin/bash

while IFS= read -r line; do
    method=$(echo "$line" | jq -r '.method')
    id=$(echo "$line" | jq -r '.id')
    
    case "$method" in
        "tools/list")
            echo "{\"jsonrpc\":\"2.0\",\"id\":$id,\"result\":[{\"name\":\"ls\",\"description\":\"List files\"}]}"
            ;;
        "tools/call")
            tool=$(echo "$line" | jq -r '.params.name')
            if [ "$tool" = "ls" ]; then
                result=$(ls -la)
                echo "{\"jsonrpc\":\"2.0\",\"id\":$id,\"result\":\"$result\"}"
            fi
            ;;
    esac
done
```

**Advantages:**
- ✅ Extremely simple for basic tasks
- ✅ No installation required (bash everywhere)
- ✅ Direct system command execution

**Use Cases:**
- Quick prototypes
- Simple file operations
- Wrapping existing CLI tools

---

## How MCP Communication Works

### Transport Layer: stdio (Standard Input/Output)

```
┌─────────────────────────────────┐
│   VS Code MCP Extension         │
│   (Client)                      │
└────────────┬────────────────────┘
             │
             │ stdin/stdout
             │ (JSON-RPC messages)
             │
┌────────────▼────────────────────┐
│   MCP Server                    │
│   (Any Language)                │
│                                 │
│   - Reads JSON from stdin       │
│   - Parses requests             │
│   - Executes operations         │
│   - Writes JSON to stdout       │
└─────────────────────────────────┘
```

### JSON-RPC Message Format

**Request from VS Code:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/list",
  "params": {}
}
```

**Response from MCP Server:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": [
    {
      "name": "my_tool",
      "description": "Does something useful",
      "inputSchema": {
        "type": "object",
        "properties": {
          "param": {"type": "string"}
        }
      }
    }
  ]
}
```

**Any language that can read/write this format works!**

---

## Real-World MCP Server Examples

### Node.js Implementations:
- **Azure DevOps MCP** (`@azure-devops/mcp`) - Work items, repos, PRs
- **GitHub MCP** - Repository operations, issues, PRs
- **GitLab MCP** - CI/CD, merge requests
- **Database MCP** - SQL queries, schema operations
- **Your Project** (`@sc-ado/mcp-server`) - Azure DevOps & Confluence

### Python Implementations:
- **Jupyter MCP** - Execute notebook cells, run Python code
- **Pandas MCP** - Dataset analysis, transformations
- **Scikit-learn MCP** - ML model inference
- **File System MCP** - Advanced file operations
- **OpenAPI MCP** - REST API client generation

### Go Implementations:
- **Kubernetes MCP** - Cluster management, pod operations
- **Docker MCP** - Container lifecycle management
- **Terraform MCP** - Infrastructure as code operations

---

## VS Code Configuration Examples

### Node.js MCP Server:
```json
{
  "servers": {
    "ado-mcp": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@sc-ado/mcp-server", "org-url", "token"]
    }
  }
}
```

### Python MCP Server:
```json
{
  "servers": {
    "data-analysis": {
      "type": "stdio",
      "command": "python3",
      "args": ["/path/to/data_mcp.py"]
    }
  }
}
```

Or with `uvx` (Python package executor):
```json
{
  "servers": {
    "data-analysis": {
      "type": "stdio",
      "command": "uvx",
      "args": ["my-python-mcp-package", "arg1"]
    }
  }
}
```

### Go MCP Server (Binary):
```json
{
  "servers": {
    "k8s-manager": {
      "type": "stdio",
      "command": "/usr/local/bin/k8s-mcp",
      "args": ["--cluster", "prod"]
    }
  }
}
```

### Multiple Servers (Mixed Languages):
```json
{
  "servers": {
    "ado-mcp": {
      "command": "npx",
      "args": ["-y", "@sc-ado/mcp-server"]
    },
    "python-data": {
      "command": "python3",
      "args": ["/path/to/data_mcp.py"]
    },
    "k8s": {
      "command": "/usr/local/bin/k8s-mcp"
    },
    "shell-utils": {
      "command": "/bin/bash",
      "args": ["/path/to/shell_mcp.sh"]
    }
  }
}
```

**All four servers run simultaneously, each providing different tools!**

---

## Package Distribution & One-Click Install

### Comparison by Language:

| Language | Package Manager | Executor | One-Click Install | Distribution Ease |
|----------|----------------|----------|-------------------|-------------------|
| **Node.js** | NPM | `npx` | ✅ Yes | ⭐⭐⭐⭐⭐ Excellent |
| **Python** | pip/PyPI | `uvx`/`pipx` | ✅ Yes | ⭐⭐⭐⭐ Great |
| **Go** | Go modules | N/A | ❌ No | ⭐⭐ Manual binary |
| **Rust** | Cargo | N/A | ❌ No | ⭐⭐ Manual binary |
| **Java** | Maven/Gradle | N/A | ❌ No | ⭐⭐ Manual JAR |
| **.NET** | NuGet | `dotnet tool` | ⚠️ Partial | ⭐⭐⭐ Good |
| **Shell** | N/A | N/A | ❌ No | ⭐ Manual script |

### Node.js: Best for One-Click Install

**Why Node.js is optimal for distribution:**

1. **NPM Registry** - Global, trusted package registry
2. **NPX** - Automatic download and execution
3. **Version Management** - Semantic versioning built-in
4. **Cross-Platform** - Works on Windows, Mac, Linux
5. **No Compilation** - JavaScript runs directly
6. **VS Code Native** - VS Code is built on Node.js/Electron

**One-Click Install URL Example:**
```markdown
[![Install](badge)](https://insiders.vscode.dev/redirect/mcp/install?name=mcp&config=...)
```

### Python: Good Alternative

**Using `uvx` (UV package executor):**
```json
{
  "command": "uvx",
  "args": ["my-python-mcp"]
}
```

**Advantages:**
- Similar to `npx` but for Python
- Automatic environment management
- Fast installation
- One-click install possible

---

## Why Node.js is Most Common

### Statistics & Reality:

**~70% of MCP servers use Node.js** because:

1. ✅ **First-class SDK** - Official `@modelcontextprotocol/sdk`
2. ✅ **VS Code ecosystem** - VS Code itself is Node.js-based
3. ✅ **JSON native** - JavaScript handles JSON effortlessly
4. ✅ **NPM distribution** - Seamless `npx` installation
5. ✅ **Async by default** - Perfect for I/O-heavy operations
6. ✅ **Developer pool** - Millions of JS/TS developers
7. ✅ **Web APIs** - Most SaaS tools have JavaScript SDKs
8. ✅ **Rich ecosystem** - Massive NPM library collection

**Python is second (~20%)** for:
- Data science and ML integrations
- Scientific computing
- When existing Python codebase exists

**Other languages (~10%)** for:
- Specialized use cases
- Performance requirements
- Legacy system integration

---

## Choosing the Right Language for Your MCP Server

### Decision Matrix:

**Choose Node.js if:**
- ✅ Integrating with web APIs (REST, GraphQL)
- ✅ Want easy distribution (NPM/npx)
- ✅ Need rapid development
- ✅ Working with JSON-heavy data
- ✅ Want one-click install experience
- ✅ Team knows JavaScript/TypeScript

**Choose Python if:**
- ✅ Doing data analysis or ML
- ✅ Have existing Python libraries to use
- ✅ Working with scientific computing
- ✅ Team prefers Python
- ✅ Need pandas, numpy, sklearn integration

**Choose Go if:**
- ✅ Need maximum performance
- ✅ Building system-level tools
- ✅ Want single binary distribution
- ✅ Deploying to Kubernetes/Docker

**Choose Rust if:**
- ✅ Performance is critical
- ✅ Safety is paramount
- ✅ Building WASM modules
- ✅ Memory constraints exist

**Choose Java/.NET if:**
- ✅ Enterprise environment requirements
- ✅ Existing JVM/.NET infrastructure
- ✅ Need enterprise library support

---

## Your Project: Why Node.js is the Right Choice

### For `@sc-ado/mcp-server`:

**Reasons Node.js is optimal:**

1. ✅ **Azure DevOps SDK** - `azure-devops-node-api` is mature and well-maintained
2. ✅ **Confluence REST API** - Easy with axios/fetch in Node.js
3. ✅ **NPM Distribution** - Can publish to SCB private NPM registry
4. ✅ **One-Click Install** - Enables seamless user experience
5. ✅ **Reference Implementation** - Azure DevOps MCP uses Node.js
6. ✅ **Code Already Written** - No need to rewrite
7. ✅ **JSON Heavy** - Azure DevOps/Confluence APIs return JSON
8. ✅ **Developer Skills** - TypeScript/JavaScript widely known

**If you used Python instead:**
- ❌ Azure DevOps Python SDK less mature
- ❌ Would need to rewrite everything
- ❌ Similar distribution challenges
- ✅ But better for data processing tasks

**Verdict:** **Stick with Node.js** - it's the perfect fit for your use case.

---

## Protocol Details: Language-Agnostic Nature

### MCP Protocol Layers:

```
┌─────────────────────────────────────────┐
│  Application Layer                      │
│  (Your business logic - Any Language)   │
└─────────────────────────────────────────┘
                  ↕
┌─────────────────────────────────────────┐
│  MCP Protocol Layer                     │
│  (JSON-RPC messages)                    │
│  - tools/list                           │
│  - tools/call                           │
│  - resources/list                       │
│  - prompts/list                         │
└─────────────────────────────────────────┘
                  ↕
┌─────────────────────────────────────────┐
│  Transport Layer                        │
│  (stdio or HTTP/SSE)                    │
└─────────────────────────────────────────┘
```

**Key Insight:** As long as your language can implement the MCP Protocol Layer (JSON-RPC), you can build an MCP server!

### Standard Methods (Any Language Must Implement):

- `initialize` - Server initialization handshake
- `tools/list` - Return available tools
- `tools/call` - Execute a tool
- `resources/list` - List available resources
- `resources/read` - Read resource content
- `prompts/list` - List available prompts
- `prompts/get` - Get a prompt

---

## Advanced: HTTP Transport (Alternative to stdio)

### Why HTTP?

Some languages are better suited for HTTP servers:

```json
{
  "servers": {
    "remote-mcp": {
      "type": "sse",
      "url": "http://localhost:8080/mcp"
    }
  }
}
```

**Advantages:**
- Can run on remote servers
- Better for long-running services
- Multiple clients can connect
- Web-friendly deployment

**Languages that prefer HTTP:**
- Java/Spring Boot
- .NET/ASP.NET
- Ruby/Rails
- PHP

---

## Resources & Further Reading

### Official Documentation:
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)

### Example Implementations:
- [Azure DevOps MCP (Node.js)](https://github.com/microsoft/azure-devops-mcp)
- [MCP Servers Collection](https://github.com/modelcontextprotocol/servers)

### Language-Specific SDKs:
- **Node.js:** `npm install @modelcontextprotocol/sdk`
- **Python:** `pip install mcp`
- **Go:** Community implementations (check GitHub)
- **Rust:** Community implementations (check crates.io)

---

## Summary

### Key Takeaways:

🌍 **MCP is language-agnostic** - Any language can build MCP servers

📦 **Node.js is most popular** - 70% of servers use it for good reasons

🐍 **Python is second choice** - Excellent for data science use cases

🚀 **Go/Rust for performance** - When speed matters most

🏢 **Java/.NET for enterprise** - Integration with existing systems

✅ **Your Node.js choice is optimal** - Perfect for Azure DevOps integration

💡 **Multiple servers can coexist** - Mix languages based on needs

---

*Last Updated: January 31, 2026*
*Authors: Saravanan R (1540326), Shiyamkumar U (2002918)*
