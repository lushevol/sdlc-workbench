import { describe, it, expect, beforeEach, vi } from 'vitest';
import { createMockServer, isValidToolResponse } from '@sc-node-mcp/shared-tests/helpers/mockServer';
import { createMockDriver, createMockElement } from './helpers/mockDriver.js';

vi.mock('../src/driver.js', () => ({ getActiveDriver: vi.fn() }));

const { getActiveDriver } = await import('../src/driver.js');
const { configureWindowTools } = await import('../src/tools/windows.js');

describe('window_manage', () => {
  let server;

  beforeEach(() => {
    vi.clearAllMocks();
    server = createMockServer();
    configureWindowTools(server);
  });

  it('lists window handles and the current handle', async () => {
    const driver = createMockDriver({
      getAllWindowHandles: vi.fn().mockResolvedValue(['w1', 'w2']),
      getWindowHandle: vi.fn().mockResolvedValue('w1')
    });
    getActiveDriver.mockReturnValue(driver);

    const response = await server.invokeTool('window_manage', { action: 'list' });

    expect(JSON.parse(response.content[0].text)).toEqual({ handles: ['w1', 'w2'], current: 'w1' });
    expect(isValidToolResponse(response)).toBe(true);
  });

  it('switches to a window by handle', async () => {
    const driver = createMockDriver();
    getActiveDriver.mockReturnValue(driver);

    const response = await server.invokeTool('window_manage', { action: 'switch', handle: 'w2' });

    expect(driver.switchTo().window).toHaveBeenCalledWith('w2');
    expect(isValidToolResponse(response)).toBe(true);
  });

  it('errors when switching without a handle', async () => {
    const driver = createMockDriver();
    getActiveDriver.mockReturnValue(driver);

    const response = await server.invokeTool('window_manage', { action: 'switch' });

    expect(response.isError).toBe(true);
  });

  it('opens a new tab and returns its handle', async () => {
    const driver = createMockDriver({ getWindowHandle: vi.fn().mockResolvedValue('w3') });
    getActiveDriver.mockReturnValue(driver);

    const response = await server.invokeTool('window_manage', { action: 'open', type: 'tab' });

    expect(driver.switchTo().newWindow).toHaveBeenCalledWith('tab');
    expect(response.content[0].text).toContain('w3');
  });

  it('closes the current window', async () => {
    const driver = createMockDriver();
    getActiveDriver.mockReturnValue(driver);

    await server.invokeTool('window_manage', { action: 'close' });

    expect(driver.close).toHaveBeenCalled();
  });

  it('maximizes the window', async () => {
    const driver = createMockDriver();
    getActiveDriver.mockReturnValue(driver);

    const response = await server.invokeTool('window_manage', { action: 'resize', maximize: true });

    expect(driver.manage().window().maximize).toHaveBeenCalled();
    expect(isValidToolResponse(response)).toBe(true);
  });

  it('resizes the window to given dimensions', async () => {
    const driver = createMockDriver();
    getActiveDriver.mockReturnValue(driver);

    const response = await server.invokeTool('window_manage', { action: 'resize', width: 1024, height: 768 });

    expect(driver.manage().window().setRect).toHaveBeenCalledWith({ width: 1024, height: 768 });
    expect(isValidToolResponse(response)).toBe(true);
  });

  it('errors when resize is missing width/height and not maximizing', async () => {
    const driver = createMockDriver();
    getActiveDriver.mockReturnValue(driver);

    const response = await server.invokeTool('window_manage', { action: 'resize' });

    expect(response.isError).toBe(true);
  });

  it('returns an error when there is no active session', async () => {
    getActiveDriver.mockImplementation(() => {
      throw new Error('No active browser session. Call browser_start first.');
    });
    const response = await server.invokeTool('window_manage', { action: 'list' });
    expect(response.isError).toBe(true);
  });
});

describe('frame_manage', () => {
  let server;

  beforeEach(() => {
    vi.clearAllMocks();
    server = createMockServer();
    configureWindowTools(server);
  });

  it('switches to a frame by locator', async () => {
    const element = createMockElement();
    const driver = createMockDriver({ findElements: vi.fn().mockResolvedValue([element]) });
    getActiveDriver.mockReturnValue(driver);

    const response = await server.invokeTool('frame_manage', {
      action: 'switch',
      locator: { using: 'id', value: 'frame1', index: 0 }
    });

    expect(driver.switchTo().frame).toHaveBeenCalledWith(element);
    expect(isValidToolResponse(response)).toBe(true);
  });

  it('switches to a frame by index', async () => {
    const driver = createMockDriver();
    getActiveDriver.mockReturnValue(driver);

    await server.invokeTool('frame_manage', { action: 'switch', index: 2 });

    expect(driver.switchTo().frame).toHaveBeenCalledWith(2);
  });

  it('errors when switching without a locator or index', async () => {
    const driver = createMockDriver();
    getActiveDriver.mockReturnValue(driver);

    const response = await server.invokeTool('frame_manage', { action: 'switch' });

    expect(response.isError).toBe(true);
  });

  it('resets to the default content', async () => {
    const driver = createMockDriver();
    getActiveDriver.mockReturnValue(driver);

    const response = await server.invokeTool('frame_manage', { action: 'default' });

    expect(driver.switchTo().defaultContent).toHaveBeenCalled();
    expect(isValidToolResponse(response)).toBe(true);
  });

  it('switches to the parent frame', async () => {
    const driver = createMockDriver();
    getActiveDriver.mockReturnValue(driver);

    await server.invokeTool('frame_manage', { action: 'parent' });

    expect(driver.switchTo().parentFrame).toHaveBeenCalled();
  });
});
