import { describe, it, expect, vi, beforeEach } from 'vitest';

// Mock dependencies before importing
vi.mock('@sc-node-mcp/core', () => ({
  createMcpServer: vi.fn(() => ({
    prompt: vi.fn(),
    tool: vi.fn(),
    resource: vi.fn()
  })),
  startMcpServer: vi.fn(),
      detectProxy: vi.fn().mockResolvedValue(''),
      detectProxyFor: vi.fn().mockResolvedValue(''),
      applyProxy: vi.fn(),
  recordStartupTelemetry: vi.fn().mockResolvedValue(undefined),
  getConfig: vi.fn(() => ({
    AZURE_DEVOPS_ORG_URL: 'https://dev.azure.com/test',
    AZURE_DEVOPS_PAT: 'test-pat',
    confluenceConfig: {
      baseUrl: '',
      username: '',
      apiToken: ''
    }
  }))
}));

vi.mock('@sc-node-mcp/ado', () => ({
  getADOConnection: vi.fn(),
  configureAdoTools: vi.fn()
}));

vi.mock('@sc-node-mcp/ado-upload-app', () => ({
  configureUploadTools: vi.fn(),
  configureUiResource: vi.fn()
}));

vi.mock('@sc-node-mcp/confluence', () => ({
  configureConfluenceTools: vi.fn()
}));

vi.mock('@sc-node-mcp/scwiki', () => ({
  configureScwikiTools: vi.fn()
}));

vi.mock('@sc-node-mcp/messaging', () => ({
  getPythonBridge: vi.fn(),
  configureEmailTools: vi.fn(),
  getTeamsNativeBridge: vi.fn(),
  configureTeamsTools: vi.fn()
}));

vi.mock('@sc-node-mcp/nexus', () => ({
  getNexusConnection: vi.fn(),
  configureNexusTools: vi.fn()
}));

vi.mock('../src/prompts.js', () => ({
  configurePrompts: vi.fn()
}));

vi.mock('../src/tools/context.js', () => ({
  configureContextTools: vi.fn()
}));

vi.mock('../src/context.js', () => ({
  getActiveContext: vi.fn(() => null),
  loadContext: vi.fn(() => null),
  saveContext: vi.fn()
}));

describe('Unified Server Index', () => {
  it('should import without errors', async () => {
    // Await the dynamic import to ensure errors are caught by the test runner
    await expect(import('../src/index.js')).resolves.toBeDefined();
  });

  it('should have all required dependencies mocked', () => {
    const coreModule = require('@sc-node-mcp/core');
    const adoModule = require('@sc-node-mcp/ado');
    const confluenceModule = require('@sc-node-mcp/confluence');

    expect(coreModule.createMcpServer).toBeDefined();
    expect(coreModule.startMcpServer).toBeDefined();
    expect(coreModule.getConfig).toBeDefined();
    expect(adoModule.getADOConnection).toBeDefined();
    expect(adoModule.configureAdoTools).toBeDefined();
    expect(confluenceModule.configureConfluenceTools).toBeDefined();
  });
});

describe('Unified Server Index – Confluence enabled', () => {
  beforeEach(() => {
    vi.resetModules();
  });

  it('should configure Confluence tools when baseUrl and token are present', async () => {
    const mockConfigureConfluenceTools = vi.fn();

    vi.doMock('@sc-node-mcp/core', () => ({
      createMcpServer: vi.fn(() => ({ prompt: vi.fn(), tool: vi.fn(), resource: vi.fn() })),
      startMcpServer: vi.fn(),
      detectProxy: vi.fn().mockResolvedValue(''),
      detectProxyFor: vi.fn().mockResolvedValue(''),
      applyProxy: vi.fn(),
      recordStartupTelemetry: vi.fn().mockResolvedValue(undefined),
      getConfig: vi.fn(() => ({
        codeReviewGuideFile: undefined,
        confluenceConfig: { baseUrl: 'https://confluence.example.com', token: 'my-token' },
        nexusConfig: { userCode: '', passCode: '' }
      }))
    }));
    vi.doMock('@sc-node-mcp/ado', () => ({ getADOConnection: vi.fn(), configureAdoTools: vi.fn() }));
    vi.doMock('@sc-node-mcp/ado-upload-app', () => ({ configureUploadTools: vi.fn(), configureUiResource: vi.fn() }));
    vi.doMock('@sc-node-mcp/confluence', () => ({ configureConfluenceTools: mockConfigureConfluenceTools }));
    vi.doMock('@sc-node-mcp/messaging', () => ({
      getPythonBridge: vi.fn(),
      configureEmailTools: vi.fn(),
      getTeamsNativeBridge: vi.fn(),
      configureTeamsTools: vi.fn()
    }));
    vi.doMock('@sc-node-mcp/nexus', () => ({ getNexusConnection: vi.fn(), configureNexusTools: vi.fn() }));
    vi.doMock('../src/prompts.js', () => ({ configurePrompts: vi.fn() }));
    vi.doMock('../src/tools/context.js', () => ({ configureContextTools: vi.fn() }));
    vi.doMock('../src/context.js', () => ({ getActiveContext: vi.fn(() => null), loadContext: vi.fn(() => null), saveContext: vi.fn() }));

    await import('../src/index.js');

    expect(mockConfigureConfluenceTools).toHaveBeenCalledOnce();
  });
});

