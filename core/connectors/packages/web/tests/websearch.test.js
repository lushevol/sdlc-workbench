import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { createMockServer, isValidToolResponse, isValidErrorResponse } from '@sc-node-mcp/shared-tests/helpers/mockServer';
import { configureWebSearchTools, stripHtml, parseDdgResults, findPython3Command, clearPythonCache } from '../src/tools/websearch.js';

// ── Mock child_process (Python bridge for web_search) ────────────────────────

vi.mock('child_process', () => ({
  spawn: vi.fn(),
  execSync: vi.fn(),
}));

import { spawn, execSync } from 'child_process';

// ── Mock node:https (used only by web_fetch) ──────────────────────────────────

vi.mock('node:https', () => ({
  default: { request: vi.fn() },
}));

import https from 'node:https';

// ── DDG Lite HTML fixture ─────────────────────────────────────────────────────

const DDG_LITE_HTML = `
<html><body>
<table>
<tr><td><a rel="nofollow" href="https://example.com/weather" class="result-link">Chennai Weather Today</a></td></tr>
<tr><td class="result-snippet">Current temperature in Chennai is 34°C with humid conditions.</td></tr>
<tr><td><a rel="nofollow" href="https://weather.com/chennai" class="result-link">Chennai Forecast</a></td></tr>
<tr><td class="result-snippet">Weekly forecast for Chennai shows high humidity.</td></tr>
</table>
</body></html>`;

// ── Python spawn helpers ──────────────────────────────────────────────────────

const PARSED_RESULTS = [
  { title: 'Chennai Weather Today', url: 'https://example.com/weather', snippet: 'Current temperature in Chennai is 34°C with humid conditions.' },
  { title: 'Chennai Forecast', url: 'https://weather.com/chennai', snippet: 'Weekly forecast for Chennai shows high humidity.' },
];

function mockPythonSuccess(results = PARSED_RESULTS) {
  execSync.mockReturnValue('Python 3.11.0');
  spawn.mockImplementation(() => ({
    stdin: { write: vi.fn(), end: vi.fn() },
    stdout: { on: vi.fn((event, cb) => event === 'data' && cb(JSON.stringify({ results }))) },
    stderr: { on: vi.fn() },
    on: vi.fn((event, cb) => event === 'close' && cb(0)),
  }));
}

function mockPythonError(errorMsg) {
  execSync.mockReturnValue('Python 3.11.0');
  spawn.mockImplementation(() => ({
    stdin: { write: vi.fn(), end: vi.fn() },
    stdout: { on: vi.fn((event, cb) => event === 'data' && cb(JSON.stringify({ error: errorMsg }))) },
    stderr: { on: vi.fn() },
    on: vi.fn((event, cb) => event === 'close' && cb(0)),
  }));
}

function mockPythonNonZeroExit(stderrMsg = 'Python crashed') {
  execSync.mockReturnValue('Python 3.11.0');
  spawn.mockImplementation(() => ({
    stdin: { write: vi.fn(), end: vi.fn() },
    stdout: { on: vi.fn() },
    stderr: { on: vi.fn((event, cb) => event === 'data' && cb(stderrMsg)) },
    on: vi.fn((event, cb) => event === 'close' && cb(1)),
  }));
}

// ── https mock helpers (for web_fetch) ───────────────────────────────────────

function mockHttpsResponse(statusCode, body) {
  https.request.mockImplementation((options, callback) => {
    const res = {
      statusCode, headers: {},
      on: vi.fn((event, handler) => {
        if (event === 'data') handler(body);
        if (event === 'end') handler();
      }),
    };
    callback(res);
    return { on: vi.fn(), end: vi.fn(), write: vi.fn() };
  });
}

function mockHttpsError(errorMessage) {
  https.request.mockImplementation(() => ({
    on: vi.fn((event, handler) => {
      if (event === 'error') handler(new Error(errorMessage));
    }),
    end: vi.fn(), write: vi.fn(),
  }));
}

// ── stripHtml() ───────────────────────────────────────────────────────────────

describe('stripHtml()', () => {
  it('removes HTML tags', () => {
    expect(stripHtml('<p>Hello</p>')).toBe('Hello');
  });

  it('removes script tags and content', () => {
    expect(stripHtml('<script>alert("x")</script>text')).toBe('text');
  });

  it('removes style tags and content', () => {
    expect(stripHtml('<style>.a{color:red}</style>text')).toBe('text');
  });

  it('decodes common HTML entities', () => {
    expect(stripHtml('a &amp; b &lt;c&gt; &quot;d&quot; &#39;e&#39; &nbsp;f')).toBe("a & b <c> \"d\" 'e' f");
  });

  it('collapses multiple whitespace into single space', () => {
    expect(stripHtml('a   b\n\tc')).toBe('a b c');
  });

  it('returns empty string for empty input', () => {
    expect(stripHtml('')).toBe('');
  });
});

