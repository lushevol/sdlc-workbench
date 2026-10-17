# Messaging Automation Scripts

This directory contains the Python automation scripts bundled with the `@sc-node-mcp/messaging` package.

## send-outlook.py

Cross-platform Python script that sends emails via your locally installed Microsoft Outlook application.

### Platform Support

- **macOS**: Uses AppleScript to automate Outlook
- **Windows**: Uses COM automation via `pywin32` package

### Requirements

**macOS:**
- Python 3.x (built-in)
- Microsoft Outlook installed and logged in
- No additional packages required

**Windows:**
- Python 3.x
- Microsoft Outlook installed and logged in
- `pywin32` package: `pip install pywin32>=305`

### Usage

This script is automatically invoked by the Node.js email bridge. It accepts JSON input via stdin:

```bash
echo '{"to":"user@example.com","subject":"Test","htmlBody":"Hello"}' | python3 send-outlook.py
```

### Input Format

```json
{
  "to": "recipient@example.com, another@example.com",
  "cc": "cc@example.com",
  "bcc": "bcc@example.com",
  "subject": "Email subject",
  "htmlBody": "Email body (supports HTML)"
}
```

### Output Format

**Success:**
```json
{"status": "success", "message": "Email sent successfully via Outlook (macOS)"}
```

**Error:**
```json
{"status": "error", "message": "Error description", "error": "Technical error details"}
```

### Security

- No credentials are stored or required
- Uses your existing Outlook authentication session
- Emails are sent through Outlook's normal sending mechanism
- Corporate email policies and DLP rules are enforced

### Troubleshooting

**macOS:**
- Grant Terminal/VS Code accessibility permissions in System Preferences
- Ensure Outlook is running and you're logged in
- Check AppleScript is not blocked by security settings

**Windows:**
- Install pywin32: `pip install pywin32`
- Run as administrator if COM automation fails
- Ensure Outlook is running and you're logged in

---

## send-teams.py

Cross-platform Python script that sends messages via your locally installed Microsoft Teams desktop application.

### Platform Support

- **macOS**: Opens a `msteams://` deep link URI and simulates Enter via AppleScript
- **Windows**: Opens a `msteams://` deep link URI and simulates Enter via `ctypes` keyboard events

### Requirements

**macOS:**
- Python 3.x
- Microsoft Teams desktop app installed and signed in
- **Accessibility permission** must be granted to the calling process
  (System Settings → Privacy & Security → Accessibility)
- No additional Python packages required

**Windows:**
- Python 3.x
- Microsoft Teams desktop app installed and signed in
- No additional Python packages required (`ctypes` is built-in)

### Usage

This script is automatically invoked by the Node.js Teams bridge. It accepts JSON input via stdin:

```bash
echo '{"to":["user@example.com"],"message":"Hello","title":"Update"}' | python3 send-teams.py
```

### Input Format

```json
{
  "to": ["recipient@example.com", "another@example.com"],
  "message": "Message body text",
  "title": "Optional title (prepended to message)"
}
```

### Output Format

**Success:**
```json
{"status": "success", "message": "Teams message sent to recipient@example.com"}
```

**Error:**
```json
{"status": "error", "message": "Error description"}
```

### Troubleshooting

**macOS:**
- Grant Accessibility permission to the calling process: System Settings → Privacy & Security → Accessibility
- Ensure Microsoft Teams is running and signed in
- Increase `TEAMS_LAUNCH_WAIT` constant in the script if Teams is slow to focus

**Windows:**
- Ensure Microsoft Teams is running and signed in
- No extra permissions required

---

## Development

These scripts are invoked by [packages/messaging/src/connection.js](../src/connection.js) which handles the Node.js ↔ Python IPC.

Do not modify these scripts without updating the corresponding Node.js bridge code and tests.
