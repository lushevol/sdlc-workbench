/**
 * Tests for the real context.js functions (no module-level mock of context.js).
 * fs and os are mocked so no real disk I/O occurs.
 */
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';

vi.mock('fs', () => ({
  readFileSync: vi.fn(),
  writeFileSync: vi.fn(),
  renameSync: vi.fn(),
  existsSync: vi.fn(),
  mkdirSync: vi.fn(),
}));

vi.mock('os', () => ({
  homedir: vi.fn(() => '/mock-home'),
}));

import { readFileSync, writeFileSync, renameSync, existsSync, mkdirSync } from 'fs';
import { loadContext, saveContext, getActiveContext, getContextFilePath } from '../src/context.js';

const CONTEXT_FILE = '/mock-home/.sc-node-mcp-context.json';

function sampleStore(overrides = {}) {
  return {
    version: '1',
    activeContext: 'my-service',
    contexts: {
      'my-service': {
        description: 'Platform service',
        workspacePaths: ['/home/user/my-service'],
        ado: {
          project: 'Platform',
          team: 'Platform-Dev',
          defaultBranch: 'develop',
          areaPath: 'Platform\\MyService',
          iterationPath: 'Platform\\Sprint 12',
        },
        repositories: [
          { name: 'my-service', isDefault: true, nexusAppId: 'ITAM__PRD__my-service' },
        ],
        confluence: { defaultSpaceKey: 'PLAT' },
      },
      'other-service': {
        description: 'Another service',
        workspacePaths: ['/home/user/other'],
        ado: { project: 'Other', team: 'Other-Team', defaultBranch: 'main' },
        repositories: [],
        confluence: {},
      },
    },
    ...overrides,
  };
}

beforeEach(() => {
  vi.clearAllMocks();
  vi.stubEnv('WORKBENCH_CONNECTOR_WORKSPACE', '');
});
afterEach(() => vi.unstubAllEnvs());

describe('getContextFilePath (real)', () => {
  it('returns path based on homedir', () => {
    expect(getContextFilePath()).toBe(CONTEXT_FILE);
  });

  it('isolates native contexts under the selected workspace root', () => {
    vi.stubEnv('WORKBENCH_CONNECTOR_WORKSPACE', '/workspace/project');
    expect(getContextFilePath()).toBe('/workspace/project/.workbench/connectors/context.json');
  });
});

describe('loadContext (real)', () => {
  it('returns null when file does not exist', () => {
    existsSync.mockReturnValue(false);
    expect(loadContext()).toBeNull();
  });

  it('does not fall back to global context when native context is absent', () => {
    vi.stubEnv('WORKBENCH_CONNECTOR_WORKSPACE', '/workspace/project');
    existsSync.mockReturnValue(false);
    expect(loadContext()).toBeNull();
    expect(existsSync).toHaveBeenCalledExactlyOnceWith('/workspace/project/.workbench/connectors/context.json');
    expect(readFileSync).not.toHaveBeenCalled();
  });

  it('returns null when JSON is malformed', () => {
    existsSync.mockReturnValue(true);
    readFileSync.mockReturnValue('not-valid-json{{{');
    expect(loadContext()).toBeNull();
  });

  it('returns parsed store object on success', () => {
    const store = sampleStore();
    existsSync.mockReturnValue(true);
    readFileSync.mockReturnValue(JSON.stringify(store));
    const result = loadContext();
    expect(result).toEqual(store);
    expect(readFileSync).toHaveBeenCalledWith(CONTEXT_FILE, 'utf8');
  });
});

describe('saveContext (real)', () => {
  it('writes to temp file then renames to final path', () => {
    const store = sampleStore();
    saveContext(store);
    expect(writeFileSync).toHaveBeenCalledWith(
      CONTEXT_FILE + '.tmp',
      JSON.stringify(store, null, 2),
      'utf8'
    );
    expect(renameSync).toHaveBeenCalledWith(CONTEXT_FILE + '.tmp', CONTEXT_FILE);
  });

  it('creates the native context directory before writing', () => {
    vi.stubEnv('WORKBENCH_CONNECTOR_WORKSPACE', '/workspace/project');
    saveContext(sampleStore());
    expect(mkdirSync).toHaveBeenCalledWith('/workspace/project/.workbench/connectors', { recursive: true });
    expect(renameSync).toHaveBeenCalledWith(
      '/workspace/project/.workbench/connectors/context.json.tmp',
      '/workspace/project/.workbench/connectors/context.json'
    );
  });
});

describe('getActiveContext (real)', () => {
  it('returns null when loadContext returns null (no file)', () => {
    existsSync.mockReturnValue(false);
    expect(getActiveContext()).toBeNull();
  });

  it('returns null when contexts is missing from store', () => {
    existsSync.mockReturnValue(true);
    readFileSync.mockReturnValue(JSON.stringify({ version: '1' }));
    expect(getActiveContext()).toBeNull();
  });

  it('auto-detects context by cwd matching workspacePaths', () => {
    const store = sampleStore({ activeContext: 'other-service' });
    existsSync.mockReturnValue(true);
    readFileSync.mockReturnValue(JSON.stringify(store));

    // Spy on process.cwd to return a path matching my-service
    const cwdSpy = vi.spyOn(process, 'cwd').mockReturnValue('/home/user/my-service/subdir');

    const ctx = getActiveContext();
    expect(ctx.ado.project).toBe('Platform');
    cwdSpy.mockRestore();
  });

  it('falls back to activeContext when no cwd match', () => {
    const store = sampleStore({ activeContext: 'my-service' });
    existsSync.mockReturnValue(true);
    readFileSync.mockReturnValue(JSON.stringify(store));

    const cwdSpy = vi.spyOn(process, 'cwd').mockReturnValue('/completely/unrelated/path');

    const ctx = getActiveContext();
    expect(ctx.ado.project).toBe('Platform');
    cwdSpy.mockRestore();
  });

  it('returns null when activeContext name is not in contexts', () => {
    const store = { version: '1', activeContext: 'nonexistent', contexts: {} };
    existsSync.mockReturnValue(true);
    readFileSync.mockReturnValue(JSON.stringify(store));

    const cwdSpy = vi.spyOn(process, 'cwd').mockReturnValue('/unrelated');
    const ctx = getActiveContext();
    expect(ctx).toBeNull();
    cwdSpy.mockRestore();
  });

  it('auto-detection returns null when no workspacePath matches cwd', () => {
    const store = sampleStore({ activeContext: null });
    store.contexts['my-service'].workspacePaths = ['/completely/different'];
    store.contexts['other-service'].workspacePaths = ['/also/different'];
    existsSync.mockReturnValue(true);
    readFileSync.mockReturnValue(JSON.stringify(store));

    const cwdSpy = vi.spyOn(process, 'cwd').mockReturnValue('/unrelated/path');
    const ctx = getActiveContext();
    expect(ctx).toBeNull();
    cwdSpy.mockRestore();
  });
});
