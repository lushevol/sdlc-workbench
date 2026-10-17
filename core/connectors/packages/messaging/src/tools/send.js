import { z } from "zod";

/**
 * Configure email send tools
 * @param {Object} server - MCP server instance
 * @param {Function} getPythonBridge - Connection provider function
 */
export function configureSendTools(server, getPythonBridge) {
  server.tool(
    "email_send",
    "Send an email via Outlook automation. Works on macOS and Windows using your logged-in Outlook session. Supports To, CC, BCC recipients and HTML/plain text body.",
    {
      to: z.array(z.string().email()).describe("Array of recipient email addresses (To field)"),
      cc: z.array(z.string().email()).optional().describe("Array of CC recipient email addresses (optional)"),
      bcc: z.array(z.string().email()).optional().describe("Array of BCC recipient email addresses (optional)"),
      subject: z.string().describe("Email subject line"),
      body: z.string().describe("Email body content (supports HTML or plain text)")
    },
    async ({ to, cc, bcc, subject, body }) => {
      try {
        // Get Python bridge connection
        const bridge = await getPythonBridge();
        
        // Send email via Python Outlook automation
        const result = await bridge.sendEmail({
          to,
          cc: cc || [],
          bcc: bcc || [],
          subject,
          htmlBody: body
        });

        // Format recipient list for response
        const recipientList = to.join(', ');
        const ccList = cc && cc.length > 0 ? `, CC: ${cc.join(', ')}` : '';
        const bccList = bcc && bcc.length > 0 ? `, BCC: ${bcc.join(', ')}` : '';
        
        const successMessage = `✅ Email sent successfully!\n\nTo: ${recipientList}${ccList}${bccList}\nSubject: ${subject}\n\n${result.message || 'Email has been queued in Outlook and will be sent.'}`;

        return {
          content: [{
            type: "text",
            text: successMessage
          }]
        };
      } catch (error) {
        const errorMessage = `❌ Failed to send email: ${error?.message || String(error)}\n\nPlease ensure:\n- Outlook is installed and running\n- You are logged into Outlook with your email account\n- Python 3.x is installed (python3 --version)\n- On Windows: pywin32 package is installed (pip install pywin32)`;
        
        return {
          content: [{
            type: "text",
            text: errorMessage
          }],
          isError: true
        };
      }
    }
  );
}
