// Controlled browser integration of actual shared modules; no live identity or BFF service.
// Canonical cases: ../06-test-cases.md#tc-fe-ces-006 through #tc-fe-ces-012.
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import fs from 'node:fs/promises';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
import http from 'node:http';

const directory = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(directory, '../../..');
process.env.PLAYWRIGHT_BROWSERS_PATH ??= path.join(root, 'adapters/browser/.browsers');
const { chromium } = await import('@playwright/test');
const task = path.resolve(directory, '..');
const phase = process.argv.includes('--baseline') ? 'baseline' : 'candidate';
const output = path.resolve(process.env.CES_TEST_OUTPUT ?? path.join(task, 'evidence/frontend-entitlement-implementation-20261106', `browser-${phase}`));
const requireBase = createRequire(path.join(root, 'repos/ui/mfe-base/package.json'));
const esbuild = requireBase('esbuild');
const hash = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
await fs.mkdir(output, { recursive: true });
try { await fs.access(path.join(output, 'run.json')); throw new Error(`Refusing to overwrite completed run: ${output}`); }
catch (error) { if (error.code !== 'ENOENT') throw error; }
const base = path.join(root, 'repos/ui/mfe-base/src');
const container = path.join(root, 'repos/ui/mfe-ratan-container/src');
const fixtures = [];
const built = await esbuild.build({
  stdin: { contents: `import * as login from ${JSON.stringify(path.join(base, 'utils/login.ts'))};
    import * as drawer from ${JSON.stringify(path.join(base, 'utils/drawer.ts'))};
    import * as profile from ${JSON.stringify(path.join(base, 'components/Profile/util.ts'))};
    import * as auth from ${JSON.stringify(path.join(container, 'ratanutils/authenticator.ts'))};
    window.ces = { login, drawer, profile, auth };`, resolveDir: root, loader: 'ts' },
  bundle: true, write: false, format: 'iife', platform: 'browser', metafile: true,
  plugins: [{ name: 'controlled-hooks', setup(build) {
    build.onResolve({ filter: /HooksBase$|\/Root\/import$/ }, () => ({ path: 'hooks', namespace: 'fixture' }));
    build.onResolve({ filter: /^\.\/logger$/ }, args => args.importer === path.join(container, 'ratanutils/authenticator.ts')
      ? { path: 'entitlement-logger', namespace: 'fixture' } : undefined);
    build.onResolve({ filter: /^\.\/common$/ }, args => args.importer === path.join(base, 'utils/login.ts')
      ? { path: 'login-transport', namespace: 'fixture' } : undefined);
    build.onLoad({ filter: /.*/, namespace: 'fixture' }, args => {
      fixtures.push(args.path);
      return { contents: args.path === 'entitlement-logger' ? `
        export const logger = {info: message => {
          const prefix = 'Entitlement permission ';
          if (typeof message === 'string' && message.startsWith(prefix)) {
            (window.__permissionLogs ??= []).push(JSON.parse(message.slice(prefix.length)));
          }
        }};` : args.path === 'hooks' ? `
        export const getHooksBase = () => ({store: window.__store, baseDispatch: action => Object.assign(window.__store, action.data)});
        export const Hooks = { getHooks: getHooksBase };` : `
        export const clearStorageWhenLogout = () => {};
        export const getJWTPayload = () => '';
        export const storeData = () => {};
      `, loader: 'js' };
    });
  } }],
});
const sourceBindings = await Promise.all(Object.keys(built.metafile.inputs).filter(file => !file.startsWith('fixture:') && !file.startsWith('<')).map(async file => {
  const absolute = path.resolve(root, file);
  return { path: path.relative(root, absolute), sha256: hash(await fs.readFile(absolute)) };
}));
const catalog = path.join(task, '06-test-cases.md');
const run = { phase, startedAt: new Date().toISOString(), scope: 'ACTUAL_SHARED_MODULES_CONTROLLED_BROWSER',
  sourceBindings, catalog: { path: path.relative(root, catalog), sha256: hash(await fs.readFile(catalog)) },
  substitutions: [...new Set(fixtures)], limits: ['Hooks store and dispatcher are controlled fixtures.',
    'Login token decoding and persistence are substituted; neither identity nor session acceptance is tested.',
    'Permission logger transport is substituted with local capture; remote log acceptance is not tested.',
    'The complete portal, saved-view backend, CES service, and BFF controller are not executed.'], cases: [] };
