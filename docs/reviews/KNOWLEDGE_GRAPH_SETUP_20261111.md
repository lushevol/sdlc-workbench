# Knowledge graph setup

The existing Workbench graph now includes the current knowledge records and their retained evidence.
The interactive viewer opens its Knowledge graph tab by default.
The [graph guide](../../.agents/skills/service-dependencies-graph/references/architecture/knowledge-graph.md) defines its inputs and evidence boundaries.

Date: 11 November 2026, Asia/Singapore.
Owner: Workbench maintainer.

## Available graph

| Scope | Result |
| --- | --- |
| Current domain records | 12/12, all candidate/draft. |
| Source revisions | 500. |
| Projected knowledge nodes | 843. |
| Declared knowledge links | 1,103. |
| Knowledge record nodes | 15, including three historical baseline intent records. |
| Unresolved references | 89, with explicit missing or historical identity limits. |
| Local knowledge freshness | `CURRENT`. |
| Local repository and context freshness | `CURRENT`. |

The graph retains exact versions, hashes, lifecycle states, source citations, criteria, audit events, and review declarations.
CES migration knowledge is version 6 and cites six exact source revisions.
Wiki navigation contributes freshness fingerprints. It does not supply a second collection of governed graph facts.

The bundle is local generated output under `relationships/service-dependencies/generated/`.
Keep its manifest and projections together.
The generated [viewer](../../relationships/service-dependencies/generated/relationship-viewer.html) needs no graph database, API key, or external assets.
Generated graph files remain excluded from Git under the existing workspace rule.
The [setup evidence](../evidence/knowledge-graph-setup-20261111/setup.json) retains snapshot checksums and actual check results.

## Open, refresh, and query

Run these commands from the Workbench root with its installed environment.

```sh
open relationships/service-dependencies/generated/relationship-viewer.html
.venv/bin/python -m ai_sdlc_workbench --workspace . graph build
.venv/bin/python -m ai_sdlc_workbench --workspace . call service-dependencies knowledge --args '{"type":"KNOWLEDGE_RECORD","governance_state":"candidate","limit":200}'
```

Search a record ID, filter its governance state, then select a node or relationship to inspect sources and backlinks.
The registered resource also supports `references` and bounded `paths` queries.
Copy exact node IDs from query results. Read source records before using their claims for engineering decisions.
Rebuild after changing knowledge, source declarations, catalogs, or repository inputs.

## Context maintenance

The build required a refresh of the [existing architecture context](../../relationships/service-dependencies/architecture-context.json).
The review compared 46 source bindings and reinvestigated six changed source files across four affected relationships.
It preserved all context IDs and 23 investigation assessments.

It corrected an obsolete claim that data-role reads always use EMS2.
Current source dispatch can select EMS3 through a mode and allowed-user gate.
Active configuration and runtime dispatch remain unverified.
The refresh also updates loader descriptions, source hashes, independent revisions, and exact citation ranges.

## Validation and limits

The deterministic build passed schema and projection validation before publishing the bundle.
Queries confirmed 12 current candidates, zero published domain records, CES version 6, six source citations, and direct navigation paths.
The configured Workbench resource returned the same 12 candidates.
The browser check passed in Microsoft Edge with no JavaScript errors or external HTTP requests.
It checked record filters, lifecycle filters, local source links, citations, and Knowledge/Architecture tab switching.
Protected canonical records, snapshots, manifest entries, and audit bytes remained unchanged.

The graph retains unresolved references instead of selecting replacement identities.
The depth-one citation query found its target and reported `MAX_DEPTH` for other branches.
This query does not establish complete path enumeration.
Local freshness checks do not establish external source freshness, semantic truth, deployment, or business execution.
The graph grants no publication or business approval.

## Output review

```json
{
  "asd_review": "PENDING",
  "automated_check": "PASSED",
  "findings": [],
  "limitations": [
    "Automated checks do not check the complete approved dictionary or grammar rules."
  ],
  "reviewed_at": null,
  "reviewer": null,
  "standard": "ASD-STE100"
}
```
