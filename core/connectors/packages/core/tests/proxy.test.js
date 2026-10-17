import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { detectProxy, detectProxyFor, applyProxy, clearProxyCache } from '../src/proxy.js';
import https from 'node:https';

vi.mock('node:https', () => ({ default: { request: vi.fn() } }));

describe('explicit proxy configuration', () => {
  beforeEach(() => {
    clearProxyCache();
    for (const key of ['HTTPS_PROXY', 'https_proxy', 'HTTP_PROXY', 'http_proxy', 'NO_PROXY', 'no_proxy']) {
      vi.stubEnv(key, '');
    }
  });

  afterEach(() => {
    vi.unstubAllEnvs();
    vi.clearAllMocks();
    clearProxyCache();
  });

  it('uses direct access when no proxy is configured without network probes', async () => {
    expect(await detectProxy()).toBe('');
    expect(await detectProxyFor('service.example.com')).toBe('');
    expect(https.request).not.toHaveBeenCalled();
  });

  it('uses the supplied proxy before environment values without probing', async () => {
    vi.stubEnv('HTTPS_PROXY', 'http://environment.example:8080');
    expect(await detectProxyFor('service.example.com', 'http://configured.example:8080'))
      .toBe('http://configured.example:8080');
    expect(https.request).not.toHaveBeenCalled();
  });

  it.each(['HTTPS_PROXY', 'https_proxy', 'HTTP_PROXY', 'http_proxy'])(
    'uses the explicitly configured %s value', async (key) => {
      vi.stubEnv(key, 'http://proxy.example:8080');
      expect(await detectProxyFor('service.example.com')).toBe('http://proxy.example:8080');
    }
  );

  it.each([
    ['service.example.com', 'service.example.com'],
    ['.example.com', 'service.example.com'],
    ['*.example.com', 'service.example.com'],
    ['.example.com', 'example.com'],
    ['*', 'service.example.com'],
    ['other.example, service.example.com', 'service.example.com'],
    ['SERVICE.EXAMPLE.COM', 'service.example.com'],
    ['service.example.com:443', 'service.example.com'],
    ['service.example.com:8443', 'https://service.example.com:8443'],
    ['[::1]:443', 'https://[::1]']
  ])('bypasses the proxy for NO_PROXY=%s and host %s', async (noProxy, host) => {
    vi.stubEnv('NO_PROXY', noProxy);
    expect(await detectProxyFor(host, 'http://proxy.example:8080')).toBe('');
  });

  it.each([
    ['example.com', 'service.example.com'],
    ['.example.com', 'example.com.attacker.example'],
    ['service.example.com:8443', 'service.example.com'],
    ['service.example.com:80', 'service.example.com']
  ])('keeps the proxy for unmatched NO_PROXY=%s and host %s', async (noProxy, host) => {
    vi.stubEnv('NO_PROXY', noProxy);
    expect(await detectProxyFor(host, 'http://proxy.example:8080')).toBe('http://proxy.example:8080');
  });

  it('honors lowercase no_proxy when NO_PROXY is absent', async () => {
    delete process.env.NO_PROXY;
    vi.stubEnv('no_proxy', 'service.example.com');
    expect(await detectProxyFor('service.example.com', 'http://proxy.example:8080')).toBe('');
  });

  it('preserves caller proxy environment values during resolution', async () => {
    vi.stubEnv('HTTPS_PROXY', 'http://proxy.example:8080');
    vi.stubEnv('NO_PROXY', 'service.example.com');
    await detectProxyFor('service.example.com');
    expect(process.env.HTTPS_PROXY).toBe('http://proxy.example:8080');
  });

  it('refreshes the legacy cached proxy only after clearing its cache', async () => {
    expect(await detectProxy('http://first.example:8080')).toBe('http://first.example:8080');
    expect(await detectProxy('http://second.example:8080')).toBe('http://first.example:8080');
    clearProxyCache();
    expect(await detectProxy('http://second.example:8080')).toBe('http://second.example:8080');
  });

  it('applies or clears the selected HTTPS proxy when requested', () => {
    applyProxy('http://proxy.example:8080');
    expect(process.env.HTTPS_PROXY).toBe('http://proxy.example:8080');
    expect(process.env.https_proxy).toBe('http://proxy.example:8080');
    applyProxy('');
    expect(process.env.HTTPS_PROXY).toBeUndefined();
    expect(process.env.https_proxy).toBeUndefined();
  });
});
