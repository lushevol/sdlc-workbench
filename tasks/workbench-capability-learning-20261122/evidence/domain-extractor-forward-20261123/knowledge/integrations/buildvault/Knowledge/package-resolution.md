# Package resolution: concepts and evidence limits

## Applicability and confidence

All sources and retained examples in this trial are synthetic.
The API specification has revision `vendor-v2`.
Captured requests use API v2 in `lab` on 2026-11-23.
The session names pipeline alpha; successful captured queries use project alpha.
This does not establish a general pipeline-to-project mapping.

Confidence is direct source support within this synthetic scope.
There is no live-system, production, deployment, acceptance, or publication evidence.

The [contract](../Contracts/packages-v2.openapi.yaml) owns wire definitions.
The [workflow](../Workflows/resolve-exact-commit.md) owns operational steps and stop conditions.

## Documented API subset

`GET /v2/packages` requires the string query parameter `project`.
The string parameters `branch` and `cursor` are optional.
A 200 JSON response contains a package array.
Each package requires `id` and `name`; their types are unspecified in the specification.
The optional `next` field accepts a string or null.

These requirements come from specification line 3.
The specification does not define authentication, errors, defaults, or total counts.
No source supplies a scoped base URL or credential values.

## Observations and selection meaning

The source commit is compared with `package.commit` when that field is available.
A missing commit prevents exact selection for that package.
This is the session's selection rule, not a vendor-required response field.

| Stable case | Exact condition | Observation and limit |
| --- | --- | --- |
| [wildcard-empty](../Contracts/examples/wildcard-empty.json) | `project=alpha`, `branch=release/*`, no cursor | Empty packages, HTTP 200, `next-1`; result completeness is unproved |
| [exact-branch](../Contracts/examples/exact-branch.json) | `project=alpha`, `branch=release/2`, no cursor | Package `p2`, name `bundle`, commit `abc123`, retention null; `next=null` |
| [forbidden](../Contracts/examples/forbidden.json) | `project=restricted`, branch and cursor omitted | HTTP 403; error `AccessDenied`, trace `synthetic-trace` |

The exact-branch capture supports a candidate for requested commit `abc123`.
It does not establish commit normalization, real hash length, global uniqueness, or download availability.
Observed `commit` and null `retention` are not required vendor fields.
One null retention value does not define the field's complete type or retention policy.

Only these branch requests were tried.
The sources do not establish that wildcards are unsupported or that exact branches always succeed.
A returned string cursor does not prove continuation was executed.
An empty first page with a cursor does not prove there are no packages.

A token change followed the 403.
No later request was retained, so the cause and correction remain unknown.
The sources do not establish the authentication mechanism or required permission.

## Legacy scope retained

The [existing convention](conventions.md) applies to legacy pipeline beta in 2025.
It remains documented historical information, not an observation from this trial.
Its `beta-<build>` naming rule does not apply to alpha.
The [legacy-beta pair](../Contracts/examples/legacy.json) remains unchanged.
Its historical memo revision, observation date, endpoint contract, and live validation are unavailable.

There is no conflict established between that legacy scope and API v2 lab captures.

## Unresolved boundaries

- Scoped endpoint, authentication, permission policy, headers, and access prerequisites.
- Omitted-branch behavior, branch matching, cursor lifecycle, and omitted-`next` semantics.
- Additional pages, pagination bounds, retries, timeouts, and total counts.
- Vendor field types for package ID/name; guaranteed commit availability and full retention schema.
- Other error cases, response media type for the 403, and required error fields.
- Duplicate-candidate selection, download, deployment, rollback, and live completion assertions.

No missing behavior was fabricated or executed to close these gaps.

## Source bindings

| Source | Exact locator and revision/date | SHA-256 |
| --- | --- | --- |
| [Specification](../../../../sources/spec.md) | Lines 1-3; synthetic revision `vendor-v2`; date not supplied | `6c1c5f8c85adc3bbdf7ddb1e23ea04d5ad486bde7a4fde07598ff97b5dbcd336` |
| [Session](../../../../sources/session.md) | Lines 1-8; 2026-11-23, lab, alpha | `0f331635032129452ed85cb3589bd1fe847e6c732bb745c0c8649d6e03acb104` |
| [Exchanges](../../../../sources/exchanges.json) | `/0`, `/1`, `/2`; each 2026-11-23, lab | `f27dcde489f2b2da7132d64a93fe5cb9b6f13b5b9d6f17cbf85bef308f3bb415` |

The paired examples preserve each source request and response without modification.
Added operation and provenance fields are extraction metadata.
Original source bytes remain outside the library and were not changed.
