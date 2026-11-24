'use strict';
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const crypto = require('node:crypto');
const assert = require('node:assert/strict');
const { execFileSync } = require('node:child_process');
const workspace = path.resolve(__dirname, '../../../..');
const repository = path.join(workspace, 'repos/testing/ratan-test-engine');
const relative = 'Tests/ratan/plugin/ui/session';
const base = path.join(repository, relative);
const acorn = require(path.join(workspace, 'repos/ui/mfe-base/node_modules/acorn'));
const inputs = JSON.parse(fs.readFileSync(path.join(__dirname, 'inputs.json')));
const original = execFileSync('git', ['-C', repository, 'show', `${inputs.revision}:${relative}/sessionRenewal.cjs`], { encoding: 'utf8' });
const hash = value => crypto.createHash('sha256').update(value).digest('hex');
const record = { status: 'IN_PROGRESS', baseline: inputs.revision, checks: [], newBusinessExecutions: 0 };
function save() { fs.writeFileSync(path.join(__dirname, 'offline-checks.json'), JSON.stringify(record, null, 2) + '\n'); }
async function check(name, operation) {
  try { record.checks.push({ name, status: 'PASSED', details: await operation() }); save(); }
  catch (error) { record.status = 'FAILED'; record.checks.push({ name, status: 'FAILED', error: error.message }); save(); throw error; }
}
function functions(source) {
  const tree = acorn.parse(source, { ecmaVersion: 2020 });
  return tree.body.flatMap(node => {
    if (node.type === 'FunctionDeclaration') return [{ name: node.id.name, source: source.slice(node.start, node.end), node }];
    if (node.type !== 'VariableDeclaration') return [];
    return node.declarations.filter(decl => decl.id.type === 'Identifier' && decl.init?.type === 'ArrowFunctionExpression')
      .map(decl => ({ name: decl.id.name, source: source.slice(decl.init.start, decl.init.end), node: decl.init }));
  });
}
function canonical(node) {
  return JSON.stringify(node, (key, value) => ['start', 'end', 'loc'].includes(key) ? undefined : value);
}
async function main() {
  const current = require(path.join(base, 'sessionRenewal.cjs'));
  const provenance = require(path.join(base, 'support/provenance.cjs')).sourceProvenance;
  const sourceFiles = provenance().testSourceFiles;
  await check('JavaScript syntax', () => {
    const scripts = sourceFiles.filter(file => file.path.endsWith('.cjs'));
    for (const file of scripts) execFileSync(process.execPath, ['--check', path.join(base, file.path)]);
    return { files: scripts.length, node: process.version };
  });
  await check('All original function bodies and assertions', () => {
    const before = functions(original);
    const after = sourceFiles.filter(file => file.path.endsWith('.cjs')).flatMap(file => {
      let text = fs.readFileSync(path.join(base, file.path), 'utf8');
      if (file.path === 'support/session.cjs') text = text.replace('...sourceProvenance(),', 'testSourceSha256: hash(fs.readFileSync(__filename)),');
      return functions(text).map(fn => ({ ...fn, file: file.path }));
    });
    const matched = before.map(old => {
      const found = after.find(fn => fn.name === old.name && canonical(fn.node) === canonical(old.node));
      assert.ok(found, `Changed or missing function: ${old.name}`);
      return { name: old.name, file: found.file, originalFunctionSha256: hash(old.source) };
    });
    assert.equal(matched.length, 41);
    return { functions: matched, exception: 'Only retain() source provenance fields changed; its comparison normalizes that documented replacement.' };
  });
  await check('Browser extension export contract', () => {
    const directory = fs.mkdtempSync(path.join(os.tmpdir(), 'session-original-'));
    try {
      const file = path.join(directory, 'original.cjs'); fs.writeFileSync(file, original); const previous = require(file);
      assert.deepEqual(Object.keys(current), Object.keys(previous));
      const names = Object.keys(previous).filter(name => typeof previous[name] === 'function');
      const parameters = fn => fn.toString().match(/^[^(]*\(([^)]*)\)/)[1];
      for (const name of names) {
        assert.equal(current[name].length, previous[name].length, name);
        assert.equal(parameters(current[name]), parameters(previous[name]), name);
        assert.equal(current[name].rfdoc, previous[name].rfdoc, name);
      }
      assert.equal(current.__esModule, true);
      return { exportedFunctions: names.length, parametersAndDocumentationUnchanged: true };
    } finally { fs.rmSync(directory, { recursive: true }); }
  });
  await check('Complete source manifest and change detection', () => {
    const directory = fs.mkdtempSync(path.join(os.tmpdir(), 'session-source-manifest-'));
    try {
      const before = provenance();
      assert.equal(before.testSourceFiles.length, 29);
      for (const file of before.testSourceFiles) {
        const target = path.join(directory, file.path); fs.mkdirSync(path.dirname(target), { recursive: true }); fs.copyFileSync(path.join(base, file.path), target);
      }
      const copied = require(path.join(directory, 'support/provenance.cjs')).sourceProvenance;
      assert.deepEqual(copied(), before);
      fs.appendFileSync(path.join(directory, 'cases/e2e-01.cjs'), '\n// Controlled offline provenance check.\n');
      const changed = copied();
      assert.equal(changed.testSourceSha256, before.testSourceSha256);
      assert.notEqual(changed.testSourceManifestSha256, before.testSourceManifestSha256);
      assert.equal(changed.testSourceFiles.filter((file, i) => file.sha256 !== before.testSourceFiles[i].sha256).length, 1);
      return { boundFiles: before.testSourceFiles.length, sourceManifestSha256: before.testSourceManifestSha256, caseOnlyChangeDetected: true, fixture: 'Temporary source copy; no repository source mutated.' };
    } finally { fs.rmSync(directory, { recursive: true }); }
  });
  await check('Offline Robot syntax', () => {
    const command = ['scripts/workbench.py', 'parse', `${relative}/session_renewal.robot`];
    const output = execFileSync(path.join(repository, '.venv/bin/python'), command, { cwd: repository, encoding: 'utf8' });
    return { command, result: JSON.parse(output) };
  });
  await check('Existing unrelated checkout changes', () => {
    for (const [file, expected] of Object.entries(inputs.preexisting_changes)) assert.equal(hash(fs.readFileSync(path.join(repository, file))), expected, file);
    return { files: Object.keys(inputs.preexisting_changes), unchanged: true };
  });
  await check('Activity case dispatch and shared session state', async () => {
    const activity = require(path.join(base, 'support/activity.cjs'));
    const originalActivity = activity.assertActivityRenewsSession;
    const calls = [];
    activity.assertActivityRenewsSession = async (kind, page) => { calls.push({ kind, page }); return kind; };
    try {
      for (const file of ['sessionRenewal.cjs', 'cases/e2e-01.cjs', 'cases/e2e-02.cjs', 'cases/e2e-03.cjs']) delete require.cache[require.resolve(path.join(base, file))];
      const facade = require(path.join(base, 'sessionRenewal.cjs')); const page = {};
      for (const kind of ['mouse', 'keyboard', 'scroll', 'unsupported']) assert.equal(await facade.assertActivityRenewsSession(kind, page), kind);
      assert.deepEqual(calls.map(call => call.kind), ['mouse', 'keyboard', 'scroll', 'unsupported']);
      assert.ok(calls.every(call => call.page === page));
      const { sessions } = require(path.join(base, 'support/common.cjs')); const marker = {};
      sessions.set(page, marker); assert.equal(require(path.join(base, 'support/common.cjs')).sessions.get(page), marker);
      return { activityKindsRouted: 3, legacyFallbackPreserved: true, singletonSessionStore: true, fixture: 'Controlled routing stub; no browser or authentication operation.' };
    } finally { activity.assertActivityRenewsSession = originalActivity; }
  });
  record.status = 'PASSED'; record.recordedAt = new Date().toISOString(); record.sourceFiles = sourceFiles; save();
  console.log(JSON.stringify({ status: record.status, checks: record.checks.length, originalFunctions: 41, exportedFunctions: 21, sourceFiles: sourceFiles.length, newBusinessExecutions: 0 }));
}
main().catch(error => { console.error(error.message); process.exitCode = 1; });
