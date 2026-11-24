import assert from 'node:assert/strict';
import { execFileSync, spawn } from 'node:child_process';
import { createHash } from 'node:crypto';
import { mkdtempSync, mkdirSync, readFileSync, rmSync, symlinkSync, writeFileSync } from 'node:fs';
import { createServer } from 'node:http';
import { createServer as createHttpsServer } from 'node:https';
import { connect } from 'node:net';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { createInterface } from 'node:readline';
import { fileURLToPath } from 'node:url';
import test from 'node:test';
import { confinedEvidencePath } from './release-readers.js';

const script = fileURLToPath(new URL('./release-session.js', import.meta.url));

async function fixture(t, handler, options = {}) {
  const directory = mkdtempSync(join(tmpdir(), 'release-session-'));
  const evidence = join(directory, 'evidence');mkdirSync(evidence);
  t.after(() => rmSync(directory, { recursive: true, force: true }));
  const server = options.tls ? createHttpsServer(options.tls, handler) : createServer(handler);
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  t.after(() => new Promise(resolve => { server.closeAllConnections();server.close(resolve); }));
  const base = `${options.tls ? 'https' : 'http'}://127.0.0.1:${server.address().port}`;
  if (options.certificate) writeFileSync(join(directory, 'test-root.pem'), options.certificate);
  writeFileSync(join(directory, '.env'), `AZURE_DEVOPS_ORG_URL=${base}\nAZURE_DEVOPS_PAT=fake-secret\nSONAR_BASE_URL=${base}\nSONAR_TOKEN=fake-secret\nNO_PROXY=127.0.0.1\n${options.environment || ''}`);
  const child = spawn(process.execPath, [script, '--workspace', directory, '--connector', options.connector || 'ado'], {
    env: { PATH: process.env.PATH, SystemRoot: process.env.SystemRoot, HOME: directory },
    stdio: ['pipe', 'pipe', 'pipe'],
  });
  let stderr = '';
  child.stderr.on('data', chunk => { stderr += chunk; });
  const pending = new Map();let sequence = 0;
  const lines = createInterface({ input: child.stdout });
  lines.on('line', line => {
    const response = JSON.parse(line);
    pending.get(response.id)?.resolve(response);pending.delete(response.id);
  });
  child.on('error', failure => { for (const item of pending.values()) item.reject(failure); });
  child.on('close', () => { for (const item of pending.values()) item.reject(new Error(`Session exited. ${stderr}`)); });
  const request = object => new Promise((resolve, reject) => {
    const id = String(++sequence);pending.set(id, { resolve, reject });child.stdin.write(`${JSON.stringify({ id, ...object })}\n`);
  });
  t.after(() => { child.kill();lines.close(); });
  const initialization = await request({ operation: 'init', allowed_tools: options.allowed || ['report_work_items'],
    run_dir: evidence, concurrency: options.concurrency || 2, request_timeout_seconds: options.timeout || 2,
    deadline_seconds: options.deadline || 10 });
  assert.equal(initialization.status, 'SUCCEEDED');
  assert.equal(initialization.endpoint, base);
  assert.doesNotMatch(JSON.stringify(initialization), /fake-secret/);
  let artifact = 0;
  return { directory, evidence, base, child, request,
    call: (tool = 'report_work_items', args = { ids: [501] }) => request({ operation: 'call', tool, arguments: args,
      evidence_path: join(evidence, `${++artifact}.json`) }),
    close: () => request({ operation: 'close' }) };
}

function json(response, data, headers = {}) {
  const bytes = JSON.stringify(data);response.writeHead(200, { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(bytes), ...headers });response.end(bytes);
}

test('RR-P2 actual HTTP concurrency is bounded and one client serves all requests', async t => {
  let active = 0;let peak = 0;let requests = 0;
  const session = await fixture(t, (request, response) => {
    assert.equal(request.headers.authorization, `Basic ${Buffer.from(':fake-secret').toString('base64')}`);
    active++;requests++;peak = Math.max(peak, active);
    setTimeout(() => { active--;json(response, { value: [{ id: 501 }] }); }, 25);
  });
  const results = await Promise.all(Array.from({ length: 8 }, () => session.call()));
  assert.ok(results.every(item => item.status === 'SUCCEEDED'));
  const closed = await session.close();
  assert.equal(requests, 8);assert.equal(peak, 2);
  assert.equal(closed.metrics.peak_concurrency, 2);
  assert.equal(closed.metrics.client_creations, 1);
  assert.equal(closed.metrics.sessions, 1);
});

