import { describe, it, expect, beforeEach, vi } from 'vitest';
import { createMockServer, isValidToolResponse } from '@sc-node-mcp/shared-tests/helpers/mockServer';
import { createMockDriver } from './helpers/mockDriver.js';

vi.mock('../src/driver.js', () => ({ getActiveDriver: vi.fn() }));

const { getActiveDriver } = await import('../src/driver.js');
const { configureAlertTools } = await import('../src/tools/alerts.js');

describe('alert tools', () => {
  let server;

  beforeEach(() => {
    vi.clearAllMocks();
    server = createMockServer();
    configureAlertTools(server);
  });

  it('accepts the alert', async () => {
    const driver = createMockDriver({ wait: vi.fn().mockResolvedValue(undefined) });
    getActiveDriver.mockReturnValue(driver);
    const alert = await driver.switchTo().alert();

    const response = await server.invokeTool('alert_handle', { action: 'accept', timeoutMs: 5000 });

    expect(alert.accept).toHaveBeenCalled();
    expect(isValidToolResponse(response)).toBe(true);
  });

  it('dismisses the alert', async () => {
    const driver = createMockDriver({ wait: vi.fn().mockResolvedValue(undefined) });
    getActiveDriver.mockReturnValue(driver);
    const alert = await driver.switchTo().alert();

    await server.invokeTool('alert_handle', { action: 'dismiss' });

    expect(alert.dismiss).toHaveBeenCalled();
  });

  it('reads the alert text', async () => {
    const driver = createMockDriver({ wait: vi.fn().mockResolvedValue(undefined) });
    getActiveDriver.mockReturnValue(driver);
    const alert = await driver.switchTo().alert();
    alert.getText.mockResolvedValue('Are you sure?');

    const response = await server.invokeTool('alert_handle', { action: 'get_text' });

    expect(response.content[0].text).toBe('Are you sure?');
  });

  it('types text into a prompt', async () => {
    const driver = createMockDriver({ wait: vi.fn().mockResolvedValue(undefined) });
    getActiveDriver.mockReturnValue(driver);
    const alert = await driver.switchTo().alert();

    const response = await server.invokeTool('alert_handle', { action: 'send_text', text: 'hello' });

    expect(alert.sendKeys).toHaveBeenCalledWith('hello');
    expect(isValidToolResponse(response)).toBe(true);
  });

  it('errors when send_text is missing text', async () => {
    const driver = createMockDriver({ wait: vi.fn().mockResolvedValue(undefined) });
    getActiveDriver.mockReturnValue(driver);

    const response = await server.invokeTool('alert_handle', { action: 'send_text' });

    expect(response.isError).toBe(true);
  });

  it('returns an error when no alert is present', async () => {
    const driver = createMockDriver({ wait: vi.fn().mockRejectedValue(new Error('No alert present')) });
    getActiveDriver.mockReturnValue(driver);

    const response = await server.invokeTool('alert_handle', { action: 'accept' });

    expect(response.isError).toBe(true);
  });

  it('returns an error for an unsupported action', async () => {
    const driver = createMockDriver({ wait: vi.fn().mockResolvedValue(undefined) });
    getActiveDriver.mockReturnValue(driver);

    const response = await server.invokeTool('alert_handle', { action: 'bogus' });

    expect(response.isError).toBe(true);
    expect(response.content[0].text).toContain('Unsupported action');
  });
});
