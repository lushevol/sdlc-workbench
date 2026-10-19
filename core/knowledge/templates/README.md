# Knowledge templates and SDLC authoring guides

Use the [SDLC authoring catalog](sdlc/README.md) for reusable engineering templates with samples and AI instructions.
The catalog covers planning, requirements, design, development, testing, release, operations, and governance.
Its authoring envelope is separate from the validated Workbench knowledge contract.

## Supported knowledge records

Each root Markdown template, except this guide, is a complete illustrative candidate.
The fixture has no business authority. No example records approval or verification.
The example source and manifest are in `examples/`.

Copy the relevant template into `knowledge/candidates/` to instantiate it.
Use `knowledge-topic.md` for connected background, terms, workflows, and historical explanations.
Classified topic drafts can use subdirectories beneath `knowledge/candidates/`.
Replace the illustrative IDs, source references, owner, dates, and domain content.
Register real source revisions in `evidence/knowledge/manifest.yaml` before validation.
Review the body and structured fields together.

Validation excludes `templates/` and `examples/` until their documents are instantiated.
Schemas under `core/knowledge/schemas/` are reference copies. Runtime checks use the
packaged contracts; editing a local schema does not disable a gate.
