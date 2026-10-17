import { z } from 'zod';
import * as cheerio from 'cheerio';
import { makeRequest, stripHtml } from './websearch.js';

// ── Helpers ───────────────────────────────────────────────────────────────────

/**
 * Resolve a raw href value against a base URL.
 * Returns the absolute URL string, or null if it cannot be resolved.
 * @param {string} href
 * @param {string} base
 * @returns {string|null}
 */
function resolveUrl(href, base) {
  if (!href) return null;
  try {
    return new URL(href, base).href;
  } catch {
    return null;
  }
}

/**
 * Return true if `url` lives on the same origin (protocol + hostname + port) as `base`.
 * @param {string} url
 * @param {string} base
 * @returns {boolean}
 */
function isSameOrigin(url, base) {
  try {
    return new URL(url).origin === new URL(base).origin;
  } catch {
    return false;
  }
}

/**
 * Extract all same-origin href links from an HTML document.
 * @param {string} html - Raw HTML body
 * @param {string} pageUrl - URL of the page (used to resolve relative links)
 * @param {string} seedUrl - Original seed URL (used for same-origin filtering)
 * @returns {string[]} Deduplicated array of absolute same-origin URLs
 */
export function extractLinks(html, pageUrl, seedUrl) {
  const $ = cheerio.load(html);
  const seen = new Set();
  const links = [];

  $('a[href]').each((_, el) => {
    const href = $(el).attr('href');
    const resolved = resolveUrl(href, pageUrl);
    if (!resolved) return;
    if (!isSameOrigin(resolved, seedUrl)) return;
    // Strip fragment and trailing slash for deduplication
    const normalised = resolved.split('#')[0].replace(/\/$/, '') || resolved;
    if (seen.has(normalised)) return;
    seen.add(normalised);
    links.push(normalised);
  });

  return links;
}

/**
 * Extract the page <title> text from an HTML document.
 * @param {string} html
 * @returns {string}
 */
export function extractTitle(html) {
  const $ = cheerio.load(html);
  return $('title').first().text().trim();
}

/**
 * Sleep for `ms` milliseconds.
 * @param {number} ms
 */
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// ── Core BFS crawl engine ─────────────────────────────────────────────────────

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
 * @param {string} body
 * @param {string} mode
 * @param {string} seedUrl
 * @returns {Object}
 */
function buildPageResult(url, body, mode, seedUrl) {
  if (mode === 'urls') return { url };
  if (mode === 'summary') return { url, title: extractTitle(body), text: stripHtml(body).slice(0, 500) };
  if (mode === 'full') return { url, title: extractTitle(body), text: stripHtml(body) };
  return { url, links: extractLinks(body, url, seedUrl) }; // 'links' mode
}

/**
 * Enqueue unvisited same-origin child links from a page.
 * @param {string} body
 * @param {string} pageUrl
 * @param {string} seedUrl
 * @param {number} depth
 * @param {Set<string>} visited
 * @param {Array<{url:string,depth:number}>} queue
 */
function enqueueLinks(body, pageUrl, seedUrl, depth, visited, queue) {
  const links = extractLinks(body, pageUrl, seedUrl);
  for (const link of links) {
    if (!visited.has(normaliseUrl(link))) {
      queue.push({ url: link, depth: depth + 1 });
    }
  }
}