test('RR-P4 an ungranted read or invalid selector sends zero HTTP requests', async t => {
  let requests = 0;
  const session = await fixture(t, (_request, response) => { requests++;json(response, {}); });
  assert.equal((await session.call('report_build_logs', { project: 'Project', buildId: 101 })).code, 'TOOL_NOT_GRANTED');
  assert.equal((await session.call('report_work_items', { ids: Array.from({ length: 201 }, (_, i) => i + 1) })).code, 'INVALID_ARGUMENT');
  assert.equal(requests, 0);assert.equal((await session.close()).metrics.requests, 0);
});

test('RR-P3 Retry-After on HTTP 200 paces the next request without replaying success', async t => {
  const times = [];
  const session = await fixture(t, (_request, response) => {
    times.push(performance.now());json(response, { value: [] }, times.length === 1 ? { 'Retry-After': '0.15' } : {});
  });
  assert.equal((await session.call()).status, 'SUCCEEDED');
  assert.equal((await session.call()).status, 'SUCCEEDED');
  assert.equal(times.length, 2);assert.ok(times[1] - times[0] >= 130);
  assert.equal((await session.close()).metrics.retries, 0);
});

test('RR-P5 large evidence is streamed with exact bytes and a small response envelope', async t => {
  const payload = JSON.stringify({ value: 'x'.repeat(5 * 1024 * 1024) });
  const session = await fixture(t, (_request, response) => {
    response.writeHead(200, { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(payload) });response.end(payload);
  });
  const result = await session.call();
  assert.equal(result.status, 'SUCCEEDED');assert.ok(JSON.stringify(result).length < 4096);
  const raw = readFileSync(result.artifact.path);
  assert.equal(raw.length, Buffer.byteLength(payload));assert.equal(raw.toString(), payload);
  assert.equal(result.artifact.sha256, createHash('sha256').update(raw).digest('hex'));
  await session.close();
});

test('Transient HTTP errors retry within the same session and retain the successful body', async t => {
  let count = 0;
  const session = await fixture(t, (_request, response) => {
    count++;
    if (count === 1) { response.writeHead(503, { 'Retry-After': '0.01' });response.end('temporary'); }
    else json(response, { value: [{ id: 501 }] });
  });
  const result = await session.call();
  assert.equal(result.status, 'SUCCEEDED');assert.equal(count, 2);
  assert.equal((await session.close()).metrics.retries, 1);
});

test('Forbidden errors retain their raw body but never retry or expose configured credentials', async t => {
  let count = 0;
  const session = await fixture(t, (_request, response) => { count++;response.writeHead(403);response.end('access denied'); });
  const result = await session.call();
  assert.equal(result.code, 'HTTP_403');assert.equal(count, 1);
  assert.equal(readFileSync(result.artifact.path, 'utf8'), 'access denied');
  assert.doesNotMatch(JSON.stringify(result), /fake-secret/);await session.close();
});

test('Evidence paths reject escape and existing files while permitting filesystem aliases', async t => {
  const directory = mkdtempSync(join(tmpdir(), 'release-paths-'));
  t.after(() => rmSync(directory, { recursive: true, force: true }));
  const root = join(directory, 'root');mkdirSync(root);
  const alias = join(directory, 'alias');symlinkSync(root, alias);
  const fs = await import('node:fs');
  assert.equal(confinedEvidencePath(fs.realpathSync(root), join(alias, 'new.json')), fs.realpathSync(root) + '/new.json');
  assert.throws(() => confinedEvidencePath(fs.realpathSync(root), join(directory, 'escape.json')));
  writeFileSync(join(root, 'existing.json'), 'preserve');
  assert.throws(() => confinedEvidencePath(fs.realpathSync(root), join(root, 'existing.json')));
  assert.equal(readFileSync(join(root, 'existing.json'), 'utf8'), 'preserve');
});

