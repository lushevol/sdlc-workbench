const NEXUS_BASE_URL = 'https://sonatypenexus.global.standardchartered.com';

/**
 * Create a Nexus IQ connection provider
 * @param {string} userCode - Nexus IQ username / user code
 * @param {string} passCode - Nexus IQ password / pass code
 * @returns {Object} Connection object with baseUrl and Authorization header
 */
export function getNexusConnection(userCode, passCode) {
  // Disable TLS certificate verification for corporate environments (same as other packages)
  process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';

  const credentials = Buffer.from(`${userCode}:${passCode}`).toString('base64');

  return {
    baseUrl: NEXUS_BASE_URL,
    headers: {
      'Authorization': `Basic ${credentials}`,
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    }
  };
}
