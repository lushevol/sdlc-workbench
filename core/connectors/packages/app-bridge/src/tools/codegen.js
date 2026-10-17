/**
 * @author Podder, Arunangshu
 * @bankId 2004018
 */

import { z } from 'zod';
import { getActiveDriver } from '../driver.js';
import { formatError } from '../errors.js';
import { HIGHLIGHT_OUTLINE_STYLE } from './elements.js';

/** Max element summaries returned by element_scan_page, mirroring element_find_all's cap. */
const DEFAULT_MAX_ELEMENTS = 50;
/** Max number of scanned elements that get outlined by element_scan_page when highlight is true. */
const MAX_HIGHLIGHT_ELEMENTS = 10;

/**
 * JavaScript injected into the page via driver.executeScript() to enumerate every interactive
 * element and suggest candidate locators for each. Runs natively in the page context — no extra
 * npm dependency needed (unlike static page-source XML parsing approaches).
 * arguments[0] = maxElements
 */
const SCAN_SCRIPT = `
  var maxElements = arguments[0];
  var shouldHighlight = arguments[1];
  var selector = 'a, button, input, select, textarea, [role="button"], [onclick], [contenteditable="true"], [tabindex]';
  var nodes = Array.prototype.slice.call(document.querySelectorAll(selector));
  var seen = new Set();

  function isVisible(el) {
    return (el.offsetParent !== null || el.getClientRects().length > 0) && !el.disabled;
  }

  function cssEscape(value) {
    return (window.CSS && window.CSS.escape) ? window.CSS.escape(value) : String(value).replace(/([^a-zA-Z0-9_-])/g, '\\\\$1');
  }

  function suggestLocators(el) {
    var locators = {};
    if (el.id) {
      locators.id = el.id;
      locators.css = '#' + cssEscape(el.id);
    }
    var name = el.getAttribute('name');
    if (name) {
      locators.name = name;
    }
    if (!locators.css) {
      var className = (el.className && typeof el.className === 'string') ? el.className.trim().split(/\\s+/)[0] : '';
      if (className) {
        locators.css = el.tagName.toLowerCase() + '.' + cssEscape(className);
      }
    }
    if (!locators.css) {
      var parent = el.parentElement;
      if (parent) {
        var siblings = Array.prototype.slice.call(parent.children).filter(function (c) { return c.tagName === el.tagName; });
        var index = siblings.indexOf(el) + 1;
        locators.css = el.tagName.toLowerCase() + ':nth-of-type(' + index + ')';
      }
    }
    if (el.tagName.toLowerCase() === 'a') {
      var linkText = (el.textContent || '').trim();
      if (linkText) {
        locators.linkText = linkText;
      }
    }
    return locators;
  }

  var matchCount = 0;
  var highlightedCount = 0;
  var elements = [];
  for (var i = 0; i < nodes.length; i++) {
    var el = nodes[i];
    if (seen.has(el) || !isVisible(el)) continue;
    seen.add(el);
    matchCount++;
    if (elements.length >= maxElements) continue;
    var text = (el.textContent || el.value || '').trim();
    if (text.length > 100) text = text.slice(0, 100) + '...';
    if (shouldHighlight && highlightedCount < ${MAX_HIGHLIGHT_ELEMENTS}) {
      try {
        el.style.outline = '${HIGHLIGHT_OUTLINE_STYLE}';
        highlightedCount++;
      } catch (e) {
        // Best-effort: highlighting is a visual aid, never fail the scan because of it.
      }
    }
    elements.push({
      tag: el.tagName.toLowerCase(),
      text: text,
      id: el.id || undefined,
      name: el.getAttribute('name') || undefined,
      class: (el.className && typeof el.className === 'string' && el.className.trim()) || undefined,
      locators: suggestLocators(el)
    });
  }

  return { matchCount: matchCount, returned: elements.length, elements: elements, highlightedCount: highlightedCount };
`;

/** One short explicit-wait + locator idiom example per supported language. */
const LANGUAGE_EXAMPLES = {
  javascript: {
    label: 'JavaScript (selenium-webdriver)',
    example: [
      "const { By, until } = require('selenium-webdriver');",
      "const element = await driver.wait(until.elementLocated(By.css('#submit')), 10000);",
      'await driver.wait(until.elementIsVisible(element), 10000);',
      'await element.click();'
    ].join('\n')
  },
  java: {
    label: 'Java (Selenium)',
    example: [
      'WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));',
      'WebElement element = wait.until(ExpectedConditions.elementToBeClickable(By.cssSelector("#submit")));',
      'element.click();'
    ].join('\n')
  },
  python: {
    label: 'Python (Selenium)',
    example: [
      'from selenium.webdriver.support.ui import WebDriverWait',
      'from selenium.webdriver.support import expected_conditions as EC',
      'from selenium.webdriver.common.by import By',
      '',
      'element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#submit")))',
      'element.click()'
    ].join('\n')
  },
  csharp: {
    label: 'C# (Selenium)',
    example: [
      'var wait = new WebDriverWait(driver, TimeSpan.FromSeconds(10));',
      'var element = wait.Until(ExpectedConditions.ElementToBeClickable(By.CssSelector("#submit")));',
      'element.Click();'
    ].join('\n')
  }
};

