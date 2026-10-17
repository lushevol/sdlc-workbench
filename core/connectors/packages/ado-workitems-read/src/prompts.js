import { z } from 'zod';

const generateMessage = (name, args, ctx) => {
  const project = args.project || ctx?.ado?.project;
  const team = args.team || ctx?.ado?.team;

  switch (name) {
    case 'create-work-item': {
      const descLine = args.description ? `\nDescription: ${args.description}` : '';
      return `Create a new work item in Azure DevOps.\n\nProject: ${project || '(required)'}\nType: ${args.type}\nTitle: ${args.title}${descLine}\n\nUse wit_create_work_item with a JSON patch document to set [System.Title], [System.Description], and any other fields.`;
    }

    case 'my-work':
      return `Show all work items currently assigned to me.\n\nUse wit_my_work_items to retrieve work items assigned to the current user, ordered by most recently changed.`;

    case 'run-work-item-query':
      return `Execute the saved work item query and return results.\n\nProject: ${project || '(required)'}\nQuery ID: ${args.queryId}\n\nUse wit_get_query_results_by_id with project "${project || args.project}" and queryId "${args.queryId}".`;

    case 'find-work-items-by-iteration':
      return `Find all work items in a specific iteration/sprint.\n\nProject: ${project || '(required)'}\nTeam: ${team || '(required)'}\nIteration: ${args.iteration}\n\nUse wit_get_work_items_for_iteration with project, team, and iterationPath "${args.iteration}".`;

    case 'view-work-item-comments':
      return `View all comments on work item #${args.workItemId}.\n\nUse wit_list_work_item_comments with id ${args.workItemId}.`;

    case 'list-work-item-pull-requests':
      return `List all pull requests linked to work item #${args.workItemId}.\n\nUse wit_list_work_item_pull_requests with id ${args.workItemId}.`;

    case 'list-work-item-commits':
      return `List all commits linked to work item #${args.workItemId}.\n\nUse wit_list_work_item_commits with id ${args.workItemId}.`;

    case 'get-multiple-work-items':
      return `Get details for multiple work items.\n\nWork Item IDs: ${args.workItemIds}\n\nParse the IDs as an integer array and use wit_get_work_items_batch_by_ids with ids [${args.workItemIds}].`;

    case 'list-work-item-revisions': {
      const topPart = args.top ? ` and top ${args.top}` : '';
      return `List the revision history of work item #${args.workItemId}.\n\nUse wit_list_work_item_revisions with id ${args.workItemId}${topPart}.`;
    }

    case 'get-work-item-attachment':
      return `Download the attachment with ID "${args.attachmentId}" from the work item and return its content as base64.\n\nProject: ${project || '(required)'}\n\nUse wit_get_work_item_attachment with project "${project || args.project}" and attachmentId "${args.attachmentId}".`;

    case 'get-work-item':
      return `Get full details of work item #${args.id}.\n\nUse wit_get_work_item with id ${args.id}.`;

    case 'get-work-item-type':
      return `Get the schema and field definitions for work item type "${args.type}".\n\nProject: ${project || '(required)'}\n\nUse wit_get_work_item_type with project "${project || args.project}" and type "${args.type}".`;

    case 'get-query':
      return `Get metadata for the saved work item query without executing it.\n\nProject: ${project || '(required)'}\nQuery ID: ${args.queryId}\n\nUse wit_get_query with project "${project || args.project}" and queryId "${args.queryId}".`;

    case 'view-backlog': {
      const backlogLevelLine = args.backlogLevel ? `\nBacklog Level: ${args.backlogLevel}` : '';
      return `View team backlog items.\n\nProject: ${project || '(required)'}\nTeam: ${team || '(required)'}${backlogLevelLine}\n\nFirst use wit_list_backlogs to get available backlog levels, then use wit_list_backlog_work_items with the desired backlogId.`;
    }

    case 'list-all-projects':
      return `List all projects in the Azure DevOps organization:\n\nInclude:\n- Project name and ID\n- Project state\n- Description\n- Last update date`;

    case 'list-project-teams':
      return `List all teams in project "${project}":\n\nInclude:\n- Team name and ID\n- Team description\n- Number of members`;

    case 'get-work-item-links':
      return `Get parent, child, and related work items linked to work item #${args.id}.\n\nUse wit_get_work_item_links with id ${args.id}.`;

    case 'query-by-url': {
      const queryDetails = args.url ? `Query URL: ${args.url}` : `Project: ${project || '(required)'}\nQuery ID: ${args.queryId}`;
      const queryToolArgs = args.url ? `url "${args.url}"` : `project "${project || args.project}" and queryId "${args.queryId}"`;
      return `Get work items from a saved Azure DevOps query.\n\n${queryDetails}\n\nUse wit_query_by_url with ${queryToolArgs}.`;
    }

    case 'get-dashboard-work-items': {
      const dashboardDetails = args.url ? `Dashboard URL: ${args.url}` : `Project: ${project || '(required)'}\nDashboard ID: ${args.dashboardId}`;
      const dashboardToolArgs = args.url ? `url "${args.url}"` : `project "${project || args.project}" and dashboardId "${args.dashboardId}"`;
      return `Get work items from query-backed widgets on an Azure DevOps dashboard.\n\n${dashboardDetails}\n\nUse wit_get_dashboard_work_items with ${dashboardToolArgs}.`;
    }

    default:
      return `Run the work item read tool for prompt: ${name}`;
  }
};

