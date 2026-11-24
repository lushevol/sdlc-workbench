// Read-only baseline/candidate source probe using the supplied captured login catalog.
const fs = require('node:fs');
const path = require('node:path');
const cp = require('node:child_process');
const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const root = path.resolve(__dirname, '../../../..');
const repo = path.join(root, 'repos/ui/mfe-base');
const ts = require(path.join(repo, 'node_modules/typescript'));
const capturePath = 'tasks/ces-entitlement-migration-20261102/ces migration/login-response.json';
const bytes = fs.readFileSync(path.join(root, capturePath));
const captured = JSON.parse(bytes);
const catalog = captured.drawers;
const hash = value => crypto.createHash('sha256').update(value).digest('hex');
const revisions = {baseline: '4c36f8e14e3d9f178b226000ebbcb41aa611616a', candidate: '5295bd7ad66f62ee5cbb547f5aa5f6ef576c41d7'};
const sources = [];
function load(revision, name, imports) {
  const source = cp.execFileSync('git', ['show', `${revision}:${name}`], {cwd: repo});
  sources.push({revision, path: `repos/ui/mfe-base/${name}`, sha256: hash(source)});
  const output = ts.transpileModule(source.toString(), {compilerOptions: {module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2020}}).outputText;
  const module = {exports: {}};
  const req = name => { assert.ok(Object.hasOwn(imports, name), `Unexpected import: ${name}`); return imports[name]; };
  new Function('require', 'module', 'exports', output)(req, module, module.exports);
  return module.exports;
}
const outcomes = {};
for (const [phase, revision] of Object.entries(revisions)) {
  const actions = [];
  const store = {drawers: catalog, workspaces: []};
  const drawer = load(revision, 'src/utils/drawer.ts', {'../hooks/HooksBase': {getHooksBase: () => ({store})}});
  const imports = {
    '../../utils/common': {uuidv4: () => 'instance', storeData: () => {}},
    '../provider': {useContext: () => [store, action => actions.push(action)]},
    '../reducer/util/ActionType': {ActionType: new Proxy({}, {get: (_, key) => key})}
  };
  if (phase === 'candidate') imports['../../utils/tileAdmission'] = load(revision, 'src/utils/tileAdmission.ts', {});
  const dispatcher = load(revision, 'src/hooks/dispathcer/index.ts', imports).default();
  dispatcher.dispatchOpenTile({from: 'captured-catalog'}, 'modal');
  const modal = catalog.flatMap(x => x.tiles).filter(x => x.tile === '/modal');
  assert.deepEqual(modal.map(x => x.id), ['66', '72']);
  assert.equal(actions.length, 1);
  if (phase === 'candidate') assert.equal(actions.filter(x => x.type === 'ADD_WORKSPACE').length, 0);
  const lookup = drawer.findTileConfig(catalog, '@fm/template_container', '/template', '/modal');
  outcomes[phase] = {captured_modal_ids: modal.map(x => x.id), dispatch_action: actions[0]?.type, dispatched_tile_id: actions[0]?.data?.workspace?.containers?.[0]?.id ?? null, deep_link_lookup_id: lookup?.id ?? null};
}
assert.equal(outcomes.baseline.dispatch_action, 'ADD_WORKSPACE');
assert.equal(outcomes.candidate.dispatch_action, 'SET_ERRORMSG');
assert.equal(outcomes.baseline.deep_link_lookup_id, '66');
assert.equal(outcomes.candidate.deep_link_lookup_id, null);
const result = {
  captured_at: new Date().toISOString(), status: 'PASSED',
  case: 'TC-FE-CES-015',
  definition: 'tasks/ces-entitlement-migration-20261102/06-test-cases.md#tc-fe-ces-015',
  runner: {path: path.relative(root, __filename), sha256: hash(fs.readFileSync(__filename))},
  capture: {path: capturePath, sha256: hash(bytes)}, sources, outcomes,
  substitutions: ['Hook store and dispatch are controlled.', 'UUID generation is controlled.', 'TypeScript compiles actual versioned modules; imports are bounded substitutes.'],
  limits: ['This is a module/source execution, not a browser or live deployed API test.', 'The supplied login is historical captured evidence, not a current entitlement response.', 'No actual upper application caller of modal was found. The existing dispatcher API has this reachable changed behavior.']
};
fs.writeFileSync(path.join(__dirname, 'upper-launch-probe.json'), JSON.stringify(result, null, 2) + '\n');
console.log(JSON.stringify(outcomes));
