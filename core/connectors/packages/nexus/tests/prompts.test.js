import { describe, it, expect, vi, beforeEach } from 'vitest';
import { configureNexusPrompts, NEXUS_PROMPTS } from '../src/prompts.js';

describe('Nexus Prompts', () => {
  let mockServer;

  beforeEach(() => {
    mockServer = { prompt: vi.fn() };
  });

  describe('NEXUS_PROMPTS constant', () => {
    it('should export NEXUS_PROMPTS object', () => {
      expect(NEXUS_PROMPTS).toBeDefined();
      expect(typeof NEXUS_PROMPTS).toBe('object');
    });

    it('should contain 1 prompt', () => {
      expect(Object.keys(NEXUS_PROMPTS)).toHaveLength(1);
    });

    it('NEXUS_SCAN should have the correct name', () => {
      expect(NEXUS_PROMPTS.NEXUS_SCAN.name).toBe('nexus-vulnerability-scan');
    });

    it('NEXUS_SCAN should have a description', () => {
      expect(NEXUS_PROMPTS.NEXUS_SCAN.description).toBeDefined();
      expect(typeof NEXUS_PROMPTS.NEXUS_SCAN.description).toBe('string');
    });

    it('NEXUS_SCAN should have applicationId and pattern arguments', () => {
      const appIdArg = NEXUS_PROMPTS.NEXUS_SCAN.arguments.find(a => a.name === 'applicationId');
      const patternArg = NEXUS_PROMPTS.NEXUS_SCAN.arguments.find(a => a.name === 'pattern');
      expect(appIdArg).toBeDefined();
      expect(patternArg).toBeDefined();
    });

    it('NEXUS_SCAN applicationId should be declared required', () => {
      const appIdArg = NEXUS_PROMPTS.NEXUS_SCAN.arguments.find(a => a.name === 'applicationId');
      expect(appIdArg.required).toBe(true);
    });

    it('NEXUS_SCAN pattern should be optional', () => {
      const patternArg = NEXUS_PROMPTS.NEXUS_SCAN.arguments.find(a => a.name === 'pattern');
      expect(patternArg.required).toBe(false);
    });

    it('NEXUS_SCAN should have an arguments array', () => {
      expect(Array.isArray(NEXUS_PROMPTS.NEXUS_SCAN.arguments)).toBe(true);
    });
  });

  describe('configureNexusPrompts()', () => {
    it('should register 1 prompt on the server', () => {
      configureNexusPrompts(mockServer);
      expect(mockServer.prompt).toHaveBeenCalledTimes(1);
    });

    it('should register the nexus-vulnerability-scan prompt', () => {
      configureNexusPrompts(mockServer);
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'nexus-vulnerability-scan');
      expect(call).toBeDefined();
    });

    it('should accept optional getContext parameter', () => {
      const getContext = vi.fn(() => null);
      expect(() => configureNexusPrompts(mockServer, { getContext })).not.toThrow();
    });

    it('should work without getContext (default null)', () => {
      expect(() => configureNexusPrompts(mockServer)).not.toThrow();
    });

    it('should use nexusAppId from context default repository when applicationId arg is absent', async () => {
      const ctx = { repositories: [{ isDefault: true, nexusAppId: 'ITAM__PROD__my-repo' }] };
      configureNexusPrompts(mockServer, { getContext: () => ctx });
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'nexus-vulnerability-scan');
      const handler = call.at(-1);
      const result = await handler({});
      expect(result.messages[0].content.text).toContain('ITAM__PROD__my-repo');
    });

    it('should use defaultBranch from ado context when branch arg is absent', async () => {
      const ctx = { ado: { defaultBranch: 'release/2.0' } };
      configureNexusPrompts(mockServer, { getContext: () => ctx });
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'nexus-vulnerability-scan');
      const handler = call.at(-1);
      const result = await handler({ applicationId: 'ITAM__DEV__app' });
      expect(result.messages[0].content.text).toContain('release/2.0');
    });
  });

  describe('generateNexusPromptMessage (via registered handlers)', () => {
    beforeEach(() => {
      configureNexusPrompts(mockServer);
    });

    it('should return valid MCP prompt response structure', async () => {
      const call = mockServer.prompt.mock.calls[0];
      const handler = call.at(-1);
      const result = await handler({ applicationId: 'ITAM__DEV__repo' });
      expect(result).toHaveProperty('messages');
      expect(Array.isArray(result.messages)).toBe(true);
      expect(result.messages[0]).toHaveProperty('role', 'user');
      expect(result.messages[0].content).toHaveProperty('type', 'text');
      expect(result.messages[0].content).toHaveProperty('text');
    });

    it('should generate nexus-vulnerability-scan message containing the applicationId', async () => {
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'nexus-vulnerability-scan');
      const handler = call.at(-1);
      const result = await handler({ applicationId: 'ITAM__PROD__my-service' });
      expect(result.messages[0].content.text).toContain('ITAM__PROD__my-service');
    });

    it('should default to pipeline-aligned scan mode when no pattern is given', async () => {
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'nexus-vulnerability-scan');
      const handler = call.at(-1);
      const result = await handler({ applicationId: 'ITAM__DEV__app' });
      expect(result.messages[0].content.text).toContain('Pipeline-aligned');
    });

    it('should use deep scan mode when pattern is deep-scan', async () => {
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'nexus-vulnerability-scan');
      const handler = call.at(-1);
      const result = await handler({ applicationId: 'ITAM__DEV__app', pattern: 'deep-scan' });
      expect(result.messages[0].content.text).toContain('Deep Scan');
    });

    it('should include fix step instruction when pattern is scan-fix', async () => {
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'nexus-vulnerability-scan');
      const handler = call.at(-1);
      const result = await handler({ applicationId: 'ITAM__DEV__app', pattern: 'scan-fix' });
      expect(result.messages[0].content.text).toContain('nexus_fix_vulnerabilities');
    });

    it('should include deep scan AND fix when pattern is deep-scan-fix', async () => {
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'nexus-vulnerability-scan');
      const handler = call.at(-1);
      const result = await handler({ applicationId: 'ITAM__DEV__app', pattern: 'deep-scan-fix' });
      const text = result.messages[0].content.text;
      expect(text).toContain('Deep Scan');
      expect(text).toContain('nexus_fix_vulnerabilities');
    });

    it('should NOT include fix step for plain scan pattern', async () => {
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'nexus-vulnerability-scan');
      const handler = call.at(-1);
      const result = await handler({ applicationId: 'ITAM__DEV__app', pattern: 'scan' });
      expect(result.messages[0].content.text).not.toContain('nexus_fix_vulnerabilities');
    });

    it('should handle undefined args gracefully', async () => {
      const call = mockServer.prompt.mock.calls[0];
      const handler = call.at(-1);
      const result = await handler(undefined);
      expect(result.messages[0].content.text).toBeDefined();
      expect(typeof result.messages[0].content.text).toBe('string');
    });
  });
});
