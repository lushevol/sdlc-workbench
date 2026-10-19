#!/usr/bin/env node
// Optional, explicit provisioning. Browser use never calls this installer.
import { createHash } from 'node:crypto';
import { spawn } from 'node:child_process';
import { createReadStream } from 'node:fs';
import * as fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const sourceRoot = path.dirname(fileURLToPath(import.meta.url));
const sources = ['package.json', 'package-lock.json', 'browser.mjs', 'bundle.mjs'];
const sha256 = bytes => createHash('sha256').update(bytes).digest('hex');
const target = () => ({ platform: process.platform, arch: process.arch, nodeMajor: Number(process.versions.node.split('.')[0]) });
const exists = async value => { try { await fs.lstat(value); return true; } catch (error) { if (error.code === 'ENOENT') return false; throw error; } };
const readJson = async value => JSON.parse(await fs.readFile(value, 'utf8'));
async function hashFile(file) {
  const hash = createHash('sha256');
  for await (const bytes of createReadStream(file)) hash.update(bytes);
  return hash.digest('hex');
}

function relativePath(value) {
  if (typeof value !== 'string' || !value || value.includes('\\') || value.includes('\0') ||
      path.posix.isAbsolute(value) || /^[A-Za-z]:/.test(value) ||
      value.split('/').some(part => !part || part === '.' || part === '..')) throw new Error(`Unsafe bundle path: ${value}`);
  return value;
}

export function registryUrl(value) {
  const url = new URL(value);
  if (url.protocol !== 'https:' || url.hostname !== 'registry.npmjs.org' || url.port ||
      url.username || url.password || url.search || url.hash || !url.pathname.endsWith('.tgz')) {
    throw new Error('Locked packages must use credential-free HTTPS tarballs from registry.npmjs.org.');
  }
  return url.href;
}

function integrity(value) {
  const match = /^(sha512|sha384|sha256)-([A-Za-z0-9+/]+={0,2})$/.exec(value ?? '');
  if (!match) throw new Error('A locked package needs one supported integrity digest.');
  const digest = Buffer.from(match[2], 'base64');
  if (digest.length !== { sha512: 64, sha384: 48, sha256: 32 }[match[1]] || digest.toString('base64') !== match[2]) {
    throw new Error('A locked package has an invalid integrity digest.');
  }
  return { algorithm: match[1], digest, encoded: match[2] };
}

function contentPath(root, value) {
  const { algorithm, digest } = integrity(value);
  const hex = digest.toString('hex');
  return path.join(root, '_cacache', 'content-v2', algorithm, hex.slice(0, 2), hex.slice(2, 4), hex.slice(4));
}

async function dependencies(root) {
  const pkg = await readJson(path.join(root, 'package.json'));
  const lock = await readJson(path.join(root, 'package-lock.json'));
  if (pkg.dependencies?.playwright !== '1.64.1' || lock.lockfileVersion !== 3 ||
      lock.packages?.['']?.dependencies?.playwright !== pkg.dependencies.playwright ||
      lock.packages?.['node_modules/playwright']?.version !== pkg.dependencies.playwright) {
    throw new Error('The optional environment requires the exact Playwright 1.64.1 package and matching lockfile.');
  }
  return Object.entries(lock.packages).filter(([name]) => name).map(([name, entry]) => {
    relativePath(name);
    integrity(entry.integrity);
    return { name, version: entry.version, url: registryUrl(entry.resolved), integrity: entry.integrity };
  });
}

async function sourceHashes(root) {
  const result = {};
  for (const name of sources) {
    const file = path.join(root, name);
    if (!(await fs.lstat(file)).isFile()) throw new Error(`Source must be a regular file: ${name}`);
    result[name] = sha256(await fs.readFile(file));
  }
  return result;
}

