import { z } from 'zod';

const MESSAGING_PROMPTS = {
  SEND_EMAIL: {
    name: 'send-email',
    description: 'Send an email via Outlook with recipients, subject, and body',
    arguments: [
      { name: 'to', description: 'Comma-separated recipient email addresses', required: true },
      { name: 'subject', description: 'Email subject line', required: true },
      { name: 'body', description: 'Email body content (supports HTML)', required: true },
      { name: 'cc', description: 'Comma-separated CC recipients (optional)', required: false },
      { name: 'bcc', description: 'Comma-separated BCC recipients (optional)', required: false }
    ]
  },

  TEAMS_SEND_CHANNEL_MESSAGE: {
    name: 'teams-send-message',
    description: 'Send a direct message or group chat via Microsoft Teams using the native Teams desktop app (no webhook required)',
    arguments: [
      { name: 'to', description: 'Comma-separated recipient email addresses', required: true },
      { name: 'message', description: 'Message body text', required: true },
      { name: 'title', description: 'Optional title prepended to the message', required: false }
    ]
  }
};

const generateMessagingPromptMessage = (name, args) => {
  switch (name) {
    case 'send-email':
      return `Send an email via Outlook:

To: ${args.to}
${args.cc ? `CC: ${args.cc}` : ''}
${args.bcc ? `BCC: ${args.bcc}` : ''}
Subject: ${args.subject}

Body:
${args.body}

This will send the email using your logged-in Outlook session (no SMTP configuration needed).`;

    case 'teams-send-message':
      return `Send a Microsoft Teams message via the native Teams app:

To: ${args.to}
${args.title ? `Title: ${args.title}` : ''}
Message: ${args.message}

This will open Teams with the message pre-filled and auto-send it.
Requires Teams to be installed and signed in.
macOS: Ensure Accessibility permission is granted (System Settings → Privacy & Security → Accessibility).`;

    default:
      return 'Unknown prompt';
  }
};

const CONTEXTUAL_OPTIONAL_FIELDS = new Set(['project', 'team', 'repository', 'repositoryId', 'applicationId']);

export function configureMessagingPrompts(server, { getContext = () => null } = {}) {
  Object.values(MESSAGING_PROMPTS).forEach(prompt => {
    const callback = async (args) => {
      const message = generateMessagingPromptMessage(prompt.name, args ?? {});
      return { messages: [{ role: 'user', content: { type: 'text', text: message } }] };
    };
    if (prompt.arguments.length === 0) {
      server.prompt(prompt.name, prompt.description, callback);
    } else {
      const argsSchema = Object.fromEntries(
        prompt.arguments.map(arg => [
          arg.name,
          (!arg.required || CONTEXTUAL_OPTIONAL_FIELDS.has(arg.name))
            ? z.string().optional().describe(arg.description)
            : z.string().describe(arg.description)
        ])
      );
      server.prompt(prompt.name, prompt.description, argsSchema, callback);
    }
  });
  console.error(`Registered ${Object.keys(MESSAGING_PROMPTS).length} messaging prompts`);
}

export { MESSAGING_PROMPTS };
