import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

/** Cached configuration — populated on first call to getConfig() */
let _cachedConfig = null;

/** Supply configuration from the Workbench root before registering connector tools. */
export function setConfig(config) {
  _cachedConfig = config;
}

/**
 * Reset the cached configuration. Intended for use in tests only.
 */
export function resetConfigCache() {
  _cachedConfig = null;
}

/**
 * Load configuration from command-line arguments, environment variables, or config.json.
 * Result is memoized for the lifetime of the process — config sources are read once.
 * Priority: 1) Command-line args, 2) Environment variables, 3) config.json
 * @returns {Object} Configuration object with ADO and Confluence settings
 */
export function getConfig() {
  if (_cachedConfig) return _cachedConfig;

  const args = process.argv.slice(2);
  
  // Try command-line arguments first (highest priority)
  if (args.length > 0) {
    _cachedConfig = getConfigFromArgs(args);
    return _cachedConfig;
  }
  
  // Try environment variables (fallback)
  if (process.env.AZURE_DEVOPS_PAT) {
    _cachedConfig = getConfigFromEnv();
    return _cachedConfig;
  }
  
  // Try config.json (backwards compatibility for local development)
  try {
    _cachedConfig = getConfigFromFile();
    return _cachedConfig;
  } catch (err) {
    throw new Error(
      'Configuration not found. Provide via:\n' +
      '  1. Command-line args: node index.js <PAT> [PROXY] [CONF_PAT]\n' +
      '  2. Environment variables: AZURE_DEVOPS_PAT, etc.\n' +
      '  3. config.json file (local development only)\n' +
      `Error: ${err.message}`
    );
  }
}

/**
 * Load configuration from command-line arguments
 * @param {string[]} args - Process arguments
 * @returns {Object} Configuration object
 */
function getConfigFromArgs(args) {
  const AZURE_DEVOPS_ORG_URL = 'https://dev.azure.com/sc-ado';
  const AZURE_DEVOPS_PAT = args[0];
  const HTTPS_PROXY = args[1] || '';
  const CONFLUENCE_BASE_URL = 'https://confluence.global.standardchartered.com';
  const CONFLUENCE_PAT = args[2] || '';
  const NEXUS_USER_CODE = args[3] || '';
  const NEXUS_PASS_CODE = args[4] || '';
  const SONAR_TOKEN = args[5] || '';
  const SCWIKI_TOKEN = args[6] || '';
  const codeReviewGuideFile = process.env.CODE_REVIEW_GUIDE_FILE || '';

  if (!AZURE_DEVOPS_PAT) {
    throw new Error(
      'Azure DevOps configuration missing.\n' +
      'Usage: node index.js <PAT> [PROXY] [CONF_PAT] [NEXUS_USER_CODE] [NEXUS_PASS_CODE] [SONAR_TOKEN] [SCWIKI_TOKEN]\n' +
      'Example: node index.js "pat-token" "http://proxy:443" "confluence-pat-token" "nexus-user" "nexus-pass" "sonar-token" "scwiki-token"'
    );
  }

  const config = buildConfig({
    AZURE_DEVOPS_ORG_URL,
    AZURE_DEVOPS_PAT,
    HTTPS_PROXY,
    CONFLUENCE_BASE_URL,
    CONFLUENCE_PAT,
    NEXUS_USER_CODE,
    NEXUS_PASS_CODE,
    codeReviewGuideFile,
    SONAR_TOKEN,
    SCWIKI_TOKEN
  });

  logConfig(config, 'command-line arguments');
  return config;
}

/**
 * Load configuration from environment variables
 * @returns {Object} Configuration object
 */
function getConfigFromEnv() {
  const AZURE_DEVOPS_ORG_URL = 'https://dev.azure.com/sc-ado';
  const AZURE_DEVOPS_PAT = process.env.AZURE_DEVOPS_PAT;
  const HTTPS_PROXY = process.env.HTTPS_PROXY || '';
  const CONFLUENCE_BASE_URL = 'https://confluence.global.standardchartered.com';
  const CONFLUENCE_PAT = process.env.CONFLUENCE_PAT || '';
  const NEXUS_USER_CODE = process.env.NEXUS_USER_CODE || '';
  const NEXUS_PASS_CODE = process.env.NEXUS_PASS_CODE || '';
  const SONAR_TOKEN = process.env.SONAR_TOKEN || '';
  const SCWIKI_TOKEN = process.env.SCWIKI_TOKEN || '';
  const codeReviewGuideFile = process.env.CODE_REVIEW_GUIDE_FILE || '';

  // Unreachable via getConfig(): the caller only invokes this function when
  // process.env.AZURE_DEVOPS_PAT is already truthy (checked synchronously,
  // same value). Kept as a defensive guard for direct/future callers.
  /* v8 ignore next 3 */
  if (!AZURE_DEVOPS_PAT) {
    throw new Error('AZURE_DEVOPS_PAT environment variable must be set');
  }

  const config = buildConfig({
    AZURE_DEVOPS_ORG_URL,
    AZURE_DEVOPS_PAT,
    HTTPS_PROXY,
    CONFLUENCE_BASE_URL,
    CONFLUENCE_PAT,
    NEXUS_USER_CODE,
    NEXUS_PASS_CODE,
    codeReviewGuideFile,
    SONAR_TOKEN,
    SCWIKI_TOKEN
  });

  logConfig(config, 'environment variables');
  return config;
}

