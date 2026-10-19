/*
 * For a detailed explanation regarding each configuration property and type check, visit:
 * https://jestjs.io/docs/configuration
 */

export default {
  // The root directory that Jest should scan for tests and modules within
  rootDir: ".",
  coverageDirectory: "./coverage",
  coverageReporters: ["text", "lcov", "cobertura"],
  coverageThreshold: {
    global: {
      branches: 90,
      lines: 90,
    },
  },
  moduleFileExtensions: ["js", "ts", "tsx"],
  moduleNameMapper: {
    "\\.(css)$": "identity-obj-proxy",
    "^.+\\.(jpg|jpeg|png|gif|eot|otf|webp|svg|ttf|woff|woff2|mp4|webm|wav|mp3|m4a|aac|oga)$": "<rootDir>/src/fileMock.js",
    "single-spa-react/parcel": "single-spa-react/lib/cjs/parcel.cjs",
  },
  setupFilesAfterEnv: ["@testing-library/jest-dom", "./jest.setup.tsx"],
  testEnvironment: "jsdom",
  transform: {
    "^.+\\.(j|t)sx?$": "babel-jest",
  },
  reporters: [
    'default',
    [
      'jest-sonar',
      {
        outputDirectory: './coverage',
        outputName: 'sonar-test-report.xml',
        reportedFilePath: 'relative',
      }
    ],
    [
      'jest-junit',
      {
        outputDirectory: './coverage',
        outputName: 'junit-test-report.xml',
        reportedFilePath: 'relative'
      }
    ]
  ],
};
