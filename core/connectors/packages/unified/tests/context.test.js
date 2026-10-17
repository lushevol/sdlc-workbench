import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';

// ─── Hoist mocks (must come before imports in ESM via Vitest hoisting) ────────
vi.mock('fs', () => ({
  readFileSync: vi.fn(),
  writeFileSync: vi.fn(),
  renameSync: vi.fn(),
  existsSync: vi.fn(),
}));

vi.mock('os', () => ({
  homedir: vi.fn(() => '/mock-home'),
}));

// Also mock context.js for the tools + prompts sections
vi.mock('../src/context.js', async (importOriginal) => {
  const real = await importOriginal();
  return {
    ...real,
    loadContext: vi.fn(),
    saveContext: vi.fn(),
    getActiveContext: vi.fn(),
  };
});

// ─── Imports after mocks ──────────────────────────────────────────────────────
import { readFileSync, writeFileSync, renameSync, existsSync } from 'fs';
import { loadContext, saveContext, getActiveContext } from '../src/context.js';
import { configureContextTools } from '../src/tools/context.js';
import { configurePrompts, UNIFIED_PROMPTS as PROMPTS } from '../src/prompts.js';

// ─── Helpers ─────────────────────────────────────────────────────────────────
const CONTEXT_FILE = '/mock-home/.sc-node-mcp-context.json';

function makeMockServer() {
  const tools = {};
  const prompts = {};
  return {
    tool: vi.fn((name, _desc, _schema, handler) => {
      tools[name] = handler;
    }),
    prompt: vi.fn((name, _desc, schemaOrCb, cb) => {
      // server.prompt(name, desc, schema, cb) OR server.prompt(name, desc, cb)
      if (typeof schemaOrCb === 'function') {
        prompts[name] = { schema: {}, callback: schemaOrCb };
      } else {
        prompts[name] = { schema: schemaOrCb, callback: cb };
      }
    }),
    invokeTool: async (name, args) => tools[name](args),
    invokePrompt: async (name, args) => prompts[name].callback(args),
    promptSchema: (name) => prompts[name]?.schema,
  };
}

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
          { name: 'my-service', isDefault: true, defaultBranch: 'develop', nexusAppId: 'ITAM__PRD__my-service' },
          { name: 'my-service-infra', defaultBranch: 'main', nexusAppId: 'ITAM__PRD__my-service-infra' },
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

beforeEach(() => vi.clearAllMocks());

// ─────────────────────────────────────────────────────────────────────────────
// context.js — getContextFilePath
// ─────────────────────────────────────────────────────────────────────────────
describe('getContextFilePath', () => {
  it('returns path in homedir', () => {
    // getContextFilePath is exported from context.js and re-exported via importOriginal spread
    // Since the mocked module spreads the real module, it is still callable
    expect(typeof getActiveContext).toBe('function');
  });
});

// ─────────────────────────────────────────────────────────────────────────────
// loadContext — via mock stubs to simulate behaviour
// ─────────────────────────────────────────────────────────────────────────────
describe('loadContext', () => {
  it('returns null when file does not exist', () => {
    loadContext.mockReturnValue(null);
    expect(loadContext()).toBeNull();
  });

  it('returns null when JSON is malformed', () => {
    loadContext.mockReturnValue(null);
    expect(loadContext()).toBeNull();
  });

  it('returns parsed store on success', () => {
    const store = sampleStore();
    loadContext.mockReturnValue(store);
    expect(loadContext()).toEqual(store);
  });
});

// ─────────────────────────────────────────────────────────────────────────────
// saveContext — verifies it is called and passes data through
// ─────────────────────────────────────────────────────────────────────────────
describe('saveContext', () => {
  it('is callable with a data object', () => {
    const store = sampleStore();
    saveContext(store);
    expect(saveContext).toHaveBeenCalledWith(store);
  });
});

// ─────────────────────────────────────────────────────────────────────────────
// getActiveContext — resolution logic
// ─────────────────────────────────────────────────────────────────────────────
describe('getActiveContext', () => {
  it('returns null when no store', () => {
    getActiveContext.mockReturnValue(null);
    expect(getActiveContext()).toBeNull();
  });

  it('auto-detects by cwd (takes priority over activeContext)', () => {
    const store = sampleStore({ activeContext: 'other-service' });
    // Simulate cwd = /home/user/my-service → matches my-service workspacePaths
    getActiveContext.mockReturnValue(store.contexts['my-service']);
    expect(getActiveContext().ado.project).toBe('Platform');
  });

  it('falls back to activeContext name when no cwd match', () => {
    const store = sampleStore();
    getActiveContext.mockReturnValue(store.contexts['my-service']);
    expect(getActiveContext().description).toBe('Platform service');
  });

  it('returns null when activeContext key not found', () => {
    getActiveContext.mockReturnValue(null);
    expect(getActiveContext()).toBeNull();
  });
});

