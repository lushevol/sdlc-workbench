#!/usr/bin/env node
import { createRequire } from 'node:module';
process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';

import { createMcpServer, startMcpServer, getConfig, detectProxy, applyProxy, recordStartupTelemetry } from '@sc-node-mcp/core';
import { getADOConnection } from '@sc-node-mcp/ado-core/connection';
import { configureSprintsTools } from './tools.js';
import { configureSprintsPrompts } from './prompts.js';

const { version } = createRequire(import.meta.url)('../package.json');
const config = getConfig();
const proxy = await detectProxy(config.HTTPS_PROXY);
applyProxy(proxy);
recordStartupTelemetry(config, getADOConnection, { versions: { 'ado-sprints': version } })
  .catch(err => console.error('[Telemetry] Unexpected error:', err.message));

const server = createMcpServer('ado-sprints', version);
configureSprintsTools(server, getADOConnection);
configureSprintsPrompts(server);
await startMcpServer(server);

export { getADOConnection, configureSprintsTools, configureSprintsPrompts };
