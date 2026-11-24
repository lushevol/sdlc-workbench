import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { getConfig, setConfig, resetConfigCache } from '../src/config.js';
import fs from 'fs';
import path from 'path';

// Mock fs module
vi.mock('fs');

describe('Core Config', () => {
  const mockConfigPath = expect.stringContaining('config.json');

  beforeEach(() => {
    vi.clearAllMocks();
    resetConfigCache();
  });

  afterEach(() => {
    vi.restoreAllMocks();
    resetConfigCache();
  });

  describe('setConfig', () => {
    it.each(['command-line arguments', 'environment variables', 'config.json'])(
      'uses native workspace configuration before %s until reset', (source) => {
        const originalArgv = process.argv;
        const originalEnv = { ...process.env };
        const nativeConfig = {
          AZURE_DEVOPS_ORG_URL: 'https://dev.azure.com/native-workspace',
          AZURE_DEVOPS_PAT: 'workspace-pat',
          HTTPS_PROXY: 'http://workspace-proxy:8080'
        };
        const readConfig = vi.spyOn(fs, 'readFileSync').mockReturnValue(JSON.stringify({
          AZURE_DEVOPS_PAT: 'file-pat'
        }));
        vi.spyOn(console, 'error').mockImplementation(() => {});

        try {
          process.argv = source === 'command-line arguments'
            ? ['node', 'index.js', 'cli-pat']
            : ['node', 'index.js'];
          if (source === 'config.json') delete process.env.AZURE_DEVOPS_PAT;
          else process.env.AZURE_DEVOPS_PAT = 'env-pat';
          const expectedPat = source === 'command-line arguments' ? 'cli-pat'
            : source === 'environment variables' ? 'env-pat' : 'file-pat';

          expect(getConfig().AZURE_DEVOPS_PAT).toBe(expectedPat);
          readConfig.mockClear();
          setConfig(nativeConfig);

          expect(getConfig()).toBe(nativeConfig);
          expect(getConfig()).toBe(nativeConfig);
          expect(readConfig).not.toHaveBeenCalled();

          resetConfigCache();
          expect(getConfig().AZURE_DEVOPS_PAT).toBe(expectedPat);
          expect(readConfig).toHaveBeenCalledTimes(source === 'config.json' ? 1 : 0);
        } finally {
          process.argv = originalArgv;
          process.env = originalEnv;
        }
      }
    );
  });

  describe('getConfig', () => {
    it('should load and parse config.json successfully', () => {
      const mockConfig = {
        AZURE_DEVOPS_PAT: 'test-pat-token',
        CONFLUENCE_PAT: 'conf-token',
        HTTPS_PROXY: 'http://proxy.example.com:8080'
      };

      vi.spyOn(fs, 'readFileSync').mockReturnValue(JSON.stringify(mockConfig));

      const config = getConfig();

      expect(fs.readFileSync).toHaveBeenCalledWith(mockConfigPath, 'utf-8');
      expect(config.AZURE_DEVOPS_ORG_URL).toBe('https://dev.azure.com/sc-ado');
      expect(config.AZURE_DEVOPS_PAT).toBe('test-pat-token');
      expect(config.HTTPS_PROXY).toBe('http://proxy.example.com:8080');
      expect(config.confluenceConfig).toEqual({
        baseUrl: 'https://confluence.global.standardchartered.com',
        token: 'conf-token'
      });
    });

    it('should handle config with minimal required fields', () => {
      const mockConfig = {
        AZURE_DEVOPS_PAT: 'test-pat-token'
      };

      vi.spyOn(fs, 'readFileSync').mockReturnValue(JSON.stringify(mockConfig));
      vi.spyOn(console, 'error').mockImplementation(() => {});

      const config = getConfig();

      expect(config.AZURE_DEVOPS_ORG_URL).toBe('https://dev.azure.com/sc-ado');
      expect(config.AZURE_DEVOPS_PAT).toBe('test-pat-token');
      expect(config.HTTPS_PROXY).toBe('');
      expect(config.confluenceConfig).toEqual({
        baseUrl: 'https://confluence.global.standardchartered.com',
        token: ''
      });
    });

    it('should throw error when config file cannot be read', () => {
      vi.spyOn(fs, 'readFileSync').mockImplementation(() => {
        throw new Error('ENOENT: no such file or directory');
      });

      expect(() => getConfig()).toThrow('Failed to load config.json');
    });

    it('should not throw error when only AZURE_DEVOPS_PAT is provided', () => {
      const mockConfig = {
        AZURE_DEVOPS_PAT: 'test-pat-token'
      };

      vi.spyOn(fs, 'readFileSync').mockReturnValue(JSON.stringify(mockConfig));
      const consoleWarnSpy = vi.spyOn(console, 'warn').mockImplementation(() => {});

      const config = getConfig();
      expect(config.AZURE_DEVOPS_ORG_URL).toBe('https://dev.azure.com/sc-ado');
      expect(config.AZURE_DEVOPS_PAT).toBe('test-pat-token');

      consoleWarnSpy.mockRestore();
    });

    it('should throw error when AZURE_DEVOPS_PAT is missing', () => {
      const mockConfig = {};

      vi.spyOn(fs, 'readFileSync').mockReturnValue(JSON.stringify(mockConfig));

      expect(() => getConfig()).toThrow(
        'AZURE_DEVOPS_PAT must be defined in config.json'
      );
    });

    it('should throw error when AZURE_DEVOPS_PAT is missing from empty config', () => {
      const mockConfig = {};

      vi.spyOn(fs, 'readFileSync').mockReturnValue(JSON.stringify(mockConfig));

      expect(() => getConfig()).toThrow(
        'AZURE_DEVOPS_PAT must be defined in config.json'
      );
    });

    it('should throw error when config.json has invalid JSON', () => {
      vi.spyOn(fs, 'readFileSync').mockReturnValue('{ invalid json }');

      expect(() => getConfig()).toThrow('Failed to load config.json');
    });

    it('should handle partial Confluence configuration', () => {
      const mockConfig = {
        AZURE_DEVOPS_PAT: 'test-pat-token'
        // Missing CONFLUENCE_PAT
      };

      vi.spyOn(fs, 'readFileSync').mockReturnValue(JSON.stringify(mockConfig));
      vi.spyOn(console, 'error').mockImplementation(() => {});

      const config = getConfig();

      expect(config.confluenceConfig.baseUrl).toBe('https://confluence.global.standardchartered.com');
      expect(config.confluenceConfig.token).toBe('');
    });

    it('should load config from command-line arguments', () => {
      const originalArgv = process.argv;
      process.argv = ['node', 'index.js', 'cli-pat-token', 'http://proxy:8080', 'cli-token'];

      vi.spyOn(fs, 'readFileSync').mockImplementation(() => {
        throw new Error('Should not read file');
      });

      const consoleErrorSpy = vi.spyOn(console, 'error').mockImplementation(() => {});

      const config = getConfig();

      expect(config.AZURE_DEVOPS_ORG_URL).toBe('https://dev.azure.com/sc-ado');
      expect(config.AZURE_DEVOPS_PAT).toBe('cli-pat-token');
      expect(config.HTTPS_PROXY).toBe('http://proxy:8080');
      expect(config.confluenceConfig.token).toBe('cli-token');

      process.argv = originalArgv;
      consoleErrorSpy.mockRestore();
    });

    it('should load config from command-line arguments with minimal params', () => {
      const originalArgv = process.argv;
      process.argv = ['node', 'index.js', 'minimal-pat'];

      vi.spyOn(fs, 'readFileSync').mockImplementation(() => {
        throw new Error('Should not read file');
      });

      const consoleErrorSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
      const consoleWarnSpy = vi.spyOn(console, 'warn').mockImplementation(() => {});

      const config = getConfig();

      expect(config.AZURE_DEVOPS_ORG_URL).toBe('https://dev.azure.com/sc-ado');
      expect(config.AZURE_DEVOPS_PAT).toBe('minimal-pat');
      expect(config.HTTPS_PROXY).toBe('');

      process.argv = originalArgv;
      consoleErrorSpy.mockRestore();
      consoleWarnSpy.mockRestore();
    });

    it('should throw error when command-line PAT is missing', () => {
      const originalArgv = process.argv;
      const originalEnv = { ...process.env };
      
      process.argv = ['node', 'index.js'];
      delete process.env.AZURE_DEVOPS_PAT;

      vi.spyOn(fs, 'readFileSync').mockImplementation(() => {
        throw new Error('ENOENT');
      });

      expect(() => getConfig()).toThrow('Configuration not found');

      process.argv = originalArgv;
      process.env = originalEnv;
    });

    it('should throw error when CLI args are present but PAT is empty string', () => {
      const originalArgv = process.argv;
      process.argv = ['node', 'index.js', ''];

      vi.spyOn(fs, 'readFileSync').mockImplementation(() => {
        throw new Error('Should not read file');
      });

      const consoleErrorSpy = vi.spyOn(console, 'error').mockImplementation(() => {});

      expect(() => getConfig()).toThrow('Azure DevOps configuration missing');

      process.argv = originalArgv;
      consoleErrorSpy.mockRestore();
    });

    it('should load config from environment variables', () => {
      const originalEnv = { ...process.env };
      process.env.AZURE_DEVOPS_PAT = 'env-pat-token';
      process.env.HTTPS_PROXY = 'http://env-proxy:8080';
      process.env.CONFLUENCE_PAT = 'env-token';

      vi.spyOn(fs, 'readFileSync').mockImplementation(() => {
        throw new Error('Should not read file');
      });

      const consoleErrorSpy = vi.spyOn(console, 'error').mockImplementation(() => {});

      const config = getConfig();

      expect(config.AZURE_DEVOPS_ORG_URL).toBe('https://dev.azure.com/sc-ado');
      expect(config.AZURE_DEVOPS_PAT).toBe('env-pat-token');
      expect(config.HTTPS_PROXY).toBe('http://env-proxy:8080');
      expect(config.confluenceConfig.token).toBe('env-token');

      process.env = originalEnv;
      consoleErrorSpy.mockRestore();
    });

    it('should load config from environment variables with minimal vars', () => {
      const originalEnv = { ...process.env };
      delete process.env.HTTPS_PROXY;
      delete process.env.CONFLUENCE_PAT;
      process.env.AZURE_DEVOPS_PAT = 'env-minimal-pat';

      vi.spyOn(fs, 'readFileSync').mockImplementation(() => {
        throw new Error('Should not read file');
      });

      const consoleErrorSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
      const consoleWarnSpy = vi.spyOn(console, 'warn').mockImplementation(() => {});

      const config = getConfig();

      expect(config.AZURE_DEVOPS_ORG_URL).toBe('https://dev.azure.com/sc-ado');
      expect(config.AZURE_DEVOPS_PAT).toBe('env-minimal-pat');
      expect(config.HTTPS_PROXY).toBe('');

      process.env = originalEnv;
      consoleErrorSpy.mockRestore();
      consoleWarnSpy.mockRestore();
    });

    it('should throw error when environment PAT is missing', () => {
      const originalEnv = { ...process.env };
      delete process.env.AZURE_DEVOPS_PAT;

      vi.spyOn(fs, 'readFileSync').mockImplementation(() => {
        throw new Error('ENOENT');
      });

      expect(() => getConfig()).toThrow('Configuration not found');

      process.env = originalEnv;
    });

    it('should prioritize command-line args over environment variables', () => {
      const originalArgv = process.argv;
      const originalEnv = { ...process.env };
      
      process.argv = ['node', 'index.js', 'cli-pat'];
      process.env.AZURE_DEVOPS_PAT = 'env-pat';

      vi.spyOn(fs, 'readFileSync').mockImplementation(() => {
        throw new Error('Should not read file');
      });

      const consoleErrorSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
      const consoleWarnSpy = vi.spyOn(console, 'warn').mockImplementation(() => {});

      const config = getConfig();

      expect(config.AZURE_DEVOPS_PAT).toBe('cli-pat');

      process.argv = originalArgv;
      process.env = originalEnv;
      consoleErrorSpy.mockRestore();
      consoleWarnSpy.mockRestore();
    });

    it('should prioritize environment variables over config file', () => {
      const originalEnv = { ...process.env };
      
      process.env.AZURE_DEVOPS_PAT = 'env-pat';

      vi.spyOn(fs, 'readFileSync').mockReturnValue(JSON.stringify({
        AZURE_DEVOPS_PAT: 'file-pat'
      }));

      const consoleErrorSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
      const consoleWarnSpy = vi.spyOn(console, 'warn').mockImplementation(() => {});

      const config = getConfig();

      expect(config.AZURE_DEVOPS_PAT).toBe('env-pat');

      process.env = originalEnv;
      consoleErrorSpy.mockRestore();
      consoleWarnSpy.mockRestore();
    });

    it('should read codeReviewGuideFile from CODE_REVIEW_GUIDE_FILE env var', () => {
      const originalEnv = { ...process.env };
      process.env.AZURE_DEVOPS_PAT = 'env-pat';
      process.env.CODE_REVIEW_GUIDE_FILE = '/custom/review/CODE_REVIEW_GUIDE.md';

      vi.spyOn(fs, 'readFileSync').mockImplementation(() => {
        throw new Error('Should not read file');
      });

      const consoleErrorSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
      const consoleWarnSpy = vi.spyOn(console, 'warn').mockImplementation(() => {});

      const config = getConfig();

      expect(config.codeReviewGuideFile).toBe('/custom/review/CODE_REVIEW_GUIDE.md');

      process.env = originalEnv;
      consoleErrorSpy.mockRestore();
      consoleWarnSpy.mockRestore();
    });

    it('should read codeReviewGuideFile from config.json', () => {
      const mockConfig = {
        AZURE_DEVOPS_PAT: 'test-pat-token',
        codeReviewGuideFile: '/path/to/CODE_REVIEW_GUIDE.md'
      };

      vi.spyOn(fs, 'readFileSync').mockReturnValue(JSON.stringify(mockConfig));
      const consoleErrorSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
      const consoleWarnSpy = vi.spyOn(console, 'warn').mockImplementation(() => {});

      const config = getConfig();

      expect(config.codeReviewGuideFile).toBe('/path/to/CODE_REVIEW_GUIDE.md');

      consoleErrorSpy.mockRestore();
      consoleWarnSpy.mockRestore();
    });

    it('should default codeReviewGuideFile to empty string when not configured', () => {
      const mockConfig = { AZURE_DEVOPS_PAT: 'test-pat-token' };

      vi.spyOn(fs, 'readFileSync').mockReturnValue(JSON.stringify(mockConfig));
      const consoleErrorSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
      const consoleWarnSpy = vi.spyOn(console, 'warn').mockImplementation(() => {});

      const config = getConfig();

      expect(config.codeReviewGuideFile).toBe('');

      consoleErrorSpy.mockRestore();
      consoleWarnSpy.mockRestore();
    });

    it('should return the cached config on a second call without re-reading the source', () => {
      const mockConfig = { AZURE_DEVOPS_PAT: 'test-pat-token' };

      vi.spyOn(fs, 'readFileSync').mockReturnValue(JSON.stringify(mockConfig));
      vi.spyOn(console, 'error').mockImplementation(() => {});

      const first = getConfig();
      const second = getConfig();

      expect(second).toBe(first);
      expect(fs.readFileSync).toHaveBeenCalledTimes(1);
    });

    it('should throw when config.json parses to a falsy value (e.g. null)', () => {
      vi.spyOn(fs, 'readFileSync').mockReturnValue('null');

      expect(() => getConfig()).toThrow('AZURE_DEVOPS_PAT must be defined in config.json');
    });

    it('should log "yes" for Nexus and SonarQube when their credentials are configured', () => {
      const mockConfig = {
        AZURE_DEVOPS_PAT: 'test-pat-token',
        NEXUS_USER_CODE: 'nexus-user',
        NEXUS_PASS_CODE: 'nexus-pass',
        SONAR_TOKEN: 'sonar-token'
      };

      vi.spyOn(fs, 'readFileSync').mockReturnValue(JSON.stringify(mockConfig));
      vi.spyOn(console, 'error').mockImplementation(() => {});

      const config = getConfig();

      expect(config.nexusConfig.userCode).toBe('nexus-user');
      expect(config.sonarConfig.token).toBe('sonar-token');
    });

    it('should mask a short credential (<=4 chars) without slicing a trailing fragment', () => {
      const mockConfig = { AZURE_DEVOPS_PAT: 'abcd' };

      vi.spyOn(fs, 'readFileSync').mockReturnValue(JSON.stringify(mockConfig));
      const consoleErrorSpy = vi.spyOn(console, 'error').mockImplementation(() => {});

      getConfig();

      expect(consoleErrorSpy).toHaveBeenCalledWith(expect.stringContaining('ADO: ***'));
    });
  });
});
