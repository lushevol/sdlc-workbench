import { chromium } from '../../adapters/browser/node_modules/playwright/index.mjs';
import { spawn } from 'node:child_process';
import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';

const root = process.cwd();
const base = path.join(root, '.workbench/uat-blotter-browser-20261021');
const [caseId = 'UAT-BLOTTER-PRIOR-TILE', runId = `run-${Date.now()}`] = process.argv.slice(2);
assert.ok(['inspect-prior', 'UAT-BLOTTER-PRIOR-TILE'].includes(caseId), 'Unknown prior-tile case.');
assert.match(runId, /^[a-zA-Z0-9_-]+$/, 'Unsafe run identifier.');
const output = path.join(root, 'tasks/portal-background-session-20261019/evidence/uat-blotter-browser-20261021/browser', runId);
const target = process.env.BLOTTER_TARGET_URL || 'http://localhost:8126/';
assert.ok(['localhost', '127.0.0.1'].includes(new URL(target).hostname), 'This runner permits local fixtures only.');
await fs.mkdir(path.dirname(output), { recursive: true });
await fs.mkdir(output, { recursive: false });
const hash = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));
const safeUrl = value => { try { const u = new URL(value); return u.origin + u.pathname; } catch { return String(value).split('?')[0]; } };
const safe = error => String(error?.message || error)
  .split(process.env.SESSION_E2E_USERNAME || '__NO_USERNAME__').join('[USERNAME]')
  .split(process.env.SESSION_E2E_PASSWORD || '__NO_PASSWORD__').join('[PASSWORD]')
  .replace(/(?:Bearer\s+)?eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+/g, '[TOKEN]')
  .replace(/https?:\/\/[^\s)"']+/g, safeUrl);
const tokenSummary = token => {
  if (!token) return null;
  let claims = {};
  try { claims = JSON.parse(Buffer.from(token.split('.')[1], 'base64url').toString('utf8')); } catch {}
  return { sha256: hash(token), iat: Number.isFinite(claims.iat) ? claims.iat : null, exp: Number.isFinite(claims.exp) ? claims.exp : null };
};
const tile = { title: 'Cashflow Blotter', container: '@fm/ratan_container', module: '/cashflow_blotter_cn', tile: '/cashflow_cn', emailSupport: 'local@example.invalid', entity: ['X_RATANONE'], subject: 'RATAN_STRATEGIC_CASHFLOW_BLOTTER', isTemplate: true, imageDarkTheme: '' };
const dashboardTile = { ...tile, title: 'Cashflow Dashboard', tile: '/cashflow_cn_dashboard' };
const drawers = [{ id: 1, label: 'Local investigation fixture', tiles: [tile, dashboardTile] }];
const entities = [{ id: 1, name: 'X_RATANONE', applicationName: 'LOCAL', roleId: 1, roleName: 'LOCAL', subjects: [{ id: 1, name: 'RATAN_STRATEGIC_CASHFLOW_BLOTTER', longName: 'RATAN_STRATEGIC_CASHFLOW_BLOTTER', actions: [{ id: 1, entitlementId: 1, name: 'UI_Read_Access' }] }] }];
const workspace = { id: 'local-blotter-workspace', label: 'Cashflow Blotter', isActive: true, containers: [{ ...tile, id: 'local-blotter-container', panelId: 'local-blotter-panel', tabId: 'local-blotter-workspace' }] };
let fixtures = { storage: {}, responses: [
  { pathname: '/api/ratan/rule/v1/fields', body: { fields: [
    { indexedTerm: 'Cashflow.Cashflow_Id', businessTerm: 'Cashflow ID', dataType: 'String', context: 'CASHFLOW_DATA', scope: '{"disabledBlotter":[]}', valueList: '[]' },
    { indexedTerm: 'Cashflow.Cashflow_State', businessTerm: 'Cashflow State', dataType: 'String', context: 'CASHFLOW_DATA', scope: '{"disabledBlotter":[]}', valueList: '["WAITING"]' },
  ], version: { fieldsConfig: 1, fields: 1 } } },
  { pathname: '/api/ratan/rule/v1/fields/versions', body: { ratan_suppression_fields_config: { activedVersion: 1 }, ratan_suppression_fields: { activedVersion: 1 } } },
] };
if (process.env.BLOTTER_FIXTURE_FILE) fixtures = JSON.parse(await fs.readFile(process.env.BLOTTER_FIXTURE_FILE, 'utf8'));
const record = {
  caseId, runId, status: 'STARTING', startedAt: new Date().toISOString(), clock: 'REAL_WALL_CLOCK', target: safeUrl(target),
  runnerSha256: hash(await fs.readFile(new URL(import.meta.url))), fixtureSha256: hash(JSON.stringify({ drawers, entities, workspaces, fixtures })),
  nativeContextPolicy: 'Fresh native Edge process and default profile context; CDP noDefaults=true; no incognito context.',
  observationLimits: ['CDP and a passive DOM observer remain attached. Natural browser freezing is not established.', 'Local identity, catalog, entitlement, and business response fixtures replace external systems. UAT parity is not established.'],
  testDoubles: ['Catalog and entitlements are injected into successful real local BFF auth response bodies. Auth headers remain real.', 'Two preseeded workspaces mount actual Dashboard and Blotter. The driver visits Dashboard, then selects Blotter through the real workspace tab.', 'Non-auth /api endpoints use disclosed local network fixtures; missing exact fixtures use an empty candidate response.'],
  catalog: { drawers, entities, workspaces }, fixtures, dashboardIntervalPolicy: 'Application DASHBOARD_REFRESH_INTERVAL remains 120000 milliseconds. No clock override or interval replacement is used.', baselineRunnerSha256: 'b85cfb7b830d81c1f65bb12c2befc2691c37f65df6e21c75eb568db62ba33641', apiResponses: [], requests: [], requestFailures: [], pageErrors: [], fixtureHits: [], nativeTabActivations: [], assertions: [], checkpoints: [],
};
record.testDoubles.push('Dashboard count queries use exact local zero-count GraphQL response shapes; actual Dashboard code, query order, middleware, and 120-second timer remain unchanged.');
if (caseId === 'UAT-BLOTTER-NO-REFRESH') record.testDoubles.push('Every /refreshtoken request is rejected with HTTP 503. No credential expiry error is returned.');
let writeQueue = Promise.resolve();
const save = () => { const data = JSON.stringify(record, null, 2) + '\n'; writeQueue = writeQueue.then(() => fs.writeFile(path.join(output, 'result.json'), data)); return writeQueue; };
await save();
let owned, page, context, cdp;
let lastRefresh = null;
function stackSummary(stack, depth = 0) {
  if (!stack || depth > 4) return undefined;
  return { callFrames: (stack.callFrames || []).map(frame => ({ functionName: safe(frame.functionName), url: safeUrl(frame.url), lineNumber: frame.lineNumber, columnNumber: frame.columnNumber })), parent: stackSummary(stack.parent, depth + 1) };
}
async function launchNative() {
  const profilePath = path.join(base, `profile-${runId}`);
  await fs.mkdir(profilePath, { recursive: false });
  const args = [`--user-data-dir=${profilePath}`, '--remote-debugging-port=0', '--remote-debugging-address=127.0.0.1', '--no-first-run', '--no-default-browser-check', '--disable-background-networking', '--disable-component-update', '--disable-sync', '--disable-edgeupdater', '--disable-updater-scheduler', '--disable-features=msForceBrowserSignIn,msEdgeUpdateLaunchServicesPreferredVersion', 'about:blank'];
  const child = spawn('/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge', args, { stdio: 'ignore' });
  owned = { child, profilePath };
  owned.exited = new Promise(resolve => { child.once('exit', resolve); child.once('error', error => { owned.launchError = error; resolve(); }); });
  record.nativeBrowser = { profilePath, args, pid: child.pid, status: 'STARTING' };
  await save();
  let port;
  for (let i = 0; i < 150; i++) {
    if (owned.launchError) throw owned.launchError;
    if (child.exitCode !== null || child.signalCode !== null) throw new Error('Native Edge exited during startup.');
    try { port = Number((await fs.readFile(path.join(profilePath, 'DevToolsActivePort'), 'utf8')).split('\n')[0]); } catch {}
    if (port > 0) break;
    await sleep(100);
  }
  assert.ok(port, 'Native Edge must publish a debugging endpoint.');
  owned.browser = await chromium.connectOverCDP(`http://127.0.0.1:${port}`, { noDefaults: true });
  context = owned.browser.contexts()[0];
  assert.ok(context, 'Native Edge default context must exist.');
  record.nativeBrowser.version = owned.browser.version(); record.nativeBrowser.status = 'CONNECTED';
  page = await context.newPage();
  page.on('pageerror', error => { record.pageErrors.push({ time: Date.now(), error: safe(error) }); });
  page.on('requestfailed', request => { record.requestFailures.push({ time: Date.now(), url: safeUrl(request.url()), error: safe(request.failure()?.errorText) }); });
  page.on('dialog', async dialog => { record.browserDialogs ??= []; record.browserDialogs.push({ time: Date.now(), type: dialog.type() }); if (dialog.type() === 'beforeunload') await dialog.accept(); else await dialog.dismiss(); });
  page.on('response', response => {
    const url = new URL(response.url());
    if (!url.pathname.includes('/api/')) return;
    const headers = response.headers();
    const item = { time: Date.now(), url: safeUrl(response.url()), status: response.status(), access: tokenSummary(headers['single-ui-authorization']), refresh: tokenSummary(headers['single-ui-refresh']) };
    if (item.refresh) lastRefresh = item.refresh;
    record.apiResponses.push(item);
  });
  cdp = await context.newCDPSession(page);
  await cdp.send('Network.enable');
  cdp.on('Network.requestWillBeSent', event => {
    const url = new URL(event.request.url);
    if (!url.pathname.includes('/api/')) return;
    let bodyShape;
    if (event.request.postData && !url.pathname.includes('/auth/')) {
      try { const value = JSON.parse(event.request.postData); bodyShape = { keys: Object.keys(value), operationName: typeof value.operationName === 'string' ? value.operationName : null, query: typeof value.query === 'string' ? value.query.slice(0, 3000) : null }; } catch { bodyShape = { encoding: 'non-JSON' }; }
    }
    record.requests.push({ time: Date.now(), requestId: event.requestId, url: safeUrl(event.request.url), method: event.request.method, type: event.type, bodyShape, initiator: { type: event.initiator.type, url: safeUrl(event.initiator.url || ''), stack: stackSummary(event.initiator.stack) } });
  });
  await context.addInitScript(({ workspaces, extraStorage }) => {
    if (!['localhost', '127.0.0.1'].includes(location.hostname)) return;
    if (!sessionStorage.getItem('__blotterFixtureSeeded')) {
      localStorage.setItem('SET_WORKSPACES', JSON.stringify(workspaces));
      for (const [key, value] of Object.entries(extraStorage)) localStorage.setItem(key, typeof value === 'string' ? value : JSON.stringify(value));
      sessionStorage.setItem('__blotterFixtureSeeded', 'true');
    }
    const state = window.__blotterObservation = { events: [], timeoutVisible: false, signInVisible: false, trustedActivity: { mousemove: 0, keydown: 0, scroll: 0 } };
    const push = event => state.events.push({ event, time: Date.now(), visibility: document.visibilityState });
    for (const name of ['visibilitychange', 'freeze', 'resume']) document.addEventListener(name, () => push(name), { passive: true });
    for (const name of ['pageshow', 'pagehide']) window.addEventListener(name, () => push(name), { passive: true });
    for (const name of ['mousemove', 'keydown', 'scroll']) document.addEventListener(name, event => { if (event.isTrusted) state.trustedActivity[name]++; }, { capture: true, passive: true });
    const inspect = () => {
      const visible = selector => { const element = document.querySelector(selector); return !!element && element.getClientRects().length > 0; };
      const timeoutVisible = visible('[aria-labelledby="timeout-dialog-title"]');
      const signInVisible = visible('[data-testid="Username"] input');
      if (timeoutVisible !== state.timeoutVisible) { state.timeoutVisible = timeoutVisible; push(timeoutVisible ? 'timeout_opened' : 'timeout_closed'); }
      if (signInVisible !== state.signInVisible) { state.signInVisible = signInVisible; push(signInVisible ? 'sign_in_visible' : 'sign_in_hidden'); }
    };
    new MutationObserver(inspect).observe(document, { childList: true, subtree: true, attributes: true });
    push('observer_attached');
  }, { workspaces, extraStorage: fixtures.storage || {} });
  await context.route('**/api/**', async route => {
    const request = route.request(), pathname = new URL(request.url()).pathname;
    if (pathname.includes('/auth/')) {
      if (caseId === 'UAT-BLOTTER-NO-REFRESH' && pathname.endsWith('/refreshtoken')) {
        record.fixtureHits.push({ time: Date.now(), pathname, fixture: 'REFRESH_ACQUISITION_REJECTED_503' });
        return route.fulfill({ status: 503, contentType: 'application/json', body: JSON.stringify({ message: 'LOCAL_REFRESH_ACQUISITION_REJECTED' }) });
      }
      if (/\/sso\/(login|validate|extend|relogin)$/.test(pathname)) {
        const upstream = await route.fetch();
        if (!upstream.ok()) return route.fulfill({ response: upstream });
        const data = await upstream.json();
        data.drawers = drawers; data.entities = entities;
        record.fixtureHits.push({ time: Date.now(), pathname, fixture: 'AUTH_BODY_CATALOG_AND_ENTITLEMENTS', upstreamStatus: upstream.status() });
        return route.fulfill({ response: upstream, json: data });
      }
      return route.continue();
    }
    let dashboardFixture;
    if (pathname === '/api/ratan/stmcn/v1/cashflows' && request.method() === 'POST') {
      let query = ''; try { query = JSON.parse(request.postData() || '{}').query || ''; } catch {}
      if (query.includes('SettlementCashflowDataUltraQueryCount')) dashboardFixture = { data: { cashflowUltraQueryCount: { count: 0 } } };
      else if (query.includes('SettlementGroupMessageCount')) dashboardFixture = { data: { groupMessages: { pageInfo: { totalHits: 0 } } } };
    }
    const exact = (fixtures.responses || []).find(item => item.pathname === pathname && (!item.method || item.method === request.method()));
    const body = dashboardFixture ?? exact?.body ?? { data: [], result: true };
    if (dashboardFixture) record.fixtureHits.push({ time: Date.now(), pathname, fixture: 'DASHBOARD_COUNT_GRAPHQL_SHAPE', body: dashboardFixture });
    record.fixtureHits.push({ time: Date.now(), pathname, fixture: exact ? 'EXACT_BUSINESS_FIXTURE' : 'EMPTY_CANDIDATE_BUSINESS_RESPONSE' });
    return route.fulfill({ status: exact?.status ?? 200, contentType: exact?.contentType ?? 'application/json', body: typeof body === 'string' ? body : JSON.stringify(body) });
  });
  await page.bringToFront();
  await save();
}
async function checkpoint(label, screenshot = true) {
  const browserState = await page.evaluate(() => ({ now: Date.now(), visibility: document.visibilityState, timeoutVisible: !!document.querySelector('[aria-labelledby="timeout-dialog-title"]')?.getClientRects().length, signInVisible: !!document.querySelector('[data-testid="Username"] input')?.getClientRects().length, homeMounted: !!document.querySelector('[aria-label="workspaces"]'), blotterMounted: !!document.querySelector('[data-testid$="_Cashflow"]'), dashboardMounted: !!document.querySelector('[data-testid$="_Cashflow_Dashboard"]'), dashboardHidden: !!document.querySelector('[data-testid$="_Cashflow_Dashboard"]')?.closest('[hidden]'), selectedWorkspace: document.querySelector('[role="tab"][aria-selected="true"]')?.textContent, gridMounted: !!document.querySelector('.ag-root-wrapper'), access: localStorage.getItem('SET_TOKEN'), workspaces: JSON.parse(localStorage.getItem('SET_WORKSPACES') || '[]'), observation: window.__blotterObservation, text: document.body?.innerText.slice(0, 3500) || '' }));
  browserState.access = tokenSummary(browserState.access); browserState.text = safe(browserState.text);
  const item = { label, at: new Date().toISOString(), ...browserState, latestRefresh: lastRefresh };
  record.checkpoints.push(item);
  if (screenshot) { item.screenshot = `${label}.png`; await page.screenshot({ path: path.join(output, item.screenshot), timeout: 10000, mask: [page.locator('[data-testid="Username"] input'), page.locator('[data-testid="password"] input')] }); }
  await save();
  return item;
}
function check(name, condition, evidence) { record.assertions.push({ name, passed: !!condition, evidence }); }
async function until(targetTime) {
  while (Date.now() < targetTime) { await sleep(Math.min(10000, targetTime - Date.now())); await checkpoint('progress-' + Date.now(), false); }
}
try {
  await launchNative();
  await page.goto(new URL('?show_normal_login=Y', target).href);
  assert.ok(process.env.SESSION_E2E_USERNAME && process.env.SESSION_E2E_PASSWORD, 'Private credential environment variables are required.');
  try {
    await page.locator('[data-testid="Username"] input').fill(process.env.SESSION_E2E_USERNAME);
    await page.locator('[data-testid="password"] input').fill(process.env.SESSION_E2E_PASSWORD);
    await page.locator('button[data-testid$="_login"]').click();
  } catch { throw new Error('Private fixture sign-in did not complete.'); }
  await page.locator('[aria-label="workspaces"]').waitFor({ state: 'visible', timeout: 45000 });
  await page.locator('[data-testid$="_Cashflow_Dashboard"]').waitFor({ state: 'visible', timeout: 60000 });
  await sleep(10000);
  const dashboardReady = await checkpoint('dashboard-visited');
  assert.ok(dashboardReady.dashboardMounted, 'Actual Dashboard must be mounted.');
  await page.locator('#workspaces-tab-local-blotter-workspace').click();
  await page.locator('[data-testid$="_Cashflow"]').waitFor({ state: 'visible', timeout: 60000 });
  await page.locator('.ag-root-wrapper').waitFor({ state: 'visible', timeout: 60000 });
  await sleep(10000);
  const selected = await checkpoint('blotter-selected');
  assert.ok(selected.dashboardMounted && selected.dashboardHidden, 'Previously visited Dashboard must remain mounted in a hidden panel.');
  assert.ok(selected.blotterMounted && selected.gridMounted, 'Actual Blotter and grid must mount.');
  assert.equal(selected.workspaces.filter(w => w.containers?.length).length, 2, 'Both seeded workspaces must remain populated.');
  const blank = await context.newPage(); await blank.goto('about:blank'); await blank.bringToFront();
  await page.waitForFunction(() => document.visibilityState === 'hidden', { timeout: 5000 });
  await sleep(1500); await page.bringToFront();
  await page.waitForFunction(() => document.visibilityState === 'visible', { timeout: 5000 });
  await sleep(7000);
  const settled = await checkpoint('prior-tile-settled');
  assert.ok(settled.access?.exp > Date.now() / 1000 + 120, 'Settled access must outlive the real 120-second Dashboard interval.');
  assert.ok(lastRefresh?.exp > settled.access.exp + 10, 'Refresh must remain usable beyond access expiry.');
  if (caseId === 'inspect-prior') {
    record.status = 'INSPECTED';
  } else {
    record.measured = { start: Date.now(), settledAccess: settled.access, refresh: lastRefresh, originalDeadline: settled.access.exp * 1000, observationDeadline: settled.access.exp * 1000 + 5000 };
    record.status = 'RUNNING'; await save();
    await blank.bringToFront(); record.nativeTabActivations.push({ time: Date.now(), target: 'blank', phase: 'dashboard-retained' });
    await page.waitForFunction(() => document.visibilityState === 'hidden', { timeout: 5000 });
    await checkpoint('dashboard-retained-hidden', false);
    await until(record.measured.observationDeadline);
    const retained = await checkpoint('dashboard-retained-result', false);
    const recurringQueries = record.requests.filter(item => item.time > record.measured.start + 100000 && item.time <= retained.now && /Settlement(CashflowDataUltraQueryCount|GroupMessageCount)/.test(item.bodyShape?.query || ''));
    const movedExtensions = record.apiResponses.filter(item => item.time >= record.measured.start && item.time <= retained.now && item.status >= 200 && item.status < 300 && item.url.endsWith('/extend') && item.access?.exp > settled.access.exp);
    const promptDuringFirstPhase = retained.observation?.events.filter(item => item.event === 'timeout_opened' && item.time >= record.measured.start && item.time <= retained.now) || [];
    check('Hidden visited Dashboard remains mounted while Blotter is selected', retained.dashboardMounted && retained.dashboardHidden && retained.blotterMounted, { dashboardMounted: retained.dashboardMounted, dashboardHidden: retained.dashboardHidden, blotterMounted: retained.blotterMounted });
    check('Real Dashboard polling completes beyond its 120-second cadence', recurringQueries.length > 0 && movedExtensions.length > 0, { recurringQueries, movedExtensions });
    check('Access expiry moves beyond its original deadline', retained.access?.exp > settled.access.exp && retained.access?.exp * 1000 > retained.now, { originalAccess: settled.access, currentAccess: retained.access });
    check('No Timeout is recorded before the renewed deadline', promptDuringFirstPhase.length === 0 && !retained.timeoutVisible, { promptDuringFirstPhase, timeoutVisible: retained.timeoutVisible });
    record.priorTilePhase = { completedAt: new Date().toISOString(), status: record.assertions.every(item => item.passed) ? 'PASSED' : 'FAILED', recurringQueryCount: recurringQueries.length, movedExtensionCount: movedExtensions.length, checkpoint: 'dashboard-retained-result' };
    await fs.writeFile(path.join(output, 'dashboard-retained-phase.json'), JSON.stringify({ ...record.priorTilePhase, measured: record.measured, assertions: record.assertions }, null, 2) + '\n');
    await save();
    // Retain volatile phase evidence before activation and removal change the mounted state.
    await page.bringToFront(); record.nativeTabActivations.push({ time: Date.now(), target: 'portal', phase: 'dashboard-removal' });
    await page.waitForFunction(() => document.visibilityState === 'visible', { timeout: 5000 });
    await checkpoint('before-dashboard-removal');
    await page.locator('[data-testid="deleteWorkspace-local-dashboard-workspace"]').click();
    await page.locator('[data-testid$="_Cashflow_Dashboard"]').waitFor({ state: 'detached', timeout: 10000 });
    await sleep(10000);
    const removed = await checkpoint('dashboard-removed-settled');
    assert.ok(!removed.dashboardMounted && removed.blotterMounted && removed.gridMounted, 'Dashboard removal must preserve the actual Blotter grid.');
    assert.equal(removed.workspaces.filter(w => w.containers?.length).length, 1, 'Only Blotter may remain populated.');
    assert.ok(removed.access?.exp > Date.now() / 1000, 'Settled access after removal must remain valid.');
    record.removalMeasured = { start: Date.now(), settledAccess: removed.access, deadline: removed.access.exp * 1000 + 5000 };
    await save();
    await until(record.removalMeasured.deadline);
    const final = await checkpoint('dashboard-removed-result');
    const laterDashboardQueries = record.requests.filter(item => item.time >= record.removalMeasured.start && /Settlement(CashflowDataUltraQueryCount|GroupMessageCount)/.test(item.bodyShape?.query || ''));
    const laterExtensions = record.apiResponses.filter(item => item.time >= record.removalMeasured.start && item.status >= 200 && item.status < 300 && item.url.endsWith('/extend') && item.access?.exp !== removed.access.exp);
    const finalOpened = final.observation?.events.filter(item => item.event === 'timeout_opened' && item.time >= record.removalMeasured.start) || [];
    check('Recurring Dashboard requests stop after removal', laterDashboardQueries.length === 0, { laterDashboardQueries });
    check('Access expiry remains fixed after Dashboard removal', laterExtensions.length === 0 && final.access?.exp === removed.access.exp, { laterExtensions, settledAccess: removed.access, finalAccess: final.access });
    check('Timeout appears after the fixed access deadline', finalOpened.some(item => item.time >= removed.access.exp * 1000) && final.timeoutVisible, { finalOpened, fixedExpiry: removed.access.exp, timeoutVisible: final.timeoutVisible });
    record.removalPhase = { completedAt: new Date().toISOString(), status: record.assertions.slice(-3).every(item => item.passed) ? 'PASSED' : 'FAILED', checkpoint: 'dashboard-removed-result' };
    await fs.writeFile(path.join(output, 'dashboard-removed-phase.json'), JSON.stringify({ ...record.removalPhase, measured: record.removalMeasured, assertions: record.assertions.slice(-3) }, null, 2) + '\n');
    await save();
    record.status = record.assertions.every(item => item.passed) ? 'PASSED' : 'FAILED';
  }
} catch (error) {
  record.status = 'FAILED'; record.error = safe(error);
  if (page) await checkpoint('failed').catch(error => { record.captureError = safe(error); });
} finally {
  record.completedAt = new Date().toISOString();
  // Retain the complete case before cleanup closes the browser or removes its disposable profile.
  await save();
  if (owned?.browser) await owned.browser.close().catch(() => {});
  if (owned?.child.exitCode === null && owned.child.signalCode === null) owned.child.kill('SIGTERM');
  if (owned) { await Promise.race([owned.exited, sleep(2000)]); if (owned.child.exitCode === null && owned.child.signalCode === null) { owned.child.kill('SIGKILL'); await Promise.race([owned.exited, sleep(2000)]); } await fs.rm(owned.profilePath, { recursive: true, force: true }); record.nativeBrowser.status = 'CLOSED'; }
  record.cleanupCompletedAt = new Date().toISOString(); await save();
}
console.log(JSON.stringify({ output, status: record.status, error: record.error }));
process.exitCode = ['PASSED', 'INSPECTED'].includes(record.status) ? 0 : 1;
