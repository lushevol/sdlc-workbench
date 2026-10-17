
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    coverage: {
      enabled: true,
      provider: 'v8',
      reporter: ['lcov', 'text-summary', 'cobertura'],
      reportsDirectory: './coverage',
      include: ['src/**/*.js'],
      exclude: ['src/**/*.styles.js', 'src/index.js', 'vitest.config.js', 'tests/**'],
      thresholds: {
        statements: 90,
        branches: 88,
        functions: 90,
        lines: 90
      }
    },
    reporters: [
      [
        'junit',
        {
          suiteName: 'vitest tests',
          outputFile: './reports/tests.xunit.xml',
          classNameTemplate: '{classname}-{title}',
          titleTemplate: '{classname}-{title}',
          ancestorSeparator: ' › ',
          usePathForSuiteName: true
        }
      ]
    ]
  }
});
