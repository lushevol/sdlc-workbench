import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { createMockServer, isValidToolResponse } from '@sc-node-mcp/shared-tests/helpers/mockServer';

// ── Mock child_process before importing anything that uses it ─────────────────

vi.mock('node:child_process', () => ({
  execSync: vi.fn(() => 'Google Chrome 125.0.0.0'),
  spawn: vi.fn(),
}));

import { execSync, spawn } from 'node:child_process';
import {
  findBrowserCommand,
  clearBrowserCache,
  fetchWithBrowser,
  crawlWithBrowser,
  configureWebCrawlBrowserTools,
} from '../src/tools/webcrawlbrowser.js';

// ── HTML fixtures ─────────────────────────────────────────────────────────────

const SEED = 'https://example.com';

function makeHtml(title, links = [], bodyText = 'Page content here') {
  const anchors = links.map(l => `<a href="${l}">link</a>`).join('');
  return `<html><head><title>${title}</title></head><body>${bodyText}${anchors}</body></html>`;
}

// ── spawn mock helpers ────────────────────────────────────────────────────────

/**
 * Make spawn() emit stdout pages in order, then close with code 0.
 * pages: array of HTML strings (one per spawn call).
 */
function mockSpawnChain(pages) {
  let callCount = 0;
  spawn.mockImplementation(() => {
    const html = pages[callCount] ?? pages[pages.length - 1];
    callCount++;
    const proc = {
      stdout: { on: vi.fn() },
      stderr: { on: vi.fn() },
      on: vi.fn(),
    };
    proc.stdout.on.mockImplementation((event, cb) => {
      if (event === 'data') cb(Buffer.from(html));
    });
    proc.stderr.on.mockImplementation(() => {});
    proc.on.mockImplementation((event, cb) => {
      if (event === 'close') cb(0); // zero exit code = success
    });
    return proc;
  });
}

/**
 * Make spawn() emit a non-zero exit code (simulates browser error).
 */
function mockSpawnError(exitCode = 1, stderrMsg = 'crash') {
  spawn.mockImplementation(() => {
    const proc = {
      stdout: { on: vi.fn() },
      stderr: { on: vi.fn() },
      on: vi.fn(),
    };
    proc.stdout.on.mockImplementation(() => {});
    proc.stderr.on.mockImplementation((event, cb) => {
      if (event === 'data') cb(Buffer.from(stderrMsg));
    });
    proc.on.mockImplementation((event, cb) => {
      if (event === 'close') cb(exitCode);
    });
    return proc;
  });
}

/**
 * Make spawn() emit an 'error' event (process failed to start).
 */
function mockSpawnProcessError(message = 'ENOENT') {
  spawn.mockImplementation(() => {
    const proc = {
      stdout: { on: vi.fn() },
      stderr: { on: vi.fn() },
      on: vi.fn(),
    };
    proc.stdout.on.mockImplementation(() => {});
    proc.stderr.on.mockImplementation(() => {});
    proc.on.mockImplementation((event, cb) => {
      if (event === 'error') cb(new Error(message));
    });
    return proc;
  });
}

// ── Reset caches between tests ────────────────────────────────────────────────

let _savedHTTPS_PROXY;
let _savedHttps_proxy;

beforeEach(() => {
  // Isolate from CI/corporate proxy env vars — tests use explicit proxy args
  _savedHTTPS_PROXY = process.env.HTTPS_PROXY;
  _savedHttps_proxy = process.env.https_proxy;
  delete process.env.HTTPS_PROXY;
  delete process.env.https_proxy;
});

afterEach(() => {
  clearBrowserCache();
  vi.clearAllMocks();
  // Re-set execSync to a working default so browser detection succeeds by default
  execSync.mockReturnValue('Google Chrome 125.0.0.0');
  // Restore proxy env vars
  if (_savedHTTPS_PROXY !== undefined) process.env.HTTPS_PROXY = _savedHTTPS_PROXY;
  if (_savedHttps_proxy !== undefined) process.env.https_proxy = _savedHttps_proxy;
});

// ── findBrowserCommand() ──────────────────────────────────────────────────────

