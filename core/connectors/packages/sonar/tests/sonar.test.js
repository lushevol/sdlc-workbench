import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { configureSonarApiTools } from '../src/tools/sonar.js';
import { createMockServer, isValidToolResponse, isValidErrorResponse } from '@sc-node-mcp/shared-tests/helpers/mockServer';

// ── Axios mock ───────────────────────────────────────────────────────────────
vi.mock('axios', () => {
  const mockInstance = {
    get: vi.fn()
  };
  return {
    default: {
      create: vi.fn(() => mockInstance)
    },
    __mockInstance: mockInstance
  };
});

import axios from 'axios';

const MOCK_SONAR_CONN = {
  baseUrl: 'https://sonarqube.vx.standardchartered.com',
  headers: {
    Authorization: 'Bearer test-token',
    Accept: 'application/json',
    'Content-Type': 'application/json'
  }
};

function getMockAxiosInstance() {
  return axios.create();
}

// ── Tests ────────────────────────────────────────────────────────────────────

describe('sonar_search_projects', () => {
  let mockServer;

  beforeEach(() => {
    mockServer = createMockServer();
    configureSonarApiTools(mockServer, () => MOCK_SONAR_CONN);
  });

  afterEach(() => {
    vi.clearAllMocks();
  });

  it('returns a valid response with project list', async () => {
    getMockAxiosInstance().get.mockResolvedValueOnce({
      data: {
        components: [
          { key: 'my-project', name: 'My Project', qualifier: 'TRK', lastAnalysisDate: '2026-04-01' }
        ]
      }
    });

    const response = await mockServer.invokeTool('sonar_search_projects', {});
    expect(isValidToolResponse(response)).toBe(true);
    expect(response.content[0].text).toContain('my-project');
  });

  it('handles missing components array gracefully', async () => {
    getMockAxiosInstance().get.mockResolvedValueOnce({ data: {} });

    const response = await mockServer.invokeTool('sonar_search_projects', {});
    expect(isValidToolResponse(response)).toBe(true);
    expect(response.content[0].text).toContain('0 project(s)');
  });

  it('uses N/A when project lastAnalysisDate is absent', async () => {
    getMockAxiosInstance().get.mockResolvedValueOnce({
      data: {
        components: [{ key: 'p', name: 'P', qualifier: 'TRK' }]
      }
    });

    const response = await mockServer.invokeTool('sonar_search_projects', {});
    expect(isValidToolResponse(response)).toBe(true);
    expect(response.content[0].text).toContain('N/A');
  });

  it('filters by query when provided', async () => {
    getMockAxiosInstance().get.mockResolvedValueOnce({
      data: { components: [] }
    });

    const response = await mockServer.invokeTool('sonar_search_projects', { query: 'foo' });
    expect(isValidToolResponse(response)).toBe(true);
    expect(response.content[0].text).toContain('matching "foo"');
  });

  it('returns an error response when axios throws', async () => {
    getMockAxiosInstance().get.mockRejectedValueOnce(new Error('Network error'));

    const response = await mockServer.invokeTool('sonar_search_projects', {});
    expect(isValidErrorResponse(response)).toBe(true);
    expect(response.content[0].text).toContain('Network error');
  });

  it('returns string representation when error has no message property', async () => {
    getMockAxiosInstance().get.mockRejectedValueOnce('plain string error');

    const response = await mockServer.invokeTool('sonar_search_projects', {});
    expect(isValidErrorResponse(response)).toBe(true);
    expect(response.content[0].text).toContain('plain string error');
  });
});

