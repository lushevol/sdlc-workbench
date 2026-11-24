const path = require('path');
require("/private/tmp/mfe-base-ut-20261020/node_modules/ts-node").register({compiler: "/private/tmp/mfe-base-ut-20261020/extra-deps/node_modules/typescript", transpileOnly: true, skipProject: true, compilerOptions: {module: 'commonjs'}});
const original = require("/Users/lushevol/code/github/ratan-release-impact/workbench/repos/ui/mfe-base/jest.config.ts").default;
module.exports = {
  ...original,
  rootDir: "/Users/lushevol/code/github/ratan-release-impact/workbench/repos/ui/mfe-base",
  cacheDirectory: "/private/tmp/mfe-base-ut-20261020/jest-cache",
  coverageDirectory: "/private/tmp/mfe-base-ut-20261020/coverage",
  reporters: ['default'],
  moduleDirectories: ['node_modules'],
  modulePaths: ["/private/tmp/mfe-base-ut-20261020/extra-deps/node_modules", "/private/tmp/mfe-base-ut-20261020/node_modules"],
  moduleNameMapper: {
    ...original.moduleNameMapper,
    '^@sctoolkit/webkit/elements/sc-button$': "/private/tmp/mfe-base-ut-20261020/empty-toolkit.cjs",
    '^@sctoolkit/webkit/elements/sc-icon-card$': "/private/tmp/mfe-base-ut-20261020/empty-toolkit.cjs"
  }
};