describe('Unified Server Index – Confluence error', () => {
  beforeEach(() => {
    vi.resetModules();
  });

  it('should skip Confluence tools gracefully when confluenceConfig throws', async () => {
    vi.doMock('@sc-node-mcp/core', () => ({
      createMcpServer: vi.fn(() => ({ prompt: vi.fn(), tool: vi.fn(), resource: vi.fn() })),
      startMcpServer: vi.fn(),
      detectProxy: vi.fn().mockResolvedValue(''),
      detectProxyFor: vi.fn().mockResolvedValue(''),
      applyProxy: vi.fn(),
      recordStartupTelemetry: vi.fn().mockResolvedValue(undefined),
      getConfig: vi.fn(() => ({
        codeReviewGuideFile: undefined,
        get confluenceConfig() { throw new Error('Confluence config error'); },
        nexusConfig: { userCode: '', passCode: '' }
      }))
    }));
    vi.doMock('@sc-node-mcp/ado', () => ({ getADOConnection: vi.fn(), configureAdoTools: vi.fn() }));
    vi.doMock('@sc-node-mcp/ado-upload-app', () => ({ configureUploadTools: vi.fn(), configureUiResource: vi.fn() }));
    vi.doMock('@sc-node-mcp/confluence', () => ({ configureConfluenceTools: vi.fn() }));
    vi.doMock('@sc-node-mcp/messaging', () => ({
      getPythonBridge: vi.fn(),
      configureEmailTools: vi.fn(),
      getTeamsNativeBridge: vi.fn(),
      configureTeamsTools: vi.fn()
    }));
    vi.doMock('@sc-node-mcp/nexus', () => ({ getNexusConnection: vi.fn(), configureNexusTools: vi.fn() }));
    vi.doMock('../src/prompts.js', () => ({ configurePrompts: vi.fn() }));
    vi.doMock('../src/tools/context.js', () => ({ configureContextTools: vi.fn() }));
    vi.doMock('../src/context.js', () => ({ getActiveContext: vi.fn(() => null), loadContext: vi.fn(() => null), saveContext: vi.fn() }));

    // Should not throw – error is caught internally
    await expect(import('../src/index.js')).resolves.toBeDefined();
  });
});

