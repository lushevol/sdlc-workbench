import { z } from "zod";
import { getConfig } from '@sc-node-mcp/core';

function configureWorkItemsWriteTools(server, getADOConnection) {
  // Add a comment to a work item
  server.tool(
    "wit_add_work_item_comment",
    "Add a comment to a work item.",
    {
      id: z.number().int().positive().describe("Work item ID"),
      text: z.string().describe("Comment text")
    },
    async ({ id, text }) => {
      try {
        const connection = await getADOConnection();
        const witApi = await connection.getWorkItemTrackingApi();

        // Get work item to determine the project
        const workItem = await witApi.getWorkItem(id);
        if (!workItem?.fields?.['System.TeamProject']) {
          return { content: [{ type: "text", text: `Unable to determine project for work item ${id}` }], isError: true };
        }
        const projectName = workItem.fields['System.TeamProject'];

        // API signature: addComment(request, project, workItemId)
        const comment = await witApi.addComment({ text }, projectName, id);
        return { content: [{ type: "text", text: JSON.stringify(comment, null, 2) }] };
      } catch (error) {
        return { content: [{ type: "text", text: error?.message || String(error) }], isError: true };
      }
    }
  );

  // Update a work item
  server.tool(
    "wit_update_work_item",
    "Update a work item by applying a JSON patch document (array of {op, path, value} operations) to the specified work item ID.",
    {
      id: z.number().int().positive().describe("Work item ID"),
      patch: z.array(z.object({ op: z.string(), path: z.string(), value: z.any() })).describe("JSON patch document")
    },
    async ({ id, patch }) => {
      try {
        const connection = await getADOConnection();
        const witApi = await connection.getWorkItemTrackingApi();
        const updated = await witApi.updateWorkItem({}, patch, id);
        return { content: [{ type: "text", text: JSON.stringify(updated, null, 2) }] };
      } catch (error) {
        return { content: [{ type: "text", text: error?.message || String(error) }], isError: true };
      }
    }
  );

  // Create a new work item
  server.tool(
    "wit_create_work_item",
    "Create a new work item of a given type in an Azure DevOps project using a JSON patch document to set fields such as title, description, and area path.",
    {
      project: z.string().describe("Project name"),
      type: z.string().describe("Work item type (e.g. 'Task', 'Bug', 'Story')"),
      patch: z.array(z.object({ op: z.string(), path: z.string(), value: z.any() })).describe("JSON patch document")
    },
    async ({ project, type, patch }) => {
      try {
        const connection = await getADOConnection();
        const witApi = await connection.getWorkItemTrackingApi();
        const created = await witApi.createWorkItem({}, patch, project, type);
        return { content: [{ type: "text", text: JSON.stringify(created, null, 2) }] };
      } catch (error) {
        return { content: [{ type: "text", text: error?.message || String(error) }], isError: true };
      }
    }
  );

  // Add child work items
  server.tool(
    "wit_add_child_work_items",
    "Add child work items to a parent work item.",
    {
      parentId: z.number().int().positive().describe("Parent work item ID"),
      childIds: z.array(z.number().int().positive()).describe("Array of child work item IDs")
    },
    async ({ parentId, childIds }) => {
      try {
        const connection = await getADOConnection();
        const witApi = await connection.getWorkItemTrackingApi();
        const config = getConfig();
        const patch = childIds.map(childId => ({
          op: "add",
          path: "/relations/-",
          value: {
            rel: "System.LinkTypes.Hierarchy-Forward",
            url: `${config.AZURE_DEVOPS_ORG_URL}/_apis/wit/workItems/${childId}`,
            attributes: {
              comment: "Added as child"
            }
          }
        }));
        const updated = await witApi.updateWorkItem({}, patch, parentId);
        return { content: [{ type: "text", text: JSON.stringify(updated, null, 2) }] };
      } catch (error) {
        return { content: [{ type: "text", text: error?.message || String(error) }], isError: true };
      }
    }
  );

  // Link two work items with a specified relation type
  server.tool(
    "wit_work_items_link",
    "Create a link between two work items with a specified relation type.",
    {
      sourceId: z.number().int().positive().describe("Source work item ID"),
      targetId: z.number().int().positive().describe("Target work item ID"),
      linkType: z.string().describe("Link type (e.g., 'System.LinkTypes.Related', 'System.LinkTypes.Dependency-Forward', 'System.LinkTypes.Hierarchy-Forward')"),
      comment: z.string().optional().describe("Optional comment for the link")
    },
    async ({ sourceId, targetId, linkType, comment }) => {
      try {
        const connection = await getADOConnection();
        const witApi = await connection.getWorkItemTrackingApi();
        const config = getConfig();
        const patch = [
          {
            op: "add",
            path: "/relations/-",
            value: {
              rel: linkType,
              url: `${config.AZURE_DEVOPS_ORG_URL}/_apis/wit/workItems/${targetId}`,
              attributes: comment ? { comment } : {}
            }
          }
        ];
        const updated = await witApi.updateWorkItem({}, patch, sourceId);
        return { content: [{ type: "text", text: JSON.stringify(updated, null, 2) }] };
      } catch (error) {
        return { content: [{ type: "text", text: error?.message || String(error) }], isError: true };
      }
    }
  );

  // Update multiple work items in batch
  server.tool(
    "wit_update_work_items_batch",
    "Update multiple work items in batch.",
    {
      updates: z.array(z.object({
        id: z.number().int().positive().describe("Work item ID"),
        patch: z.array(z.object({ op: z.string(), path: z.string(), value: z.any() })).describe("JSON patch document")
      })).describe("Array of work item updates")
    },
    async ({ updates }) => {
      try {
        const connection = await getADOConnection();
        const witApi = await connection.getWorkItemTrackingApi();

        const results = [];
        for (const update of updates) {
          try {
            const result = await witApi.updateWorkItem({}, update.patch, update.id);
            results.push({ id: update.id, success: true, result });
          } catch (error) {
            results.push({ id: update.id, success: false, error: error.message });
          }
        }

        return { content: [{ type: "text", text: JSON.stringify(results, null, 2) }] };
      } catch (error) {
        return { content: [{ type: "text", text: error?.message || String(error) }], isError: true };
      }
    }
  );

  // Remove links from a work item
  server.tool(
    "wit_work_item_unlink",
    "Remove one or more links from a work item by link relation type or URL.",
    {
      project: z.string().describe("Azure DevOps project name or ID"),
      id: z.number().int().positive().describe("Work item ID to remove links from"),
      type: z.string().optional().describe("Link relation type to remove (e.g., 'System.LinkTypes.Related', 'System.LinkTypes.Hierarchy-Forward')"),
      url: z.string().optional().describe("Specific relation URL to remove (remove exact link by URL)")
    },
    async ({ project, id, type, url }) => {
      try {
        const connection = await getADOConnection();
        const witApi = await connection.getWorkItemTrackingApi();
        const workItem = await witApi.getWorkItem(id, undefined, undefined, 1 /* expand relations */);
        if (!workItem?.relations) {
          return { content: [{ type: "text", text: "Work item has no relations to remove." }] };
        }
        const patch = [];
        workItem.relations.forEach((rel, index) => {
          const matchByType = type && rel.rel === type;
          const matchByUrl = url && rel.url === url;
          if (matchByType || matchByUrl) {
            patch.push({ op: "remove", path: `/relations/${index}` });
          }
        });
        if (patch.length === 0) {
          return { content: [{ type: "text", text: "No matching relations found to remove." }] };
        }
        // Apply removals in reverse index order to avoid index shift
        const sortedPatch = patch.toSorted((a, b) => {
          const aIdx = Number.parseInt(a.path.split('/')[2]);
          const bIdx = Number.parseInt(b.path.split('/')[2]);
          return bIdx - aIdx;
        });
        const updated = await witApi.updateWorkItem({}, sortedPatch, id, project);
        return { content: [{ type: "text", text: JSON.stringify(updated, null, 2) }] };
      } catch (error) {
        return { content: [{ type: "text", text: error?.message || String(error) }], isError: true };
      }
    }
  );

  // Link a work item to a pull request
  server.tool(
    "wit_link_work_item_to_pull_request",
    "Explicitly link a work item to an existing pull request using an artifact link.",
    {
      projectId: z.string().describe("Azure DevOps project name or ID"),
      repositoryId: z.string().describe("Repository ID or name"),
      pullRequestId: z.number().int().positive().describe("Pull request ID"),
      workItemId: z.number().int().positive().describe("Work item ID to link")
    },
    async ({ projectId, repositoryId, pullRequestId, workItemId }) => {
      try {
        const connection = await getADOConnection();
        const witApi = await connection.getWorkItemTrackingApi();
        const orgUrl = connection.serverUrl;
        const orgName = orgUrl.split('/').pop();
        // Build the PR artifact URI
        const artifactUri = `vstfs:///Git/PullRequestId/${projectId}%2F${repositoryId}%2F${pullRequestId}`;
        const patch = [{
          op: "add",
          path: "/relations/-",
          value: {
            rel: "ArtifactLink",
            url: artifactUri,
            attributes: { name: "Pull Request", comment: `Linked via MCP tool (org: ${orgName})` }
          }
        }];
        const updated = await witApi.updateWorkItem({}, patch, workItemId, projectId);
        return { content: [{ type: "text", text: JSON.stringify(updated, null, 2) }] };
      } catch (error) {
        return { content: [{ type: "text", text: error?.message || String(error) }], isError: true };
      }
    }
  );

  // Update an existing work item comment
  server.tool(
    "wit_update_work_item_comment",
    "Edit the text of an existing comment on a work item.",
    {
      project: z.string().describe("Azure DevOps project name or ID"),
      id: z.number().int().positive().describe("Work item ID"),
      commentId: z.number().int().positive().describe("Comment ID to update"),
      text: z.string().describe("New text content for the comment")
    },
    async ({ project, id, commentId, text }) => {
      try {
        const connection = await getADOConnection();
        const witApi = await connection.getWorkItemTrackingApi();
        const updated = await witApi.updateComment({ text }, project, id, commentId);
        return { content: [{ type: "text", text: JSON.stringify(updated, null, 2) }] };
      } catch (error) {
        return { content: [{ type: "text", text: error?.message || String(error) }], isError: true };
      }
    }
  );
}

export { configureWorkItemsWriteTools };
