/**
 * @author Podder, Arunangshu
 * @bankId 2004018
 */

import { z } from 'zod';
import { getActiveDriver } from '../driver.js';
import { formatError } from '../errors.js';

/**
 * Register script_execute: runs arbitrary JavaScript in the browser (sync or async).
 * @param {import('@modelcontextprotocol/sdk/server/mcp.js').McpServer} server
 */
export function configureScriptTools(server) {
  server.tool(
    'script_execute',
    'Execute JavaScript in the browser. Use for advanced interactions not covered by other tools ' +
      '(e.g. reading computed styles, scrolling, DOM manipulation). Arguments are accessible via ' +
      'arguments[0], arguments[1], etc. inside the script.',
    {
      script: z.string().describe('JavaScript code to execute'),
      args: z.array(z.unknown()).optional().default([]).describe('Arguments passed to the script'),
      async: z
        .boolean()
        .optional()
        .default(false)
        .describe('Run as an async script — the script must invoke the implicit final callback argument to return a result')
    },
    async ({ script, args, async: isAsync }) => {
      try {
        const driver = getActiveDriver();
        const result = isAsync ? await driver.executeAsyncScript(script, ...args) : await driver.executeScript(script, ...args);
        return { content: [{ type: 'text', text: JSON.stringify(result ?? null, null, 2) }] };
      } catch (error) {
        return { content: [{ type: 'text', text: formatError(error) }], isError: true };
      }
    }
  );
}
