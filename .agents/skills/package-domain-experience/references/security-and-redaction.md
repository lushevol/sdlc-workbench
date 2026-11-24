# Security and redaction

Inspect every selected file before promotion.

Remove or replace credentials, access tokens, cookies, private keys, authorization headers, personal data, customer data, private query values, machine-specific paths, and live environment values.

Keep variable names, types, sources, allowed values, and safe placeholders. Put actual values in ignored `.env`, `workspace.local.yaml`, approved process environment, or the target repository's private configuration.

Label fixtures as `synthetic` or `redacted`. State when a fixture cannot establish production behavior.
Keep raw logs and screenshots in task evidence. Promote a small excerpt only when the excerpt is required to reproduce or understand the procedure.

Do not treat a URL as reusable merely because it appeared in a log. Record its purpose, environment, access requirements, and whether it is a documentation reference or an execution target.
