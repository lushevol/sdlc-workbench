import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { spawn } from 'node:child_process';
import { EventEmitter, once } from 'node:events';
import { access, mkdtemp, readFile, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import test from 'node:test';
import { claimConfigDirectory, finalizeSmoke, terminateChild } from './browser.mjs';

async function temporaryDirectory(t) {
  const directory = await mkdtemp(path.join(os.tmpdir(), 'browser-robustness-'));
  t.after(() => rm(directory, { recursive: true, force: true }));
  return directory;
}

async function runningChild(t, script) {
  const child = spawn(process.execPath, ['-e', script], { stdio: ['ignore', 'pipe', 'ignore'] });
  t.after(async () => {
    if (child.exitCode === null && child.signalCode === null) {
      const exited = once(child, 'exit');
      child.kill('SIGKILL');
      await exited;
    }
  });
  await once(child.stdout, 'data');
  return child;
}

test('signal termination completes without waiting for a second exit event', { timeout: 5000 }, async t => {
  const child = await runningChild(t, "process.stdout.write('ready'); setInterval(() => {}, 1000)");
  await terminateChild(child, { graceMs: 300, forceMs: 300 });
  assert.equal(child.exitCode, null);
  assert.equal(child.signalCode, 'SIGTERM');
  assert.equal(child.listenerCount('exit'), 0);
  // A second cleanup sees signalCode and returns immediately.
  await terminateChild(child, { graceMs: 300, forceMs: 300 });
});

test('a child that ignores SIGTERM is killed within the second deadline', { timeout: 5000, skip: process.platform === 'win32' }, async t => {
  const child = await runningChild(t, "process.on('SIGTERM', () => {}); process.stdout.write('ready'); setInterval(() => {}, 1000)");
  await terminateChild(child, { graceMs: 50, forceMs: 500 });
  assert.equal(child.signalCode, 'SIGKILL');
  assert.equal(child.listenerCount('exit'), 0);
});

test('a missing exit event has a bounded failure and releases its listener', { timeout: 2000 }, async () => {
  const child = Object.assign(new EventEmitter(), { pid: 123, exitCode: null, signalCode: null });
  const signals = [];
  child.kill = signal => { signals.push(signal); return true; };
  await assert.rejects(terminateChild(child, { graceMs: 10, forceMs: 10 }), /did not exit after SIGKILL/);
  assert.deepEqual(signals, ['SIGTERM', 'SIGKILL']);
  assert.equal(child.listenerCount('exit'), 0);
});

test('cleanup failures retain the original error, all later cleanup, and artifact hashes', async t => {
  const output = await temporaryDirectory(t);
  await writeFile(path.join(output, 'snapshot.yaml'), '- heading "retained"\n');
  const report = { status: 'FAILED', error: 'Error: original navigation failure' };
  const calls = [];
  await finalizeSmoke(report, output, [
    ['trace', () => { calls.push('trace'); throw new Error('trace connection lost'); }],
    ['browser context', () => { calls.push('context'); throw new Error('context close failed'); }],
    ['native child', () => { calls.push('native'); }],
    ['temporary profile', () => { calls.push('profile'); }],
    ['fixture server', () => { calls.push('server'); }],
  ]);
  assert.deepEqual(calls, ['trace', 'context', 'native', 'profile', 'server']);
  const result = JSON.parse(await readFile(path.join(output, 'result.json'), 'utf8'));
  assert.equal(result.status, 'FAILED');
  assert.equal(result.error, 'Error: original navigation failure');
  assert.deepEqual(result.cleanup_errors, [
    { step: 'trace', error: 'Error: trace connection lost' },
    { step: 'browser context', error: 'Error: context close failed' },
  ]);
  assert.ok(Number.isFinite(Date.parse(result.finished_at)));
  const manifest = JSON.parse(await readFile(path.join(output, 'manifest.json'), 'utf8'));
  assert.deepEqual(Object.keys(manifest.artifacts).sort(), ['result.json', 'snapshot.yaml']);
  for (const [name, artifact] of Object.entries(manifest.artifacts)) {
    const bytes = await readFile(path.join(output, name));
    assert.equal(artifact.sha256, createHash('sha256').update(bytes).digest('hex'));
    assert.equal(artifact.size_bytes, bytes.length);
  }
});

test('cleanup failure changes a successful smoke to FAILED', async t => {
  const output = await temporaryDirectory(t);
  const report = { status: 'PASSED', assertions: ['fixture passed'] };
  await finalizeSmoke(report, output, [['native child', () => { throw new Error('shutdown timed out'); }]]);
  const result = JSON.parse(await readFile(path.join(output, 'result.json'), 'utf8'));
  assert.equal(result.status, 'FAILED');
  assert.equal(result.error, undefined);
  assert.deepEqual(result.assertions, ['fixture passed']);
  assert.equal(result.cleanup_errors[0].error, 'Error: shutdown timed out');
  await access(path.join(output, 'manifest.json'));
});

test('a successful cleanup retains a successful smoke', async t => {
  const output = await temporaryDirectory(t);
  await finalizeSmoke({ status: 'PASSED' }, output, [['native child', () => {}]]);
  const result = JSON.parse(await readFile(path.join(output, 'result.json'), 'utf8'));
  assert.equal(result.status, 'PASSED');
  assert.equal(result.cleanup_errors, undefined);
});

test('competing launchers cannot delete the winner or a later session', async t => {
  const output = await temporaryDirectory(t);
  const configDir = path.join(output, 'native-chromium');
  const claims = await Promise.allSettled([claimConfigDirectory(configDir), claimConfigDirectory(configDir)]);
  const winners = claims.filter(result => result.status === 'fulfilled');
  const losers = claims.filter(result => result.status === 'rejected');
  assert.equal(winners.length, 1);
  assert.equal(losers.length, 1);
  assert.match(String(losers[0].reason), /native session record exists/);
  const config = path.join(configDir, 'owner.json');
  await writeFile(config, 'winner bytes');
  assert.equal(await readFile(config, 'utf8'), 'winner bytes');
  const releaseWinner = winners[0].value;
  await releaseWinner();
  await assert.rejects(access(configDir), { code: 'ENOENT' });
  const releaseNext = await claimConfigDirectory(configDir);
  await writeFile(config, 'later session bytes');
  await releaseWinner();
  assert.equal(await readFile(config, 'utf8'), 'later session bytes');
  await releaseNext();
  await assert.rejects(access(configDir), { code: 'ENOENT' });
});
