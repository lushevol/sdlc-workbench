import { describe, it, expect } from 'vitest';
import * as coreModule from '../src/index.js';

describe('Core Index', () => {
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

  it('should set NODE_TLS_REJECT_UNAUTHORIZED to 0', () => {
    // This is set when the module is imported
    expect(process.env.NODE_TLS_REJECT_UNAUTHORIZED).toBe('0');
  });
});
