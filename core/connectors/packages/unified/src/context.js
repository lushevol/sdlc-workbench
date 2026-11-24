/**
 * Re-export shim — context logic has moved to @sc-node-mcp/core.
 * This file is kept so that unified/tools/context.js stays unmodified.
 */
export { getActiveContext, loadContext, saveContext, getContextFilePath } from '@sc-node-mcp/core';
