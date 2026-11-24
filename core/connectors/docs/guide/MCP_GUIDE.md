# Model Context Protocol (MCP) Guide

## What is MCP?

Model Context Protocol (MCP) is an open protocol that standardizes integration and automation between developer tools, code editors, and cloud services. MCP enables tools ("servers") to expose capabilities—such as querying work items, managing repositories, or automating workflows—so that clients (like VS Code extensions or automation tools) can discover and use them in a consistent, dynamic way.

### Key Concepts

- Enables dynamic discovery and invocation of APIs
- Reduces the need for custom integrations for each tool or service
- Facilitates automation, scripting, and advanced developer workflows

## MCP Architecture Deep Dive

### Core Components

MCP operates on a client-server architecture with three fundamental components:

1. **MCP Server**: A process that exposes tools (functions) and resources through standardized interfaces. Servers are typically implemented in Node.js, Python, or other languages and run as separate processes.

2. **MCP Client**: An application (like VS Code, Claude Desktop, or custom scripts) that discovers and invokes tools exposed by MCP servers.

3. **Transport Layer**: The communication channel between client and server. MCP supports multiple transports:
   - **stdio** (Standard Input/Output): Default transport for local processes
   - **HTTP/SSE** (Server-Sent Events): For remote servers and web-based clients
   - **WebSockets**: For bidirectional, real-time communication

### Protocol Flow

```
[MCP Client] <--> [Transport Layer] <--> [MCP Server] <--> [External APIs]
     |                                          |
   VS Code                                 Azure DevOps
  Copilot                                  Confluence
                                           GitHub, etc.
```

1. **Initialization**: Client starts server process and establishes connection
2. **Capability Discovery**: Server announces available tools, resources, and prompts
3. **Tool Invocation**: Client sends tool requests with parameters
4. **Response Handling**: Server executes tool and returns structured JSON response
5. **Error Management**: Standardized error responses with `isError` flag

## How Node.js and npx Power MCP Servers

### The Role of Node.js

Node.js is the runtime environment that executes MCP server code. When an MCP server is implemented in JavaScript/TypeScript (like this project), Node.js provides:

- **Process Management**: Runs the server as a separate process with its own memory space
- **Event Loop**: Handles asynchronous operations (API calls, file I/O) without blocking
- **Module System**: Loads dependencies (Azure DevOps SDK, MCP SDK) at runtime
- **stdio Interface**: Provides standard input/output streams for communication with the client

**Example Server Startup**:
```bash
# Direct node execution
node packages/unified/src/index.js

# What happens:
# 1. Node.js loads index.js and all its imports
# 2. Server initializes MCP SDK and registers tools
# 3. Server listens on stdin for client messages
# 4. Server writes responses to stdout (JSON-RPC format)
```

### The Role of npx

`npx` is a package runner tool that comes with npm (Node Package Manager). It simplifies MCP server execution by:

1. **Package Resolution**: Automatically downloads and caches npm packages without requiring global installation
2. **Version Management**: Ensures the correct package version is used for each invocation
3. **Temporary Execution**: Runs packages directly without polluting global namespace

**MCP Configuration with npx**:
```json
{
  "mcpServers": {
    "azure-devops": {
      "command": "npx",
      "args": ["-y", "@sc-node-mcp/unified"]
    }
  }
}
```

**What npx does**:
```
npx @sc-node-mcp/unified
  ↓
1. Checks npm cache for package
2. Downloads from npm registry if missing
3. Locates package entry point (usually bin/index.js)
4. Executes: node <path-to-package>/index.js
5. Package runs as MCP server on stdio transport
```

### Local Development vs Production

**Development Mode** (Direct Node):
```json
{
  "command": "node",
  "args": ["${workspaceFolder}/packages/unified/src/index.js"]
}
```
- Runs source code directly without build step
- Immediate feedback during development
- Uses local dependencies from node_modules
```
            [SSE Stream for events]
                    |
          [Authentication Middleware]
              [Rate Limiting]
              [Load Balancer]
```

**1. Tool Discovery (GET /tools)**:

```http
GET /tools HTTP/1.1
Host: mcp-server.example.com
Authorization: Bearer <token>

Response:
{
  "tools": [
    {
      "name": "wit_get_work_item",
      "description": "Retrieve work item by ID",
      "inputSchema": {
        "type": "object",
        "properties": {
          "id": {"type": "number"}
        }
      }
    }
  ]
```

**2. Tool Invocation (POST /invoke)**:
```http
Authorization: Bearer <token>
Content-Type: application/json

{
  "tool": "wit_get_work_item",
}

  "content": [
    {
      "type": "text",
      "text": "{\"id\": 123456, \"title\": \"Fix bug\", ...}"
    }
```
**3. Server-Sent Events (SSE) for Streaming**:

