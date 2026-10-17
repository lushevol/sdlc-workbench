#!/usr/bin/env node
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
import { realpathSync } from 'node:fs';

// Disable TLS certificate verification for corporate environments
process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';

import { createMcpServer, startMcpServer, getConfig, recordStartupTelemetry } from '@sc-node-mcp/core';
import { getADOConnection } from '@sc-node-mcp/ado-core/connection';
import { getSonarConnection } from './connection.js';
import { configureSonarTools } from './tools.js';
import { configureSonarPrompts } from './prompts.js';

async function main() {
  try {
    const config = getConfig();

    const { sonarConfig } = config;
    if (!sonarConfig?.token) {
      throw new Error(
        'SonarQube token is required.\n' +
        'Usage: node index.js <ADO_PAT> [PROXY] [CONF_PAT] [NEXUS_USER] [NEXUS_PASS] <SONAR_TOKEN>\n' +
        'Or set the SONAR_TOKEN environment variable.'
      );
    }

    const { version } = createRequire(import.meta.url)('../package.json');
    // Fire-and-forget startup telemetry — uses ADO PAT for identity
    recordStartupTelemetry(config, getADOConnection, { versions: { 'sonar': version } })
      .catch(err => console.error('[Telemetry] Unexpected error:', err.message));

    const server = createMcpServer('sonar', version);

    const sonarConnectionProvider = () => getSonarConnection(sonarConfig.token);
    configureSonarTools(server, sonarConnectionProvider);
    configureSonarPrompts(server);

    await startMcpServer(server);

    console.error('SonarQube MCP server running on stdio');
  } catch (error) {
    console.error('Failed to start SonarQube MCP server:', error.message);
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

export { configureSonarTools, getSonarConnection, configureSonarPrompts };
