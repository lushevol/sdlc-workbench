# Messaging MCP Server

MCP server for messaging automation — send emails via Outlook and messages via Microsoft Teams. This package provides AI assistants with the ability to communicate through your locally installed Outlook and Teams applications, bypassing SMTP/webhook restrictions common in corporate environments.

## Features

- 🚀 **Send emails** via Outlook automation (no SMTP configuration needed)
- 💬 **Send Teams messages** via the installed Teams desktop app (no webhook or API setup required)
- 🔒 **Corporate-friendly** — Uses your existing Outlook and Teams sessions (no credentials stored)
- 🌍 **Cross-platform** — Works on macOS (AppleScript) and Windows (COM automation / URI deep links)
- 🤖 **MCP integration** — Seamlessly works with AI assistants via Model Context Protocol
- 📧 **Rich email formatting** — Supports HTML and plain text emails
- 👥 **Multiple recipients** — To, CC, and BCC for email; direct message or group chat for Teams

## Requirements

- **Node.js** 18.x or higher
- **Python** 3.6+ (automatically detects `python3`, `python`, or `py` commands)
  - ✅ Supports **all Python 3.x versions** (3.6, 3.7, 3.8, 3.9, 3.10, 3.11, 3.12+)
  - ✅ Supports multiple Python installations
  - ✅ Automatically validates Python 3.x compatibility
  - ✅ Falls back to alternative commands if primary not found
  - ❌ Python 2.x is not supported
- **Outlook** installed and logged in with your email account (for `email_send`)
- **Microsoft Teams** installed and signed in (for `teams_send_message`)
  - macOS: Accessibility permission must be granted to the calling process
    (System Settings → Privacy & Security → Accessibility)
- **macOS** or **Windows** operating system

> **Note:** The package automatically detects and validates your Python installation. It tries `python3`, `python`, and `py` (Windows) commands in order, and verifies that Python 3.x is available. **Any Python 3.x version works** — no specific minor version required!

## Installation

```bash
# Add to a project
yarn add @sc-node-mcp/messaging

# Global installation
yarn global add @sc-node-mcp/messaging
```

## Usage

### NPX Direct Execution

```bash
npx -y @sc-node-mcp/messaging
```

### Global Installation

```bash
sc-node-mcp-messaging
```

### Standalone Server

Run the MCP server directly:

```bash
node packages/messaging/src/index.js
```

### VS Code MCP Extension

Configure in your `.vscode/mcp.json`:

```json
{
  "mcpServers": {
    "messaging": {
      "command": "node",
      "args": ["/path/to/SC_Node_MCP/packages/messaging/src/index.js"]
    }
  }
}
```

### Programmatic Usage

```javascript
import { getPythonBridge, configureEmailTools, getTeamsNativeBridge, configureTeamsTools } from '@sc-node-mcp/messaging';
import { createMcpServer, startMcpServer } from '@sc-node-mcp/core';

const server = createMcpServer('messaging', '2.4.0');
configureEmailTools(server, getPythonBridge);
configureTeamsTools(server, getTeamsNativeBridge);
await startMcpServer(server);
```

## Available Tools

### `email_send`

Send an email via Outlook.

**Parameters:**
- `to` (required): Array of recipient email addresses
- `cc` (optional): Array of CC recipient email addresses
- `bcc` (optional): Array of BCC recipient email addresses
- `subject` (required): Email subject line
- `body` (required): Email body (plain text or HTML)

**Example:**

```javascript
{
  "to": ["recipient@example.com"],
  "cc": ["manager@example.com"],
  "subject": "Project Update",
  "body": "<h1>Status Report</h1><p>All tasks completed.</p>"
}
```

**Response:**

```json
{
  "content": [{
    "type": "text",
    "text": "✅ Email sent successfully!\n\nTo: recipient@example.com, CC: manager@example.com\nSubject: Project Update\n\nEmail has been queued in Outlook and will be sent."
  }]
}
```

---

### `teams_send_message`

Send a message to one or more people on Microsoft Teams using the installed Teams desktop app.

**Parameters:**
- `to` (required): Array of recipient email addresses (1 = direct message, 2+ = group chat)
- `message` (required): Message body text to send
- `title` (optional): Title prepended to the message on a new line

**Example:**

```javascript
{
  "to": ["colleague@example.com"],
  "message": "The deployment is complete.",
  "title": "Deploy Update"
}
```

**Response:**

```json
{
  "content": [{
    "type": "text",
    "text": "✅ Teams message sent successfully!\n\nTo: colleague@example.com\nTitle: Deploy Update\nMessage: The deployment is complete.\n\nMessage delivered via Microsoft Teams."
  }]
}
```

