import { describe, it, expect, beforeEach, vi } from 'vitest';
import { createMockServer, isValidToolResponse } from '@sc-node-mcp/shared-tests/helpers/mockServer';

vi.mock('../src/cdp.js', () => ({
  getCdpConnection: vi.fn(),
  ensureNetworkCaptureEnabled: vi.fn().mockResolvedValue(undefined)
}));

const { getCdpConnection, ensureNetworkCaptureEnabled } = await import('../src/cdp.js');
const { configureEmulationTools } = await import('../src/tools/emulation.js');

describe('emulation tools', () => {
  let server;
  let connection;

  beforeEach(() => {
    vi.clearAllMocks();
    connection = { send: vi.fn().mockResolvedValue({}) };
    getCdpConnection.mockResolvedValue(connection);
    ensureNetworkCaptureEnabled.mockResolvedValue(undefined);
    server = createMockServer();
    configureEmulationTools(server);
  });

  it('does nothing and reports so when no parameters are given', async () => {
    const response = await server.invokeTool('browser_emulate', {});

    expect(connection.send).not.toHaveBeenCalled();
    expect(response.content[0].text).toContain('No emulation parameters were given');
    expect(isValidToolResponse(response)).toBe(true);
  });

  it('sets colorScheme and clears it via "auto"', async () => {
    await server.invokeTool('browser_emulate', { colorScheme: 'dark' });
    expect(connection.send).toHaveBeenCalledWith('Emulation.setEmulatedMedia', {
      features: [{ name: 'prefers-color-scheme', value: 'dark' }]
    });

    await server.invokeTool('browser_emulate', { colorScheme: 'auto' });
    expect(connection.send).toHaveBeenCalledWith('Emulation.setEmulatedMedia', { features: [] });
  });

  it('sets cpuThrottlingRate', async () => {
    await server.invokeTool('browser_emulate', { cpuThrottlingRate: 4 });
    expect(connection.send).toHaveBeenCalledWith('Emulation.setCPUThrottlingRate', { rate: 4 });
  });

  it('applies a network conditions preset and enables network capture as a side effect', async () => {
    const response = await server.invokeTool('browser_emulate', { networkConditions: 'Slow 3G' });

    expect(ensureNetworkCaptureEnabled).toHaveBeenCalled();
    expect(connection.send).toHaveBeenCalledWith(
      'Network.emulateNetworkConditions',
      expect.objectContaining({ offline: false, latency: 400 })
    );
    expect(response.content[0].text).toContain('networkConditions=Slow 3G');
  });

  it('sets and clears geolocation', async () => {
    await server.invokeTool('browser_emulate', { geolocation: '37.7749,-122.4194' });
    expect(connection.send).toHaveBeenCalledWith('Emulation.setGeolocationOverride', {
      latitude: 37.7749,
      longitude: -122.4194,
      accuracy: 1
    });

    await server.invokeTool('browser_emulate', { geolocation: '' });
    expect(connection.send).toHaveBeenCalledWith('Emulation.clearGeolocationOverride', {});
  });

  it('rejects an invalid geolocation string', async () => {
    const response = await server.invokeTool('browser_emulate', { geolocation: 'not-a-location' });
    expect(response.isError).toBe(true);
    expect(response.content[0].text).toContain('Invalid geolocation');
  });

  it('overrides and resets the user agent', async () => {
    await server.invokeTool('browser_emulate', { userAgent: 'CustomAgent/1.0' });
    expect(connection.send).toHaveBeenCalledWith('Emulation.setUserAgentOverride', { userAgent: 'CustomAgent/1.0' });

    connection.send.mockResolvedValueOnce({ userAgent: 'RealDefaultAgent/1.0' });
    await server.invokeTool('browser_emulate', { userAgent: '' });
    expect(connection.send).toHaveBeenCalledWith('Browser.getVersion', {});
    expect(connection.send).toHaveBeenCalledWith('Emulation.setUserAgentOverride', { userAgent: 'RealDefaultAgent/1.0' });
  });

  it('sets and clears extra HTTP headers', async () => {
    await server.invokeTool('browser_emulate', { extraHttpHeaders: '{"X-Custom":"value"}' });
    expect(connection.send).toHaveBeenCalledWith('Network.setExtraHTTPHeaders', { headers: { 'X-Custom': 'value' } });

    await server.invokeTool('browser_emulate', { extraHttpHeaders: '' });
    expect(connection.send).toHaveBeenCalledWith('Network.setExtraHTTPHeaders', { headers: {} });
  });

  it('rejects malformed extraHttpHeaders JSON', async () => {
    const response = await server.invokeTool('browser_emulate', { extraHttpHeaders: 'not json' });
    expect(response.isError).toBe(true);
  });

  it('parses and applies a viewport string, including mobile/touch/landscape flags', async () => {
    await server.invokeTool('browser_emulate', { viewport: '375x667x2,mobile,touch,landscape' });

    expect(connection.send).toHaveBeenCalledWith('Emulation.setDeviceMetricsOverride', {
      width: 375,
      height: 667,
      deviceScaleFactor: 2,
      mobile: true,
      screenOrientation: { type: 'landscapePrimary', angle: 90 }
    });
    expect(connection.send).toHaveBeenCalledWith('Emulation.setTouchEmulationEnabled', { enabled: true });
  });

  it('defaults deviceScaleFactor to 1 and flags to false when omitted', async () => {
    await server.invokeTool('browser_emulate', { viewport: '1280x720' });

    expect(connection.send).toHaveBeenCalledWith('Emulation.setDeviceMetricsOverride', {
      width: 1280,
      height: 720,
      deviceScaleFactor: 1,
      mobile: false,
      screenOrientation: { type: 'portraitPrimary', angle: 0 }
    });
    expect(connection.send).toHaveBeenCalledWith('Emulation.setTouchEmulationEnabled', { enabled: false });
  });

  it('rejects an invalid viewport string', async () => {
    const response = await server.invokeTool('browser_emulate', { viewport: 'not-a-viewport' });
    expect(response.isError).toBe(true);
    expect(response.content[0].text).toContain('Invalid viewport');
  });

  it('returns an error when the CDP connection cannot be established', async () => {
    getCdpConnection.mockRejectedValue(new Error('No active browser session. Call browser_start first.'));

    const response = await server.invokeTool('browser_emulate', { colorScheme: 'dark' });

    expect(response.isError).toBe(true);
  });
});
