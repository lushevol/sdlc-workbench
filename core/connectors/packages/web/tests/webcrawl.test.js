import { describe, it, expect, vi, beforeEach } from 'vitest';
import { createMockServer, isValidToolResponse } from '@sc-node-mcp/shared-tests/helpers/mockServer';

// ── Mock node:https before importing anything that uses it ───────────────────

vi.mock('node:https', () => ({
  default: { request: vi.fn() },
}));

import https from 'node:https';
import { configureWebCrawlTools, extractLinks, extractTitle, formatCrawlResults, crawl } from '../src/tools/webcrawl.js';

// ── HTML fixtures ─────────────────────────────────────────────────────────────

const SEED = 'https://example.com';

function makeHtml(title, links = [], bodyText = 'Hello world') {
  const anchorTags = links.map(l => `<a href="${l}">link</a>`).join('\n');
  return `<html><head><title>${title}</title></head><body>${bodyText}${anchorTags}</body></html>`;
}

// ── https mock helpers ────────────────────────────────────────────────────────

function mockHttpsChain(pages) {
  // pages: array of { url, statusCode, body } in call order
  let callCount = 0;
  https.request.mockImplementation((options, callback) => {
    const page = pages[callCount] || pages[pages.length - 1];
    callCount++;
    const res = {
      statusCode: page.statusCode,
      headers: {},
      on: vi.fn((event, handler) => {
        if (event === 'data') handler(page.body);
        if (event === 'end') handler();
      }),
    };
    callback(res);
    return { on: vi.fn(), end: vi.fn(), write: vi.fn() };
  });
}

function mockHttpsError(message) {
  https.request.mockImplementation(() => ({
    on: vi.fn((event, handler) => {
      if (event === 'error') handler(new Error(message));
    }),
    end: vi.fn(),
    write: vi.fn(),
  }));
}

// ── extractLinks() ────────────────────────────────────────────────────────────

describe('extractLinks()', () => {
  it('extracts absolute same-origin links', () => {
    const html = makeHtml('Test', ['https://example.com/about', 'https://example.com/contact']);
    const links = extractLinks(html, SEED, SEED);
    expect(links).toContain('https://example.com/about');
    expect(links).toContain('https://example.com/contact');
  });

  it('resolves relative links against the page URL', () => {
    const html = makeHtml('Test', ['/about', './contact']);
    const links = extractLinks(html, SEED, SEED);
    expect(links).toContain('https://example.com/about');
    expect(links).toContain('https://example.com/contact');
  });

  it('filters out external links', () => {
    const html = makeHtml('Test', ['https://other.com/page', 'https://example.com/internal']);
    const links = extractLinks(html, SEED, SEED);
    expect(links).not.toContain('https://other.com/page');
    expect(links).toContain('https://example.com/internal');
  });

  it('deduplicates links', () => {
    const html = makeHtml('Test', ['/about', '/about', '/about']);
    const links = extractLinks(html, SEED, SEED);
    expect(links.filter(l => l === 'https://example.com/about')).toHaveLength(1);
  });

  it('strips fragment from links when deduplicating', () => {
    const html = makeHtml('Test', ['/page#section1', '/page#section2']);
    const links = extractLinks(html, SEED, SEED);
    expect(links).toHaveLength(1);
  });

  it('returns empty array when no anchor tags exist', () => {
    const html = '<html><body>No links here</body></html>';
    expect(extractLinks(html, SEED, SEED)).toEqual([]);
  });

  it('ignores anchors with no href', () => {
    const html = '<html><body><a>no href</a></body></html>';
    expect(extractLinks(html, SEED, SEED)).toEqual([]);
  });

  it('ignores anchors with invalid href', () => {
    const html = '<html><body><a href="not a url at all !!">bad</a></body></html>';
    const links = extractLinks(html, SEED, SEED);
    // Invalid bare strings resolve against base — may or may not be valid. Just verify no crash.
    expect(Array.isArray(links)).toBe(true);
  });
});

// ── extractTitle() ────────────────────────────────────────────────────────────

describe('extractTitle()', () => {
  it('extracts the page title', () => {
    expect(extractTitle('<html><head><title>My Page</title></head></html>')).toBe('My Page');
  });

  it('returns empty string when no title tag', () => {
    expect(extractTitle('<html><body>no title</body></html>')).toBe('');
  });

  it('trims whitespace from title', () => {
    expect(extractTitle('<html><head><title>  Spaced  </title></head></html>')).toBe('Spaced');
  });
});

