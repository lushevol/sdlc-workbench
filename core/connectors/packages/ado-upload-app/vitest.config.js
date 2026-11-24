import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    coverage: {
      enabled: true,
      provider: "v8",
      reporter: ["lcov", "text-summary", "cobertura"],
      reportsDirectory: "./coverage",
      include: ["src/**"],
      exclude: [
        "src/server/server.js",  // thin entry-point with top-level await — not importable in tests
        "src/app/mcp-app.js"     // UI glue / DOM entry-point — integration-tested separately
      ],
      thresholds: {
        lines: 90,
        functions: 90,
        branches: 90,
        statements: 90
      }
    },
    reporters: [
      "default",
      [
        "junit",
        {
          suiteName: "vitest tests",
          outputFile: "./reports/tests.xunit.xml",
          classNameTemplate: "{classname}-{title}",
          titleTemplate: "{classname}-{title}",
          ancestorSeparator: " › ",
          usePathForSuiteName: true
        }
      ]
    ]
  }
});
