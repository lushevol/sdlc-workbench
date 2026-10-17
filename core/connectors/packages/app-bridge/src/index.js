#!/usr/bin/env node
/**
 * @author Podder, Arunangshu
 * @bankId 2004018
 */
process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';

import { createRequire } from 'node:module';
import { createMcpServer, startMcpServer } from '@sc-node-mcp/core';
import { getAppBridgeConfig } from './config.js';
import { configureAppBridgeTools } from './tools.js';
import { configureAppBridgePrompts } from './prompts.js';

const { version } = createRequire(import.meta.url)('../package.json');

// No recordStartupTelemetry() here: it requires an ADO connection to resolve identity, which
// this package has no concept of.
getAppBridgeConfig();

const server = createMcpServer('app-bridge', version);
configureAppBridgeTools(server);
configureAppBridgePrompts(server);
await startMcpServer(server);

export { configureAppBridgeTools, configureAppBridgePrompts };
