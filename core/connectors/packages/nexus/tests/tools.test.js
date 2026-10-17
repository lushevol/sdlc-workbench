import { describe, it, expect, vi } from 'vitest';
import { configureNexusTools } from '../src/tools.js';
import { createMockServer } from '@sc-node-mcp/shared-tests/helpers/mockServer';

describe('configureNexusTools', () => {
  it('registers nexus_scan_vulnerabilities on the server', () => {
    const mockServer = createMockServer();
    const nexusProvider = vi.fn();
    const adoProvider = vi.fn();

    configureNexusTools(mockServer, nexusProvider, adoProvider);

    const names = mockServer.getRegisteredTools().map(t => t.name);
    expect(names).toContain('nexus_scan_vulnerabilities');
  });

  it('logs a success message to stderr', () => {
    const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
    const mockServer = createMockServer();

    configureNexusTools(mockServer, vi.fn(), vi.fn());

    expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining('registered'));
  });
});
