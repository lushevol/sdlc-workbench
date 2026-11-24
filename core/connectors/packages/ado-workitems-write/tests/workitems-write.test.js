import { describe, it, expect, vi, beforeEach } from 'vitest';
import { configureWorkItemsWriteTools } from '../src/tools/workitems-write.js';
import { createMockServer, isValidToolResponse, isValidErrorResponse } from '@sc-node-mcp/shared-tests/helpers/mockServer';
import { createMockConnection, createMockWitApi } from '@sc-node-mcp/shared-tests/helpers/mockConnection';

vi.mock('@sc-node-mcp/core', () => ({
  getConfig: vi.fn(() => ({
    AZURE_DEVOPS_ORG_URL: 'https://dev.azure.com/test-org',
    AZURE_DEVOPS_PAT: 'test-pat'
  }))
}));

vi.mock('@sc-node-mcp/ado-core/connection', () => ({
  getADOConnection: vi.fn()
}));

describe('configureWorkItemsWriteTools', () => {
  let mockServer;
  let mockConnection;
  let mockWitApi;
  let getConnectionMock;

  beforeEach(() => {
    mockServer = createMockServer();
    mockConnection = createMockConnection();
    mockWitApi = createMockWitApi();

    mockConnection.getWorkItemTrackingApi.mockResolvedValue(mockWitApi);

    getConnectionMock = vi.fn().mockResolvedValue(mockConnection);
    configureWorkItemsWriteTools(mockServer, getConnectionMock);
  });

  // ─── wit_add_work_item_comment ──────────────────────────────────────────────

  describe('wit_add_work_item_comment', () => {
    it('should add a comment to a work item', async () => {
      const workItem = { id: 42, fields: { 'System.TeamProject': 'MyProject' } };
      mockWitApi.getWorkItem.mockResolvedValue(workItem);
      const commentResult = { id: 1, text: 'Hello world' };
      mockWitApi.addComment.mockResolvedValue(commentResult);

      const response = await mockServer.invokeTool('wit_add_work_item_comment', { id: 42, text: 'Hello world' });

      expect(isValidToolResponse(response)).toBe(true);
      expect(mockWitApi.getWorkItem).toHaveBeenCalledWith(42);
      expect(mockWitApi.addComment).toHaveBeenCalledWith({ text: 'Hello world' }, 'MyProject', 42);
      const content = JSON.parse(response.content[0].text);
      expect(content.text).toBe('Hello world');
    });

    it('should return error when project cannot be determined', async () => {
      mockWitApi.getWorkItem.mockResolvedValue({ id: 42, fields: {} });

      const response = await mockServer.invokeTool('wit_add_work_item_comment', { id: 42, text: 'test' });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('Unable to determine project');
    });

    it('should return error when work item not found', async () => {
      mockWitApi.getWorkItem.mockResolvedValue(null);

      const response = await mockServer.invokeTool('wit_add_work_item_comment', { id: 99, text: 'test' });

      expect(isValidErrorResponse(response)).toBe(true);
    });

    it('should handle API errors', async () => {
      mockWitApi.getWorkItem.mockRejectedValue(new Error('API error'));

      const response = await mockServer.invokeTool('wit_add_work_item_comment', { id: 42, text: 'test' });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('API error');
    });

    it('should fall back to String(error) when error has no message', async () => {
      mockWitApi.getWorkItem.mockRejectedValue('plain string error');

      const response = await mockServer.invokeTool('wit_add_work_item_comment', { id: 42, text: 'test' });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('plain string error');
    });
  });

  // ─── wit_update_work_item ───────────────────────────────────────────────────

  describe('wit_update_work_item', () => {
    it('should update a work item with the given patch', async () => {
      const updated = { id: 10, fields: { 'System.Title': 'New Title' } };
      mockWitApi.updateWorkItem.mockResolvedValue(updated);
      const patch = [{ op: 'add', path: '/fields/System.Title', value: 'New Title' }];

      const response = await mockServer.invokeTool('wit_update_work_item', { id: 10, patch });

      expect(isValidToolResponse(response)).toBe(true);
      expect(mockWitApi.updateWorkItem).toHaveBeenCalledWith({}, patch, 10);
      const content = JSON.parse(response.content[0].text);
      expect(content.id).toBe(10);
    });

    it('should handle API errors', async () => {
      mockWitApi.updateWorkItem.mockRejectedValue(new Error('Update failed'));

      const response = await mockServer.invokeTool('wit_update_work_item', {
        id: 10,
        patch: [{ op: 'add', path: '/fields/System.State', value: 'Done' }]
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('Update failed');
    });

    it('should fall back to String(error) when error has no message', async () => {
      mockWitApi.updateWorkItem.mockRejectedValue({ code: 404 });

      const response = await mockServer.invokeTool('wit_update_work_item', {
        id: 10,
        patch: [{ op: 'add', path: '/fields/System.State', value: 'Done' }]
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('[object Object]');
    });
  });

  // ─── wit_create_work_item ───────────────────────────────────────────────────

  describe('wit_create_work_item', () => {
    it('should create a new work item', async () => {
      const created = { id: 200, fields: { 'System.Title': 'New Bug' } };
      mockWitApi.createWorkItem.mockResolvedValue(created);
      const patch = [{ op: 'add', path: '/fields/System.Title', value: 'New Bug' }];

      const response = await mockServer.invokeTool('wit_create_work_item', {
        project: 'MyProject',
        type: 'Bug',
        patch
      });

      expect(isValidToolResponse(response)).toBe(true);
      expect(mockWitApi.createWorkItem).toHaveBeenCalledWith({}, patch, 'MyProject', 'Bug');
      const content = JSON.parse(response.content[0].text);
      expect(content.id).toBe(200);
    });

    it('should handle API errors', async () => {
      mockWitApi.createWorkItem.mockRejectedValue(new Error('Creation failed'));

      const response = await mockServer.invokeTool('wit_create_work_item', {
        project: 'MyProject',
        type: 'Task',
        patch: [{ op: 'add', path: '/fields/System.Title', value: 'Test' }]
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('Creation failed');
    });

    it('should fall back to String(error) when error has no message', async () => {
      mockWitApi.createWorkItem.mockRejectedValue('no message');

      const response = await mockServer.invokeTool('wit_create_work_item', {
        project: 'MyProject',
        type: 'Task',
        patch: [{ op: 'add', path: '/fields/System.Title', value: 'Test' }]
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('no message');
    });
  });

  // ─── wit_add_child_work_items ───────────────────────────────────────────────

  describe('wit_add_child_work_items', () => {
    it('should add child work items to a parent', async () => {
      const updated = { id: 1, relations: [] };
      mockWitApi.updateWorkItem.mockResolvedValue(updated);

      const response = await mockServer.invokeTool('wit_add_child_work_items', {
        parentId: 1,
        childIds: [10, 11]
      });

      expect(isValidToolResponse(response)).toBe(true);
      const [, patch, parentId] = mockWitApi.updateWorkItem.mock.calls[0];
      expect(parentId).toBe(1);
      expect(patch).toHaveLength(2);
      expect(patch[0].op).toBe('add');
      expect(patch[0].value.rel).toBe('System.LinkTypes.Hierarchy-Forward');
      expect(patch[0].value.url).toContain('https://dev.azure.com/test-org/_apis/wit/workItems/10');
      expect(patch[1].value.url).toContain('https://dev.azure.com/test-org/_apis/wit/workItems/11');
    });

    it('should handle API errors', async () => {
      mockWitApi.updateWorkItem.mockRejectedValue(new Error('Link failed'));

      const response = await mockServer.invokeTool('wit_add_child_work_items', {
        parentId: 1,
        childIds: [5]
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('Link failed');
    });

    it('should fall back to String(error) when error has no message', async () => {
      mockWitApi.updateWorkItem.mockRejectedValue(42);

      const response = await mockServer.invokeTool('wit_add_child_work_items', {
        parentId: 1,
        childIds: [5]
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('42');
    });
  });

  // ─── wit_work_items_link ────────────────────────────────────────────────────

  describe('wit_work_items_link', () => {
    it('should create a link between two work items', async () => {
      const updated = { id: 100, relations: [{ rel: 'System.LinkTypes.Related' }] };
      mockWitApi.updateWorkItem.mockResolvedValue(updated);

      const response = await mockServer.invokeTool('wit_work_items_link', {
        sourceId: 100,
        targetId: 200,
        linkType: 'System.LinkTypes.Related'
      });

      expect(isValidToolResponse(response)).toBe(true);
      const [, patch, sourceId] = mockWitApi.updateWorkItem.mock.calls[0];
      expect(sourceId).toBe(100);
      expect(patch[0].value.rel).toBe('System.LinkTypes.Related');
      expect(patch[0].value.url).toContain('/_apis/wit/workItems/200');
      expect(patch[0].value.attributes).toEqual({});
    });

    it('should include comment in link attributes when provided', async () => {
      mockWitApi.updateWorkItem.mockResolvedValue({ id: 1 });

      await mockServer.invokeTool('wit_work_items_link', {
        sourceId: 1,
        targetId: 2,
        linkType: 'System.LinkTypes.Related',
        comment: 'See also'
      });

      const [, patch] = mockWitApi.updateWorkItem.mock.calls[0];
      expect(patch[0].value.attributes).toEqual({ comment: 'See also' });
    });

    it('should handle API errors', async () => {
      mockWitApi.updateWorkItem.mockRejectedValue(new Error('Link error'));

      const response = await mockServer.invokeTool('wit_work_items_link', {
        sourceId: 1,
        targetId: 2,
        linkType: 'System.LinkTypes.Related'
      });

      expect(isValidErrorResponse(response)).toBe(true);
    });

    it('should fall back to String(error) when error has no message', async () => {
      mockWitApi.updateWorkItem.mockRejectedValue('link error string');

      const response = await mockServer.invokeTool('wit_work_items_link', {
        sourceId: 1,
        targetId: 2,
        linkType: 'System.LinkTypes.Related'
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('link error string');
    });
  });

  // ─── wit_update_work_items_batch ────────────────────────────────────────────

  describe('wit_update_work_items_batch', () => {
    it('should update multiple work items and return results', async () => {
      mockWitApi.updateWorkItem
        .mockResolvedValueOnce({ id: 1, fields: {} })
        .mockResolvedValueOnce({ id: 2, fields: {} });

      const updates = [
        { id: 1, patch: [{ op: 'add', path: '/fields/System.State', value: 'Done' }] },
        { id: 2, patch: [{ op: 'add', path: '/fields/System.State', value: 'Active' }] }
      ];

      const response = await mockServer.invokeTool('wit_update_work_items_batch', { updates });

      expect(isValidToolResponse(response)).toBe(true);
      const results = JSON.parse(response.content[0].text);
      expect(results).toHaveLength(2);
      expect(results[0].success).toBe(true);
      expect(results[0].id).toBe(1);
      expect(results[1].success).toBe(true);
      expect(results[1].id).toBe(2);
    });

    it('should record failures for individual items without aborting the batch', async () => {
      mockWitApi.updateWorkItem
        .mockResolvedValueOnce({ id: 1, fields: {} })
        .mockRejectedValueOnce(new Error('Item 2 locked'));

      const updates = [
        { id: 1, patch: [{ op: 'add', path: '/fields/System.State', value: 'Done' }] },
        { id: 2, patch: [{ op: 'add', path: '/fields/System.State', value: 'Done' }] }
      ];

      const response = await mockServer.invokeTool('wit_update_work_items_batch', { updates });

      expect(isValidToolResponse(response)).toBe(true);
      const results = JSON.parse(response.content[0].text);
      expect(results[0].success).toBe(true);
      expect(results[1].success).toBe(false);
      expect(results[1].error).toBe('Item 2 locked');
    });

    it('should handle connection errors', async () => {
      getConnectionMock.mockRejectedValueOnce(new Error('Connection refused'));
      const freshServer = createMockServer();
      configureWorkItemsWriteTools(freshServer, getConnectionMock);

      const response = await freshServer.invokeTool('wit_update_work_items_batch', {
        updates: [{ id: 1, patch: [] }]
      });

      expect(isValidErrorResponse(response)).toBe(true);
    });

    it('should fall back to String(error) for connection errors without message', async () => {
      getConnectionMock.mockRejectedValueOnce('conn failed');
      const freshServer = createMockServer();
      configureWorkItemsWriteTools(freshServer, getConnectionMock);

      const response = await freshServer.invokeTool('wit_update_work_items_batch', {
        updates: [{ id: 1, patch: [] }]
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('conn failed');
    });
  });

  // ─── wit_work_item_unlink ───────────────────────────────────────────────────

  describe('wit_work_item_unlink', () => {
    it('should remove a matching relation by type', async () => {
      const workItemWithRelations = {
        id: 5,
        relations: [
          { rel: 'System.LinkTypes.Related', url: 'https://dev.azure.com/test-org/_apis/wit/workItems/10' },
          { rel: 'System.LinkTypes.Hierarchy-Forward', url: 'https://dev.azure.com/test-org/_apis/wit/workItems/20' }
        ]
      };
      mockWitApi.getWorkItem.mockResolvedValue(workItemWithRelations);
      mockWitApi.updateWorkItem.mockResolvedValue({ id: 5, relations: [] });

      const response = await mockServer.invokeTool('wit_work_item_unlink', {
        project: 'MyProject',
        id: 5,
        type: 'System.LinkTypes.Related'
      });

      expect(isValidToolResponse(response)).toBe(true);
      const patchArg = mockWitApi.updateWorkItem.mock.calls[0][1];
      expect(patchArg).toHaveLength(1);
      expect(patchArg[0].op).toBe('remove');
      expect(patchArg[0].path).toBe('/relations/0');
    });

    it('should remove a matching relation by URL', async () => {
      const targetUrl = 'https://dev.azure.com/test-org/_apis/wit/workItems/10';
      mockWitApi.getWorkItem.mockResolvedValue({
        id: 5,
        relations: [
          { rel: 'System.LinkTypes.Related', url: targetUrl }
        ]
      });
      mockWitApi.updateWorkItem.mockResolvedValue({ id: 5, relations: [] });

      const response = await mockServer.invokeTool('wit_work_item_unlink', {
        project: 'MyProject',
        id: 5,
        url: targetUrl
      });

      expect(isValidToolResponse(response)).toBe(true);
    });

    it('should return message when no matching relations found', async () => {
      mockWitApi.getWorkItem.mockResolvedValue({
        id: 5,
        relations: [{ rel: 'System.LinkTypes.Related', url: 'https://example.com/1' }]
      });

      const response = await mockServer.invokeTool('wit_work_item_unlink', {
        project: 'MyProject',
        id: 5,
        type: 'System.LinkTypes.Duplicate'
      });

      expect(isValidToolResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('No matching relations found to remove.');
    });

    it('should return message when work item has no relations', async () => {
      mockWitApi.getWorkItem.mockResolvedValue({ id: 5 });

      const response = await mockServer.invokeTool('wit_work_item_unlink', {
        project: 'MyProject',
        id: 5,
        type: 'System.LinkTypes.Related'
      });

      expect(isValidToolResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('Work item has no relations to remove.');
    });

    it('should apply removals in reverse index order', async () => {
      mockWitApi.getWorkItem.mockResolvedValue({
        id: 5,
        relations: [
          { rel: 'System.LinkTypes.Related', url: 'https://example.com/0' },
          { rel: 'System.LinkTypes.Related', url: 'https://example.com/1' },
          { rel: 'System.LinkTypes.Related', url: 'https://example.com/2' }
        ]
      });
      mockWitApi.updateWorkItem.mockResolvedValue({ id: 5, relations: [] });

      await mockServer.invokeTool('wit_work_item_unlink', {
        project: 'MyProject',
        id: 5,
        type: 'System.LinkTypes.Related'
      });

      const patchArg = mockWitApi.updateWorkItem.mock.calls[0][1];
      // Should be sorted in descending index order: 2, 1, 0
      expect(patchArg[0].path).toBe('/relations/2');
      expect(patchArg[1].path).toBe('/relations/1');
      expect(patchArg[2].path).toBe('/relations/0');
    });

    it('should handle API errors', async () => {
      mockWitApi.getWorkItem.mockRejectedValue(new Error('Unlink error'));

      const response = await mockServer.invokeTool('wit_work_item_unlink', {
        project: 'MyProject',
        id: 5,
        type: 'System.LinkTypes.Related'
      });

      expect(isValidErrorResponse(response)).toBe(true);
    });

    it('should fall back to String(error) when error has no message', async () => {
      mockWitApi.getWorkItem.mockRejectedValue({ status: 500 });

      const response = await mockServer.invokeTool('wit_work_item_unlink', {
        project: 'MyProject',
        id: 5,
        type: 'System.LinkTypes.Related'
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('[object Object]');
    });
  });

  // ─── wit_link_work_item_to_pull_request ─────────────────────────────────────

  describe('wit_link_work_item_to_pull_request', () => {
    it('should link a work item to a pull request via artifact link', async () => {
      const updated = { id: 55, relations: [{ rel: 'ArtifactLink' }] };
      mockWitApi.updateWorkItem.mockResolvedValue(updated);

      const response = await mockServer.invokeTool('wit_link_work_item_to_pull_request', {
        projectId: 'MyProject',
        repositoryId: 'my-repo',
        pullRequestId: 999,
        workItemId: 55
      });

      expect(isValidToolResponse(response)).toBe(true);
      const patchArg = mockWitApi.updateWorkItem.mock.calls[0][1];
      expect(patchArg[0].op).toBe('add');
      expect(patchArg[0].value.rel).toBe('ArtifactLink');
      expect(patchArg[0].value.url).toBe('vstfs:///Git/PullRequestId/MyProject%2Fmy-repo%2F999');
      expect(patchArg[0].value.attributes.name).toBe('Pull Request');
      expect(patchArg[0].value.attributes.comment).toContain('sc-ado');
    });

    it('should use connection.serverUrl to derive org name', async () => {
      mockConnection.serverUrl = 'https://dev.azure.com/custom-org';
      mockWitApi.updateWorkItem.mockResolvedValue({ id: 1 });

      await mockServer.invokeTool('wit_link_work_item_to_pull_request', {
        projectId: 'Proj',
        repositoryId: 'repo',
        pullRequestId: 1,
        workItemId: 1
      });

      const patchArg = mockWitApi.updateWorkItem.mock.calls[0][1];
      expect(patchArg[0].value.attributes.comment).toContain('custom-org');
    });

    it('should handle API errors', async () => {
      mockWitApi.updateWorkItem.mockRejectedValue(new Error('Link to PR failed'));

      const response = await mockServer.invokeTool('wit_link_work_item_to_pull_request', {
        projectId: 'P',
        repositoryId: 'R',
        pullRequestId: 1,
        workItemId: 1
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('Link to PR failed');
    });

    it('should fall back to String(error) when error has no message', async () => {
      mockWitApi.updateWorkItem.mockRejectedValue('pr link failed');

      const response = await mockServer.invokeTool('wit_link_work_item_to_pull_request', {
        projectId: 'P',
        repositoryId: 'R',
        pullRequestId: 1,
        workItemId: 1
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('pr link failed');
    });
  });

  // ─── wit_update_work_item_comment ───────────────────────────────────────────

  describe('wit_update_work_item_comment', () => {
    it('should update an existing work item comment', async () => {
      const updatedComment = { id: 7, text: 'Updated text' };
      mockWitApi.updateComment.mockResolvedValue(updatedComment);

      const response = await mockServer.invokeTool('wit_update_work_item_comment', {
        project: 'MyProject',
        id: 42,
        commentId: 7,
        text: 'Updated text'
      });

      expect(isValidToolResponse(response)).toBe(true);
      expect(mockWitApi.updateComment).toHaveBeenCalledWith(
        { text: 'Updated text' },
        'MyProject',
        42,
        7
      );
      const content = JSON.parse(response.content[0].text);
      expect(content.text).toBe('Updated text');
    });

    it('should handle API errors', async () => {
      mockWitApi.updateComment.mockRejectedValue(new Error('Comment not found'));

      const response = await mockServer.invokeTool('wit_update_work_item_comment', {
        project: 'MyProject',
        id: 42,
        commentId: 99,
        text: 'New text'
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('Comment not found');
    });

    it('should fall back to String(error) when error has no message', async () => {
      mockWitApi.updateComment.mockRejectedValue('comment error');

      const response = await mockServer.invokeTool('wit_update_work_item_comment', {
        project: 'MyProject',
        id: 42,
        commentId: 1,
        text: 'text'
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('comment error');
    });
  });
});
