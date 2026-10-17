import { z } from 'zod';

function configureSearchTools(server, getADOConnection) {

  // Search code across ADO repositories
  server.tool(
    'search_code',
    'Search for code text across Azure DevOps repositories. Supports filtering by project, repository, branch, and file path.',
    {
      searchText: z.string().describe('Text to search for in code'),
      project: z.string().optional().describe('Limit search to a specific project'),
      repository: z.string().optional().describe('Limit search to a specific repository name'),
      branch: z.string().optional().describe('Limit search to a specific branch (e.g., "main")'),
      path: z.string().optional().describe('Limit search to a specific file path prefix (e.g., "/src")'),
      top: z.number().int().positive().optional().default(25).describe('Maximum number of results to return (default 25)'),
      skip: z.number().int().nonnegative().optional().describe('Number of results to skip for pagination')
    },
    async ({ searchText, project, repository, branch, path, top, skip }) => {
      try {
        const connection = await getADOConnection();
        const orgUrl = connection.serverUrl;
        const orgName = orgUrl.split('/').pop();

        const filters = {};
        if (project) filters.Project = [project];
        if (repository) filters.Repository = [repository];
        if (branch) filters.Branch = [branch];
        if (path) filters.Path = [path];

        const body = {
          searchText,
          $skip: skip || 0,
          $top: top || 25,
          filters: Object.keys(filters).length > 0 ? filters : undefined,
          includeFacets: false
        };

        const searchUrl = `https://almsearch.dev.azure.com/${orgName}/_apis/search/codesearchresults?api-version=7.0`;
        const response = await connection.rest.create(searchUrl, body);
        return { content: [{ type: 'text', text: JSON.stringify(response.result, null, 2) }] };
      } catch (error) {
        return { content: [{ type: 'text', text: error?.message || String(error) }], isError: true };
      }
    }
  );

  // Search work items by text
  server.tool(
    'search_workitem',
    'Search Azure DevOps work items by free text with optional filters for project, type, state, and assignee.',
    {
      searchText: z.string().describe('Text to search for in work items (title, description, comments)'),
      project: z.string().optional().describe('Limit search to a specific project'),
      workItemType: z.string().optional().describe('Filter by work item type (e.g., "Bug", "Task", "User Story")'),
      state: z.string().optional().describe('Filter by work item state (e.g., "Active", "Closed")'),
      assignedTo: z.string().optional().describe('Filter by assignee display name or email'),
      areaPath: z.string().optional().describe('Filter by area path'),
      top: z.number().int().positive().optional().default(25).describe('Maximum number of results to return (default 25)'),
      skip: z.number().int().nonnegative().optional().describe('Number of results to skip for pagination')
    },
    async ({ searchText, project, workItemType, state, assignedTo, areaPath, top, skip }) => {
      try {
        const connection = await getADOConnection();
        const orgUrl = connection.serverUrl;
        const orgName = orgUrl.split('/').pop();

        const filters = {};
        if (project) filters.Project = [project];
        if (workItemType) filters['Work Item Types'] = [workItemType];
        if (state) filters['States'] = [state];
        if (assignedTo) filters['Assigned To'] = [assignedTo];
        if (areaPath) filters['Area Paths'] = [areaPath];

        const body = {
          searchText,
          $skip: skip || 0,
          $top: top || 25,
          filters: Object.keys(filters).length > 0 ? filters : undefined,
          includeFacets: false
        };

        const searchUrl = `https://almsearch.dev.azure.com/${orgName}/_apis/search/workitemsearchresults?api-version=7.0`;
        const response = await connection.rest.create(searchUrl, body);
        return { content: [{ type: 'text', text: JSON.stringify(response.result, null, 2) }] };
      } catch (error) {
        return { content: [{ type: 'text', text: error?.message || String(error) }], isError: true };
      }
    }
  );
}

export { configureSearchTools };
