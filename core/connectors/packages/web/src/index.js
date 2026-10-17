#!/usr/bin/env node
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
import { realpathSync } from 'node:fs';

// Disable TLS certificate verification for corporate environments
process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';

import { createMcpServer, startMcpServer, getConfig, detectProxy, detectProxyFor, applyProxy } from '@sc-node-mcp/core';
import { configureWebTools } from './tools.js';
import { configureWebPrompts } from './prompts.js';

async function main() {
  try {
    const config = getConfig();

    const proxy = await detectProxy(config.HTTPS_PROXY);
    applyProxy(proxy);

    // Detect proxy for external internet — may differ from the ADO proxy route.
    // If no candidate succeeds for DuckDuckGo (e.g. corporate firewall blocks the probe),
    // fall back to the ADO proxy so the Python bridge and web_fetch still route through it.
    const webProxy = (await detectProxyFor('html.duckduckgo.com', config.HTTPS_PROXY)) || proxy;

    const { version } = createRequire(import.meta.url)('../package.json');

    const server = createMcpServer('sc-node-mcp-web', version);

    configureWebTools(server, webProxy);
    configureWebPrompts(server);

    await startMcpServer(server);

    console.error('Web MCP server running on stdio');
  } catch (error) {
    console.error('Failed to start Web MCP server:', error.message);
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

export { configureWebTools, configureWebPrompts };
