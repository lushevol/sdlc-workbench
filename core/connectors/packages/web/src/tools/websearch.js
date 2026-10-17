import { z } from 'zod';
import https from 'node:https';
import { HttpsProxyAgent } from 'https-proxy-agent';
import { spawn, execSync } from 'node:child_process';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = fileURLToPath(new URL('.', import.meta.url));

// ── Python bridge (DDG search) ─────────────────────────────────────────────────
// DuckDuckGo uses TLS fingerprinting (JA3) to detect bots.
// Python's ssl module generates a different fingerprint that passes DDG's checks,
// while Node.js OpenSSL is blocked. This bridge mirrors the messaging package pattern.

/** Cached Python 3.x executable path. '' = not found. */
let _pythonCmd = null;

/**
 * Detect the Python 3.x executable, caching the result.
 * Tries python3, python, py (Windows). Throws if none found.
 */
export function findPython3Command() {
  if (_pythonCmd !== null) return _pythonCmd;
  const candidates = process.platform === 'win32'
    ? ['python3', 'python', 'py']
    : ['python3', 'python'];
  for (const cmd of candidates) {
    try {
      const out = execSync(`${cmd} --version`, { encoding: 'utf8', timeout: 3000, stdio: ['ignore', 'pipe', 'pipe'] });
      if (/Python 3\./i.test(out)) { _pythonCmd = cmd; return cmd; }
    } catch { /* try next */ }
  }
  _pythonCmd = '';
  throw new Error('Python 3.x not found. Install Python 3 to enable web_search.');
}

/** Reset the cached Python command. Intended for use in tests only. */
export function clearPythonCache() { _pythonCmd = null; }

/**
 * Run search-ddg.py as a subprocess, passing query + proxy via stdin JSON.
 * Returns an array of {title, url, snippet} objects.
 */
function searchViaPython(query, proxy) {
  return new Promise((resolve, reject) => {
    const pythonCmd = findPython3Command();
    const scriptPath = join(__dirname, '..', '..', 'scripts', 'search-ddg.py');
    const proc = spawn(pythonCmd, [scriptPath], { stdio: ['pipe', 'pipe', 'pipe'] });

    let stdout = '';
    let stderr = '';
    proc.stdout.on('data', (d) => { stdout += d; });
    proc.stderr.on('data', (d) => { stderr += d; });
    proc.on('error', reject);
    proc.on('close', (code) => {
      if (code !== 0) {
        reject(new Error(`Python search exited ${code}: ${stderr.trim()}`));
        return;
      }
      try {
        const result = JSON.parse(stdout.trim());
        if (result.error) reject(new Error(result.error));
        else resolve(result.results || []);
      } catch {
        reject(new Error(`Failed to parse search response: ${stdout.slice(0, 200)}`));
      }
    });

    proc.stdin.write(JSON.stringify({ query, proxy: proxy || '' }));
    proc.stdin.end();
  });
}

// ── HTTP helpers (used by web_fetch) ──────────────────────────────────────────

const REDIRECT_STATUSES = new Set([301, 302, 303, 307, 308]);

/**
 * Make an HTTP request (GET or POST) and return statusCode + body.
 * Follows redirects up to 3 hops. Honours explicit proxy or HTTPS_PROXY env var.
 * Used by the web_fetch tool (not DDG search — that uses the Python bridge).
 */
export function makeRequest(url, proxy, options = {}, postBody = null, redirectCount = 0) {
  if (redirectCount > 3) {
    return Promise.reject(new Error('Too many redirects'));
  }

  const proxyUrl = proxy ?? (process.env.HTTPS_PROXY || process.env.https_proxy);
  const parsed = new URL(url);

  const reqOptions = {
    hostname: parsed.hostname,
    path: parsed.pathname + parsed.search,
    method: postBody ? 'POST' : 'GET',
    headers: {
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
      ...options.headers
    }
  };

  if (proxyUrl) {
    reqOptions.agent = new HttpsProxyAgent(proxyUrl);
  }

  return new Promise((resolve, reject) => {
    const req = https.request(reqOptions, (res) => {
      if (REDIRECT_STATUSES.has(res.statusCode) && res.headers.location) {
        res.resume();
        const nextUrl = new URL(res.headers.location, url).href;
        resolve(makeRequest(nextUrl, proxy, options, null, redirectCount + 1));
        return;
      }

      let body = '';
      res.on('data', (chunk) => { body += chunk; });
      res.on('end', () => resolve({ statusCode: res.statusCode, body }));
    });
    req.on('error', reject);
    if (postBody) req.write(postBody);
    req.end();
  });
}

