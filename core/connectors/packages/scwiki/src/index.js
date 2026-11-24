#!/usr/bin/env node
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
import { realpathSync } from 'node:fs';

import { createMcpServer, startMcpServer, getConfig, detectProxyFor, recordStartupTelemetry } from '@sc-node-mcp/core';
import { getADOConnection } from '@sc-node-mcp/ado-core/connection';
import { configureScwikiTools } from './tools.js';
import { configureScwikiPrompts } from './prompts.js';

async function main() {
  try {
    console.error('[SC-NODE-MCP] SC Wiki starting...');
    const config = getConfig();
    const { scwikiConfig, HTTPS_PROXY } = config;

    if (!scwikiConfig.baseUrl || !scwikiConfig.token) {
      throw new Error(
        'SC Wiki configuration is incomplete.\n' +
        'Usage: node index.js <ADO_PAT> [PROXY] [CONF_PAT] [NEXUS_USER] [NEXUS_PASS] [SONAR_TOKEN] <SCWIKI_TOKEN>\n' +
        'Or set the SCWIKI_TOKEN environment variable.'
      );
    }

    // Resolve the configured proxy and bypass rules for SC Wiki.
    const scwikiProxy = await detectProxyFor(
      'scwiki.global.standardchartered.com',
      HTTPS_PROXY
    );

    const { version } = createRequire(import.meta.url)('../package.json');
    // Fire-and-forget startup telemetry — uses ADO PAT for identity
    recordStartupTelemetry(config, getADOConnection, { versions: { 'scwiki': version } })
      .catch(err => console.error('[Telemetry] Unexpected error:', err.message));

    const server = createMcpServer('scwiki', version);
    configureScwikiTools(server, { ...scwikiConfig, proxy: scwikiProxy });
    configureScwikiPrompts(server);

    await startMcpServer(server);
    console.error('SC Wiki MCP Server running on stdio');
  } catch (error) {
    console.error('Failed to start SC Wiki MCP server:', error.message);
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
  try {
    await main();
  } catch (error) {
    console.error('Fatal error in main():', error);
    process.exit(1);
  }
}

export { configureScwikiTools, configureScwikiPrompts };
