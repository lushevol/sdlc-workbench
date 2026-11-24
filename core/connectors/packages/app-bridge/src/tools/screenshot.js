/**
 * @author Podder, Arunangshu
 * @bankId 2004018
 */

import { z } from 'zod';
import { writeFile } from 'node:fs/promises';
import { getActiveDriver } from '../driver.js';
import { locatorSchema, findOne } from '../locators.js';
import { formatError } from '../errors.js';

/**
 * Register screenshot_capture: captures the viewport (default) or a single element (when a
 * locator is given), returning an inline MCP image content block plus optionally saving to disk.
 * @param {import('@modelcontextprotocol/sdk/server/mcp.js').McpServer} server
 */
export function configureScreenshotTools(server) {
  server.tool(
    'screenshot_capture',
    'Take a screenshot of the current viewport, or of a single element when a locator is given. ' +
      'Returns the image inline; optionally also saves it to disk.',
    {
      locator: locatorSchema.optional().describe('If given, screenshot only this element instead of the full viewport'),
      outputPath: z.string().optional().describe('Absolute file path to also save the screenshot to (PNG)')
    },
    async ({ locator, outputPath }) => {
      try {
        const driver = getActiveDriver();
        const base64 = locator ? await (await findOne(driver, locator)).takeScreenshot() : await driver.takeScreenshot();

        if (outputPath) {
          await writeFile(outputPath, Buffer.from(base64, 'base64'));
        }

        const content = [{ type: 'image', data: base64, mimeType: 'image/png' }];
        if (outputPath) {
          content.push({ type: 'text', text: `Screenshot saved to ${outputPath}` });
        }
        return { content };
      } catch (error) {
        return { content: [{ type: 'text', text: formatError(error) }], isError: true };
      }
    }
  );
}