await fs.writeFile(path.join(output, 'run-binding.json'), JSON.stringify(run, null, 2));
const bundle = built.outputFiles[0].text;
const server = http.createServer((req, res) => {
  res.setHeader('content-type', req.url === '/bundle.js' ? 'application/javascript' : 'text/html');
  res.end(req.url === '/bundle.js' ? bundle : '<!doctype html><title>CES shared module integration</title><main><h1>CES shared module integration</h1><output id="result"></output></main><script>window.__store={}</script><script src="/bundle.js"></script>');
});
await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
process.env.PLAYWRIGHT_BROWSERS_PATH ??= path.join(root, 'adapters/browser/.browsers');
let browser;
const legacy = { name: 'X_RATANONE', roleName: 'PSS', subjects: [{ name: 'feature-a', actions: [{ name: 'action-a' }] }] };
const ces = { name: 'RATAN_ENTITLEMENT_RULE', applicationName: 'RATAN', applicationId: '51358', roleName: null,
  roleList: ['Role A', 'Role B'], subjects: [{ name: 'feature-a', entitlementSource: 'EMS3', actions: [{ name: 'action-a' }] }] };
const route = (source = 'EMS3', tileId = '1') => ({ tileId, source, entityNames: source === 'EMS3' ? ['RATAN_ENTITLEMENT_RULE'] : ['X_RATANONE'], features: ['feature-a'], ...(source === 'EMS3' ? { applicationId: '51358' } : {}) });
try {
  browser = await chromium.launch({ channel: 'chromium', headless: true, chromiumSandbox: true });
  run.browserVersion = browser.version();
  async function check(id, name, fixture, operation, expected, expectedSource) {
    const context = await browser.newContext();
    const page = await context.newPage();
    const record = { id, name, startedAt: new Date().toISOString(), expected, status: 'RUNNING' };
    try {
      await page.goto(`http://127.0.0.1:${server.address().port}`);
      await page.evaluate(fixture => { window.__store = fixture; }, fixture);
      record.actual = await page.evaluate(operation);
      assert.deepEqual(record.actual, expected);
      if (expectedSource) {
        record.sourceLogs = await page.evaluate(() => window.__permissionLogs ?? []);
        assert.ok(record.sourceLogs.some(log => log.code === 'feature-a:action-a' && log.source === expectedSource && log.allowed === expected), `Missing ${expectedSource} decision log`);
      }
      record.status = 'PASSED';
    } catch (error) { record.status = 'FAILED'; record.error = error.message; }
    finally {
      record.endedAt = new Date().toISOString();
      const filename = `${id}-${name}.json`;
      await fs.writeFile(path.join(output, filename), JSON.stringify(record, null, 2));
      run.cases.push({ id, name, status: record.status, path: filename });
      await fs.writeFile(path.join(output, 'progress.json'), JSON.stringify(run.cases, null, 2));
      await context.close();
    }
  }
  await check('TC-FE-CES-007', 'unchanged-calls', { entities: [ces], entitlementRouting: [route()] },
    () => [window.ces.auth.hasPermission('feature-a:action-a'), window.ces.auth.hasPermission('feature-a:missing')], [true, false]);
  await check('TC-FE-CES-008', 'union-legacy-only', { entities: [legacy, { ...ces, subjects: [] }], entitlementRouting: [route()], user: { entitlement: { actions: ['feature-a:action-a'] } } },
    () => window.ces.auth.hasPermission('feature-a:action-a'), true, 'EMS2');
  await check('TC-FE-CES-008', 'union-ces-only', { entities: [{ ...legacy, subjects: [] }, ces], entitlementRouting: [route('EMS2'), route('EMS3', '2')] },
    () => window.ces.auth.hasPermission('feature-a:action-a'), true, 'EMS3');
  await check('TC-FE-CES-006', 'duplicate-and-app-scope', { entities: [{ ...ces, subjects: [] }, ces, { ...ces, applicationId: 'other' }], entitlementRouting: [route()] },
    () => window.ces.auth.hasPermission('feature-a:action-a'), true);
  await check('TC-FE-CES-008', 'union-both', { entities: [legacy, ces], entitlementRouting: [route(), route('EMS2', '2')] },
    () => window.ces.auth.hasPermission('feature-a:action-a'), true, 'EMS2');
  await check('TC-FE-CES-008', 'union-neither', { entities: [{ ...legacy, subjects: [] }, { ...ces, subjects: [] }], entitlementRouting: [route(), route('EMS2', '2')] },
    () => window.ces.auth.hasPermission('feature-a:action-a'), false, 'NONE');
  await check('TC-FE-CES-008', 'legacy-without-routes', { entities: [legacy, ces] },
    () => window.ces.auth.hasPermission('feature-a:action-a'), true, 'EMS2');
  await check('TC-FE-CES-006', 'ces-requires-application-route', { entities: [ces] },
    () => window.ces.auth.hasPermission('feature-a:action-a'), false, 'NONE');
  await check('TC-FE-CES-006', 'ces-empty-routes-deny', { entities: [ces], entitlementRouting: [] },
    () => window.ces.auth.hasPermission('feature-a:action-a'), false, 'NONE');
  await check('TC-FE-CES-006', 'reject-unrelated-application', { entities: [{ ...ces, applicationId: 'other' }], entitlementRouting: [route()] },
    () => window.ces.auth.hasPermission('feature-a:action-a'), false);
  await check('TC-FE-CES-006', 'reject-unrelated-feature-action', { entities: [ces], entitlementRouting: [route()] },
    () => [window.ces.auth.hasPermission('other-feature:action-a'), window.ces.auth.hasPermission('feature-a:missing'), window.ces.auth.hasPermission('feature-a:action-a:extra')], [false, false, false]);
  await check('TC-FE-CES-010', 'refresh-removes-grant', { entities: [ces], entitlementRouting: [route()], drawers: [{ tiles: [{ id: 1 }] }] },
    () => { window.ces.login.handleEntities({ data: { entities: [] } }); window.ces.login.handleDrawers({ data: { drawers: [] } }); return [window.ces.auth.hasPermission('feature-a:action-a'), window.__store.drawers.length]; }, [false, 0]);
  await check('TC-FE-CES-011', 'profile-and-roles', { entities: [ces], user: { id: '1481696', fullName: 'Fixture User' } },
    () => [window.ces.profile.getName(window.__store.entities[0]), window.__store.entities.find(entity => entity.applicationId === '51358' && entity.name === 'RATAN_ENTITLEMENT_RULE').roleList, window.ces.auth.getUser().role ?? null],
    ['RATAN :: RATAN_ENTITLEMENT_RULE :: Role A, Role B', ['Role A', 'Role B'], null]);
  const tile = { id: 1, container: '@fixture/container', module: 'feature-a', tile: 'main', entryName: 'a' };
  await check('TC-FE-CES-012', 'restore-exact-id', { drawers: [{ tiles: [tile, { ...tile, id: 2, entryName: 'b' }] }] },
    () => window.ces.drawer.findTile(window.__store.drawers, { containers: [{ applicationTileId: '2', container: '@fixture/container', module: 'feature-a', tile: 'main', entryName: 'b' }] })?.id, 2);
  await check('TC-FE-CES-012', 'restore-legacy-first-match', { drawers: [{ tiles: [tile, { ...tile, id: 2 }] }] },
    () => window.ces.drawer.findTile(window.__store.drawers, { containers: [{ container: '@fixture/container', module: 'feature-a', tile: 'main', entryName: 'a' }] })?.id ?? null, 1);
  await check('TC-FE-CES-012', 'restore-ces-ambiguous', { drawers: [{ tiles: [{ ...tile, entitlementSource: 'EMS3' }, { ...tile, id: 2, entitlementSource: 'EMS3' }] }] },
    () => window.ces.drawer.findTile(window.__store.drawers, { containers: [{ container: '@fixture/container', module: 'feature-a', tile: 'main', entryName: 'a' }] })?.id ?? null, null);
} finally {
  await browser?.close();
  await new Promise(resolve => server.close(resolve));
  run.endedAt = new Date().toISOString();
  run.status = run.cases.some(item => item.status === 'FAILED') || !run.cases.length ? 'FAILED' : 'PASSED';
  await fs.writeFile(path.join(output, 'run.json'), JSON.stringify(run, null, 2));
}
console.log(JSON.stringify({ phase, status: run.status, cases: run.cases, output }, null, 2));
if (run.status !== 'PASSED') process.exitCode = 1;
