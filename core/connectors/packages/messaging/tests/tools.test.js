import { describe, it, expect, vi, beforeEach } from 'vitest';
import { configureEmailTools } from '../src/tools.js';
import { createMockServer } from '@sc-node-mcp/shared-tests/helpers/mockServer';

describe('Email Tools Registration', () => {
  let mockServer;
  let mockBridge;
  let getPythonBridgeMock;

  beforeEach(() => {
    mockServer = createMockServer();
    mockBridge = { sendEmail: vi.fn() };
    getPythonBridgeMock = vi.fn().mockResolvedValue(mockBridge);
  });

  it('should register email_send tool via configureEmailTools', () => {
    configureEmailTools(mockServer, getPythonBridgeMock);
    const tools = mockServer.getRegisteredTools();
    const toolNames = tools.map(t => t.name);
    expect(toolNames).toContain('email_send');
  });

  it('should log success message to stderr', () => {
    const stderrSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
    configureEmailTools(mockServer, getPythonBridgeMock);
    expect(stderrSpy).toHaveBeenCalledWith('Email tools registered successfully');
    stderrSpy.mockRestore();
  });
});
