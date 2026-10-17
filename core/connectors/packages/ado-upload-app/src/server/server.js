#!/usr/bin/env node
import { createRequire } from 'node:module';

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import * as azdev from "azure-devops-node-api";
import { getConfig, recordStartupTelemetry } from "@sc-node-mcp/core";
import { configureUploadTools, configureUiResource } from "../tools.js";

/**
 * Get an authenticated Azure DevOps connection using config from CLI args / env / config.json.
 */
async function getADOConnection() {
  const { AZURE_DEVOPS_ORG_URL, AZURE_DEVOPS_PAT, HTTPS_PROXY } = getConfig();

  if (HTTPS_PROXY) {
    process.env.HTTPS_PROXY = HTTPS_PROXY;
    console.error("Proxy in use for Azure DevOps requests:", process.env.HTTPS_PROXY);
  }

  const authHandler = azdev.getPersonalAccessTokenHandler(AZURE_DEVOPS_PAT);
  return new azdev.WebApi(AZURE_DEVOPS_ORG_URL, authHandler);
}

const config = getConfig();
const { version } = createRequire(import.meta.url)('../../package.json');
recordStartupTelemetry(config, getADOConnection, { versions: { 'ado-upload-app': version } })
  .catch(err => console.error('[Telemetry] Unexpected error:', err.message));

const server = new McpServer({ name: "ado-upload-app", version });

configureUploadTools(server, getADOConnection);
configureUiResource(server);

const transport = new StdioServerTransport();
await server.connect(transport);
console.error("ADO Upload App MCP server running on stdio");
