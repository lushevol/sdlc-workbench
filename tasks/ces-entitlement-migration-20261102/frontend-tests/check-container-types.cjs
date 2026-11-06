// Check the adapter's TypeScript types with explicit shared-module substitutes.
// This is not the owning application's complete declaration build.
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");
const root = path.resolve(__dirname, "../../..");
const repo = path.join(root, "repos/ui/mfe-ratan-container");
const ts = require(require.resolve("typescript", {
  paths: [path.join(root, "repos/ui/mfe-base"), repo],
}));
const selected = [
  "src/ratanutils/authenticator.ts",
  "src/ratanutils/roleOwnership.ts",
  "src/Root/routing/common/interface.ts",
  "src/packages/Analysis/v2/User/utils.ts",
];
const virtual = new Map([
  [path.join(repo, ".ces-typecheck/hooks.d.ts"), "export const Hooks: { getHooks(): { store?: any } };"],
  [path.join(repo, ".ces-typecheck/monitor.d.ts"), "export class MonitorUser {}"],
  [path.join(repo, ".ces-typecheck/crypto.d.ts"), "export function encode(value: string): string;"],
]);
const options = {
  target: ts.ScriptTarget.ES2020,
  module: ts.ModuleKind.ESNext,
  moduleResolution: ts.ModuleResolutionKind.NodeJs,
  strict: true,
  noImplicitAny: false,
  skipLibCheck: true,
  noEmit: true,
  types: ["react"],
  typeRoots: [path.join(root, "repos/ui/mfe-base/node_modules/@types")],
};
const host = ts.createCompilerHost(options);
const read = host.readFile.bind(host);
const exists = host.fileExists.bind(host);
host.readFile = file => virtual.get(file) ?? read(file);
host.fileExists = file => virtual.has(file) || exists(file);
host.getSourceFile = (file, languageVersion) => {
  const source = host.readFile(file);
  return source === undefined ? undefined : ts.createSourceFile(file, source, languageVersion, true);
};
host.resolveModuleNames = (names, containing) => names.map(name => {
  let stub;
  if (containing.endsWith("/ratanutils/authenticator.ts") && name === "../Root/import") stub = "hooks";
  if (containing.endsWith("/User/utils.ts")) {
    if (name === "../import") stub = "hooks";
    if (name === "./index") stub = "monitor";
    if (name === "../Storage/crypto") stub = "crypto";
  }
  return stub
    ? { resolvedFileName: path.join(repo, `.ces-typecheck/${stub}.d.ts`), extension: ts.Extension.Dts }
    : ts.resolveModuleName(name, containing, options, host).resolvedModule;
});
const program = ts.createProgram(selected.map(file => path.join(repo, file)), options, host);
const diagnostics = ts.getPreEmitDiagnostics(program).map(item => ({
  code: item.code,
  file: item.file ? path.relative(root, item.file.fileName) : null,
  line: item.file && item.start !== undefined ? item.file.getLineAndCharacterOfPosition(item.start).line + 1 : null,
  message: ts.flattenDiagnosticMessageText(item.messageText, " "),
}));
const sha = bytes => crypto.createHash("sha256").update(bytes).digest("hex");
const result = {
  status: diagnostics.length ? "FAILED" : "PASSED",
  node: process.version,
  typescript: ts.version,
  sources: selected.map(file => ({ path: path.relative(root, path.join(repo, file)), sha256: sha(fs.readFileSync(path.join(repo, file))) })),
  substituted_boundaries: [...virtual].map(([file, declaration]) => ({ name: path.basename(file), declaration })),
  diagnostics,
  limits: [
    "Four selected production source files only; shared Hooks, MonitorUser, and crypto boundaries use declared substitutes.",
    "This does not type-check the complete container, UI components, consuming applications, or installed @fm/base package.",
    "The container has no local node_modules; cached existing mfe-base TypeScript is reused without downloads.",
  ],
};
const output = path.join(
  process.env.CES_TEST_OUTPUT
    ? path.resolve(root, process.env.CES_TEST_OUTPUT)
    : path.join(__dirname, "../evidence/frontend-entitlement-implementation-20261106"),
  "container-types.json"
);
fs.writeFileSync(output, JSON.stringify(result, null, 2) + "\n");
console.log(JSON.stringify(result, null, 2));
process.exitCode = diagnostics.length ? 1 : 0;
