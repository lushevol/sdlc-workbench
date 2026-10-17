import { describe, it, expect, beforeEach, vi } from 'vitest';
import { createMockServer, isValidToolResponse } from '@sc-node-mcp/shared-tests/helpers/mockServer';
import { createMockDriver } from './helpers/mockDriver.js';

vi.mock('../src/driver.js', () => ({
  buildDriver: vi.fn(),
  clearActiveDriver: vi.fn(),
  hasActiveDriver: vi.fn(),
  getActiveDriver: vi.fn()
}));

const { buildDriver, clearActiveDriver, hasActiveDriver, getActiveDriver } = await import('../src/driver.js');
const { configureSessionTools } = await import('../src/tools/session.js');

describe('session tools', () => {
  let server;

  beforeEach(() => {
    vi.clearAllMocks();
    server = createMockServer();
    configureSessionTools(server);
  });

  describe('browser_start', () => {
    it('launches a browser session', async () => {
      buildDriver.mockResolvedValue({});
      const response = await server.invokeTool('browser_start', { browser: 'chrome', headless: false });
      expect(isValidToolResponse(response)).toBe(true);
      expect(buildDriver).toHaveBeenCalledWith(expect.objectContaining({ browser: 'chrome' }));
      expect(response.content[0].text).toContain('chrome');
    });

    it('returns an error when buildDriver fails', async () => {
      buildDriver.mockRejectedValue(new Error('No driver path configured for "chrome"'));
      const response = await server.invokeTool('browser_start', { browser: 'chrome' });
      expect(response.isError).toBe(true);
      expect(response.content[0].text).toContain('No driver path configured');
    });
  });

  describe('browser_close', () => {
    it('reports a closed session', async () => {
      hasActiveDriver.mockReturnValue(true);
      clearActiveDriver.mockResolvedValue(undefined);
      const response = await server.invokeTool('browser_close', {});
      expect(isValidToolResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('closed');
    });

    it('reports no active session', async () => {
      hasActiveDriver.mockReturnValue(false);
      clearActiveDriver.mockResolvedValue(undefined);
      const response = await server.invokeTool('browser_close', {});
      expect(response.content[0].text).toContain('No active browser session');
    });

    it('returns an error when clearActiveDriver fails', async () => {
      hasActiveDriver.mockReturnValue(true);
      clearActiveDriver.mockRejectedValue(new Error('quit failed'));
      const response = await server.invokeTool('browser_close', {});
      expect(response.isError).toBe(true);
    });
  });

  describe('browser_set_timeouts', () => {
    it('sets only the provided timeouts on the active driver', async () => {
      const driver = createMockDriver();
      getActiveDriver.mockReturnValue(driver);
      const response = await server.invokeTool('browser_set_timeouts', { implicitMs: 5000 });
      expect(driver.manage().setTimeouts).toHaveBeenCalledWith({ implicit: 5000 });
      expect(isValidToolResponse(response)).toBe(true);
    });

    it('sets all three timeouts when all are provided', async () => {
      const driver = createMockDriver();
      getActiveDriver.mockReturnValue(driver);
      await server.invokeTool('browser_set_timeouts', { implicitMs: 1000, pageLoadMs: 2000, scriptMs: 3000 });
      expect(driver.manage().setTimeouts).toHaveBeenCalledWith({ implicit: 1000, pageLoad: 2000, script: 3000 });
    });

    it('returns an error when there is no active session', async () => {
      getActiveDriver.mockImplementation(() => {
        throw new Error('No active browser session. Call browser_start first.');
      });
      const response = await server.invokeTool('browser_set_timeouts', {});
      expect(response.isError).toBe(true);
    });
  });
});