// ── parseDdgResults() ─────────────────────────────────────────────────────────

describe('parseDdgResults()', () => {
  it('parses titles, URLs, and snippets from DDG Lite HTML', () => {
    const results = parseDdgResults(DDG_LITE_HTML);
    expect(results.length).toBeGreaterThanOrEqual(2);
    expect(results[0].title).toBe('Chennai Weather Today');
    expect(results[0].url).toBe('https://example.com/weather');
    expect(results[0].snippet).toContain('34°C');
  });

  it('respects the maxResults limit', () => {
    const results = parseDdgResults(DDG_LITE_HTML, 1);
    expect(results).toHaveLength(1);
  });

  it('returns empty array for empty HTML', () => {
    expect(parseDdgResults('')).toHaveLength(0);
  });

  it('decodes HTML entities in titles and snippets', () => {
    const html = '<a href="https://x.com" class="result-link">A &amp; B</a>\n<td class="result-snippet">foo &lt;bar&gt;</td>';
    const results = parseDdgResults(html, 5);
    expect(results[0].title).toBe('A & B');
    expect(results[0].snippet).toBe('foo <bar>');
  });

  it('skips entries with empty title or url', () => {
    const html = '<a href="" class="result-link"></a>\n<td class="result-snippet">orphan snippet</td>';
    const results = parseDdgResults(html, 5);
    expect(results).toHaveLength(0);
  });

  it('handles missing snippets gracefully', () => {
    const html = '<a href="https://example.com" class="result-link">Title Only</a>';
    const results = parseDdgResults(html, 5);
    expect(results[0].snippet).toBe('');
  });
});

// ── findPython3Command() ──────────────────────────────────────────────────────

describe('findPython3Command()', () => {
  beforeEach(() => { clearPythonCache(); vi.clearAllMocks(); });
  afterEach(() => clearPythonCache());

  it('returns python3 when it reports Python 3.x', () => {
    execSync.mockReturnValue('Python 3.11.0\n');
    expect(findPython3Command()).toBe('python3');
  });

  it('caches result on subsequent calls', () => {
    execSync.mockReturnValue('Python 3.9.0');
    findPython3Command();
    findPython3Command();
    expect(execSync).toHaveBeenCalledTimes(1);
  });

  it('throws when no Python 3.x executable is found', () => {
    execSync.mockImplementation(() => { throw new Error('not found'); });
    expect(() => findPython3Command()).toThrow('Python 3.x not found');
  });
});

// ── web_search tool ───────────────────────────────────────────────────────────

