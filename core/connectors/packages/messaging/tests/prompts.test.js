import { describe, it, expect, vi, beforeEach } from 'vitest';
import { configureMessagingPrompts, MESSAGING_PROMPTS } from '../src/prompts.js';

describe('Messaging Prompts', () => {
  let mockServer;

  beforeEach(() => {
    mockServer = { prompt: vi.fn() };
  });

  describe('MESSAGING_PROMPTS constant', () => {
    it('should export MESSAGING_PROMPTS object', () => {
      expect(MESSAGING_PROMPTS).toBeDefined();
      expect(typeof MESSAGING_PROMPTS).toBe('object');
    });

    it('should contain 2 prompts', () => {
      expect(Object.keys(MESSAGING_PROMPTS)).toHaveLength(2);
    });

    it('each prompt should have name, description, and arguments array', () => {
      Object.values(MESSAGING_PROMPTS).forEach(prompt => {
        expect(prompt.name).toBeDefined();
        expect(typeof prompt.name).toBe('string');
        expect(prompt.description).toBeDefined();
        expect(Array.isArray(prompt.arguments)).toBe(true);
      });
    });

    it('SEND_EMAIL should have required to, subject, and body arguments', () => {
      const toArg = MESSAGING_PROMPTS.SEND_EMAIL.arguments.find(a => a.name === 'to');
      const subjectArg = MESSAGING_PROMPTS.SEND_EMAIL.arguments.find(a => a.name === 'subject');
      const bodyArg = MESSAGING_PROMPTS.SEND_EMAIL.arguments.find(a => a.name === 'body');
      expect(toArg.required).toBe(true);
      expect(subjectArg.required).toBe(true);
      expect(bodyArg.required).toBe(true);
    });

    it('SEND_EMAIL should have optional cc and bcc arguments', () => {
      const ccArg = MESSAGING_PROMPTS.SEND_EMAIL.arguments.find(a => a.name === 'cc');
      const bccArg = MESSAGING_PROMPTS.SEND_EMAIL.arguments.find(a => a.name === 'bcc');
      expect(ccArg.required).toBe(false);
      expect(bccArg.required).toBe(false);
    });

    it('TEAMS_SEND_CHANNEL_MESSAGE should have required to and message arguments', () => {
      const toArg = MESSAGING_PROMPTS.TEAMS_SEND_CHANNEL_MESSAGE.arguments.find(a => a.name === 'to');
      const msgArg = MESSAGING_PROMPTS.TEAMS_SEND_CHANNEL_MESSAGE.arguments.find(a => a.name === 'message');
      expect(toArg.required).toBe(true);
      expect(msgArg.required).toBe(true);
    });

    it('TEAMS_SEND_CHANNEL_MESSAGE should have optional title argument', () => {
      const titleArg = MESSAGING_PROMPTS.TEAMS_SEND_CHANNEL_MESSAGE.arguments.find(a => a.name === 'title');
      expect(titleArg).toBeDefined();
      expect(titleArg.required).toBe(false);
    });
  });

  describe('configureMessagingPrompts()', () => {
    it('should register all 2 prompts on the server', () => {
      configureMessagingPrompts(mockServer);
      expect(mockServer.prompt).toHaveBeenCalledTimes(2);
    });

    it('should register the send-email prompt', () => {
      configureMessagingPrompts(mockServer);
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'send-email');
      expect(call).toBeDefined();
    });

    it('should register the teams-send-message prompt', () => {
      configureMessagingPrompts(mockServer);
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'teams-send-message');
      expect(call).toBeDefined();
    });

    it('should accept optional getContext parameter', () => {
      const getContext = vi.fn(() => null);
      expect(() => configureMessagingPrompts(mockServer, { getContext })).not.toThrow();
    });

    it('should work without getContext (default null)', () => {
      expect(() => configureMessagingPrompts(mockServer)).not.toThrow();
    });
  });

  describe('generateMessagingPromptMessage (via registered handlers)', () => {
    beforeEach(() => {
      configureMessagingPrompts(mockServer);
    });

    it('should return valid MCP prompt response structure', async () => {
      const call = mockServer.prompt.mock.calls[0];
      const handler = call.at(-1);
      const result = await handler({ to: 'a@b.com', subject: 'Hello', body: 'World' });
      expect(result).toHaveProperty('messages');
      expect(Array.isArray(result.messages)).toBe(true);
      expect(result.messages[0]).toHaveProperty('role', 'user');
      expect(result.messages[0].content).toHaveProperty('type', 'text');
      expect(result.messages[0].content).toHaveProperty('text');
    });

    it('should generate send-email message containing to, subject, and body', async () => {
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'send-email');
      const handler = call.at(-1);
      const result = await handler({ to: 'user@example.com', subject: 'Test Subject', body: 'Test Body' });
      expect(result.messages[0].content.text).toContain('user@example.com');
      expect(result.messages[0].content.text).toContain('Test Subject');
      expect(result.messages[0].content.text).toContain('Test Body');
    });

    it('should include CC in send-email message when cc is provided', async () => {
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'send-email');
      const handler = call.at(-1);
      const result = await handler({ to: 'a@b.com', subject: 'Hi', body: 'Body', cc: 'cc@b.com' });
      expect(result.messages[0].content.text).toContain('cc@b.com');
    });

    it('should include BCC in send-email message when bcc is provided', async () => {
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'send-email');
      const handler = call.at(-1);
      const result = await handler({ to: 'a@b.com', subject: 'Hi', body: 'Body', bcc: 'bcc@b.com' });
      expect(result.messages[0].content.text).toContain('bcc@b.com');
    });

    it('should mention Outlook in send-email message', async () => {
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'send-email');
      const handler = call.at(-1);
      const result = await handler({ to: 'a@b.com', subject: 'S', body: 'B' });
      expect(result.messages[0].content.text).toContain('Outlook');
    });

    it('should generate teams-send-message containing to and message', async () => {
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'teams-send-message');
      const handler = call.at(-1);
      const result = await handler({ to: 'colleague@company.com', message: 'Hello Teams!' });
      expect(result.messages[0].content.text).toContain('colleague@company.com');
      expect(result.messages[0].content.text).toContain('Hello Teams!');
    });

    it('should include title in teams-send-message when provided', async () => {
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'teams-send-message');
      const handler = call.at(-1);
      const result = await handler({ to: 'a@b.com', message: 'Msg', title: 'My Title' });
      expect(result.messages[0].content.text).toContain('My Title');
    });

    it('should mention Teams in teams-send-message', async () => {
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'teams-send-message');
      const handler = call.at(-1);
      const result = await handler({ to: 'a@b.com', message: 'Hello' });
      expect(result.messages[0].content.text).toContain('Teams');
    });

    it('should handle undefined args gracefully', async () => {
      const call = mockServer.prompt.mock.calls.find(c => c[0] === 'send-email');
      const handler = call.at(-1);
      const result = await handler(undefined);
      expect(result.messages[0].content.text).toBeDefined();
      expect(typeof result.messages[0].content.text).toBe('string');
    });
  });
});
