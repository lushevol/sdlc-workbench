import { z } from 'zod';

const CONFLUENCE_PROMPTS = {
  MY_PAGES: {
    name: 'my-confluence-pages',
    description: 'List my recent Confluence pages',
    arguments: [
      { name: 'spaceKey', description: 'Confluence space key (optional)', required: false }
    ]
  },

  SEARCH_CONFLUENCE: {
    name: 'search-confluence',
    description: 'Search Confluence pages using CQL',
    arguments: [
      { name: 'cql', description: 'CQL query string', required: true },
      { name: 'limit', description: 'Max results to return (optional)', required: false }
    ]
  },

  UPDATE_CONFLUENCE_PAGE: {
    name: 'update-confluence-page',
    description: 'Update the content of a Confluence page',
    arguments: [
      { name: 'pageId', description: 'Confluence page ID (numeric string)', required: true },
      { name: 'body', description: 'New page body in Confluence Storage Format (XHTML)', required: true },
      { name: 'title', description: 'New page title (optional — keeps existing if omitted)', required: false }
    ]
  },

  GET_CONFLUENCE_PAGE_ID: {
    name: 'get-confluence-page-id',
    description: 'Look up a Confluence page ID from its URL',
    arguments: [
      { name: 'pageUrl', description: 'Full Confluence page URL', required: true }
    ]
  },

  READ_CONFLUENCE_PAGE: {
    name: 'read-confluence-page',
    description: 'Read the full content of a Confluence page from its URL',
    arguments: [
      { name: 'pageUrl', description: 'Full Confluence page URL (Cloud or Server-style)', required: true }
    ]
  },

  CREATE_CONFLUENCE_PAGE: {
    name: 'create-confluence-page',
    description: 'Create a new Confluence page under a parent page',
    arguments: [
      { name: 'parentPageUrl', description: 'Full URL of the parent Confluence page', required: true },
      { name: 'title', description: 'Title for the new page', required: true },
      { name: 'body', description: 'Page body in Confluence Storage Format (XHTML). Defaults to empty page if omitted.', required: false }
    ]
  },

  GET_CONFLUENCE_PAGE: {
    name: 'get-confluence-page',
    description: 'Get a Confluence page by its ID',
    arguments: [
      { name: 'pageId', description: 'Confluence page ID (numeric string)', required: true }
    ]
  },

  FIND_CONFLUENCE_PAGE: {
    name: 'find-confluence-page',
    description: 'Find a Confluence page by space key and title',
    arguments: [
      { name: 'spaceKey', description: 'Confluence space key', required: true },
      { name: 'title', description: 'Page title to search for', required: true }
    ]
  },

  GET_CONFLUENCE_PAGE_CHILDREN: {
    name: 'get-confluence-page-children',
    description: 'List the child pages of a Confluence page',
    arguments: [
      { name: 'pageId', description: 'Parent Confluence page ID', required: true },
      { name: 'limit', description: 'Max children to return (optional)', required: false }
    ]
  },

  LIST_CONFLUENCE_SPACES: {
    name: 'list-confluence-spaces',
    description: 'List all Confluence spaces',
    arguments: [
      { name: 'limit', description: 'Max spaces to return (optional)', required: false }
    ]
  },

  GET_CONFLUENCE_SPACE: {
    name: 'get-confluence-space',
    description: 'Get details of a Confluence space',
    arguments: [
      { name: 'spaceKey', description: 'Confluence space key', required: true }
    ]
  },

  DELETE_CONFLUENCE_PAGE: {
    name: 'delete-confluence-page',
    description: 'Delete a Confluence page (requires title confirmation)',
    arguments: [
      { name: 'pageId', description: 'Page ID to delete', required: true },
      { name: 'title', description: 'Page title for confirmation (must match exactly)', required: true }
    ]
  },

  ADD_CONFLUENCE_COMMENT: {
    name: 'add-confluence-comment',
    description: 'Add a page-level comment to a Confluence page',
    arguments: [
      { name: 'pageId', description: 'Confluence page ID', required: true },
      { name: 'body', description: 'Comment body in Confluence Storage Format (XHTML)', required: true }
    ]
  },

  GET_CONFLUENCE_LABELS: {
    name: 'get-confluence-labels',
    description: 'Get all labels on a Confluence page',
    arguments: [
      { name: 'pageId', description: 'Confluence page ID', required: true }
    ]
  },

  ADD_CONFLUENCE_LABEL: {
    name: 'add-confluence-label',
    description: 'Add a label to a Confluence page',
    arguments: [
      { name: 'pageId', description: 'Confluence page ID', required: true },
      { name: 'label', description: 'Label name (lowercase, no spaces)', required: true }
    ]
  }
};

