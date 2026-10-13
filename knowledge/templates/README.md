# Illustrative templates

Every Markdown template in this directory is a complete illustrative candidate.
The fixture has no business authority. No example records approval or verification.
The example source and manifest are in `examples/`.

Copy the relevant template into `knowledge/candidates/` to instantiate it.
Replace the illustrative IDs, source references, owner, dates, and domain content.
Register real source revisions in `knowledge/raw/manifest.yaml` before validation.
Review the body and structured fields together.

Validation excludes `templates/` and `examples/` until their documents are instantiated.
Schemas under `knowledge/schemas/` are reference copies. Runtime checks use the
packaged contracts; editing a local schema does not disable a gate.
