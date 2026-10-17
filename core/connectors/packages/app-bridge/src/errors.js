/**
 * @author Podder, Arunangshu
 * @bankId 2004018
 */

/**
 * Format a caught error for an MCP tool's isError response text.
 * Falls back to String(error) when the thrown value isn't an Error instance (or lacks a message) —
 * e.g. a plain string or object was thrown instead of an Error.
 * @param {unknown} error
 * @returns {string}
 */
export function formatError(error) {
  return error?.message || String(error);
}
