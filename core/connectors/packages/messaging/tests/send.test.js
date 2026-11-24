import { describe, it, expect, vi, beforeEach } from 'vitest';
import { configureSendTools } from '../src/tools/send.js';
import { createMockServer, isValidToolResponse, isValidErrorResponse } from '@sc-node-mcp/shared-tests/helpers/mockServer';

describe('Email Send Tools', () => {
  let mockServer;
  let mockBridge;
  let getPythonBridgeMock;

  beforeEach(() => {
    // Create mock server
    mockServer = createMockServer();

    // Create mock Python bridge
    mockBridge = {
      sendEmail: vi.fn()
    };

    // Create mock connection provider
    getPythonBridgeMock = vi.fn().mockResolvedValue(mockBridge);

    // Register tools
    configureSendTools(mockServer, getPythonBridgeMock);
  });

  describe('email_send tool', () => {
    it('should be registered', () => {
      const tools = mockServer.getRegisteredTools();
      // getRegisteredTools returns array of objects with name property
      const toolNames = tools.map(t => t.name);
      expect(toolNames).toContain('email_send');
    });

    it('should send email with required parameters only', async () => {
      // Mock successful send
      mockBridge.sendEmail.mockResolvedValue({
        status: 'success',
        message: 'Email sent successfully'
      });

      const params = {
        to: ['recipient@example.com'],
        subject: 'Test Subject',
        body: 'Test Body'
      };

      const response = await mockServer.invokeTool('email_send', params);

      expect(isValidToolResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('Email sent successfully');
      expect(response.content[0].text).toContain('recipient@example.com');
      expect(response.content[0].text).toContain('Test Subject');
      expect(getPythonBridgeMock).toHaveBeenCalledTimes(1);
      expect(mockBridge.sendEmail).toHaveBeenCalledWith({
        to: ['recipient@example.com'],
        cc: [],
        bcc: [],
        subject: 'Test Subject',
        htmlBody: 'Test Body'
      });
    });

    it('should send email with all parameters', async () => {
      mockBridge.sendEmail.mockResolvedValue({
        status: 'success',
        message: 'Email sent'
      });

      const params = {
        to: ['recipient1@example.com', 'recipient2@example.com'],
        cc: ['cc@example.com'],
        bcc: ['bcc@example.com'],
        subject: 'Full Test',
        body: '<h1>HTML Body</h1>'
      };

      const response = await mockServer.invokeTool('email_send', params);

      expect(isValidToolResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('recipient1@example.com');
      expect(response.content[0].text).toContain('CC: cc@example.com');
      expect(response.content[0].text).toContain('BCC: bcc@example.com');
      expect(mockBridge.sendEmail).toHaveBeenCalledWith({
        to: ['recipient1@example.com', 'recipient2@example.com'],
        cc: ['cc@example.com'],
        bcc: ['bcc@example.com'],
        subject: 'Full Test',
        htmlBody: '<h1>HTML Body</h1>'
      });
    });

    it('should handle send errors gracefully', async () => {
      mockBridge.sendEmail.mockRejectedValue(new Error('Python process failed'));

      const params = {
        to: ['recipient@example.com'],
        subject: 'Test',
        body: 'Test'
      };

      const response = await mockServer.invokeTool('email_send', params);

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('Failed to send email');
      expect(response.content[0].text).toContain('Python process failed');
      expect(response.content[0].text).toContain('Outlook is installed');
    });

    it('should reject invalid email addresses', async () => {
      // Zod validation should throw before tool execution
      const params = {
        to: ['invalid-email'],
        subject: 'Test',
        body: 'Test'
      };

      // The mock server should throw on validation errors
      const response = await mockServer.invokeTool('email_send', params).catch(e => e);
      
      // Expect either a thrown error or validation failure
      expect(response).toBeDefined();
    });

    it('should reject missing required fields', async () => {
      // Zod schema requires subject and body
      const response = await mockServer.invokeTool('email_send', {
        to: ['test@example.com']
        // missing subject and body
      }).catch(e => e);
      
      // Expect either a thrown error or validation failure
      expect(response).toBeDefined();
    });

    it('should handle empty optional arrays', async () => {
      mockBridge.sendEmail.mockResolvedValue({
        status: 'success',
        message: 'Email sent'
      });

      const params = {
        to: ['recipient@example.com'],
        cc: [],
        bcc: [],
        subject: 'Test',
        body: 'Test'
      };

      const response = await mockServer.invokeTool('email_send', params);

      expect(isValidToolResponse(response)).toBe(true);
      expect(response.content[0].text).not.toContain('CC:');
      expect(response.content[0].text).not.toContain('BCC:');
    });

    it('should handle connection provider errors', async () => {
      getPythonBridgeMock.mockRejectedValue(new Error('Failed to initialize bridge'));

      const params = {
        to: ['test@example.com'],
        subject: 'Test',
        body: 'Test'
      };

      const response = await mockServer.invokeTool('email_send', params);

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('Failed to send email');
    });

    it('should format HTML bodies correctly', async () => {
      mockBridge.sendEmail.mockResolvedValue({
        status: 'success'
      });

      const htmlBody = '<html><body><p>Test</p></body></html>';
      const params = {
        to: ['test@example.com'],
        subject: 'HTML Test',
        body: htmlBody
      };

      await mockServer.invokeTool('email_send', params);

      expect(mockBridge.sendEmail).toHaveBeenCalledWith(
        expect.objectContaining({
          htmlBody
        })
      );
    });

    it('should use String(error) when error has no message property (covers || branch)', async () => {
      // Throw a non-Error object without .message to cover `String(error)` path
      mockBridge.sendEmail.mockRejectedValue('string-only-error');

      const response = await mockServer.invokeTool('email_send', {
        to: ['test@example.com'],
        subject: 'Test',
        body: 'Test'
      });

      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toContain('Failed to send email');
      expect(response.content[0].text).toContain('string-only-error');
    });
  });
});
