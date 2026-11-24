import test from 'node:test';
import assert from 'node:assert/strict';
import * as fs from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import { createHash } from 'node:crypto';
import { createServer } from 'node:http';
import { spawn, spawnSync } from 'node:child_process';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { makeManifest, verifyBundle, installBundle, registryUrl, prepareBundle,
  downloadPackage, runDownload } from './bundle.mjs';

async function fixture(t) {
  const root = await fs.mkdtemp(path.join(os.tmpdir(), 'browser-bundle-test-'));
  t.after(() => fs.rm(root, { recursive: true, force: true }));
  const bundle = path.join(root, 'bundle');
  const source = path.join(bundle, 'source');
  await fs.mkdir(source, { recursive: true });
  const bytes = Buffer.from('controlled package cache fixture');
  const digest = createHash('sha512').update(bytes).digest();
  const hex = digest.toString('hex');
  const cache = path.join(bundle, 'cache/_cacache/content-v2/sha512', hex.slice(0, 2), hex.slice(2, 4), hex.slice(4));
  await fs.mkdir(path.dirname(cache), { recursive: true });
  await fs.writeFile(cache, bytes);
  await fs.writeFile(path.join(source, 'package.json'), JSON.stringify({ dependencies: { playwright: '1.64.1' } }));
  await fs.writeFile(path.join(source, 'package-lock.json'), JSON.stringify({ lockfileVersion: 3, packages: {
    '': { dependencies: { playwright: '1.64.1' } }, 'node_modules/playwright': {
      version: '1.64.1', resolved: 'https://registry.npmjs.org/playwright/-/playwright-1.64.1.tgz', integrity: `sha512-${digest.toString('base64')}`,
    },
  } }));
  await fs.writeFile(path.join(source, 'browser.mjs'), '// controlled source fixture\n');
  await fs.writeFile(path.join(source, 'bundle.mjs'), '// controlled source fixture\n');
  await fs.mkdir(path.join(bundle, 'browsers/framework'), { recursive: true });
  await fs.writeFile(path.join(bundle, 'browsers/framework/browser'), 'controlled browser fixture');
  const manifest = await makeManifest(bundle, source);
  const save = async () => fs.writeFile(path.join(bundle, 'manifest.json'), JSON.stringify(manifest));
  await save();
  return { root, bundle, source, cache, manifest, save };
}

test('valid inventory detects browser mutation and unexpected files', async t => {
  const f = await fixture(t);
  await verifyBundle(f.bundle, f.source);
  await fs.writeFile(path.join(f.bundle, 'browsers/framework/browser'), 'changed');
  await assert.rejects(verifyBundle(f.bundle, f.source), /integrity mismatch/);
  await fs.writeFile(path.join(f.bundle, 'browsers/framework/browser'), 'controlled browser fixture');
  await fs.writeFile(path.join(f.bundle, 'browsers/extra'), 'unexpected');
  await assert.rejects(verifyBundle(f.bundle, f.source), /integrity mismatch/);
});

test('target mismatch and traversing manifest paths fail before installation', async t => {
  const f = await fixture(t);
  f.manifest.target.arch = 'other';
  await f.save();
  await assert.rejects(installBundle(f.bundle, path.join(f.root, 'installation'), f.source), /target does not match/);
  await assert.rejects(fs.stat(path.join(f.root, 'installation')), { code: 'ENOENT' });
  f.manifest.target.arch = process.arch;
  f.manifest.files.push({ path: '../outside', type: 'file' });
  await f.save();
  await assert.rejects(verifyBundle(f.bundle, f.source), /Unsafe bundle path/);
});

test('installation preserves an existing destination', async t => {
  const f = await fixture(t);
  const destination = path.join(f.root, 'installation');
  await fs.mkdir(destination);
  await fs.writeFile(path.join(destination, 'keep'), 'unrelated');
  await assert.rejects(installBundle(f.bundle, destination, f.source), /Destination already exists/);
  assert.equal(await fs.readFile(path.join(destination, 'keep'), 'utf8'), 'unrelated');
});

test('only internal relative browser symlinks are accepted', async t => {
  if (process.platform === 'win32') { t.skip('Symlink creation can require Windows privileges.'); return; }
  const f = await fixture(t);
  await fs.symlink('framework/browser', path.join(f.bundle, 'browsers/current'));
  await fs.writeFile(path.join(f.bundle, 'manifest.json'), JSON.stringify(await makeManifest(f.bundle, f.source)));
  await verifyBundle(f.bundle, f.source);
  await fs.unlink(path.join(f.bundle, 'browsers/current'));
  await fs.symlink('../source/browser.mjs', path.join(f.bundle, 'browsers/current'));
  await assert.rejects(verifyBundle(f.bundle, f.source), /Unsafe browser symlink/);
  await fs.unlink(path.join(f.bundle, 'browsers/current'));
  await fs.symlink('browser.mjs', path.join(f.source, 'forbidden'));
  await assert.rejects(verifyBundle(f.bundle, f.source), /Unsafe browser symlink/);
});

