import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { getPythonBridge, getTeamsNativeBridge, clearPythonCache } from '../src/connection.js';
import { spawn, execSync } from 'child_process';
import { EventEmitter } from 'events';

// Mock child_process module
vi.mock('child_process', () => ({
  spawn: vi.fn(),
  execSync: vi.fn()
}));

describe('Python Bridge Connection', () => {
  let mockPythonProcess;

  beforeEach(() => {
    // Mock execSync to return Python 3.x version
    execSync.mockReturnValue('Python 3.11.0');
    
    // Create mock process with event emitter
    mockPythonProcess = new EventEmitter();
    mockPythonProcess.stdin = {
      write: vi.fn(),
      end: vi.fn()
    };
    mockPythonProcess.stdout = new EventEmitter();
    mockPythonProcess.stderr = new EventEmitter();
    mockPythonProcess.kill = vi.fn();

    // Mock spawn to return our mock process
    spawn.mockReturnValue(mockPythonProcess);
  });

  afterEach(() => {
    vi.clearAllMocks();
    clearPythonCache();
  });

  describe('getPythonBridge', () => {
    it('should return bridge object with sendEmail method', async () => {
      const bridge = await getPythonBridge();
      
      expect(bridge).toBeDefined();
      expect(bridge.sendEmail).toBeDefined();
      expect(typeof bridge.sendEmail).toBe('function');
    });

    it('should spawn Python process with correct arguments', async () => {
      const bridge = await getPythonBridge();
      
      // Trigger sendEmail
      const sendPromise = bridge.sendEmail({
        to: ['test@example.com'],
        subject: 'Test',
        htmlBody: 'Body'
      });

      // Simulate successful Python execution
      mockPythonProcess.stdout.emit('data', JSON.stringify({ status: 'success', message: 'Sent' }));
      mockPythonProcess.emit('close', 0);

      await sendPromise;

      expect(spawn).toHaveBeenCalled();
      const spawnArgs = spawn.mock.calls[0];
      const command = spawnArgs[0];
      const args = spawnArgs[1];
      
      // Should detect and use a Python 3.x command
      expect(['python', 'python3', 'py']).toContain(command);
      expect(args[0]).toContain('send-outlook.py');
      // Verify it's using the bundled script in scripts directory
      expect(args[0]).toContain('scripts');
      expect(args[0]).not.toContain('email-automation');
      
      // Verify version was checked
      expect(execSync).toHaveBeenCalled();
    });

    it('should send email data via stdin as JSON', async () => {
      const bridge = await getPythonBridge();
      
      const emailData = {
        to: ['recipient@example.com'],
        cc: ['cc@example.com'],
        subject: 'Test Subject',
        htmlBody: 'Test Body'
      };

      const sendPromise = bridge.sendEmail(emailData);

      // Simulate success
      mockPythonProcess.stdout.emit('data', JSON.stringify({ status: 'success' }));
      mockPythonProcess.emit('close', 0);

      await sendPromise;

      // Verify stdin write was called with correct JSON
      expect(mockPythonProcess.stdin.write).toHaveBeenCalled();
      const writtenData = mockPythonProcess.stdin.write.mock.calls[0][0];
      const parsedData = JSON.parse(writtenData);
      
      expect(parsedData.to).toEqual(['recipient@example.com']);
      expect(parsedData.cc).toEqual(['cc@example.com']);
      expect(parsedData.subject).toBe('Test Subject');
      expect(parsedData.htmlBody).toBe('Test Body');
      expect(mockPythonProcess.stdin.end).toHaveBeenCalled();
    });

    it('should pass multiple recipient arrays through unchanged', async () => {
      const bridge = await getPythonBridge();
      
      const sendPromise = bridge.sendEmail({
        to: ['user1@example.com', 'user2@example.com'],
        cc: ['cc1@example.com', 'cc2@example.com'],
        bcc: ['bcc@example.com'],
        subject: 'Test',
        htmlBody: 'Body'
      });

      mockPythonProcess.stdout.emit('data', JSON.stringify({ status: 'success' }));
      mockPythonProcess.emit('close', 0);

      await sendPromise;

      const writtenData = mockPythonProcess.stdin.write.mock.calls[0][0];
      const parsedData = JSON.parse(writtenData);
      
      expect(parsedData.to).toEqual(['user1@example.com', 'user2@example.com']);
      expect(parsedData.cc).toEqual(['cc1@example.com', 'cc2@example.com']);
      expect(parsedData.bcc).toEqual(['bcc@example.com']);
    });

    it('should handle empty CC and BCC arrays', async () => {
      const bridge = await getPythonBridge();
      
      const sendPromise = bridge.sendEmail({
        to: ['test@example.com'],
        cc: [],
        bcc: [],
        subject: 'Test',
        htmlBody: 'Body'
      });

      mockPythonProcess.stdout.emit('data', JSON.stringify({ status: 'success' }));
      mockPythonProcess.emit('close', 0);

      await sendPromise;

      const writtenData = mockPythonProcess.stdin.write.mock.calls[0][0];
      const parsedData = JSON.parse(writtenData);
      
      expect(parsedData.cc).toEqual([]);
      expect(parsedData.bcc).toEqual([]);
    });

    it('should parse JSON response from stdout', async () => {
      const bridge = await getPythonBridge();
      
      const sendPromise = bridge.sendEmail({
        to: ['test@example.com'],
        subject: 'Test',
        htmlBody: 'Body'
      });

      const expectedResponse = { status: 'success', message: 'Email sent via Outlook' };
      mockPythonProcess.stdout.emit('data', JSON.stringify(expectedResponse));
      mockPythonProcess.emit('close', 0);

      const result = await sendPromise;
      
      expect(result).toEqual(expectedResponse);
    });

    it('should handle non-JSON stdout as success message', async () => {
      const bridge = await getPythonBridge();
      
      const sendPromise = bridge.sendEmail({
        to: ['test@example.com'],
        subject: 'Test',
        htmlBody: 'Body'
      });

      mockPythonProcess.stdout.emit('data', 'Email sent successfully\n');
      mockPythonProcess.emit('close', 0);

      const result = await sendPromise;
      
      expect(result.status).toBe('success');
      expect(result.message).toContain('Email sent successfully');
    });

    it('should reject on non-zero exit code', async () => {
      const bridge = await getPythonBridge();
      
      const sendPromise = bridge.sendEmail({
        to: ['test@example.com'],
        subject: 'Test',
        htmlBody: 'Body'
      });

      mockPythonProcess.stderr.emit('data', 'Python error occurred');
      mockPythonProcess.emit('close', 1);

      await expect(sendPromise).rejects.toThrow('Python process exited with code 1');
    });

    it('should reject on Python process spawn error', async () => {
      const bridge = await getPythonBridge();
      
      const sendPromise = bridge.sendEmail({
        to: ['test@example.com'],
        subject: 'Test',
        htmlBody: 'Body'
      });

      mockPythonProcess.emit('error', new Error('ENOENT: python3 not found'));

      await expect(sendPromise).rejects.toThrow('Failed to spawn Python process');
    });

    it('should handle multi-chunk stdout data', async () => {
      const bridge = await getPythonBridge();
      
      const sendPromise = bridge.sendEmail({
        to: ['test@example.com'],
        subject: 'Test',
        htmlBody: 'Body'
      });

      // Simulate chunked data
      const response = JSON.stringify({ status: 'success', message: 'Sent' });
      const midpoint = Math.floor(response.length / 2);
      mockPythonProcess.stdout.emit('data', response.slice(0, midpoint));
      mockPythonProcess.stdout.emit('data', response.slice(midpoint));
      mockPythonProcess.emit('close', 0);

      const result = await sendPromise;
      
      expect(result.status).toBe('success');
    });

    it('should include stderr in error message', async () => {
      const bridge = await getPythonBridge();
      
      const sendPromise = bridge.sendEmail({
        to: ['test@example.com'],
        subject: 'Test',
        htmlBody: 'Body'
      });

      mockPythonProcess.stderr.emit('data', 'Outlook not running');
      mockPythonProcess.stderr.emit('data', '\nPython traceback...');
      mockPythonProcess.emit('close', 1);

      await expect(sendPromise).rejects.toThrow('Outlook not running');
    });
  });

  describe('Python Version Detection', () => {
    it('should use python3 command when available', async () => {
      execSync.mockReturnValue('Python 3.11.0');
      
      const bridge = await getPythonBridge();
      const sendPromise = bridge.sendEmail({
        to: ['test@example.com'],
        subject: 'Test',
        htmlBody: 'Body'
      });

      mockPythonProcess.stdout.emit('data', JSON.stringify({ status: 'success' }));
      mockPythonProcess.emit('close', 0);
      await sendPromise;

      expect(spawn).toHaveBeenCalled();
      const command = spawn.mock.calls[0][0];
      expect(['python3', 'python', 'py']).toContain(command);
    });

    it('should fallback to python command if python3 fails', async () => {
      // Mock to fail for python3 but succeed for python
      execSync.mockImplementation((cmd) => {
        if (cmd.startsWith('python3')) {
          throw new Error('Command not found');
        } else if (cmd.startsWith('python ')) {
          return 'Python 3.9.0';
        }
        throw new Error('Command not found');
      });

      const bridge = await getPythonBridge();
      const sendPromise = bridge.sendEmail({
        to: ['test@example.com'],
        subject: 'Test',
        htmlBody: 'Body'
      });

      mockPythonProcess.stdout.emit('data', JSON.stringify({ status: 'success' }));
      mockPythonProcess.emit('close', 0);
      await sendPromise;

      expect(spawn).toHaveBeenCalled();
      const command = spawn.mock.calls[0][0];
      expect(command).toBe('python');
    });

    it('should reject Python 2.x installations', async () => {
      // All Python commands return version 2.x
      execSync.mockReturnValue('Python 2.7.18');

      const bridge = await getPythonBridge();
      
      // The error should be thrown immediately when trying to send
      await expect(bridge.sendEmail({
        to: ['test@example.com'],
        subject: 'Test',
        htmlBody: 'Body'
      })).rejects.toThrow('Python 3.x not found');
      
      // spawn should not have been called
      expect(spawn).not.toHaveBeenCalled();
    });

    it('should handle case when no Python is installed', async () => {
      execSync.mockImplementation(() => {
        throw new Error('Command not found');
      });

      const bridge = await getPythonBridge();
      
      // The error should be thrown immediately when trying to send
      await expect(bridge.sendEmail({
        to: ['test@example.com'],
        subject: 'Test',
        htmlBody: 'Body'
      })).rejects.toThrow('Python 3.x not found');
      
      // spawn should not have been called
      expect(spawn).not.toHaveBeenCalled();
    });

    it('should cache Python command detection', async () => {
      execSync.mockReturnValue('Python 3.10.0');

      const bridge = await getPythonBridge();
      
      // Send first email
      let sendPromise = bridge.sendEmail({
        to: ['test1@example.com'],
        subject: 'Test 1',
        htmlBody: 'Body'
      });
      mockPythonProcess.stdout.emit('data', JSON.stringify({ status: 'success' }));
      mockPythonProcess.emit('close', 0);
      await sendPromise;

      const firstCallCount = execSync.mock.calls.length;

      // Send second email
      sendPromise = bridge.sendEmail({
        to: ['test2@example.com'],
        subject: 'Test 2',
        htmlBody: 'Body'
      });
      mockPythonProcess.stdout.emit('data', JSON.stringify({ status: 'success' }));
      mockPythonProcess.emit('close', 0);
      await sendPromise;

      // execSync should be called same number of times (cached)
      expect(execSync.mock.calls.length).toBe(firstCallCount);
    });

    it('should support py launcher on Windows', async () => {
      // Mock Windows platform
      const originalPlatform = process.platform;
      Object.defineProperty(process, 'platform', { value: 'win32' });

      execSync.mockImplementation((cmd) => {
        if (cmd.includes('py ')) {
          return 'Python 3.11.0';
        }
        throw new Error('Command not found');
      });

      const bridge = await getPythonBridge();
      const sendPromise = bridge.sendEmail({
        to: ['test@example.com'],
        subject: 'Test',
        htmlBody: 'Body'
      });

      mockPythonProcess.stdout.emit('data', JSON.stringify({ status: 'success' }));
      mockPythonProcess.emit('close', 0);
      await sendPromise;

      expect(spawn).toHaveBeenCalled();
      const command = spawn.mock.calls[0][0];
      expect(['python3', 'python', 'py']).toContain(command);

      // Restore platform
      Object.defineProperty(process, 'platform', { value: originalPlatform });
    });

    it('should use stdout as error message when stderr is empty (covers || fallback)', async () => {
      const bridge = await getPythonBridge();
      const sendPromise = bridge.sendEmail({
        to: ['test@example.com'],
        subject: 'Test',
        htmlBody: 'Body'
      });
      // Only stdout has content, stderr is empty → covers `stderr || stdout` false arm
      mockPythonProcess.stdout.emit('data', 'Unhandled Python exception');
      mockPythonProcess.emit('close', 1);

      await expect(sendPromise).rejects.toThrow('Unhandled Python exception');
    });

    it('should use fallback success message when stdout is empty (covers || fallback)', async () => {
      const bridge = await getPythonBridge();
      const sendPromise = bridge.sendEmail({
        to: ['test@example.com'],
        subject: 'Test',
        htmlBody: 'Body'
      });
      // Emit non-JSON empty stdout → JSON.parse fails, stdout.trim() = '' → fallback fires
      mockPythonProcess.stdout.emit('data', '');
      mockPythonProcess.emit('close', 0);

      const result = await sendPromise;
      expect(result.status).toBe('success');
      expect(result.message).toBe('Email sent successfully');
    });
  });

  describe('Teams Native Bridge', () => {
    beforeEach(() => {
      clearPythonCache();
      execSync.mockReturnValue('Python 3.11.0');
      mockPythonProcess = new EventEmitter();
      mockPythonProcess.stdin = { write: vi.fn(), end: vi.fn() };
      mockPythonProcess.stdout = new EventEmitter();
      mockPythonProcess.stderr = new EventEmitter();
      mockPythonProcess.kill = vi.fn();
      spawn.mockReturnValue(mockPythonProcess);
    });

    it('should send a Teams message via the bridge', async () => {
      const bridge = await getTeamsNativeBridge();
      const sendPromise = bridge.sendMessage(['user@example.com'], 'Hello Teams', 'Title');

      mockPythonProcess.stdout.emit('data', JSON.stringify({ status: 'success', message: 'Sent' }));
      mockPythonProcess.emit('close', 0);

      const result = await sendPromise;
      expect(result.status).toBe('success');
    });

    it('should handle non-JSON stdout as success (covers || fallback in teams bridge)', async () => {
      const bridge = await getTeamsNativeBridge();
      const sendPromise = bridge.sendMessage(['user@example.com'], 'Hello', undefined);

      // Non-JSON stdout triggers the catch block → resolve with fallback
      mockPythonProcess.stdout.emit('data', 'Teams message delivered');
      mockPythonProcess.emit('close', 0);

      const result = await sendPromise;
      expect(result.status).toBe('success');
      expect(result.message).toContain('Teams message delivered');
    });

    it('should use fallback when teams stdout is empty and non-JSON (covers || branch)', async () => {
      const bridge = await getTeamsNativeBridge();
      const sendPromise = bridge.sendMessage(['user@example.com'], 'Hello', undefined);

      mockPythonProcess.stdout.emit('data', '');
      mockPythonProcess.emit('close', 0);

      const result = await sendPromise;
      expect(result.status).toBe('success');
      expect(result.message).toBe('Teams message sent successfully');
    });

    it('should use stdout as teams error when stderr is empty (covers || fallback)', async () => {
      const bridge = await getTeamsNativeBridge();
      const sendPromise = bridge.sendMessage(['user@example.com'], 'Hello', undefined);

      mockPythonProcess.stdout.emit('data', 'Teams process error');
      mockPythonProcess.emit('close', 1);

      await expect(sendPromise).rejects.toThrow('Teams process error');
    });
  });
});
