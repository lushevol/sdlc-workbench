# Source adapter boundary

Source adapters connect external engineering sources to the shared knowledge contracts.
Examples include document systems, issue trackers, source repositories, API specifications, and test catalogs.
Each adapter must preserve the original source identity and access limits.

An adapter must:

1. Use a registered source ID and the source's supported access mechanism.
2. Keep credentials outside tracked workspace configuration.
3. Record original locators, source revisions, retrieval times, and retained-byte hashes.
4. Preserve unchanged raw bytes when local retention is permitted.
5. Create new snapshots for changed source versions.
6. Distinguish source text from extracted candidate knowledge and findings.
7. Retain errors, omissions, and access limits without inventing source content.
8. Use shared Workbench validation and execution grants where applicable.

Registration does not grant access or execution.
The current `knowledge.local` provider reads configured local Markdown and text files.
It does not implement remote document synchronization or automatic governance.
This directory defines future adapter responsibilities; it ships no external source connector.

Read the [workspace design](../../docs/WORKSPACE_DESIGN.md) and [ingestion procedure](../../.agents/skills/ingest-knowledge/SKILL.md).
