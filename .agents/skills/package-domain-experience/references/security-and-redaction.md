# Security and redaction

Inspect every selected file before promotion.

Remove or replace credentials, access tokens, cookies, private keys, authorization headers, personal data, customer data, private query values, machine-specific paths, and live environment values.

Keep variable names, types, sources, allowed values, and safe placeholders. Put actual values in ignored `.env`, `workspace.local.yaml`, approved process environment, or the target repository's private configuration.

Label fixtures as `synthetic` or `redacted`. State when a fixture cannot establish production behavior.
Keep routine logs in ignored local storage. Retain raw logs and screenshots as task evidence when a consequential claim requires them.
Select only necessary evidence for the reusable packet.
An excerpt must retain enough context to reproduce or understand the procedure.
Keep the original raw evidence when omitted context could change the conclusion. A hash cannot replace those bytes.

Do not treat a URL as reusable merely because it appeared in a log. Record its purpose, environment, access requirements, and whether it is a documentation reference or an execution target.
