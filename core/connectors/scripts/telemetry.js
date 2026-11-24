#!/usr/bin/env node
/**
 * Telemetry pull + serve script.
 *
 * Usage:
 *   yarn telemetry                   # pull data from ADO then open dashboard
 *   yarn telemetry --users           # print unique user list + save users.json
 *   TELEMETRY_PORT=5000 yarn telemetry
 *
 * Prerequisites:
 *   AZURE_DEVOPS_PAT env var (or config.json at repo root)
 */
import { createServer } from 'node:http';
import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'node:fs';
import { join, dirname, extname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { execSync } from 'node:child_process';
import * as azdev from 'azure-devops-node-api';
import nodeFetch from 'node-fetch';
import { HttpsProxyAgent } from 'https-proxy-agent';
import { fetchTelemetryData } from './telemetry-pull.js';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, '..');
const DATA_DIR = join(ROOT, 'docs', 'telemetry', 'data');
const DATA_FILE = join(DATA_DIR, 'usage.log');
const USERS_FILE = join(DATA_DIR, 'users.json');
const USERS_CSV  = join(DATA_DIR, 'users.csv');
const SERVE_DIR = join(ROOT, 'docs', 'telemetry');
const PORT = Number(process.env.TELEMETRY_PORT) || 4000;
const ADO_ORG_URL = 'https://dev.azure.com/sc-ado';

// ─── Auth ─────────────────────────────────────────────────────────────────────

function getPat() {
  if (process.env.AZURE_DEVOPS_PAT) return process.env.AZURE_DEVOPS_PAT;
  try {
    const cfg = JSON.parse(readFileSync(join(ROOT, 'config.json'), 'utf-8'));
    if (cfg.AZURE_DEVOPS_PAT) return cfg.AZURE_DEVOPS_PAT;
  } catch { /* config.json absent */ }
  throw new Error(
    'No PAT found. Set AZURE_DEVOPS_PAT environment variable or add it to config.json.'
  );
}

function getProxy() {
  if (process.env.HTTPS_PROXY) return process.env.HTTPS_PROXY;
  try {
    const cfg = JSON.parse(readFileSync(join(ROOT, 'config.json'), 'utf-8'));
    if (cfg.HTTPS_PROXY) return cfg.HTTPS_PROXY;
  } catch { /* config.json absent */ }
  return null; // No proxy configured
}

// ─── Pull ─────────────────────────────────────────────────────────────────────

async function pull() {
  console.log('[Telemetry] Fetching usage.log from ADO...');

  const HTTPS_PROXY = getProxy();
  if (HTTPS_PROXY) {
    process.env.HTTPS_PROXY = HTTPS_PROXY;
    console.error("Proxy in use for Azure DevOps requests:", process.env.HTTPS_PROXY);
  }
  const pat = getPat();
  const authHandler = azdev.getPersonalAccessTokenHandler(pat);
  const connection = new azdev.WebApi(ADO_ORG_URL, authHandler, {
    ignoreSslError: true,
  });

  const content = await fetchTelemetryData(connection);

  if (!existsSync(DATA_DIR)) mkdirSync(DATA_DIR, { recursive: true });
  writeFileSync(DATA_FILE, content, 'utf-8');
  const lines = content.trim().split('\n').filter(Boolean).length;
  console.log(`[Telemetry] Saved ${lines} record(s) to docs/telemetry/data/usage.log`);
}

// ─── Serve ────────────────────────────────────────────────────────────────────

const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.js':   'application/javascript; charset=utf-8',
  '.css':  'text/css; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.log':  'text/plain; charset=utf-8',
  '.ico':  'image/x-icon',
};

function startServer() {
  return new Promise((resolve) => {
    const server = createServer((req, res) => {
      let filePath = join(SERVE_DIR, req.url === '/' ? '/dashboard.html' : req.url);
      // strip query strings
      filePath = filePath.split('?')[0];

      try {
        const content = readFileSync(filePath);
        const ext = extname(filePath).toLowerCase();
        res.writeHead(200, { 'Content-Type': MIME[ext] || 'application/octet-stream' });
        res.end(content);
      } catch {
        res.writeHead(404, { 'Content-Type': 'text/plain' });
        res.end('Not found');
      }
    });

    server.listen(PORT, '127.0.0.1', () => {
      console.log(`[Telemetry] Dashboard running at http://localhost:${PORT}`);
      resolve(server);
    });

    server.on('error', (err) => {
      if (err.code === 'EADDRINUSE') {
        console.error(`[Telemetry] Port ${PORT} is in use. Set TELEMETRY_PORT to use another port.`);
      } else {
        console.error('[Telemetry] Server error:', err.message);
      }
      process.exit(1);
    });
  });
}

function openBrowser(url) {
  try {
    let cmd;
    if (process.platform === 'darwin') {
      cmd = `open "${url}"`;
    } else if (process.platform === 'win32') {
      cmd = `start "" "${url}"`;
    } else {
      cmd = `xdg-open "${url}"`;
    }
    execSync(cmd, { stdio: 'ignore' });
  } catch {
    // Non-fatal — user can open the URL manually
  }
}

