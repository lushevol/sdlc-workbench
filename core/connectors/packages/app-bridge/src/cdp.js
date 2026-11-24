/**
 * @author Podder, Arunangshu
 * @bankId 2004018
 */

import { getActiveDriver } from './driver.js';

/** Active CDP connection singleton for the current browser session. null until first use. */
let _cdpConnection = null;

/** Network-request capture buffer. Single running buffer since session start (see decisions in
 * docs/guide/APP_BRIDGE_TOOLS_GUIDE.md) — not reset per navigation; use network_clear_requests. */
let _networkRequests = [];
/** Map from CDP requestId -> index in _networkRequests, for O(1) updates from later events. */
let _cdpRequestIdToIndex = new Map();
let _nextReqId = 1;
let _networkCaptureEnabled = false;

/** Console-message capture buffer. Same single-running-buffer semantics as network requests. */
let _consoleMessages = [];
let _nextMsgId = 1;
let _consoleCaptureEnabled = false;

/** Raw performance-trace state, shared by performance_start_trace/performance_stop_trace. Lives
 * here (rather than in tools/performance.js) so driver.js only ever depends on this one shared
 * module for CDP-related session teardown, keeping the existing tools -> driver.js dependency
 * direction intact. */
let _tracingActive = false;
let _traceEvents = [];

/**
 * Get (creating if necessary) the CDP connection for the active driver session. Lazily
 * established on first use by any network/console/emulation/performance tool — browser_start
 * does not eagerly open a CDP connection.
 * @returns {Promise<Object>} A selenium-webdriver CdpConnection.
 */
export async function getCdpConnection() {
  if (!_cdpConnection) {
    const driver = getActiveDriver();
    _cdpConnection = await driver.createCDPConnection('page');
  }
  return _cdpConnection;
}

/**
 * Parse a raw CDP websocket message string into its JSON payload, returning null for anything
 * malformed, non-JSON, or not a plain object. This is the single place malformed-message handling
 * is implemented (and unit tested) — callers never need their own try/catch for this.
 * @param {string} raw
 * @returns {{method?: string, params?: Object}|null}
 */
export function parseCdpMessage(raw) {
  try {
    const parsed = JSON.parse(raw);
    return parsed && typeof parsed === 'object' ? parsed : null;
  } catch {
    return null;
  }
}

/**
 * Subscribe to a specific CDP push event (fire-and-forget, no waiting/timeout). Reaches into the
 * connection's underlying WebSocket (`_wsConnection`) the same way selenium-webdriver's own
 * driver.onLogEvent()/onIntercept() helpers do internally — there is no public `.on()` on the
 * CdpConnection object itself for unsolicited events.
 * @param {Object} connection
 * @param {string} methodName e.g. 'Network.requestWillBeSent'
 * @param {(params: Object) => void} callback
 */
export function onCdpEvent(connection, methodName, callback) {
  connection._wsConnection.on('message', (raw) => {
    const message = parseCdpMessage(raw);
    if (message && message.method === methodName) {
      callback(message.params);
    }
  });
}

/**
 * Wait for a specific CDP event to arrive, resolving with its params, or reject if it doesn't
 * arrive within `timeout` ms. This is the single place the "event never arrives" branch is
 * implemented and unit tested — consumers (only performance_stop_trace today) don't need to
 * reimplement or re-test timeout handling themselves.
 * @param {Object} connection
 * @param {string} methodName
 * @param {Object} [options]
 * @param {number} [options.timeout=30000]
 * @param {(params: Object) => boolean} [options.predicate] Optional extra filter on top of methodName.
 * @returns {Promise<Object>} The event's params.
 */
export function waitForCdpEvent(connection, methodName, { timeout = 30000, predicate } = {}) {
  return new Promise((resolve, reject) => {
    let settled = false;

    const listener = (raw) => {
      if (settled) return;
      const message = parseCdpMessage(raw);
      if (!message || message.method !== methodName) return;
      if (predicate && !predicate(message.params)) return;
      settled = true;
      clearTimeout(timer);
      connection._wsConnection.off('message', listener);
      resolve(message.params);
    };

    const timer = setTimeout(() => {
      if (settled) return;
      settled = true;
      connection._wsConnection.off('message', listener);
      reject(new Error(`Timed out after ${timeout}ms waiting for CDP event "${methodName}".`));
    }, timeout);

    connection._wsConnection.on('message', listener);
  });
}

/**
 * @param {string} cdpRequestId
 * @returns {Object|undefined}
 */
function findNetworkEntry(cdpRequestId) {
  const index = _cdpRequestIdToIndex.get(cdpRequestId);
  return index === undefined ? undefined : _networkRequests[index];
}

/**
 * Ensure network-request capture is active for the current session (idempotent — safe to call
 * from multiple tools/multiple times). Enables the CDP Network domain and registers listeners
 * that accumulate requests into an in-memory buffer with our own sequential `reqid`.
 * @returns {Promise<void>}
 */
