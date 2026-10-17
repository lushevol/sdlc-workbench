/**
 * @author Podder, Arunangshu
 * @bankId 2004018
 */

import { z } from 'zod';
import { getCdpConnection, ensureNetworkCaptureEnabled } from '../cdp.js';
import { formatError } from '../errors.js';

/** @param {number} kilobitsPerSecond @returns {number} bytes/sec, as required by Network.emulateNetworkConditions. */
function kbps(kilobitsPerSecond) {
  return (kilobitsPerSecond * 1024) / 8;
}

/** @param {number} megabitsPerSecond @returns {number} bytes/sec. */
function mbps(megabitsPerSecond) {
  return (megabitsPerSecond * 1024 * 1024) / 8;
}

/**
 * Approximate Network.emulateNetworkConditions presets, roughly matching Chrome DevTools'
 * built-in throttling profiles. "Online" explicitly disables throttling (downloadThroughput/
 * uploadThroughput: -1 means "no override" per the CDP spec).
 */
const NETWORK_CONDITION_PRESETS = {
  Online: { offline: false, latency: 0, downloadThroughput: -1, uploadThroughput: -1 },
  Offline: { offline: true, latency: 0, downloadThroughput: 0, uploadThroughput: 0 },
  'Slow 3G': { offline: false, latency: 400, downloadThroughput: kbps(500), uploadThroughput: kbps(500) },
  'Fast 3G': { offline: false, latency: 150, downloadThroughput: kbps(1600), uploadThroughput: kbps(750) },
  'Slow 4G': { offline: false, latency: 170, downloadThroughput: mbps(9), uploadThroughput: mbps(1.5) },
  'Fast 4G': { offline: false, latency: 60, downloadThroughput: mbps(20), uploadThroughput: mbps(10) }
};

/**
 * Parse a "<latitude>,<longitude>" geolocation string.
 * @param {string} value
 * @returns {{latitude: number, longitude: number, accuracy: number}}
 */
function parseGeolocation(value) {
  const [latText, longText] = value.split(',').map((part) => part.trim());
  const latitude = Number(latText);
  const longitude = Number(longText);
  const valid = Number.isFinite(latitude) && Number.isFinite(longitude) && latitude >= -90 && latitude <= 90 && longitude >= -180 && longitude <= 180;
  if (!valid) {
    throw new Error(
      `Invalid geolocation "${value}". Expected "<latitude>,<longitude>" with latitude in [-90, 90] and longitude in [-180, 180].`
    );
  }
  return { latitude, longitude, accuracy: 1 };
}

/**
 * Parse a "<width>x<height>x<devicePixelRatio>[,mobile][,touch][,landscape]" viewport string.
 * @param {string} value
 * @returns {{width: number, height: number, deviceScaleFactor: number, mobile: boolean, touch: boolean, landscape: boolean}}
 */
function parseViewport(value) {
  const [dimensions, ...flags] = value.split(',').map((part) => part.trim());
  const [width, height, deviceScaleFactor] = dimensions.split('x').map(Number);
  if (!width || !height) {
    throw new Error(`Invalid viewport "${value}". Expected "<width>x<height>x<devicePixelRatio>[,mobile][,touch][,landscape]".`);
  }
  return {
    width,
    height,
    deviceScaleFactor: deviceScaleFactor || 1,
    mobile: flags.includes('mobile'),
    touch: flags.includes('touch'),
    landscape: flags.includes('landscape')
  };
}

/**
 * Register browser_emulate: consolidated device/network/environment emulation via CDP. Each
 * parameter is applied independently — omit a parameter to leave that setting unchanged; pass its
 * documented "clear" value (see each parameter's description) to reset it to default.
 * @param {import('@modelcontextprotocol/sdk/server/mcp.js').McpServer} server
 */