describe('sonar_get_branches', () => {
  let mockServer;

  beforeEach(() => {
    mockServer = createMockServer();
    configureSonarApiTools(mockServer, () => MOCK_SONAR_CONN);
  });

  afterEach(() => {
    vi.clearAllMocks();
  });

  it('returns a valid response with branches', async () => {
    getMockAxiosInstance().get.mockResolvedValueOnce({
      data: {
        branches: [
          { name: 'main', type: 'LONG', isMain: true, status: { qualityGateStatus: 'OK' }, analysisDate: '2026-04-01' }
        ]
      }
    });

    const response = await mockServer.invokeTool('sonar_get_branches', { project: 'my-project' });
    expect(isValidToolResponse(response)).toBe(true);
    expect(response.content[0].text).toContain('my-project');
    expect(response.content[0].text).toContain('main');
  });

  it('uses N/A when analysisDate is absent', async () => {
    getMockAxiosInstance().get.mockResolvedValueOnce({
      data: {
        branches: [{ name: 'orphan', type: 'SHORT', isMain: false, status: {} }]
      }
    });

    const response = await mockServer.invokeTool('sonar_get_branches', { project: 'my-project' });
    expect(isValidToolResponse(response)).toBe(true);
    expect(response.content[0].text).toContain('N/A');
  });

  it('handles missing branches array gracefully', async () => {
    getMockAxiosInstance().get.mockResolvedValueOnce({ data: {} });

    const response = await mockServer.invokeTool('sonar_get_branches', { project: 'my-project' });
    expect(isValidToolResponse(response)).toBe(true);
    expect(response.content[0].text).toContain('0 analysed branch(es)');
  });

  it('returns an error response when axios throws', async () => {
    getMockAxiosInstance().get.mockRejectedValueOnce(new Error('Unauthorized'));

    const response = await mockServer.invokeTool('sonar_get_branches', { project: 'my-project' });
    expect(isValidErrorResponse(response)).toBe(true);
  });

  it('returns string representation when error has no message property', async () => {
    getMockAxiosInstance().get.mockRejectedValueOnce('plain string error');

    const response = await mockServer.invokeTool('sonar_get_branches', { project: 'my-project' });
    expect(isValidErrorResponse(response)).toBe(true);
    expect(response.content[0].text).toContain('plain string error');
  });
});

describe('sonar_get_quality_gate_status', () => {
  let mockServer;

  beforeEach(() => {
    mockServer = createMockServer();
    configureSonarApiTools(mockServer, () => MOCK_SONAR_CONN);
  });

  afterEach(() => {
    vi.clearAllMocks();
  });

  it('returns PASSED status when quality gate is OK', async () => {
    getMockAxiosInstance().get.mockResolvedValueOnce({
      data: {
        projectStatus: {
          status: 'OK',
          conditions: [
            { status: 'OK', metricKey: 'coverage', actualValue: '85', errorThreshold: '80' }
          ]
        }
      }
    });

    const response = await mockServer.invokeTool('sonar_get_quality_gate_status', { projectKey: 'my-project' });
    expect(isValidToolResponse(response)).toBe(true);
    expect(response.content[0].text).toContain('✅ PASSED');
  });

  it('returns FAILED status and lists failing conditions', async () => {
    getMockAxiosInstance().get.mockResolvedValueOnce({
      data: {
        projectStatus: {
          status: 'ERROR',
          conditions: [
            { status: 'ERROR', metricKey: 'coverage', actualValue: '72', errorThreshold: '80' }
          ]
        }
      }
    });

    const response = await mockServer.invokeTool('sonar_get_quality_gate_status', { projectKey: 'my-project' });
    expect(isValidToolResponse(response)).toBe(true);
    expect(response.content[0].text).toContain('❌ FAILED');
    expect(response.content[0].text).toContain('coverage');
  });

  it('includes branch in output when provided', async () => {
    getMockAxiosInstance().get.mockResolvedValueOnce({
      data: { projectStatus: { status: 'OK', conditions: [] } }
    });

    const response = await mockServer.invokeTool('sonar_get_quality_gate_status', {
      projectKey: 'my-project',
      branch: 'develop'
    });
    expect(isValidToolResponse(response)).toBe(true);
    expect(response.content[0].text).toContain('Branch: develop');
  });

  it('includes PR in output when pullRequest param is provided', async () => {
    getMockAxiosInstance().get.mockResolvedValueOnce({
      data: { projectStatus: { status: 'ERROR', conditions: [] } }
    });

    const response = await mockServer.invokeTool('sonar_get_quality_gate_status', {
      projectKey: 'my-project',
      pullRequest: '42'
    });
    expect(isValidToolResponse(response)).toBe(true);
    expect(response.content[0].text).toContain('PR: 42');
  });

  it('handles missing conditions array in projectStatus gracefully', async () => {
    getMockAxiosInstance().get.mockResolvedValueOnce({
      data: { projectStatus: { status: 'OK' } }
    });

    const response = await mockServer.invokeTool('sonar_get_quality_gate_status', { projectKey: 'my-project' });
    expect(isValidToolResponse(response)).toBe(true);
    expect(response.content[0].text).toContain('✅ PASSED');
  });

  it('lists failing conditions with N/A threshold when errorThreshold absent', async () => {
    getMockAxiosInstance().get.mockResolvedValueOnce({
      data: {
        projectStatus: {
          status: 'ERROR',
          conditions: [
            { status: 'ERROR', metricKey: 'new_coverage', actualValue: '50' }
          ]
        }
      }
    });

    const response = await mockServer.invokeTool('sonar_get_quality_gate_status', { projectKey: 'my-project' });
    expect(isValidToolResponse(response)).toBe(true);
    expect(response.content[0].text).toContain('threshold=N/A');
  });

  it('returns an error response when axios throws', async () => {
    getMockAxiosInstance().get.mockRejectedValueOnce(new Error('Not found'));

    const response = await mockServer.invokeTool('sonar_get_quality_gate_status', { projectKey: 'missing' });
    expect(isValidErrorResponse(response)).toBe(true);
  });

  it('returns string representation when error has no message property', async () => {
    getMockAxiosInstance().get.mockRejectedValueOnce('plain string error');

    const response = await mockServer.invokeTool('sonar_get_quality_gate_status', { projectKey: 'my-project' });
    expect(isValidErrorResponse(response)).toBe(true);
    expect(response.content[0].text).toContain('plain string error');
  });
});

