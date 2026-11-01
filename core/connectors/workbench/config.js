import { readFileSync } from 'node:fs';
import { isAbsolute, join, resolve } from 'node:path';
import { parse } from 'dotenv';

export function loadConfig(workspaceRoot) {
  if (typeof workspaceRoot !== 'string' || !isAbsolute(workspaceRoot)) {
    throw new Error('An absolute workspace path is required.');
  }

  let fileEnvironment = {};
  try {
    fileEnvironment = parse(readFileSync(join(workspaceRoot, '.env')));
  } catch (error) {
    if (error.code !== 'ENOENT') throw new Error('The workspace environment file cannot be read.');
  }
  const env = { ...fileEnvironment, ...process.env };
  if (env.NODE_EXTRA_CA_CERTS) {
    env.NODE_EXTRA_CA_CERTS = resolve(workspaceRoot, env.NODE_EXTRA_CA_CERTS);
  }
  const value = name => env[name] || '';
  const codeReviewGuideFile = value('CODE_REVIEW_GUIDE_FILE');
  return {
    workspaceRoot: resolve(workspaceRoot),
    env,
    AZURE_DEVOPS_ORG_URL: value('AZURE_DEVOPS_ORG_URL'),
    AZURE_DEVOPS_PAT: value('AZURE_DEVOPS_PAT'),
    HTTPS_PROXY: value('HTTPS_PROXY') || value('https_proxy') || value('HTTP_PROXY') || value('http_proxy'),
    codeReviewGuideFile: codeReviewGuideFile ? resolve(workspaceRoot, codeReviewGuideFile) : '',
    confluenceConfig: {
      baseUrl: value('CONFLUENCE_BASE_URL'),
      token: value('CONFLUENCE_PAT'),
    },
    scwikiConfig: {
      baseUrl: value('SCWIKI_URL'),
      token: value('SCWIKI_TOKEN'),
      wiki: value('SCWIKI_WIKI') || 'xwiki',
    },
    nexusConfig: {
      baseUrl: value('NEXUS_BASE_URL'),
      userCode: value('NEXUS_USER_CODE'),
      passCode: value('NEXUS_PASS_CODE'),
    },
    sonarConfig: {
      baseUrl: value('SONAR_BASE_URL'),
      token: value('SONAR_TOKEN'),
    },
    kibanaConfig: {
      baseUrl: value('KIBANA_BASE_URL'),
      apiKey: value('KIBANA_API_KEY'),
      username: value('KIBANA_USERNAME'),
      password: value('KIBANA_PASSWORD'),
      indices: value('KIBANA_ALLOWED_INDICES').split(',').map(item => item.trim()).filter(Boolean),
      maxRangeHours: Number(value('KIBANA_MAX_RANGE_HOURS') || '24'),
    },
    postgresqlConfig: {
      host: value('WORKBENCH_PG_HOST'),
      port: value('WORKBENCH_PG_PORT') || '5432',
      database: value('WORKBENCH_PG_DATABASE'),
      user: value('WORKBENCH_PG_USER'),
      password: value('WORKBENCH_PG_PASSWORD'),
      sslMode: value('WORKBENCH_PG_SSL_MODE') || 'verify-full',
      caFile: value('WORKBENCH_PG_CA_FILE') ? resolve(workspaceRoot, value('WORKBENCH_PG_CA_FILE')) : '',
      statementTimeoutMs: value('WORKBENCH_PG_STATEMENT_TIMEOUT_MS') || '15000',
      maxRows: value('WORKBENCH_PG_MAX_ROWS') || '1000',
    },
  };
}
