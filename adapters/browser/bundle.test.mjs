import test from 'node:test';
import assert from 'node:assert/strict';
import * as fs from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import { createHash } from 'node:crypto';
import { makeManifest, verifyBundle, installBundle, registryUrl } from './bundle.mjs';

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