describe('sonar_get_issues', () => {
  let mockServer;

  beforeEach(() => {
    mockServer = createMockServer();
    configureSonarApiTools(mockServer, () => MOCK_SONAR_CONN);
  });

  afterEach(() => {
    vi.clearAllMocks();
  });

  it('returns a valid response with issues', async () => {
    getMockAxiosInstance().get.mockResolvedValueOnce({
      data: {
        total: 2,
        issues: [
          { key: 'AX1', type: 'BUG', severity: 'CRITICAL', message: 'NPE', component: 'my-project:Foo.java', line: 42, status: 'OPEN', rule: 'java:S2259', effort: '30min' },
          { key: 'AX2', type: 'VULNERABILITY', severity: 'BLOCKER', message: 'SQL injection', component: 'my-project:Bar.java', line: 10, status: 'OPEN', rule: 'java:S2077', effort: '1h' }
        ]
      }
    });

    const response = await mockServer.invokeTool('sonar_get_issues', { componentKeys: 'my-project' });
    expect(isValidToolResponse(response)).toBe(true);
    expect(response.content[0].text).toContain('2 issue(s)');
    expect(response.content[0].text).toContain('BUG');
  });

  it('includes branch in output when provided', async () => {
    getMockAxiosInstance().get.mockResolvedValueOnce({
      data: { total: 0, issues: [] }
    });

    const response = await mockServer.invokeTool('sonar_get_issues', {
      componentKeys: 'my-project',
      branch: 'feature/x'
    });
    expect(isValidToolResponse(response)).toBe(true);
    expect(response.content[0].text).toContain('branch "feature/x"');
  });

  it('filters by types and severities when provided', async () => {
    getMockAxiosInstance().get.mockResolvedValueOnce({
      data: { total: 0, issues: [] }
    });

    const response = await mockServer.invokeTool('sonar_get_issues', {
      componentKeys: 'my-project',
      types: 'VULNERABILITY',
      severities: 'BLOCKER,CRITICAL'
    });
    expect(isValidToolResponse(response)).toBe(true);
  });

  it('handles missing total and issues array gracefully', async () => {
    getMockAxiosInstance().get.mockResolvedValueOnce({ data: {} });

    const response = await mockServer.invokeTool('sonar_get_issues', { componentKeys: 'my-project' });
    expect(isValidToolResponse(response)).toBe(true);
    expect(response.content[0].text).toContain('0 issue(s)');
  });

  it('returns an error response when axios throws', async () => {
    getMockAxiosInstance().get.mockRejectedValueOnce(new Error('Server error'));

    const response = await mockServer.invokeTool('sonar_get_issues', { componentKeys: 'my-project' });
    expect(isValidErrorResponse(response)).toBe(true);
  });

  it('returns string representation when error has no message property', async () => {
    getMockAxiosInstance().get.mockRejectedValueOnce('plain string error');

    const response = await mockServer.invokeTool('sonar_get_issues', { componentKeys: 'my-project' });
    expect(isValidErrorResponse(response)).toBe(true);
    expect(response.content[0].text).toContain('plain string error');
  });
});

