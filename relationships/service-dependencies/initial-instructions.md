# Optional relationship discovery notes

The skill discovers dependencies from repository sources without requiring this file or human relationship input.
Optional notes can record corrections, source locations, and hypotheses. English or Chinese input is supported.
These notes supply regression expectations. They do not establish source facts, provider identity, or runtime behavior.

Entry point source: [user request](../../tasks/workbench-graph-instruction-integration-20261028/evidence/graph-instruction-integration-20261028/user-input-instruction-location-20261028.txt), 28 October 2026.

## Existing architecture notes

Compare independent discovery with the [preserved architecture explanation](../../knowledge/evidence/sources/user-clarifications/architecture-20261022/user-message.txt).
It describes the four MFE layers, Nginx, BFF, SDK, and Auth Server.
Keep that historical source unchanged. Add corrections and newer information below.

The [reviewed context](architecture-context.json) contains the previous investigation and its source references.
The agent maintains that structured file after checking current repository sources.

## New repositories and corrections

If useful, add dated notes here. No relationship inventory is required from the user.

- Repository name and relative path under `repos/`.
- Its purpose, provided interfaces, and expected consumers.
- Suspected API, messaging, storage, shared-code, configuration, or routing relationships.
- Known aliases, useful source locations, uncertainties, and investigation exclusions.
- Corrections to earlier notes, with the affected claim identified.

Leave unknown details explicit. The agent investigates all in-scope repositories and boundary families independently of these notes.

## Apply changes

To request discovery, ask:

> Use $service-dependencies-graph. Discover dependencies from all in-scope repositories, investigate extraction gaps, and regenerate the graph.

The agent checks available source first. Optional notes are compared with independently discovered declarations.
The agent preserves changed notes as dated evidence before editing them.
It records supported relationships, inferences, conflicts, and missing evidence through canonical extraction and reviewed context.
A build command alone validates and renders saved context. It does not investigate this Markdown file.

Open the generated [relationship viewer](generated/relationship-viewer.html) after successful generation.

## Output review

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```
