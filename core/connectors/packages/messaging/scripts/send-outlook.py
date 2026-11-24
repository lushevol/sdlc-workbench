#!/usr/bin/env python3
"""
Cross-Platform Outlook Email Sender for MCP
Works on both macOS (AppleScript) and Windows (COM automation)

This script is bundled with the @sc-node-mcp/email package and is invoked
by the Node.js email bridge to send emails via the locally installed Outlook application.
"""

import sys
import json
import platform
import re
import subprocess

def _as_recipient_list(value):
    """
    Normalize a recipients field to a list of non-empty address strings.
    Accepts a list (the format sent by the Node.js bridge) or, as a
    backward-compat fallback, a comma/semicolon-separated string.
    """
    if not value:
        return []
    if isinstance(value, list):
        return [addr.strip() for addr in value if addr and addr.strip()]
    return [addr.strip() for addr in re.split(r'[;,]', value) if addr.strip()]

def send_email_via_outlook_windows(email_data):
    """
    Send email using Windows Outlook via COM automation
    """
    try:
        import win32com.client
        
        # Initialize Outlook Application
        outlook = win32com.client.Dispatch("Outlook.Application")
        
        # Create new email item (olMailItem = 0x0)
        mail = outlook.CreateItem(0x0)
        
        # Set email properties
        mail.Subject = email_data.get('subject', '')
        mail.HTMLBody = email_data.get('htmlBody', '')
        
        to_addresses = _as_recipient_list(email_data.get('to'))
        cc_addresses = _as_recipient_list(email_data.get('cc'))
        bcc_addresses = _as_recipient_list(email_data.get('bcc'))
        
        # Outlook COM reliably splits a ';'-separated list into distinct
        # recipients regardless of locale (',' is not guaranteed to work).
        if to_addresses:
            mail.To = '; '.join(to_addresses)
        
        if cc_addresses:
            mail.CC = '; '.join(cc_addresses)
        
        if bcc_addresses:
            mail.BCC = '; '.join(bcc_addresses)
        
        # Set importance (high = 2, normal = 1, low = 0)
        if email_data.get('importance') == 'high':
            mail.Importance = 2
        
        # Send the email
        mail.Send()
        
        return {
            'success': True,
            'message': 'Email sent successfully via Outlook (Windows)'
        }
        
    except ImportError:
        return {
            'success': False,
            'error': 'pywin32 not installed',
            'message': 'Please install pywin32: pip install pywin32'
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'message': f'Failed to send email: {str(e)}'
        }

def send_email_via_outlook_macos(email_data):
    """
    Send email using macOS Outlook via AppleScript
    """
    try:
        # Escape strings for AppleScript
        def escape_applescript(s):
            if not s:
                return ''
            return s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\r', '\\r')
        
        def build_recipient_statements(addresses, recipient_kind):
            # Emit one AppleScript recipient-creation statement per address
            # so every To/CC/BCC address becomes its own distinct recipient.
            return '\n                '.join(
                f'make new {recipient_kind} at newMessage with properties '
                f'{{email address:{{address:"{escape_applescript(addr)}"}}}}'
                for addr in addresses
            )
        
        to_addresses = _as_recipient_list(email_data.get('to'))
        cc_addresses = _as_recipient_list(email_data.get('cc'))
        bcc_addresses = _as_recipient_list(email_data.get('bcc'))
        
        to_statements = build_recipient_statements(to_addresses, 'recipient')
        cc_statements = build_recipient_statements(cc_addresses, 'cc recipient')
        bcc_statements = build_recipient_statements(bcc_addresses, 'bcc recipient')
        
        subject = escape_applescript(email_data.get('subject', ''))
        html_body = escape_applescript(email_data.get('htmlBody', ''))
        
        # AppleScript to create and send email
        applescript = f'''
        tell application "Microsoft Outlook"
            set newMessage to make new outgoing message with properties {{subject:"{subject}"}}
            
            tell newMessage
                -- Set HTML content
                set content to "{html_body}"
                
                -- Add TO recipients (one statement per address)
                {to_statements}
                
                -- Add CC recipients (one statement per address)
                {cc_statements}
                
                -- Add BCC recipients (one statement per address)
                {bcc_statements}
                
                -- Send the email
                send
            end tell
            
            return "Email sent successfully"
        end tell
        '''
        
        # Execute AppleScript
        result = subprocess.run(
            ['osascript', '-e', applescript],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            return {
                'success': True,
                'message': f'Email sent successfully via Outlook (macOS)'
            }
        else:
            return {
                'success': False,
                'error': result.stderr,
                'message': f'AppleScript error: {result.stderr}'
            }
            
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'message': f'Failed to send email: {str(e)}'
        }

def send_email(email_data):
    """
    Send email via Outlook - detects platform automatically
    """
    system = platform.system()
    
    if system == 'Darwin':  # macOS
        return send_email_via_outlook_macos(email_data)
    elif system == 'Windows':
        return send_email_via_outlook_windows(email_data)
    else:
        return {
            'success': False,
            'error': f'Unsupported platform: {system}',
            'message': f'This application only supports macOS and Windows. Detected: {system}'
        }

if __name__ == '__main__':
    try:
        # Read JSON data from stdin (MCP server mode)
        if not sys.stdin.isatty():
            stdin_data = sys.stdin.read()
            email_data = json.loads(stdin_data)
            
            result = send_email(email_data)

            if result['success']:
                print(json.dumps({'status': 'success', 'message': result.get('message', 'Email sent successfully')}))
                sys.exit(0)
            else:
                print(json.dumps({'status': 'error', 'message': result.get('message', 'Failed to send email'), 'error': result.get('error', '')}), file=sys.stderr)
                sys.exit(1)
        else:
            # No stdin input - show usage
            print(json.dumps({
                'status': 'error',
                'message': 'This script expects JSON input via stdin. Use: echo \'{"to":"user@example.com","subject":"Test","htmlBody":"Body"}\' | python3 send-outlook.py'
            }), file=sys.stderr)
            sys.exit(1)

    except json.JSONDecodeError as e:
        result = {
            'status': 'error',
            'error': f'Invalid JSON: {str(e)}',
            'message': 'Failed to parse JSON input from stdin'
        }
        print(json.dumps(result), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        result = {
            'status': 'error',
            'error': str(e),
            'message': f'Unexpected error: {str(e)}'
        }
        print(json.dumps(result), file=sys.stderr)
        sys.exit(1)
