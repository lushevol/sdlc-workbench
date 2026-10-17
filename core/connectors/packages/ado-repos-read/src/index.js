#!/usr/bin/env node
import { createRequire } from 'node:module';

import { createMcpServer, startMcpServer, getConfig, detectProxy, applyProxy, recordStartupTelemetry } from '@sc-node-mcp/core';
import { getADOConnection } from '@sc-node-mcp/ado-core/connection';
import { configureReposReadTools } from './tools.js';
import { configureReposReadPrompts } from './prompts.js';

const { version } = createRequire(import.meta.url)('../package.json');
const config = getConfig();
const proxy = await detectProxy(config.HTTPS_PROXY);
applyProxy(proxy);
recordStartupTelemetry(config, getADOConnection, { versions: { 'ado-repos-read': version } })
  .catch(err => console.error('[Telemetry] Unexpected error:', err.message));

const server = createMcpServer('ado-repos-read', version);
configureReposReadTools(server, getADOConnection);
configureReposReadPrompts(server);
await startMcpServer(server);

export { getADOConnection, configureReposReadTools, configureReposReadPrompts };
