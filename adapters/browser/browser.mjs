import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { spawn, execFileSync } from 'node:child_process';
import { createServer } from 'node:http';
import { access, mkdir, mkdtemp, readFile, rm, writeFile } from 'node:fs/promises';
import { constants } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { parseArgs } from 'node:util';
import { setTimeout as delay } from 'node:timers/promises';

const root = path.dirname(fileURLToPath(import.meta.url));
// Resolve before importing Playwright. Startup never installs packages or browsers.
process.env.PLAYWRIGHT_BROWSERS_PATH = path.join(root, '.browsers');
const ignoredBackgroundDefaults = [
  '--disable-background-timer-throttling',
  '--disable-backgrounding-occluded-windows',
  '--disable-renderer-backgrounding',
];
const sha256 = value => createHash('sha256').update(value).digest('hex');
const json = value => JSON.stringify(value, null, 2) + '\n';
const launchOptions = browser => ({
  headless: false,
  chromiumSandbox: true,
  ...(browser === 'msedge' ? { channel: 'msedge' } : {}),
  ignoreDefaultArgs: ignoredBackgroundDefaults,
});
function channel(value) {
  if (!['chromium', 'msedge'].includes(value)) throw new Error('Select chromium or msedge.');
  return value;
}
function git(...args) {
  try { return execFileSync('git', ['-C', root, ...args], { encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'] }).trim(); }
  catch { return null; }
}
async function runtime() {
  const { chromium } = await import('playwright');
  const packageInfo = JSON.parse(await readFile(path.join(root, 'node_modules/playwright/package.json')));
  return { chromium, packageInfo };
}
function edgeExecutable() {
  const bases = [process.env['PROGRAMFILES(X86)'], process.env.PROGRAMFILES, process.env.LOCALAPPDATA].filter(Boolean);
  return process.platform === 'darwin' ? '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge'
    : process.platform === 'win32' ? bases.map(base => path.join(base, 'Microsoft/Edge/Application/msedge.exe'))
    : '/opt/microsoft/msedge/msedge';
}

const childExited = child => child.exitCode !== null || child.signalCode !== null;

export async function terminateChild(child, { graceMs = 3000, forceMs = 3000 } = {}) {
  if (childExited(child) || child.pid === undefined) return;
  let onExit;
  const exited = new Promise(resolve => { onExit = resolve; child.once('exit', onExit); });
  const waitForExit = async milliseconds => {
    let timer;
    try {
      return await Promise.race([exited.then(() => true), new Promise(resolve => {
        timer = setTimeout(() => resolve(false), milliseconds);
      })]);
    } finally { clearTimeout(timer); }
  };
  try {
    child.kill('SIGTERM');
    if (childExited(child) || await waitForExit(graceMs)) return;
    child.kill('SIGKILL');
    if (childExited(child) || await waitForExit(forceMs)) return;
    throw new Error('Disposable browser did not exit after SIGKILL.');
  } finally { child.removeListener('exit', onExit); }
}

export async function cleanupSteps(steps) {
  const errors = [];
  for (const [step, run] of steps) {
    try { await run(); } catch (error) { errors.push({ step, error: String(error) }); }
  }
  return errors;
}

export async function finalizeSmoke(report, output, steps) {
  const errors = [...(report.cleanup_errors ?? []), ...await cleanupSteps(steps)];
  if (errors.length) { report.cleanup_errors = errors; report.status = 'FAILED'; }
  report.finished_at = new Date().toISOString();
  await writeFile(path.join(output, 'result.json'), json(report));
  const artifacts = {};
  for (const name of ['result.json', 'snapshot.yaml', 'returned.png', 'trace.zip']) {
    try { const bytes = await readFile(path.join(output, name)); artifacts[name] = { sha256: sha256(bytes), size_bytes: bytes.length }; }
    catch { /* Failed runs can have partial evidence. */ }
  }
  await writeFile(path.join(output, 'manifest.json'), json({ schema_version: 1, artifacts }));
}

export async function claimConfigDirectory(directory) {
  try { await mkdir(directory); }
  catch (error) {
    if (error.code === 'EEXIST') throw new Error('A native session record exists. Close its launcher before opening another.');
    throw error;
  }
  // The launcher owns this directory. Concurrent launchers and CLI clients cannot remove it.
  let release;
  return () => release ??= rm(directory, { recursive: true, force: true });
}

async function nativeBrowser(chromium, browser, profile) {
  const candidates = browser === 'msedge' ? [edgeExecutable()].flat() : [chromium.executablePath()];
  let executable;
  for (const candidate of candidates) {
    try { await access(candidate, constants.X_OK); executable = candidate; break; } catch { /* Try next declared location. */ }
  }
  if (!executable) throw new Error('Browser executable is absent. Provision it explicitly before launch.');
  // Own fresh profile, loopback endpoint, native lifecycle, and no updater startup.
  const args = [`--user-data-dir=${profile}`, '--remote-debugging-port=0', '--remote-debugging-address=127.0.0.1',
    '--no-first-run', '--no-default-browser-check', '--disable-background-networking', '--disable-component-update', '--disable-sync',
    ...(browser === 'msedge' ? ['--disable-edgeupdater', '--disable-updater-scheduler',
      '--disable-features=msForceBrowserSignIn,msEdgeUpdateLaunchServicesPreferredVersion'] : []), 'about:blank'];
  const child = spawn(executable, args, { stdio: 'ignore' });
  let launchError;
  child.on('error', error => { launchError = error; });
  const close = () => terminateChild(child);
  try {
    let port;
    for (let attempts = 0; attempts < 150; attempts++) {
      if (launchError) throw launchError;
      if (childExited(child)) throw new Error(`Disposable browser exited: ${child.exitCode ?? child.signalCode}`);
      try { port = Number((await readFile(path.join(profile, 'DevToolsActivePort'), 'utf8')).split('\n')[0]); } catch { /* Browser startup pending. */ }
      if (port > 0) break;
      await delay(100);
    }
    if (!(port > 0)) throw new Error('Disposable browser did not create its loopback endpoint.');
    const endpoint = `http://127.0.0.1:${port}`;
    const instance = await chromium.connectOverCDP(endpoint, { noDefaults: true });
    return { instance, close, executable, args, endpoint };
  } catch (error) {
    const errors = await cleanupSteps([['native child', close]]);
    if (errors.length) error.cleanup_errors = errors;
    throw error;
  }
}
async function doctor() {
  const { chromium, packageInfo } = await runtime();
  const executable = chromium.executablePath();
  let chromiumPresent = true;
  try { await access(executable, constants.X_OK); } catch { chromiumPresent = false; }
  const edgeCandidates = [edgeExecutable()].flat();
  let edge = null;
  for (const candidate of edgeCandidates) {
    try { await access(candidate, constants.X_OK); edge = candidate; break; } catch { /* Try next declared location. */ }
  }
  const result = {
    status: chromiumPresent && edge ? 'READY' : 'INCOMPLETE',
    checked_at: new Date().toISOString(), platform: process.platform, arch: process.arch,
    os_release: os.release(), node: process.version, playwright: packageInfo.version,
    chromium: { present: chromiumPresent, executable }, edge: { present: Boolean(edge), executable: edge },
    browser_launch_tested: false,
    limitations: ['Presence checks do not establish browser launch or business behavior.'],
  };
  console.log(json(result));
  if (result.status !== 'READY') process.exitCode = 1;
}

// The fixture contains no credentials, external resources, or business behavior.
const fixture = `<!doctype html><html lang="en"><meta charset="utf-8">
<title>Workbench browser tooling smoke</title>
<style>body{font:20px system-ui;margin:60px;line-height:1.6}button{font:inherit}</style>
<h1>Workbench browser tooling smoke</h1>
<p>This local fixture checks browser tooling.</p><button>Confirm browser control</button>
<p id="result" role="status">Waiting for a click</p>
<script>
window.observations = [];
function record(event) {
  window.observations.push({event, at:new Date().toISOString(), monotonic_ms:performance.now(),
    visibility:document.visibilityState, focused:document.hasFocus()});
}
record('load');
for (const event of ['visibilitychange','freeze','resume','pagehide','pageshow']) {
  document.addEventListener(event, () => record(event));
}
document.querySelector('button').onclick = () => {
  document.querySelector('#result').textContent = 'Browser control confirmed'; record('click');
};
</script></html>`;

async function smoke(browser, output) {
  const { chromium, packageInfo } = await runtime();
  // Exclusive creation preserves earlier evidence.
  await mkdir(output, { recursive: false });
  const sourceNames = ['browser.mjs', 'package.json', 'package-lock.json'];
  const sourceHashes = Object.fromEntries(await Promise.all(sourceNames.map(async name => [name, sha256(await readFile(path.join(root, name)))])));
  const report = {
    kind: 'controlled-local-tooling-smoke', status: 'FAILED', started_at: new Date().toISOString(),
    browser, playwright: packageInfo.version, node: process.version, platform: process.platform,
    arch: process.arch, os_release: os.release(), source: { head: git('rev-parse', 'HEAD'), files: sourceHashes },
    profile: 'New temporary profile; removed on close',
    connection: 'Playwright connectOverCDP with noDefaults true; own loopback endpoint only',
    assertions: [],
    limitations: [
      'This short smoke does not reproduce the portal incident or verify business behavior.',
      'A fresh automated profile does not establish the personal browser configuration.',
      'A tab switch does not establish natural freezing or a 30-minute background interval.',
    ],
  };
  let context;
  let instance;
  let profile;
  let native;
  let tracing = false;
  const server = createServer((request, response) => {
    response.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'no-store' });
    response.end(request.url === '/other' ? '<!doctype html><title>Other tab</title><h1>Other tab</h1>' : fixture);
  });
  try {
    await new Promise((resolve, reject) => { server.once('error', reject); server.listen(0, '127.0.0.1', resolve); });
    report.origin = `http://127.0.0.1:${server.address().port}`;
    profile = await mkdtemp(path.join(os.tmpdir(), 'workbench-browser-smoke-'));
    native = await nativeBrowser(chromium, browser, profile);
    instance = native.instance;
    report.launch = { executable: native.executable, args: native.args };
    context = instance.contexts()[0];
    report.browser_version = instance.version();
    await context.tracing.start({ screenshots: true, snapshots: true, sources: true });
    tracing = true;
    const page = context.pages()[0] ?? await context.newPage();
    await page.goto(report.origin);
    report.user_agent = await page.evaluate(() => navigator.userAgent);
    await page.getByRole('button', { name: 'Confirm browser control' }).click();
    assert.equal(await page.getByRole('status').textContent(), 'Browser control confirmed');
    report.assertions.push('Role locator click changes the visible status text.');
    const other = await context.newPage();
    await other.goto(`${report.origin}/other`);
    await page.bringToFront();
    await page.waitForFunction(() => document.visibilityState === 'visible');
    const switchMarker = await page.evaluate(() => performance.now());
    const hidden = page.waitForFunction(() => document.visibilityState === 'hidden', null, { polling: 100, timeout: 5000 });
    report.switch_requested_at = new Date().toISOString();
    await other.bringToFront();
    await hidden;
    // Native timer in the visible second tab; no clock changes or forced lifecycle events.
    await other.evaluate(() => new Promise(resolve => setTimeout(resolve, 2000)));
    report.return_requested_at = new Date().toISOString();
    await page.bringToFront();
    await page.waitForFunction(() => document.visibilityState === 'visible');
    report.observations = await page.evaluate(() => window.observations);
    const hiddenEvent = report.observations.find(event => event.monotonic_ms >= switchMarker && event.visibility === 'hidden');
    const returnEvent = report.observations.find(event => hiddenEvent && event.monotonic_ms > hiddenEvent.monotonic_ms && event.visibility === 'visible');
    assert.ok(hiddenEvent && returnEvent, 'Expected timestamped hidden and visible observations.');
    report.hidden_interval_ms = returnEvent.monotonic_ms - hiddenEvent.monotonic_ms;
    assert.ok(report.hidden_interval_ms >= 2000, 'Expected at least 2000 ms in the background.');
    report.assertions.push('Native visibility events record hidden, then visible, at least 2000 ms apart.');
    await writeFile(path.join(output, 'snapshot.yaml'), await page.locator('body').ariaSnapshot());
    await page.screenshot({ path: path.join(output, 'returned.png') });
    report.status = 'PASSED';
  } catch (error) {
    report.error = String(error);
    if (error.cleanup_errors) report.cleanup_errors = error.cleanup_errors;
    if (context) report.page_states = await Promise.all(context.pages().map(async page => ({
      url: page.url(), ...await page.evaluate(() => ({ visibility: document.visibilityState, focused: document.hasFocus(), observations: window.observations })),
    }))).catch(() => []);
    process.exitCode = 1;
  } finally {
    await finalizeSmoke(report, output, [
      ['trace', () => tracing && context.tracing.stop({ path: path.join(output, 'trace.zip') })],
      ['browser context', () => context?.close()],
      ['browser connection', () => instance?.close()],
      ['native child', () => native?.close()],
      ['temporary profile', () => profile && rm(profile, { recursive: true, force: true })],
      ['fixture server', () => new Promise(resolve => server.close(resolve))],
    ]);
    if (report.status !== 'PASSED') process.exitCode = 1;
    console.log(json({ ...report, output }));
  }
}

async function open(browser, url) {
  const { chromium, packageInfo } = await runtime();
  const output = path.join(root, 'evidence');
  await mkdir(output, { recursive: true });
  const configDir = path.join(output, `native-${browser}`);
  const config = path.join(configDir, '.playwright', 'cli.config.json');
  let releaseConfig;
  let profile;
  let native;
  let failure;
  try {
    releaseConfig = await claimConfigDirectory(configDir);
    profile = await mkdtemp(path.join(os.tmpdir(), 'workbench-browser-investigation-'));
    native = await nativeBrowser(chromium, browser, profile);
    await mkdir(path.dirname(config), { recursive: true });
    await writeFile(config, json({ browser: { browserName: 'chromium', cdpEndpoint: native.endpoint }, outputDir: output }), { flag: 'wx' });
    const context = native.instance.contexts()[0];
    const page = context.pages()[0] ?? await context.newPage();
    await page.goto(url);
    console.log(json({ status: 'OPEN', browser, version: native.instance.version(), playwright: packageInfo.version,
      opened_at: new Date().toISOString(), endpoint: native.endpoint, profile: 'temporary',
      next_command: `node browser.mjs agent-native ${browser} open`, stop: 'Press Ctrl+C in this launcher to close and remove the profile.' }));
    await new Promise(resolve => {
      process.once('SIGINT', resolve);
      process.once('SIGTERM', resolve);
      native.instance.once('disconnected', resolve);
    });
  } catch (error) { failure = error; throw error; }
  finally {
    const errors = await cleanupSteps([
      ['browser connection', () => native?.instance.close()],
      ['native child', () => native?.close()],
      ['native config', () => releaseConfig?.()],
      ['temporary profile', () => profile && rm(profile, { recursive: true, force: true })],
    ]);
    if (errors.length) {
      if (failure) failure.cleanup_errors = [...(failure.cleanup_errors ?? []), ...errors];
      else { const error = new Error('Native session cleanup failed.'); error.cleanup_errors = errors; throw error; }
    }
  }
}

async function agent(browser, commands, native = false) {
  const allowed = ['open', 'goto', 'snapshot', 'find', 'click', 'fill', 'press', 'tab-new', 'tab-select', 'tab-list', 'screenshot', 'tracing-start', 'tracing-stop', 'close', 'run-code', 'console', 'requests'];
  if (!allowed.includes(commands[0])) throw new Error(`Select an agent command: ${allowed.join(', ')}.`);
  if (commands.some(arg => /^--?(profile|persistent|extension|cdp|endpoint|config|browser|user-data-dir)(=|$)/.test(arg))) {
    throw new Error('The agent wrapper requires its own isolated profile and configuration.');
  }
  await runtime();
  const output = path.join(root, 'evidence');
  await mkdir(output, { recursive: true });
  const configDir = path.join(output, `${native ? 'native' : 'agent'}-${browser}`);
  const config = path.join(configDir, '.playwright', 'cli.config.json');
  if (native) await access(config);
  else { await mkdir(path.dirname(config), { recursive: true }); await writeFile(config, json({ browser: { browserName: 'chromium', isolated: true, launchOptions: launchOptions(browser) }, outputDir: output })); }
  const env = Object.fromEntries(Object.entries(process.env).filter(([name]) => !/^(PLAYWRIGHT_MCP_|PWTEST_CLI_)/.test(name)));
  env.PWTEST_CLI_GLOBAL_CONFIG = output;
  const args = [path.join(root, 'node_modules/playwright/cli.js'), 'cli', `-s=workbench-${native ? 'native-' : ''}${browser}`, ...commands];
  const child = spawn(process.execPath, args, { cwd: configDir, stdio: 'inherit', env });
  process.exitCode = await new Promise((resolve, reject) => { child.once('error', reject); child.once('exit', code => resolve(code ?? 1)); });
}

async function main() {
  try {
    const [mode = 'doctor', ...rest] = process.argv.slice(2);
    if (mode === 'agent' || mode === 'agent-native') {
      await agent(channel(rest[0]), rest.slice(1), mode === 'agent-native');
    } else {
      const { values } = parseArgs({ args: rest, options: { browser: { type: 'string', default: 'chromium' }, output: { type: 'string' }, url: { type: 'string', default: 'about:blank' } } });
      if (mode === 'doctor') await doctor();
      else if (mode === 'open') await open(channel(values.browser), values.url);
      else if (mode === 'smoke') {
        const browser = channel(values.browser);
        const output = values.output ? path.resolve(values.output) : path.join(root, 'evidence', `${Date.now()}-${browser}`);
        await mkdir(path.dirname(output), { recursive: true });
        await smoke(browser, output);
      } else throw new Error('Use doctor, smoke, open --browser chromium|msedge --url URL, or agent[-native] chromium|msedge COMMAND.');
    }
  } catch (error) {
    console.error(String(error));
    if (error.cleanup_errors) console.error(json({ cleanup_errors: error.cleanup_errors }));
    process.exitCode = 1;
  }
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) await main();
