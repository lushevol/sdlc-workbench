#!/usr/bin/env node
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
import { realpathSync } from 'node:fs';
process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';

import { createMcpServer, startMcpServer, getConfig, detectProxy, applyProxy, recordStartupTelemetry } from '@sc-node-mcp/core';
import { getADOConnection } from './connection.js';
import { configureAdoTools } from './tools.js';
import { configureAdoPrompts } from './prompts.js';

const { version } = createRequire(import.meta.url)('../package.json');

async function main() {
  const config = getConfig();
  const { codeReviewGuideFile } = config;

  // Auto-detect and apply the best proxy
  const proxy = await detectProxy(config.HTTPS_PROXY);
  applyProxy(proxy);

  // Fire-and-forget startup telemetry — never blocks or crashes the server
  recordStartupTelemetry(config, getADOConnection, { versions: { 'ado': version } })
    .catch(err => console.error('[Telemetry] Unexpected error:', err.message));

  const server = createMcpServer('ado', version);
  
  // Configure ADO tools
  configureAdoTools(server, getADOConnection, { codeReviewGuideFile });

  // Configure ADO prompts
  configureAdoPrompts(server);
  
  await startMcpServer(server);
  console.error('[SC-NODE-MCP] ADO server ready');
}

// Only run main() if this file is executed directly, not when imported
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

export { getADOConnection, configureAdoTools, configureAdoPrompts };
