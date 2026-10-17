import { describe, it, expect, vi, beforeEach } from 'vitest';
import { configureAdoTools } from '../src/tools.js';
import { createMockServer } from '@sc-node-mcp/shared-tests/helpers/mockServer';
import { createMockConnection } from '@sc-node-mcp/shared-tests/helpers/mockConnection';

describe('ADO Tools Configuration', () => {
  let mockServer;
  let mockConnectionProvider;

  beforeEach(() => {
    mockServer = createMockServer();
    mockConnectionProvider = vi.fn().mockResolvedValue(createMockConnection());
  });

  it('should register all ADO tools on the server', () => {
    configureAdoTools(mockServer, mockConnectionProvider);

    const tools = mockServer.getRegisteredTools();
    expect(tools.length).toBeGreaterThan(0);
  });

  it('should register work item tools', () => {
    configureAdoTools(mockServer, mockConnectionProvider);

    const toolNames = mockServer.getRegisteredTools().map(t => t.name);
    
    expect(toolNames).toContain('wit_get_work_item');
    expect(toolNames).toContain('wit_my_work_items');
    expect(toolNames).toContain('wit_list_projects');
    expect(toolNames).toContain('wit_create_work_item');
    expect(toolNames).toContain('wit_update_work_item');
  });

  it('should register repository tools', () => {
    configureAdoTools(mockServer, mockConnectionProvider);

    const toolNames = mockServer.getRegisteredTools().map(t => t.name);
    
    expect(toolNames).toContain('repo_list_repos_by_project');
    expect(toolNames).toContain('repo_list_pull_requests_by_repo_or_project');
    expect(toolNames).toContain('repo_list_branches_by_repo');
    expect(toolNames).toContain('repo_create_pull_request');
  });

  it('should register review tools', () => {
    configureAdoTools(mockServer, mockConnectionProvider);

    const toolNames = mockServer.getRegisteredTools().map(t => t.name);
    
    expect(toolNames).toContain('post_pr_comment');
    expect(toolNames).toContain('repo_review_pr');
    expect(toolNames).toContain('repo_pr_diff');
  });

  it('should register pipeline tools', () => {
    configureAdoTools(mockServer, mockConnectionProvider);

    const toolNames = mockServer.getRegisteredTools().map(t => t.name);

    expect(toolNames).toContain('pipelines_get_build_definitions');
    expect(toolNames).toContain('pipelines_run_pipeline');
    expect(toolNames).toContain('pipelines_list_runs');
    expect(toolNames).toContain('pipelines_get_run');
    expect(toolNames).toContain('pipelines_get_build_status');
    expect(toolNames).toContain('pipelines_get_builds');
    expect(toolNames).toContain('pipelines_cancel_run');
    expect(toolNames).toContain('pipelines_retry_stage');
    expect(toolNames).toContain('pipelines_list_work_item_pipelines');
  });

  it('should pass connection provider to all tool modules', () => {
    configureAdoTools(mockServer, mockConnectionProvider);

    // All tools should have been registered via server.tool()
    expect(mockServer.tool).toHaveBeenCalled();
    expect(mockServer.tool.mock.calls.length).toBeGreaterThan(0);
  });
});
