import { describe, it, expect, beforeEach, vi } from 'vitest';
import { createMockServer } from '@sc-node-mcp/shared-tests/helpers/mockServer';
import { createMockDriver, createMockElement } from './helpers/mockDriver.js';

vi.mock('../src/driver.js', () => ({ getActiveDriver: vi.fn() }));
vi.mock('node:fs/promises', () => ({ writeFile: vi.fn().mockResolvedValue(undefined) }));

const { getActiveDriver } = await import('../src/driver.js');
const { writeFile } = await import('node:fs/promises');
const { configureScreenshotTools } = await import('../src/tools/screenshot.js');

describe('screenshot tools', () => {
  let server;

  beforeEach(() => {
    vi.clearAllMocks();
    server = createMockServer();
    configureScreenshotTools(server);
  });

  it('captures the full viewport when no locator is given', async () => {
    const driver = createMockDriver({ takeScreenshot: vi.fn().mockResolvedValue('base64data') });
    getActiveDriver.mockReturnValue(driver);

    const response = await server.invokeTool('screenshot_capture', {});

    expect(driver.takeScreenshot).toHaveBeenCalled();
    expect(response.content[0]).toEqual({ type: 'image', data: 'base64data', mimeType: 'image/png' });
    expect(response.isError).toBeUndefined();
  });

  it('captures a single element when a locator is given', async () => {
    const element = createMockElement({ takeScreenshot: vi.fn().mockResolvedValue('elementdata') });
    const driver = createMockDriver({ findElements: vi.fn().mockResolvedValue([element]) });
    getActiveDriver.mockReturnValue(driver);

    const response = await server.invokeTool('screenshot_capture', { locator: { using: 'id', value: 'x', index: 0 } });

    expect(element.takeScreenshot).toHaveBeenCalled();
    expect(driver.takeScreenshot).not.toHaveBeenCalled();
    expect(response.content[0].data).toBe('elementdata');
  });

  it('saves the screenshot to disk when outputPath is given', async () => {
    const driver = createMockDriver({ takeScreenshot: vi.fn().mockResolvedValue('base64data') });
    getActiveDriver.mockReturnValue(driver);

    const response = await server.invokeTool('screenshot_capture', { outputPath: '/tmp/shot.png' });

    expect(writeFile).toHaveBeenCalledWith('/tmp/shot.png', Buffer.from('base64data', 'base64'));
    expect(response.content).toHaveLength(2);
    expect(response.content[1].text).toContain('/tmp/shot.png');
  });

  it('returns an error when there is no active session', async () => {
    getActiveDriver.mockImplementation(() => {
      throw new Error('No active browser session. Call browser_start first.');
    });
    const response = await server.invokeTool('screenshot_capture', {});
    expect(response.isError).toBe(true);
  });
});
