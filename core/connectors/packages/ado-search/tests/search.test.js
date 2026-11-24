import { describe, it, expect, vi, beforeEach } from 'vitest';
import { configureSearchTools } from '../src/tools/search.js';
import { createMockServer, isValidToolResponse, isValidErrorResponse } from '@sc-node-mcp/shared-tests/helpers/mockServer';
import { createMockConnection } from '@sc-node-mcp/shared-tests/helpers/mockConnection';

describe('Search Tools', () => {
  let mockServer;
  let mockConnection;
  let getConnectionMock;

  beforeEach(() => {
    mockServer = createMockServer();
    mockConnection = createMockConnection();
    mockConnection.serverUrl = 'https://dev.azure.com/sc-ado';
    mockConnection.rest = {
      get: vi.fn(),
      create: vi.fn()
    };
    getConnectionMock = vi.fn().mockResolvedValue(mockConnection);
    configureSearchTools(mockServer, getConnectionMock);
  });

  describe('search_code', () => {
    it('should search code and return results', async () => {
      const mockResult = {
        count: 1,
        results: [{ fileName: 'index.js', path: '/src/index.js', matches: {} }]
      };
      mockConnection.rest.create.mockResolvedValue({ result: mockResult });

      const response = await mockServer.invokeTool('search_code', {
        searchText: 'configureAdoTools'
      });

      expect(isValidToolResponse(response)).toBe(true);
      const result = JSON.parse(response.content[0].text);
      expect(result.count).toBe(1);
    });

    it('should apply project and repository filters', async () => {
      mockConnection.rest.create.mockResolvedValue({ result: { count: 0, results: [] } });

      await mockServer.invokeTool('search_code', {
        searchText: 'myFunction',
        project: 'TBQPR',
        repository: 'my-repo',
        branch: 'main',
        path: '/src'
      });

      expect(mockConnection.rest.create).toHaveBeenCalledWith(
        expect.stringContaining('codesearchresults'),
        expect.objectContaining({
          searchText: 'myFunction',
          filters: {
            Project: ['TBQPR'],
            Repository: ['my-repo'],
            Branch: ['main'],
            Path: ['/src']
          }
        })
      );
    });

    it('should return error on API failure', async () => {
      mockConnection.rest.create.mockRejectedValue(new Error('Search API error'));

      const response = await mockServer.invokeTool('search_code', {
        searchText: 'test'
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('Search API error');
    });
  });

  describe('search_workitem', () => {
    it('should search work items and return results', async () => {
      const mockResult = {
        count: 2,
        results: [
          { fields: { 'system.id': '123', 'system.title': 'Bug fix' } },
          { fields: { 'system.id': '456', 'system.title': 'Feature request' } }
        ]
      };
      mockConnection.rest.create.mockResolvedValue({ result: mockResult });

      const response = await mockServer.invokeTool('search_workitem', {
        searchText: 'payment gateway'
      });

      expect(isValidToolResponse(response)).toBe(true);
      const result = JSON.parse(response.content[0].text);
      expect(result.count).toBe(2);
    });

    it('should apply work item filters', async () => {
      mockConnection.rest.create.mockResolvedValue({ result: { count: 0, results: [] } });

      await mockServer.invokeTool('search_workitem', {
        searchText: 'login bug',
        project: 'TBQPR',
        workItemType: 'Bug',
        state: 'Active',
        assignedTo: 'john.doe@company.com'
      });

      expect(mockConnection.rest.create).toHaveBeenCalledWith(
        expect.stringContaining('workitemsearchresults'),
        expect.objectContaining({
          searchText: 'login bug',
          filters: {
            Project: ['TBQPR'],
            'Work Item Types': ['Bug'],
            'States': ['Active'],
            'Assigned To': ['john.doe@company.com']
          }
        })
      );
    });

    it('should return error on search failure', async () => {
      mockConnection.rest.create.mockRejectedValue(new Error('Work item search failed'));

      const response = await mockServer.invokeTool('search_workitem', {
        searchText: 'test'
      });

      expect(isValidErrorResponse(response)).toBe(true);
    });
  });
});
