import { describe, it, expect, beforeEach, vi } from 'vitest';
import { createMockServer, isValidToolResponse } from '@sc-node-mcp/shared-tests/helpers/mockServer';
import { createMockDriver, createMockElement } from './helpers/mockDriver.js';

vi.mock('../src/driver.js', () => ({ getActiveDriver: vi.fn() }));

const { getActiveDriver } = await import('../src/driver.js');
const { configureInteractionTools } = await import('../src/tools/interaction.js');

const LOCATOR = { using: 'id', value: 'field', index: 0 };

function driverWith(element) {
  return createMockDriver({ findElements: vi.fn().mockResolvedValue([element]) });
}

describe('interaction tools', () => {
  let server;

  beforeEach(() => {
    vi.clearAllMocks();
    server = createMockServer();
    configureInteractionTools(server);
  });

  it('element_click clicks the found element', async () => {
    const element = createMockElement();
    getActiveDriver.mockReturnValue(driverWith(element));
    const response = await server.invokeTool('element_click', { locator: LOCATOR });
    expect(element.click).toHaveBeenCalled();
    expect(isValidToolResponse(response)).toBe(true);
  });

  it('element_click returns an error when the element is not found', async () => {
    getActiveDriver.mockReturnValue(createMockDriver({ findElements: vi.fn().mockResolvedValue([]) }));
    const response = await server.invokeTool('element_click', { locator: LOCATOR });
    expect(response.isError).toBe(true);
  });

  it('element_send_keys clears then types by default', async () => {
    const element = createMockElement();
    getActiveDriver.mockReturnValue(driverWith(element));
    await server.invokeTool('element_send_keys', { locator: LOCATOR, text: 'hello' });
    expect(element.clear).toHaveBeenCalled();
    expect(element.sendKeys).toHaveBeenCalledWith('hello');
  });

  it('element_send_keys skips clearing when clearFirst is false', async () => {
    const element = createMockElement();
    getActiveDriver.mockReturnValue(driverWith(element));
    await server.invokeTool('element_send_keys', { locator: LOCATOR, text: 'hello', clearFirst: false });
    expect(element.clear).not.toHaveBeenCalled();
    expect(element.sendKeys).toHaveBeenCalledWith('hello');
  });

  it('element_clear clears the element', async () => {
    const element = createMockElement();
    getActiveDriver.mockReturnValue(driverWith(element));
    await server.invokeTool('element_clear', { locator: LOCATOR });
    expect(element.clear).toHaveBeenCalled();
  });

  it('element_get_text returns the element text', async () => {
    const element = createMockElement({ getText: vi.fn().mockResolvedValue('some text') });
    getActiveDriver.mockReturnValue(driverWith(element));
    const response = await server.invokeTool('element_get_text', { locator: LOCATOR });
    expect(response.content[0].text).toBe('some text');
  });

  it('element_get_attribute returns the attribute value', async () => {
    const element = createMockElement({ getAttribute: vi.fn().mockResolvedValue('https://example.com') });
    getActiveDriver.mockReturnValue(driverWith(element));
    const response = await server.invokeTool('element_get_attribute', { locator: LOCATOR, attribute: 'href' });
    expect(element.getAttribute).toHaveBeenCalledWith('href');
    expect(response.content[0].text).toBe('https://example.com');
  });

  it('element_get_attribute returns empty string for null attribute', async () => {
    const element = createMockElement({ getAttribute: vi.fn().mockResolvedValue(null) });
    getActiveDriver.mockReturnValue(driverWith(element));
    const response = await server.invokeTool('element_get_attribute', { locator: LOCATOR, attribute: 'missing' });
    expect(response.content[0].text).toBe('');
  });

  it('element_get_css_value returns the computed value', async () => {
    const element = createMockElement({ getCssValue: vi.fn().mockResolvedValue('rgb(0, 0, 0)') });
    getActiveDriver.mockReturnValue(driverWith(element));
    const response = await server.invokeTool('element_get_css_value', { locator: LOCATOR, property: 'color' });
    expect(element.getCssValue).toHaveBeenCalledWith('color');
    expect(response.content[0].text).toBe('rgb(0, 0, 0)');
  });

  it('element_get_rect returns location and size', async () => {
    const rect = { x: 1, y: 2, width: 3, height: 4 };
    const element = createMockElement({ getRect: vi.fn().mockResolvedValue(rect) });
    getActiveDriver.mockReturnValue(driverWith(element));
    const response = await server.invokeTool('element_get_rect', { locator: LOCATOR });
    expect(JSON.parse(response.content[0].text)).toEqual(rect);
  });

  it('element_get_state returns displayed/enabled/selected flags', async () => {
    const element = createMockElement({
      isDisplayed: vi.fn().mockResolvedValue(true),
      isEnabled: vi.fn().mockResolvedValue(false),
      isSelected: vi.fn().mockResolvedValue(true)
    });
    getActiveDriver.mockReturnValue(driverWith(element));
    const response = await server.invokeTool('element_get_state', { locator: LOCATOR });
    expect(JSON.parse(response.content[0].text)).toEqual({ displayed: true, enabled: false, selected: true });
  });

  it('element_upload_file sends the file path to the input', async () => {
    const element = createMockElement();
    getActiveDriver.mockReturnValue(driverWith(element));
    const response = await server.invokeTool('element_upload_file', { locator: LOCATOR, filePath: '/tmp/file.txt' });
    expect(element.sendKeys).toHaveBeenCalledWith('/tmp/file.txt');
    expect(response.content[0].text).toContain('/tmp/file.txt');
  });

  const REMAINING_TOOLS = [
    ['element_send_keys', { locator: LOCATOR, text: 'hi' }],
    ['element_clear', { locator: LOCATOR }],
    ['element_get_text', { locator: LOCATOR }],
    ['element_get_attribute', { locator: LOCATOR, attribute: 'href' }],
    ['element_get_css_value', { locator: LOCATOR, property: 'color' }],
    ['element_get_rect', { locator: LOCATOR }],
    ['element_get_state', { locator: LOCATOR }],
    ['element_upload_file', { locator: LOCATOR, filePath: '/tmp/f.txt' }]
  ];

  it.each(REMAINING_TOOLS)('%s returns an error when there is no active session', async (name, params) => {
    getActiveDriver.mockImplementation(() => {
      throw new Error('No active browser session. Call browser_start first.');
    });
    const response = await server.invokeTool(name, params);
    expect(response.isError).toBe(true);
  });
});
