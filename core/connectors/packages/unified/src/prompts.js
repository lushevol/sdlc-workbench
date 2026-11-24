/**
 * MCP Prompts for Unified Server
 * Aggregates per-package prompts and registers unified-only prompts.
 */
import { z } from 'zod';
import { getActiveContext } from './context.js';
import { configureAdoPrompts } from '@sc-node-mcp/ado';
import { configureConfluencePrompts } from '@sc-node-mcp/confluence';
import { configureScwikiPrompts } from '@sc-node-mcp/scwiki';
import { configureMessagingPrompts } from '@sc-node-mcp/messaging';
import { configureNexusPrompts } from '@sc-node-mcp/nexus';
import { configureSonarPrompts } from '@sc-node-mcp/sonar';

// Unified-only prompts (not in any sub-package)
const UNIFIED_PROMPTS = {
  UPLOAD_ATTACHMENT_UI: {
    name: 'upload-attachment-ui',
    description: 'Open the interactive file upload panel to attach files to an Azure DevOps work item',
    arguments: [
      { name: 'project', description: 'Azure DevOps project name (optional — pre-fills the UI)', required: false },
      { name: 'wiId', description: 'Work item ID to attach files to (optional — pre-fills the UI)', required: false }
    ]
  },

  SET_CONTEXT: {
    name: 'set-context',
    description: 'Guided workflow to set up the active workspace context (project, team, default repo, Nexus app ID, Confluence space key)',
    arguments: [
      { name: 'name', description: 'Context name (e.g., my-service)', required: true },
      { name: 'project', description: 'Azure DevOps project name', required: false },
      { name: 'team', description: 'Team name', required: false },
      { name: 'defaultRepo', description: 'Default repository name', required: false },
      { name: 'nexusAppId', description: 'Nexus IQ application ID for the default repo (format: ITAM__ENV__REPO_NAME)', required: false },
      { name: 'confluenceSpaceKey', description: 'Default Confluence space key (e.g., PLAT)', required: false }
    ]
  },

  SWITCH_CONTEXT: {
    name: 'switch-context',
    description: 'Switch the active workspace context to a previously saved context by name',
    arguments: [
      { name: 'name', description: 'Context name to switch to (use list-contexts to see available names)', required: true }
    ]
  },

  LIST_CONTEXTS: {
    name: 'list-contexts',
    description: 'List all saved workspace contexts with their project, team, and workspace path details',
    arguments: []
  }
};

const buildUploadAttachmentMessage = (args) => {
  let projectLine = 'Project: (enter your Azure DevOps project name)\n';
  if (args.project) projectLine = `Project: ${args.project}\n`;
  let wiIdLine = 'Work Item ID: (enter the work item ID to attach files to)\n';
  if (args.wiId) wiIdLine = `Work Item ID: ${args.wiId}\n`;
  const titleParts = ['Open the ADO file upload panel'];
  if (args.project) titleParts.push(`for project "${args.project}"`);
  if (args.wiId) titleParts.push(`and work item #${args.wiId}`);
  const panelTitle = titleParts.join(' ');
  return `${panelTitle}:\n\n${projectLine}${wiIdLine}\nUse wit_upload_attachment_ui to open the interactive upload panel.\nThe panel lets you drag-and-drop or browse for files, then uploads them as AttachedFile relations on the work item.\n\nIf project and work item ID are provided, the fields will be pre-filled in the UI.`;
};

const buildSetContextMessage = (args) => {
  const lines = [`- name: ${args.name}`];
  if (args.project) lines.push(`- project: ${args.project}`);
  if (args.team) lines.push(`- team: ${args.team}`);
  if (args.defaultRepo) {
    const nexusPart = args.nexusAppId ? `, "nexusAppId": "${args.nexusAppId}"` : '';
    lines.push(`- repositories: [{ "name": "${args.defaultRepo}", "isDefault": true${nexusPart} }]`);
  }
  if (args.confluenceSpaceKey) lines.push(`- confluenceSpaceKey: ${args.confluenceSpaceKey}`);
  return `Set up the active workspace context named "${args.name}".\n\nUse ctx_set with the following values:\n${lines.join('\n')}\n\nAfter saving, confirm the context is active by calling ctx_get.`;
};

const generateUnifiedPromptMessage = (name, args = {}) => {
  switch (name) {
    case 'upload-attachment-ui':
      return buildUploadAttachmentMessage(args);

    case 'set-context':
      return buildSetContextMessage(args);

    case 'switch-context':
      return `Switch the active workspace context to "${args.name}".

Call ctx_switch with name="${args.name}".

All subsequent tool calls will auto-fill project, team, and repository arguments from the "${args.name}" context.
Use ctx_get to confirm the switch was successful.`;

    case 'list-contexts':
      return `List all saved workspace contexts.

Call ctx_list to show all stored contexts with their names, active marker, project, team, and workspace paths.

The currently active context is marked with ✓. Use switch-context (or ctx_switch directly) to change the active context.`;

    default:
      return 'Unknown prompt';
  }
};

const CONTEXTUAL_OPTIONAL_FIELDS = new Set([
  'project', 'team', 'repository', 'repositoryId', 'applicationId'
]);

export const configurePrompts = (server) => {
  // Per-package prompts — each gets getActiveContext for context auto-fill
  configureAdoPrompts(server, { getContext: getActiveContext });
  configureConfluencePrompts(server, { getContext: getActiveContext });
  configureScwikiPrompts(server);
  configureMessagingPrompts(server, { getContext: getActiveContext });
  configureNexusPrompts(server, { getContext: getActiveContext });
  configureSonarPrompts(server, { getContext: getActiveContext });

  // Unified-only prompts
  Object.values(UNIFIED_PROMPTS).forEach(prompt => {
    const callback = async (args) => {
      const message = generateUnifiedPromptMessage(prompt.name, args ?? {});
      return {
        messages: [{ role: 'user', content: { type: 'text', text: message } }]
      };
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

  console.error(`Registered ${Object.keys(UNIFIED_PROMPTS).length} unified-only prompts`);
};

export { UNIFIED_PROMPTS };