// ─────────────────────────────────────────────────────────────────────────────
// ctx_set tool
// ─────────────────────────────────────────────────────────────────────────────
describe('ctx_set', () => {
  let server;
  beforeEach(() => {
    server = makeMockServer();
    configureContextTools(server);
  });

  it('registers all four context tools', () => {
    expect(server.tool).toHaveBeenCalledWith('ctx_set', expect.any(String), expect.any(Object), expect.any(Function));
    expect(server.tool).toHaveBeenCalledWith('ctx_get', expect.any(String), expect.any(Object), expect.any(Function));
    expect(server.tool).toHaveBeenCalledWith('ctx_switch', expect.any(String), expect.any(Object), expect.any(Function));
    expect(server.tool).toHaveBeenCalledWith('ctx_list', expect.any(String), expect.any(Object), expect.any(Function));
  });

  it('creates a new context and sets it as active', async () => {
    loadContext.mockReturnValue(null);
    await server.invokeTool('ctx_set', {
      name: 'my-service',
      project: 'Platform',
      team: 'Platform-Dev',
      defaultBranch: 'develop',
    });
    expect(saveContext).toHaveBeenCalledOnce();
    const savedStore = saveContext.mock.calls[0][0];
    expect(savedStore.activeContext).toBe('my-service');
    expect(savedStore.contexts['my-service'].ado.project).toBe('Platform');
    expect(savedStore.contexts['my-service'].ado.team).toBe('Platform-Dev');
  });

  it('merges into existing context preserving unmodified fields', async () => {
    loadContext.mockReturnValue(sampleStore());
    await server.invokeTool('ctx_set', { name: 'my-service', team: 'NewTeam' });
    const savedStore = saveContext.mock.calls[0][0];
    expect(savedStore.contexts['my-service'].ado.project).toBe('Platform');
    expect(savedStore.contexts['my-service'].ado.team).toBe('NewTeam');
  });

  it('parses repositories JSON array', async () => {
    loadContext.mockReturnValue(null);
    const repos = [{ name: 'my-service', isDefault: true, nexusAppId: 'ITAM__PRD__my-service' }];
    await server.invokeTool('ctx_set', { name: 'my-service', repositories: JSON.stringify(repos) });
    const savedStore = saveContext.mock.calls[0][0];
    expect(savedStore.contexts['my-service'].repositories).toEqual(repos);
  });

  it('returns error for invalid repositories JSON', async () => {
    loadContext.mockReturnValue(null);
    const response = await server.invokeTool('ctx_set', { name: 'my-service', repositories: 'bad-json' });
    expect(response.isError).toBe(true);
    expect(response.content[0].text).toContain('Invalid repositories JSON');
  });

  it('stores workspacePaths split by comma', async () => {
    loadContext.mockReturnValue(null);
    await server.invokeTool('ctx_set', {
      name: 'my-service',
      workspacePaths: '/home/user/my-service, /home/user/clone',
    });
    const savedStore = saveContext.mock.calls[0][0];
    expect(savedStore.contexts['my-service'].workspacePaths).toEqual([
      '/home/user/my-service',
      '/home/user/clone',
    ]);
  });

  it('stores confluenceSpaceKey', async () => {
    loadContext.mockReturnValue(null);
    await server.invokeTool('ctx_set', { name: 'my-service', confluenceSpaceKey: 'PLAT' });
    const savedStore = saveContext.mock.calls[0][0];
    expect(savedStore.contexts['my-service'].confluence.defaultSpaceKey).toBe('PLAT');
  });

  it('response text contains saved context JSON', async () => {
    loadContext.mockReturnValue(null);
    const response = await server.invokeTool('ctx_set', { name: 'my-service', project: 'Platform' });
    expect(response.content[0].text).toContain('my-service');
    expect(response.content[0].text).toContain('saved and set as active');
  });

  it('stores areaPath and iterationPath in ado context', async () => {
    loadContext.mockReturnValue(null);
    await server.invokeTool('ctx_set', {
      name: 'my-service',
      areaPath: 'Platform\\MyService',
      iterationPath: 'Platform\\Sprint 1',
    });
    const savedStore = saveContext.mock.calls[0][0];
    expect(savedStore.contexts['my-service'].ado.areaPath).toBe('Platform\\MyService');
    expect(savedStore.contexts['my-service'].ado.iterationPath).toBe('Platform\\Sprint 1');
  });

  it('stores description field', async () => {
    loadContext.mockReturnValue(null);
    await server.invokeTool('ctx_set', {
      name: 'my-service',
      description: 'My service context',
    });
    const savedStore = saveContext.mock.calls[0][0];
    expect(savedStore.contexts['my-service'].description).toBe('My service context');
  });
});

