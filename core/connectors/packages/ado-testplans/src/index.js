#!/usr/bin/env node
import { createRequire } from 'node:module';
process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';
import { createMcpServer, startMcpServer, getConfig, detectProxy, applyProxy, recordStartupTelemetry } from '@sc-node-mcp/core';
import { getADOConnection } from '@sc-node-mcp/ado-core/connection';
import { configureTestPlanToolsModule } from './tools.js';
import { configureTestPlanPrompts } from './prompts.js';

const { version } = createRequire(import.meta.url)('../package.json');
const config = getConfig();
const proxy = await detectProxy(config.HTTPS_PROXY);
applyProxy(proxy);
recordStartupTelemetry(config, getADOConnection, { versions: { 'ado-testplans': version } })
  .catch(err => console.error('[Telemetry] Unexpected error:', err.message));

const server = createMcpServer('ado-testplans', version);
configureTestPlanToolsModule(server, getADOConnection);
configureTestPlanPrompts(server);
await startMcpServer(server);

export { getADOConnection, configureTestPlanToolsModule, configureTestPlanPrompts };