describe('web_search tool', () => {
  let mockServer;

  beforeEach(() => {
    clearPythonCache();
    vi.clearAllMocks();
    mockServer = createMockServer();
    configureWebSearchTools(mockServer);
  });

  afterEach(() => {
    clearPythonCache();
    delete process.env.HTTPS_PROXY;
  });

  it('registers web_search on the server', () => {
    const names = mockServer.getRegisteredTools().map(t => t.name);
    expect(names).toContain('web_search');
  });

  it('returns structured results on success', async () => {
    mockPythonSuccess();

    const response = await mockServer.invokeTool('web_search', { query: 'Chennai weather' });

    expect(isValidToolResponse(response)).toBe(true);
    expect(response.isError).toBeFalsy();
    expect(response.content[0].text).toContain('Chennai Weather Today');
    expect(response.content[0].text).toContain('https://example.com/weather');
    expect(response.content[0].text).toContain('34°C');
  });

  it('formats results as numbered markdown list', async () => {
    mockPythonSuccess();

    const response = await mockServer.invokeTool('web_search', { query: 'test' });

    expect(response.content[0].text).toMatch(/^1\. \*\*/m);
    expect(response.content[0].text).toMatch(/2\. \*\*/);
  });

  it('returns "No results found" when Python returns empty array', async () => {
    mockPythonSuccess([]);

    const response = await mockServer.invokeTool('web_search', { query: 'xyzzy123' });

    expect(isValidToolResponse(response)).toBe(true);
    expect(response.content[0].text).toContain('No results found');
  });

  it('returns isError true when Python reports an error', async () => {
    mockPythonError('HTTP 403: Forbidden');

    const response = await mockServer.invokeTool('web_search', { query: 'fail' });

    expect(isValidErrorResponse(response)).toBe(true);
    expect(response.content[0].text).toContain('403');
  });

  it('returns isError true when Python exits non-zero', async () => {
    mockPythonNonZeroExit('SyntaxError: bad input');

    const response = await mockServer.invokeTool('web_search', { query: 'crash' });

    expect(isValidErrorResponse(response)).toBe(true);
  });

  it('returns isError true when Python is not found', async () => {
    execSync.mockImplementation(() => { throw new Error('not found'); });

    const response = await mockServer.invokeTool('web_search', { query: 'no python' });

    expect(isValidErrorResponse(response)).toBe(true);
    expect(response.content[0].text).toContain('Python 3.x not found');
  });

  it('passes the proxy to the Python script via stdin JSON', async () => {
    let stdinData = '';
    execSync.mockReturnValue('Python 3.11.0');
    spawn.mockImplementation(() => {
      const stdinMock = { write: vi.fn((d) => { stdinData += d; }), end: vi.fn() };
      return {
        stdin: stdinMock,
        stdout: { on: vi.fn((event, cb) => event === 'data' && cb(JSON.stringify({ results: PARSED_RESULTS }))) },
        stderr: { on: vi.fn() },
        on: vi.fn((event, cb) => event === 'close' && cb(0)),
      };
    });

    const serverWithProxy = createMockServer();
    configureWebSearchTools(serverWithProxy, 'http://127.0.0.1:9000');
    await serverWithProxy.invokeTool('web_search', { query: 'proxy test' });

    const payload = JSON.parse(stdinData);
    expect(payload.proxy).toBe('http://127.0.0.1:9000');
    expect(payload.query).toBe('proxy test');
  });

  it('passes the query to the Python script', async () => {
    let stdinData = '';
    execSync.mockReturnValue('Python 3.11.0');
    spawn.mockImplementation(() => {
      const stdinMock = { write: vi.fn((d) => { stdinData += d; }), end: vi.fn() };
      return {
        stdin: stdinMock,
        stdout: { on: vi.fn((event, cb) => event === 'data' && cb(JSON.stringify({ results: [] }))) },
        stderr: { on: vi.fn() },
        on: vi.fn((event, cb) => event === 'close' && cb(0)),
      };
    });

    await mockServer.invokeTool('web_search', { query: 'Chennai weather 2026' });

    const payload = JSON.parse(stdinData);
    expect(payload.query).toBe('Chennai weather 2026');
  });

  it('invokes the correct search-ddg.py script path', async () => {
    mockPythonSuccess();

    await mockServer.invokeTool('web_search', { query: 'test' });

    const spawnArgs = spawn.mock.calls[0];
    expect(spawnArgs[1][0]).toContain('search-ddg.py');
    expect(spawnArgs[1][0]).toContain('scripts');
  });

  it('returns "No results found" when Python returns {} without results key', async () => {
    execSync.mockReturnValue('Python 3.11.0');
    spawn.mockImplementation(() => ({
      stdin: { write: vi.fn(), end: vi.fn() },
      stdout: { on: vi.fn((event, cb) => event === 'data' && cb(JSON.stringify({}))) },
      stderr: { on: vi.fn() },
      on: vi.fn((event, cb) => event === 'close' && cb(0)),
    }));

    const response = await mockServer.invokeTool('web_search', { query: 'missing key' });

    expect(isValidToolResponse(response)).toBe(true);
    expect(response.content[0].text).toContain('No results found');
  });

  it('returns isError true when Python stdout is invalid JSON', async () => {
    execSync.mockReturnValue('Python 3.11.0');
    spawn.mockImplementation(() => ({
      stdin: { write: vi.fn(), end: vi.fn() },
      stdout: { on: vi.fn((event, cb) => event === 'data' && cb('not valid json {{{')) },
      stderr: { on: vi.fn() },
      on: vi.fn((event, cb) => event === 'close' && cb(0)),
    }));

    const response = await mockServer.invokeTool('web_search', { query: 'bad json' });

    expect(isValidErrorResponse(response)).toBe(true);
    expect(response.content[0].text).toContain('Failed to parse search response');
  });

  it('falls back to String(error) when spawn emits error with no message', async () => {
    execSync.mockReturnValue('Python 3.11.0');
    spawn.mockImplementation(() => ({
      stdin: { write: vi.fn(), end: vi.fn() },
      stdout: { on: vi.fn() },
      stderr: { on: vi.fn() },
      on: vi.fn((event, cb) => event === 'error' && cb({ code: 'ENOENT' })),
    }));

    const response = await mockServer.invokeTool('web_search', { query: 'spawn error' });

    expect(isValidErrorResponse(response)).toBe(true);
    expect(response.content[0].text).toContain('[object Object]');
  });
});

