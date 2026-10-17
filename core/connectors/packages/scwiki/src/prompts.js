import { z } from 'zod';

const SCWIKI_PROMPTS = {
  SEARCH_SCWIKI: {
    name: 'search-scwiki',
    description: 'Search SC Wiki pages by keyword',
    arguments: [
      { name: 'query', description: 'Keywords to search for', required: true },
      { name: 'limit', description: 'Max results to return (optional)', required: false }
    ]
  },

  GET_SCWIKI_PAGE: {
    name: 'get-scwiki-page',
    description: 'Get an SC Wiki page by its dotted reference',
    arguments: [
      { name: 'pageReference', description: 'Dotted XWiki page reference, e.g. "Space.PageName"', required: true }
    ]
  },

  FIND_SCWIKI_PAGE: {
    name: 'find-scwiki-page',
    description: 'Find an SC Wiki page from its browser URL',
    arguments: [
      { name: 'pageUrl', description: 'Full SC Wiki page URL', required: true }
    ]
  },

  CREATE_SCWIKI_PAGE: {
    name: 'create-scwiki-page',
    description: 'Create a new SC Wiki page',
    arguments: [
      { name: 'pageReference', description: 'Dotted XWiki page reference for the new page', required: true },
      { name: 'title', description: 'Title for the new page', required: true },
      { name: 'content', description: 'Page content in XWiki syntax (optional)', required: false }
    ]
  },

  UPDATE_SCWIKI_PAGE: {
    name: 'update-scwiki-page',
    description: 'Update the title and/or content of an existing SC Wiki page',
    arguments: [
      { name: 'pageReference', description: 'Dotted XWiki page reference', required: true },
      { name: 'title', description: 'New page title (optional)', required: false },
      { name: 'content', description: 'New page content in XWiki syntax (optional)', required: false }
    ]
  },

  DELETE_SCWIKI_PAGE: {
    name: 'delete-scwiki-page',
    description: 'Delete an SC Wiki page (requires title confirmation)',
    arguments: [
      { name: 'pageReference', description: 'Dotted XWiki page reference to delete', required: true },
      { name: 'title', description: 'Page title for confirmation (must match exactly)', required: true }
    ]
  },

  GET_SCWIKI_PAGE_CHILDREN: {
    name: 'get-scwiki-page-children',
    description: 'List the child pages of an SC Wiki page',
    arguments: [
      { name: 'pageReference', description: 'Parent SC Wiki page reference', required: true },
      { name: 'limit', description: 'Max children to return (optional)', required: false }
    ]
  },

  LIST_SCWIKI_SPACES: {
    name: 'list-scwiki-spaces',
    description: 'List the top-level spaces in SC Wiki',
    arguments: [
      { name: 'limit', description: 'Max spaces to return (optional)', required: false }
    ]
  },

  LIST_MY_SCWIKI_PAGES: {
    name: 'list-my-scwiki-pages',
    description: 'List SC Wiki pages created by the authenticated user',
    arguments: [
      { name: 'limit', description: 'Max pages to return (optional)', required: false }
    ]
  },

  ADD_SCWIKI_COMMENT: {
    name: 'add-scwiki-comment',
    description: 'Add a comment to an SC Wiki page',
    arguments: [
      { name: 'pageReference', description: 'SC Wiki page reference', required: true },
      { name: 'text', description: 'Comment text', required: true }
    ]
  },

  GET_SCWIKI_LABELS: {
    name: 'get-scwiki-labels',
    description: 'Get all tags on an SC Wiki page',
    arguments: [
      { name: 'pageReference', description: 'SC Wiki page reference', required: true }
    ]
  },

  ADD_SCWIKI_LABEL: {
    name: 'add-scwiki-label',
    description: 'Add a tag to an SC Wiki page',
    arguments: [
      { name: 'pageReference', description: 'SC Wiki page reference', required: true },
      { name: 'tag', description: 'Tag name', required: true }
    ]
  },

  GET_SCWIKI_PAGE_HISTORY: {
    name: 'get-scwiki-page-history',
    description: 'Get the version history of an SC Wiki page',
    arguments: [
      { name: 'pageReference', description: 'SC Wiki page reference', required: true },
      { name: 'limit', description: 'Max versions to return (optional)', required: false }
    ]
  },

  LIST_SCWIKI_ATTACHMENTS: {
    name: 'list-scwiki-attachments',
    description: 'List the attachments on an SC Wiki page',
    arguments: [
      { name: 'pageReference', description: 'SC Wiki page reference', required: true }
    ]
  }
};