// Native macOS browser frameworks contain relative links. Only internal browser links are allowed.
async function entries(root, directory = '') {
  const result = [];
  for (const name of (await fs.readdir(path.join(root, directory))).sort()) {
    const relative = relativePath(directory ? `${directory}/${name}` : name);
    if (relative === 'manifest.json') continue;
    if (!['source', 'browsers', 'cache'].includes(relative.split('/')[0])) throw new Error(`Unexpected bundle entry: ${relative}`);
    const file = path.join(root, relative);
    const stat = await fs.lstat(file);
    if (stat.isSymbolicLink()) {
      const link = await fs.readlink(file);
      const browserRoot = await fs.realpath(path.join(root, 'browsers'));
      const resolved = await fs.realpath(file);
      const inside = path.relative(browserRoot, resolved);
      if (!relative.startsWith('browsers/') || path.isAbsolute(link) || /^[A-Za-z]:/.test(link) || link.includes('\\') ||
          !inside || inside === '..' || inside.startsWith(`..${path.sep}`) || path.isAbsolute(inside)) {
        throw new Error(`Unsafe browser symlink: ${relative}`);
      }
      result.push({ path: relative, type: 'symlink', target: link });
    } else if (stat.isDirectory()) {
      result.push({ path: relative, type: 'directory' });
      result.push(...await entries(root, relative));
    } else if (stat.isFile()) {
      result.push({ path: relative, type: 'file', size: stat.size, mode: stat.mode & 0o777,
        sha256: await hashFile(file) });
    } else throw new Error(`Unsupported bundle entry: ${relative}`);
  }
  return result;
}

export async function makeManifest(root, expectedSource = sourceRoot) {
  return { schemaVersion: 1, createdAt: new Date().toISOString(), target: target(),
    sourceHashes: await sourceHashes(expectedSource), packages: await dependencies(expectedSource), files: await entries(root) };
}

export async function verifyBundle(bundle, expectedSource = sourceRoot) {
  bundle = path.resolve(bundle);
  if (!(await fs.lstat(bundle)).isDirectory()) throw new Error('Bundle must be a regular directory.');
  const manifestPath = path.join(bundle, 'manifest.json');
  if (!(await fs.lstat(manifestPath)).isFile()) throw new Error('Bundle manifest must be a regular file.');
  const manifest = await readJson(manifestPath);
  if (manifest.schemaVersion !== 1 || JSON.stringify(manifest.target) !== JSON.stringify(target())) {
    throw new Error('Bundle target does not match this OS, architecture, and Node major.');
  }
  const expectedHashes = await sourceHashes(expectedSource);
  if (JSON.stringify(manifest.sourceHashes) !== JSON.stringify(expectedHashes)) throw new Error('Bundle source does not match this tool revision.');
  if (JSON.stringify(await sourceHashes(path.join(bundle, 'source'))) !== JSON.stringify(expectedHashes)) {
    throw new Error('Bundled source hashes do not match this tool revision.');
  }
  const packages = await dependencies(path.join(bundle, 'source'));
  if (JSON.stringify(manifest.packages) !== JSON.stringify(packages)) throw new Error('Bundle package manifest does not match the lockfile.');
  if (!Array.isArray(manifest.files)) throw new Error('Bundle has no file inventory.');
  const seen = new Set();
  for (const entry of manifest.files) {
    relativePath(entry.path);
    if (seen.has(entry.path)) throw new Error('Bundle inventory contains a duplicate path.');
    seen.add(entry.path);
  }
  if (JSON.stringify(manifest.files) !== JSON.stringify(await entries(bundle))) {
    throw new Error('Bundle inventory or file integrity mismatch.');
  }
  for (const pkg of packages) {
    const bytes = await fs.readFile(contentPath(path.join(bundle, 'cache'), pkg.integrity));
    const { algorithm, encoded } = integrity(pkg.integrity);
    if (createHash(algorithm).update(bytes).digest('base64') !== encoded) throw new Error(`Cached package integrity mismatch: ${pkg.name}`);
  }
  return manifest;
}