describe('sonar_get_hotspots', () => {
  let mockServer;

  beforeEach(() => {
    mockServer = createMockServer();
    configureSonarApiTools(mockServer, () => MOCK_SONAR_CONN);
  });

  afterEach(() => {
    vi.clearAllMocks();
  });

  it('returns a valid response with hotspots', async () => {
    getMockAxiosInstance().get.mockResolvedValueOnce({
      data: {
        paging: { total: 1 },
        hotspots: [
          { key: 'H1', component: 'my-project:Auth.java', securityCategory: 'auth', vulnerabilityProbability: 'HIGH', status: 'TO_REVIEW', line: 55, message: 'Weak hash', ruleKey: 'java:S2070' }
        ]
      }
    });

    const response = await mockServer.invokeTool('sonar_get_hotspots', { projectKey: 'my-project' });
    expect(isValidToolResponse(response)).toBe(true);
    expect(response.content[0].text).toContain('1 security hotspot(s)');
    expect(response.content[0].text).toContain('TO_REVIEW');
  });

  it('handles missing paging and hotspots arrays gracefully', async () => {
    getMockAxiosInstance().get.mockResolvedValueOnce({ data: {} });

    const response = await mockServer.invokeTool('sonar_get_hotspots', { projectKey: 'my-project' });
    expect(isValidToolResponse(response)).toBe(true);
    expect(response.content[0].text).toContain('0 security hotspot(s)');
  });

  it('includes branch in output when provided', async () => {
    getMockAxiosInstance().get.mockResolvedValueOnce({
      data: { paging: { total: 0 }, hotspots: [] }
    });

    const response = await mockServer.invokeTool('sonar_get_hotspots', {
      projectKey: 'my-project',
      branch: 'develop'
    });
    expect(isValidToolResponse(response)).toBe(true);
    expect(response.content[0].text).toContain('branch "develop"');
  });

  it('filters by REVIEWED status when provided', async () => {
    getMockAxiosInstance().get.mockResolvedValueOnce({
      data: { paging: { total: 0 }, hotspots: [] }
    });

    const response = await mockServer.invokeTool('sonar_get_hotspots', {
      projectKey: 'my-project',
      status: 'REVIEWED'
    });
    expect(isValidToolResponse(response)).toBe(true);
    expect(response.content[0].text).toContain('"REVIEWED"');
  });

  it('returns an error response when axios throws', async () => {
    getMockAxiosInstance().get.mockRejectedValueOnce(new Error('Timeout'));

    const response = await mockServer.invokeTool('sonar_get_hotspots', { projectKey: 'my-project' });
    expect(isValidErrorResponse(response)).toBe(true);
  });

  it('returns string representation when error has no message property', async () => {
    getMockAxiosInstance().get.mockRejectedValueOnce('plain string error');

    const response = await mockServer.invokeTool('sonar_get_hotspots', { projectKey: 'my-project' });
    expect(isValidErrorResponse(response)).toBe(true);
    expect(response.content[0].text).toContain('plain string error');
  });
});

