#!/usr/bin/env node

/**
 * Generate VS Code MCP one-click install URLs
 * Creates encoded URLs for both VS Code Stable and Insiders
 * with input prompts for user configuration
 */

// VS Code input prompts configuration
const inputs = [
  {
    id: 'ado_pat',
    type: 'promptString',
    description: 'Azure DevOps Personal Access Token',
    password: true
  },
  {
    id: 'https_proxy',
    type: 'promptString',
    description: 'HTTPS Proxy URL (optional, e.g., http://10.239.9.190:443 - press Enter to skip)'
  },
  {
    id: 'confluence_pat',
    type: 'promptString',
    description: 'Confluence PAT (optional, press Enter to skip)',
    password: true
  },
  {
    id: 'nexus_user',
    type: 'promptString',
    description: 'Nexus IQ User Code (optional, press Enter to skip)'
  },
  {
    id: 'nexus_pass',
    type: 'promptString',
    description: 'Nexus IQ Pass Code (optional, press Enter to skip)',
    password: true
  },
  {
    id: 'sonar_token',
    type: 'promptString',
    description: 'SonarQube Token (optional, press Enter to skip)',
    password: true
  },
  {
    id: 'scwiki_token',
    type: 'promptString',
    description: 'SC Wiki (XWiki) Bearer Token (optional, press Enter to skip)',
    password: true
  },
  {
    id: 'code_review_guide',
    type: 'promptString',
    description: 'Your CODE_REVIEW_GUIDE.md file full path (optional, press Enter to skip)'
  }
];

// MCP Server configuration
const serverConfig = {
  type: 'stdio',
  command: 'npx',
  args: [
    '-y',
    '@sc-node-mcp/unified',
    '${input:ado_pat}',
    '${input:https_proxy}',
    '${input:confluence_pat}',
    '${input:nexus_user}',
    '${input:nexus_pass}',
    '${input:sonar_token}',
    '${input:scwiki_token}'
  ],
  env: {
    CODE_REVIEW_GUIDE_FILE: '${input:code_review_guide}',
    npm_config_registry: "https://artifactory.global.standardchartered.com/artifactory/api/npm/npm-release"
  }
};

// Encode configurations for URL
const encodedConfig = encodeURIComponent(JSON.stringify(serverConfig));
const encodedInputs = encodeURIComponent(JSON.stringify(inputs));

// Server name for VS Code
const serverName = 'sc-node-mcp';

// Generate URLs
const stableBaseUrl = 'https://vscode.dev/redirect/mcp/install';
const insidersBaseUrl = 'https://vscode.dev/redirect/mcp/install';
const stableUrl = `${stableBaseUrl}?name=${serverName}&config=${encodedConfig}&inputs=${encodedInputs}`;
const insidersUrl = `${insidersBaseUrl}?name=${serverName}&quality=insiders&config=${encodedConfig}&inputs=${encodedInputs}`;

// Badge URLs
const stableBadgeUrl = 'https://img.shields.io/badge/VS_Code-Install_SC_NODE_MCP/UNIFIED-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white';
const insidersBadgeUrl = 'https://img.shields.io/badge/VS_Code_Insiders-Install_SC_NODE_MCP/UNIFIED-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white';

// Community links
const teamsChannelBadgeUrl = 'https://img.shields.io/badge/Teams-SC_Node_MCP_Channel-6264A7?style=flat-square&logo=microsoftteams&logoColor=white';
const teamsChannelUrl = 'https://teams.microsoft.com/l/channel/19%3Aa7d9f31b11af4fde82c04c5c98c85411%40thread.tacv2/SC%20Node%20MCP?groupId=183250c7-8132-4b25-9e5b-207d4393d739&tenantId=b44900f1-2def-4c3b-9ec6-9020d604e19e';

// ADO Pipeline status and coverage
const adoOrg = 'sc-ado';
const adoProject = 'DDCPQPR';
const adoPipelineId = '46487';
const adoBranch = 'main';
const adoPipelineUrl = `https://dev.azure.com/${adoOrg}/${adoProject}/_build?definitionId=${adoPipelineId}&_a=summary`;
const adoPipelineBadgeUrl = `https://dev.azure.com/${adoOrg}/${adoProject}/_apis/build/status/${adoPipelineId}?branchName=${adoBranch}&style=flat-square&label=Pipeline`;