describe('findBrowserCommand()', () => {
  it('returns a non-empty string when a browser is found', () => {
    const cmd = findBrowserCommand();
    expect(typeof cmd).toBe('string');
    expect(cmd.length).toBeGreaterThan(0);
  });

  it('caches result on repeated calls', () => {
    findBrowserCommand();
    findBrowserCommand();
    // execSync should only be called until one candidate succeeds
    expect(execSync).toHaveBeenCalledTimes(1);
  });

  it('throws when no browser is detected', () => {
    execSync.mockImplementation(() => { throw new Error('not found'); });
    expect(() => findBrowserCommand()).toThrow('No Chrome or Edge browser found');
  });

  it('tries next candidate when first fails', () => {
    execSync
      .mockImplementationOnce(() => { throw new Error('not found'); })
      .mockReturnValue('Google Chrome 125.0.0.0');
    const cmd = findBrowserCommand();
    expect(typeof cmd).toBe('string');
    expect(execSync).toHaveBeenCalledTimes(2);
  });

  it('returns cached value after first detection (no extra execSync calls)', () => {
    const cmd1 = findBrowserCommand();
    const cmd2 = findBrowserCommand();
    expect(cmd1).toBe(cmd2);
    expect(execSync.mock.calls.length).toBe(1);
  });
});

// ── clearBrowserCache() ───────────────────────────────────────────────────────

describe('clearBrowserCache()', () => {
  it('forces re-detection on next call', () => {
    findBrowserCommand(); // populates cache
    clearBrowserCache();
    findBrowserCommand(); // should call execSync again
    expect(execSync.mock.calls.length).toBeGreaterThan(1);
  });
});

// ── fetchWithBrowser() ────────────────────────────────────────────────────────

describe('fetchWithBrowser()', () => {
  it('returns HTML string from stdout', async () => {
    const html = makeHtml('Test Page');
    mockSpawnChain([html]);
    const result = await fetchWithBrowser(SEED, undefined);
    expect(result).toContain('Test Page');
  });

  it('rejects on non-zero exit code', async () => {
    mockSpawnError(1, 'crashed');
    await expect(fetchWithBrowser(SEED, undefined)).rejects.toThrow('Browser exited 1');
  });

  it('rejects on spawn error (process not found)', async () => {
    mockSpawnProcessError('ENOENT');
    await expect(fetchWithBrowser(SEED, undefined)).rejects.toThrow('ENOENT');
  });

  it('passes proxy as --proxy-server arg when provided', async () => {
    const html = makeHtml('Proxied');
    mockSpawnChain([html]);
    await fetchWithBrowser(SEED, 'http://proxy.example.com:8080');
    expect(spawn).toHaveBeenCalledWith(
      expect.any(String),
      expect.arrayContaining(['--proxy-server=http://proxy.example.com:8080']),
      expect.any(Object)
    );
  });

  it('does not include --proxy-server arg when proxy is undefined', async () => {
    const html = makeHtml('No proxy');
    mockSpawnChain([html]);
    await fetchWithBrowser(SEED, undefined);
    const args = spawn.mock.calls[0][1];
    expect(args.some(a => a.startsWith('--proxy-server'))).toBe(false);
  });

  it('includes headless, dump-dom, anti-detection and virtual-time flags', async () => {
    mockSpawnChain([makeHtml('Flags')]);
    await fetchWithBrowser(SEED, undefined);
    const args = spawn.mock.calls[0][1];
    expect(args).toContain('--headless=new');
    expect(args).toContain('--dump-dom');
    expect(args).toContain('--disable-blink-features=AutomationControlled');
    expect(args).toContain('--virtual-time-budget=10000');
    expect(args.some(a => a.startsWith('--user-agent='))).toBe(true);
  });
});

// ── crawlWithBrowser() ────────────────────────────────────────────────────────

