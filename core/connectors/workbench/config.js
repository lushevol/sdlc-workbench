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
  };
}