function run(command, args, options) {
  return new Promise((resolve, reject) => {
    const child = spawn(command, args, { ...options, stdio: 'inherit', shell: false });
    child.on('error', reject);
    child.on('exit', (code, signal) => code === 0 ? resolve() : reject(new Error(`Provisioning command failed: ${code ?? signal}`)));
  });
}

async function npmCli() {
  const executable = await fs.realpath(process.execPath);
  const bases = [...new Set([path.dirname(process.execPath), path.dirname(executable)])];
  const candidates = [process.env.npm_execpath,
    ...bases.flatMap(base => [path.join(base, 'node_modules/npm/bin/npm-cli.js'), path.join(base, '../lib/node_modules/npm/bin/npm-cli.js')]),
    ...(process.env.PATH ?? '').split(path.delimiter).map(base => path.join(base, 'npm'))];
  for (const candidate of candidates.filter(Boolean)) {
    try { const resolved = await fs.realpath(candidate); if (path.basename(resolved) === 'npm-cli.js') return resolved; } catch {}
  }
  throw new Error('Cannot locate npm-cli.js. Install npm beside Node or invoke this script through npm.');
}

export async function prepareBundle(output) {
  output = path.resolve(output);
  if (await exists(output)) throw new Error('Bundle output already exists. Select a new output directory.');
  const packages = await dependencies(sourceRoot);
  const installed = await readJson(path.join(sourceRoot, 'node_modules/playwright/package.json'));
  if (installed.version !== '1.64.1') throw new Error('Run npm ci in the optional environment before preparing a bundle.');
  const initialSourceHashes = await sourceHashes(sourceRoot);
  await fs.mkdir(output);
  try {
    await fs.mkdir(path.join(output, 'source'));
    for (const name of sources) await fs.copyFile(path.join(sourceRoot, name), path.join(output, 'source', name));
    for (const pkg of packages) {
      console.error(`Download ${pkg.url}`);
      const response = await fetch(pkg.url, { redirect: 'error', signal: AbortSignal.timeout(120_000) });
      if (!response.ok) throw new Error(`Package download failed: HTTP ${response.status}`);
      const bytes = Buffer.from(await response.arrayBuffer());
      const { algorithm, encoded } = integrity(pkg.integrity);
      if (createHash(algorithm).update(bytes).digest('base64') !== encoded) throw new Error(`Package integrity mismatch: ${pkg.name}`);
      const destination = contentPath(path.join(output, 'cache'), pkg.integrity);
      await fs.mkdir(path.dirname(destination), { recursive: true });
      await fs.writeFile(destination, bytes);
    }
    const browsers = path.join(output, 'browsers');
    const existingBrowsers = path.join(sourceRoot, '.browsers');
    if (await exists(existingBrowsers)) {
      if (!(await fs.lstat(existingBrowsers)).isDirectory()) throw new Error('Local browser cache must be a regular directory.');
      await fs.cp(existingBrowsers, browsers, { recursive: true, verbatimSymlinks: true });
      await fs.rm(path.join(browsers, '.links'), { recursive: true, force: true });
    }
    await run(process.execPath, [path.join(sourceRoot, 'node_modules/playwright/cli.js'), 'install', 'chromium', '--no-shell'],
      { cwd: sourceRoot, env: { ...process.env, PLAYWRIGHT_BROWSERS_PATH: browsers } });
    // Playwright creates machine-specific package links. Browser execution does not need them.
    await fs.rm(path.join(browsers, '.links'), { recursive: true, force: true });
    if (JSON.stringify(await sourceHashes(sourceRoot)) !== JSON.stringify(initialSourceHashes)) {
      throw new Error('Tool source changed during bundle preparation. Prepare again from stable source files.');
    }
    const manifest = await makeManifest(output);
    await fs.writeFile(path.join(output, 'manifest.json'), `${JSON.stringify(manifest, null, 2)}\n`);
    await verifyBundle(output);
    return { status: 'PREPARED', bundle: output, target: manifest.target, files: manifest.files.length,
      manifestSha256: sha256(await fs.readFile(path.join(output, 'manifest.json'))) };
  } catch (error) {
    await fs.rm(output, { recursive: true, force: true });
    throw error;
  }
}