describe('crawlWithBrowser()', () => {
  it('returns single result for a page with no links', async () => {
    mockSpawnChain([makeHtml('Home')]);
    const results = await crawlWithBrowser({
      seedUrl: SEED, mode: 'urls', maxDepth: 1, maxPages: 10, delayMs: 0,
    });
    expect(results).toHaveLength(1);
    expect(results[0].url).toBe(SEED);
  });

  it('mode urls — only returns url field', async () => {
    mockSpawnChain([makeHtml('Home')]);
    const [r] = await crawlWithBrowser({
      seedUrl: SEED, mode: 'urls', maxDepth: 1, maxPages: 10, delayMs: 0,
    });
    expect(Object.keys(r)).toEqual(['url']);
  });

  it('mode summary — returns url, title, text (truncated)', async () => {
    mockSpawnChain([makeHtml('Summary Title', [], 'A'.repeat(600))]);
    const [r] = await crawlWithBrowser({
      seedUrl: SEED, mode: 'summary', maxDepth: 1, maxPages: 10, delayMs: 0,
    });
    expect(r.url).toBeDefined();
    expect(r.title).toBe('Summary Title');
    expect(r.text.length).toBeLessThanOrEqual(500);
  });

  it('mode full — returns url, title, full text', async () => {
    const longText = 'B'.repeat(700);
    mockSpawnChain([makeHtml('Full Title', [], longText)]);
    const [r] = await crawlWithBrowser({
      seedUrl: SEED, mode: 'full', maxDepth: 1, maxPages: 10, delayMs: 0,
    });
    expect(r.title).toBe('Full Title');
    expect(r.text.length).toBeGreaterThan(500);
  });

  it('mode links — returns url and links array', async () => {
    mockSpawnChain([makeHtml('Links', [`${SEED}/page1`, `${SEED}/page2`])]);
    const [r] = await crawlWithBrowser({
      seedUrl: SEED, mode: 'links', maxDepth: 0, maxPages: 10, delayMs: 0,
    });
    expect(Array.isArray(r.links)).toBe(true);
  });

  it('follows same-origin links to maxDepth', async () => {
    const page1 = makeHtml('Home', [`${SEED}/about`]);
    const page2 = makeHtml('About');
    mockSpawnChain([page1, page2]);
    const results = await crawlWithBrowser({
      seedUrl: SEED, mode: 'urls', maxDepth: 1, maxPages: 10, delayMs: 0,
    });
    expect(results.length).toBeGreaterThanOrEqual(2);
    expect(results.map(r => r.url)).toContain(`${SEED}/about`);
  });

  it('does not follow cross-origin links', async () => {
    const page = makeHtml('Home', ['https://other.com/page', `${SEED}/ok`]);
    const aboutPage = makeHtml('OK');
    mockSpawnChain([page, aboutPage]);
    const results = await crawlWithBrowser({
      seedUrl: SEED, mode: 'urls', maxDepth: 2, maxPages: 20, delayMs: 0,
    });
    expect(results.map(r => r.url)).not.toContain('https://other.com/page');
  });

  it('stops at maxDepth — does not enqueue links at max depth', async () => {
    // depth 0 = seed, depth 1 = about, should NOT enqueue links from about
    const seed = makeHtml('Home', [`${SEED}/about`]);
    const about = makeHtml('About', [`${SEED}/contact`]);
    const contact = makeHtml('Contact');
    mockSpawnChain([seed, about, contact]);
    const results = await crawlWithBrowser({
      seedUrl: SEED, mode: 'urls', maxDepth: 1, maxPages: 20, delayMs: 0,
    });
    expect(results.map(r => r.url)).not.toContain(`${SEED}/contact`);
  });

  it('respects maxPages limit', async () => {
    const seed = makeHtml('Home', [`${SEED}/p1`, `${SEED}/p2`, `${SEED}/p3`]);
    const page = makeHtml('Sub');
    mockSpawnChain([seed, page, page, page]);
    const results = await crawlWithBrowser({
      seedUrl: SEED, mode: 'urls', maxDepth: 3, maxPages: 2, delayMs: 0,
    });
    expect(results.length).toBeLessThanOrEqual(2);
  });

  it('skips already-visited URLs (circular link prevention)', async () => {
    // Home links back to itself
    const seed = makeHtml('Home', [SEED, `${SEED}/page1`]);
    const page1 = makeHtml('Page1');
    mockSpawnChain([seed, page1]);
    const results = await crawlWithBrowser({
      seedUrl: SEED, mode: 'urls', maxDepth: 3, maxPages: 20, delayMs: 0,
    });
    const urls = results.map(r => r.url);
    // SEED should appear exactly once
    expect(urls.filter(u => u === SEED)).toHaveLength(1);
  });

  it('skips pages that fail (browser error) and continues', async () => {
    // seed page succeeds, next page fails, third page succeeds
    let callCount = 0;
    spawn.mockImplementation(() => {
      callCount++;
      if (callCount === 2) {
        // Fail the second spawn (the /about page)
        const proc = {
          stdout: { on: vi.fn() },
          stderr: { on: vi.fn() },
          on: vi.fn(),
        };
        proc.stdout.on.mockImplementation(() => {});
        proc.stderr.on.mockImplementation((event, cb) => {
          if (event === 'data') cb(Buffer.from('crash'));
        });
        proc.on.mockImplementation((event, cb) => {
          if (event === 'close') cb(1); // non-zero
        });
        return proc;
      }
      const html = callCount === 1
        ? makeHtml('Home', [`${SEED}/about`, `${SEED}/contact`])
        : makeHtml('Contact');
      const proc = {
        stdout: { on: vi.fn() },
        stderr: { on: vi.fn() },
        on: vi.fn(),
      };
      proc.stdout.on.mockImplementation((event, cb) => {
        if (event === 'data') cb(Buffer.from(html));
      });
      proc.stderr.on.mockImplementation(() => {});
      proc.on.mockImplementation((event, cb) => {
        if (event === 'close') cb(0);
      });
      return proc;
    });

    const results = await crawlWithBrowser({
      seedUrl: SEED, mode: 'urls', maxDepth: 2, maxPages: 20, delayMs: 0,
    });
    expect(results.map(r => r.url)).toContain(SEED);
    expect(results.map(r => r.url)).not.toContain(`${SEED}/about`);
    expect(results.map(r => r.url)).toContain(`${SEED}/contact`);
  });

  it('uses delayMs between requests', async () => {
    const seed = makeHtml('Home', [`${SEED}/p1`]);
    const p1 = makeHtml('P1');
    mockSpawnChain([seed, p1]);
    const start = Date.now();
    await crawlWithBrowser({
      seedUrl: SEED, mode: 'urls', maxDepth: 1, maxPages: 10, delayMs: 50,
    });
    const elapsed = Date.now() - start;
    expect(elapsed).toBeGreaterThanOrEqual(40);
  });
});

