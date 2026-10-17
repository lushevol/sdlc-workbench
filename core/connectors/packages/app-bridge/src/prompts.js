/**
 * @author Podder, Arunangshu
 * @bankId 2004018
 */

import { z } from 'zod';

/**
 * Guided MCP prompts for app-bridge. Expanded in step with the full tool set — see
 * docs/guide/APP_BRIDGE_TOOLS_GUIDE.md for the corresponding usage guide.
 */
const APP_BRIDGE_PROMPTS = {
  OPEN_AND_SCREENSHOT: {
    name: 'open-and-screenshot',
    description: 'Launch a browser, navigate to a URL, and take a screenshot of the result.',
    arguments: [
      { name: 'url', description: 'The URL to open', required: true },
      { name: 'browser', description: 'Browser to use: chrome or edge (default: chrome)', required: false }
    ]
  },
  FIND_AND_CLICK: {
    name: 'find-and-click',
    description: 'Find an element on the current page by a natural-language description and click it.',
    arguments: [{ name: 'description', description: 'What the element looks like or contains (e.g. "the Submit button")', required: true }]
  },
  FILL_A_FORM: {
    name: 'fill-a-form',
    description: 'Fill in and submit a form on the current page.',
    arguments: [{ name: 'fields', description: 'Field labels/names and the values to enter, as free text', required: true }]
  }
};

const generateAppBridgePromptMessage = (name, args) => {
  if (name === 'open-and-screenshot') {
    const browser = args.browser || 'chrome';
    return (
      `Open ${browser} and navigate to: ${args.url || '(enter the URL to open)'}\n\n` +
      `Use browser_start with:\n- browser: "${browser}"\n\n` +
      `Then use browser_navigate with:\n- url: "${args.url || '(enter the URL)'}"\n\n` +
      `Then use screenshot_capture to see the result.`
    );
  }
  if (name === 'find-and-click') {
    return (
      `Find and click the element described as: ${args.description || '(describe the element)'}\n\n` +
      `Use element_find_all with a locator guessed from the description (e.g. css/xpath/linkText) to ` +
      `identify the right element and its index, then use element_click with that locator and index.`
    );
  }
  if (name === 'fill-a-form') {
    return (
      `Fill in the form on the current page with: ${args.fields || '(describe the fields and values)'}\n\n` +
      `For each field, use element_find (or element_find_all) to locate the input, then element_send_keys ` +
      `to type the value. Use select_option for <select> dropdowns. Finish with element_click on the submit button.`
    );
  }
  return 'Unknown prompt';
};

/**
 * Register app-bridge guided prompts on the given MCP server.
 * @param {import('@modelcontextprotocol/sdk/server/mcp.js').McpServer} server
 */
export function configureAppBridgePrompts(server) {
  Object.values(APP_BRIDGE_PROMPTS).forEach((prompt) => {
    const callback = async (args) => {
      const message = generateAppBridgePromptMessage(prompt.name, args ?? {});
      return { messages: [{ role: 'user', content: { type: 'text', text: message } }] };
    };

    const argsSchema = Object.fromEntries(
      prompt.arguments.map((arg) => [
        arg.name,
        arg.required ? z.string().describe(arg.description) : z.string().optional().describe(arg.description)
      ])
    );
    server.prompt(prompt.name, prompt.description, argsSchema, callback);
  });
  console.error(`Registered ${Object.keys(APP_BRIDGE_PROMPTS).length} App Bridge prompts`);
}

export { APP_BRIDGE_PROMPTS, generateAppBridgePromptMessage };
