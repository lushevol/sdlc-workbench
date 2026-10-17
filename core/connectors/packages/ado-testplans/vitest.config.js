
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    coverage: {
      enabled: true,
      provider: 'v8',
      reporter: ['lcov', 'text-summary', 'cobertura'],
      reportsDirectory: './coverage',
      include: ['src/**/*.js'],
      exclude: ['src/**/*.styles.js', 'src/index.js', 'src/tools.js', 'vitest.config.js'],
      thresholds: {
        statements: 80,
        branches: 80,
        functions: 80,
        lines: 80
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