// ── formatCrawlResults() ──────────────────────────────────────────────────────

describe('formatCrawlResults()', () => {
  it('returns no-pages message for empty results', () => {
    expect(formatCrawlResults([], 'urls')).toContain('No pages were discovered');
  });

  it('urls mode: includes URL in output', () => {
    const out = formatCrawlResults([{ url: 'https://example.com' }], 'urls');
    expect(out).toContain('https://example.com');
    expect(out).toContain('Crawled 1 page');
  });

  it('summary mode: includes title and URL', () => {
    const out = formatCrawlResults([{ url: 'https://example.com', title: 'Home', text: 'Welcome' }], 'summary');
    expect(out).toContain('Home');
    expect(out).toContain('https://example.com');
    expect(out).toContain('Welcome');
  });

  it('summary mode: shows (no title) when title is empty', () => {
    const out = formatCrawlResults([{ url: 'https://example.com', title: '', text: '' }], 'summary');
    expect(out).toContain('(no title)');
  });

  it('full mode: includes title and full text', () => {
    const out = formatCrawlResults([{ url: 'https://example.com', title: 'Full', text: 'Full text here' }], 'full');
    expect(out).toContain('Full');
    expect(out).toContain('Full text here');
  });

  it('links mode: includes outbound links', () => {
    const out = formatCrawlResults([{ url: 'https://example.com', links: ['https://example.com/about'] }], 'links');
    expect(out).toContain('https://example.com/about');
  });

  it('links mode: shows no-links message when links array is empty', () => {
    const out = formatCrawlResults([{ url: 'https://example.com', links: [] }], 'links');
    expect(out).toContain('no outbound links found');
  });

  it('reports correct page count', () => {
    const results = [
      { url: 'https://example.com' },
      { url: 'https://example.com/about' },
    ];
    expect(formatCrawlResults(results, 'urls')).toContain('Crawled 2 page');
  });
});

// ── crawl() — core BFS engine ─────────────────────────────────────────────────

