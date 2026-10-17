import { z } from 'zod';
import { spawn, execSync } from 'node:child_process';
import { extractLinks, extractTitle, formatCrawlResults } from './webcrawl.js';
import { stripHtml } from './websearch.js';

// ── Browser detection ─────────────────────────────────────────────────────────
// Mirrors findPython3Command() in websearch.js — detect system Chrome/Edge,
// cache the result, throw if nothing found.

/** Cached browser executable path. null = not yet detected. '' = not found. */
let _browserCmd = null;

/**
 * Browser executable candidates ordered by preference, per platform.
 * @returns {string[]}
 */
function getBrowserCandidates() {
  if (process.platform === 'darwin') {
    return [
      '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
      '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
      'google-chrome',
      'chromium',
    ];
  }
  if (process.platform === 'win32') {
    return [
      String.raw`C:\Program Files\Google\Chrome\Application\chrome.exe`,
      String.raw`C:\Program Files (x86)\Google\Chrome\Application\chrome.exe`,
      String.raw`C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`,
      String.raw`C:\Program Files\Microsoft\Edge\Application\msedge.exe`,
    ];
  }
  // Linux / other
  return ['google-chrome', 'chromium-browser', 'microsoft-edge', 'chromium'];
}

/**
 * Detect the system Chrome or Edge executable, caching the result.
 * Tries candidates in platform order. Throws if none found.
 * @returns {string} Executable path or command name
 */
export function findBrowserCommand() {
  if (_browserCmd !== null) return _browserCmd;

  for (const cmd of getBrowserCandidates()) {
    try {
      const out = execSync(`"${cmd}" --version`, {
        encoding: 'utf8',
        timeout: 5000,
        stdio: ['ignore', 'pipe', 'pipe'],
      });
      if (/Chrome|Edge|Chromium/i.test(out)) {
        _browserCmd = cmd;
        return cmd;
      }
    } catch { /* try next */ }
  }

  _browserCmd = '';
  throw new Error(
    'No Chrome or Edge browser found. Install Google Chrome or Microsoft Edge to enable web_crawl_browser.'
  );
}

/**
 * Reset the cached browser command. Intended for use in tests only.
 */
export function clearBrowserCache() { _browserCmd = null; }

// ── Single-page fetch via system browser ──────────────────────────────────────

/**
 * Build the proxy CLI argument array for Chrome/Edge.
 * @param {string|undefined} proxy
 * @returns {string[]}
 */
function proxyArgs(proxy) {
  const url = proxy ?? (process.env.HTTPS_PROXY || process.env.https_proxy);
  return url ? [`--proxy-server=${url}`] : [];
}

/**
 * Fetch a URL using the system Chrome/Edge in headless mode.
 * Returns the fully JS-rendered HTML as a string.
 * Rejects on non-zero exit or spawn error.
 * @param {string} url
 * @param {string|undefined} proxy
 * @returns {Promise<string>}
 */
export function fetchWithBrowser(url, proxy) {
  return new Promise((resolve, reject) => {
    const browserCmd = findBrowserCommand();

    const args = [
      '--headless=new',
      '--dump-dom',
      '--no-sandbox',
      '--disable-gpu',
      '--disable-dev-shm-usage',
      '--ignore-certificate-errors',
      '--disable-extensions',
      // Bypass headless/automation detection (sites check navigator.webdriver and UA)
      '--disable-blink-features=AutomationControlled',
      '--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
      // Give JS up to 10 seconds of virtual time to execute before DOM is captured
      // This is critical for SPAs: without it --dump-dom captures the pre-render shell
      '--virtual-time-budget=10000',
      ...proxyArgs(proxy),
      url,
    ];

    const proc = spawn(browserCmd, args, { stdio: ['ignore', 'pipe', 'pipe'] });

    let html = '';
    let stderr = '';
    proc.stdout.on('data', (chunk) => { html += chunk; });
    proc.stderr.on('data', (chunk) => { stderr += chunk; });
    proc.on('error', reject);
    proc.on('close', (code) => {
      if (code !== 0) {
        reject(new Error(`Browser exited ${code}: ${stderr.slice(0, 300).trim()}`));
        return;
      }
      resolve(html);
    });
  });
}

// ── Helpers shared with web_crawl ─────────────────────────────────────────────

/**
 * Normalise a URL by stripping fragment and trailing slash.
 * @param {string} url
 * @returns {string}
 */
function normaliseUrl(url) {
  return url.split('#')[0].replace(/\/$/, '') || url;
}

/**
 * Build a single page result object based on the requested mode.
 * @param {string} url
 * @param {string} html
 * @param {string} mode
 * @param {string} seedUrl
 * @returns {Object}
 */
function buildPageResult(url, html, mode, seedUrl) {
  if (mode === 'urls') return { url };
  if (mode === 'summary') return { url, title: extractTitle(html), text: stripHtml(html).slice(0, 500) };
  if (mode === 'full') return { url, title: extractTitle(html), text: stripHtml(html) };
  return { url, links: extractLinks(html, url, seedUrl) }; // 'links' mode
}

