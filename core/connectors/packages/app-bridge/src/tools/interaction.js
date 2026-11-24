/**
 * @author Podder, Arunangshu
 * @bankId 2004018
 */

import { z } from 'zod';
import { getActiveDriver } from '../driver.js';
import { locatorSchema, findOne } from '../locators.js';
import { formatError } from '../errors.js';

/**
 * Register single-element interaction and introspection tools: element_click, element_send_keys,
 * element_clear, element_get_text, element_get_attribute, element_get_css_value, element_get_rect,
 * element_get_state, element_upload_file.
 * @param {import('@modelcontextprotocol/sdk/server/mcp.js').McpServer} server
 */
export function configureInteractionTools(server) {
  server.tool(
    'element_click',
    'Click an element matching a locator.',
    { locator: locatorSchema },
    async ({ locator }) => {
      try {
        const driver = getActiveDriver();
        const element = await findOne(driver, locator);
        await element.click();
        return { content: [{ type: 'text', text: 'Clicked element.' }] };
      } catch (error) {
        return { content: [{ type: 'text', text: formatError(error) }], isError: true };
      }
    }
  );

  server.tool(
    'element_send_keys',
    'Type text into an element matching a locator. Clears the field first by default.',
    {
      locator: locatorSchema,
      text: z.string().describe('Text to type'),
      clearFirst: z.boolean().optional().default(true).describe('Clear the field before typing (default: true)')
    },
    async ({ locator, text, clearFirst }) => {
      try {
        const driver = getActiveDriver();
        const element = await findOne(driver, locator);
        if (clearFirst !== false) await element.clear();
        await element.sendKeys(text);
        return { content: [{ type: 'text', text: `Typed text into element.` }] };
      } catch (error) {
        return { content: [{ type: 'text', text: formatError(error) }], isError: true };
      }
    }
  );

  server.tool(
    'element_clear',
    'Clear the value of an input or textarea element matching a locator.',
    { locator: locatorSchema },
    async ({ locator }) => {
      try {
        const driver = getActiveDriver();
        const element = await findOne(driver, locator);
        await element.clear();
        return { content: [{ type: 'text', text: 'Cleared element.' }] };
      } catch (error) {
        return { content: [{ type: 'text', text: formatError(error) }], isError: true };
      }
    }
  );

  server.tool(
    'element_get_text',
    'Get the visible text of an element matching a locator.',
    { locator: locatorSchema },
    async ({ locator }) => {
      try {
        const driver = getActiveDriver();
        const element = await findOne(driver, locator);
        const text = await element.getText();
        return { content: [{ type: 'text', text }] };
      } catch (error) {
        return { content: [{ type: 'text', text: formatError(error) }], isError: true };
      }
    }
  );

  server.tool(
    'element_get_attribute',
    'Get an attribute or property value from an element matching a locator (e.g. href, value, class).',
    { locator: locatorSchema, attribute: z.string().describe('Attribute or property name to read') },
    async ({ locator, attribute }) => {
      try {
        const driver = getActiveDriver();
        const element = await findOne(driver, locator);
        const value = await element.getAttribute(attribute);
        return { content: [{ type: 'text', text: value ?? '' }] };
      } catch (error) {
        return { content: [{ type: 'text', text: formatError(error) }], isError: true };
      }
    }
  );

  server.tool(
    'element_get_css_value',
    'Get a computed CSS property value from an element matching a locator (e.g. color, display).',
    { locator: locatorSchema, property: z.string().describe('CSS property name to read') },
    async ({ locator, property }) => {
      try {
        const driver = getActiveDriver();
        const element = await findOne(driver, locator);
        const value = await element.getCssValue(property);
        return { content: [{ type: 'text', text: value }] };
      } catch (error) {
        return { content: [{ type: 'text', text: formatError(error) }], isError: true };
      }
    }
  );

  server.tool(
    'element_get_rect',
    'Get the location and size of an element matching a locator.',
    { locator: locatorSchema },
    async ({ locator }) => {
      try {
        const driver = getActiveDriver();
        const element = await findOne(driver, locator);
        const rect = await element.getRect();
        return { content: [{ type: 'text', text: JSON.stringify(rect, null, 2) }] };
      } catch (error) {
        return { content: [{ type: 'text', text: formatError(error) }], isError: true };
      }
    }
  );

  server.tool(
    'element_get_state',
    'Get whether an element matching a locator is displayed, enabled, and selected.',
    { locator: locatorSchema },
    async ({ locator }) => {
      try {
        const driver = getActiveDriver();
        const element = await findOne(driver, locator);
        const [displayed, enabled, selected] = await Promise.all([
          element.isDisplayed(),
          element.isEnabled(),
          element.isSelected()
        ]);
        return { content: [{ type: 'text', text: JSON.stringify({ displayed, enabled, selected }, null, 2) }] };
      } catch (error) {
        return { content: [{ type: 'text', text: formatError(error) }], isError: true };
      }
    }
  );

  server.tool(
    'element_upload_file',
    'Upload a file by sending its absolute path to a file input element (<input type="file">) matching a locator.',
    { locator: locatorSchema, filePath: z.string().describe('Absolute path to the file to upload') },
    async ({ locator, filePath }) => {
      try {
        const driver = getActiveDriver();
        const element = await findOne(driver, locator);
        await element.sendKeys(filePath);
        return { content: [{ type: 'text', text: `Uploaded file: ${filePath}` }] };
      } catch (error) {
        return { content: [{ type: 'text', text: formatError(error) }], isError: true };
      }
    }
  );
}
