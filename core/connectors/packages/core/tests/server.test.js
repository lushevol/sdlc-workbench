import { describe, it, expect, vi, beforeEach } from 'vitest';
import { createMcpServer, startMcpServer } from '../src/server.js';
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';

// Mock SDK modules
vi.mock('@modelcontextprotocol/sdk/server/mcp.js');
vi.mock('@modelcontextprotocol/sdk/server/stdio.js');

describe('Core Server', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('createMcpServer', () => {
    it('should wrap the tool method and increment toolCount', async () => {
      const originalTool = vi.fn();
      const mockServerWithTool = { tool: originalTool };
      McpServer.mockImplementation(function() { return mockServerWithTool; });

      const server = createMcpServer('test', '1.0.0');

      // tool should be replaced with a wrapper
      expect(server.tool).not.toBe(originalTool);
      expect(server.toolCount).toBe(0);

      // Register a tool — should increment toolCount and delegate to originalTool
      const handler = vi.fn().mockResolvedValue({ content: [{ type: 'text', text: 'result' }] });
      server.tool('my_tool', 'desc', {}, handler);

      expect(server.toolCount).toBe(1);
      expect(originalTool).toHaveBeenCalledTimes(1);

      // The wrapped handler should call the original and log status
      const wrappedHandler = originalTool.mock.calls[0].at(-1);
      const errorSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
      await wrappedHandler({}, {});
      expect(handler).toHaveBeenCalled();
      expect(errorSpy).toHaveBeenCalledWith(expect.stringContaining('my_tool'));
      errorSpy.mockRestore();
    });

    it('should log error status when tool handler returns isError', async () => {
      const originalTool = vi.fn();
      McpServer.mockImplementation(function() { return { tool: originalTool }; });

      const server = createMcpServer('test', '1.0.0');
      const handler = vi.fn().mockResolvedValue({ isError: true, content: [{ type: 'text', text: 'err' }] });
      server.tool('failing_tool', 'desc', {}, handler);

      const wrappedHandler = originalTool.mock.calls[0].at(-1);
      const errorSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
      await wrappedHandler({}, {});
      expect(errorSpy).toHaveBeenCalledWith(expect.stringContaining('error'));
      errorSpy.mockRestore();
    });

    it('should create MCP server with provided name and version', () => {
      const mockServer = { name: 'test-server', version: '1.0.0' };
      McpServer.mockImplementation(function() { return mockServer; });

      const server = createMcpServer('test-server', '1.0.0');

      expect(McpServer).toHaveBeenCalledWith({
        name: 'test-server',
        version: '1.0.0',
        capabilities: {
          resources: {},
          tools: {},
          prompts: {}
        }
      });
      expect(server).toBe(mockServer);
    });

    it('should create server with different names', () => {
      const mockServer = { name: 'ado-server', version: '2.0.0' };
      McpServer.mockImplementation(function() { return mockServer; });

      const server = createMcpServer('ado-server', '2.0.0');

      expect(McpServer).toHaveBeenCalledWith(
        expect.objectContaining({
          name: 'ado-server',
          version: '2.0.0'
        })
      );
    });

    it('should create server with default capabilities structure', () => {
      McpServer.mockImplementation(function(config) { return config; });

      const server = createMcpServer('test', '1.0.0');

      expect(server.capabilities).toEqual({
        resources: {},
        tools: {},
        prompts: {}
      });
    });

    it('should pass through a tool() call whose last argument is not a handler function', () => {
      const originalTool = vi.fn();
      McpServer.mockImplementation(function() { return { tool: originalTool }; });

      const server = createMcpServer('test', '1.0.0');
      server.tool('schema_only_tool', 'desc', { some: 'schema' });

      expect(server.toolCount).toBe(1);
      expect(originalTool).toHaveBeenCalledWith('schema_only_tool', 'desc', { some: 'schema' });
    });
  });

  describe('startMcpServer', () => {
    it('should create transport and connect server', async () => {
      const mockTransport = {
        start: vi.fn(),
        close: vi.fn()
      };
      const mockServer = {
        connect: vi.fn().mockResolvedValue(undefined),
        name: 'test-server'
      };

      StdioServerTransport.mockImplementation(function() { return mockTransport; });

      const result = await startMcpServer(mockServer);

      expect(StdioServerTransport).toHaveBeenCalled();
      expect(mockServer.connect).toHaveBeenCalledWith(mockTransport);
      expect(result).toBe(mockServer);
    });

    it('should handle connection errors', async () => {
      const mockTransport = { start: vi.fn(), close: vi.fn() };
      const mockServer = {
        connect: vi.fn().mockRejectedValue(new Error('Connection failed'))
      };

      StdioServerTransport.mockImplementation(function() { return mockTransport; });

      await expect(startMcpServer(mockServer)).rejects.toThrow('Connection failed');
      expect(mockServer.connect).toHaveBeenCalledWith(mockTransport);
    });

    it('should return the connected server', async () => {
      const mockTransport = { start: vi.fn() };
      const mockServer = {
        connect: vi.fn().mockResolvedValue(undefined),
        name: 'connected-server'
      };

      StdioServerTransport.mockImplementation(function() { return mockTransport; });

      const result = await startMcpServer(mockServer);

      expect(result).toBe(mockServer);
      expect(result.name).toBe('connected-server');
    });
  });

  describe('Integration', () => {
    it('should create and start server in sequence', async () => {
      const mockTransport = { start: vi.fn() };
      const mockServerInstance = {
        connect: vi.fn().mockResolvedValue(undefined),
        name: 'integration-test'
      };

      McpServer.mockImplementation(function() { return mockServerInstance; });
      StdioServerTransport.mockImplementation(function() { return mockTransport; });

      const server = createMcpServer('integration-test', '1.0.0');
      const startedServer = await startMcpServer(server);

      expect(McpServer).toHaveBeenCalled();
      expect(StdioServerTransport).toHaveBeenCalled();
      expect(mockServerInstance.connect).toHaveBeenCalledWith(mockTransport);
      expect(startedServer).toBe(mockServerInstance);
    });
  });
});