describe('Unified Server Index – SC Wiki enabled', () => {
  beforeEach(() => {
    vi.resetModules();
  });

  it('should configure SC Wiki tools when baseUrl and token are present', async () => {
    const mockConfigureScwikiTools = vi.fn();

    vi.doMock('@sc-node-mcp/core', () => ({
      createMcpServer: vi.fn(() => ({ prompt: vi.fn(), tool: vi.fn(), resource: vi.fn() })),
      startMcpServer: vi.fn(),
      detectProxy: vi.fn().mockResolvedValue(''),
      detectProxyFor: vi.fn().mockResolvedValue(''),
      applyProxy: vi.fn(),
      recordStartupTelemetry: vi.fn().mockResolvedValue(undefined),
      getConfig: vi.fn(() => ({
        codeReviewGuideFile: undefined,
        confluenceConfig: { baseUrl: '', token: '' },
        scwikiConfig: { baseUrl: 'https://scwiki.example.com', token: 'my-token' },
        nexusConfig: { userCode: '', passCode: '' }
      }))
    }));
    vi.doMock('@sc-node-mcp/ado', () => ({ getADOConnection: vi.fn(), configureAdoTools: vi.fn() }));
    vi.doMock('@sc-node-mcp/ado-upload-app', () => ({ configureUploadTools: vi.fn(), configureUiResource: vi.fn() }));
    vi.doMock('@sc-node-mcp/confluence', () => ({ configureConfluenceTools: vi.fn() }));
    vi.doMock('@sc-node-mcp/scwiki', () => ({ configureScwikiTools: mockConfigureScwikiTools }));
    vi.doMock('@sc-node-mcp/messaging', () => ({
      getPythonBridge: vi.fn(),
      configureEmailTools: vi.fn(),
      getTeamsNativeBridge: vi.fn(),
      configureTeamsTools: vi.fn()
    }));
    vi.doMock('@sc-node-mcp/nexus', () => ({ getNexusConnection: vi.fn(), configureNexusTools: vi.fn() }));
    vi.doMock('../src/prompts.js', () => ({ configurePrompts: vi.fn() }));
    vi.doMock('../src/tools/context.js', () => ({ configureContextTools: vi.fn() }));
    vi.doMock('../src/context.js', () => ({ getActiveContext: vi.fn(() => null), loadContext: vi.fn(() => null), saveContext: vi.fn() }));

    await import('../src/index.js');

    expect(mockConfigureScwikiTools).toHaveBeenCalledOnce();
  });
});

describe('Unified Server Index – SC Wiki config defined but no credentials', () => {
  beforeEach(() => {
    vi.resetModules();
  });

  it('should skip SC Wiki tools when token is empty', async () => {
    const mockConfigureScwikiTools = vi.fn();

    vi.doMock('@sc-node-mcp/core', () => ({
      createMcpServer: vi.fn(() => ({ prompt: vi.fn(), tool: vi.fn(), resource: vi.fn() })),
      startMcpServer: vi.fn(),
      detectProxy: vi.fn().mockResolvedValue(''),
      detectProxyFor: vi.fn().mockResolvedValue(''),
      applyProxy: vi.fn(),
      recordStartupTelemetry: vi.fn().mockResolvedValue(undefined),
      getConfig: vi.fn(() => ({
        codeReviewGuideFile: undefined,
        confluenceConfig: { baseUrl: '', token: '' },
        scwikiConfig: { baseUrl: 'https://scwiki.example.com', token: '' },
        nexusConfig: { userCode: '', passCode: '' }
      }))
    }));
    vi.doMock('@sc-node-mcp/ado', () => ({ getADOConnection: vi.fn(), configureAdoTools: vi.fn() }));
    vi.doMock('@sc-node-mcp/ado-upload-app', () => ({ configureUploadTools: vi.fn(), configureUiResource: vi.fn() }));
    vi.doMock('@sc-node-mcp/confluence', () => ({ configureConfluenceTools: vi.fn() }));
    vi.doMock('@sc-node-mcp/scwiki', () => ({ configureScwikiTools: mockConfigureScwikiTools }));
    vi.doMock('@sc-node-mcp/messaging', () => ({
      getPythonBridge: vi.fn(),
      configureEmailTools: vi.fn(),
      getTeamsNativeBridge: vi.fn(),
      configureTeamsTools: vi.fn()
    }));
    vi.doMock('@sc-node-mcp/nexus', () => ({ getNexusConnection: vi.fn(), configureNexusTools: vi.fn() }));
    vi.doMock('../src/prompts.js', () => ({ configurePrompts: vi.fn() }));
    vi.doMock('../src/tools/context.js', () => ({ configureContextTools: vi.fn() }));
    vi.doMock('../src/context.js', () => ({ getActiveContext: vi.fn(() => null), loadContext: vi.fn(() => null), saveContext: vi.fn() }));

    await import('../src/index.js');

    expect(mockConfigureScwikiTools).not.toHaveBeenCalled();
  });
});

