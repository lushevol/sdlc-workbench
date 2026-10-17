import { z } from 'zod';

const TESTPLAN_TOOLS = {
  list_test_plans: 'testplan_list_test_plans',
  create_test_plan: 'testplan_create_test_plan',
  list_test_suites: 'testplan_list_test_suites',
  create_test_suite: 'testplan_create_test_suite',
  add_test_cases_to_suite: 'testplan_add_test_cases_to_suite',
  list_test_cases: 'testplan_list_test_cases',
  create_test_case: 'testplan_create_test_case',
  update_test_case_steps: 'testplan_update_test_case_steps',
  show_test_results_from_build_id: 'testplan_show_test_results_from_build_id',
};

function configureTestPlanTools(server, getADOConnection) {

  // List test plans in a project
  server.tool(
    TESTPLAN_TOOLS.list_test_plans,
    'List all test plans in an Azure DevOps project.',
    {
      project: z.string().describe('Azure DevOps project name or ID'),
      filterActivePlans: z.boolean().optional().describe('If true, return only active test plans'),
      top: z.number().int().positive().optional().describe('Maximum number of test plans to return')
    },
    async ({ project, filterActivePlans, top }) => {
      try {
        const connection = await getADOConnection();
        const testPlanApi = await connection.getTestPlanApi();
        const plans = (await testPlanApi.getTestPlans(project, undefined, undefined, filterActivePlans, undefined)) || [];
        const filtered = filterActivePlans ? plans.filter(p => p.state === 'Active') : plans;
        const result = top ? filtered.slice(0, top) : filtered;
        if (result.length === 0) {
          return { content: [{ type: 'text', text: `No test plans found for project "${project}". Verify the project name is correct.` }] };
        }
        return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] };
      } catch (error) {
        return { content: [{ type: 'text', text: error?.message || String(error) }], isError: true };
      }
    }
  );

  // Create a new test plan
  server.tool(
    TESTPLAN_TOOLS.create_test_plan,
    'Create a new test plan in an Azure DevOps project.',
    {
      project: z.string().describe('Azure DevOps project name or ID'),
      name: z.string().describe('Name of the test plan'),
      iteration: z.string().describe('Iteration path for the test plan (e.g., "MyProject/Sprint 1")'),
      areaPath: z.string().optional().describe('Area path for the test plan'),
      description: z.string().optional().describe('Description of the test plan'),
      startDate: z.string().optional().describe('Start date in ISO 8601 format'),
      endDate: z.string().optional().describe('End date in ISO 8601 format')
    },
    async ({ project, name, iteration, areaPath, description, startDate, endDate }) => {
      try {
        const connection = await getADOConnection();
        const testPlanApi = await connection.getTestPlanApi();
        const planCreateParams = {
          name,
          iteration,
          areaPath,
          description,
          startDate: startDate ? new Date(startDate) : undefined,
          endDate: endDate ? new Date(endDate) : undefined
        };
        const plan = await testPlanApi.createTestPlan(planCreateParams, project);
        return { content: [{ type: 'text', text: JSON.stringify(plan, null, 2) }] };
      } catch (error) {
        return { content: [{ type: 'text', text: error?.message || String(error) }], isError: true };
      }
    }
  );

  // List test suites in a test plan
  server.tool(
    TESTPLAN_TOOLS.list_test_suites,
    'List all test suites in a test plan, returned in a hierarchical structure.',
    {
      project: z.string().describe('Azure DevOps project name or ID'),
      planId: z.number().int().positive().describe('Test plan ID'),
      top: z.number().int().positive().optional().describe('Maximum number of suites to return')
    },
    async ({ project, planId, top }) => {
      try {
        const connection = await getADOConnection();
        const testPlanApi = await connection.getTestPlanApi();
        const suites = (await testPlanApi.getTestSuitesForPlan(project, planId, undefined, undefined, true)) || [];
        const result = top ? suites.slice(0, top) : suites;
        if (result.length === 0) {
          return { content: [{ type: 'text', text: `No test suites found for plan ${planId} in project "${project}". Verify the project name and plan ID are correct.` }] };
        }
        return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] };
      } catch (error) {
        return { content: [{ type: 'text', text: error?.message || String(error) }], isError: true };
      }
    }
  );

  // Create a test suite
  server.tool(
    TESTPLAN_TOOLS.create_test_suite,
    'Create a new test suite inside a test plan.',
    {
      project: z.string().describe('Azure DevOps project name or ID'),
      planId: z.number().int().positive().describe('Test plan ID'),
      parentSuiteId: z.number().int().positive().describe('Parent suite ID (use the root suite ID from the plan)'),
      name: z.string().describe('Name of the test suite'),
      suiteType: z.enum(['staticTestSuite', 'dynamicTestSuite', 'requirementTestSuite']).optional().default('staticTestSuite').describe('Type of test suite')
    },
    async ({ project, planId, parentSuiteId, name, suiteType }) => {
      try {
        const connection = await getADOConnection();
        const testPlanApi = await connection.getTestPlanApi();
        const suiteCreateParams = {
          name,
          suiteType: suiteType || 'staticTestSuite',
          parentSuite: { id: parentSuiteId }
        };
        const suite = await testPlanApi.createTestSuite(suiteCreateParams, project, planId);
        return { content: [{ type: 'text', text: JSON.stringify(suite, null, 2) }] };
      } catch (error) {
        return { content: [{ type: 'text', text: error?.message || String(error) }], isError: true };
      }
    }
  );

  // Add test cases to a suite
  server.tool(
    TESTPLAN_TOOLS.add_test_cases_to_suite,
    'Add existing test case work items to a test suite.',
    {
      project: z.string().describe('Azure DevOps project name or ID'),
      planId: z.number().int().positive().describe('Test plan ID'),
      suiteId: z.number().int().positive().describe('Test suite ID'),
      testCaseIds: z.array(z.number().int().positive()).describe('Array of test case work item IDs to add')
    },
    async ({ project, planId, suiteId, testCaseIds }) => {
      try {
        const connection = await getADOConnection();
        const testPlanApi = await connection.getTestPlanApi();
        const testCaseRefs = testCaseIds.map(id => ({ workItem: { id } }));
        const result = await testPlanApi.addTestCasesToSuite(testCaseRefs, project, planId, suiteId);
        return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] };
      } catch (error) {
        return { content: [{ type: 'text', text: error?.message || String(error) }], isError: true };
      }
    }
  );

  // List test cases in a suite
  server.tool(
    TESTPLAN_TOOLS.list_test_cases,
    'List all test cases in a test suite. By default also includes test cases from child suites, since many suites are organized as containers whose test cases live in nested child suites.',
    {
      project: z.string().describe('Azure DevOps project name or ID'),
      planId: z.number().int().positive().describe('Test plan ID'),
      suiteId: z.number().int().positive().describe('Test suite ID'),
      includeChildSuites: z.boolean().optional().default(true).describe('If true (default), also include test cases from child/nested suites. Set to false to only return test cases directly assigned to this suite.'),
      top: z.number().int().positive().optional().describe('Maximum number of test cases to return')
    },
    async ({ project, planId, suiteId, includeChildSuites, top }) => {
      try {
        const connection = await getADOConnection();
        const testPlanApi = await connection.getTestPlanApi();
        // default to true explicitly since MCP clients may omit this optional param
        const isRecursive = includeChildSuites !== false;
        const testCases = (await testPlanApi.getTestCaseList(
          project, planId, suiteId,
          undefined, undefined, undefined, undefined, undefined, undefined, undefined,
          isRecursive
        )) || [];
        const result = top ? testCases.slice(0, top) : testCases;
        if (result.length === 0) {
          return { content: [{ type: 'text', text: `No test cases found for suite ${suiteId} in plan ${planId}, project "${project}". Verify the project name, plan ID, and suite ID are correct.` }] };
        }
        return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] };
      } catch (error) {
        return { content: [{ type: 'text', text: error?.message || String(error) }], isError: true };
      }
    }
  );

  // Create a test case work item
  server.tool(
    TESTPLAN_TOOLS.create_test_case,
    'Create a new test case work item with optional steps.',
    {
      project: z.string().describe('Azure DevOps project name or ID'),
      title: z.string().describe('Title of the test case'),
      areaPath: z.string().optional().describe('Area path for the test case'),
      iterationPath: z.string().optional().describe('Iteration path for the test case'),
      priority: z.number().int().min(1).max(4).optional().describe('Priority (1=Critical, 2=High, 3=Medium, 4=Low)'),
      steps: z.array(z.object({
        action: z.string().describe('Step action description'),
        expectedResult: z.string().optional().describe('Expected result for this step')
      })).optional().describe('List of test steps')
    },
    async ({ project, title, areaPath, iterationPath, priority, steps }) => {
      try {
        const connection = await getADOConnection();
        const witApi = await connection.getWorkItemTrackingApi();

        const patch = [
          { op: 'add', path: '/fields/System.Title', value: title },
          { op: 'add', path: '/fields/System.AreaPath', value: areaPath || project },
        ];

        if (iterationPath) patch.push({ op: 'add', path: '/fields/System.IterationPath', value: iterationPath });
        if (priority) patch.push({ op: 'add', path: '/fields/Microsoft.VSTS.Common.Priority', value: priority });

        if (steps && steps.length > 0) {
          const stepsXml = steps.map((s, i) =>
            `<step id="${i + 2}" type="ValidateStep">` +
            `<parameterizedString isformatted="true">${s.action}</parameterizedString>` +
            `<parameterizedString isformatted="true">${s.expectedResult || ''}</parameterizedString>` +
            `<description/></step>`
          ).join('');
          patch.push({ op: 'add', path: '/fields/Microsoft.VSTS.TCM.Steps', value: `<steps id="0" last="${steps.length + 1}">${stepsXml}</steps>` });
        }

        const testCase = await witApi.createWorkItem({}, patch, project, 'Test Case');
        return { content: [{ type: 'text', text: JSON.stringify(testCase, null, 2) }] };
      } catch (error) {
        return { content: [{ type: 'text', text: error?.message || String(error) }], isError: true };
      }
    }
  );

  // Update test case steps
  server.tool(
    TESTPLAN_TOOLS.update_test_case_steps,
    'Update the steps of an existing test case work item.',
    {
      project: z.string().describe('Azure DevOps project name or ID'),
      testCaseId: z.number().int().positive().describe('Test case work item ID'),
      steps: z.array(z.object({
        action: z.string().describe('Step action description'),
        expectedResult: z.string().optional().describe('Expected result for this step')
      })).describe('New list of test steps (replaces all existing steps)')
    },
    async ({ project, testCaseId, steps }) => {
      try {
        const connection = await getADOConnection();
        const witApi = await connection.getWorkItemTrackingApi();

        const stepsXml = steps.map((s, i) =>
          `<step id="${i + 2}" type="ValidateStep">` +
          `<parameterizedString isformatted="true">${s.action}</parameterizedString>` +
          `<parameterizedString isformatted="true">${s.expectedResult || ''}</parameterizedString>` +
          `<description/></step>`
        ).join('');

        const patch = [{
          op: 'replace',
          path: '/fields/Microsoft.VSTS.TCM.Steps',
          value: `<steps id="0" last="${steps.length + 1}">${stepsXml}</steps>`
        }];

        const updated = await witApi.updateWorkItem({}, patch, testCaseId, project);
        return { content: [{ type: 'text', text: JSON.stringify(updated, null, 2) }] };
      } catch (error) {
        return { content: [{ type: 'text', text: error?.message || String(error) }], isError: true };
      }
    }
  );

  // Get test results for a build
  server.tool(
    TESTPLAN_TOOLS.show_test_results_from_build_id,
    'Get test pass/fail results for a specific build. Returns test case titles, error messages, stack traces, and outcomes.',
    {
      project: z.string().describe('Azure DevOps project name or ID'),
      buildId: z.number().int().positive().describe('Build ID to retrieve test results for'),
      outcomes: z.array(z.enum(['passed', 'failed', 'aborted', 'inconclusive', 'notExecuted', 'blocked', 'notApplicable'])).optional().describe('Filter by test outcome(s)')
    },
    async ({ project, buildId, outcomes }) => {
      try {
        const connection = await getADOConnection();
        const testApi = await connection.getTestApi();
        const runs = await testApi.getTestRuns(project, undefined, undefined, buildId.toString());
        if (!runs || runs.length === 0) {
          return { content: [{ type: 'text', text: JSON.stringify({ buildId, testRuns: [] }, null, 2) }] };
        }
        const testRuns = [];
        for (const run of runs) {
          const results = await testApi.getTestResults(project, run.id);
          const filteredResults = (results || []).filter(r =>
            !outcomes || outcomes.length === 0 || outcomes.includes(r.outcome?.toLowerCase())
          ).map(r => ({
            testCaseTitle: r.testCaseTitle,
            outcome: r.outcome,
            errorMessage: r.errorMessage,
            stackTrace: r.stackTrace,
            durationInMs: r.durationInMs
          }));
          testRuns.push({ runId: run.id, runName: run.name, results: filteredResults });
        }
        return { content: [{ type: 'text', text: JSON.stringify({ buildId, testRuns }, null, 2) }] };
      } catch (error) {
        return { content: [{ type: 'text', text: error?.message || String(error) }], isError: true };
      }
    }
  );
}

export { TESTPLAN_TOOLS, configureTestPlanTools };
