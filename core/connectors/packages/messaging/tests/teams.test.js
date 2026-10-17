import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { configureTeamsTools } from '../src/tools/teams.js';
import { getTeamsNativeBridge, clearPythonCache } from '../src/connection.js';
import { createMockServer, isValidToolResponse, isValidErrorResponse } from '@sc-node-mcp/shared-tests/helpers/mockServer';
import { spawn, execSync } from 'child_process';
import { EventEmitter } from 'events';

// Mock child_process module
vi.mock('child_process', () => ({
  spawn: vi.fn(),
  execSync: vi.fn()
}));

// ─── Tool layer tests ─────────────────────────────────────────────────────────

describe('Teams Tools', () => {
  let mockServer;
  let mockBridge;
  let getTeamsBridgeMock;

  beforeEach(() => {
    mockServer = createMockServer();

    mockBridge = {
      sendMessage: vi.fn()
    };

    getTeamsBridgeMock = vi.fn().mockResolvedValue(mockBridge);

    configureTeamsTools(mockServer, getTeamsBridgeMock);
  });

  describe('teams_send_message tool', () => {
    it('should be registered', () => {
      const toolNames = mockServer.getRegisteredTools().map(t => t.name);
      expect(toolNames).toContain('teams_send_message');
    });

    it('should send a direct message with required parameters only', async () => {
      mockBridge.sendMessage.mockResolvedValue({
        status: 'success',
        message: 'Teams message sent to user@example.com'
      });

      const params = {
        to: ['user@example.com'],
        message: 'Hello, Teams!'
      };

      const response = await mockServer.invokeTool('teams_send_message', params);

      expect(isValidToolResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('Teams message sent successfully');
      expect(response.content[0].text).toContain('user@example.com');
      expect(response.content[0].text).toContain('Hello, Teams!');
      expect(getTeamsBridgeMock).toHaveBeenCalledTimes(1);
      expect(mockBridge.sendMessage).toHaveBeenCalledWith(
        ['user@example.com'],
        'Hello, Teams!',
        undefined
      );
    });

    it('should send a group chat message to multiple recipients', async () => {
      mockBridge.sendMessage.mockResolvedValue({
        status: 'success',
        message: 'Teams message sent to user1@example.com, user2@example.com'
      });

      const params = {
        to: ['user1@example.com', 'user2@example.com'],
        message: 'Team standup in 5 minutes.',
        title: 'Standup Reminder'
      };

      const response = await mockServer.invokeTool('teams_send_message', params);

      expect(isValidToolResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('user1@example.com');
      expect(response.content[0].text).toContain('Standup Reminder');
      expect(mockBridge.sendMessage).toHaveBeenCalledWith(
        ['user1@example.com', 'user2@example.com'],
        'Team standup in 5 minutes.',
        'Standup Reminder'
      );
    });

    it('should handle send errors gracefully', async () => {
      mockBridge.sendMessage.mockRejectedValue(
        new Error('AppleScript failed: Teams process not found')
      );

      const params = {
        to: ['user@example.com'],
        message: 'Test message'
      };

      const response = await mockServer.invokeTool('teams_send_message', params);

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('Failed to send Teams message');
      expect(response.content[0].text).toContain('Teams process not found');
      expect(response.content[0].text).toContain('Accessibility permission');
    });

    it('should reject an invalid email address', async () => {
      const params = {
        to: ['not-an-email'],
        message: 'Hello'
      };

      const response = await mockServer.invokeTool('teams_send_message', params).catch(e => e);

      const isRejected = response instanceof Error || (response && response.isError === true);
      expect(isRejected).toBe(true);
    });

    it('should reject an empty to array', async () => {
      const params = {
        to: [],
        message: 'Hello'
      };

      const response = await mockServer.invokeTool('teams_send_message', params).catch(e => e);

      const isRejected = response instanceof Error || (response && response.isError === true);
      expect(isRejected).toBe(true);
    });

    it('should reject an empty message', async () => {
      const params = {
        to: ['user@example.com'],
        message: ''
      };

      const response = await mockServer.invokeTool('teams_send_message', params).catch(e => e);

      const isRejected = response instanceof Error || (response && response.isError === true);
      expect(isRejected).toBe(true);
    });

    it('should use fallback text when result has no message (covers || branch)', async () => {
      // result.message is absent → covers `result.message || 'Message delivered...'` false arm
      mockBridge.sendMessage.mockResolvedValue({ status: 'success' });

      const response = await mockServer.invokeTool('teams_send_message', {
        to: ['user@example.com'],
        message: 'Hello!'
      });

      expect(isValidToolResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('Message delivered via Microsoft Teams');
    });

    it('should use String(error) when error has no message property (covers || branch)', async () => {
      // Throw a string (no .message) to cover `error?.message || String(error)` false arm
      mockBridge.sendMessage.mockRejectedValue('string-error-teams');

      const response = await mockServer.invokeTool('teams_send_message', {
        to: ['user@example.com'],
        message: 'Hello!'
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('string-error-teams');
    });
  });
});

// ─── Connection layer tests ────────────────────────────────────────────────────

describe('Teams Native Bridge (connection.js)', () => {
  let mockPythonProcess;

  beforeEach(() => {
    execSync.mockReturnValue('Python 3.11.0');

    mockPythonProcess = new EventEmitter();
    mockPythonProcess.stdin = { write: vi.fn(), end: vi.fn() };
    mockPythonProcess.stdout = new EventEmitter();
    mockPythonProcess.stderr = new EventEmitter();
    mockPythonProcess.kill = vi.fn();

    spawn.mockReturnValue(mockPythonProcess);
  });

  afterEach(() => {
    vi.clearAllMocks();
    clearPythonCache();
  });

  it('should return bridge object with sendMessage method', async () => {
    const bridge = await getTeamsNativeBridge();
    expect(bridge).toBeDefined();
    expect(typeof bridge.sendMessage).toBe('function');
  });

  it('should spawn Python with the bundled send-teams.py script', async () => {
    const bridge = await getTeamsNativeBridge();

    const sendPromise = bridge.sendMessage(['user@example.com'], 'Hello');

    mockPythonProcess.stdout.emit('data', JSON.stringify({ status: 'success', message: 'Sent' }));
    mockPythonProcess.emit('close', 0);

    await sendPromise;

    expect(spawn).toHaveBeenCalled();
    const scriptArg = spawn.mock.calls[0][1][0];
    expect(scriptArg).toContain('send-teams.py');
    expect(scriptArg).toContain('scripts');
    expect(scriptArg).not.toContain('email-automation');
  });

  it('should write correct JSON with to array to stdin', async () => {
    const bridge = await getTeamsNativeBridge();

    const sendPromise = bridge.sendMessage(
      ['user1@example.com', 'user2@example.com'],
      'Hello, Teams!',
      'My Title'
    );

    mockPythonProcess.stdout.emit('data', JSON.stringify({ status: 'success' }));
    mockPythonProcess.emit('close', 0);

    await sendPromise;

    const writtenData = JSON.parse(mockPythonProcess.stdin.write.mock.calls[0][0]);
    expect(writtenData.to).toEqual(['user1@example.com', 'user2@example.com']);
    expect(writtenData.message).toBe('Hello, Teams!');
    expect(writtenData.title).toBe('My Title');
  });

  it('should reject when Python exits with non-zero code', async () => {
    const bridge = await getTeamsNativeBridge();

    const sendPromise = bridge.sendMessage(['user@example.com'], 'Hello');

    mockPythonProcess.stderr.emit('data', 'Teams process not found');
    mockPythonProcess.emit('close', 1);

    await expect(sendPromise).rejects.toThrow('Python process exited with code 1');
  });
});

