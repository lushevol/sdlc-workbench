import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { recordStartupTelemetry } from '../src/telemetry.js';

// ─── Mock helpers ────────────────────────────────────────────────────────────

function makeReadableStream(content) {
  const { Readable } = require('node:stream');
  const stream = new Readable();
  stream.push(content);
  stream.push(null);
  return stream;
}

function makeGitApi({
  repoId = 'repo-abc-123',
  refs = [{ objectId: 'deadbeef1234567890000000000000000000000a' }],
  fileContent = null,
  createPushError = null,
} = {}) {
  const mockGetItemContent = fileContent === null
    ? vi.fn().mockRejectedValue(Object.assign(new Error('File not found'), { statusCode: 404 }))
    : vi.fn().mockResolvedValue(Buffer.from(fileContent, 'utf-8'));

  const mockCreatePush = createPushError
    ? vi.fn().mockRejectedValue(createPushError)
    : vi.fn().mockResolvedValue({ commits: [{ commitId: 'new-sha' }] });

  return {
    getRepository: vi.fn().mockResolvedValue({ id: repoId }),
    getRefs: vi.fn().mockResolvedValue(refs),
    getItemContent: mockGetItemContent,
    createPush: mockCreatePush,
  };
}

function makeConnection(gitApi, user = 'Jane Doe') {
  return {
    connect: vi.fn().mockResolvedValue({
      authenticatedUser: { providerDisplayName: user, id: 'user-id-1' },
    }),
    getGitApi: vi.fn().mockResolvedValue(gitApi),
  };
}

const BASE_CONFIG = {
  confluenceConfig: { token: '' },
  nexusConfig: { userCode: '' },
  sonarConfig: { token: '' },
};

const BASE_TELEMETRY_OPTS = { versions: { 'ado': '1.0.0' } };

// ─── Tests ───────────────────────────────────────────────────────────────────

