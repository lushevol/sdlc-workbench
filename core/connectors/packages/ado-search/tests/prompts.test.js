import { describe, it, expect, vi, beforeEach } from 'vitest';
import { configureSearchPrompts } from '../src/prompts.js';

describe('Search Prompts', () => {
  let mockServer;

  beforeEach(() => {
    mockServer = { prompt: vi.fn() };
  });

  describe('configureSearchPrompts()', () => {
    it('should register 2 prompts on the server', () => {
      configureSearchPrompts(mockServer);
      expect(mockServer.prompt).toHaveBeenCalledTimes(2);
    });

    it('should register search-code prompt', () => {
      configureSearchPrompts(mockServer);
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'search-code');
      expect(call).toBeDefined();
    });

    it('should register search-work-item prompt', () => {
      configureSearchPrompts(mockServer);
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'search-work-item');
      expect(call).toBeDefined();
    });

    it('should work without options argument', () => {
      expect(() => configureSearchPrompts(mockServer)).not.toThrow();
    });

    it('should invoke default getContext when no options provided', async () => {
      configureSearchPrompts(mockServer);
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'search-code');
      const result = await call.at(-1)({ searchText: 'test query' });
      expect(result.messages[0].content.text).toBeDefined();
    });

    it('should accept optional getContext parameter', () => {
      const getContext = vi.fn(() => null);
      expect(() => configureSearchPrompts(mockServer, { getContext })).not.toThrow();
    });
  });

  describe('search-code prompt message', () => {
    const getHandler = (getContext = () => null) => {
      configureSearchPrompts(mockServer, { getContext });
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'search-code');
      return call.at(-1);
    };

    it('should return a user message for a basic search', async () => {
      const handler = getHandler();
      const result = await handler({ searchText: 'configureTools' });
      expect(result.messages).toHaveLength(1);
      expect(result.messages[0].role).toBe('user');
      expect(result.messages[0].content.type).toBe('text');
      expect(result.messages[0].content.text).toContain('configureTools');
    });

    it('should include project filter in message when provided', async () => {
      const handler = getHandler();
      const result = await handler({ searchText: 'fn', project: 'TBQPR' });
      expect(result.messages[0].content.text).toContain('TBQPR');
    });

    it('should include repository filter in message when provided', async () => {
      const handler = getHandler();
      const result = await handler({ searchText: 'fn', repository: 'my-repo' });
      expect(result.messages[0].content.text).toContain('my-repo');
    });

    it('should include branch filter in message when provided', async () => {
      const handler = getHandler();
      const result = await handler({ searchText: 'fn', branch: 'main' });
      expect(result.messages[0].content.text).toContain('main');
    });

    it('should include all filters when all are provided', async () => {
      const handler = getHandler();
      const result = await handler({
        searchText: 'myFunction',
        project: 'TBQPR',
        repository: 'my-repo',
        branch: 'main'
      });
      const text = result.messages[0].content.text;
      expect(text).toContain('myFunction');
      expect(text).toContain('TBQPR');
      expect(text).toContain('my-repo');
      expect(text).toContain('main');
    });

    it('should use project from context when not provided in args', async () => {
      const ctx = { ado: { project: 'CtxProject' } };
      const handler = getHandler(() => ctx);
      const result = await handler({ searchText: 'test' });
      expect(result.messages[0].content.text).toContain('CtxProject');
    });

    it('should prefer explicit project arg over context value', async () => {
      const ctx = { ado: { project: 'CtxProject' } };
      const handler = getHandler(() => ctx);
      const result = await handler({ searchText: 'test', project: 'ExplicitProject' });
      expect(result.messages[0].content.text).toContain('ExplicitProject');
    });

    it('should handle null args gracefully', async () => {
      const handler = getHandler();
      const result = await handler(null);
      expect(result.messages[0].content.text).toBeDefined();
    });
  });

  describe('search-work-item prompt message', () => {
    const getHandler = (getContext = () => null) => {
      configureSearchPrompts(mockServer, { getContext });
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'search-work-item');
      return call.at(-1);
    };

    it('should return a user message for a basic work item search', async () => {
      const handler = getHandler();
      const result = await handler({ searchText: 'payment gateway' });
      expect(result.messages).toHaveLength(1);
      expect(result.messages[0].role).toBe('user');
      expect(result.messages[0].content.text).toContain('payment gateway');
    });

    it('should include project filter in message when provided', async () => {
      const handler = getHandler();
      const result = await handler({ searchText: 'bug', project: 'TBQPR' });
      expect(result.messages[0].content.text).toContain('TBQPR');
    });

    it('should include workItemType filter in message when provided', async () => {
      const handler = getHandler();
      const result = await handler({ searchText: 'login', workItemType: 'Bug' });
      expect(result.messages[0].content.text).toContain('Bug');
    });

    it('should include state filter in message when provided', async () => {
      const handler = getHandler();
      const result = await handler({ searchText: 'login', state: 'Active' });
      expect(result.messages[0].content.text).toContain('Active');
    });

    it('should include all filters when all are provided', async () => {
      const handler = getHandler();
      const result = await handler({
        searchText: 'login bug',
        project: 'TBQPR',
        workItemType: 'Bug',
        state: 'Active'
      });
      const text = result.messages[0].content.text;
      expect(text).toContain('login bug');
      expect(text).toContain('TBQPR');
      expect(text).toContain('Bug');
      expect(text).toContain('Active');
    });

    it('should use project from context when not provided in args', async () => {
      const ctx = { ado: { project: 'CtxProject' } };
      const handler = getHandler(() => ctx);
      const result = await handler({ searchText: 'payment' });
      expect(result.messages[0].content.text).toContain('CtxProject');
    });

    it('should prefer explicit project arg over context value', async () => {
      const ctx = { ado: { project: 'CtxProject' } };
      const handler = getHandler(() => ctx);
      const result = await handler({ searchText: 'test', project: 'ExplicitProject' });
      expect(result.messages[0].content.text).toContain('ExplicitProject');
    });

    it('should handle null args gracefully', async () => {
      const handler = getHandler();
      const result = await handler(null);
      expect(result.messages[0].content.text).toBeDefined();
    });
  });
});
