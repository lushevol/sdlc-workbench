#!/usr/bin/env node

/**
 * update-contributors.js
 *
 * Scans git log to build a Contributors table in README.md.
 * Deduplication is fully automatic — no .mailmap required:
 *   1. Emails that resolve to an ADO GUID are merged per GUID.
 *   2. Unresolved emails whose name matches (exact or word-overlap) a resolved
 *      name are folded into that resolved entry.
 *   3. Remaining truly distinct names get their own row.
 *
 * Resolution cascade:
 *   Step 1:   General search by email.
 *   Step 1.2: MailAddress filter (more precise for email lookups).
 *   Step 1.3: AccountName using the email local-part.
 *   Step 1.5: Full display-name unique search (unique hit only).
 *   Step 1.6: Transpose "Last, First" → "First Last" (unique hit only).
 *   Step 2:   Per-token name search convergence.
 *   Step 3-4: Bank ID fallbacks (numeric IDs in email local-part or name).
 *
 * Flags:
 *   --debug   Print verbose resolution traces to stderr.
 */

import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { execSync } from 'node:child_process';
import nodeFetch from 'node-fetch';
import { HttpsProxyAgent } from 'https-proxy-agent';

process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, '..');
const readmePath = join(root, 'README.md');
const logPath = join(root, 'readme-update.log');

let DEBUG = process.argv.includes('--debug');
const PROBE_AVATARS = process.argv.includes('--probe-avatars');

const START_MARKER = '<!-- CONTRIBUTORS-START -->';
const END_MARKER = '<!-- CONTRIBUTORS-END -->';

const ADO_ORG_URL = 'https://dev.azure.com/sc-ado';
const ADO_VSSPS_URL = 'https://vssps.dev.azure.com/sc-ado';

// SCB ZScaler proxy fallback — mirrors copilot-cli-setup.py
const DEFAULT_PROXY_URL = 'http://gateway.zscloud.net:443';
const BANKID_EMAIL_DOMAIN = 'zone1.scb.net';

// Side-effect log: email → { how, guid } — populated during resolution
const _resolutionLog = new Map();
// Flag to avoid repeating the same HTTP error warning on every request
let _httpWarnedOnce = false;
// Set to true when a proxy ETIMEDOUT is detected — triggers automatic ZScaler fallback retry
let _proxyTimedOut = false;

const BOT_PATTERNS = [
  /@users\.noreply\./i,
  /noreply/i,
  /build-agent/i,
  /ado-pipeline/i,
  /azure-devops/i,
  /vstfs/i,
  /^svc\./i,
];

function isBot(name, email) {
  return BOT_PATTERNS.some(re => re.test(`${name}|${email}`));
}

function loadConfig() {
  let pat = process.env.AZURE_DEVOPS_PAT || null;
  let proxy = process.env.HTTPS_PROXY || null;
  const configPath = join(root, 'config.json');
  if (existsSync(configPath)) {
    try {
      const cfg = JSON.parse(readFileSync(configPath, 'utf8'));
      if (!pat) pat = cfg.AZURE_DEVOPS_PAT || null;
      if (!proxy) proxy = cfg.HTTPS_PROXY || null;
    } catch { /* ignore */ }
  }
  // Fall back to SCB ZScaler proxy if nothing configured
  if (!proxy) proxy = DEFAULT_PROXY_URL;
  return { pat, proxy };
}

