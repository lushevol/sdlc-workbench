import { describe, it, expect, vi, beforeEach } from 'vitest';
import { configureScwikiPrompts, SCWIKI_PROMPTS } from '../src/prompts.js';

describe('SC Wiki Prompts', () => {
  let mockServer;

  beforeEach(() => {
    mockServer = { prompt: vi.fn() };
  });

  describe('SCWIKI_PROMPTS constant', () => {
    it('should export SCWIKI_PROMPTS object', () => {
      expect(SCWIKI_PROMPTS).toBeDefined();
      expect(typeof SCWIKI_PROMPTS).toBe('object');
    });

    it('should contain 14 prompts', () => {
      expect(Object.keys(SCWIKI_PROMPTS)).toHaveLength(14);
    });

    it('each prompt should have name, description, and arguments array', () => {
      Object.values(SCWIKI_PROMPTS).forEach(prompt => {
        expect(prompt.name).toBeDefined();
        expect(typeof prompt.name).toBe('string');
        expect(prompt.description).toBeDefined();
        expect(Array.isArray(prompt.arguments)).toBe(true);
      });
    });

    it('prompt names should all be unique', () => {
      const names = Object.values(SCWIKI_PROMPTS).map(p => p.name);
      const uniqueNames = new Set(names);
      expect(uniqueNames.size).toBe(names.length);
    });

    it('SEARCH_SCWIKI should have a required query argument', () => {
      const arg = SCWIKI_PROMPTS.SEARCH_SCWIKI.arguments.find(a => a.name === 'query');
      expect(arg).toBeDefined();
      expect(arg.required).toBe(true);
    });

    it('UPDATE_SCWIKI_PAGE should have optional title and content arguments', () => {
      const titleArg = SCWIKI_PROMPTS.UPDATE_SCWIKI_PAGE.arguments.find(a => a.name === 'title');
      const contentArg = SCWIKI_PROMPTS.UPDATE_SCWIKI_PAGE.arguments.find(a => a.name === 'content');
      expect(titleArg.required).toBe(false);
      expect(contentArg.required).toBe(false);
    });

    it('DELETE_SCWIKI_PAGE should have required pageReference and title arguments', () => {
      const refArg = SCWIKI_PROMPTS.DELETE_SCWIKI_PAGE.arguments.find(a => a.name === 'pageReference');
      const titleArg = SCWIKI_PROMPTS.DELETE_SCWIKI_PAGE.arguments.find(a => a.name === 'title');
      expect(refArg.required).toBe(true);
      expect(titleArg.required).toBe(true);
    });
  });

  describe('configureScwikiPrompts()', () => {
    it('should register all 14 prompts on the server', () => {
      configureScwikiPrompts(mockServer);
      expect(mockServer.prompt).toHaveBeenCalledTimes(14);
    });

    it('should not throw when invoked', () => {
      expect(() => configureScwikiPrompts(mockServer)).not.toThrow();
    });

    it('each registered prompt callback should return a message with all optional args present', async () => {
      configureScwikiPrompts(mockServer);
      const fullArgs = {
        query: 'x', pageReference: 'Sandbox.WebHome', pageUrl: 'https://x', title: 'T',
        text: 'x', tag: 't', content: 'c', limit: '5'
      };
      for (const call of mockServer.prompt.mock.calls) {
        const callback = call[call.length - 1];
        const result = await callback(fullArgs);
        expect(result.messages[0].content.text).toEqual(expect.any(String));
      }
    });

    it('each registered prompt callback should return a message with all optional args absent', async () => {
      configureScwikiPrompts(mockServer);
      for (const call of mockServer.prompt.mock.calls) {
        const callback = call[call.length - 1];
        const result = await callback({});
        expect(result.messages[0].content.text).toEqual(expect.any(String));
      }
    });
  });
});