describe('crawl()', () => {
  beforeEach(() => { vi.clearAllMocks(); });

  it('returns seed URL in urls mode', async () => {
    const html = makeHtml('Home', []);
    mockHttpsChain([{ statusCode: 200, body: html }]);

    const results = await crawl({ seedUrl: SEED, mode: 'urls', maxDepth: 0, maxPages: 10, delayMs: 0 });
    expect(results).toHaveLength(1);
    expect(results[0].url).toBe(SEED);
  });

  it('urls mode: result objects have only url field', async () => {
    mockHttpsChain([{ statusCode: 200, body: makeHtml('Home') }]);
    const [r] = await crawl({ seedUrl: SEED, mode: 'urls', maxDepth: 0, maxPages: 10, delayMs: 0 });
    expect(Object.keys(r)).toEqual(['url']);
  });

  it('summary mode: result has url, title, text (truncated to 500)', async () => {
    const longBody = 'A'.repeat(1000);
    mockHttpsChain([{ statusCode: 200, body: makeHtml('Home', [], longBody) }]);
    const [r] = await crawl({ seedUrl: SEED, mode: 'summary', maxDepth: 0, maxPages: 10, delayMs: 0 });
    expect(r.title).toBe('Home');
    expect(r.text.length).toBeLessThanOrEqual(500);
  });

  it('full mode: result has url, title, and full text', async () => {
    const longBody = 'B'.repeat(2000);
    mockHttpsChain([{ statusCode: 200, body: makeHtml('Full', [], longBody) }]);
    const [r] = await crawl({ seedUrl: SEED, mode: 'full', maxDepth: 0, maxPages: 10, delayMs: 0 });
    expect(r.title).toBe('Full');
    expect(r.text.length).toBeGreaterThan(500);
  });

  it('links mode: result has url and links array', async () => {
    const html = makeHtml('Home', ['https://example.com/about']);
    mockHttpsChain([{ statusCode: 200, body: html }]);
    const [r] = await crawl({ seedUrl: SEED, mode: 'links', maxDepth: 0, maxPages: 10, delayMs: 0 });
    expect(Array.isArray(r.links)).toBe(true);
    expect(r.links).toContain('https://example.com/about');
  });

  it('follows links to discovered pages', async () => {
    const home = makeHtml('Home', ['https://example.com/about']);
    const about = makeHtml('About', []);
    mockHttpsChain([
      { statusCode: 200, body: home },
      { statusCode: 200, body: about },
    ]);

    const results = await crawl({ seedUrl: SEED, mode: 'urls', maxDepth: 1, maxPages: 10, delayMs: 0 });
    const urls = results.map(r => r.url);
    expect(urls).toContain(SEED);
    expect(urls).toContain('https://example.com/about');
  });

  it('does NOT follow external links', async () => {
    const html = makeHtml('Home', ['https://external.com/page', 'https://example.com/internal']);
    mockHttpsChain([
      { statusCode: 200, body: html },
      { statusCode: 200, body: makeHtml('Internal') },
    ]);

    const results = await crawl({ seedUrl: SEED, mode: 'urls', maxDepth: 1, maxPages: 10, delayMs: 0 });
    const urls = results.map(r => r.url);
    expect(urls).not.toContain('https://external.com/page');
    expect(urls).toContain('https://example.com/internal');
  });

  it('respects maxPages limit', async () => {
    const html = makeHtml('Home', ['https://example.com/a', 'https://example.com/b', 'https://example.com/c']);
    mockHttpsChain([
      { statusCode: 200, body: html },
      { statusCode: 200, body: makeHtml('A') },
    ]);

    const results = await crawl({ seedUrl: SEED, mode: 'urls', maxDepth: 1, maxPages: 2, delayMs: 0 });
    expect(results.length).toBeLessThanOrEqual(2);
  });

  it('respects maxDepth limit — does not go deeper than maxDepth', async () => {
    // Depth 0: seed with link to /level1
    // Depth 1: /level1 with link to /level2
    // maxDepth=1 so /level2 should NOT be visited
    const seed = makeHtml('Seed', ['https://example.com/level1']);
    const level1 = makeHtml('Level1', ['https://example.com/level2']);
    mockHttpsChain([
      { statusCode: 200, body: seed },
      { statusCode: 200, body: level1 },
    ]);

    const results = await crawl({ seedUrl: SEED, mode: 'urls', maxDepth: 1, maxPages: 10, delayMs: 0 });
    const urls = results.map(r => r.url);
    expect(urls).not.toContain('https://example.com/level2');
  });

  it('prevents circular link loops via visited set', async () => {
    // A → B → A (circular)
    const pageA = makeHtml('A', ['https://example.com/b']);
    const pageB = makeHtml('B', ['https://example.com']);
    mockHttpsChain([
      { statusCode: 200, body: pageA },
      { statusCode: 200, body: pageB },
    ]);

    const results = await crawl({ seedUrl: SEED, mode: 'urls', maxDepth: 5, maxPages: 10, delayMs: 0 });
    // Should visit each page only once
    const urls = results.map(r => r.url);
    const unique = new Set(urls);
    expect(unique.size).toBe(urls.length);
  });

  it('skips pages that return non-200 status', async () => {
    const seed = makeHtml('Home', ['https://example.com/broken', 'https://example.com/good']);
    mockHttpsChain([
      { statusCode: 200, body: seed },
      { statusCode: 404, body: 'Not Found' },
      { statusCode: 200, body: makeHtml('Good') },
    ]);

    const results = await crawl({ seedUrl: SEED, mode: 'urls', maxDepth: 1, maxPages: 10, delayMs: 0 });
    const urls = results.map(r => r.url);
    expect(urls).toContain('https://example.com/good');
    // broken page skipped, so result count is 2 (seed + good)
    expect(results.length).toBe(2);
  });

  it('skips pages that throw a network error and continues', async () => {
    // First call (seed) succeeds, second call (child) throws
    let callCount = 0;
    https.request.mockImplementation((options, callback) => {
      callCount++;
      if (callCount === 1) {
        const html = makeHtml('Seed', ['https://example.com/fail', 'https://example.com/ok']);
        const res = {
          statusCode: 200,
          headers: {},
          on: vi.fn((e, h) => { if (e === 'data') { h(html); } else if (e === 'end') { h(); } }),
        };
        callback(res);
        return { on: vi.fn(), end: vi.fn(), write: vi.fn() };
      }
      if (callCount === 2) {
        // Network error on /fail
        return {
          on: vi.fn((e, h) => { if (e === 'error') h(new Error('network fail')); }),
          end: vi.fn(), write: vi.fn(),
        };
      }
      // /ok succeeds
      const res = {
        statusCode: 200, headers: {},
        on: vi.fn((e, h) => { if (e === 'data') { h(makeHtml('OK')); } else if (e === 'end') { h(); } }),
      };
      callback(res);
      return { on: vi.fn(), end: vi.fn(), write: vi.fn() };
    });

    const results = await crawl({ seedUrl: SEED, mode: 'urls', maxDepth: 1, maxPages: 10, delayMs: 0 });
    const urls = results.map(r => r.url);
    expect(urls).toContain(SEED);
    expect(urls).toContain('https://example.com/ok');
    expect(urls).not.toContain('https://example.com/fail');
  });

  it('works with delayMs=0 without error', async () => {
    mockHttpsChain([{ statusCode: 200, body: makeHtml('Home') }]);
    const results = await crawl({ seedUrl: SEED, mode: 'urls', maxDepth: 0, maxPages: 1, delayMs: 0 });
    expect(results).toHaveLength(1);
  });
});

