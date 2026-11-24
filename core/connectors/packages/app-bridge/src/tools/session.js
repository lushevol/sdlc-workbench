/**
 * @author Podder, Arunangshu
 * @bankId 2004018
 */

import { z } from 'zod';
import { buildDriver, clearActiveDriver, hasActiveDriver, getActiveDriver } from '../driver.js';
import { formatError } from '../errors.js';

/**
 * Register browser session lifecycle tools: browser_start, browser_close, browser_set_timeouts.
 * @param {import('@modelcontextprotocol/sdk/server/mcp.js').McpServer} server
 */
export function configureSessionTools(server) {
  server.tool(
    'browser_start',
    'Launch a new Chrome or Edge browser session, replacing any existing session. The chosen ' +
      "browser's driver path must already be configured (--chromedriver-path/--edgedriver-path " +
      'CLI flags or CHROMEDRIVER_PATH/EDGEDRIVER_PATH env vars). Visible (headed) by default.',
    {
      browser: z.enum(['chrome', 'edge']).describe('Which browser to launch'),
      headless: z.boolean().optional().default(false).describe('Run without a visible window (default: false)'),
      windowWidth: z.number().int().positive().optional().default(1280).describe('Initial window width in pixels'),
      windowHeight: z.number().int().positive().optional().default(800).describe('Initial window height in pixels'),
      extraArgs: z.array(z.string()).optional().default([]).describe('Additional raw Chrome/Edge command-line switches')
    },
    async ({ browser, headless, windowWidth, windowHeight, extraArgs }) => {
      try {
        await buildDriver({ browser, headless, windowWidth, windowHeight, extraArgs });
        return { content: [{ type: 'text', text: `${browser} browser session started (headless: ${headless}).` }] };
      } catch (error) {
        return { content: [{ type: 'text', text: formatError(error) }], isError: true };
      }
    }
  );

  server.tool('browser_close', 'Close the active browser session, if any.', {}, async () => {
    try {
      const wasActive = hasActiveDriver();
      await clearActiveDriver();
      return {
        content: [{ type: 'text', text: wasActive ? 'Browser session closed.' : 'No active browser session to close.' }]
      };
    } catch (error) {
      return { content: [{ type: 'text', text: formatError(error) }], isError: true };
    }
  });

  server.tool(
    'browser_set_timeouts',
    'Set implicit wait, page load, and script execution timeouts for the active browser session.',
    {
      implicitMs: z.number().int().nonnegative().optional().describe('Implicit element-find wait, in ms'),
      pageLoadMs: z.number().int().nonnegative().optional().describe('Page load timeout, in ms'),
      scriptMs: z.number().int().nonnegative().optional().describe('Script execution timeout, in ms')
    },
    async ({ implicitMs, pageLoadMs, scriptMs }) => {
      try {
        const driver = getActiveDriver();
        const timeouts = {};
        if (implicitMs !== undefined) timeouts.implicit = implicitMs;
        if (pageLoadMs !== undefined) timeouts.pageLoad = pageLoadMs;
        if (scriptMs !== undefined) timeouts.script = scriptMs;
        await driver.manage().setTimeouts(timeouts);
        return { content: [{ type: 'text', text: `Timeouts updated: ${JSON.stringify(timeouts)}` }] };
      } catch (error) {
        return { content: [{ type: 'text', text: formatError(error) }], isError: true };
      }
    }
  );
}
