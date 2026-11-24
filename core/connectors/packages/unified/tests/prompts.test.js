import { describe, it, expect, vi, beforeEach } from 'vitest';

// Mock sub-package prompt configurators
vi.mock('@sc-node-mcp/ado', () => ({ configureAdoPrompts: vi.fn() }));
vi.mock('@sc-node-mcp/confluence', () => ({ configureConfluencePrompts: vi.fn() }));
vi.mock('@sc-node-mcp/scwiki', () => ({ configureScwikiPrompts: vi.fn() }));
vi.mock('@sc-node-mcp/messaging', () => ({ configureMessagingPrompts: vi.fn() }));
vi.mock('@sc-node-mcp/nexus', () => ({ configureNexusPrompts: vi.fn() }));
vi.mock('@sc-node-mcp/sonar', () => ({ configureSonarPrompts: vi.fn() }));

// Ensure getActiveContext returns null so prompts use only explicit args
vi.mock('../src/context.js', () => ({
  getActiveContext: vi.fn(() => null),
  loadContext: vi.fn(() => null),
  saveContext: vi.fn()
}));

import { configureAdoPrompts } from '@sc-node-mcp/ado';
import { configureConfluencePrompts } from '@sc-node-mcp/confluence';
import { configureScwikiPrompts } from '@sc-node-mcp/scwiki';
import { configureMessagingPrompts } from '@sc-node-mcp/messaging';
import { configureNexusPrompts } from '@sc-node-mcp/nexus';
import { configureSonarPrompts } from '@sc-node-mcp/sonar';
import { configurePrompts, UNIFIED_PROMPTS } from '../src/prompts.js';

