import { describe, it, expect, vi, beforeEach } from 'vitest';
import { getADOConnection } from '../src/connection.js';
import * as azdev from 'azure-devops-node-api';

// Mock dependencies
vi.mock('azure-devops-node-api');
vi.mock('@sc-node-mcp/core', () => ({
  getConfig: vi.fn(() => ({
    AZURE_DEVOPS_ORG_URL: 'https://dev.azure.com/test-org',
    AZURE_DEVOPS_PAT: 'test-pat-token',
  }))
}));

describe('ADO Connection', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    delete process.env.HTTPS_PROXY;
  });

  it('should create connection with PAT authentication', async () => {
    const mockWebApi = { test: 'mockWebApi' };
    const mockAuthHandler = { test: 'mockAuthHandler' };
    
    vi.spyOn(azdev, 'getPersonalAccessTokenHandler').mockReturnValue(mockAuthHandler);
    vi.spyOn(azdev, 'WebApi').mockImplementation(function() { return mockWebApi; });

    const connection = await getADOConnection();

    expect(azdev.getPersonalAccessTokenHandler).toHaveBeenCalledWith('test-pat-token');
    expect(azdev.WebApi).toHaveBeenCalledWith('https://dev.azure.com/test-org', mockAuthHandler);
    expect(connection).toBe(mockWebApi);
  });

  it('does not mutate HTTPS_PROXY env var (proxy is applied by detectProxy at startup)', async () => {
    const mockWebApi = { test: 'mockWebApi' };
    const mockAuthHandler = { test: 'mockAuthHandler' };
    
    vi.spyOn(azdev, 'getPersonalAccessTokenHandler').mockReturnValue(mockAuthHandler);
    vi.spyOn(azdev, 'WebApi').mockImplementation(function() { return mockWebApi; });

    await getADOConnection();

    // connection.js no longer touches process.env.HTTPS_PROXY
    expect(process.env.HTTPS_PROXY).toBeUndefined();
  });

  it('should work without proxy configuration', async () => {
    const mockWebApi = { test: 'mockWebApi' };
    const mockAuthHandler = { test: 'mockAuthHandler' };
    
    vi.spyOn(azdev, 'getPersonalAccessTokenHandler').mockReturnValue(mockAuthHandler);
    vi.spyOn(azdev, 'WebApi').mockImplementation(function() { return mockWebApi; });

    await getADOConnection();

    expect(process.env.HTTPS_PROXY).toBeUndefined();
  });
});
