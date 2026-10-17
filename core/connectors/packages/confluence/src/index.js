#!/usr/bin/env node
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
import { realpathSync } from 'node:fs';

import { createMcpServer, startMcpServer, getConfig, detectProxyFor, recordStartupTelemetry } from '@sc-node-mcp/core';
import { getADOConnection } from '@sc-node-mcp/ado-core/connection';
import { configureConfluenceTools } from './tools.js';
import { configureConfluencePrompts } from './prompts.js';

async function main() {
  try {
    console.error('[SC-NODE-MCP] Confluence starting...');
    const config = getConfig();
    const { confluenceConfig, HTTPS_PROXY } = config;

    if (!confluenceConfig.baseUrl || !confluenceConfig.token) {
      throw new Error(
        'Confluence configuration is incomplete.\n' +
        'Usage: node index.js <ADO_PAT> [PROXY] <CONF_PAT>\n' +
        'Or set the CONFLUENCE_PAT environment variable.'
      );
    }

    // Resolve the configured proxy and bypass rules for Confluence.
    const confluenceProxy = await detectProxyFor(
      'confluence.global.standardchartered.com',
      HTTPS_PROXY
    );

    const { version } = createRequire(import.meta.url)('../package.json');
    // Fire-and-forget startup telemetry — uses ADO PAT for identity
    recordStartupTelemetry(config, getADOConnection, { versions: { 'confluence': version } })
      .catch(err => console.error('[Telemetry] Unexpected error:', err.message));

    const server = createMcpServer('confluence', version);
    configureConfluenceTools(server, { ...confluenceConfig, proxy: confluenceProxy });
    configureConfluencePrompts(server);

    await startMcpServer(server);
    console.error('Confluence MCP Server running on stdio');
  } catch (error) {
    console.error('Failed to start Confluence MCP server:', error.message);
    process.exit(1);
  }
}

// Only run main() if this file is executed directly, not when imported by the unified package
const isMain = (() => {
  try {
    return realpathSync(fileURLToPath(import.meta.url)) === realpathSync(process.argv[1]);
  } catch {
    return import.meta.url === `file://${process.argv[1]}`;
  }
})();

if (isMain) {
  main().catch((error) => {
    console.error('Fatal error in main():', error);
    process.exit(1);
  });
}

export { configureConfluenceTools, configureConfluencePrompts };