export async function installBundle(bundle, destination, expectedSource = sourceRoot) {
  bundle = path.resolve(bundle);
  destination = path.resolve(destination);
  if (await exists(destination)) throw new Error('Destination already exists. Installation requires a new directory.');
  const manifest = await verifyBundle(bundle, expectedSource);
  const cli = await npmCli();
  const temporary = await fs.mkdtemp(path.join(os.tmpdir(), 'workbench-browser-install-'));
  let created = false;
  try {
    await fs.mkdir(destination);
    created = true;
    for (const name of sources) await fs.copyFile(path.join(bundle, 'source', name), path.join(destination, name));
    await fs.cp(path.join(bundle, 'browsers'), path.join(destination, '.browsers'), { recursive: true, verbatimSymlinks: true });
    await fs.cp(path.join(bundle, 'cache'), path.join(temporary, 'cache'), { recursive: true });
    const userConfig = path.join(temporary, 'user.npmrc');
    const globalConfig = path.join(temporary, 'global.npmrc');
    await fs.writeFile(userConfig, '');
    await fs.writeFile(globalConfig, '');
    const env = Object.fromEntries(Object.entries(process.env).filter(([name]) =>
      !/^npm_/i.test(name) && !/^(https?|all|no)_proxy$/i.test(name) && name !== 'NODE_OPTIONS'));
    Object.assign(env, { NPM_CONFIG_USERCONFIG: userConfig, NPM_CONFIG_GLOBALCONFIG: globalConfig,
      NPM_CONFIG_CACHE: path.join(temporary, 'cache'), NPM_CONFIG_OFFLINE: 'true',
      NPM_CONFIG_UPDATE_NOTIFIER: 'false',
      PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD: '1', PLAYWRIGHT_BROWSERS_PATH: path.join(destination, '.browsers') });
    await run(process.execPath, [cli, 'ci', '--offline', '--ignore-scripts', '--no-audit', '--no-fund', '--registry=https://registry.npmjs.org'],
      { cwd: destination, env });
    await fs.copyFile(path.join(bundle, 'manifest.json'), path.join(destination, 'bundle-manifest.json'));
    return { status: 'INSTALLED', destination, target: manifest.target,
      browsersPath: path.join(destination, '.browsers'), network: 'offline npm install; no fallback or browser download' };
  } catch (error) {
    if (created) await fs.rm(destination, { recursive: true, force: true });
    throw error;
  } finally { await fs.rm(temporary, { recursive: true, force: true }); }
}

async function main() {
  const [command, ...args] = process.argv.slice(2);
  const options = {};
  for (let i = 0; i < args.length; i += 2) {
    if (!['--output', '--bundle', '--destination'].includes(args[i]) || !args[i + 1] || args[i + 1].startsWith('--') || options[args[i]]) {
      throw new Error('Usage: node bundle.mjs prepare --output NEW_PATH | install --bundle PATH --destination NEW_PATH');
    }
    options[args[i]] = args[i + 1];
  }
  if (Number(process.versions.node.split('.')[0]) < 22 ||
      (process.versions.node.startsWith('22.') && Number(process.versions.node.split('.')[1]) < 12)) throw new Error('Node >=22.12.0 is required.');
  if (command === 'prepare' && Object.keys(options).every(key => key === '--output')) {
    return prepareBundle(options['--output'] ?? path.resolve(sourceRoot, '../../.workbench/browser-bundle'));
  }
  if (command === 'install' && options['--bundle'] && options['--destination'] && !options['--output']) {
    return installBundle(options['--bundle'], options['--destination']);
  }
  throw new Error('Usage: node bundle.mjs prepare --output NEW_PATH | install --bundle PATH --destination NEW_PATH');
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  main().then(result => console.log(JSON.stringify(result, null, 2))).catch(error => {
    console.error(JSON.stringify({ status: 'FAILED', error: error.message })); process.exitCode = 1;
  });
}
