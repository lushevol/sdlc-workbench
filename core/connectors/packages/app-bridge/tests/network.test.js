import { describe, it, expect, beforeEach, vi } from 'vitest';
import { createMockServer, isValidToolResponse } from '@sc-node-mcp/shared-tests/helpers/mockServer';

vi.mock('../src/cdp.js', () => ({
  ensureNetworkCaptureEnabled: vi.fn().mockResolvedValue(undefined),
  getNetworkRequests: vi.fn().mockReturnValue([]),
  clearNetworkRequests: vi.fn(),
  getCdpConnection: vi.fn()
}));
vi.mock('node:fs/promises', () => ({ writeFile: vi.fn().mockResolvedValue(undefined) }));

const { ensureNetworkCaptureEnabled, getNetworkRequests, clearNetworkRequests, getCdpConnection } = await import('../src/cdp.js');
const { writeFile } = await import('node:fs/promises');
const { configureNetworkTools } = await import('../src/tools/network.js');

function makeEntry(overrides = {}) {
  return {
    reqid: 1,
    cdpRequestId: 'r1',
    url: 'https://example.com',
    method: 'GET',
    resourceType: 'Document',
    requestHeaders: { Accept: '*/*' },
    status: 200,
    statusText: 'OK',
    responseHeaders: { 'content-type': 'text/html' },
    mimeType: 'text/html',
    encodedDataLength: 100,
    failed: false,
    errorText: undefined,
    ...overrides
  };
}

describe('network tools', () => {
  let server;

  beforeEach(() => {
    vi.clearAllMocks();
    ensureNetworkCaptureEnabled.mockResolvedValue(undefined);
    getNetworkRequests.mockReturnValue([]);
    server = createMockServer();
    configureNetworkTools(server);
  });

  describe('network_list_requests', () => {
    it('lists all captured requests as summaries', async () => {
      getNetworkRequests.mockReturnValue([makeEntry(), makeEntry({ reqid: 2, resourceType: 'XHR' })]);

      const response = await server.invokeTool('network_list_requests', {});

      expect(ensureNetworkCaptureEnabled).toHaveBeenCalled();
      const parsed = JSON.parse(response.content[0].text);
      expect(parsed.total).toBe(2);
      expect(parsed.requests).toHaveLength(2);
      expect(parsed.requests[0]).not.toHaveProperty('requestHeaders');
      expect(isValidToolResponse(response)).toBe(true);
    });

    it('filters by resourceTypes', async () => {
      getNetworkRequests.mockReturnValue([makeEntry({ reqid: 1, resourceType: 'Document' }), makeEntry({ reqid: 2, resourceType: 'XHR' })]);

      const response = await server.invokeTool('network_list_requests', { resourceTypes: ['XHR'] });

      const parsed = JSON.parse(response.content[0].text);
      expect(parsed.total).toBe(1);
      expect(parsed.requests[0].reqid).toBe(2);
    });

    it('paginates with pageIdx/pageSize', async () => {
      getNetworkRequests.mockReturnValue([makeEntry({ reqid: 1 }), makeEntry({ reqid: 2 }), makeEntry({ reqid: 3 })]);

      const response = await server.invokeTool('network_list_requests', { pageIdx: 1, pageSize: 2 });

      const parsed = JSON.parse(response.content[0].text);
      expect(parsed.requests).toHaveLength(1);
      expect(parsed.requests[0].reqid).toBe(3);
    });

    it('returns an error when capture cannot be enabled', async () => {
      ensureNetworkCaptureEnabled.mockRejectedValue(new Error('No active browser session. Call browser_start first.'));

      const response = await server.invokeTool('network_list_requests', {});

      expect(response.isError).toBe(true);
    });
  });

  describe('network_get_request', () => {
    it('returns an error when the reqid is not found', async () => {
      getNetworkRequests.mockReturnValue([]);

      const response = await server.invokeTool('network_get_request', { reqid: 99 });

      expect(response.isError).toBe(true);
      expect(response.content[0].text).toContain('No network request found with reqid 99');
    });

    it('inlines request and response bodies by default', async () => {
      getNetworkRequests.mockReturnValue([makeEntry()]);
      const connection = {
        send: vi.fn((method) => {
          if (method === 'Network.getRequestPostData') return Promise.resolve({ postData: 'a=1' });
          if (method === 'Network.getResponseBody') return Promise.resolve({ body: '<html/>', base64Encoded: false });
          return Promise.resolve({});
        })
      };
      getCdpConnection.mockResolvedValue(connection);

      const response = await server.invokeTool('network_get_request', { reqid: 1 });

      const parsed = JSON.parse(response.content[0].text);
      expect(parsed.requestBody).toBe('a=1');
      expect(parsed.responseBody).toBe('<html/>');
      expect(parsed.reqid).toBe(1);
    });

    it('decodes a base64-encoded response body', async () => {
      getNetworkRequests.mockReturnValue([makeEntry()]);
      const connection = {
        send: vi.fn((method) => {
          if (method === 'Network.getRequestPostData') return Promise.reject(new Error('no post data'));
          if (method === 'Network.getResponseBody')
            return Promise.resolve({ body: Buffer.from('hello').toString('base64'), base64Encoded: true });
          return Promise.resolve({});
        })
      };
      getCdpConnection.mockResolvedValue(connection);

      const response = await server.invokeTool('network_get_request', { reqid: 1 });

      const parsed = JSON.parse(response.content[0].text);
      expect(parsed.responseBody).toBe('hello');
      expect(parsed.requestBody).toBeUndefined();
    });

    it('saves bodies to disk when file paths are given', async () => {
      getNetworkRequests.mockReturnValue([makeEntry()]);
      const connection = {
        send: vi.fn((method) => {
          if (method === 'Network.getRequestPostData') return Promise.resolve({ postData: 'a=1' });
          if (method === 'Network.getResponseBody') return Promise.resolve({ body: '<html/>', base64Encoded: false });
          return Promise.resolve({});
        })
      };
      getCdpConnection.mockResolvedValue(connection);

      const response = await server.invokeTool('network_get_request', {
        reqid: 1,
        requestFilePath: '/tmp/req.bin',
        responseFilePath: '/tmp/res.bin'
      });

      expect(writeFile).toHaveBeenCalledWith('/tmp/req.bin', 'a=1');
      expect(writeFile).toHaveBeenCalledWith('/tmp/res.bin', Buffer.from('<html/>', 'utf-8'));
      const parsed = JSON.parse(response.content[0].text);
      expect(parsed.requestBodySavedTo).toBe('/tmp/req.bin');
      expect(parsed.responseBodySavedTo).toBe('/tmp/res.bin');
      expect(parsed.requestBody).toBeUndefined();
      expect(parsed.responseBody).toBeUndefined();
    });

    it('omits body fields gracefully when neither body is available', async () => {
      getNetworkRequests.mockReturnValue([makeEntry()]);
      const connection = {
        send: vi.fn().mockRejectedValue(new Error('not available'))
      };
      getCdpConnection.mockResolvedValue(connection);

      const response = await server.invokeTool('network_get_request', { reqid: 1 });

      const parsed = JSON.parse(response.content[0].text);
      expect(parsed.requestBody).toBeUndefined();
      expect(parsed.responseBody).toBeUndefined();
      expect(response.isError).toBeUndefined();
    });
  });

  describe('network_clear_requests', () => {
    it('clears the buffer', async () => {
      const response = await server.invokeTool('network_clear_requests', {});

      expect(clearNetworkRequests).toHaveBeenCalled();
      expect(isValidToolResponse(response)).toBe(true);
    });
  });
});
