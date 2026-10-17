/**
 * @author Podder, Arunangshu
 * @bankId 2004018
 */

import { z } from 'zod';
import { getActiveDriver } from '../driver.js';
import { formatError } from '../errors.js';

/**
 * Register cookie management tools: cookie_add, cookie_get, cookie_delete.
 * @param {import('@modelcontextprotocol/sdk/server/mcp.js').McpServer} server
 */
export function configureCookieTools(server) {
  server.tool(
    'cookie_add',
    "Add a cookie. The browser must already be on a page from the cookie's domain.",
    {
      name: z.string().describe('Cookie name'),
      value: z.string().describe('Cookie value'),
      domain: z.string().optional().describe('Cookie domain'),
      path: z.string().optional().describe('Cookie path'),
      secure: z.boolean().optional().describe('Secure flag'),
      httpOnly: z.boolean().optional().describe('HTTP-only flag'),
      expiry: z.number().optional().describe('Expiry as a Unix timestamp (seconds)')
    },
    async ({ name, value, domain, path, secure, httpOnly, expiry }) => {
      try {
        const driver = getActiveDriver();
        const spec = { name, value };
        if (domain !== undefined) spec.domain = domain;
        if (path !== undefined) spec.path = path;
        if (secure !== undefined) spec.secure = secure;
        if (httpOnly !== undefined) spec.httpOnly = httpOnly;
        if (expiry !== undefined) spec.expiry = expiry;
        await driver.manage().addCookie(spec);
        return { content: [{ type: 'text', text: `Added cookie: ${name}` }] };
      } catch (error) {
        return { content: [{ type: 'text', text: formatError(error) }], isError: true };
      }
    }
  );

  server.tool(
    'cookie_get',
    'Get all cookies, or a specific one by name.',
    { name: z.string().optional().describe('Cookie name. Omit for all cookies.') },
    async ({ name }) => {
      try {
        const driver = getActiveDriver();
        const result = name ? await driver.manage().getCookie(name) : await driver.manage().getCookies();
        return { content: [{ type: 'text', text: JSON.stringify(result ?? null, null, 2) }] };
      } catch (error) {
        return { content: [{ type: 'text', text: formatError(error) }], isError: true };
      }
    }
  );

  server.tool(
    'cookie_delete',
    'Delete all cookies, or a specific one by name.',
    { name: z.string().optional().describe('Cookie name. Omit to delete all.') },
    async ({ name }) => {
      try {
        const driver = getActiveDriver();
        if (name) {
          await driver.manage().deleteCookie(name);
          return { content: [{ type: 'text', text: `Deleted cookie: ${name}` }] };
        }
        await driver.manage().deleteAllCookies();
        return { content: [{ type: 'text', text: 'Deleted all cookies.' }] };
      } catch (error) {
        return { content: [{ type: 'text', text: formatError(error) }], isError: true };
      }
    }
  );
}
