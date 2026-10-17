import { vi } from 'vitest';

/**
 * Create a fake selenium-webdriver CdpConnection with a vi.fn() `.send()` stub and a fake
 * underlying WebSocket (`_wsConnection`) supporting `.on()`/`.off()`, so tests can simulate
 * incoming CDP push events via the returned `__emit()` helper.
 * @param {Object} [overrides]
 * @returns {Object}
 */
export function createMockCdpConnection(overrides = {}) {
  const listeners = new Set();
  const wsConnection = {
    on: vi.fn((event, listener) => {
      if (event === 'message') listeners.add(listener);
    }),
    off: vi.fn((event, listener) => {
      if (event === 'message') listeners.delete(listener);
    })
  };
  return {
    send: vi.fn().mockResolvedValue({}),
    _wsConnection: wsConnection,
    /** Test helper: simulate the browser sending a raw CDP message (object or already-stringified). */
    __emit(messageObject) {
      const raw = typeof messageObject === 'string' ? messageObject : JSON.stringify(messageObject);
      for (const listener of [...listeners]) listener(raw);
    },
    ...overrides
  };
}

/**
 * Create a fake Selenium WebElement with vi.fn() stubs for every method used across app-bridge
 * tool implementations. Pass `overrides` to customize specific method return values/behavior.
 * @param {Object} [overrides]
 * @returns {Object}
 */
export function createMockElement(overrides = {}) {
  return {
    click: vi.fn().mockResolvedValue(undefined),
    sendKeys: vi.fn().mockResolvedValue(undefined),
    clear: vi.fn().mockResolvedValue(undefined),
    submit: vi.fn().mockResolvedValue(undefined),
    getText: vi.fn().mockResolvedValue(''),
    getAttribute: vi.fn().mockResolvedValue(null),
    getCssValue: vi.fn().mockResolvedValue(''),
    getTagName: vi.fn().mockResolvedValue('div'),
    getRect: vi.fn().mockResolvedValue({ x: 0, y: 0, width: 0, height: 0 }),
    isDisplayed: vi.fn().mockResolvedValue(true),
    isEnabled: vi.fn().mockResolvedValue(true),
    isSelected: vi.fn().mockResolvedValue(false),
    takeScreenshot: vi.fn().mockResolvedValue('ZmFrZS1zY3JlZW5zaG90'),
    getShadowRoot: vi.fn(),
    ...overrides
  };
}

/**
 * Create a fake Selenium WebDriver with vi.fn() stubs for every method used across app-bridge
 * tool implementations. Pass `overrides` to customize specific method return values/behavior.
 * @param {Object} [overrides]
 * @returns {Object}
 */
export function createMockDriver(overrides = {}) {
  const navigate = {
    back: vi.fn().mockResolvedValue(undefined),
    forward: vi.fn().mockResolvedValue(undefined),
    refresh: vi.fn().mockResolvedValue(undefined),
    to: vi.fn().mockResolvedValue(undefined)
  };

  const alert = {
    accept: vi.fn().mockResolvedValue(undefined),
    dismiss: vi.fn().mockResolvedValue(undefined),
    getText: vi.fn().mockResolvedValue(''),
    sendKeys: vi.fn().mockResolvedValue(undefined)
  };

  const switchTo = {
    frame: vi.fn().mockResolvedValue(undefined),
    parentFrame: vi.fn().mockResolvedValue(undefined),
    defaultContent: vi.fn().mockResolvedValue(undefined),
    window: vi.fn().mockResolvedValue(undefined),
    newWindow: vi.fn().mockResolvedValue(undefined),
    alert: vi.fn().mockResolvedValue(alert)
  };

  const manage = {
    setTimeouts: vi.fn().mockResolvedValue(undefined),
    getCookies: vi.fn().mockResolvedValue([]),
    getCookie: vi.fn().mockResolvedValue(null),
    addCookie: vi.fn().mockResolvedValue(undefined),
    deleteCookie: vi.fn().mockResolvedValue(undefined),
    deleteAllCookies: vi.fn().mockResolvedValue(undefined),
    window: vi.fn().mockReturnValue({
      setRect: vi.fn().mockResolvedValue(undefined),
      maximize: vi.fn().mockResolvedValue(undefined)
    })
  };

  const actionsChain = {
    move: vi.fn().mockReturnThis(),
    press: vi.fn().mockReturnThis(),
    release: vi.fn().mockReturnThis(),
    click: vi.fn().mockReturnThis(),
    doubleClick: vi.fn().mockReturnThis(),
    contextClick: vi.fn().mockReturnThis(),
    dragAndDrop: vi.fn().mockReturnThis(),
    keyDown: vi.fn().mockReturnThis(),
    keyUp: vi.fn().mockReturnThis(),
    sendKeys: vi.fn().mockReturnThis(),
    pause: vi.fn().mockReturnThis(),
    perform: vi.fn().mockResolvedValue(undefined)
  };

  return {
    get: vi.fn().mockResolvedValue(undefined),
    navigate: vi.fn().mockReturnValue(navigate),
    getCurrentUrl: vi.fn().mockResolvedValue('https://example.com'),
    getTitle: vi.fn().mockResolvedValue('Example'),
    getPageSource: vi.fn().mockResolvedValue('<html></html>'),
    findElement: vi.fn(),
    findElements: vi.fn().mockResolvedValue([]),
    wait: vi.fn(),
    manage: vi.fn().mockReturnValue(manage),
    switchTo: vi.fn().mockReturnValue(switchTo),
    actions: vi.fn().mockReturnValue(actionsChain),
    executeScript: vi.fn().mockResolvedValue(null),
    executeAsyncScript: vi.fn().mockResolvedValue(null),
    takeScreenshot: vi.fn().mockResolvedValue('ZmFrZS1zY3JlZW5zaG90'),
    getWindowHandle: vi.fn().mockResolvedValue('window-1'),
    getAllWindowHandles: vi.fn().mockResolvedValue(['window-1']),
    close: vi.fn().mockResolvedValue(undefined),
    quit: vi.fn().mockResolvedValue(undefined),
    createCDPConnection: vi.fn().mockResolvedValue(createMockCdpConnection()),
    ...overrides
  };
}