describe('Unified Server Index – Nexus enabled', () => {
  beforeEach(() => {
    vi.resetModules();
  });

  it('should configure Nexus tools and invoke nexusConnectionProvider when credentials are present', async () => {
    const mockGetNexusConnection = vi.fn(() => ({}));
    const mockConfigureNexusTools = vi.fn((server, provider) => {
      // Call the provider to cover the nexusConnectionProvider arrow function body
      provider();
    });

    vi.doMock('@sc-node-mcp/core', () => ({
      createMcpServer: vi.fn(() => ({ prompt: vi.fn(), tool: vi.fn(), resource: vi.fn() })),
      startMcpServer: vi.fn(),
      detectProxy: vi.fn().mockResolvedValue(''),
      detectProxyFor: vi.fn().mockResolvedValue(''),
      applyProxy: vi.fn(),
      recordStartupTelemetry: vi.fn().mockResolvedValue(undefined),
      getConfig: vi.fn(() => ({
        codeReviewGuideFile: undefined,
        confluenceConfig: { baseUrl: '', token: '' },
        nexusConfig: { userCode: 'user123', passCode: 'pass456' }
      }))
    }));
    vi.doMock('@sc-node-mcp/ado', () => ({ getADOConnection: vi.fn(), configureAdoTools: vi.fn() }));
    vi.doMock('@sc-node-mcp/ado-upload-app', () => ({ configureUploadTools: vi.fn(), configureUiResource: vi.fn() }));
    vi.doMock('@sc-node-mcp/confluence', () => ({ configureConfluenceTools: vi.fn() }));
    vi.doMock('@sc-node-mcp/messaging', () => ({
      getPythonBridge: vi.fn(),
      configureEmailTools: vi.fn(),
      getTeamsNativeBridge: vi.fn(),
      configureTeamsTools: vi.fn()
    }));
    vi.doMock('@sc-node-mcp/nexus', () => ({
      getNexusConnection: mockGetNexusConnection,
      configureNexusTools: mockConfigureNexusTools
    }));
    vi.doMock('../src/prompts.js', () => ({ configurePrompts: vi.fn() }));
    vi.doMock('../src/tools/context.js', () => ({ configureContextTools: vi.fn() }));
    vi.doMock('../src/context.js', () => ({ getActiveContext: vi.fn(() => null), loadContext: vi.fn(() => null), saveContext: vi.fn() }));

    await import('../src/index.js');

    expect(mockConfigureNexusTools).toHaveBeenCalledOnce();
    expect(mockGetNexusConnection).toHaveBeenCalledWith('user123', 'pass456');
  });
});

describe('Unified Server Index – Nexus config defined but no credentials', () => {
  beforeEach(() => {
    vi.resetModules();
  });

  it('should skip Nexus tools when userCode and passCode are empty', async () => {
    const mockConfigureNexusTools = vi.fn();

    vi.doMock('@sc-node-mcp/core', () => ({
      createMcpServer: vi.fn(() => ({ prompt: vi.fn(), tool: vi.fn(), resource: vi.fn() })),
      startMcpServer: vi.fn(),
      detectProxy: vi.fn().mockResolvedValue(''),
      detectProxyFor: vi.fn().mockResolvedValue(''),
      applyProxy: vi.fn(),
      recordStartupTelemetry: vi.fn().mockResolvedValue(undefined),
      getConfig: vi.fn(() => ({
        codeReviewGuideFile: undefined,
        confluenceConfig: { baseUrl: '', token: '' },
        nexusConfig: { userCode: '', passCode: '' }
      }))
    }));
    vi.doMock('@sc-node-mcp/ado', () => ({ getADOConnection: vi.fn(), configureAdoTools: vi.fn() }));
    vi.doMock('@sc-node-mcp/ado-upload-app', () => ({ configureUploadTools: vi.fn(), configureUiResource: vi.fn() }));
    vi.doMock('@sc-node-mcp/confluence', () => ({ configureConfluenceTools: vi.fn() }));
    vi.doMock('@sc-node-mcp/messaging', () => ({
      getPythonBridge: vi.fn(),
      configureEmailTools: vi.fn(),
      getTeamsNativeBridge: vi.fn(),
      configureTeamsTools: vi.fn()
    }));
    vi.doMock('@sc-node-mcp/nexus', () => ({
      getNexusConnection: vi.fn(),
      configureNexusTools: mockConfigureNexusTools
    }));
    vi.doMock('../src/prompts.js', () => ({ configurePrompts: vi.fn() }));
    vi.doMock('../src/tools/context.js', () => ({ configureContextTools: vi.fn() }));
    vi.doMock('../src/context.js', () => ({ getActiveContext: vi.fn(() => null), loadContext: vi.fn(() => null), saveContext: vi.fn() }));

    await import('../src/index.js');

    expect(mockConfigureNexusTools).not.toHaveBeenCalled();
  });
});

