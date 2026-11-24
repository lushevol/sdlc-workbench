import { describe, it, expect, beforeEach, vi } from 'vitest';
import { z } from 'zod';
import { createMockServer } from '@sc-node-mcp/shared-tests/helpers/mockServer';
import { createMockDriver } from './helpers/mockDriver.js';

vi.mock('../src/driver.js', () => ({ getActiveDriver: vi.fn() }));

const { getActiveDriver } = await import('../src/driver.js');
const { configureCodegenTools } = await import('../src/tools/codegen.js');

describe('codegen tools', () => {
  let server;

  beforeEach(() => {
    vi.clearAllMocks();
    server = createMockServer();
    configureCodegenTools(server);
  });

  describe('element_scan_page', () => {
    it('scans the page and returns the executeScript result', async () => {
      const scanResult = {
        matchCount: 2,
        returned: 2,
        elements: [
          { tag: 'button', text: 'Submit', id: 'submit-btn', locators: { id: 'submit-btn', css: '#submit-btn' } },
          { tag: 'a', text: 'Home', locators: { css: 'a:nth-of-type(1)', linkText: 'Home' } }
        ],
        highlightedCount: 2
      };
      const driver = createMockDriver({ executeScript: vi.fn().mockResolvedValue(scanResult) });
      getActiveDriver.mockReturnValue(driver);

      const response = await server.invokeTool('element_scan_page', {});

      expect(driver.executeScript).toHaveBeenCalledWith(expect.any(String), 50, true);
      expect(JSON.parse(response.content[0].text)).toEqual(scanResult);
    });

    it('passes a custom maxElements through to executeScript', async () => {
      const driver = createMockDriver({ executeScript: vi.fn().mockResolvedValue({ matchCount: 0, returned: 0, elements: [] }) });
      getActiveDriver.mockReturnValue(driver);

      await server.invokeTool('element_scan_page', { maxElements: 10 });

      expect(driver.executeScript).toHaveBeenCalledWith(expect.any(String), 10, true);
    });

    it('passes highlight: false through to executeScript when requested', async () => {
      const driver = createMockDriver({ executeScript: vi.fn().mockResolvedValue({ matchCount: 0, returned: 0, elements: [], highlightedCount: 0 }) });
      getActiveDriver.mockReturnValue(driver);

      await server.invokeTool('element_scan_page', { highlight: false });

      expect(driver.executeScript).toHaveBeenCalledWith(expect.any(String), 50, false);
    });

    it('returns an error when there is no active session', async () => {
      getActiveDriver.mockImplementation(() => {
        throw new Error('No active browser session. Call browser_start first.');
      });

      const response = await server.invokeTool('element_scan_page', {});

      expect(response.isError).toBe(true);
    });

    it('returns an error when executeScript rejects', async () => {
      const driver = createMockDriver({ executeScript: vi.fn().mockRejectedValue(new Error('script failed')) });
      getActiveDriver.mockReturnValue(driver);

      const response = await server.invokeTool('element_scan_page', {});

      expect(response.isError).toBe(true);
      expect(response.content[0].text).toContain('script failed');
    });

    it('validates maxElements schema (positive integer, default 50)', () => {
      const tool = server.getTool('element_scan_page');
      const schema = z.object(tool.schema);

      expect(schema.parse({}).maxElements).toBe(50);
      expect(schema.safeParse({ maxElements: 0 }).success).toBe(false);
      expect(schema.safeParse({ maxElements: -1 }).success).toBe(false);
      expect(schema.parse({ maxElements: 5 }).maxElements).toBe(5);
    });

    it('validates highlight schema (boolean, default true)', () => {
      const tool = server.getTool('element_scan_page');
      const schema = z.object(tool.schema);

      expect(schema.parse({}).highlight).toBe(true);
      expect(schema.parse({ highlight: false }).highlight).toBe(false);
      expect(schema.safeParse({ highlight: 'yes' }).success).toBe(false);
    });
  });

  describe('codegen_generate_test', () => {
    const STEPS = ['Open the login page', 'Type "admin" into the username field', 'Click the Submit button'];

    it('defaults to javascript and echoes the steps', async () => {
      const response = await server.invokeTool('codegen_generate_test', { steps: STEPS });
      const text = response.content[0].text;

      expect(text).toContain('JavaScript (selenium-webdriver)');
      expect(text).toContain('- 1. Open the login page');
      expect(text).toContain('- 2. Type "admin" into the username field');
      expect(text).toContain('- 3. Click the Submit button');
    });

    it('references the real app-bridge tool names in the workflow', async () => {
      const response = await server.invokeTool('codegen_generate_test', { steps: STEPS });
      const text = response.content[0].text;

      for (const toolName of [
        'browser_start',
        'browser_navigate',
        'element_find',
        'element_find_all',
        'element_scan_page',
        'element_click',
        'element_send_keys',
        'element_wait_for',
        'element_get_text',
        'screenshot_capture'
      ]) {
        expect(text).toContain(toolName);
      }
    });

    it('instructs the LLM to run steps for real before generating code', async () => {
      const response = await server.invokeTool('codegen_generate_test', { steps: STEPS });
      expect(response.content[0].text).toContain('DO NOT generate code from the steps alone');
    });

    it('instructs a bare script with no test-framework wrapper', async () => {
      const response = await server.invokeTool('codegen_generate_test', { steps: STEPS });
      const text = response.content[0].text;
      expect(text).toContain('Do NOT wrap the output in a test-framework structure');
      expect(text).toContain('no describe/it');
    });

    it.each([
      ['java', 'Java (Selenium)', 'ExpectedConditions.elementToBeClickable'],
      ['python', 'Python (Selenium)', 'expected_conditions'],
      ['csharp', 'C# (Selenium)', 'ExpectedConditions.ElementToBeClickable'],
      ['javascript', 'JavaScript (selenium-webdriver)', 'until.elementLocated']
    ])('includes the %s idiom example when language=%s', async (language, label, snippet) => {
      const response = await server.invokeTool('codegen_generate_test', { steps: STEPS, language });
      const text = response.content[0].text;
      expect(text).toContain(label);
      expect(text).toContain(snippet);
    });

    it('does not require an active browser session', async () => {
      getActiveDriver.mockImplementation(() => {
        throw new Error('No active browser session. Call browser_start first.');
      });
      const response = await server.invokeTool('codegen_generate_test', { steps: STEPS });
      expect(response.isError).toBeUndefined();
    });

    it('validates the steps/language schema', () => {
      const tool = server.getTool('codegen_generate_test');
      const schema = z.object(tool.schema);

      expect(schema.safeParse({ steps: [] }).success).toBe(false);
      expect(schema.safeParse({ steps: ['one step'] }).success).toBe(true);
      expect(schema.parse({ steps: ['x'] }).language).toBe('javascript');
      expect(schema.safeParse({ steps: ['x'], language: 'ruby' }).success).toBe(false);
    });
  });
});
