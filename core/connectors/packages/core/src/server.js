import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';

export function createMcpServer(name, version) {
  const mcpServer = new McpServer({
    name,
    version,
    capabilities: {
      resources: {},
      tools: {},
      prompts: {},
    },
  });

  // Wrap .tool() to emit per-call logs and track count
  // NOTE: .tool() is deprecated by the SDK's own types in favor of .registerTool(),
  // but is kept here intentionally for backward compatibility with existing callers.
  let toolCount = 0;
  if (typeof mcpServer.tool === 'function') {
    const originalTool = mcpServer.tool.bind(mcpServer);
    mcpServer.tool = function (...args) {
      const toolName = args[0];
      const lastArg = args.at(-1);
      if (typeof lastArg === 'function') {
        args[args.length - 1] = async function (params, extra) {
          const result = await lastArg(params, extra);
          const status = result?.isError ? 'error' : 'ok';
          console.error(`[SC-NODE-MCP] Tool: ${toolName} → ${status}`);
          return result;
        };
      }
      toolCount++;
      return originalTool(...args);
    };
  }

  Object.defineProperty(mcpServer, 'toolCount', { get: () => toolCount });

  return mcpServer;
}

export async function startMcpServer(server) {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  return server;
}