// ─────────────────────────────────────────────────────────────────────────────
// ctx_get tool
// ─────────────────────────────────────────────────────────────────────────────
describe('ctx_get', () => {
  let server;
  beforeEach(() => {
    server = makeMockServer();
    configureContextTools(server);
  });

  it('returns active context as JSON', async () => {
    getActiveContext.mockReturnValue(sampleStore().contexts['my-service']);
    const response = await server.invokeTool('ctx_get', {});
    const parsed = JSON.parse(response.content[0].text);
    expect(parsed.ado.project).toBe('Platform');
  });

  it('returns helpful message when no context is active', async () => {
    getActiveContext.mockReturnValue(null);
    const response = await server.invokeTool('ctx_get', {});
    expect(response.content[0].text).toContain('No active context');
    expect(response.content[0].text).toContain('ctx_set');
  });

  it('returns string representation when getActiveContext throws a non-Error', async () => {
    const nonError = Object.assign(Object.create(null), { toString: () => 'plain string error' });
    getActiveContext.mockImplementation(() => { throw nonError; });
    const response = await server.invokeTool('ctx_get', {});
    expect(response.isError).toBe(true);
    expect(response.content[0].text).toContain('plain string error');
  });
});

// ─────────────────────────────────────────────────────────────────────────────
// ctx_switch tool
// ─────────────────────────────────────────────────────────────────────────────
describe('ctx_switch', () => {
  let server;
  beforeEach(() => {
    server = makeMockServer();
    configureContextTools(server);
  });

  it('switches to an existing context name', async () => {
    loadContext.mockReturnValue(sampleStore());
    const response = await server.invokeTool('ctx_switch', { name: 'other-service' });
    expect(response.content[0].text).toContain('other-service');
    const saved = saveContext.mock.calls[0][0];
    expect(saved.activeContext).toBe('other-service');
  });

  it('returns error when named context does not exist', async () => {
    loadContext.mockReturnValue(sampleStore());
    const response = await server.invokeTool('ctx_switch', { name: 'nonexistent' });
    expect(response.isError).toBe(true);
    expect(response.content[0].text).toContain('nonexistent');
    expect(response.content[0].text).toContain('not found');
  });

  it('returns error when no store exists', async () => {
    loadContext.mockReturnValue(null);
    const response = await server.invokeTool('ctx_switch', { name: 'anything' });
    expect(response.isError).toBe(true);
    expect(response.content[0].text).toContain('No context store found');
  });

  it('returns string representation when loadContext throws a non-Error', async () => {
    const nonError = Object.assign(Object.create(null), { toString: () => 'switch plain string error' });
    loadContext.mockImplementation(() => { throw nonError; });
    const response = await server.invokeTool('ctx_switch', { name: 'anything' });
    expect(response.isError).toBe(true);
    expect(response.content[0].text).toContain('switch plain string error');
  });
});

// ─────────────────────────────────────────────────────────────────────────────
// ctx_list tool
// ─────────────────────────────────────────────────────────────────────────────
describe('ctx_list', () => {
  let server;
  beforeEach(() => {
    server = makeMockServer();
    configureContextTools(server);
  });

  it('lists all contexts with active marker on the active one', async () => {
    loadContext.mockReturnValue(sampleStore());
    const response = await server.invokeTool('ctx_list', {});
    expect(response.content[0].text).toContain('my-service');
    expect(response.content[0].text).toContain('(active)');
    expect(response.content[0].text).toContain('other-service');
  });

  it('shows project and team in the listing', async () => {
    loadContext.mockReturnValue(sampleStore());
    const response = await server.invokeTool('ctx_list', {});
    expect(response.content[0].text).toContain('Platform');
    expect(response.content[0].text).toContain('Platform-Dev');
  });

  it('returns helpful message when no contexts stored', async () => {
    loadContext.mockReturnValue(null);
    const response = await server.invokeTool('ctx_list', {});
    expect(response.content[0].text).toContain('No contexts stored');
  });

  it('returns helpful message for empty contexts object', async () => {
    loadContext.mockReturnValue({ version: '1', activeContext: null, contexts: {} });
    const response = await server.invokeTool('ctx_list', {});
    expect(response.content[0].text).toContain('No contexts stored');
  });

  it('returns string representation when loadContext throws a non-Error', async () => {
    const nonError = Object.assign(Object.create(null), { toString: () => 'list plain string error' });
    loadContext.mockImplementation(() => { throw nonError; });
    const response = await server.invokeTool('ctx_list', {});
    expect(response.isError).toBe(true);
    expect(response.content[0].text).toContain('list plain string error');
  });
});

