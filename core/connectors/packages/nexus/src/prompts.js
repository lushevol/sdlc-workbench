import { z } from 'zod';

const NEXUS_PROMPTS = {
  NEXUS_SCAN: {
    name: 'nexus-vulnerability-scan',
    description: 'Scan local npm dependencies for security vulnerabilities using Nexus IQ. Node.js (npm/yarn) projects only — reads package.json and node_modules. Supports 4 patterns driven by prompt keywords — see pattern argument.',
    arguments: [
      { name: 'applicationId', description: 'Nexus IQ application ID (format: ITAM__ENV__REPO_NAME)', required: true },
      {
        name: 'pattern',
        description: [
          'Scan pattern derived from the user prompt keyword:',
          '  scan           → "Scan for nexus vulnerability"            — pipeline-aligned, no fix',
          '  scan-fix       → "Scan for nexus vulnerability and fix"    — pipeline-aligned + auto-fix',
          '  deep-scan      → "Deep Scan for nexus vulnerability"       — exhaustive (all deps), no fix',
          '  deep-scan-fix  → "Deep Scan for nexus vulnerability and fix" — exhaustive + auto-fix',
          'Default: scan',
        ].join('\n'),
        required: false
      }
    ]
  }
};

const generateNexusPromptMessage = (name, args, ctx) => {
  const branch   = args.branch        || ctx?.ado?.defaultBranch;
  const nexusApp = args.applicationId || ctx?.repositories?.find(r => r.isDefault)?.nexusAppId;
  if (name === 'nexus-vulnerability-scan') {
      const pattern  = (args.pattern || 'scan').toLowerCase().replaceAll(/[\s_]+/g, '-');
      const isDeep   = pattern.includes('deep');
      const isFix    = pattern.includes('fix');
      const modeLabel = isDeep
        ? 'Deep Scan — all dependencies including devDependencies, all CVEs and sonatype-* findings, no filters'
        : 'Pipeline-aligned Scan — production dependencies only, sonatype-* excluded, CVSS ≥ 4.0, matches ADO pipeline';
      const depScope = isDeep ? 'all' : 'production';
      const filterNote = isDeep
        ? 'report ALL findings (no filters — includes sonatype-* IDs, devDependency CVEs, and low/informational)'
        : 'apply pipeline-aligned filters: production deps only, CVSS ≥ 4.0, sonatype-* proprietary IDs excluded';
      const fixStep = isFix
        ? `\n5. After the scan completes, call nexus_fix_vulnerabilities to automatically remediate actionable vulnerabilities`
        : '';
      const deepModeArg = isDeep ? `\n- deepMode: true` : '';
      const scanBranch = args.branch || branch || 'develop';
      return `Scan local npm dependencies for security vulnerabilities using Nexus IQ (Node.js/npm/yarn projects only):\n\nApplication ID: ${nexusApp || args.applicationId}\nBranch: ${scanBranch}\nScan Mode: ${modeLabel}\n\n> **Scope:** This tool reads the local \`package.json\` and \`node_modules\` from the project directory. It supports Node.js projects using npm or yarn. Other ecosystems (Maven, pip, NuGet, etc.) are not currently supported.\n\nUse nexus_scan_vulnerabilities with:\n- applicationId: "${nexusApp || args.applicationId}"${deepModeArg}\n\nThe tool will:\n1. Run yarn/npm install to ensure node_modules reflects the current lockfile\n2. Parse local package.json and node_modules for ${depScope} dependencies\n3. Submit components to Nexus IQ for policy evaluation\n4. ${filterNote}${fixStep}\n\nAfter the scan, reports are generated in JSON, Markdown, and HTML formats and the HTML opens in the browser automatically.\nReturn a vulnerability summary grouped by severity (Critical / High / Medium / Low).`;
  }
  return 'Unknown prompt';
};

const CONTEXTUAL_OPTIONAL_FIELDS = new Set(['project', 'team', 'repository', 'repositoryId', 'applicationId']);

export function configureNexusPrompts(server, { getContext = () => null } = {}) {
  Object.values(NEXUS_PROMPTS).forEach(prompt => {
    const callback = async (args) => {
      const ctx = getContext();
      const message = generateNexusPromptMessage(prompt.name, args ?? {}, ctx);
      return { messages: [{ role: 'user', content: { type: 'text', text: message } }] };
    };
    if (prompt.arguments.length === 0) {
      server.prompt(prompt.name, prompt.description, callback);
    } else {
      const argsSchema = Object.fromEntries(
        prompt.arguments.map(arg => [
          arg.name,
          (!arg.required || CONTEXTUAL_OPTIONAL_FIELDS.has(arg.name))
            ? z.string().optional().describe(arg.description)
            : z.string().describe(arg.description)
        ])
      );
      server.prompt(prompt.name, prompt.description, argsSchema, callback);
    }
  });
  console.error(`Registered ${Object.keys(NEXUS_PROMPTS).length} Nexus prompts`);
}

export { NEXUS_PROMPTS };
