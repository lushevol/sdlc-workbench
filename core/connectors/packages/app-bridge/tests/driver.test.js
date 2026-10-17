import { describe, it, expect, beforeEach, vi } from 'vitest';

const build = vi.fn();
const forBrowser = vi.fn();
const setChromeOptions = vi.fn();
const setChromeService = vi.fn();
const setEdgeOptions = vi.fn();
const setEdgeService = vi.fn();

vi.mock('selenium-webdriver', () => {
  // A real class (not vi.fn().mockImplementation()) so `new Builder()` keeps
  // working under vitest v4's stricter mock-function construct handling.
  class Builder {
    forBrowser(...args) {
      forBrowser(...args);
      return this;
    }
    setChromeOptions(...args) {
      setChromeOptions(...args);
      return this;
    }
    setChromeService(...args) {
      setChromeService(...args);
      return this;
    }
    setEdgeOptions(...args) {
      setEdgeOptions(...args);
      return this;
    }
    setEdgeService(...args) {
      setEdgeService(...args);
      return this;
    }
    build(...args) {
      return build(...args);
    }
  }
  return { Builder };
});

vi.mock('selenium-webdriver/chrome.js', () => {
  class Options {
    addArguments() {
      return this;
    }
    windowSize() {
      return this;
    }
    setChromeBinaryPath() {
      return this;
    }
  }
  class ServiceBuilder {
    constructor(path) {
      this.path = path;
    }
  }
  return { default: { Options, ServiceBuilder } };
});

vi.mock('selenium-webdriver/edge.js', () => {
  class Options {
    addArguments() {
      return this;
    }
    windowSize() {
      return this;
    }
    setEdgeChromiumBinaryPath() {
      return this;
    }
  }
  class ServiceBuilder {
    constructor(path) {
      this.path = path;
    }
  }
  return { default: { Options, ServiceBuilder } };
});

vi.mock('@sc-node-mcp/core', () => ({
  detectProxy: vi.fn().mockResolvedValue(''),
  applyProxy: vi.fn()
}));

vi.mock('../src/config.js', () => ({
  getAppBridgeConfig: vi.fn()
}));

vi.mock('../src/cdp.js', () => ({
  resetCdpState: vi.fn()
}));

const { detectProxy, applyProxy } = await import('@sc-node-mcp/core');
const { getAppBridgeConfig } = await import('../src/config.js');
const { resetCdpState } = await import('../src/cdp.js');
const {
  buildDriver,
  getActiveDriver,
  getActiveBrowser,
  hasActiveDriver,
  clearActiveDriver,
  proxyArgs,
  resolveBrowserProxy,
  resetDriverStateForTests
} = await import('../src/driver.js');

