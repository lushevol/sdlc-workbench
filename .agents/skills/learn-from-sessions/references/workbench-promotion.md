# Promote experience into Workbench assets

Promote an experience into shared Workbench assets when it generalizes beyond one task and improves future agent execution.

Use these targets.

- `AGENTS.md` for durable project-wide operating guidance.
- `.agents/skills/<skill>/` for reusable agent procedures and their focused helpers.
- `core/skills/` for small installed runtime guidance.
- `scripts/` for project-owned deterministic helpers.

Keep application source, business-repository files, credentials, private configuration, and environment-specific values in their existing owners.
Keep canonical domain meaning in `knowledge/records/` and link it from the packet.

Before changing a shared asset, inspect its callers and existing instructions. Apply the smallest compatible change. Preserve unrelated text and behavior.

Record the target, `add` or `update` action, purpose, packet source section, before hash, after hash, and checks in `manifest.yaml` under `promotions`.
Run the target skill validator, focused helper tests, or the applicable project check after the change.
Link the changed target from the owning task and retain the promotion as part of the packet provenance.

Do not promote a one-off workaround, unsupported business conclusion, raw log, secret-bearing file, or synthetic fixture into shared guidance.