// ─── Granular package URL helpers ─────────────────────────────────────────────

const REGISTRY_URL = 'https://artifactory.global.standardchartered.com/artifactory/api/npm/npm-release';

const INPUT_ADO_PAT = { id: 'ado_pat', type: 'promptString', description: 'Azure DevOps Personal Access Token', password: true };
const INPUT_HTTPS_PROXY = { id: 'https_proxy', type: 'promptString', description: 'HTTPS Proxy URL (optional, e.g., http://10.239.9.190:443 - press Enter to skip)' };
const INPUT_CODE_REVIEW_GUIDE = { id: 'code_review_guide', type: 'promptString', description: 'Your CODE_REVIEW_GUIDE.md file full path (optional, press Enter to skip)' };
const INPUT_CONFLUENCE_PAT = { id: 'confluence_pat', type: 'promptString', description: 'Confluence PAT (optional, press Enter to skip)', password: true };
const INPUT_NEXUS_USER = { id: 'nexus_user', type: 'promptString', description: 'Nexus IQ User Code (optional, press Enter to skip)' };
const INPUT_NEXUS_PASS = { id: 'nexus_pass', type: 'promptString', description: 'Nexus IQ Pass Code (optional, press Enter to skip)', password: true };
const INPUT_SONAR_TOKEN = { id: 'sonar_token', type: 'promptString', description: 'SonarQube Token (optional, press Enter to skip)', password: true };
const INPUT_SCWIKI_TOKEN = { id: 'scwiki_token', type: 'promptString', description: 'SC Wiki (XWiki) Bearer Token (optional, press Enter to skip)', password: true };
const INPUT_CHROMEDRIVER_PATH = { id: 'chromedriver_path', type: 'promptString', description: 'Absolute path to chromedriver (optional, press Enter to skip)' };
const INPUT_EDGEDRIVER_PATH = { id: 'edgedriver_path', type: 'promptString', description: 'Absolute path to msedgedriver (optional, press Enter to skip)' };

function makeInstallUrls(pkg, args, inputList, nameSlug, label) {
  const config = {
    type: 'stdio',
    command: 'npx',
    args: ['-y', pkg, ...args],
    env: { npm_config_registry: REGISTRY_URL }
  };
  const name = nameSlug || pkg.replace('@sc-node-mcp/', 'sc-node-mcp-');
  const base = 'https://vscode.dev/redirect/mcp/install';
  const encConfig = encodeURIComponent(JSON.stringify(config));
  const encInputs = encodeURIComponent(JSON.stringify(inputList));
  const badgeLabel = (label || pkg.replace('@sc-node-mcp/', '')).toUpperCase().replaceAll('-', '_');
  const stableUrl = `${base}?name=${name}&config=${encConfig}&inputs=${encInputs}`;
  const insidersUrl = `${base}?name=${name}&quality=insiders&config=${encConfig}&inputs=${encInputs}`;
  const stableBadge = `https://img.shields.io/badge/VS_Code-Install_${badgeLabel}-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white`;
  const insidersBadge = `https://img.shields.io/badge/VS_Code_Insiders-Install_${badgeLabel}-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white`;
  return { stableUrl, insidersUrl, stableBadge, insidersBadge };
}