test('Sonar structured reads preserve selectors and payloads', async t => {
  let requested;
  const session = await fixture(t, (request, response) => { requested = request.url;json(response, { component: { measures: [{ metric: 'alert_status', value: 'OK' }] } }); },
    { connector: 'sonar', allowed: ['report_sonar_measures'] });
  const result = await session.call('report_sonar_measures', { component: 'quality-r1', pullRequest: '17', metricKeys: 'alert_status' });
  assert.equal(result.status, 'SUCCEEDED');assert.match(requested, /pullRequest=17/);
  assert.equal(JSON.parse(readFileSync(result.artifact.path, 'utf8')).component.measures[0].value, 'OK');
  const invalid = await session.call('report_sonar_measures', { component: 'quality-r1', branch: 'main', pullRequest: '17' });
  assert.equal(invalid.code, 'INVALID_ARGUMENT');await session.close();
});

test('A collection deadline aborts active reads and releases queued requests', async t => {
  const session = await fixture(t, (_request, response) => { setTimeout(() => json(response, {}), 200); },
    { deadline: 0.05, concurrency: 1 });
  const results = await Promise.all([session.call(), session.call()]);
  assert.ok(results.every(item => item.code === 'DEADLINE_EXCEEDED'));
  assert.equal((await session.close()).metrics.requests, 1);
});

test('Source comparison semantics preserve base, target, and common-commit mode', async t => {
  const requests = [];
  const session = await fixture(t, (request, response) => { requests.push(new URL(request.url, 'http://fixture'));json(response, {}); },
    { allowed: ['report_compare', 'report_commits'] });
  const values = { project: 'Project', repository: 'r1', base: 'production', target: 'candidate' };
  await session.call('report_compare', { ...values, common: true });
  await session.call('report_compare', { ...values, common: false });
  await session.call('report_commits', values);
  assert.equal(requests[0].searchParams.get('baseVersion'), 'production');
  assert.equal(requests[0].searchParams.get('targetVersion'), 'candidate');
  assert.equal(requests[0].searchParams.get('diffCommonCommit'), 'true');
  assert.equal(requests[1].searchParams.get('diffCommonCommit'), 'false');
  assert.equal(requests[2].searchParams.get('searchCriteria.itemVersion.version'), 'production');
  assert.equal(requests[2].searchParams.get('searchCriteria.compareVersion.version'), 'candidate');
  assert.equal(requests[2].searchParams.get('searchCriteria.includeWorkItems'), 'true');
  await session.close();
});

test('Throttle evidence reduces the concurrency of subsequent HTTP attempts', async t => {
  // Given a session permits four requests and the first response asks for a delay.
  let requests = 0;let active = 0;let peak = 0;
  const session = await fixture(t, (_request, response) => {
    requests++;active++;peak = Math.max(peak, active);
    setTimeout(() => {
      active--;json(response, {}, requests === 1 ? { 'Retry-After': '0.01' } : {});
    }, 10);
  }, { concurrency: 4 });
  await session.call();
  // When six subsequent reads are scheduled together.
  const results = await Promise.all(Array.from({ length: 6 }, () => session.call()));
  // Then all responses succeed and the reduced HTTP concurrency is two.
  assert.ok(results.every(result => result.status === 'SUCCEEDED'));
  assert.equal(requests, 7);assert.equal(peak, 2);
  assert.equal((await session.close()).metrics.concurrency_reductions, 1);
});

test('A local evidence write failure does not replay a remote read', async t => {
  // Given the evidence destination becomes a directory after validation.
  let requests = 0;let evidence;
  const session = await fixture(t, (_request, response) => {
    requests++;mkdirSync(join(evidence, '1.json'), { recursive: true });json(response, {});
  });
  evidence = session.evidence;
  // When the connector cannot write the retained response.
  const result = await session.call();
  // Then it reports failure after exactly one HTTP attempt.
  assert.equal(result.status, 'ERROR');assert.equal(result.code, 'REQUEST_FAILED');
  assert.equal(requests, 1);assert.equal((await session.close()).metrics.retries, 0);
});

