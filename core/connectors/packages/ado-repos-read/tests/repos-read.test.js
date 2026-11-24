import { describe, it, expect, vi, beforeEach } from 'vitest';
import { configureReposReadTools } from '../src/tools/repos-read.js';
import { createMockServer, isValidToolResponse, isValidErrorResponse } from '@sc-node-mcp/shared-tests/helpers/mockServer';
import { createMockConnection, createMockGitApi, createMockCoreApi } from '@sc-node-mcp/shared-tests/helpers/mockConnection';

vi.mock('@sc-node-mcp/core', () => ({
  getConfig: vi.fn(() => ({
    AZURE_DEVOPS_ORG_URL: 'https://dev.azure.com/test-org',
    AZURE_DEVOPS_PAT: 'test-pat'
  }))
}));

vi.mock('@sc-node-mcp/ado-core/connection', () => ({
  getADOConnection: vi.fn()
}));

describe('configureReposReadTools', () => {
  let mockServer;
  let mockConnection;
  let mockGitApi;
  let mockCoreApi;
  let getConnectionMock;

  beforeEach(() => {
    mockServer = createMockServer();
    mockConnection = createMockConnection();
    mockGitApi = createMockGitApi();
    mockCoreApi = createMockCoreApi();

    // Add methods not present in the default mock
    mockGitApi.getPullRequestsByProject = vi.fn().mockResolvedValue([]);
    mockGitApi.getPullRequestWorkItemRefs = vi.fn().mockResolvedValue([]);

    mockConnection.getGitApi.mockResolvedValue(mockGitApi);
    mockConnection.getCoreApi.mockResolvedValue(mockCoreApi);

    getConnectionMock = vi.fn().mockResolvedValue(mockConnection);
    configureReposReadTools(mockServer, getConnectionMock);
  });

  // ─── repo_list_repos_by_project ───────────────────────────────────────────

  describe('repo_list_repos_by_project', () => {
    it('should list repositories for a project', async () => {
      const repos = [{ id: 'r1', name: 'my-repo' }, { id: 'r2', name: 'other-repo' }];
      mockGitApi.getRepositories.mockResolvedValue(repos);

      const response = await mockServer.invokeTool('repo_list_repos_by_project', { project: 'MyProject' });

      expect(isValidToolResponse(response)).toBe(true);
      expect(mockGitApi.getRepositories).toHaveBeenCalledWith('MyProject');
      const content = JSON.parse(response.content[0].text);
      expect(content).toHaveLength(2);
    });

    it('should filter repos by name', async () => {
      const repos = [{ id: 'r1', name: 'my-repo' }, { id: 'r2', name: 'other-repo' }];
      mockGitApi.getRepositories.mockResolvedValue(repos);

      const response = await mockServer.invokeTool('repo_list_repos_by_project', { project: 'MyProject', repoNameFilter: 'my' });

      expect(isValidToolResponse(response)).toBe(true);
      const content = JSON.parse(response.content[0].text);
      expect(content).toHaveLength(1);
      expect(content[0].name).toBe('my-repo');
    });

    it('should apply skip and top pagination', async () => {
      const repos = [{ id: 'r1' }, { id: 'r2' }, { id: 'r3' }, { id: 'r4' }];
      mockGitApi.getRepositories.mockResolvedValue(repos);

      const response = await mockServer.invokeTool('repo_list_repos_by_project', { project: 'MyProject', skip: 1, top: 2 });

      expect(isValidToolResponse(response)).toBe(true);
      const content = JSON.parse(response.content[0].text);
      expect(content).toHaveLength(2);
      expect(content[0].id).toBe('r2');
    });

    it('should handle API errors', async () => {
      mockGitApi.getRepositories.mockRejectedValue(new Error('API error'));

      const response = await mockServer.invokeTool('repo_list_repos_by_project', { project: 'MyProject' });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('API error');
    });

    it('should handle non-Error throws', async () => {
      mockGitApi.getRepositories.mockRejectedValue(null);

      const response = await mockServer.invokeTool('repo_list_repos_by_project', { project: 'MyProject' });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('null');
    });
  });

  // ─── repo_list_pull_requests_by_repo_or_project ───────────────────────────

  describe('repo_list_pull_requests_by_repo_or_project', () => {
    it('should list PRs by repositoryId', async () => {
      const prs = [{ pullRequestId: 1 }, { pullRequestId: 2 }];
      mockGitApi.getPullRequests.mockResolvedValue(prs);

      const response = await mockServer.invokeTool('repo_list_pull_requests_by_repo_or_project', { repositoryId: 'my-repo' });

      expect(isValidToolResponse(response)).toBe(true);
      expect(mockGitApi.getPullRequests).toHaveBeenCalled();
      const content = JSON.parse(response.content[0].text);
      expect(content).toHaveLength(2);
    });

    it('should list PRs by project', async () => {
      const prs = [{ pullRequestId: 3 }];
      mockGitApi.getPullRequestsByProject.mockResolvedValue(prs);

      const response = await mockServer.invokeTool('repo_list_pull_requests_by_repo_or_project', { project: 'MyProject' });

      expect(isValidToolResponse(response)).toBe(true);
      expect(mockGitApi.getPullRequestsByProject).toHaveBeenCalledWith('MyProject', expect.any(Object));
    });

    it('should apply status filter for completed PRs', async () => {
      mockGitApi.getPullRequests.mockResolvedValue([]);

      await mockServer.invokeTool('repo_list_pull_requests_by_repo_or_project', { repositoryId: 'r', status: 'completed' });

      expect(mockGitApi.getPullRequests).toHaveBeenCalledWith('r', expect.objectContaining({ status: 3 }), undefined);
    });

    it('should not set status for all filter', async () => {
      mockGitApi.getPullRequests.mockResolvedValue([]);

      await mockServer.invokeTool('repo_list_pull_requests_by_repo_or_project', { repositoryId: 'r', status: 'all' });

      expect(mockGitApi.getPullRequests).toHaveBeenCalledWith('r', expect.not.objectContaining({ status: expect.anything() }), undefined);
    });

    it('should apply reviewer and creator filters', async () => {
      mockGitApi.getPullRequests.mockResolvedValue([]);

      await mockServer.invokeTool('repo_list_pull_requests_by_repo_or_project', {
        repositoryId: 'r', created_by_user: 'uid1', user_is_reviewer: 'uid2', skip: 5, top: 10
      });

      expect(mockGitApi.getPullRequests).toHaveBeenCalledWith('r', expect.objectContaining({
        creatorId: 'uid1', reviewerId: 'uid2', skip: 5, top: 10
      }), undefined);
    });

    it('should apply sourceRefName and targetRefName filters', async () => {
      mockGitApi.getPullRequests.mockResolvedValue([]);

      await mockServer.invokeTool('repo_list_pull_requests_by_repo_or_project', {
        repositoryId: 'r', sourceRefName: 'refs/heads/feature', targetRefName: 'refs/heads/main'
      });

      expect(mockGitApi.getPullRequests).toHaveBeenCalledWith('r', expect.objectContaining({
        sourceRefName: 'refs/heads/feature', targetRefName: 'refs/heads/main'
      }), undefined);
    });

    it('should apply abandoned status', async () => {
      mockGitApi.getPullRequests.mockResolvedValue([]);

      await mockServer.invokeTool('repo_list_pull_requests_by_repo_or_project', { repositoryId: 'r', status: 'abandoned' });

      expect(mockGitApi.getPullRequests).toHaveBeenCalledWith('r', expect.objectContaining({ status: 2 }), undefined);
    });

    it('should apply status filter', async () => {
      mockGitApi.getPullRequests.mockResolvedValue([]);

      await mockServer.invokeTool('repo_list_pull_requests_by_repo_or_project', { repositoryId: 'r', status: 'active' });

      expect(mockGitApi.getPullRequests).toHaveBeenCalledWith('r', expect.objectContaining({ status: 1 }), undefined);
    });

    it('should error when neither repositoryId nor project provided', async () => {
      const response = await mockServer.invokeTool('repo_list_pull_requests_by_repo_or_project', {});

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('Either repositoryId or project must be provided');
    });

    it('should handle API errors', async () => {
      mockGitApi.getPullRequests.mockRejectedValue(new Error('Network error'));

      const response = await mockServer.invokeTool('repo_list_pull_requests_by_repo_or_project', { repositoryId: 'my-repo' });

      expect(isValidErrorResponse(response)).toBe(true);
    });

    it('should handle non-Error throws', async () => {
      mockGitApi.getPullRequests.mockRejectedValue(undefined);

      const response = await mockServer.invokeTool('repo_list_pull_requests_by_repo_or_project', { repositoryId: 'r' });

      expect(isValidErrorResponse(response)).toBe(true);
    });
  });

  // ─── repo_list_branches_by_repo ──────────────────────────────────────────

  describe('repo_list_branches_by_repo', () => {
    it('should list branches with explicit project', async () => {
      const branches = [{ name: 'main' }, { name: 'feature/x' }];
      mockGitApi.getBranches.mockResolvedValue(branches);

      const response = await mockServer.invokeTool('repo_list_branches_by_repo', { repositoryId: 'my-repo', project: 'MyProject' });

      expect(isValidToolResponse(response)).toBe(true);
      expect(mockGitApi.getBranches).toHaveBeenCalledWith('my-repo', 'MyProject');
      const content = JSON.parse(response.content[0].text);
      expect(content).toHaveLength(2);
    });

    it('should auto-discover project when not provided', async () => {
      mockCoreApi.getProjects.mockResolvedValue([{ name: 'DiscoveredProject' }]);
      mockGitApi.getRepository.mockResolvedValue({ id: 'r1', name: 'my-repo' });
      mockGitApi.getBranches.mockResolvedValue([{ name: 'main' }]);

      const response = await mockServer.invokeTool('repo_list_branches_by_repo', { repositoryId: 'my-repo' });

      expect(isValidToolResponse(response)).toBe(true);
      expect(mockCoreApi.getProjects).toHaveBeenCalled();
    });

    it('should error when repo not found in any project', async () => {
      mockCoreApi.getProjects.mockResolvedValue([{ name: 'SomeProject' }]);
      mockGitApi.getRepository.mockRejectedValue(new Error('Not found'));

      const response = await mockServer.invokeTool('repo_list_branches_by_repo', { repositoryId: 'unknown-repo' });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('not found in any project');
    });

    it('should filter branches by name', async () => {
      mockGitApi.getBranches.mockResolvedValue([{ name: 'main' }, { name: 'feature/search' }, { name: 'hotfix/bug' }]);

      const response = await mockServer.invokeTool('repo_list_branches_by_repo', { repositoryId: 'my-repo', project: 'P', filterContains: 'feature' });

      expect(isValidToolResponse(response)).toBe(true);
      const content = JSON.parse(response.content[0].text);
      expect(content).toHaveLength(1);
      expect(content[0].name).toBe('feature/search');
    });

    it('should apply top limit', async () => {
      mockGitApi.getBranches.mockResolvedValue([{ name: 'b1' }, { name: 'b2' }, { name: 'b3' }]);

      const response = await mockServer.invokeTool('repo_list_branches_by_repo', { repositoryId: 'my-repo', project: 'P', top: 2 });

      const content = JSON.parse(response.content[0].text);
      expect(content).toHaveLength(2);
    });

    it('should handle API errors', async () => {
      mockGitApi.getBranches.mockRejectedValue(new Error('Git API error'));

      const response = await mockServer.invokeTool('repo_list_branches_by_repo', { repositoryId: 'my-repo', project: 'P' });

      expect(isValidErrorResponse(response)).toBe(true);
    });

    it('should handle non-Error throws', async () => {
      mockGitApi.getBranches.mockRejectedValue(null);

      const response = await mockServer.invokeTool('repo_list_branches_by_repo', { repositoryId: 'r', project: 'P' });

      expect(isValidErrorResponse(response)).toBe(true);
    });
  });

  // ─── repo_list_my_branches_by_repo ───────────────────────────────────────

  describe('repo_list_my_branches_by_repo', () => {
    it('should list branches with project', async () => {
      mockGitApi.getBranches.mockResolvedValue([{ name: 'main' }, { name: 'feature/mine' }]);

      const response = await mockServer.invokeTool('repo_list_my_branches_by_repo', { repositoryId: 'my-repo', project: 'MyProject' });

      expect(isValidToolResponse(response)).toBe(true);
      expect(mockGitApi.getBranches).toHaveBeenCalled();
    });

    it('should filter and apply top', async () => {
      mockGitApi.getBranches.mockResolvedValue([{ name: 'feature/a' }, { name: 'feature/b' }, { name: 'main' }]);

      const response = await mockServer.invokeTool('repo_list_my_branches_by_repo', { repositoryId: 'my-repo', project: 'P', filterContains: 'feature', top: 1 });

      const content = JSON.parse(response.content[0].text);
      expect(content).toHaveLength(1);
    });

    it('should auto-discover project when not provided', async () => {
      mockCoreApi.getProjects.mockResolvedValue([{ name: 'WrongProject' }, { name: 'AutoProject' }]);
      // First project throws (repo not found), second succeeds
      mockGitApi.getRepository
        .mockRejectedValueOnce(new Error('not found'))
        .mockResolvedValue({ id: 'r1' });
      mockGitApi.getBranches.mockResolvedValue([{ name: 'feature/mine' }]);

      const response = await mockServer.invokeTool('repo_list_my_branches_by_repo', { repositoryId: 'my-repo' });

      expect(isValidToolResponse(response)).toBe(true);
      expect(mockCoreApi.getProjects).toHaveBeenCalled();
    });

    it('should handle API errors', async () => {
      mockGitApi.getBranches.mockRejectedValue(new Error('Error'));

      const response = await mockServer.invokeTool('repo_list_my_branches_by_repo', { repositoryId: 'my-repo', project: 'P' });

      expect(isValidErrorResponse(response)).toBe(true);
    });
  });

  // ─── repo_list_pull_request_threads ──────────────────────────────────────

  describe('repo_list_pull_request_threads', () => {
    it('should list threads for a PR', async () => {
      const threads = [{ id: 1 }, { id: 2 }, { id: 3 }];
      mockGitApi.getThreads.mockResolvedValue(threads);

      const response = await mockServer.invokeTool('repo_list_pull_request_threads', { repositoryId: 'my-repo', pullRequestId: 42 });

      expect(isValidToolResponse(response)).toBe(true);
      expect(mockGitApi.getThreads).toHaveBeenCalledWith('my-repo', 42, undefined, undefined, undefined);
      const content = JSON.parse(response.content[0].text);
      expect(content).toHaveLength(3);
    });

    it('should apply skip and top pagination', async () => {
      mockGitApi.getThreads.mockResolvedValue([{ id: 1 }, { id: 2 }, { id: 3 }, { id: 4 }]);

      const response = await mockServer.invokeTool('repo_list_pull_request_threads', { repositoryId: 'r', pullRequestId: 1, skip: 1, top: 2 });

      const content = JSON.parse(response.content[0].text);
      expect(content).toHaveLength(2);
      expect(content[0].id).toBe(2);
    });

    it('should handle API errors', async () => {
      mockGitApi.getThreads.mockRejectedValue(new Error('Thread error'));

      const response = await mockServer.invokeTool('repo_list_pull_request_threads', { repositoryId: 'r', pullRequestId: 1 });

      expect(isValidErrorResponse(response)).toBe(true);
    });
  });

  // ─── repo_get_repo_by_name_or_id ──────────────────────────────────────────

  describe('repo_get_repo_by_name_or_id', () => {
    it('should get repository by name', async () => {
      const repo = { id: 'r1', name: 'my-repo', defaultBranch: 'refs/heads/main' };
      mockGitApi.getRepository.mockResolvedValue(repo);

      const response = await mockServer.invokeTool('repo_get_repo_by_name_or_id', { project: 'MyProject', repositoryNameOrId: 'my-repo' });

      expect(isValidToolResponse(response)).toBe(true);
      expect(mockGitApi.getRepository).toHaveBeenCalledWith('my-repo', 'MyProject');
      const content = JSON.parse(response.content[0].text);
      expect(content.name).toBe('my-repo');
    });

    it('should handle API errors', async () => {
      mockGitApi.getRepository.mockRejectedValue(new Error('Not found'));

      const response = await mockServer.invokeTool('repo_get_repo_by_name_or_id', { project: 'P', repositoryNameOrId: 'unknown' });

      expect(isValidErrorResponse(response)).toBe(true);
    });
  });

  // ─── repo_get_branch_by_name ─────────────────────────────────────────────

  describe('repo_get_branch_by_name', () => {
    it('should get branch details with project', async () => {
      const branch = { name: 'main', commit: { commitId: 'abc123' } };
      mockGitApi.getBranch.mockResolvedValue(branch);

      const response = await mockServer.invokeTool('repo_get_branch_by_name', { repositoryId: 'my-repo', branchName: 'main', project: 'MyProject' });

      expect(isValidToolResponse(response)).toBe(true);
      expect(mockGitApi.getBranch).toHaveBeenCalledWith('my-repo', 'main', 'MyProject');
      const content = JSON.parse(response.content[0].text);
      expect(content.name).toBe('main');
    });

    it('should auto-discover project', async () => {
      mockCoreApi.getProjects.mockResolvedValue([{ name: 'WrongProject' }, { name: 'AutoProject' }]);
      mockGitApi.getRepository
        .mockRejectedValueOnce(new Error('not found'))
        .mockResolvedValue({ id: 'r1' });
      mockGitApi.getBranch.mockResolvedValue({ name: 'develop' });

      const response = await mockServer.invokeTool('repo_get_branch_by_name', { repositoryId: 'my-repo', branchName: 'develop' });

      expect(isValidToolResponse(response)).toBe(true);
    });

    it('should handle API errors', async () => {
      mockGitApi.getBranch.mockRejectedValue(new Error('Branch not found'));

      const response = await mockServer.invokeTool('repo_get_branch_by_name', { repositoryId: 'r', branchName: 'missing', project: 'P' });

      expect(isValidErrorResponse(response)).toBe(true);
    });
  });

  // ─── repo_get_pull_request_by_id ─────────────────────────────────────────

  describe('repo_get_pull_request_by_id', () => {
    it('should get PR by ID', async () => {
      const pr = { pullRequestId: 42, title: 'My PR', repository: { project: { name: 'P' } } };
      mockGitApi.getPullRequestById.mockResolvedValue(pr);

      const response = await mockServer.invokeTool('repo_get_pull_request_by_id', { repositoryId: 'my-repo', pullRequestId: 42 });

      expect(isValidToolResponse(response)).toBe(true);
      expect(mockGitApi.getPullRequestById).toHaveBeenCalledWith(42);
      const content = JSON.parse(response.content[0].text);
      expect(content.pullRequestId).toBe(42);
    });

    it('should include work item refs when requested', async () => {
      const pr = { pullRequestId: 42, repository: { project: { name: 'MyProject' } } };
      mockGitApi.getPullRequestById.mockResolvedValue(pr);
      mockGitApi.getPullRequestWorkItemRefs.mockResolvedValue([{ id: 100 }]);

      const response = await mockServer.invokeTool('repo_get_pull_request_by_id', { repositoryId: 'my-repo', pullRequestId: 42, includeWorkItemRefs: true });

      expect(isValidToolResponse(response)).toBe(true);
      expect(mockGitApi.getPullRequestWorkItemRefs).toHaveBeenCalled();
      const content = JSON.parse(response.content[0].text);
      expect(content.workItemRefs).toBeDefined();
    });

    it('should handle API errors', async () => {
      mockGitApi.getPullRequestById.mockRejectedValue(new Error('PR not found'));

      const response = await mockServer.invokeTool('repo_get_pull_request_by_id', { repositoryId: 'r', pullRequestId: 999 });

      expect(isValidErrorResponse(response)).toBe(true);
    });
  });

  // ─── repo_search_commits ─────────────────────────────────────────────────

  describe('repo_search_commits', () => {
    it('should search commits', async () => {
      const commits = [{ commitId: 'abc', comment: 'Fix bug' }];
      mockGitApi.getCommits.mockResolvedValue(commits);

      const response = await mockServer.invokeTool('repo_search_commits', { project: 'MyProject', repository: 'my-repo' });

      expect(isValidToolResponse(response)).toBe(true);
      expect(mockGitApi.getCommits).toHaveBeenCalledWith('my-repo', expect.any(Object), 'MyProject');
      const content = JSON.parse(response.content[0].text);
      expect(content[0].commitId).toBe('abc');
    });

    it('should apply text and date filters', async () => {
      mockGitApi.getCommits.mockResolvedValue([]);

      await mockServer.invokeTool('repo_search_commits', {
        project: 'P', repository: 'r',
        searchText: 'fix', author: 'John', fromDate: '2024-01-01', toDate: '2024-12-31'
      });

      expect(mockGitApi.getCommits).toHaveBeenCalledWith('r', expect.objectContaining({
        searchText: 'fix', author: 'John', fromDate: '2024-01-01', toDate: '2024-12-31'
      }), 'P');
    });

    it('should apply version with tag type', async () => {
      mockGitApi.getCommits.mockResolvedValue([]);

      await mockServer.invokeTool('repo_search_commits', {
        project: 'P', repository: 'r', version: 'v1.0.0', versionType: 'tag'
      });

      expect(mockGitApi.getCommits).toHaveBeenCalledWith('r', expect.objectContaining({
        itemVersion: { version: 'v1.0.0', versionType: 1 }
      }), 'P');
    });

    it('should apply version with commit type', async () => {
      mockGitApi.getCommits.mockResolvedValue([]);

      await mockServer.invokeTool('repo_search_commits', {
        project: 'P', repository: 'r', version: 'abc123', versionType: 'commit'
      });

      expect(mockGitApi.getCommits).toHaveBeenCalledWith('r', expect.objectContaining({
        itemVersion: { version: 'abc123', versionType: 2 }
      }), 'P');
    });

    it('should apply version with branch type', async () => {
      mockGitApi.getCommits.mockResolvedValue([]);

      await mockServer.invokeTool('repo_search_commits', {
        project: 'P', repository: 'r', version: 'main', versionType: 'branch'
      });

      expect(mockGitApi.getCommits).toHaveBeenCalledWith('r', expect.objectContaining({
        itemVersion: { version: 'main', versionType: 0 }
      }), 'P');
    });

    it('should apply all optional criteria', async () => {
      mockGitApi.getCommits.mockResolvedValue([]);

      await mockServer.invokeTool('repo_search_commits', {
        project: 'P', repository: 'r',
        committer: 'Jane', committerEmail: 'jane@co.com', authorEmail: 'john@co.com',
        fromCommit: 'start', toCommit: 'end',
        commitIds: ['c1', 'c2'], includeWorkItems: true, includeLinks: true, skip: 2, top: 5
      });

      expect(mockGitApi.getCommits).toHaveBeenCalledWith('r', expect.objectContaining({
        committer: 'Jane', committerEmail: 'jane@co.com', authorEmail: 'john@co.com',
        fromCommitId: 'start', toCommitId: 'end',
        ids: ['c1', 'c2'], includeWorkItems: true, includeLinks: true, $skip: 2, $top: 5
      }), 'P');
    });

    it('should handle API errors', async () => {
      mockGitApi.getCommits.mockRejectedValue(new Error('Commits error'));

      const response = await mockServer.invokeTool('repo_search_commits', { project: 'P', repository: 'r' });

      expect(isValidErrorResponse(response)).toBe(true);
    });
  });

  // ─── repo_get_file_content ───────────────────────────────────────────────

  describe('repo_get_file_content', () => {
    it('should return file content', async () => {
      mockGitApi.getItemContent.mockResolvedValue((async function* () { yield Buffer.from('const x = 1;'); })());

      const response = await mockServer.invokeTool('repo_get_file_content', { repositoryId: 'my-repo', path: '/src/index.js' });

      expect(isValidToolResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('const x = 1;');
    });

    it('should pass version descriptor for branch', async () => {
      mockGitApi.getItemContent.mockResolvedValue((async function* () { yield Buffer.from('content'); })());

      await mockServer.invokeTool('repo_get_file_content', { repositoryId: 'r', path: '/file.js', version: 'develop', versionType: 'branch' });

      expect(mockGitApi.getItemContent).toHaveBeenCalledWith(
        'r', '/file.js', undefined, undefined, undefined, undefined, undefined, undefined,
        { version: 'develop', versionType: 0 }
      );
    });

    it('should pass version descriptor for tag', async () => {
      mockGitApi.getItemContent.mockResolvedValue((async function* () { yield Buffer.from('tagged'); })());

      await mockServer.invokeTool('repo_get_file_content', { repositoryId: 'r', path: '/file.js', version: 'v1.0', versionType: 'tag' });

      expect(mockGitApi.getItemContent).toHaveBeenCalledWith(
        'r', '/file.js', undefined, undefined, undefined, undefined, undefined, undefined,
        { version: 'v1.0', versionType: 1 }
      );
    });

    it('should pass version descriptor for commit', async () => {
      mockGitApi.getItemContent.mockResolvedValue((async function* () { yield Buffer.from('at commit'); })());

      await mockServer.invokeTool('repo_get_file_content', { repositoryId: 'r', path: '/file.js', version: 'abc123', versionType: 'commit' });

      expect(mockGitApi.getItemContent).toHaveBeenCalledWith(
        'r', '/file.js', undefined, undefined, undefined, undefined, undefined, undefined,
        { version: 'abc123', versionType: 2 }
      );
    });

    it('should handle API errors', async () => {
      mockGitApi.getItemContent.mockRejectedValue(new Error('File not found'));

      const response = await mockServer.invokeTool('repo_get_file_content', { repositoryId: 'r', path: '/missing.js' });

      expect(isValidErrorResponse(response)).toBe(true);
    });
  });

  // ─── repo_list_directory ─────────────────────────────────────────────────

  describe('repo_list_directory', () => {
    it('should list root directory', async () => {
      const items = [{ path: '/src', isFolder: true }, { path: '/README.md', isFolder: false }];
      mockGitApi.getItems.mockResolvedValue(items);

      const response = await mockServer.invokeTool('repo_list_directory', { repositoryId: 'my-repo' });

      expect(isValidToolResponse(response)).toBe(true);
      expect(mockGitApi.getItems).toHaveBeenCalledWith('my-repo', undefined, '/', 1, undefined, undefined, undefined, undefined, undefined);
    });

    it('should use recursive level when recursive is true', async () => {
      mockGitApi.getItems.mockResolvedValue([]);

      await mockServer.invokeTool('repo_list_directory', { repositoryId: 'r', recursive: true });

      expect(mockGitApi.getItems).toHaveBeenCalledWith('r', undefined, '/', 120, undefined, undefined, undefined, undefined, undefined);
    });

    it('should pass tag version descriptor', async () => {
      mockGitApi.getItems.mockResolvedValue([]);

      await mockServer.invokeTool('repo_list_directory', { repositoryId: 'r', path: '/src', version: 'v2.0', versionType: 'tag' });

      expect(mockGitApi.getItems).toHaveBeenCalledWith('r', undefined, '/src', 1, undefined, undefined, undefined, undefined, { version: 'v2.0', versionType: 1 });
    });

    it('should pass commit version descriptor', async () => {
      mockGitApi.getItems.mockResolvedValue([]);

      await mockServer.invokeTool('repo_list_directory', { repositoryId: 'r', path: '/src', version: 'deadbeef', versionType: 'commit' });

      expect(mockGitApi.getItems).toHaveBeenCalledWith('r', undefined, '/src', 1, undefined, undefined, undefined, undefined, { version: 'deadbeef', versionType: 2 });
    });

    it('should handle API errors', async () => {
      mockGitApi.getItems.mockRejectedValue(new Error('Items error'));

      const response = await mockServer.invokeTool('repo_list_directory', { repositoryId: 'r' });

      expect(isValidErrorResponse(response)).toBe(true);
    });
  });

  // ─── repo_get_pull_request_changes ───────────────────────────────────────

  describe('repo_get_pull_request_changes', () => {
    it('should get PR changes using latest iteration', async () => {
      mockGitApi.getPullRequestIterations.mockResolvedValue([{ id: 1 }, { id: 2 }]);
      mockGitApi.getPullRequestIterationChanges.mockResolvedValue({ changeEntries: [{ item: { path: '/src/file.js' } }] });

      const response = await mockServer.invokeTool('repo_get_pull_request_changes', { repositoryId: 'my-repo', pullRequestId: 42 });

      expect(isValidToolResponse(response)).toBe(true);
      expect(mockGitApi.getPullRequestIterationChanges).toHaveBeenCalledWith('my-repo', 42, 2, undefined, undefined, undefined);
    });

    it('should use explicit iterationId when provided', async () => {
      mockGitApi.getPullRequestIterationChanges.mockResolvedValue({ changeEntries: [] });

      await mockServer.invokeTool('repo_get_pull_request_changes', { repositoryId: 'r', pullRequestId: 1, iterationId: 3 });

      expect(mockGitApi.getPullRequestIterations).not.toHaveBeenCalled();
      expect(mockGitApi.getPullRequestIterationChanges).toHaveBeenCalledWith('r', 1, 3, undefined, undefined, undefined);
    });

    it('should handle API errors', async () => {
      mockGitApi.getPullRequestIterations.mockRejectedValue(new Error('Iteration error'));

      const response = await mockServer.invokeTool('repo_get_pull_request_changes', { repositoryId: 'r', pullRequestId: 1 });

      expect(isValidErrorResponse(response)).toBe(true);
    });
  });
});
