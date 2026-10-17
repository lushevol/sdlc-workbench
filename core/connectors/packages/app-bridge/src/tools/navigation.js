/**
 * @author Podder, Arunangshu
 * @bankId 2004018
 */

import { z } from 'zod';
import { By } from 'selenium-webdriver';
import { getActiveDriver } from '../driver.js';
import { formatError } from '../errors.js';

/** Default max wait time for browser_wait_for_text, in ms. */
const DEFAULT_WAIT_FOR_TEXT_TIMEOUT_MS = 10000;

/** Cap on returned page source length, mirroring web_fetch's truncation convention. */
const MAX_PAGE_SOURCE_CHARS = 15000;

/**
 * Register page navigation tools: browser_navigate(_back/_forward), browser_refresh,
 * browser_get_page_info, browser_get_page_source, browser_wait_for_text.
 * @param {import('@modelcontextprotocol/sdk/server/mcp.js').McpServer} server
 */
export function configureNavigationTools(server) {
  server.tool(
    'browser_navigate',
    'Navigate the active browser session to a URL.',
    { url: z.string().url().describe('The URL to navigate to') },
    async ({ url }) => {
      try {
        const driver = getActiveDriver();
        await driver.get(url);
        return { content: [{ type: 'text', text: `Navigated to ${url}` }] };
      } catch (error) {
        return { content: [{ type: 'text', text: formatError(error) }], isError: true };
      }
    }
  );

  server.tool('browser_navigate_back', 'Go back one entry in the browser history.', {}, async () => {
    try {
      const driver = getActiveDriver();
      await driver.navigate().back();
      return { content: [{ type: 'text', text: 'Navigated back.' }] };
    } catch (error) {
      return { content: [{ type: 'text', text: formatError(error) }], isError: true };
    }
  });

  server.tool('browser_navigate_forward', 'Go forward one entry in the browser history.', {}, async () => {
    try {
      const driver = getActiveDriver();
      await driver.navigate().forward();
      return { content: [{ type: 'text', text: 'Navigated forward.' }] };
    } catch (error) {
      return { content: [{ type: 'text', text: formatError(error) }], isError: true };
    }
  });

  server.tool('browser_refresh', 'Reload the current page.', {}, async () => {
    try {
      const driver = getActiveDriver();
      await driver.navigate().refresh();
      return { content: [{ type: 'text', text: 'Page refreshed.' }] };
    } catch (error) {
      return { content: [{ type: 'text', text: formatError(error) }], isError: true };
    }
  });

  server.tool('browser_get_page_info', 'Get the current URL and page title.', {}, async () => {
    try {
      const driver = getActiveDriver();
      const [url, title] = await Promise.all([driver.getCurrentUrl(), driver.getTitle()]);
      return { content: [{ type: 'text', text: JSON.stringify({ url, title }, null, 2) }] };
    } catch (error) {
      return { content: [{ type: 'text', text: formatError(error) }], isError: true };
    }
  });

  server.tool(
    'browser_get_page_source',
    `Get the full HTML source of the current page (truncated to ${MAX_PAGE_SOURCE_CHARS} characters).`,
    {},
    async () => {
      try {
        const driver = getActiveDriver();
        const source = await driver.getPageSource();
        const truncated = source.length > MAX_PAGE_SOURCE_CHARS;
        const text = truncated ? `${source.slice(0, MAX_PAGE_SOURCE_CHARS)}\n...[truncated]` : source;
        return { content: [{ type: 'text', text }] };
      } catch (error) {
        return { content: [{ type: 'text', text: formatError(error) }], isError: true };
      }
    }
  );

  server.tool(
    'browser_wait_for_text',
    'Wait for any of the given text strings to appear anywhere on the page. Unlike ' +
      'element_wait_for, this is not scoped to a single element/locator — it checks the whole ' +
      'page body text.',
    {
      text: z.array(z.string()).min(1).describe('Non-empty list of text values. Resolves as soon as any one appears on the page.'),
      timeout: z
        .number()
        .int()
        .positive()
        .optional()
        .default(DEFAULT_WAIT_FOR_TEXT_TIMEOUT_MS)
        .describe(`Maximum wait time in milliseconds (default ${DEFAULT_WAIT_FOR_TEXT_TIMEOUT_MS}).`)
    },
    async ({ text, timeout }) => {
      try {
        const driver = getActiveDriver();
        const found = await driver.wait(async () => {
          const body = await driver.findElement(By.tagName('body')).getText();
          return text.find((candidate) => body.includes(candidate)) || false;
        }, timeout);
        return { content: [{ type: 'text', text: `Found text: "${found}"` }] };
      } catch (error) {
        return { content: [{ type: 'text', text: formatError(error) }], isError: true };
      }
    }
  );
}