describe('sonar_get_measures', () => {
  let mockServer;

  beforeEach(() => {
    mockServer = createMockServer();
    configureSonarApiTools(mockServer, () => MOCK_SONAR_CONN);
  });

  afterEach(() => {
    vi.clearAllMocks();
  });

  it('returns a valid response with measures as key-value pairs', async () => {
    getMockAxiosInstance().get.mockResolvedValueOnce({
      data: {
        component: {
          key: 'my-project',
          measures: [
            { metric: 'coverage', value: '85.3' },
            { metric: 'bugs', value: '2' },
            { metric: 'vulnerabilities', value: '0' }
          ]
        }
      }
    });

    const response = await mockServer.invokeTool('sonar_get_measures', { component: 'my-project' });
    expect(isValidToolResponse(response)).toBe(true);
    expect(response.content[0].text).toContain('coverage');
    expect(response.content[0].text).toContain('85.3');
  });

  it('includes branch in output when provided', async () => {
    getMockAxiosInstance().get.mockResolvedValueOnce({
      data: { component: { key: 'my-project', measures: [] } }
    });

    const response = await mockServer.invokeTool('sonar_get_measures', {
      component: 'my-project',
      branch: 'main'
    });
    expect(isValidToolResponse(response)).toBe(true);
    expect(response.content[0].text).toContain('branch "main"');
  });

  it('accepts custom metricKeys', async () => {
    getMockAxiosInstance().get.mockResolvedValueOnce({
      data: { component: { measures: [{ metric: 'ncloc', value: '5000' }] } }
    });

    const response = await mockServer.invokeTool('sonar_get_measures', {
      component: 'my-project',
      metricKeys: 'ncloc'
    });
    expect(isValidToolResponse(response)).toBe(true);
    expect(response.content[0].text).toContain('ncloc');
  });

  it('falls back to periods value when measure has no direct value', async () => {
    getMockAxiosInstance().get.mockResolvedValueOnce({
      data: {
        component: {
          measures: [
            { metric: 'new_coverage', periods: [{ value: '78.5' }] }
          ]
        }
      }
    });

    const response = await mockServer.invokeTool('sonar_get_measures', { component: 'my-project' });
    expect(isValidToolResponse(response)).toBe(true);
    expect(response.content[0].text).toContain('78.5');
  });

  it('sets null for measures with no value or periods', async () => {
    getMockAxiosInstance().get.mockResolvedValueOnce({
      data: {
        component: {
          measures: [{ metric: 'some_metric' }]
        }
      }
    });

    const response = await mockServer.invokeTool('sonar_get_measures', { component: 'my-project' });
    expect(isValidToolResponse(response)).toBe(true);
    expect(response.content[0].text).toContain('null');
  });

  it('handles empty periods array gracefully', async () => {
    getMockAxiosInstance().get.mockResolvedValueOnce({
      data: {
        component: {
          measures: [{ metric: 'new_coverage', periods: [] }]
        }
      }
    });

    const response = await mockServer.invokeTool('sonar_get_measures', { component: 'my-project' });
    expect(isValidToolResponse(response)).toBe(true);
    expect(response.content[0].text).toContain('new_coverage');
  });

  it('handles missing component in response gracefully', async () => {
    getMockAxiosInstance().get.mockResolvedValueOnce({ data: {} });

    const response = await mockServer.invokeTool('sonar_get_measures', { component: 'my-project' });
    expect(isValidToolResponse(response)).toBe(true);
  });

  it('returns an error response when axios throws', async () => {
    getMockAxiosInstance().get.mockRejectedValueOnce(new Error('Forbidden'));

    const response = await mockServer.invokeTool('sonar_get_measures', { component: 'my-project' });
    expect(isValidErrorResponse(response)).toBe(true);
  });

  it('returns string representation when error has no message property', async () => {
    getMockAxiosInstance().get.mockRejectedValueOnce('plain string error');

    const response = await mockServer.invokeTool('sonar_get_measures', { component: 'my-project' });
    expect(isValidErrorResponse(response)).toBe(true);
    expect(response.content[0].text).toContain('plain string error');
  });
});
