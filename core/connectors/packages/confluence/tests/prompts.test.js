import { describe, it, expect, vi, beforeEach } from 'vitest';
import { configureConfluencePrompts, CONFLUENCE_PROMPTS } from '../src/prompts.js';

describe('Confluence Prompts', () => {
  let mockServer;

  beforeEach(() => {
    mockServer = { prompt: vi.fn() };
  });

  describe('CONFLUENCE_PROMPTS constant', () => {
    it('should export CONFLUENCE_PROMPTS object', () => {
      expect(CONFLUENCE_PROMPTS).toBeDefined();
      expect(typeof CONFLUENCE_PROMPTS).toBe('object');
    });

    it('should contain 15 prompts', () => {
      expect(Object.keys(CONFLUENCE_PROMPTS)).toHaveLength(15);
    });

    it('each prompt should have name, description, and arguments array', () => {
      Object.values(CONFLUENCE_PROMPTS).forEach(prompt => {
        expect(prompt.name).toBeDefined();
        expect(typeof prompt.name).toBe('string');
        expect(prompt.description).toBeDefined();
        expect(Array.isArray(prompt.arguments)).toBe(true);
      });
    });

    it('MY_PAGES should have an optional spaceKey argument', () => {
      const arg = CONFLUENCE_PROMPTS.MY_PAGES.arguments.find(a => a.name === 'spaceKey');
      expect(arg).toBeDefined();
      expect(arg.required).toBe(false);
    });

    it('SEARCH_CONFLUENCE should have a required cql argument', () => {
      const arg = CONFLUENCE_PROMPTS.SEARCH_CONFLUENCE.arguments.find(a => a.name === 'cql');
      expect(arg).toBeDefined();
      expect(arg.required).toBe(true);
    });

    it('UPDATE_CONFLUENCE_PAGE should have required pageId and body arguments', () => {
      const pageIdArg = CONFLUENCE_PROMPTS.UPDATE_CONFLUENCE_PAGE.arguments.find(a => a.name === 'pageId');
      const bodyArg = CONFLUENCE_PROMPTS.UPDATE_CONFLUENCE_PAGE.arguments.find(a => a.name === 'body');
      expect(pageIdArg.required).toBe(true);
      expect(bodyArg.required).toBe(true);
    });

    it('CREATE_CONFLUENCE_PAGE should have required parentPageUrl and title arguments', () => {
      const urlArg = CONFLUENCE_PROMPTS.CREATE_CONFLUENCE_PAGE.arguments.find(a => a.name === 'parentPageUrl');
      const titleArg = CONFLUENCE_PROMPTS.CREATE_CONFLUENCE_PAGE.arguments.find(a => a.name === 'title');
      expect(urlArg.required).toBe(true);
      expect(titleArg.required).toBe(true);
    });

    it('prompt names should all be unique', () => {
      const names = Object.values(CONFLUENCE_PROMPTS).map(p => p.name);
      const uniqueNames = new Set(names);
      expect(uniqueNames.size).toBe(names.length);
    });
  });

  describe('configureConfluencePrompts()', () => {
    it('should register all 15 prompts on the server', () => {
      configureConfluencePrompts(mockServer);
      expect(mockServer.prompt).toHaveBeenCalledTimes(15);
    });

    it('should accept optional getContext parameter', () => {
      const getContext = vi.fn(() => null);
      expect(() => configureConfluencePrompts(mockServer, { getContext })).not.toThrow();
    });

    it('should work without getContext (default null)', () => {
      expect(() => configureConfluencePrompts(mockServer)).not.toThrow();
    });

    it('should use defaultSpaceKey from context when spaceKey arg is absent', async () => {
      const ctx = { confluence: { defaultSpaceKey: 'MYSPACE' } };
      configureConfluencePrompts(mockServer, { getContext: () => ctx });
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'my-confluence-pages');
      const handler = call.at(-1);
      const result = await handler({});
      expect(result.messages[0].content.text).toContain('MYSPACE');
    });

    it('should prefer explicit spaceKey arg over context defaultSpaceKey', async () => {
      const ctx = { confluence: { defaultSpaceKey: 'ContextSpace' } };
      configureConfluencePrompts(mockServer, { getContext: () => ctx });
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'my-confluence-pages');
      const handler = call.at(-1);
      const result = await handler({ spaceKey: 'ExplicitSpace' });
      expect(result.messages[0].content.text).toContain('ExplicitSpace');
      expect(result.messages[0].content.text).not.toContain('ContextSpace');
    });

    it('should default to an empty args object when a handler is invoked with no arguments', async () => {
      configureConfluencePrompts(mockServer);
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'my-confluence-pages');
      const handler = call.at(-1);
      const result = await handler();
      expect(result.messages[0].content.text).toContain('across all spaces');
    });
  });

  describe('generateConfluencePromptMessage (via registered handlers)', () => {
    beforeEach(() => {
      configureConfluencePrompts(mockServer);
    });

    it('should return valid MCP prompt response structure', async () => {
      const call = mockServer.prompt.mock.calls[0];
      const handler = call.at(-1);
      const result = await handler({});
      expect(result).toHaveProperty('messages');
      expect(Array.isArray(result.messages)).toBe(true);
      expect(result.messages[0]).toHaveProperty('role', 'user');
      expect(result.messages[0].content).toHaveProperty('type', 'text');
      expect(result.messages[0].content).toHaveProperty('text');
    });

    it('should generate my-confluence-pages without spaceKey (across all spaces)', async () => {
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'my-confluence-pages');
      const handler = call.at(-1);
      const result = await handler({});
      expect(result.messages[0].content.text).toContain('across all spaces');
    });

    it('should generate my-confluence-pages with spaceKey clause when provided', async () => {
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'my-confluence-pages');
      const handler = call.at(-1);
      const result = await handler({ spaceKey: 'DEVTEAM' });
      expect(result.messages[0].content.text).toContain('DEVTEAM');
    });

    it('should generate search-confluence with cql query', async () => {
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'search-confluence');
      const handler = call.at(-1);
      const result = await handler({ cql: 'space = DEV AND type = page' });
      expect(result.messages[0].content.text).toContain('space = DEV AND type = page');
    });

    it('should include limit in search-confluence when provided', async () => {
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'search-confluence');
      const handler = call.at(-1);
      const result = await handler({ cql: 'space = DEV', limit: '20' });
      expect(result.messages[0].content.text).toContain('20');
    });

    it('should generate update-confluence-page with pageId and body', async () => {
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'update-confluence-page');
      const handler = call.at(-1);
      const result = await handler({ pageId: '12345', body: '<p>New content</p>' });
      expect(result.messages[0].content.text).toContain('12345');
      expect(result.messages[0].content.text).toContain('New content');
    });

    it('should include new title in update-confluence-page when provided', async () => {
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'update-confluence-page');
      const handler = call.at(-1);
      const result = await handler({ pageId: '99', body: '<p>x</p>', title: 'Renamed Page' });
      expect(result.messages[0].content.text).toContain('Renamed Page');
    });

    it('should generate get-confluence-page-id with pageUrl', async () => {
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'get-confluence-page-id');
      const handler = call.at(-1);
      const result = await handler({ pageUrl: 'https://confluence.global.standardchartered.com/display/TEAM/Page' });
      expect(result.messages[0].content.text).toContain('https://confluence.global.standardchartered.com');
    });

    it('should generate read-confluence-page with pageUrl', async () => {
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'read-confluence-page');
      const handler = call.at(-1);
      const result = await handler({ pageUrl: 'https://confluence.example.com/pages/99' });
      expect(result.messages[0].content.text).toContain('https://confluence.example.com/pages/99');
    });

    it('should generate create-confluence-page with parentPageUrl and title', async () => {
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'create-confluence-page');
      const handler = call.at(-1);
      const result = await handler({ parentPageUrl: 'https://confluence.example.com/parent', title: 'New Page' });
      expect(result.messages[0].content.text).toContain('https://confluence.example.com/parent');
      expect(result.messages[0].content.text).toContain('New Page');
    });

    it('should include body content in create-confluence-page when provided', async () => {
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'create-confluence-page');
      const handler = call.at(-1);
      const result = await handler({ parentPageUrl: 'https://parent.url', title: 'My Page', body: '<p>Hello</p>' });
      expect(result.messages[0].content.text).toContain('<p>Hello</p>');
    });

    it('should indicate empty page in create-confluence-page when body is omitted', async () => {
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'create-confluence-page');
      const handler = call.at(-1);
      const result = await handler({ parentPageUrl: 'https://parent.url', title: 'Empty Page' });
      expect(result.messages[0].content.text).toContain('empty');
    });

    it('should handle undefined args gracefully', async () => {
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'search-confluence');
      const handler = call.at(-1);
      const result = await handler(undefined);
      expect(result.messages[0].content.text).toBeDefined();
      expect(typeof result.messages[0].content.text).toBe('string');
    });

    it('should generate get-confluence-page with pageId', async () => {
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'get-confluence-page');
      const handler = call.at(-1);
      const result = await handler({ pageId: '111222333' });
      expect(result.messages[0].content.text).toContain('111222333');
    });

    it('should generate find-confluence-page with spaceKey and title', async () => {
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'find-confluence-page');
      const handler = call.at(-1);
      const result = await handler({ spaceKey: 'PLAT', title: 'Architecture Guide' });
      expect(result.messages[0].content.text).toContain('PLAT');
      expect(result.messages[0].content.text).toContain('Architecture Guide');
    });

    it('should generate get-confluence-page-children with pageId', async () => {
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'get-confluence-page-children');
      const handler = call.at(-1);
      const result = await handler({ pageId: '999' });
      expect(result.messages[0].content.text).toContain('999');
    });

    it('should include limit in get-confluence-page-children when provided', async () => {
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'get-confluence-page-children');
      const handler = call.at(-1);
      const result = await handler({ pageId: '999', limit: '10' });
      expect(result.messages[0].content.text).toContain('10');
    });

    it('should generate list-confluence-spaces without limit', async () => {
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'list-confluence-spaces');
      const handler = call.at(-1);
      const result = await handler({});
      expect(result.messages[0].content.text).toContain('confluence_list_spaces');
    });

    it('should include limit in list-confluence-spaces when provided', async () => {
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'list-confluence-spaces');
      const handler = call.at(-1);
      const result = await handler({ limit: '20' });
      expect(result.messages[0].content.text).toContain('20');
    });

    it('should generate get-confluence-space with spaceKey', async () => {
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'get-confluence-space');
      const handler = call.at(-1);
      const result = await handler({ spaceKey: 'TEAM' });
      expect(result.messages[0].content.text).toContain('TEAM');
    });

    it('should generate delete-confluence-page with pageId and title', async () => {
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'delete-confluence-page');
      const handler = call.at(-1);
      const result = await handler({ pageId: '888', title: 'Old Page' });
      expect(result.messages[0].content.text).toContain('888');
      expect(result.messages[0].content.text).toContain('Old Page');
    });

    it('should generate add-confluence-comment with pageId and body', async () => {
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'add-confluence-comment');
      const handler = call.at(-1);
      const result = await handler({ pageId: '555', body: '<p>Nice work</p>' });
      expect(result.messages[0].content.text).toContain('555');
      expect(result.messages[0].content.text).toContain('<p>Nice work</p>');
    });

    it('should generate get-confluence-labels with pageId', async () => {
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'get-confluence-labels');
      const handler = call.at(-1);
      const result = await handler({ pageId: '444' });
      expect(result.messages[0].content.text).toContain('444');
    });

    it('should generate add-confluence-label with pageId and label', async () => {
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'add-confluence-label');
      const handler = call.at(-1);
      const result = await handler({ pageId: '333', label: 'architecture' });
      expect(result.messages[0].content.text).toContain('architecture');
      expect(result.messages[0].content.text).toContain('333');
    });
  });
});
