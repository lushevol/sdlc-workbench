import { configureWebSearchTools } from './tools/websearch.js';
import { configureWebCrawlTools } from './tools/webcrawl.js';
import { configureWebCrawlBrowserTools } from './tools/webcrawlbrowser.js';

/**
 * Configure all web tools on the MCP server.
 * Registers: web_search, web_fetch, web_crawl, web_crawl_browser
 * @param {Object} server - MCP server instance
 */
export function configureWebTools(server, proxy) {
  configureWebSearchTools(server, proxy);
  configureWebCrawlTools(server, proxy);
  configureWebCrawlBrowserTools(server, proxy);
  console.error('Web tools registered successfully');
}
