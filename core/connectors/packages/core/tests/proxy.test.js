import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { detectProxy, detectProxyFor, applyProxy, clearProxyCache, testConnectivity } from '../src/proxy.js';

// ── Mock https and HttpsProxyAgent ───────────────────────────────────────────

vi.mock('node:https', () => ({
  default: {
    request: vi.fn(),
  },
}));

vi.mock('https-proxy-agent', () => ({
  HttpsProxyAgent: vi.fn().mockImplementation(function(url) { return { proxyUrl: url }; }),
}));

import https from 'node:https';
import { HttpsProxyAgent } from 'https-proxy-agent';

// ── Helpers ──────────────────────────────────────────────────────────────────

/**
 * Build a mock request object that emits a response (connectivity = true).
 */
function mockRequestSuccess() {
  const mockRes = { resume: vi.fn(), statusCode: 200 };
  const mockReq = {
    on: vi.fn(),
    end: vi.fn(),
  };
  https.request.mockImplementationOnce((_options, callback) => {
    callback(mockRes);
    return mockReq;
  });
  return mockReq;
}

/**
 * Build a mock request object that emits an error (connectivity = false).
 */
function mockRequestFailure() {
  const mockReq = {
    on: vi.fn((event, handler) => {
      if (event === 'error') handler(new Error('ECONNREFUSED'));
    }),
    end: vi.fn(),
  };
  https.request.mockImplementationOnce(() => mockReq);
  return mockReq;
}

/**
 * Build a mock request that returns a specific HTTP status code.
 * Used to test 5xx rejection (e.g. 502 Bad Gateway from a proxy).
 */
function mockRequestWithStatus(status) {
  const mockRes = { resume: vi.fn(), statusCode: status };
  const mockReq = {
    on: vi.fn(),
    end: vi.fn(),
  };
  https.request.mockImplementationOnce((_options, callback) => {
    callback(mockRes);
    return mockReq;
  });
  return mockReq;
}

/**
 * Build a mock request that succeeds, then also fires a (late) error handler —
 * used to exercise the double-settle guard once the result is already resolved.
 */
function mockRequestSuccessThenLateError() {
  const mockRes = { resume: vi.fn(), statusCode: 200 };
  const mockReq = {
    on: vi.fn((event, handler) => {
      if (event === 'error') handler(new Error('late error after response'));
    }),
    end: vi.fn(),
  };
  https.request.mockImplementationOnce((_options, callback) => {
    callback(mockRes);
    return mockReq;
  });
  return mockReq;
}

// ── Tests ─────────────────────────────────────────────────────────────────────

