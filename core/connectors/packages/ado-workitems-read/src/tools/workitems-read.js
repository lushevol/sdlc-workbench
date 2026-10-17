import { z } from "zod";

function configureWorkItemsReadTools(server, getADOConnection) {
  // List all projects in the Azure DevOps organization
  server.tool(
    "wit_list_projects",
    "List all projects in the Azure DevOps organization.",
    {},
    async () => {
      try {
        const connection = await getADOConnection();
        const coreApi = await connection.getCoreApi();
        const result = await coreApi.getProjects();
        return { content: [{ type: "text", text: JSON.stringify(result, null, 2) }] };
      } catch (error) {
        return { content: [{ type: "text", text: error?.message || String(error) }], isError: true };
      }
    }
  );

  server.tool(
    "wit_get_work_item",
    "Retrieve details of a specific Azure DevOps work item by its ID.",
    {
      id: z.number().int().positive().describe("ID of the work item to retrieve")
    }, async ({ id }) => {
      try {
        const connection = await getADOConnection();
        const witApi = await connection.getWorkItemTrackingApi();
        const workItem = await witApi.getWorkItem(id);
        if (!workItem) {
          return { content: [{ type: "text", text: `Work item with ID ${id} not found.` }], isError: true };
        }
        return {
          content: [{ type: "text", text: JSON.stringify(workItem, null, 2) }],
        };
      } catch (error) {
        return { content: [{ type: "text", text: error?.message || String(error) }], isError: true };
      }
    }
  );

  // List work items assigned to the current user
  server.tool(
    "wit_my_work_items",
    "List work items assigned to the current user.",
    {
      top: z.number().int().positive().optional().describe("Max number of work items to return")
    },
    async ({ top }) => {
      try {
        const connection = await getADOConnection();
        const witApi = await connection.getWorkItemTrackingApi();
        // Use WIQL to query assigned to me
        const query = {
          query: `SELECT [System.Id] FROM WorkItems WHERE [System.AssignedTo] = @Me ORDER BY [System.ChangedDate] DESC`
        };
        const result = await witApi.queryByWiql(query);
        const ids = result.workItems.map(wi => wi.id).slice(0, top || 20);
        if (!ids.length) return { content: [{ type: "text", text: "No work items found assigned to you." }] };
        const items = await witApi.getWorkItems(ids);
        return { content: [{ type: "text", text: JSON.stringify(items, null, 2) }] };
      } catch (error) {
        return { content: [{ type: "text", text: error?.message || String(error) }], isError: true };
      }
    }
  );

  // Get multiple work items by IDs
  server.tool(
    "wit_get_work_items_batch_by_ids",
    "Get multiple work items by IDs.",
    {
      ids: z.array(z.number().int().positive()).describe("Array of work item IDs")
    },
    async ({ ids }) => {
      try {
        const connection = await getADOConnection();
        const witApi = await connection.getWorkItemTrackingApi();
        const items = await witApi.getWorkItems(ids);
        return { content: [{ type: "text", text: JSON.stringify(items, null, 2) }] };
      } catch (error) {
        return { content: [{ type: "text", text: error?.message || String(error) }], isError: true };
      }
    }
  );

  // List comments for a work item
  server.tool(
    "wit_list_work_item_comments",
    "List comments for a work item.",
    {
      id: z.number().int().positive().describe("Work item ID")
    },
    async ({ id }) => {
      try {
        const connection = await getADOConnection();
        const witApi = await connection.getWorkItemTrackingApi();

        // Get work item to determine the project
        const workItem = await witApi.getWorkItem(id);
        if (!workItem?.fields?.['System.TeamProject']) {
          return { content: [{ type: "text", text: `Unable to determine project for work item ${id}` }], isError: true };
        }
        const projectName = workItem.fields['System.TeamProject'];

        // API signature: getComments(project, workItemId, top?, continuationToken?, ...)
        const comments = await witApi.getComments(projectName, id);
        return { content: [{ type: "text", text: JSON.stringify(comments, null, 2) }] };
      } catch (error) {
        return { content: [{ type: "text", text: error?.message || String(error) }], isError: true };
      }
    }
  );

  // Get work item type details
  server.tool(
    "wit_get_work_item_type",
    "Get field definitions and metadata for a specific work item type (e.g., Bug, Task, User Story) in an Azure DevOps project.",
    {
      project: z.string().describe("Azure DevOps project name"),
      type: z.string().describe("Work item type name (e.g., 'Task', 'Bug', 'User Story')")
    },
    async ({ project, type }) => {
      try {
        const connection = await getADOConnection();
        const witApi = await connection.getWorkItemTrackingApi();
        const workItemType = await witApi.getWorkItemType(project, type);
        return { content: [{ type: "text", text: JSON.stringify(workItemType, null, 2) }] };
      } catch (error) {
        return { content: [{ type: "text", text: error?.message || String(error) }], isError: true };
      }
    }
  );

  // List available backlogs
  server.tool(
    "wit_list_backlogs",
    "List all backlog levels (e.g., Epics, Features, Stories) available to a specific team in an Azure DevOps project.",
    {
      project: z.string().describe("Azure DevOps project name"),
      team: z.string().describe("Team name")
    },
    async ({ project, team }) => {
      try {
        const connection = await getADOConnection();
        const workApi = await connection.getWorkApi();
        const backlogs = await workApi.getBacklogs({ project, team });
        return { content: [{ type: "text", text: JSON.stringify(backlogs, null, 2) }] };
      } catch (error) {
        return { content: [{ type: "text", text: error?.message || String(error) }], isError: true };
      }
    }
  );

  // List work items in a specific backlog
  server.tool(
    "wit_list_backlog_work_items",
    "List all work items in a named team backlog level (identified by backlogId, e.g. 'Microsoft.RequirementCategory') in an Azure DevOps project.",
    {
      project: z.string().describe("Azure DevOps project name"),
      team: z.string().describe("Team name"),
      backlogId: z.string().describe("Backlog ID (e.g., 'Microsoft.RequirementCategory', 'Microsoft.FeatureCategory')")
    },
    async ({ project, team, backlogId }) => {
      try {
        const connection = await getADOConnection();
        const workApi = await connection.getWorkApi();
        const backlog = await workApi.getBacklogLevelWorkItems({ project, team }, backlogId);
        return { content: [{ type: "text", text: JSON.stringify(backlog, null, 2) }] };
      } catch (error) {
        return { content: [{ type: "text", text: error?.message || String(error) }], isError: true };
      }
    }
  );

  // List teams for a project
  server.tool(
    "wit_list_teams",
    "List all teams in an Azure DevOps project.",
    {
      project: z.string().describe("Azure DevOps project name")
    },
    async ({ project }) => {
      try {
        const connection = await getADOConnection();
        const coreApi = await connection.getCoreApi();
        const teams = await coreApi.getTeams(project);
        return { content: [{ type: "text", text: JSON.stringify(teams, null, 2) }] };
      } catch (error) {
        return { content: [{ type: "text", text: error?.message || String(error) }], isError: true };
      }
    }
  );

  // List iterations for a project and team
  server.tool(
    "wit_list_iterations",
    "List all iterations for a project and team.",
    {
      project: z.string().describe("Azure DevOps project name"),
      team: z.string().describe("Team name")
    },
    async ({ project, team }) => {
      try {
        const connection = await getADOConnection();
        const workApi = await connection.getWorkApi();
        const iterations = await workApi.getTeamIterations({ project, team });
        return { content: [{ type: "text", text: JSON.stringify(iterations, null, 2) }] };
      } catch (error) {
        return { content: [{ type: "text", text: error?.message || String(error) }], isError: true };
      }
    }
  );

  // Get work items for an iteration
  server.tool(
    "wit_get_work_items_for_iteration",
    "Get work items for a specific iteration.",
    {
      project: z.string().describe("Azure DevOps project name"),
      team: z.string().describe("Team name"),
      iterationPath: z.string().describe("Iteration path")
    },
    async ({ project, team, iterationPath }) => {
      try {
        const connection = await getADOConnection();
        const witApi = await connection.getWorkItemTrackingApi();

        // Escape single quotes to prevent SQL injection
        const escapedPath = iterationPath.replaceAll("'", "''");

        const query = {
          query: `SELECT [System.Id], [System.Title], [System.State], [System.AssignedTo] FROM WorkItems WHERE [System.IterationPath] = '${escapedPath}' ORDER BY [System.ChangedDate] DESC`
        };

        const result = await witApi.queryByWiql(query, { project, team });
        const ids = result.workItems.map(wi => wi.id);

        if (!ids.length) {
          return { content: [{ type: "text", text: "No work items found for this iteration." }] };
        }

        const items = await witApi.getWorkItems(ids);
        return { content: [{ type: "text", text: JSON.stringify(items, null, 2) }] };
      } catch (error) {
        return { content: [{ type: "text", text: error?.message || String(error) }], isError: true };
      }
    }
  );

  // Get a query by ID
  server.tool(
    "wit_get_query",
    "Get a work item query by ID.",
    {
      project: z.string().describe("Azure DevOps project name"),
      queryId: z.string().describe("Query ID")
    },
    async ({ project, queryId }) => {
      try {
        const connection = await getADOConnection();
        const witApi = await connection.getWorkItemTrackingApi();
        const query = await witApi.getQuery(project, queryId);
        return { content: [{ type: "text", text: JSON.stringify(query, null, 2) }] };
      } catch (error) {
        return { content: [{ type: "text", text: error?.message || String(error) }], isError: true };
      }
    }
  );

  // Get query results by ID
  server.tool(
    "wit_get_query_results_by_id",
    "Execute a query and get results by query ID.",
    {
      project: z.string().describe("Azure DevOps project name"),
      queryId: z.string().describe("Query ID"),
      top: z.number().int().positive().optional().describe("Max number of results to return")
    },
    async ({ project, queryId, top }) => {
      try {
        const connection = await getADOConnection();
        const witApi = await connection.getWorkItemTrackingApi();

        const result = await witApi.queryById(queryId, { project });
        const ids = result.workItems.map(wi => wi.id).slice(0, top || 100);

        if (!ids.length) {
          return { content: [{ type: "text", text: "No work items found for this query." }] };
        }

        const items = await witApi.getWorkItems(ids);
        return { content: [{ type: "text", text: JSON.stringify(items, null, 2) }] };
      } catch (error) {
        return { content: [{ type: "text", text: error?.message || String(error) }], isError: true };
      }
    }
  );

  // List pull requests associated with a work item
  server.tool(
    "wit_list_work_item_pull_requests",
    "List all pull requests linked to a work item.",
    {
      id: z.number().int().positive().describe("Work item ID")
    },
    async ({ id }) => {
      try {
        const connection = await getADOConnection();
        const witApi = await connection.getWorkItemTrackingApi();

        // Get work item with relations
        const workItem = await witApi.getWorkItem(id, undefined, undefined, 1 /* expand relations */);

        if (!workItem?.relations) {
          return { content: [{ type: "text", text: "No pull requests found linked to this work item." }] };
        }

        // Filter for artifact links that are pull requests
        const prLinks = workItem.relations.filter(rel =>
          rel.rel === "ArtifactLink" &&
          rel.url &&
          (rel.url.includes("PullRequestId") || rel.attributes?.name === "Pull Request")
        );

        if (prLinks.length === 0) {
          return { content: [{ type: "text", text: "No pull requests found linked to this work item." }] };
        }

        return { content: [{ type: "text", text: JSON.stringify(prLinks, null, 2) }] };
      } catch (error) {
        return { content: [{ type: "text", text: error?.message || String(error) }], isError: true };
      }
    }
  );

  // List commits associated with a work item
  server.tool(
    "wit_list_work_item_commits",
    "List all commits linked to a work item.",
    {
      id: z.number().int().positive().describe("Work item ID")
    },
    async ({ id }) => {
      try {
        const connection = await getADOConnection();
        const witApi = await connection.getWorkItemTrackingApi();

        // Get work item with relations
        const workItem = await witApi.getWorkItem(id, undefined, undefined, 1 /* expand relations */);

        if (!workItem?.relations) {
          return { content: [{ type: "text", text: "No commits found linked to this work item." }] };
        }

        // Filter for artifact links that are commits
        const commitLinks = workItem.relations.filter(rel =>
          rel.rel === "ArtifactLink" &&
          rel.url &&
          (rel.url.includes("Commit") || rel.attributes?.name === "Commit")
        );

        if (commitLinks.length === 0) {
          return { content: [{ type: "text", text: "No commits found linked to this work item." }] };
        }

        return { content: [{ type: "text", text: JSON.stringify(commitLinks, null, 2) }] };
      } catch (error) {
        return { content: [{ type: "text", text: error?.message || String(error) }], isError: true };
      }
    }
  );

  // List work item revision history
  server.tool(
    "wit_list_work_item_revisions",
    "Get the full revision/change history of a work item.",
    {
      project: z.string().describe("Azure DevOps project name or ID"),
      id: z.number().int().positive().describe("Work item ID"),
      top: z.number().int().positive().optional().describe("Maximum number of revisions to return"),
      skip: z.number().int().nonnegative().optional().describe("Number of revisions to skip")
    },
    async ({ project, id, top, skip }) => {
      try {
        const connection = await getADOConnection();
        const witApi = await connection.getWorkItemTrackingApi();
        const revisions = await witApi.getRevisions(id, top, skip, 1 /* expand all */);
        return { content: [{ type: "text", text: JSON.stringify(revisions, null, 2) }] };
      } catch (error) {
        return { content: [{ type: "text", text: error?.message || String(error) }], isError: true };
      }
    }
  );

  // Download a work item attachment
  server.tool(
    "wit_get_work_item_attachment",
    "Download a work item attachment by its ID and return the content as base64. Useful for viewing images or files attached to bugs.",
    {
      project: z.string().describe("Azure DevOps project name or ID"),
      attachmentId: z.string().describe("Attachment GUID (from work item relations of type AttachedFile)"),
      fileName: z.string().optional().describe("Expected file name (for display purposes)")
    },
    async ({ project, attachmentId, fileName }) => {
      try {
        const connection = await getADOConnection();
        const witApi = await connection.getWorkItemTrackingApi();
        const stream = await witApi.getAttachmentContent(attachmentId, fileName, project);
        const chunks = [];
        for await (const chunk of stream) {
          chunks.push(chunk);
        }
        const base64 = Buffer.concat(chunks).toString('base64');
        return { content: [{ type: "text", text: JSON.stringify({ attachmentId, fileName, base64Content: base64 }, null, 2) }] };
      } catch (error) {
        return { content: [{ type: "text", text: error?.message || String(error) }], isError: true };
      }
    }
  );

  // Get parent/child/related work items linked to a work item
  server.tool(
    "wit_get_work_item_links",
    "Get work items linked to a given work item, grouped by relation type (parent, child, related).",
    {
      id: z.number().int().positive().describe("Work item ID")
    },
    async ({ id }) => {
      try {
        const connection = await getADOConnection();
        const witApi = await connection.getWorkItemTrackingApi();
        const workItem = await witApi.getWorkItem(id, undefined, undefined, 1 /* WorkItemExpand.Relations */);
        const relations = workItem?.relations || [];

        const RELATION_GROUPS = {
          "System.LinkTypes.Hierarchy-Reverse": "parent",
          "System.LinkTypes.Hierarchy-Forward": "child",
          "System.LinkTypes.Related": "related"
        };

        const groups = { parent: [], child: [], related: [] };
        const idToGroup = new Map();
        for (const rel of relations) {
          const group = RELATION_GROUPS[rel.rel];
          if (!group) continue;
          const match = rel.url?.match(/workItems\/(\d+)$/);
          if (!match) continue;
          idToGroup.set(Number(match[1]), group);
        }

        if (idToGroup.size === 0) {
          return { content: [{ type: "text", text: `No parent/child/related links found for work item ${id}.` }] };
        }

        const linkedItems = await witApi.getWorkItems([...idToGroup.keys()]);
        for (const item of linkedItems) groups[idToGroup.get(item.id)].push(item);

        return { content: [{ type: "text", text: JSON.stringify(groups, null, 2) }] };
      } catch (error) {
        return { content: [{ type: "text", text: error?.message || String(error) }], isError: true };
      }
    }
  );

  // Get work items from a saved query, given its URL or project+queryId
  server.tool(
    "wit_query_by_url",
    "Get work items from a saved Azure DevOps query, given its URL or project+queryId.",
    {
      url: z.string().optional().describe("Full ADO query URL, e.g. https://dev.azure.com/org/Project/_queries/query/{queryId}"),
      project: z.string().optional().describe("Project name (if not passing url)"),
      queryId: z.string().optional().describe("Query ID (if not passing url)"),
      top: z.number().int().positive().optional().describe("Max number of work items to return")
    },
    async ({ url, project, queryId, top }) => {
      try {
        let resolvedProject = project;
        let resolvedQueryId = queryId;

        if (url) {
          const match = url.match(/\/([^/]+)\/_queries\/query(?:-edit)?\/([0-9a-fA-F-]{36})/);
          if (!match) {
            return {
              content: [{ type: "text", text: "This URL is not a query link. Dashboard links are not supported by this tool — use wit_get_dashboard_work_items instead." }],
              isError: true
            };
          }
          [, resolvedProject, resolvedQueryId] = match;
        }

        if (!resolvedProject || !resolvedQueryId) {
          return { content: [{ type: "text", text: "Provide either 'url' or both 'project' and 'queryId'." }], isError: true };
        }

        const connection = await getADOConnection();
        const witApi = await connection.getWorkItemTrackingApi();
        const result = await witApi.queryById(resolvedQueryId, { project: resolvedProject });
        const ids = (result?.workItems || []).map(wi => wi.id).slice(0, top || 200);

        if (!ids.length) {
          return { content: [{ type: "text", text: "No work items found for this query." }] };
        }

        const items = await witApi.getWorkItems(ids);
        return { content: [{ type: "text", text: JSON.stringify(items, null, 2) }] };
      } catch (error) {
        return { content: [{ type: "text", text: error?.message || String(error) }], isError: true };
      }
    }
  );

  // Get work items from query-backed widgets on a dashboard, given its URL or project+dashboardId
  server.tool(
    "wit_get_dashboard_work_items",
    "Get work items from all query-backed widgets on an Azure DevOps dashboard, given its URL or project+dashboardId.",
    {
      url: z.string().optional().describe("Full ADO dashboard URL, e.g. https://dev.azure.com/org/Project/_dashboards/dashboard/{dashboardId}"),
      project: z.string().optional().describe("Project name (if not passing url)"),
      dashboardId: z.string().optional().describe("Dashboard ID (if not passing url)"),
      team: z.string().optional().describe("Team name (optional, for team-scoped dashboards)")
    },
    async ({ url, project, dashboardId, team }) => {
      try {
        let resolvedProject = project;
        let resolvedTeam = team;
        let resolvedDashboardId = dashboardId;

        if (url) {
          const match = url.match(/dev\.azure\.com\/[^/]+\/([^/]+)\/(?:([^/]+)\/)?_dashboards\/dashboard\/([0-9a-fA-F-]{36})/);
          if (!match) {
            return { content: [{ type: "text", text: "This URL is not a dashboard link." }], isError: true };
          }
          [, resolvedProject, resolvedTeam, resolvedDashboardId] = match;
          resolvedTeam = resolvedTeam || team;
        }

        if (!resolvedProject || !resolvedDashboardId) {
          return { content: [{ type: "text", text: "Provide either 'url' or both 'project' and 'dashboardId'." }], isError: true };
        }

        const connection = await getADOConnection();
        const dashboardApi = await connection.getDashboardApi();
        const witApi = await connection.getWorkItemTrackingApi();
        const dashboard = await dashboardApi.getDashboard({ project: resolvedProject, team: resolvedTeam }, resolvedDashboardId);

        const results = [];
        for (const widget of dashboard?.widgets || []) {
          let settings;
          try {
            settings = JSON.parse(widget.settings || "{}");
          } catch {
            continue; // not a JSON settings blob, skip
          }
          const widgetQueryId = settings.queryId || settings.savedQueryId;
          if (!widgetQueryId) continue;

          const queryResult = await witApi.queryById(widgetQueryId, { project: resolvedProject });
          const ids = (queryResult?.workItems || []).map(wi => wi.id);
          const items = ids.length ? await witApi.getWorkItems(ids) : [];
          results.push({ widgetName: widget.name, widgetType: widget.contributionId, queryId: widgetQueryId, items });
        }

        if (!results.length) {
          return { content: [{ type: "text", text: "No query-backed widgets found on this dashboard." }] };
        }

        return { content: [{ type: "text", text: JSON.stringify(results, null, 2) }] };
      } catch (error) {
        return { content: [{ type: "text", text: error?.message || String(error) }], isError: true };
      }
    }
  );
}

export { configureWorkItemsReadTools };
