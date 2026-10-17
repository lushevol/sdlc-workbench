import { z } from 'zod';

const SONAR_PROMPTS = {
  SONAR_PROJECT_HEALTH: {
    name: 'sonar-project-health',
    description: 'Get a full code quality health report for a SonarQube project: quality gate, key metrics, and open issues',
    arguments: [
      { name: 'projectKey', description: 'SonarQube project key', required: true },
      { name: 'branch', description: 'Branch name (optional, defaults to main branch)', required: false }
    ]
  },

  SONAR_SECURITY_REVIEW: {
    name: 'sonar-security-review',
    description: 'Get a security-focused review of a SonarQube project: vulnerabilities, security hotspots, and security rating',
    arguments: [
      { name: 'projectKey', description: 'SonarQube project key', required: true },
      { name: 'branch', description: 'Branch name (optional, defaults to main branch)', required: false }
    ]
  },

  SONAR_SEARCH_PROJECTS: {
    name: 'sonar-search-projects',
    description: 'Search or list SonarQube projects by name or key',
    arguments: [
      { name: 'query', description: 'Filter text — project name or key substring (optional)', required: false }
    ]
  },

  SONAR_GET_BRANCHES: {
    name: 'sonar-get-branches',
    description: 'List all analysed branches for a SonarQube project',
    arguments: [
      { name: 'projectKey', description: 'SonarQube project key', required: true }
    ]
  },

  SONAR_GET_QUALITY_GATE: {
    name: 'sonar-get-quality-gate',
    description: 'Check the quality gate pass/fail status for a SonarQube project branch or pull request',
    arguments: [
      { name: 'projectKey', description: 'SonarQube project key', required: true },
      { name: 'branch', description: 'Branch name (optional, defaults to main branch)', required: false },
      { name: 'pullRequest', description: 'Pull request ID (optional, mutually exclusive with branch)', required: false }
    ]
  },

  SONAR_GET_ISSUES: {
    name: 'sonar-get-issues',
    description: 'Search for bugs, vulnerabilities, and code smells in a SonarQube project',
    arguments: [
      { name: 'projectKey', description: 'SonarQube project key', required: true },
      { name: 'types', description: 'Comma-separated types: BUG, VULNERABILITY, CODE_SMELL (optional)', required: false },
      { name: 'severities', description: 'Comma-separated severities: BLOCKER, CRITICAL, MAJOR, MINOR, INFO (optional)', required: false },
      { name: 'branch', description: 'Branch name (optional)', required: false }
    ]
  },

  SONAR_GET_HOTSPOTS: {
    name: 'sonar-get-hotspots',
    description: 'List security hotspots in a SonarQube project that require manual review',
    arguments: [
      { name: 'projectKey', description: 'SonarQube project key', required: true },
      { name: 'branch', description: 'Branch name (optional, defaults to main branch)', required: false },
      { name: 'status', description: 'Review status: TO_REVIEW or REVIEWED (optional, defaults to TO_REVIEW)', required: false }
    ]
  },

  SONAR_GET_MEASURES: {
    name: 'sonar-get-measures',
    description: 'Retrieve code quality metrics (coverage, bugs, vulnerabilities, code smells, tech debt) for a SonarQube project',
    arguments: [
      { name: 'component', description: 'SonarQube project key (component key)', required: true },
      { name: 'metricKeys', description: 'Comma-separated metric keys (optional, defaults to standard set)', required: false },
      { name: 'branch', description: 'Branch name (optional)', required: false }
    ]
  }
};

const generateSonarPromptMessage = (name, args, ctx) => {
  switch (name) {
    case 'sonar-project-health':   return sonarProjectHealth(args, ctx);
    case 'sonar-security-review':  return sonarSecurityReview(args, ctx);
    case 'sonar-search-projects':  return sonarSearchProjects(args);
    case 'sonar-get-branches':     return sonarGetBranches(args);
    case 'sonar-get-quality-gate': return sonarGetQualityGate(args, ctx);
    case 'sonar-get-issues':       return sonarGetIssues(args, ctx);
    case 'sonar-get-hotspots':     return sonarGetHotspots(args, ctx);
    case 'sonar-get-measures':     return sonarGetMeasures(args, ctx);
    default:                       return 'Unknown prompt';
  }
};

