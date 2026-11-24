#!/usr/bin/env node
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
import { realpathSync } from 'node:fs';

import { createMcpServer, startMcpServer, getConfig, recordStartupTelemetry } from '@sc-node-mcp/core';
import { getADOConnection } from '@sc-node-mcp/ado-core/connection';
import { getPythonBridge, getTeamsNativeBridge } from './connection.js';
import { configureEmailTools } from './tools.js';
import { configureTeamsTools } from './tools/teams.js';
import { configureMessagingPrompts } from './prompts.js';

/**
 * Main entry point for the Email MCP server
 */
async function main() {
  try {
    const config = getConfig();
    const { version } = createRequire(import.meta.url)('../package.json');

    // Fire-and-forget startup telemetry — uses ADO PAT for identity
    recordStartupTelemetry(config, getADOConnection, { versions: { 'messaging': version } })
      .catch(err => console.error('[Telemetry] Unexpected error:', err.message));

    // Create MCP server
    const server = createMcpServer('messaging', version);
    
    // Register email tools
    configureEmailTools(server, getPythonBridge);
    
    // Register Teams tools
    configureTeamsTools(server, getTeamsNativeBridge);

    // Register messaging prompts
    configureMessagingPrompts(server);
    
    // Start the server
    await startMcpServer(server);
    
    console.error('Messaging MCP server running on stdio');
    console.error('Ready to send emails via Outlook and messages via Microsoft Teams');
  } catch (error) {
    console.error('Failed to start Email MCP server:', error);
    process.exit(1);
  }
}

// Run main if this file is executed directly
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

// Export for testing and programmatic use
export { getPythonBridge, configureEmailTools, getTeamsNativeBridge, configureTeamsTools, configureMessagingPrompts };