test('Native MCP reads enforce the complete serialized response limit', async t => {
  // Given a raw response fits four MiB but its two MCP representations do not.
  let requests = 0;
  const session = await fixture(t, (_request, response) => {
    requests++;json(response, { value: 'x'.repeat(2200000) });
  });
  const bridge = fileURLToPath(new URL('./bridge.js', import.meta.url));
  // When the existing native bridge invokes the shared reader.
  const raw = await new Promise((resolve, reject) => {
    const child = spawn(process.execPath, [bridge, '--workspace', session.directory], {
      env: { PATH: process.env.PATH, SystemRoot: process.env.SystemRoot, HOME: session.directory },
      stdio: ['pipe', 'pipe', 'pipe'],
    });
    let stdout = '';let stderr = '';
    child.stdout.on('data', chunk => { stdout += chunk; });
    child.stderr.on('data', chunk => { stderr += chunk; });
    child.on('error', reject);
    child.on('close', code => {
      if (code === 0) resolve(stdout);else reject(new Error(stderr));
    });
    child.stdin.end(JSON.stringify({ connector: 'ado', operation: 'call',
      tool: 'report_work_items', arguments: { ids: [501] } }));
  });
  // Then the bridge returns a small explicit error after one HTTP read.
  assert.equal(JSON.parse(raw).status, 'ERROR');assert.equal(requests, 1);
  assert.ok(Buffer.byteLength(raw) < 4096);await session.close();
});

test('The root certificate file applies to direct and proxied report TLS reads', async t => {
  // Given a local HTTPS fixture uses a private certificate authority from root .env.
  try { execFileSync('openssl', ['version'], { stdio: 'ignore' }); }
  catch { t.skip('OpenSSL is unavailable for the local TLS fixture.');return; }
  const directory = mkdtempSync(join(tmpdir(), 'release-report-tls-'));
  t.after(() => rmSync(directory, { recursive: true, force: true }));
  const cert = join(directory, 'root.pem');const key = join(directory, 'server.key');
  execFileSync('openssl', ['req', '-x509', '-newkey', 'rsa:2048', '-nodes', '-keyout', key,
    '-out', cert, '-days', '1', '-subj', '/CN=127.0.0.1', '-addext', 'subjectAltName=IP:127.0.0.1'], { stdio: 'ignore' });
  const certificate = readFileSync(cert);
  const tls = { cert: certificate, key: readFileSync(key) };
  let requests = 0;let tunnels = 0;
  const handler = (_request, response) => { requests++;json(response, { value: [{ id: 501 }] }); };
  const direct = await fixture(t, handler, { tls, certificate, environment: 'NODE_EXTRA_CA_CERTS=test-root.pem\n' });
  // When the report reader connects directly.
  assert.equal((await direct.call()).status, 'SUCCEEDED');await direct.close();
  const proxy = createServer();const sockets = new Set();
  proxy.on('connect', (request, socket, head) => {
    tunnels++;const target = new URL(`http://${request.url}`);
    const upstream = connect(Number(target.port), '127.0.0.1', () => {
      socket.write('HTTP/1.1 200 Connection Established\r\n\r\n');
      if (head.length) upstream.write(head);
      socket.pipe(upstream);upstream.pipe(socket);
    });
    for (const item of [socket, upstream]) {
      sockets.add(item);item.on('close', () => sockets.delete(item));
      item.on('error', () => { socket.destroy();upstream.destroy(); });
    }
  });
  await new Promise(resolve => proxy.listen(0, '127.0.0.1', resolve));
  t.after(() => new Promise(resolve => { for (const socket of sockets) socket.destroy();proxy.close(resolve); }));
  const proxied = await fixture(t, handler, { tls, certificate,
    environment: `NODE_EXTRA_CA_CERTS=test-root.pem\nHTTPS_PROXY=http://127.0.0.1:${proxy.address().port}\nNO_PROXY=\n` });
  // When the same trust configuration is used through a local CONNECT proxy.
  const proxiedResult = await proxied.call();
  assert.equal(proxiedResult.status, 'SUCCEEDED', JSON.stringify(proxiedResult));await proxied.close();
  // Then both service reads succeed with certificate validation enabled.
  assert.equal(requests, 2);assert.equal(tunnels, 1);
});
