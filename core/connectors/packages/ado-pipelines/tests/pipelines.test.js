import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { configurePipelineTools, PIPELINE_TOOLS } from '../src/tools/pipelines.js';
import { configurePipelineTools as configurePipelineToolsOrchestrator } from '../src/tools.js';
import { configurePipelinePrompts } from '../src/prompts.js';
import { createMockServer, isValidToolResponse, isValidErrorResponse } from '@sc-node-mcp/shared-tests/helpers/mockServer';
import { createMockConnection, createMockBuildApi, createMockPipelinesApi, createMockTaskAgentApi } from '@sc-node-mcp/shared-tests/helpers/mockConnection';

vi.mock('@sc-node-mcp/core', () => ({
  getConfig: vi.fn().mockReturnValue({ AZURE_DEVOPS_PAT: 'test-pat' }),
  createMcpServer: vi.fn(),
  startMcpServer: vi.fn()
}));

vi.mock('@sc-node-mcp/ado-core/connection', () => ({
  getADOConnection: vi.fn()
}));

describe('Pipeline Tools', () => {
  let mockServer;
  let mockConnection;
  let mockBuildApi;
  let mockPipelinesApi;
  let mockTaskAgentApi;
  let getConnectionMock;

  beforeEach(() => {
    mockServer = createMockServer();
    mockConnection = createMockConnection();
    mockBuildApi = createMockBuildApi();
    mockPipelinesApi = createMockPipelinesApi();
    mockTaskAgentApi = createMockTaskAgentApi();
    mockConnection.getBuildApi.mockResolvedValue(mockBuildApi);
    mockConnection.getPipelinesApi.mockResolvedValue(mockPipelinesApi);
    mockConnection.getTaskAgentApi.mockResolvedValue(mockTaskAgentApi);
    mockConnection.serverUrl = 'https://dev.azure.com/sc-ado';
    getConnectionMock = vi.fn().mockResolvedValue(mockConnection);
    configurePipelineTools(mockServer, getConnectionMock);
  });

  describe('pipelines_get_build_definitions', () => {
    it('should return build definitions for a project', async () => {
      const definitions = [{ id: 1, name: 'CI Pipeline' }, { id: 2, name: 'CD Pipeline' }];
      mockBuildApi.getDefinitions.mockResolvedValue(definitions);

      const response = await mockServer.invokeTool(PIPELINE_TOOLS.get_build_definitions, { project: 'TestProject' });

      expect(isValidToolResponse(response)).toBe(true);
      const result = JSON.parse(response.content[0].text);
      expect(result).toHaveLength(2);
      expect(result[0].name).toBe('CI Pipeline');
    });

    it('should filter by name, repositoryId, repositoryType, and top', async () => {
      mockBuildApi.getDefinitions.mockResolvedValue([{ id: 1, name: 'CI Pipeline' }]);

      const response = await mockServer.invokeTool(PIPELINE_TOOLS.get_build_definitions, {
        project: 'TestProject',
        name: 'CI Pipeline',
        repositoryId: 'repo-123',
        repositoryType: 'TfsGit',
        top: 10
      });

      expect(isValidToolResponse(response)).toBe(true);
      expect(mockBuildApi.getDefinitions).toHaveBeenCalledWith(
        'TestProject', 'CI Pipeline', 'repo-123', 'TfsGit', undefined, 10
      );
    });

    it('should return error on API failure', async () => {
      mockBuildApi.getDefinitions.mockRejectedValue(new Error('API error'));

      const response = await mockServer.invokeTool(PIPELINE_TOOLS.get_build_definitions, { project: 'TestProject' });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('API error');
    });

    it('should use String() when rejection has no message property', async () => {
      mockBuildApi.getDefinitions.mockRejectedValue({ toString: () => 'raw definitions error' });

      const response = await mockServer.invokeTool(PIPELINE_TOOLS.get_build_definitions, { project: 'TestProject' });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('raw definitions error');
    });
  });

  describe('pipelines_run_pipeline', () => {
    it('should trigger a pipeline run', async () => {
      const run = { id: 100, state: 'inProgress' };
      mockPipelinesApi.runPipeline.mockResolvedValue(run);

      const response = await mockServer.invokeTool(PIPELINE_TOOLS.run_pipeline, {
        project: 'TestProject',
        pipelineId: 1
      });

      expect(isValidToolResponse(response)).toBe(true);
      const result = JSON.parse(response.content[0].text);
      expect(result.id).toBe(100);
      expect(result.state).toBe('inProgress');
    });

    it('should normalize branch name without refs/heads/ prefix', async () => {
      mockPipelinesApi.runPipeline.mockResolvedValue({ id: 100 });

      await mockServer.invokeTool(PIPELINE_TOOLS.run_pipeline, {
        project: 'TestProject',
        pipelineId: 1,
        branchName: 'main'
      });

      const callArgs = mockPipelinesApi.runPipeline.mock.calls[0][0];
      expect(callArgs.resources.repositories.self.refName).toBe('refs/heads/main');
    });

    it('should not double-prefix an already-normalized branch name', async () => {
      mockPipelinesApi.runPipeline.mockResolvedValue({ id: 100 });

      await mockServer.invokeTool(PIPELINE_TOOLS.run_pipeline, {
        project: 'TestProject',
        pipelineId: 1,
        branchName: 'refs/heads/main'
      });

      const callArgs = mockPipelinesApi.runPipeline.mock.calls[0][0];
      expect(callArgs.resources.repositories.self.refName).toBe('refs/heads/main');
    });

    it('should pass templateParameters, variables, and stagesToSkip', async () => {
      mockPipelinesApi.runPipeline.mockResolvedValue({ id: 100 });

      await mockServer.invokeTool(PIPELINE_TOOLS.run_pipeline, {
        project: 'TestProject',
        pipelineId: 1,
        templateParameters: { env: 'prod' },
        variables: { myVar: { value: 'myVal', isSecret: false } },
        stagesToSkip: ['QA']
      });

      const callArgs = mockPipelinesApi.runPipeline.mock.calls[0][0];
      expect(callArgs.templateParameters).toEqual({ env: 'prod' });
      expect(callArgs.variables).toEqual({ myVar: { value: 'myVal', isSecret: false } });
      expect(callArgs.stagesToSkip).toEqual(['QA']);
    });

    it('should not add resources when no branchName is given', async () => {
      mockPipelinesApi.runPipeline.mockResolvedValue({ id: 100 });

      await mockServer.invokeTool(PIPELINE_TOOLS.run_pipeline, {
        project: 'TestProject',
        pipelineId: 1
      });

      const callArgs = mockPipelinesApi.runPipeline.mock.calls[0][0];
      expect(callArgs.resources).toBeUndefined();
    });

    it('should return error on API failure', async () => {
      mockPipelinesApi.runPipeline.mockRejectedValue(new Error('Pipeline not found'));

      const response = await mockServer.invokeTool(PIPELINE_TOOLS.run_pipeline, {
        project: 'TestProject',
        pipelineId: 999
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('Pipeline not found');
    });

    it('should use String() when rejection has no message property', async () => {
      mockPipelinesApi.runPipeline.mockRejectedValue({ toString: () => 'raw run error' });

      const response = await mockServer.invokeTool(PIPELINE_TOOLS.run_pipeline, {
        project: 'TestProject',
        pipelineId: 1
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('raw run error');
    });
  });

  describe('pipelines_list_runs (with pipelineId — uses Pipelines API)', () => {
    it('should list all runs for a specific pipeline', async () => {
      const runs = [{ id: 1, state: 'completed' }, { id: 2, state: 'inProgress' }];
      mockPipelinesApi.listRuns.mockResolvedValue(runs);

      const response = await mockServer.invokeTool(PIPELINE_TOOLS.list_runs, {
        project: 'TestProject',
        pipelineId: 1,
        statusFilter: 'all'
      });

      expect(isValidToolResponse(response)).toBe(true);
      const result = JSON.parse(response.content[0].text);
      expect(result).toHaveLength(2);
    });

    it('should filter runs by inProgress status', async () => {
      const runs = [
        { id: 1, state: 'completed' },
        { id: 2, state: 'inProgress' }
      ];
      mockPipelinesApi.listRuns.mockResolvedValue(runs);

      const response = await mockServer.invokeTool(PIPELINE_TOOLS.list_runs, {
        project: 'TestProject',
        pipelineId: 1,
        statusFilter: 'inProgress'
      });

      const result = JSON.parse(response.content[0].text);
      expect(result).toHaveLength(1);
      expect(result[0].id).toBe(2);
    });

    it('should filter runs by branch after normalizing name', async () => {
      const runs = [
        { id: 1, resources: { repositories: { self: { refName: 'refs/heads/main' } } } },
        { id: 2, resources: { repositories: { self: { refName: 'refs/heads/feature/x' } } } }
      ];
      mockPipelinesApi.listRuns.mockResolvedValue(runs);

      const response = await mockServer.invokeTool(PIPELINE_TOOLS.list_runs, {
        project: 'TestProject',
        pipelineId: 1,
        branchName: 'main'
      });

      const result = JSON.parse(response.content[0].text);
      expect(result).toHaveLength(1);
      expect(result[0].id).toBe(1);
    });

    it('should return error on API failure', async () => {
      mockPipelinesApi.listRuns.mockRejectedValue(new Error('Unauthorized'));

      const response = await mockServer.invokeTool(PIPELINE_TOOLS.list_runs, {
        project: 'TestProject',
        pipelineId: 1
      });

      expect(isValidErrorResponse(response)).toBe(true);
    });

    it('should not double-prefix branchName already starting with refs/', async () => {
      const runs = [
        { id: 1, resources: { repositories: { self: { refName: 'refs/heads/main' } } } }
      ];
      mockPipelinesApi.listRuns.mockResolvedValue(runs);

      const response = await mockServer.invokeTool(PIPELINE_TOOLS.list_runs, {
        project: 'TestProject',
        pipelineId: 1,
        branchName: 'refs/heads/main'
      });

      const result = JSON.parse(response.content[0].text);
      expect(result).toHaveLength(1);
    });

    it('should filter runs by completed status using Pipelines API', async () => {
      const runs = [
        { id: 1, state: 'completed' },
        { id: 2, state: 'inProgress' }
      ];
      mockPipelinesApi.listRuns.mockResolvedValue(runs);

      const response = await mockServer.invokeTool(PIPELINE_TOOLS.list_runs, {
        project: 'TestProject',
        pipelineId: 1,
        statusFilter: 'completed'
      });

      const result = JSON.parse(response.content[0].text);
      expect(result).toHaveLength(1);
      expect(result[0].id).toBe(1);
    });

    it('should filter runs by cancelling status using Pipelines API', async () => {
      const runs = [
        { id: 1, state: 'cancelling' },
        { id: 2, state: 'inProgress' }
      ];
      mockPipelinesApi.listRuns.mockResolvedValue(runs);

      const response = await mockServer.invokeTool(PIPELINE_TOOLS.list_runs, {
        project: 'TestProject',
        pipelineId: 1,
        statusFilter: 'cancelling'
      });

      const result = JSON.parse(response.content[0].text);
      expect(result).toHaveLength(1);
      expect(result[0].id).toBe(1);
    });

    it('should use String() when rejection has no message property (Pipelines API path)', async () => {
      mockPipelinesApi.listRuns.mockRejectedValue({ toString: () => 'raw list runs error' });

      const response = await mockServer.invokeTool(PIPELINE_TOOLS.list_runs, {
        project: 'TestProject',
        pipelineId: 1
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('raw list runs error');
    });
  });

  describe('pipelines_list_runs (without pipelineId — uses Build API)', () => {
    it('should list all builds in project using Build API', async () => {
      const builds = [{ id: 10, buildNumber: '1.0.1' }, { id: 11, buildNumber: '1.0.2' }];
      mockBuildApi.getBuilds.mockResolvedValue(builds);

      const response = await mockServer.invokeTool(PIPELINE_TOOLS.list_runs, {
        project: 'TestProject',
        statusFilter: 'all'
      });

      expect(isValidToolResponse(response)).toBe(true);
      const result = JSON.parse(response.content[0].text);
      expect(result).toHaveLength(2);
    });

    it('should map statusFilter "inProgress" to Build API enum value 1', async () => {
      mockBuildApi.getBuilds.mockResolvedValue([]);

      await mockServer.invokeTool(PIPELINE_TOOLS.list_runs, {
        project: 'TestProject',
        statusFilter: 'inProgress'
      });

      expect(mockBuildApi.getBuilds.mock.calls[0][8]).toBe(1);
    });

    it('should map statusFilter "completed" to Build API enum value 2', async () => {
      mockBuildApi.getBuilds.mockResolvedValue([]);

      await mockServer.invokeTool(PIPELINE_TOOLS.list_runs, {
        project: 'TestProject',
        statusFilter: 'completed'
      });

      expect(mockBuildApi.getBuilds.mock.calls[0][8]).toBe(2);
    });

    it('should normalize branch name when using Build API', async () => {
      mockBuildApi.getBuilds.mockResolvedValue([]);

      await mockServer.invokeTool(PIPELINE_TOOLS.list_runs, {
        project: 'TestProject',
        branchName: 'main',
        statusFilter: 'all'
      });

      expect(mockBuildApi.getBuilds.mock.calls[0][17]).toBe('refs/heads/main');
    });

    it('should map statusFilter "cancelling" to Build API enum value 32', async () => {
      mockBuildApi.getBuilds.mockResolvedValue([]);

      await mockServer.invokeTool(PIPELINE_TOOLS.list_runs, {
        project: 'TestProject',
        statusFilter: 'cancelling'
      });

      expect(mockBuildApi.getBuilds.mock.calls[0][8]).toBe(32);
    });

    it('should use String() when rejection has no message property (Build API path)', async () => {
      mockBuildApi.getBuilds.mockRejectedValue({ toString: () => 'raw build list error' });

      const response = await mockServer.invokeTool(PIPELINE_TOOLS.list_runs, {
        project: 'TestProject'
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('raw build list error');
    });
  });

  describe('pipelines_get_run', () => {
    it('should get details of a specific pipeline run', async () => {
      const run = { id: 789, state: 'completed', result: 'succeeded' };
      mockPipelinesApi.getRun.mockResolvedValue(run);

      const response = await mockServer.invokeTool(PIPELINE_TOOLS.get_run, {
        project: 'TestProject',
        pipelineId: 123,
        runId: 789
      });

      expect(isValidToolResponse(response)).toBe(true);
      const result = JSON.parse(response.content[0].text);
      expect(result.id).toBe(789);
      expect(result.result).toBe('succeeded');
      expect(mockPipelinesApi.getRun).toHaveBeenCalledWith('TestProject', 123, 789);
    });

    it('should return error when run is not found', async () => {
      mockPipelinesApi.getRun.mockRejectedValue(new Error('Run not found'));

      const response = await mockServer.invokeTool(PIPELINE_TOOLS.get_run, {
        project: 'TestProject',
        pipelineId: 123,
        runId: 999
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('Run not found');
    });

    it('should use String() when rejection has no message property', async () => {
      mockPipelinesApi.getRun.mockRejectedValue({ toString: () => 'raw get run error' });

      const response = await mockServer.invokeTool(PIPELINE_TOOLS.get_run, {
        project: 'TestProject',
        pipelineId: 123,
        runId: 999
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('raw get run error');
    });
  });

  describe('pipelines_get_build_status', () => {
    it('should get build status by build ID', async () => {
      const build = { id: 456, status: 'completed', result: 'succeeded' };
      mockBuildApi.getBuild.mockResolvedValue(build);

      const response = await mockServer.invokeTool(PIPELINE_TOOLS.get_build_status, {
        project: 'TestProject',
        buildId: 456
      });

      expect(isValidToolResponse(response)).toBe(true);
      const result = JSON.parse(response.content[0].text);
      expect(result.id).toBe(456);
      expect(result.status).toBe('completed');
      expect(mockBuildApi.getBuild).toHaveBeenCalledWith('TestProject', 456);
    });

    it('should return error when build is not found', async () => {
      mockBuildApi.getBuild.mockRejectedValue(new Error('Build not found'));

      const response = await mockServer.invokeTool(PIPELINE_TOOLS.get_build_status, {
        project: 'TestProject',
        buildId: 999
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('Build not found');
    });

    it('should use String() when rejection has no message property', async () => {
      mockBuildApi.getBuild.mockRejectedValue({ toString: () => 'raw status error' });

      const response = await mockServer.invokeTool(PIPELINE_TOOLS.get_build_status, {
        project: 'TestProject',
        buildId: 999
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('raw status error');
    });
  });

  describe('pipelines_get_builds', () => {
    it('should get builds with all filters applied', async () => {
      const builds = [{ id: 1 }, { id: 2 }];
      mockBuildApi.getBuilds.mockResolvedValue(builds);

      const response = await mockServer.invokeTool(PIPELINE_TOOLS.get_builds, {
        project: 'TestProject',
        definitions: [123],
        branchName: 'main',
        statusFilter: 'completed',
        resultFilter: 'succeeded',
        top: 10
      });

      expect(isValidToolResponse(response)).toBe(true);
      const result = JSON.parse(response.content[0].text);
      expect(result).toHaveLength(2);
    });

    it('should map resultFilter "failed" to enum value 8', async () => {
      mockBuildApi.getBuilds.mockResolvedValue([]);

      await mockServer.invokeTool(PIPELINE_TOOLS.get_builds, {
        project: 'TestProject',
        resultFilter: 'failed'
      });

      expect(mockBuildApi.getBuilds.mock.calls[0][9]).toBe(8);
    });

    it('should map resultFilter "succeeded" to enum value 2', async () => {
      mockBuildApi.getBuilds.mockResolvedValue([]);

      await mockServer.invokeTool(PIPELINE_TOOLS.get_builds, {
        project: 'TestProject',
        resultFilter: 'succeeded'
      });

      expect(mockBuildApi.getBuilds.mock.calls[0][9]).toBe(2);
    });

    it('should map resultFilter "partiallySucceeded" to enum value 4', async () => {
      mockBuildApi.getBuilds.mockResolvedValue([]);

      await mockServer.invokeTool(PIPELINE_TOOLS.get_builds, {
        project: 'TestProject',
        resultFilter: 'partiallySucceeded'
      });

      expect(mockBuildApi.getBuilds.mock.calls[0][9]).toBe(4);
    });

    it('should normalize branch name', async () => {
      mockBuildApi.getBuilds.mockResolvedValue([]);

      await mockServer.invokeTool(PIPELINE_TOOLS.get_builds, {
        project: 'TestProject',
        branchName: 'develop'
      });

      expect(mockBuildApi.getBuilds.mock.calls[0][17]).toBe('refs/heads/develop');
    });

    it('should return error on API failure', async () => {
      mockBuildApi.getBuilds.mockRejectedValue(new Error('Unauthorized'));

      const response = await mockServer.invokeTool(PIPELINE_TOOLS.get_builds, {
        project: 'TestProject'
      });

      expect(isValidErrorResponse(response)).toBe(true);
    });

    it('should map statusFilter "inProgress" to enum value 1', async () => {
      mockBuildApi.getBuilds.mockResolvedValue([]);

      await mockServer.invokeTool(PIPELINE_TOOLS.get_builds, {
        project: 'TestProject',
        statusFilter: 'inProgress'
      });

      expect(mockBuildApi.getBuilds.mock.calls[0][8]).toBe(1);
    });

    it('should map statusFilter "cancelling" to enum value 32', async () => {
      mockBuildApi.getBuilds.mockResolvedValue([]);

      await mockServer.invokeTool(PIPELINE_TOOLS.get_builds, {
        project: 'TestProject',
        statusFilter: 'cancelling'
      });

      expect(mockBuildApi.getBuilds.mock.calls[0][8]).toBe(32);
    });

    it('should map statusFilter "notStarted" to enum value 8', async () => {
      mockBuildApi.getBuilds.mockResolvedValue([]);

      await mockServer.invokeTool(PIPELINE_TOOLS.get_builds, {
        project: 'TestProject',
        statusFilter: 'notStarted'
      });

      expect(mockBuildApi.getBuilds.mock.calls[0][8]).toBe(8);
    });

    it('should map resultFilter "canceled" to enum value 32', async () => {
      mockBuildApi.getBuilds.mockResolvedValue([]);

      await mockServer.invokeTool(PIPELINE_TOOLS.get_builds, {
        project: 'TestProject',
        resultFilter: 'canceled'
      });

      expect(mockBuildApi.getBuilds.mock.calls[0][9]).toBe(32);
    });

    it('should pass already-prefixed branchName unchanged', async () => {
      mockBuildApi.getBuilds.mockResolvedValue([]);

      await mockServer.invokeTool(PIPELINE_TOOLS.get_builds, {
        project: 'TestProject',
        branchName: 'refs/heads/main'
      });

      expect(mockBuildApi.getBuilds.mock.calls[0][17]).toBe('refs/heads/main');
    });

    it('should use String() when rejection has no message property', async () => {
      mockBuildApi.getBuilds.mockRejectedValue({ toString: () => 'raw builds error' });

      const response = await mockServer.invokeTool(PIPELINE_TOOLS.get_builds, {
        project: 'TestProject'
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('raw builds error');
    });
  });

  describe('pipelines_cancel_run', () => {
    it('should cancel a running pipeline build', async () => {
      const cancelledBuild = { id: 789, status: 32 };
      mockBuildApi.updateBuild.mockResolvedValue(cancelledBuild);

      const response = await mockServer.invokeTool(PIPELINE_TOOLS.cancel_run, {
        project: 'TestProject',
        buildId: 789
      });

      expect(isValidToolResponse(response)).toBe(true);
      const result = JSON.parse(response.content[0].text);
      expect(result.message).toContain('cancellation');
      expect(result.build.id).toBe(789);
      expect(mockBuildApi.updateBuild).toHaveBeenCalledWith(
        { status: 32 }, 'TestProject', 789
      );
    });

    it('should return error when build cannot be cancelled', async () => {
      mockBuildApi.updateBuild.mockRejectedValue(new Error('Cannot cancel completed build'));

      const response = await mockServer.invokeTool(PIPELINE_TOOLS.cancel_run, {
        project: 'TestProject',
        buildId: 999
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('Cannot cancel completed build');
    });

    it('should use String() when rejection has no message property', async () => {
      mockBuildApi.updateBuild.mockRejectedValue({ toString: () => 'raw cancel error' });

      const response = await mockServer.invokeTool(PIPELINE_TOOLS.cancel_run, {
        project: 'TestProject',
        buildId: 999
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('raw cancel error');
    });
  });

  describe('pipelines_retry_stage', () => {
    afterEach(() => {
      vi.unstubAllGlobals();
    });

    it('should retry a pipeline stage via REST PATCH', async () => {
      const mockFetch = vi.fn().mockResolvedValue({
        ok: true,
        json: vi.fn().mockResolvedValue({ stageReference: { stageName: 'Deploy' } })
      });
      vi.stubGlobal('fetch', mockFetch);

      const response = await mockServer.invokeTool(PIPELINE_TOOLS.retry_stage, {
        project: 'TestProject',
        buildId: 789,
        stageName: 'Deploy',
        forceRetryAllJobs: true
      });

      expect(isValidToolResponse(response)).toBe(true);
      const result = JSON.parse(response.content[0].text);
      expect(result.message).toContain('Deploy');
      expect(mockFetch).toHaveBeenCalledWith(
        expect.stringContaining('/TestProject/_apis/build/builds/789/stages/Deploy'),
        expect.objectContaining({ method: 'PATCH' })
      );
    });

    it('should send forceRetryAllJobs in request body', async () => {
      const mockFetch = vi.fn().mockResolvedValue({
        ok: true,
        json: vi.fn().mockResolvedValue({})
      });
      vi.stubGlobal('fetch', mockFetch);

      await mockServer.invokeTool(PIPELINE_TOOLS.retry_stage, {
        project: 'TestProject',
        buildId: 789,
        stageName: 'Deploy',
        forceRetryAllJobs: true
      });

      const fetchCallBody = JSON.parse(mockFetch.mock.calls[0][1].body);
      expect(fetchCallBody.forceRetryAllJobs).toBe(true);
      expect(fetchCallBody.state).toBe('retry');
    });

    it('should return error when fetch response is not ok', async () => {
      const mockFetch = vi.fn().mockResolvedValue({
        ok: false,
        status: 400,
        text: vi.fn().mockResolvedValue('Bad request')
      });
      vi.stubGlobal('fetch', mockFetch);

      const response = await mockServer.invokeTool(PIPELINE_TOOLS.retry_stage, {
        project: 'TestProject',
        buildId: 789,
        stageName: 'Deploy'
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('Failed to retry stage');
    });

    it('should use String() when fetch itself rejects without Error', async () => {
      const mockFetch = vi.fn().mockRejectedValue({ toString: () => 'network failure' });
      vi.stubGlobal('fetch', mockFetch);

      const response = await mockServer.invokeTool(PIPELINE_TOOLS.retry_stage, {
        project: 'TestProject',
        buildId: 789,
        stageName: 'Deploy'
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('network failure');
    });
  });

  describe('pipelines_list_work_item_pipelines', () => {
    it('should find builds linked to a specific work item', async () => {
      const builds = [
        { id: 1, buildNumber: '1.0.1', definition: { name: 'CI', id: 10 }, status: 'completed', result: 'succeeded', _links: { web: { href: 'https://example.com/build/1' } } },
        { id: 2, buildNumber: '1.0.2', definition: { name: 'CI', id: 10 }, status: 'completed', result: 'succeeded', _links: {} }
      ];
      mockBuildApi.getBuilds.mockResolvedValue(builds);
      mockBuildApi.getBuildWorkItemsRefs.mockResolvedValueOnce([{ id: '12345' }, { id: '99999' }]);
      mockBuildApi.getBuildWorkItemsRefs.mockResolvedValueOnce([{ id: '11111' }]);

      const response = await mockServer.invokeTool(PIPELINE_TOOLS.list_work_item_pipelines, {
        project: 'TestProject',
        workItemId: 12345
      });

      expect(isValidToolResponse(response)).toBe(true);
      const result = JSON.parse(response.content[0].text);
      expect(result.workItemId).toBe(12345);
      expect(result.totalBuildsFound).toBe(1);
      expect(result.builds[0].buildId).toBe(1);
      expect(result.builds[0].buildNumber).toBe('1.0.1');
    });

    it('should return empty builds when no builds are linked to the work item', async () => {
      mockBuildApi.getBuilds.mockResolvedValue([
        { id: 1, buildNumber: '1.0.1', _links: {} }
      ]);
      mockBuildApi.getBuildWorkItemsRefs.mockResolvedValue([{ id: '99999' }]);

      const response = await mockServer.invokeTool(PIPELINE_TOOLS.list_work_item_pipelines, {
        project: 'TestProject',
        workItemId: 12345
      });

      expect(isValidToolResponse(response)).toBe(true);
      const result = JSON.parse(response.content[0].text);
      expect(result.totalBuildsFound).toBe(0);
      expect(result.builds).toHaveLength(0);
    });

    it('should continue gracefully when getBuildWorkItemsRefs throws for a build', async () => {
      mockBuildApi.getBuilds.mockResolvedValue([{ id: 1, buildNumber: '1.0.1', _links: {} }]);
      mockBuildApi.getBuildWorkItemsRefs.mockRejectedValue(new Error('Access denied'));

      const response = await mockServer.invokeTool(PIPELINE_TOOLS.list_work_item_pipelines, {
        project: 'TestProject',
        workItemId: 12345
      });

      expect(isValidToolResponse(response)).toBe(true);
      const result = JSON.parse(response.content[0].text);
      expect(result.totalBuildsFound).toBe(0);
    });

    it('should return error when getBuilds API fails', async () => {
      mockBuildApi.getBuilds.mockRejectedValue(new Error('Project not found'));

      const response = await mockServer.invokeTool(PIPELINE_TOOLS.list_work_item_pipelines, {
        project: 'TestProject',
        workItemId: 12345
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('Project not found');
    });

    it('should use fallback URL when build has no _links.web.href', async () => {
      const builds = [
        { id: 5, buildNumber: '2.0.0', definition: { name: 'CD', id: 20 }, status: 'completed', result: 'succeeded', _links: {} }
      ];
      mockBuildApi.getBuilds.mockResolvedValue(builds);
      mockBuildApi.getBuildWorkItemsRefs.mockResolvedValue([{ id: '12345' }]);

      const response = await mockServer.invokeTool(PIPELINE_TOOLS.list_work_item_pipelines, {
        project: 'TestProject',
        workItemId: 12345
      });

      expect(isValidToolResponse(response)).toBe(true);
      const result = JSON.parse(response.content[0].text);
      expect(result.totalBuildsFound).toBe(1);
      expect(result.builds[0].url).toContain('dev.azure.com');
    });

    it('should use String() when rejection has no message property', async () => {
      mockBuildApi.getBuilds.mockRejectedValue({ toString: () => 'raw work item error' });

      const response = await mockServer.invokeTool(PIPELINE_TOOLS.list_work_item_pipelines, {
        project: 'TestProject',
        workItemId: 12345
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('raw work item error');
    });
  });

  describe('get_build_log', () => {
    it('should return concatenated log output for a build', async () => {
      mockBuildApi.getBuildLogs.mockResolvedValue([
        { id: 1, type: 'container' },
        { id: 2, type: 'step' }
      ]);
      mockBuildApi.getBuildLogLines.mockResolvedValue(['Starting...', 'Done.']);

      const response = await mockServer.invokeTool(PIPELINE_TOOLS.get_build_log, {
        project: 'TestProject',
        buildId: 42
      });

      expect(isValidToolResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('Log 1');
      expect(response.content[0].text).toContain('Log 2');
    });

    it('should return notice when no logs exist for a build', async () => {
      mockBuildApi.getBuildLogs.mockResolvedValue([]);

      const response = await mockServer.invokeTool(PIPELINE_TOOLS.get_build_log, {
        project: 'TestProject',
        buildId: 99
      });

      expect(isValidToolResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('No logs found');
    });

    it('should return notice when getBuildLogs returns null', async () => {
      mockBuildApi.getBuildLogs.mockResolvedValue(null);

      const response = await mockServer.invokeTool(PIPELINE_TOOLS.get_build_log, {
        project: 'TestProject',
        buildId: 99
      });

      expect(isValidToolResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('No logs found');
    });

    it('should return error when getBuildLogs API fails', async () => {
      mockBuildApi.getBuildLogs.mockRejectedValue(new Error('Logs unavailable'));

      const response = await mockServer.invokeTool(PIPELINE_TOOLS.get_build_log, {
        project: 'TestProject',
        buildId: 42
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('Logs unavailable');
    });

    it('should fall back to "step" when log type is absent', async () => {
      mockBuildApi.getBuildLogs.mockResolvedValue([{ id: 1 }]);
      mockBuildApi.getBuildLogLines.mockResolvedValue(['line1']);

      const response = await mockServer.invokeTool(PIPELINE_TOOLS.get_build_log, {
        project: 'TestProject',
        buildId: 42
      });

      expect(isValidToolResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('(step)');
    });

    it('should use String() when rejection has no message property', async () => {
      mockBuildApi.getBuildLogs.mockRejectedValue({ toString: () => 'raw log error' });

      const response = await mockServer.invokeTool(PIPELINE_TOOLS.get_build_log, {
        project: 'TestProject',
        buildId: 42
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('raw log error');
    });
  });

  describe('get_build_changes', () => {
    it('should return changes associated with a build', async () => {
      mockBuildApi.getBuildChanges.mockResolvedValue([
        { id: 'abc123', message: 'Fix bug', author: { displayName: 'Dev' } }
      ]);

      const response = await mockServer.invokeTool(PIPELINE_TOOLS.get_build_changes, {
        project: 'TestProject',
        buildId: 42
      });

      expect(isValidToolResponse(response)).toBe(true);
      const result = JSON.parse(response.content[0].text);
      expect(result).toHaveLength(1);
      expect(result[0].id).toBe('abc123');
    });

    it('should respect top parameter when fetching changes', async () => {
      mockBuildApi.getBuildChanges.mockResolvedValue([]);

      const response = await mockServer.invokeTool(PIPELINE_TOOLS.get_build_changes, {
        project: 'TestProject',
        buildId: 42,
        top: 5
      });

      expect(isValidToolResponse(response)).toBe(true);
      expect(mockBuildApi.getBuildChanges).toHaveBeenCalledWith('TestProject', 42, undefined, 5, true);
    });

    it('should return error when getBuildChanges API fails', async () => {
      mockBuildApi.getBuildChanges.mockRejectedValue(new Error('Access denied'));

      const response = await mockServer.invokeTool(PIPELINE_TOOLS.get_build_changes, {
        project: 'TestProject',
        buildId: 42
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('Access denied');
    });

    it('should use String() when rejection has no message property', async () => {
      mockBuildApi.getBuildChanges.mockRejectedValue({ toString: () => 'raw changes error' });

      const response = await mockServer.invokeTool(PIPELINE_TOOLS.get_build_changes, {
        project: 'TestProject',
        buildId: 42
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('raw changes error');
    });
  });

  describe('list_artifacts', () => {
    it('should return list of artifacts for a build', async () => {
      mockBuildApi.getArtifacts.mockResolvedValue([
        { id: 1, name: 'drop', resource: { url: 'https://example.com/drop.zip' } }
      ]);

      const response = await mockServer.invokeTool(PIPELINE_TOOLS.list_artifacts, {
        project: 'TestProject',
        buildId: 42
      });

      expect(isValidToolResponse(response)).toBe(true);
      const result = JSON.parse(response.content[0].text);
      expect(result).toHaveLength(1);
      expect(result[0].name).toBe('drop');
    });

    it('should return error when getArtifacts API fails', async () => {
      mockBuildApi.getArtifacts.mockRejectedValue(new Error('Not found'));

      const response = await mockServer.invokeTool(PIPELINE_TOOLS.list_artifacts, {
        project: 'TestProject',
        buildId: 42
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('Not found');
    });

    it('should use String() when rejection has no message property', async () => {
      mockBuildApi.getArtifacts.mockRejectedValue({ toString: () => 'raw artifacts error' });

      const response = await mockServer.invokeTool(PIPELINE_TOOLS.list_artifacts, {
        project: 'TestProject',
        buildId: 42
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('raw artifacts error');
    });
  });

  describe('pipelines_list_variable_groups', () => {
    it('should list variable groups for a project', async () => {
      const groups = [{ id: 1, name: 'Common Vars' }, { id: 2, name: 'Prod Vars' }];
      mockTaskAgentApi.getVariableGroups.mockResolvedValue(groups);

      const response = await mockServer.invokeTool(PIPELINE_TOOLS.list_variable_groups, { project: 'TestProject' });

      expect(isValidToolResponse(response)).toBe(true);
      expect(mockTaskAgentApi.getVariableGroups).toHaveBeenCalledWith('TestProject', undefined, undefined, undefined);
      const result = JSON.parse(response.content[0].text);
      expect(result).toHaveLength(2);
    });

    it('should filter by groupName and top', async () => {
      mockTaskAgentApi.getVariableGroups.mockResolvedValue([]);

      await mockServer.invokeTool(PIPELINE_TOOLS.list_variable_groups, { project: 'TestProject', groupName: 'Prod', top: 5 });

      expect(mockTaskAgentApi.getVariableGroups).toHaveBeenCalledWith('TestProject', 'Prod', undefined, 5);
    });

    it('should handle API errors', async () => {
      mockTaskAgentApi.getVariableGroups.mockRejectedValue(new Error('Library unavailable'));

      const response = await mockServer.invokeTool(PIPELINE_TOOLS.list_variable_groups, { project: 'TestProject' });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('Library unavailable');
    });
  });

  describe('pipelines_get_variable_group', () => {
    it('should get a variable group by ID', async () => {
      const group = { id: 7, name: 'Common Vars', variables: { key: { value: 'val' } } };
      mockTaskAgentApi.getVariableGroup.mockResolvedValue(group);

      const response = await mockServer.invokeTool(PIPELINE_TOOLS.get_variable_group, { project: 'TestProject', groupId: 7 });

      expect(isValidToolResponse(response)).toBe(true);
      expect(mockTaskAgentApi.getVariableGroup).toHaveBeenCalledWith('TestProject', 7);
      const result = JSON.parse(response.content[0].text);
      expect(result.id).toBe(7);
    });

    it('should handle API errors', async () => {
      mockTaskAgentApi.getVariableGroup.mockRejectedValue(new Error('Group not found'));

      const response = await mockServer.invokeTool(PIPELINE_TOOLS.get_variable_group, { project: 'TestProject', groupId: 999 });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('Group not found');
    });
  });

  describe('configurePipelineTools orchestrator', () => {
    it('should register all pipeline tools via tools.js', () => {
      const server = createMockServer();
      configurePipelineToolsOrchestrator(server, getConnectionMock);
      expect(server.getRegisteredTools().length).toBeGreaterThan(0);
    });
  });

  describe('configurePipelinePrompts', () => {
    it('should register pipeline prompts on the server', () => {
      const server = createMockServer();
      server.prompt = vi.fn();
      configurePipelinePrompts(server);
      expect(server.prompt).toHaveBeenCalled();
    });

    it('should invoke prompt callbacks and cover message generators', async () => {
      const storedCallbacks = new Map();
      const server = createMockServer();
      server.prompt = vi.fn((name, _desc, _args, callback) => {
        storedCallbacks.set(name, callback);
      });
      configurePipelinePrompts(server);
      expect(storedCallbacks.size).toBeGreaterThan(0);

      const result = await storedCallbacks.get('run-pipeline')({ pipelineId: '5', project: 'MyProject' });
      expect(result.messages[0].content.text).toContain('pipelines_run_pipeline');

      const statusResult = await storedCallbacks.get('get-pipeline-status')({ buildId: '10', project: 'MyProject' });
      expect(statusResult.messages[0].content.text).toContain('pipelines_get_build_status');

      const logsResult = await storedCallbacks.get('get-build-logs')({ buildId: '10', project: 'MyProject' });
      expect(logsResult.messages[0].content.text).toContain('pipelines_get_build_log');

      const changesResult = await storedCallbacks.get('get-build-changes')({ buildId: '10', project: 'MyProject' });
      expect(changesResult.messages[0].content.text).toContain('pipelines_get_build_changes');

      const artifactsResult = await storedCallbacks.get('list-build-artifacts')({ buildId: '10', project: 'MyProject' });
      expect(artifactsResult.messages[0].content.text).toContain('pipelines_list_artifacts');

      const runResult = await storedCallbacks.get('get-pipeline-run')({ pipelineId: '5', runId: '3', project: 'MyProject' });
      expect(runResult.messages[0].content.text).toContain('pipelines_get_run');

      const retryResult = await storedCallbacks.get('retry-pipeline-stage')({ buildId: '10', stageName: 'Build', project: 'MyProject' });
      expect(retryResult.messages[0].content.text).toContain('pipelines_retry_stage');

      // Cover the remaining 5 message generators
      const listRunsResult = await storedCallbacks.get('list-pipeline-runs')({ project: 'MyProject', pipelineId: '5', branchName: 'main', statusFilter: 'completed' });
      expect(listRunsResult.messages[0].content.text).toContain('pipelines_list_runs');

      const cancelResult = await storedCallbacks.get('cancel-pipeline')({ buildId: '10', project: 'MyProject' });
      expect(cancelResult.messages[0].content.text).toContain('pipelines_cancel_run');

      const definitionsResult = await storedCallbacks.get('list-build-definitions')({ project: 'MyProject', name: 'MyPipeline', repositoryId: 'repo-1' });
      expect(definitionsResult.messages[0].content.text).toContain('pipelines_get_build_definitions');

      const buildsResult = await storedCallbacks.get('get-builds')({ project: 'MyProject', branchName: 'main', statusFilter: 'completed', resultFilter: 'succeeded' });
      expect(buildsResult.messages[0].content.text).toContain('pipelines_get_builds');

      const witPipelinesResult = await storedCallbacks.get('list-work-item-pipelines')({ workItemId: '123', project: 'MyProject' });
      expect(witPipelinesResult.messages[0].content.text).toContain('pipelines_list_work_item_pipelines');

      // Cover retry with forceRetryAllJobs
      const forceRetryResult = await storedCallbacks.get('retry-pipeline-stage')({ buildId: '10', stageName: 'Build', project: 'MyProject', forceRetryAllJobs: 'true' });
      expect(forceRetryResult.messages[0].content.text).toContain('forceRetryAllJobs');

      // Cover the 2 variable-group (Library) message generators
      const listGroupsResult = await storedCallbacks.get('list-variable-groups')({ project: 'MyProject' });
      expect(listGroupsResult.messages[0].content.text).toContain('pipelines_list_variable_groups');

      const listGroupsFilteredResult = await storedCallbacks.get('list-variable-groups')({ project: 'MyProject', groupName: 'Prod' });
      expect(listGroupsFilteredResult.messages[0].content.text).toContain('groupName "Prod"');

      const getGroupResult = await storedCallbacks.get('get-variable-group')({ project: 'MyProject', groupId: '7' });
      expect(getGroupResult.messages[0].content.text).toContain('pipelines_get_variable_group');
    });

    it('should use context to fill project when not provided in args', async () => {
      const storedCallbacks = new Map();
      const server = createMockServer();
      server.prompt = vi.fn((name, _desc, _args, callback) => {
        storedCallbacks.set(name, callback);
      });
      const getContext = vi.fn().mockReturnValue({ ado: { project: 'CtxProject' } });
      configurePipelinePrompts(server, { getContext });

      const result = await storedCallbacks.get('run-pipeline')({ pipelineId: '5' });
      expect(result.messages[0].content.text).toContain('CtxProject');
    });

    it('should use context for all generators when project not in args', async () => {
      const storedCallbacks = new Map();
      const server = createMockServer();
      server.prompt = vi.fn((name, _desc, _args, cb) => storedCallbacks.set(name, cb));
      const getContext = vi.fn().mockReturnValue({ ado: { project: 'CtxProject' } });
      configurePipelinePrompts(server, { getContext });

      // Call all generators without project to cover ctx?.ado?.project branch in each
      for (const [, cb] of storedCallbacks) {
        const r = await cb({ buildId: '1', pipelineId: '1', runId: '1', workItemId: '1', stageName: 'S', groupId: '1' });
        expect(r.messages[0].content.text).toContain('CtxProject');
      }
    });

    it('should fall back to (required) when no project in args or context', async () => {
      const storedCallbacks = new Map();
      const server = createMockServer();
      server.prompt = vi.fn((name, _desc, _args, cb) => storedCallbacks.set(name, cb));
      // Default getContext = () => null — no context available
      configurePipelinePrompts(server);

      // Call all generators with undefined args — covers args ?? {}, '(required)' fallback,
      // and all optional-param ternary null/'') paths
      for (const [, cb] of storedCallbacks) {
        const r = await cb(undefined);
        expect(r.messages[0].content.text).toContain('(required)');
      }
    });

    it('should include optional params in prompt text when provided', async () => {
      const storedCallbacks = new Map();
      const server = createMockServer();
      server.prompt = vi.fn((name, _desc, _args, cb) => storedCallbacks.set(name, cb));
      configurePipelinePrompts(server);

      // run-pipeline with branchName covers L117 and L118 truthy ternary paths
      const r1 = await storedCallbacks.get('run-pipeline')({ project: 'P', pipelineId: '1', branchName: 'main' });
      expect(r1.messages[0].content.text).toContain('main');

      // get-build-logs with filter covers L164 truthy ternary
      const r2 = await storedCallbacks.get('get-build-logs')({ project: 'P', buildId: '1', filter: 'error' });
      expect(r2.messages[0].content.text).toContain('error');

      // get-build-changes with top covers L169 truthy ternary
      const r3 = await storedCallbacks.get('get-build-changes')({ project: 'P', buildId: '1', top: '10' });
      expect(r3.messages[0].content.text).toContain('10');
    });
  });
});