describe('Unified Prompts — thin aggregator', () => {
  let mockServer;

  beforeEach(() => {
    mockServer = { prompt: vi.fn() };
    vi.clearAllMocks();
  });

  describe('UNIFIED_PROMPTS constant', () => {
    it('should export UNIFIED_PROMPTS object', () => {
      expect(UNIFIED_PROMPTS).toBeDefined();
      expect(typeof UNIFIED_PROMPTS).toBe('object');
    });

    it('should contain exactly 4 unified-only prompts', () => {
      expect(Object.keys(UNIFIED_PROMPTS)).toHaveLength(4);
    });

    it('should include UPLOAD_ATTACHMENT_UI', () => {
      expect(UNIFIED_PROMPTS.UPLOAD_ATTACHMENT_UI).toBeDefined();
      expect(UNIFIED_PROMPTS.UPLOAD_ATTACHMENT_UI.name).toBe('upload-attachment-ui');
    });

    it('should include SET_CONTEXT', () => {
      expect(UNIFIED_PROMPTS.SET_CONTEXT).toBeDefined();
      expect(UNIFIED_PROMPTS.SET_CONTEXT.name).toBe('set-context');
    });

    it('should include SWITCH_CONTEXT', () => {
      expect(UNIFIED_PROMPTS.SWITCH_CONTEXT).toBeDefined();
      expect(UNIFIED_PROMPTS.SWITCH_CONTEXT.name).toBe('switch-context');
    });

    it('should include LIST_CONTEXTS', () => {
      expect(UNIFIED_PROMPTS.LIST_CONTEXTS).toBeDefined();
      expect(UNIFIED_PROMPTS.LIST_CONTEXTS.name).toBe('list-contexts');
    });

    it('should have correct structure for each unified prompt', () => {
      Object.values(UNIFIED_PROMPTS).forEach(prompt => {
        expect(prompt.name).toBeDefined();
        expect(prompt.description).toBeDefined();
        expect(Array.isArray(prompt.arguments)).toBe(true);
      });
    });

    it('LIST_CONTEXTS has no arguments', () => {
      expect(UNIFIED_PROMPTS.LIST_CONTEXTS.arguments).toHaveLength(0);
    });

    it('SET_CONTEXT has a required name argument and optional contextual fields', () => {
      const nameArg = UNIFIED_PROMPTS.SET_CONTEXT.arguments.find(a => a.name === 'name');
      const projectArg = UNIFIED_PROMPTS.SET_CONTEXT.arguments.find(a => a.name === 'project');
      const teamArg = UNIFIED_PROMPTS.SET_CONTEXT.arguments.find(a => a.name === 'team');
      expect(nameArg).toBeDefined();
      expect(nameArg.required).toBe(true);
      expect(projectArg.required).toBe(false);
      expect(teamArg.required).toBe(false);
    });

    it('SWITCH_CONTEXT has a required name argument', () => {
      const nameArg = UNIFIED_PROMPTS.SWITCH_CONTEXT.arguments.find(a => a.name === 'name');
      expect(nameArg).toBeDefined();
      expect(nameArg.required).toBe(true);
    });
  });

  describe('configurePrompts', () => {
    it('calls configureAdoPrompts with server and getActiveContext', () => {
      configurePrompts(mockServer);
      expect(configureAdoPrompts).toHaveBeenCalledOnce();
      expect(configureAdoPrompts).toHaveBeenCalledWith(mockServer, expect.objectContaining({ getContext: expect.any(Function) }));
    });

    it('calls configureConfluencePrompts with server and getActiveContext', () => {
      configurePrompts(mockServer);
      expect(configureConfluencePrompts).toHaveBeenCalledOnce();
      expect(configureConfluencePrompts).toHaveBeenCalledWith(mockServer, expect.objectContaining({ getContext: expect.any(Function) }));
    });

    it('calls configureScwikiPrompts with server', () => {
      configurePrompts(mockServer);
      expect(configureScwikiPrompts).toHaveBeenCalledOnce();
      expect(configureScwikiPrompts).toHaveBeenCalledWith(mockServer);
    });

    it('calls configureMessagingPrompts with server and getActiveContext', () => {
      configurePrompts(mockServer);
      expect(configureMessagingPrompts).toHaveBeenCalledOnce();
      expect(configureMessagingPrompts).toHaveBeenCalledWith(mockServer, expect.objectContaining({ getContext: expect.any(Function) }));
    });

    it('calls configureNexusPrompts with server and getActiveContext', () => {
      configurePrompts(mockServer);
      expect(configureNexusPrompts).toHaveBeenCalledOnce();
      expect(configureNexusPrompts).toHaveBeenCalledWith(mockServer, expect.objectContaining({ getContext: expect.any(Function) }));
    });

    it('calls configureSonarPrompts with server and getActiveContext', () => {
      configurePrompts(mockServer);
      expect(configureSonarPrompts).toHaveBeenCalledOnce();
      expect(configureSonarPrompts).toHaveBeenCalledWith(mockServer, expect.objectContaining({ getContext: expect.any(Function) }));
    });

    it('registers exactly 4 unified-only prompts on the server', () => {
      configurePrompts(mockServer);
      expect(mockServer.prompt).toHaveBeenCalledTimes(4);
    });

    it('registers upload-attachment-ui prompt', () => {
      configurePrompts(mockServer);
      expect(mockServer.prompt.mock.calls.map(c => c[0])).toContain('upload-attachment-ui');
    });

    it('registers set-context prompt', () => {
      configurePrompts(mockServer);
      expect(mockServer.prompt.mock.calls.map(c => c[0])).toContain('set-context');
    });

    it('registers switch-context prompt', () => {
      configurePrompts(mockServer);
      expect(mockServer.prompt.mock.calls.map(c => c[0])).toContain('switch-context');
    });

    it('registers list-contexts prompt', () => {
      configurePrompts(mockServer);
      expect(mockServer.prompt.mock.calls.map(c => c[0])).toContain('list-contexts');
    });

    it('registers a handler function for each prompt', () => {
      configurePrompts(mockServer);
      mockServer.prompt.mock.calls.forEach(call => {
        expect(typeof call.at(-1)).toBe('function');
      });
    });
  });

  describe('Unified prompt handlers', () => {
    const getHandler = (name) => {
      configurePrompts(mockServer);
      return mockServer.prompt.mock.calls.find(c => c[0] === name).at(-1);
    };

    it('should return proper message structure from each handler', async () => {
      configurePrompts(mockServer);
      for (const call of mockServer.prompt.mock.calls) {
        const result = await call.at(-1)({});
        expect(result).toHaveProperty('messages');
        expect(Array.isArray(result.messages)).toBe(true);
        expect(result.messages[0]).toHaveProperty('role', 'user');
        expect(result.messages[0].content).toHaveProperty('type', 'text');
        expect(result.messages[0].content).toHaveProperty('text');
      }
    });

    it('upload-attachment-ui — generates message with UI tool reference', async () => {
      const handler = getHandler('upload-attachment-ui');
      const result = await handler({ project: 'MyProject', wiId: '42' });
      expect(result.messages[0].content.text).toContain('wit_upload_attachment_ui');
      expect(result.messages[0].content.text).toContain('MyProject');
      expect(result.messages[0].content.text).toContain('42');
    });

    it('upload-attachment-ui — works without optional args', async () => {
      const handler = getHandler('upload-attachment-ui');
      const result = await handler({});
      expect(result.messages[0].content.text).toContain('wit_upload_attachment_ui');
    });

    it('set-context — generates message with ctx_set tool reference', async () => {
      const handler = getHandler('set-context');
      const result = await handler({ name: 'my-service', project: 'Proj', team: 'Team1' });
      expect(result.messages[0].content.text).toContain('ctx_set');
      expect(result.messages[0].content.text).toContain('my-service');
      expect(result.messages[0].content.text).toContain('Proj');
      expect(result.messages[0].content.text).toContain('Team1');
    });

    it('set-context — includes nexusAppId in repo entry when provided', async () => {
      const handler = getHandler('set-context');
      const result = await handler({ name: 'svc', defaultRepo: 'my-repo', nexusAppId: 'ITAM__DEV__my-repo' });
      expect(result.messages[0].content.text).toContain('my-repo');
      expect(result.messages[0].content.text).toContain('ITAM__DEV__my-repo');
    });

    it('switch-context — generates message with ctx_switch tool reference', async () => {
      const handler = getHandler('switch-context');
      const result = await handler({ name: 'prod-ctx' });
      expect(result.messages[0].content.text).toContain('ctx_switch');
      expect(result.messages[0].content.text).toContain('prod-ctx');
    });

    it('list-contexts — generates message with ctx_list tool reference', async () => {
      const handler = getHandler('list-contexts');
      const result = await handler({});
      expect(result.messages[0].content.text).toContain('ctx_list');
    });
  });
});
