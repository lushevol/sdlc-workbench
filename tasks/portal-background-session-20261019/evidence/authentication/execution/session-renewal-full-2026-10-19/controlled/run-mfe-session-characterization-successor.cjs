const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const { stripTypeScriptTypes } = require('node:module');
const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const root = process.argv[2];
const output = process.argv[3];
const bindingPath = process.argv[4];
const binding = JSON.parse(fs.readFileSync(bindingPath, 'utf8'));
const fixtureInputs = JSON.parse(fs.readFileSync(binding.input.path, 'utf8'));
const assertionInventory = JSON.parse(fs.readFileSync(binding.assertion_inventory.path, 'utf8'));
const actualHarnessSha256 = crypto.createHash('sha256').update(fs.readFileSync(__filename)).digest('hex');
assert.equal(actualHarnessSha256, binding.harness.sha256, 'Harness must match original pre-run hash');
const results = [];
const hashes = {};
const initialTime = Date.parse(fixtureInputs.initial_time);
const noop = () => {};
const deferred = () => {
  let resolve, reject;
  const promise = new Promise((accept, decline) => { resolve = accept; reject = decline; });
  return { promise, resolve, reject };
};
async function fixture() {
  let now = initialTime, sequence = 0, active;
  const timers = new Map(), listeners = new Map(), added = [], removed = [], requests = [], reloginQueue = [];
  const state = { store: { token: fixtureInputs.access_token, expiredIn: now / 1000 + fixtureInputs.access_lifetime_seconds, refreshToken: fixtureInputs.refresh_token, isOnLogout: false, workspaces: [], entities: [], drawers: [] }, logout: 0, closes: [], errors: [], analytics: [], decodedTokens: [], refreshExp: now / 1000 + fixtureInputs.refresh_lifetime_seconds };
  class ClockDate extends Date {
    constructor(...args) { super(...(args.length ? args : [now])); }
    static now() { return now; }
  }
  const document = {
    addEventListener(type, fn, options) {
      if (!listeners.has(type)) listeners.set(type, new Set());
      listeners.get(type).add(fn); added.push({ type, fn, options });
    },
    removeEventListener(type, fn, options) {
      listeners.get(type)?.delete(fn); removed.push({ type, fn, options });
    },
    getElementById: () => null,
  };
  const react = {
    useRef(initial) {
      const index = active.index++;
      if (!(index in active.hooks)) active.hooks[index] = { current: initial };
      return active.hooks[index];
    },
    useState(initial) {
      const instance = active, index = instance.index++;
      if (!(index in instance.hooks)) instance.hooks[index] = initial;
      return [instance.hooks[index], value => {
        const next = typeof value === 'function' ? value(instance.hooks[index]) : value;
        if (!Object.is(next, instance.hooks[index])) { instance.hooks[index] = next; instance.dirty = true; }
      }];
    },
    useCallback(fn, deps) {
      const index = active.index++, previous = active.hooks[index];
      if (!previous || deps.some((value, i) => !Object.is(value, previous.deps[i]))) active.hooks[index] = { fn, deps };
      return active.hooks[index].fn;
    },
    useEffect(effect, deps) {
      const instance = active, index = instance.index++, previous = instance.hooks[index];
      if (!previous || !deps || deps.some((value, i) => !Object.is(value, previous.deps[i]))) {
        instance.pending.push(() => {
          previous?.cleanup?.();
          const cleanup = effect();
          instance.hooks[index] = { deps, cleanup };
        });
      }
    },
  };
  function mount(component, props) {
    const instance = { hooks: [], pending: [], dirty: true, index: 0, result: undefined };
    instance.render = () => {
      let attempts = 0;
      do {
        if (++attempts > 20) throw Error('Hook model render loop');
        instance.dirty = false; instance.index = 0; instance.pending = []; active = instance;
        instance.result = component(props);
        instance.pending.forEach(effect => effect());
      } while (instance.dirty);
      return instance.result;
    };
    instance.flush = () => { if (instance.dirty) instance.render(); };
    instance.unmount = () => { instance.hooks.forEach(hook => hook?.cleanup?.()); };
    instance.render(); return instance;
  }
  const context = vm.createContext({
    URLSearchParams, AbortController, Date: ClockDate,
    window: { location: { search: '' } }, document,
    setTimeout(fn, delay) { const id = ++sequence; timers.set(id, { fn, at: now + Math.max(0, Number(delay) || 0) }); return id; },
    clearTimeout(id) { timers.delete(id); },
    console: { error: noop, info: noop, log: noop },
  });
  const network = { post(url, body, config) {
    requests.push({ url, body, config, at: now });
    return url.endsWith('/relogin') ? (reloginQueue.shift() || Promise.resolve({ status: 200 })) : Promise.resolve({ status: 200 });
  } };
  const modules = new Map();
  async function load(relative, values) {
    const absolute = path.join(root, relative), source = fs.readFileSync(absolute, 'utf8');
    hashes[relative] = crypto.createHash('sha256').update(source).digest('hex');
    const module = new vm.SourceTextModule(stripTypeScriptTypes(source, { mode: 'transform' }), { context, identifier: absolute });
    await module.link(async specifier => {
      const value = values[specifier];
      if (!value) throw Error(`Unexpected import ${specifier} in ${relative}`);
      if (value instanceof vm.Module) return value;
      return new vm.SyntheticModule(Object.keys(value), function () {
        Object.entries(value).forEach(([key, item]) => this.setExport(key, item));
      }, { context });
    });
    await module.evaluate(); modules.set(relative, module); return module;
  }
  const hooks = { getHooksBase: () => ({ store: state.store }) };
  const endpoints = await load('src/hooks/service/util/getEndpoint.ts', {});
  const services = await load('src/hooks/service/index.ts', { axios: { AxiosPromise: null, AxiosRequestConfig: null, AxiosResponse: null }, '../HooksBase': hooks, './config': { default: network }, './util/getEndpoint': endpoints });
  const extend = await load('src/hooks/service/util/extend.ts', { '../../HooksBase': hooks, '../config': { default: network }, './getEndpoint': endpoints });
  const dispatcher = { default: () => ({ dispacthLoading: noop, dispacthWorkspaces: noop, dispacthCurrentWorkspace: noop, addWorkspace: noop, dispacthErrorMessage: error => state.errors.push(error), dispacthIsOnLogout: value => { state.store.isOnLogout = value; } }) };
  const analytics = { default: () => ({ ButtonEvent: (...args) => state.analytics.push(args), TileEvent: noop, TabEvent: noop, ModalEvent: (...args) => state.analytics.push(args) }) };
  const provider = { useContext: () => [state.store, noop] };
  const common = { validateWorkspace: value => value, aOrb: (a, b) => a ?? b, getJWTPayload: token => { state.decodedTokens.push(token); return { exp: state.refreshExp }; }, waitFor: () => Promise.resolve() };
  const home = await load('src/pages/Home/common/useController.ts', {
    react: { default: react }, '../../../hooks/provider': provider, '../../../hooks/dispathcer': dispatcher,
    '../../../hooks/model/workspaces': { Workspace: null }, '../../../analytics/model': { AnalyticsData: null },
    '../../../utils/common': common, '../../../hooks/service': services, '../../../hooks/service/util/extend': extend,
    '../../../analytics': analytics, '../../../utils/login': { handleLoginEntities: noop }, './util': { setDetail: noop, refreshTabUtil: noop },
  });
  const timeout = await load('src/components/Timeout/common/useController.ts', {
    react: { default: react }, '../../../hooks/provider': provider, '../../../hooks/dispathcer': dispatcher,
    './interface': { TimeoutProps: null }, '../../../analytics/model': { AnalyticsData: null },
    '../../../utils/common': common, '../../../hooks/service': services, '../../../analytics': analytics,
    '../../../services': { default: () => ({ logout: () => { state.logout++; return Promise.resolve(); } }) },
  });
  function advance(milliseconds, instance) {
    const target = now + milliseconds;
    while (true) {
      const next = [...timers.entries()].filter(([, timer]) => timer.at <= target).sort((a, b) => a[1].at - b[1].at)[0];
      if (!next) break;
      now = next[1].at; timers.delete(next[0]); next[1].fn(); instance?.flush();
    }
    now = target; instance?.flush();
  }
  function activity(type, instance) { [...(listeners.get(type) || [])].forEach(fn => fn({ type })); instance?.flush(); }
  return { state, requests, reloginQueue, added, removed, listeners, timers, advance, activity, mountHome: () => mount(home.namespace.default), mountTimeout: () => mount(timeout.namespace.default, { setOpen: value => state.closes.push(value) }), services: services.namespace, extend: extend.namespace, now: () => now };
}
async function check(name, test) {
  try { const details = await test(); results.push({ name, status: 'PASSED', asserted_predicates: assertionInventory[name], ...details }); }
  catch (error) { results.push({ name, status: 'FAILED', asserted_predicates: assertionInventory[name], error: error.stack }); }
}
(async () => {

  for (const type of fixtureInputs.short_activity.types) {
    await check(`${type} for 15 seconds at 100 ms records eligible extend requests`, async () => {
      const f = await fixture(), home = f.mountHome(), started = f.now();
      assert.ok(f.state.store.token); assert.ok(f.state.store.expiredIn - f.now() / 1000 >= 30);
      let events = 0;
      for (let elapsed = 0; elapsed < fixtureInputs.short_activity.duration_ms; elapsed += fixtureInputs.short_activity.event_interval_ms) {
        f.activity(type, home); events++; f.advance(fixtureInputs.short_activity.event_interval_ms, home);
        assert.equal(home.result.showTimeout, false);
      }
      const requests = f.requests.filter(request => request.url.endsWith('/extend'));
      assert.equal(events, 150); assert.equal(f.now() - started, 15000);
      assert.equal(requests.length, fixtureInputs.short_activity.expected_request_count);
      assert.deepEqual(requests.map(request => request.at - started), [0, 5000, 10000]);
      assert.ok(requests.every(request => request.body.singleUIAuthorization === fixtureInputs.access_token));
      home.unmount();
      return { event_type: type, events, event_interval_ms: 100, duration_ms: 15000, request_count: requests.length, request_offsets_ms: requests.map(request => request.at - started), successful_backend_renewal: 'NOT_ASSESSED' };
    });
  }
  await check('four-hour activity keeps the Home timeout signal absent with mocked expiry updates', async () => {
    const f = await fixture(), home = f.mountHome(), started = f.now();
    const settings = fixtureInputs.four_hour_activity;
    let replacements = 0, timeoutSignals = 0, events = 0, handledRequests = 0;
    for (let elapsed = 0; elapsed < settings.duration_ms; elapsed += settings.event_interval_ms) {
      f.activity('mousemove', home); events++;
      for (const request of f.requests.slice(handledRequests)) {
        assert.ok(request.url.endsWith('/extend'));
        f.state.store = { ...f.state.store, token: `controlled-updated-token-${++replacements}`, expiredIn: f.now() / 1000 + settings.access_lifetime_after_mock_update_seconds };
        home.render();
      }
      handledRequests = f.requests.length;
      if (home.result.showTimeout) timeoutSignals++;
      f.advance(settings.event_interval_ms, home);
      if (home.result.showTimeout) timeoutSignals++;
    }
    const requests = f.requests.filter(request => request.url.endsWith('/extend'));
    assert.equal(events, 14400); assert.equal(f.now() - started, 14400000);
    assert.equal(requests.length, settings.expected_request_count); assert.equal(replacements, requests.length);
    assert.ok(requests.slice(1).every((request, i) => request.at - requests[i].at === 5000));
    assert.equal(timeoutSignals, 0); assert.equal(f.state.logout, 0);
    assert.equal(f.requests.filter(request => request.url.endsWith('/refreshtoken')).length, 0);
    home.unmount();
    return { events, duration_ms: 14400000, event_interval_ms: 1000, request_count: requests.length, mocked_store_replacements: replacements, timeout_signal_count: timeoutSignals, actual_success_handler: 'NOT_EXECUTED', fresh_SSO_prompt_count: 'NOT_ASSESSED', successful_backend_renewal: 'NOT_ASSESSED' };
  });
  await check('continuous activity renews without an idle gap', async () => {
    const f = await fixture(), home = f.mountHome();
    for (let i = 0; i < 1000; i++) { f.activity('mousemove', home); f.advance(1000, home); }
    const renewals = f.requests.filter(request => request.url.endsWith('/extend'));
    assert.equal(renewals.length, 200);
    assert.ok(renewals.slice(1).every((request, i) => request.at - renewals[i].at === 5000));
    home.unmount(); return { events: 1000, elapsed_ms: 1000000, renewal_calls: renewals.length, cadence_ms: 5000 };
  });
  await check('activity types share one cadence and capture registration', async () => {
    const f = await fixture(), home = f.mountHome();
    const types = ['mousemove', 'mousedown', 'keydown', 'scroll'];
    types.forEach(type => f.activity(type, home)); assert.equal(f.requests.length, 1);
    f.advance(4999, home); f.activity('scroll', home); assert.equal(f.requests.length, 1);
    f.advance(1, home); f.activity('keydown', home); assert.equal(f.requests.length, 2);
    types.forEach(type => assert.ok(f.added.some(x => x.type === type && x.options.capture === true && x.options.passive === true)));
    home.unmount(); return { activity_types: types, shared_calls: 2, capture_and_passive: true };
  });
  await check('each activity type can independently renew', async () => {
    for (const type of ['mousemove', 'mousedown', 'keydown', 'scroll']) {
      const f = await fixture(), home = f.mountHome(); f.activity(type, home); assert.equal(f.requests.length, 1); home.unmount();
    }
    return { independent_types: 4 };
  });
  await check('idle periods do not renew', async () => {
    const f = await fixture(), home = f.mountHome(); f.advance(60000, home); assert.equal(f.requests.length, 0);
    f.activity('keydown', home); f.advance(60000, home); assert.equal(f.requests.length, 1); home.unmount();
    return { initial_idle_ms: 60000, after_activity_idle_ms: 60000, renewal_calls: 1 };
  });
  await check('current session, logout, missing token, and near-expiry guards', async () => {
    const f = await fixture(), home = f.mountHome(); f.activity('mousemove', home);
    f.state.store = { ...f.state.store, token: 'replacement', expiredIn: f.state.store.expiredIn + 60 }; home.render();
    f.advance(5000, home); f.activity('scroll', home); assert.equal(f.requests.at(-1).body.singleUIAuthorization, f.state.store.token);
    f.state.store = { ...f.state.store, isOnLogout: true }; home.render(); f.advance(5000, home); f.activity('keydown', home); assert.equal(f.requests.length, 2);
    f.state.store = { ...f.state.store, isOnLogout: false, token: undefined }; home.render(); f.activity('keydown', home); assert.equal(f.requests.length, 2);
    f.state.store = { ...f.state.store, token: 'fixture', expiredIn: f.now() / 1000 + 24 }; home.render(); f.activity('keydown', home);
    assert.equal(f.requests.filter(request => request.url.endsWith('/extend')).length, 2);
    await f.extend.extend(f.now() / 1000 + 25, false, 'fixture');
    assert.equal(f.requests.filter(request => request.url.endsWith('/extend')).length, 3);
    home.unmount(); return { latest_token_used: true, logout_blocks: true, missing_token_blocks: true, below_25s_blocks: true, exactly_25s_allowed: true };
  });
  await check('unmount removes listeners and session timers', async () => {
    const f = await fixture(), home = f.mountHome(); const initial = f.requests.length; home.unmount();
    ['mousemove', 'mousedown', 'keydown', 'scroll'].forEach(type => { assert.equal(f.listeners.get(type).size, 0); assert.ok(f.removed.some(x => x.type === type && x.options.capture)); f.activity(type, home); });
    f.advance(7200000); assert.equal(f.requests.length, initial); assert.equal(f.timers.size, 0);
    return { removed_types: 4, remaining_timers: f.timers.size };
  });
  await check('idle expiry retains refresh request and prompt', async () => {
    const f = await fixture(); f.state.store.expiredIn = f.now() / 1000 + 60; const home = f.mountHome();
    f.advance(34999, home); assert.equal(f.requests.length, 0); f.advance(1, home);
    assert.equal(f.requests.length, 1); assert.ok(f.requests[0].url.endsWith('/refreshtoken')); assert.equal(home.result.showTimeout, false);
    f.advance(25000, home); assert.equal(home.result.showTimeout, true); home.unmount();
    return { refresh_before_expiry_ms: 25000, prompt_at_expiry: true, activity_renewals: 0 };
  });
  await check('actual relogin returns pending promise and preserves successful result', async () => {
    const f = await fixture(), request = deferred(); f.reloginQueue.push(request.promise);
    const actual = f.services.relogin(); assert.equal(actual, request.promise); let settled = false; actual.then(() => { settled = true; }); await Promise.resolve(); assert.equal(settled, false);
    request.resolve({ status: 200 }); assert.deepEqual(await actual, { status: 200 });
    return { returned_request_identity: true, pending_until_resolution: true, success_propagated: true };
  });
  await check('actual relogin propagates rejection and aborts the older request', async () => {
    const f = await fixture(), first = deferred(), second = deferred(); f.reloginQueue.push(first.promise, second.promise);
    const older = f.services.relogin(), signal = f.services.signal.relogin.signal, current = f.services.relogin(); assert.equal(signal.aborted, true);
    const failure = new Error('Controlled renewal rejection'); const caught = assert.rejects(current, error => error === failure); second.reject(failure); await caught;
    first.resolve({ status: 200 }); await older;
    return { request_rejection_propagated: true, older_request_aborted: true };
  });
  await check('Timeout stays open while pending and closes after success', async () => {
    const f = await fixture(), request = deferred(); f.reloginQueue.push(request.promise); const timeout = f.mountTimeout();
    assert.equal(f.state.store.refreshToken, fixtureInputs.refresh_token); assert.deepEqual(f.state.decodedTokens, [fixtureInputs.refresh_token]); assert.equal(f.timers.size, 1);
    const renewal = timeout.result.extend(); timeout.flush(); assert.equal(timeout.result.loading, true); assert.deepEqual(f.state.closes, []);
    await Promise.resolve(); timeout.flush(); assert.deepEqual(f.state.closes, []); assert.equal(f.state.analytics.filter(event => event[0] === 'close').length, 0);
    request.resolve({ status: 200 }); await renewal; timeout.flush(); assert.deepEqual(f.state.closes, [false]); assert.equal(timeout.result.loading, false); assert.equal(f.timers.size, 0);
    timeout.unmount(); return { refresh_token_present: true, refresh_token_validity: 'MOCKED_NOT_VALIDATED', expiry_timer_armed: true, pending_closure_count: 0, successful_closure_count: 1, open_while_pending: true, closed_after_success: true, loading_reset: true };
  });
  await check('Timeout rejection remains retryable and successful retry clears expiry timer', async () => {
    const f = await fixture(); f.state.store.refreshToken = 'fixture'; const timeout = f.mountTimeout();
    const failed = deferred(); f.reloginQueue.push(failed.promise); const renewal = timeout.result.extend(); failed.reject(new Error('Controlled renewal failure')); await renewal; timeout.flush();
    assert.deepEqual(f.state.closes, []); assert.equal(timeout.result.loading, false); assert.equal(f.state.errors.filter(error => error !== undefined).length, 1); assert.equal(f.timers.size, 1);
    const retry = deferred(); f.reloginQueue.push(retry.promise); const retried = timeout.result.extend(); timeout.flush(); assert.equal(timeout.result.loading, true);
    retry.resolve({ status: 200 }); await retried; timeout.flush(); assert.deepEqual(f.state.closes, [false]); assert.equal(timeout.result.loading, false); assert.equal(f.timers.size, 0); assert.equal(f.state.errors.at(-1), undefined);
    f.advance(120000, timeout); await Promise.resolve(); assert.equal(f.state.logout, 0); timeout.unmount();
    return { rejection_keeps_open: true, rejection_resets_loading: true, retry_succeeds: true, successful_retry_clears_timer: true };
  });
  await check('Timeout failure retains refresh expiry logout', async () => {
    const f = await fixture(); f.state.store.refreshToken = 'fixture'; f.state.refreshExp = f.now() / 1000 + 10; const timeout = f.mountTimeout();
    const failed = deferred(); f.reloginQueue.push(failed.promise); const renewal = timeout.result.extend(); failed.reject(new Error('Controlled renewal failure')); await renewal; timeout.flush();
    f.advance(7999, timeout); await Promise.resolve(); assert.equal(f.state.logout, 0);
    f.advance(1, timeout); await Promise.resolve(); await Promise.resolve(); await Promise.resolve(); assert.equal(f.state.logout, 1);
    timeout.unmount(); return { logout_deadline_before_refresh_expiry_ms: 2000, failure_preserves_deadline: true };
  });
})().then(() => { const status = results.some(check => check.status === 'FAILED') ? 'FAILED' : 'PASSED'; finish(status); if (status === 'FAILED') process.exitCode = 1; }).catch(error => { finish('FAILED', error.stack); process.stderr.write(error.stack + '\n'); process.exitCode = 1; });
function finish(status, failure) {
  const result = { status, execution_mode: 'controlled_source_characterization', business_verification: 'NOT_VERIFIED', original_binding: binding, original_binding_sha256: crypto.createHash('sha256').update(fs.readFileSync(bindingPath)).digest('hex'), harness_sha256: actualHarnessSha256, argv: process.argv, runtime: process.version, worktree: root, source_sha256: hashes, checks: results, failure: failure || null, mocks: ['React hooks use a deterministic state, ref, effect, and callback model.', 'Document listeners use a controlled event registry and capture option checks.', 'Date and browser timers use a controlled clock.', 'Axios post returns controlled promises and records request arguments.', 'JWT decoding, analytics, dispatcher side effects, and logout are controlled inputs.', 'waitFor resolves immediately in Timeout characterization.', 'Refresh token presence is controlled; JWT decoding returns configured exp without token validation.', 'Four-hour fixture manually updates access token and expiry after each request; real response handlers do not execute.'], limits: ['Actual changed TypeScript executes after Node stripTypeScriptTypes transformation.', 'The harness is not React, jsdom, browser, backend, identity provider, or E2E execution.', 'The harness does not prove deployed timeout policy or indefinite backend renewal.', 'This execution does not run Jest assertions.', 'Request counts and mocked responses do not prove successful backend renewal.', 'Four-hour no-timeout results depend on mocked response/store updates; fresh SSO navigation is unassessed.'] };
  fs.writeFileSync(output, JSON.stringify(result, null, 2) + '\n');
  process.stdout.write(JSON.stringify({ status, checks: results.length, failures: results.filter(x => x.status === 'FAILED').length, output }) + '\n');
}