test('locked downloads reject non-registry hosts, credentials, and URL additions', () => {
  assert.equal(registryUrl('https://registry.npmjs.org/playwright/-/playwright-1.64.1.tgz'),
    'https://registry.npmjs.org/playwright/-/playwright-1.64.1.tgz');
  for (const value of ['http://registry.npmjs.org/a.tgz', 'https://other.test/a.tgz',
    'https://token@registry.npmjs.org/a.tgz', 'https://registry.npmjs.org/a.tgz?token=private']) {
    assert.throws(() => registryUrl(value), /credential-free HTTPS/);
  }
});

test('cached package bytes must match lock integrity even with an updated file inventory', async t => {
  const f = await fixture(t);
  await fs.writeFile(f.cache, 'mutated cache');
  await fs.writeFile(path.join(f.bundle, 'manifest.json'), JSON.stringify(await makeManifest(f.bundle, f.source)));
  await assert.rejects(verifyBundle(f.bundle, f.source), /Cached package integrity mismatch/);
});

test('package deadline covers stalled headers and a partially received body', { timeout: 6000 }, async t => {
  for (const sendHeaders of [false, true]) {
    const server = createServer((request, response) => {
      if (sendHeaders) { response.writeHead(200); response.write('incomplete package'); }
    });
    server.listen(0, '127.0.0.1');
    await new Promise(resolve => server.once('listening', resolve));
    try {
      const started = Date.now();
      await assert.rejects(downloadPackage(`http://127.0.0.1:${server.address().port}/package`, 1),
        /Warning: Locked browser package download timed out after 1 seconds.*Manual recovery:/);
      assert.ok(Date.now() - started < 2500, 'Download did not stop near the one-second deadline.');
    } finally {
      server.closeAllConnections();
      await new Promise(resolve => server.close(resolve));
    }
  }
});

test('package failures provide manual recovery without remote diagnostics', async () => {
  const server = createServer((request, response) => {
    response.writeHead(403, 'PRIVATE_COMPANY_PROXY_DETAIL');
    response.end('PRIVATE_COMPANY_PROXY_BODY');
  });
  server.listen(0, '127.0.0.1');
  await new Promise(resolve => server.once('listening', resolve));
  try {
    await assert.rejects(downloadPackage(`http://127.0.0.1:${server.address().port}/package`, 1), error => {
      assert.match(error.message, /Warning:.*Manual recovery:.*bundle.mjs install/);
      assert.doesNotMatch(error.message, /PRIVATE_COMPANY/);
      return true;
    });
  } finally { await new Promise(resolve => server.close(resolve)); }
});

test('Playwright timeout stops the downloader and its descendant before later writes',
  { timeout: 6000, skip: process.platform === 'win32' }, async t => {
    const root = await fs.mkdtemp(path.join(os.tmpdir(), 'browser-timeout-test-'));
    t.after(() => fs.rm(root, { recursive: true, force: true }));
    const marker = path.join(root, 'unexpected-completion');
    const ready = path.join(root, 'descendant-started');
    const descendant = `require('node:fs').writeFileSync(${JSON.stringify(ready)}, 'ready'); ` +
      `setTimeout(() => {require('node:fs').writeFileSync(${JSON.stringify(marker)}, 'download continued');}, 1600);`;
    const launcher = `require('node:child_process').spawn(process.execPath, ['-e', ${JSON.stringify(descendant)}], {stdio: 'ignore'}); setInterval(() => {}, 1000);`;
    await assert.rejects(runDownload(process.execPath, ['-e', launcher], {}, 1),
      /Warning: Playwright browser download timed out after 1 seconds.*Manual recovery:/);
    assert.equal(await fs.readFile(ready, 'utf8'), 'ready');
    await new Promise(resolve => setTimeout(resolve, 1000));
    await assert.rejects(fs.stat(marker), { code: 'ENOENT' });
  });

test('Playwright command failures are sanitized and successful local commands complete', async () => {
  const originalListeners = ['SIGINT', 'SIGTERM'].map(signal => process.listenerCount(signal));
  await runDownload(process.execPath, ['-e', 'process.exit(0)'], {}, 1);
  await assert.rejects(runDownload(process.execPath,
    ['-e', "console.error('PRIVATE_COMPANY_PROXY_DETAIL'); process.exit(1)"], {}, 1), error => {
    assert.match(error.message, /Warning: Playwright browser.*Manual recovery:/);
    assert.doesNotMatch(error.message, /PRIVATE_COMPANY/);
    return true;
  });
  assert.deepEqual(['SIGINT', 'SIGTERM'].map(signal => process.listenerCount(signal)), originalListeners);
});

