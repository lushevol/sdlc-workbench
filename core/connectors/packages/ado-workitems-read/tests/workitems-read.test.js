import { describe, it, expect, vi, beforeEach } from 'vitest';
import { configureWorkItemsReadTools } from '../src/tools/workitems-read.js';
import { createMockServer, isValidToolResponse, isValidErrorResponse } from '@sc-node-mcp/shared-tests/helpers/mockServer';
import { createMockConnection, createMockWitApi, createMockCoreApi, createMockDashboardApi } from '@sc-node-mcp/shared-tests/helpers/mockConnection';

vi.mock('@sc-node-mcp/core', () => ({
  getConfig: vi.fn(() => ({
    AZURE_DEVOPS_ORG_URL: 'https://dev.azure.com/test-org',
    AZURE_DEVOPS_PAT: 'test-pat'
  }))
}));

vi.mock('@sc-node-mcp/ado-core/connection', () => ({
  getADOConnection: vi.fn()
}));

describe('configureWorkItemsReadTools', () => {
  let mockServer;
  let mockConnection;
  let mockWitApi;
  let mockCoreApi;
  let mockWorkApi;
  let mockDashboardApi;
  let getConnectionMock;

  beforeEach(() => {
    mockServer = createMockServer();
    mockConnection = createMockConnection();
    mockWitApi = createMockWitApi();
    // Add methods not in the default mock
    mockWitApi.getWorkItemType = vi.fn();
    mockWitApi.getQuery = vi.fn();
    mockWitApi.queryById = vi.fn();
    mockCoreApi = createMockCoreApi();
    mockWorkApi = {
      getBacklogs: vi.fn(),
      getBacklogLevelWorkItems: vi.fn(),
      getTeamIterations: vi.fn()
    };
    mockDashboardApi = createMockDashboardApi();

    mockConnection.getWorkItemTrackingApi.mockResolvedValue(mockWitApi);
    mockConnection.getCoreApi.mockResolvedValue(mockCoreApi);
    mockConnection.getWorkApi.mockResolvedValue(mockWorkApi);
    mockConnection.getDashboardApi.mockResolvedValue(mockDashboardApi);

    getConnectionMock = vi.fn().mockResolvedValue(mockConnection);
    configureWorkItemsReadTools(mockServer, getConnectionMock);
  });

  describe('wit_list_projects', () => {
    it('should list all projects', async () => {
      const projects = [{ id: 'proj-1', name: 'Project A' }];
      mockCoreApi.getProjects.mockResolvedValue(projects);

      const response = await mockServer.invokeTool('wit_list_projects', {});

      expect(isValidToolResponse(response)).toBe(true);
      const content = JSON.parse(response.content[0].text);
      expect(content).toEqual(projects);
    });

    it('should handle API errors', async () => {
      mockCoreApi.getProjects.mockRejectedValue(new Error('API error'));

      const response = await mockServer.invokeTool('wit_list_projects', {});

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('API error');
    });
  });

  describe('wit_get_work_item', () => {
    it('should retrieve work item by ID', async () => {
      const mockWorkItem = { id: 123, fields: { 'System.Title': 'Test' } };
      mockWitApi.getWorkItem.mockResolvedValue(mockWorkItem);

      const response = await mockServer.invokeTool('wit_get_work_item', { id: 123 });

      expect(isValidToolResponse(response)).toBe(true);
      expect(mockWitApi.getWorkItem).toHaveBeenCalledWith(123);
      const content = JSON.parse(response.content[0].text);
      expect(content.id).toBe(123);
    });

    it('should return error when work item is null', async () => {
      mockWitApi.getWorkItem.mockResolvedValue(null);

      const response = await mockServer.invokeTool('wit_get_work_item', { id: 999 });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('not found');
    });

    it('should handle API errors', async () => {
      mockWitApi.getWorkItem.mockRejectedValue(new Error('Connection refused'));

      const response = await mockServer.invokeTool('wit_get_work_item', { id: 123 });

      expect(isValidErrorResponse(response)).toBe(true);
    });
  });

  describe('wit_my_work_items', () => {
    it('should return work items assigned to current user', async () => {
      const mockItems = [{ id: 1 }, { id: 2 }];
      mockWitApi.queryByWiql.mockResolvedValue({ workItems: [{ id: 1 }, { id: 2 }] });
      mockWitApi.getWorkItems.mockResolvedValue(mockItems);

      const response = await mockServer.invokeTool('wit_my_work_items', {});

      expect(isValidToolResponse(response)).toBe(true);
      expect(mockWitApi.queryByWiql).toHaveBeenCalled();
      expect(mockWitApi.getWorkItems).toHaveBeenCalledWith([1, 2]);
    });

    it('should return message when no work items found', async () => {
      mockWitApi.queryByWiql.mockResolvedValue({ workItems: [] });

      const response = await mockServer.invokeTool('wit_my_work_items', {});

      expect(isValidToolResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('No work items found');
    });

    it('should respect top parameter', async () => {
      const ids = Array.from({ length: 30 }, (_, i) => ({ id: i + 1 }));
      mockWitApi.queryByWiql.mockResolvedValue({ workItems: ids });
      mockWitApi.getWorkItems.mockResolvedValue([]);

      await mockServer.invokeTool('wit_my_work_items', { top: 5 });

      expect(mockWitApi.getWorkItems).toHaveBeenCalledWith([1, 2, 3, 4, 5]);
    });

    it('should handle API errors', async () => {
      mockWitApi.queryByWiql.mockRejectedValue(new Error('WIQL error'));

      const response = await mockServer.invokeTool('wit_my_work_items', {});

      expect(isValidErrorResponse(response)).toBe(true);
    });
  });

  describe('wit_get_work_items_batch_by_ids', () => {
    it('should return multiple work items', async () => {
      const items = [{ id: 1 }, { id: 2 }, { id: 3 }];
      mockWitApi.getWorkItems.mockResolvedValue(items);

      const response = await mockServer.invokeTool('wit_get_work_items_batch_by_ids', { ids: [1, 2, 3] });

      expect(isValidToolResponse(response)).toBe(true);
      expect(mockWitApi.getWorkItems).toHaveBeenCalledWith([1, 2, 3]);
    });

    it('should handle API errors', async () => {
      mockWitApi.getWorkItems.mockRejectedValue(new Error('Batch error'));

      const response = await mockServer.invokeTool('wit_get_work_items_batch_by_ids', { ids: [1] });

      expect(isValidErrorResponse(response)).toBe(true);
    });
  });

  describe('wit_list_work_item_comments', () => {
    it('should list comments for a work item', async () => {
      const workItemWithProject = {
        id: 42,
        fields: { 'System.TeamProject': 'MyProject' }
      };
      mockWitApi.getWorkItem.mockResolvedValue(workItemWithProject);
      mockWitApi.getComments.mockResolvedValue({ comments: [{ text: 'A comment' }] });

      const response = await mockServer.invokeTool('wit_list_work_item_comments', { id: 42 });

      expect(isValidToolResponse(response)).toBe(true);
      expect(mockWitApi.getComments).toHaveBeenCalledWith('MyProject', 42);
    });

    it('should return error when work item has no project field', async () => {
      mockWitApi.getWorkItem.mockResolvedValue({ id: 42, fields: {} });

      const response = await mockServer.invokeTool('wit_list_work_item_comments', { id: 42 });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('Unable to determine project');
    });

    it('should return error when work item is null', async () => {
      mockWitApi.getWorkItem.mockResolvedValue(null);

      const response = await mockServer.invokeTool('wit_list_work_item_comments', { id: 42 });

      expect(isValidErrorResponse(response)).toBe(true);
    });

    it('should handle API errors', async () => {
      mockWitApi.getWorkItem.mockRejectedValue(new Error('Not found'));

      const response = await mockServer.invokeTool('wit_list_work_item_comments', { id: 42 });

      expect(isValidErrorResponse(response)).toBe(true);
    });
  });

  describe('wit_get_work_item_type', () => {
    it('should return work item type details', async () => {
      const typeDetails = { name: 'Bug', fields: [] };
      mockWitApi.getWorkItemType.mockResolvedValue(typeDetails);

      const response = await mockServer.invokeTool('wit_get_work_item_type', { project: 'MyProject', type: 'Bug' });

      expect(isValidToolResponse(response)).toBe(true);
      expect(mockWitApi.getWorkItemType).toHaveBeenCalledWith('MyProject', 'Bug');
    });

    it('should handle API errors', async () => {
      mockWitApi.getWorkItemType.mockRejectedValue(new Error('Type not found'));

      const response = await mockServer.invokeTool('wit_get_work_item_type', { project: 'MyProject', type: 'Unknown' });

      expect(isValidErrorResponse(response)).toBe(true);
    });
  });

  describe('wit_list_backlogs', () => {
    it('should list available backlogs', async () => {
      const backlogs = [{ id: 'Microsoft.RequirementCategory', name: 'Stories' }];
      mockWorkApi.getBacklogs.mockResolvedValue(backlogs);

      const response = await mockServer.invokeTool('wit_list_backlogs', { project: 'MyProject', team: 'Team A' });

      expect(isValidToolResponse(response)).toBe(true);
      expect(mockWorkApi.getBacklogs).toHaveBeenCalledWith({ project: 'MyProject', team: 'Team A' });
    });

    it('should handle API errors', async () => {
      mockWorkApi.getBacklogs.mockRejectedValue(new Error('Work API error'));

      const response = await mockServer.invokeTool('wit_list_backlogs', { project: 'MyProject', team: 'Team A' });

      expect(isValidErrorResponse(response)).toBe(true);
    });
  });

  describe('wit_list_backlog_work_items', () => {
    it('should list work items in a backlog', async () => {
      const backlog = { workItems: [{ target: { id: 1 } }] };
      mockWorkApi.getBacklogLevelWorkItems.mockResolvedValue(backlog);

      const response = await mockServer.invokeTool('wit_list_backlog_work_items', {
        project: 'MyProject',
        team: 'Team A',
        backlogId: 'Microsoft.RequirementCategory'
      });

      expect(isValidToolResponse(response)).toBe(true);
      expect(mockWorkApi.getBacklogLevelWorkItems).toHaveBeenCalledWith(
        { project: 'MyProject', team: 'Team A' },
        'Microsoft.RequirementCategory'
      );
    });

    it('should handle API errors', async () => {
      mockWorkApi.getBacklogLevelWorkItems.mockRejectedValue(new Error('Backlog error'));

      const response = await mockServer.invokeTool('wit_list_backlog_work_items', {
        project: 'MyProject',
        team: 'Team A',
        backlogId: 'Microsoft.RequirementCategory'
      });

      expect(isValidErrorResponse(response)).toBe(true);
    });
  });

  describe('wit_list_teams', () => {
    it('should list teams for a project', async () => {
      const teams = [{ id: 'team-1', name: 'Team A' }];
      mockCoreApi.getTeams.mockResolvedValue(teams);

      const response = await mockServer.invokeTool('wit_list_teams', { project: 'MyProject' });

      expect(isValidToolResponse(response)).toBe(true);
      expect(mockCoreApi.getTeams).toHaveBeenCalledWith('MyProject');
    });

    it('should handle API errors', async () => {
      mockCoreApi.getTeams.mockRejectedValue(new Error('Core API error'));

      const response = await mockServer.invokeTool('wit_list_teams', { project: 'MyProject' });

      expect(isValidErrorResponse(response)).toBe(true);
    });
  });

  describe('wit_list_iterations', () => {
    it('should list iterations for project and team', async () => {
      const iterations = [{ id: 'iter-1', name: 'Sprint 1' }];
      mockWorkApi.getTeamIterations.mockResolvedValue(iterations);

      const response = await mockServer.invokeTool('wit_list_iterations', { project: 'MyProject', team: 'Team A' });

      expect(isValidToolResponse(response)).toBe(true);
      expect(mockWorkApi.getTeamIterations).toHaveBeenCalledWith({ project: 'MyProject', team: 'Team A' });
    });

    it('should handle API errors', async () => {
      mockWorkApi.getTeamIterations.mockRejectedValue(new Error('Iteration error'));

      const response = await mockServer.invokeTool('wit_list_iterations', { project: 'MyProject', team: 'Team A' });

      expect(isValidErrorResponse(response)).toBe(true);
    });
  });

  describe('wit_get_work_items_for_iteration', () => {
    it('should return work items for an iteration', async () => {
      mockWitApi.queryByWiql.mockResolvedValue({ workItems: [{ id: 10 }, { id: 11 }] });
      mockWitApi.getWorkItems.mockResolvedValue([{ id: 10 }, { id: 11 }]);

      const response = await mockServer.invokeTool('wit_get_work_items_for_iteration', {
        project: 'MyProject',
        team: 'Team A',
        iterationPath: String.raw`MyProject\Sprint 1`
      });

      expect(isValidToolResponse(response)).toBe(true);
      expect(mockWitApi.queryByWiql).toHaveBeenCalled();
      expect(mockWitApi.getWorkItems).toHaveBeenCalledWith([10, 11]);
    });

    it('should escape single quotes in iteration path', async () => {
      mockWitApi.queryByWiql.mockResolvedValue({ workItems: [] });

      await mockServer.invokeTool('wit_get_work_items_for_iteration', {
        project: 'MyProject',
        team: 'Team A',
        iterationPath: String.raw`My'Project\Sprint 1`
      });

      const callArg = mockWitApi.queryByWiql.mock.calls[0][0];
      expect(callArg.query).toContain("My''Project");
    });

    it('should return message when no work items found', async () => {
      mockWitApi.queryByWiql.mockResolvedValue({ workItems: [] });

      const response = await mockServer.invokeTool('wit_get_work_items_for_iteration', {
        project: 'MyProject',
        team: 'Team A',
        iterationPath: String.raw`MyProject\Sprint 1`
      });

      expect(isValidToolResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('No work items found');
    });

    it('should handle API errors', async () => {
      mockWitApi.queryByWiql.mockRejectedValue(new Error('WIQL failed'));

      const response = await mockServer.invokeTool('wit_get_work_items_for_iteration', {
        project: 'MyProject',
        team: 'Team A',
        iterationPath: String.raw`MyProject\Sprint 1`
      });

      expect(isValidErrorResponse(response)).toBe(true);
    });
  });

  describe('wit_get_query', () => {
    it('should return query metadata', async () => {
      const query = { id: 'query-guid', name: 'My Query' };
      mockWitApi.getQuery.mockResolvedValue(query);

      const response = await mockServer.invokeTool('wit_get_query', { project: 'MyProject', queryId: 'query-guid' });

      expect(isValidToolResponse(response)).toBe(true);
      expect(mockWitApi.getQuery).toHaveBeenCalledWith('MyProject', 'query-guid');
    });

    it('should handle API errors', async () => {
      mockWitApi.getQuery.mockRejectedValue(new Error('Query not found'));

      const response = await mockServer.invokeTool('wit_get_query', { project: 'MyProject', queryId: 'bad-id' });

      expect(isValidErrorResponse(response)).toBe(true);
    });
  });

  describe('wit_get_query_results_by_id', () => {
    it('should execute query and return work items', async () => {
      mockWitApi.queryById.mockResolvedValue({ workItems: [{ id: 1 }, { id: 2 }] });
      mockWitApi.getWorkItems.mockResolvedValue([{ id: 1 }, { id: 2 }]);

      const response = await mockServer.invokeTool('wit_get_query_results_by_id', {
        project: 'MyProject',
        queryId: 'query-guid'
      });

      expect(isValidToolResponse(response)).toBe(true);
      expect(mockWitApi.queryById).toHaveBeenCalledWith('query-guid', { project: 'MyProject' });
      expect(mockWitApi.getWorkItems).toHaveBeenCalledWith([1, 2]);
    });

    it('should return message when query has no results', async () => {
      mockWitApi.queryById.mockResolvedValue({ workItems: [] });

      const response = await mockServer.invokeTool('wit_get_query_results_by_id', {
        project: 'MyProject',
        queryId: 'query-guid'
      });

      expect(isValidToolResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('No work items found');
    });

    it('should handle API errors', async () => {
      mockWitApi.queryById.mockRejectedValue(new Error('Query execution failed'));

      const response = await mockServer.invokeTool('wit_get_query_results_by_id', {
        project: 'MyProject',
        queryId: 'query-guid'
      });

      expect(isValidErrorResponse(response)).toBe(true);
    });
  });

  describe('wit_list_work_item_pull_requests', () => {
    it('should return pull requests linked to a work item', async () => {
      const prRelation = {
        rel: 'ArtifactLink',
        url: 'vstfs:///Git/PullRequestId/proj%2Frepo%2F42',
        attributes: { name: 'Pull Request' }
      };
      mockWitApi.getWorkItem.mockResolvedValue({ id: 1, relations: [prRelation] });

      const response = await mockServer.invokeTool('wit_list_work_item_pull_requests', { id: 1 });

      expect(isValidToolResponse(response)).toBe(true);
      expect(mockWitApi.getWorkItem).toHaveBeenCalledWith(1, undefined, undefined, 1);
      const content = JSON.parse(response.content[0].text);
      expect(content).toHaveLength(1);
    });

    it('should return message when no PRs linked', async () => {
      mockWitApi.getWorkItem.mockResolvedValue({ id: 1, relations: [] });

      const response = await mockServer.invokeTool('wit_list_work_item_pull_requests', { id: 1 });

      expect(isValidToolResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('No pull requests found');
    });

    it('should return message when work item has no relations', async () => {
      mockWitApi.getWorkItem.mockResolvedValue({ id: 1 });

      const response = await mockServer.invokeTool('wit_list_work_item_pull_requests', { id: 1 });

      expect(isValidToolResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('No pull requests found');
    });

    it('should match PR relation via attributes.name when URL lacks PullRequestId', async () => {
      const prRelation = {
        rel: 'ArtifactLink',
        url: 'vstfs:///Git/GenericLink/proj%2Frepo%2F42',
        attributes: { name: 'Pull Request' }
      };
      mockWitApi.getWorkItem.mockResolvedValue({ id: 1, relations: [prRelation] });

      const response = await mockServer.invokeTool('wit_list_work_item_pull_requests', { id: 1 });

      expect(isValidToolResponse(response)).toBe(true);
      const content = JSON.parse(response.content[0].text);
      expect(content).toHaveLength(1);
    });

    it('should handle API errors', async () => {
      mockWitApi.getWorkItem.mockRejectedValue(new Error('Not found'));

      const response = await mockServer.invokeTool('wit_list_work_item_pull_requests', { id: 1 });

      expect(isValidErrorResponse(response)).toBe(true);
    });
  });

  describe('wit_list_work_item_commits', () => {
    it('should return commits linked to a work item', async () => {
      const commitRelation = {
        rel: 'ArtifactLink',
        url: 'vstfs:///Git/Commit/proj%2Frepo%2Fabc123',
        attributes: { name: 'Commit' }
      };
      mockWitApi.getWorkItem.mockResolvedValue({ id: 1, relations: [commitRelation] });

      const response = await mockServer.invokeTool('wit_list_work_item_commits', { id: 1 });

      expect(isValidToolResponse(response)).toBe(true);
      const content = JSON.parse(response.content[0].text);
      expect(content).toHaveLength(1);
    });

    it('should return message when no commits linked', async () => {
      mockWitApi.getWorkItem.mockResolvedValue({ id: 1, relations: [] });

      const response = await mockServer.invokeTool('wit_list_work_item_commits', { id: 1 });

      expect(isValidToolResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('No commits found');
    });

    it('should return message when work item has no relations', async () => {
      mockWitApi.getWorkItem.mockResolvedValue({ id: 1 });

      const response = await mockServer.invokeTool('wit_list_work_item_commits', { id: 1 });

      expect(isValidToolResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('No commits found');
    });

    it('should match commit relation via attributes.name when URL lacks Commit keyword', async () => {
      const commitRelation = {
        rel: 'ArtifactLink',
        url: 'vstfs:///Git/GenericLink/proj%2Frepo%2Fabc123',
        attributes: { name: 'Commit' }
      };
      mockWitApi.getWorkItem.mockResolvedValue({ id: 1, relations: [commitRelation] });

      const response = await mockServer.invokeTool('wit_list_work_item_commits', { id: 1 });

      expect(isValidToolResponse(response)).toBe(true);
      const content = JSON.parse(response.content[0].text);
      expect(content).toHaveLength(1);
    });

    it('should handle API errors', async () => {
      mockWitApi.getWorkItem.mockRejectedValue(new Error('Not found'));

      const response = await mockServer.invokeTool('wit_list_work_item_commits', { id: 1 });

      expect(isValidErrorResponse(response)).toBe(true);
    });
  });

  describe('wit_list_work_item_revisions', () => {
    it('should return revision history', async () => {
      const revisions = [{ rev: 1 }, { rev: 2 }];
      mockWitApi.getRevisions.mockResolvedValue(revisions);

      const response = await mockServer.invokeTool('wit_list_work_item_revisions', {
        project: 'MyProject',
        id: 42
      });

      expect(isValidToolResponse(response)).toBe(true);
      expect(mockWitApi.getRevisions).toHaveBeenCalledWith(42, undefined, undefined, 1);
    });

    it('should pass top and skip parameters', async () => {
      mockWitApi.getRevisions.mockResolvedValue([]);

      await mockServer.invokeTool('wit_list_work_item_revisions', {
        project: 'MyProject',
        id: 42,
        top: 5,
        skip: 10
      });

      expect(mockWitApi.getRevisions).toHaveBeenCalledWith(42, 5, 10, 1);
    });

    it('should handle API errors', async () => {
      mockWitApi.getRevisions.mockRejectedValue(new Error('Revisions error'));

      const response = await mockServer.invokeTool('wit_list_work_item_revisions', {
        project: 'MyProject',
        id: 42
      });

      expect(isValidErrorResponse(response)).toBe(true);
    });
  });

  describe('wit_get_work_item_links', () => {
    it('should return parent, child, and related work items grouped by relation type', async () => {
      mockWitApi.getWorkItem.mockResolvedValue({
        id: 1,
        relations: [
          { rel: 'System.LinkTypes.Hierarchy-Reverse', url: 'https://dev.azure.com/org/_apis/wit/workItems/10' },
          { rel: 'System.LinkTypes.Hierarchy-Forward', url: 'https://dev.azure.com/org/_apis/wit/workItems/20' },
          { rel: 'System.LinkTypes.Related', url: 'https://dev.azure.com/org/_apis/wit/workItems/30' },
          { rel: 'ArtifactLink', url: 'vstfs:///Git/Commit/proj%2Frepo%2Fabc123' }
        ]
      });
      mockWitApi.getWorkItems.mockResolvedValue([
        { id: 10, fields: { 'System.Title': 'Parent' } },
        { id: 20, fields: { 'System.Title': 'Child' } },
        { id: 30, fields: { 'System.Title': 'Related' } }
      ]);

      const response = await mockServer.invokeTool('wit_get_work_item_links', { id: 1 });

      expect(isValidToolResponse(response)).toBe(true);
      expect(mockWitApi.getWorkItem).toHaveBeenCalledWith(1, undefined, undefined, 1);
      expect(mockWitApi.getWorkItems).toHaveBeenCalledWith([10, 20, 30]);
      const content = JSON.parse(response.content[0].text);
      expect(content.parent).toHaveLength(1);
      expect(content.child).toHaveLength(1);
      expect(content.related).toHaveLength(1);
    });

    it('should return message when no hierarchy/related links found', async () => {
      mockWitApi.getWorkItem.mockResolvedValue({ id: 1, relations: [] });

      const response = await mockServer.invokeTool('wit_get_work_item_links', { id: 1 });

      expect(isValidToolResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('No parent/child/related links found');
    });

    it('should return message when work item has no relations field', async () => {
      mockWitApi.getWorkItem.mockResolvedValue({ id: 1 });

      const response = await mockServer.invokeTool('wit_get_work_item_links', { id: 1 });

      expect(isValidToolResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('No parent/child/related links found');
    });

    it('should handle API errors', async () => {
      mockWitApi.getWorkItem.mockRejectedValue(new Error('Not found'));

      const response = await mockServer.invokeTool('wit_get_work_item_links', { id: 1 });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('Not found');
    });
  });

  describe('wit_query_by_url', () => {
    it('should resolve work items given project and queryId', async () => {
      mockWitApi.queryById.mockResolvedValue({ workItems: [{ id: 1 }, { id: 2 }] });
      mockWitApi.getWorkItems.mockResolvedValue([{ id: 1 }, { id: 2 }]);

      const response = await mockServer.invokeTool('wit_query_by_url', { project: 'MyProject', queryId: 'query-guid' });

      expect(isValidToolResponse(response)).toBe(true);
      expect(mockWitApi.queryById).toHaveBeenCalledWith('query-guid', { project: 'MyProject' });
      expect(mockWitApi.getWorkItems).toHaveBeenCalledWith([1, 2]);
    });

    it('should parse project and queryId from a query URL', async () => {
      mockWitApi.queryById.mockResolvedValue({ workItems: [{ id: 5 }] });
      mockWitApi.getWorkItems.mockResolvedValue([{ id: 5 }]);

      const response = await mockServer.invokeTool('wit_query_by_url', {
        url: 'https://dev.azure.com/sc-ado/MyProject/_queries/query/2a29568d-2200-40c6-b596-ccb6506af764'
      });

      expect(isValidToolResponse(response)).toBe(true);
      expect(mockWitApi.queryById).toHaveBeenCalledWith('2a29568d-2200-40c6-b596-ccb6506af764', { project: 'MyProject' });
    });

    it('should reject dashboard links with a clear message', async () => {
      const response = await mockServer.invokeTool('wit_query_by_url', {
        url: 'https://dev.azure.com/sc-ado/DDCPQPR/_dashboards/dashboard/2a29568d-2200-40c6-b596-ccb6506af764'
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('wit_get_dashboard_work_items');
    });

    it('should error when neither url nor project+queryId are provided', async () => {
      const response = await mockServer.invokeTool('wit_query_by_url', {});

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain("Provide either 'url'");
    });

    it('should return message when query has no results', async () => {
      mockWitApi.queryById.mockResolvedValue({ workItems: [] });

      const response = await mockServer.invokeTool('wit_query_by_url', { project: 'MyProject', queryId: 'query-guid' });

      expect(isValidToolResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('No work items found');
    });

    it('should handle API errors', async () => {
      mockWitApi.queryById.mockRejectedValue(new Error('Query failed'));

      const response = await mockServer.invokeTool('wit_query_by_url', { project: 'MyProject', queryId: 'query-guid' });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('Query failed');
    });
  });

  describe('wit_get_dashboard_work_items', () => {
    it('should return work items from query-backed widgets', async () => {
      mockDashboardApi.getDashboard.mockResolvedValue({
        widgets: [
          { name: 'Open Bugs', contributionId: 'ms.vss-dashboards-web.query-tile-widget', settings: JSON.stringify({ queryId: 'query-guid' }) },
          { name: 'Markdown Note', contributionId: 'ms.vss-dashboards-web.markdown-widget', settings: JSON.stringify({ text: 'hello' }) }
        ]
      });
      mockWitApi.queryById.mockResolvedValue({ workItems: [{ id: 1 }] });
      mockWitApi.getWorkItems.mockResolvedValue([{ id: 1 }]);

      const response = await mockServer.invokeTool('wit_get_dashboard_work_items', { project: 'MyProject', dashboardId: 'dash-guid' });

      expect(isValidToolResponse(response)).toBe(true);
      expect(mockDashboardApi.getDashboard).toHaveBeenCalledWith({ project: 'MyProject', team: undefined }, 'dash-guid');
      const content = JSON.parse(response.content[0].text);
      expect(content).toHaveLength(1);
      expect(content[0].widgetName).toBe('Open Bugs');
      expect(content[0].items).toEqual([{ id: 1 }]);
    });

    it('should parse project and dashboardId from a dashboard URL', async () => {
      mockDashboardApi.getDashboard.mockResolvedValue({ widgets: [] });

      const response = await mockServer.invokeTool('wit_get_dashboard_work_items', {
        url: 'https://dev.azure.com/sc-ado/DDCPQPR/_dashboards/dashboard/2a29568d-2200-40c6-b596-ccb6506af764'
      });

      expect(isValidToolResponse(response)).toBe(true);
      expect(mockDashboardApi.getDashboard).toHaveBeenCalledWith(
        { project: 'DDCPQPR', team: undefined },
        '2a29568d-2200-40c6-b596-ccb6506af764'
      );
    });

    it('should skip widgets with malformed settings JSON', async () => {
      mockDashboardApi.getDashboard.mockResolvedValue({
        widgets: [{ name: 'Broken', settings: '{not-json' }]
      });

      const response = await mockServer.invokeTool('wit_get_dashboard_work_items', { project: 'MyProject', dashboardId: 'dash-guid' });

      expect(isValidToolResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('No query-backed widgets found');
    });

    it('should return message when no query-backed widgets found', async () => {
      mockDashboardApi.getDashboard.mockResolvedValue({ widgets: [] });

      const response = await mockServer.invokeTool('wit_get_dashboard_work_items', { project: 'MyProject', dashboardId: 'dash-guid' });

      expect(isValidToolResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('No query-backed widgets found');
    });

    it('should reject non-dashboard URLs with a clear message', async () => {
      const response = await mockServer.invokeTool('wit_get_dashboard_work_items', {
        url: 'https://dev.azure.com/sc-ado/MyProject/_queries/query/2a29568d-2200-40c6-b596-ccb6506af764'
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('not a dashboard link');
    });

    it('should error when neither url nor project+dashboardId are provided', async () => {
      const response = await mockServer.invokeTool('wit_get_dashboard_work_items', {});

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain("Provide either 'url'");
    });

    it('should handle API errors', async () => {
      mockDashboardApi.getDashboard.mockRejectedValue(new Error('Dashboard not found'));

      const response = await mockServer.invokeTool('wit_get_dashboard_work_items', { project: 'MyProject', dashboardId: 'dash-guid' });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('Dashboard not found');
    });
  });

  describe('error fallback (String(error) path)', () => {
    it('wit_list_projects falls back to String(error)', async () => {
      mockCoreApi.getProjects.mockRejectedValue('raw string error');
      const response = await mockServer.invokeTool('wit_list_projects', {});
      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('raw string error');
    });

    it('wit_get_work_item falls back to String(error)', async () => {
      mockWitApi.getWorkItem.mockRejectedValue('raw wit error');
      const response = await mockServer.invokeTool('wit_get_work_item', { id: 1 });
      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('raw wit error');
    });

    it('wit_my_work_items falls back to String(error)', async () => {
      mockWitApi.queryByWiql.mockRejectedValue('raw query error');
      const response = await mockServer.invokeTool('wit_my_work_items', {});
      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('raw query error');
    });

    it('wit_get_work_items_batch_by_ids falls back to String(error)', async () => {
      mockWitApi.getWorkItems.mockRejectedValue('raw batch error');
      const response = await mockServer.invokeTool('wit_get_work_items_batch_by_ids', { ids: [1] });
      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('raw batch error');
    });

    it('wit_list_work_item_comments falls back to String(error)', async () => {
      mockWitApi.getWorkItem.mockResolvedValue({ fields: { 'System.TeamProject': 'P' } });
      mockWitApi.getComments.mockRejectedValue('raw comments error');
      const response = await mockServer.invokeTool('wit_list_work_item_comments', { id: 1 });
      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('raw comments error');
    });

    it('wit_get_work_item_type falls back to String(error)', async () => {
      mockWitApi.getWorkItemType.mockRejectedValue('raw type error');
      const response = await mockServer.invokeTool('wit_get_work_item_type', { project: 'P', type: 'Bug' });
      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('raw type error');
    });

    it('wit_list_backlogs falls back to String(error)', async () => {
      mockWorkApi.getBacklogs.mockRejectedValue('raw backlogs error');
      const response = await mockServer.invokeTool('wit_list_backlogs', { project: 'P', team: 'T' });
      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('raw backlogs error');
    });

    it('wit_list_backlog_work_items falls back to String(error)', async () => {
      mockWorkApi.getBacklogLevelWorkItems.mockRejectedValue('raw backlog-wi error');
      const response = await mockServer.invokeTool('wit_list_backlog_work_items', { project: 'P', team: 'T', backlogId: 'bid' });
      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('raw backlog-wi error');
    });

    it('wit_list_teams falls back to String(error)', async () => {
      mockCoreApi.getTeams.mockRejectedValue('raw teams error');
      const response = await mockServer.invokeTool('wit_list_teams', { project: 'P' });
      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('raw teams error');
    });

    it('wit_list_iterations falls back to String(error)', async () => {
      mockWorkApi.getTeamIterations.mockRejectedValue('raw iterations error');
      const response = await mockServer.invokeTool('wit_list_iterations', { project: 'P', team: 'T' });
      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('raw iterations error');
    });

    it('wit_get_work_items_for_iteration falls back to String(error)', async () => {
      mockWitApi.queryByWiql.mockRejectedValue('raw iter-wi error');
      const response = await mockServer.invokeTool('wit_get_work_items_for_iteration', { project: 'P', iterationPath: 'Sprint 1' });
      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('raw iter-wi error');
    });

    it('wit_get_query falls back to String(error)', async () => {
      mockWitApi.getQuery.mockRejectedValue('raw getquery error');
      const response = await mockServer.invokeTool('wit_get_query', { project: 'P', queryId: 'q-id' });
      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('raw getquery error');
    });

    it('wit_get_query_results_by_id falls back to String(error)', async () => {
      mockWitApi.queryById.mockRejectedValue('raw query-results error');
      const response = await mockServer.invokeTool('wit_get_query_results_by_id', { project: 'P', queryId: 'q-id' });
      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('raw query-results error');
    });

    it('wit_list_work_item_pull_requests falls back to String(error)', async () => {
      mockWitApi.getWorkItem.mockRejectedValue('raw pr-links error');
      const response = await mockServer.invokeTool('wit_list_work_item_pull_requests', { id: 1 });
      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('raw pr-links error');
    });

    it('wit_list_work_item_commits falls back to String(error)', async () => {
      mockWitApi.getWorkItem.mockRejectedValue('raw commit-links error');
      const response = await mockServer.invokeTool('wit_list_work_item_commits', { id: 1 });
      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('raw commit-links error');
    });

    it('wit_list_work_item_revisions falls back to String(error)', async () => {
      mockWitApi.getRevisions.mockRejectedValue('raw revisions error');
      const response = await mockServer.invokeTool('wit_list_work_item_revisions', { project: 'P', id: 1 });
      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('raw revisions error');
    });
  });
});

async function* helloWorldStream() {
  yield Buffer.from('hello world');
}

async function* dataStream() {
  yield Buffer.from('data');
}

describe('wit_get_work_item_attachment (stream tests)', () => {
  let mockServer;
  let mockConnection;
  let mockWitApi;
  let getConnectionMock;

  beforeEach(() => {
    mockServer = createMockServer();
    mockConnection = createMockConnection();
    mockWitApi = createMockWitApi();
    mockWitApi.getWorkItemType = vi.fn();
    mockWitApi.getQuery = vi.fn();
    mockWitApi.queryById = vi.fn();
    mockConnection.getWorkItemTrackingApi.mockResolvedValue(mockWitApi);
    getConnectionMock = vi.fn().mockResolvedValue(mockConnection);
    configureWorkItemsReadTools(mockServer, getConnectionMock);
  });

  it('should download attachment and return base64', async () => {
    mockWitApi.getAttachmentContent.mockResolvedValue(helloWorldStream());

    const response = await mockServer.invokeTool('wit_get_work_item_attachment', {
      project: 'MyProject',
      attachmentId: 'attach-guid',
      fileName: 'test.txt'
    });

    expect(isValidToolResponse(response)).toBe(true);
    const content = JSON.parse(response.content[0].text);
    expect(content.attachmentId).toBe('attach-guid');
    expect(content.fileName).toBe('test.txt');
    expect(content.base64Content).toBe(Buffer.from('hello world').toString('base64'));
  });

  it('should work without fileName', async () => {
    mockWitApi.getAttachmentContent.mockResolvedValue(dataStream());

    const response = await mockServer.invokeTool('wit_get_work_item_attachment', {
      project: 'MyProject',
      attachmentId: 'attach-guid'
    });

    expect(isValidToolResponse(response)).toBe(true);
  });

  it('should handle API errors', async () => {
    mockWitApi.getAttachmentContent.mockRejectedValue(new Error('Attachment not found'));

    const response = await mockServer.invokeTool('wit_get_work_item_attachment', {
      project: 'MyProject',
      attachmentId: 'bad-guid'
    });

    expect(isValidErrorResponse(response)).toBe(true);
  });

  it('wit_get_work_item_attachment falls back to String(error)', async () => {
    mockWitApi.getAttachmentContent.mockRejectedValue('raw attachment error');

    const response = await mockServer.invokeTool('wit_get_work_item_attachment', {
      project: 'MyProject',
      attachmentId: 'some-guid'
    });

    expect(isValidErrorResponse(response)).toBe(true);
    expect(response.content[0].text).toBe('raw attachment error');
  });
});