// ── web_crawl_browser MCP tool ────────────────────────────────────────────────

// Create the mock server once at module scope (avoids async init inside describe)
const mockServer = createMockServer();
configureWebCrawlBrowserTools(mockServer, undefined);

describe('web_crawl_browser tool registration', () => {
  it('registers the tool on the server', () => {
    const names = mockServer.getRegisteredTools().map(t => t.name);
    expect(names).toContain('web_crawl_browser');
  });

  it('returns a valid tool response on success', async () => {
    mockSpawnChain([makeHtml('FactSet', [])]);
    const response = await mockServer.invokeTool('web_crawl_browser', {
      url: SEED, mode: 'summary', maxDepth: 1, maxPages: 5, delayMs: 0,
    });
    expect(isValidToolResponse(response)).toBe(true);
  });

  it('returns isError when browser is not found', async () => {
    clearBrowserCache();
    execSync.mockImplementation(() => { throw new Error('not found'); });
    const response = await mockServer.invokeTool('web_crawl_browser', {
      url: SEED, mode: 'summary',
    });
    expect(response.isError).toBe(true);
  });

  it('uses default mode summary', async () => {
    mockSpawnChain([makeHtml('Default Mode', [], 'Some content')]);
    const response = await mockServer.invokeTool('web_crawl_browser', {
      url: SEED,
    });
    expect(isValidToolResponse(response)).toBe(true);
    expect(response.content[0].text).toContain('Default Mode');
  });

  it('all 4 modes produce valid responses', async () => {
    for (const mode of ['urls', 'summary', 'full', 'links']) {
      mockSpawnChain([makeHtml('Page', [])]);
      const response = await mockServer.invokeTool('web_crawl_browser', {
        url: SEED, mode,
      });
      expect(isValidToolResponse(response)).toBe(true);
    }
  });
});
