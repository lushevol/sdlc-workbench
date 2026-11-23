# BuildVault

Synthetic integration reference for the documented API v2 subset and retained lab cases from 2026-11-23.
The library also preserves the separate legacy beta scope from 2025.
Extraction does not establish live behavior or authorize execution.

- [Package listing contract](Contracts/packages-v2.openapi.yaml): operation `listPackages`; query and response definitions.
- Paired cases: [wildcard-empty](Contracts/examples/wildcard-empty.json), [exact-branch](Contracts/examples/exact-branch.json), [forbidden](Contracts/examples/forbidden.json).
- [Exact-commit resolution workflow](Workflows/resolve-exact-commit.md): selection steps, paging boundary, failures, and stop conditions.
- [Package concepts, evidence hashes, and limits](Knowledge/package-resolution.md).
- [Existing convention](Knowledge/conventions.md): legacy beta names; do not extend this rule to alpha.
- [Existing package case](Contracts/examples/legacy.json): unchanged `legacy-beta` pair.

Authentication, permissions, endpoint, cursor semantics, and retry policy remain incomplete.
No continuation request, successful 403 correction, package download, or deployment was retained.
