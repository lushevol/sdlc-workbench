let _cachedProxy;

export function clearProxyCache() {
  _cachedProxy = undefined;
}

function bypassProxy(host) {
  const noProxy = process.env.NO_PROXY ?? process.env.no_proxy ?? '';
  const target = new URL(host.includes('://') ? host : `https://${host}`);
  const targetPort = target.port || (target.protocol === 'http:' ? '80' : '443');

  return noProxy.split(/[\s,]+/).some((entry) => {
    if (!entry) return false;
    if (entry === '*') return true;

    const includeSubdomains = entry.startsWith('.') || entry.startsWith('*.');
    const address = entry.replace(/^\*?\./, '');
    try {
      const excluded = new URL(`http://${address}`);
      // URL removes default ports. Preserve an explicit :80 when comparing ports.
      const excludedPort = excluded.port || (address.endsWith(':80') ? '80' : '');
      if (excludedPort && excludedPort !== targetPort) return false;

      return target.hostname === excluded.hostname || (
        includeSubdomains && target.hostname.endsWith(`.${excluded.hostname}`)
      );
    } catch {
      return false;
    }
  });
}

/** Resolve an explicit proxy without connectivity probes or environment changes. */
export async function detectProxyFor(host, userProvidedProxy = '') {
  if (bypassProxy(host)) return '';
  return userProvidedProxy || process.env.HTTPS_PROXY || process.env.https_proxy ||
    process.env.HTTP_PROXY || process.env.http_proxy || '';
}

/** Preserve the legacy API while using only configured proxy values. */
export async function detectProxy(userProvidedProxy = '') {
  if (_cachedProxy === undefined) {
    _cachedProxy = await detectProxyFor('dev.azure.com', userProvidedProxy);
  }
  return _cachedProxy;
}

/** Apply a caller-selected proxy to HTTP clients that use environment variables. */
export function applyProxy(proxy) {
  if (proxy) {
    process.env.HTTPS_PROXY = proxy;
    process.env.https_proxy = proxy;
  } else {
    delete process.env.HTTPS_PROXY;
    delete process.env.https_proxy;
  }
}
