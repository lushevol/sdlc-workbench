import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { mkdtempSync, readFileSync, readdirSync, realpathSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import path from 'node:path';
import test from 'node:test';
import { digest } from '../support/audit-fixture.js';

function files(directory: string): string[] {
  return readdirSync(directory, { withFileTypes: true }).flatMap(entry => {
    const file = path.join(directory, entry.name);
    return entry.isDirectory() ? files(file) : [file];
  });
}
function execute(environment: NodeJS.ProcessEnv) {
  return new Promise<{ code: number | null; output: string }>((resolve, reject) => {
    const child = spawn(process.execPath, ['--import', 'tsx', '--import', './e2e/browser-config.ts',
      'node_modules/@playwright/test/cli.js', 'test', '--config=e2e/audit.config.ts', '--workers=1'], {
      env: { ...process.env, E2E_ENVIRONMENT: undefined, E2E_ENVIRONMENTS_FILE: undefined, ...environment },
      stdio: ['ignore', 'pipe', 'pipe'],
    });
    let output = '';
    child.stdout.on('data', bytes => { output += bytes; });
    child.stderr.on('data', bytes => { output += bytes; });
    const timeout = setTimeout(() => { child.kill('SIGTERM'); reject(new Error('Controlled audit retention probe timed out.')); }, 60_000);
    child.on('error', error => { clearTimeout(timeout); reject(error); });
    child.on('close', code => { clearTimeout(timeout); resolve({ code, output }); });
  });
}

test('Given passing and failed browser cases, When capturing default and explicit audit modes, Then traces remain durable without default duplicates',
  { timeout: 120_000 }, async t => {
    const temporary = mkdtempSync(path.join(tmpdir(), 'audit-retention-browser-'));
    const specs = mkdtempSync(path.resolve('e2e/.audit-retention-probe-'));
    t.after(() => {
      rmSync(temporary, { recursive: true, force: true });
      rmSync(specs, { recursive: true, force: true });
    });
    writeFileSync(path.join(specs, 'retention.spec.ts'), `import { test, expect } from '../support/audit-fixture.js';
      test('RETENTION-101 passes', async ({ page, audit }) => {
        await page.setContent('<main>Controlled retention probe</main>');
        await audit.capture('starting-state', 'Controlled passing page before the assertion.');
        await expect(page.locator('main')).toHaveText('Controlled retention probe');
      });
      test('RETENTION-102 fails deliberately', async ({ page, audit }) => {
        await page.setContent('<main>Controlled failure probe</main>');
        await audit.capture('starting-state', 'Controlled failing page before the assertion.');
        expect(await page.locator('main').textContent()).toBe('Deliberately different expected text');
      });\n`);
    for (const explicit of [false, true]) {
      const output = path.join(temporary, explicit ? 'explicit' : 'default');
      const run = await execute({ E2E_AUDIT_TEST_DIR: specs, E2E_AUDIT_OUTPUT: output,
        E2E_AUDIT_SCOPE: 'SYNTHETIC_HARNESS', E2E_AUDIT_TRACE: explicit ? 'on' : undefined,
        E2E_AUDIT_HTML: explicit ? '1' : undefined });
      assert.equal(run.code, 1, run.output);
      const outcome = JSON.parse(readFileSync(path.join(output, 'run-result.json'), 'utf8'));
      assert.deepEqual(outcome.statuses, { passed: 1, failed: 1 }, run.output);
      assert.equal(outcome.completedTests, 2);
      assert.equal(outcome.incompleteTests.length, 0);
      const payloads = files(output);
      const traces = payloads.filter(file => file.endsWith('.zip'));
      assert.equal(traces.length, explicit ? 4 : 1,
        'Default mode keeps only the failed trace; explicit HTML deliberately copies both on-mode traces.');
      assert.equal(readdirSync(output).includes('html-report'), explicit);
      const cases = readdirSync(path.join(output, 'cases')).map(id => path.join(output, 'cases', id));
      for (const directory of cases) {
        const record = JSON.parse(readFileSync(path.join(directory, 'result.json'), 'utf8'));
        const manifest = JSON.parse(readFileSync(path.join(directory, 'artifact-manifest.json'), 'utf8'));
        for (const attachment of record.attachments) {
          assert.equal(attachment.retention, 'REUSED_RUN_ARTIFACT');
          assert.equal(attachment.retainedPath, realpathSync(attachment.originalPath));
          assert.equal(digest(readFileSync(attachment.retainedPath)), attachment.sha256,
            'Canonical payload bytes must survive runner cleanup.');
          assert.ok(manifest.artifacts.some((item: { path: string; sha256: string }) =>
            item.path === attachment.retainedPath && item.sha256 === attachment.sha256));
        }
        assert.ok(files(directory).some(file => file.endsWith('.png')), 'Passing and failed screenshots remain retained.');
        assert.ok(!files(directory).some(file => file.endsWith('.zip')), 'A case references the canonical trace without copying it.');
      }
      const inputs = JSON.parse(readFileSync(path.join(output, 'run-inputs.json'), 'utf8'));
      assert.equal(inputs.captureSettings.htmlReport, explicit);
      assert.equal(inputs.captureSettings.projects[0].trace, explicit ? 'on' : 'retain-on-failure');
    }
  });