describe('Unified Server Index – Nexus config error', () => {
  beforeEach(() => {
    vi.resetModules();
  });

  it('should skip Nexus tools gracefully when nexusConfig accessor throws', async () => {
    vi.doMock('@sc-node-mcp/core', () => ({
      createMcpServer: vi.fn(() => ({ prompt: vi.fn(), tool: vi.fn(), resource: vi.fn() })),
      startMcpServer: vi.fn(),
      detectProxy: vi.fn().mockResolvedValue(''),
      detectProxyFor: vi.fn().mockResolvedValue(''),
      applyProxy: vi.fn(),
      recordStartupTelemetry: vi.fn().mockResolvedValue(undefined),
      getConfig: vi.fn(() => ({
        codeReviewGuideFile: undefined,
        confluenceConfig: { baseUrl: '', token: '' },
        get nexusConfig() { throw new Error('Nexus config error'); }
      }))
    }));
    vi.doMock('@sc-node-mcp/ado', () => ({ getADOConnection: vi.fn(), configureAdoTools: vi.fn() }));
    vi.doMock('@sc-node-mcp/ado-upload-app', () => ({ configureUploadTools: vi.fn(), configureUiResource: vi.fn() }));
    vi.doMock('@sc-node-mcp/confluence', () => ({ configureConfluenceTools: vi.fn() }));
    vi.doMock('@sc-node-mcp/messaging', () => ({
      getPythonBridge: vi.fn(),
      configureEmailTools: vi.fn(),
      getTeamsNativeBridge: vi.fn(),
      configureTeamsTools: vi.fn()
    }));
    vi.doMock('@sc-node-mcp/nexus', () => ({ getNexusConnection: vi.fn(), configureNexusTools: vi.fn() }));
    vi.doMock('../src/prompts.js', () => ({ configurePrompts: vi.fn() }));
    vi.doMock('../src/tools/context.js', () => ({ configureContextTools: vi.fn() }));
    vi.doMock('../src/context.js', () => ({ getActiveContext: vi.fn(() => null), loadContext: vi.fn(() => null), saveContext: vi.fn() }));

    // Should not throw – error is caught internally
    await expect(import('../src/index.js')).resolves.toBeDefined();
  });
});

describe('Unified Server Index – outer catch path', () => {
  beforeEach(() => {
    vi.resetModules();
  });

  it('should call process.exit(1) when startMcpServer rejects', async () => {
    const mockExit = vi.spyOn(process, 'exit').mockImplementation(() => {});

    vi.doMock('@sc-node-mcp/core', () => ({
      createMcpServer: vi.fn(() => ({ prompt: vi.fn(), tool: vi.fn(), resource: vi.fn() })),
      startMcpServer: vi.fn().mockRejectedValue(new Error('Server failed to start')),
      detectProxy: vi.fn().mockResolvedValue(''),
      detectProxyFor: vi.fn().mockResolvedValue(''),
      applyProxy: vi.fn(),
      recordStartupTelemetry: vi.fn().mockResolvedValue(undefined),
      getConfig: vi.fn(() => ({
        codeReviewGuideFile: undefined,
        confluenceConfig: { baseUrl: '', token: '' },
        nexusConfig: { userCode: '', passCode: '' }
      }))
    }));
    vi.doMock('@sc-node-mcp/ado', () => ({ getADOConnection: vi.fn(), configureAdoTools: vi.fn() }));
    vi.doMock('@sc-node-mcp/ado-upload-app', () => ({ configureUploadTools: vi.fn(), configureUiResource: vi.fn() }));
    vi.doMock('@sc-node-mcp/confluence', () => ({ configureConfluenceTools: vi.fn() }));
    vi.doMock('@sc-node-mcp/messaging', () => ({
      getPythonBridge: vi.fn(),
      configureEmailTools: vi.fn(),
      getTeamsNativeBridge: vi.fn(),
      configureTeamsTools: vi.fn()
    }));
    vi.doMock('@sc-node-mcp/nexus', () => ({ getNexusConnection: vi.fn(), configureNexusTools: vi.fn() }));
    vi.doMock('../src/prompts.js', () => ({ configurePrompts: vi.fn() }));
    vi.doMock('../src/tools/context.js', () => ({ configureContextTools: vi.fn() }));
    vi.doMock('../src/context.js', () => ({ getActiveContext: vi.fn(() => null), loadContext: vi.fn(() => null), saveContext: vi.fn() }));

    await import('../src/index.js');
    // Allow the async main() rejection to propagate through the .catch() handler
    await new Promise(resolve => setTimeout(resolve, 50));

    expect(mockExit).toHaveBeenCalledWith(1);
    mockExit.mockRestore();
  });
});