// Granular package install URL definitions
const granularPackages = [
  {
    pkg: '@sc-node-mcp/ado',
    label: 'ado',
    args: ['${input:ado_pat}', '${input:https_proxy}'],
    inputs: [INPUT_ADO_PAT, INPUT_HTTPS_PROXY, INPUT_CODE_REVIEW_GUIDE],
    description: 'All ADO tools (meta-package)'
  },
  {
    pkg: '@sc-node-mcp/ado-workitems-read',
    label: 'ado-workitems-read',
    args: ['${input:ado_pat}', '${input:https_proxy}'],
    inputs: [INPUT_ADO_PAT, INPUT_HTTPS_PROXY],
    description: 'ADO Work Items — Read (17 tools)'
  },
  {
    pkg: '@sc-node-mcp/ado-workitems-write',
    label: 'ado-workitems-write',
    args: ['${input:ado_pat}', '${input:https_proxy}'],
    inputs: [INPUT_ADO_PAT, INPUT_HTTPS_PROXY],
    description: 'ADO Work Items — Write (9 tools)'
  },
  {
    pkg: '@sc-node-mcp/ado-repos-read',
    label: 'ado-repos-read',
    args: ['${input:ado_pat}', '${input:https_proxy}'],
    inputs: [INPUT_ADO_PAT, INPUT_HTTPS_PROXY],
    description: 'ADO Repos — Read (12 tools)'
  },
  {
    pkg: '@sc-node-mcp/ado-repos-write',
    label: 'ado-repos-write',
    args: ['${input:ado_pat}', '${input:https_proxy}'],
    inputs: [INPUT_ADO_PAT, INPUT_HTTPS_PROXY],
    description: 'ADO Repos — Write (9 tools)'
  },
  {
    pkg: '@sc-node-mcp/ado-review',
    label: 'ado-review',
    args: ['${input:ado_pat}', '${input:https_proxy}'],
    inputs: [INPUT_ADO_PAT, INPUT_HTTPS_PROXY, INPUT_CODE_REVIEW_GUIDE],
    description: 'ADO PR Review (4 tools)'
  },
  {
    pkg: '@sc-node-mcp/ado-pipelines',
    label: 'ado-pipelines',
    args: ['${input:ado_pat}', '${input:https_proxy}'],
    inputs: [INPUT_ADO_PAT, INPUT_HTTPS_PROXY],
    description: 'ADO Pipelines (12 tools)'
  },
  {
    pkg: '@sc-node-mcp/ado-testplans',
    label: 'ado-testplans',
    args: ['${input:ado_pat}', '${input:https_proxy}'],
    inputs: [INPUT_ADO_PAT, INPUT_HTTPS_PROXY],
    description: 'ADO Test Plans (9 tools)'
  },
  {
    pkg: '@sc-node-mcp/ado-sprints',
    label: 'ado-sprints',
    args: ['${input:ado_pat}', '${input:https_proxy}'],
    inputs: [INPUT_ADO_PAT, INPUT_HTTPS_PROXY],
    description: 'ADO Sprints & Capacity (8 tools)'
  },
  {
    pkg: '@sc-node-mcp/ado-search',
    label: 'ado-search',
    args: ['${input:ado_pat}', '${input:https_proxy}'],
    inputs: [INPUT_ADO_PAT, INPUT_HTTPS_PROXY],
    description: 'ADO Search — Code & Work Items (2 tools)'
  },
  {
    pkg: '@sc-node-mcp/confluence',
    label: 'confluence',
    args: ['${input:ado_pat}', '${input:https_proxy}', '${input:confluence_pat}'],
    inputs: [INPUT_ADO_PAT, INPUT_HTTPS_PROXY, INPUT_CONFLUENCE_PAT],
    description: 'Confluence (15 tools)'
  },
  {
    pkg: '@sc-node-mcp/scwiki',
    label: 'scwiki',
    args: ['${input:ado_pat}', '${input:https_proxy}', '', '', '', '', '${input:scwiki_token}'],
    inputs: [INPUT_ADO_PAT, INPUT_HTTPS_PROXY, INPUT_SCWIKI_TOKEN],
    description: 'SC Wiki (14 tools)'
  },
  {
    pkg: '@sc-node-mcp/messaging',
    label: 'messaging',
    args: ['${input:ado_pat}', '${input:https_proxy}'],
    inputs: [INPUT_ADO_PAT, INPUT_HTTPS_PROXY],
    description: 'Messaging — Outlook + Teams'
  },
  {
    pkg: '@sc-node-mcp/nexus',
    label: 'nexus',
    args: ['${input:ado_pat}', '${input:https_proxy}', '', '${input:nexus_user}', '${input:nexus_pass}'],
    inputs: [INPUT_ADO_PAT, INPUT_HTTPS_PROXY, INPUT_NEXUS_USER, INPUT_NEXUS_PASS],
    description: 'Nexus IQ Scanning (2 tools)'
  },
  {
    pkg: '@sc-node-mcp/sonar',
    label: 'sonar',
    args: ['${input:ado_pat}', '${input:https_proxy}', '', '', '', '${input:sonar_token}'],
    inputs: [INPUT_ADO_PAT, INPUT_HTTPS_PROXY, INPUT_SONAR_TOKEN],
    description: 'SonarQube (6 tools)'
  },
  {
    pkg: '@sc-node-mcp/ado-upload-app',
    label: 'ado-upload-app',
    args: ['${input:ado_pat}', '${input:https_proxy}'],
    inputs: [INPUT_ADO_PAT, INPUT_HTTPS_PROXY],
    description: 'ADO Upload App (file attachments UI)'
  },
  {
    pkg: '@sc-node-mcp/web',
    label: 'web',
    args: ['${input:ado_pat}', '${input:https_proxy}'],
    inputs: [INPUT_ADO_PAT, INPUT_HTTPS_PROXY],
    description: 'Web Search & Crawl (4 tools)'
  },
  {
    pkg: '@sc-node-mcp/app-bridge',
    label: 'app-bridge',
    args: ['--chromedriver-path', '${input:chromedriver_path}', '--edgedriver-path', '${input:edgedriver_path}'],
    inputs: [INPUT_CHROMEDRIVER_PATH, INPUT_EDGEDRIVER_PATH],
    description: 'Browser Automation — Selenium WebDriver (48 tools)'
  }
];

