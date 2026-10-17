import { describe, it, expect, vi, beforeEach } from 'vitest';
import {
  configureScwikiTools,
  SCWIKI_TOOLS,
  parsePageReference,
  buildPagePath,
  parseViewUrl,
  checkConfig,
  formatError,
  buildAxiosConfig
} from '../src/tools/scwiki.js';
import { createMockServer, isValidToolResponse, isValidErrorResponse } from '@sc-node-mcp/shared-tests/helpers/mockServer';
import axios from 'axios';

vi.mock('axios');

describe('SC Wiki Tools', () => {
  let mockServer;
  let scwikiConfig;

  beforeEach(() => {
    vi.clearAllMocks();
    mockServer = createMockServer();
    scwikiConfig = {
      baseUrl: 'https://scwiki.example.com',
      token: 'test-bearer-token',
      wiki: 'xwiki'
    };
  });

  describe('configureScwikiTools', () => {
    it('should register all 14 tools on the server', () => {
      configureScwikiTools(mockServer, scwikiConfig);
      const tools = mockServer.getRegisteredTools();
      expect(tools).toHaveLength(14);
    });

    it('should register every tool name from SCWIKI_TOOLS', () => {
      configureScwikiTools(mockServer, scwikiConfig);
      Object.values(SCWIKI_TOOLS).forEach(name => {
        expect(mockServer.getTool(name)).toBeDefined();
      });
    });

    it('should gate every tool behind checkConfig when config is invalid', async () => {
      configureScwikiTools(mockServer, null);
      const genericParams = {
        pageReference: 'Sandbox.WebHome',
        query: 'x',
        pageUrl: 'https://scwiki.example.com/bin/view/Sandbox/',
        title: 'x',
        text: 'x',
        tag: 'x',
        content: 'x'
      };
      for (const name of Object.values(SCWIKI_TOOLS)) {
        const response = await mockServer.invokeTool(name, genericParams);
        expect(isValidErrorResponse(response)).toBe(true);
      }
      expect(axios.get).not.toHaveBeenCalled();
      expect(axios.post).not.toHaveBeenCalled();
      expect(axios.put).not.toHaveBeenCalled();
      expect(axios.delete).not.toHaveBeenCalled();
    });
  });

  describe('checkConfig', () => {
    it('returns an error when both baseUrl and token are missing', () => {
      expect(checkConfig(null)).not.toBeNull();
      expect(checkConfig({})).not.toBeNull();
    });

    it('returns an error when only baseUrl is present', () => {
      expect(checkConfig({ baseUrl: 'https://x' })).not.toBeNull();
    });

    it('returns an error when only token is present', () => {
      expect(checkConfig({ token: 't' })).not.toBeNull();
    });

    it('returns null when both baseUrl and token are present', () => {
      expect(checkConfig({ baseUrl: 'https://x', token: 't' })).toBeNull();
    });
  });

  describe('formatError', () => {
    it('returns the .message of an Error instance', () => {
      expect(formatError(new Error('boom'))).toBe('boom');
    });

    it('falls back to String(error) for a non-Error rejection value', () => {
      expect(formatError('plain string failure')).toBe('plain string failure');
    });

    it('falls back to String(error) for a nullish rejection value', () => {
      expect(formatError(null)).toBe('null');
    });
  });

  describe('buildAxiosConfig', () => {
    it('does not set an httpsAgent when no proxy is configured', () => {
      const config = buildAxiosConfig('token', '');
      expect(config.httpsAgent).toBeUndefined();
    });

    it('sets an httpsAgent when an explicit proxy URL is provided', () => {
      const config = buildAxiosConfig('token', 'http://proxy.example.com:8080');
      expect(config.httpsAgent).toBeDefined();
    });
  });

  describe('parsePageReference', () => {
    it('parses a simple two-part reference', () => {
      expect(parsePageReference('Sandbox.WebHome')).toEqual({
        wiki: undefined,
        spaceSegments: ['Sandbox'],
        pageName: 'WebHome'
      });
    });

    it('parses a nested-space reference', () => {
      expect(parsePageReference('Sandbox.S2B NG.WebHome')).toEqual({
        wiki: undefined,
        spaceSegments: ['Sandbox', 'S2B NG'],
        pageName: 'WebHome'
      });
    });

    it('parses a reference with an escaped literal dot', () => {
      expect(parsePageReference('Sandbox.Release 1\\.0.WebHome')).toEqual({
        wiki: undefined,
        spaceSegments: ['Sandbox', 'Release 1.0'],
        pageName: 'WebHome'
      });
    });

    it('parses a reference with a "wiki:" prefix', () => {
      expect(parsePageReference('otherwiki:Sandbox.WebHome')).toEqual({
        wiki: 'otherwiki',
        spaceSegments: ['Sandbox'],
        pageName: 'WebHome'
      });
    });

    it('throws on a reference with an empty segment', () => {
      expect(() => parsePageReference('Sandbox..WebHome')).toThrow(/Invalid page reference/);
    });

    it('does not treat a colon after the first dot as a wiki prefix', () => {
      expect(parsePageReference('Sandbox.Page:Name')).toEqual({
        wiki: undefined,
        spaceSegments: ['Sandbox'],
        pageName: 'Page:Name'
      });
    });

    it('throws on a reference with no space segment', () => {
      expect(() => parsePageReference('WebHome')).toThrow(/Invalid page reference/);
    });

    it('throws on an empty reference', () => {
      expect(() => parsePageReference('')).toThrow(/Invalid page reference/);
    });

    it('throws on a non-string reference', () => {
      expect(() => parsePageReference(undefined)).toThrow(/Invalid page reference/);
    });
  });

  describe('buildPagePath', () => {
    it('builds a path for a single-space reference', () => {
      const parsed = parsePageReference('Sandbox.WebHome');
      expect(buildPagePath(parsed, 'xwiki')).toBe('/wikis/xwiki/spaces/Sandbox/pages/WebHome');
    });

    it('builds a path for a nested-space reference with an encoded space', () => {
      const parsed = parsePageReference('Sandbox.S2B NG.WebHome');
      expect(buildPagePath(parsed, 'xwiki')).toBe('/wikis/xwiki/spaces/Sandbox/spaces/S2B%20NG/pages/WebHome');
    });

    it('uses the reference\'s own wiki prefix over the default wiki', () => {
      const parsed = parsePageReference('otherwiki:Sandbox.WebHome');
      expect(buildPagePath(parsed, 'xwiki')).toBe('/wikis/otherwiki/spaces/Sandbox/pages/WebHome');
    });
  });

  describe('parseViewUrl', () => {
    it('defaults to WebHome for a trailing-slash nested-space URL', () => {
      expect(parseViewUrl('https://scwiki.example.com/bin/view/Sandbox/S2B%20NG/')).toBe('Sandbox.S2B NG.WebHome');
    });

    it('uses the final segment as the page name when there is no trailing slash', () => {
      expect(parseViewUrl('https://scwiki.example.com/bin/view/Sandbox/MyPage')).toBe('Sandbox.MyPage');
    });

    it('escapes literal dots found in decoded segments', () => {
      expect(parseViewUrl('https://scwiki.example.com/bin/view/Sandbox/Release%201.0/')).toBe('Sandbox.Release 1\\.0.WebHome');
    });

    it('throws when the URL has no /bin/view/ path', () => {
      expect(() => parseViewUrl('https://scwiki.example.com/rest/wikis')).toThrow(/Could not parse/);
    });
  });

  describe('scwiki_search', () => {
    beforeEach(() => configureScwikiTools(mockServer, scwikiConfig));

    it('should return search results', async () => {
      axios.get.mockResolvedValue({ data: { searchResults: [{ pageFullName: 'Sandbox.WebHome' }] } });
      const response = await mockServer.invokeTool(SCWIKI_TOOLS.search, { query: 'test' });
      expect(isValidToolResponse(response)).toBe(true);
      expect(axios.get).toHaveBeenCalledWith(
        expect.stringContaining('/rest/wikis/xwiki/search?q=test'),
        expect.any(Object)
      );
    });

    it('should return an error response on failure', async () => {
      axios.get.mockRejectedValue(new Error('network error'));
      const response = await mockServer.invokeTool(SCWIKI_TOOLS.search, { query: 'test' });
      expect(isValidErrorResponse(response)).toBe(true);
    });

    it('should return config-missing error when config is invalid', async () => {
      configureScwikiTools(mockServer, null);
      const response = await mockServer.invokeTool(SCWIKI_TOOLS.search, { query: 'test' });
      expect(isValidErrorResponse(response)).toBe(true);
      expect(axios.get).not.toHaveBeenCalled();
    });
  });

  describe('scwiki_get_page', () => {
    beforeEach(() => configureScwikiTools(mockServer, scwikiConfig));

    it('should return the page fields', async () => {
      axios.get.mockResolvedValue({
        data: {
          id: 'xwiki:Sandbox.WebHome', fullName: 'Sandbox.WebHome', wiki: 'xwiki', space: 'Sandbox',
          name: 'WebHome', title: 'Home', version: '1.1', content: 'Hello', syntax: 'xwiki/2.1',
          parent: null, created: 1, creator: 'XWiki.user', modified: 1, modifier: 'XWiki.user',
          xwikiAbsoluteUrl: 'https://scwiki.example.com/bin/view/Sandbox/'
        }
      });
      const response = await mockServer.invokeTool(SCWIKI_TOOLS.get_page, { pageReference: 'Sandbox.WebHome' });
      expect(isValidToolResponse(response)).toBe(true);
      const parsed = JSON.parse(response.content[0].text);
      expect(parsed.title).toBe('Home');
      expect(parsed.content).toBe('Hello');
    });

    it('should return an error response for an invalid reference', async () => {
      const response = await mockServer.invokeTool(SCWIKI_TOOLS.get_page, { pageReference: 'NoSpace' });
      expect(isValidErrorResponse(response)).toBe(true);
    });

    it('should return an error response on axios failure', async () => {
      axios.get.mockRejectedValue(new Error('boom'));
      const response = await mockServer.invokeTool(SCWIKI_TOOLS.get_page, { pageReference: 'Sandbox.WebHome' });
      expect(isValidErrorResponse(response)).toBe(true);
    });
  });

  describe('scwiki_find_page', () => {
    beforeEach(() => configureScwikiTools(mockServer, scwikiConfig));

    it('should resolve the URL and return page metadata', async () => {
      axios.get.mockResolvedValue({ data: { title: 'S2B NG', content: 'Hello Testing mate' } });
      const response = await mockServer.invokeTool(SCWIKI_TOOLS.find_page, {
        pageUrl: 'https://scwiki.example.com/bin/view/Sandbox/S2B%20NG/'
      });
      expect(isValidToolResponse(response)).toBe(true);
      const parsed = JSON.parse(response.content[0].text);
      expect(parsed.pageReference).toBe('Sandbox.S2B NG.WebHome');
      expect(parsed.title).toBe('S2B NG');
    });

    it('should return an error response for an unparsable URL', async () => {
      const response = await mockServer.invokeTool(SCWIKI_TOOLS.find_page, { pageUrl: 'https://scwiki.example.com/rest/wikis' });
      expect(isValidErrorResponse(response)).toBe(true);
    });
  });

  describe('scwiki_create_page', () => {
    beforeEach(() => configureScwikiTools(mockServer, scwikiConfig));

    it('should PUT a form-urlencoded body and return the created page', async () => {
      axios.put.mockResolvedValue({ data: { title: 'New Page', content: 'Body', version: '1.1' } });
      const response = await mockServer.invokeTool(SCWIKI_TOOLS.create_page, {
        pageReference: 'Sandbox.NewPage',
        title: 'New Page',
        content: 'Body'
      });
      expect(isValidToolResponse(response)).toBe(true);
      expect(axios.put).toHaveBeenCalledWith(
        expect.stringContaining('/wikis/xwiki/spaces/Sandbox/pages/NewPage'),
        expect.stringContaining('title=New+Page'),
        expect.objectContaining({ headers: expect.objectContaining({ 'Content-Type': 'application/x-www-form-urlencoded' }) })
      );
    });

    it('should return an error response on axios failure', async () => {
      axios.put.mockRejectedValue(new Error('boom'));
      const response = await mockServer.invokeTool(SCWIKI_TOOLS.create_page, { pageReference: 'Sandbox.NewPage', title: 'T' });
      expect(isValidErrorResponse(response)).toBe(true);
    });
  });

  describe('scwiki_update_page', () => {
    beforeEach(() => configureScwikiTools(mockServer, scwikiConfig));

    it('should PUT the updated content', async () => {
      axios.put.mockResolvedValue({ data: { title: 'Home', content: 'Updated', version: '2.1' } });
      const response = await mockServer.invokeTool(SCWIKI_TOOLS.update_page, {
        pageReference: 'Sandbox.WebHome',
        content: 'Updated'
      });
      expect(isValidToolResponse(response)).toBe(true);
      const parsed = JSON.parse(response.content[0].text);
      expect(parsed.content).toBe('Updated');
    });

    it('should reject when neither title nor content is provided', async () => {
      const response = await mockServer.invokeTool(SCWIKI_TOOLS.update_page, { pageReference: 'Sandbox.WebHome' });
      expect(isValidErrorResponse(response)).toBe(true);
      expect(axios.put).not.toHaveBeenCalled();
    });

    it('should return an error response on axios failure', async () => {
      axios.put.mockRejectedValue(new Error('boom'));
      const response = await mockServer.invokeTool(SCWIKI_TOOLS.update_page, { pageReference: 'Sandbox.WebHome', content: 'x' });
      expect(isValidErrorResponse(response)).toBe(true);
    });
  });

  describe('scwiki_delete_page', () => {
    beforeEach(() => configureScwikiTools(mockServer, scwikiConfig));

    it('should delete the page when the title matches', async () => {
      axios.get.mockResolvedValue({ data: { title: 'WebHome' } });
      axios.delete.mockResolvedValue({ data: {} });
      const response = await mockServer.invokeTool(SCWIKI_TOOLS.delete_page, {
        pageReference: 'Sandbox.WebHome',
        title: 'WebHome'
      });
      expect(isValidToolResponse(response)).toBe(true);
      expect(axios.delete).toHaveBeenCalled();
    });

    it('should cancel the deletion when the title does not match', async () => {
      axios.get.mockResolvedValue({ data: { title: 'Actual Title' } });
      const response = await mockServer.invokeTool(SCWIKI_TOOLS.delete_page, {
        pageReference: 'Sandbox.WebHome',
        title: 'Wrong Title'
      });
      expect(isValidErrorResponse(response)).toBe(true);
      expect(axios.delete).not.toHaveBeenCalled();
    });

    it('should return an error response on axios failure', async () => {
      axios.get.mockRejectedValue(new Error('boom'));
      const response = await mockServer.invokeTool(SCWIKI_TOOLS.delete_page, { pageReference: 'Sandbox.WebHome', title: 'x' });
      expect(isValidErrorResponse(response)).toBe(true);
    });
  });

  describe('scwiki_get_page_children', () => {
    beforeEach(() => configureScwikiTools(mockServer, scwikiConfig));

    it('should list child pages', async () => {
      axios.get.mockResolvedValue({ data: { pageSummaries: [] } });
      const response = await mockServer.invokeTool(SCWIKI_TOOLS.get_page_children, { pageReference: 'Sandbox.WebHome' });
      expect(isValidToolResponse(response)).toBe(true);
      expect(axios.get).toHaveBeenCalledWith(expect.stringContaining('/children?number=25'), expect.any(Object));
    });

    it('should return an error response on axios failure', async () => {
      axios.get.mockRejectedValue(new Error('boom'));
      const response = await mockServer.invokeTool(SCWIKI_TOOLS.get_page_children, { pageReference: 'Sandbox.WebHome' });
      expect(isValidErrorResponse(response)).toBe(true);
    });
  });

  describe('scwiki_list_spaces', () => {
    beforeEach(() => configureScwikiTools(mockServer, scwikiConfig));

    it('should list spaces', async () => {
      axios.get.mockResolvedValue({ data: { spaces: [] } });
      const response = await mockServer.invokeTool(SCWIKI_TOOLS.list_spaces, {});
      expect(isValidToolResponse(response)).toBe(true);
      expect(axios.get).toHaveBeenCalledWith(expect.stringContaining('/wikis/xwiki/spaces?number=50'), expect.any(Object));
    });

    it('should return an error response on axios failure', async () => {
      axios.get.mockRejectedValue(new Error('boom'));
      const response = await mockServer.invokeTool(SCWIKI_TOOLS.list_spaces, {});
      expect(isValidErrorResponse(response)).toBe(true);
    });
  });

  describe('scwiki_list_my_pages', () => {
    beforeEach(() => configureScwikiTools(mockServer, scwikiConfig));

    it('should resolve the current user then query pages by creator', async () => {
      axios.get
        .mockResolvedValueOnce({ data: { id: 'XWiki.user' } })
        .mockResolvedValueOnce({ data: { searchResults: [] } });
      const response = await mockServer.invokeTool(SCWIKI_TOOLS.list_my_pages, {});
      expect(isValidToolResponse(response)).toBe(true);
      expect(axios.get).toHaveBeenNthCalledWith(1, expect.stringContaining('/wikis/xwiki/user'), expect.any(Object));
      expect(axios.get).toHaveBeenNthCalledWith(2, expect.stringContaining('type=xwql'), expect.any(Object));
    });

    it('should return an error response when the current user cannot be resolved', async () => {
      axios.get.mockResolvedValueOnce({ data: {} });
      const response = await mockServer.invokeTool(SCWIKI_TOOLS.list_my_pages, {});
      expect(isValidErrorResponse(response)).toBe(true);
    });

    it('should return an error response on axios failure', async () => {
      axios.get.mockRejectedValue(new Error('boom'));
      const response = await mockServer.invokeTool(SCWIKI_TOOLS.list_my_pages, {});
      expect(isValidErrorResponse(response)).toBe(true);
    });
  });

  describe('scwiki_add_comment', () => {
    beforeEach(() => configureScwikiTools(mockServer, scwikiConfig));

    it('should post the comment', async () => {
      axios.post.mockResolvedValue({ data: { id: '1' } });
      const response = await mockServer.invokeTool(SCWIKI_TOOLS.add_comment, { pageReference: 'Sandbox.WebHome', text: 'hi' });
      expect(isValidToolResponse(response)).toBe(true);
      expect(axios.post).toHaveBeenCalledWith(
        expect.stringContaining('/comments'),
        expect.stringContaining('text=hi'),
        expect.any(Object)
      );
    });

    it('should return an error response on axios failure', async () => {
      axios.post.mockRejectedValue(new Error('boom'));
      const response = await mockServer.invokeTool(SCWIKI_TOOLS.add_comment, { pageReference: 'Sandbox.WebHome', text: 'hi' });
      expect(isValidErrorResponse(response)).toBe(true);
    });
  });

  describe('scwiki_get_labels', () => {
    beforeEach(() => configureScwikiTools(mockServer, scwikiConfig));

    it('should get the tags', async () => {
      axios.get.mockResolvedValue({ data: { tags: [] } });
      const response = await mockServer.invokeTool(SCWIKI_TOOLS.get_labels, { pageReference: 'Sandbox.WebHome' });
      expect(isValidToolResponse(response)).toBe(true);
      expect(axios.get).toHaveBeenCalledWith(expect.stringContaining('/tags'), expect.any(Object));
    });

    it('should return an error response on axios failure', async () => {
      axios.get.mockRejectedValue(new Error('boom'));
      const response = await mockServer.invokeTool(SCWIKI_TOOLS.get_labels, { pageReference: 'Sandbox.WebHome' });
      expect(isValidErrorResponse(response)).toBe(true);
    });
  });

  describe('scwiki_add_label', () => {
    beforeEach(() => configureScwikiTools(mockServer, scwikiConfig));

    it('should add the tag', async () => {
      axios.put.mockResolvedValue({ data: { tags: ['test'] } });
      const response = await mockServer.invokeTool(SCWIKI_TOOLS.add_label, { pageReference: 'Sandbox.WebHome', tag: 'test' });
      expect(isValidToolResponse(response)).toBe(true);
      expect(axios.put).toHaveBeenCalledWith(
        expect.stringContaining('/tags'),
        expect.stringContaining('tag=test'),
        expect.any(Object)
      );
    });

    it('should return an error response on axios failure', async () => {
      axios.put.mockRejectedValue(new Error('boom'));
      const response = await mockServer.invokeTool(SCWIKI_TOOLS.add_label, { pageReference: 'Sandbox.WebHome', tag: 'test' });
      expect(isValidErrorResponse(response)).toBe(true);
    });
  });

  describe('scwiki_get_page_history', () => {
    beforeEach(() => configureScwikiTools(mockServer, scwikiConfig));

    it('should get the version history', async () => {
      axios.get.mockResolvedValue({ data: { historySummaries: [] } });
      const response = await mockServer.invokeTool(SCWIKI_TOOLS.get_page_history, { pageReference: 'Sandbox.WebHome' });
      expect(isValidToolResponse(response)).toBe(true);
      expect(axios.get).toHaveBeenCalledWith(expect.stringContaining('/history?number=25'), expect.any(Object));
    });

    it('should return an error response on axios failure', async () => {
      axios.get.mockRejectedValue(new Error('boom'));
      const response = await mockServer.invokeTool(SCWIKI_TOOLS.get_page_history, { pageReference: 'Sandbox.WebHome' });
      expect(isValidErrorResponse(response)).toBe(true);
    });
  });

  describe('scwiki_list_attachments', () => {
    beforeEach(() => configureScwikiTools(mockServer, scwikiConfig));

    it('should list attachments', async () => {
      axios.get.mockResolvedValue({ data: { attachments: [] } });
      const response = await mockServer.invokeTool(SCWIKI_TOOLS.list_attachments, { pageReference: 'Sandbox.WebHome' });
      expect(isValidToolResponse(response)).toBe(true);
      expect(axios.get).toHaveBeenCalledWith(expect.stringContaining('/attachments'), expect.any(Object));
    });

    it('should return an error response on axios failure', async () => {
      axios.get.mockRejectedValue(new Error('boom'));
      const response = await mockServer.invokeTool(SCWIKI_TOOLS.list_attachments, { pageReference: 'Sandbox.WebHome' });
      expect(isValidErrorResponse(response)).toBe(true);
    });
  });
});
