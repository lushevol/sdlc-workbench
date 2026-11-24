# Context responsibility

The context layer loads workspace configuration and registry declarations.
This directory implements catalog loading.
The shared workspace loader lives in `core/workspace.py`.
Repository, service, capability, and tool declarations identify available engineering context.
Catalog entries do not establish knowledge authority or freshness.
Use the knowledge review procedures and deterministic provenance checks for their separate evidence boundaries.
