import { describe, it, expect, vi, beforeEach } from 'vitest';
import { configureSonarPrompts, SONAR_PROMPTS } from '../src/prompts.js';

describe('Sonar Prompts', () => {
  let mockServer;

  beforeEach(() => {
    mockServer = { prompt: vi.fn() };
  });

  describe('SONAR_PROMPTS constant', () => {
    it('should export SONAR_PROMPTS object', () => {
      expect(SONAR_PROMPTS).toBeDefined();
      expect(typeof SONAR_PROMPTS).toBe('object');
    });

    it('should contain 8 prompts', () => {
      expect(Object.keys(SONAR_PROMPTS)).toHaveLength(8);
    });

    it('each prompt should have name, description, and arguments array', () => {
      Object.values(SONAR_PROMPTS).forEach(prompt => {
        expect(prompt.name).toBeDefined();
        expect(typeof prompt.name).toBe('string');
        expect(prompt.description).toBeDefined();
        expect(Array.isArray(prompt.arguments)).toBe(true);
      });
    });

    it('SONAR_PROJECT_HEALTH should have a required projectKey argument', () => {
      const arg = SONAR_PROMPTS.SONAR_PROJECT_HEALTH.arguments.find(a => a.name === 'projectKey');
      expect(arg).toBeDefined();
      expect(arg.required).toBe(true);
    });

    it('SONAR_PROJECT_HEALTH should have an optional branch argument', () => {
      const arg = SONAR_PROMPTS.SONAR_PROJECT_HEALTH.arguments.find(a => a.name === 'branch');
      expect(arg).toBeDefined();
      expect(arg.required).toBe(false);
    });

    it('SONAR_SEARCH_PROJECTS should have only an optional query argument', () => {
      const queryArg = SONAR_PROMPTS.SONAR_SEARCH_PROJECTS.arguments.find(a => a.name === 'query');
      expect(queryArg).toBeDefined();
      expect(queryArg.required).toBe(false);
      expect(SONAR_PROMPTS.SONAR_SEARCH_PROJECTS.arguments).toHaveLength(1);
    });

    it('SONAR_GET_QUALITY_GATE should have optional branch and pullRequest arguments', () => {
      const branchArg = SONAR_PROMPTS.SONAR_GET_QUALITY_GATE.arguments.find(a => a.name === 'branch');
      const prArg = SONAR_PROMPTS.SONAR_GET_QUALITY_GATE.arguments.find(a => a.name === 'pullRequest');
      expect(branchArg.required).toBe(false);
      expect(prArg.required).toBe(false);
    });

    it('prompt names should all be unique', () => {
      const names = Object.values(SONAR_PROMPTS).map(p => p.name);
      const uniqueNames = new Set(names);
      expect(uniqueNames.size).toBe(names.length);
    });
  });

  describe('configureSonarPrompts()', () => {
    it('should register all 8 prompts on the server', () => {
      configureSonarPrompts(mockServer);
      expect(mockServer.prompt).toHaveBeenCalledTimes(8);
    });

    it('should accept optional getContext parameter', () => {
      const getContext = vi.fn(() => null);
      expect(() => configureSonarPrompts(mockServer, { getContext })).not.toThrow();
    });

    it('should work without getContext (default null)', () => {
      expect(() => configureSonarPrompts(mockServer)).not.toThrow();
    });

    it('should use defaultBranch from ADO context in sonar-project-health when branch arg is absent', async () => {
      const ctx = { ado: { defaultBranch: 'main' } };
      configureSonarPrompts(mockServer, { getContext: () => ctx });
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'sonar-project-health');
      const handler = call.at(-1);
      const result = await handler({ projectKey: 'my-project' });
      expect(result.messages[0].content.text).toContain('"main"');
    });

    it('should prefer explicit branch over context defaultBranch', async () => {
      const ctx = { ado: { defaultBranch: 'main' } };
      configureSonarPrompts(mockServer, { getContext: () => ctx });
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'sonar-project-health');
      const handler = call.at(-1);
      const result = await handler({ projectKey: 'my-project', branch: 'feature/x' });
      expect(result.messages[0].content.text).toContain('feature/x');
      expect(result.messages[0].content.text).not.toContain('"main"');
    });
  });

  describe('generateSonarPromptMessage (via registered handlers)', () => {
    beforeEach(() => {
      configureSonarPrompts(mockServer);
    });

    it('should return valid MCP prompt response structure', async () => {
      const call = mockServer.prompt.mock.calls[0];
      const handler = call.at(-1);
      const result = await handler({ projectKey: 'my-project' });
      expect(result).toHaveProperty('messages');
      expect(Array.isArray(result.messages)).toBe(true);
      expect(result.messages[0]).toHaveProperty('role', 'user');
      expect(result.messages[0].content).toHaveProperty('type', 'text');
      expect(result.messages[0].content).toHaveProperty('text');
    });

    it('should generate sonar-project-health message with projectKey', async () => {
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'sonar-project-health');
      const handler = call.at(-1);
      const result = await handler({ projectKey: 'my-service' });
      expect(result.messages[0].content.text).toContain('my-service');
      expect(result.messages[0].content.text).toContain('quality');
    });

    it('should include branch clause in sonar-project-health when branch is provided', async () => {
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'sonar-project-health');
      const handler = call.at(-1);
      const result = await handler({ projectKey: 'my-service', branch: 'develop' });
      expect(result.messages[0].content.text).toContain('develop');
    });

    it('should generate sonar-security-review message with projectKey', async () => {
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'sonar-security-review');
      const handler = call.at(-1);
      const result = await handler({ projectKey: 'secure-app' });
      expect(result.messages[0].content.text).toContain('secure-app');
      expect(result.messages[0].content.text).toContain('security');
    });

    it('should generate sonar-search-projects without query (list all)', async () => {
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'sonar-search-projects');
      const handler = call.at(-1);
      const result = await handler({});
      expect(result.messages[0].content.text).toContain('list all projects');
    });

    it('should generate sonar-search-projects with query filter when provided', async () => {
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'sonar-search-projects');
      const handler = call.at(-1);
      const result = await handler({ query: 'payment' });
      expect(result.messages[0].content.text).toContain('payment');
    });

    it('should generate sonar-get-branches with projectKey', async () => {
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'sonar-get-branches');
      const handler = call.at(-1);
      const result = await handler({ projectKey: 'repo-x' });
      expect(result.messages[0].content.text).toContain('repo-x');
    });

    it('should generate sonar-get-quality-gate with pullRequest clause when pullRequest is provided', async () => {
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'sonar-get-quality-gate');
      const handler = call.at(-1);
      const result = await handler({ projectKey: 'proj', pullRequest: '42' });
      expect(result.messages[0].content.text).toContain('"42"');
    });

    it('should generate sonar-get-quality-gate with branch clause when branch is provided', async () => {
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'sonar-get-quality-gate');
      const handler = call.at(-1);
      const result = await handler({ projectKey: 'proj', branch: 'release/1.0' });
      expect(result.messages[0].content.text).toContain('release/1.0');
    });

    it('should generate sonar-get-issues with projectKey and optional type/severity filters', async () => {
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'sonar-get-issues');
      const handler = call.at(-1);
      const result = await handler({ projectKey: 'my-proj', types: 'BUG', severities: 'CRITICAL' });
      expect(result.messages[0].content.text).toContain('my-proj');
      expect(result.messages[0].content.text).toContain('BUG');
      expect(result.messages[0].content.text).toContain('CRITICAL');
    });

    it('should default to BUG,VULNERABILITY,CODE_SMELL in sonar-get-issues when types is absent', async () => {
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'sonar-get-issues');
      const handler = call.at(-1);
      const result = await handler({ projectKey: 'proj' });
      expect(result.messages[0].content.text).toContain('BUG,VULNERABILITY,CODE_SMELL');
    });

    it('should generate sonar-get-hotspots with default status TO_REVIEW when status is absent', async () => {
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'sonar-get-hotspots');
      const handler = call.at(-1);
      const result = await handler({ projectKey: 'proj-a' });
      expect(result.messages[0].content.text).toContain('TO_REVIEW');
    });

    it('should generate sonar-get-measures with default metric keys when metricKeys is absent', async () => {
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'sonar-get-measures');
      const handler = call.at(-1);
      const result = await handler({ component: 'my-component' });
      expect(result.messages[0].content.text).toContain('bugs');
      expect(result.messages[0].content.text).toContain('coverage');
    });

    it('should use defaultBranch from context in sonar-get-issues', async () => {
      const ctx = { ado: { defaultBranch: 'sprint-5' } };
      const serverWithCtx = { prompt: vi.fn() };
      configureSonarPrompts(serverWithCtx, { getContext: () => ctx });
      const call = serverWithCtx.prompt.mock.calls.find(c => c[0] === 'sonar-get-issues');
      const handler = call.at(-1);
      const result = await handler({ projectKey: 'acme' });
      expect(result.messages[0].content.text).toContain('sprint-5');
    });

    it('should handle undefined args gracefully', async () => {
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'sonar-project-health');
      const handler = call.at(-1);
      const result = await handler(undefined);
      expect(result.messages[0].content.text).toBeDefined();
      expect(typeof result.messages[0].content.text).toBe('string');
    });
  });
});
