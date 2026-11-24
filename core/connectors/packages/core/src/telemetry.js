
const TELEMETRY_BRANCH = 'telemetry/usage-log';
const TELEMETRY_FILE = '/usage.log';
const TELEMETRY_PROJECT = 'DDCPQPR';
const TELEMETRY_REPO = '23966-sc-node-mcp';
const ZERO_SHA = '0000000000000000000000000000000000000000';

// How long to wait for connection.connect() before giving up and using 'unknown' as the user.
const IDENTITY_TIMEOUT_MS = 8000;

/**
 * Resolve the authenticated user's display name from an ADO connection.
 * Returns { user, resolved: true } on success.
 * Returns { user: 'unknown', resolved: false } on timeout (logs a warning).
 * Re-throws 401/403 so the caller can abort telemetry (bad PAT).
 * Re-throws all other errors so the caller can log them.
 *
 * @param {Object} connection - ADO WebApi connection (already obtained from getConnection)
 * @returns {Promise<{ user: string, resolved: boolean }>}
 */
async function resolveIdentity(connection) {
  const timeoutErr = Object.assign(new Error('identity check timed out'), { isTelemetryTimeout: true });
  try {
    const connectionData = await Promise.race([
      connection.connect(),
      new Promise((_, reject) => setTimeout(() => reject(timeoutErr), IDENTITY_TIMEOUT_MS)),
    ]);
    const user =
      connectionData?.authenticatedUser?.providerDisplayName ||
      connectionData?.authenticatedUser?.id ||
      'unknown';
    return { user, resolved: true };
  } catch (err) {
    if (err?.statusCode === 401 || err?.statusCode === 403) throw err;
    if (err?.isTelemetryTimeout) {
      console.error('[Telemetry] Identity check timed out — recording with user: unknown');
      return { user: 'unknown', resolved: false };
    }
    throw err;
  }
}

/**
 * Record a startup telemetry entry to the ADO repo branch `telemetry/usage-log`
 * in the `DDCPQPR/23966-sc-node-mcp` repository.
 * Fire-and-forget — never throws, never blocks server startup.
 *
 * @param {Object} config - Application config from getConfig()
 * @param {Function} getConnection - ADO connection provider function
 * @param {Object} opts - Package identity
 * @param {Object} opts.versions - Map of package names to versions (e.g. { 'ado-pipelines': '1.2.3' })
 */
export async function recordStartupTelemetry(config, getConnection, { versions }) {
  if (process.env.DISABLE_TELEMETRY === '1') {
    console.error('[Telemetry] Disabled via DISABLE_TELEMETRY=1');
    return;
  }

  // Track whether identity was resolved — distinguishes a 401 from pushRecord (PAT lacks
  // write access, tools still work) from a 401 out of resolveIdentity (PAT is invalid).
  let identityResolved = false;

  try {
    const connection = await getConnection();
    const { user } = await resolveIdentity(connection);
    identityResolved = true;

    const record = JSON.stringify({
      timestamp: new Date().toISOString(),
      user,
      versions,
      platform: process.platform,
      nodeVersion: process.version,
    });

    await pushRecord(connection, TELEMETRY_PROJECT, TELEMETRY_REPO, record, false);
    console.error(`[Telemetry] Recorded session for ${user}`);
  } catch (err) {
    // 401/403 has two distinct meanings depending on where it was thrown:
    //  - identityResolved=false: from resolveIdentity → PAT invalid/expired → ADO tools also broken
    //  - identityResolved=true:  from pushRecord     → PAT lacks write access → tools are fine
    if (err?.statusCode === 401 || err?.statusCode === 403) {
      if (identityResolved) {
        console.error('[Telemetry] Skipped: PAT lacks write access to the telemetry repository. MCP tools are fully functional.');
      } else {
        console.error('[Telemetry] Skipped: ADO PAT is invalid or expired. MCP ADO tools will also be unavailable — please refresh your PAT.');
      }
      return;
    }
    console.error('[Telemetry] Failed to record startup:', err.message);
  }
}

/**
 * Append a record to usage.log on the telemetry branch via ADO Git push.
 * Retries once on 409 Conflict (concurrent write).
 *
 * @param {Object} connection - ADO WebApi connection
 * @param {string} project - ADO project name
 * @param {string} repo - ADO repository name
 * @param {string} record - JSON string to append
 * @param {boolean} isRetry - True if this is the retry attempt
 */
async function pushRecord(connection, project, repo, record, isRetry) {
  const gitApi = await connection.getGitApi();

  const repository = await gitApi.getRepository(repo, project);
  const repoId = repository.id;

  // Get current branch tip SHA (ZERO_SHA if branch doesn't exist yet)
  const refs = await gitApi.getRefs(repoId, project, `heads/${TELEMETRY_BRANCH}`);
  const branchExists = Array.isArray(refs) && refs.length > 0;
  const tipSha = branchExists ? refs[0].objectId : ZERO_SHA;

  // Try to read the existing log file; if absent, start fresh
  let existingContent = '';
  let fileExistsInRepo = false;

  if (branchExists) {
    try {
      const stream = await gitApi.getItemContent(
        repoId,
        TELEMETRY_FILE,
        project,
        null, null, false, false, false,
        { versionType: 0 /* Branch */, version: TELEMETRY_BRANCH }
      );
      const rawContent = await streamToString(stream);
      fileExistsInRepo = true;
      // Guard against proxy interceptors (e.g. Zscaler) returning an HTML block page
      // instead of the file content. Only retain lines that parse as JSON objects —
      // any HTML, error page, or other non-NDJSON content is silently discarded so
      // it can never be written back into the log.
      existingContent = rawContent
        .split('\n')
        .filter(line => {
          const trimmed = line.trim();
          if (!trimmed) return false;
          try {
            const parsed = JSON.parse(trimmed);
            return typeof parsed === 'object' && parsed !== null;
          } catch {
            return false;
          }
        })
        .join('\n');
    } catch {
      // File doesn't exist on this branch yet — will be created as Add
    }
  }

  const newContent = existingContent.trim()
    ? existingContent.trimEnd() + '\n' + record + '\n'
    : record + '\n';

  try {
    await gitApi.createPush(
      {
        refUpdates: [{ name: `refs/heads/${TELEMETRY_BRANCH}`, oldObjectId: tipSha }],
        commits: [
          {
            comment: '[telemetry] startup recorded',
            changes: [
              {
                changeType: fileExistsInRepo ? 2 /* Edit */ : 1 /* Add */,
                item: { path: TELEMETRY_FILE },
                newContent: { content: newContent, contentType: 0 /* RawText */ },
              },
            ],
          },
        ],
      },
      repoId,
      project
    );
  } catch (err) {
    // 409 Conflict = concurrent write, retry once with a fresh read
    if (!isRetry && err?.statusCode === 409) {
      await new Promise(resolve => setTimeout(resolve, 1000));
      return pushRecord(connection, project, repo, record, true);
    }
    throw err;
  }

  return true;
}

/**
 * Converts an ADO SDK response (Buffer, string, or ReadableStream) to a string.
 */
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
