import { vi } from 'vitest';

/**
 * Creates a mock Azure DevOps connection with common API methods
 * @returns {Object} Mocked connection object with getWorkItemTrackingApi, getGitApi, etc.
 */
export function createMockConnection() {
  const mockConnection = {
    getWorkItemTrackingApi: vi.fn(),
    getGitApi: vi.fn(),
    getCoreApi: vi.fn(),
    getWorkApi: vi.fn(),
    getBuildApi: vi.fn(),
    getPipelinesApi: vi.fn(),
    getTestPlanApi: vi.fn(),
    getTestApi: vi.fn(),
    getTaskAgentApi: vi.fn(),
    getDashboardApi: vi.fn(),
    serverUrl: 'https://dev.azure.com/sc-ado',
    rest: {
      get: vi.fn(),
      create: vi.fn()
    }
  };

  return mockConnection;
}

/**
 * Creates a mock Build API with common methods
 * @param {Object} options - Configuration for mock responses
 * @returns {Object} Mocked Build API
 */
export function createMockBuildApi(options = {}) {
  const {
    definitions = [],
    build = null,
    builds = [],
    updateResult = null,
    workItemRefs = []
  } = options;

  return {
    getDefinitions: vi.fn().mockResolvedValue(definitions),
    getBuild: vi.fn().mockResolvedValue(build),
    getBuilds: vi.fn().mockResolvedValue(builds),
    updateBuild: vi.fn().mockResolvedValue(updateResult),
    getBuildWorkItemsRefs: vi.fn().mockResolvedValue(workItemRefs),
    getBuildChanges: vi.fn().mockResolvedValue([]),
    getArtifacts: vi.fn().mockResolvedValue([]),
    getBuildLogs: vi.fn().mockResolvedValue([]),
    getBuildLogLines: vi.fn().mockResolvedValue([])
  };
}

/**
 * Creates a mock Pipelines API with common methods
 * @param {Object} options - Configuration for mock responses
 * @returns {Object} Mocked Pipelines API
 */
export function createMockPipelinesApi(options = {}) {
  const {
    run = null,
    runs = []
  } = options;

  return {
    runPipeline: vi.fn().mockResolvedValue(run),
    listRuns: vi.fn().mockResolvedValue(runs),
    getRun: vi.fn().mockResolvedValue(run)
  };
}

/**
 * Creates a mock Task Agent API with common methods (variable groups / Library)
 * @param {Object} options - Configuration for mock responses
 * @returns {Object} Mocked Task Agent API
 */
export function createMockTaskAgentApi(options = {}) {
  const {
    variableGroups = [],
    variableGroup = null
  } = options;

  return {
    getVariableGroups: vi.fn().mockResolvedValue(variableGroups),
    getVariableGroup: vi.fn().mockResolvedValue(variableGroup)
  };
}

/**
 * Creates a mock Dashboard API with common methods
 * @param {Object} options - Configuration for mock responses
 * @returns {Object} Mocked Dashboard API
 */
export function createMockDashboardApi(options = {}) {
  const {
    dashboard = null
  } = options;

  return {
    getDashboard: vi.fn().mockResolvedValue(dashboard)
  };
}

/**
 * Creates a mock Work Item Tracking API with common methods
 * @param {Object} options - Configuration for mock responses
 * @returns {Object} Mocked WIT API
 */
export function createMockWitApi(options = {}) {
  const {
    workItem = null,
    workItems = [],
    queryResult = null,
    updateResult = null,
    createResult = null,
    comments = []
  } = options;

  return {
    getWorkItem: vi.fn().mockResolvedValue(workItem),
    getWorkItems: vi.fn().mockResolvedValue(workItems),
    queryByWiql: vi.fn().mockResolvedValue(queryResult),
    queryById: vi.fn().mockResolvedValue(queryResult),
    updateWorkItem: vi.fn().mockResolvedValue(updateResult),
    createWorkItem: vi.fn().mockResolvedValue(createResult),
    addComment: vi.fn().mockResolvedValue({ text: 'Comment added' }),
    getComments: vi.fn().mockResolvedValue({ comments }),
    getWorkItemRelations: vi.fn().mockResolvedValue([]),
    updateComment: vi.fn().mockResolvedValue({ id: 1, text: 'Updated comment' }),
    getRevisions: vi.fn().mockResolvedValue([]),
    getAttachmentContent: vi.fn().mockResolvedValue((async function* () { yield Buffer.from('attachment'); })()),
    getClassificationNode: vi.fn().mockResolvedValue({}),
    createOrUpdateClassificationNode: vi.fn().mockResolvedValue({})
  };
}

/**
 * Creates a mock Git API with common methods
 * @param {Object} options - Configuration for mock responses
 * @returns {Object} Mocked Git API
 */