```http
GET /sse HTTP/1.1
Host: mcp-server.example.com
Authorization: Bearer <token>
Accept: text/event-stream

Response:
Content-Type: text/event-stream

data: {"type": "tool_result", "status": "in_progress"}
data: {"type": "tool_result", "status": "complete", "content": [...]}
```

### Implementing HTTP MCP Server

**Express.js Example**:
```javascript
import { createHTTPServer } from '@modelcontextprotocol/sdk/http';
import express from 'express';

const app = express();
const mcpServer = createHTTPServer(/* tools config */);

// Mount MCP endpoints
app.use('/mcp', mcpServer.router);

// Authentication middleware
app.use((req, res, next) => {
  const token = req.headers.authorization?.replace('Bearer ', '');
  if (!validateToken(token)) {
    return res.status(401).json({ error: 'Unauthorized' });
  }
  next();
});

app.listen(3000, () => {
  console.log('MCP HTTP server running on port 3000');
});
```

### HTTP MCP Security Considerations

1. **Authentication**: Use OAuth 2.0, API keys, or JWT tokens
2. **Authorization**: Validate user permissions before tool execution
3. **TLS/SSL**: Always use HTTPS in production
4. **Rate Limiting**: Prevent abuse with request throttling
5. **CORS**: Configure Cross-Origin Resource Sharing for web clients
6. **Input Validation**: Sanitize all tool parameters to prevent injection attacks

### When to Use HTTP MCP

**Choose HTTP MCP when**:
- Deploying server to cloud (AWS, Azure, GCP)
- Supporting web-based clients or browser extensions
- Sharing server across multiple users/teams
- Implementing centralized authentication and auditing
- Scaling horizontally with load balancers

**Stick with stdio MCP when**:
- Running locally in VS Code or IDE
- Single-user development workflows
- No need for remote access
- Simpler setup and configuration
- Better performance for local operations

## Message Format and JSON-RPC

MCP uses JSON-RPC 2.0 as its message format for both stdio and HTTP transports.

### Request Message Structure

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "wit_get_work_item",
    "arguments": {
      "id": 123456
    }
  }
}
```

### Response Message Structure

**Success**:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "{\"id\": 123456, \"title\": \"Example\"}"
      }
    ]
  }
}
```

