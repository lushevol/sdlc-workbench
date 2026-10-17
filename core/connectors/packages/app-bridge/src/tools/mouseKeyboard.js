/**
 * @author Podder, Arunangshu
 * @bankId 2004018
 */

import { z } from 'zod';
import { Key } from 'selenium-webdriver';
import { getActiveDriver } from '../driver.js';
import { locatorSchema, findOne } from '../locators.js';
import { formatError } from '../errors.js';

/**
 * Register mouse and keyboard Actions-API tools: mouse_hover, mouse_double_click,
 * mouse_right_click, mouse_drag_and_drop, keyboard_press_key.
 * @param {import('@modelcontextprotocol/sdk/server/mcp.js').McpServer} server
 */
export function configureMouseKeyboardTools(server) {
  server.tool(
    'mouse_hover',
    'Move the mouse over an element matching a locator (hover).',
    { locator: locatorSchema },
    async ({ locator }) => {
      try {
        const driver = getActiveDriver();
        const element = await findOne(driver, locator);
        await driver.actions().move({ origin: element }).perform();
        return { content: [{ type: 'text', text: 'Hovered over element.' }] };
      } catch (error) {
        return { content: [{ type: 'text', text: formatError(error) }], isError: true };
      }
    }
  );

  server.tool(
    'mouse_double_click',
    'Double-click an element matching a locator.',
    { locator: locatorSchema },
    async ({ locator }) => {
      try {
        const driver = getActiveDriver();
        const element = await findOne(driver, locator);
        await driver.actions().doubleClick(element).perform();
        return { content: [{ type: 'text', text: 'Double-clicked element.' }] };
      } catch (error) {
        return { content: [{ type: 'text', text: formatError(error) }], isError: true };
      }
    }
  );

  server.tool(
    'mouse_right_click',
    'Right-click (context-click) an element matching a locator.',
    { locator: locatorSchema },
    async ({ locator }) => {
      try {
        const driver = getActiveDriver();
        const element = await findOne(driver, locator);
        await driver.actions().contextClick(element).perform();
        return { content: [{ type: 'text', text: 'Right-clicked element.' }] };
      } catch (error) {
        return { content: [{ type: 'text', text: formatError(error) }], isError: true };
      }
    }
  );

  server.tool(
    'mouse_drag_and_drop',
    'Drag an element matching sourceLocator and drop it onto an element matching targetLocator.',
    { sourceLocator: locatorSchema, targetLocator: locatorSchema },
    async ({ sourceLocator, targetLocator }) => {
      try {
        const driver = getActiveDriver();
        const [source, target] = await Promise.all([findOne(driver, sourceLocator), findOne(driver, targetLocator)]);
        await driver.actions().dragAndDrop(source, target).perform();
        return { content: [{ type: 'text', text: 'Dragged and dropped element.' }] };
      } catch (error) {
        return { content: [{ type: 'text', text: formatError(error) }], isError: true };
      }
    }
  );

  server.tool(
    'keyboard_press_key',
    'Send a keyboard key to an element (or the currently focused element if no locator is given). ' +
      'Accepts a special key name (e.g. ENTER, TAB, ESCAPE, ARROW_DOWN) or literal text.',
    {
      key: z.string().describe('Special key name (e.g. ENTER, TAB, ESCAPE, ARROW_DOWN) or literal text to send'),
      locator: locatorSchema.optional().describe('If given, send the key to this element instead of the focused element')
    },
    async ({ key, locator }) => {
      try {
        const driver = getActiveDriver();
        const keyValue = Key[key] ?? key;

        if (locator) {
          const element = await findOne(driver, locator);
          await element.sendKeys(keyValue);
        } else {
          await driver.actions().sendKeys(keyValue).perform();
        }

        return { content: [{ type: 'text', text: `Sent key: ${key}` }] };
      } catch (error) {
        return { content: [{ type: 'text', text: formatError(error) }], isError: true };
      }
    }
  );
}
