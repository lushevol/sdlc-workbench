import { describe, it, expect, beforeEach, vi } from 'vitest';
import { createMockDriver, createMockCdpConnection } from './helpers/mockDriver.js';

vi.mock('../src/driver.js', () => ({ getActiveDriver: vi.fn() }));

const { getActiveDriver } = await import('../src/driver.js');
const {
  getCdpConnection,
  parseCdpMessage,
  onCdpEvent,
  waitForCdpEvent,
  ensureNetworkCaptureEnabled,
  getNetworkRequests,
  clearNetworkRequests,
  ensureConsoleCaptureEnabled,
  getConsoleMessages,
  clearConsoleMessages,
  isTracingActive,
  setTracingActive,
  pushTraceEvents,
  drainTraceEvents,
  resetCdpState
} = await import('../src/cdp.js');

describe('cdp', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    resetCdpState();
  });

  describe('getCdpConnection', () => {
    it('lazily creates a CDP connection via the active driver', async () => {
      const driver = createMockDriver();
      const connection = createMockCdpConnection();
      driver.createCDPConnection.mockResolvedValue(connection);
      getActiveDriver.mockReturnValue(driver);

      const result = await getCdpConnection();

      expect(driver.createCDPConnection).toHaveBeenCalledWith('page');
      expect(result).toBe(connection);
    });

    it('caches the connection across calls', async () => {
      const driver = createMockDriver();
      getActiveDriver.mockReturnValue(driver);

      await getCdpConnection();
      await getCdpConnection();

      expect(driver.createCDPConnection).toHaveBeenCalledTimes(1);
    });
  });

  describe('parseCdpMessage', () => {
    it('parses a valid JSON object message', () => {
      expect(parseCdpMessage('{"method":"Network.requestWillBeSent","params":{}}')).toEqual({
        method: 'Network.requestWillBeSent',
        params: {}
      });
    });

    it('returns null for malformed/non-JSON input', () => {
      expect(parseCdpMessage('not json')).toBeNull();
    });

    it('returns null for valid JSON that is not a plain object', () => {
      expect(parseCdpMessage('42')).toBeNull();
      expect(parseCdpMessage('null')).toBeNull();
    });
  });

  describe('onCdpEvent', () => {
    it('invokes the callback only for matching methods, ignoring other methods and malformed messages', () => {
      const connection = createMockCdpConnection();
      const callback = vi.fn();
      onCdpEvent(connection, 'Network.requestWillBeSent', callback);

      connection.__emit('not json');
      connection.__emit({ method: 'Network.responseReceived', params: { requestId: '1' } });
      connection.__emit({ method: 'Network.requestWillBeSent', params: { requestId: '2' } });

      expect(callback).toHaveBeenCalledTimes(1);
      expect(callback).toHaveBeenCalledWith({ requestId: '2' });
    });
  });

  describe('waitForCdpEvent', () => {
    it('resolves with the params of the matching event', async () => {
      const connection = createMockCdpConnection();
      const promise = waitForCdpEvent(connection, 'Tracing.tracingComplete', { timeout: 1000 });

      connection.__emit({ method: 'Tracing.dataCollected', params: { value: [] } });
      connection.__emit({ method: 'Tracing.tracingComplete', params: { dataLossOccurred: false } });

      await expect(promise).resolves.toEqual({ dataLossOccurred: false });
    });

    it('applies an optional predicate filter', async () => {
      const connection = createMockCdpConnection();
      const promise = waitForCdpEvent(connection, 'Network.responseReceived', {
        timeout: 1000,
        predicate: (params) => params.requestId === '2'
      });

      connection.__emit({ method: 'Network.responseReceived', params: { requestId: '1' } });
      connection.__emit({ method: 'Network.responseReceived', params: { requestId: '2' } });

      await expect(promise).resolves.toEqual({ requestId: '2' });
    });

    it('rejects with a timeout error if the event never arrives', async () => {
      vi.useFakeTimers();
      try {
        const connection = createMockCdpConnection();
        const promise = waitForCdpEvent(connection, 'Tracing.tracingComplete', { timeout: 5000 });
        const assertion = expect(promise).rejects.toThrow(/Timed out after 5000ms/);
        await vi.advanceTimersByTimeAsync(5000);
        await assertion;
      } finally {
        vi.useRealTimers();
      }
    });
  });

  describe('network capture', () => {
    it('enables the Network domain and accumulates a request/response lifecycle', async () => {
      const driver = createMockDriver();
      const connection = createMockCdpConnection();
      driver.createCDPConnection.mockResolvedValue(connection);
      getActiveDriver.mockReturnValue(driver);

      await ensureNetworkCaptureEnabled();

      expect(connection.send).toHaveBeenCalledWith('Network.enable', {});

      connection.__emit({
        method: 'Network.requestWillBeSent',
        params: { requestId: 'r1', request: { url: 'https://example.com', method: 'GET', headers: {} }, type: 'Document', timestamp: 1 }
      });
      connection.__emit({
        method: 'Network.responseReceived',
        params: { requestId: 'r1', response: { status: 200, statusText: 'OK', headers: {}, mimeType: 'text/html' } }
      });
      connection.__emit({ method: 'Network.loadingFinished', params: { requestId: 'r1', encodedDataLength: 123 } });

      const requests = getNetworkRequests();
      expect(requests).toHaveLength(1);
      expect(requests[0]).toMatchObject({
        reqid: 1,
        url: 'https://example.com',
        status: 200,
        mimeType: 'text/html',
        encodedDataLength: 123,
        failed: false
      });
    });

    it('marks a request as failed on Network.loadingFailed', async () => {
      const driver = createMockDriver();
      const connection = createMockCdpConnection();
      driver.createCDPConnection.mockResolvedValue(connection);
      getActiveDriver.mockReturnValue(driver);

      await ensureNetworkCaptureEnabled();

      connection.__emit({
        method: 'Network.requestWillBeSent',
        params: { requestId: 'r1', request: { url: 'https://example.com', method: 'GET', headers: {} }, type: 'Document', timestamp: 1 }
      });
      connection.__emit({ method: 'Network.loadingFailed', params: { requestId: 'r1', errorText: 'net::ERR_FAILED' } });

      expect(getNetworkRequests()[0]).toMatchObject({ failed: true, errorText: 'net::ERR_FAILED' });
    });

    it('ignores response/finished/failed events for unknown requestIds', async () => {
      const driver = createMockDriver();
      const connection = createMockCdpConnection();
      driver.createCDPConnection.mockResolvedValue(connection);
      getActiveDriver.mockReturnValue(driver);

      await ensureNetworkCaptureEnabled();

      connection.__emit({ method: 'Network.responseReceived', params: { requestId: 'unknown', response: {} } });
      connection.__emit({ method: 'Network.loadingFinished', params: { requestId: 'unknown', encodedDataLength: 1 } });
      connection.__emit({ method: 'Network.loadingFailed', params: { requestId: 'unknown', errorText: 'x' } });

      expect(getNetworkRequests()).toHaveLength(0);
    });

    it('is idempotent — calling twice only enables the domain once', async () => {
      const driver = createMockDriver();
      const connection = createMockCdpConnection();
      driver.createCDPConnection.mockResolvedValue(connection);
      getActiveDriver.mockReturnValue(driver);

      await ensureNetworkCaptureEnabled();
      await ensureNetworkCaptureEnabled();

      expect(connection.send).toHaveBeenCalledTimes(1);
    });

    it('clearNetworkRequests empties the buffer without resetting the reqid counter', async () => {
      const driver = createMockDriver();
      const connection = createMockCdpConnection();
      driver.createCDPConnection.mockResolvedValue(connection);
      getActiveDriver.mockReturnValue(driver);
      await ensureNetworkCaptureEnabled();
      connection.__emit({
        method: 'Network.requestWillBeSent',
        params: { requestId: 'r1', request: { url: 'https://example.com', method: 'GET' }, type: 'Document', timestamp: 1 }
      });

      clearNetworkRequests();
      connection.__emit({
        method: 'Network.requestWillBeSent',
        params: { requestId: 'r2', request: { url: 'https://example.com/2', method: 'GET' }, type: 'Document', timestamp: 2 }
      });

      const requests = getNetworkRequests();
      expect(requests).toHaveLength(1);
      expect(requests[0].reqid).toBe(2);
    });
  });

  describe('console capture', () => {
    it('enables Runtime/Log domains and accumulates console-api and log entries', async () => {
      const driver = createMockDriver();
      const connection = createMockCdpConnection();
      driver.createCDPConnection.mockResolvedValue(connection);
      getActiveDriver.mockReturnValue(driver);

      await ensureConsoleCaptureEnabled();

      expect(connection.send).toHaveBeenCalledWith('Runtime.enable', {});
      expect(connection.send).toHaveBeenCalledWith('Log.enable', {});

      connection.__emit({
        method: 'Runtime.consoleAPICalled',
        params: {
          type: 'log',
          timestamp: 1,
          args: [{ type: 'string', value: 'hello' }, { type: 'object', description: 'Object' }, { type: 'undefined' }]
        }
      });
      connection.__emit({
        method: 'Log.entryAdded',
        params: { entry: { level: 'error', text: 'boom', timestamp: 2, url: 'https://example.com', lineNumber: 10 } }
      });

      const messages = getConsoleMessages();
      expect(messages).toHaveLength(2);
      expect(messages[0]).toMatchObject({ msgid: 1, source: 'console-api', type: 'log', text: 'hello Object undefined' });
      expect(messages[1]).toMatchObject({ msgid: 2, source: 'log', type: 'error', text: 'boom' });
    });

    it('is idempotent — calling twice only enables the domains once', async () => {
      const driver = createMockDriver();
      const connection = createMockCdpConnection();
      driver.createCDPConnection.mockResolvedValue(connection);
      getActiveDriver.mockReturnValue(driver);

      await ensureConsoleCaptureEnabled();
      await ensureConsoleCaptureEnabled();

      expect(connection.send).toHaveBeenCalledTimes(2);
    });

    it('clearConsoleMessages empties the buffer without resetting the msgid counter', async () => {
      const driver = createMockDriver();
      const connection = createMockCdpConnection();
      driver.createCDPConnection.mockResolvedValue(connection);
      getActiveDriver.mockReturnValue(driver);
      await ensureConsoleCaptureEnabled();
      connection.__emit({ method: 'Runtime.consoleAPICalled', params: { type: 'log', timestamp: 1, args: [] } });

      clearConsoleMessages();
      connection.__emit({ method: 'Runtime.consoleAPICalled', params: { type: 'log', timestamp: 2, args: [] } });

      const messages = getConsoleMessages();
      expect(messages).toHaveLength(1);
      expect(messages[0].msgid).toBe(2);
    });
  });

  describe('tracing state', () => {
    it('tracks active/inactive via isTracingActive/setTracingActive', () => {
      expect(isTracingActive()).toBe(false);
      setTracingActive(true);
      expect(isTracingActive()).toBe(true);
      setTracingActive(false);
      expect(isTracingActive()).toBe(false);
    });

    it('accumulates and drains trace events', () => {
      pushTraceEvents([{ name: 'a' }]);
      pushTraceEvents([{ name: 'b' }, { name: 'c' }]);

      const events = drainTraceEvents();

      expect(events).toEqual([{ name: 'a' }, { name: 'b' }, { name: 'c' }]);
      expect(drainTraceEvents()).toEqual([]);
    });
  });

  describe('resetCdpState', () => {
    it('clears the connection singleton and all capture buffers/counters', async () => {
      const driver = createMockDriver();
      const connection = createMockCdpConnection();
      driver.createCDPConnection.mockResolvedValue(connection);
      getActiveDriver.mockReturnValue(driver);

      await ensureNetworkCaptureEnabled();
      connection.__emit({
        method: 'Network.requestWillBeSent',
        params: { requestId: 'r1', request: { url: 'https://example.com', method: 'GET' }, type: 'Document', timestamp: 1 }
      });
      setTracingActive(true);
      pushTraceEvents([{ name: 'a' }]);

      resetCdpState();

      expect(getNetworkRequests()).toHaveLength(0);
      expect(getConsoleMessages()).toHaveLength(0);
      expect(isTracingActive()).toBe(false);
      expect(drainTraceEvents()).toEqual([]);

      await getCdpConnection();
      expect(driver.createCDPConnection).toHaveBeenCalledTimes(2);
    });
  });
});