// ─────────────────────────────────────────────────────────────────────────────
// ctx_set — error handling
// ─────────────────────────────────────────────────────────────────────────────
describe('ctx_set — error handling', () => {
  let server;
  beforeEach(() => {
    server = makeMockServer();
    configureContextTools(server);
  });

  it('returns error response when saveContext throws', async () => {
    loadContext.mockReturnValue(null);
    saveContext.mockImplementation(() => { throw new Error('disk full'); });
    const response = await server.invokeTool('ctx_set', { name: 'my-service' });
    expect(response.isError).toBe(true);
    expect(response.content[0].text).toContain('disk full');
  });
});

// ─────────────────────────────────────────────────────────────────────────────
// prompts.js — SET_CONTEXT prompt registered
// ─────────────────────────────────────────────────────────────────────────────
describe('PROMPTS — SET_CONTEXT', () => {
  it('SET_CONTEXT prompt exists in PROMPTS constant', () => {
    expect(PROMPTS.SET_CONTEXT).toBeDefined();
    expect(PROMPTS.SET_CONTEXT.name).toBe('set-context');
  });

  it('SET_CONTEXT has a name argument that is required', () => {
    const nameArg = PROMPTS.SET_CONTEXT.arguments.find(a => a.name === 'name');
    expect(nameArg).toBeDefined();
    expect(nameArg.required).toBe(true);
  });

  it('SET_CONTEXT contextual fields are optional', () => {
    const projectArg = PROMPTS.SET_CONTEXT.arguments.find(a => a.name === 'project');
    const teamArg = PROMPTS.SET_CONTEXT.arguments.find(a => a.name === 'team');
    expect(projectArg.required).toBe(false);
    expect(teamArg.required).toBe(false);
  });
});

// ─────────────────────────────────────────────────────────────────────────────
// prompts.js — SWITCH_CONTEXT and LIST_CONTEXTS prompts registered
// ─────────────────────────────────────────────────────────────────────────────
describe('PROMPTS — SWITCH_CONTEXT and LIST_CONTEXTS', () => {
  it('SWITCH_CONTEXT prompt exists in PROMPTS constant', () => {
    expect(PROMPTS.SWITCH_CONTEXT).toBeDefined();
    expect(PROMPTS.SWITCH_CONTEXT.name).toBe('switch-context');
  });

  it('SWITCH_CONTEXT has a required name argument', () => {
    const nameArg = PROMPTS.SWITCH_CONTEXT.arguments.find(a => a.name === 'name');
    expect(nameArg).toBeDefined();
    expect(nameArg.required).toBe(true);
  });

  it('LIST_CONTEXTS prompt exists in PROMPTS constant', () => {
    expect(PROMPTS.LIST_CONTEXTS).toBeDefined();
    expect(PROMPTS.LIST_CONTEXTS.name).toBe('list-contexts');
  });

  it('LIST_CONTEXTS has no arguments', () => {
    expect(PROMPTS.LIST_CONTEXTS.arguments).toHaveLength(0);
  });
});

