/**
 * Context MCP Tools
 * Exposes ctx_set, ctx_get, ctx_switch, ctx_list for managing workspace context.
 */
import { z } from 'zod';
import { loadContext, saveContext, getActiveContext } from '../context.js';

/**
 * Registers the four context management tools on the MCP server.
 * @param {import('@modelcontextprotocol/sdk/server/mcp.js').McpServer} server
 */
export function configureContextTools(server) {
  // ─── ctx_set ────────────────────────────────────────────────────────────────
  server.tool(
    'ctx_set',
    'Create or update a named workspace context and set it as the active context. ' +
    'Stores ADO project, team, default branch, area/iteration paths, repository list, ' +
    'Nexus app IDs, and Confluence space key in ~/.sc-node-mcp-context.json.',
    {
      name: z.string().describe('Context name (e.g., my-service)'),
      description: z.string().optional().describe('Human-readable label for this context'),
      project: z.string().optional().describe('Azure DevOps project name'),
      team: z.string().optional().describe('Team name'),
      defaultBranch: z.string().optional().describe('Default branch (e.g., develop)'),
      areaPath: z.string().optional().describe('Work item area path'),
      iterationPath: z.string().optional().describe('Current iteration path (e.g., Platform\\Sprint 12)'),
      workspacePaths: z.string().optional().describe(
        'Comma-separated local folder paths — when the MCP server cwd matches one, this context auto-activates'
      ),
      repositories: z.string().optional().describe(
        'JSON array of repository objects: [{name, isDefault, defaultBranch, nexusAppId}]'
      ),
      confluenceSpaceKey: z.string().optional().describe('Default Confluence space key (e.g., PLAT)'),
    },
    async (args) => {
      try {
        const store = loadContext() || { version: '1', activeContext: null, contexts: {} };

        let repositories;
        if (args.repositories) {
          try {
            repositories = JSON.parse(args.repositories);
          } catch {
            return {
              content: [{ type: 'text', text: 'Invalid repositories JSON. Expected an array like: [{"name":"my-service","isDefault":true,"nexusAppId":"ITAM__PRD__my-service"}]' }],
              isError: true
            };
          }
        }

        const existing = store.contexts[args.name] || {};
        const existingAdo = existing.ado || {};
        const existingConfluence = existing.confluence || {};

        const updatedAdo = {
          ...existingAdo,
          ...(args.project       !== undefined ? { project:       args.project }       : {}),
          ...(args.team          !== undefined ? { team:          args.team }          : {}),
          ...(args.defaultBranch !== undefined ? { defaultBranch: args.defaultBranch } : {}),
          ...(args.areaPath      !== undefined ? { areaPath:      args.areaPath }      : {}),
          ...(args.iterationPath !== undefined ? { iterationPath: args.iterationPath } : {}),
        };

        const updatedConfluence = {
          ...existingConfluence,
          ...(args.confluenceSpaceKey !== undefined ? { defaultSpaceKey: args.confluenceSpaceKey } : {}),
        };

        store.contexts[args.name] = {
          ...existing,
          ...(args.description  !== undefined ? { description: args.description }  : {}),
          ...(args.workspacePaths !== undefined
            ? { workspacePaths: args.workspacePaths.split(',').map(p => p.trim()).filter(Boolean) }
            : {}),
          ...(Object.keys(updatedAdo).length > 0 ? { ado: updatedAdo } : {}),
          ...(repositories !== undefined ? { repositories } : {}),
          ...(Object.keys(updatedConfluence).length > 0 ? { confluence: updatedConfluence } : {}),
        };

        store.activeContext = args.name;
        saveContext(store);

        return {
          content: [{
            type: 'text',
            text: `Context "${args.name}" saved and set as active.\n\n${JSON.stringify(store.contexts[args.name], null, 2)}`
          }]
        };
      } catch (error) {
        return { content: [{ type: 'text', text: error?.message || String(error) }], isError: true };
      }
    }
  );

  // ─── ctx_get ────────────────────────────────────────────────────────────────
  server.tool(
    'ctx_get',
    'Get the current active context as JSON. Auto-detects context by matching workspacePaths against cwd; falls back to the named activeContext.',
    {},
    async () => {
      try {
        const ctx = getActiveContext();
        if (!ctx) {
          return {
            content: [{ type: 'text', text: 'No active context. Use ctx_set to create one.' }]
          };
        }
        return { content: [{ type: 'text', text: JSON.stringify(ctx, null, 2) }] };
      } catch (error) {
        return { content: [{ type: 'text', text: error?.message || String(error) }], isError: true };
      }
    }
  );

  // ─── ctx_switch ─────────────────────────────────────────────────────────────
  server.tool(
    'ctx_switch',
    'Switch the active context to a different stored context name.',
    {
      name: z.string().describe('Context name to switch to'),
    },
    async ({ name }) => {
      try {
        const store = loadContext();
        if (!store || !store.contexts) {
          return {
            content: [{ type: 'text', text: 'No context store found. Use ctx_set to create a context first.' }],
            isError: true
          };
        }
        if (!store.contexts[name]) {
          const names = Object.keys(store.contexts).join(', ') || '(none)';
          return {
            content: [{ type: 'text', text: `Context "${name}" not found. Available contexts: ${names}` }],
            isError: true
          };
        }
        store.activeContext = name;
        saveContext(store);
        return { content: [{ type: 'text', text: `Active context switched to "${name}".` }] };
      } catch (error) {
        return { content: [{ type: 'text', text: error?.message || String(error) }], isError: true };
      }
    }
  );

  // ─── ctx_list ────────────────────────────────────────────────────────────────
  server.tool(
    'ctx_list',
    'List all stored context names with their descriptions and workspace paths.',
    {},
    async () => {
      try {
        const store = loadContext();
        if (!store || !store.contexts || Object.keys(store.contexts).length === 0) {
          return {
            content: [{ type: 'text', text: 'No contexts stored. Use ctx_set to create one.' }]
          };
        }
        const lines = Object.entries(store.contexts).map(([ctxName, ctx]) => {
          const activeMarker = ctxName === store.activeContext ? ' ✓ (active)' : '';
          const desc = ctx.description || '(no description)';
          const paths = (ctx.workspacePaths || []).join(', ') || 'none';
          const project = ctx.ado?.project ? ` | project: ${ctx.ado.project}` : '';
          const team = ctx.ado?.team ? ` | team: ${ctx.ado.team}` : '';
          return `• ${ctxName}${activeMarker}\n  ${desc}${project}${team}\n  Paths: ${paths}`;
        });
        return { content: [{ type: 'text', text: lines.join('\n\n') }] };
      } catch (error) {
        return { content: [{ type: 'text', text: error?.message || String(error) }], isError: true };
      }
    }
  );
}