// ─── Users Mode ───────────────────────────────────────────────────────────────

const ADO_VSSPS_URL = 'https://vssps.dev.azure.com/sc-ado';
let _usersHttpWarnedOnce = false;

function _makeAdoLimiter(concurrency) {
  let active = 0;
  const queue = [];
  function _advance() { active--; if (queue.length) queue.shift()(); }
  return fn => new Promise((res, rej) => {
    const run = () => { active++; Promise.resolve(fn()).then(res, rej).finally(_advance); };
    active < concurrency ? run() : queue.push(run);
  });
}

const _adoLimiter = _makeAdoLimiter(15);
const _adoHitsCache = new Map();

async function _doAdoFetch(filter, value, creds, agent) {
  const url = `${ADO_VSSPS_URL}/_apis/identities?searchFilter=${filter}&filterValue=${encodeURIComponent(value)}&api-version=7.1`;
  const res = await nodeFetch(url, { headers: { Authorization: `Basic ${creds}` }, agent });
  if (!res.ok) return [];
  return (await res.json())?.value ?? [];
}

async function _adoFetchHits(filter, value, pat, agent) {
  const key = `${filter}::${value.toLowerCase()}`;
  if (_adoHitsCache.has(key)) return _adoHitsCache.get(key);
  const creds = Buffer.from(`:${pat}`).toString('base64');
  const promise = _adoLimiter(async () => {
    try {
      return await _doAdoFetch(filter, value, creds, agent);
    } catch (e) {
      if (!_usersHttpWarnedOnce) console.warn(`  ⚠  ADO request failed: ${e?.message}`);
      _usersHttpWarnedOnce = true;
      return [];
    }
  });
  _adoHitsCache.set(key, promise);
  return promise;
}

function _extractEmail(hit) {
  return hit?.properties?.Mail?.$value || hit?.mailAddress || '';
}

/**
 * Resolve a telemetry display name → email using a 3-step cascade:
 *   1. Reverse "First [Middle] Last" → "Last, First [Middle]" (sc-ado customDisplayName format)
 *      and find exact providerDisplayName match; extract properties.Mail.$value
 *   2. Direct General search (handles names already in Last,First or single-token form)
 *   3. Per-token convergence — all long tokens resolve to the same identity
 */
async function resolveEmailByName(name, pat, agent) {
  const nameLower = name.toLowerCase();
  const parts = name.trim().split(/\s+/);

  // Step 1: multi-depth reversal (sc-ado customDisplayName is "Surname [Initial], GivenName")
  // Surnames can span 1, 2, or 3 trailing words: try each depth.
  if (parts.length >= 2) {
    const depths = Math.min(3, parts.length - 1);
    for (let d = 1; d <= depths; d++) {
      const surname = parts.slice(parts.length - d).join(' ');
      const given   = parts.slice(0, parts.length - d).join(' ');
      const reversed = `${surname}, ${given}`;
      const hits = await _adoFetchHits('General', reversed, pat, agent);
      const exact = hits.find(h => h?.providerDisplayName?.toLowerCase() === nameLower);
      if (exact) return _extractEmail(exact);
    }
  }

  // Step 2: direct name search (fallback for already-reversed or single-token names)
  const hits2 = await _adoFetchHits('General', name, pat, agent);
  const exact2 = hits2.find(h => h?.providerDisplayName?.toLowerCase() === nameLower);
  if (exact2) return _extractEmail(exact2);

  // Step 3: per-token convergence
  const tokens = name.split(/[\s,._-]+/).filter(w => w.length > 4);
  if (tokens.length === 0) return '';
  const allHits = await Promise.all(tokens.map(t => _adoFetchHits('General', t, pat, agent)));
  const found = new Map();
  for (const hits of allHits) {
    for (const h of hits) if (h?.id) found.set(h.id, h);
  }
  if (found.size === 1) return _extractEmail([...found.values()][0]);
  return '';
}

function _initTelemetryUser(entry) {
  return {
    name: entry.user,
    sessions: 0,
    firstSeen: entry.timestamp,
    lastSeen: entry.timestamp,
    latestVersion: entry.version ?? '',
    toolsEnabled: new Set(entry.toolsEnabled ?? []),
  };
}

function _updateTelemetryUser(u, entry) {
  u.sessions++;
  if (entry.timestamp < u.firstSeen) u.firstSeen = entry.timestamp;
  if (entry.timestamp > u.lastSeen) {
    u.lastSeen = entry.timestamp;
    u.latestVersion = entry.version ?? u.latestVersion;
  }
  for (const t of (entry.toolsEnabled ?? [])) u.toolsEnabled.add(t);
}

