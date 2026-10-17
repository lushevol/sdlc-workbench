import js from '@eslint/js';
import security from 'eslint-plugin-security';

export default [
  {
    ignores: [
      '**/node_modules/**',
      '**/dist/**',
      '**/coverage/**',
      '**/reports/**',
      '**/src/tempRepos/**',
      '**/nexus-report/**',
      'docs/**'
    ]
  },
  js.configs.recommended,
  {
    plugins: { security },
    rules: {
      ...security.configs.recommended.rules,
      // Extremely noisy on ordinary bracket-notation property access; the repo's
      // real command-injection risks are caught by detect-child-process instead.
      'security/detect-object-injection': 'off',
      'no-unused-vars': 'warn',
      'no-console': 'off'
    },
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: 'module',
      globals: {
        process: 'readonly',
        console: 'readonly',
        Buffer: 'readonly',
        __dirname: 'readonly',
        __filename: 'readonly',
        module: 'readonly',
        require: 'readonly',
        setTimeout: 'readonly',
        setInterval: 'readonly',
        clearTimeout: 'readonly',
        clearInterval: 'readonly',
        URL: 'readonly',
        fetch: 'readonly'
      }
    }
  },
  {
    files: ['**/tests/**/*.js', '**/*.test.js'],
    languageOptions: {
      globals: {
        describe: 'readonly',
        it: 'readonly',
        test: 'readonly',
        expect: 'readonly',
        beforeEach: 'readonly',
        afterEach: 'readonly',
        beforeAll: 'readonly',
        afterAll: 'readonly',
        vi: 'readonly'
      }
    },
    rules: {
      // Test mocks routinely need child_process/fs mocking patterns that trip these.
      'security/detect-child-process': 'off',
      'security/detect-non-literal-fs-filename': 'off'
    }
  },
  {
    // Browser-side UI code for the ado-upload-app embedded panel (runs in a
    // webview, not Node.js).
    files: ['packages/ado-upload-app/src/app/**/*.js'],
    languageOptions: {
      globals: {
        document: 'readonly',
        window: 'readonly',
        navigator: 'readonly',
        FileReader: 'readonly',
        File: 'readonly',
        FormData: 'readonly',
        fetch: 'readonly'
      }
    }
  }
];
