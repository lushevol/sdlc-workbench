import { describe, it, expect, beforeEach, vi } from 'vitest';
import { createMockServer, isValidToolResponse } from '@sc-node-mcp/shared-tests/helpers/mockServer';
import { createMockDriver } from './helpers/mockDriver.js';

vi.mock('../src/driver.js', () => ({ getActiveDriver: vi.fn() }));

const { getActiveDriver } = await import('../src/driver.js');
const { configureScriptTools } = await import('../src/tools/script.js');

describe('script tools', () => {
  let server;

  beforeEach(() => {
    vi.clearAllMocks();
    server = createMockServer();
    configureScriptTools(server);
  });

  it('script_execute runs a synchronous script with args', async () => {
    const driver = createMockDriver({ executeScript: vi.fn().mockResolvedValue(42) });
    getActiveDriver.mockReturnValue(driver);

    const response = await server.invokeTool('script_execute', {
      script: 'return arguments[0] + arguments[1];',
      args: [1, 2],
      async: false
    });

    expect(driver.executeScript).toHaveBeenCalledWith('return arguments[0] + arguments[1];', 1, 2);
    expect(response.content[0].text).toBe('42');
    expect(isValidToolResponse(response)).toBe(true);
  });

  it('script_execute runs an async script when async is true', async () => {
    const driver = createMockDriver({ executeAsyncScript: vi.fn().mockResolvedValue('done') });
    getActiveDriver.mockReturnValue(driver);

    const response = await server.invokeTool('script_execute', { script: 'arguments[arguments.length-1]();', args: [], async: true });

    expect(driver.executeAsyncScript).toHaveBeenCalledWith('arguments[arguments.length-1]();');
    expect(response.content[0].text).toBe('"done"');
  });

  it('returns null as the result when the script returns undefined', async () => {
    const driver = createMockDriver({ executeScript: vi.fn().mockResolvedValue(undefined) });
    getActiveDriver.mockReturnValue(driver);

    const response = await server.invokeTool('script_execute', { script: 'void 0;', args: [], async: false });
    expect(response.content[0].text).toBe('null');
  });

  it('returns an error when script execution fails', async () => {
    const driver = createMockDriver({ executeScript: vi.fn().mockRejectedValue(new Error('script error')) });
    getActiveDriver.mockReturnValue(driver);

    const response = await server.invokeTool('script_execute', { script: 'throw new Error("x")', args: [], async: false });
    expect(response.isError).toBe(true);
  });
});
