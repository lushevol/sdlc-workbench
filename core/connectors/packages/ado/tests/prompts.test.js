import { describe, it, expect, vi, beforeEach } from 'vitest';
import { configureAdoPrompts, ADO_PROMPTS } from '../src/prompts.js';

describe('ADO Prompts', () => {
  let mockServer;

  beforeEach(() => {
    mockServer = { prompt: vi.fn() };
  });

  describe('ADO_PROMPTS constant', () => {
    it('should export ADO_PROMPTS object', () => {
      expect(ADO_PROMPTS).toBeDefined();
      expect(typeof ADO_PROMPTS).toBe('object');
    });

    it('should contain 87 prompts', () => {
      expect(Object.keys(ADO_PROMPTS)).toHaveLength(87);
    });

    it('each prompt should have name, description, and arguments array', () => {
      Object.values(ADO_PROMPTS).forEach(prompt => {
        expect(prompt.name).toBeDefined();
        expect(typeof prompt.name).toBe('string');
        expect(prompt.description).toBeDefined();
        expect(typeof prompt.description).toBe('string');
        expect(Array.isArray(prompt.arguments)).toBe(true);
      });
    });

    it('MY_WORK prompt should have no arguments', () => {
      expect(ADO_PROMPTS.MY_WORK.arguments).toHaveLength(0);
    });

    it('LIST_ALL_PROJECTS prompt should have no arguments', () => {
      expect(ADO_PROMPTS.LIST_ALL_PROJECTS.arguments).toHaveLength(0);
    });

    it('CREATE_WORK_ITEM should have required project and title arguments', () => {
      const projectArg = ADO_PROMPTS.CREATE_WORK_ITEM.arguments.find(a => a.name === 'project');
      const titleArg = ADO_PROMPTS.CREATE_WORK_ITEM.arguments.find(a => a.name === 'title');
      expect(projectArg).toBeDefined();
      expect(projectArg.required).toBe(true);
      expect(titleArg).toBeDefined();
      expect(titleArg.required).toBe(true);
    });

    it('prompt names should all be unique', () => {
      const names = Object.values(ADO_PROMPTS).map(p => p.name);
      const uniqueNames = new Set(names);
      expect(uniqueNames.size).toBe(names.length);
    });

    it('REVIEW_PR should have required prUrl argument', () => {
      const prUrlArg = ADO_PROMPTS.REVIEW_PR.arguments.find(a => a.name === 'prUrl');
      expect(prUrlArg).toBeDefined();
      expect(prUrlArg.required).toBe(true);
    });
  });

  describe('configureAdoPrompts()', () => {
    it('should register all 87 prompts on the server', () => {
      configureAdoPrompts(mockServer);
      expect(mockServer.prompt).toHaveBeenCalledTimes(87);
    });

    it('should accept optional getContext parameter', () => {
      const getContext = vi.fn(() => null);
      expect(() => configureAdoPrompts(mockServer, { getContext })).not.toThrow();
    });

    it('should work without getContext (default null)', () => {
      expect(() => configureAdoPrompts(mockServer)).not.toThrow();
    });

    it('should register MY_WORK as a no-arg prompt (3-argument server.prompt call)', () => {
      configureAdoPrompts(mockServer);
      const myWorkCall = mockServer.prompt.mock.calls.find(c => c[0] === 'my-work');
      expect(myWorkCall).toBeDefined();
      expect(myWorkCall).toHaveLength(3);
    });

    it('should register CREATE_WORK_ITEM with args schema (4-argument server.prompt call)', () => {
      configureAdoPrompts(mockServer);
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'create-work-item');
      expect(call).toBeDefined();
      expect(call).toHaveLength(4);
    });

    it('should use project from getContext when explicit project arg is absent', async () => {
      const ctx = { ado: { project: 'MyProject', team: 'MyTeam' } };
      configureAdoPrompts(mockServer, { getContext: () => ctx });
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'create-work-item');
      const handler = call.at(-1);
      const result = await handler({ title: 'A new story' });
      expect(result.messages[0].content.text).toContain('MyProject');
    });

    it('should prefer explicit project arg over context value', async () => {
      const ctx = { ado: { project: 'ContextProject' } };
      configureAdoPrompts(mockServer, { getContext: () => ctx });
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'create-work-item');
      const handler = call.at(-1);
      const result = await handler({ title: 'My Task', project: 'ExplicitProject' });
      expect(result.messages[0].content.text).toContain('ExplicitProject');
      expect(result.messages[0].content.text).not.toContain('ContextProject');
    });

    it('should use team from getContext in sprint-planning', async () => {
      const ctx = { ado: { project: 'CtxProj', team: 'CtxTeam' } };
      configureAdoPrompts(mockServer, { getContext: () => ctx });
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'sprint-planning');
      const handler = call.at(-1);
      const result = await handler({});
      expect(result.messages[0].content.text).toContain('CtxTeam');
      expect(result.messages[0].content.text).toContain('CtxProj');
    });
  });

  describe('generateAdoPromptMessage (via registered handlers)', () => {
    beforeEach(() => {
      configureAdoPrompts(mockServer);
    });

    it('should return valid MCP prompt response structure for first registered prompt', async () => {
      const call = mockServer.prompt.mock.calls[0];
      const handler = call.at(-1);
      const result = await handler({});
      expect(result).toHaveProperty('messages');
      expect(Array.isArray(result.messages)).toBe(true);
      expect(result.messages[0]).toHaveProperty('role', 'user');
      expect(result.messages[0]).toHaveProperty('content');
      expect(result.messages[0].content).toHaveProperty('type', 'text');
      expect(result.messages[0].content).toHaveProperty('text');
    });

    it('should generate message for create-work-item with explicit args', async () => {
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'create-work-item');
      const handler = call.at(-1);
      const result = await handler({ project: 'TestProj', title: 'My Feature', type: 'Bug' });
      expect(result.messages[0].content.text).toContain('TestProj');
      expect(result.messages[0].content.text).toContain('My Feature');
      expect(result.messages[0].content.text).toContain('Bug');
    });

    it('should generate message for my-work (no args prompt)', async () => {
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'my-work');
      const handler = call.at(-1);
      const result = await handler({});
      expect(result.messages).toHaveLength(1);
      expect(result.messages[0].role).toBe('user');
      expect(result.messages[0].content.text).toContain('work items');
    });

    it('should generate message for list-all-projects (no args prompt)', async () => {
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'list-all-projects');
      const handler = call.at(-1);
      const result = await handler({});
      expect(result.messages[0].content.text).toContain('projects');
    });

    it('should generate message for review-pr with prUrl', async () => {
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'review-pr');
      const handler = call.at(-1);
      const result = await handler({ prUrl: 'https://dev.azure.com/sc-ado/proj/_git/repo/pullrequest/123' });
      expect(result.messages[0].content.text).toContain('https://dev.azure.com/sc-ado/proj/_git/repo/pullrequest/123');
    });

    it('should generate message for run-pipeline with project and pipelineId', async () => {
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'run-pipeline');
      const handler = call.at(-1);
      const result = await handler({ project: 'ProjX', pipelineId: '42' });
      expect(result.messages[0].content.text).toContain('ProjX');
      expect(result.messages[0].content.text).toContain('42');
    });

    it('should generate message for search-code with searchText', async () => {
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'search-code');
      const handler = call.at(-1);
      const result = await handler({ searchText: 'useEffect' });
      expect(result.messages[0].content.text).toContain('useEffect');
    });

    it('should generate message for list-test-plans with project', async () => {
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'list-test-plans');
      const handler = call.at(-1);
      const result = await handler({ project: 'TestProjA' });
      expect(result.messages[0].content.text).toContain('TestProjA');
    });

    it('should generate message for get-identity-ids with identifiers', async () => {
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'get-identity-ids');
      const handler = call.at(-1);
      const result = await handler({ identifiers: 'user@example.com' });
      expect(result.messages[0].content.text).toContain('user@example.com');
    });

    it('should generate message for get-work-item with id', async () => {
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'get-work-item');
      const handler = call.at(-1);
      const result = await handler({ id: '99' });
      expect(result.messages[0].content.text).toContain('99');
    });

    it('should generate message for delete-pr-review-comments mentioning the copilot prefix', async () => {
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'delete-pr-review-comments');
      const handler = call.at(-1);
      const result = await handler({ prUrl: 'https://dev.azure.com/sc-ado/p/_git/r/pullrequest/7' });
      expect(result.messages[0].content.text).toContain('🤖');
    });

    it('should use defaultBranch from context in create-branch when no sourceBranch is given', async () => {
      const ctx = { ado: { defaultBranch: 'develop' }, repositories: [{ isDefault: true, name: 'MyRepo' }] };
      const serverWithCtx = { prompt: vi.fn() };
      configureAdoPrompts(serverWithCtx, { getContext: () => ctx });
      const call = serverWithCtx.prompt.mock.calls.find(c => c[0] === 'create-branch');
      const handler = call.at(-1);
      const result = await handler({ repository: 'MyRepo', branchName: 'feature/new' });
      expect(result.messages[0].content.text).toContain('feature/new');
      expect(result.messages[0].content.text).toContain('develop');
    });

    it('should generate message for nexus-scan prompt: search-work-item', async () => {
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'search-work-item');
      const handler = call.at(-1);
      const result = await handler({ searchText: 'login bug' });
      expect(result.messages[0].content.text).toContain('login bug');
    });

    it('should generate message for get-pipeline-status with buildId', async () => {
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'get-pipeline-status');
      const handler = call.at(-1);
      const result = await handler({ project: 'MyProj', buildId: '555' });
      expect(result.messages[0].content.text).toContain('555');
    });

    it('should generate message for update-work-item with field and value', async () => {
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'update-work-item');
      const handler = call.at(-1);
      const result = await handler({ id: '10', field: 'System.State', value: 'Active' });
      expect(result.messages[0].content.text).toContain('System.State');
      expect(result.messages[0].content.text).toContain('Active');
    });

    it('should handle undefined args gracefully', async () => {
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'create-work-item');
      const handler = call.at(-1);
      const result = await handler(undefined);
      expect(result.messages[0].content.text).toBeDefined();
      expect(typeof result.messages[0].content.text).toBe('string');
    });
  });

  describe('branch coverage sweep — all 87 prompt handlers', () => {
    it('every registered prompt handler returns a valid MCP response with empty args', async () => {
      configureAdoPrompts(mockServer);
      for (const call of mockServer.prompt.mock.calls) {
        const handler = call.at(-1);
        const result = await handler({});
        expect(result.messages).toHaveLength(1);
        expect(result.messages[0].role).toBe('user');
        expect(result.messages[0].content.type).toBe('text');
        expect(typeof result.messages[0].content.text).toBe('string');
      }
    });

    it('every registered prompt handler returns a valid response with realistic args', async () => {
      configureAdoPrompts(mockServer);
      const args = {
        project: 'TestProject', team: 'TestTeam', repository: 'my-repo',
        branch: 'main', iteration: 'TestProject/Sprint 1', title: 'Test Title',
        type: 'Bug', description: 'A description', prUrl: 'https://dev.azure.com/sc-ado/p/_git/r/pullrequest/1',
        sourceBranch: 'feature/x', targetBranch: 'main', branchName: 'feature/x',
        workItemIds: '1,2,3', queryId: 'my-query', searchTerm: 'hello',
        fromDate: '2024-01-01', toDate: '2024-12-31', action: 'add',
        reviewers: 'user@example.com', filter: 'feat', workItemId: '42',
        comment: 'Nice work', filePath: '/src/index.js', line: '10',
        parentId: '1', childIds: '2,3', sourceId: '1', targetId: '2',
        linkType: 'Related', backlogLevel: 'Stories', mergeStrategy: 'squash',
        deleteSourceBranch: 'yes', pipelineId: '5', runId: '10',
        branchName2: 'develop', statusFilter: 'inProgress', resultFilter: 'succeeded',
        buildId: '100', searchText: 'hello', top: '10',
        filterActivePlans: 'yes', planId: '1', parentSuiteId: '2', suiteId: '3',
        testCaseIds: '1,2', testCaseId: '10', steps: 'Step 1\nStep 2', priority: '1',
        path: '/src', recursive: 'yes', pullRequestId: '7', vote: 'approve',
        threadId: '5', status: 'fixed', content: 'Reply text',
        workItemId2: '20', relationUrls: 'vstfs:///WorkItemTracking/1',
        repositoryId: 'my-repo', projectId: 'TestProject', commentId: '3',
        text: 'Updated comment', attachmentId: 'abc-123',
        name: 'Sprint 42', startDate: '2024-01-01', endDate: '2024-03-01',
        timeframe: 'current', iterationId: 'guid-1234', teamMemberId: 'member-guid',
        activityName: 'Development', hoursPerDay: '6', identifiers: 'user@example.com',
        forceRetryAllJobs: 'yes', stageName: 'Build', includeWorkItems: 'yes',
        pullRequest: '5', metricKeys: 'bugs', applicationId: 'ITAM__DEV__app',
        pipelineId2: '2', workItemType: 'Bug', state: 'Active', severity: 'CRITICAL',
      };
      for (const call of mockServer.prompt.mock.calls) {
        const handler = call.at(-1);
        const result = await handler(args);
        expect(typeof result.messages[0].content.text).toBe('string');
      }
    });
  });
});
