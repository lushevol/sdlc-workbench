#!/usr/bin/env node
import { createRequire } from 'node:module';

import { createMcpServer, startMcpServer, getConfig, detectProxy, applyProxy, recordStartupTelemetry } from '@sc-node-mcp/core';
import { getADOConnection } from '@sc-node-mcp/ado-core/connection';
import { configureReposWriteTools } from './tools.js';
import { configureReposWritePrompts } from './prompts.js';

const { version } = createRequire(import.meta.url)('../package.json');
const config = getConfig();
const proxy = await detectProxy(config.HTTPS_PROXY);
applyProxy(proxy);
recordStartupTelemetry(config, getADOConnection, { versions: { 'ado-repos-write': version } })
  .catch(err => console.error('[Telemetry] Unexpected error:', err.message));

const server = createMcpServer('ado-repos-write', version);
configureReposWriteTools(server, getADOConnection);
configureReposWritePrompts(server);
await startMcpServer(server);

export { getADOConnection, configureReposWriteTools, configureReposWritePrompts };
