#!/usr/bin/env python3
"""
Microsoft Teams native app automation.

Opens the installed Teams client via the msteams:// URI deep link with
the message pre-filled, then simulates pressing Enter to send — the same
pattern used by the Outlook email automation.

Requires:
  - Microsoft Teams desktop app installed and signed in
  - macOS: Accessibility permission granted to the calling process
           (System Settings → Privacy & Security → Accessibility)
  - Windows: No extra permissions required (uses ctypes keyboard event)

Reads JSON from stdin:
  {
    "to": ["user@example.com", "other@example.com"],
    "message": "Hello, Teams!",
    "title": "Optional title"   // optional — prepended to message
  }

Writes JSON result to stdout:
  {"status": "success", "message": "Teams message sent to user@example.com"}

On failure, writes error JSON to stderr and exits with code 1.
"""

import json
import sys
import subprocess
import time
import urllib.parse
import platform


# Seconds to wait after opening the Teams URI before simulating Enter.
# Increase if Teams is slow to launch on this machine.
TEAMS_LAUNCH_WAIT = 2.5


def _send_macos(uri, to):
    """Open Teams URI and press Enter via AppleScript (macOS)."""
    subprocess.run(['open', uri], check=True)
    time.sleep(TEAMS_LAUNCH_WAIT)

    # AppleScript: bring the Teams process to front and press Enter.
    # Handles both classic Teams ("Microsoft Teams") and new Teams
    # ("Microsoft Teams (work or school)").
    applescript = r'''
set sent to false
tell application "System Events"
    repeat with teamsName in {"Microsoft Teams (work or school)", "Microsoft Teams", "Teams"}
        if exists (process teamsName) then
            tell process teamsName
                set frontmost to true
                delay 0.5
                keystroke return
            end tell
            set sent to true
            exit repeat
        end if
    end repeat
end tell
if not sent then
    error "Microsoft Teams process not found. Please ensure Teams is open and signed in."
end if
'''
    result = subprocess.run(
        ['osascript', '-e', applescript],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        err = result.stderr.strip() or result.stdout.strip()
        raise RuntimeError(
            f"AppleScript failed to send via Teams: {err}\n"
            "Make sure this process has Accessibility permission: "
            "System Settings → Privacy & Security → Accessibility"
        )
    return {"status": "success", "message": f"Teams message sent to {', '.join(to)}"}


def _send_windows(uri, to):
    """Open Teams URI and press Enter via ctypes keyboard event (Windows)."""
    import os
    os.startfile(uri)
    time.sleep(TEAMS_LAUNCH_WAIT)

    # Bring the Teams window to the foreground if pywin32 is available,
    # then simulate an Enter keypress via ctypes (no extra install needed).
    try:
        import win32gui
        import win32con
        def _bring_to_front(hwnd, _):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if 'Microsoft Teams' in title or title == 'Teams':
                    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                    win32gui.SetForegroundWindow(hwnd)
        win32gui.EnumWindows(_bring_to_front, None)
        time.sleep(0.3)
    except ImportError:
        pass  # Try the keystroke anyway — Teams may already be focused

    import ctypes
    VK_RETURN = 0x0D
    KEYEVENTF_KEYUP = 0x0002
    ctypes.windll.user32.keybd_event(VK_RETURN, 0, 0, 0)
    time.sleep(0.05)
    ctypes.windll.user32.keybd_event(VK_RETURN, 0, KEYEVENTF_KEYUP, 0)

    return {"status": "success", "message": f"Teams message sent to {', '.join(to)}"}


def send_teams_message_native(to, message, title=None):
    """
    Send a Teams message via the native Teams desktop app.

    Args:
        to (list[str]): Recipient email addresses (1 = DM, 2+ = group chat).
        message (str): Message body text.
        title (str, optional): Optional title — prepended to the message body.

    Returns:
        dict: {"status": "success", "message": "..."}
    """
    if not to:
        raise ValueError("'to' is required — provide at least one email address")
    if not message:
        raise ValueError("'message' is required")

    # Combine title + message if title provided
    full_message = f"{title}\n{message}" if title else message

    # Build the Teams deep-link URI
    users_param = ','.join(to)
    encoded_message = urllib.parse.quote(full_message)
    uri = (
        f"msteams://teams.microsoft.com/l/chat/0/0"
        f"?users={users_param}&message={encoded_message}"
    )

    system = platform.system()
    if system == 'Darwin':
        return _send_macos(uri, to)
    elif system == 'Windows':
        return _send_windows(uri, to)
    else:
        raise RuntimeError(
            f"Platform '{system}' is not supported. "
            "Teams native automation requires macOS or Windows with Teams installed."
        )


def main():
    try:
        raw = sys.stdin.read()
        if not raw.strip():
            raise ValueError("No input received on stdin")

        data = json.loads(raw)
        to = data.get("to", [])
        message = data.get("message", "")
        title = data.get("title")

        result = send_teams_message_native(to, message, title)
        print(json.dumps(result))

    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