export function configureWorkItemsReadPrompts(server, { getContext = () => null } = {}) {
  const prompts = [
    {
      name: 'create-work-item',
      description: 'Create a new work item',
      args: {
        project: z.string().optional().describe('Azure DevOps project name'),
        type: z.string().describe('Work item type (e.g. Task, Bug, User Story)'),
        title: z.string().describe('Work item title'),
        description: z.string().optional().describe('Work item description')
      }
    },
    {
      name: 'my-work',
      description: 'Show work items assigned to me',
      args: null
    },
    {
      name: 'run-work-item-query',
      description: 'Execute a saved work item query',
      args: {
        project: z.string().optional().describe('Azure DevOps project name'),
        queryId: z.string().describe('Query ID or path')
      }
    },
    {
      name: 'find-work-items-by-iteration',
      description: 'Find work items by iteration/sprint',
      args: {
        project: z.string().optional().describe('Azure DevOps project name'),
        team: z.string().optional().describe('Team name'),
        iteration: z.string().describe('Iteration path')
      }
    },
    {
      name: 'view-work-item-comments',
      description: 'View comments on a work item',
      args: {
        workItemId: z.string().describe('Work item ID')
      }
    },
    {
      name: 'list-work-item-pull-requests',
      description: 'List PRs linked to a work item',
      args: {
        project: z.string().optional().describe('Azure DevOps project name'),
        workItemId: z.string().describe('Work item ID')
      }
    },
    {
      name: 'list-work-item-commits',
      description: 'List commits linked to a work item',
      args: {
        project: z.string().optional().describe('Azure DevOps project name'),
        workItemId: z.string().describe('Work item ID')
      }
    },
    {
      name: 'get-multiple-work-items',
      description: 'Get details for multiple work items',
      args: {
        workItemIds: z.string().describe('Comma-separated work item IDs')
      }
    },
    {
      name: 'list-work-item-revisions',
      description: 'List revision history of a work item',
      args: {
        workItemId: z.string().describe('Work item ID'),
        top: z.string().optional().describe('Maximum number of revisions to return')
      }
    },
    {
      name: 'get-work-item-attachment',
      description: 'Download a work item attachment as base64',
      args: {
        project: z.string().optional().describe('Azure DevOps project name'),
        attachmentId: z.string().describe('Attachment GUID (from work item relations of type AttachedFile)')
      }
    },
    {
      name: 'get-work-item',
      description: 'Get full details of a single work item',
      args: {
        id: z.string().describe('Work item ID')
      }
    },
    {
      name: 'get-work-item-type',
      description: 'Get work item type schema and fields',
      args: {
        project: z.string().optional().describe('Azure DevOps project name'),
        type: z.string().describe('Work item type name (e.g. Task, Bug, User Story)')
      }
    },
    {
      name: 'get-query',
      description: 'Get work item query metadata without executing',
      args: {
        project: z.string().optional().describe('Azure DevOps project name'),
        queryId: z.string().describe('Query ID or path')
      }
    },
    {
      name: 'view-backlog',
      description: 'View team backlog items',
      args: {
        project: z.string().optional().describe('Azure DevOps project name'),
        team: z.string().optional().describe('Team name'),
        backlogLevel: z.string().optional().describe('Backlog level (e.g. Microsoft.RequirementCategory)')
      }
    },
    {
      name: 'list-all-projects',
      description: 'List all projects in the Azure DevOps organization',
      args: null
    },
    {
      name: 'list-project-teams',
      description: 'List all teams in a project',
      args: {
        project: z.string().optional().describe('Azure DevOps project name')
      }
    },
    {
      name: 'get-work-item-links',
      description: 'Get parent/child/related work items linked to a work item',
      args: {
        id: z.string().describe('Work item ID')
      }
    },
    {
      name: 'query-by-url',
      description: 'Get work items from a saved query URL or project+queryId',
      args: {
        url: z.string().optional().describe('Full ADO query URL'),
        project: z.string().optional().describe('Azure DevOps project name (if not passing url)'),
        queryId: z.string().optional().describe('Query ID (if not passing url)')
      }
    },
    {
      name: 'get-dashboard-work-items',
      description: 'Get work items from query-backed widgets on a dashboard URL or project+dashboardId',
      args: {
        url: z.string().optional().describe('Full ADO dashboard URL'),
        project: z.string().optional().describe('Azure DevOps project name (if not passing url)'),
        dashboardId: z.string().optional().describe('Dashboard ID (if not passing url)')
      }
    }
  ];

  for (const prompt of prompts) {
    const callback = async (args) => {
      const ctx = getContext();
      return { messages: [{ role: 'user', content: { type: 'text', text: generateMessage(prompt.name, args ?? {}, ctx) } }] };
    };
    if (prompt.args === null) {
      server.prompt(prompt.name, prompt.description, callback);
    } else {
      server.prompt(prompt.name, prompt.description, prompt.args, callback);
    }
  }

  console.error(`Registered ${prompts.length} work item read prompts`);
}