test('invalid download limits fail before creating preparation output', async t => {
  const root = await fs.mkdtemp(path.join(os.tmpdir(), 'browser-timeout-validation-'));
  t.after(() => fs.rm(root, { recursive: true, force: true }));
  const output = path.join(root, 'not-created');
  for (const value of [0, -1, 0.5, NaN, Infinity, 86401]) {
    await assert.rejects(prepareBundle(output, { downloadTimeout: value }), /integer from 1 to 86400/);
    await assert.rejects(fs.stat(output), { code: 'ENOENT' });
  }
  const script = fileURLToPath(new URL('./bundle.mjs', import.meta.url));
  for (const value of ['0', '1.5', 'unknown']) {
    const result = spawnSync(process.execPath, [script, 'prepare', '--output', output, '--download-timeout', value],
      { encoding: 'utf8', timeout: 2000 });
    assert.equal(result.status, 1);
    assert.match(result.stderr, /integer from 1 to 86400/);
    await assert.rejects(fs.stat(output), { code: 'ENOENT' });
  }
});

test('preparation forwards its deadline and removes an incomplete browser bundle', { timeout: 4000 }, async t => {
  const f = await fixture(t);
  const implementation = fileURLToPath(new URL('./bundle.mjs', import.meta.url));
  await fs.copyFile(implementation, path.join(f.source, 'bundle.mjs'));
  const installed = path.join(f.source, 'node_modules/playwright');
  await fs.mkdir(installed, { recursive: true });
  await fs.writeFile(path.join(installed, 'package.json'), JSON.stringify({ version: '1.64.1' }));
  await fs.writeFile(path.join(installed, 'cli.js'), 'setInterval(() => {}, 1000);');
  t.mock.method(globalThis, 'fetch', async () => new Response(Buffer.from('controlled package cache fixture')));
  const candidate = await import(pathToFileURL(path.join(f.source, 'bundle.mjs')).href);
  const output = path.join(f.root, 'incomplete-bundle');
  await assert.rejects(candidate.prepareBundle(output, { downloadTimeout: 1 }),
    /Playwright browser download timed out after 1 seconds/);
  await assert.rejects(fs.stat(output), { code: 'ENOENT' });
});

test('interrupting preparation stops downloader descendants and removes its partial bundle',
  { timeout: 10000, skip: process.platform === 'win32' }, async t => {
    for (const signal of ['SIGINT', 'SIGTERM']) {
      const f = await fixture(t);
      const implementation = fileURLToPath(new URL('./bundle.mjs', import.meta.url));
      const modulePath = path.join(f.source, 'bundle.mjs');
      await fs.copyFile(implementation, modulePath);
      const installed = path.join(f.source, 'node_modules/playwright');
      await fs.mkdir(installed, { recursive: true });
      await fs.writeFile(path.join(installed, 'package.json'), JSON.stringify({ version: '1.64.1' }));
      const ready = path.join(f.root, 'downloader-started');
      const marker = path.join(f.root, 'orphan-completed');
      const descendant = `setTimeout(() => {require('node:fs').writeFileSync(${JSON.stringify(marker)}, 'orphan continued');}, 1500);`;
      const cli = `require('node:child_process').spawn(process.execPath, ['-e', ${JSON.stringify(descendant)}], {stdio: 'ignore'}); ` +
        `require('node:fs').writeFileSync(${JSON.stringify(ready)}, String(process.pid)); setInterval(() => {}, 1000);`;
      await fs.writeFile(path.join(installed, 'cli.js'), cli);
      const output = path.join(f.root, 'interrupted-bundle');
      const launcher = `import {prepareBundle} from ${JSON.stringify(pathToFileURL(modulePath).href)}; ` +
        "globalThis.fetch = async () => new Response(Buffer.from('controlled package cache fixture')); " +
        `try { await prepareBundle(${JSON.stringify(output)}, {downloadTimeout: 30}); } ` +
        "catch (error) { console.error(error.message); process.exitCode = 1; }";
      const child = spawn(process.execPath, ['--input-type=module', '-e', launcher], { stdio: ['ignore', 'ignore', 'pipe'] });
      let diagnostics = '';
      child.stderr.on('data', bytes => { diagnostics += bytes; });
      t.after(async () => {
        if (child.exitCode === null && child.signalCode === null) child.kill('SIGKILL');
        try { process.kill(-Number(await fs.readFile(ready, 'utf8')), 'SIGKILL'); } catch {}
      });
      const closed = new Promise(resolve => child.once('close', (code, exitSignal) => resolve({ code, exitSignal })));
      const readyDeadline = Date.now() + 3000;
      while (true) {
        try { await fs.stat(ready); break; } catch (error) { if (error.code !== 'ENOENT') throw error; }
        assert.ok(Date.now() < readyDeadline, 'The downloader did not reach the controlled interruption checkpoint.');
        await new Promise(resolve => setTimeout(resolve, 20));
      }
      child.kill(signal);
      const result = await closed;
      assert.equal(result.code, 1);
      assert.equal(result.exitSignal, null);
      assert.match(diagnostics, new RegExp(`download was interrupted by ${signal}.*Manual recovery:`));
      await assert.rejects(fs.stat(output), { code: 'ENOENT' });
      await new Promise(resolve => setTimeout(resolve, 1700));
      await assert.rejects(fs.stat(marker), { code: 'ENOENT' });
    }
  });
