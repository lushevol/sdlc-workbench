/**
 * @author Podder, Arunangshu
 * @bankId 2004018
 */

import { z } from 'zod';
import { until } from 'selenium-webdriver';
import { getActiveDriver } from '../driver.js';
import { formatError } from '../errors.js';

/**
 * Register alert_handle: accept/dismiss/read/type into the current browser alert, confirm, or
 * prompt dialog.
 * @param {import('@modelcontextprotocol/sdk/server/mcp.js').McpServer} server
 */
export function configureAlertTools(server) {
  server.tool(
    'alert_handle',
    'Handle the current browser alert, confirm, or prompt dialog: accept, dismiss, read its text, ' +
      'or type into a prompt before accepting.',
    {
      action: z.enum(['accept', 'dismiss', 'get_text', 'send_text']).describe('Action to perform on the alert'),
      text: z.string().optional().describe('Text to type — required when action is "send_text"'),
      timeoutMs: z.number().int().positive().optional().default(5000).describe('Max time to wait for the alert, in ms (default 5000)')
    },
    async ({ action, text, timeoutMs }) => {
      try {
        const driver = getActiveDriver();
        await driver.wait(until.alertIsPresent(), timeoutMs);
        const alert = await driver.switchTo().alert();

        if (action === 'accept') {
          await alert.accept();
          return { content: [{ type: 'text', text: 'Alert accepted.' }] };
        }
        if (action === 'dismiss') {
          await alert.dismiss();
          return { content: [{ type: 'text', text: 'Alert dismissed.' }] };
        }
        if (action === 'get_text') {
          const alertText = await alert.getText();
          return { content: [{ type: 'text', text: alertText }] };
        }
        if (action === 'send_text') {
          if (!text) throw new Error('text is required when action is "send_text"');
          await alert.sendKeys(text);
          return { content: [{ type: 'text', text: `Typed text into alert: ${text}` }] };
        }
        throw new Error(`Unsupported action "${action}"`);
      } catch (error) {
        return { content: [{ type: 'text', text: formatError(error) }], isError: true };
      }
    }
  );
}
