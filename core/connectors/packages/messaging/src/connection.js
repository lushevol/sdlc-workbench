import { spawn, execSync } from 'child_process';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Cache for detected Python command
let cachedPythonCommand = null;

/**
 * Clear the cached Python command (for testing)
 * @internal
 */
export function clearPythonCache() {
  cachedPythonCommand = null;
}

/**
 * Get the path to the Python email automation script
 * @returns {string} Absolute path to send-outlook.py
 */
function getPythonScriptPath() {
  // Use bundled Python script in packages/email/scripts/
  return join(__dirname, '..', 'scripts', 'send-outlook.py');
}

/**
 * Check if a Python command supports Python 3.x
 * @param {string} command - Python command to test (python3, python, py)
 * @returns {boolean} True if command exists and is Python 3.x
 * @note Supports all Python 3.x versions (3.6, 3.7, 3.8, 3.9, 3.10, 3.11, 3.12+)
 */
function isPython3(command) {
  try {
    // Check Python version
    const version = execSync(`${command} --version`, { 
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'pipe'],
      timeout: 5000
    }).trim();
    
    // Parse version (e.g., "Python 3.9.1" or "Python 3.11.0")
    // Accepts any Python 3.x version (no minor version restriction)
    const match = version.match(/Python (\d+)\.(\d+)/);
    if (match) {
      const majorVersion = parseInt(match[1], 10);
      return majorVersion === 3;  // ✅ All Python 3.x versions supported
    }
    return false;
  } catch (error) {
    // Command not found or failed to execute
    return false;
  }
}

/**
 * Find available Python 3.x command
 * Tries multiple common Python commands and validates version
 * @returns {string} Python command to use (python3, python, or py)
 * @throws {Error} If no Python 3.x installation is found
 */
function findPython3Command() {
  // Return cached result if available
  if (cachedPythonCommand) {
    return cachedPythonCommand;
  }

  // Try common Python commands in order of preference
  const candidates = process.platform === 'win32'
    ? ['python3', 'python', 'py']  // Windows: py launcher is common
    : ['python3', 'python'];        // Unix: python3 is standard

  for (const command of candidates) {
    if (isPython3(command)) {
      cachedPythonCommand = command;
      console.error(`[Messaging MCP] Using Python command: ${command}`);
      return command;
    }
  }

  // No Python 3.x found
  throw new Error(
    'Python 3.x not found. Please install Python 3.x and ensure it is available in PATH. ' +
    `Tried commands: ${candidates.join(', ')}`
  );
}

/**
 * Send email via Python Outlook automation bridge
 * @param {Object} emailData - Email data
 * @param {string[]} emailData.to - To recipients
 * @param {string[]} emailData.cc - CC recipients
 * @param {string[]} emailData.bcc - BCC recipients
 * @param {string} emailData.subject - Email subject
 * @param {string} emailData.htmlBody - Email body (HTML or plain text)
 * @returns {Promise<Object>} Result with status and message
 */
async function sendEmailViaPython(emailData) {
  return new Promise((resolve, reject) => {
    const pythonScript = getPythonScriptPath();
    
    // Find available Python 3.x command (with caching)
    let pythonCommand;
    try {
      pythonCommand = findPython3Command();
    } catch (error) {
      reject(error);
      return;
    }
    
    // Spawn Python process
    const pythonProcess = spawn(pythonCommand, [pythonScript], {
      stdio: ['pipe', 'pipe', 'pipe']
    });

    let stdout = '';
    let stderr = '';

    // Collect output
    pythonProcess.stdout.on('data', (data) => {
      stdout += data.toString();
    });

    pythonProcess.stderr.on('data', (data) => {
      stderr += data.toString();
    });

    pythonProcess.on('close', (code) => {
      if (code !== 0) {
        reject(new Error(`Python process exited with code ${code}: ${stderr || stdout}`));
      } else {
        try {
          // Try to parse JSON response
          const response = JSON.parse(stdout.trim());
          resolve(response);
        } catch (e) {
          // If not JSON, treat stdout as success message
          resolve({ status: 'success', message: stdout.trim() || 'Email sent successfully' });
        }
      }
    });

    pythonProcess.on('error', (error) => {
      reject(new Error(`Failed to spawn Python process: ${error.message}`));
    });

    // Send email data to Python via stdin as JSON
    try {
      const jsonData = JSON.stringify(emailData);
      pythonProcess.stdin.write(jsonData);
      pythonProcess.stdin.end();
    } catch (error) {
      pythonProcess.kill();
      reject(new Error(`Failed to write to Python stdin: ${error.message}`));
    }
  });
}

