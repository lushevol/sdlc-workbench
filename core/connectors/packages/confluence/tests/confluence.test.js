import { describe, it, expect, vi, beforeEach } from 'vitest';
import { configureConfluenceTools } from '../src/tools.js';
import { createMockServer, isValidToolResponse, isValidErrorResponse } from '@sc-node-mcp/shared-tests/helpers/mockServer';
import axios from 'axios';

// Mock axios
vi.mock('axios');

describe('Confluence Tools', () => {
  let mockServer;
  let confluenceConfig;

  beforeEach(() => {
    vi.clearAllMocks();
    mockServer = createMockServer();
    confluenceConfig = {
      baseUrl: 'https://confluence.example.com',
      token: 'test-bearer-token'
    };
  });

  describe('configureConfluenceTools', () => {
    it('should register confluence tools on the server', () => {
      configureConfluenceTools(mockServer, confluenceConfig);

      const tools = mockServer.getRegisteredTools();
      expect(tools.length).toBeGreaterThan(0);
    });

    it('should register confluence_list_my_pages tool', () => {
      configureConfluenceTools(mockServer, confluenceConfig);

      const tool = mockServer.getTool('confluence_list_my_pages');
      expect(tool).toBeDefined();
      expect(tool.name).toBe('confluence_list_my_pages');
      expect(tool.description).toContain('Confluence pages');
    });
  });

  describe('confluence_list_my_pages', () => {
    beforeEach(() => {
      configureConfluenceTools(mockServer, confluenceConfig);
    });

    it('should list pages via CQL creator=currentUser()', async () => {
      const mockPages = {
        data: {
          results: [
            { id: '123', title: 'Test Page 1' },
            { id: '456', title: 'Test Page 2' }
          ]
        }
      };

      axios.get.mockResolvedValue(mockPages);

      const response = await mockServer.invokeTool('confluence_list_my_pages', {});

      expect(isValidToolResponse(response)).toBe(true);
      expect(axios.get).toHaveBeenCalled();

      const url = axios.get.mock.calls[0][0];
      expect(url).toContain('content/search');
      expect(url).toContain('creator=currentUser()');

      const content = JSON.parse(response.content[0].text);
      expect(content).toHaveLength(2);
      expect(content[0].title).toBe('Test Page 1');
    });

    it('should respect limit parameter', async () => {
      axios.get.mockResolvedValue({ data: { results: [] } });

      await mockServer.invokeTool('confluence_list_my_pages', { limit: 5 });

      expect(axios.get).toHaveBeenCalledWith(
        expect.stringContaining('limit=5'),
        expect.any(Object)
      );
    });

    it('should use default limit of 10', async () => {
      axios.get.mockResolvedValue({ data: { results: [] } });

      await mockServer.invokeTool('confluence_list_my_pages', {});

      expect(axios.get).toHaveBeenCalledWith(
        expect.stringContaining('limit=10'),
        expect.any(Object)
      );
    });

    it('should filter by space key in CQL when provided', async () => {
      axios.get.mockResolvedValue({ data: { results: [] } });

      await mockServer.invokeTool('confluence_list_my_pages', { spaceKey: 'TEST' });

      const url = axios.get.mock.calls[0][0];
      expect(url).toContain('TEST');
    });

    it('should use Bearer token authentication', async () => {
      axios.get.mockResolvedValue({ data: { results: [] } });

      await mockServer.invokeTool('confluence_list_my_pages', {});

      expect(axios.get).toHaveBeenCalledWith(
        expect.any(String),
        expect.objectContaining({
          headers: expect.objectContaining({
            Authorization: 'Bearer test-bearer-token',
            Accept: 'application/json'
          })
        })
      );
    });

    it('should return error when Confluence config is missing', async () => {
      configureConfluenceTools(mockServer, null);

      const response = await mockServer.invokeTool('confluence_list_my_pages', {});

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('Confluence config missing');
    });

    it('should return error when Confluence config is incomplete', async () => {
      const incompleteConfig = {
        baseUrl: 'https://confluence.example.com'
        // Missing token
      };

      configureConfluenceTools(mockServer, incompleteConfig);

      const response = await mockServer.invokeTool('confluence_list_my_pages', {});

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('Confluence config missing');
    });

    it('should handle API errors gracefully', async () => {
      axios.get.mockRejectedValue(new Error('Network error'));

      const response = await mockServer.invokeTool('confluence_list_my_pages', {});

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('Network error');
    });

    it('should handle empty results', async () => {
      axios.get.mockResolvedValue({ data: { results: [] } });

      const response = await mockServer.invokeTool('confluence_list_my_pages', {});

      expect(isValidToolResponse(response)).toBe(true);
      const content = JSON.parse(response.content[0].text);
      expect(content).toHaveLength(0);
    });

    it('should handle 401 unauthorized error', async () => {
      const error = new Error('Request failed with status code 401');
      error.response = { status: 401 };
      axios.get.mockRejectedValue(error);

      const response = await mockServer.invokeTool('confluence_list_my_pages', {});

      expect(isValidErrorResponse(response)).toBe(true);
    });

    it('should handle non-Error thrown values', async () => {
      axios.get.mockRejectedValue('raw list pages error');
      const response = await mockServer.invokeTool('confluence_list_my_pages', {});
      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('raw list pages error');
    });

    it('should default to an empty list when the response has no results field', async () => {
      axios.get.mockResolvedValue({ data: {} });

      const response = await mockServer.invokeTool('confluence_list_my_pages', {});

      expect(isValidToolResponse(response)).toBe(true);
      expect(JSON.parse(response.content[0].text)).toEqual([]);
    });

    it('should route the request through an explicit proxy when configured', async () => {
      axios.get.mockResolvedValue({ data: { results: [] } });
      configureConfluenceTools(mockServer, { ...confluenceConfig, proxy: 'http://10.239.9.190:443' });

      const response = await mockServer.invokeTool('confluence_list_my_pages', {});

      expect(isValidToolResponse(response)).toBe(true);
      expect(axios.get).toHaveBeenCalledWith(
        expect.any(String),
        expect.objectContaining({ httpsAgent: expect.anything() })
      );
    });
  });

  describe('confluence_search', () => {
    beforeEach(() => {
      configureConfluenceTools(mockServer, confluenceConfig);
    });

    it('should search Confluence with provided CQL', async () => {
      const mockResults = {
        data: {
          results: [
            { id: '789', title: 'Search Result Page', type: 'page' }
          ]
        }
      };

      axios.get.mockResolvedValue(mockResults);

      const response = await mockServer.invokeTool('confluence_search', {
        cql: 'type=page AND space.key="TEAM"'
      });

      expect(isValidToolResponse(response)).toBe(true);
      const url = axios.get.mock.calls[0][0];
      expect(url).toContain('content/search');
      expect(url).toContain(encodeURIComponent('type=page AND space.key="TEAM"'));

      const content = JSON.parse(response.content[0].text);
      expect(content).toHaveLength(1);
      expect(content[0].title).toBe('Search Result Page');
    });

    it('should respect limit parameter', async () => {
      axios.get.mockResolvedValue({ data: { results: [] } });

      await mockServer.invokeTool('confluence_search', { cql: 'type=page', limit: 3 });

      expect(axios.get).toHaveBeenCalledWith(
        expect.stringContaining('limit=3'),
        expect.any(Object)
      );
    });

    it('should use default limit of 10', async () => {
      axios.get.mockResolvedValue({ data: { results: [] } });

      await mockServer.invokeTool('confluence_search', { cql: 'type=page' });

      expect(axios.get).toHaveBeenCalledWith(
        expect.stringContaining('limit=10'),
        expect.any(Object)
      );
    });

    it('should use Bearer token authentication', async () => {
      axios.get.mockResolvedValue({ data: { results: [] } });

      await mockServer.invokeTool('confluence_search', { cql: 'type=page' });

      expect(axios.get).toHaveBeenCalledWith(
        expect.any(String),
        expect.objectContaining({
          headers: expect.objectContaining({
            Authorization: 'Bearer test-bearer-token'
          })
        })
      );
    });

    it('should return error when config is missing', async () => {
      configureConfluenceTools(mockServer, null);

      const response = await mockServer.invokeTool('confluence_search', { cql: 'type=page' });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('Confluence config missing');
    });

    it('should handle network errors gracefully', async () => {
      axios.get.mockRejectedValue(new Error('Network error'));

      const response = await mockServer.invokeTool('confluence_search', { cql: 'type=page' });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('Network error');
    });

    it('should include expand params in search URL', async () => {
      axios.get.mockResolvedValue({ data: { results: [] } });

      await mockServer.invokeTool('confluence_search', { cql: 'type=page' });

      const url = axios.get.mock.calls[0][0];
      expect(url).toContain('expand=version,space,history');
    });

    it('should handle empty search results', async () => {
      axios.get.mockResolvedValue({ data: { results: [] } });

      const response = await mockServer.invokeTool('confluence_search', { cql: 'type=page AND title="nonexistent"' });

      expect(isValidToolResponse(response)).toBe(true);
      const content = JSON.parse(response.content[0].text);
      expect(content).toHaveLength(0);
    });

    it('should handle non-Error thrown values', async () => {
      axios.get.mockRejectedValue('raw search error');
      const response = await mockServer.invokeTool('confluence_search', { cql: 'type=page' });
      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('raw search error');
    });

    it('should default to an empty list when the response has no results field', async () => {
      axios.get.mockResolvedValue({ data: {} });

      const response = await mockServer.invokeTool('confluence_search', { cql: 'type=page' });

      expect(isValidToolResponse(response)).toBe(true);
      expect(JSON.parse(response.content[0].text)).toEqual([]);
    });
  });

  describe('confluence_update_page', () => {
    beforeEach(() => {
      configureConfluenceTools(mockServer, confluenceConfig);
    });

    it('should fetch current version then PUT updated page', async () => {
      const getResponse = {
        data: {
          id: '111',
          title: 'Original Title',
          version: { number: 3 }
        }
      };
      const putResponse = {
        data: {
          id: '111',
          title: 'Original Title',
          version: { number: 4 }
        }
      };

      axios.get.mockResolvedValue(getResponse);
      axios.put.mockResolvedValue(putResponse);

      const response = await mockServer.invokeTool('confluence_update_page', {
        pageId: '111',
        body: '<p>New content</p>'
      });

      expect(isValidToolResponse(response)).toBe(true);

      // GET to fetch current version
      expect(axios.get).toHaveBeenCalledWith(
        expect.stringContaining('content/111'),
        expect.objectContaining({
          headers: expect.objectContaining({ Authorization: 'Bearer test-bearer-token' })
        })
      );

      // PUT with incremented version
      expect(axios.put).toHaveBeenCalledWith(
        expect.stringContaining('content/111'),
        expect.objectContaining({
          version: { number: 4 },
          title: 'Original Title',
          type: 'page',
          body: {
            storage: {
              value: '<p>New content</p>',
              representation: 'storage'
            }
          }
        }),
        expect.any(Object)
      );
    });

    it('should use provided title if given', async () => {
      axios.get.mockResolvedValue({ data: { title: 'Old Title', version: { number: 1 } } });
      axios.put.mockResolvedValue({ data: { id: '111', title: 'New Title', version: { number: 2 } } });

      await mockServer.invokeTool('confluence_update_page', {
        pageId: '111',
        body: '<p>content</p>',
        title: 'New Title'
      });

      expect(axios.put).toHaveBeenCalledWith(
        expect.any(String),
        expect.objectContaining({ title: 'New Title' }),
        expect.any(Object)
      );
    });

    it('should keep existing title when title param is omitted', async () => {
      axios.get.mockResolvedValue({ data: { title: 'Existing Title', version: { number: 2 } } });
      axios.put.mockResolvedValue({ data: { id: '111', title: 'Existing Title', version: { number: 3 } } });

      await mockServer.invokeTool('confluence_update_page', {
        pageId: '111',
        body: '<p>content</p>'
      });

      expect(axios.put).toHaveBeenCalledWith(
        expect.any(String),
        expect.objectContaining({ title: 'Existing Title' }),
        expect.any(Object)
      );
    });

    it('should return error when config is missing', async () => {
      configureConfluenceTools(mockServer, null);

      const response = await mockServer.invokeTool('confluence_update_page', {
        pageId: '111',
        body: '<p>content</p>'
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('Confluence config missing');
    });

    it('should handle page not found (GET fails)', async () => {
      axios.get.mockRejectedValue(new Error('Request failed with status code 404'));

      const response = await mockServer.invokeTool('confluence_update_page', {
        pageId: '999',
        body: '<p>content</p>'
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('404');
    });

    it('should handle PUT errors gracefully', async () => {
      axios.get.mockResolvedValue({ data: { title: 'Title', version: { number: 1 } } });
      axios.put.mockRejectedValue(new Error('Conflict updating page'));

      const response = await mockServer.invokeTool('confluence_update_page', {
        pageId: '111',
        body: '<p>content</p>'
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('Conflict');
    });

    it('should handle non-Error thrown values', async () => {
      axios.get.mockRejectedValue('raw update error');
      const response = await mockServer.invokeTool('confluence_update_page', { pageId: '111', body: '<p>content</p>' });
      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('raw update error');
    });
  });

  describe('confluence_get_page_id', () => {
    beforeEach(() => {
      configureConfluenceTools(mockServer, confluenceConfig);
    });

    it('should resolve page ID from Cloud-style URL with numeric ID in path', async () => {
      axios.get.mockResolvedValue({
        data: {
          id: '123456789',
          title: 'My Page',
          space: { key: 'TEAM' },
          version: { number: 5 },
          _links: { webui: '/wiki/spaces/TEAM/pages/123456789/My+Page' }
        }
      });

      const response = await mockServer.invokeTool('confluence_get_page_id', {
        pageUrl: 'https://confluence.example.com/wiki/spaces/TEAM/pages/123456789/My+Page'
      });

      expect(isValidToolResponse(response)).toBe(true);
      const content = JSON.parse(response.content[0].text);
      expect(content.id).toBe('123456789');
      expect(content.title).toBe('My Page');
      expect(content.space).toBe('TEAM');
      expect(content.version).toBe(5);

      // Should have called the direct content endpoint, not search
      expect(axios.get).toHaveBeenCalledWith(
        expect.stringContaining('/rest/api/content/123456789'),
        expect.any(Object)
      );
    });

    it('should resolve page ID from viewpage.action?pageId= URL', async () => {
      axios.get.mockResolvedValue({
        data: {
          id: '3626394117',
          title: 'Classic Server Page',
          space: { key: 'SC' },
          version: { number: 1 },
          _links: { webui: '/pages/viewpage.action?pageId=3626394117' }
        }
      });

      const response = await mockServer.invokeTool('confluence_get_page_id', {
        pageUrl: 'https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3626394117'
      });

      expect(isValidToolResponse(response)).toBe(true);
      const content = JSON.parse(response.content[0].text);
      expect(content.id).toBe('3626394117');
      expect(content.title).toBe('Classic Server Page');
      expect(content.space).toBe('SC');

      // Should call the direct content endpoint using the query-param ID
      expect(axios.get).toHaveBeenCalledWith(
        expect.stringContaining('/rest/api/content/3626394117'),
        expect.any(Object)
      );
    });

    it('should use Bearer auth when resolving page ID', async () => {
      axios.get.mockResolvedValue({
        data: { id: '111', title: 'T', space: { key: 'S' }, version: { number: 1 }, _links: {} }
      });

      await mockServer.invokeTool('confluence_get_page_id', {
        pageUrl: 'https://confluence.example.com/wiki/spaces/S/pages/111/T'
      });

      expect(axios.get).toHaveBeenCalledWith(
        expect.any(String),
        expect.objectContaining({
          headers: expect.objectContaining({ Authorization: 'Bearer test-bearer-token' })
        })
      );
    });

    it('should resolve page ID from Server-style display URL via CQL', async () => {
      axios.get.mockResolvedValue({
        data: {
          results: [{
            id: '987654321',
            title: 'Server Page',
            space: { key: 'PROJ' },
            version: { number: 2 },
            _links: { webui: '/display/PROJ/Server+Page' }
          }]
        }
      });

      const response = await mockServer.invokeTool('confluence_get_page_id', {
        pageUrl: 'https://confluence.example.com/display/PROJ/Server+Page'
      });

      expect(isValidToolResponse(response)).toBe(true);
      const content = JSON.parse(response.content[0].text);
      expect(content.id).toBe('987654321');
      expect(content.title).toBe('Server Page');
      expect(content.space).toBe('PROJ');

      // Should have called the search endpoint (CQL)
      expect(axios.get).toHaveBeenCalledWith(
        expect.stringContaining('content/search'),
        expect.any(Object)
      );
    });

    it('should return error when display-URL search returns no results', async () => {
      axios.get.mockResolvedValue({ data: { results: [] } });

      const response = await mockServer.invokeTool('confluence_get_page_id', {
        pageUrl: 'https://confluence.example.com/display/PROJ/NonexistentPage'
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('No page found');
    });

    it('should return error for unrecognised URL format', async () => {
      const response = await mockServer.invokeTool('confluence_get_page_id', {
        pageUrl: 'https://confluence.example.com/some/random/path'
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('Could not parse page ID');
    });

    it('should return error when config is missing', async () => {
      configureConfluenceTools(mockServer, null);

      const response = await mockServer.invokeTool('confluence_get_page_id', {
        pageUrl: 'https://confluence.example.com/wiki/spaces/X/pages/1/Title'
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('Confluence config missing');
    });

    it('should handle API errors gracefully', async () => {
      axios.get.mockRejectedValue(new Error('Network error'));

      const response = await mockServer.invokeTool('confluence_get_page_id', {
        pageUrl: 'https://confluence.example.com/wiki/spaces/X/pages/123/Title'
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('Network error');
    });

    it('should handle non-Error thrown values', async () => {
      axios.get.mockRejectedValue('raw page id error');
      const response = await mockServer.invokeTool('confluence_get_page_id', {
        pageUrl: 'https://confluence.example.com/wiki/spaces/X/pages/123/Title'
      });
      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('raw page id error');
    });

    it('should default to an empty list when display-URL search response has no results field', async () => {
      axios.get.mockResolvedValue({ data: {} });

      const response = await mockServer.invokeTool('confluence_get_page_id', {
        pageUrl: 'https://confluence.example.com/display/PROJ/SomePage'
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('No page found');
    });

    it('should fall back to the source pageUrl when the resolved page has no _links', async () => {
      axios.get.mockResolvedValue({
        data: {
          results: [{ id: '1', title: 'T', space: { key: 'S' }, version: { number: 1 } }]
        }
      });

      const response = await mockServer.invokeTool('confluence_get_page_id', {
        pageUrl: 'https://confluence.example.com/display/S/T'
      });

      expect(isValidToolResponse(response)).toBe(true);
      const content = JSON.parse(response.content[0].text);
      expect(content.url).toBe('https://confluence.example.com/display/S/T');
    });
  });

  describe('confluence_create_page', () => {
    beforeEach(() => {
      configureConfluenceTools(mockServer, confluenceConfig);
    });

    it('should create a page under a Cloud-style parent URL', async () => {
      const parentGetResponse = {
        data: { id: '123456789', space: { key: 'TEAM' } }
      };
      const postResponse = {
        data: {
          id: '999',
          title: 'New Child Page',
          space: { key: 'TEAM' },
          _links: { webui: '/wiki/spaces/TEAM/pages/999/New+Child+Page' }
        }
      };

      axios.get.mockResolvedValue(parentGetResponse);
      axios.post.mockResolvedValue(postResponse);

      const response = await mockServer.invokeTool('confluence_create_page', {
        parentPageUrl: 'https://confluence.example.com/wiki/spaces/TEAM/pages/123456789/Parent+Page',
        title: 'New Child Page'
      });

      expect(isValidToolResponse(response)).toBe(true);

      expect(axios.get).toHaveBeenCalledWith(
        expect.stringContaining('/rest/api/content/123456789'),
        expect.any(Object)
      );
      expect(axios.post).toHaveBeenCalledWith(
        expect.stringContaining('/rest/api/content'),
        expect.objectContaining({
          type: 'page',
          title: 'New Child Page',
          ancestors: [{ id: '123456789' }],
          space: { key: 'TEAM' }
        }),
        expect.any(Object)
      );

      const content = JSON.parse(response.content[0].text);
      expect(content.id).toBe('999');
      expect(content.title).toBe('New Child Page');
      expect(content.space).toBe('TEAM');
      expect(content.url).toContain('999');
    });

    it('should default body to empty paragraph when omitted', async () => {
      axios.get.mockResolvedValue({ data: { space: { key: 'TEAM' } } });
      axios.post.mockResolvedValue({
        data: { id: '1', title: 'Page', space: { key: 'TEAM' }, _links: {} }
      });

      await mockServer.invokeTool('confluence_create_page', {
        parentPageUrl: 'https://confluence.example.com/wiki/spaces/TEAM/pages/123/Parent',
        title: 'Page'
      });

      expect(axios.post).toHaveBeenCalledWith(
        expect.any(String),
        expect.objectContaining({
          body: { storage: { value: '<p></p>', representation: 'storage' } }
        }),
        expect.any(Object)
      );
    });

    it('should create a page under a Server-style display URL', async () => {
      const searchResponse = {
        data: {
          results: [{ id: '987', space: { key: 'PROJ' } }]
        }
      };
      const postResponse = {
        data: { id: '888', title: 'Child Page', space: { key: 'PROJ' }, _links: {} }
      };

      axios.get.mockResolvedValue(searchResponse);
      axios.post.mockResolvedValue(postResponse);

      const response = await mockServer.invokeTool('confluence_create_page', {
        parentPageUrl: 'https://confluence.example.com/display/PROJ/Parent+Page',
        title: 'Child Page',
        body: '<p>Hello world</p>'
      });

      expect(isValidToolResponse(response)).toBe(true);
      expect(axios.get).toHaveBeenCalledWith(
        expect.stringContaining('content/search'),
        expect.any(Object)
      );
      expect(axios.post).toHaveBeenCalledWith(
        expect.any(String),
        expect.objectContaining({ ancestors: [{ id: '987' }], space: { key: 'PROJ' } }),
        expect.any(Object)
      );
    });

    it('should return error when parent page not found via display URL', async () => {
      axios.get.mockResolvedValue({ data: { results: [] } });

      const response = await mockServer.invokeTool('confluence_create_page', {
        parentPageUrl: 'https://confluence.example.com/display/PROJ/NonexistentPage',
        title: 'Child Page'
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('No parent page found');
    });

    it('should return error for unrecognised parent URL format', async () => {
      const response = await mockServer.invokeTool('confluence_create_page', {
        parentPageUrl: 'https://confluence.example.com/some/random/path',
        title: 'Child Page'
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('Could not parse parent page ID');
    });

    it('should return error when config is missing', async () => {
      configureConfluenceTools(mockServer, null);

      const response = await mockServer.invokeTool('confluence_create_page', {
        parentPageUrl: 'https://confluence.example.com/wiki/spaces/TEAM/pages/1/Parent',
        title: 'Child'
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('Confluence config missing');
    });

    it('should handle API errors gracefully', async () => {
      axios.get.mockRejectedValue(new Error('Network error'));

      const response = await mockServer.invokeTool('confluence_create_page', {
        parentPageUrl: 'https://confluence.example.com/wiki/spaces/TEAM/pages/123/Parent',
        title: 'Child'
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('Network error');
    });

    it('should handle non-Error thrown values', async () => {
      axios.get.mockRejectedValue('raw create page error');
      const response = await mockServer.invokeTool('confluence_create_page', {
        parentPageUrl: 'https://confluence.example.com/wiki/spaces/TEAM/pages/123/Parent',
        title: 'Child'
      });
      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('raw create page error');
    });

    it('should default to an empty list when parent search response has no results field', async () => {
      axios.get.mockResolvedValue({ data: {} });

      const response = await mockServer.invokeTool('confluence_create_page', {
        parentPageUrl: 'https://confluence.example.com/display/PROJ/Parent',
        title: 'Child'
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('No parent page found');
    });
  });

  describe('confluence_read_page', () => {
    beforeEach(() => {
      configureConfluenceTools(mockServer, confluenceConfig);
    });

    it('should read page content from a Cloud-style URL', async () => {
      axios.get.mockResolvedValue({
        data: {
          id: '123456789',
          title: 'My Page',
          space: { key: 'TEAM' },
          version: { number: 3 },
          body: {
            view: { value: '<p>Hello world</p>' },
            storage: { value: '<p>Hello world</p>' },
            export_view: { value: '<p>Tab content rendered</p>' }
          },
          _links: { webui: '/wiki/spaces/TEAM/pages/123456789/My+Page' }
        }
      });

      const response = await mockServer.invokeTool('confluence_read_page', {
        pageUrl: 'https://confluence.example.com/wiki/spaces/TEAM/pages/123456789/My+Page'
      });

      expect(isValidToolResponse(response)).toBe(true);
      const content = JSON.parse(response.content[0].text);
      expect(content.id).toBe('123456789');
      expect(content.title).toBe('My Page');
      expect(content.space).toBe('TEAM');
      expect(content.version).toBe(3);
      expect(content.body.view).toBe('<p>Hello world</p>');
      expect(content.body.storage).toBe('<p>Hello world</p>');
      expect(content.body.export_view).toBe('<p>Tab content rendered</p>');

      // Should call the content endpoint directly with expand params including export_view
      expect(axios.get).toHaveBeenCalledWith(
        expect.stringContaining('/rest/api/content/123456789'),
        expect.any(Object)
      );
      expect(axios.get).toHaveBeenCalledWith(
        expect.stringContaining('body.export_view'),
        expect.any(Object)
      );
    });

    it('should read page content from a viewpage.action?pageId= URL', async () => {
      axios.get.mockResolvedValue({
        data: {
          id: '3626394117',
          title: 'Classic Server Page',
          space: { key: 'SC' },
          version: { number: 2 },
          body: {
            view: { value: '<p>Page content</p>' },
            storage: { value: '<p>Page content</p>' }
          },
          _links: { webui: '/pages/viewpage.action?pageId=3626394117' }
        }
      });

      const response = await mockServer.invokeTool('confluence_read_page', {
        pageUrl: 'https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3626394117'
      });

      expect(isValidToolResponse(response)).toBe(true);
      const content = JSON.parse(response.content[0].text);
      expect(content.id).toBe('3626394117');
      expect(content.title).toBe('Classic Server Page');
      expect(content.space).toBe('SC');
      expect(content.version).toBe(2);
      expect(content.body.view).toBe('<p>Page content</p>');

      // Should call the content endpoint directly using the query-param ID
      expect(axios.get).toHaveBeenCalledWith(
        expect.stringContaining('/rest/api/content/3626394117'),
        expect.any(Object)
      );
    });

    it('should read page content via CQL for a Server-style URL', async () => {
      // First call: CQL search to resolve ID
      const searchResponse = {
        data: {
          results: [{ id: '987654321' }]
        }
      };
      // Second call: fetch full page by ID
      const pageResponse = {
        data: {
          id: '987654321',
          title: 'Server Page',
          space: { key: 'PROJ' },
          version: { number: 1 },
          body: {
            view: { value: '<p>Content</p>' },
            storage: { value: '<p>Content</p>' }
          },
          _links: { webui: '/display/PROJ/Server+Page' }
        }
      };
      axios.get.mockResolvedValueOnce(searchResponse).mockResolvedValueOnce(pageResponse);

      const response = await mockServer.invokeTool('confluence_read_page', {
        pageUrl: 'https://confluence.example.com/display/PROJ/Server+Page'
      });

      expect(isValidToolResponse(response)).toBe(true);
      const content = JSON.parse(response.content[0].text);
      expect(content.id).toBe('987654321');
      expect(content.title).toBe('Server Page');

      // First call should be CQL search
      expect(axios.get).toHaveBeenNthCalledWith(1,
        expect.stringContaining('content/search'),
        expect.any(Object)
      );
      // Second call fetches full page
      expect(axios.get).toHaveBeenNthCalledWith(2,
        expect.stringContaining('/rest/api/content/987654321'),
        expect.any(Object)
      );
    });

    it('should return error when Server-style URL resolves to no page', async () => {
      axios.get.mockResolvedValue({ data: { results: [] } });

      const response = await mockServer.invokeTool('confluence_read_page', {
        pageUrl: 'https://confluence.example.com/display/PROJ/NonexistentPage'
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('No page found');
    });

    it('should default to an empty list when Server-style URL search response has no results field', async () => {
      axios.get.mockResolvedValue({ data: {} });

      const response = await mockServer.invokeTool('confluence_read_page', {
        pageUrl: 'https://confluence.example.com/display/PROJ/NonexistentPage'
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('No page found');
    });

    it('should return error for unrecognised URL format', async () => {
      const response = await mockServer.invokeTool('confluence_read_page', {
        pageUrl: 'https://confluence.example.com/some/random/path'
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('Could not parse page ID');
    });

    it('should use Bearer token authentication', async () => {
      axios.get.mockResolvedValue({
        data: {
          id: '1', title: 'T', space: { key: 'S' }, version: { number: 1 },
          body: { view: { value: '' }, storage: { value: '' } }, _links: {}
        }
      });

      await mockServer.invokeTool('confluence_read_page', {
        pageUrl: 'https://confluence.example.com/wiki/spaces/S/pages/1/T'
      });

      expect(axios.get).toHaveBeenCalledWith(
        expect.any(String),
        expect.objectContaining({
          headers: expect.objectContaining({ Authorization: 'Bearer test-bearer-token' })
        })
      );
    });

    it('should return error when config is missing', async () => {
      configureConfluenceTools(mockServer, null);

      const response = await mockServer.invokeTool('confluence_read_page', {
        pageUrl: 'https://confluence.example.com/wiki/spaces/X/pages/1/Title'
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('Confluence config missing');
    });

    it('should handle API errors gracefully', async () => {
      axios.get.mockRejectedValue(new Error('Network timeout'));

      const response = await mockServer.invokeTool('confluence_read_page', {
        pageUrl: 'https://confluence.example.com/wiki/spaces/X/pages/123/Title'
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('Network timeout');
    });

    it('should handle non-Error thrown values', async () => {
      axios.get.mockRejectedValue('raw read page error');
      const response = await mockServer.invokeTool('confluence_read_page', {
        pageUrl: 'https://confluence.example.com/wiki/spaces/X/pages/123/Title'
      });
      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('raw read page error');
    });
  });

  describe('confluence_get_page', () => {
    beforeEach(() => {
      configureConfluenceTools(mockServer, confluenceConfig);
    });

    it('should return page content by ID including export_view', async () => {
      axios.get.mockResolvedValue({
        data: {
          id: '111222333',
          title: 'Page with Tabs',
          space: { key: 'TEAM' },
          version: { number: 2 },
          body: {
            view: { value: '<p>View HTML</p>' },
            storage: { value: '<p>Storage XML</p>' },
            export_view: { value: '<p>Export HTML with tabs</p>' }
          },
          _links: { webui: '/wiki/spaces/TEAM/pages/111222333/Page+with+Tabs' }
        }
      });

      const response = await mockServer.invokeTool('confluence_get_page', { pageId: '111222333' });

      expect(isValidToolResponse(response)).toBe(true);
      const content = JSON.parse(response.content[0].text);
      expect(content.id).toBe('111222333');
      expect(content.title).toBe('Page with Tabs');
      expect(content.space).toBe('TEAM');
      expect(content.version).toBe(2);
      expect(content.body.view).toBe('<p>View HTML</p>');
      expect(content.body.storage).toBe('<p>Storage XML</p>');
      expect(content.body.export_view).toBe('<p>Export HTML with tabs</p>');
      expect(content.url).toContain('111222333');

      expect(axios.get).toHaveBeenCalledWith(
        expect.stringContaining('/rest/api/content/111222333'),
        expect.any(Object)
      );
      expect(axios.get).toHaveBeenCalledWith(
        expect.stringContaining('body.export_view'),
        expect.any(Object)
      );
    });

    it('should return error when config is missing', async () => {
      configureConfluenceTools(mockServer, null);

      const response = await mockServer.invokeTool('confluence_get_page', { pageId: '123' });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('Confluence config missing');
    });

    it('should handle API errors gracefully', async () => {
      axios.get.mockRejectedValue(new Error('Not Found'));

      const response = await mockServer.invokeTool('confluence_get_page', { pageId: '999' });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('Not Found');
    });

    it('should handle non-Error thrown values', async () => {
      axios.get.mockRejectedValue('raw get page error');
      const response = await mockServer.invokeTool('confluence_get_page', { pageId: '999' });
      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('raw get page error');
    });
  });

  describe('confluence_find_page', () => {
    beforeEach(() => {
      configureConfluenceTools(mockServer, confluenceConfig);
    });

    it('should find a page by space key and title via CQL', async () => {
      axios.get.mockResolvedValue({
        data: {
          results: [{
            id: '555666777',
            title: 'Architecture Overview',
            space: { key: 'PLAT' },
            version: { number: 4 },
            _links: { webui: '/wiki/spaces/PLAT/pages/555666777/Architecture+Overview' }
          }]
        }
      });

      const response = await mockServer.invokeTool('confluence_find_page', {
        spaceKey: 'PLAT',
        title: 'Architecture Overview'
      });

      expect(isValidToolResponse(response)).toBe(true);
      const content = JSON.parse(response.content[0].text);
      expect(content.id).toBe('555666777');
      expect(content.title).toBe('Architecture Overview');
      expect(content.space).toBe('PLAT');
      expect(content.version).toBe(4);

      const url = axios.get.mock.calls[0][0];
      expect(url).toContain('content/search');
      expect(url).toContain(encodeURIComponent('type=page AND space.key="PLAT" AND title="Architecture Overview"'));
    });

    it('should return error when no page found', async () => {
      axios.get.mockResolvedValue({ data: { results: [] } });

      const response = await mockServer.invokeTool('confluence_find_page', {
        spaceKey: 'PLAT',
        title: 'Nonexistent Page'
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('No page found');
      expect(response.content[0].text).toContain('Nonexistent Page');
    });

    it('should return error when config is missing', async () => {
      configureConfluenceTools(mockServer, null);

      const response = await mockServer.invokeTool('confluence_find_page', {
        spaceKey: 'PLAT',
        title: 'Any Title'
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('Confluence config missing');
    });

    it('should default to an empty list when the response has no results field', async () => {
      axios.get.mockResolvedValue({ data: {} });

      const response = await mockServer.invokeTool('confluence_find_page', {
        spaceKey: 'PLAT',
        title: 'Any Title'
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('No page found');
    });

    it('should handle API errors gracefully', async () => {
      axios.get.mockRejectedValue(new Error('Network error'));

      const response = await mockServer.invokeTool('confluence_find_page', {
        spaceKey: 'PLAT',
        title: 'Some Page'
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('Network error');
    });

    it('should handle non-Error thrown values', async () => {
      axios.get.mockRejectedValue('raw find page error');
      const response = await mockServer.invokeTool('confluence_find_page', {
        spaceKey: 'PLAT',
        title: 'Some Page'
      });
      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('raw find page error');
    });
  });

  describe('confluence_get_page_children', () => {
    beforeEach(() => {
      configureConfluenceTools(mockServer, confluenceConfig);
    });

    it('should return child pages of a given page ID', async () => {
      axios.get.mockResolvedValue({
        data: {
          results: [
            { id: '111', title: 'Child 1', space: { key: 'TEAM' }, _links: { webui: '/wiki/spaces/TEAM/pages/111/Child+1' } },
            { id: '222', title: 'Child 2', space: { key: 'TEAM' }, _links: { webui: '/wiki/spaces/TEAM/pages/222/Child+2' } }
          ]
        }
      });

      const response = await mockServer.invokeTool('confluence_get_page_children', { pageId: '999' });

      expect(isValidToolResponse(response)).toBe(true);
      const content = JSON.parse(response.content[0].text);
      expect(content).toHaveLength(2);
      expect(content[0].id).toBe('111');
      expect(content[0].title).toBe('Child 1');
      expect(content[0].space).toBe('TEAM');
      expect(content[0].url).toContain('111');

      expect(axios.get).toHaveBeenCalledWith(
        expect.stringContaining('/rest/api/content/999/child/page'),
        expect.any(Object)
      );
    });

    it('should use default limit of 25', async () => {
      axios.get.mockResolvedValue({ data: { results: [] } });

      await mockServer.invokeTool('confluence_get_page_children', { pageId: '999' });

      expect(axios.get).toHaveBeenCalledWith(
        expect.stringContaining('limit=25'),
        expect.any(Object)
      );
    });

    it('should respect provided limit', async () => {
      axios.get.mockResolvedValue({ data: { results: [] } });

      await mockServer.invokeTool('confluence_get_page_children', { pageId: '999', limit: 10 });

      expect(axios.get).toHaveBeenCalledWith(
        expect.stringContaining('limit=10'),
        expect.any(Object)
      );
    });

    it('should return error when config is missing', async () => {
      configureConfluenceTools(mockServer, null);

      const response = await mockServer.invokeTool('confluence_get_page_children', { pageId: '999' });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('Confluence config missing');
    });

    it('should handle API errors gracefully', async () => {
      axios.get.mockRejectedValue(new Error('Not Found'));

      const response = await mockServer.invokeTool('confluence_get_page_children', { pageId: '999' });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('Not Found');
    });

    it('should handle non-Error thrown values', async () => {
      axios.get.mockRejectedValue('raw children error');
      const response = await mockServer.invokeTool('confluence_get_page_children', { pageId: '999' });
      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('raw children error');
    });

    it('should default to an empty list when the response has no results field', async () => {
      axios.get.mockResolvedValue({ data: {} });

      const response = await mockServer.invokeTool('confluence_get_page_children', { pageId: '999' });

      expect(isValidToolResponse(response)).toBe(true);
      expect(JSON.parse(response.content[0].text)).toEqual([]);
    });

    it('should return a null url when a child page has no _links', async () => {
      axios.get.mockResolvedValue({
        data: { results: [{ id: '1', title: 'Child', space: { key: 'TEAM' } }] }
      });

      const response = await mockServer.invokeTool('confluence_get_page_children', { pageId: '999' });

      expect(isValidToolResponse(response)).toBe(true);
      expect(JSON.parse(response.content[0].text)[0].url).toBeNull();
    });
  });

  describe('confluence_list_spaces', () => {
    beforeEach(() => {
      configureConfluenceTools(mockServer, confluenceConfig);
    });

    it('should return list of spaces', async () => {
      axios.get.mockResolvedValue({
        data: {
          results: [
            { key: 'TEAM', name: 'Team Space', type: 'global', _links: { webui: '/wiki/spaces/TEAM' } },
            { key: 'PLAT', name: 'Platform Space', type: 'global', _links: { webui: '/wiki/spaces/PLAT' } }
          ]
        }
      });

      const response = await mockServer.invokeTool('confluence_list_spaces', {});

      expect(isValidToolResponse(response)).toBe(true);
      const content = JSON.parse(response.content[0].text);
      expect(content).toHaveLength(2);
      expect(content[0].key).toBe('TEAM');
      expect(content[0].name).toBe('Team Space');
      expect(content[0].type).toBe('global');
      expect(content[0].url).toContain('TEAM');

      expect(axios.get).toHaveBeenCalledWith(
        expect.stringContaining('/rest/api/space'),
        expect.any(Object)
      );
    });

    it('should use default limit of 50', async () => {
      axios.get.mockResolvedValue({ data: { results: [] } });

      await mockServer.invokeTool('confluence_list_spaces', {});

      expect(axios.get).toHaveBeenCalledWith(
        expect.stringContaining('limit=50'),
        expect.any(Object)
      );
    });

    it('should respect provided limit', async () => {
      axios.get.mockResolvedValue({ data: { results: [] } });

      await mockServer.invokeTool('confluence_list_spaces', { limit: 20 });

      expect(axios.get).toHaveBeenCalledWith(
        expect.stringContaining('limit=20'),
        expect.any(Object)
      );
    });

    it('should return error when config is missing', async () => {
      configureConfluenceTools(mockServer, null);

      const response = await mockServer.invokeTool('confluence_list_spaces', {});

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('Confluence config missing');
    });

    it('should handle API errors gracefully', async () => {
      axios.get.mockRejectedValue(new Error('Service Unavailable'));

      const response = await mockServer.invokeTool('confluence_list_spaces', {});

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('Service Unavailable');
    });

    it('should handle non-Error thrown values', async () => {
      axios.get.mockRejectedValue('raw list spaces error');
      const response = await mockServer.invokeTool('confluence_list_spaces', {});
      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('raw list spaces error');
    });

    it('should default to an empty list when the response has no results field', async () => {
      axios.get.mockResolvedValue({ data: {} });

      const response = await mockServer.invokeTool('confluence_list_spaces', {});

      expect(isValidToolResponse(response)).toBe(true);
      expect(JSON.parse(response.content[0].text)).toEqual([]);
    });

    it('should return a null url when a space has no _links', async () => {
      axios.get.mockResolvedValue({
        data: { results: [{ key: 'TEAM', name: 'Team Space', type: 'global' }] }
      });

      const response = await mockServer.invokeTool('confluence_list_spaces', {});

      expect(isValidToolResponse(response)).toBe(true);
      expect(JSON.parse(response.content[0].text)[0].url).toBeNull();
    });
  });

  describe('confluence_get_space', () => {
    beforeEach(() => {
      configureConfluenceTools(mockServer, confluenceConfig);
    });

    it('should return space details', async () => {
      axios.get.mockResolvedValue({
        data: {
          key: 'PLAT',
          name: 'Platform Space',
          type: 'global',
          description: { plain: { value: 'Platform engineering space' } },
          homepage: { id: '123456' },
          _links: { webui: '/wiki/spaces/PLAT' }
        }
      });

      const response = await mockServer.invokeTool('confluence_get_space', { spaceKey: 'PLAT' });

      expect(isValidToolResponse(response)).toBe(true);
      const content = JSON.parse(response.content[0].text);
      expect(content.key).toBe('PLAT');
      expect(content.name).toBe('Platform Space');
      expect(content.type).toBe('global');
      expect(content.description).toBe('Platform engineering space');
      expect(content.homepageId).toBe('123456');
      expect(content.url).toContain('PLAT');

      expect(axios.get).toHaveBeenCalledWith(
        expect.stringContaining('/rest/api/space/PLAT'),
        expect.any(Object)
      );
    });

    it('should return error when config is missing', async () => {
      configureConfluenceTools(mockServer, null);

      const response = await mockServer.invokeTool('confluence_get_space', { spaceKey: 'PLAT' });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('Confluence config missing');
    });

    it('should handle API errors gracefully', async () => {
      axios.get.mockRejectedValue(new Error('Space not found'));

      const response = await mockServer.invokeTool('confluence_get_space', { spaceKey: 'NOTEXIST' });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('Space not found');
    });

    it('should handle non-Error thrown values', async () => {
      axios.get.mockRejectedValue('raw get space error');
      const response = await mockServer.invokeTool('confluence_get_space', { spaceKey: 'NOTEXIST' });
      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('raw get space error');
    });
  });

  describe('confluence_delete_page', () => {
    beforeEach(() => {
      configureConfluenceTools(mockServer, confluenceConfig);
    });

    it('should delete page when title matches', async () => {
      axios.get.mockResolvedValue({ data: { title: 'Old Sprint Notes', version: { number: 3 } } });
      axios.delete = vi.fn().mockResolvedValue({});

      const response = await mockServer.invokeTool('confluence_delete_page', {
        pageId: '888999',
        title: 'Old Sprint Notes'
      });

      expect(isValidToolResponse(response)).toBe(true);
      const content = JSON.parse(response.content[0].text);
      expect(content.deleted).toBe(true);
      expect(content.id).toBe('888999');
      expect(content.title).toBe('Old Sprint Notes');

      expect(axios.get).toHaveBeenCalledWith(
        expect.stringContaining('/rest/api/content/888999'),
        expect.any(Object)
      );
      expect(axios.delete).toHaveBeenCalledWith(
        expect.stringContaining('/rest/api/content/888999'),
        expect.any(Object)
      );
    });

    it('should return error when title does not match', async () => {
      axios.get.mockResolvedValue({ data: { title: 'Actual Page Title', version: { number: 1 } } });

      const response = await mockServer.invokeTool('confluence_delete_page', {
        pageId: '888999',
        title: 'Wrong Title'
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('Title mismatch');
      expect(response.content[0].text).toContain('Wrong Title');
      expect(response.content[0].text).toContain('Actual Page Title');
    });

    it('should return error when config is missing', async () => {
      configureConfluenceTools(mockServer, null);

      const response = await mockServer.invokeTool('confluence_delete_page', {
        pageId: '123',
        title: 'Some Title'
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('Confluence config missing');
    });

    it('should handle GET errors gracefully (page not found)', async () => {
      axios.get.mockRejectedValue(new Error('Request failed with status code 404'));

      const response = await mockServer.invokeTool('confluence_delete_page', {
        pageId: '999',
        title: 'Any Title'
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('404');
    });

    it('should handle non-Error thrown values', async () => {
      axios.get.mockRejectedValue('raw delete error');
      const response = await mockServer.invokeTool('confluence_delete_page', { pageId: '999', title: 'Any Title' });
      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('raw delete error');
    });
  });

  describe('confluence_add_comment', () => {
    beforeEach(() => {
      configureConfluenceTools(mockServer, confluenceConfig);
    });

    it('should post a comment and return comment id and url', async () => {
      axios.post = vi.fn().mockResolvedValue({
        data: {
          id: 'comment-123',
          _links: { webui: '/wiki/spaces/TEAM/pages/999/Page?focusedCommentId=comment-123' }
        }
      });

      const response = await mockServer.invokeTool('confluence_add_comment', {
        pageId: '999',
        body: '<p>Great work!</p>'
      });

      expect(isValidToolResponse(response)).toBe(true);
      const content = JSON.parse(response.content[0].text);
      expect(content.id).toBe('comment-123');
      expect(content.pageId).toBe('999');
      expect(content.url).toContain('comment-123');

      expect(axios.post).toHaveBeenCalledWith(
        expect.stringContaining('/rest/api/content'),
        expect.objectContaining({
          type: 'comment',
          container: { id: '999', type: 'page' },
          body: { storage: { value: '<p>Great work!</p>', representation: 'storage' } }
        }),
        expect.any(Object)
      );
    });

    it('should return error when config is missing', async () => {
      configureConfluenceTools(mockServer, null);

      const response = await mockServer.invokeTool('confluence_add_comment', {
        pageId: '999',
        body: '<p>Comment</p>'
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('Confluence config missing');
    });

    it('should handle API errors gracefully', async () => {
      axios.post = vi.fn().mockRejectedValue(new Error('Forbidden'));

      const response = await mockServer.invokeTool('confluence_add_comment', {
        pageId: '999',
        body: '<p>Comment</p>'
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('Forbidden');
    });

    it('should handle non-Error thrown values', async () => {
      axios.post = vi.fn().mockRejectedValue('raw add comment error');

      const response = await mockServer.invokeTool('confluence_add_comment', {
        pageId: '999',
        body: '<p>Comment</p>'
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('raw add comment error');
    });

    it('should return a null url when the created comment has no _links', async () => {
      axios.post = vi.fn().mockResolvedValue({ data: { id: 'comment-1' } });

      const response = await mockServer.invokeTool('confluence_add_comment', {
        pageId: '999',
        body: '<p>Comment</p>'
      });

      expect(isValidToolResponse(response)).toBe(true);
      expect(JSON.parse(response.content[0].text).url).toBeNull();
    });
  });

  describe('confluence_get_labels', () => {
    beforeEach(() => {
      configureConfluenceTools(mockServer, confluenceConfig);
    });

    it('should return labels for a page', async () => {
      axios.get.mockResolvedValue({
        data: {
          results: [
            { id: 'label-1', name: 'architecture', prefix: 'global' },
            { id: 'label-2', name: 'design', prefix: 'global' }
          ]
        }
      });

      const response = await mockServer.invokeTool('confluence_get_labels', { pageId: '444' });

      expect(isValidToolResponse(response)).toBe(true);
      const content = JSON.parse(response.content[0].text);
      expect(content).toHaveLength(2);
      expect(content[0].name).toBe('architecture');

      expect(axios.get).toHaveBeenCalledWith(
        expect.stringContaining('/rest/api/content/444/label'),
        expect.any(Object)
      );
    });

    it('should return error when config is missing', async () => {
      configureConfluenceTools(mockServer, null);

      const response = await mockServer.invokeTool('confluence_get_labels', { pageId: '444' });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('Confluence config missing');
    });

    it('should handle API errors gracefully', async () => {
      axios.get.mockRejectedValue(new Error('Not Found'));

      const response = await mockServer.invokeTool('confluence_get_labels', { pageId: '999' });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('Not Found');
    });

    it('should handle non-Error thrown values', async () => {
      axios.get.mockRejectedValue('raw get labels error');
      const response = await mockServer.invokeTool('confluence_get_labels', { pageId: '999' });
      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('raw get labels error');
    });

    it('should default to an empty list when the response has no results field', async () => {
      axios.get.mockResolvedValue({ data: {} });

      const response = await mockServer.invokeTool('confluence_get_labels', { pageId: '444' });

      expect(isValidToolResponse(response)).toBe(true);
      expect(JSON.parse(response.content[0].text)).toEqual([]);
    });
  });

  describe('confluence_add_label', () => {
    beforeEach(() => {
      configureConfluenceTools(mockServer, confluenceConfig);
    });

    it('should add a label and return updated labels list', async () => {
      axios.post = vi.fn().mockResolvedValue({
        data: {
          results: [
            { id: 'label-1', name: 'newlabel', prefix: 'global' }
          ]
        }
      });

      const response = await mockServer.invokeTool('confluence_add_label', {
        pageId: '555',
        label: 'newlabel'
      });

      expect(isValidToolResponse(response)).toBe(true);
      const content = JSON.parse(response.content[0].text);
      expect(content).toHaveLength(1);
      expect(content[0].name).toBe('newlabel');

      expect(axios.post).toHaveBeenCalledWith(
        expect.stringContaining('/rest/api/content/555/label'),
        [{ prefix: 'global', name: 'newlabel' }],
        expect.any(Object)
      );
    });

    it('should return error when config is missing', async () => {
      configureConfluenceTools(mockServer, null);

      const response = await mockServer.invokeTool('confluence_add_label', {
        pageId: '555',
        label: 'newlabel'
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('Confluence config missing');
    });

    it('should handle API errors gracefully', async () => {
      axios.post = vi.fn().mockRejectedValue(new Error('Forbidden'));

      const response = await mockServer.invokeTool('confluence_add_label', {
        pageId: '555',
        label: 'newlabel'
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('Forbidden');
    });

    it('should handle non-Error thrown values', async () => {
      axios.post = vi.fn().mockRejectedValue('raw add label error');
      const response = await mockServer.invokeTool('confluence_add_label', { pageId: '555', label: 'newlabel' });
      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('raw add label error');
    });

    it('should default to an empty list when the response has no results field', async () => {
      axios.post = vi.fn().mockResolvedValue({ data: {} });

      const response = await mockServer.invokeTool('confluence_add_label', { pageId: '555', label: 'newlabel' });

      expect(isValidToolResponse(response)).toBe(true);
      expect(JSON.parse(response.content[0].text)).toEqual([]);
    });
  });

  describe('URL and optional-field edge cases', () => {
    beforeEach(() => {
      configureConfluenceTools(mockServer, confluenceConfig);
    });

    it('confluence_get_page: should handle missing _links gracefully (url = null)', async () => {
      axios.get.mockResolvedValue({
        data: {
          id: '1',
          title: 'Page',
          space: { key: 'S' },
          version: { number: 1 },
          body: { view: { value: '' }, storage: { value: '' }, export_view: { value: '' } },
          _links: {}
        }
      });

      const response = await mockServer.invokeTool('confluence_get_page', { pageId: '1' });
      expect(isValidToolResponse(response)).toBe(true);
      const content = JSON.parse(response.content[0].text);
      expect(content.url).toBeNull();
    });

    it('confluence_find_page: should handle missing _links gracefully', async () => {
      axios.get.mockResolvedValue({
        data: {
          results: [{
            id: '1', title: 'T', space: { key: 'S' }, version: { number: 1 }, _links: {}
          }]
        }
      });

      const response = await mockServer.invokeTool('confluence_find_page', { spaceKey: 'S', title: 'T' });
      expect(isValidToolResponse(response)).toBe(true);
      const content = JSON.parse(response.content[0].text);
      expect(content.url).toBeNull();
    });

    it('confluence_get_page_children: should return empty array for page with no children', async () => {
      axios.get.mockResolvedValue({ data: { results: [] } });

      const response = await mockServer.invokeTool('confluence_get_page_children', { pageId: '1' });
      expect(isValidToolResponse(response)).toBe(true);
      const content = JSON.parse(response.content[0].text);
      expect(content).toHaveLength(0);
    });

    it('confluence_list_spaces: should return empty array when no spaces found', async () => {
      axios.get.mockResolvedValue({ data: { results: [] } });

      const response = await mockServer.invokeTool('confluence_list_spaces', {});
      expect(isValidToolResponse(response)).toBe(true);
      const content = JSON.parse(response.content[0].text);
      expect(content).toHaveLength(0);
    });

    it('confluence_get_space: should handle missing description gracefully', async () => {
      axios.get.mockResolvedValue({
        data: { key: 'S', name: 'Space', type: 'global', _links: { webui: '/wiki/spaces/S' } }
      });

      const response = await mockServer.invokeTool('confluence_get_space', { spaceKey: 'S' });
      expect(isValidToolResponse(response)).toBe(true);
      const content = JSON.parse(response.content[0].text);
      expect(content.description).toBeUndefined();
      expect(content.homepageId).toBeUndefined();
    });

    it('confluence_get_labels: should return empty array when page has no labels', async () => {
      axios.get.mockResolvedValue({ data: { results: [] } });

      const response = await mockServer.invokeTool('confluence_get_labels', { pageId: '1' });
      expect(isValidToolResponse(response)).toBe(true);
      const content = JSON.parse(response.content[0].text);
      expect(content).toHaveLength(0);
    });
  });
});
