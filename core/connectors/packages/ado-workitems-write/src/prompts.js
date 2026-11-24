import { z } from 'zod';

const generateMessage = (name, args, ctx) => {
  const project = args.project || ctx?.ado?.project;

  switch (name) {
    case 'update-multiple-work-items':
      return `Update multiple work items in batch.\n\nWork Item IDs: ${args.workItemIds}\nUpdate Type: ${args.updateType}\nValue: ${args.value}\n\nUse wit_update_work_items_batch with an updates array where each entry has an id and a patch document setting the appropriate field.`;

    case 'add-work-item-comment':
      return `Add a comment to work item #${args.workItemId}.\n\nComment: ${args.comment}\n\nUse wit_add_work_item_comment with id ${args.workItemId} and text "${args.comment}".`;

    case 'add-child-items':
      return `Add child work items to parent #${args.parentId}.\n\nChild IDs: ${args.childIds}\n\nParse the child IDs as an integer array and use wit_add_child_work_items with parentId ${args.parentId} and childIds [${args.childIds}].`;

    case 'link-related-work-items': {
      const linkTypeLine = args.linkType ? `\nLink Type: ${args.linkType}` : '\nLink Type: System.LinkTypes.Related (default)';
      return `Link two work items together.\n\nSource ID: ${args.sourceId}\nTarget ID: ${args.targetId}${linkTypeLine}\n\nUse wit_work_items_link with sourceId ${args.sourceId}, targetId ${args.targetId}, and linkType "${args.linkType || 'System.LinkTypes.Related'}".`;
    }

    case 'unlink-work-item':
      return `Remove links from work item #${args.workItemId}.\n\nRelation URLs to remove: ${args.relationUrls}\n\nUse wit_work_item_unlink with id ${args.workItemId} and the url of the relation to remove.`;

    case 'link-work-item-to-pr': {
      const resolvedProject = args.projectId || project || '(required)';
      const projectLine = resolvedProject !== '(required)' ? `\nProject: ${resolvedProject}` : '';
      return `Link work item #${args.workItemId} to pull request #${args.pullRequestId}.\n\nRepository: ${args.repositoryId}${projectLine}\n\nUse wit_link_work_item_to_pull_request with workItemId ${args.workItemId}, pullRequestId ${args.pullRequestId}, repositoryId "${args.repositoryId}", and projectId "${resolvedProject}".`;
    }

    case 'update-work-item-comment':
      return `Update the text of comment #${args.commentId} on work item #${args.workItemId}.\n\nProject: ${args.project || project || '(required)'}\nNew text: ${args.text}\n\nUse wit_update_work_item_comment with project "${args.project || project || '(required)'}", id ${args.workItemId}, commentId ${args.commentId}, and text "${args.text}".`;

    case 'update-work-item': {
      return `Update a field on work item #${args.id}.\n\nField: ${args.field}\nValue: ${args.value}\n\nUse wit_update_work_item with id ${args.id} and a patch document: [{ op: "add", path: "/fields/${args.field}", value: "${args.value}" }].`;
    }

    default:
      return `Run the work item write tool for prompt: ${name}`;
  }
};

export function configureWorkItemsWritePrompts(server, { getContext = () => null } = {}) {
  const prompts = [
    {
      name: 'update-multiple-work-items',
      description: 'Update multiple work items in batch',
      args: {
        workItemIds: z.string().describe('Comma-separated work item IDs to update'),
        updateType: z.string().describe('Type of update (e.g. field path like /fields/System.State)'),
        value: z.string().describe('New value to apply to each work item')
      }
    },
    {
      name: 'add-work-item-comment',
      description: 'Add a comment to a work item',
      args: {
        workItemId: z.string().describe('Work item ID'),
        comment: z.string().describe('Comment text to add')
      }
    },
    {
      name: 'add-child-items',
      description: 'Add child work items to a parent',
      args: {
        parentId: z.string().describe('Parent work item ID'),
        childIds: z.string().describe('Comma-separated child work item IDs')
      }
    },
    {
      name: 'link-related-work-items',
      description: 'Link two work items together',
      args: {
        sourceId: z.string().describe('Source work item ID'),
        targetId: z.string().describe('Target work item ID'),
        linkType: z.string().optional().describe('Link type (e.g. System.LinkTypes.Related, System.LinkTypes.Dependency-Forward)')
      }
    },
    {
      name: 'unlink-work-item',
      description: 'Remove links from a work item',
      args: {
        workItemId: z.string().describe('Work item ID to remove links from'),
        relationUrls: z.string().describe('Relation URL(s) to remove (comma-separated)')
      }
    },
    {
      name: 'link-work-item-to-pr',
      description: 'Link a work item to a pull request',
      args: {
        workItemId: z.string().describe('Work item ID'),
        pullRequestId: z.string().describe('Pull request ID'),
        repositoryId: z.string().describe('Repository ID or name'),
        projectId: z.string().optional().describe('Azure DevOps project name or ID')
      }
    },
    {
      name: 'update-work-item-comment',
      description: 'Update the text of an existing work item comment',
      args: {
        project: z.string().optional().describe('Azure DevOps project name or ID'),
        workItemId: z.string().describe('Work item ID'),
        commentId: z.string().describe('Comment ID to update'),
        text: z.string().describe('New comment text')
      }
    },
    {
      name: 'update-work-item',
      description: 'Update a field on a work item',
      args: {
        id: z.string().describe('Work item ID'),
        field: z.string().describe('Field path (e.g. System.State, System.AssignedTo)'),
        value: z.string().describe('New field value')
      }
    }
  ];

  for (const prompt of prompts) {
    server.prompt(prompt.name, prompt.description, prompt.args, async (args) => {
      const ctx = getContext();
      return { messages: [{ role: 'user', content: { type: 'text', text: generateMessage(prompt.name, args ?? {}, ctx) } }] };
    });
  }

  console.error(`Registered ${prompts.length} work item write prompts`);
}