export async function ensureNetworkCaptureEnabled() {
  if (_networkCaptureEnabled) return;
  const connection = await getCdpConnection();
  await connection.send('Network.enable', {});

  onCdpEvent(connection, 'Network.requestWillBeSent', (params) => {
    const entry = {
      reqid: _nextReqId++,
      cdpRequestId: params.requestId,
      url: params.request?.url,
      method: params.request?.method,
      resourceType: params.type,
      requestHeaders: params.request?.headers,
      timestamp: params.timestamp,
      status: undefined,
      statusText: undefined,
      responseHeaders: undefined,
      mimeType: undefined,
      encodedDataLength: undefined,
      failed: false,
      errorText: undefined
    };
    _cdpRequestIdToIndex.set(params.requestId, _networkRequests.length);
    _networkRequests.push(entry);
  });

  onCdpEvent(connection, 'Network.responseReceived', (params) => {
    const entry = findNetworkEntry(params.requestId);
    if (!entry) return;
    entry.status = params.response?.status;
    entry.statusText = params.response?.statusText;
    entry.responseHeaders = params.response?.headers;
    entry.mimeType = params.response?.mimeType;
  });

  onCdpEvent(connection, 'Network.loadingFinished', (params) => {
    const entry = findNetworkEntry(params.requestId);
    if (!entry) return;
    entry.encodedDataLength = params.encodedDataLength;
  });

  onCdpEvent(connection, 'Network.loadingFailed', (params) => {
    const entry = findNetworkEntry(params.requestId);
    if (!entry) return;
    entry.failed = true;
    entry.errorText = params.errorText;
  });

  _networkCaptureEnabled = true;
}

/** @returns {Object[]} The captured network requests buffer (single running buffer). */
export function getNetworkRequests() {
  return _networkRequests;
}

/** Manually empty the captured-requests buffer. Does not reset the reqid counter. */
export function clearNetworkRequests() {
  _networkRequests = [];
  _cdpRequestIdToIndex = new Map();
}

/**
 * Best-effort stringification of a CDP Runtime.RemoteObject console argument.
 * @param {Object} arg
 * @returns {string}
 */
function stringifyRemoteObject(arg) {
  if (arg.value !== undefined) return typeof arg.value === 'string' ? arg.value : JSON.stringify(arg.value);
  if (arg.description !== undefined) return arg.description;
  return String(arg.type);
}

/**
 * Ensure console-message capture is active for the current session (idempotent). Enables the CDP
 * Runtime and Log domains and registers listeners that accumulate messages into an in-memory
 * buffer with our own sequential `msgid`.
 * @returns {Promise<void>}
 */
export async function ensureConsoleCaptureEnabled() {
  if (_consoleCaptureEnabled) return;
  const connection = await getCdpConnection();
  await connection.send('Runtime.enable', {});
  await connection.send('Log.enable', {});

  onCdpEvent(connection, 'Runtime.consoleAPICalled', (params) => {
    _consoleMessages.push({
      msgid: _nextMsgId++,
      source: 'console-api',
      type: params.type,
      text: (params.args || []).map(stringifyRemoteObject).join(' '),
      timestamp: params.timestamp,
      stackTrace: params.stackTrace
    });
  });

  onCdpEvent(connection, 'Log.entryAdded', (params) => {
    const entry = params.entry || {};
    _consoleMessages.push({
      msgid: _nextMsgId++,
      source: 'log',
      type: entry.level,
      text: entry.text,
      timestamp: entry.timestamp,
      url: entry.url,
      lineNumber: entry.lineNumber
    });
  });

  _consoleCaptureEnabled = true;
}

/** @returns {Object[]} The captured console messages buffer (single running buffer). */
export function getConsoleMessages() {
  return _consoleMessages;
}

/** Manually empty the captured-messages buffer. Does not reset the msgid counter. */
export function clearConsoleMessages() {
  _consoleMessages = [];
}

/** @returns {boolean} Whether a performance trace is currently being recorded. */
export function isTracingActive() {
  return _tracingActive;
}

/** @param {boolean} active */
export function setTracingActive(active) {
  _tracingActive = active;
}

/** @param {Object[]} events Raw CDP trace events (e.g. from a Tracing.dataCollected chunk). */
export function pushTraceEvents(events) {
  _traceEvents.push(...events);
}

/** @returns {Object[]} The accumulated raw trace events, clearing the internal buffer. */
export function drainTraceEvents() {
  const events = _traceEvents;
  _traceEvents = [];
  return events;
}

/**
 * Tear down all CDP state. Called from driver.js's clearActiveDriver() so a new browser_start
 * always begins with a fresh CDP connection and empty capture buffers/counters — mirrors the
 * existing singleton-replacement philosophy already used for _activeDriver. Also usable as a
 * test-reset helper.
 */
export function resetCdpState() {
  _cdpConnection = null;
  _networkRequests = [];
  _cdpRequestIdToIndex = new Map();
  _nextReqId = 1;
  _networkCaptureEnabled = false;
  _consoleMessages = [];
  _nextMsgId = 1;
  _consoleCaptureEnabled = false;
  _tracingActive = false;
  _traceEvents = [];
}
