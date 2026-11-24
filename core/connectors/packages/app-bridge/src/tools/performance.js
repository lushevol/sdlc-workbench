/**
 * @author Podder, Arunangshu
 * @bankId 2004018
 */

import { z } from 'zod';
import zlib from 'node:zlib';
import { promisify } from 'node:util';
import { writeFile } from 'node:fs/promises';
import { getActiveDriver } from '../driver.js';
import { getCdpConnection, onCdpEvent, waitForCdpEvent, isTracingActive, setTracingActive, pushTraceEvents, drainTraceEvents } from '../cdp.js';
import { formatError } from '../errors.js';

const gzipAsync = promisify(zlib.gzip);

/** How long to wait after (re)load before auto-stopping a trace, mirroring Chrome DevTools' own behavior. */
const AUTO_STOP_DELAY_MS = 5000;
/** Timeout waiting for Tracing.tracingComplete after Tracing.end(). */
const TRACING_COMPLETE_TIMEOUT_MS = 30000;

/**
 * Chrome tracing categories to record, matching Chrome DevTools' own timeline categories (plain
 * category name strings, not proprietary logic — see chrome-devtools-mcp's src/tools/performance.ts).
 */
const TRACE_CATEGORIES = [
  '-*',
  'blink.console',
  'blink.user_timing',
  'devtools.timeline',
  'disabled-by-default-devtools.screenshot',
  'disabled-by-default-devtools.timeline',
  'disabled-by-default-devtools.timeline.invalidationTracking',
  'disabled-by-default-devtools.timeline.frame',
  'disabled-by-default-devtools.timeline.stack',
  'disabled-by-default-v8.cpu_profiler',
  'disabled-by-default-v8.cpu_profiler.hires',
  'latencyInfo',
  'loading',
  'v8.execute',
  'v8'
];

/**
 * Compute naive, self-computed trace stats (event count, duration, top categories). This is NOT
 * the Core Web Vitals/LCP/CLS "Insights" analysis chrome-devtools-mcp's performance_analyze_insight
 * provides — that requires bundling Chrome DevTools' own trace-processing engine, deliberately out
 * of scope here (see /memories/repo/app-bridge-cdp.md).
 * @param {Object[]} events
 * @returns {{eventCount: number, durationMs: number, topCategories: {category: string, count: number}[]}}
 */
function computeTraceStats(events) {
  let minTs = Infinity;
  let maxTs = -Infinity;
  const categoryCounts = {};
  for (const event of events) {
    if (typeof event.ts === 'number') {
      if (event.ts < minTs) minTs = event.ts;
      if (event.ts > maxTs) maxTs = event.ts;
    }
    if (event.cat) {
      categoryCounts[event.cat] = (categoryCounts[event.cat] || 0) + 1;
    }
  }
  const durationMs = events.length > 0 && minTs <= maxTs ? (maxTs - minTs) / 1000 : 0;
  const topCategories = Object.entries(categoryCounts)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10)
    .map(([category, count]) => ({ category, count }));
  return { eventCount: events.length, durationMs, topCategories };
}

/**
 * Stop the active trace, compute basic stats, and optionally save the raw trace JSON to disk.
 * @param {string} [filePath]
 * @returns {Promise<string>} A human-readable summary.
 */
async function stopTracingAndSummarize(filePath) {
  const connection = await getCdpConnection();
  const completePromise = waitForCdpEvent(connection, 'Tracing.tracingComplete', { timeout: TRACING_COMPLETE_TIMEOUT_MS });
  await connection.send('Tracing.end', {});
  await completePromise;

  const events = drainTraceEvents();
  setTracingActive(false);
  const stats = computeTraceStats(events);

  const lines = [
    'The performance trace has been stopped.',
    `Basic stats (raw, no Core Web Vitals/insight analysis): ${JSON.stringify(stats, null, 2)}`
  ];

  if (filePath) {
    const json = JSON.stringify({ traceEvents: events });
    const data = filePath.endsWith('.gz') ? await gzipAsync(Buffer.from(json)) : Buffer.from(json);
    await writeFile(filePath, data);
    lines.push(`The raw trace data was saved to ${filePath}.`);
  }

  return lines.join('\n\n');
}

/**
 * Register performance_start_trace / performance_stop_trace: raw CDP Tracing.start/Tracing.end
 * capture with naive, self-computed stats. Deliberately does NOT provide Core Web Vitals/LCP/CLS
 * "Insights" — see /memories/repo/app-bridge-cdp.md for why.
 * @param {import('@modelcontextprotocol/sdk/server/mcp.js').McpServer} server
 */
export function configurePerformanceTools(server) {
  server.tool(
    'performance_start_trace',
    'Start a raw CDP performance trace recording on the active page. Returns basic stats only ' +
      '(event count, duration, category counts) when stopped — no Core Web Vitals/LCP/CLS insight analysis.',
    {
      reload: z
        .boolean()
        .optional()
        .default(true)
        .describe('Navigate to about:blank, then back to the current URL, around starting the trace to clear prior state.'),
      autoStop: z.boolean().optional().default(true).describe('Automatically stop the trace a few seconds after (re)load.'),
      filePath: z.string().optional().describe('Absolute or relative path to save the raw trace JSON to (.json or .json.gz).')
    },
    async ({ reload, autoStop, filePath }) => {
      const doReload = reload !== false;
      const doAutoStop = autoStop !== false;
      try {
        if (isTracingActive()) {
          return {
            content: [{ type: 'text', text: 'A performance trace is already running. Use performance_stop_trace to stop it.' }]
          };
        }

        const driver = getActiveDriver();
        const connection = await getCdpConnection();
        const currentUrl = await driver.getCurrentUrl();

        if (doReload) {
          await driver.get('about:blank');
        }

        onCdpEvent(connection, 'Tracing.dataCollected', (params) => {
          if (Array.isArray(params?.value)) pushTraceEvents(params.value);
        });
        await connection.send('Tracing.start', { traceConfig: { includedCategories: TRACE_CATEGORIES } });
        setTracingActive(true);

        if (doReload) {
          await driver.get(currentUrl);
        }

        if (doAutoStop) {
          await new Promise((resolve) => setTimeout(resolve, AUTO_STOP_DELAY_MS));
          const summary = await stopTracingAndSummarize(filePath);
          return { content: [{ type: 'text', text: summary }] };
        }

        return { content: [{ type: 'text', text: 'The performance trace is being recorded. Use performance_stop_trace to stop it.' }] };
      } catch (error) {
        setTracingActive(false);
        return { content: [{ type: 'text', text: formatError(error) }], isError: true };
      }
    }
  );

  server.tool(
    'performance_stop_trace',
    'Stop the active raw CDP performance trace recording started by performance_start_trace.',
    { filePath: z.string().optional().describe('Absolute or relative path to save the raw trace JSON to (.json or .json.gz).') },
    async ({ filePath }) => {
      try {
        if (!isTracingActive()) {
          return { content: [{ type: 'text', text: 'No performance trace is currently running.' }] };
        }
        const summary = await stopTracingAndSummarize(filePath);
        return { content: [{ type: 'text', text: summary }] };
      } catch (error) {
        setTracingActive(false);
        return { content: [{ type: 'text', text: formatError(error) }], isError: true };
      }
    }
  );
}
