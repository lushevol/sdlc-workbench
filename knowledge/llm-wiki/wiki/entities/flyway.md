---
sources: ["summaries/KT-admin-and-onboarding.md"]
type: "Product"
description: "Database migration tool whose retained SQL defines the portal admin catalog schema draft."
---

> Derived candidate/draft knowledge; publication review remains pending. [Canonical source bindings](../../source-manifest.json).

# Flyway

Flyway is a database migration tool. In the [[summaries/KT-admin-and-onboarding]] material, Flyway holds the retained SQL definitions for the admin catalog of the [[entities/fmo-post-trade-portal]].

## Role in the portal admin module

The Flyway page configures a schema-history table and enables migration baselining from version zero. Baseline migration lets the tool adopt an existing schema without replaying older migration scripts.

These are retained design definitions. They do not establish a confirmed deployed schema or an executed migration.

## Catalog schema in the retained SQL

The SQL describes the data model behind [[concepts/admin-catalog-configuration]]:

- Import-map records have unique keys.
- Category records have unique labels.
- Tile records reference both category records and import-map records through foreign keys.
- Separate import-map, category, and tile audit tables preserve change history.

These relationships show the design vocabulary for module mappings, drawer categories, and tile configuration. The audit tables match the change-history idea in the [[concepts/maker-checker-verification-workflow]], but the text does not show that the SQL enforces that workflow.

## Evidence limits

No inspected deployment or connectivity execution exists for this SQL. The retained definitions cannot establish the current schema, the active migration state, or the applied constraints.

Owner: unknown. Next action: connect applicable migrations and environment-specific checks before an onboarding change uses this schema.

## Related pages

- [[summaries/KT-admin-and-onboarding]]
- [[concepts/admin-catalog-configuration]]
- [[concepts/maker-checker-verification-workflow]]
- [[entities/fmo-post-trade-portal]]
- [[entities/single-ui-bff]]