export function createMockGitApi(options = {}) {
  const {
    repositories = [],
    pullRequest = null,
    pullRequests = [],
    branches = [],
    commits = [],
    threads = []
  } = options;

  return {
    getRepositories: vi.fn().mockResolvedValue(repositories),
    getRepository: vi.fn().mockResolvedValue(repositories[0] || null),
    getPullRequest: vi.fn().mockResolvedValue(pullRequest),
    getPullRequests: vi.fn().mockResolvedValue(pullRequests),
    getPullRequestById: vi.fn().mockResolvedValue(pullRequest),
    createPullRequest: vi.fn().mockResolvedValue(pullRequest),
    updatePullRequest: vi.fn().mockResolvedValue(pullRequest),
    getBranches: vi.fn().mockResolvedValue(branches),
    getBranch: vi.fn().mockResolvedValue(branches[0] || null),
    createBranch: vi.fn().mockResolvedValue({ name: 'refs/heads/new-branch' }),
    getCommits: vi.fn().mockResolvedValue(commits),
    getThreads: vi.fn().mockResolvedValue(threads),
    createThread: vi.fn().mockResolvedValue({ id: 1, comments: [] }),
    createComment: vi.fn().mockResolvedValue({ id: 1, content: 'Comment' }),
    deleteComment: vi.fn().mockResolvedValue({}),
    getIdentities: vi.fn().mockResolvedValue([]),
    getItemContent: vi.fn().mockResolvedValue((async function* () { yield Buffer.from('file content'); })()),
    getItems: vi.fn().mockResolvedValue([]),
    getPullRequestIterations: vi.fn().mockResolvedValue([{ id: 1 }]),
    getPullRequestIterationChanges: vi.fn().mockResolvedValue({ changeEntries: [] }),
    createPullRequestReviewer: vi.fn().mockResolvedValue({ vote: 10 }),
    updateThread: vi.fn().mockResolvedValue({ id: 1, status: 2 })
  };
}

/**
 * Creates a mock Core API with common methods
 * @param {Object} options - Configuration for mock responses
 * @returns {Object} Mocked Core API
 */
export function createMockCoreApi(options = {}) {
  const {
    projects = [],
    teams = []
  } = options;

  return {
    getProjects: vi.fn().mockResolvedValue(projects),
    getProject: vi.fn().mockResolvedValue(projects[0] || null),
    getTeams: vi.fn().mockResolvedValue(teams),
    getTeam: vi.fn().mockResolvedValue(teams[0] || null)
  };
}

/**
 * Creates a mock Work API with common methods
 * @param {Object} options - Configuration for mock responses
 * @returns {Object} Mocked Work API
 */
export function createMockWorkApi(options = {}) {
  const {
    iterations = [],
    backlogs = []
  } = options;

  return {
    getTeamIterations: vi.fn().mockResolvedValue(iterations),
    getBacklogs: vi.fn().mockResolvedValue(backlogs),
    getTeamSettings: vi.fn().mockResolvedValue({ workingDays: [1, 2, 3, 4, 5] }),
    postTeamIteration: vi.fn().mockResolvedValue({}),
    getCapacitiesWithIdentityRefAndTotals: vi.fn().mockResolvedValue([]),
    updateCapacityWithIdentityRef: vi.fn().mockResolvedValue({})
  };
}

/**
 * Creates a mock Test Plan API with common methods
 * @returns {Object} Mocked TestPlan API
 */
export function createMockTestPlanApi() {
  return {
    getTestPlans: vi.fn().mockResolvedValue([]),
    createTestPlan: vi.fn().mockResolvedValue({ id: 1, name: 'Test Plan' }),
    getTestSuitesForPlan: vi.fn().mockResolvedValue([]),
    createTestSuite: vi.fn().mockResolvedValue({ id: 1, name: 'Test Suite' }),
    addTestCasesToSuite: vi.fn().mockResolvedValue([]),
    getTestCaseList: vi.fn().mockResolvedValue([])
  };
}

/**
 * Creates a mock Test API with common methods
 * @returns {Object} Mocked Test API
 */
export function createMockTestApi() {
  return {
    getTestRuns: vi.fn().mockResolvedValue([]),
    getTestResults: vi.fn().mockResolvedValue([])
  };
}

/**
 * Sets up a full mock connection with all APIs configured
 * @param {Object} options - Configuration for all APIs
 * @returns {Object} Fully configured mock connection
 */
export function setupMockConnection(options = {}) {
  const connection = createMockConnection();
  
  connection.getWorkItemTrackingApi.mockResolvedValue(
    createMockWitApi(options.wit || {})
  );
  
  connection.getGitApi.mockResolvedValue(
    createMockGitApi(options.git || {})
  );
  
  connection.getCoreApi.mockResolvedValue(
    createMockCoreApi(options.core || {})
  );
  
  connection.getWorkApi.mockResolvedValue(
    createMockWorkApi(options.work || {})
  );

  connection.getBuildApi.mockResolvedValue(
    createMockBuildApi(options.build || {})
  );

  connection.getPipelinesApi.mockResolvedValue(
    createMockPipelinesApi(options.pipelines || {})
  );

  connection.getTestPlanApi.mockResolvedValue(
    createMockTestPlanApi()
  );

  connection.getTestApi.mockResolvedValue(
    createMockTestApi()
  );

  connection.getTaskAgentApi.mockResolvedValue(
    createMockTaskAgentApi(options.taskAgent || {})
  );

  connection.getDashboardApi.mockResolvedValue(
    createMockDashboardApi(options.dashboard || {})
  );

  return connection;
}
