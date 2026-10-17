#!/usr/bin/env node
import { createRequire } from 'node:module';
process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';

import { createMcpServer, startMcpServer, getConfig, detectProxy, applyProxy, recordStartupTelemetry } from '@sc-node-mcp/core';
import { getADOConnection } from '@sc-node-mcp/ado-core/connection';
import { configureWorkItemsReadTools } from './tools.js';
import { configureWorkItemsReadPrompts } from './prompts.js';

const { version } = createRequire(import.meta.url)('../package.json');
const config = getConfig();
const proxy = await detectProxy(config.HTTPS_PROXY);
applyProxy(proxy);
recordStartupTelemetry(config, getADOConnection, { versions: { 'ado-workitems-read': version } })
  .catch(err => console.error('[Telemetry] Unexpected error:', err.message));

const server = createMcpServer('ado-workitems-read', version);
configureWorkItemsReadTools(server, getADOConnection);
configureWorkItemsReadPrompts(server);
await startMcpServer(server);

export { getADOConnection, configureWorkItemsReadTools, configureWorkItemsReadPrompts };