/**
 * Parse DuckDuckGo Lite HTML into structured [{title, url, snippet}] results.
 */
export function parseDdgResults(html, maxResults = 10) {
  const linkPat = /<a[^>]+href=['"]([^'"]+)['"][^>]+class=['"]result-link['"][^>]*>([\s\S]*?)<\/a>/gi;
  const snipPat = /class=['"]result-snippet['"][^>]*>([\s\S]*?)<\/td>/gi;

  const stripTags = (s) => s.replace(/<[^>]+>/g, '').trim();
  const unescape = (s) => s
    .replaceAll('&amp;', '&').replaceAll('&lt;', '<').replaceAll('&gt;', '>')
    .replaceAll('&quot;', '"').replaceAll('&#39;', "'").replaceAll('&nbsp;', ' ');
  const clean = (s) => unescape(stripTags(s)).replace(/\s+/g, ' ').trim();

  const links = [];
  let m;
  // eslint-disable-next-line no-cond-assign
  while ((m = linkPat.exec(html)) !== null) {
    links.push({ url: m[1], title: clean(m[2]) });
  }

  const snippets = [];
  // eslint-disable-next-line no-cond-assign
  while ((m = snipPat.exec(html)) !== null) {
    snippets.push(clean(m[1]));
  }

  const results = [];
  for (let i = 0; i < Math.min(links.length, maxResults); i++) {
    const { title, url } = links[i];
    if (title && url) {
      results.push({ title, url, snippet: snippets[i] || '' });
    }
  }
  return results;
}

/**
 * Strip HTML tags and collapse whitespace, returning plain text.
 * Used by web_fetch.
 */
export function stripHtml(html) {
  return html
    .replace(/<script[\s\S]*?<\/script>/gi, ' ')
    .replace(/<style[\s\S]*?<\/style>/gi, ' ')
    .replace(/<[^>]+>/g, ' ')
    .replaceAll('&nbsp;', ' ')
    .replaceAll('&amp;', '&')
    .replaceAll('&lt;', '<')
    .replaceAll('&gt;', '>')
    .replaceAll('&quot;', '"')
    .replaceAll('&#39;', "'")
    .replace(/\s+/g, ' ')
    .trim();
}

const MAX_RESPONSE_CHARS = 15000;

// ── Tool registration ──────────────────────────────────────────────────────────

/**
 * Register web_search and web_fetch tools on the MCP server.
 * @param {Object} server - MCP server instance
 * @param {string|undefined} proxy - Explicit proxy URL (or undefined to use env var)
 */
export function configureWebSearchTools(server, proxy) {
  // ── web_search ───────────────────────────────────────────────────────────────
  server.tool(
    'web_search',
    'Search the web using DuckDuckGo Lite (no API key required). Returns structured results with title, URL, and snippet.',
    {
      query: z.string().describe('The search query')
    },
    async ({ query }) => {
      try {
        const results = await searchViaPython(query, proxy);

        if (results.length === 0) {
          return { content: [{ type: 'text', text: 'No results found.' }] };
        }

        const formatted = results
          .map((r, i) => `${i + 1}. **${r.title}**\n   URL: ${r.url}\n   ${r.snippet}`)
          .join('\n\n');
        return { content: [{ type: 'text', text: formatted }] };
      } catch (error) {
        return {
          content: [{ type: 'text', text: error?.message || String(error) }],
          isError: true
        };
      }
    }
  );

  // ── web_fetch ────────────────────────────────────────────────────────────────
  server.tool(
    'web_fetch',
    'Fetch and read the plain-text content of a specific URL. Use after web_search to read a result page in full.',
    {
      url: z.string().url().describe('The full HTTPS URL to fetch')
    },
    async ({ url }) => {
      try {
        const { statusCode, body } = await makeRequest(url, proxy);

        if (statusCode !== 200) {
          return {
            content: [{ type: 'text', text: `Fetch request failed with HTTP ${statusCode}` }],
            isError: true
          };
        }

        const text = stripHtml(body).slice(0, MAX_RESPONSE_CHARS);
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

