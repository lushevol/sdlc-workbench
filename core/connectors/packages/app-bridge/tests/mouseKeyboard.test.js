import { describe, it, expect, beforeEach, vi } from 'vitest';
import { createMockServer, isValidToolResponse } from '@sc-node-mcp/shared-tests/helpers/mockServer';
import { createMockDriver, createMockElement } from './helpers/mockDriver.js';

vi.mock('../src/driver.js', () => ({ getActiveDriver: vi.fn() }));

const { getActiveDriver } = await import('../src/driver.js');
const { configureMouseKeyboardTools } = await import('../src/tools/mouseKeyboard.js');

const LOCATOR = { using: 'id', value: 'target', index: 0 };
const SOURCE = { using: 'id', value: 'source', index: 0 };
const TARGET = { using: 'id', value: 'target', index: 0 };

function driverWith(element) {
  return createMockDriver({ findElements: vi.fn().mockResolvedValue([element]) });
}

describe('mouse/keyboard tools', () => {
  let server;

  beforeEach(() => {
    vi.clearAllMocks();
    server = createMockServer();
    configureMouseKeyboardTools(server);
  });

  it('mouse_hover moves to the element', async () => {
    const element = createMockElement();
    const driver = driverWith(element);
    getActiveDriver.mockReturnValue(driver);

    const response = await server.invokeTool('mouse_hover', { locator: LOCATOR });

    const actions = driver.actions();
    expect(actions.move).toHaveBeenCalledWith({ origin: element });
    expect(actions.perform).toHaveBeenCalled();
    expect(isValidToolResponse(response)).toBe(true);
  });

  it('mouse_double_click double-clicks the element', async () => {
    const element = createMockElement();
    const driver = driverWith(element);
    getActiveDriver.mockReturnValue(driver);

    await server.invokeTool('mouse_double_click', { locator: LOCATOR });

    expect(driver.actions().doubleClick).toHaveBeenCalledWith(element);
  });

  it('mouse_right_click context-clicks the element', async () => {
    const element = createMockElement();
    const driver = driverWith(element);
    getActiveDriver.mockReturnValue(driver);

    await server.invokeTool('mouse_right_click', { locator: LOCATOR });

    expect(driver.actions().contextClick).toHaveBeenCalledWith(element);
  });

  it('mouse_drag_and_drop drags the source to the target', async () => {
    const source = createMockElement();
    const target = createMockElement();
    let call = 0;
    const driver = createMockDriver({
      findElements: vi.fn().mockImplementation(async () => (call++ === 0 ? [source] : [target]))
    });
    getActiveDriver.mockReturnValue(driver);

    const response = await server.invokeTool('mouse_drag_and_drop', { sourceLocator: SOURCE, targetLocator: TARGET });

    expect(driver.actions().dragAndDrop).toHaveBeenCalledWith(source, target);
    expect(isValidToolResponse(response)).toBe(true);
  });

  it('keyboard_press_key sends a special key to the active element when no locator given', async () => {
    const driver = createMockDriver();
    getActiveDriver.mockReturnValue(driver);

    const response = await server.invokeTool('keyboard_press_key', { key: 'ENTER' });

    expect(driver.actions().sendKeys).toHaveBeenCalledWith('\uE007');
    expect(isValidToolResponse(response)).toBe(true);
  });

  it('keyboard_press_key sends literal text when the key name is not a special key', async () => {
    const driver = createMockDriver();
    getActiveDriver.mockReturnValue(driver);

    await server.invokeTool('keyboard_press_key', { key: 'a' });

    expect(driver.actions().sendKeys).toHaveBeenCalledWith('a');
  });

  it('keyboard_press_key sends the key to a specific element when a locator is given', async () => {
    const element = createMockElement();
    const driver = driverWith(element);
    getActiveDriver.mockReturnValue(driver);

    await server.invokeTool('keyboard_press_key', { key: 'TAB', locator: LOCATOR });

    expect(element.sendKeys).toHaveBeenCalledWith('\uE004');
  });

  it('returns an error when there is no active session', async () => {
    getActiveDriver.mockImplementation(() => {
      throw new Error('No active browser session. Call browser_start first.');
    });
    const response = await server.invokeTool('mouse_hover', { locator: LOCATOR });
    expect(response.isError).toBe(true);
  });

  const OTHER_TOOLS = [
    ['mouse_double_click', { locator: LOCATOR }],
    ['mouse_right_click', { locator: LOCATOR }],
    ['mouse_drag_and_drop', { sourceLocator: SOURCE, targetLocator: TARGET }],
    ['keyboard_press_key', { key: 'ENTER' }]
  ];

  it.each(OTHER_TOOLS)('%s returns an error when there is no active session', async (name, params) => {
    getActiveDriver.mockImplementation(() => {
      throw new Error('No active browser session. Call browser_start first.');
    });
    const response = await server.invokeTool(name, params);
    expect(response.isError).toBe(true);
  });
});
