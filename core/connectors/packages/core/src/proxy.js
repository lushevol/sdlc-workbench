import https from 'node:https';
import { HttpsProxyAgent } from 'https-proxy-agent';

/** HTTPS host used to probe ADO connectivity for detectProxy() */
const PROBE_HOST = 'dev.azure.com';
const PROBE_PATH = '/';
const PROBE_TIMEOUT_MS = 5000;

/**
 * Known proxy candidates to try, in priority order.
 * Empty string = direct connection (no proxy).
 * 127.0.0.1:9000 is a local proxy/SSH tunnel that bypasses Zscaler for external internet access.
 */
const KNOWN_PROXIES = [
  '',
  'http://127.0.0.1:9000',
  'http://10.239.9.190:443',
  'http://gateway.zscloud.net:443',
];

/** Cached proxy — undefined until detectProxy() is first called; '' = no proxy */
let _cachedProxy;
// Note: rejectUnauthorized:false is intentional — corporate environments use self-signed certs (same as all other packages)

/**
 * Reset the cached proxy detection result. Intended for use in tests only.
 */
export function clearProxyCache() {
  _cachedProxy = undefined;
}

/**
 * Test whether a given proxy (or direct connection if proxyUrl is '') can reach the target host.
 * Any HTTP response in the 1xx–4xx range is treated as connectivity confirmed.
 * 5xx responses (e.g. 502 Bad Gateway) indicate the proxy could not forward the request
 * to the target and are treated as a connectivity failure.
 * @param {string} proxyUrl - Proxy URL, or '' for direct connection
 * @param {number} [timeoutMs] - Timeout in milliseconds
 * @param {string} [host] - Hostname to probe (defaults to PROBE_HOST = dev.azure.com)
 * @returns {Promise<boolean>}
 */
export function testConnectivity(proxyUrl, timeoutMs = PROBE_TIMEOUT_MS, host = PROBE_HOST) {
  return new Promise((resolve) => {
    // NODE_TLS_REJECT_UNAUTHORIZED='0' is set globally in core/index.js; no per-request override needed
    const options = {
      hostname: host,
      path: PROBE_PATH,
      method: 'HEAD',
    };

    if (proxyUrl) {
      options.agent = new HttpsProxyAgent(proxyUrl);
    }

    let settled = false;
    const settle = (result) => {
      if (!settled) {
        settled = true;
        resolve(result);
      }
    };

    const timer = setTimeout(() => settle(false), timeoutMs);

    try {
      const req = https.request(options, (res) => {
        clearTimeout(timer);
        res.resume(); // drain so the connection can be reused/closed
        // 5xx means the proxy/gateway itself failed to forward the request — not connected
        if (res.statusCode >= 500) {
          settle(false);
          return;
        }
        settle(true);
      });
      req.on('error', () => {
        clearTimeout(timer);
        settle(false);
      });
      req.end();
    } catch {
      clearTimeout(timer);
      settle(false);
    }
  });
}

/**
 * Auto-detect the best proxy configuration by probing all known candidates in parallel.
 *
 * Priority order: no proxy → http://10.239.9.190:443 → http://gateway.zscloud.net:443 → user-provided
 *
 * If the user provided a proxy not in the known list it is appended as the last candidate.
 * If all candidates fail, the user-provided proxy is returned as-is (graceful degradation —
 * the real network error will surface when a tool is actually invoked).
 *
 * Result is cached for the lifetime of the process.
 *
 * @param {string} [userProvidedProxy=''] - Proxy from CLI arg / env var / config.json
 * @returns {Promise<string>} The proxy URL to use, or '' for no proxy
 */
export async function detectProxy(userProvidedProxy = '') {
  if (_cachedProxy !== undefined) return _cachedProxy;

  // Build candidate list; append user-provided at the end only if it's not already included
  const candidates = [...KNOWN_PROXIES];
  if (userProvidedProxy && !candidates.includes(userProvidedProxy)) {
    candidates.push(userProvidedProxy);
  }

  // Probe all candidates simultaneously — each candidate is tested against PROBE_HOST (ADO)
  const results = await Promise.all(
    candidates.map(async (proxy) => ({ proxy, ok: await testConnectivity(proxy) }))
  );

  // Pick the first successful candidate (array order = priority order)
  const winner = results.find((r) => r.ok);

  if (winner) {
    _cachedProxy = winner.proxy;
    const label = _cachedProxy === '' ? 'none' : _cachedProxy;
    console.error(`[SC-NODE-MCP] Proxy: ${label} (auto-detected)`);
    return _cachedProxy;
  }

  // All candidates failed — fall back to user-provided; let the real call surface the error
  _cachedProxy = userProvidedProxy || '';
  const label = _cachedProxy || 'none';
  console.error(`[SC-NODE-MCP] Proxy: ${label} (auto-detection failed, using user-provided)`);
  return _cachedProxy;
}

/**
 * Detect the best proxy for a specific service host, independent of the global ADO proxy.
 *
 * Probes the same known candidates as detectProxy() but tests them against `host` rather
 * than the ADO probe host. This allows each service (Confluence, SonarQube, etc.) to use
 * the proxy route that actually works for it — which may differ from the ADO proxy.
 *
 * Unlike detectProxy(), this function is NOT cached. Callers should store the result.
 *
 * @param {string} host - Service hostname to probe (e.g. 'confluence.global.standardchartered.com')
 * @param {string} [userProvidedProxy=''] - Proxy from CLI arg / env var / config.json
 * @returns {Promise<string>} The proxy URL to use for this host, or '' for direct connection
 */
export async function detectProxyFor(host, userProvidedProxy = '') {
  const candidates = [...KNOWN_PROXIES];
  if (userProvidedProxy && !candidates.includes(userProvidedProxy)) {
    candidates.push(userProvidedProxy);
  }

  const results = await Promise.all(
    candidates.map(async (proxy) => ({ proxy, ok: await testConnectivity(proxy, PROBE_TIMEOUT_MS, host) }))
  );

  const winner = results.find((r) => r.ok);
  if (winner) {
    const label = winner.proxy === '' ? 'none' : winner.proxy;
    console.error(`[SC-NODE-MCP] Proxy for ${host}: ${label} (auto-detected)`);
    return winner.proxy;
  }

  const fallback = userProvidedProxy || '';
  const label = fallback || 'none';
  console.error(`[SC-NODE-MCP] Proxy for ${host}: ${label} (auto-detection failed, using user-provided)`);
  return fallback;
}

/**
 * Apply the resolved proxy URL to the current process environment.
 * azure-devops-node-api (node-fetch), axios, and other HTTP clients read HTTPS_PROXY automatically.
 * Removes HTTPS_PROXY from the environment when proxy is '' (no proxy).
 *
 * @param {string} proxy - Proxy URL, or '' to disable proxy
 */
export function applyProxy(proxy) {
  if (proxy) {
    process.env.HTTPS_PROXY = proxy;
    process.env.https_proxy = proxy;
  } else {
    delete process.env.HTTPS_PROXY;
    delete process.env.https_proxy;
  }
}
