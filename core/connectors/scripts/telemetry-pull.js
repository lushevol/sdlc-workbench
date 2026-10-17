const TELEMETRY_BRANCH = 'telemetry/usage-log';
const TELEMETRY_FILE = '/usage.log';
const TELEMETRY_PROJECT = 'DDCPQPR';
const TELEMETRY_REPO = '23966-sc-node-mcp';

/**
 * Fetch the raw NDJSON content of usage.log from the ADO telemetry branch.
 *
 * @param {Object} connection - ADO WebApi connection instance
 * @returns {Promise<string>} Raw NDJSON file content
 * @throws {Error} If the branch does not exist or the file cannot be read
 */
export async function fetchTelemetryData(connection) {
  const gitApi = await connection.getGitApi();
  const repository = await gitApi.getRepository(TELEMETRY_REPO, TELEMETRY_PROJECT);
  const repoId = repository.id;

  const refs = await gitApi.getRefs(repoId, TELEMETRY_PROJECT, `heads/${TELEMETRY_BRANCH}`);
  if (!Array.isArray(refs) || refs.length === 0) {
    throw new Error(
      `Branch '${TELEMETRY_BRANCH}' does not exist yet. ` +
      'Start the MCP server at least once to create it.'
    );
  }

  const stream = await gitApi.getItemContent(
    repoId,
    TELEMETRY_FILE,
    TELEMETRY_PROJECT,
    null, null, false, false, false,
    { versionType: 0 /* Branch */, version: TELEMETRY_BRANCH }
  );

  return streamToString(stream);
}

function streamToString(stream) {
  if (Buffer.isBuffer(stream)) return Promise.resolve(stream.toString('utf-8'));
  if (typeof stream === 'string') return Promise.resolve(stream);
  return new Promise((resolve, reject) => {
    const chunks = [];
    stream.on('data', chunk =>
      chunks.push(Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk))
    );
    stream.on('end', () => resolve(Buffer.concat(chunks).toString('utf-8')));
    stream.on('error', reject);
  });
}
