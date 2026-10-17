import assert from 'node:assert/strict';
import { execFileSync, spawn } from 'node:child_process';
import { mkdtempSync, mkdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { createServer } from 'node:http';
import { createServer as createHttpsServer } from 'node:https';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import test from 'node:test';
import { createConnectorServer, CONNECTORS } from './server.js';

const bridgePath = fileURLToPath(new URL('./bridge.js', import.meta.url));

function fixture(t, content = '') {
  const root = mkdtempSync(join(tmpdir(), 'workbench-connectors-bridge-'));
  t.after(() => rmSync(root, { recursive: true, force: true }));
  writeFileSync(join(root, '.env'), content);
  return root;
}

function requestBridge(root, request, { args = ['--workspace', root], env = {}, cwd = root } = {}) {
  return new Promise((resolve, reject) => {
    const child = spawn(process.execPath, [bridgePath, ...args], {
      cwd,
      env: { PATH: process.env.PATH, SystemRoot: process.env.SystemRoot, HOME: root, USERPROFILE: root, ...env },
      stdio: ['pipe', 'pipe', 'pipe'],
    });
    let stdout = '';
    let stderr = '';
    child.stdout.on('data', chunk => { stdout += chunk; });
    child.stderr.on('data', chunk => { stderr += chunk; });
    child.on('error', reject);
    child.on('close', code => {
      try {
        assert.equal(code, 0, stderr);
        assert.equal(stdout.trim().split('\n').length, 1);
        resolve({ envelope: JSON.parse(stdout), stdout, stderr });
      } catch (error) { reject(error); }
    });
    child.stdin.end(typeof request === 'string' ? request : JSON.stringify(request));
  });
}

async function localServer(t, handler) {
  const server = createServer(handler);
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  t.after(() => new Promise(resolve => server.close(resolve)));
  return `http://127.0.0.1:${server.address().port}`;
}

test('Confluence calls use the root endpoint and process credential from an unrelated working directory', async t => {
  const seen = [];
  const baseUrl = await localServer(t, (request, response) => {
    seen.push({ url: request.url, auth: request.headers.authorization });
    response.writeHead(200, { 'Content-Type': 'application/json' });
    response.end(JSON.stringify({ results: [{ key: 'ROOT', name: 'Root space' }] }));
  });
  const root = fixture(t, `CONFLUENCE_BASE_URL=${baseUrl}\nCONFLUENCE_PAT=file-token\n`);
  const nested = join(root, 'nested');
  mkdirSync(nested);
  writeFileSync(join(nested, '.env'), 'CONFLUENCE_BASE_URL=http://127.0.0.1:1\nCONFLUENCE_PAT=nested-token\n');
  writeFileSync(join(root, 'config.json'), JSON.stringify({ CONFLUENCE_PAT: 'legacy-token' }));
  const { envelope } = await requestBridge(root, {
    connector: 'confluence', operation: 'call', tool: 'confluence_list_spaces', arguments: {},
  }, { cwd: nested, env: { CONFLUENCE_PAT: 'process-token' } });
  assert.equal(envelope.status, 'SUCCEEDED');
  assert.match(envelope.result.content[0].text, /Root space/);
  assert.equal(seen.length, 1);
  assert.match(seen[0].url, /^\/rest\/api\/space/);
  assert.equal(seen[0].auth, 'Bearer process-token');
});

test('SonarQube can execute without Azure DevOps configuration', async t => {
  const baseUrl = await localServer(t, (request, response) => {
    assert.equal(request.headers.authorization, 'Bearer sonar-test-token');
    assert.match(request.url, /^\/api\/projects\/search/);
    response.writeHead(200, { 'Content-Type': 'application/json' });
    response.end(JSON.stringify({ components: [{ key: 'sample', name: 'Sample Project' }] }));
  });
  const root = fixture(t, `SONAR_BASE_URL=${baseUrl}\nSONAR_TOKEN=sonar-test-token\n`);
  const { envelope } = await requestBridge(root, {
    connector: 'sonar', operation: 'call', tool: 'sonar_search_projects', arguments: {},
  });
  assert.equal(envelope.status, 'SUCCEEDED');
  assert.match(envelope.result.content[0].text, /Sample Project/);
});

test('root certificates and NO_PROXY control Confluence and XWiki HTTPS access', async t => {
  try {
    execFileSync('openssl', ['version'], { stdio: 'ignore' });
  } catch {
    t.skip('OpenSSL is unavailable for the local TLS fixture.');
    return;
  }
  const root = fixture(t);
  mkdirSync(join(root, 'certificates'));
  const certificatePath = join(root, 'certificates', 'root.pem');
  const keyPath = join(root, 'certificates', 'server.key');
  execFileSync('openssl', [
    'req', '-x509', '-newkey', 'rsa:2048', '-nodes', '-keyout', keyPath,
    '-out', certificatePath, '-days', '1', '-subj', '/CN=127.0.0.1',
    '-addext', 'subjectAltName=IP:127.0.0.1',
  ], { stdio: 'ignore' });
  let calls = 0;
  const server = createHttpsServer({ key: readFileSync(keyPath), cert: readFileSync(certificatePath) }, (_request, response) => {
    calls++;
    response.writeHead(200, { 'Content-Type': 'application/json' });
    response.end(JSON.stringify({ results: [{ key: 'TLS', name: 'Trusted root' }] }));
  });
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  t.after(() => new Promise(resolve => server.close(resolve)));
  const endpoint = `https://127.0.0.1:${server.address().port}`;
  const settings = `CONFLUENCE_BASE_URL=${endpoint}\nCONFLUENCE_PAT=tls-token\nSCWIKI_URL=${endpoint}\nSCWIKI_TOKEN=wiki-token\n`;
  writeFileSync(join(root, '.env'), settings);
  const request = { connector: 'confluence', operation: 'call', tool: 'confluence_list_spaces' };
  assert.equal((await requestBridge(root, request)).envelope.status, 'ERROR');
  assert.equal(calls, 0);
  const trusted = `${settings}NODE_EXTRA_CA_CERTS=certificates/root.pem\nHTTPS_PROXY=http://127.0.0.1:1\n`;
  writeFileSync(join(root, '.env'), trusted);
  assert.equal((await requestBridge(root, request)).envelope.status, 'ERROR');
  assert.equal(calls, 0);
  writeFileSync(join(root, '.env'), `${trusted}NO_PROXY=127.0.0.1\n`);
  const { envelope } = await requestBridge(root, request);
  assert.equal(envelope.status, 'SUCCEEDED');
  assert.match(envelope.result.content[0].text, /Trusted root/);
  assert.equal(calls, 1);
  const wiki = await requestBridge(root, { connector: 'scwiki', operation: 'call', tool: 'scwiki_list_spaces' });
  assert.equal(wiki.envelope.status, 'SUCCEEDED');
  assert.match(wiki.envelope.result.content[0].text, /Trusted root/);
  assert.equal(calls, 2);
});

test('tool validation rejects invalid arguments before any external call', async t => {
  let calls = 0;
  const baseUrl = await localServer(t, (_request, response) => { calls++; response.end('{}'); });
  const root = fixture(t, `CONFLUENCE_BASE_URL=${baseUrl}\nCONFLUENCE_PAT=must-not-appear\n`);
  const result = await requestBridge(root, {
    connector: 'confluence', operation: 'call', tool: 'confluence_read_page', arguments: { pageId: 42 },
  });
  assert.equal(result.envelope.status, 'ERROR');
  assert.equal(calls, 0);
  assert.doesNotMatch(result.stdout, /must-not-appear/);
});

test('external failures produce a fixed error envelope', async t => {
  const baseUrl = await localServer(t, (_request, response) => {
    response.writeHead(403, { 'Content-Type': 'text/plain' });
    response.end('must-not-appear');
  });
  const root = fixture(t, `CONFLUENCE_BASE_URL=${baseUrl}\nCONFLUENCE_PAT=must-not-appear\n`);
  const { envelope, stdout } = await requestBridge(root, {
    connector: 'confluence', operation: 'call', tool: 'confluence_list_spaces',
  });
  assert.equal(envelope.status, 'ERROR');
  assert.equal(envelope.code, 'TOOL_ERROR');
  assert.equal(envelope.result, undefined);
  assert.doesNotMatch(stdout, /must-not-appear/);
});

test('bridge requires an absolute selected root and handles malformed JSON', async t => {
  const root = fixture(t);
  const malformed = await requestBridge(root, '{');
  assert.equal(malformed.envelope.code, 'INVALID_REQUEST');
  const relative = await requestBridge(root, { connector: 'web', operation: 'list' }, {
    args: ['--workspace', '.'],
  });
  assert.equal(relative.envelope.code, 'INVALID_REQUEST');
  const unsupported = await requestBridge(root, { connector: 'app-bridge', operation: 'list' });
  assert.equal(unsupported.envelope.code, 'INVALID_REQUEST');
});

test('tool discovery does not require credentials or network access', async t => {
  const root = fixture(t);
  for (const connector of CONNECTORS) {
    const { envelope } = await requestBridge(root, { connector, operation: 'list' });
    assert.equal(envelope.status, 'SUCCEEDED', connector);
    assert.ok(envelope.tools.length > 0, connector);
    assert.ok(envelope.tools.every(tool => typeof tool.name === 'string' && tool.inputSchema), connector);
  }
});

test('tool registration preserves TLS settings and needs no connection at startup', async t => {
  const previous = process.env.NODE_TLS_REJECT_UNAUTHORIZED;
  delete process.env.NODE_TLS_REJECT_UNAUTHORIZED;
  t.after(() => {
    if (previous === undefined) delete process.env.NODE_TLS_REJECT_UNAUTHORIZED;
    else process.env.NODE_TLS_REJECT_UNAUTHORIZED = previous;
  });
  const config = {
    workspaceRoot: dirname(bridgePath), env: {}, HTTPS_PROXY: '', codeReviewGuideFile: '',
    AZURE_DEVOPS_ORG_URL: 'https://ado.example/organization', AZURE_DEVOPS_PAT: 'ado-token',
    confluenceConfig: { baseUrl: 'https://confluence.example', token: 'confluence-token' },
    scwikiConfig: { baseUrl: 'https://wiki.example', token: 'wiki-token', wiki: 'xwiki' },
    nexusConfig: { baseUrl: 'https://nexus.example', userCode: 'user', passCode: 'password' },
    sonarConfig: { baseUrl: 'https://sonar.example', token: 'sonar-token' },
  };
  for (const connector of CONNECTORS) {
    const server = await createConnectorServer(connector, config);
    assert.equal(process.env.NODE_TLS_REJECT_UNAUTHORIZED, undefined, connector);
    await server.close();
  }
});
