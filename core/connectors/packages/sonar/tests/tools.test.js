import { describe, it, expect } from 'vitest';
import { configureSonarTools } from '../src/tools.js';
import { createMockServer } from '@sc-node-mcp/shared-tests/helpers/mockServer';

const MOCK_SONAR_CONN = {
  baseUrl: 'https://sonarqube.vx.standardchartered.com',
  headers: {
    Authorization: 'Bearer test-token',
    Accept: 'application/json',
    'Content-Type': 'application/json'
  }
};

describe('configureSonarTools', () => {
  it('registers all 6 sonar tools on the server', () => {
    const mockServer = createMockServer();
    configureSonarTools(mockServer, () => MOCK_SONAR_CONN);
    const names = mockServer.getRegisteredTools().map(t => t.name);

    expect(names).toContain('sonar_search_projects');
    expect(names).toContain('sonar_get_branches');
    expect(names).toContain('sonar_get_quality_gate_status');
    expect(names).toContain('sonar_get_issues');
    expect(names).toContain('sonar_get_hotspots');
    expect(names).toContain('sonar_get_measures');
  });

  it('registers exactly 6 tools', () => {
    const mockServer = createMockServer();
    configureSonarTools(mockServer, () => MOCK_SONAR_CONN);
    const sonarTools = mockServer.getRegisteredTools().filter(t => t.name.startsWith('sonar_'));
    expect(sonarTools).toHaveLength(6);
  });
});
