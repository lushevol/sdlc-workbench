const c = require("../../frontend-tests/container-jest.config.cjs");
const path = require("path");
module.exports = {
  ...c,
  rootDir: __dirname,
  testMatch: [path.join(__dirname, "review-legacy-alias.ces.test.ts")],
  moduleNameMapper: {
    "^\\.\\./Root/import$": path.resolve(__dirname, "../../../../repos/ui/mfe-ratan-container/src/Root/import"),
  },
  moduleDirectories: [
    path.resolve(__dirname, "../../../../repos/ui/mfe-base/node_modules"),
    path.resolve(__dirname, "../../../../repos/ui/mfe-ratan-container/node_modules"),
  ],
};