/**
 * Build the instructional text returned by codegen_generate_test. Pure text — no driver access,
 * no execution, no history tracking. Mirrors appium-mcp's appium_generate_tests: the calling LLM
 * is told to drive the REAL tools for each step first, then author the final code from what
 * actually happened (the conversation's own message history is the "recording").
 * @param {{ steps: string[], language: 'javascript'|'java'|'python'|'csharp' }} params
 * @returns {string}
 */
function buildInstructions({ steps, language }) {
  const { label, example } = LANGUAGE_EXAMPLES[language];

  return [
    '## Instructions',
    '- You are a Selenium WebDriver test generator.',
    '- You are given a test scenario and must generate raw Selenium code for it, including accurate locators.',
    '',
    '### Ordered workflow (use these exact MCP tool names)',
    '1. browser_start — launch Chrome or Edge if no session is active yet.',
    '2. browser_navigate — go to the starting URL if the scenario implies one.',
    '3. Discover the target element for each step — use element_find (single match) or element_find_all ' +
      '(to disambiguate multiple matches). Use element_scan_page if you need a broader snapshot of the whole ' +
      'page instead of guessing a locator.',
    "4. Interact using the tool matching each step's intent: element_click, element_send_keys, element_clear, " +
      'select_option, mouse_hover, mouse_double_click, mouse_right_click, mouse_drag_and_drop, ' +
      'keyboard_press_key, alert_handle, cookie_add / cookie_get / cookie_delete, window_manage, frame_manage.',
    '5. Use element_wait_for (condition: visible/clickable/etc.) before interacting with elements that might ' +
      'not be immediately ready, instead of a fixed sleep.',
    '6. Use element_get_text / element_get_attribute / element_get_state when a step implies an assertion or ' +
      'verification.',
    '7. Use screenshot_capture at the end of the scenario, or on failure, if useful.',
    '',
    '- DO NOT generate code from the steps alone. DO run each step with the real tools above against the live ' +
      'browser first.',
    `- Only after all steps have been performed, emit a bare, sequential ${label} Selenium script based on the ` +
      'actual tool calls and locators used in this conversation.',
    '- Do NOT wrap the output in a test-framework structure — no describe/it, no @Test/TestNG/JUnit ' +
      'annotations, no pytest fixtures. Just the ordered actions as a plain runnable script.',
    '- Use explicit waits in the generated code, never fixed sleeps.',
    '- Use the same locator strategies and values that were actually confirmed via the tools during this ' +
      'conversation — do not invent untested locators.',
    '',
    `### Explicit-wait idiom example (${label})`,
    '```',
    example,
    '```',
    '',
    'Steps:',
    ...steps.map((step, index) => `- ${index + 1}. ${step}`)
  ].join('\n');
}

/**
 * Register test-code-generation tools: element_scan_page, codegen_generate_test.
 * @param {import('@modelcontextprotocol/sdk/server/mcp.js').McpServer} server
 */
export function configureCodegenTools(server) {
  server.tool(
    'element_scan_page',
    'Scan the entire current page for interactive elements (links, buttons, inputs, selects, ' +
      'textareas, and elements with role=button/onclick/contenteditable/tabindex) and suggest ' +
      'candidate locators for each — independent of any specific locator query. Useful for ' +
      'discovering real, working locators before writing automation code. By default also outlines ' +
      `the first ${MAX_HIGHLIGHT_ELEMENTS} returned elements in the browser (${HIGHLIGHT_OUTLINE_STYLE}) ` +
      'for visual confirmation; set highlight: false to skip this. Best-effort — a failed highlight ' +
      'never fails the tool call; check the returned highlightedCount field to confirm how many were applied.',
    {
      maxElements: z
        .number()
        .int()
        .positive()
        .optional()
        .default(DEFAULT_MAX_ELEMENTS)
        .describe(`Max number of elements to return (default ${DEFAULT_MAX_ELEMENTS})`),
      highlight: z
        .boolean()
        .optional()
        .default(true)
        .describe(
          `Outline up to the first ${MAX_HIGHLIGHT_ELEMENTS} returned elements in the browser ` +
            `(${HIGHLIGHT_OUTLINE_STYLE}) for visual confirmation (default: true)`
        )
    },
    async ({ maxElements, highlight }) => {
      try {
        const driver = getActiveDriver();
        const shouldHighlight = highlight !== false;
        const result = await driver.executeScript(SCAN_SCRIPT, maxElements ?? DEFAULT_MAX_ELEMENTS, shouldHighlight);
        return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] };
      } catch (error) {
        return { content: [{ type: 'text', text: formatError(error) }], isError: true };
      }
    }
  );

  server.tool(
    'codegen_generate_test',
    'Generate raw Selenium test code (including working locators) for a natural-language test ' +
      'scenario. Returns step-by-step instructions for driving the real browser tools first, then ' +
      'writing the final code from what actually happened — this tool does not execute anything ' +
      'itself and does not track history; the conversation itself is the recording.',
    {
      steps: z.array(z.string()).min(1).describe('Natural-language steps describing the test scenario, in order'),
      language: z
        .enum(['javascript', 'java', 'python', 'csharp'])
        .optional()
        .default('javascript')
        .describe('Target Selenium language binding for the generated code (default: javascript)')
    },
    async ({ steps, language }) => {
      try {
        const text = buildInstructions({ steps, language: language || 'javascript' });
        return { content: [{ type: 'text', text }] };
      } catch (error) {
        return { content: [{ type: 'text', text: formatError(error) }], isError: true };
      }
    }
  );
}