function sonarBranchClause(args, ctx) {
  const sqBranch = args.branch || ctx?.ado?.defaultBranch;
  return sqBranch ? ` on branch "${sqBranch}"` : '';
}

function sonarBranchArg(args, ctx) {
  const sqBranch = args.branch || ctx?.ado?.defaultBranch;
  return sqBranch ? ` and branch="${sqBranch}"` : '';
}

function sonarProjectHealth(args, ctx) {
  const sqProject = args.projectKey;
  const branchClause = sonarBranchClause(args, ctx);
  const branchArg = sonarBranchArg(args, ctx);
  return `Get a complete code quality health report for SonarQube project "${sqProject}"${branchClause}.

Steps:
1. Call sonar_get_quality_gate_status with projectKey="${sqProject}"${branchArg} to check overall pass/fail status.
2. Call sonar_get_measures with component="${sqProject}"${branchArg} to retrieve key metrics (coverage, duplication, bugs, code smells, tech debt).
3. Call sonar_get_issues with componentKeys="${sqProject}"${branchArg}, types="BUG,VULNERABILITY", severities="BLOCKER,CRITICAL" to list the highest-priority issues.

Present the results as a health dashboard with:
- Quality Gate: PASSED / FAILED
- Coverage %, Duplication %, Lines of Code
- Bug count, Vulnerability count, Code Smell count, Technical Debt
- Top BLOCKER/CRITICAL issues (up to 10)`;
}

function sonarSecurityReview(args, ctx) {
  const sqProject = args.projectKey;
  const branchClause = sonarBranchClause(args, ctx);
  const branchArg = sonarBranchArg(args, ctx);
  return `Perform a security-focused review of SonarQube project "${sqProject}"${branchClause}.

Steps:
1. Call sonar_get_measures with component="${sqProject}"${branchArg} and metricKeys="vulnerabilities,security_rating,security_hotspots,security_review_rating" to get the security rating.
2. Call sonar_get_issues with componentKeys="${sqProject}"${branchArg}, types="VULNERABILITY" to list all open vulnerabilities.
3. Call sonar_get_hotspots with projectKey="${sqProject}"${branchArg}, status="TO_REVIEW" to list unreviewed security hotspots.

Present the results as a security review with:
- Security Rating (A–E) and Hotspot review coverage
- All open vulnerabilities grouped by severity (BLOCKER > CRITICAL > MAJOR)
- Security hotspots requiring manual review, grouped by category
- Recommended remediation priorities`;
}

function sonarSearchProjects(args) {
  const sqQuery = args.query;
  const matchClause = sqQuery ? ` matching "${sqQuery}"` : '';
  const callClause = sqQuery ? ` with query="${sqQuery}"` : ' (no filter — list all projects)';
  return `Search SonarQube for projects${matchClause}.

Call sonar_search_projects${callClause}.

Present the results as a table with columns: Project Name, Project Key, Last Analysis Date, Quality Gate Status.`;
}

function sonarGetBranches(args) {
  const sqProject = args.projectKey;
  return `List all analysed branches for SonarQube project "${sqProject}".

Call sonar_get_branches with projectKey="${sqProject}".

Present the results as a table with columns: Branch Name, Type (LONG/SHORT/PULL_REQUEST), Main Branch, Quality Gate Status, Last Analysis Date.`;
}

function sonarGetQualityGate(args, ctx) {
  const sqProject = args.projectKey;
  const sqBranch = args.branch || ctx?.ado?.defaultBranch;
  const sqPR = args.pullRequest;
  let subjectClause;
  let callArg;
  if (sqPR) {
    subjectClause = ` pull request "${sqPR}"`;
    callArg = ` and pullRequest="${sqPR}"`;
  } else if (sqBranch) {
    subjectClause = ` on branch "${sqBranch}"`;
    callArg = ` and branch="${sqBranch}"`;
  } else {
    subjectClause = '';
    callArg = '';
  }
  return `Check the quality gate status for SonarQube project "${sqProject}"${subjectClause}.

Call sonar_get_quality_gate_status with projectKey="${sqProject}"${callArg}.

Present the result as:
- Overall Status: PASSED ✅ / FAILED ❌
- Individual condition results (metric name, operator, threshold, actual value, status)`;
}