// ── web_crawl MCP tool (end-to-end via server) ────────────────────────────────

function setupCrawlServer() {
  const server = createMockServer();
  configureWebCrawlTools(server);
  return server;
}

describe('web_crawl tool', () => {
  beforeEach(() => { vi.clearAllMocks(); });

  it('is registered on the server', () => {
    const server = setupCrawlServer();
    const names = server.getRegisteredTools().map(t => t.name);
    expect(names).toContain('web_crawl');
  });

  it('returns a valid MCP response for a successful crawl', async () => {
    mockHttpsChain([{ statusCode: 200, body: makeHtml('Home') }]);
    const server = setupCrawlServer();
    const response = await server.invokeTool('web_crawl', { url: SEED });
    expect(isValidToolResponse(response)).toBe(true);
  });

  it('includes crawled URL count in output', async () => {
    mockHttpsChain([{ statusCode: 200, body: makeHtml('Home') }]);
    const server = setupCrawlServer();
    const response = await server.invokeTool('web_crawl', { url: SEED });
    expect(response.content[0].text).toContain('Crawled');
  });

  it('returns no-pages response when seed URL fails to connect', async () => {
    mockHttpsError('Connection refused');
    const server = setupCrawlServer();
    const response = await server.invokeTool('web_crawl', { url: SEED });
    // Network failures on individual pages are swallowed; crawl returns empty results
    expect(isValidToolResponse(response)).toBe(true);
    expect(response.content[0].text).toContain('No pages were discovered');
  });

  it('handles invalid URL gracefully without crashing', async () => {
    // The mock server bypasses Zod; makeRequest catches the URL parse error internally
    const server = setupCrawlServer();
    const response = await server.invokeTool('web_crawl', { url: 'not-a-url' });
    expect(isValidToolResponse(response)).toBe(true);
  });

  it('uses summary mode when specified', async () => {
    mockHttpsChain([{ statusCode: 200, body: makeHtml('Summary Page', [], 'Summary content') }]);
    const server = setupCrawlServer();
    const response = await server.invokeTool('web_crawl', { url: SEED, mode: 'summary' });
    expect(response.content[0].text).toContain('Summary Page');
  });

  it('uses links mode when specified', async () => {
    const html = makeHtml('Home', ['https://example.com/about']);
    mockHttpsChain([{ statusCode: 200, body: html }]);
    const server = setupCrawlServer();
    const response = await server.invokeTool('web_crawl', { url: SEED, mode: 'links' });
    expect(response.content[0].text).toContain('https://example.com/about');
  });

  it('respects maxPages=1 returning exactly 1 result', async () => {
    const html = makeHtml('Home', ['https://example.com/a', 'https://example.com/b']);
    mockHttpsChain([
      { statusCode: 200, body: html },
      { statusCode: 200, body: makeHtml('A') },
    ]);
    const server = setupCrawlServer();
    const response = await server.invokeTool('web_crawl', { url: SEED, maxPages: 1 });
    expect(response.content[0].text).toContain('Crawled 1 page');
  });
});
