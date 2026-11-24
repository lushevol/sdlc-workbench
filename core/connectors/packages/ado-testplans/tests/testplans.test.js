import { describe, it, expect, vi, beforeEach } from 'vitest';
import { configureTestPlanTools, TESTPLAN_TOOLS } from '../src/tools/testplans.js';
import { configureTestPlanPrompts } from '../src/prompts.js';
import { createMockServer, isValidToolResponse, isValidErrorResponse } from '@sc-node-mcp/shared-tests/helpers/mockServer';
import { createMockConnection, createMockTestPlanApi, createMockTestApi, createMockWitApi } from '@sc-node-mcp/shared-tests/helpers/mockConnection';

vi.mock('@sc-node-mcp/ado-core/connection', () => ({
  getADOConnection: vi.fn()
}));

describe('Test Plan Tools', () => {
  let mockServer;
  let mockConnection;
  let mockTestPlanApi;
  let mockTestApi;
  let mockWitApi;
  let getConnectionMock;

  beforeEach(() => {
    mockServer = createMockServer();
    mockConnection = createMockConnection();
    mockTestPlanApi = createMockTestPlanApi();
    mockTestApi = createMockTestApi();
    mockWitApi = createMockWitApi();
    mockConnection.getTestPlanApi.mockResolvedValue(mockTestPlanApi);
    mockConnection.getTestApi.mockResolvedValue(mockTestApi);
    mockConnection.getWorkItemTrackingApi.mockResolvedValue(mockWitApi);
    getConnectionMock = vi.fn().mockResolvedValue(mockConnection);
    configureTestPlanTools(mockServer, getConnectionMock);
  });

  describe('testplan_list_test_plans', () => {
    it('should list all test plans in a project', async () => {
      const testPlans = [
        { id: 1, name: 'Sprint 1 Tests' },
        { id: 2, name: 'Sprint 2 Tests' }
      ];
      mockTestPlanApi.getTestPlans.mockResolvedValue(testPlans);

      const response = await mockServer.invokeTool(TESTPLAN_TOOLS.list_test_plans, {
        project: 'TestProject'
      });

      expect(isValidToolResponse(response)).toBe(true);
      const result = JSON.parse(response.content[0].text);
      expect(result).toHaveLength(2);
      expect(result[0].name).toBe('Sprint 1 Tests');
    });

    it('should filter by active plans when filterActivePlans is true', async () => {
      const allPlans = [
        { id: 1, name: 'Active Plan', state: 'Active' },
        { id: 2, name: 'Inactive Plan', state: 'Inactive' }
      ];
      mockTestPlanApi.getTestPlans.mockResolvedValue(allPlans);

      const response = await mockServer.invokeTool(TESTPLAN_TOOLS.list_test_plans, {
        project: 'TestProject',
        filterActivePlans: true
      });

      expect(isValidToolResponse(response)).toBe(true);
      const result = JSON.parse(response.content[0].text);
      expect(result).toHaveLength(1);
      expect(result[0].name).toBe('Active Plan');
    });

    it('should return all plans when filterActivePlans is false', async () => {
      const allPlans = [
        { id: 1, name: 'Active Plan', state: 'Active' },
        { id: 2, name: 'Closed Plan', state: 'Closed' }
      ];
      mockTestPlanApi.getTestPlans.mockResolvedValue(allPlans);

      const response = await mockServer.invokeTool(TESTPLAN_TOOLS.list_test_plans, {
        project: 'TestProject',
        filterActivePlans: false
      });

      expect(isValidToolResponse(response)).toBe(true);
      const result = JSON.parse(response.content[0].text);
      expect(result).toHaveLength(2);
    });

    it('should return a helpful message when the API returns null (invalid/empty project)', async () => {
      mockTestPlanApi.getTestPlans.mockResolvedValue(null);

      const response = await mockServer.invokeTool(TESTPLAN_TOOLS.list_test_plans, {
        project: 'NonExistentProject'
      });

      expect(isValidToolResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('No test plans found');
      expect(response.content[0].text).toContain('NonExistentProject');
    });

    it('should return error on API failure', async () => {
      mockTestPlanApi.getTestPlans.mockRejectedValue(new Error('Project not found'));

      const response = await mockServer.invokeTool(TESTPLAN_TOOLS.list_test_plans, {
        project: 'TestProject'
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('Project not found');
    });

    it('should handle non-Error thrown values', async () => {
      mockTestPlanApi.getTestPlans.mockRejectedValue('raw plan error');
      const response = await mockServer.invokeTool(TESTPLAN_TOOLS.list_test_plans, {
        project: 'TestProject'
      });
      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('raw plan error');
    });
  });

  describe('testplan_create_test_plan', () => {
    it('should create a test plan with all parameters', async () => {
      const testPlan = { id: 10, name: 'My Test Plan' };
      mockTestPlanApi.createTestPlan.mockResolvedValue(testPlan);

      const response = await mockServer.invokeTool(TESTPLAN_TOOLS.create_test_plan, {
        project: 'TestProject',
        name: 'My Test Plan',
        iteration: 'TestProject/Sprint 1',
        startDate: '2024-01-01T00:00:00Z',
        endDate: '2024-01-15T00:00:00Z'
      });

      expect(isValidToolResponse(response)).toBe(true);
      const result = JSON.parse(response.content[0].text);
      expect(result.id).toBe(10);
      expect(mockTestPlanApi.createTestPlan).toHaveBeenCalledWith(
        expect.objectContaining({ name: 'My Test Plan', iteration: 'TestProject/Sprint 1' }),
        'TestProject'
      );
    });

    it('should create a test plan with only required parameters', async () => {
      mockTestPlanApi.createTestPlan.mockResolvedValue({ id: 11, name: 'Basic Plan' });

      const response = await mockServer.invokeTool(TESTPLAN_TOOLS.create_test_plan, {
        project: 'TestProject',
        name: 'Basic Plan',
        iteration: 'TestProject/Iteration 1'
      });

      expect(isValidToolResponse(response)).toBe(true);
    });

    it('should return error on API failure', async () => {
      mockTestPlanApi.createTestPlan.mockRejectedValue(new Error('Invalid iteration path'));

      const response = await mockServer.invokeTool(TESTPLAN_TOOLS.create_test_plan, {
        project: 'TestProject',
        name: 'My Plan',
        iteration: 'Invalid/Path'
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('Invalid iteration path');
    });

    it('should handle non-Error thrown values', async () => {
      mockTestPlanApi.createTestPlan.mockRejectedValue('raw plan create error');
      const response = await mockServer.invokeTool(TESTPLAN_TOOLS.create_test_plan, {
        project: 'TestProject',
        name: 'My Plan',
        iteration: 'TestProject/Sprint 1'
      });
      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('raw plan create error');
    });
  });

  describe('testplan_list_test_suites', () => {
    it('should list test suites in a plan', async () => {
      const suites = [
        { id: 1, name: 'Root Suite' },
        { id: 2, name: 'Login Tests' }
      ];
      mockTestPlanApi.getTestSuitesForPlan.mockResolvedValue(suites);

      const response = await mockServer.invokeTool(TESTPLAN_TOOLS.list_test_suites, {
        project: 'TestProject',
        planId: 5
      });

      expect(isValidToolResponse(response)).toBe(true);
      const result = JSON.parse(response.content[0].text);
      expect(result).toHaveLength(2);
    });

    it('should return a helpful message when the API returns null (invalid plan/project)', async () => {
      mockTestPlanApi.getTestSuitesForPlan.mockResolvedValue(null);

      const response = await mockServer.invokeTool(TESTPLAN_TOOLS.list_test_suites, {
        project: 'TestProject',
        planId: 999
      });

      expect(isValidToolResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('No test suites found');
    });

    it('should return error on API failure', async () => {
      mockTestPlanApi.getTestSuitesForPlan.mockRejectedValue(new Error('Plan not found'));

      const response = await mockServer.invokeTool(TESTPLAN_TOOLS.list_test_suites, {
        project: 'TestProject',
        planId: 999
      });

      expect(isValidErrorResponse(response)).toBe(true);
    });

    it('should handle non-Error thrown values', async () => {
      mockTestPlanApi.getTestSuitesForPlan.mockRejectedValue('raw suite list error');
      const response = await mockServer.invokeTool(TESTPLAN_TOOLS.list_test_suites, {
        project: 'TestProject',
        planId: 5
      });
      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('raw suite list error');
    });
  });

  describe('testplan_create_test_suite', () => {
    it('should create a test suite in a plan', async () => {
      const suite = { id: 20, name: 'New Test Suite' };
      mockTestPlanApi.createTestSuite.mockResolvedValue(suite);

      const response = await mockServer.invokeTool(TESTPLAN_TOOLS.create_test_suite, {
        project: 'TestProject',
        planId: 5,
        parentSuiteId: 1,
        name: 'New Test Suite'
      });

      expect(isValidToolResponse(response)).toBe(true);
      const result = JSON.parse(response.content[0].text);
      expect(result.id).toBe(20);
    });

    it('should return error on API failure', async () => {
      mockTestPlanApi.createTestSuite.mockRejectedValue(new Error('Suite creation failed'));

      const response = await mockServer.invokeTool(TESTPLAN_TOOLS.create_test_suite, {
        project: 'TestProject',
        planId: 5,
        parentSuiteId: 1,
        name: 'Bad Suite'
      });

      expect(isValidErrorResponse(response)).toBe(true);
    });

    it('should handle non-Error thrown values', async () => {
      mockTestPlanApi.createTestSuite.mockRejectedValue('raw suite create error');
      const response = await mockServer.invokeTool(TESTPLAN_TOOLS.create_test_suite, {
        project: 'TestProject',
        planId: 5,
        parentSuiteId: 1,
        name: 'My Suite'
      });
      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('raw suite create error');
    });
  });

  describe('testplan_add_test_cases_to_suite', () => {
    it('should add test cases to a suite', async () => {
      const result = { count: 2 };
      mockTestPlanApi.addTestCasesToSuite.mockResolvedValue(result);

      const response = await mockServer.invokeTool(TESTPLAN_TOOLS.add_test_cases_to_suite, {
        project: 'TestProject',
        planId: 5,
        suiteId: 10,
        testCaseIds: [101, 102]
      });

      expect(isValidToolResponse(response)).toBe(true);
    });

    it('should return error on API failure', async () => {
      mockTestPlanApi.addTestCasesToSuite.mockRejectedValue(new Error('Test case not found'));

      const response = await mockServer.invokeTool(TESTPLAN_TOOLS.add_test_cases_to_suite, {
        project: 'TestProject',
        planId: 5,
        suiteId: 10,
        testCaseIds: [999]
      });

      expect(isValidErrorResponse(response)).toBe(true);
    });

    it('should handle non-Error thrown values', async () => {
      mockTestPlanApi.addTestCasesToSuite.mockRejectedValue('raw add error');
      const response = await mockServer.invokeTool(TESTPLAN_TOOLS.add_test_cases_to_suite, {
        project: 'TestProject',
        planId: 5,
        suiteId: 10,
        testCaseIds: [101]
      });
      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('raw add error');
    });
  });

  describe('testplan_list_test_cases', () => {
    it('should list test cases in a suite', async () => {
      const testCases = [
        { workItem: { id: 101, name: 'Login test' } },
        { workItem: { id: 102, name: 'Logout test' } }
      ];
      mockTestPlanApi.getTestCaseList.mockResolvedValue(testCases);

      const response = await mockServer.invokeTool(TESTPLAN_TOOLS.list_test_cases, {
        project: 'TestProject',
        planId: 5,
        suiteId: 10
      });

      expect(isValidToolResponse(response)).toBe(true);
      const result = JSON.parse(response.content[0].text);
      expect(result).toHaveLength(2);
    });

    it('should default to including test cases from child suites (isRecursive=true)', async () => {
      mockTestPlanApi.getTestCaseList.mockResolvedValue([{ workItem: { id: 101 } }]);

      await mockServer.invokeTool(TESTPLAN_TOOLS.list_test_cases, {
        project: 'TestProject',
        planId: 5,
        suiteId: 10
      });

      expect(mockTestPlanApi.getTestCaseList).toHaveBeenCalledWith(
        'TestProject', 5, 10,
        undefined, undefined, undefined, undefined, undefined, undefined, undefined,
        true
      );
    });

    it('should only return direct test cases when includeChildSuites is false', async () => {
      mockTestPlanApi.getTestCaseList.mockResolvedValue([{ workItem: { id: 101 } }]);

      await mockServer.invokeTool(TESTPLAN_TOOLS.list_test_cases, {
        project: 'TestProject',
        planId: 5,
        suiteId: 10,
        includeChildSuites: false
      });

      expect(mockTestPlanApi.getTestCaseList).toHaveBeenCalledWith(
        'TestProject', 5, 10,
        undefined, undefined, undefined, undefined, undefined, undefined, undefined,
        false
      );
    });

    it('should return a helpful message when the API returns null (invalid suite/plan/project)', async () => {
      mockTestPlanApi.getTestCaseList.mockResolvedValue(null);

      const response = await mockServer.invokeTool(TESTPLAN_TOOLS.list_test_cases, {
        project: 'TestProject',
        planId: 5,
        suiteId: 999
      });

      expect(isValidToolResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('No test cases found');
    });

    it('should return error on API failure', async () => {
      mockTestPlanApi.getTestCaseList.mockRejectedValue(new Error('Suite not found'));

      const response = await mockServer.invokeTool(TESTPLAN_TOOLS.list_test_cases, {
        project: 'TestProject',
        planId: 5,
        suiteId: 999
      });

      expect(isValidErrorResponse(response)).toBe(true);
    });

    it('should handle non-Error thrown values', async () => {
      mockTestPlanApi.getTestCaseList.mockRejectedValue('raw list cases error');
      const response = await mockServer.invokeTool(TESTPLAN_TOOLS.list_test_cases, {
        project: 'TestProject',
        planId: 5,
        suiteId: 10
      });
      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('raw list cases error');
    });
  });

  describe('testplan_create_test_case', () => {
    it('should create a test case with title and optional steps', async () => {
      const testCase = { id: 201 };
      mockWitApi.createWorkItem.mockResolvedValue(testCase);

      const steps = [
        { action: 'Navigate to login', expectedResult: 'Login page appears' }
      ];
      const response = await mockServer.invokeTool(TESTPLAN_TOOLS.create_test_case, {
        project: 'TestProject',
        title: 'Test login functionality',
        priority: 2,
        steps
      });

      expect(isValidToolResponse(response)).toBe(true);
      const result = JSON.parse(response.content[0].text);
      expect(result.id).toBe(201);
    });

    it('should create a test case without steps', async () => {
      mockWitApi.createWorkItem.mockResolvedValue({ id: 202 });

      const response = await mockServer.invokeTool(TESTPLAN_TOOLS.create_test_case, {
        project: 'TestProject',
        title: 'Minimal test case'
      });

      expect(isValidToolResponse(response)).toBe(true);
    });

    it('should return error on API failure', async () => {
      mockWitApi.createWorkItem.mockRejectedValue(new Error('Unauthorized'));

      const response = await mockServer.invokeTool(TESTPLAN_TOOLS.create_test_case, {
        project: 'TestProject',
        title: 'Test case'
      });

      expect(isValidErrorResponse(response)).toBe(true);
    });

    it('should handle non-Error thrown values', async () => {
      mockWitApi.createWorkItem.mockRejectedValue('raw create case error');
      const response = await mockServer.invokeTool(TESTPLAN_TOOLS.create_test_case, {
        project: 'TestProject',
        title: 'Test case'
      });
      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('raw create case error');
    });
  });

  describe('testplan_update_test_case_steps', () => {
    it('should update test case steps', async () => {
      const updatedTestCase = { id: 201 };
      mockWitApi.updateWorkItem.mockResolvedValue(updatedTestCase);

      const steps = [
        { action: 'Open browser', expectedResult: 'Browser opens' },
        { action: 'Navigate to URL', expectedResult: 'Page loads' }
      ];
      const response = await mockServer.invokeTool(TESTPLAN_TOOLS.update_test_case_steps, {
        project: 'TestProject',
        testCaseId: 201,
        steps
      });

      expect(isValidToolResponse(response)).toBe(true);
      expect(mockWitApi.updateWorkItem).toHaveBeenCalledWith(
        {},
        expect.any(Array),
        201,
        'TestProject'
      );
    });

    it('should return error on API failure', async () => {
      mockWitApi.updateWorkItem.mockRejectedValue(new Error('Test case not found'));

      const response = await mockServer.invokeTool(TESTPLAN_TOOLS.update_test_case_steps, {
        project: 'TestProject',
        testCaseId: 999,
        steps: []
      });

      expect(isValidErrorResponse(response)).toBe(true);
    });

    it('should handle steps without expectedResult', async () => {
      mockWitApi.updateWorkItem.mockResolvedValue({ id: 201 });
      const response = await mockServer.invokeTool(TESTPLAN_TOOLS.update_test_case_steps, {
        project: 'TestProject',
        testCaseId: 201,
        steps: [{ action: 'Click button' }]
      });
      expect(isValidToolResponse(response)).toBe(true);
    });

    it('should handle non-Error thrown values', async () => {
      mockWitApi.updateWorkItem.mockRejectedValue('raw update steps error');
      const response = await mockServer.invokeTool(TESTPLAN_TOOLS.update_test_case_steps, {
        project: 'TestProject',
        testCaseId: 201,
        steps: [{ action: 'Click' }]
      });
      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('raw update steps error');
    });
  });

  describe('testplan_show_test_results_from_build_id', () => {
    it('should return test results for a build', async () => {
      const testRuns = [{ id: 301, name: 'Test Run 1' }];
      const testResults = [
        { id: 1, outcome: 'Passed', testCase: { name: 'Test A' } },
        { id: 2, outcome: 'Failed', testCase: { name: 'Test B' } }
      ];
      mockTestApi.getTestRuns.mockResolvedValue(testRuns);
      mockTestApi.getTestResults.mockResolvedValue(testResults);

      const response = await mockServer.invokeTool(TESTPLAN_TOOLS.show_test_results_from_build_id, {
        project: 'TestProject',
        buildId: 789
      });

      expect(isValidToolResponse(response)).toBe(true);
      const result = JSON.parse(response.content[0].text);
      expect(result.buildId).toBe(789);
      expect(result.testRuns).toHaveLength(1);
    });

    it('should return empty results when no test runs exist for build', async () => {
      mockTestApi.getTestRuns.mockResolvedValue([]);

      const response = await mockServer.invokeTool(TESTPLAN_TOOLS.show_test_results_from_build_id, {
        project: 'TestProject',
        buildId: 999
      });

      expect(isValidToolResponse(response)).toBe(true);
      const result = JSON.parse(response.content[0].text);
      expect(result.testRuns).toHaveLength(0);
    });

    it('should return error on API failure', async () => {
      mockTestApi.getTestRuns.mockRejectedValue(new Error('Project not found'));

      const response = await mockServer.invokeTool(TESTPLAN_TOOLS.show_test_results_from_build_id, {
        project: 'TestProject',
        buildId: 789
      });

      expect(isValidErrorResponse(response)).toBe(true);
    });

    it('should filter results by outcomes when provided', async () => {
      const testRuns = [{ id: 301, name: 'Test Run 1' }];
      const testResults = [
        { outcome: 'Passed', testCaseTitle: 'Test A', errorMessage: null, stackTrace: null, durationInMs: 100 },
        { outcome: 'Failed', testCaseTitle: 'Test B', errorMessage: 'err', stackTrace: null, durationInMs: 200 }
      ];
      mockTestApi.getTestRuns.mockResolvedValue(testRuns);
      mockTestApi.getTestResults.mockResolvedValue(testResults);
      const response = await mockServer.invokeTool(TESTPLAN_TOOLS.show_test_results_from_build_id, {
        project: 'TestProject',
        buildId: 789,
        outcomes: ['passed']
      });
      expect(isValidToolResponse(response)).toBe(true);
      const result = JSON.parse(response.content[0].text);
      expect(result.testRuns[0].results).toHaveLength(1);
    });

    it('should handle non-Error thrown values', async () => {
      mockTestApi.getTestRuns.mockRejectedValue('raw results error');
      const response = await mockServer.invokeTool(TESTPLAN_TOOLS.show_test_results_from_build_id, {
        project: 'TestProject',
        buildId: 789
      });
      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('raw results error');
    });
  });

  describe('TESTPLAN_TOOLS constants', () => {
    it('should define all expected tool name constants', () => {
      expect(TESTPLAN_TOOLS.list_test_plans).toBe('testplan_list_test_plans');
      expect(TESTPLAN_TOOLS.create_test_plan).toBe('testplan_create_test_plan');
      expect(TESTPLAN_TOOLS.list_test_suites).toBe('testplan_list_test_suites');
      expect(TESTPLAN_TOOLS.create_test_suite).toBe('testplan_create_test_suite');
      expect(TESTPLAN_TOOLS.add_test_cases_to_suite).toBe('testplan_add_test_cases_to_suite');
      expect(TESTPLAN_TOOLS.list_test_cases).toBe('testplan_list_test_cases');
      expect(TESTPLAN_TOOLS.create_test_case).toBe('testplan_create_test_case');
      expect(TESTPLAN_TOOLS.update_test_case_steps).toBe('testplan_update_test_case_steps');
      expect(TESTPLAN_TOOLS.show_test_results_from_build_id).toBe('testplan_show_test_results_from_build_id');
    });

    it('should register all 9 tools on the server', () => {
      expect(mockServer.registeredTools.size).toBe(9);
    });
  });

  describe('testplan_list_test_plans - top parameter', () => {
    it('should limit results when top is provided', async () => {
      const plans = [
        { id: 1, name: 'Plan A', state: 'Active' },
        { id: 2, name: 'Plan B', state: 'Active' },
        { id: 3, name: 'Plan C', state: 'Active' }
      ];
      mockTestPlanApi.getTestPlans.mockResolvedValue(plans);

      const response = await mockServer.invokeTool(TESTPLAN_TOOLS.list_test_plans, {
        project: 'TestProject',
        top: 2
      });

      expect(isValidToolResponse(response)).toBe(true);
      const result = JSON.parse(response.content[0].text);
      expect(result).toHaveLength(2);
    });
  });

  describe('testplan_list_test_suites - top parameter', () => {
    it('should limit results when top is provided', async () => {
      const suites = [
        { id: 1, name: 'Suite A' },
        { id: 2, name: 'Suite B' },
        { id: 3, name: 'Suite C' }
      ];
      mockTestPlanApi.getTestSuitesForPlan.mockResolvedValue(suites);

      const response = await mockServer.invokeTool(TESTPLAN_TOOLS.list_test_suites, {
        project: 'TestProject',
        planId: 5,
        top: 1
      });

      expect(isValidToolResponse(response)).toBe(true);
      const result = JSON.parse(response.content[0].text);
      expect(result).toHaveLength(1);
    });
  });

  describe('testplan_list_test_cases - top parameter', () => {
    it('should limit results when top is provided', async () => {
      const testCases = [
        { workItem: { id: 101, name: 'TC 1' } },
        { workItem: { id: 102, name: 'TC 2' } },
        { workItem: { id: 103, name: 'TC 3' } }
      ];
      mockTestPlanApi.getTestCaseList.mockResolvedValue(testCases);

      const response = await mockServer.invokeTool(TESTPLAN_TOOLS.list_test_cases, {
        project: 'TestProject',
        planId: 5,
        suiteId: 10,
        top: 2
      });

      expect(isValidToolResponse(response)).toBe(true);
      const result = JSON.parse(response.content[0].text);
      expect(result).toHaveLength(2);
    });
  });

  describe('testplan_create_test_case - optional fields', () => {
    it('should create a test case with areaPath and iterationPath', async () => {
      mockWitApi.createWorkItem.mockResolvedValue({ id: 203 });

      const response = await mockServer.invokeTool(TESTPLAN_TOOLS.create_test_case, {
        project: 'TestProject',
        title: 'Test with area',
        areaPath: 'TestProject/Area',
        iterationPath: 'TestProject/Sprint 1',
        priority: 1,
        steps: [{ action: 'Do something' }]
      });

      expect(isValidToolResponse(response)).toBe(true);
    });
  });

  describe('testplan_show_test_results_from_build_id - outcomes filter', () => {
    it('should filter results by outcome', async () => {
      const testRuns = [{ id: 401, name: 'Run 1' }];
      const testResults = [
        { id: 1, outcome: 'Passed', testCaseTitle: 'Test A' },
        { id: 2, outcome: 'Failed', testCaseTitle: 'Test B' }
      ];
      mockTestApi.getTestRuns.mockResolvedValue(testRuns);
      mockTestApi.getTestResults.mockResolvedValue(testResults);

      const response = await mockServer.invokeTool(TESTPLAN_TOOLS.show_test_results_from_build_id, {
        project: 'TestProject',
        buildId: 101,
        outcomes: ['failed']
      });

      expect(isValidToolResponse(response)).toBe(true);
      const result = JSON.parse(response.content[0].text);
      expect(result.testRuns[0].results).toHaveLength(1);
      expect(result.testRuns[0].results[0].outcome).toBe('Failed');
    });
  });

  describe('Test Plan Prompts', () => {
    it('should register all prompts on the server', () => {
      const server = createMockServer();
      server.prompt = vi.fn();
      configureTestPlanPrompts(server);
      expect(server.prompt).toHaveBeenCalledTimes(9);
    });

    it('should invoke all prompt callbacks and cover message generators', async () => {
      const storedCallbacks = new Map();
      const server = createMockServer();
      server.prompt = vi.fn((name, _desc, _args, callback) => {
        storedCallbacks.set(name, callback);
      });
      configureTestPlanPrompts(server);

      const listResult = await storedCallbacks.get('list-test-plans')({ project: 'MyProject', filterActivePlans: 'true' });
      expect(listResult.messages[0].content.text).toContain('testplan_list_test_plans');

      const listNoFilterResult = await storedCallbacks.get('list-test-plans')({ project: 'MyProject' });
      expect(listNoFilterResult.messages[0].content.text).toContain('testplan_list_test_plans');

      const createPlanResult = await storedCallbacks.get('create-test-plan')({ project: 'MyProject', name: 'Sprint 1 Tests', iteration: 'MyProject/Sprint 1', startDate: '2024-01-01', endDate: '2024-01-15' });
      expect(createPlanResult.messages[0].content.text).toContain('testplan_create_test_plan');

      const listSuitesResult = await storedCallbacks.get('list-test-suites')({ project: 'MyProject', planId: '5' });
      expect(listSuitesResult.messages[0].content.text).toContain('testplan_list_test_suites');

      const createSuiteResult = await storedCallbacks.get('create-test-suite')({ project: 'MyProject', planId: '5', parentSuiteId: '1', name: 'Login Tests' });
      expect(createSuiteResult.messages[0].content.text).toContain('testplan_create_test_suite');

      const addCasesResult = await storedCallbacks.get('add-test-cases-to-suite')({ project: 'MyProject', planId: '5', suiteId: '10', testCaseIds: '101,102' });
      expect(addCasesResult.messages[0].content.text).toContain('testplan_add_test_cases_to_suite');

      const listCasesResult = await storedCallbacks.get('list-test-cases')({ project: 'MyProject', planId: '5', suiteId: '10' });
      expect(listCasesResult.messages[0].content.text).toContain('testplan_list_test_cases');

      const createCaseResult = await storedCallbacks.get('create-test-case')({ project: 'MyProject', title: 'Login test', priority: '2', steps: '[{"action":"Click"}]' });
      expect(createCaseResult.messages[0].content.text).toContain('testplan_create_test_case');

      const createCaseNoExtrasResult = await storedCallbacks.get('create-test-case')({ project: 'MyProject', title: 'Simple test' });
      expect(createCaseNoExtrasResult.messages[0].content.text).toContain('testplan_create_test_case');

      const updateStepsResult = await storedCallbacks.get('update-test-case-steps')({ testCaseId: '201', steps: '[{"action":"Click"}]' });
      expect(updateStepsResult.messages[0].content.text).toContain('testplan_update_test_case_steps');

      const buildResultsResult = await storedCallbacks.get('show-build-test-results')({ project: 'MyProject', buildId: '789' });
      expect(buildResultsResult.messages[0].content.text).toContain('testplan_show_test_results_from_build_id');
    });

    it('should use context project when not provided in args', async () => {
      const storedCallbacks = new Map();
      const server = createMockServer();
      server.prompt = vi.fn((name, _desc, _args, callback) => {
        storedCallbacks.set(name, callback);
      });
      const getContext = vi.fn().mockReturnValue({ ado: { project: 'CtxProject' } });
      configureTestPlanPrompts(server, { getContext });

      const result = await storedCallbacks.get('list-test-plans')({});
      expect(result.messages[0].content.text).toContain('CtxProject');
    });
  });
});
