// Reuse installed application test dependencies. This config performs no downloads.
const path = require("path");
const workbenchRoot = path.resolve(__dirname, "../../..");
const container = path.join(workbenchRoot, "repos/ui/mfe-ratan-container");
const base = path.join(workbenchRoot, "repos/ui/mfe-base");
const dependency = name => require.resolve(name, { paths: [container, base] });

module.exports = {
  rootDir: container,
  testEnvironment: "node",
  testMatch: [
    "**/authenticator.ces.test.ts",
    "**/authenticator.logging.test.ts",
    "**/authenticator.test.ts",
    "**/authenticator[01].test.ts",
    "**/authenticator.xratanone.test.ts",
    "**/User/utils.ces.test.ts",
    "**/roleOwnership.ces.test.ts",
    "**/roleOwnership.ui.ces.test.tsx",
  ],
  moduleDirectories: ["node_modules", path.join(base, "node_modules")],
  setupFilesAfterEnv: [path.join(__dirname, "container-hooks.setup.cjs")],
  transform: {
    "^.+\\.(j|t)sx?$": [dependency("babel-jest"), {
      babelrc: false,
      configFile: false,
      presets: [
        [dependency("@babel/preset-env"), { targets: { node: "current" } }],
        dependency("@babel/preset-typescript"),
        [dependency("@babel/preset-react"), { runtime: "automatic" }],
      ],
    }],
  },
};