// Strip ASCII and Unicode curly quotes (e.g. git mis-configs like "1357492")
const STRIP_QUOTES_RE = /["\u201c\u201d\u2018\u2019]/g;

function getRawEntries() {
  let raw;
  try {
    raw = execSync('git log --format="%H|%an|%ae"', {
      cwd: root, encoding: 'utf8', stdio: ['pipe', 'pipe', 'pipe'],
    });
  } catch {
    console.warn('⚠ Could not read git log — is this a git repository?');
    return new Map();
  }

  const byEmail = new Map();
  for (const line of raw.trim().split('\n')) {
    if (!line.trim()) continue;
    // Format: <hash>|<name>|<email>
    const firstPipe = line.indexOf('|');
    if (firstPipe === -1) continue;
    const commitHash = line.slice(0, firstPipe).trim();
    const rest = line.slice(firstPipe + 1);
    const secondPipe = rest.indexOf('|');
    if (secondPipe === -1) continue;
    const name = rest.slice(0, secondPipe).trim().replace(STRIP_QUOTES_RE, '');
    const email = rest.slice(secondPipe + 1).trim().toLowerCase().replace(STRIP_QUOTES_RE, '');
    if (isBot(name, email)) continue;
    if (byEmail.has(email)) {
      const entry = byEmail.get(email);
      entry.commits++;
      // Keep up to 3 most-recent hashes (git log is newest-first)
      if (entry.hashes.length < 3) entry.hashes.push(commitHash);
    } else {
      byEmail.set(email, { name, email, commits: 1, hashes: [commitHash] });
    }
  }
  console.log(`📋 Git log scanned: ${byEmail.size} unique contributor(s) found`);
  return byEmail;
}

function buildBankIdEmail(bankId) {
  return `${bankId}@${BANKID_EMAIL_DOMAIN}`;
}

function buildAvatarUrl(guid) {
  return `${ADO_ORG_URL}/_api/_common/identityImage?id=${guid}&size=2`;
}

/**
 * Extract the best avatar URL from an ADO identity hit.
 * Prefers _links.avatar.href (canonical REST endpoint) over the legacy identityImage URL.
 * The _links URL works for both MSA and AAD identities and is what ADO itself uses.
 */
function extractAvatarUrl(hit) {
  const linkUrl = hit?._links?.avatar?.href;
  if (linkUrl) {
    // Ensure size=2 is appended (ADO's _links omits it by default)
    return linkUrl.includes('size=') ? linkUrl : `${linkUrl}?size=2`;
  }
  return buildAvatarUrl(hit.id);
}

function _noteResolution(email, how, guid) {
  _resolutionLog.set(email, { how, guid });
}

// ---------------------------------------------------------------------------
// Concurrency limiter — caps simultaneous ADO HTTP requests to avoid 429s
// ---------------------------------------------------------------------------
const ADO_CONCURRENCY = 15;

function makeLimiter(concurrency) {
  let active = 0;
  const queue = [];
  return function limit(fn) {
    return new Promise((resolve, reject) => {
      const run = () => {
        active++;
        Promise.resolve(fn()).then(resolve, reject).finally(() => {
          active--;
          if (queue.length) queue.shift()();
        });
      };
      if (active < concurrency) run();
      else queue.push(run);
    });
  };
}

const _limiter = makeLimiter(ADO_CONCURRENCY);

// ---------------------------------------------------------------------------
// Request cache — Promise<hit[]> keyed by "FILTER::value"
// Identical queries (e.g. same name token for different emails) share one request.
// ---------------------------------------------------------------------------
const _adoCache = new Map();

async function _adoFetchHits(searchFilter, filterValue, pat, agent) {
  const key = `${searchFilter}::${filterValue.toLowerCase()}`;
  if (_adoCache.has(key)) {
    if (DEBUG) console.error(`  [debug] cache hit: ${key}`);
    return _adoCache.get(key);
  }

  const promise = _limiter(async () => {
    try {
      const creds = Buffer.from(`:${pat}`).toString('base64');
      const url = `${ADO_VSSPS_URL}/_apis/identities?searchFilter=${searchFilter}&filterValue=${encodeURIComponent(filterValue)}&api-version=7.1`;
      if (DEBUG) console.error(`  [debug] GET ${url}`);
      const res = await nodeFetch(url, { headers: { Authorization: `Basic ${creds}` }, agent });
      if (!res.ok) {
        if (DEBUG) console.error(`  [debug] response: ${res.status}`);
        // Always surface auth/proxy errors — these explain why everyone is unresolved
        if (res.status === 401 || res.status === 403) {
          console.warn(`  ⚠  ADO returned ${res.status} — PAT may lack "Identity (Read)" scope or is expired.`);
        } else if (res.status === 407) {
          console.warn(`  ⚠  ADO returned 407 — proxy authentication required. Check HTTPS_PROXY config.`);
        } else if (!_httpWarnedOnce) {
          console.warn(`  ⚠  ADO returned ${res.status} for ${searchFilter}::${filterValue}`);
        }
        _httpWarnedOnce = true;
        return [];
      }
      const hits = (await res.json())?.value ?? [];
      if (DEBUG) console.error(`  [debug] ${searchFilter} hits: ${hits.length}`);
      return hits;
    } catch (e) {
      if (DEBUG) console.error(`  [debug] exception: ${e?.message}`);
      if (!_httpWarnedOnce) {
        if (e?.code === 'ETIMEDOUT' || e?.message?.includes('ETIMEDOUT')) {
          _proxyTimedOut = true;
          console.warn(`  ⚠  ADO request timed out — proxy unreachable (${e.message.split(' ').pop()})`);
          console.warn(`     Will automatically retry with ZScaler fallback: ${DEFAULT_PROXY_URL}`);
        } else {
          console.warn(`  ⚠  ADO request failed: ${e?.message}`);
        }
      } else if ((e?.code === 'ETIMEDOUT' || e?.message?.includes('ETIMEDOUT')) && !_proxyTimedOut) {
        _proxyTimedOut = true;
      }
      _httpWarnedOnce = true;
      return [];
    }
  });

  _adoCache.set(key, promise);
  return promise;
}

async function adoIdentitySearch(filterValue, pat, agent) {
  const hits = await _adoFetchHits('General', filterValue, pat, agent);
  return hits[0] ?? null;
}

/** Returns a result ONLY when exactly one hit exists. */
async function adoIdentitySearchUnique(filterValue, pat, agent) {
  const hits = await _adoFetchHits('General', filterValue, pat, agent);
  if (DEBUG) console.error(`  [debug] unique search ${JSON.stringify(filterValue)} → ${hits.length} hit(s)`);
  return hits.length === 1 ? hits[0] : null;
}

/** Search by Windows login / AccountName — most reliable for SCB numeric bank IDs. */
async function adoAccountSearch(bankId, pat, agent) {
  const hits = await _adoFetchHits('AccountName', bankId, pat, agent);
  if (DEBUG) console.error(`  [debug] AccountName search ${JSON.stringify(bankId)} → ${hits.length} hit(s)`);
  return hits.length === 1 ? hits[0] : null;
}

/** Search by MailAddress filter — more precise than General for email lookups. */
async function adoMailSearch(email, pat, agent) {
  const hits = await _adoFetchHits('MailAddress', email, pat, agent);
  if (DEBUG) console.error(`  [debug] MailAddress search ${JSON.stringify(email)} → ${hits.length} hit(s)`);
  return hits.length === 1 ? hits[0] : null;
}

/** Steps 3-4: resolve via numeric bank ID embedded in email local-part or name. */
async function resolveByBankId(email, name, pat, agent) {
  // Step 3: numeric prefix of the email local-part
  const localPart = email.split('@')[0];
  const m = localPart.match(/^(\d{6,8})/);
  if (m) {
    const bankId = m[1];
    const bankIdEmail = buildBankIdEmail(bankId);
    if (bankIdEmail !== email) {
      const hit = await adoIdentitySearch(bankIdEmail, pat, agent);
      if (hit) { _noteResolution(email, 'Step 3 — bank ID zone1 email (General search)', hit.id); return { guid: hit.id, avatarUrl: extractAvatarUrl(hit) }; }
    }
    const hitAcc = await adoAccountSearch(bankId, pat, agent);
    if (hitAcc) { _noteResolution(email, 'Step 3 — bank ID AccountName filter', hitAcc.id); return { guid: hitAcc.id, avatarUrl: extractAvatarUrl(hitAcc) }; }
    const hitUniq = await adoIdentitySearchUnique(bankId, pat, agent);
    if (hitUniq) { _noteResolution(email, 'Step 3 — bank ID unique General search', hitUniq.id); return { guid: hitUniq.id, avatarUrl: extractAvatarUrl(hitUniq) }; }
  }

  // Step 4: name is itself a bare bank ID (e.g. git name configured as 1357492)
  if (/^\d{6,8}$/.test(name)) {
    const hit = await adoIdentitySearch(buildBankIdEmail(name), pat, agent);
    if (hit) { _noteResolution(email, 'Step 4 — bare bank ID name → zone1 email', hit.id); return { guid: hit.id, avatarUrl: extractAvatarUrl(hit) }; }
    const hitAcc = await adoAccountSearch(name, pat, agent);
    if (hitAcc) { _noteResolution(email, 'Step 4 — bare bank ID AccountName filter', hitAcc.id); return { guid: hitAcc.id, avatarUrl: extractAvatarUrl(hitAcc) }; }
  }

  return null;
}

/**
 * Resolve email → ADO GUID using a full cascade of strategies.
 *
 * Step 1:   General search by email.
 * Step 1.2: MailAddress filter.
 * Step 1.3: AccountName using email local-part.
 * Step 1.5: Full display-name unique search.
 * Step 1.6: Transpose "Last, First" → "First Last".
 * Step 2:   Per-token name searches — fired in parallel, accept only when all converge on one GUID.
 * Step 3-4: Bank ID fallbacks.
 */
async function resolveAdoIdentity(email, name, pat, agent) {
  // Step 1: General email search
  const byEmail = await adoIdentitySearch(email, pat, agent);
  if (byEmail) { _noteResolution(email, 'Step 1 — General email search', byEmail.id); return { guid: byEmail.id, avatarUrl: extractAvatarUrl(byEmail) }; }

  // Step 1.2: MailAddress filter
  const byMail = await adoMailSearch(email, pat, agent);
  if (byMail) { _noteResolution(email, 'Step 1.2 — MailAddress filter', byMail.id); return { guid: byMail.id, avatarUrl: extractAvatarUrl(byMail) }; }

  // Step 1.3: AccountName using email local-part (skip bare numeric local-parts — handled in step 3)
  const localPart = email.split('@')[0];
  if (localPart && !/^\d+$/.test(localPart)) {
    const byAccount = await adoAccountSearch(localPart, pat, agent);
    if (byAccount) { _noteResolution(email, 'Step 1.3 — AccountName (email local-part)', byAccount.id); return { guid: byAccount.id, avatarUrl: extractAvatarUrl(byAccount) }; }
  }

  // Step 1.5: full display-name unique search
  const byDisplayName = await adoIdentitySearchUnique(name, pat, agent);
  if (byDisplayName) { _noteResolution(email, 'Step 1.5 — display name unique search', byDisplayName.id); return { guid: byDisplayName.id, avatarUrl: extractAvatarUrl(byDisplayName) }; }

  // Step 1.6: transpose "Last, First" → "First Last"
  if (name.includes(',')) {
    const [last, first] = name.split(',', 2);
    const transposed = `${first.trim()} ${last.trim()}`;
    const byTransposed = await adoIdentitySearchUnique(transposed, pat, agent);
    if (byTransposed) { _noteResolution(email, "Step 1.6 — transposed 'First Last' name search", byTransposed.id); return { guid: byTransposed.id, avatarUrl: extractAvatarUrl(byTransposed) }; }
  }

  // Step 2: per-token searches fired in PARALLEL — accept only when all converge on one GUID
  const tokens = name.split(/[\s,._-]+/).filter(w => w.length > 4);
  if (tokens.length > 0) {
    const tokenResults = await Promise.all(tokens.map(t => adoIdentitySearch(t, pat, agent)));
    const found = new Map();
    for (const identity of tokenResults) {
      if (identity) found.set(identity.id, identity);
    }
    if (found.size === 1) {
      const [guid] = found.keys();
      const hit = found.get(guid);
      _noteResolution(email, 'Step 2 — per-token name search convergence', guid);
      return { guid, avatarUrl: extractAvatarUrl(hit) };
    }
  }

  return resolveByBankId(email, name, pat, agent);
}

/**
 * Extract significant words (>2 chars) from a name for overlap matching.
 * Using 3+ chars catches short surnames (Tam, Low, Pan, Ken, etc.)
 */
function nameWords(name) {
  return new Set(
    name.toLowerCase().split(/[\s,._-]+/).filter(w => w.length > 2)
  );
}

/**
 * Returns true if names share at least one significant word.
 */
function nameOverlaps(nameA, nameB) {
  const wordsA = nameWords(nameA);
  const wordsB = nameWords(nameB);
  for (const w of wordsA) {
    if (wordsB.has(w)) return true;
  }
  return false;
}

/**
 * Three-pass merge:
 * 1. GUID → merge all emails sharing the same ADO GUID into one row.
 * 2. Name-exact → fold unresolved emails whose name (case-insensitive) matches a resolved name.
 * 3. Word-overlap → fold unresolved emails sharing a significant word with exactly one resolved name.
 * 4. Standalone → anything remaining gets its own row (no image).
 */
function mergeEntries(byEmail, guidMap) {
  const byGuid = new Map();

  // Pass 1: GUID merge
  for (const [email, entry] of byEmail) {
    const identity = guidMap.get(email);
    if (!identity) continue;
    const { guid } = identity;
    if (byGuid.has(guid)) {
      const existing = byGuid.get(guid);
      existing.commits += entry.commits;
      if (entry.commits > existing._topCommits) {
        // Prefer proper display names over bare numeric bank IDs
        if (!/^\d+$/.test(entry.name)) {
          existing.name = entry.name;
        }
        existing._topCommits = entry.commits;
      }
    } else {
      byGuid.set(guid, {
        name: entry.name,
        commits: entry.commits,
        avatarUrl: identity.avatarUrl ?? buildAvatarUrl(guid),
        _topCommits: entry.commits,
      });
    }
  }

  // Resolved names map: nameLower → guid
  const resolvedNameToGuid = new Map();
  for (const [guid, data] of byGuid) {
    resolvedNameToGuid.set(data.name.toLowerCase(), guid);
  }

  const unresolved = [];
  for (const [email, entry] of byEmail) {
    if (guidMap.get(email)) continue;
    unresolved.push(entry);
  }

  const standalone = new Map();

  for (const entry of unresolved) {
    const nameLower = entry.name.toLowerCase();

    // Pass 2: exact name match
    if (resolvedNameToGuid.has(nameLower)) {
      byGuid.get(resolvedNameToGuid.get(nameLower)).commits += entry.commits;
      continue;
    }

    // Pass 3: word-overlap match (merge only if exactly one resolved name matches)
    const matches = [...resolvedNameToGuid.entries()].filter(([rName]) =>
      nameOverlaps(entry.name, rName)
    );
    if (matches.length === 1) {
      byGuid.get(matches[0][1]).commits += entry.commits;
      continue;
    }

    // Pass 4: standalone (also dedup by name within standalones)
    if (standalone.has(nameLower)) {
      standalone.get(nameLower).commits += entry.commits;
    } else {
      standalone.set(nameLower, { name: entry.name, commits: entry.commits });
    }
  }

  return [
    ...[...byGuid.values()].map(({ name, commits, avatarUrl }) => ({ name, commits, avatarUrl })),
    ...[...standalone.values()],
  ].sort((a, b) => b.commits - a.commits);
}

const COLS_PER_ROW = 7;

function buildBlock(contributors) {
  const date = new Date().toISOString().slice(0, 10);
  const colWidth = Math.floor(100 / COLS_PER_ROW);
  const lines = [START_MARKER, `## Contributors ✨`, '', `*(last-updated ${date})*`, ''];

  lines.push('<table>');
  lines.push('  <tbody>');

  for (let i = 0; i < contributors.length; i += COLS_PER_ROW) {
    const row = contributors.slice(i, i + COLS_PER_ROW);
    lines.push('    <tr>');
    for (const c of row) {
      const cell = c.avatarUrl
        ? `      <td align="center" valign="top" width="${colWidth}%">\n        <img src="${c.avatarUrl}" width="80px" alt="${c.name}"/><br/>\n        <sub><b>${c.name}</b></sub>\n      </td>`
        : `      <td align="center" valign="top" width="${colWidth}%">\n        <br/>\n        <b>${c.name}</b>\n      </td>`;
      lines.push(cell);
    }
    lines.push('    </tr>');
  }

  lines.push('  </tbody>');
  lines.push('</table>');
  lines.push('');
  lines.push(END_MARKER);
  return lines.join('\n');
}

function writeLog(byEmail, guidMap) {
  const resolvedCount = [...guidMap.values()].filter(Boolean).length;
  const unresolvedCount = [...guidMap.values()].filter(v => !v).length;
  const now = new Date().toISOString().replace('T', ' ').slice(0, 19);

  const lines = [
    'README Contributors Update Log',
    `Generated : ${now}`,
    `Repository: ${root}`,
    '='.repeat(70),
    '',
    `Emails processed : ${byEmail.size}`,
    `ADO resolved     : ${resolvedCount}`,
    `Unresolved       : ${unresolvedCount}`,
    '',
    '-'.repeat(70),
    '',
  ];

  const sorted = [...byEmail.entries()].sort(([, a], [, b]) =>
    a.name.toLowerCase().localeCompare(b.name.toLowerCase())
  );

  for (const [email, entry] of sorted) {
    const { name, commits, hashes = [] } = entry;
    const resolution = guidMap.get(email);
    const logEntry = _resolutionLog.get(email) ?? {};

    let commitLabel = `git log (${commits} commit${commits !== 1 ? 's' : ''})`;
    if (hashes.length) {
      const short = hashes.map(h => h.slice(0, 8));
      const more = commits > hashes.length ? `  (+${commits - hashes.length} more)` : '';
      commitLabel += `  hashes: ${short.join(', ')}${more}`;
    }

    lines.push(`  ${name}`);
    lines.push(`    Email  : ${email}`);
    lines.push(`    Source : ${commitLabel}`);
    if (resolution) {
      const how = logEntry.how ?? 'resolved (method not recorded)';
      lines.push(`    ADO    : ${how}`);
      lines.push(`    GUID   : ${resolution.guid}`);
    } else {
      lines.push(`    ADO    : UNRESOLVED — no account found in sc-ado`);
      lines.push(`    GUID   : —`);
    }
    lines.push('');
  }

  writeFileSync(logPath, lines.join('\n'), 'utf8');
  console.log(`✓ Resolution log written → readme-update.log`);
}

function updateReadme(block) {
  const content = readFileSync(readmePath, 'utf8');
  const startIdx = content.indexOf(START_MARKER);
  const endIdx = content.indexOf(END_MARKER);
  if (startIdx === -1 || endIdx === -1) {
    console.error('ERROR: Could not find CONTRIBUTORS markers in README.md');
    process.exit(1);
  }
  writeFileSync(readmePath,
    content.slice(0, startIdx) + block + content.slice(endIdx + END_MARKER.length),
    'utf8'
  );
}

/**
 * HEAD-probe each avatar URL with the PAT to verify they are reachable.
 * Run with --probe-avatars to diagnose image loading issues.
 */
async function probeAvatarUrls(contributors, pat, agent) {
  const withAvatars = contributors.filter(c => c.avatarUrl);
  if (withAvatars.length === 0) {
    console.log('⚠  No avatar URLs to probe.');
    return;
  }
  console.log(`\n🔎 Probing ${withAvatars.length} avatar URL(s)...`);
  const creds = Buffer.from(`:${pat}`).toString('base64');
  await Promise.all(withAvatars.map(async c => {
    try {
      const res = await nodeFetch(c.avatarUrl, {
        method: 'HEAD',
        headers: { Authorization: `Basic ${creds}` },
        agent,
      });
      const icon = res.ok ? '✓' : '✗';
      console.log(`  ${icon} [${res.status}] ${c.name}`);
      console.log(`       ${c.avatarUrl}`);
      if (!res.ok) console.log(`       ← ${res.statusText}`);
    } catch (e) {
      console.log(`  ✗ [ERR] ${c.name} — ${e.message}`);
      console.log(`       ${c.avatarUrl}`);
    }
  }));
}

async function main() {
  const byEmail = getRawEntries();
  if (byEmail.size === 0) {
    console.warn('⚠ No contributors found — README.md not updated.');
    return;
  }

  const { pat, proxy } = loadConfig();

  console.log(`🔑 Config: PAT=${pat ? 'found ✓' : 'NOT FOUND ✗'} | Proxy=${proxy || 'none'}`);
  if (DEBUG) {
    console.error(`[debug] PAT loaded: ${pat ? 'yes' : 'no'}`);
    console.error(`[debug] Proxy: ${proxy || 'none'}`);
  }

  const agent = proxy ? new HttpsProxyAgent(proxy) : undefined;
  let contributors;

  if (pat) {
    const total = byEmail.size;

    /**
     * Run one full resolution pass. Clears module-level state first so that
     * retries with a different proxy agent start clean.
     */
    async function runResolutionPass(passAgent, label) {
      _adoCache.clear();
      _resolutionLog.clear();
      _httpWarnedOnce = false;
      _proxyTimedOut = false;

      let resolved = 0;
      let unresolved = 0;
      console.log(`\n🔍 Resolving ${total} contributor(s) against ADO${label ? ` (${label})` : ''}...`);

      const guidMap = new Map();
      await Promise.all(
        [...byEmail.keys()].map(async email => {
          const entry = byEmail.get(email);
          if (DEBUG) console.error(`[debug] resolving: ${entry.name} <${email}>`);
          const identity = await resolveAdoIdentity(email, entry.name, pat, passAgent);
          guidMap.set(email, identity);
          if (identity) {
            resolved++;
            const how = _resolutionLog.get(email)?.how ?? 'resolved';
            console.log(`  ✓ ${entry.name.padEnd(30)} → ${identity.guid.slice(0, 8)}… (${how})`);
            if (DEBUG) console.error(`     avatar: ${identity.avatarUrl}`);
          } else {
            unresolved++;
            if (!_resolutionLog.has(email)) {
              _resolutionLog.set(email, { how: 'all strategies exhausted — no account in sc-ado' });
            }
            console.log(`  ✗ ${entry.name.padEnd(30)} → unresolved (${email})`);
          }
        })
      );

      console.log(`\n📊 Resolution complete: ${resolved}/${total} resolved, ${unresolved} unresolved`);
      return { guidMap, resolved, unresolved };
    }

    let { guidMap, resolved, unresolved } = await runResolutionPass(agent);

    // If configured proxy timed out and it differs from the ZScaler default, auto-retry
    if (_proxyTimedOut && proxy !== DEFAULT_PROXY_URL) {
      console.log(`\n🔄 Configured proxy timed out. Retrying with ZScaler fallback: ${DEFAULT_PROXY_URL}`);
      const fallbackAgent = new HttpsProxyAgent(DEFAULT_PROXY_URL);
      ({ guidMap, resolved, unresolved } = await runResolutionPass(fallbackAgent, 'ZScaler fallback'));
    }

    contributors = mergeEntries(byEmail, guidMap);
    writeLog(byEmail, guidMap);

    if (PROBE_AVATARS) {
      await probeAvatarUrls(contributors, pat, agent);
    } else if (unresolved === total) {
      if (_httpWarnedOnce) {
        console.log('⚠  All contributors unresolved — ADO requests failed (see warning above).');
      } else {
        console.log('⚠  All contributors unresolved — check PAT permissions (Identity read scope required).');
      }
    } else {
      const withImages = contributors.filter(c => c.avatarUrl).length;
      if (withImages === 0 && resolved > 0) {
        console.log('⚠  GUIDs resolved but no avatar URLs found. Run with --probe-avatars to diagnose.');
      } else if (withImages > 0) {
        console.log(`🖼  ${withImages} avatar URL(s) embedded. Run with --probe-avatars to verify they load.`);
      }
    }
  } else {
    console.log('ℹ No AZURE_DEVOPS_PAT found — using name-based deduplication, no images.');
    console.log('  Set AZURE_DEVOPS_PAT env var or add it to config.json to enable avatars.');
    const byName = new Map();
    for (const entry of byEmail.values()) {
      const key = entry.name.toLowerCase();
      if (byName.has(key)) byName.get(key).commits += entry.commits;
      else byName.set(key, { name: entry.name, commits: entry.commits });
    }
    contributors = [...byName.values()].sort((a, b) => b.commits - a.commits);
  }

  const block = buildBlock(contributors);
  updateReadme(block);

  const withImages = contributors.filter(c => c.avatarUrl).length;
  console.log(`\n✓ README.md updated — ${contributors.length} contributor(s), ${withImages} with avatar(s)`);
}

main().catch(err => {
  console.error('ERROR:', err?.message || String(err));
  process.exit(1);
});
