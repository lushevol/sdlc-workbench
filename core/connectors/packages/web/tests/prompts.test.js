import { describe, it, expect, vi, beforeEach } from 'vitest';
import { configureWebPrompts, WEB_PROMPTS, generateWebPromptMessage } from '../src/prompts.js';

describe('WEB_PROMPTS constant', () => {
  it('exports WEB_PROMPTS object', () => {
    expect(WEB_PROMPTS).toBeDefined();
    expect(typeof WEB_PROMPTS).toBe('object');
  });

  it('contains 4 prompts', () => {
    expect(Object.keys(WEB_PROMPTS)).toHaveLength(4);
  });

  it('WEB_SEARCH has correct name', () => {
    expect(WEB_PROMPTS.WEB_SEARCH.name).toBe('web-search');
  });

  it('WEB_FETCH has correct name', () => {
    expect(WEB_PROMPTS.WEB_FETCH.name).toBe('web-fetch');
  });

  it('each prompt has a description', () => {
    for (const prompt of Object.values(WEB_PROMPTS)) {
      expect(typeof prompt.description).toBe('string');
      expect(prompt.description.length).toBeGreaterThan(0);
    }
  });

  it('WEB_SEARCH has a required query argument', () => {
    const queryArg = WEB_PROMPTS.WEB_SEARCH.arguments.find(a => a.name === 'query');
    expect(queryArg).toBeDefined();
    expect(queryArg.required).toBe(true);
  });

  it('WEB_FETCH has a required url argument', () => {
    const urlArg = WEB_PROMPTS.WEB_FETCH.arguments.find(a => a.name === 'url');
    expect(urlArg).toBeDefined();
    expect(urlArg.required).toBe(true);
  });
});

describe('configureWebPrompts()', () => {
  let mockServer;

  beforeEach(() => {
    mockServer = { prompt: vi.fn() };
  });

  it('registers 4 prompts on the server', () => {
    configureWebPrompts(mockServer);
    expect(mockServer.prompt).toHaveBeenCalledTimes(4);
  });

  it('registers web-search prompt', () => {
    configureWebPrompts(mockServer);
    const call = mockServer.prompt.mock.calls.find(c => c[0] === 'web-search');
    expect(call).toBeDefined();
  });

  it('registers web-fetch prompt', () => {
    configureWebPrompts(mockServer);
    const call = mockServer.prompt.mock.calls.find(c => c[0] === 'web-fetch');
    expect(call).toBeDefined();
  });

  it('works without getContext option', () => {
    expect(() => configureWebPrompts(mockServer)).not.toThrow();
  });

  it('works with a getContext function that returns null', () => {
    expect(() => configureWebPrompts(mockServer, { getContext: () => null })).not.toThrow();
  });

  it('logs registration count to stderr', () => {
    const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
    configureWebPrompts(mockServer);
    expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining('4'));
    consoleSpy.mockRestore();
  });

  it('web-search handler returns a valid MCP message with query', async () => {
    configureWebPrompts(mockServer);
    const call = mockServer.prompt.mock.calls.find(c => c[0] === 'web-search');
    // call is [name, description, argsSchema, callback]
    const callback = call[call.length - 1];
    const result = await callback({ query: 'latest Node.js version' });
    expect(result.messages).toHaveLength(1);
    expect(result.messages[0].role).toBe('user');
    expect(result.messages[0].content.text).toContain('latest Node.js version');
  });

  it('web-fetch handler returns a valid MCP message with url', async () => {
    configureWebPrompts(mockServer);
    const call = mockServer.prompt.mock.calls.find(c => c[0] === 'web-fetch');
    const callback = call[call.length - 1];
    const result = await callback({ url: 'https://example.com' });
    expect(result.messages).toHaveLength(1);
    expect(result.messages[0].content.text).toContain('https://example.com');
  });

  it('web-search handler handles missing args gracefully', async () => {
    configureWebPrompts(mockServer);
    const call = mockServer.prompt.mock.calls.find(c => c[0] === 'web-search');
    const callback = call[call.length - 1];
    const result = await callback({});
    expect(result.messages[0].content.text).toContain('enter your search query');
  });

  it('web-fetch handler handles missing url gracefully', async () => {
    configureWebPrompts(mockServer);
    const call = mockServer.prompt.mock.calls.find(c => c[0] === 'web-fetch');
    const callback = call[call.length - 1];
    const result = await callback({});
    expect(result.messages[0].content.text).toContain('enter the URL');
  });

  it('callback handles null args via null coalescing', async () => {
    configureWebPrompts(mockServer);
    const call = mockServer.prompt.mock.calls.find(c => c[0] === 'web-search');
    const callback = call[call.length - 1];
    const result = await callback(null);
    expect(result.messages[0].content.text).toBeDefined();
  });

  it('calls getContext on each callback invocation', async () => {
    const getContext = vi.fn(() => null);
    configureWebPrompts(mockServer, { getContext });
    const call = mockServer.prompt.mock.calls.find(c => c[0] === 'web-search');
    const callback = call[call.length - 1];
    await callback({ query: 'test' });
    expect(getContext).toHaveBeenCalledOnce();
  });
});

describe('generateWebPromptMessage()', () => {
  it('returns Unknown prompt for unrecognised name', () => {
    expect(generateWebPromptMessage('unknown-tool', {})).toBe('Unknown prompt');
  });

  it('includes query in web-search message', () => {
    const msg = generateWebPromptMessage('web-search', { query: 'hello' });
    expect(msg).toContain('hello');
  });

  it('includes placeholder when query is missing in web-search', () => {
    const msg = generateWebPromptMessage('web-search', {});
    expect(msg).toContain('enter your search query');
  });

  it('includes url in web-fetch message', () => {
    const msg = generateWebPromptMessage('web-fetch', { url: 'https://example.com' });
    expect(msg).toContain('https://example.com');
  });

  it('includes placeholder when url is missing in web-fetch', () => {
    const msg = generateWebPromptMessage('web-fetch', {});
    expect(msg).toContain('enter the URL');
  });

  it('includes url and mode in web-crawl message', () => {
    const msg = generateWebPromptMessage('web-crawl', { url: 'https://example.com', mode: 'summary' });
    expect(msg).toContain('https://example.com');
    expect(msg).toContain('summary');
  });

  it('defaults mode to "urls" and shows a placeholder url when web-crawl args are missing', () => {
    const msg = generateWebPromptMessage('web-crawl', {});
    expect(msg).toContain('enter the seed URL');
    expect(msg).toContain('"urls"');
  });

  it('includes url and mode in web-crawl-browser message', () => {
    const msg = generateWebPromptMessage('web-crawl-browser', { url: 'https://example.com', mode: 'full' });
    expect(msg).toContain('https://example.com');
    expect(msg).toContain('full');
  });

  it('defaults mode to "summary" and shows a placeholder url when web-crawl-browser args are missing', () => {
    const msg = generateWebPromptMessage('web-crawl-browser', {});
    expect(msg).toContain('enter the seed URL');
    expect(msg).toContain('"summary"');
  });
});