/**
 * Crawl a website starting from `seedUrl` using BFS.
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
export async function crawl({ seedUrl, mode, maxDepth, maxPages, delayMs, proxy }) {
  const visited = new Set();
  const queue = [{ url: seedUrl, depth: 0 }];
  const results = [];

  while (queue.length > 0 && results.length < maxPages) {
    const { url, depth } = queue.shift();
    const normUrl = normaliseUrl(url);
    if (visited.has(normUrl)) continue;
    visited.add(normUrl);

    let body;
    try {
      const response = await makeRequest(normUrl, proxy);
      if (response.statusCode !== 200) continue;
      body = response.body;
    } catch {
      continue; // skip pages that fail to fetch
    }

    results.push(buildPageResult(normUrl, body, mode, seedUrl));

    if (depth < maxDepth) {
      enqueueLinks(body, normUrl, seedUrl, depth, visited, queue);
    }

    if (delayMs > 0 && queue.length > 0) {
      await sleep(delayMs);
    }
  }

  return results;
}

// ── Format output for MCP response ───────────────────────────────────────────

function titleLabel(title) {
  return title ? `**${title}**` : '(no title)';
}

function formatUrlEntry(r, idx) {
  return [`${idx} ${r.url}`];
}

function formatSummaryEntry(r, idx) {
  const entry = [`${idx} ${titleLabel(r.title)}`, `   URL: ${r.url}`];
  if (r.text) entry.push(`   ${r.text}`);
  entry.push('');
  return entry;
}

function formatFullEntry(r, idx) {
  const entry = [`${idx} ${titleLabel(r.title)}`, `   URL: ${r.url}`];
  if (r.text) entry.push(`\n${r.text}\n`);
  entry.push('');
  return entry;
}

function formatLinksEntry(r, idx) {
  const entry = [`${idx} ${r.url}`];
  if (r.links && r.links.length > 0) {
    r.links.forEach(l => entry.push(`   \u2192 ${l}`));
  } else {
    entry.push('   (no outbound links found)');
  }
  entry.push('');
  return entry;
}

const ENTRY_FORMATTERS = {
  urls: formatUrlEntry,
  summary: formatSummaryEntry,
  full: formatFullEntry,
  links: formatLinksEntry,
};

/**
 * Format crawl results into a human-readable string for MCP response.
 * @param {Object[]} results
 * @param {string} mode
 * @returns {string}
 */
export function formatCrawlResults(results, mode) {
  if (results.length === 0) return 'No pages were discovered during the crawl.';

  const formatter = ENTRY_FORMATTERS[mode] || formatUrlEntry;
  const lines = [`Crawled ${results.length} page(s):\n`];

  results.forEach((r, i) => {
    lines.push(...formatter(r, `${i + 1}.`));
  });

  return lines.join('\n');
}

// ── Tool registration ─────────────────────────────────────────────────────────

/**
 * Register the web_crawl tool on the MCP server.
 * @param {Object} server - MCP server instance
 * @param {string|undefined} proxy - Proxy URL (optional)
 */
export function configureWebCrawlTools(server, proxy) {
  server.tool(
    'web_crawl',
    [
      'Crawl a website starting from a seed URL, following links within the same domain.',
      'Returns results in one of four modes:',
      '  • urls    — list of all discovered URLs (default)',
      '  • summary — URL + page title + first 500 characters of text per page',
      '  • full    — URL + page title + full plain-text content per page',
      '  • links   — URL + all outbound same-domain links per page (link graph)',
      'Crawl stays within the same domain as the seed URL.',
      'Use maxDepth and maxPages to control scope.'
    ].join(' '),
    {
      url: z.string().url().describe('The seed URL to start crawling from'),
      mode: z.enum(['urls', 'summary', 'full', 'links']).default('urls').describe(
        'Output mode: urls (URL list only), summary (URL+title+snippet), full (URL+title+full text), links (URL+outbound links)'
      ),
      maxDepth: z.number().int().min(1).max(10).default(3).optional().describe(
        'Maximum link depth from the seed URL (default: 3, max: 10)'
      ),
      maxPages: z.number().int().min(1).max(200).default(50).optional().describe(
        'Maximum number of pages to visit (default: 50, max: 200)'
      ),
      delayMs: z.number().int().min(0).max(5000).default(500).optional().describe(
        'Delay in milliseconds between requests to avoid rate limiting (default: 500)'
      )
    },
    async ({ url, mode = 'urls', maxDepth = 3, maxPages = 50, delayMs = 500 }) => {
      try {
        const results = await crawl({ seedUrl: url, mode, maxDepth, maxPages, delayMs, proxy });
        const text = formatCrawlResults(results, mode);
        return { content: [{ type: 'text', text }] };
      } catch (error) {
        return {
          content: [{ type: 'text', text: error?.message || String(error) }],
          isError: true
        };
      }
    }
  );
}