function buildTelemetryUsers() {
  if (!existsSync(DATA_FILE)) {
    console.warn('[Users] usage.log not found \u2014 no telemetry data.');
    return [];
  }
  const raw = readFileSync(DATA_FILE, 'utf-8');
  const byUser = new Map();

  for (const line of raw.trim().split('\n')) {
    if (!line.trim()) continue;
    let entry;
    try { entry = JSON.parse(line); } catch { continue; }
    if (!entry.user) continue;

    const key = entry.user.toLowerCase();
    if (!byUser.has(key)) byUser.set(key, _initTelemetryUser(entry));
    _updateTelemetryUser(byUser.get(key), entry);
  }

  return [...byUser.values()]
    .map(u => ({
      name: u.name,
      sessions: u.sessions,
      firstSeen: u.firstSeen ? u.firstSeen.slice(0, 10) : '',
      lastSeen: u.lastSeen ? u.lastSeen.slice(0, 10) : '',
      latestVersion: u.latestVersion,
      toolsEnabled: [...u.toolsEnabled].sort((a, b) => a.localeCompare(b)).join(', '),
    }))
    .sort((a, b) => b.sessions - a.sessions);
}

function truncate(str, max) {
  return str.length > max ? str.slice(0, max - 1) + '\u2026' : str;
}

function printTable(title, headers, rows, maxWidths) {
  const widths = headers.map((h, i) => {
    const cap = maxWidths?.[i] ?? Infinity;
    return Math.min(cap, Math.max(h.length, ...rows.map(r => String(r[i] ?? '').length)));
  });

  const rowLine = (cells) =>
    '\u2502' + cells.map((c, i) => ` ${truncate(String(c ?? ''), widths[i]).padEnd(widths[i])} `).join('\u2502') + '\u2502';

  const divider = (l, m, r) => l + widths.map(w => '\u2500'.repeat(w + 2)).join(m) + r;

  console.log(`\n${title}`);
  console.log(divider('\u250c', '\u252c', '\u2510'));
  console.log(rowLine(headers));
  console.log(divider('\u251c', '\u253c', '\u2524'));
  if (rows.length === 0) {
    const totalWidth = widths.reduce((a, b) => a + b + 3, 1);
    console.log('\u2502' + ' (no data)'.padEnd(totalWidth - 2) + ' \u2502');
  } else {
    for (const r of rows) console.log(rowLine(r));
  }
  console.log(divider('\u2514', '\u2534', '\u2518'));
}

function saveUsersJson(users) {
  if (!existsSync(DATA_DIR)) mkdirSync(DATA_DIR, { recursive: true });
  writeFileSync(USERS_FILE, JSON.stringify({
    generatedAt: new Date().toISOString(),
    telemetryUsers: users,
  }, null, 2), 'utf-8');
  console.log('\u2713 Saved to docs/telemetry/data/users.json');
}

function saveUsersCsv(users) {
  if (!existsSync(DATA_DIR)) mkdirSync(DATA_DIR, { recursive: true });
  const escape = (v) => `"${String(v ?? '').replaceAll('"', '""')}"`;
  const headers = ['Name', 'Email', 'Sessions', 'First Seen', 'Last Seen', 'Version', 'Tools Enabled'];
  const rows = users.map(u =>
    [u.name, u.email ?? '', u.sessions, u.firstSeen, u.lastSeen, u.latestVersion, u.toolsEnabled].map(escape).join(',')
  );
  writeFileSync(USERS_CSV, [headers.join(','), ...rows].join('\n'), 'utf-8');
  console.log('\u2713 Saved to docs/telemetry/data/users.csv');
}

async function runUsersMode() {
  try {
    await pull();
  } catch (err) {
    console.error(`[Users] Pull failed: ${err.message}`);
    console.error('[Users] Attempting to use existing local data...');
  }

  const users = buildTelemetryUsers();
  _usersHttpWarnedOnce = false;
  _adoHitsCache.clear();

  let pat, agent;
  try {
    pat = getPat();
    const proxy = getProxy();
    if (proxy) agent = new HttpsProxyAgent(proxy);
    // Corporate CA bypass — same requirement as update-contributors.js
    process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';
  } catch {
    console.warn('[Users] No PAT configured \u2014 email resolution skipped.');
  }

  if (pat) {
    console.log(`\n\ud83d\udd0d Resolving ${users.length} user email(s) via ADO...`);
    await Promise.all(users.map(async u => {
      const email = await resolveEmailByName(u.name, pat, agent);
      u.email = email;
      const icon = email ? '\u2713' : '\u2717';
      console.log(`  ${icon} ${u.name.padEnd(35)}\u2192 ${email || 'unresolved'}`);
    }));
  }

  console.log(`\n\u2713 ${users.length} unique telemetry user(s)`);
  saveUsersJson(users);
  saveUsersCsv(users);
}

// ─── Main ─────────────────────────────────────────────────────────────────────

async function main() {
  if (process.argv.includes('--users')) {
    await runUsersMode();
    return;
  }

  try {
    await pull();
  } catch (err) {
    console.error(`[Telemetry] Pull failed: ${err.message}`);
    console.error('[Telemetry] Starting server with existing data (if any)...');
  }

  const server = await startServer();
  const url = `http://localhost:${PORT}/dashboard.html`;
  openBrowser(url);
  console.log(`[Telemetry] Press Ctrl+C to stop.`);

  process.on('SIGINT', () => {
    server.close(() => {
      console.log('\n[Telemetry] Server stopped.');
      process.exit(0);
    });
  });
}

try {
  await main();
} catch (err) {
  console.error('[Telemetry] Fatal error:', err.message);
  process.exit(1);
}
