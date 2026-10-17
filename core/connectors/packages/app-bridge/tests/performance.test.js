import { describe, it, expect, beforeEach, vi } from 'vitest';
import zlib from 'node:zlib';
import { createMockServer, isValidToolResponse } from '@sc-node-mcp/shared-tests/helpers/mockServer';
import { createMockDriver } from './helpers/mockDriver.js';

vi.mock('../src/driver.js', () => ({ getActiveDriver: vi.fn() }));
vi.mock('node:fs/promises', () => ({ writeFile: vi.fn().mockResolvedValue(undefined) }));

vi.mock('../src/cdp.js', () => {
  let tracingActive = false;
  let events = [];
  return {
    getCdpConnection: vi.fn(),
    onCdpEvent: vi.fn(),
    waitForCdpEvent: vi.fn().mockResolvedValue({}),
    isTracingActive: vi.fn(() => tracingActive),
    setTracingActive: vi.fn((active) => {
      tracingActive = active;
    }),
    pushTraceEvents: vi.fn((newEvents) => {
      events.push(...newEvents);
    }),
    drainTraceEvents: vi.fn(() => {
      const drained = events;
      events = [];
      return drained;
    })
  };
});

const { getActiveDriver } = await import('../src/driver.js');
const { writeFile } = await import('node:fs/promises');
const {
  getCdpConnection,
  onCdpEvent,
  waitForCdpEvent,
  isTracingActive,
  setTracingActive,
  drainTraceEvents
} = await import('../src/cdp.js');
const { configurePerformanceTools } = await import('../src/tools/performance.js');

describe('performance tools', () => {
  let server;
  let connection;

  beforeEach(() => {
    vi.clearAllMocks();
    setTracingActive(false);
    drainTraceEvents();
    connection = { send: vi.fn().mockResolvedValue({}) };
    getCdpConnection.mockResolvedValue(connection);
    waitForCdpEvent.mockResolvedValue({});
    server = createMockServer();
    configurePerformanceTools(server);
  });

  describe('performance_start_trace', () => {
    it('starts a trace with reload, without auto-stopping', async () => {
      const driver = createMockDriver({ getCurrentUrl: vi.fn().mockResolvedValue('https://example.com') });
      getActiveDriver.mockReturnValue(driver);

      const response = await server.invokeTool('performance_start_trace', { reload: true, autoStop: false });

      expect(driver.get).toHaveBeenNthCalledWith(1, 'about:blank');
      expect(driver.get).toHaveBeenNthCalledWith(2, 'https://example.com');
      expect(connection.send).toHaveBeenCalledWith('Tracing.start', expect.objectContaining({ traceConfig: expect.any(Object) }));
      expect(isTracingActive()).toBe(true);
      expect(response.content[0].text).toContain('is being recorded');
      expect(isValidToolResponse(response)).toBe(true);
    });

    it('does not reload when reload is false', async () => {
      const driver = createMockDriver();
      getActiveDriver.mockReturnValue(driver);

      await server.invokeTool('performance_start_trace', { reload: false, autoStop: false });

      expect(driver.get).not.toHaveBeenCalled();
    });

    it('reports already-running without starting a new trace', async () => {
      setTracingActive(true);
      const driver = createMockDriver();
      getActiveDriver.mockReturnValue(driver);

      const response = await server.invokeTool('performance_start_trace', {});

      expect(connection.send).not.toHaveBeenCalled();
      expect(response.content[0].text).toContain('already running');
    });

    it('auto-stops after the delay and returns the stopped summary', async () => {
      vi.useFakeTimers();
      try {
        const driver = createMockDriver();
        getActiveDriver.mockReturnValue(driver);

        const promise = server.invokeTool('performance_start_trace', { reload: false, autoStop: true });
        await vi.advanceTimersByTimeAsync(5000);
        const response = await promise;

        expect(connection.send).toHaveBeenCalledWith('Tracing.end', {});
        expect(response.content[0].text).toContain('The performance trace has been stopped.');
        expect(isTracingActive()).toBe(false);
      } finally {
        vi.useRealTimers();
      }
    });

    it('resets tracing state and returns an error if a setup step throws', async () => {
      const driver = createMockDriver({ getCurrentUrl: vi.fn().mockRejectedValue(new Error('boom')) });
      getActiveDriver.mockReturnValue(driver);

      const response = await server.invokeTool('performance_start_trace', {});

      expect(response.isError).toBe(true);
      expect(isTracingActive()).toBe(false);
    });
  });

  describe('performance_stop_trace', () => {
    it('reports nothing running when no trace is active', async () => {
      const response = await server.invokeTool('performance_stop_trace', {});

      expect(connection.send).not.toHaveBeenCalled();
      expect(response.content[0].text).toContain('No performance trace is currently running.');
    });

    it('stops the trace, computes basic stats, and clears tracing state', async () => {
      const driver = createMockDriver();
      getActiveDriver.mockReturnValue(driver);
      const captureCallback = vi.fn();
      onCdpEvent.mockImplementation((_conn, _method, cb) => {
        captureCallback.mockImplementation(cb);
      });
      await server.invokeTool('performance_start_trace', { reload: false, autoStop: false });
      captureCallback({ value: [{ ts: 1000, cat: 'devtools.timeline' }, { ts: 2000, cat: 'v8' }] });

      const response = await server.invokeTool('performance_stop_trace', {});

      expect(connection.send).toHaveBeenCalledWith('Tracing.end', {});
      expect(waitForCdpEvent).toHaveBeenCalledWith(connection, 'Tracing.tracingComplete', expect.any(Object));
      expect(response.content[0].text).toContain('eventCount');
      expect(response.content[0].text).toContain('"eventCount": 2');
      expect(isTracingActive()).toBe(false);
    });

    it('saves plain JSON when filePath does not end in .gz', async () => {
      setTracingActive(true);

      const response = await server.invokeTool('performance_stop_trace', { filePath: 'trace.json' });

      expect(writeFile).toHaveBeenCalledWith('trace.json', Buffer.from(JSON.stringify({ traceEvents: [] })));
      expect(response.content[0].text).toContain('saved to trace.json');
    });

    it('saves gzip-compressed data when filePath ends in .gz', async () => {
      setTracingActive(true);

      await server.invokeTool('performance_stop_trace', { filePath: 'trace.json.gz' });

      expect(writeFile).toHaveBeenCalledWith('trace.json.gz', expect.any(Buffer));
      const [, savedBuffer] = writeFile.mock.calls[0];
      const decompressed = zlib.gunzipSync(savedBuffer).toString();
      expect(JSON.parse(decompressed)).toEqual({ traceEvents: [] });
    });

    it('resets tracing state and returns an error if stopping fails', async () => {
      setTracingActive(true);
      waitForCdpEvent.mockRejectedValue(new Error('Timed out after 30000ms'));

      const response = await server.invokeTool('performance_stop_trace', {});

      expect(response.isError).toBe(true);
      expect(isTracingActive()).toBe(false);
    });
  });
});
