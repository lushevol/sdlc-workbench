(function () {
  'use strict';
  if (window.__SESSION_EVIDENCE__) return;
  const key = '__PORTAL_SESSION_EVIDENCE_20261019__';
  const schema = 'portal-session-sparse-observer-v1';
  const navigationId = String(Date.now()) + '-' + Math.random().toString(16).slice(2);
  let prior;
  try { prior = JSON.parse(localStorage.getItem(key) || 'null'); } catch (_) {}
  const data = prior && prior.schema === schema && Array.isArray(prior.events)
    ? prior : { schema, createdAt: new Date().toISOString(), events: [] };
  const claims = function (token) {
    if (typeof token !== 'string') return null;
    try {
      const encoded = token.trim().split(/\s+/).pop().split('.')[1];
      const payload = JSON.parse(atob(encoded.replace(/-/g, '+').replace(/_/g, '/')));
      const result = {};
      for (const name of ['iat', 'exp', 'auth_time', 'max_age']) {
        if (typeof payload[name] === 'number') result[name] = payload[name];
      }
      return result;
    } catch (_) { return { decodeFailed: true }; }
  };
  const snapshot = function (store) {
    return {
      tokenPresent: !!(store && store.token),
      refreshPresent: !!(store && store.refreshToken),
      access: claims(store && store.token),
      refresh: claims(store && store.refreshToken),
      expiredIn: typeof (store && store.expiredIn) === 'number' ? store.expiredIn : null,
      isOnLogout: !!(store && store.isOnLogout),
    };
  };
  const record = function (event, details) {
    try {
      data.events.push({
        sequence: data.events.length + 1, navigationId, event,
        timestamp: new Date().toISOString(), wallTimeMs: Date.now(),
        performanceTimeMs: performance.now(), visibility: document.visibilityState,
        details: details || {},
      });
      // Preserve sparse evidence through an automatic logout or navigation.
      localStorage.setItem(key, JSON.stringify(data));
    } catch (_) {}
  };
  const api = {
    schema, key, data, record, claims, snapshot,
    transition: function (action, before, after) {
      if (['SET_TOKEN', 'SET_REFRESH_TOKEN', 'SET_EXPIRED_TOKEN', 'CLEAR', 'SET_IS_ON_LOGOUT'].includes(action)) {
        record('state_transition', { action, before: snapshot(before), after: snapshot(after) });
      }
    },
    exportJSON: function () { return JSON.stringify(data, null, 2); },
    download: function () {
      const blob = new Blob([api.exportJSON()], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const anchor = document.createElement('a');
      anchor.href = url;
      anchor.download = 'portal-session-evidence-' + Date.now() + '.json';
      anchor.click();
      URL.revokeObjectURL(url);
    },
  };
  window.__SESSION_EVIDENCE__ = api;
  for (const event of ['visibilitychange', 'freeze', 'resume']) {
    document.addEventListener(event, function () { record('lifecycle_' + event); });
  }
  for (const event of ['pageshow', 'pagehide']) {
    window.addEventListener(event, function (value) {
      record('lifecycle_' + event, { persisted: !!value.persisted });
    });
  }
  record('observer_initialized', {
    wasDiscarded: !!document.wasDiscarded,
    timeOrigin: performance.timeOrigin,
    timersWrapped: false, periodicTasksAdded: false, networkRequestsAdded: false,
  });
}());