describe('Unified Server Index – SonarQube enabled', () => {
  beforeEach(() => {
    vi.resetModules();
  });

  it('should configure SonarQube tools and invoke sonarConnectionProvider when token is present', async () => {
    const mockGetSonarConnection = vi.fn(() => ({}));
    const mockConfigureSonarTools = vi.fn((server, provider) => {
      provider(); // invoke the arrow function to cover its body
    });

    vi.doMock('@sc-node-mcp/core', () => ({
      createMcpServer: vi.fn(() => ({ prompt: vi.fn(), tool: vi.fn(), resource: vi.fn() })),
      startMcpServer: vi.fn(),
      detectProxy: vi.fn().mockResolvedValue(''),
      detectProxyFor: vi.fn().mockResolvedValue(''),
      applyProxy: vi.fn(),
      recordStartupTelemetry: vi.fn().mockResolvedValue(undefined),
      getConfig: vi.fn(() => ({
        codeReviewGuideFile: undefined,
        confluenceConfig: { baseUrl: '', token: '' },
        nexusConfig: { userCode: '', passCode: '' },
        sonarConfig: { token: 'sonar-token-abc' }
      }))
    }));
    vi.doMock('@sc-node-mcp/ado', () => ({ getADOConnection: vi.fn(), configureAdoTools: vi.fn() }));
    vi.doMock('@sc-node-mcp/ado-upload-app', () => ({ configureUploadTools: vi.fn(), configureUiResource: vi.fn() }));
    vi.doMock('@sc-node-mcp/confluence', () => ({ configureConfluenceTools: vi.fn() }));
    vi.doMock('@sc-node-mcp/messaging', () => ({
      getPythonBridge: vi.fn(),
      configureEmailTools: vi.fn(),
      getTeamsNativeBridge: vi.fn(),
      configureTeamsTools: vi.fn()
    }));
    vi.doMock('@sc-node-mcp/nexus', () => ({ getNexusConnection: vi.fn(), configureNexusTools: vi.fn() }));
    vi.doMock('@sc-node-mcp/sonar', () => ({
      getSonarConnection: mockGetSonarConnection,
      configureSonarTools: mockConfigureSonarTools
    }));
    vi.doMock('../src/prompts.js', () => ({ configurePrompts: vi.fn() }));
    vi.doMock('../src/tools/context.js', () => ({ configureContextTools: vi.fn() }));
    vi.doMock('../src/context.js', () => ({ getActiveContext: vi.fn(() => null), loadContext: vi.fn(() => null), saveContext: vi.fn() }));

    await import('../src/index.js');

    expect(mockConfigureSonarTools).toHaveBeenCalledOnce();
    expect(mockGetSonarConnection).toHaveBeenCalledWith('sonar-token-abc');
  });
});

describe('Unified Server Index – SonarQube skip (no token)', () => {
  beforeEach(() => {
    vi.resetModules();
  });

  it('should skip SonarQube tools when token is absent', async () => {
    const mockConfigureSonarTools = vi.fn();

    vi.doMock('@sc-node-mcp/core', () => ({
      createMcpServer: vi.fn(() => ({ prompt: vi.fn(), tool: vi.fn(), resource: vi.fn() })),
      startMcpServer: vi.fn(),
      detectProxy: vi.fn().mockResolvedValue(''),
      detectProxyFor: vi.fn().mockResolvedValue(''),
      applyProxy: vi.fn(),
      recordStartupTelemetry: vi.fn().mockResolvedValue(undefined),
      getConfig: vi.fn(() => ({
        codeReviewGuideFile: undefined,
        confluenceConfig: { baseUrl: '', token: '' },
        nexusConfig: { userCode: '', passCode: '' },
        sonarConfig: { token: '' }
      }))
    }));
    vi.doMock('@sc-node-mcp/ado', () => ({ getADOConnection: vi.fn(), configureAdoTools: vi.fn() }));
    vi.doMock('@sc-node-mcp/ado-upload-app', () => ({ configureUploadTools: vi.fn(), configureUiResource: vi.fn() }));
    vi.doMock('@sc-node-mcp/confluence', () => ({ configureConfluenceTools: vi.fn() }));
    vi.doMock('@sc-node-mcp/messaging', () => ({
      getPythonBridge: vi.fn(),
      configureEmailTools: vi.fn(),
      getTeamsNativeBridge: vi.fn(),
      configureTeamsTools: vi.fn()
    }));
    vi.doMock('@sc-node-mcp/nexus', () => ({ getNexusConnection: vi.fn(), configureNexusTools: vi.fn() }));
    vi.doMock('@sc-node-mcp/sonar', () => ({
      getSonarConnection: vi.fn(),
      configureSonarTools: mockConfigureSonarTools
    }));
    vi.doMock('../src/prompts.js', () => ({ configurePrompts: vi.fn() }));
    vi.doMock('../src/tools/context.js', () => ({ configureContextTools: vi.fn() }));
    vi.doMock('../src/context.js', () => ({ getActiveContext: vi.fn(() => null), loadContext: vi.fn(() => null), saveContext: vi.fn() }));

    await import('../src/index.js');

    expect(mockConfigureSonarTools).not.toHaveBeenCalled();
  });
});

