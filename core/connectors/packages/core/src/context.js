/**
 * Context Store for SC Node MCP
 * Native workspace contexts remain inside the selected Workbench root.
 */
import { readFileSync, writeFileSync, renameSync, existsSync, mkdirSync } from 'fs';
import { homedir } from 'os';
import { join, dirname } from 'path';

const CONTEXT_FILE = join(homedir(), '.sc-node-mcp-context.json');

/**
 * Returns the path to the context file (overridable in tests).
 */
export function getContextFilePath() {
  if (process.env.WORKBENCH_CONNECTOR_WORKSPACE) {
    return join(process.env.WORKBENCH_CONNECTOR_WORKSPACE, '.workbench', 'connectors', 'context.json');
  }
  return CONTEXT_FILE;
}

/**
 * Reads and parses the selected workspace or legacy context file.
 * Returns null safely if the file does not exist or cannot be parsed.
 * @returns {Object|null}
 */
export function loadContext() {
  try {
    const filePath = getContextFilePath();
    if (!existsSync(filePath)) return null;
    const raw = readFileSync(filePath, 'utf8');
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

/**
 * Atomically writes the full context store back to disk via a temp-file rename.
 * @param {Object} data - Full context store object
 */
export function saveContext(data) {
  const filePath = getContextFilePath();
  const tmp = filePath + '.tmp';
  mkdirSync(dirname(filePath), { recursive: true });
  writeFileSync(tmp, JSON.stringify(data, null, 2), 'utf8');
  renameSync(tmp, filePath);
}

/**
 * Resolves and returns the active context object.
 *
 * Priority:
 *  1. A context whose workspacePaths[] contains (or is a prefix of) process.cwd()
 *  2. The context named by store.activeContext
 *  3. null
 *
 * @returns {Object|null} Active context object (ado, repositories, confluence sections) or null
 */
export function getActiveContext() {
  const store = loadContext();
  if (!store || !store.contexts) return null;

  const cwd = process.env.WORKBENCH_CONNECTOR_WORKSPACE || process.cwd();

  // Auto-detect by workspacePaths match — takes priority over activeContext name
  for (const ctx of Object.values(store.contexts)) {
    if (
      Array.isArray(ctx.workspacePaths) &&
      ctx.workspacePaths.some(p => cwd.startsWith(p))
    ) {
      return ctx;
    }
  }

  // Fall back to explicit activeContext pointer
  if (store.activeContext && store.contexts[store.activeContext]) {
    return store.contexts[store.activeContext];
  }

  return null;
}