/**
 * Enqueue unvisited same-origin child links from a page.
 * @param {string} html
 * @param {string} pageUrl
 * @param {string} seedUrl
 * @param {number} depth
 * @param {Set<string>} visited
 * @param {Array<{url:string,depth:number}>} queue
 */
function enqueueLinks(html, pageUrl, seedUrl, depth, visited, queue) {
  const links = extractLinks(html, pageUrl, seedUrl);
  for (const link of links) {
    if (!visited.has(normaliseUrl(link))) {
      queue.push({ url: link, depth: depth + 1 });
    }
  }
}

/**
 * Sleep for `ms` milliseconds.
 * @param {number} ms
 */
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// ── Core BFS crawl engine (browser-powered) ───────────────────────────────────

/**
 * Crawl a website starting from `seedUrl` using BFS.
 * Each page is fetched via the system browser (JS rendered).
 * Stays within the same origin. Respects depth, page, and delay limits.
 *
 * @param {Object} opts
 * @param {string}  opts.seedUrl   - Starting URL
 * @param {string}  opts.mode      - 'urls' | 'summary' | 'full' | 'links'
 * @param {number}  opts.maxDepth  - Maximum link depth from seed
 * @param {number}  opts.maxPages  - Maximum number of pages to visit
 * @param {number}  opts.delayMs   - Delay between requests in milliseconds
 * @param {string|undefined} opts.proxy - Proxy URL (optional)
 * @returns {Promise<Object[]>} Array of result objects (shape depends on mode)
 */
export async function crawlWithBrowser({ seedUrl, mode, maxDepth, maxPages, delayMs, proxy }) {
  findBrowserCommand(); // Throws immediately if no browser found — propagates to tool handler
  const visited = new Set();
  const queue = [{ url: seedUrl, depth: 0 }];
  const results = [];

  while (queue.length > 0 && results.length < maxPages) {
    const { url, depth } = queue.shift();
    const normUrl = normaliseUrl(url);
    if (visited.has(normUrl)) continue;
    visited.add(normUrl);

    let html;
    try {
      html = await fetchWithBrowser(normUrl, proxy);
    } catch {
      continue; // skip pages that fail — browser error or non-zero exit
    }

    results.push(buildPageResult(normUrl, html, mode, seedUrl));

    if (depth < maxDepth) {
      enqueueLinks(html, normUrl, seedUrl, depth, visited, queue);
    }

    if (delayMs > 0 && queue.length > 0) {
      await sleep(delayMs);
    }
  }

  return results;
}

// ── Tool registration ─────────────────────────────────────────────────────────

/**
 * Register the web_crawl_browser tool on the MCP server.
 * @param {Object} server - MCP server instance
 * @param {string|undefined} proxy - Proxy URL (optional)
 */
export function configureWebCrawlBrowserTools(server, proxy) {
  server.tool(
    'web_crawl_browser',
    [
      'Crawl a website using the system-installed Chrome or Edge browser (no install required).',
      'Renders JavaScript — works on React/Angular/Vue SPAs that web_crawl cannot handle.',
      'Follows links within the same domain (BFS). Returns results in one of four modes:',
      '  • urls    — list of all discovered URLs',
      '  • summary — URL + page title + first 500 characters of text per page (default)',
      '  • full    — URL + page title + full plain-text content per page',
      '  • links   — URL + all outbound same-domain links per page (link graph)',
      'Requires Google Chrome or Microsoft Edge installed on the system.',
    ].join(' '),
    {
      url: z.string().url().describe('The seed URL to start crawling from'),
      mode: z.enum(['urls', 'summary', 'full', 'links']).default('summary').describe(
        'Output mode: urls (URL list only), summary (URL+title+snippet), full (URL+title+full text), links (URL+outbound links)'
      ),
      maxDepth: z.number().int().min(1).max(10).default(3).optional().describe(
        'Maximum link depth from the seed URL (default: 3, max: 10)'
      ),
      maxPages: z.number().int().min(1).max(200).default(50).optional().describe(
        'Maximum number of pages to visit (default: 50, max: 200)'
      ),
      delayMs: z.number().int().min(0).max(10000).default(1000).optional().describe(
        'Delay in milliseconds between page loads (default: 1000 — browser is slower than plain HTTP)'
      ),
    },
    async ({ url, mode = 'summary', maxDepth = 3, maxPages = 50, delayMs = 1000 }) => {
      try {
        const results = await crawlWithBrowser({ seedUrl: url, mode, maxDepth, maxPages, delayMs, proxy });
        const text = formatCrawlResults(results, mode);
        return { content: [{ type: 'text', text }] };
      } catch (error) {
        return {
          content: [{ type: 'text', text: error?.message || String(error) }],
          isError: true,
        };
      }
    }
  );
}
