import { describe, it, expect, vi, beforeEach } from 'vitest';
import { configureConfluenceTools } from '../src/tools.js';
import { createMockServer } from '@sc-node-mcp/shared-tests/helpers/mockServer';

describe('Confluence Tools Module', () => {
  let mockServer;
  let confluenceConfig;

  beforeEach(() => {
    mockServer = createMockServer();
    confluenceConfig = {
      baseUrl: 'https://confluence.example.com',
      token: 'test-bearer-token'
    };
  });

  describe('configureConfluenceTools', () => {
    it('should be a function', () => {
      expect(typeof configureConfluenceTools).toBe('function');
    });

    it('should accept server and config parameters', () => {
      expect(() => {
        configureConfluenceTools(mockServer, confluenceConfig);
      }).not.toThrow();
    });

    it('should register tools on the provided server', () => {
      configureConfluenceTools(mockServer, confluenceConfig);

      expect(mockServer.tool).toHaveBeenCalled();
      expect(mockServer.tool.mock.calls.length).toBeGreaterThan(0);
    });

    it('should handle null config gracefully', () => {
      expect(() => {
        configureConfluenceTools(mockServer, null);
      }).not.toThrow();
    });

    it('should handle undefined config gracefully', () => {
      expect(() => {
        configureConfluenceTools(mockServer, undefined);
      }).not.toThrow();
    });

    it('should register correct tool names', () => {
      configureConfluenceTools(mockServer, confluenceConfig);

      const toolNames = mockServer.getRegisteredTools().map(t => t.name);
      expect(toolNames).toContain('confluence_list_my_pages');
      expect(toolNames).toContain('confluence_search');
      expect(toolNames).toContain('confluence_update_page');
      expect(toolNames).toContain('confluence_get_page_id');
      expect(toolNames).toContain('confluence_create_page');
      expect(toolNames).toContain('confluence_read_page');
    });
  });
});
