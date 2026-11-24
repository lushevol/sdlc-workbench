/**
 * @author Podder, Arunangshu
 * @bankId 2004018
 */

import { Builder } from 'selenium-webdriver';
import chrome from 'selenium-webdriver/chrome.js';
import edge from 'selenium-webdriver/edge.js';
import { detectProxy, applyProxy } from '@sc-node-mcp/core';
import { getAppBridgeConfig } from './config.js';
import { resetCdpState } from './cdp.js';

/** Active driver singleton. null when no browser session is open. */
let _activeDriver = null;
/** @type {'chrome'|'edge'|null} */
let _activeBrowser = null;

/**
 * Get the active WebDriver session, or throw a clear error if none is open.
 * @returns {import('selenium-webdriver').WebDriver}
 */
export function getActiveDriver() {
  if (!_activeDriver) {
    throw new Error('No active browser session. Call browser_start first.');
  }
  return _activeDriver;
}

/**
 * @returns {'chrome'|'edge'|null} The browser of the active session, or null if none.
 */
export function getActiveBrowser() {
  return _activeBrowser;
}

/**
 * @returns {boolean} Whether a browser session is currently open.
 */
export function hasActiveDriver() {
  return _activeDriver !== null;
}

/**
 * Quit the active browser session (if any) and clear the singleton.
 * Safe to call when there is no active session.
 */
export async function clearActiveDriver() {
  if (_activeDriver) {
    try {
      await _activeDriver.quit();
    } finally {
      _activeDriver = null;
      _activeBrowser = null;
      resetCdpState();
    }
  }
}

/**
 * Build the --proxy-server=<url> CLI argument for Chrome/Edge, or [] if no proxy is configured.
 * Mirrors the proxyArgs() helper in packages/web/src/tools/webcrawlbrowser.js — Node's own
 * HTTPS_PROXY env var has no effect on the browser's own network stack, so the proxy must be
 * passed as a browser launch argument instead.
 * @param {string} proxy
 * @returns {string[]}
 */
export function proxyArgs(proxy) {
  return proxy ? [`--proxy-server=${proxy}`] : [];
}

/**
 * Resolve the configured proxy for browser launch through the shared proxy settings.
 * @param {string} configuredProxy
 * @returns {Promise<string>} Resolved proxy URL, or '' for direct connection.
 */
export async function resolveBrowserProxy(configuredProxy) {
  const proxy = await detectProxy(configuredProxy);
  applyProxy(proxy);
  return proxy;
}

/**
 * Launch a new Chrome or Edge browser session, replacing any existing session.
 * @param {Object} opts
 * @param {'chrome'|'edge'} opts.browser
 * @param {boolean} [opts.headless=false]
 * @param {number} [opts.windowWidth=1280]
 * @param {number} [opts.windowHeight=800]
 * @param {string[]} [opts.extraArgs=[]] Additional raw Chrome/Edge command-line switches.
 * @returns {Promise<import('selenium-webdriver').WebDriver>}
 */
export async function buildDriver({ browser, headless = false, windowWidth = 1280, windowHeight = 800, extraArgs = [] }) {
  if (browser !== 'chrome' && browser !== 'edge') {
    throw new Error(`Unsupported browser "${browser}". Use "chrome" or "edge".`);
  }

  const config = getAppBridgeConfig();
  const driverPath = browser === 'chrome' ? config.chromedriverPath : config.edgedriverPath;
  if (!driverPath) {
    const flag = browser === 'chrome' ? '--chromedriver-path' : '--edgedriver-path';
    const envVar = browser === 'chrome' ? 'CHROMEDRIVER_PATH' : 'EDGEDRIVER_PATH';
    throw new Error(
      `No driver path configured for "${browser}". Provide ${flag} as a CLI argument or set the ` +
      `${envVar} environment variable to the absolute path of the ${browser}driver executable.`
    );
  }

  const binaryPath = browser === 'chrome' ? config.chromeBinaryPath : config.edgeBinaryPath;
  const proxy = await resolveBrowserProxy(config.proxy);

  await clearActiveDriver();

  const args = ['--ignore-certificate-errors', ...proxyArgs(proxy), ...extraArgs];
  if (headless) args.unshift('--headless=new');

  let driver;
  if (browser === 'chrome') {
    const options = new chrome.Options().addArguments(...args).windowSize({ width: windowWidth, height: windowHeight });
    if (binaryPath) options.setChromeBinaryPath(binaryPath);
    const service = new chrome.ServiceBuilder(driverPath);
    driver = await new Builder().forBrowser('chrome').setChromeOptions(options).setChromeService(service).build();
  } else {
    const options = new edge.Options().addArguments(...args).windowSize({ width: windowWidth, height: windowHeight });
    if (binaryPath) options.setEdgeChromiumBinaryPath(binaryPath);
    const service = new edge.ServiceBuilder(driverPath);
    driver = await new Builder().forBrowser('MicrosoftEdge').setEdgeOptions(options).setEdgeService(service).build();
  }

  _activeDriver = driver;
  _activeBrowser = browser;
  return driver;
}

/**
 * Reset internal singleton state without quitting a real driver. Intended for use in tests only.
 */
export function resetDriverStateForTests() {
  _activeDriver = null;
  _activeBrowser = null;
}
