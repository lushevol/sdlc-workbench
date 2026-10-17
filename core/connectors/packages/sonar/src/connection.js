const SONAR_BASE_URL = 'https://sonarqube.vx.standardchartered.com';

/**
 * Create a SonarQube connection provider
 * @param {string} token - SonarQube user token
 * @returns {Object} Connection object with baseUrl and Authorization header
 */
export function getSonarConnection(token) {
  return {
    baseUrl: SONAR_BASE_URL,
    headers: {
      'Authorization': `Bearer ${token}`,
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    }
  };
}