describe('proxy', () => {
  const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {});

  beforeEach(() => {
    clearProxyCache();
    consoleSpy.mockClear();
    vi.clearAllMocks();
    delete process.env.HTTPS_PROXY;
    delete process.env.https_proxy;
  });

  afterEach(() => {
    clearProxyCache();
    delete process.env.HTTPS_PROXY;
    delete process.env.https_proxy;
  });

  // ── testConnectivity ──────────────────────────────────────────────────────

  describe('testConnectivity', () => {
    it('returns true when the request receives any HTTP response', async () => {
      mockRequestSuccess();
      const result = await testConnectivity('');
      expect(result).toBe(true);
    });

    it('returns false when the request errors', async () => {
      mockRequestFailure();
      const result = await testConnectivity('');
      expect(result).toBe(false);
    });

    it('ignores a late error that arrives after the response already settled the result', async () => {
      mockRequestSuccessThenLateError();
      const result = await testConnectivity('');
      expect(result).toBe(true);
    });

    it('returns false when the response status is 5xx (proxy/gateway failure)', async () => {
      mockRequestWithStatus(502);
      const result = await testConnectivity('');
      expect(result).toBe(false);
    });

    it('passes HttpsProxyAgent when proxyUrl is provided', async () => {
      mockRequestSuccess();
      await testConnectivity('http://10.239.9.190:443');
      expect(HttpsProxyAgent).toHaveBeenCalledWith('http://10.239.9.190:443');
      const callOptions = https.request.mock.calls[0][0];
      expect(callOptions.agent).toBeDefined();
    });

    it('does not set agent when proxyUrl is empty', async () => {
      mockRequestSuccess();
      await testConnectivity('');
      const callOptions = https.request.mock.calls[0][0];
      expect(callOptions.agent).toBeUndefined();
    });
  });

  // ── detectProxy ───────────────────────────────────────────────────────────

  describe('detectProxy', () => {
    it('returns empty string when direct connection (no proxy) works first', async () => {
      mockRequestSuccess();           // '' — wins
      mockRequestFailure();           // http://127.0.0.1:9000 — fails
      mockRequestFailure();           // http://10.239.9.190:443 — fails
      mockRequestFailure();           // http://gateway.zscloud.net:443 — fails

      const proxy = await detectProxy('');
      expect(proxy).toBe('');
      expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining('none (auto-detected)'));
    });

    it('returns first known proxy when direct fails but proxy works', async () => {
      mockRequestFailure();           // '' — fails
      mockRequestSuccess();           // http://127.0.0.1:9000 — wins
      mockRequestFailure();           // http://10.239.9.190:443 — fails
      mockRequestFailure();           // http://gateway.zscloud.net:443 — fails

      const proxy = await detectProxy('');
      expect(proxy).toBe('http://127.0.0.1:9000');
      expect(consoleSpy).toHaveBeenCalledWith(
        expect.stringContaining('http://127.0.0.1:9000 (auto-detected)')
      );
    });

    it('returns second known proxy when direct and local proxy fail', async () => {
      mockRequestFailure();           // '' — fails
      mockRequestFailure();           // http://127.0.0.1:9000 — fails
      mockRequestSuccess();           // http://10.239.9.190:443 — wins
      mockRequestFailure();           // http://gateway.zscloud.net:443 — fails

      const proxy = await detectProxy('');
      expect(proxy).toBe('http://10.239.9.190:443');
      expect(consoleSpy).toHaveBeenCalledWith(
        expect.stringContaining('http://10.239.9.190:443 (auto-detected)')
      );
    });

    it('returns third known proxy when only that one works', async () => {
      mockRequestFailure();           // '' — fails
      mockRequestFailure();           // http://127.0.0.1:9000 — fails
      mockRequestFailure();           // http://10.239.9.190:443 — fails
      mockRequestSuccess();           // http://gateway.zscloud.net:443 — wins

      const proxy = await detectProxy('');
      expect(proxy).toBe('http://gateway.zscloud.net:443');
    });

    it('includes user-provided proxy as last candidate when not already in known list', async () => {
      mockRequestFailure();           // '' — fails
      mockRequestFailure();           // http://127.0.0.1:9000 — fails
      mockRequestFailure();           // http://10.239.9.190:443 — fails
      mockRequestFailure();           // http://gateway.zscloud.net:443 — fails
      mockRequestSuccess();           // user-provided — wins

      const proxy = await detectProxy('http://custom-proxy:8080');
      expect(proxy).toBe('http://custom-proxy:8080');
    });

    it('does not duplicate user-provided proxy when it is already a known candidate', async () => {
      // http://10.239.9.190:443 is a known candidate — should NOT be added again
      mockRequestFailure();           // '' — fails
      mockRequestFailure();           // http://127.0.0.1:9000 — fails
      mockRequestSuccess();           // http://10.239.9.190:443 — wins (not duplicated at end)
      mockRequestFailure();           // http://gateway.zscloud.net:443 — fails

      const proxy = await detectProxy('http://10.239.9.190:443');
      expect(proxy).toBe('http://10.239.9.190:443');
      // Only 4 candidates (no duplication) × 1 probe host = ≤4 requests
      expect(https.request.mock.calls.length).toBeLessThanOrEqual(4);
    });

    it('falls back to user-provided proxy when all candidates fail', async () => {
      mockRequestFailure();           // ''
      mockRequestFailure();           // http://127.0.0.1:9000
      mockRequestFailure();           // http://10.239.9.190:443
      mockRequestFailure();           // http://gateway.zscloud.net:443
      mockRequestFailure();           // user-provided

      const proxy = await detectProxy('http://fallback-proxy:443');
      expect(proxy).toBe('http://fallback-proxy:443');
      expect(consoleSpy).toHaveBeenCalledWith(
        expect.stringContaining('auto-detection failed, using user-provided')
      );
    });

    it('returns empty string when all candidates fail and no user proxy provided', async () => {
      mockRequestFailure();           // ''
      mockRequestFailure();           // http://127.0.0.1:9000
      mockRequestFailure();           // http://10.239.9.190:443
      mockRequestFailure();           // http://gateway.zscloud.net:443

      const proxy = await detectProxy('');
      expect(proxy).toBe('');
      expect(consoleSpy).toHaveBeenCalledWith(
        expect.stringContaining('auto-detection failed, using user-provided')
      );
    });

    it('returns cached result on subsequent calls without re-probing', async () => {
      mockRequestSuccess();           // '' — wins first call
      mockRequestFailure();
      mockRequestFailure();
      mockRequestFailure();
      const first = await detectProxy('');
      const requestCountAfterFirst = https.request.mock.calls.length;

      // Second call without clearing cache — must return same result with no new probing
      const second = await detectProxy('');
      expect(first).toBe(second);
      expect(https.request.mock.calls.length).toBe(requestCountAfterFirst);
    });
  });

  // ── detectProxyFor ─────────────────────────────────────────────────

  describe('detectProxyFor', () => {
    it('returns direct (empty string) when direct connection reaches the service', async () => {
      mockRequestSuccess();           // '' — wins
      mockRequestFailure();           // http://127.0.0.1:9000
      mockRequestFailure();           // http://10.239.9.190:443
      mockRequestFailure();           // http://gateway.zscloud.net:443

      const proxy = await detectProxyFor('confluence.global.standardchartered.com');
      expect(proxy).toBe('');
      expect(consoleSpy).toHaveBeenCalledWith(
        expect.stringContaining('Proxy for confluence.global.standardchartered.com: none (auto-detected)')
      );
    });

    it('returns proxy when direct fails but local proxy can reach the service', async () => {
      mockRequestFailure();           // '' — fails
      mockRequestSuccess();           // http://127.0.0.1:9000 — wins
      mockRequestFailure();           // http://10.239.9.190:443
      mockRequestFailure();           // http://gateway.zscloud.net:443

      const proxy = await detectProxyFor('confluence.global.standardchartered.com');
      expect(proxy).toBe('http://127.0.0.1:9000');
    });

    it('returns corporate proxy when direct and local proxy fail', async () => {
      mockRequestFailure();           // '' — fails
      mockRequestFailure();           // http://127.0.0.1:9000 — fails
      mockRequestSuccess();           // http://10.239.9.190:443 — wins
      mockRequestFailure();           // http://gateway.zscloud.net:443

      const proxy = await detectProxyFor('confluence.global.standardchartered.com');
      expect(proxy).toBe('http://10.239.9.190:443');
    });

    it('correctly picks direct even when the ADO proxy returns 502 for the service', async () => {
      // This is the key scenario: the ADO proxy works for ADO but 502s for Confluence
      // detectProxyFor tests direct FIRST and finds it works — selects direct (no proxy)
      mockRequestSuccess();           // '' — wins (direct works for Confluence)
      mockRequestFailure();           // http://127.0.0.1:9000
      mockRequestWithStatus(502);     // http://10.239.9.190:443 — 502 → fail
      mockRequestFailure();           // http://gateway.zscloud.net:443

      const proxy = await detectProxyFor('confluence.global.standardchartered.com', 'http://10.239.9.190:443');
      expect(proxy).toBe('');
    });

    it('falls back to user-provided proxy when all candidates fail', async () => {
      mockRequestFailure();           // ''
      mockRequestFailure();           // http://127.0.0.1:9000
      mockRequestFailure();           // http://10.239.9.190:443
      mockRequestFailure();           // http://gateway.zscloud.net:443
      mockRequestFailure();           // user-provided

      const proxy = await detectProxyFor('confluence.global.standardchartered.com', 'http://custom:443');
      expect(proxy).toBe('http://custom:443');
      expect(consoleSpy).toHaveBeenCalledWith(
        expect.stringContaining('auto-detection failed, using user-provided')
      );
    });

    it('falls back to "none" (empty string) when all candidates fail and no proxy was provided', async () => {
      mockRequestFailure();           // ''
      mockRequestFailure();           // http://127.0.0.1:9000
      mockRequestFailure();           // http://10.239.9.190:443
      mockRequestFailure();           // http://gateway.zscloud.net:443

      const proxy = await detectProxyFor('confluence.global.standardchartered.com');
      expect(proxy).toBe('');
      expect(consoleSpy).toHaveBeenCalledWith(
        expect.stringContaining('Proxy for confluence.global.standardchartered.com: none (auto-detection failed, using user-provided)')
      );
    });

    it('is not cached — probes on every call', async () => {
      mockRequestSuccess();
      mockRequestFailure();
      mockRequestFailure();
      mockRequestFailure();
      await detectProxyFor('confluence.global.standardchartered.com');

      const countAfterFirst = https.request.mock.calls.length;

      mockRequestSuccess();
      mockRequestFailure();
      mockRequestFailure();
      mockRequestFailure();
      await detectProxyFor('confluence.global.standardchartered.com');

      expect(https.request.mock.calls.length).toBeGreaterThan(countAfterFirst);
    });
  });

  // ── applyProxy ────────────────────────────────────────────────────────────

  describe('applyProxy', () => {
    it('sets HTTPS_PROXY env vars when proxy is provided', () => {
      applyProxy('http://10.239.9.190:443');
      expect(process.env.HTTPS_PROXY).toBe('http://10.239.9.190:443');
      expect(process.env.https_proxy).toBe('http://10.239.9.190:443');
    });

    it('deletes HTTPS_PROXY env vars when proxy is empty string', () => {
      process.env.HTTPS_PROXY = 'http://existing:443';
      process.env.https_proxy = 'http://existing:443';
      applyProxy('');
      expect(process.env.HTTPS_PROXY).toBeUndefined();
      expect(process.env.https_proxy).toBeUndefined();
    });
  });

  // ── clearProxyCache ───────────────────────────────────────────────────────

  describe('clearProxyCache', () => {
    it('forces re-detection on next call after cache is cleared', async () => {
      mockRequestSuccess();           // '' — wins first call
      mockRequestFailure();
      mockRequestFailure();
      mockRequestFailure();
      await detectProxy('');

      clearProxyCache();
      const requestCountBeforeSecond = https.request.mock.calls.length;

      mockRequestSuccess();           // '' — wins second call
      mockRequestFailure();
      mockRequestFailure();
      mockRequestFailure();
      await detectProxy('');

      expect(https.request.mock.calls.length).toBeGreaterThan(requestCountBeforeSecond);
    });
  });
});