/**
 * Get the path to the Python Teams webhook script
 * @returns {string} Absolute path to send-teams.py
 */
function getPythonTeamsScriptPath() {
  return join(__dirname, '..', 'scripts', 'send-teams.py');
}

/**
 * Send a Teams message via the Python native automation bridge
 * @param {Object} data - Teams message data
 * @param {string[]} data.to - Recipient email addresses
 * @param {string} data.message - Message body text
 * @param {string} [data.title] - Optional title
 * @returns {Promise<Object>} Result with status and message
 */
async function sendTeamsNativeViaPython(data) {
  return new Promise((resolve, reject) => {
    const pythonScript = getPythonTeamsScriptPath();

    let pythonCommand;
    try {
      pythonCommand = findPython3Command();
    } catch (error) {
      reject(error);
      return;
    }

    const pythonProcess = spawn(pythonCommand, [pythonScript], {
      stdio: ['pipe', 'pipe', 'pipe']
    });

    let stdout = '';
    let stderr = '';

    pythonProcess.stdout.on('data', (chunk) => { stdout += chunk.toString(); });
    pythonProcess.stderr.on('data', (chunk) => { stderr += chunk.toString(); });

    pythonProcess.on('close', (code) => {
      if (code !== 0) {
        reject(new Error(`Python process exited with code ${code}: ${stderr || stdout}`));
      } else {
        try {
          resolve(JSON.parse(stdout.trim()));
        } catch {
          resolve({ status: 'success', message: stdout.trim() || 'Teams message sent successfully' });
        }
      }
    });

    pythonProcess.on('error', (error) => {
      reject(new Error(`Failed to spawn Python process: ${error.message}`));
    });

    try {
      pythonProcess.stdin.write(JSON.stringify(data));
      pythonProcess.stdin.end();
    } catch (error) {
      pythonProcess.kill();
      reject(new Error(`Failed to write to Python stdin: ${error.message}`));
    }
  });
}

/**
 * Get Teams native bridge connection provider
 * Sends messages via the installed Teams desktop app (no webhook or API needed)
 * @returns {Promise<Object>} Bridge object with sendMessage method
 */
export async function getTeamsNativeBridge() {
  return {
    /**
     * Send a message to one or more people on Teams using the native app
     * @param {string[]} to - Recipient email addresses (1 = DM, 2+ = group chat)
     * @param {string} message - Message body text
     * @param {string} [title] - Optional title prepended to the message
     * @returns {Promise<Object>} Result object
     */
    sendMessage: async (to, message, title) => {
      return await sendTeamsNativeViaPython({ to, message, title });
    }
  };
}

/**
 * Get Python bridge connection provider
 * This returns an object with methods to interact with the Python email automation
 * @returns {Promise<Object>} Bridge object with sendEmail method
 */
export async function getPythonBridge() {
  return {
    /**
     * Send an email via Outlook automation
     * @param {Object} params - Email parameters
     * @param {string[]} params.to - To recipients (email addresses)
     * @param {string[]} [params.cc] - CC recipients
     * @param {string[]} [params.bcc] - BCC recipients
     * @param {string} params.subject - Email subject
     * @param {string} params.htmlBody - Email body (HTML or plain text)
     * @returns {Promise<Object>} Result object
     */
    sendEmail: async ({ to, cc = [], bcc = [], subject, htmlBody }) => {
      // Pass recipient arrays through as-is; the Python script builds one
      // recipient per address so multiple To/CC/BCC addresses are preserved.
      const emailData = {
        to,
        cc,
        bcc,
        subject,
        htmlBody
      };

      return await sendEmailViaPython(emailData);
    }
  };
}
