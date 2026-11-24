import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { getAppBridgeConfig, resetAppBridgeConfigCache } from '../src/config.js';

describe('config', () => {
  const originalArgv = process.argv;
  const originalEnv = { ...process.env };

  beforeEach(() => {
    resetAppBridgeConfigCache();
    process.argv = [...originalArgv.slice(0, 2)];
    delete process.env.CHROMEDRIVER_PATH;
    delete process.env.EDGEDRIVER_PATH;
    delete process.env.HTTPS_PROXY;
    delete process.env.CHROME_BINARY_PATH;
    delete process.env.EDGE_BINARY_PATH;
    vi.spyOn(console, 'error').mockImplementation(() => {});
  });

  afterEach(() => {
    process.argv = originalArgv;
    process.env = { ...originalEnv };
    vi.restoreAllMocks();
  });

  it('parses named CLI flags', () => {
    process.argv = [
      ...process.argv,
      '--chromedriver-path',
      '/path/to/chromedriver',
      '--edgedriver-path',
      '/path/to/edgedriver',
      '--proxy',
      'http://proxy:8080',
      '--chrome-binary-path',
      '/chrome-bin',
      '--edge-binary-path',
      '/edge-bin'
    ];

    const config = getAppBridgeConfig();

    expect(config).toEqual({
      chromedriverPath: '/path/to/chromedriver',
      edgedriverPath: '/path/to/edgedriver',
      proxy: 'http://proxy:8080',
      chromeBinaryPath: '/chrome-bin',
      edgeBinaryPath: '/edge-bin'
    });
  });

  it('falls back to environment variables when no CLI flags are given', () => {
    process.env.CHROMEDRIVER_PATH = '/env/chromedriver';
    process.env.EDGEDRIVER_PATH = '/env/edgedriver';
    process.env.HTTPS_PROXY = 'http://envproxy:8080';

    const config = getAppBridgeConfig();

    expect(config.chromedriverPath).toBe('/env/chromedriver');
    expect(config.edgedriverPath).toBe('/env/edgedriver');
    expect(config.proxy).toBe('http://envproxy:8080');
  });

  it('prioritizes CLI flags over environment variables', () => {
    process.env.CHROMEDRIVER_PATH = '/env/chromedriver';
    process.argv = [...process.argv, '--chromedriver-path', '/cli/chromedriver'];

    const config = getAppBridgeConfig();

    expect(config.chromedriverPath).toBe('/cli/chromedriver');
  });

  it('defaults every field to an empty string when nothing is configured', () => {
    const config = getAppBridgeConfig();

    expect(config).toEqual({
      chromedriverPath: '',
      edgedriverPath: '',
      proxy: '',
      chromeBinaryPath: '',
      edgeBinaryPath: ''
    });
  });

  it('memoizes the config across calls until reset', () => {
    process.argv = [...process.argv, '--chromedriver-path', '/first'];
    const first = getAppBridgeConfig();

    process.argv = [...process.argv, '--chromedriver-path', '/second'];
    const second = getAppBridgeConfig();

    expect(second).toBe(first);
    expect(second.chromedriverPath).toBe('/first');
  });

  it('re-parses after resetAppBridgeConfigCache', () => {
    process.argv = [...process.argv, '--chromedriver-path', '/first'];
    getAppBridgeConfig();

    resetAppBridgeConfigCache();
    process.argv = [...originalArgv.slice(0, 2), '--chromedriver-path', '/second'];
    const second = getAppBridgeConfig();

    expect(second.chromedriverPath).toBe('/second');
  });

  it('ignores a trailing flag with no value', () => {
    process.argv = [...process.argv, '--chromedriver-path'];
    const config = getAppBridgeConfig();
    expect(config.chromedriverPath).toBe('');
  });
});
