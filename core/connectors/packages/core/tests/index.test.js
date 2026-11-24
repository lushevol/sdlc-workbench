import { describe, it, expect, vi, afterEach } from 'vitest';
import * as coreModule from '../src/index.js';

describe('Core Index', () => {
  afterEach(() => vi.unstubAllEnvs());

  it('should export getConfig', () => {
    expect(coreModule.getConfig).toBeDefined();
    expect(typeof coreModule.getConfig).toBe('function');
  });

  it('should export createMcpServer', () => {
    expect(coreModule.createMcpServer).toBeDefined();
    expect(typeof coreModule.createMcpServer).toBe('function');
  });

  it('should export startMcpServer', () => {
    expect(coreModule.startMcpServer).toBeDefined();
    expect(typeof coreModule.startMcpServer).toBe('function');
  });

  it('should export all required functions', () => {
    const exportedFunctions = ['getConfig', 'createMcpServer', 'startMcpServer'];
    
    exportedFunctions.forEach(funcName => {
      expect(coreModule[funcName]).toBeDefined();
      expect(typeof coreModule[funcName]).toBe('function');
    });
  });

  it.each([undefined, '1'])('preserves the caller TLS setting %s during import', async (value) => {
    vi.stubEnv('NODE_TLS_REJECT_UNAUTHORIZED', value);
    vi.resetModules();
    await import('../src/index.js');
    expect(process.env.NODE_TLS_REJECT_UNAUTHORIZED).toBe(value);
  });
});
