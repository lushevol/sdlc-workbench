import { configureWorkItemsReadTools } from '@sc-node-mcp/ado-workitems-read/tools';
import { configureWorkItemsWriteTools } from '@sc-node-mcp/ado-workitems-write/tools';
import { configureReposReadTools } from '@sc-node-mcp/ado-repos-read/tools';
import { configureReposWriteTools } from '@sc-node-mcp/ado-repos-write/tools';
import { configureReviewTools } from '@sc-node-mcp/ado-review/tools';
import { configurePipelineTools } from '@sc-node-mcp/ado-pipelines/tools';
import { configureTestPlanToolsModule } from '@sc-node-mcp/ado-testplans/tools';
import { configureSprintsTools } from '@sc-node-mcp/ado-sprints/tools';
import { configureSearchTools } from '@sc-node-mcp/ado-search/tools';

/**
 * Configure all ADO tools on the MCP server
 * @param {McpServer} server - MCP server instance
 * @param {Function} connectionProvider - Function that returns Azure DevOps connection
 * @param {Object} [options={}] - Optional configuration passed to individual tools
 * @param {string} [options.codeReviewGuideFile] - Full path to the review guidelines file (e.g. /path/to/CODE_REVIEW_GUIDE.md)
 */
export function configureAdoTools(server, connectionProvider, options = {}) {
  configureWorkItemsReadTools(server, connectionProvider);
  configureWorkItemsWriteTools(server, connectionProvider);
  configureReposReadTools(server, connectionProvider);
  configureReposWriteTools(server, connectionProvider);
  configureReviewTools(server, connectionProvider, options);
  configurePipelineTools(server, connectionProvider);
  configureTestPlanToolsModule(server, connectionProvider);
  configureSprintsTools(server, connectionProvider);
  configureSearchTools(server, connectionProvider);

  console.error('Registered all Azure DevOps tools');
}
