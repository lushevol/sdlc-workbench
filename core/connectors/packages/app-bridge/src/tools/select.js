/**
 * @author Podder, Arunangshu
 * @bankId 2004018
 */

import { z } from 'zod';
import { Select } from 'selenium-webdriver';
import { getActiveDriver } from '../driver.js';
import { locatorSchema, findOne } from '../locators.js';
import { formatError } from '../errors.js';

const SELECT_METHODS = {
  select: { value: 'selectByValue', label: 'selectByVisibleText', index: 'selectByIndex' },
  deselect: { value: 'deselectByValue', label: 'deselectByVisibleText', index: 'deselectByIndex' }
};

/**
 * Register HTML <select> dropdown tools: select_get_options, select_option.
 * @param {import('@modelcontextprotocol/sdk/server/mcp.js').McpServer} server
 */
export function configureSelectTools(server) {
  server.tool(
    'select_get_options',
    'List the options of a <select> element matching a locator, including which are currently selected.',
    { locator: locatorSchema },
    async ({ locator }) => {
      try {
        const driver = getActiveDriver();
        const element = await findOne(driver, locator);
        const select = new Select(element);
        const options = await select.getOptions();
        const summaries = await Promise.all(
          options.map(async (option) => ({
            text: await option.getText(),
            value: await option.getAttribute('value'),
            selected: await option.isSelected()
          }))
        );
        return { content: [{ type: 'text', text: JSON.stringify(summaries, null, 2) }] };
      } catch (error) {
        return { content: [{ type: 'text', text: formatError(error) }], isError: true };
      }
    }
  );

  server.tool(
    'select_option',
    'Select, deselect, or deselect-all options of a <select> element matching a locator, by value, label, or index.',
    {
      locator: locatorSchema,
      action: z.enum(['select', 'deselect', 'deselect_all']).optional().default('select').describe('Action to perform (default: select)'),
      by: z.enum(['value', 'label', 'index']).optional().describe('How to identify the option (required unless action is deselect_all)'),
      value: z
        .string()
        .optional()
        .describe('Value/label/index (as a string) identifying the option — required unless action is deselect_all')
    },
    async ({ locator, action, by, value }) => {
      try {
        const effectiveAction = action || 'select';
        const driver = getActiveDriver();
        const element = await findOne(driver, locator);
        const select = new Select(element);

        if (effectiveAction === 'deselect_all') {
          await select.deselectAll();
          return { content: [{ type: 'text', text: 'Deselected all options.' }] };
        }

        if (!by || value === undefined) {
          throw new Error('"by" and "value" are required unless action is "deselect_all"');
        }

        const methodName = SELECT_METHODS[effectiveAction][by];
        const arg = by === 'index' ? Number(value) : value;
        await select[methodName](arg);

        return {
          content: [
            { type: 'text', text: `${effectiveAction === 'select' ? 'Selected' : 'Deselected'} option by ${by}: ${value}` }
          ]
        };
      } catch (error) {
        return { content: [{ type: 'text', text: formatError(error) }], isError: true };
      }
    }
  );
}
