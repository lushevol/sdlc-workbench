/**
 * @author Podder, Arunangshu
 * @bankId 2004018
 */

import { z } from 'zod';
import { writeFile } from 'node:fs/promises';
import { ensureNetworkCaptureEnabled, getNetworkRequests, clearNetworkRequests, getCdpConnection } from '../cdp.js';
import { formatError } from '../errors.js';

/** Cap on inlined request/response body length, mirroring browser_get_page_source's truncation convention. */
const MAX_BODY_CHARS = 15000;

/**
 * @param {Object} entry
 * @returns {Object} A compact summary for list views (no headers/bodies).
 */
function summarizeRequest(entry) {
  return {
    reqid: entry.reqid,
    url: entry.url,
    method: entry.method,
    resourceType: entry.resourceType,
    status: entry.status,
    statusText: entry.statusText,
    mimeType: entry.mimeType,
    encodedDataLength: entry.encodedDataLength,
    failed: entry.failed,
    errorText: entry.errorText
  };
}

/**
 * @param {string|undefined} text
 * @returns {string|undefined}
 */
function truncate(text) {
  if (!text) return text;
  return text.length > MAX_BODY_CHARS ? `${text.slice(0, MAX_BODY_CHARS)}...[truncated]` : text;
}

/**
 * Register network inspection tools: network_list_requests, network_get_request,
 * network_clear_requests. Capture starts lazily on first use of any of these tools (not at
 * browser_start) and accumulates into a single running buffer for the whole session — it is not
 * reset on navigation; use network_clear_requests to reset manually.
 * @param {import('@modelcontextprotocol/sdk/server/mcp.js').McpServer} server
 */
export function configureNetworkTools(server) {
  server.tool(
    'network_list_requests',
    'List network requests captured for the current browser session since it was started (or ' +
      'since network_clear_requests was last called). Capture starts automatically the first time ' +
      'this tool (or network_get_request) is called.',
    {
      resourceTypes: z
        .array(z.string())
        .optional()
        .describe('Only include requests of these CDP resource types (e.g. "Document", "XHR", "Fetch", "Script", "Image"). Omit for all types.'),
      pageIdx: z.number().int().min(0).optional().default(0).describe('0-based page number to return. Omit for the first page.'),
      pageSize: z.number().int().positive().optional().describe('Maximum number of requests to return. Omit to return all matching requests.')
    },
    async ({ resourceTypes, pageIdx, pageSize }) => {
      try {
        await ensureNetworkCaptureEnabled();
        let requests = getNetworkRequests();
        if (resourceTypes && resourceTypes.length > 0) {
          requests = requests.filter((request) => resourceTypes.includes(request.resourceType));
        }

        const page = pageIdx ?? 0;
        const size = pageSize ?? requests.length;
        const start = page * size;
        const pageItems = requests.slice(start, start + size).map(summarizeRequest);

        return {
          content: [
            { type: 'text', text: JSON.stringify({ total: requests.length, pageIdx: page, pageSize: size, requests: pageItems }, null, 2) }
          ]
        };
      } catch (error) {
        return { content: [{ type: 'text', text: formatError(error) }], isError: true };
      }
    }
  );

  server.tool(
    'network_get_request',
    'Get full detail for one captured network request by reqid, including request/response ' +
      'bodies (inline, or saved to disk when a file path is given). Call network_list_requests ' +
      'first to find a reqid.',
    {
      reqid: z.number().int().describe('The reqid of the network request, from network_list_requests.'),
      requestFilePath: z.string().optional().describe('Absolute path to save the request body to instead of inlining it.'),
      responseFilePath: z.string().optional().describe('Absolute path to save the response body to instead of inlining it.')
    },
    async ({ reqid, requestFilePath, responseFilePath }) => {
      try {
        await ensureNetworkCaptureEnabled();
        const entry = getNetworkRequests().find((request) => request.reqid === reqid);
        if (!entry) {
          return {
            content: [
              { type: 'text', text: `No network request found with reqid ${reqid}. Call network_list_requests to see available requests.` }
            ],
            isError: true
          };
        }

        const connection = await getCdpConnection();
        const detail = {
          reqid: entry.reqid,
          url: entry.url,
          method: entry.method,
          resourceType: entry.resourceType,
          requestHeaders: entry.requestHeaders,
          status: entry.status,
          statusText: entry.statusText,
          responseHeaders: entry.responseHeaders,
          mimeType: entry.mimeType,
          encodedDataLength: entry.encodedDataLength,
          failed: entry.failed,
          errorText: entry.errorText
        };

        try {
          const requestBody = await connection.send('Network.getRequestPostData', { requestId: entry.cdpRequestId });
          if (requestFilePath) {
            await writeFile(requestFilePath, requestBody.postData ?? '');
            detail.requestBodySavedTo = requestFilePath;
          } else {
            detail.requestBody = truncate(requestBody.postData);
          }
        } catch {
          // No request body available (e.g. a GET request) — not an error.
        }

        try {
          const responseBody = await connection.send('Network.getResponseBody', { requestId: entry.cdpRequestId });
          const decoded = responseBody.base64Encoded
            ? Buffer.from(responseBody.body, 'base64')
            : Buffer.from(responseBody.body ?? '', 'utf-8');
          if (responseFilePath) {
            await writeFile(responseFilePath, decoded);
            detail.responseBodySavedTo = responseFilePath;
          } else {
            detail.responseBody = truncate(decoded.toString('utf-8'));
          }
        } catch {
          // Response body not available (e.g. still loading, redirect, or evicted) — not an error.
        }

        return { content: [{ type: 'text', text: JSON.stringify(detail, null, 2) }] };
      } catch (error) {
        return { content: [{ type: 'text', text: formatError(error) }], isError: true };
      }
    }
  );

  server.tool('network_clear_requests', 'Manually clear the captured network requests buffer.', {}, async () => {
    try {
      clearNetworkRequests();
      return { content: [{ type: 'text', text: 'Cleared captured network requests.' }] };
    } catch (error) {
      return { content: [{ type: 'text', text: formatError(error) }], isError: true };
    }
  });
}