/**
 * Load configuration from config.json file
 * @returns {Object} Configuration object
 */
function getConfigFromFile() {
  const __filename = fileURLToPath(import.meta.url);
  const __dirname = path.dirname(__filename);
  const configPath = path.resolve(__dirname, '../../../config.json');
  
  let config;
  try {
    config = JSON.parse(fs.readFileSync(configPath, 'utf-8'));
  } catch (err) {
    throw new Error(`Failed to load config.json: ${err.message}`);
  }

  const AZURE_DEVOPS_ORG_URL = 'https://dev.azure.com/sc-ado';
  const CONFLUENCE_BASE_URL = 'https://confluence.global.standardchartered.com';
  const { 
    AZURE_DEVOPS_PAT, 
    CONFLUENCE_PAT = '', 
    HTTPS_PROXY = '',
    NEXUS_USER_CODE = '',
    NEXUS_PASS_CODE = '',
    SONAR_TOKEN = '',
    SCWIKI_TOKEN = '',
    codeReviewGuideFile = ''
  } = config || {};

  if (!AZURE_DEVOPS_PAT) {
    throw new Error('AZURE_DEVOPS_PAT must be defined in config.json');
  }

  const configObj = buildConfig({
    AZURE_DEVOPS_ORG_URL,
    AZURE_DEVOPS_PAT,
    HTTPS_PROXY,
    CONFLUENCE_BASE_URL,
    CONFLUENCE_PAT,
    NEXUS_USER_CODE,
    NEXUS_PASS_CODE,
    codeReviewGuideFile,
    SONAR_TOKEN,
    SCWIKI_TOKEN
  });

  logConfig(configObj, 'config.json');
  return configObj;
}

/**
 * Build standardized configuration object
 * @param {Object} options
 * @returns {Object} Configuration object
 */
function buildConfig({
  AZURE_DEVOPS_ORG_URL,
  AZURE_DEVOPS_PAT,
  HTTPS_PROXY,
  CONFLUENCE_BASE_URL,
  CONFLUENCE_PAT,
  NEXUS_USER_CODE = '',
  NEXUS_PASS_CODE = '',
  codeReviewGuideFile = '',
  SONAR_TOKEN = '',
  SCWIKI_TOKEN = ''
}) {
  const confluenceConfig = {
    baseUrl: CONFLUENCE_BASE_URL,
    token: CONFLUENCE_PAT
  };

  const nexusConfig = {
    baseUrl: 'https://sonatypenexus.global.standardchartered.com',
    userCode: NEXUS_USER_CODE,
    passCode: NEXUS_PASS_CODE
  };

  const sonarConfig = {
    baseUrl: 'https://sonarqube.vx.standardchartered.com',
    token: SONAR_TOKEN
  };

  // Unlike the other service URLs above, SC Wiki's URL is env-overridable (not fully hardcoded)
  const scwikiConfig = {
    baseUrl: process.env.SCWIKI_URL || 'https://scwiki.global.standardchartered.com',
    token: SCWIKI_TOKEN,
    wiki: process.env.SCWIKI_WIKI || 'xwiki'
  };

  return { 
    AZURE_DEVOPS_ORG_URL, 
    AZURE_DEVOPS_PAT, 
    confluenceConfig,
    nexusConfig,
    sonarConfig,
    scwikiConfig,
    HTTPS_PROXY,
    codeReviewGuideFile
  };
}

/**
 * Log a concise one-line startup summary (no credentials in full, sensitive values masked).
 * @param {Object} config - Configuration object
 * @param {string} source - Configuration source description
 */
function logConfig(config, source) {
  const confluence = config.confluenceConfig?.token ? 'yes' : 'no';
  const nexus = config.nexusConfig?.userCode ? 'yes' : 'no';
  const sonar = config.sonarConfig?.token ? 'yes' : 'no';
  const scwiki = config.scwikiConfig?.token ? 'yes' : 'no';
  console.error(
    `[SC-NODE-MCP] Config: ${source} | ADO: ${maskCredential(config.AZURE_DEVOPS_PAT)} | Confluence: ${confluence} | Nexus: ${nexus} | SonarQube: ${sonar} | SCWiki: ${scwiki}`
  );
}

/**
 * Mask sensitive credential for logging
 * @param {string} credential - Credential to mask
 * @returns {string} Masked credential
 */
function maskCredential(credential) {
  // Unreachable via getConfig(): every loader already validates AZURE_DEVOPS_PAT
  // is truthy before buildConfig()/logConfig() are reached.
  /* v8 ignore next */
  if (!credential) return 'Not set';
  if (credential.length <= 4) return '***';
  return '***' + credential.slice(-4);
}
