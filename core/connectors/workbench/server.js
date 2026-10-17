import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { setConfig } from '../packages/core/src/config.js';
import { detectProxyFor } from '../packages/core/src/proxy.js';

export const CONNECTORS = Object.freeze([
  'ado', 'confluence', 'scwiki', 'nexus', 'sonar', 'messaging', 'web',
]);

function requireSettings(values) {
  if (values.some(value => typeof value !== 'string' || !value.trim())) {
    throw new Error('The selected connector configuration is incomplete.');
  }
}

function requireEndpoint(value) {
  requireSettings([value]);
  const url = new URL(value);
  if (!['http:', 'https:'].includes(url.protocol) || url.username || url.password || url.search || url.hash) {
    throw new Error('The selected connector endpoint is invalid.');
  }
}

export function validateConnectorConfig(connector, config) {
  switch (connector) {
    case 'ado':
      requireEndpoint(config.AZURE_DEVOPS_ORG_URL);
      requireSettings([config.AZURE_DEVOPS_PAT]);
      break;
    case 'confluence':
      requireEndpoint(config.confluenceConfig.baseUrl);
      requireSettings([config.confluenceConfig.token]);
      break;
    case 'scwiki':
      requireEndpoint(config.scwikiConfig.baseUrl);
      requireSettings([config.scwikiConfig.token]);
      break;
    case 'nexus':
      requireEndpoint(config.nexusConfig.baseUrl);
      requireSettings([config.nexusConfig.userCode, config.nexusConfig.passCode]);
      break;
    case 'sonar':
      requireEndpoint(config.sonarConfig.baseUrl);
      requireSettings([config.sonarConfig.token]);
      break;
  }
}

export async function createConnectorServer(connector, config) {
  if (!CONNECTORS.includes(connector)) throw new Error('The connector is unsupported.');
  setConfig(config);
  const server = new McpServer({ name: `workbench-${connector}`, version: '1.0.0' });

  switch (connector) {
    case 'ado': {
      const azdev = await import('azure-devops-node-api');
      const { configureAdoTools } = await import('../packages/ado/src/tools.js');
      const connection = () => new azdev.WebApi(
        config.AZURE_DEVOPS_ORG_URL,
        azdev.getPersonalAccessTokenHandler(config.AZURE_DEVOPS_PAT),
      );
      configureAdoTools(server, connection, { codeReviewGuideFile: config.codeReviewGuideFile });
      break;
    }
    case 'confluence': {
      const { configureConfluenceTools } = await import('../packages/confluence/src/tools.js');
      const proxy = config.confluenceConfig.baseUrl ?
        await detectProxyFor(config.confluenceConfig.baseUrl, config.HTTPS_PROXY) : '';
      configureConfluenceTools(server, { ...config.confluenceConfig, proxy });
      break;
    }
    case 'scwiki': {
      const { configureScwikiTools } = await import('../packages/scwiki/src/tools.js');
      const proxy = config.scwikiConfig.baseUrl ?
        await detectProxyFor(config.scwikiConfig.baseUrl, config.HTTPS_PROXY) : '';
      configureScwikiTools(server, { ...config.scwikiConfig, proxy });
      break;
    }
    case 'nexus': {
      const { baseUrl, userCode, passCode } = config.nexusConfig;
      const { configureNexusTools } = await import('../packages/nexus/src/tools.js');
      configureNexusTools(server, () => ({
        baseUrl,
        headers: {
          Authorization: `Basic ${Buffer.from(`${userCode}:${passCode}`).toString('base64')}`,
          'Content-Type': 'application/json',
          Accept: 'application/json',
        },
      }));
      break;
    }
    case 'sonar': {
      const { baseUrl, token } = config.sonarConfig;
      const { configureSonarTools } = await import('../packages/sonar/src/tools.js');
      configureSonarTools(server, () => ({
        baseUrl,
        headers: { Authorization: `Bearer ${token}`, Accept: 'application/json' },
      }));
      break;
    }
    case 'messaging': {
      const { getPythonBridge, getTeamsNativeBridge } = await import('../packages/messaging/src/connection.js');
      const { configureEmailTools } = await import('../packages/messaging/src/tools.js');
      const { configureTeamsTools } = await import('../packages/messaging/src/tools/teams.js');
      configureEmailTools(server, getPythonBridge);
      configureTeamsTools(server, getTeamsNativeBridge);
      break;
    }
    case 'web': {
      const { configureWebTools } = await import('../packages/web/src/tools.js');
      configureWebTools(server, config.HTTPS_PROXY);
      break;
    }
  }
  return server;
}