describe('recordStartupTelemetry', () => {
  let consoleErrorSpy;

  beforeEach(() => {
    consoleErrorSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.restoreAllMocks();
    vi.useRealTimers();
    delete process.env.DISABLE_TELEMETRY;
  });

  // ── Opt-out via DISABLE_TELEMETRY ────────────────────────────────────────

  it('skips recording when DISABLE_TELEMETRY=1 is set', async () => {
    process.env.DISABLE_TELEMETRY = '1';
    const getConnection = vi.fn();

    await recordStartupTelemetry(BASE_CONFIG, getConnection, BASE_TELEMETRY_OPTS);

    expect(getConnection).not.toHaveBeenCalled();
    expect(consoleErrorSpy).toHaveBeenCalledWith('[Telemetry] Disabled via DISABLE_TELEMETRY=1');
  });

  it('runs normally when DISABLE_TELEMETRY is unset', async () => {
    delete process.env.DISABLE_TELEMETRY;
    const gitApi = makeGitApi({ refs: [] });
    const connection = makeConnection(gitApi);
    const getConnection = vi.fn().mockResolvedValue(connection);

    await recordStartupTelemetry(BASE_CONFIG, getConnection, BASE_TELEMETRY_OPTS);

    expect(gitApi.createPush).toHaveBeenCalledTimes(1);
  });

  // ── New branch / new file (Add) ──────────────────────────────────────────

  it('creates new file (Add) when branch does not exist yet', async () => {
    const gitApi = makeGitApi({ refs: [], fileContent: null });
    const connection = makeConnection(gitApi);
    const getConnection = vi.fn().mockResolvedValue(connection);

    await recordStartupTelemetry(BASE_CONFIG, getConnection, BASE_TELEMETRY_OPTS);

    const pushCall = gitApi.createPush.mock.calls[0];
    const push = pushCall[0];

    // Branch creation: oldObjectId must be the zero SHA
    expect(push.refUpdates[0].oldObjectId).toBe('0000000000000000000000000000000000000000');
    expect(push.refUpdates[0].name).toBe('refs/heads/telemetry/usage-log');

    // Change type 1 = Add
    expect(push.commits[0].changes[0].changeType).toBe(1);
    expect(push.commits[0].changes[0].item.path).toBe('/usage.log');
    expect(gitApi.getItemContent).not.toHaveBeenCalled();
  });

  // ── Existing branch, existing file (Edit / append) ──────────────────────

  it('appends to existing file (Edit) when branch and file already exist', async () => {
    const existing = '{"timestamp":"2026-01-01T00:00:00.000Z","user":"Old User","version":"1.0.0","toolsEnabled":["ado"]}\n';
    const gitApi = makeGitApi({ fileContent: existing });
    const connection = makeConnection(gitApi, 'New User');
    const getConnection = vi.fn().mockResolvedValue(connection);

    await recordStartupTelemetry(BASE_CONFIG, getConnection, BASE_TELEMETRY_OPTS);

    const push = gitApi.createPush.mock.calls[0][0];

    // Change type 2 = Edit
    expect(push.commits[0].changes[0].changeType).toBe(2);

    // Content must include both old and new record
    const content = push.commits[0].changes[0].newContent.content;
    expect(content).toContain('"Old User"');
    expect(content).toContain('"New User"');
  });

  it('uses correct tip SHA from existing branch', async () => {
    const tipSha = 'aaaa1111bbbb2222cccc3333dddd4444eeee5555';
    const gitApi = makeGitApi({ refs: [{ objectId: tipSha }], fileContent: 'existing\n' });
    const connection = makeConnection(gitApi);
    const getConnection = vi.fn().mockResolvedValue(connection);

    await recordStartupTelemetry(BASE_CONFIG, getConnection, BASE_TELEMETRY_OPTS);

    const push = gitApi.createPush.mock.calls[0][0];
    expect(push.refUpdates[0].oldObjectId).toBe(tipSha);
  });

  // ── versions field ────────────────────────────────────────────────────────

  it('records a versions object with the package name as key', async () => {
    const gitApi = makeGitApi({ refs: [] });
    const connection = makeConnection(gitApi);
    const getConnection = vi.fn().mockResolvedValue(connection);

    await recordStartupTelemetry(BASE_CONFIG, getConnection, BASE_TELEMETRY_OPTS);

    const push = gitApi.createPush.mock.calls[0][0];
    const record = JSON.parse(push.commits[0].changes[0].newContent.content.trim());
    expect(record.versions).toEqual({ 'ado': '1.0.0' });
  });

  it('records the provided versions object as-is', async () => {
    const gitApi = makeGitApi({ refs: [] });
    const connection = makeConnection(gitApi);
    const getConnection = vi.fn().mockResolvedValue(connection);

    await recordStartupTelemetry(BASE_CONFIG, getConnection, { versions: { 'ado-pipelines': '2.0.0' } });

    const push = gitApi.createPush.mock.calls[0][0];
    const record = JSON.parse(push.commits[0].changes[0].newContent.content.trim());
    expect(record.versions).toEqual({ 'ado-pipelines': '2.0.0' });
  });

  it('records a multi-package versions object when multiple packages are provided', async () => {
    const gitApi = makeGitApi({ refs: [] });
    const connection = makeConnection(gitApi);
    const getConnection = vi.fn().mockResolvedValue(connection);

    const multiVersions = { 'sc-node-mcp': '3.0.0', 'ado': '4.1.0', 'confluence': '2.0.0' };
    await recordStartupTelemetry(BASE_CONFIG, getConnection, { versions: multiVersions });

    const push = gitApi.createPush.mock.calls[0][0];
    const record = JSON.parse(push.commits[0].changes[0].newContent.content.trim());
    expect(record.versions).toEqual(multiVersions);
  });

  // ── Record content ────────────────────────────────────────────────────────

  it('includes user, versions, timestamp, and all schema fields in the record', async () => {
    const gitApi = makeGitApi({ refs: [] });
    const connection = makeConnection(gitApi, 'Alice Smith');
    const getConnection = vi.fn().mockResolvedValue(connection);

    await recordStartupTelemetry(BASE_CONFIG, getConnection, BASE_TELEMETRY_OPTS);

    const push = gitApi.createPush.mock.calls[0][0];
    const record = JSON.parse(push.commits[0].changes[0].newContent.content.trim());

    expect(record.user).toBe('Alice Smith');
    expect(record.versions).toEqual({ 'ado': '1.0.0' });
    expect(record.timestamp).toMatch(/^\d{4}-\d{2}-\d{2}T/);
    expect(record.platform).toBe(process.platform);
    expect(record.nodeVersion).toBe(process.version);
    expect(record.vsCodeVersion).toBeUndefined();
    expect(record.toolsEnabled).toBeUndefined();
    expect(record.version).toBeUndefined();
  });


  it('falls back to user id when providerDisplayName is absent', async () => {
    const gitApi = makeGitApi({ refs: [] });
    const connection = {
      connect: vi.fn().mockResolvedValue({
        authenticatedUser: { providerDisplayName: null, id: 'user-id-fallback' },
      }),
      getGitApi: vi.fn().mockResolvedValue(gitApi),
    };
    const getConnection = vi.fn().mockResolvedValue(connection);

    await recordStartupTelemetry(BASE_CONFIG, getConnection, BASE_TELEMETRY_OPTS);

    const push = gitApi.createPush.mock.calls[0][0];
    const record = JSON.parse(push.commits[0].changes[0].newContent.content.trim());
    expect(record.user).toBe('user-id-fallback');
  });

  // ── Conflict retry (409) ─────────────────────────────────────────────────

  it('retries once on 409 Conflict and succeeds', async () => {
    const conflictError = Object.assign(new Error('Conflict'), { statusCode: 409 });
    // First call throws 409, second call succeeds
    const createPush = vi.fn()
      .mockRejectedValueOnce(conflictError)
      .mockResolvedValueOnce({ commits: [] });

    const gitApi = {
      getRepository: vi.fn().mockResolvedValue({ id: 'repo-id' }),
      getRefs: vi.fn().mockResolvedValue([{ objectId: 'sha1' }]),
      getItemContent: vi.fn().mockResolvedValue(Buffer.from('line1\n')),
      createPush,
    };
    const connection = makeConnection(gitApi);
    const getConnection = vi.fn().mockResolvedValue(connection);

    // Advance the fake timer to satisfy the 1s retry delay
    const promise = recordStartupTelemetry(BASE_CONFIG, getConnection, BASE_TELEMETRY_OPTS);
    await vi.runAllTimersAsync();
    await promise;

    expect(createPush).toHaveBeenCalledTimes(2);
  });

  it('does not retry a second time if the retry also fails', async () => {
    const conflictError = Object.assign(new Error('Conflict'), { statusCode: 409 });
    const createPush = vi.fn().mockRejectedValue(conflictError);

    const gitApi = {
      getRepository: vi.fn().mockResolvedValue({ id: 'repo-id' }),
      getRefs: vi.fn().mockResolvedValue([{ objectId: 'sha1' }]),
      getItemContent: vi.fn().mockResolvedValue(Buffer.from('line1\n')),
      createPush,
    };
    const connection = makeConnection(gitApi);
    const getConnection = vi.fn().mockResolvedValue(connection);

    const promise = recordStartupTelemetry(BASE_CONFIG, getConnection, BASE_TELEMETRY_OPTS);
    await vi.runAllTimersAsync();
    await promise;

    // Called twice (initial + one retry), then gives up
    expect(createPush).toHaveBeenCalledTimes(2);
    expect(consoleErrorSpy).toHaveBeenCalledWith(
      '[Telemetry] Failed to record startup:',
      expect.any(String)
    );
  });

  // ── Graceful failure ─────────────────────────────────────────────────────

  it('catches and logs error if getConnection throws', async () => {
    const getConnection = vi.fn().mockRejectedValue(new Error('network error'));

    await recordStartupTelemetry(BASE_CONFIG, getConnection, BASE_TELEMETRY_OPTS);

    expect(consoleErrorSpy).toHaveBeenCalledWith(
      '[Telemetry] Failed to record startup:',
      'network error'
    );
  });

  it('catches and logs error if getRepository throws', async () => {
    const gitApi = {
      getRepository: vi.fn().mockRejectedValue(new Error('repo not found')),
      getRefs: vi.fn(),
      getItemContent: vi.fn(),
      createPush: vi.fn(),
    };
    const connection = makeConnection(gitApi);
    const getConnection = vi.fn().mockResolvedValue(connection);

    await recordStartupTelemetry(BASE_CONFIG, getConnection, BASE_TELEMETRY_OPTS);

    expect(consoleErrorSpy).toHaveBeenCalledWith(
      '[Telemetry] Failed to record startup:',
      'repo not found'
    );
    expect(gitApi.createPush).not.toHaveBeenCalled();
  });

  it('logs success message after recording', async () => {
    const gitApi = makeGitApi({ refs: [] });
    const connection = makeConnection(gitApi, 'Bob Jones');
    const getConnection = vi.fn().mockResolvedValue(connection);

    await recordStartupTelemetry(BASE_CONFIG, getConnection, BASE_TELEMETRY_OPTS);

    expect(consoleErrorSpy).toHaveBeenCalledWith('[Telemetry] Recorded session for Bob Jones');
  });

  // ── Every startup is always recorded (no deduplication) ──────────────────

  it('records every startup even when the same user+version already exists in the log', async () => {
    // First call: fresh branch
    const gitApi1 = makeGitApi({ refs: [], fileContent: null });
    const connection1 = makeConnection(gitApi1, 'Alice');
    await recordStartupTelemetry(BASE_CONFIG, vi.fn().mockResolvedValue(connection1), BASE_TELEMETRY_OPTS);

    const firstContent = gitApi1.createPush.mock.calls[0][0].commits[0].changes[0].newContent.content;

    // Second call: same user, same version — should still push
    const gitApi2 = makeGitApi({ refs: [{ objectId: 'sha-existing' }], fileContent: firstContent });
    const connection2 = makeConnection(gitApi2, 'Alice');
    await recordStartupTelemetry(BASE_CONFIG, vi.fn().mockResolvedValue(connection2), BASE_TELEMETRY_OPTS);

    expect(gitApi2.createPush).toHaveBeenCalledTimes(1);
    expect(consoleErrorSpy).toHaveBeenCalledWith('[Telemetry] Recorded session for Alice');
  });

  it('records a new entry on every startup regardless of existing log content', async () => {
    const existingContent = '{"timestamp":"2025-01-01T00:00:00.000Z","user":"Alice","version":"0.0.0-placeholder","toolsEnabled":["ado"]}\n';
    const gitApi = makeGitApi({ refs: [{ objectId: 'sha-existing' }], fileContent: existingContent });
    const connection = makeConnection(gitApi, 'Alice');

    await recordStartupTelemetry(BASE_CONFIG, vi.fn().mockResolvedValue(connection), BASE_TELEMETRY_OPTS);

    expect(gitApi.createPush).toHaveBeenCalledTimes(1);
  });

  it('records separate entries for different users on the same startup', async () => {
    const gitApi1 = makeGitApi({ refs: [], fileContent: null });
    await recordStartupTelemetry(BASE_CONFIG, vi.fn().mockResolvedValue(makeConnection(gitApi1, 'Alice')), BASE_TELEMETRY_OPTS);

    const firstContent = gitApi1.createPush.mock.calls[0][0].commits[0].changes[0].newContent.content;

    const gitApi2 = makeGitApi({ refs: [{ objectId: 'sha-existing' }], fileContent: firstContent });
    await recordStartupTelemetry(BASE_CONFIG, vi.fn().mockResolvedValue(makeConnection(gitApi2, 'Bob')), BASE_TELEMETRY_OPTS);

    expect(gitApi2.createPush).toHaveBeenCalledTimes(1);
    const content = gitApi2.createPush.mock.calls[0][0].commits[0].changes[0].newContent.content;
    expect(content).toContain('"Alice"');
    expect(content).toContain('"Bob"');
  });

  // ── 401 / 403 handling ───────────────────────────────────────────────────

  it('logs PAT-expired message and skips when connect() returns 401 (identity not resolved)', async () => {
    const authError = Object.assign(new Error('Failed request: (401)'), { statusCode: 401 });
    const connection = {
      connect: vi.fn().mockRejectedValue(authError),
      getGitApi: vi.fn(),
    };
    const getConnection = vi.fn().mockResolvedValue(connection);

    await recordStartupTelemetry(BASE_CONFIG, getConnection, BASE_TELEMETRY_OPTS);

    expect(consoleErrorSpy).toHaveBeenCalledWith(
      '[Telemetry] Skipped: ADO PAT is invalid or expired. MCP ADO tools will also be unavailable — please refresh your PAT.'
    );
    // Must NOT log the generic failure message
    expect(consoleErrorSpy).not.toHaveBeenCalledWith(
      '[Telemetry] Failed to record startup:',
      expect.any(String)
    );
  });

  // ── Identity timeout handling ─────────────────────────────────────────────

  it('records with user: unknown when connect() times out', async () => {
    const gitApi = makeGitApi({ refs: [] });
    const connection = {
      // connect() that never settles — simulates a missing/wrong proxy environment
      connect: vi.fn().mockReturnValue(new Promise(() => {})),
      getGitApi: vi.fn().mockResolvedValue(gitApi),
    };
    const getConnection = vi.fn().mockResolvedValue(connection);

    const promise = recordStartupTelemetry(BASE_CONFIG, getConnection, BASE_TELEMETRY_OPTS);
    // Advance fake timers to fire the 8-second identity-check timeout
    await vi.runAllTimersAsync();
    await promise;

    // Timeout warning must be logged
    expect(consoleErrorSpy).toHaveBeenCalledWith(
      '[Telemetry] Identity check timed out — recording with user: unknown'
    );
    // Record must still be pushed
    expect(gitApi.createPush).toHaveBeenCalledTimes(1);
    const push = gitApi.createPush.mock.calls[0][0];
    const record = JSON.parse(push.commits[0].changes[0].newContent.content.trim());
    expect(record.user).toBe('unknown');
  });

  it('does not invoke createPush when connect() times out if push also fails', async () => {
    const pushError = new Error('Network error');
    const gitApi = makeGitApi({ createPushError: pushError });
    const connection = {
      connect: vi.fn().mockReturnValue(new Promise(() => {})),
      getGitApi: vi.fn().mockResolvedValue(gitApi),
    };
    const getConnection = vi.fn().mockResolvedValue(connection);

    const promise = recordStartupTelemetry(BASE_CONFIG, getConnection, BASE_TELEMETRY_OPTS);
    await vi.runAllTimersAsync();
    await promise;

    // Timeout warning first, then the push error
    expect(consoleErrorSpy).toHaveBeenCalledWith(
      '[Telemetry] Identity check timed out — recording with user: unknown'
    );
    expect(consoleErrorSpy).toHaveBeenCalledWith(
      '[Telemetry] Failed to record startup:',
      'Network error'
    );
  });

  it('logs no-write-access message and skips when createPush returns 401 (identity resolved)', async () => {
    const pushError = Object.assign(new Error('Failed request: (401)'), { statusCode: 401 });
    const gitApi = makeGitApi({ createPushError: pushError });
    const connection = makeConnection(gitApi, 'Alice');
    const getConnection = vi.fn().mockResolvedValue(connection);

    await recordStartupTelemetry(BASE_CONFIG, getConnection, BASE_TELEMETRY_OPTS);

    expect(consoleErrorSpy).toHaveBeenCalledWith(
      '[Telemetry] Skipped: PAT lacks write access to the telemetry repository. MCP tools are fully functional.'
    );
    expect(consoleErrorSpy).not.toHaveBeenCalledWith(
      '[Telemetry] Failed to record startup:',
      expect.any(String)
    );
  });

  it('applies the same 401 handling when statusCode is 403', async () => {
    const forbiddenError = Object.assign(new Error('Failed request: (403)'), { statusCode: 403 });
    const gitApi = makeGitApi({ createPushError: forbiddenError });
    const connection = makeConnection(gitApi, 'Alice');
    const getConnection = vi.fn().mockResolvedValue(connection);

    await recordStartupTelemetry(BASE_CONFIG, getConnection, BASE_TELEMETRY_OPTS);

    expect(consoleErrorSpy).toHaveBeenCalledWith(
      '[Telemetry] Skipped: PAT lacks write access to the telemetry repository. MCP tools are fully functional.'
    );
  });

  it('does not invoke createPush after a 401 on connect()', async () => {
    const authError = Object.assign(new Error('Failed request: (401)'), { statusCode: 401 });
    const connection = {
      connect: vi.fn().mockRejectedValue(authError),
      getGitApi: vi.fn(),
    };
    const getConnection = vi.fn().mockResolvedValue(connection);

    await recordStartupTelemetry(BASE_CONFIG, getConnection, BASE_TELEMETRY_OPTS);

    expect(connection.getGitApi).not.toHaveBeenCalled();
  });

  // ── Proxy block page (Zscaler) ───────────────────────────────────────────

  it('ignores proxy block page HTML and writes only the new entry when Zscaler intercepts getItemContent', async () => {
    const zscalerHtml =
      '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3c.org/TR/1999/REC-html401-19991224/loose.dtd">\n' +
      '<html><head><title>Internet Security by Zscaler</title></head>\n' +
      '<body>Sorry, you don\'t have permission to visit this site.</body></html>\n';

    const gitApi = makeGitApi({ fileContent: zscalerHtml });
    const connection = makeConnection(gitApi, 'Nishant Vikram Singh');
    const getConnection = vi.fn().mockResolvedValue(connection);

    await recordStartupTelemetry(BASE_CONFIG, getConnection, BASE_TELEMETRY_OPTS);

    const push = gitApi.createPush.mock.calls[0][0];
    const change = push.commits[0].changes[0];

    // File existed in the repo → changeType must be 2 (Edit), not 1 (Add)
    expect(change.changeType).toBe(2);

    // Content must contain no HTML
    const content = change.newContent.content;
    expect(content).not.toContain('<!DOCTYPE');
    expect(content).not.toContain('<html>');
    expect(content).not.toContain('Zscaler');

    // Content must have exactly one line: the new telemetry entry
    const lines = content.trim().split('\n').filter(Boolean);
    expect(lines).toHaveLength(1);
    const entry = JSON.parse(lines[0]);
    expect(entry.user).toBe('Nishant Vikram Singh');
  });

  it('appends new entry after existing valid lines when Zscaler HTML is mixed with valid NDJSON', async () => {
    const mixedContent =
      '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01">\n' +
      '{"timestamp":"2026-01-01T00:00:00.000Z","user":"Previous User","version":"2.0.0","toolsEnabled":["ado"]}\n' +
      '<body>Sorry, blocked.</body>\n';

    const gitApi = makeGitApi({ fileContent: mixedContent });
    const connection = makeConnection(gitApi, 'New User');
    const getConnection = vi.fn().mockResolvedValue(connection);

    await recordStartupTelemetry(BASE_CONFIG, getConnection, BASE_TELEMETRY_OPTS);

    const push = gitApi.createPush.mock.calls[0][0];
    const content = push.commits[0].changes[0].newContent.content;

    // Valid prior entry must be preserved; HTML lines must be gone
    expect(content).toContain('"Previous User"');
    expect(content).toContain('"New User"');
    expect(content).not.toContain('<!DOCTYPE');
    expect(content).not.toContain('<body>');

    // Exactly two entries
    const lines = content.trim().split('\n').filter(Boolean);
    expect(lines).toHaveLength(2);
    lines.forEach(line => expect(() => JSON.parse(line)).not.toThrow());
  });
});
