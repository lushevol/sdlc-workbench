/**
 * @author Podder, Arunangshu
 * @bankId 2004018
 */

import { z } from 'zod';
import { getActiveDriver } from '../driver.js';
import { locatorSchema, findOne } from '../locators.js';
import { formatError } from '../errors.js';

/**
 * Register window_manage and frame_manage — consolidated action-enum tools for the tightly
 * coupled window/tab and frame concepts.
 * @param {import('@modelcontextprotocol/sdk/server/mcp.js').McpServer} server
 */
export function configureWindowTools(server) {
  server.tool(
    'window_manage',
    'Manage browser windows/tabs: list handles, switch to one, open a new tab/window, close the ' +
      'current one, or resize/maximize the window.',
    {
      action: z.enum(['list', 'switch', 'open', 'close', 'resize']).describe('Action to perform'),
      handle: z.string().optional().describe('Window handle — required when action is "switch"'),
      type: z.enum(['tab', 'window']).optional().default('tab').describe('Used when action is "open" (default: tab)'),
      width: z.number().int().positive().optional().describe('Used when action is "resize"'),
      height: z.number().int().positive().optional().describe('Used when action is "resize"'),
      maximize: z.boolean().optional().describe('When action is "resize", maximize instead of setting width/height')
    },
    async ({ action, handle, type, width, height, maximize }) => {
      try {
        const driver = getActiveDriver();

        if (action === 'list') {
          const [handles, current] = await Promise.all([driver.getAllWindowHandles(), driver.getWindowHandle()]);
          return { content: [{ type: 'text', text: JSON.stringify({ handles, current }, null, 2) }] };
        }
        if (action === 'switch') {
          if (!handle) throw new Error('handle is required when action is "switch"');
          await driver.switchTo().window(handle);
          return { content: [{ type: 'text', text: `Switched to window: ${handle}` }] };
        }
        if (action === 'open') {
          await driver.switchTo().newWindow(type);
          const newHandle = await driver.getWindowHandle();
          return { content: [{ type: 'text', text: `Opened new ${type}: ${newHandle}` }] };
        }
        if (action === 'close') {
          await driver.close();
          return { content: [{ type: 'text', text: 'Closed current window/tab.' }] };
        }
        if (action === 'resize') {
          const win = driver.manage().window();
          if (maximize) {
            await win.maximize();
            return { content: [{ type: 'text', text: 'Window maximized.' }] };
          }
          if (!width || !height) {
            throw new Error('width and height are required when action is "resize" (unless maximize is true)');
          }
          await win.setRect({ width, height });
          return { content: [{ type: 'text', text: `Window resized to ${width}x${height}.` }] };
        }
        throw new Error(`Unsupported action "${action}"`);
      } catch (error) {
        return { content: [{ type: 'text', text: formatError(error) }], isError: true };
      }
    }
  );

  server.tool(
    'frame_manage',
    'Switch focus between frames: switch into a frame by locator or 0-based index, or reset to ' +
      'the default content or the parent frame.',
    {
      action: z.enum(['switch', 'default', 'parent']).describe('Action to perform'),
      locator: locatorSchema.optional().describe('Frame locator — used when action is "switch" (mutually exclusive with index)'),
      index: z
        .number()
        .int()
        .nonnegative()
        .optional()
        .describe('0-based frame index — used when action is "switch" (mutually exclusive with locator)')
    },
    async ({ action, locator, index }) => {
      try {
        const driver = getActiveDriver();

        if (action === 'switch') {
          if (locator) {
            const element = await findOne(driver, locator);
            await driver.switchTo().frame(element);
          } else if (index !== undefined) {
            await driver.switchTo().frame(index);
          } else {
            throw new Error('locator or index is required when action is "switch"');
          }
          return { content: [{ type: 'text', text: 'Switched to frame.' }] };
        }
        if (action === 'default') {
          await driver.switchTo().defaultContent();
          return { content: [{ type: 'text', text: 'Switched to default content.' }] };
        }
        if (action === 'parent') {
          await driver.switchTo().parentFrame();
          return { content: [{ type: 'text', text: 'Switched to parent frame.' }] };
        }
        throw new Error(`Unsupported action "${action}"`);
      } catch (error) {
        return { content: [{ type: 'text', text: formatError(error) }], isError: true };
      }
    }
  );
}