describe('Unified Server Index – SonarQube config error', () => {
  beforeEach(() => {
    vi.resetModules();
  });

  it('should skip SonarQube tools gracefully when sonarConfig accessor throws', async () => {
    vi.doMock('@sc-node-mcp/core', () => ({
      createMcpServer: vi.fn(() => ({ prompt: vi.fn(), tool: vi.fn(), resource: vi.fn() })),
      startMcpServer: vi.fn(),
      detectProxy: vi.fn().mockResolvedValue(''),
      detectProxyFor: vi.fn().mockResolvedValue(''),
      applyProxy: vi.fn(),
      recordStartupTelemetry: vi.fn().mockResolvedValue(undefined),
      getConfig: vi.fn(() => ({
        codeReviewGuideFile: undefined,
        confluenceConfig: { baseUrl: '', token: '' },
        nexusConfig: { userCode: '', passCode: '' },
        get sonarConfig() { throw new Error('Sonar config error'); }
      }))
    }));
    vi.doMock('@sc-node-mcp/ado', () => ({ getADOConnection: vi.fn(), configureAdoTools: vi.fn() }));
    vi.doMock('@sc-node-mcp/ado-upload-app', () => ({ configureUploadTools: vi.fn(), configureUiResource: vi.fn() }));
    vi.doMock('@sc-node-mcp/confluence', () => ({ configureConfluenceTools: vi.fn() }));
    vi.doMock('@sc-node-mcp/messaging', () => ({
      getPythonBridge: vi.fn(),
      configureEmailTools: vi.fn(),
      getTeamsNativeBridge: vi.fn(),
      configureTeamsTools: vi.fn()
    }));
    vi.doMock('@sc-node-mcp/nexus', () => ({ getNexusConnection: vi.fn(), configureNexusTools: vi.fn() }));
    vi.doMock('@sc-node-mcp/sonar', () => ({ getSonarConnection: vi.fn(), configureSonarTools: vi.fn() }));
    vi.doMock('../src/prompts.js', () => ({ configurePrompts: vi.fn() }));
    vi.doMock('../src/tools/context.js', () => ({ configureContextTools: vi.fn() }));
    vi.doMock('../src/context.js', () => ({ getActiveContext: vi.fn(() => null), loadContext: vi.fn(() => null), saveContext: vi.fn() }));

    await expect(import('../src/index.js')).resolves.toBeDefined();
  });
});

