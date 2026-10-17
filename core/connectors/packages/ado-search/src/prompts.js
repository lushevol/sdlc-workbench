import { z } from 'zod';

export function configureSearchPrompts(server, { getContext = () => null } = {}) {
  const prompts = [
    {
      name: 'search-code',
      description: 'Search code across Azure DevOps repositories',
      args: {
        searchText: z.string().describe('Text or code pattern to search for'),
        project: z.string().optional().describe('Limit search to a specific project'),
        repository: z.string().optional().describe('Limit search to a specific repository'),
        branch: z.string().optional().describe('Limit search to a specific branch')
      }
    },
    {
      name: 'search-work-item',
      description: 'Search Azure DevOps work items by text',
      args: {
        searchText: z.string().describe('Text to search in work item titles, descriptions, and comments'),
        project: z.string().optional().describe('Limit search to a specific project'),
        workItemType: z.string().optional().describe('Filter by work item type, e.g. Bug, Task'),
        state: z.string().optional().describe('Filter by state, e.g. Active, Closed')
      }
    }
  ];

  const messages = {
    'search-code': (args, ctx) => {
      const project = args.project || ctx?.ado?.project;
      const filters = [
        project ? 'project: ' + project : null,
        args.repository ? 'repository: ' + args.repository : null,
        args.branch ? 'branch: ' + args.branch : null
      ].filter(Boolean).join(', ');
      const filterLine = filters ? ' (filters: ' + filters + ')' : '';
      return `Search for code matching "${args.searchText}"${filterLine}.\n\nUse search_code with searchText "${args.searchText}"${project ? ', project "' + project + '"' : ''}${args.repository ? ', repository "' + args.repository + '"' : ''}${args.branch ? ', branch "' + args.branch + '"' : ''}.`;
    },
    'search-work-item': (args, ctx) => {
      const project = args.project || ctx?.ado?.project;
      const filters = [
        project ? 'project: ' + project : null,
        args.workItemType ? 'type: ' + args.workItemType : null,
        args.state ? 'state: ' + args.state : null
      ].filter(Boolean).join(', ');
      const filterLine = filters ? ' (filters: ' + filters + ')' : '';
      return `Search work items for "${args.searchText}"${filterLine}.\n\nUse search_workitem with searchText "${args.searchText}"${project ? ', project "' + project + '"' : ''}${args.workItemType ? ', workItemType "' + args.workItemType + '"' : ''}${args.state ? ', state "' + args.state + '"' : ''}.`;
    }
  };

  for (const prompt of prompts) {
    const callback = async (args) => {
      const ctx = getContext();
      const text = messages[prompt.name](args ?? {}, ctx);
      return { messages: [{ role: 'user', content: { type: 'text', text } }] };
    };
    server.prompt(prompt.name, prompt.description, prompt.args, callback);
  }
}
