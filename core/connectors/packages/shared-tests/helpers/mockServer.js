import { vi } from 'vitest';

/**
 * Creates a mock MCP server for testing tool registration
 * @returns {Object} Mock server with tool registration tracking
 */
export function createMockServer() {
  const registeredTools = new Map();
  
  const server = {
    tool: vi.fn((name, description, schema, handler) => {
      registeredTools.set(name, {
        name,
        description,
        schema,
        handler
      });
    }),
    
    // Helper to get registered tools
    getRegisteredTools() {
      return Array.from(registeredTools.values());
    },
    
    // Helper to get a specific tool
    getTool(name) {
      return registeredTools.get(name);
    },
    
    // Helper to invoke a tool handler
    async invokeTool(name, params) {
      const tool = registeredTools.get(name);
      if (!tool) {
        throw new Error(`Tool ${name} not registered`);
      }
      return await tool.handler(params);
    },
    
    // Expose the internal registeredTools Map for assertions
    registeredTools,

    // Mock other MCP server methods
    connect: vi.fn(),
    close: vi.fn()
  };
  
  return server;
}

/**
 * Creates a mock stdio transport for MCP server testing
 * @returns {Object} Mock transport
 */
export function createMockTransport() {
  return {
    start: vi.fn(),
    close: vi.fn(),
    send: vi.fn(),
    onMessage: vi.fn(),
    onError: vi.fn(),
    onClose: vi.fn()
  };
}

/**
 * Helper to validate tool response format
 * @param {Object} response - Tool response to validate
 * @returns {boolean} True if response is valid
 */
export function isValidToolResponse(response) {
  if (!response || typeof response !== 'object') {
    return false;
  }
  
  // Check for content array
  if (!Array.isArray(response.content)) {
    return false;
  }
  
  // Check each content item
  for (const item of response.content) {
    if (!item.type || !item.text) {
      return false;
    }
  }
  
  return true;
}

/**
 * Helper to validate error response format
 * @param {Object} response - Tool response to validate
 * @returns {boolean} True if response is a valid error response
 */
export function isValidErrorResponse(response) {
  return isValidToolResponse(response) && response.isError === true;
}

/**
 * Helper to extract text from tool response
 * @param {Object} response - Tool response
 * @returns {string} Extracted text content
 */
export function extractResponseText(response) {
  if (!isValidToolResponse(response)) {
    throw new Error('Invalid tool response format');
  }
  
  return response.content[0].text;
}

/**
 * Helper to parse JSON response
 * @param {Object} response - Tool response
 * @returns {Object} Parsed JSON object
 */
export function parseResponseJson(response) {
  const text = extractResponseText(response);
  return JSON.parse(text);
}
