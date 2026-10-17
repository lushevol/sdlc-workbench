/**
 * @author Podder, Arunangshu
 * @bankId 2004018
 */

import { configureSessionTools } from './tools/session.js';
import { configureNavigationTools } from './tools/navigation.js';
import { configureElementTools } from './tools/elements.js';
import { configureInteractionTools } from './tools/interaction.js';
import { configureSelectTools } from './tools/select.js';
import { configureScriptTools } from './tools/script.js';
import { configureMouseKeyboardTools } from './tools/mouseKeyboard.js';
import { configureAlertTools } from './tools/alerts.js';
import { configureCookieTools } from './tools/cookies.js';
import { configureWindowTools } from './tools/windows.js';
import { configureScreenshotTools } from './tools/screenshot.js';
import { configureCodegenTools } from './tools/codegen.js';
import { configureNetworkTools } from './tools/network.js';
import { configureConsoleTools } from './tools/console.js';
import { configureEmulationTools } from './tools/emulation.js';
import { configurePerformanceTools } from './tools/performance.js';

/**
 * Register all app-bridge (Selenium browser automation) tools on the given MCP server.
 * @param {import('@modelcontextprotocol/sdk/server/mcp.js').McpServer} server
 */
export function configureAppBridgeTools(server) {
  configureSessionTools(server);
  configureNavigationTools(server);
  configureElementTools(server);
  configureInteractionTools(server);
  configureSelectTools(server);
  configureScriptTools(server);
  configureMouseKeyboardTools(server);
  configureAlertTools(server);
  configureCookieTools(server);
  configureWindowTools(server);
  configureScreenshotTools(server);
  configureCodegenTools(server);
  configureNetworkTools(server);
  configureConsoleTools(server);
  configureEmulationTools(server);
  configurePerformanceTools(server);
}
