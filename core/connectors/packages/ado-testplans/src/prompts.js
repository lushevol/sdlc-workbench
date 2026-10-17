import { z } from 'zod';

export function configureTestPlanPrompts(server, { getContext = () => null } = {}) {
  const prompts = [
    {
      name: 'list-test-plans',
      description: 'List test plans in an Azure DevOps project',
      args: {
        project: z.string().optional().describe('Azure DevOps project name or ID'),
        filterActivePlans: z.string().optional().describe('Set to "true" to return only active test plans')
      }
    },
    {
      name: 'create-test-plan',
      description: 'Create a new test plan in a project',
      args: {
        project: z.string().optional().describe('Azure DevOps project name or ID'),
        name: z.string().describe('Name of the test plan'),
        iteration: z.string().describe('Iteration path (e.g., "MyProject/Sprint 1")'),
        startDate: z.string().optional().describe('Start date in ISO 8601 format'),
        endDate: z.string().optional().describe('End date in ISO 8601 format')
      }
    },
    {
      name: 'list-test-suites',
      description: 'List test suites in a test plan',
      args: {
        project: z.string().optional().describe('Azure DevOps project name or ID'),
        planId: z.string().describe('Test plan ID')
      }
    },
    {
      name: 'create-test-suite',
      description: 'Create a new test suite in a test plan',
      args: {
        project: z.string().optional().describe('Azure DevOps project name or ID'),
        planId: z.string().describe('Test plan ID'),
        parentSuiteId: z.string().describe('Parent suite ID'),
        name: z.string().describe('Name of the test suite')
      }
    },
    {
      name: 'add-test-cases-to-suite',
      description: 'Add existing test cases to a test suite',
      args: {
        project: z.string().optional().describe('Azure DevOps project name or ID'),
        planId: z.string().describe('Test plan ID'),
        suiteId: z.string().describe('Test suite ID'),
        testCaseIds: z.string().describe('Comma-separated test case IDs to add')
      }
    },
    {
      name: 'list-test-cases',
      description: 'List test cases in a test suite',
      args: {
        project: z.string().optional().describe('Azure DevOps project name or ID'),
        planId: z.string().describe('Test plan ID'),
        suiteId: z.string().describe('Test suite ID')
      }
    },
    {
      name: 'create-test-case',
      description: 'Create a new test case work item',
      args: {
        project: z.string().optional().describe('Azure DevOps project name or ID'),
        title: z.string().describe('Title of the test case'),
        priority: z.string().optional().describe('Priority: 1=Critical, 2=High, 3=Medium, 4=Low'),
        steps: z.string().optional().describe('JSON array of steps with action and expectedResult')
      }
    },
    {
      name: 'update-test-case-steps',
      description: 'Update the steps of an existing test case',
      args: {
        project: z.string().optional().describe('Azure DevOps project name or ID'),
        testCaseId: z.string().describe('Test case work item ID'),
        steps: z.string().describe('JSON array of steps with action and expectedResult')
      }
    },
    {
      name: 'show-build-test-results',
      description: 'Show test results for a specific build',
      args: {
        project: z.string().optional().describe('Azure DevOps project name or ID'),
        buildId: z.string().describe('Build ID to retrieve test results for')
      }
    }
  ];

  const messages = {
    'list-test-plans': (args, ctx) => {
      const project = args.project || ctx?.ado?.project || '(required)';
      const activeFilter = args.filterActivePlans === 'true' ? ' (active plans only)' : '';
      return `List test plans in project "${project}"${activeFilter}.\n\nUse testplan_list_test_plans with project "${project}"${args.filterActivePlans === 'true' ? ' and filterActivePlans true' : ''}.`;
    },
    'create-test-plan': (args, ctx) => {
      const project = args.project || ctx?.ado?.project || '(required)';
      const dates = [
        args.startDate ? `startDate: ${args.startDate}` : null,
        args.endDate ? `endDate: ${args.endDate}` : null
      ].filter(Boolean).join(', ');
      const dateLine = dates ? `\nDates: ${dates}` : '';
      return `Create test plan "${args.name}" in project "${project}".\nIteration: ${args.iteration}${dateLine}\n\nUse testplan_create_test_plan with project "${project}", name "${args.name}", and iteration "${args.iteration}".`;
    },
    'list-test-suites': (args, ctx) => {
      const project = args.project || ctx?.ado?.project || '(required)';
      return `List test suites in plan ${args.planId} for project "${project}".\n\nUse testplan_list_test_suites with project "${project}" and planId ${args.planId}.`;
    },
    'create-test-suite': (args, ctx) => {
      const project = args.project || ctx?.ado?.project || '(required)';
      return `Create test suite "${args.name}" in plan ${args.planId} under parent suite ${args.parentSuiteId} in project "${project}".\n\nUse testplan_create_test_suite with project "${project}", planId ${args.planId}, parentSuiteId ${args.parentSuiteId}, and name "${args.name}".`;
    },
    'add-test-cases-to-suite': (args, ctx) => {
      const project = args.project || ctx?.ado?.project || '(required)';
      return `Add test cases [${args.testCaseIds}] to suite ${args.suiteId} in plan ${args.planId} for project "${project}".\n\nUse testplan_add_test_cases_to_suite with project "${project}", planId ${args.planId}, suiteId ${args.suiteId}, and testCaseIds array.`;
    },
    'list-test-cases': (args, ctx) => {
      const project = args.project || ctx?.ado?.project || '(required)';
      return `List test cases in suite ${args.suiteId} of plan ${args.planId} for project "${project}".\n\nUse testplan_list_test_cases with project "${project}", planId ${args.planId}, and suiteId ${args.suiteId}.`;
    },
    'create-test-case': (args, ctx) => {
      const project = args.project || ctx?.ado?.project || '(required)';
      const extras = [
        args.priority ? `priority: ${args.priority}` : null,
        args.steps ? 'with steps' : null
      ].filter(Boolean).join(', ');
      const extrasLine = extras ? ` (${extras})` : '';
      const priorityParam = args.priority ? ` and priority ${args.priority}` : '';
      return `Create test case "${args.title}" in project "${project}"${extrasLine}.\n\nUse testplan_create_test_case with project "${project}" and title "${args.title}"${priorityParam}.`;
    },
    'update-test-case-steps': (args, ctx) => {
      const project = args.project || ctx?.ado?.project || '';
      const projectNote = project ? ` (project: ${project})` : '';
      return `Update steps for test case ${args.testCaseId}${projectNote}.\n\nUse testplan_update_test_case_steps with id ${args.testCaseId} and the steps array.`;
    },
    'show-build-test-results': (args, ctx) => {
      const project = args.project || ctx?.ado?.project || '(required)';
      return `Show test results for build ${args.buildId} in project "${project}".\n\nUse testplan_show_test_results_from_build_id with project "${project}" and buildId ${args.buildId}.`;
    }
  };

  for (const prompt of prompts) {
    const callback = async (args) => {
      const ctx = getContext();
      const text = messages[prompt.name](args ?? {}, ctx);
      return { messages: [{ role: 'user', content: { type: 'text', text } }] };
    };
    server.prompt(prompt.name, prompt.description, prompt.args, callback);
  }

  console.error(`Registered ${prompts.length} test plan prompts`);
}