**Error**:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32603,
    "message": "Internal error",
    "data": "Work item not found"
  }
}
```

### MCP-Specific Methods

- `initialize`: Handshake between client and server
- `tools/list`: Discover available tools
- `tools/call`: Invoke a specific tool
- `resources/list`: List available resources
- `resources/read`: Read a specific resource
- `prompts/list`: List available prompt templates
- `prompts/get`: Retrieve a prompt template

## How MCP Works in Practice

1. **Server Registration:** Each MCP server describes its available tools (APIs) and capabilities in a machine-readable format. This allows clients to discover what actions are possible without prior knowledge of the server's implementation.
2. **Communication:** MCP servers and clients typically communicate over standard input/output (stdio), but the protocol is transport-agnostic and could be extended to sockets or other channels.
3. **Tool Invocation:** Clients send requests to invoke specific tools (e.g., list work items, create a pull request) with parameters. The server executes the requested action and returns a structured response.
4. **Dynamic Discovery:** Because the protocol is standardized, new tools can be added to servers and immediately become available to clients without requiring client-side updates.

## Use Cases for MCP

- **Editor Integration:** Connect code editors (like VS Code) to cloud services, CI/CD systems, or project management tools for seamless workflows.
- **Automation:** Script complex developer workflows by chaining together MCP tool invocations across multiple servers.
- **Custom Developer Portals:** Build dashboards or portals that aggregate and automate actions from many different tools using a single protocol.

## Why Use MCP?

- **Extensibility:** Easily add new tools and capabilities to your developer environment.
- **Interoperability:** Connect disparate systems and services without custom adapters for each integration.
- **Maintainability:** Reduce the maintenance burden by relying on a common protocol and discoverable APIs.
- **Security:** Centralize authentication and authorization at the server level, reducing the risk of credential sprawl.

## Getting Started with MCP

### VS Code

1. **Install GitHub Copilot extension** (includes MCP client support).
2. **Configure Servers:** Define your MCP servers in `.vscode/mcp.json` in your workspace:
   ```json
   {
     "mcpServers": {
       "sc-node-mcp": {
         "command": "node",
         "args": ["<path-to>/packages/unified/src/index.js"],
         "env": {
           "AZURE_DEVOPS_PAT": "<your-pat>"
         }
       }
     }
   }
   ```
3. **Discover Tools:** Open Copilot Chat and use `@` to invoke tools.
4. **Automate Workflows:** Chain tool invocations to automate repetitive or complex tasks.

### IntelliJ IDEA

MCP is supported in IntelliJ via the **GitHub Copilot plugin** (v1.5+). The MCP server runs identically — only the config file location and format differ.

#### Prerequisites
- IntelliJ IDEA 2024.1 or later (any edition: Community, Ultimate, etc.)
- GitHub Copilot plugin installed and signed in
- Node.js 18+ installed

#### Setup Steps

1. **Install the GitHub Copilot plugin:**
   - Go to `File → Settings → Plugins → Marketplace`
   - Search for **"GitHub Copilot"** → Install → Restart IntelliJ

2. **Create or edit the MCP config file** at:
   ```
   %LOCALAPPDATA%\github-copilot\intellij\mcp.json
   ```
   On Windows: `C:\Users\<username>\AppData\Local\github-copilot\intellij\mcp.json`

3. **Add your server configuration** (note: IntelliJ uses `"servers"` key and requires `"type": "stdio"`):
   ```json
   {
     "servers": {
       "sc-node-mcp": {
         "type": "stdio",
         "command": "C:\\Program Files\\nodejs\\node.exe",
         "args": [
           "<full-path-to>\\packages\\unified\\src\\index.js"
         ],
         "env": {
           "AZURE_DEVOPS_PAT": "<your-pat>",
           "HTTPS_PROXY": "<your-proxy-if-needed>",
           "NODE_TLS_REJECT_UNAUTHORIZED": "0",
           "CONFLUENCE_PAT": "<your-confluence-pat>"
         }
       }
     }
   }
   ```

4. **Restart IntelliJ** — open Copilot Chat and MCP tools will be available.

#### VS Code vs IntelliJ Config Comparison

| Aspect | VS Code | IntelliJ |
|--------|---------|----------|
| Config location | `.vscode/mcp.json` (workspace) | `%LOCALAPPDATA%\github-copilot\intellij\mcp.json` (global) |
| Root key | `"mcpServers"` | `"servers"` |
| `type` field | Not required | Required: `"type": "stdio"` |
| Scope | Per workspace | Global (all projects) |
| Requires | Copilot Chat extension | GitHub Copilot plugin |

> **Tip:** The MCP server itself (`packages/unified/src/index.js`) is identical for both clients — only the config file location and format differs.


> **Tip:** For a full step-by-step IntelliJ configuration walkthrough, see the [IntelliJ Setup Guide](../INTELLIJ_SETUP.md).

## MCP in This Project

By running the included servers, you can:
- Query and manage work items
- List and manage repositories, branches, and pull requests
- Perform automated PR reviews with customizable guidelines
- Integrate these capabilities into your editor or automation scripts with minimal setup

## Further Reading

- [Model Context Protocol Documentation](https://modelcontextprotocol.io/) (if available)
- [Use MCP servers in VS Code](https://code.visualstudio.com/docs/copilot/chat/mcp-servers)
- [MCP SDK on GitHub](https://github.com/modelcontextprotocol/sdk)
- [JSON-RPC 2.0 Specification](https://www.jsonrpc.org/specification)
- [Server-Sent Events (SSE) Specification](https://html.spec.whatwg.org/multipage/server-sent-events.html)

## Troubleshooting Common Issues

### stdio Transport Issues

**Server not starting**:
- Check Node.js version (requires v18+)
- Verify config.json exists with required credentials
- Check stderr output for initialization errors

**Tools not discovered**:
- Ensure server initialization completes successfully
- Check client MCP configuration syntax
- Verify server process is running (check Task Manager/Activity Monitor)

### HTTP Transport Issues

**Connection refused**:
- Verify server is listening on correct port
- Check firewall rules allow connections
- Ensure HTTPS certificates are valid

**Authentication failures**:
- Verify Bearer token is valid and not expired
- Check authorization headers are properly formatted
- Ensure server authentication middleware is configured

**CORS errors**:
- Configure CORS headers on server: `Access-Control-Allow-Origin`
- Set allowed methods: `Access-Control-Allow-Methods`
- Include credentials if needed: `Access-Control-Allow-Credentials`

### Performance Optimization

**stdio Transport**:
- Keep server process running (avoid repeated restarts)
- Use connection pooling for external APIs
- Cache frequently accessed data

**HTTP Transport**:
- Implement HTTP caching headers (ETag, Cache-Control)
- Use CDN for static assets
- Enable gzip/brotli compression
- Deploy close to users (regional endpoints)