## How It Works

This MCP server acts as a bridge between Node.js and Python. Bundled Python scripts provide cross-platform automation for both Outlook and Teams:

### Email (`email_send`)
1. **Node.js MCP server** receives tool invocation from AI assistant
2. **Python bridge** spawns a Python process with email data via stdin (`scripts/send-outlook.py`)
3. **Python script** automates Outlook using platform-specific APIs:
   - **macOS:** AppleScript (`osascript`)
   - **Windows:** COM automation (`win32com`)
4. **Outlook** sends the email using your authenticated session
5. **Response** returns to AI assistant with success/error status

### Teams (`teams_send_message`)
1. **Node.js MCP server** receives tool invocation from AI assistant
2. **Python bridge** spawns a Python process with message data via stdin (`scripts/send-teams.py`)
3. **Python script** opens a `msteams://` deep link URI in the Teams desktop app with the message pre-filled, then simulates pressing Enter to send
4. **Response** returns to AI assistant with success/error status

Both scripts are bundled with the npm package and automatically deployed on installation.

## Development

### Running Tests

```bash
# Run all tests
yarn test

# Watch mode
yarn test:watch

# Coverage report
yarn test:coverage

# UI mode
yarn test:ui
```

### Project Structure

```
packages/messaging/
├── src/
│   ├── index.js          # Entry point
│   ├── connection.js     # Python bridge providers (email + Teams)
│   ├── tools.js          # Email tool registration orchestrator
│   └── tools/
│       ├── send.js       # Email send tool implementation
│       └── teams.js      # Teams message tool implementation
├── scripts/
│   ├── send-outlook.py   # Bundled Python script for Outlook email automation
│   ├── send-teams.py     # Bundled Python script for Teams native app messaging
│   └── README.md         # Python script documentation
├── tests/
│   ├── send.test.js      # Email tool tests
│   ├── teams.test.js     # Teams tool tests
│   └── connection.test.js # Bridge tests
├── package.json
├── vitest.config.js
└── README.md
```

## Troubleshooting

### Python version issues

The package automatically detects and validates Python 3.x installations. If you encounter issues:

- **Check Python is installed:** 
  ```bash
  python3 --version  # macOS/Linux
  python --version   # Windows or alternative
  py --version       # Windows Python Launcher
  ```
- **Ensure Python 3.x is available:** Python 2.x is not supported
- **Verify Python is in PATH:** The package tries `python3`, `python`, and `py` commands
- **Check error message:** It will indicate which commands were attempted

**Common scenarios:**
- ✅ `python3` available → Uses `python3`
- ✅ Only `python` points to Python 3.x → Uses `python`  
- ✅ Windows with Python Launcher → Uses `py`
- ❌ Only Python 2.x installed → Error message with installation instructions
- ⚙️ Command caching → Python detection runs once and caches the result

### Email not sending

- **Ensure Outlook is installed and running**
- **Verify you're logged into Outlook** with your email account
- **Review error messages** in the MCP server output

### Teams message not sending

- **Ensure Microsoft Teams is installed and you are signed in**
- **macOS:** Grant Accessibility permission to the calling process
  (System Settings → Privacy & Security → Accessibility)
- **Increase `TEAMS_LAUNCH_WAIT`** in `send-teams.py` if Teams is slow to open

### Platform-specific issues

**macOS:**
- Grant Terminal/VS Code accessibility permissions in System Settings → Privacy & Security → Accessibility
- Ensures AppleScript is not blocked by security settings (required by both Outlook and Teams automation)

**Windows:**
- For email: Install `pywin32`: `pip install pywin32>=305`
- For Teams: No extra packages required (uses URI deep links + keyboard simulation via `ctypes`)
- Run as administrator if COM automation fails
- Check Windows Defender is not blocking automation

### Corporate environment

- **No SMTP ports required** — Solution works entirely through local Outlook
- **No Teams webhook URL needed** — Uses the installed desktop app directly
- **No proxy configuration needed** — Outlook and Teams handle network communication
- **No credentials stored** — Uses your existing authenticated sessions

## Prompts

The `@sc-node-mcp/messaging` package ships 2 MCP prompts for guided messaging workflows:

- `send-email` — Compose and send an email via Outlook
- `teams-send-message` — Send a message to one or more people on Microsoft Teams

See [PROMPTS.md](../../docs/PROMPTS.md) for the full prompt reference.

## License

ISC

## Related Packages

- [@sc-node-mcp/core](../core) - Core MCP server infrastructure
- [@sc-node-mcp/ado](../ado) - Azure DevOps MCP server
- [@sc-node-mcp/unified](../unified) - Combined MCP server
