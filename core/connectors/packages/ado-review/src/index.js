#!/usr/bin/env node
import { createRequire } from 'node:module';
process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';
import { createMcpServer, startMcpServer, getConfig, detectProxy, applyProxy, recordStartupTelemetry } from '@sc-node-mcp/core';
import { getADOConnection } from '@sc-node-mcp/ado-core/connection';
import { configureReviewTools } from './tools.js';
import { configureReviewPrompts } from './prompts.js';

const { version } = createRequire(import.meta.url)('../package.json');
const config = getConfig();
const proxy = await detectProxy(config.HTTPS_PROXY);
applyProxy(proxy);
recordStartupTelemetry(config, getADOConnection, { versions: { 'ado-review': version } })
  .catch(err => console.error('[Telemetry] Unexpected error:', err.message));

const server = createMcpServer('ado-review', version);
configureReviewTools(server, getADOConnection, { codeReviewGuideFile: config.codeReviewGuideFile });
configureReviewPrompts(server);
await startMcpServer(server);

export { getADOConnection, configureReviewTools, configureReviewPrompts };