describe('Unified Server Index – context resource handler', () => {
  beforeEach(() => {
    vi.resetModules();
  });

  it('should invoke resource callback and return JSON when context exists', async () => {
    const mockCtx = { project: 'MyProject', team: 'DevTeam' };
    let resourceCallback;

    vi.doMock('@sc-node-mcp/core', () => ({
      createMcpServer: vi.fn(() => ({
        prompt: vi.fn(),
        tool: vi.fn(),
        resource: vi.fn((_name, _template, _opts, cb) => { resourceCallback = cb; })
      })),
      startMcpServer: vi.fn(),
      detectProxy: vi.fn().mockResolvedValue(''),
      detectProxyFor: vi.fn().mockResolvedValue(''),
      applyProxy: vi.fn(),
      recordStartupTelemetry: vi.fn().mockResolvedValue(undefined),
      getConfig: vi.fn(() => ({
        codeReviewGuideFile: undefined,
        confluenceConfig: { baseUrl: '', token: '' },
        nexusConfig: { userCode: '', passCode: '' },
        sonarConfig: { token: '' }
      }))
    }));
    vi.doMock('@sc-node-mcp/ado', () => ({ getADOConnection: vi.fn(), configureAdoTools: vi.fn() }));
    vi.doMock('@sc-node-mcp/ado-upload-app', () => ({ configureUploadTools: vi.fn(), configureUiResource: vi.fn() }));
    vi.doMock('@sc-node-mcp/confluence', () => ({ configureConfluenceTools: vi.fn() }));
    vi.doMock('@sc-node-mcp/messaging', () => ({
      getPythonBridge: vi.fn(),
      configureEmailTools: vi.fn(),
      getTeamsNativeBridge: vi.fn(),
      configureTeamsTools: vi.fn()
    }));
    vi.doMock('@sc-node-mcp/nexus', () => ({ getNexusConnection: vi.fn(), configureNexusTools: vi.fn() }));
    vi.doMock('@sc-node-mcp/sonar', () => ({ getSonarConnection: vi.fn(), configureSonarTools: vi.fn() }));
    vi.doMock('../src/prompts.js', () => ({ configurePrompts: vi.fn() }));
    vi.doMock('../src/tools/context.js', () => ({ configureContextTools: vi.fn() }));
    vi.doMock('../src/context.js', () => ({
      getActiveContext: vi.fn(() => mockCtx),
      loadContext: vi.fn(() => null),
      saveContext: vi.fn()
    }));

    await import('../src/index.js');

    expect(resourceCallback).toBeDefined();
    const result = await resourceCallback({ href: 'context://active' });
    expect(result.contents[0].text).toContain('MyProject');
    expect(result.contents[0].mimeType).toBe('application/json');
  });

  it('should return No active context message when context is null', async () => {
    let resourceCallback;

    vi.doMock('@sc-node-mcp/core', () => ({
      createMcpServer: vi.fn(() => ({
        prompt: vi.fn(),
        tool: vi.fn(),
        resource: vi.fn((_name, _template, _opts, cb) => { resourceCallback = cb; })
      })),
      startMcpServer: vi.fn(),
      detectProxy: vi.fn().mockResolvedValue(''),
      detectProxyFor: vi.fn().mockResolvedValue(''),
      applyProxy: vi.fn(),
      recordStartupTelemetry: vi.fn().mockResolvedValue(undefined),
      getConfig: vi.fn(() => ({
        codeReviewGuideFile: undefined,
        confluenceConfig: { baseUrl: '', token: '' },
        nexusConfig: { userCode: '', passCode: '' },
        sonarConfig: { token: '' }
      }))
    }));
    vi.doMock('@sc-node-mcp/ado', () => ({ getADOConnection: vi.fn(), configureAdoTools: vi.fn() }));
    vi.doMock('@sc-node-mcp/ado-upload-app', () => ({ configureUploadTools: vi.fn(), configureUiResource: vi.fn() }));
    vi.doMock('@sc-node-mcp/confluence', () => ({ configureConfluenceTools: vi.fn() }));
    vi.doMock('@sc-node-mcp/messaging', () => ({
      getPythonBridge: vi.fn(),
      configureEmailTools: vi.fn(),
      getTeamsNativeBridge: vi.fn(),
      configureTeamsTools: vi.fn()
    }));
    vi.doMock('@sc-node-mcp/nexus', () => ({ getNexusConnection: vi.fn(), configureNexusTools: vi.fn() }));
    vi.doMock('@sc-node-mcp/sonar', () => ({ getSonarConnection: vi.fn(), configureSonarTools: vi.fn() }));
    vi.doMock('../src/prompts.js', () => ({ configurePrompts: vi.fn() }));
    vi.doMock('../src/tools/context.js', () => ({ configureContextTools: vi.fn() }));
    vi.doMock('../src/context.js', () => ({
      getActiveContext: vi.fn(() => null),
      loadContext: vi.fn(() => null),
      saveContext: vi.fn()
    }));

    await import('../src/index.js');

    expect(resourceCallback).toBeDefined();
    const result = await resourceCallback({ href: 'context://active' });
    expect(result.contents[0].text).toContain('No active context');
  });
});
