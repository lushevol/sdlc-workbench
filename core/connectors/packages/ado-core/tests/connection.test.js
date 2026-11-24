import { describe, it, expect, vi, beforeEach } from 'vitest';

vi.mock('azure-devops-node-api', () => ({
  getPersonalAccessTokenHandler: vi.fn(),
  WebApi: vi.fn()
}));

vi.mock('@sc-node-mcp/core', () => ({
  getConfig: vi.fn()
}));

import * as azdev from 'azure-devops-node-api';
import { getConfig } from '@sc-node-mcp/core';
import { getADOConnection } from '../src/connection.js';

describe('getADOConnection', () => {
  const mockAuthHandler = { scheme: 'Bearer', token: 'test-pat' };
  const mockWebApiInstance = { serverUrl: 'https://dev.azure.com/sc-ado' };

  beforeEach(() => {
    vi.clearAllMocks();
    vi.mocked(azdev.getPersonalAccessTokenHandler).mockReturnValue(mockAuthHandler);
    vi.mocked(azdev.WebApi).mockImplementation(function() { return mockWebApiInstance; });
  });

  it('should create a WebApi connection with PAT from config', async () => {
    getConfig.mockReturnValue({
      AZURE_DEVOPS_ORG_URL: 'https://dev.azure.com/sc-ado',
      AZURE_DEVOPS_PAT: 'my-test-pat'
    });

    const connection = await getADOConnection();

    expect(getConfig).toHaveBeenCalledOnce();
    expect(azdev.getPersonalAccessTokenHandler).toHaveBeenCalledWith('my-test-pat');
    expect(azdev.WebApi).toHaveBeenCalledWith('https://dev.azure.com/sc-ado', mockAuthHandler);
    expect(connection).toBe(mockWebApiInstance);
  });

  it('should use the org URL from config when constructing WebApi', async () => {
    getConfig.mockReturnValue({
      AZURE_DEVOPS_ORG_URL: 'https://dev.azure.com/sc-ado',
      AZURE_DEVOPS_PAT: 'another-pat'
    });

    await getADOConnection();

    expect(azdev.WebApi).toHaveBeenCalledWith(
      'https://dev.azure.com/sc-ado',
      expect.any(Object)
    );
  });

  it('should throw when getPersonalAccessTokenHandler throws', async () => {
    getConfig.mockReturnValue({
      AZURE_DEVOPS_ORG_URL: 'https://dev.azure.com/sc-ado',
      AZURE_DEVOPS_PAT: undefined
    });
    vi.mocked(azdev.getPersonalAccessTokenHandler).mockImplementation(() => {
      throw new Error('PAT is required');
    });

    await expect(getADOConnection()).rejects.toThrow('PAT is required');
  });
});

