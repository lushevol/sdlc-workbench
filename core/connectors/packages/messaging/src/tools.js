import { configureSendTools } from './tools/send.js';

/**
 * Configure all email tools
 * @param {Object} server - MCP server instance
 * @param {Function} connectionProvider - Connection provider function (getPythonBridge)
 */
export function configureEmailTools(server, connectionProvider) {
  // Register send tools
  configureSendTools(server, connectionProvider);
  
  console.error('Email tools registered successfully');
}