// ── web_fetch tool ────────────────────────────────────────────────────────────

describe('web_fetch tool', () => {
  let mockServer;

  beforeEach(() => {
    vi.clearAllMocks();
    mockServer = createMockServer();
    configureWebSearchTools(mockServer);
  });

  afterEach(() => {
    delete process.env.HTTPS_PROXY;
  });

  it('registers web_fetch on the server', () => {
    const names = mockServer.getRegisteredTools().map(t => t.name);
    expect(names).toContain('web_fetch');
  });

  it('returns stripped text on successful fetch', async () => {
    const htmlBody = '<html><body><h1>Page Title</h1><p>Page content here.</p></body></html>';
    mockHttpsResponse(200, htmlBody);

    const response = await mockServer.invokeTool('web_fetch', { url: 'https://example.com/page' });

    expect(isValidToolResponse(response)).toBe(true);
    expect(response.isError).toBeFalsy();
    expect(response.content[0].text).toContain('Page Title');
    expect(response.content[0].text).toContain('Page content here.');
  });

  it('truncates response to 15000 characters', async () => {
    const longBody = '<p>' + 'x'.repeat(20000) + '</p>';
    mockHttpsResponse(200, longBody);

    const response = await mockServer.invokeTool('web_fetch', { url: 'https://example.com' });

    expect(response.content[0].text.length).toBeLessThanOrEqual(15000);
  });

  it('returns isError true on non-200 status code', async () => {
    mockHttpsResponse(404, '');

    const response = await mockServer.invokeTool('web_fetch', { url: 'https://example.com/missing' });

    expect(isValidErrorResponse(response)).toBe(true);
    expect(response.content[0].text).toContain('404');
  });

  it('returns isError true when https throws', async () => {
    mockHttpsError('ETIMEDOUT');

    const response = await mockServer.invokeTool('web_fetch', { url: 'https://example.com' });

    expect(isValidErrorResponse(response)).toBe(true);
    expect(response.content[0].text).toContain('ETIMEDOUT');
  });

  it('falls back to String(error) when error has no message', async () => {
    https.request.mockImplementation(() => ({
      on: vi.fn((event, handler) => {
        if (event === 'error') handler({ toString: () => 'FetchErrorObject' });
      }),
      end: vi.fn(), write: vi.fn(),
    }));

    const response = await mockServer.invokeTool('web_fetch', { url: 'https://example.com' });

    expect(isValidErrorResponse(response)).toBe(true);
  });

  it('uses HttpsProxyAgent when HTTPS_PROXY is set', async () => {
    process.env.HTTPS_PROXY = 'http://proxy.example.com:8080';
    mockHttpsResponse(200, '<p>result</p>');

    const response = await mockServer.invokeTool('web_fetch', { url: 'https://example.com' });

    expect(isValidToolResponse(response)).toBe(true);
    expect(https.request).toHaveBeenCalledWith(
      expect.objectContaining({ agent: expect.anything() }),
      expect.any(Function)
    );
  });

  it('sends request to the correct hostname and path', async () => {
    mockHttpsResponse(200, '<p>ok</p>');

    await mockServer.invokeTool('web_fetch', { url: 'https://example.com/some/path?q=1' });

    const callOptions = https.request.mock.calls[0][0];
    expect(callOptions.hostname).toBe('example.com');
    expect(callOptions.path).toBe('/some/path?q=1');
  });

  it('uses GET method for web_fetch', async () => {
    mockHttpsResponse(200, '<p>ok</p>');

    await mockServer.invokeTool('web_fetch', { url: 'https://example.com' });

    const callOptions = https.request.mock.calls[0][0];
    expect(callOptions.method).toBe('GET');
  });

  it('follows a redirect (302) to the final page', async () => {
    let callCount = 0;
    https.request.mockImplementation((options, callback) => {
      callCount++;
      if (callCount === 1) {
        const res = {
          statusCode: 302,
          headers: { location: 'https://example.com/final' },
          on: vi.fn((event, handler) => { if (event === 'end') handler(); }),
          resume: vi.fn(),
        };
        callback(res);
      } else {
        const res = {
          statusCode: 200,
          headers: {},
          on: vi.fn((event, handler) => {
            if (event === 'data') handler('<p>redirected content</p>');
            if (event === 'end') handler();
          }),
        };
        callback(res);
      }
      return { on: vi.fn(), end: vi.fn(), write: vi.fn() };
    });

    const response = await mockServer.invokeTool('web_fetch', { url: 'https://example.com/old' });

    expect(isValidToolResponse(response)).toBe(true);
    expect(response.content[0].text).toContain('redirected content');
  });
});
