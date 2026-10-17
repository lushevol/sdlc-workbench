#!/usr/bin/env node
import { createRequire } from 'node:module';
import { createMcpServer, startMcpServer, getConfig, detectProxy, detectProxyFor, applyProxy, recordStartupTelemetry } from '@sc-node-mcp/core';
import { getADOConnection, configureAdoTools } from '@sc-node-mcp/ado';
import { configureUploadTools, configureUiResource } from '@sc-node-mcp/ado-upload-app';
import { configureConfluenceTools } from '@sc-node-mcp/confluence';
import { configureScwikiTools } from '@sc-node-mcp/scwiki';
import { getPythonBridge, configureEmailTools, getTeamsNativeBridge, configureTeamsTools } from '@sc-node-mcp/messaging';
import { getNexusConnection, configureNexusTools } from '@sc-node-mcp/nexus';
import { getSonarConnection, configureSonarTools } from '@sc-node-mcp/sonar';
import { configurePrompts } from './prompts.js';
import { configureContextTools } from './tools/context.js';
import { getActiveContext } from './context.js';

const require = createRequire(import.meta.url);
const { version } = require('../package.json');

/** Register Confluence tools if credentials are configured; logs and skips otherwise. */
function registerConfluenceTools(server, config, confluenceProxy) {
  try {
    const { confluenceConfig } = config;
    if (confluenceConfig.baseUrl && confluenceConfig.token) {
      configureConfluenceTools(server, { ...confluenceConfig, proxy: confluenceProxy });
    } else {
      console.error('[SC-NODE-MCP] Confluence credentials not provided — skipping Confluence tools');
    }
  } catch (e) {
    console.error('[SC-NODE-MCP] Confluence configuration error — skipping:', e.message);
  }
}

/** Register SC Wiki tools if credentials are configured; logs and skips otherwise. */
function registerScwikiTools(server, config, scwikiProxy) {
  try {
    const { scwikiConfig } = config;
    if (scwikiConfig.baseUrl && scwikiConfig.token) {
      configureScwikiTools(server, { ...scwikiConfig, proxy: scwikiProxy });
    } else {
      console.error('[SC-NODE-MCP] SC Wiki credentials not provided — skipping SC Wiki tools');
    }
  } catch (e) {
    console.error('[SC-NODE-MCP] SC Wiki configuration error — skipping:', e.message);
  }
}

/** Register Nexus IQ tools if credentials are configured; logs and skips otherwise. */
function registerNexusTools(server, config) {
  try {
    const { nexusConfig } = config;
    if (nexusConfig.userCode && nexusConfig.passCode) {
      const nexusConnectionProvider = () => getNexusConnection(nexusConfig.userCode, nexusConfig.passCode);
      configureNexusTools(server, nexusConnectionProvider);
    } else {
      console.error('[SC-NODE-MCP] Nexus IQ credentials not provided — skipping Nexus tools');
    }
  } catch (e) {
    console.error('[SC-NODE-MCP] Nexus IQ configuration error — skipping:', e.message);
  }
}

/** Register SonarQube tools if a token is configured; logs and skips otherwise. */
function registerSonarTools(server, config) {
  try {
    const { sonarConfig } = config;
    if (sonarConfig?.token) {
      const sonarConnectionProvider = () => getSonarConnection(sonarConfig.token);
      configureSonarTools(server, sonarConnectionProvider);
    } else {
      console.error('[SC-NODE-MCP] SonarQube token not provided — skipping SonarQube tools');
    }
  } catch (e) {
    console.error('[SC-NODE-MCP] SonarQube configuration error — skipping:', e.message);
  }
}

async function main() {
  try {
    // Load configuration first
    const config = getConfig();
    const { codeReviewGuideFile } = config;

    // Apply the configured proxy for ADO.
    const proxy = await detectProxy(config.HTTPS_PROXY);
    applyProxy(proxy);

    // Resolve the configured proxy and bypass rules for Confluence.
    const confluenceProxy = await detectProxyFor(
      'confluence.global.standardchartered.com',
      config.HTTPS_PROXY
    );

    // Resolve the configured proxy and bypass rules for SC Wiki.
    const scwikiProxy = await detectProxyFor(
      'scwiki.global.standardchartered.com',
      config.HTTPS_PROXY
    );

    console.error(`[SC-NODE-MCP] v${version} starting...`);

    // Build versions map — always-active packages plus conditionally-active ones
    const versions = {
      'sc-node-mcp': version,
      'ado': require('@sc-node-mcp/ado/package.json').version,
      'ado-upload-app': require('@sc-node-mcp/ado-upload-app/package.json').version,
      'messaging': require('@sc-node-mcp/messaging/package.json').version,
      ...((() => { try { return config.confluenceConfig?.token; } catch { return null; } })() ? { 'confluence': require('@sc-node-mcp/confluence/package.json').version } : {}),
      ...((() => { try { return config.scwikiConfig?.token; } catch { return null; } })() ? { 'scwiki': require('@sc-node-mcp/scwiki/package.json').version } : {}),
      ...((() => { try { return config.nexusConfig?.userCode; } catch { return null; } })() ? { 'nexus': require('@sc-node-mcp/nexus/package.json').version } : {}),
      ...((() => { try { return config.sonarConfig?.token; } catch { return null; } })() ? { 'sonar': require('@sc-node-mcp/sonar/package.json').version } : {}),
    };

    // Fire-and-forget startup telemetry — never blocks or crashes the server
    recordStartupTelemetry(config, getADOConnection, { versions }).catch(err =>
      console.error('[Telemetry] Unexpected error:', err.message)
    );
    
    const server = createMcpServer('sc-node-mcp', version);
    
    // Configure prompts
    configurePrompts(server);

    // Configure context tools (always available — reads/writes ~/.sc-node-mcp-context.json)
    configureContextTools(server);

    // Register context:// resource so AI clients can inspect the active context at any time
    server.resource(
      'Active Context',
      'context://active',
      { description: 'Current active workspace context (project, team, repos, Nexus app IDs, Confluence space)' },
      async (uri) => {
        const ctx = getActiveContext();
        const text = ctx ? JSON.stringify(ctx, null, 2) : 'No active context. Use ctx_set to create one.';
        return {
          contents: [{ uri: uri.href, mimeType: 'application/json', text }]
        };
      }
    );

    // Configure ADO tools (always available since PAT is required)
    configureAdoTools(server, getADOConnection, { codeReviewGuideFile });

    // Configure ADO Upload App tools (UI panel + headless upload)
    configureUploadTools(server, getADOConnection);
    configureUiResource(server);
    
    // Configure Email tools (always available - uses Outlook session, no credentials needed)
    configureEmailTools(server, getPythonBridge);

    configureTeamsTools(server, getTeamsNativeBridge);

    registerConfluenceTools(server, config, confluenceProxy);
    registerScwikiTools(server, config, scwikiProxy);
    registerNexusTools(server, config);
    registerSonarTools(server, config);

    await startMcpServer(server);
    console.error(`[SC-NODE-MCP] Tools registered: ${server.toolCount}`);
    console.error('[SC-NODE-MCP] Server ready');
  } catch (error) {
    console.error('[SC-NODE-MCP] Failed to start server:', error.message);
    throw error;
  }
}

// Run main() - this module is always the entry point
main().catch((error) => {
  console.error('Fatal error in main():', error);
  process.exit(1);
});
