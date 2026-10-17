import { describe, it, expect, beforeEach, vi } from 'vitest';
import { createMockServer, isValidToolResponse } from '@sc-node-mcp/shared-tests/helpers/mockServer';
import { createMockDriver, createMockElement } from './helpers/mockDriver.js';

vi.mock('../src/driver.js', () => ({ getActiveDriver: vi.fn() }));

const { getActiveDriver } = await import('../src/driver.js');
const { configureElementTools } = await import('../src/tools/elements.js');

function summarizableElement(overrides = {}) {
  return createMockElement({
    getTagName: vi.fn().mockResolvedValue('button'),
    getText: vi.fn().mockResolvedValue('Submit'),
    getAttribute: vi.fn().mockImplementation((name) => Promise.resolve(name === 'id' ? 'submit-btn' : null)),
    ...overrides
  });
}

describe('element tools', () => {
  let server;

  beforeEach(() => {
    vi.clearAllMocks();
    server = createMockServer();
    configureElementTools(server);
  });

  describe('element_find', () => {
    it('returns a summary of the matched element', async () => {
      const element = summarizableElement();
      const driver = createMockDriver({ findElements: vi.fn().mockResolvedValue([element]) });
      getActiveDriver.mockReturnValue(driver);

      const response = await server.invokeTool('element_find', { locator: { using: 'id', value: 'submit-btn', index: 0 } });
      const parsed = JSON.parse(response.content[0].text);

      expect(parsed.matchCount).toBe(1);
      expect(parsed.element.tag).toBe('button');
      expect(parsed.element.text).toBe('Submit');
      expect(isValidToolResponse(response)).toBe(true);
    });

    it('returns an error when no element matches', async () => {
      const driver = createMockDriver({ findElements: vi.fn().mockResolvedValue([]) });
      getActiveDriver.mockReturnValue(driver);

      const response = await server.invokeTool('element_find', { locator: { using: 'id', value: 'missing', index: 0 } });
      expect(response.isError).toBe(true);
    });

    it('returns an error when the index is out of range', async () => {
      const driver = createMockDriver({ findElements: vi.fn().mockResolvedValue([summarizableElement()]) });
      getActiveDriver.mockReturnValue(driver);

      const response = await server.invokeTool('element_find', { locator: { using: 'id', value: 'x', index: 5 } });
      expect(response.isError).toBe(true);
    });

    it('truncates long text snippets', async () => {
      const element = summarizableElement({ getText: vi.fn().mockResolvedValue('a'.repeat(300)) });
      const driver = createMockDriver({ findElements: vi.fn().mockResolvedValue([element]) });
      getActiveDriver.mockReturnValue(driver);

      const response = await server.invokeTool('element_find', { locator: { using: 'id', value: 'x', index: 0 } });
      const parsed = JSON.parse(response.content[0].text);
      expect(parsed.element.text.endsWith('...')).toBe(true);
    });

    it('returns an error when there is no active session', async () => {
      getActiveDriver.mockImplementation(() => {
        throw new Error('No active browser session. Call browser_start first.');
      });
      const response = await server.invokeTool('element_find', { locator: { using: 'id', value: 'x' } });
      expect(response.isError).toBe(true);
    });

    it('highlights the matched element by default', async () => {
      const element = summarizableElement();
      const driver = createMockDriver({ findElements: vi.fn().mockResolvedValue([element]) });
      getActiveDriver.mockReturnValue(driver);

      const response = await server.invokeTool('element_find', { locator: { using: 'id', value: 'submit-btn', index: 0 } });
      const parsed = JSON.parse(response.content[0].text);

      expect(driver.executeScript).toHaveBeenCalledWith('arguments[0].style.outline = arguments[1];', element, '2px solid red');
      expect(parsed.highlighted).toBe(true);
    });

    it('skips highlighting when highlight is false', async () => {
      const element = summarizableElement();
      const driver = createMockDriver({ findElements: vi.fn().mockResolvedValue([element]) });
      getActiveDriver.mockReturnValue(driver);

      const response = await server.invokeTool('element_find', {
        locator: { using: 'id', value: 'submit-btn', index: 0 },
        highlight: false
      });
      const parsed = JSON.parse(response.content[0].text);

      expect(driver.executeScript).not.toHaveBeenCalled();
      expect(parsed.highlighted).toBe(false);
    });

    it('still returns the element when highlighting fails', async () => {
      const element = summarizableElement();
      const driver = createMockDriver({
        findElements: vi.fn().mockResolvedValue([element]),
        executeScript: vi.fn().mockRejectedValue(new Error('script blocked'))
      });
      getActiveDriver.mockReturnValue(driver);

      const response = await server.invokeTool('element_find', { locator: { using: 'id', value: 'submit-btn', index: 0 } });
      const parsed = JSON.parse(response.content[0].text);

      expect(response.isError).toBeFalsy();
      expect(parsed.highlighted).toBe(false);
      expect(parsed.element.tag).toBe('button');
    });
  });

  describe('element_find_all', () => {
    it('returns summaries for all matches', async () => {
      const elements = [summarizableElement(), summarizableElement()];
      const driver = createMockDriver({ findElements: vi.fn().mockResolvedValue(elements) });
      getActiveDriver.mockReturnValue(driver);

      const response = await server.invokeTool('element_find_all', { locator: { using: 'css', value: 'button' } });
      const parsed = JSON.parse(response.content[0].text);
      expect(parsed.matchCount).toBe(2);
      expect(parsed.returned).toBe(2);
    });

    it('caps returned summaries at 50', async () => {
      const elements = Array.from({ length: 60 }, () => summarizableElement());
      const driver = createMockDriver({ findElements: vi.fn().mockResolvedValue(elements) });
      getActiveDriver.mockReturnValue(driver);

      const response = await server.invokeTool('element_find_all', { locator: { using: 'css', value: 'button' } });
      const parsed = JSON.parse(response.content[0].text);
      expect(parsed.matchCount).toBe(60);
      expect(parsed.returned).toBe(50);
    });

    it('returns an error on driver failure', async () => {
      const driver = createMockDriver({ findElements: vi.fn().mockRejectedValue(new Error('boom')) });
      getActiveDriver.mockReturnValue(driver);

      const response = await server.invokeTool('element_find_all', { locator: { using: 'css', value: 'button' } });
      expect(response.isError).toBe(true);
    });
  });

  describe('element_wait_for', () => {
    it('waits for present condition', async () => {
      const driver = createMockDriver({ wait: vi.fn().mockResolvedValue(summarizableElement()) });
      getActiveDriver.mockReturnValue(driver);

      const response = await server.invokeTool('element_wait_for', {
        locator: { using: 'id', value: 'x' },
        condition: 'present',
        timeoutMs: 5000
      });
      expect(driver.wait).toHaveBeenCalledTimes(1);
      expect(isValidToolResponse(response)).toBe(true);
    });

    it('waits for visible condition with two wait calls', async () => {
      const driver = createMockDriver({ wait: vi.fn().mockResolvedValue(summarizableElement()) });
      getActiveDriver.mockReturnValue(driver);

      await server.invokeTool('element_wait_for', { locator: { using: 'id', value: 'x' }, condition: 'visible' });
      expect(driver.wait).toHaveBeenCalledTimes(2);
    });

    it('waits for clickable condition with three wait calls', async () => {
      const driver = createMockDriver({ wait: vi.fn().mockResolvedValue(summarizableElement()) });
      getActiveDriver.mockReturnValue(driver);

      await server.invokeTool('element_wait_for', { locator: { using: 'id', value: 'x' }, condition: 'clickable' });
      expect(driver.wait).toHaveBeenCalledTimes(3);
    });

    it('waits for text_contains condition', async () => {
      const driver = createMockDriver({ wait: vi.fn().mockResolvedValue(summarizableElement()) });
      getActiveDriver.mockReturnValue(driver);

      const response = await server.invokeTool('element_wait_for', {
        locator: { using: 'id', value: 'x' },
        condition: 'text_contains',
        text: 'hello'
      });
      expect(driver.wait).toHaveBeenCalledTimes(2);
      expect(isValidToolResponse(response)).toBe(true);
    });

    it('errors when text_contains is missing the text parameter', async () => {
      const driver = createMockDriver({ wait: vi.fn().mockResolvedValue(summarizableElement()) });
      getActiveDriver.mockReturnValue(driver);

      const response = await server.invokeTool('element_wait_for', {
        locator: { using: 'id', value: 'x' },
        condition: 'text_contains'
      });
      expect(response.isError).toBe(true);
    });

    it('returns an error when the wait times out', async () => {
      const driver = createMockDriver({ wait: vi.fn().mockRejectedValue(new Error('Wait timed out')) });
      getActiveDriver.mockReturnValue(driver);

      const response = await server.invokeTool('element_wait_for', { locator: { using: 'id', value: 'x' }, condition: 'present' });
      expect(response.isError).toBe(true);
    });
  });
});
