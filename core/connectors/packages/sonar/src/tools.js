import { configureSonarApiTools } from './tools/sonar.js';

/**
 * Register all SonarQube tools on the MCP server.
 * @param {import('@modelcontextprotocol/sdk/server/mcp.js').McpServer} server
 * @param {() => Object} sonarConnectionProvider
 */
export function configureSonarTools(server, sonarConnectionProvider) {
  configureSonarApiTools(server, sonarConnectionProvider);
  console.error('SonarQube tools registered successfully');
}
