import { z } from "zod";

/**
 * Configure Teams messaging tools
 * @param {Object} server - MCP server instance
 * @param {Function} getTeamsNativeBridge - Connection provider function
 */
export function configureTeamsTools(server, getTeamsNativeBridge) {
  server.tool(
    "teams_send_message",
    "Send a message to one or more people on Microsoft Teams using the installed Teams desktop app. Uses your logged-in Teams session — no webhook URL or API setup required. Supports direct messages (1 recipient) and group chats (multiple recipients). Requires Teams to be installed and signed in. macOS: Accessibility permission must be granted to the calling process (System Settings → Privacy & Security → Accessibility).",
    {
      to: z.array(z.string().email()).min(1).describe("Array of recipient email addresses (1 = direct message, 2+ = group chat)"),
      message: z.string().min(1).describe("Message body text to send"),
      title: z.string().optional().describe("Optional title prepended to the message on a new line")
    },
    async ({ to, message, title }) => {
      try {
        const bridge = await getTeamsNativeBridge();

        const result = await bridge.sendMessage(to, message, title);

        const recipientList = to.join(', ');
        const titleLine = title ? `\nTitle: ${title}` : '';
        const successMessage = `✅ Teams message sent successfully!\n\nTo: ${recipientList}${titleLine}\nMessage: ${message}\n\n${result.message || 'Message delivered via Microsoft Teams.'}`;

        return {
          content: [{
            type: "text",
            text: successMessage
          }]
        };
      } catch (error) {
        const errorMessage = `❌ Failed to send Teams message: ${error?.message || String(error)}\n\nPlease ensure:\n- Microsoft Teams is installed and you are signed in\n- Python 3.x is installed (python3 --version)\n- macOS: Accessibility permission granted to this process\n  (System Settings → Privacy & Security → Accessibility)\n- Windows: Microsoft Teams app is open`;

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

