import { describe, it, expect, beforeEach } from 'vitest';
import { configureScwikiTools } from '../src/tools.js';
import { createMockServer } from '@sc-node-mcp/shared-tests/helpers/mockServer';

describe('SC Wiki Tools Module', () => {
  let mockServer;
  let scwikiConfig;

  beforeEach(() => {
    mockServer = createMockServer();
    scwikiConfig = {
      baseUrl: 'https://scwiki.example.com',
      token: 'test-bearer-token',
      wiki: 'xwiki'
    };
  });

  describe('configureScwikiTools', () => {
    it('should be a function', () => {
      expect(typeof configureScwikiTools).toBe('function');
    });

    it('should accept server and config parameters', () => {
      expect(() => {
        configureScwikiTools(mockServer, scwikiConfig);
      }).not.toThrow();
    });

    it('should register tools on the provided server', () => {
      configureScwikiTools(mockServer, scwikiConfig);

      expect(mockServer.tool).toHaveBeenCalled();
      expect(mockServer.tool.mock.calls.length).toBeGreaterThan(0);
    });

    it('should handle null config gracefully', () => {
      expect(() => {
        configureScwikiTools(mockServer, null);
      }).not.toThrow();
    });
  });
});