const SCWIKI_PROMPT_MESSAGE_BUILDERS = {
  'search-scwiki': (args) => `Search SC Wiki using the following keywords:

Query: ${args.query}
${args.limit ? `Limit: ${args.limit}` : ''}

Use the scwiki_search tool. Return page title, reference, and URL for each result.`,

  'get-scwiki-page': (args) => `Get the SC Wiki page at reference "${args.pageReference}".

Use the scwiki_get_page tool. Return:
- Page title and reference
- Version
- Full content
- Page URL`,

  'find-scwiki-page': (args) => `Find the SC Wiki page at this URL:

${args.pageUrl}

Use the scwiki_find_page tool. Return the resolved page reference, title, version, and full content.`,

  'create-scwiki-page': (args) => `Create a new SC Wiki page:

Page Reference: ${args.pageReference}
Title: ${args.title}
${args.content ? `\nContent (XWiki syntax):\n${args.content}` : '\nContent: (empty — create a blank page to be filled in later)'}

Use the scwiki_create_page tool. Return the new page reference, title, version, and URL.`,

  'update-scwiki-page': (args) => `Update the SC Wiki page at reference "${args.pageReference}".

${args.title ? `New Title: ${args.title}\n` : ''}${args.content ? `New Content (XWiki syntax):\n${args.content}` : ''}

Use the scwiki_update_page tool. Return the updated page reference, title, and version.`,

  'delete-scwiki-page': (args) => `Delete the SC Wiki page with the following details:

Page Reference: ${args.pageReference}
Title (confirmation): ${args.title}

Use the scwiki_delete_page tool. The title must match exactly — if there is a mismatch, the deletion will be cancelled. Return the result.`,

  'get-scwiki-page-children': (args) => {
    const limitLine = args.limit ? `\nLimit: ${args.limit}` : '';
    return `List the child pages of SC Wiki page "${args.pageReference}".${limitLine}\n\nUse the scwiki_get_page_children tool. Return the list of child page references, titles, and URLs.`;
  },

  'list-scwiki-spaces': (args) => {
    const limitLine = args.limit ? `\nLimit: ${args.limit}` : '';
    return `List all SC Wiki spaces.${limitLine}\n\nUse the scwiki_list_spaces tool. Return the space name and URL for each space.`;
  },

  'list-my-scwiki-pages': (args) => {
    const limitLine = args.limit ? `\nLimit: ${args.limit}` : '';
    return `List my recent SC Wiki pages.${limitLine}\n\nUse the scwiki_list_my_pages tool. Return page title, reference, and last modified date.`;
  },

  'add-scwiki-comment': (args) => `Add a comment to SC Wiki page "${args.pageReference}".

Comment Text:
${args.text}

Use the scwiki_add_comment tool. Return the result.`,

  'get-scwiki-labels': (args) => `Get all tags on SC Wiki page "${args.pageReference}".

Use the scwiki_get_labels tool. Return the list of tag names.`,

  'add-scwiki-label': (args) => `Add the tag "${args.tag}" to SC Wiki page "${args.pageReference}".

Use the scwiki_add_label tool. Return the updated tags list.`,

  'get-scwiki-page-history': (args) => {
    const limitLine = args.limit ? `\nLimit: ${args.limit}` : '';
    return `Get the version history of SC Wiki page "${args.pageReference}".${limitLine}\n\nUse the scwiki_get_page_history tool. Return the list of versions with author and date.`;
  },

  'list-scwiki-attachments': (args) => `List the attachments on SC Wiki page "${args.pageReference}".

Use the scwiki_list_attachments tool. Return name, size, and MIME type for each attachment.`
};

const generateScwikiPromptMessage = (name, args) => {
  const builder = SCWIKI_PROMPT_MESSAGE_BUILDERS[name];
  return builder ? builder(args) : 'Unknown prompt';
};

export function configureScwikiPrompts(server) {
  Object.values(SCWIKI_PROMPTS).forEach(prompt => {
    const callback = async (args) => {
      const message = generateScwikiPromptMessage(prompt.name, args ?? {});
      return { messages: [{ role: 'user', content: { type: 'text', text: message } }] };
    };
    if (prompt.arguments.length === 0) {
      server.prompt(prompt.name, prompt.description, callback);
    } else {
      const argsSchema = Object.fromEntries(
        prompt.arguments.map(arg => [
          arg.name,
          arg.required
            ? z.string().describe(arg.description)
            : z.string().optional().describe(arg.description)
        ])
      );
      server.prompt(prompt.name, prompt.description, argsSchema, callback);
    }
  });
  console.error(`Registered ${Object.keys(SCWIKI_PROMPTS).length} SC Wiki prompts`);
}

export { SCWIKI_PROMPTS };
