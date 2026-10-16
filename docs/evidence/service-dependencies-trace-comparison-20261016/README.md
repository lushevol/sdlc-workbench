---
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
  - SVG exports use the shipped renderer. They are not browser screenshots.
  - Static source facts do not establish runtime execution or deployment.
  - Parent and local repository inventories differ.
---

# Service dependency trace comparison

Comparison date: 16 October 2026.
The updated skill preserves method callsites, SQL method context, imported frontend wrappers, and routing limits.
The viewer separates repository links, API paths, shared code, configuration, storage, messages, and package declarations.

## Source scope

The local graph contains nine repositories.
The parent graph contains thirteen repositories.
The two inventories share four repositories.
The local graph has five repositories that the parent graph does not have.
The parent graph has nine backend repositories that the local graph does not have.
Counts across the two inventories do not measure extractor quality by themselves.

The parent source was rebuilt with the updated skill.
The local source was rebuilt with the previous skill and the updated skill.
Source fingerprints match within each before and after comparison.

## Measured change

| Snapshot | Production nodes | Production edges | Provided APIs | Provided traces with method calls | Method callsites | SQL method sites | Highest links |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Local previous skill | 6,135 | 12,669 | 41 | 0 | 0 | 0 | 3 |
| Local updated skill | 6,144 | 12,729 | 41 | 35 | 1,138 | 40 | 4 |
| Parent previous skill | 2,456 | 4,259 | 175 | 0 | 0 | 0 | 33 |
| Parent updated skill | 10,722 | 26,763 | 175 | 149 | 21,390 | 41 | 36 |

The parent updated graph has more repositories and more source declarations.
Its totals cannot represent the local workspace because nine backend repositories are absent locally.

## What the pictures show

The overview pair shows one additional resolved aggregate link.
The API pair shows method paths and separate declaration context.
The frontend picture shows imported HTTP wrapper calls that were previously absent.
The storage picture shows table and column declarations without claiming execution.
The configuration picture keeps complete names and directed edges.
The parent configuration and messaging pairs show the updated extraction on the identical parent source set.
The focused trace picture shows the `/tile/data` method path and selected SQL methods.

- [Overview before](01-overview-before.png) and [after](01-overview-after.png)
- [API trace before](02-api-trace-before.png) and [after](02-api-trace-after.png)
- [Focused `/tile/data` trace](13-trace-focus-after.png)
- [Configuration](03-configuration-after.png)
- [Imported frontend calls](04-frontend-calls-after.png)
- [Storage and columns](05-storage-after.png)
- [Shared code](06-shared-after.png)
- [GraphQL](07-graphql-after.png)
- [Business structure](08-business-after.png)
- [Package declarations](09-packages-after.png)
- [Parent configuration before](10-parent-config-parent.png) and [after](10-parent-config-parent_after.png)
- [Parent messaging before](11-messaging-parent.png) and [after](11-messaging-parent_after.png)

SVG exports remain beside each PNG.
The machine-readable [comparison data](comparison.json) contains source fingerprints, counts, trace integrity results, and repository differences.
The [trace cases](trace-cases.json) record selected methods, evidence stops, and traversal limits.

## Trace limits

Implementation alternatives remain unselected because static declarations do not establish runtime dispatch.
Database mappings remain declaration context and do not establish executed access.
Dynamic clients and routing mutations remain unresolved.
Deferred callbacks remain declaration context.
Each trace records six-hop, 160-node, and 240-edge limits.

## Validation

Automated validation passed for the skill suite, Workbench suite, graph snapshots, package smoke test, and wheel build.
Visual review used SVG exports from the shipped renderer.
Browser screenshots were unavailable in the current environment.
Full ASD-STE100 review remains pending.