export function configureEmulationTools(server) {
  server.tool(
    'browser_emulate',
    'Emulate device/network/environment conditions on the active page via Chrome DevTools ' +
      'Protocol. Each parameter is applied independently: omit a parameter to leave that setting ' +
      "unchanged; pass its documented \"clear\" value to reset it to default.",
    {
      colorScheme: z.enum(['dark', 'light', 'auto']).optional().describe('Emulate dark/light mode. "auto" clears the override.'),
      cpuThrottlingRate: z.number().positive().optional().describe('CPU slowdown factor. 1 disables throttling.'),
      networkConditions: z
        .enum(['Online', 'Offline', 'Slow 3G', 'Fast 3G', 'Slow 4G', 'Fast 4G'])
        .optional()
        .describe('Throttle the network to an approximate preset. "Online" disables throttling.'),
      geolocation: z
        .string()
        .optional()
        .describe('"<latitude>,<longitude>" to override geolocation. Pass an empty string to clear the override.'),
      userAgent: z
        .string()
        .optional()
        .describe("User agent to emulate. Pass an empty string to reset to the browser's real user agent."),
      extraHttpHeaders: z
        .string()
        .optional()
        .describe('Extra HTTP headers as a JSON object string, e.g. {"X-Custom":"value"}. Pass an empty string to clear all extra headers.'),
      viewport: z
        .string()
        .optional()
        .describe('"<width>x<height>x<devicePixelRatio>[,mobile][,touch][,landscape]" to emulate a device viewport.')
    },
    async ({ colorScheme, cpuThrottlingRate, networkConditions, geolocation, userAgent, extraHttpHeaders, viewport }) => {
      try {
        const connection = await getCdpConnection();
        const applied = [];

        if (colorScheme !== undefined) {
          const features = colorScheme === 'auto' ? [] : [{ name: 'prefers-color-scheme', value: colorScheme }];
          await connection.send('Emulation.setEmulatedMedia', { features });
          applied.push(`colorScheme=${colorScheme}`);
        }

        if (cpuThrottlingRate !== undefined) {
          await connection.send('Emulation.setCPUThrottlingRate', { rate: cpuThrottlingRate });
          applied.push(`cpuThrottlingRate=${cpuThrottlingRate}`);
        }

        if (networkConditions !== undefined) {
          // Network domain must be enabled for the throttling to take effect; this also starts
          // background network-request capture as a documented side effect.
          await ensureNetworkCaptureEnabled();
          await connection.send('Network.emulateNetworkConditions', NETWORK_CONDITION_PRESETS[networkConditions]);
          applied.push(`networkConditions=${networkConditions}`);
        }

        if (geolocation !== undefined) {
          if (geolocation === '') {
            await connection.send('Emulation.clearGeolocationOverride', {});
            applied.push('geolocation=cleared');
          } else {
            await connection.send('Emulation.setGeolocationOverride', parseGeolocation(geolocation));
            applied.push(`geolocation=${geolocation}`);
          }
        }

        if (userAgent !== undefined) {
          const resolvedUserAgent = userAgent === '' ? (await connection.send('Browser.getVersion', {})).userAgent : userAgent;
          await connection.send('Emulation.setUserAgentOverride', { userAgent: resolvedUserAgent });
          applied.push(userAgent === '' ? 'userAgent=reset to default' : `userAgent=${userAgent}`);
        }

        if (extraHttpHeaders !== undefined) {
          await ensureNetworkCaptureEnabled();
          const headers = extraHttpHeaders === '' ? {} : JSON.parse(extraHttpHeaders);
          await connection.send('Network.setExtraHTTPHeaders', { headers });
          applied.push(extraHttpHeaders === '' ? 'extraHttpHeaders=cleared' : 'extraHttpHeaders=set');
        }

        if (viewport !== undefined) {
          const parsed = parseViewport(viewport);
          await connection.send('Emulation.setDeviceMetricsOverride', {
            width: parsed.width,
            height: parsed.height,
            deviceScaleFactor: parsed.deviceScaleFactor,
            mobile: parsed.mobile,
            screenOrientation: { type: parsed.landscape ? 'landscapePrimary' : 'portraitPrimary', angle: parsed.landscape ? 90 : 0 }
          });
          await connection.send('Emulation.setTouchEmulationEnabled', { enabled: parsed.touch });
          applied.push(`viewport=${viewport}`);
        }

        if (applied.length === 0) {
          return { content: [{ type: 'text', text: 'No emulation parameters were given; nothing changed.' }] };
        }
        return { content: [{ type: 'text', text: `Applied: ${applied.join(', ')}` }] };
      } catch (error) {
        return { content: [{ type: 'text', text: formatError(error) }], isError: true };
      }
    }
  );
}
