import { describe, it, expect, beforeEach, vi } from 'vitest';
import { createMockServer, isValidToolResponse } from '@sc-node-mcp/shared-tests/helpers/mockServer';
import { createMockDriver, createMockElement } from './helpers/mockDriver.js';

vi.mock('../src/driver.js', () => ({ getActiveDriver: vi.fn() }));

const { getActiveDriver } = await import('../src/driver.js');
const { configureNavigationTools } = await import('../src/tools/navigation.js');

describe('navigation tools', () => {
  let server;

  beforeEach(() => {
    vi.clearAllMocks();
    server = createMockServer();
    configureNavigationTools(server);
  });

  it('browser_navigate navigates to the given URL', async () => {
    const driver = createMockDriver();
    getActiveDriver.mockReturnValue(driver);
    const response = await server.invokeTool('browser_navigate', { url: 'https://example.com' });
    expect(driver.get).toHaveBeenCalledWith('https://example.com');
    expect(isValidToolResponse(response)).toBe(true);
  });

  it('browser_navigate returns an error when there is no active session', async () => {
    getActiveDriver.mockImplementation(() => {
      throw new Error('No active browser session. Call browser_start first.');
    });
    const response = await server.invokeTool('browser_navigate', { url: 'https://example.com' });
    expect(response.isError).toBe(true);
  });

  it('browser_navigate_back goes back in history', async () => {
    const driver = createMockDriver();
    getActiveDriver.mockReturnValue(driver);
    await server.invokeTool('browser_navigate_back', {});
    expect(driver.navigate().back).toHaveBeenCalled();
  });

  it('browser_navigate_forward goes forward in history', async () => {
    const driver = createMockDriver();
    getActiveDriver.mockReturnValue(driver);
    await server.invokeTool('browser_navigate_forward', {});
    expect(driver.navigate().forward).toHaveBeenCalled();
  });

  it('browser_refresh reloads the page', async () => {
    const driver = createMockDriver();
    getActiveDriver.mockReturnValue(driver);
    await server.invokeTool('browser_refresh', {});
    expect(driver.navigate().refresh).toHaveBeenCalled();
  });

  it('browser_get_page_info returns url and title', async () => {
    const driver = createMockDriver({
      getCurrentUrl: vi.fn().mockResolvedValue('https://example.com'),
      getTitle: vi.fn().mockResolvedValue('Example Title')
    });
    getActiveDriver.mockReturnValue(driver);
    const response = await server.invokeTool('browser_get_page_info', {});
    const parsed = JSON.parse(response.content[0].text);
    expect(parsed).toEqual({ url: 'https://example.com', title: 'Example Title' });
  });

  it('browser_get_page_source returns the full source when short', async () => {
    const driver = createMockDriver({ getPageSource: vi.fn().mockResolvedValue('<html>short</html>') });
    getActiveDriver.mockReturnValue(driver);
    const response = await server.invokeTool('browser_get_page_source', {});
    expect(response.content[0].text).toBe('<html>short</html>');
  });

  it('browser_get_page_source truncates long source', async () => {
    const longSource = 'a'.repeat(20000);
    const driver = createMockDriver({ getPageSource: vi.fn().mockResolvedValue(longSource) });
    getActiveDriver.mockReturnValue(driver);
    const response = await server.invokeTool('browser_get_page_source', {});
    expect(response.content[0].text).toContain('[truncated]');
    expect(response.content[0].text.length).toBeLessThan(longSource.length);
  });

  const OTHER_TOOLS = [
    'browser_navigate_back',
    'browser_navigate_forward',
    'browser_refresh',
    'browser_get_page_info',
    'browser_get_page_source',
    'browser_wait_for_text'
  ];

  it.each(OTHER_TOOLS)('%s returns an error when there is no active session', async (name) => {
    getActiveDriver.mockImplementation(() => {
      throw new Error('No active browser session. Call browser_start first.');
    });
    const response = await server.invokeTool(name, {});
    expect(response.isError).toBe(true);
  });

  describe('browser_wait_for_text', () => {
    it('resolves when driver.wait finds one of the given text strings', async () => {
      const driver = createMockDriver({ wait: vi.fn().mockResolvedValue('Hello world') });
      getActiveDriver.mockReturnValue(driver);

      const response = await server.invokeTool('browser_wait_for_text', { text: ['Hello world'], timeout: 5000 });

      expect(driver.wait).toHaveBeenCalledWith(expect.any(Function), 5000);
      expect(response.content[0].text).toContain('Hello world');
      expect(isValidToolResponse(response)).toBe(true);
    });

    it('the wait predicate returns the first matching text found in the page body', async () => {
      const element = createMockElement({ getText: vi.fn().mockResolvedValue('Some Hello world text') });
      const driver = createMockDriver({
        findElement: vi.fn().mockReturnValue(element),
        wait: vi.fn().mockImplementation(async (predicate) => predicate())
      });
      getActiveDriver.mockReturnValue(driver);

      const response = await server.invokeTool('browser_wait_for_text', { text: ['Nope', 'Hello world'] });

      expect(response.content[0].text).toContain('Hello world');
    });

    it('the wait predicate returns false when no candidate text is found', async () => {
      const element = createMockElement({ getText: vi.fn().mockResolvedValue('Nothing relevant here') });
      const driver = createMockDriver({
        findElement: vi.fn().mockReturnValue(element),
        wait: vi.fn().mockImplementation(async (predicate) => predicate())
      });
      getActiveDriver.mockReturnValue(driver);

      const response = await server.invokeTool('browser_wait_for_text', { text: ['Nope'] });

      expect(response.content[0].text).toContain('Found text: "false"');
    });

    it('returns an error when the wait times out', async () => {
      const driver = createMockDriver({ wait: vi.fn().mockRejectedValue(new Error('Wait timed out after 1000ms')) });
      getActiveDriver.mockReturnValue(driver);

      const response = await server.invokeTool('browser_wait_for_text', { text: ['x'], timeout: 1000 });

      expect(response.isError).toBe(true);
    });
  });
});
