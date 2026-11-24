import { describe, it, expect, beforeEach, vi } from 'vitest';
import { createMockServer, isValidToolResponse } from '@sc-node-mcp/shared-tests/helpers/mockServer';
import { createMockDriver } from './helpers/mockDriver.js';

vi.mock('../src/driver.js', () => ({ getActiveDriver: vi.fn() }));

const { getActiveDriver } = await import('../src/driver.js');
const { configureCookieTools } = await import('../src/tools/cookies.js');

describe('cookie tools', () => {
  let server;

  beforeEach(() => {
    vi.clearAllMocks();
    server = createMockServer();
    configureCookieTools(server);
  });

  it('cookie_add adds a cookie with only the provided fields', async () => {
    const driver = createMockDriver();
    getActiveDriver.mockReturnValue(driver);

    const response = await server.invokeTool('cookie_add', { name: 'session', value: 'abc123' });

    expect(driver.manage().addCookie).toHaveBeenCalledWith({ name: 'session', value: 'abc123' });
    expect(isValidToolResponse(response)).toBe(true);
  });

  it('cookie_add passes through optional fields when given', async () => {
    const driver = createMockDriver();
    getActiveDriver.mockReturnValue(driver);

    await server.invokeTool('cookie_add', {
      name: 'session',
      value: 'abc123',
      domain: '.example.com',
      path: '/',
      secure: true,
      httpOnly: true,
      expiry: 1234567890
    });

    expect(driver.manage().addCookie).toHaveBeenCalledWith({
      name: 'session',
      value: 'abc123',
      domain: '.example.com',
      path: '/',
      secure: true,
      httpOnly: true,
      expiry: 1234567890
    });
  });

  it('cookie_get returns all cookies when no name is given', async () => {
    const cookies = [{ name: 'a', value: '1' }];
    const driver = createMockDriver({ manage: vi.fn() });
    driver.manage.mockReturnValue({ getCookies: vi.fn().mockResolvedValue(cookies), getCookie: vi.fn() });
    getActiveDriver.mockReturnValue(driver);

    const response = await server.invokeTool('cookie_get', {});

    expect(JSON.parse(response.content[0].text)).toEqual(cookies);
  });

  it('cookie_get returns a single cookie by name', async () => {
    const cookie = { name: 'session', value: 'abc123' };
    const driver = createMockDriver({ manage: vi.fn() });
    driver.manage.mockReturnValue({ getCookie: vi.fn().mockResolvedValue(cookie), getCookies: vi.fn() });
    getActiveDriver.mockReturnValue(driver);

    const response = await server.invokeTool('cookie_get', { name: 'session' });

    expect(JSON.parse(response.content[0].text)).toEqual(cookie);
  });

  it('cookie_delete deletes a specific cookie by name', async () => {
    const driver = createMockDriver();
    getActiveDriver.mockReturnValue(driver);

    const response = await server.invokeTool('cookie_delete', { name: 'session' });

    expect(driver.manage().deleteCookie).toHaveBeenCalledWith('session');
    expect(isValidToolResponse(response)).toBe(true);
  });

  it('cookie_delete deletes all cookies when no name is given', async () => {
    const driver = createMockDriver();
    getActiveDriver.mockReturnValue(driver);

    await server.invokeTool('cookie_delete', {});

    expect(driver.manage().deleteAllCookies).toHaveBeenCalled();
  });

  it('returns an error when there is no active session', async () => {
    getActiveDriver.mockImplementation(() => {
      throw new Error('No active browser session. Call browser_start first.');
    });
    const response = await server.invokeTool('cookie_get', {});
    expect(response.isError).toBe(true);
  });

  const OTHER_TOOLS = [
    ['cookie_add', { name: 'a', value: '1' }],
    ['cookie_delete', {}]
  ];

  it.each(OTHER_TOOLS)('%s returns an error when there is no active session', async (name, params) => {
    getActiveDriver.mockImplementation(() => {
      throw new Error('No active browser session. Call browser_start first.');
    });
    const response = await server.invokeTool(name, params);
    expect(response.isError).toBe(true);
  });
});
