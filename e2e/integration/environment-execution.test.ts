import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { createServer, type Server } from 'node:http';
import { once } from 'node:events';
import { mkdtempSync, mkdirSync, readFileSync, writeFileSync, rmSync, readdirSync, copyFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import path from 'node:path';
import test from 'node:test';
import { loginUi, portalUi } from '../catalog/ui-contracts.js';

function command(args: string[], environment: NodeJS.ProcessEnv): Promise<{ code: number | null; output: string }> {
  return new Promise((resolve, reject) => {
    const child = spawn(process.execPath, args, { env: { ...process.env, ...environment }, stdio: ['ignore', 'pipe', 'pipe'] });
    let output = '';
    child.stdout.on('data', value => { output += value; });
    child.stderr.on('data', value => { output += value; });
    const timeout = setTimeout(() => { child.kill('SIGTERM'); reject(new Error('Controlled environment execution timed out.')); }, 60_000);
    child.on('error', error => { clearTimeout(timeout); reject(error); });
    child.on('close', code => { clearTimeout(timeout); resolve({ code, output }); });
  });
}
const playwright = ['--import', 'tsx', '--import', './e2e/browser-config.ts', 'node_modules/@playwright/test/cli.js', 'test'];
const remote = [...playwright, '--config=e2e/remote.config.ts'];

test('Given distinct deployed profiles, When the real runners execute, Then target, saved state, assertions, and failures stay distinct',
  { timeout: 120_000 }, async t => {
    const directory = mkdtempSync(path.join(tmpdir(), 'e2e-remote-integration-'));
    // Put private inputs inside the source scan to verify explicit snapshot exclusion.
    const privateDirectory = mkdtempSync(path.resolve('e2e/.target-integration-'));
    const requests: string[] = [];
    const servers: Server[] = [];
    t.after(async () => {
      await Promise.all(servers.map(server => new Promise<void>(resolve => { server.closeAllConnections(); server.close(() => resolve()); })));
      rmSync(directory, { recursive: true, force: true });
      rmSync(privateDirectory, { recursive: true, force: true });
    });
    async function serve(kind: 'login' | 'portal' | 'redirect', destination?: string) {
      const server = createServer((request, response) => {
        requests.push(`${kind}:${new URL(request.url!, 'http://fixture.invalid').pathname}`);
        if (kind === 'portal' && request.headers.cookie !== 'session=controlled-private-state') {
          response.writeHead(401); response.end('Authentication state was not supplied.'); return;
        }
        response.setHeader('content-type', 'text/html');
        if (kind === 'redirect') {
          response.end(`<script>setTimeout(() => location.href = ${JSON.stringify(destination)}, 100)</script>`);
          return;
        }
        response.end(kind === 'login'
          ? `<main data-testid="NonprodPortal_login"><input placeholder="${loginUi.usernamePlaceholder}"><input type="password" placeholder="${loginUi.passwordPlaceholder}"><button>${loginUi.signInButtonName}</button><a href="/sso">${loginUi.ssoLinkName}</a></main>`
          : `<main data-testid="ProductionPortal_home"><div role="tablist" aria-label="${portalUi.workspaceListName}"><div role="tab"><input aria-label="${portalUi.workspaceName}" value="Expected Workspace"></div></div></main>`);
      });
      servers.push(server); server.listen(0, '127.0.0.1'); await once(server, 'listening');
      const address = server.address();
      assert.ok(address && typeof address !== 'string');
      return `http://127.0.0.1:${address.port}`;
    }
    const nonprod = await serve('login');
    const production = await serve('portal');
    const redirect = await serve('redirect', `${nonprod}/deployment/login`);
    const state = path.join(privateDirectory, 'state.json');
    writeFileSync(state, JSON.stringify({ cookies: [{ name: 'session', value: 'controlled-private-state', domain: '127.0.0.1',
      path: '/', expires: -1, httpOnly: true, secure: false, sameSite: 'Lax' }], origins: [] }));
    const profiles = path.join(privateDirectory, 'environments.json');
    writeFileSync(profiles, JSON.stringify({ environments: {
      nonprod: { targetUrl: `${nonprod}/deployment/login?entry=1#start`, prefix: 'NonprodPortal', storageState: './state.json' },
      prod: { targetUrl: `${production}/deployment/portal`, prefix: 'ProductionPortal', area: 'portal',
        storageState: './state.json', workspaceName: 'Expected Workspace' },
      wrong: { targetUrl: `${nonprod}/deployment/login`, prefix: 'WrongPrefix', storageState: './state.json' },
      redirect: { targetUrl: `${redirect}/start`, prefix: 'NonprodPortal', storageState: './state.json' },
    } }));
    for (const environment of ['nonprod', 'prod', 'wrong', 'redirect']) {
      const expectedStatus = ['wrong', 'redirect'].includes(environment) ? 'failed' : 'passed';
      const output = path.join(directory, environment);
      const result = await command(remote, { E2E_ENVIRONMENT: environment, E2E_ENVIRONMENTS_FILE: profiles, E2E_AUDIT_OUTPUT: output });
      if (process.env.E2E_INTEGRATION_EVIDENCE) {
        const retained = path.resolve(process.env.E2E_INTEGRATION_EVIDENCE, environment);
        mkdirSync(retained, { recursive: true });
        writeFileSync(path.join(retained, 'execution.json'), JSON.stringify({ code: result.code, output: result.output }, null, 2));
        for (const file of ['run-inputs.json', 'run-result.json']) copyFileSync(path.join(output, file), path.join(retained, file));
        const caseId = readdirSync(path.join(output, 'cases'))[0]!;
        copyFileSync(path.join(output, 'cases', caseId, 'result.json'), path.join(retained, 'case-result.json'));
      }
      assert.equal(result.code, expectedStatus === 'failed' ? 1 : 0, result.output);
      const inputs = JSON.parse(readFileSync(path.join(output, 'run-inputs.json'), 'utf8'));
      const outcome = JSON.parse(readFileSync(path.join(output, 'run-result.json'), 'utf8'));
      assert.equal(inputs.target.environment, environment);
      assert.ok(inputs.sourceHashes.every((source: { path: string }) => path.resolve(source.path) !== profiles && path.resolve(source.path) !== state),
        'Private profiles and authentication state must not enter retained source snapshots.');
      assert.equal(inputs.target.targetUrl, environment === 'prod' ? `${production}/deployment/portal`
        : environment === 'redirect' ? `${redirect}/start` : `${nonprod}/deployment/login`);
      assert.equal(outcome.canonicalBusinessExecution, 'CONFIGURED_APPLICATION_ASSERTIONS');
      assert.equal(outcome.statuses[expectedStatus], 1);
      assert.equal(outcome.completedTests, 1);
      const caseDirectory = path.join(output, 'cases', readdirSync(path.join(output, 'cases'))[0]!);
      const record = JSON.parse(readFileSync(path.join(caseDirectory, 'result.json'), 'utf8'));
      assert.equal(record.scope, 'CONFIGURED_APPLICATION');
      assert.equal(record.actualStatus, expectedStatus);
      if (environment === 'redirect') assert.ok(JSON.stringify(record.errors).includes('selected target origin'),
        'A matching UI after an asynchronous cross-origin redirect must fail the target assertion.');
      assert.ok(!JSON.stringify(inputs).includes('controlled-private-state'));
    }
    assert.ok(requests.includes('login:/deployment/login'));
    assert.ok(requests.includes('portal:/deployment/portal'));

    const cli = await command(['--import', 'tsx', '--import', './e2e/browser-config.ts', 'e2e/ai/runner.ts', 'validate',
      '--environment', 'nonprod', '--environments-file', profiles, '--out', path.join(directory, 'cli')],
      { E2E_ENVIRONMENT: undefined, E2E_ENVIRONMENTS_FILE: undefined });
    assert.equal(cli.code, 0, cli.output);
    const cliResult = JSON.parse(readFileSync(path.join(directory, 'cli/result.json'), 'utf8'));
    assert.equal(cliResult.scope, 'configured-application');
    assert.equal(cliResult.target.environment, 'nonprod');
    assert.equal(cliResult.results[0].area, 'login');
    assert.equal(cliResult.results[0].status, 'passed');
    if (process.env.E2E_INTEGRATION_EVIDENCE) {
      writeFileSync(path.resolve(process.env.E2E_INTEGRATION_EVIDENCE, 'cli-result.json'), JSON.stringify(cliResult, null, 2));
    }

    const before = requests.length;
    const rejected = await command([...playwright, '--config=e2e/audit.config.ts', '--list', '--reporter=line'],
      { E2E_ENVIRONMENT: 'prod', E2E_ENVIRONMENTS_FILE: profiles });
    assert.equal(rejected.code, 1);
    assert.match(rejected.output, /Named targets use e2e:remote/);
    assert.equal(requests.length, before, 'Local audit selection must fail before any target request.');
    if (process.env.E2E_INTEGRATION_EVIDENCE) {
      writeFileSync(path.resolve(process.env.E2E_INTEGRATION_EVIDENCE, 'fixture-rejection.json'),
        JSON.stringify({ code: rejected.code, output: rejected.output, requestsBefore: before, requestsAfter: requests.length }, null, 2));
    }
  });
