#!/usr/bin/env node
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
import { realpathSync } from 'node:fs';

// Disable TLS certificate verification for corporate environments
process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';

import { createMcpServer, startMcpServer, getConfig, recordStartupTelemetry } from '@sc-node-mcp/core';
import { getADOConnection } from '@sc-node-mcp/ado-core/connection';
import { getNexusConnection } from './connection.js';
import { configureNexusTools } from './tools.js';
import { configureNexusPrompts } from './prompts.js';

async function main() {
  try {
    const config = getConfig();

    const { nexusConfig } = config;
    if (!nexusConfig.userCode || !nexusConfig.passCode) {
      throw new Error(
        'Nexus IQ credentials are required.\n' +
        'Usage: node index.js <ADO_PAT> [PROXY] [CONF_PAT] <NEXUS_USER_CODE> <NEXUS_PASS_CODE>\n' +
        'Or set NEXUS_USER_CODE and NEXUS_PASS_CODE environment variables.'
      );
    }

    const { version } = createRequire(import.meta.url)('../package.json');
    // Fire-and-forget startup telemetry — uses ADO PAT for identity
    recordStartupTelemetry(config, getADOConnection, { versions: { 'nexus': version } })
      .catch(err => console.error('[Telemetry] Unexpected error:', err.message));

    const server = createMcpServer('nexus', version);

    // Bind the Nexus connection to the configured credentials
    const nexusConnectionProvider = () => getNexusConnection(nexusConfig.userCode, nexusConfig.passCode);

    configureNexusTools(server, nexusConnectionProvider);
    configureNexusPrompts(server);

    await startMcpServer(server);

    console.error('Nexus IQ MCP server running on stdio');
  } catch (error) {
    console.error('Failed to start Nexus MCP server:', error.message);
    process.exit(1);
  }
}

const isMain = (() => {
  try {
    return realpathSync(fileURLToPath(import.meta.url)) === realpathSync(process.argv[1]);
  } catch {
    return import.meta.url === `file://${process.argv[1]}`;
  }
})();

if (isMain) {
  main().catch((error) => {
    console.error('Fatal error:', error);
    process.exit(1);
  });
}

export { configureNexusTools, getNexusConnection, configureNexusPrompts };