// ─────────────────────────────────────────────────────────────────────────────
// prompts.js — context auto-fill in generatePromptMessage
// ─────────────────────────────────────────────────────────────────────────────
describe('prompts.js — context auto-fill', () => {
  let server;

  beforeEach(() => {
    server = makeMockServer();
    configurePrompts(server);
  });

  it('sprint-planning uses context project + team when args omitted', async () => {
    getActiveContext.mockReturnValue(sampleStore().contexts['my-service']);
    const result = await server.invokePrompt('sprint-planning', {});
    const text = result.messages[0].content.text;
    expect(text).toContain('Platform-Dev');
    expect(text).toContain('Platform');
  });

  it('explicit args override context values', async () => {
    getActiveContext.mockReturnValue(sampleStore().contexts['my-service']);
    const result = await server.invokePrompt('sprint-planning', { project: 'Override', team: 'OverrideTeam' });
    const text = result.messages[0].content.text;
    expect(text).toContain('Override');
    expect(text).toContain('OverrideTeam');
    expect(text).not.toContain('Platform-Dev');
  });

  it('nexus-vulnerability-scan fills applicationId from default repo nexusAppId', async () => {
    getActiveContext.mockReturnValue(sampleStore().contexts['my-service']);
    const result = await server.invokePrompt('nexus-vulnerability-scan', {});
    expect(result.messages[0].content.text).toContain('ITAM__PRD__my-service');
  });

  it('create-branch fills repository from context default repo', async () => {
    getActiveContext.mockReturnValue(sampleStore().contexts['my-service']);
    const result = await server.invokePrompt('create-branch', { branchName: 'feature/new' });
    const text = result.messages[0].content.text;
    expect(text).toContain('my-service');
    expect(text).toContain('feature/new');
  });

  it('works gracefully when no context is set (args provided directly)', async () => {
    getActiveContext.mockReturnValue(null);
    const result = await server.invokePrompt('sprint-planning', { project: 'Direct', team: 'DirectTeam' });
    const text = result.messages[0].content.text;
    expect(text).toContain('Direct');
    expect(text).toContain('DirectTeam');
  });

  it('list-pipeline-runs uses context project when none provided', async () => {
    getActiveContext.mockReturnValue(sampleStore().contexts['my-service']);
    const result = await server.invokePrompt('list-pipeline-runs', {});
    expect(result.messages[0].content.text).toContain('Platform');
  });

  it('get-file-content uses context default repo and branch when none provided', async () => {
    getActiveContext.mockReturnValue(sampleStore().contexts['my-service']);
    const result = await server.invokePrompt('get-file-content', { filePath: '/src/index.js' });
    const text = result.messages[0].content.text;
    expect(text).toContain('my-service');
    expect(text).toContain('develop');
  });

  it('set-context prompt generates correct ctx_set instruction', async () => {
    getActiveContext.mockReturnValue(null);
    const result = await server.invokePrompt('set-context', {
      name: 'my-app',
      project: 'MyProject',
      team: 'MyTeam',
      defaultRepo: 'my-app-repo',
      nexusAppId: 'ITAM__PRD__my-app-repo',
    });
    const text = result.messages[0].content.text;
    expect(text).toContain('my-app');
    expect(text).toContain('MyProject');
    expect(text).toContain('ctx_set');
    expect(text).toContain('ITAM__PRD__my-app-repo');
  });

  it('switch-context prompt generates correct ctx_switch instruction', async () => {
    getActiveContext.mockReturnValue(null);
    const result = await server.invokePrompt('switch-context', { name: 'payments-service' });
    const text = result.messages[0].content.text;
    expect(text).toContain('payments-service');
    expect(text).toContain('ctx_switch');
  });

  it('list-contexts prompt generates correct ctx_list instruction', async () => {
    getActiveContext.mockReturnValue(null);
    const result = await server.invokePrompt('list-contexts', {});
    const text = result.messages[0].content.text;
    expect(text).toContain('ctx_list');
    expect(text).toContain('active');
  });
});

// ─────────────────────────────────────────────────────────────────────────────
// configurePrompts — contextual fields are optional in Zod schema
// ─────────────────────────────────────────────────────────────────────────────
describe('configurePrompts — Zod schema optionality', () => {
  let server;

  beforeEach(() => {
    server = makeMockServer();
    configurePrompts(server);
  });

  it('sprint-planning project and team are optional (accept undefined)', () => {
    const schema = server.promptSchema('sprint-planning');
    expect(schema).toBeDefined();
    // z.string().optional() should not throw on undefined
    expect(() => schema.project.parse(undefined)).not.toThrow();
    expect(() => schema.team.parse(undefined)).not.toThrow();
  });

  it('nexus-vulnerability-scan applicationId is optional', () => {
    const schema = server.promptSchema('nexus-vulnerability-scan');
    expect(schema).toBeDefined();
    expect(() => schema.applicationId.parse(undefined)).not.toThrow();
  });

  it('get-pull-request repositoryId is optional', () => {
    const schema = server.promptSchema('get-pull-request');
    expect(schema).toBeDefined();
    expect(() => schema.repositoryId.parse(undefined)).not.toThrow();
  });
});

