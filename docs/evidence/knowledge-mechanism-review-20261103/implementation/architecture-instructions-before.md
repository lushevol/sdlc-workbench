# Relationship discovery instructions

Edit this file when you add repositories or learn more about their relationships.
Write in English or Chinese. Partial information and uncertain guesses are useful starting points.
These notes guide investigation. They do not establish source facts or runtime behavior.

Entry point source: [user request](../../docs/evidence/graph-instruction-integration-20261028/user-input-instruction-location-20261028.txt), 28 October 2026.

## Existing architecture notes

Start with the [preserved architecture explanation](../../evidence/knowledge/sources/user-clarifications/architecture-20261022/user-message.txt).
It describes the four MFE layers, Nginx, BFF, SDK, and Auth Server.
Keep that historical source unchanged. Add corrections and newer information below.

The [reviewed context](architecture-context.json) contains the previous investigation and its source references.
The agent maintains that structured file after checking current repository sources.

## New repositories and corrections

Add dated notes here. Include what you know:

- Repository name and relative path under `repos/`.
- Its purpose, provided interfaces, and expected consumers.
- Suspected API, messaging, storage, shared-code, configuration, or routing relationships.
- Known aliases, useful source locations, uncertainties, and investigation exclusions.
- Corrections to earlier notes, with the affected claim identified.

Leave unknown details explicit. The agent must also discover relationships beyond these notes.

## Apply changes

After updating this file, ask:

> Use $service-dependencies-graph. Read relationships/service-dependencies/initial-instructions.md, investigate all repos, update the reviewed context, and regenerate the graph.

The agent preserves these notes as dated evidence before investigation.
It records supported relationships, inferences, conflicts, and missing evidence in the reviewed context.
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