function sonarGetIssues(args, ctx) {
  const sqProject = args.projectKey;
  const sqBranch = args.branch || ctx?.ado?.defaultBranch;
  const sqTypes = args.types || 'BUG,VULNERABILITY,CODE_SMELL';
  const sqSeverities = args.severities;
  const branchClause = sqBranch ? ` on branch "${sqBranch}"` : '';
  const branchArg = sqBranch ? `, branch="${sqBranch}"` : '';
  const severitiesArg = sqSeverities ? `, severities="${sqSeverities}"` : '';
  return `Search for issues in SonarQube project "${sqProject}"${branchClause}.

Call sonar_get_issues with componentKeys="${sqProject}"${branchArg}, types="${sqTypes}"${severitiesArg}.

Present the results grouped by type and severity, showing: Issue message, file path, line number, severity, and effort to fix.`;
}

function sonarGetHotspots(args, ctx) {
  const sqProject = args.projectKey;
  const sqBranch = args.branch || ctx?.ado?.defaultBranch;
  const sqStatus = args.status || 'TO_REVIEW';
  const branchClause = sqBranch ? ` on branch "${sqBranch}"` : '';
  const branchArg = sqBranch ? `, branch="${sqBranch}"` : '';
  return `List security hotspots for SonarQube project "${sqProject}"${branchClause} with status "${sqStatus}".

Call sonar_get_hotspots with projectKey="${sqProject}"${branchArg}, status="${sqStatus}".

Present the results grouped by security category, showing: vulnerability probability (HIGH/MEDIUM/LOW), file path, line number, and description for each hotspot.`;
}

function sonarGetMeasures(args, ctx) {
  const sqComponent = args.component;
  const sqBranch = args.branch || ctx?.ado?.defaultBranch;
  const sqMetrics = args.metricKeys || 'bugs,vulnerabilities,code_smells,coverage,duplicated_lines_density,ncloc,sqale_index,reliability_rating,security_rating,sqale_rating';
  const branchClause = sqBranch ? ` on branch "${sqBranch}"` : '';
  const branchArg = sqBranch ? `, branch="${sqBranch}"` : '';
  return `Retrieve code quality metrics for SonarQube project "${sqComponent}"${branchClause}.

Call sonar_get_measures with component="${sqComponent}"${branchArg}, metricKeys="${sqMetrics}".

Present the results as a metrics dashboard:
- Coverage: X%
- Duplicated code: X%
- Lines of code: X
- Bugs: X | Vulnerabilities: X | Code Smells: X
- Technical debt: X (sqale_index in minutes)
- Reliability Rating: A–E | Security Rating: A–E | Maintainability Rating: A–E`;
}

const CONTEXTUAL_OPTIONAL_FIELDS = new Set(['project', 'team', 'repository', 'repositoryId', 'applicationId']);

export function configureSonarPrompts(server, { getContext = () => null } = {}) {
  Object.values(SONAR_PROMPTS).forEach(prompt => {
    const callback = async (args) => {
      const ctx = getContext();
      const message = generateSonarPromptMessage(prompt.name, args ?? {}, ctx);
      return { messages: [{ role: 'user', content: { type: 'text', text: message } }] };
    };
    if (prompt.arguments.length === 0) {
      server.prompt(prompt.name, prompt.description, callback);
    } else {
      const argsSchema = Object.fromEntries(
        prompt.arguments.map(arg => [
          arg.name,
          (!arg.required || CONTEXTUAL_OPTIONAL_FIELDS.has(arg.name))
            ? z.string().optional().describe(arg.description)
            : z.string().describe(arg.description)
        ])
      );
      server.prompt(prompt.name, prompt.description, argsSchema, callback);
    }
  });
  console.error(`Registered ${Object.keys(SONAR_PROMPTS).length} Sonar prompts`);
}

export { SONAR_PROMPTS };
