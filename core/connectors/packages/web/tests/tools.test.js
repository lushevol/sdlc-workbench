import { describe, it, expect, vi } from 'vitest';
import { configureWebTools } from '../src/tools.js';
import { createMockServer } from '@sc-node-mcp/shared-tests/helpers/mockServer';

vi.mock('node:https', () => ({ default: { request: vi.fn() } }));
vi.mock('node:child_process', () => ({
  execSync: vi.fn(() => 'Google Chrome 125.0.0.0'),
  spawn: vi.fn(),
}));

describe('configureWebTools', () => {
  it('registers web_search and web_fetch on the server', () => {
    const mockServer = createMockServer();

    configureWebTools(mockServer);

    const names = mockServer.getRegisteredTools().map(t => t.name);
    expect(names).toContain('web_search');
    expect(names).toContain('web_fetch');
  });

  it('registers exactly 4 tools', () => {
    const mockServer = createMockServer();

    configureWebTools(mockServer);

    expect(mockServer.getRegisteredTools()).toHaveLength(4);
  });

  it('logs a success message to stderr', () => {
    const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
    const mockServer = createMockServer();

    configureWebTools(mockServer);

    expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining('registered'));
    consoleSpy.mockRestore();
  });
});
