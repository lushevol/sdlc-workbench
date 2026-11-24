/**
 * @author Podder, Arunangshu
 * @bankId 2004018
 */

import { z } from 'zod';
import { until } from 'selenium-webdriver';
import { getActiveDriver } from '../driver.js';
import { locatorSchema, resolveBy, findAll, describeLocator } from '../locators.js';
import { formatError } from '../errors.js';

/** Max length of a summarized element's text snippet. */
const MAX_SUMMARY_TEXT_CHARS = 200;
/** Max number of element summaries returned by element_find_all. */
const MAX_MATCHES = 50;
/**
 * Inline CSS outline applied to the matched element by element_find when highlight is true.
 * Exported so other tools (e.g. element_scan_page) can reuse the exact same visual style.
 */
export const HIGHLIGHT_OUTLINE_STYLE = '2px solid red';

/**
 * Build a compact, JSON-friendly summary of an element for LLM consumption.
 * @param {import('selenium-webdriver').WebElement} element
 * @returns {Promise<Object>}
 */
async function summarizeElement(element) {
  const [tag, text, id, className] = await Promise.all([
    element.getTagName(),
    element.getText(),
    element.getAttribute('id'),
    element.getAttribute('class')
  ]);
  return {
    tag,
    text: text.length > MAX_SUMMARY_TEXT_CHARS ? `${text.slice(0, MAX_SUMMARY_TEXT_CHARS)}...` : text,
    id: id || undefined,
    class: className || undefined
  };
}

/**
 * Register element location tools: element_find, element_find_all, element_wait_for.
 * @param {import('@modelcontextprotocol/sdk/server/mcp.js').McpServer} server
 */
export function configureElementTools(server) {
  server.tool(
    'element_find',
    'Find one element matching a locator (supports all Selenium locator strategies plus relative ' +
      'locators). Returns a summary of the matched element and the total number of matches. By ' +
      `default also outlines the matched element in the browser (${HIGHLIGHT_OUTLINE_STYLE}) for ` +
      'visual confirmation; set highlight: false to skip this.',
    {
      locator: locatorSchema,
      highlight: z
        .boolean()
        .optional()
        .default(true)
        .describe(`Outline the matched element in the browser (${HIGHLIGHT_OUTLINE_STYLE}) for visual confirmation (default: true)`)
    },
    async ({ locator, highlight }) => {
      try {
        const driver = getActiveDriver();
        const matches = await findAll(driver, locator);
        if (matches.length === 0) {
          return {
            content: [{ type: 'text', text: `No element found for locator ${describeLocator(locator)}` }],
            isError: true
          };
        }
        const index = locator.index ?? 0;
        if (index >= matches.length) {
          return {
            content: [
              {
                type: 'text',
                text: `Locator ${describeLocator(locator)} matched ${matches.length} element(s); index ${index} is out of range`
              }
            ],
            isError: true
          };
        }
        const target = matches[index];
        let highlighted = false;
        if (highlight !== false) {
          try {
            await driver.executeScript('arguments[0].style.outline = arguments[1];', target, HIGHLIGHT_OUTLINE_STYLE);
            highlighted = true;
          } catch {
            // Best-effort: highlighting is a visual aid, never fail the find because of it.
            highlighted = false;
          }
        }
        const summary = await summarizeElement(target);
        return {
          content: [
            { type: 'text', text: JSON.stringify({ matchCount: matches.length, index, highlighted, element: summary }, null, 2) }
          ]
        };
      } catch (error) {
        return { content: [{ type: 'text', text: formatError(error) }], isError: true };
      }
    }
  );

  server.tool(
    'element_find_all',
    `Find all elements matching a locator (supports relative locators). Returns up to ${MAX_MATCHES} ` +
      'element summaries; use the returned index with other tools to target a specific match.',
    { locator: locatorSchema },
    async ({ locator }) => {
      try {
        const driver = getActiveDriver();
        const matches = await findAll(driver, locator);
        const capped = matches.slice(0, MAX_MATCHES);
        const summaries = await Promise.all(capped.map(summarizeElement));
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify({ matchCount: matches.length, returned: summaries.length, elements: summaries }, null, 2)
            }
          ]
        };
      } catch (error) {
        return { content: [{ type: 'text', text: formatError(error) }], isError: true };
      }
    }
  );

  server.tool(
    'element_wait_for',
    'Wait until an element reaches a condition: present, visible, invisible, clickable, or text_contains.',
    {
      locator: locatorSchema,
      condition: z.enum(['present', 'visible', 'invisible', 'clickable', 'text_contains']).describe('Condition to wait for'),
      text: z.string().optional().describe('Required when condition is "text_contains"'),
      timeoutMs: z.number().int().positive().optional().default(10000).describe('Max time to wait, in ms (default 10000)')
    },
    async ({ locator, condition, text, timeoutMs }) => {
      try {
        const driver = getActiveDriver();
        const by = resolveBy(locator);
        const element = await driver.wait(until.elementLocated(by), timeoutMs);

        if (condition === 'visible') {
          await driver.wait(until.elementIsVisible(element), timeoutMs);
        } else if (condition === 'invisible') {
          await driver.wait(until.elementIsNotVisible(element), timeoutMs);
        } else if (condition === 'clickable') {
          await driver.wait(until.elementIsVisible(element), timeoutMs);
          await driver.wait(until.elementIsEnabled(element), timeoutMs);
        } else if (condition === 'text_contains') {
          if (!text) throw new Error('text is required when condition is "text_contains"');
          await driver.wait(until.elementTextContains(element, text), timeoutMs);
        }
        // condition === 'present' — already satisfied by elementLocated above.

        return { content: [{ type: 'text', text: `Condition "${condition}" met for locator ${describeLocator(locator)}` }] };
      } catch (error) {
        return { content: [{ type: 'text', text: formatError(error) }], isError: true };
      }
    }
  );
}
