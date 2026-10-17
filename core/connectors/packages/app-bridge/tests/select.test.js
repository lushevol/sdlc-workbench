import { describe, it, expect, beforeEach, vi } from 'vitest';
import { createMockServer, isValidToolResponse } from '@sc-node-mcp/shared-tests/helpers/mockServer';
import { createMockDriver, createMockElement } from './helpers/mockDriver.js';

vi.mock('../src/driver.js', () => ({ getActiveDriver: vi.fn() }));

vi.mock('selenium-webdriver', async (importOriginal) => {
  const actual = await importOriginal();
  class Select {
    constructor(element) {
      this.element = element;
    }
  }
  Select.prototype.getOptions = vi.fn().mockResolvedValue([]);
  Select.prototype.selectByValue = vi.fn().mockResolvedValue(undefined);
  Select.prototype.selectByVisibleText = vi.fn().mockResolvedValue(undefined);
  Select.prototype.selectByIndex = vi.fn().mockResolvedValue(undefined);
  Select.prototype.deselectByValue = vi.fn().mockResolvedValue(undefined);
  Select.prototype.deselectByVisibleText = vi.fn().mockResolvedValue(undefined);
  Select.prototype.deselectByIndex = vi.fn().mockResolvedValue(undefined);
  Select.prototype.deselectAll = vi.fn().mockResolvedValue(undefined);
  return { ...actual, Select };
});

const { getActiveDriver } = await import('../src/driver.js');
const { Select } = await import('selenium-webdriver');
const { configureSelectTools } = await import('../src/tools/select.js');

const LOCATOR = { using: 'id', value: 'dropdown', index: 0 };

function driverWith(element) {
  return createMockDriver({ findElements: vi.fn().mockResolvedValue([element]) });
}

describe('select tools', () => {
  let server;

  beforeEach(() => {
    vi.clearAllMocks();
    server = createMockServer();
    configureSelectTools(server);
  });

  describe('select_get_options', () => {
    it('lists options with selected flags', async () => {
      const option1 = createMockElement({
        getText: vi.fn().mockResolvedValue('One'),
        getAttribute: vi.fn().mockResolvedValue('1'),
        isSelected: vi.fn().mockResolvedValue(true)
      });
      const option2 = createMockElement({
        getText: vi.fn().mockResolvedValue('Two'),
        getAttribute: vi.fn().mockResolvedValue('2'),
        isSelected: vi.fn().mockResolvedValue(false)
      });
      Select.prototype.getOptions.mockResolvedValue([option1, option2]);
      getActiveDriver.mockReturnValue(driverWith(createMockElement()));

      const response = await server.invokeTool('select_get_options', { locator: LOCATOR });
      const parsed = JSON.parse(response.content[0].text);

      expect(parsed).toEqual([
        { text: 'One', value: '1', selected: true },
        { text: 'Two', value: '2', selected: false }
      ]);
      expect(isValidToolResponse(response)).toBe(true);
    });

    it('returns an error when the select element is not found', async () => {
      getActiveDriver.mockReturnValue(createMockDriver({ findElements: vi.fn().mockResolvedValue([]) }));
      const response = await server.invokeTool('select_get_options', { locator: LOCATOR });
      expect(response.isError).toBe(true);
    });

    it('returns an error when there is no active session', async () => {
      getActiveDriver.mockImplementation(() => {
        throw new Error('No active browser session. Call browser_start first.');
      });
      const response = await server.invokeTool('select_get_options', { locator: LOCATOR });
      expect(response.isError).toBe(true);
    });
  });

  describe('select_option', () => {
    it.each([
      ['select', 'value', 'selectByValue'],
      ['select', 'label', 'selectByVisibleText'],
      ['select', 'index', 'selectByIndex'],
      ['deselect', 'value', 'deselectByValue'],
      ['deselect', 'label', 'deselectByVisibleText'],
      ['deselect', 'index', 'deselectByIndex']
    ])('dispatches action=%s by=%s to Select.%s', async (action, by, method) => {
      getActiveDriver.mockReturnValue(driverWith(createMockElement()));
      const value = by === 'index' ? '1' : 'foo';

      const response = await server.invokeTool('select_option', { locator: LOCATOR, action, by, value });

      expect(Select.prototype[method]).toHaveBeenCalledWith(by === 'index' ? 1 : value);
      expect(isValidToolResponse(response)).toBe(true);
    });

    it('deselects all options', async () => {
      getActiveDriver.mockReturnValue(driverWith(createMockElement()));
      const response = await server.invokeTool('select_option', { locator: LOCATOR, action: 'deselect_all' });
      expect(Select.prototype.deselectAll).toHaveBeenCalled();
      expect(isValidToolResponse(response)).toBe(true);
    });

    it('errors when by/value are missing for a select action', async () => {
      getActiveDriver.mockReturnValue(driverWith(createMockElement()));
      const response = await server.invokeTool('select_option', { locator: LOCATOR, action: 'select' });
      expect(response.isError).toBe(true);
    });

    it('defaults action to select when omitted', async () => {
      getActiveDriver.mockReturnValue(driverWith(createMockElement()));
      const response = await server.invokeTool('select_option', { locator: LOCATOR, by: 'value', value: 'foo' });
      expect(Select.prototype.selectByValue).toHaveBeenCalledWith('foo');
      expect(isValidToolResponse(response)).toBe(true);
    });

    it('returns an error when there is no active session', async () => {
      getActiveDriver.mockImplementation(() => {
        throw new Error('No active browser session. Call browser_start first.');
      });
      const response = await server.invokeTool('select_option', { locator: LOCATOR, action: 'deselect_all' });
      expect(response.isError).toBe(true);
    });
  });
});
