/**
 * @author Podder, Arunangshu
 * @bankId 2004018
 */

import { z } from 'zod';
import { ensureConsoleCaptureEnabled, getConsoleMessages, clearConsoleMessages } from '../cdp.js';
import { formatError } from '../errors.js';

/** Cap on inlined message text length in list views. */
const MAX_SUMMARY_TEXT_CHARS = 200;

/**
 * @param {Object} message
 * @returns {Object} A compact summary for list views (no stack trace).
 */
function summarizeMessage(message) {
  const text = message.text || '';
  return {
    msgid: message.msgid,
    source: message.source,
    type: message.type,
    text: text.length > MAX_SUMMARY_TEXT_CHARS ? `${text.slice(0, MAX_SUMMARY_TEXT_CHARS)}...` : text,
    timestamp: message.timestamp
  };
}

/**
 * Register console inspection tools: console_list_messages, console_get_message,
 * console_clear_messages. Capture starts lazily on first use of any of these tools (not at
 * browser_start) and accumulates into a single running buffer for the whole session — it is not
 * reset on navigation; use console_clear_messages to reset manually.
 * @param {import('@modelcontextprotocol/sdk/server/mcp.js').McpServer} server
 */
export function configureConsoleTools(server) {
  server.tool(
    'console_list_messages',
    'List console messages (console.* API calls and browser Log entries) captured for the ' +
      'current browser session since it was started (or since console_clear_messages was last ' +
      'called). Capture starts automatically the first time this tool (or console_get_message) is called.',
    {
      types: z
        .array(z.string())
        .optional()
        .describe('Only include messages of these types (e.g. "log", "warning", "error", "info", "debug"). Omit for all types.'),
      pageIdx: z.number().int().min(0).optional().default(0).describe('0-based page number to return. Omit for the first page.'),
      pageSize: z.number().int().positive().optional().describe('Maximum number of messages to return. Omit to return all matching messages.')
    },
    async ({ types, pageIdx, pageSize }) => {
      try {
        await ensureConsoleCaptureEnabled();
        let messages = getConsoleMessages();
        if (types && types.length > 0) {
          messages = messages.filter((message) => types.includes(message.type));
        }

        const page = pageIdx ?? 0;
        const size = pageSize ?? messages.length;
        const start = page * size;
        const pageItems = messages.slice(start, start + size).map(summarizeMessage);

        return {
          content: [
            { type: 'text', text: JSON.stringify({ total: messages.length, pageIdx: page, pageSize: size, messages: pageItems }, null, 2) }
          ]
        };
      } catch (error) {
        return { content: [{ type: 'text', text: formatError(error) }], isError: true };
      }
    }
  );

  server.tool(
    'console_get_message',
    'Get full detail for one captured console message by msgid, including its stack trace when ' +
      'available. Call console_list_messages first to find a msgid.',
    { msgid: z.number().int().describe('The msgid of the console message, from console_list_messages.') },
    async ({ msgid }) => {
      try {
        await ensureConsoleCaptureEnabled();
        const message = getConsoleMessages().find((entry) => entry.msgid === msgid);
        if (!message) {
          return {
            content: [
              { type: 'text', text: `No console message found with msgid ${msgid}. Call console_list_messages to see available messages.` }
            ],
            isError: true
          };
        }
        return { content: [{ type: 'text', text: JSON.stringify(message, null, 2) }] };
      } catch (error) {
        return { content: [{ type: 'text', text: formatError(error) }], isError: true };
      }
    }
  );

  server.tool('console_clear_messages', 'Manually clear the captured console messages buffer.', {}, async () => {
    try {
      clearConsoleMessages();
      return { content: [{ type: 'text', text: 'Cleared captured console messages.' }] };
    } catch (error) {
      return { content: [{ type: 'text', text: formatError(error) }], isError: true };
    }
  });
}
