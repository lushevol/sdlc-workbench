/**
 * Enrich vulnerabilities with fix version information via the Nexus IQ Remediation API.
 * POST /api/v2/components/remediation/application/{internalAppId}?stageId={stage}
 *
 * For each vulnerable component, returns:
 *   - fixVersion: the recommended safe version (from next-no-violations, or next-non-failing fallback)
 *   - remediationTypes: array of type strings present in the response
 *   - hasNoViolationsFix: true if next-no-violations fix is available
 */

/**
 * Extract the version segment from a packageUrl: pkg:npm/name@version
 * @param {string} packageUrl
 * @returns {string|null}
 */
function extractVersionFromPurl(packageUrl) {
  const match = (packageUrl || '').match(/@([^@]+)$/);
  return match ? match[1] : null;
}

/**
 * Returns true when a component name looks like a Maven groupId:artifactId.
 * @param {string} componentName
 * @returns {boolean}
 */
function isMavenComponent(componentName) {
  return /^[^/@:]+:[^/@:]+$/.test(componentName);
}

/**
 * Build the package URL for a vulnerability component.
 * Maven:  pkg:maven/groupId/artifactId@version
 * npm:    pkg:npm/name@version
 */
function buildPurl(componentName, version) {
  if (isMavenComponent(componentName)) {
    const [groupId, artifactId] = componentName.split(':');
    return `pkg:maven/${groupId}/${artifactId}@${version}`;
  }
  return `pkg:npm/${componentName}@${version}`;
}

/**
 * Fetch remediation info for a single component.
 * For Maven pURLs the Nexus IQ Remediation API requires `componentIdentifier`
 * instead of `packageUrl` — sending a Maven pURL causes a 400 because the
 * API parses it and expects a `type` coordinate that Maven pURLs don't carry.
 *
 * @param {string} baseUrl
 * @param {Object} headers
 * @param {string} internalAppId
 * @param {string} packageUrl  e.g. "pkg:npm/lodash@4.17.20" or "pkg:maven/com.example/lib@1.0.0"
 * @param {string} stage
 * @returns {Promise<{fixVersion: string|null, remediationTypes: string[], hasNoViolationsFix: boolean}>}
 */
async function fetchComponentRemediation(baseUrl, headers, internalAppId, packageUrl, stage) {
  try {
    const url = `${baseUrl}/api/v2/components/remediation/application/${encodeURIComponent(internalAppId)}?stageId=${encodeURIComponent(stage)}`;

    // Maven: send componentIdentifier only (no packageUrl) to avoid 400
    let body;
    if (packageUrl.startsWith('pkg:maven/')) {
      const m = packageUrl.match(/^pkg:maven\/([^/]+)\/([^@]+)@(.+)$/);
      if (!m) return { fixVersion: null, remediationTypes: [], hasNoViolationsFix: false };
      body = {
        componentIdentifier: {
          format: 'maven',
          coordinates: { groupId: m[1], artifactId: m[2], version: m[3], extension: 'jar' }
        }
      };
    } else {
      body = { packageUrl };
    }

    const response = await fetch(url, {
      method: 'POST',
      headers,
      body: JSON.stringify(body)
    });

    if (!response.ok) {
      return { fixVersion: null, remediationTypes: [], hasNoViolationsFix: false };
    }

    const data = await response.json();
    const versionChanges = data?.remediation?.versionChanges ?? [];
    const remediationTypes = versionChanges.map(c => c.type);
    const hasNoViolationsFix = remediationTypes.includes('next-no-violations');

    let fixVersion = null;
    const noViolationsChange = versionChanges.find(c => c.type === 'next-no-violations');
    if (noViolationsChange) {
      fixVersion = extractVersionFromPurl(noViolationsChange.data?.component?.packageUrl);
    } else {
      const nonFailingChange = versionChanges.find(c => c.type === 'next-non-failing');
      if (nonFailingChange) {
        fixVersion = extractVersionFromPurl(nonFailingChange.data?.component?.packageUrl);
      }
    }

    return { fixVersion, remediationTypes, hasNoViolationsFix };
  } catch {
    return { fixVersion: null, remediationTypes: [], hasNoViolationsFix: false };
  }
}

/**
 * Enrich a list of parsed vulnerability objects with fix version information.
 * Calls the Nexus Remediation API once per unique component (pkg@version).
 *
 * @param {string} baseUrl
 * @param {Object} headers
 * @param {string} internalAppId
 * @param {Array<Object>} vulnerabilities - parsed vulnerability objects from parseVulnerabilities
 * @param {string} stage
 * @returns {Promise<Array<Object>>} Enriched vulnerability objects
 */
export async function enrichFixVersions(baseUrl, headers, internalAppId, vulnerabilities, stage) {
  // Collect unique component purls to minimise API calls
  // Maven components are identified by 'groupId:artifactId' naming convention
  const componentPurls = new Map();
  for (const v of vulnerabilities) {
    const key = `${v.component}@${v.version}`;
    if (!componentPurls.has(key)) {
      componentPurls.set(key, buildPurl(v.component, v.version));
    }
  }

  // Fan out in parallel — failures are silently swallowed inside fetchComponentRemediation
  const remediationMap = new Map();
  await Promise.all(
    Array.from(componentPurls.entries()).map(async ([key, purl]) => {
      const result = await fetchComponentRemediation(baseUrl, headers, internalAppId, purl, stage);
      remediationMap.set(key, result);
    })
  );

  // Merge remediation data back onto each vulnerability
  return vulnerabilities.map(v => {
    const key = `${v.component}@${v.version}`;
    const rem = remediationMap.get(key) ?? { fixVersion: null, remediationTypes: [], hasNoViolationsFix: false };
    // Prefer remediation API fix version; fall back to fixedInVersion from eval results
    const fixVersion = rem.fixVersion ?? v.fixVersion;
    return {
      ...v,
      fixVersion,
      remediationTypes: rem.remediationTypes,
      hasNoViolationsFix: rem.hasNoViolationsFix
    };
  });
}
