import { z } from 'zod';
import axios from 'axios';

const DEFAULT_METRIC_KEYS = [
  'bugs',
  'vulnerabilities',
  'code_smells',
  'coverage',
  'duplicated_lines_density',
  'ncloc',
  'sqale_index',
  'reliability_rating',
  'security_rating',
  'sqale_rating'
].join(',');

/**
 * Build an axios instance pre-configured with SonarQube auth headers.
 * @param {Object} connection - { baseUrl, headers }
 * @returns {import('axios').AxiosInstance}
 */
function buildClient(connection) {
  return axios.create({
    baseURL: connection.baseUrl,
    headers: connection.headers
  });
}

/**
 * Register all SonarQube tools on the MCP server.
 * @param {import('@modelcontextprotocol/sdk/server/mcp.js').McpServer} server
 * @param {() => Object} sonarConnectionProvider
 */
export function configureSonarApiTools(server, sonarConnectionProvider) {

  // ── sonar_search_projects ─────────────────────────────────────────────────
  server.tool(
    'sonar_search_projects',
    'Search or list SonarQube projects by name. Returns project keys, names, and last analysis dates.',
    {
      query: z.string().optional().describe('Filter projects whose name or key contains this text'),
      pageSize: z.number().optional().default(50).describe('Maximum number of projects to return (default 50)')
    },
    async ({ query, pageSize = 50 }) => {
      try {
        const connection = sonarConnectionProvider();
        const client = buildClient(connection);
        const params = { ps: pageSize };
        if (query) params.q = query;

        const { data } = await client.get('/api/projects/search', { params });
        const projects = (data.components || []).map(p => ({
          key: p.key,
          name: p.name,
          qualifier: p.qualifier,
          lastAnalysisDate: p.lastAnalysisDate || 'N/A'
        }));

        const summary = `Found ${projects.length} project(s)${query ? ` matching "${query}"` : ''}.\n\n`;
        return {
          content: [{ type: 'text', text: summary + JSON.stringify(projects, null, 2) }]
        };
      } catch (error) {
        return {
          content: [{ type: 'text', text: error?.message || String(error) }],
          isError: true
        };
      }
    }
  );

  // ── sonar_get_branches ────────────────────────────────────────────────────
  server.tool(
    'sonar_get_branches',
    'List all analysed branches for a SonarQube project. Returns branch names, types, status, and last analysis dates.',
    {
      project: z.string().describe('SonarQube project key')
    },
    async ({ project }) => {
      try {
        const connection = sonarConnectionProvider();
        const client = buildClient(connection);

        const { data } = await client.get('/api/project_branches/list', {
          params: { project }
        });

        const branches = (data.branches || []).map(b => ({
          name: b.name,
          type: b.type,
          isMain: b.isMain,
          status: b.status,
          analysisDate: b.analysisDate || 'N/A'
        }));

        const summary = `Project "${project}" has ${branches.length} analysed branch(es).\n\n`;
        return {
          content: [{ type: 'text', text: summary + JSON.stringify(branches, null, 2) }]
        };
      } catch (error) {
        return {
          content: [{ type: 'text', text: error?.message || String(error) }],
          isError: true
        };
      }
    }
  );

  // ── sonar_get_quality_gate_status ─────────────────────────────────────────
  server.tool(
    'sonar_get_quality_gate_status',
    'Get the quality gate pass/fail status for a project branch or pull request. Shows overall status and any failing conditions.',
    {
      projectKey: z.string().describe('SonarQube project key'),
      branch: z.string().optional().describe('Branch name (omit to use the main branch)'),
      pullRequest: z.string().optional().describe('Pull request ID (mutually exclusive with branch)')
    },
    async ({ projectKey, branch, pullRequest }) => {
      try {
        const connection = sonarConnectionProvider();
        const client = buildClient(connection);
        const params = { projectKey };
        if (pullRequest) {
          params.pullRequest = pullRequest;
        } else if (branch) {
          params.branch = branch;
        }

        const { data } = await client.get('/api/qualitygates/project_status', { params });
        const qg = data.projectStatus;

        const status = qg.status; // OK | ERROR | NONE | WARN
        const failingConditions = (qg.conditions || []).filter(c => c.status === 'ERROR');

        let text = `Quality Gate: ${status === 'OK' ? '✅ PASSED' : '❌ FAILED'}\n`;
        text += `Project: ${projectKey}`;
        if (branch) text += ` | Branch: ${branch}`;
        if (pullRequest) text += ` | PR: ${pullRequest}`;
        text += '\n';

        if (failingConditions.length > 0) {
          text += `\nFailing conditions (${failingConditions.length}):\n`;
          failingConditions.forEach(c => {
            text += `  • ${c.metricKey}: actual=${c.actualValue}, threshold=${c.errorThreshold || 'N/A'}\n`;
          });
        }

        text += '\n' + JSON.stringify(qg, null, 2);
        return { content: [{ type: 'text', text }] };
      } catch (error) {
        return {
          content: [{ type: 'text', text: error?.message || String(error) }],
          isError: true
        };
      }
    }
  );

  // ── sonar_get_issues ──────────────────────────────────────────────────────
  server.tool(
    'sonar_get_issues',
    'Search for issues (bugs, vulnerabilities, code smells) in a SonarQube project. Supports filtering by type, severity, and branch.',
    {
      componentKeys: z.string().describe('Comma-separated project keys to search issues in'),
      types: z.string().optional().describe('Comma-separated issue types: BUG, VULNERABILITY, CODE_SMELL (default: all)'),
      severities: z.string().optional().describe('Comma-separated severities: BLOCKER, CRITICAL, MAJOR, MINOR, INFO (default: all)'),
      branch: z.string().optional().describe('Branch name to filter by'),
      statuses: z.string().optional().describe('Comma-separated statuses: OPEN, CONFIRMED, REOPENED, RESOLVED, CLOSED (default: OPEN)'),
      pageSize: z.number().optional().default(50).describe('Maximum issues to return (default 50)')
    },
    async ({ componentKeys, types, severities, branch, statuses = 'OPEN', pageSize = 50 }) => {
      try {
        const connection = sonarConnectionProvider();
        const client = buildClient(connection);
        const params = {
          componentKeys,
          statuses,
          ps: pageSize
        };
        if (types) params.types = types;
        if (severities) params.severities = severities;
        if (branch) params.branch = branch;

        const { data } = await client.get('/api/issues/search', { params });
        const total = data.total || 0;
        const issues = (data.issues || []).map(i => ({
          key: i.key,
          type: i.type,
          severity: i.severity,
          message: i.message,
          component: i.component,
          line: i.line,
          status: i.status,
          rule: i.rule,
          effort: i.effort
        }));

        let text = `Found ${total} issue(s) in "${componentKeys}"`;
        if (branch) text += ` on branch "${branch}"`;
        text += ` (showing ${issues.length}).\n\n`;
        text += JSON.stringify(issues, null, 2);
        return { content: [{ type: 'text', text }] };
      } catch (error) {
        return {
          content: [{ type: 'text', text: error?.message || String(error) }],
          isError: true
        };
      }
    }
  );

  // ── sonar_get_hotspots ────────────────────────────────────────────────────
  server.tool(
    'sonar_get_hotspots',
    'Search for security hotspots in a SonarQube project that require manual review. Returns hotspot details and review status.',
    {
      projectKey: z.string().describe('SonarQube project key'),
      branch: z.string().optional().describe('Branch name (omit for main branch)'),
      status: z.enum(['TO_REVIEW', 'REVIEWED']).optional().describe('Filter by review status (default: TO_REVIEW)'),
      pageSize: z.number().optional().default(50).describe('Maximum hotspots to return (default 50)')
    },
    async ({ projectKey, branch, status = 'TO_REVIEW', pageSize = 50 }) => {
      try {
        const connection = sonarConnectionProvider();
        const client = buildClient(connection);
        const params = { projectKey, status, ps: pageSize };
        if (branch) params.branch = branch;

        const { data } = await client.get('/api/hotspots/search', { params });
        const total = data.paging?.total || 0;
        const hotspots = (data.hotspots || []).map(h => ({
          key: h.key,
          component: h.component,
          securityCategory: h.securityCategory,
          vulnerabilityProbability: h.vulnerabilityProbability,
          status: h.status,
          line: h.line,
          message: h.message,
          rule: h.ruleKey
        }));

        let text = `Found ${total} security hotspot(s) in "${projectKey}"`;
        if (branch) text += ` on branch "${branch}"`;
        text += ` with status "${status}" (showing ${hotspots.length}).\n\n`;
        text += JSON.stringify(hotspots, null, 2);
        return { content: [{ type: 'text', text }] };
      } catch (error) {
        return {
          content: [{ type: 'text', text: error?.message || String(error) }],
          isError: true
        };
      }
    }
  );

  // ── sonar_get_measures ────────────────────────────────────────────────────
  server.tool(
    'sonar_get_measures',
    'Get code quality metrics for a SonarQube project. Returns coverage, duplication, bugs, vulnerabilities, technical debt, and more.',
    {
      component: z.string().describe('SonarQube project key'),
      branch: z.string().optional().describe('Branch name (omit for main branch)'),
      metricKeys: z.string().optional().describe(
        `Comma-separated metric keys to retrieve. Defaults to: ${DEFAULT_METRIC_KEYS}`
      )
    },
    async ({ component, branch, metricKeys }) => {
      try {
        const connection = sonarConnectionProvider();
        const client = buildClient(connection);
        const params = {
          component,
          metricKeys: metricKeys || DEFAULT_METRIC_KEYS
        };
        if (branch) params.branch = branch;

        const { data } = await client.get('/api/measures/component', { params });
        const comp = data.component;
        const measures = (comp?.measures || []).reduce((acc, m) => {
          acc[m.metric] = m.value ?? m.periods?.[0]?.value ?? null;
          return acc;
        }, {});

        let text = `Measures for "${component}"`;
        if (branch) text += ` on branch "${branch}"`;
        text += ':\n\n';
        text += JSON.stringify(measures, null, 2);
        return { content: [{ type: 'text', text }] };
      } catch (error) {
        return {
          content: [{ type: 'text', text: error?.message || String(error) }],
          isError: true
        };
      }
    }
  );
}
