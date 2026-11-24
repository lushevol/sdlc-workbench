import { configureScanTools } from './tools/scan.js';
import { configureFixTools } from './tools/fix-vulnerabilities.js';

/**
 * Configure all Nexus IQ tools on the MCP server.
 * Registers: nexus_scan_vulnerabilities, nexus_fix_vulnerabilities
 * @param {Object} server - MCP server instance
 * @param {Function} nexusConnectionProvider - Returns a Nexus connection object { baseUrl, headers }
 */
export function configureNexusTools(server, nexusConnectionProvider) {
  configureScanTools(server, nexusConnectionProvider);
  configureFixTools(server);
  console.error('Nexus IQ tools registered successfully');
}
