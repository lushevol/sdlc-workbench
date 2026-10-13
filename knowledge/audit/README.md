# Audit events

Append one YAML file per event. Use the event ID as its filename.
Use [the audit schema](../schemas/audit-event.schema.json).

Keep earlier events unchanged. Record item ID/version, actor, time, prior and next state,
full document SHA256, reason, and exact evidence source references.
Declare human approval with `action: approval` and `actor: human:<id>`.
Validation checks declared metadata. It does not authenticate the actor.
Use Git review to confirm authors preserved earlier events.
