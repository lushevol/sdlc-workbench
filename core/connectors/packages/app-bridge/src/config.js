/**
 * @author Podder, Arunangshu
 * @bankId 2004018
 */

/** Cached configuration — populated on first call to getAppBridgeConfig() */
let _cachedConfig = null;

/** Maps named CLI flags to config keys */
const FLAG_MAP = {
  '--chromedriver-path': 'chromedriverPath',
  '--edgedriver-path': 'edgedriverPath',
  '--proxy': 'proxy',
  '--chrome-binary-path': 'chromeBinaryPath',
  '--edge-binary-path': 'edgeBinaryPath'
};

/** Maps config keys to their environment variable fallback names */
const ENV_MAP = {
  chromedriverPath: 'CHROMEDRIVER_PATH',
  edgedriverPath: 'EDGEDRIVER_PATH',
  proxy: 'HTTPS_PROXY',
  chromeBinaryPath: 'CHROME_BINARY_PATH',
  edgeBinaryPath: 'EDGE_BINARY_PATH'
};

/**
 * Reset the cached configuration. Intended for use in tests only.
 */
export function resetAppBridgeConfigCache() {
  _cachedConfig = null;
}

/**
 * Parse app-bridge configuration from named CLI flags, falling back to environment variables.
 * Unlike @sc-node-mcp/core's getConfig(), this uses named flags (--chromedriver-path, etc.)
 * rather than positional args, since app-bridge has no ADO/Confluence/Nexus/Sonar concept to
 * position around. Neither driver path is required at startup — browser_start returns a clear
 * error later if the requested browser's driver path was never configured.
 *
 * Priority: 1) Command-line flags, 2) Environment variables.
 * Result is memoized for the lifetime of the process.
 *
 * @returns {{chromedriverPath: string, edgedriverPath: string, proxy: string, chromeBinaryPath: string, edgeBinaryPath: string}}
 */
export function getAppBridgeConfig() {
  if (_cachedConfig) return _cachedConfig;

  const args = process.argv.slice(2);
  const fromArgs = {};
  for (let i = 0; i < args.length; i++) {
    const key = FLAG_MAP[args[i]];
    if (key) {
      fromArgs[key] = args[i + 1] || '';
      i++;
    }
  }

  const config = {};
  for (const key of Object.keys(ENV_MAP)) {
    config[key] = fromArgs[key] || process.env[ENV_MAP[key]] || '';
  }

  logConfig(config);
  _cachedConfig = config;
  return config;
}

/**
 * Log a concise one-line startup summary (no secrets to mask — driver paths and proxy URLs
 * are not sensitive).
 * @param {Object} config
 */
function logConfig(config) {
  console.error(
    `[APP-BRIDGE] Config: chromedriver=${config.chromedriverPath || 'not set'} | ` +
    `edgedriver=${config.edgedriverPath || 'not set'} | ` +
    `proxy=${config.proxy || 'auto-detect'}`
  );
}