describe('driver', () => {
  beforeEach(() => {
    resetDriverStateForTests();
    vi.clearAllMocks();
    getAppBridgeConfig.mockReturnValue({
      chromedriverPath: '',
      edgedriverPath: '',
      proxy: '',
      chromeBinaryPath: '',
      edgeBinaryPath: ''
    });
    detectProxy.mockResolvedValue('');
  });

  describe('getActiveDriver / hasActiveDriver / getActiveBrowser', () => {
    it('reports no active driver initially', () => {
      expect(hasActiveDriver()).toBe(false);
      expect(getActiveBrowser()).toBeNull();
    });

    it('throws a clear error when no session is open', () => {
      expect(() => getActiveDriver()).toThrow(/No active browser session/);
    });
  });

  describe('proxyArgs', () => {
    it('returns an empty array when no proxy is set', () => {
      expect(proxyArgs('')).toEqual([]);
    });

    it('returns a --proxy-server argument when a proxy is set', () => {
      expect(proxyArgs('http://proxy:8080')).toEqual(['--proxy-server=http://proxy:8080']);
    });
  });

  describe('resolveBrowserProxy', () => {
    it('detects and applies the proxy', async () => {
      detectProxy.mockResolvedValue('http://10.239.9.190:443');
      const proxy = await resolveBrowserProxy('');
      expect(detectProxy).toHaveBeenCalledWith('');
      expect(applyProxy).toHaveBeenCalledWith('http://10.239.9.190:443');
      expect(proxy).toBe('http://10.239.9.190:443');
    });
  });

  describe('buildDriver', () => {
    it('throws for an unsupported browser', async () => {
      await expect(buildDriver({ browser: 'firefox' })).rejects.toThrow(/Unsupported browser/);
    });

    it('throws when chromedriver path is not configured', async () => {
      await expect(buildDriver({ browser: 'chrome' })).rejects.toThrow(/No driver path configured for "chrome"/);
    });

    it('throws when edgedriver path is not configured', async () => {
      await expect(buildDriver({ browser: 'edge' })).rejects.toThrow(/No driver path configured for "edge"/);
    });

    it('launches chrome and sets the active driver singleton', async () => {
      getAppBridgeConfig.mockReturnValue({
        chromedriverPath: '/path/to/chromedriver',
        edgedriverPath: '',
        proxy: '',
        chromeBinaryPath: '',
        edgeBinaryPath: ''
      });
      const fakeDriver = { quit: vi.fn().mockResolvedValue(undefined) };
      build.mockResolvedValue(fakeDriver);

      const result = await buildDriver({ browser: 'chrome' });

      expect(forBrowser).toHaveBeenCalledWith('chrome');
      expect(setChromeOptions).toHaveBeenCalled();
      expect(setChromeService).toHaveBeenCalled();
      expect(result).toBe(fakeDriver);
      expect(hasActiveDriver()).toBe(true);
      expect(getActiveBrowser()).toBe('chrome');
      expect(getActiveDriver()).toBe(fakeDriver);
    });

    it('launches edge and sets the active driver singleton', async () => {
      getAppBridgeConfig.mockReturnValue({
        chromedriverPath: '',
        edgedriverPath: '/path/to/edgedriver',
        proxy: '',
        chromeBinaryPath: '',
        edgeBinaryPath: ''
      });
      const fakeDriver = { quit: vi.fn().mockResolvedValue(undefined) };
      build.mockResolvedValue(fakeDriver);

      await buildDriver({ browser: 'edge', headless: true });

      expect(forBrowser).toHaveBeenCalledWith('MicrosoftEdge');
      expect(setEdgeOptions).toHaveBeenCalled();
      expect(setEdgeService).toHaveBeenCalled();
      expect(getActiveBrowser()).toBe('edge');
    });

    it('quits an existing session before launching a new one', async () => {
      getAppBridgeConfig.mockReturnValue({
        chromedriverPath: '/path/to/chromedriver',
        edgedriverPath: '',
        proxy: '',
        chromeBinaryPath: '',
        edgeBinaryPath: ''
      });
      const firstDriver = { quit: vi.fn().mockResolvedValue(undefined) };
      const secondDriver = { quit: vi.fn().mockResolvedValue(undefined) };
      build.mockResolvedValueOnce(firstDriver).mockResolvedValueOnce(secondDriver);

      await buildDriver({ browser: 'chrome' });
      await buildDriver({ browser: 'chrome' });

      expect(firstDriver.quit).toHaveBeenCalled();
      expect(getActiveDriver()).toBe(secondDriver);
    });

    it('applies binary path overrides when configured', async () => {
      getAppBridgeConfig.mockReturnValue({
        chromedriverPath: '/path/to/chromedriver',
        edgedriverPath: '',
        proxy: '',
        chromeBinaryPath: '/custom/chrome',
        edgeBinaryPath: ''
      });
      build.mockResolvedValue({ quit: vi.fn() });

      await buildDriver({ browser: 'chrome' });

      expect(setChromeOptions).toHaveBeenCalled();
    });

    it('applies the edge binary path override when configured', async () => {
      getAppBridgeConfig.mockReturnValue({
        chromedriverPath: '',
        edgedriverPath: '/path/to/edgedriver',
        proxy: '',
        chromeBinaryPath: '',
        edgeBinaryPath: '/custom/edge'
      });
      build.mockResolvedValue({ quit: vi.fn() });

      await buildDriver({ browser: 'edge' });

      expect(setEdgeOptions).toHaveBeenCalled();
    });
  });

  describe('clearActiveDriver', () => {
    it('is a no-op when there is no active session', async () => {
      await expect(clearActiveDriver()).resolves.toBeUndefined();
      expect(resetCdpState).not.toHaveBeenCalled();
    });

    it('quits the active driver, clears state, and tears down CDP state', async () => {
      getAppBridgeConfig.mockReturnValue({
        chromedriverPath: '/path/to/chromedriver',
        edgedriverPath: '',
        proxy: '',
        chromeBinaryPath: '',
        edgeBinaryPath: ''
      });
      const fakeDriver = { quit: vi.fn().mockResolvedValue(undefined) };
      build.mockResolvedValue(fakeDriver);
      await buildDriver({ browser: 'chrome' });

      await clearActiveDriver();

      expect(fakeDriver.quit).toHaveBeenCalled();
      expect(hasActiveDriver()).toBe(false);
      expect(getActiveBrowser()).toBeNull();
      expect(resetCdpState).toHaveBeenCalled();
    });

    it('tears down CDP state even if quit() throws', async () => {
      getAppBridgeConfig.mockReturnValue({
        chromedriverPath: '/path/to/chromedriver',
        edgedriverPath: '',
        proxy: '',
        chromeBinaryPath: '',
        edgeBinaryPath: ''
      });
      const fakeDriver = { quit: vi.fn().mockRejectedValue(new Error('quit failed')) };
      build.mockResolvedValue(fakeDriver);
      await buildDriver({ browser: 'chrome' });

      await expect(clearActiveDriver()).rejects.toThrow('quit failed');

      expect(hasActiveDriver()).toBe(false);
      expect(resetCdpState).toHaveBeenCalled();
    });
  });
});
