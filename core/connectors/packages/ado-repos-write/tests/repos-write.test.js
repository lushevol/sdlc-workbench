import { describe, it, expect, vi, beforeEach } from 'vitest';
import { configureReposWriteTools, clearVsspsProxyCache } from '../src/tools/repos-write.js';
import { createMockServer, isValidToolResponse, isValidErrorResponse } from '@sc-node-mcp/shared-tests/helpers/mockServer';
import { createMockConnection, createMockGitApi, createMockCoreApi, createMockWitApi } from '@sc-node-mcp/shared-tests/helpers/mockConnection';

const mockDetectProxyFor = vi.fn().mockResolvedValue('');

vi.mock('@sc-node-mcp/core', () => ({
  getConfig: vi.fn(() => ({
    AZURE_DEVOPS_ORG_URL: 'https://dev.azure.com/test-org',
    AZURE_DEVOPS_PAT: 'test-pat',
    HTTPS_PROXY: ''
  })),
  detectProxyFor: (...args) => mockDetectProxyFor(...args)
}));

vi.mock('@sc-node-mcp/ado-core/connection', () => ({
  getADOConnection: vi.fn()
}));

describe('configureReposWriteTools', () => {
  let mockServer;
  let mockConnection;
  let mockGitApi;
  let mockCoreApi;
  let mockWitApi;
  let getConnectionMock;

  beforeEach(() => {
    mockServer = createMockServer();
    mockConnection = createMockConnection();
    mockGitApi = createMockGitApi();
    mockCoreApi = createMockCoreApi();
    mockWitApi = createMockWitApi();
    clearVsspsProxyCache();
    mockDetectProxyFor.mockClear();
    mockDetectProxyFor.mockResolvedValue('');

    // Add write methods not present in default mock
    mockGitApi.updateRefs = vi.fn().mockResolvedValue([{ success: true, name: 'refs/heads/new-branch' }]);
    mockGitApi.createPullRequestLabel = vi.fn().mockResolvedValue({ name: 'label1' });
    mockGitApi.deletePullRequestReviewer = vi.fn().mockResolvedValue({});

    mockConnection.getGitApi.mockResolvedValue(mockGitApi);
    mockConnection.getCoreApi.mockResolvedValue(mockCoreApi);
    mockConnection.getWorkItemTrackingApi.mockResolvedValue(mockWitApi);

    getConnectionMock = vi.fn().mockResolvedValue(mockConnection);
    configureReposWriteTools(mockServer, getConnectionMock);
  });

  // ─── repo_create_branch ──────────────────────────────────────────────────

  describe('repo_create_branch', () => {
    it('should create a branch from an explicit source branch', async () => {
      const repo = { id: 'r1', defaultBranch: 'refs/heads/main' };
      mockGitApi.getRepository.mockResolvedValue(repo);
      mockGitApi.getBranch.mockResolvedValue({ commit: { commitId: 'abc123' } });

      const response = await mockServer.invokeTool('repo_create_branch', {
        repositoryId: 'my-repo', branchName: 'feature/new', project: 'MyProject', sourceBranchName: 'main'
      });

      expect(isValidToolResponse(response)).toBe(true);
      expect(mockGitApi.updateRefs).toHaveBeenCalledWith(
        [expect.objectContaining({ name: 'refs/heads/feature/new', newObjectId: 'abc123' })],
        'my-repo', 'MyProject'
      );
    });

    it('should create a branch from default branch when no source provided', async () => {
      const repo = { id: 'r1', defaultBranch: 'refs/heads/main' };
      mockGitApi.getRepository.mockResolvedValue(repo);
      mockGitApi.getBranch.mockResolvedValue({ commit: { commitId: 'def456' } });

      const response = await mockServer.invokeTool('repo_create_branch', {
        repositoryId: 'my-repo', branchName: 'feature/auto', project: 'P'
      });

      expect(isValidToolResponse(response)).toBe(true);
      expect(mockGitApi.updateRefs).toHaveBeenCalled();
    });

    it('should create a branch from explicit commit ID', async () => {
      const repo = { id: 'r1', defaultBranch: 'refs/heads/main' };
      mockGitApi.getRepository.mockResolvedValue(repo);

      const response = await mockServer.invokeTool('repo_create_branch', {
        repositoryId: 'my-repo', branchName: 'feature/from-commit', project: 'P', sourceCommitId: 'sha999'
      });

      expect(isValidToolResponse(response)).toBe(true);
      expect(mockGitApi.updateRefs).toHaveBeenCalledWith(
        [expect.objectContaining({ newObjectId: 'sha999' })],
        'my-repo', 'P'
      );
    });

    it('should auto-discover project when not provided', async () => {
      mockCoreApi.getProjects.mockResolvedValue([{ name: 'AutoProject' }]);
      const repo = { id: 'r1', defaultBranch: 'refs/heads/main' };
      mockGitApi.getRepository.mockResolvedValue(repo);
      mockGitApi.getBranch.mockResolvedValue({ commit: { commitId: 'abc' } });

      const response = await mockServer.invokeTool('repo_create_branch', {
        repositoryId: 'my-repo', branchName: 'feature/discovered'
      });

      expect(isValidToolResponse(response)).toBe(true);
      expect(mockCoreApi.getProjects).toHaveBeenCalled();
    });

    it('should skip project that throws during auto-discovery (catch+continue)', async () => {
      mockCoreApi.getProjects.mockResolvedValue([{ name: 'ErrorProject' }, { name: 'RealProject' }]);
      // First getRepository throws, second succeeds with repo
      mockGitApi.getRepository
        .mockRejectedValueOnce(new Error('Project access denied'))
        .mockResolvedValue({ id: 'r1', name: 'my-repo', defaultBranch: 'refs/heads/main' });
      mockGitApi.getBranch.mockResolvedValue({ commit: { commitId: 'abc' } });

      const response = await mockServer.invokeTool('repo_create_branch', {
        repositoryId: 'my-repo', branchName: 'new-branch'
      });

      expect(isValidToolResponse(response)).toBe(true);
    });

    it('should fall back to String(error) when non-Error is thrown', async () => {
      mockGitApi.getRepository.mockRejectedValue('raw branch error');

      const response = await mockServer.invokeTool('repo_create_branch', {
        repositoryId: 'r', branchName: 'feature/x', project: 'P'
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('raw branch error');
    });

    it('should handle API errors', async () => {
      mockGitApi.getRepository.mockRejectedValue(new Error('Repo not found'));

      const response = await mockServer.invokeTool('repo_create_branch', {
        repositoryId: 'missing', branchName: 'feature/x', project: 'P'
      });

      expect(isValidErrorResponse(response)).toBe(true);
    });

    it('should fall back to main when repo has no defaultBranch', async () => {
      const repo = { id: 'r1', defaultBranch: undefined };
      mockGitApi.getRepository.mockResolvedValue(repo);
      mockGitApi.getBranch.mockResolvedValue({ commit: { commitId: 'fallback' } });

      const response = await mockServer.invokeTool('repo_create_branch', {
        repositoryId: 'r', branchName: 'new-branch', project: 'P'
      });

      expect(isValidToolResponse(response)).toBe(true);
      expect(mockGitApi.getBranch).toHaveBeenCalledWith('r', 'main', 'P');
    });

    it('should skip repo with null response in auto-discovery', async () => {
      mockCoreApi.getProjects.mockResolvedValue([{ name: 'Empty' }, { name: 'Real' }]);
      // First project returns null (repo not in this project), second succeeds
      mockGitApi.getRepository
        .mockResolvedValueOnce(null)
        .mockResolvedValue({ id: 'r1', name: 'my-repo', defaultBranch: 'refs/heads/main' });
      mockGitApi.getBranch.mockResolvedValue({ commit: { commitId: 'abc' } });

      const response = await mockServer.invokeTool('repo_create_branch', {
        repositoryId: 'my-repo', branchName: 'new-branch'
      });

      expect(isValidToolResponse(response)).toBe(true);
    });
  });

  // ─── repo_create_pull_request ────────────────────────────────────────────

  describe('repo_create_pull_request', () => {
    it('should create a pull request', async () => {
      const pr = { pullRequestId: 1, title: 'My PR', artifactId: 'vstfs:///Git/...' };
      mockGitApi.createPullRequest.mockResolvedValue(pr);

      const response = await mockServer.invokeTool('repo_create_pull_request', {
        repositoryId: 'my-repo', sourceRefName: 'feature/x', targetRefName: 'main', title: 'My PR'
      });

      expect(isValidToolResponse(response)).toBe(true);
      expect(mockGitApi.createPullRequest).toHaveBeenCalledWith(
        expect.objectContaining({ sourceRefName: 'refs/heads/feature/x', targetRefName: 'refs/heads/main', title: 'My PR' }),
        'my-repo'
      );
    });

    it('should not prefix refs that already have refs/ prefix', async () => {
      const pr = { pullRequestId: 2, artifactId: 'vstfs:///' };
      mockGitApi.createPullRequest.mockResolvedValue(pr);

      await mockServer.invokeTool('repo_create_pull_request', {
        repositoryId: 'r', sourceRefName: 'refs/heads/feature', targetRefName: 'refs/heads/main', title: 'T'
      });

      expect(mockGitApi.createPullRequest).toHaveBeenCalledWith(
        expect.objectContaining({ sourceRefName: 'refs/heads/feature', targetRefName: 'refs/heads/main' }),
        'r'
      );
    });

    it('should add labels when provided', async () => {
      const pr = { pullRequestId: 3, artifactId: 'vstfs:///' };
      mockGitApi.createPullRequest.mockResolvedValue(pr);

      await mockServer.invokeTool('repo_create_pull_request', {
        repositoryId: 'r', sourceRefName: 'feature', targetRefName: 'main', title: 'T', labels: ['wip']
      });

      expect(mockGitApi.createPullRequestLabel).toHaveBeenCalledWith({ name: 'wip' }, 'r', 3);
    });

    it('should link work items when provided', async () => {
      const pr = { pullRequestId: 4, artifactId: 'vstfs:///artifact' };
      mockGitApi.createPullRequest.mockResolvedValue(pr);

      await mockServer.invokeTool('repo_create_pull_request', {
        repositoryId: 'r', sourceRefName: 'feature', targetRefName: 'main', title: 'T', workItems: [100]
      });

      expect(mockWitApi.updateWorkItem).toHaveBeenCalled();
    });

    it('should handle API errors', async () => {
      mockGitApi.createPullRequest.mockRejectedValue(new Error('Create PR failed'));

      const response = await mockServer.invokeTool('repo_create_pull_request', {
        repositoryId: 'r', sourceRefName: 'feature', targetRefName: 'main', title: 'T'
      });

      expect(isValidErrorResponse(response)).toBe(true);
    });

    it('should set forkSource when forkSourceRepositoryId provided', async () => {
      const pr = { pullRequestId: 5, artifactId: 'vstfs:///' };
      mockGitApi.createPullRequest.mockResolvedValue(pr);

      await mockServer.invokeTool('repo_create_pull_request', {
        repositoryId: 'r', sourceRefName: 'feature', targetRefName: 'main', title: 'T',
        forkSourceRepositoryId: 'fork-repo-id', isDraft: true
      });

      expect(mockGitApi.createPullRequest).toHaveBeenCalledWith(
        expect.objectContaining({ forkSource: { repository: { id: 'fork-repo-id' } }, isDraft: true }),
        'r'
      );
    });

    it('should fall back to String(error) when non-Error is thrown', async () => {
      mockGitApi.createPullRequest.mockRejectedValue('raw create-pr error');

      const response = await mockServer.invokeTool('repo_create_pull_request', {
        repositoryId: 'r', sourceRefName: 'feature', targetRefName: 'main', title: 'T'
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('raw create-pr error');
    });
  });

  // ─── repo_update_pull_request ────────────────────────────────────────────

  describe('repo_update_pull_request', () => {
    it('should update PR title and description', async () => {
      mockGitApi.getPullRequestById.mockResolvedValue({ repository: { project: { name: 'P' } } });
      mockGitApi.getPullRequest.mockResolvedValue({ createdBy: { id: 'u1' } });
      mockGitApi.updatePullRequest.mockResolvedValue({ pullRequestId: 42, title: 'Updated' });

      const response = await mockServer.invokeTool('repo_update_pull_request', {
        repositoryId: 'r', pullRequestId: 42, title: 'Updated', description: 'New desc'
      });

      expect(isValidToolResponse(response)).toBe(true);
      expect(mockGitApi.updatePullRequest).toHaveBeenCalledWith(
        expect.objectContaining({ title: 'Updated', description: 'New desc' }),
        'r', 42, 'P'
      );
    });

    it('should update PR status to abandoned', async () => {
      mockGitApi.getPullRequestById.mockResolvedValue({ repository: { project: { name: 'P' } } });
      mockGitApi.getPullRequest.mockResolvedValue({ createdBy: { id: 'u1' } });
      mockGitApi.updatePullRequest.mockResolvedValue({ status: 2 });

      await mockServer.invokeTool('repo_update_pull_request', {
        repositoryId: 'r', pullRequestId: 42, status: 'abandoned'
      });

      expect(mockGitApi.updatePullRequest).toHaveBeenCalledWith(
        expect.objectContaining({ status: 2 }), 'r', 42, 'P'
      );
    });

    it('should update PR status to active', async () => {
      mockGitApi.getPullRequestById.mockResolvedValue({ repository: { project: { name: 'P' } } });
      mockGitApi.getPullRequest.mockResolvedValue({ createdBy: { id: 'u1' } });
      mockGitApi.updatePullRequest.mockResolvedValue({ status: 1 });

      await mockServer.invokeTool('repo_update_pull_request', {
        repositoryId: 'r', pullRequestId: 42, status: 'active'
      });

      expect(mockGitApi.updatePullRequest).toHaveBeenCalledWith(
        expect.objectContaining({ status: 1 }), 'r', 42, 'P'
      );
    });

    it('should update PR status to completed', async () => {
      mockGitApi.getPullRequestById.mockResolvedValue({ repository: { project: { name: 'P' } } });
      mockGitApi.getPullRequest.mockResolvedValue({ createdBy: { id: 'u1' } });
      mockGitApi.updatePullRequest.mockResolvedValue({ status: 3 });

      await mockServer.invokeTool('repo_update_pull_request', {
        repositoryId: 'r', pullRequestId: 42, status: 'completed'
      });

      expect(mockGitApi.updatePullRequest).toHaveBeenCalledWith(
        expect.objectContaining({ status: 3 }), 'r', 42, 'P'
      );
    });

    it('should set autoComplete and mergeStrategy noFastForward', async () => {
      const createdBy = { id: 'u1' };
      mockGitApi.getPullRequestById.mockResolvedValue({ repository: { project: { name: 'P' } } });
      mockGitApi.getPullRequest.mockResolvedValue({ createdBy });
      mockGitApi.updatePullRequest.mockResolvedValue({ pullRequestId: 42 });

      await mockServer.invokeTool('repo_update_pull_request', {
        repositoryId: 'r', pullRequestId: 42, autoComplete: true,
        mergeStrategy: 'noFastForward', deleteSourceBranch: true, transitionWorkItems: true
      });

      expect(mockGitApi.updatePullRequest).toHaveBeenCalledWith(
        expect.objectContaining({
          autoCompleteSetBy: createdBy,
          completionOptions: expect.objectContaining({ mergeStrategy: 2, deleteSourceBranch: true })
        }),
        'r', 42, 'P'
      );
    });

    it('should set mergeStrategy squash', async () => {
      mockGitApi.getPullRequestById.mockResolvedValue({ repository: { project: { name: 'P' } } });
      mockGitApi.getPullRequest.mockResolvedValue({ createdBy: { id: 'u1' } });
      mockGitApi.updatePullRequest.mockResolvedValue({});

      await mockServer.invokeTool('repo_update_pull_request', {
        repositoryId: 'r', pullRequestId: 1, mergeStrategy: 'squash'
      });

      expect(mockGitApi.updatePullRequest).toHaveBeenCalledWith(
        expect.objectContaining({ completionOptions: expect.objectContaining({ mergeStrategy: 3 }) }),
        'r', 1, 'P'
      );
    });

    it('should set mergeStrategy rebase', async () => {
      mockGitApi.getPullRequestById.mockResolvedValue({ repository: { project: { name: 'P' } } });
      mockGitApi.getPullRequest.mockResolvedValue({ createdBy: { id: 'u1' } });
      mockGitApi.updatePullRequest.mockResolvedValue({});

      await mockServer.invokeTool('repo_update_pull_request', {
        repositoryId: 'r', pullRequestId: 1, mergeStrategy: 'rebase'
      });

      expect(mockGitApi.updatePullRequest).toHaveBeenCalledWith(
        expect.objectContaining({ completionOptions: expect.objectContaining({ mergeStrategy: 4 }) }),
        'r', 1, 'P'
      );
    });

    it('should set mergeStrategy rebaseMerge', async () => {
      mockGitApi.getPullRequestById.mockResolvedValue({ repository: { project: { name: 'P' } } });
      mockGitApi.getPullRequest.mockResolvedValue({ createdBy: { id: 'u1' } });
      mockGitApi.updatePullRequest.mockResolvedValue({});

      await mockServer.invokeTool('repo_update_pull_request', {
        repositoryId: 'r', pullRequestId: 1, mergeStrategy: 'rebaseMerge'
      });

      expect(mockGitApi.updatePullRequest).toHaveBeenCalledWith(
        expect.objectContaining({ completionOptions: expect.objectContaining({ mergeStrategy: 5 }) }),
        'r', 1, 'P'
      );
    });

    it('should set deleteSourceBranch without mergeStrategy', async () => {
      mockGitApi.getPullRequestById.mockResolvedValue({ repository: { project: { name: 'P' } } });
      mockGitApi.getPullRequest.mockResolvedValue({ createdBy: { id: 'u1' } });
      mockGitApi.updatePullRequest.mockResolvedValue({});

      await mockServer.invokeTool('repo_update_pull_request', {
        repositoryId: 'r', pullRequestId: 1, deleteSourceBranch: true
      });

      expect(mockGitApi.updatePullRequest).toHaveBeenCalledWith(
        expect.objectContaining({
          completionOptions: expect.objectContaining({ deleteSourceBranch: true, mergeStrategy: undefined })
        }),
        'r', 1, 'P'
      );
    });

    it('should skip auto-discover when project is provided', async () => {
      mockGitApi.getPullRequest.mockResolvedValue({ createdBy: { id: 'u1' } });
      mockGitApi.updatePullRequest.mockResolvedValue({ pullRequestId: 1 });

      await mockServer.invokeTool('repo_update_pull_request', {
        repositoryId: 'r', pullRequestId: 1, project: 'ExplicitProject', title: 'T'
      });

      expect(mockGitApi.getPullRequestById).not.toHaveBeenCalled();
      expect(mockGitApi.getPullRequest).toHaveBeenCalledWith('r', 1, 'ExplicitProject');
    });

    it('should handle API errors', async () => {
      mockGitApi.getPullRequestById.mockRejectedValue(new Error('PR not found'));

      const response = await mockServer.invokeTool('repo_update_pull_request', {
        repositoryId: 'r', pullRequestId: 999
      });

      expect(isValidErrorResponse(response)).toBe(true);
    });

    it('should fall back to String(error) when non-Error is thrown', async () => {
      mockGitApi.getPullRequestById.mockRejectedValue('raw update-pr error');

      const response = await mockServer.invokeTool('repo_update_pull_request', {
        repositoryId: 'r', pullRequestId: 1
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('raw update-pr error');
    });
  });

  // ─── repo_update_pull_request_reviewers ──────────────────────────────────

  describe('repo_update_pull_request_reviewers', () => {
    // Mocks connection.rest.create (IdentityPicker), which supports fuzzy name matching
    // unlike the legacy exact-match /_apis/identities endpoint it replaced.
    const identityPickerResult = (identities) => ({ result: { results: [{ identities }] } });

    it('should add reviewer by email', async () => {
      mockGitApi.getPullRequestById.mockResolvedValue({ repository: { project: { name: 'P' } } });
      mockConnection.rest.create.mockResolvedValue(
        identityPickerResult([{ localId: 'user-guid', displayName: 'John Doe' }])
      );
      mockGitApi.createPullRequestReviewer.mockResolvedValue({ displayName: 'John Doe', vote: 0 });

      const response = await mockServer.invokeTool('repo_update_pull_request_reviewers', {
        repositoryId: 'r', pullRequestId: 42,
        reviewerIdentifiers: ['john.doe@company.com'], action: 'add'
      });

      expect(isValidToolResponse(response)).toBe(true);
      const content = JSON.parse(response.content[0].text);
      expect(content[0].action).toBe('added');
      expect(content[0].userId).toBe('user-guid');
    });

    it('should remove reviewer', async () => {
      mockGitApi.getPullRequestById.mockResolvedValue({ repository: { project: { name: 'P' } } });
      mockConnection.rest.create.mockResolvedValue(
        identityPickerResult([{ localId: 'user-guid', displayName: 'Jane Smith' }])
      );

      const response = await mockServer.invokeTool('repo_update_pull_request_reviewers', {
        repositoryId: 'r', pullRequestId: 42,
        reviewerIdentifiers: ['jane.smith@company.com'], action: 'remove'
      });

      expect(isValidToolResponse(response)).toBe(true);
      expect(mockGitApi.deletePullRequestReviewer).toHaveBeenCalled();
      const content = JSON.parse(response.content[0].text);
      expect(content[0].action).toBe('removed');
    });

    it('should return error entry for unfound user', async () => {
      mockGitApi.getPullRequestById.mockResolvedValue({ repository: { project: { name: 'P' } } });
      mockConnection.rest.create.mockResolvedValue(identityPickerResult([]));

      const response = await mockServer.invokeTool('repo_update_pull_request_reviewers', {
        repositoryId: 'r', pullRequestId: 42,
        reviewerIdentifiers: ['unknown@company.com'], action: 'add'
      });

      expect(isValidToolResponse(response)).toBe(true);
      const content = JSON.parse(response.content[0].text);
      expect(content[0].error).toContain('User not found');
    });

    it('should convert employee ID to username before searching', async () => {
      mockGitApi.getPullRequestById.mockResolvedValue({ repository: { project: { name: 'P' } } });
      mockConnection.rest.create.mockResolvedValue(
        identityPickerResult([{ localId: 'user-guid', displayName: 'Employee' }])
      );
      mockGitApi.createPullRequestReviewer.mockResolvedValue({ displayName: 'Employee', vote: 0 });

      const response = await mockServer.invokeTool('repo_update_pull_request_reviewers', {
        repositoryId: 'r', pullRequestId: 42,
        reviewerIdentifiers: ['1540326'], action: 'add'
      });

      expect(isValidToolResponse(response)).toBe(true);
      expect(mockConnection.rest.create).toHaveBeenCalledWith(
        expect.any(String),
        expect.objectContaining({ query: '1540326@zone1.scb.net' })
      );
      const content = JSON.parse(response.content[0].text);
      expect(content[0].action).toBe('added');
    });

    it('should handle missing result in API response', async () => {
      mockGitApi.getPullRequestById.mockResolvedValue({ repository: { project: { name: 'P' } } });
      // Returns response with no result (undefined) → falls back to []
      mockConnection.rest.create.mockResolvedValue({});

      const response = await mockServer.invokeTool('repo_update_pull_request_reviewers', {
        repositoryId: 'r', pullRequestId: 42,
        reviewerIdentifiers: ['user@company.com'], action: 'add'
      });

      const content = JSON.parse(response.content[0].text);
      expect(content[0].error).toContain('User not found');
    });

    it('should use samAccountName fallback when displayName is absent', async () => {
      mockGitApi.getPullRequestById.mockResolvedValue({ repository: { project: { name: 'P' } } });
      mockConnection.rest.create.mockResolvedValue(
        identityPickerResult([{ localId: 'user-guid', displayName: null, samAccountName: 'display.user@company.com' }])
      );
      mockGitApi.createPullRequestReviewer.mockResolvedValue({ displayName: 'Display User', vote: 0 });

      const response = await mockServer.invokeTool('repo_update_pull_request_reviewers', {
        repositoryId: 'r', pullRequestId: 42,
        reviewerIdentifiers: ['display.user@company.com'], action: 'add', project: 'ExplicitProject'
      });

      expect(isValidToolResponse(response)).toBe(true);
      const content = JSON.parse(response.content[0].text);
      expect(content[0].userName).toBe('display.user@company.com');
    });

    it('should fuzzy-match a reviewer by partial display name', async () => {
      mockGitApi.getPullRequestById.mockResolvedValue({ repository: { project: { name: 'P' } } });
      mockConnection.rest.create.mockResolvedValue(
        identityPickerResult([{ localId: 'display-guid', displayName: 'Raghavan, Saravanan' }])
      );
      mockGitApi.createPullRequestReviewer.mockResolvedValue({ displayName: 'Raghavan, Saravanan', vote: 0 });

      const response = await mockServer.invokeTool('repo_update_pull_request_reviewers', {
        repositoryId: 'r', pullRequestId: 42,
        reviewerIdentifiers: ['Saravanan R'], action: 'add'
      });

      expect(isValidToolResponse(response)).toBe(true);
      const content = JSON.parse(response.content[0].text);
      expect(content[0].action).toBe('added');
    });

    it('should fall back to entityId when identity has no localId (not yet materialized)', async () => {
      mockGitApi.getPullRequestById.mockResolvedValue({ repository: { project: { name: 'P' } } });
      mockConnection.rest.create.mockResolvedValue(
        identityPickerResult([{ localId: null, entityId: 'vss.ds.v1.aad.user.abc', displayName: 'New Hire' }])
      );
      mockGitApi.createPullRequestReviewer.mockResolvedValue({ displayName: 'New Hire', vote: 0 });

      const response = await mockServer.invokeTool('repo_update_pull_request_reviewers', {
        repositoryId: 'r', pullRequestId: 42,
        reviewerIdentifiers: ['new.hire@company.com'], action: 'add'
      });

      const content = JSON.parse(response.content[0].text);
      expect(content[0].userId).toBe('vss.ds.v1.aad.user.abc');
    });

    it('should handle inner per-reviewer error', async () => {
      mockGitApi.getPullRequestById.mockResolvedValue({ repository: { project: { name: 'P' } } });
      mockConnection.rest.create.mockResolvedValue(
        identityPickerResult([{ localId: 'user-guid', displayName: 'John' }])
      );
      mockGitApi.createPullRequestReviewer.mockRejectedValue(new Error('Reviewer conflict'));

      const response = await mockServer.invokeTool('repo_update_pull_request_reviewers', {
        repositoryId: 'r', pullRequestId: 42,
        reviewerIdentifiers: ['john@company.com'], action: 'add'
      });

      expect(isValidToolResponse(response)).toBe(true);
      const content = JSON.parse(response.content[0].text);
      expect(content[0].error).toBe('Reviewer conflict');
    });

    it('should show conversion note for unfound employee ID', async () => {
      mockGitApi.getPullRequestById.mockResolvedValue({ repository: { project: { name: 'P' } } });
      mockConnection.rest.create.mockResolvedValue(identityPickerResult([]));

      const response = await mockServer.invokeTool('repo_update_pull_request_reviewers', {
        repositoryId: 'r', pullRequestId: 42,
        reviewerIdentifiers: ['9999999'], action: 'add'
      });

      const content = JSON.parse(response.content[0].text);
      expect(content[0].error).toContain('converted from 9999999');
    });

    it('should handle API errors', async () => {
      mockGitApi.getPullRequestById.mockRejectedValue(new Error('PR fetch error'));

      const response = await mockServer.invokeTool('repo_update_pull_request_reviewers', {
        repositoryId: 'r', pullRequestId: 42, reviewerIdentifiers: ['x'], action: 'add'
      });

      expect(isValidErrorResponse(response)).toBe(true);
    });

    it('should report not found when identity lookup throws', async () => {
      mockGitApi.getPullRequestById.mockResolvedValue({ repository: { project: { name: 'P' } } });
      mockConnection.rest.create.mockRejectedValue(new Error('IdentityPicker unavailable'));

      const response = await mockServer.invokeTool('repo_update_pull_request_reviewers', {
        repositoryId: 'r', pullRequestId: 42,
        reviewerIdentifiers: ['not.found@company.com'], action: 'add'
      });

      expect(isValidToolResponse(response)).toBe(true);
      const content = JSON.parse(response.content[0].text);
      expect(content[0].error).toContain('User not found');
    });

    it('should fall back to String(error) when non-Error is thrown on getPullRequestById', async () => {
      mockGitApi.getPullRequestById.mockRejectedValue('raw reviewers error');

      const response = await mockServer.invokeTool('repo_update_pull_request_reviewers', {
        repositoryId: 'r', pullRequestId: 42, reviewerIdentifiers: ['x'], action: 'add'
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('raw reviewers error');
    });
  });

  // ─── repo_vote_pull_request ──────────────────────────────────────────────

  describe('repo_vote_pull_request', () => {
    it('should cast an approve vote', async () => {
      mockGitApi.getPullRequest.mockResolvedValue({ createdBy: { id: 'u1' } });
      mockGitApi.createPullRequestReviewer.mockResolvedValue({ vote: 10 });

      const response = await mockServer.invokeTool('repo_vote_pull_request', {
        repositoryId: 'r', pullRequestId: 42, vote: 'approve'
      });

      expect(isValidToolResponse(response)).toBe(true);
      expect(mockGitApi.createPullRequestReviewer).toHaveBeenCalledWith(
        expect.objectContaining({ vote: 10 }), 'r', 42, 'u1', undefined
      );
    });

    it('should cast a reject vote', async () => {
      mockGitApi.getPullRequest.mockResolvedValue({ createdBy: { id: 'u2' } });
      mockGitApi.createPullRequestReviewer.mockResolvedValue({ vote: -10 });

      await mockServer.invokeTool('repo_vote_pull_request', {
        repositoryId: 'r', pullRequestId: 1, vote: 'reject', project: 'P'
      });

      expect(mockGitApi.createPullRequestReviewer).toHaveBeenCalledWith(
        expect.objectContaining({ vote: -10 }), 'r', 1, 'u2', 'P'
      );
    });

    it('should cast approveWithSuggestions vote', async () => {
      mockGitApi.getPullRequest.mockResolvedValue({ createdBy: { id: 'u1' } });
      mockGitApi.createPullRequestReviewer.mockResolvedValue({ vote: 5 });

      await mockServer.invokeTool('repo_vote_pull_request', {
        repositoryId: 'r', pullRequestId: 1, vote: 'approveWithSuggestions'
      });

      expect(mockGitApi.createPullRequestReviewer).toHaveBeenCalledWith(
        expect.objectContaining({ vote: 5 }), 'r', 1, 'u1', undefined
      );
    });

    it('should cast waitForAuthor vote', async () => {
      mockGitApi.getPullRequest.mockResolvedValue({ createdBy: { id: 'u1' } });
      mockGitApi.createPullRequestReviewer.mockResolvedValue({ vote: -5 });

      await mockServer.invokeTool('repo_vote_pull_request', {
        repositoryId: 'r', pullRequestId: 1, vote: 'waitForAuthor'
      });

      expect(mockGitApi.createPullRequestReviewer).toHaveBeenCalledWith(
        expect.objectContaining({ vote: -5 }), 'r', 1, 'u1', undefined
      );
    });

    it('should cast reset vote', async () => {
      mockGitApi.getPullRequest.mockResolvedValue({ createdBy: { id: 'u1' } });
      mockGitApi.createPullRequestReviewer.mockResolvedValue({ vote: 0 });

      await mockServer.invokeTool('repo_vote_pull_request', {
        repositoryId: 'r', pullRequestId: 1, vote: 'reset'
      });

      expect(mockGitApi.createPullRequestReviewer).toHaveBeenCalledWith(
        expect.objectContaining({ vote: 0 }), 'r', 1, 'u1', undefined
      );
    });

    it('should handle null createdBy in PR', async () => {
      mockGitApi.getPullRequest.mockResolvedValue({ createdBy: null });
      mockGitApi.createPullRequestReviewer.mockResolvedValue({ vote: 0 });

      const response = await mockServer.invokeTool('repo_vote_pull_request', {
        repositoryId: 'r', pullRequestId: 1, vote: 'reset'
      });

      expect(isValidToolResponse(response)).toBe(true);
      expect(mockGitApi.createPullRequestReviewer).toHaveBeenCalledWith(
        { vote: 0, id: undefined }, 'r', 1, undefined, undefined
      );
    });

    it('should handle API errors', async () => {
      mockGitApi.getPullRequest.mockRejectedValue(new Error('Vote error'));

      const response = await mockServer.invokeTool('repo_vote_pull_request', {
        repositoryId: 'r', pullRequestId: 1, vote: 'approve'
      });

      expect(isValidErrorResponse(response)).toBe(true);
    });

    it('should fall back to String(error) when non-Error is thrown', async () => {
      mockGitApi.getPullRequest.mockRejectedValue('raw vote error');

      const response = await mockServer.invokeTool('repo_vote_pull_request', {
        repositoryId: 'r', pullRequestId: 1, vote: 'approve'
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('raw vote error');
    });
  });

  // ─── repo_update_pull_request_thread ─────────────────────────────────────

  describe('repo_update_pull_request_thread', () => {
    it('should update thread status to fixed', async () => {
      mockGitApi.updateThread.mockResolvedValue({ id: 5, status: 2 });

      const response = await mockServer.invokeTool('repo_update_pull_request_thread', {
        repositoryId: 'r', pullRequestId: 42, threadId: 5, status: 'fixed'
      });

      expect(isValidToolResponse(response)).toBe(true);
      expect(mockGitApi.updateThread).toHaveBeenCalledWith({ status: 2 }, 'r', 42, 5, undefined);
      const content = JSON.parse(response.content[0].text);
      expect(content.status).toBe(2);
    });

    it('should update thread status to closed', async () => {
      mockGitApi.updateThread.mockResolvedValue({ id: 5, status: 4 });

      await mockServer.invokeTool('repo_update_pull_request_thread', {
        repositoryId: 'r', pullRequestId: 42, threadId: 5, status: 'closed', project: 'P'
      });

      expect(mockGitApi.updateThread).toHaveBeenCalledWith({ status: 4 }, 'r', 42, 5, 'P');
    });

    it('should handle API errors', async () => {
      mockGitApi.updateThread.mockRejectedValue(new Error('Thread error'));

      const response = await mockServer.invokeTool('repo_update_pull_request_thread', {
        repositoryId: 'r', pullRequestId: 1, threadId: 1, status: 'active'
      });

      expect(isValidErrorResponse(response)).toBe(true);
    });

    it('should fall back to String(error) when non-Error is thrown', async () => {
      mockGitApi.updateThread.mockRejectedValue('raw thread error');

      const response = await mockServer.invokeTool('repo_update_pull_request_thread', {
        repositoryId: 'r', pullRequestId: 1, threadId: 1, status: 'fixed'
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('raw thread error');
    });
  });

  // ─── repo_reply_to_comment ───────────────────────────────────────────────

  describe('repo_reply_to_comment', () => {
    it('should reply to a thread', async () => {
      mockGitApi.createComment.mockResolvedValue({ id: 10, content: 'Reply text' });

      const response = await mockServer.invokeTool('repo_reply_to_comment', {
        repositoryId: 'r', pullRequestId: 42, threadId: 5, content: 'Reply text'
      });

      expect(isValidToolResponse(response)).toBe(true);
      expect(mockGitApi.createComment).toHaveBeenCalledWith(
        { content: 'Reply text', commentType: 1 }, 'r', 42, 5, undefined
      );
    });

    it('should handle API errors', async () => {
      mockGitApi.createComment.mockRejectedValue(new Error('Comment error'));

      const response = await mockServer.invokeTool('repo_reply_to_comment', {
        repositoryId: 'r', pullRequestId: 1, threadId: 1, content: 'test'
      });

      expect(isValidErrorResponse(response)).toBe(true);
    });

    it('should fall back to String(error) when non-Error is thrown', async () => {
      mockGitApi.createComment.mockRejectedValue('raw reply error');

      const response = await mockServer.invokeTool('repo_reply_to_comment', {
        repositoryId: 'r', pullRequestId: 1, threadId: 1, content: 'test'
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('raw reply error');
    });
  });

  // ─── repo_create_pull_request_thread ─────────────────────────────────────

  describe('repo_create_pull_request_thread', () => {
    it('should create a general PR thread', async () => {
      mockGitApi.getPullRequestById.mockResolvedValue({ repository: { project: { name: 'P' }, id: 'repo-id', name: 'my-repo' } });
      mockGitApi.createThread.mockResolvedValue({ id: 1, comments: [{ content: 'New thread' }] });

      const response = await mockServer.invokeTool('repo_create_pull_request_thread', {
        repositoryId: 'my-repo', pullRequestId: 42, content: 'New thread'
      });

      expect(isValidToolResponse(response)).toBe(true);
      expect(mockGitApi.createThread).toHaveBeenCalledWith(
        expect.objectContaining({ comments: [{ content: 'New thread', commentType: 1 }] }),
        'my-repo', 42, 'P'
      );
    });

    it('should auto-discover repo when repositoryId matches pullRequestId', async () => {
      // pr.repository.id is null → falls back to pr.repository.name (covers BRDA:378,53,1)
      mockGitApi.getPullRequestById.mockResolvedValue({
        repository: { project: { name: 'P' }, id: null, name: 'actual-repo' }
      });
      mockGitApi.createThread.mockResolvedValue({ id: 4 });

      // repositoryId === String(pullRequestId) → should auto-discover repo from PR
      const response = await mockServer.invokeTool('repo_create_pull_request_thread', {
        repositoryId: '42', pullRequestId: 42, content: 'Thread'
      });

      expect(isValidToolResponse(response)).toBe(true);
      expect(mockGitApi.createThread).toHaveBeenCalledWith(
        expect.anything(), 'actual-repo', 42, 'P'
      );
    });

    it('should create a file-level thread with filePath but no line numbers', async () => {
      mockGitApi.getPullRequestById.mockResolvedValue({ repository: { project: { name: 'P' }, id: 'r1' } });
      mockGitApi.createThread.mockResolvedValue({ id: 5 });

      // filePath set but no rightFileStartLine/rightFileEndLine → ternaries take false branch → undefined
      await mockServer.invokeTool('repo_create_pull_request_thread', {
        repositoryId: 'r', pullRequestId: 1, content: 'General file comment',
        filePath: '/src/index.js', project: 'P'
      });

      expect(mockGitApi.createThread).toHaveBeenCalledWith(
        expect.objectContaining({
          threadContext: expect.objectContaining({
            filePath: '/src/index.js',
            rightFileStart: undefined,
            rightFileEnd: undefined
          })
        }),
        'r', 1, 'P'
      );
    });

    it('should create a file-level thread with line context', async () => {
      mockGitApi.getPullRequestById.mockResolvedValue({ repository: { project: { name: 'P' }, id: 'r1' } });
      mockGitApi.createThread.mockResolvedValue({ id: 2 });

      await mockServer.invokeTool('repo_create_pull_request_thread', {
        repositoryId: 'r', pullRequestId: 1, content: 'Line comment',
        filePath: '/src/index.js', rightFileStartLine: 10, rightFileEndLine: 10, project: 'P'
      });

      expect(mockGitApi.createThread).toHaveBeenCalledWith(
        expect.objectContaining({
          threadContext: expect.objectContaining({ filePath: '/src/index.js' })
        }),
        'r', 1, 'P'
      );
    });

    it('should create thread with status and explicit offsets', async () => {
      mockGitApi.getPullRequestById.mockResolvedValue({ repository: { project: { name: 'P' }, id: 'r1' } });
      mockGitApi.createThread.mockResolvedValue({ id: 3 });

      await mockServer.invokeTool('repo_create_pull_request_thread', {
        repositoryId: 'r', pullRequestId: 1, content: 'Comment', project: 'P',
        filePath: '/file.ts', rightFileStartLine: 5, rightFileEndLine: 7,
        rightFileStartOffset: 3, rightFileEndOffset: 8, status: 'active'
      });

      expect(mockGitApi.createThread).toHaveBeenCalledWith(
        expect.objectContaining({
          status: 1,
          threadContext: expect.objectContaining({
            rightFileStart: { line: 5, offset: 3 },
            rightFileEnd: { line: 7, offset: 8 }
          })
        }),
        'r', 1, 'P'
      );
    });

    it('should handle API errors', async () => {
      mockGitApi.getPullRequestById.mockRejectedValue(new Error('PR not found'));

      const response = await mockServer.invokeTool('repo_create_pull_request_thread', {
        repositoryId: 'r', pullRequestId: 999, content: 'comment'
      });

      expect(isValidErrorResponse(response)).toBe(true);
    });

    it('should fall back to String(error) when non-Error is thrown', async () => {
      // getPullRequestById must succeed so the inner catch doesn't wrap into Error
      mockGitApi.getPullRequestById.mockResolvedValue({ repository: { project: { name: 'P' }, id: 'r1' } });
      mockGitApi.createThread.mockRejectedValue('raw thread-create error');

      const response = await mockServer.invokeTool('repo_create_pull_request_thread', {
        repositoryId: 'r', pullRequestId: 999, content: 'comment'
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('raw thread-create error');
    });
  });

  // ─── core_get_identity_ids ───────────────────────────────────────────────

  describe('core_get_identity_ids', () => {
    it('should resolve identity by search filter using fuzzy IdentityPicker match', async () => {
      mockConnection.rest.create.mockResolvedValue({
        result: { results: [{ identities: [{ localId: 'guid-123', displayName: 'John Doe', mail: 'john.doe@company.com' }] }] }
      });

      const response = await mockServer.invokeTool('core_get_identity_ids', { searchFilter: 'john.doe' });

      expect(isValidToolResponse(response)).toBe(true);
      expect(mockConnection.rest.create).toHaveBeenCalledWith(
        expect.stringContaining('vssps.dev.azure.com'),
        expect.objectContaining({ query: 'john.doe' })
      );
      const content = JSON.parse(response.content[0].text);
      expect(content.value[0].id).toBe('guid-123');
      expect(content.count).toBe(1);
    });

    it('should fall back to entityId when identity has no localId', async () => {
      mockConnection.rest.create.mockResolvedValue({
        result: { results: [{ identities: [{ localId: null, entityId: 'vss.ds.v1.aad.user.abc', displayName: 'New Hire' }] }] }
      });

      const response = await mockServer.invokeTool('core_get_identity_ids', { searchFilter: 'new hire' });

      const content = JSON.parse(response.content[0].text);
      expect(content.value[0].id).toBe('vss.ds.v1.aad.user.abc');
      expect(content.value[0].isLocal).toBe(false);
    });

    it('should return an empty list when no identities match', async () => {
      mockConnection.rest.create.mockResolvedValue({ result: { results: [{ identities: [] }] } });

      const response = await mockServer.invokeTool('core_get_identity_ids', { searchFilter: 'nobody' });

      const content = JSON.parse(response.content[0].text);
      expect(content).toEqual({ count: 0, value: [] });
    });

    it('should retry a two-word query in "Surname, Firstname" order when the plain query has no matches', async () => {
      mockConnection.rest.create
        .mockResolvedValueOnce({ result: { results: [{ identities: [] }] } }) // "Saravanan R3" — no match
        .mockResolvedValueOnce(                                              // "R3, Saravanan" — matches
          { result: { results: [{ identities: [{ localId: 'guid-r3', displayName: 'R3, Saravanan' }] }] } }
        );

      const response = await mockServer.invokeTool('core_get_identity_ids', { searchFilter: 'Saravanan R3' });

      expect(mockConnection.rest.create).toHaveBeenNthCalledWith(2,
        expect.any(String), expect.objectContaining({ query: 'R3, Saravanan' })
      );
      const content = JSON.parse(response.content[0].text);
      expect(content.value[0].id).toBe('guid-r3');
    });

    it('should try the other comma order when the first swap also has no matches', async () => {
      mockConnection.rest.create
        .mockResolvedValueOnce({ result: { results: [{ identities: [] }] } }) // "R3 Saravanan" — no match
        .mockResolvedValueOnce({ result: { results: [{ identities: [] }] } }) // "Saravanan, R3" — no match
        .mockResolvedValueOnce(                                              // "R3, Saravanan" — matches
          { result: { results: [{ identities: [{ localId: 'guid-r3', displayName: 'R3, Saravanan' }] }] } }
        );

      const response = await mockServer.invokeTool('core_get_identity_ids', { searchFilter: 'R3 Saravanan' });

      expect(mockConnection.rest.create).toHaveBeenCalledTimes(3);
      const content = JSON.parse(response.content[0].text);
      expect(content.value[0].id).toBe('guid-r3');
    });

    it('should not retry a query that already contains a comma', async () => {
      mockConnection.rest.create.mockResolvedValue({ result: { results: [{ identities: [] }] } });

      const response = await mockServer.invokeTool('core_get_identity_ids', { searchFilter: 'Saravanan, R3' });

      expect(mockConnection.rest.create).toHaveBeenCalledTimes(1);
      const content = JSON.parse(response.content[0].text);
      expect(content).toEqual({ count: 0, value: [] });
    });

    it('should not retry a single-word query with no matches', async () => {
      mockConnection.rest.create.mockResolvedValue({ result: { results: [{ identities: [] }] } });

      const response = await mockServer.invokeTool('core_get_identity_ids', { searchFilter: 'Nobody' });

      expect(mockConnection.rest.create).toHaveBeenCalledTimes(1);
      const content = JSON.parse(response.content[0].text);
      expect(content).toEqual({ count: 0, value: [] });
    });

    it('should handle API errors', async () => {
      mockConnection.rest.create.mockRejectedValue(new Error('Identity API error'));

      const response = await mockServer.invokeTool('core_get_identity_ids', { searchFilter: 'unknown' });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('Identity API error');
    });

    it('should handle non-Error throws', async () => {
      mockConnection.rest.create.mockRejectedValue(null);

      const response = await mockServer.invokeTool('core_get_identity_ids', { searchFilter: 'x' });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('null');
    });
  });

  // ─── vssps proxy handling ─────────────────────────────────────────────────
  // vssps.dev.azure.com is a different host than the one the shared startup proxy
  // auto-detection probes, so identity lookups resolve their own proxy independently.

  describe('vssps proxy resolution for identity lookups', () => {
    it('detects a proxy for vssps.dev.azure.com and applies it only for the duration of the call', async () => {
      mockDetectProxyFor.mockResolvedValue('http://vssps-proxy:443');
      let observedProxyDuringCall;
      mockConnection.rest.create.mockImplementation(async () => {
        observedProxyDuringCall = process.env.HTTPS_PROXY;
        return { result: { results: [{ identities: [{ localId: 'guid-123', displayName: 'John Doe' }] }] } };
      });
      process.env.HTTPS_PROXY = 'http://original-proxy:443';

      const response = await mockServer.invokeTool('core_get_identity_ids', { searchFilter: 'john.doe' });

      expect(mockDetectProxyFor).toHaveBeenCalledWith('vssps.dev.azure.com', '');
      expect(observedProxyDuringCall).toBe('http://vssps-proxy:443');
      expect(process.env.HTTPS_PROXY).toBe('http://original-proxy:443');
      expect(isValidToolResponse(response)).toBe(true);

      delete process.env.HTTPS_PROXY;
    });

    it('removes HTTPS_PROXY during the call when no proxy is needed, then restores the prior value', async () => {
      mockDetectProxyFor.mockResolvedValue('');
      let observedProxyDuringCall = 'unset';
      mockConnection.rest.create.mockImplementation(async () => {
        observedProxyDuringCall = process.env.HTTPS_PROXY;
        return { result: { results: [{ identities: [] }] } };
      });
      process.env.HTTPS_PROXY = 'http://original-proxy:443';

      await mockServer.invokeTool('core_get_identity_ids', { searchFilter: 'nobody' });

      expect(observedProxyDuringCall).toBeUndefined();
      expect(process.env.HTTPS_PROXY).toBe('http://original-proxy:443');

      delete process.env.HTTPS_PROXY;
    });

    it('restores HTTPS_PROXY correctly even when the identity call throws', async () => {
      mockDetectProxyFor.mockResolvedValue('http://vssps-proxy:443');
      mockConnection.rest.create.mockRejectedValue(new Error('boom'));
      process.env.HTTPS_PROXY = 'http://original-proxy:443';

      await mockServer.invokeTool('core_get_identity_ids', { searchFilter: 'x' });

      expect(process.env.HTTPS_PROXY).toBe('http://original-proxy:443');

      delete process.env.HTTPS_PROXY;
    });

    it('restores a prior lowercase https_proxy value after the call', async () => {
      mockDetectProxyFor.mockResolvedValue('http://vssps-proxy:443');
      mockConnection.rest.create.mockResolvedValue({ result: { results: [{ identities: [] }] } });
      process.env.https_proxy = 'http://original-lowercase-proxy:443';

      await mockServer.invokeTool('core_get_identity_ids', { searchFilter: 'x' });

      expect(process.env.https_proxy).toBe('http://original-lowercase-proxy:443');

      delete process.env.https_proxy;
    });

    it('only detects the vssps proxy once across multiple identity lookups', async () => {
      mockConnection.rest.create.mockResolvedValue({ result: { results: [{ identities: [] }] } });

      await mockServer.invokeTool('core_get_identity_ids', { searchFilter: 'first' });
      await mockServer.invokeTool('core_get_identity_ids', { searchFilter: 'second' });

      expect(mockDetectProxyFor).toHaveBeenCalledTimes(1);
    });
  });
});
