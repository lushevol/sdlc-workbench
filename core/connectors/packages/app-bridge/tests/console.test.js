import { describe, it, expect, beforeEach, vi } from 'vitest';
import { createMockServer, isValidToolResponse } from '@sc-node-mcp/shared-tests/helpers/mockServer';

vi.mock('../src/cdp.js', () => ({
  ensureConsoleCaptureEnabled: vi.fn().mockResolvedValue(undefined),
  getConsoleMessages: vi.fn().mockReturnValue([]),
  clearConsoleMessages: vi.fn()
}));

const { ensureConsoleCaptureEnabled, getConsoleMessages, clearConsoleMessages } = await import('../src/cdp.js');
const { configureConsoleTools } = await import('../src/tools/console.js');

function makeMessage(overrides = {}) {
  return {
    msgid: 1,
    source: 'console-api',
    type: 'log',
    text: 'hello world',
    timestamp: 1,
    stackTrace: undefined,
    ...overrides
  };
}

describe('console tools', () => {
  let server;

  beforeEach(() => {
    vi.clearAllMocks();
    ensureConsoleCaptureEnabled.mockResolvedValue(undefined);
    getConsoleMessages.mockReturnValue([]);
    server = createMockServer();
    configureConsoleTools(server);
  });

  describe('console_list_messages', () => {
    it('lists all captured messages as summaries', async () => {
      getConsoleMessages.mockReturnValue([makeMessage(), makeMessage({ msgid: 2, type: 'error' })]);

      const response = await server.invokeTool('console_list_messages', {});

      expect(ensureConsoleCaptureEnabled).toHaveBeenCalled();
      const parsed = JSON.parse(response.content[0].text);
      expect(parsed.total).toBe(2);
      expect(parsed.messages).toHaveLength(2);
      expect(isValidToolResponse(response)).toBe(true);
    });

    it('filters by types', async () => {
      getConsoleMessages.mockReturnValue([makeMessage({ msgid: 1, type: 'log' }), makeMessage({ msgid: 2, type: 'error' })]);

      const response = await server.invokeTool('console_list_messages', { types: ['error'] });

      const parsed = JSON.parse(response.content[0].text);
      expect(parsed.total).toBe(1);
      expect(parsed.messages[0].msgid).toBe(2);
    });

    it('truncates long message text in the summary', async () => {
      getConsoleMessages.mockReturnValue([makeMessage({ text: 'x'.repeat(300) })]);

      const response = await server.invokeTool('console_list_messages', {});

      const parsed = JSON.parse(response.content[0].text);
      expect(parsed.messages[0].text.endsWith('...')).toBe(true);
      expect(parsed.messages[0].text.length).toBeLessThan(300);
    });

    it('paginates with pageIdx/pageSize', async () => {
      getConsoleMessages.mockReturnValue([makeMessage({ msgid: 1 }), makeMessage({ msgid: 2 }), makeMessage({ msgid: 3 })]);

      const response = await server.invokeTool('console_list_messages', { pageIdx: 1, pageSize: 2 });

      const parsed = JSON.parse(response.content[0].text);
      expect(parsed.messages).toHaveLength(1);
      expect(parsed.messages[0].msgid).toBe(3);
    });

    it('returns an error when capture cannot be enabled', async () => {
      ensureConsoleCaptureEnabled.mockRejectedValue(new Error('No active browser session. Call browser_start first.'));

      const response = await server.invokeTool('console_list_messages', {});

      expect(response.isError).toBe(true);
    });
  });

  describe('console_get_message', () => {
    it('returns an error when the msgid is not found', async () => {
      getConsoleMessages.mockReturnValue([]);

      const response = await server.invokeTool('console_get_message', { msgid: 99 });

      expect(response.isError).toBe(true);
      expect(response.content[0].text).toContain('No console message found with msgid 99');
    });

    it('returns the full message detail including the stack trace', async () => {
      getConsoleMessages.mockReturnValue([makeMessage({ stackTrace: { callFrames: [] } })]);

      const response = await server.invokeTool('console_get_message', { msgid: 1 });

      const parsed = JSON.parse(response.content[0].text);
      expect(parsed.stackTrace).toEqual({ callFrames: [] });
      expect(parsed.text).toBe('hello world');
    });
  });

  describe('console_clear_messages', () => {
    it('clears the buffer', async () => {
      const response = await server.invokeTool('console_clear_messages', {});

      expect(clearConsoleMessages).toHaveBeenCalled();
      expect(isValidToolResponse(response)).toBe(true);
    });
  });
});