// Generate URL objects for all granular packages
const granularUrls = granularPackages.map(p => ({
  ...p,
  ...makeInstallUrls(p.pkg, p.args, p.inputs, undefined, p.label)
}));

// Generate the granular packages Markdown table
function generateGranularTable() {
  const rows = granularUrls.map(p =>
    `| ${p.description} | [![VS Code](${p.stableBadge})](${p.stableUrl}) [![VS Code Insiders](${p.insidersBadge})](${p.insidersUrl}) |`
  );
  return [
    '| Package | Install |',
    '|---------|---------|',
    ...rows
  ].join('\n');
}

// Named exports for use by other scripts (e.g. update-readme.js)
export { inputs, serverConfig, stableUrl, insidersUrl, stableBadgeUrl, insidersBadgeUrl, teamsChannelBadgeUrl, teamsChannelUrl, adoPipelineUrl, adoPipelineBadgeUrl, granularUrls, generateGranularTable };

// Only print when run directly
if (import.meta.url === `file://${process.argv[1]}`) {
  console.log('='.repeat(80));
  console.log('VS Code MCP One-Click Install URLs');
  console.log('='.repeat(80));
  console.log('');

  console.log('VS Code Stable URL:');
  console.log(stableUrl);
  console.log('');

  console.log('VS Code Insiders URL:');
  console.log(insidersUrl);
  console.log('');

  console.log('='.repeat(80));
  console.log('Markdown Badges for README.md');
  console.log('='.repeat(80));
  console.log('');

  console.log('VS Code Stable Badge:');
  console.log(`[![Install with NPX in VS Code](${stableBadgeUrl})](${stableUrl})`);
  console.log('');

  console.log('VS Code Insiders Badge:');
  console.log(`[![Install with NPX in VS Code Insiders](${insidersBadgeUrl})](${insidersUrl})`);
  console.log('');

  console.log('='.repeat(80));
  console.log('Configuration Details');
  console.log('='.repeat(80));
  console.log('');

  console.log('Server Name:', serverName);
  console.log('Package:', serverConfig.args[1]);
  console.log('Command:', serverConfig.command);
  console.log('Number of Input Prompts:', inputs.length);
  console.log('');

  console.log('Input Prompts:');
  inputs.forEach((input, index) => {
    console.log(`  ${index + 1}. ${input.id}: ${input.description}${input.password ? ' (masked)' : ''}`);
  });
  console.log('');

  console.log('='.repeat(80));
  console.log('Next Steps');
  console.log('='.repeat(80));
  console.log('');
  console.log('1. Run `npm run update-readme` to sync install URLs in README.md automatically');
  console.log('2. Test the install URLs in both VS Code Stable and Insiders');
  console.log('3. Verify all input prompts appear correctly');
  console.log('4. Ensure the package is published to SCB NPM registry before sharing');
  console.log('');

  console.log('='.repeat(80));
  console.log('Publishing Checklist');
  console.log('='.repeat(80));
  console.log('');
  console.log('□ Packages configured with publishConfig pointing to SCB registry');
  console.log('□ All package.json files have "files" field (excludes tests/coverage)');
  console.log('□ Shebangs added to all entry points (#!/usr/bin/env node)');
  console.log('□ Config loading supports command-line args');
  console.log('□ Logged into SCB NPM registry: npm login --registry=https://artifactory.global.standardchartered.com/artifactory/api/npm/npm-release');
  console.log('□ Tested locally with npm link');
  console.log('□ Ready to publish: lerna publish');
  console.log('');
}