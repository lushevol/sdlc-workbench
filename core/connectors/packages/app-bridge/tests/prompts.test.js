import { describe, it, expect, vi } from 'vitest';
import { configureAppBridgePrompts, APP_BRIDGE_PROMPTS, generateAppBridgePromptMessage } from '../src/prompts.js';

describe('APP_BRIDGE_PROMPTS constant', () => {
  it('is defined with 3 prompts', () => {
    expect(APP_BRIDGE_PROMPTS).toBeDefined();
    expect(Object.keys(APP_BRIDGE_PROMPTS)).toHaveLength(3);
  });

  it('OPEN_AND_SCREENSHOT has a required url argument', () => {
    const urlArg = APP_BRIDGE_PROMPTS.OPEN_AND_SCREENSHOT.arguments.find((a) => a.name === 'url');
    expect(urlArg).toBeDefined();
    expect(urlArg.required).toBe(true);
  });

  it('every prompt has a non-empty description', () => {
    for (const prompt of Object.values(APP_BRIDGE_PROMPTS)) {
      expect(typeof prompt.description).toBe('string');
      expect(prompt.description.length).toBeGreaterThan(0);
    }
  });
});

describe('generateAppBridgePromptMessage', () => {
  it('generates a message for open-and-screenshot with defaults', () => {
    const message = generateAppBridgePromptMessage('open-and-screenshot', {});
    expect(message).toContain('chrome');
    expect(message).toContain('browser_start');
  });

  it('generates a message for open-and-screenshot with explicit args', () => {
    const message = generateAppBridgePromptMessage('open-and-screenshot', { url: 'https://example.com', browser: 'edge' });
    expect(message).toContain('https://example.com');
    expect(message).toContain('edge');
  });

  it('generates a message for find-and-click', () => {
    const message = generateAppBridgePromptMessage('find-and-click', { description: 'the Submit button' });
    expect(message).toContain('the Submit button');
    expect(message).toContain('element_click');
  });

  it('generates a message for fill-a-form', () => {
    const message = generateAppBridgePromptMessage('fill-a-form', { fields: 'name=John' });
    expect(message).toContain('name=John');
    expect(message).toContain('select_option');
  });

  it('returns a fallback message for an unknown prompt', () => {
    expect(generateAppBridgePromptMessage('unknown-prompt', {})).toBe('Unknown prompt');
  });
});

describe('configureAppBridgePrompts', () => {
  it('registers all app-bridge prompts on the server', () => {
    const server = { prompt: vi.fn() };
    configureAppBridgePrompts(server);
    expect(server.prompt).toHaveBeenCalledTimes(3);
  });

  it('registers each prompt callback returning a valid MCP message', async () => {
    const server = { prompt: vi.fn() };
    configureAppBridgePrompts(server);

    for (const call of server.prompt.mock.calls) {
      const callback = call[call.length - 1];
      const result = await callback({});
      expect(result.messages).toHaveLength(1);
      expect(result.messages[0].role).toBe('user');
      expect(typeof result.messages[0].content.text).toBe('string');
    }
  });

  it('handles a callback invoked with no arguments', async () => {
    const server = { prompt: vi.fn() };
    configureAppBridgePrompts(server);

    const call = server.prompt.mock.calls.find((c) => c[0] === 'open-and-screenshot');
    const callback = call[call.length - 1];
    const result = await callback();

    expect(result.messages).toHaveLength(1);
  });
});