const generateConfluencePromptMessage = (name, args, ctx) => {
  const spaceKey = args.spaceKey || ctx?.confluence?.defaultSpaceKey;
  switch (name) {
    case 'my-confluence-pages': {
      const resolvedSpace = args.spaceKey || spaceKey;
      const spaceClause = resolvedSpace ? ` in space "${resolvedSpace}"` : ' across all spaces';
      return `List my recent Confluence pages${spaceClause}.

Include:
- Page title
- Last modified date
- Space
- Page URL`;
    }

    case 'search-confluence':
      return `Search Confluence using CQL:

Query: ${args.cql}
${args.limit ? `Limit: ${args.limit}` : ''}

Return:
- Page title and ID
- Space and URL
- Last modified date and author`;

    case 'update-confluence-page':
      return `Update Confluence page:

Page ID: ${args.pageId}
${args.title ? `New Title: ${args.title}` : ''}

New Body (Confluence Storage Format):
${args.body}`;

    case 'get-confluence-page-id':
      return `Look up the Confluence page ID for this URL:

${args.pageUrl}

Return the page ID, title, space key, and current version number so I can use them with other Confluence tools.`;

    case 'read-confluence-page':
      return `Read the full content of the following Confluence page:

${args.pageUrl}

Use the confluence_read_page tool to fetch the page. Return:
- Page title and ID
- Space key and current version number
- Full page content (use the view body for readable output)
- Page URL`;

    case 'create-confluence-page':
      return `Create a new Confluence page under the following parent page:

Parent Page URL: ${args.parentPageUrl}
New Page Title: ${args.title}
${args.body ? `\nPage Body (Confluence Storage Format):\n${args.body}` : '\nPage Body: (empty — create a blank page to be filled in later)'}

Use the confluence_create_page tool to create the page. Return the new page ID, title, space, and URL.`;

    case 'get-confluence-page':
      return `Get the full content of the following Confluence page by ID:

Page ID: ${args.pageId}

Use the confluence_get_page tool. Return:
- Page title and ID
- Space key and version number
- Full page content (use the view body for readable output; export_view captures tab content)
- Page URL`;

    case 'find-confluence-page':
      return `Find the Confluence page with the following details:

Space Key: ${args.spaceKey}
Title: ${args.title}

Use the confluence_find_page tool. Return:
- Page ID, title, space, and version
- Page URL`;

    case 'get-confluence-page-children': {
      const limitLine = args.limit ? `\nLimit: ${args.limit}` : '';
      return `List the child pages of Confluence page ID ${args.pageId}.${limitLine}\n\nUse the confluence_get_page_children tool. Return:\n- List of child page IDs, titles, spaces, and URLs`;
    }

    case 'list-confluence-spaces': {
      const limitLine = args.limit ? `\nLimit: ${args.limit}` : '';
      return `List all Confluence spaces.${limitLine}\n\nUse the confluence_list_spaces tool. Return:\n- Space key, name, type, and URL for each space`;
    }

    case 'get-confluence-space':
      return `Get the details of the Confluence space with key "${args.spaceKey}".

Use the confluence_get_space tool. Return:
- Space key, name, and type
- Description
- Homepage page ID
- Space URL`;

    case 'delete-confluence-page':
      return `Delete the Confluence page with the following details:

Page ID: ${args.pageId}
Title (confirmation): ${args.title}

Use the confluence_delete_page tool. The title must match exactly — if there is a mismatch, the deletion will be cancelled. Return the result.`;

    case 'add-confluence-comment':
      return `Add a comment to Confluence page ID ${args.pageId}.

Comment Body (Confluence Storage Format):
${args.body}

Use the confluence_add_comment tool. Return the new comment ID and URL.`;

    case 'get-confluence-labels':
      return `Get all labels on Confluence page ID ${args.pageId}.

Use the confluence_get_labels tool. Return the list of label names.`;

    case 'add-confluence-label':
      return `Add the label "${args.label}" to Confluence page ID ${args.pageId}.

Use the confluence_add_label tool. Return the updated labels list.`;

    default:
      return 'Unknown prompt';
  }
};

const CONTEXTUAL_OPTIONAL_FIELDS = new Set(['project', 'team', 'repository', 'repositoryId', 'applicationId']);

export function configureConfluencePrompts(server, { getContext = () => null } = {}) {
  Object.values(CONFLUENCE_PROMPTS).forEach(prompt => {
    const callback = async (args) => {
      const ctx = getContext();
      const message = generateConfluencePromptMessage(prompt.name, args ?? {}, ctx);
      return { messages: [{ role: 'user', content: { type: 'text', text: message } }] };
    };
    if (prompt.arguments.length === 0) {
      server.prompt(prompt.name, prompt.description, callback);
    } else {
      const argsSchema = Object.fromEntries(
        prompt.arguments.map(arg => [
          arg.name,
          (!arg.required || CONTEXTUAL_OPTIONAL_FIELDS.has(arg.name))
            ? z.string().optional().describe(arg.description)
            : z.string().describe(arg.description)
        ])
      );
      server.prompt(prompt.name, prompt.description, argsSchema, callback);
    }
  });
  console.error(`Registered ${Object.keys(CONFLUENCE_PROMPTS).length} Confluence prompts`);
}

export { CONFLUENCE_PROMPTS };
