# Workflow: resolve a package for an exact source commit

## Purpose and applicability

Resolve a candidate package by comparing its commit with the requested source commit.
The retained scenario uses synthetic BuildVault v2, lab environment, and pipeline/project alpha on 2026-11-23.
The workflow remains partial: pagination, download, and deployment were not executed.

Use the [listing contract](../Contracts/packages-v2.openapi.yaml) and [source boundaries](../Knowledge/package-resolution.md).
The operation identity is `listPackages`.
This reference does not grant access or authorize execution.

## Prerequisites and inputs

| Input | Type and source | Supported values or limits |
| --- | --- | --- |
| `project` | Required API string; supplied project | `alpha` in successful captures; `restricted` returned 403 |
| `branch` | Optional API string; requested branch | `release/2` and `release/*` were tried; no default is documented |
| `target_commit` | Local string from the exact requested source revision | Compare with `package.commit`; it is not an API parameter |
| `cursor` | Optional API string from a returned cursor | `next-1` was returned; no continuation request was retained |
| Base URL | Authorized environment configuration | Not supplied; obtain it before any live operation |
| Access configuration | Authorized connector configuration | Authentication method and required permissions are unknown |

The synthetic candidate has commit `abc123`.
This value does not establish accepted real commit lengths or normalization rules.
Do not put credential values into contracts or examples.

## Procedure

1. Record the requested project, branch, environment, API version, and exact source commit.
   Stop exact selection when the requested commit is unavailable.
   Verify authorized endpoint and access configuration before any live request.
2. Call `GET /v2/packages` with required `project` and optional `branch`.
   The retained exact-branch request is `project=alpha`, `branch=release/2`, without a cursor.
   Its [paired case](../Contracts/examples/exact-branch.json) returned HTTP 200 and package `p2`, named `bundle`.
3. Inspect the response status before reading a package page.
   A successful page contains `packages`; each package requires `id` and `name` under vendor-v2.
   The specification does not guarantee a `commit` field.
4. Compare the requested source commit with each available `package.commit`.
   The retained `p2` value is `abc123`; this supports a match only when the requested commit equals `abc123`.
   A package without a commit cannot establish an exact match.
   Do not substitute its name, branch, or package ID for commit evidence.
5. Inspect the optional `next` property, including on empty pages.
   The [wildcard case](../Contracts/examples/wildcard-empty.json) returned no packages and `next="next-1"`.
   That response does not establish an empty complete result.
   The documented cursor parameter supplies a continuation input; no cursor request was captured.
   Preserve project and branch when preparing continuation, and obtain an authorized paging limit before running it.
   This continuation procedure is unverified in the trial.
6. Record candidate identity, observed commit, request condition, response, and source binding.
   The exact-branch capture returned `next=null`; no later pages were retained.
   The specification gives cursor types but does not define omitted-cursor completion semantics.
   Stop for clarification if completeness or duplicate matches affect selection.
7. End this procedure at the evidence-backed candidate result.
   Download and deployment interfaces, assertions, recovery, and execution remain unsupported.

## Decision rules

The session requires commit comparison when `package.commit` is available.
A missing commit prevents exact selection for that package.
This rule comes from session lines 3-4, not the vendor schema.

The following are conservative procedure guards, not observed vendor guarantees:

- Stop on multiple candidate matches until a selection rule is supplied.
- Stop when absent `next` leaves required completeness unresolved.
- Do not retry a failed request until access and retry policy are established.
- Stop at any unknown download or deployment step.

No retry count, timeout, automatic branch fallback, or wildcard interpretation was established.

## Failure points

| Case | Attempt and actual result | Cause status and next action |
| --- | --- | --- |
| `wildcard-empty` | `alpha`, `release/*`: HTTP 200, empty packages, `next-1` | Branch semantics remain unknown; continuation was not retained |
| `exact-branch` | `alpha`, `release/2`: HTTP 200, one matching-commit candidate for target `abc123`, `next=null` | Different request succeeded; this does not prove a universal wildcard correction |
| `forbidden` | `restricted`, branch omitted: HTTP 403, `AccessDenied`, `synthetic-trace` | Cause unknown; token changed later, with no retained follow-up request |

Preserve the [403 pair](../Contracts/examples/forbidden.json) and session line 6.
A token change does not establish the authentication mechanism, cause, or a successful correction.

## Verification and recovery

For a candidate, retain its requested commit, actual `commit`, ID, name, request, response, and evidence source.
Check that the two commit values match before claiming exact selection.
Check page completeness and conflicting candidates before claiming a unique result.
These are procedure assertions; the trial performed only offline extraction checks.

No download, deployment, live request, retry, continuation, rollback, or recovery was executed.
There is no demonstrated live mutation to reverse.
Any later execution needs its own authorized endpoint, access, bounds, and retained results.

## Evidence

- [Session](../../../../sources/session.md), lines 1-8; 2026-11-23, lab, alpha.
- [Vendor specification](../../../../sources/spec.md), lines 1-3; revision `vendor-v2`.
- [Exchanges](../../../../sources/exchanges.json), JSON pointers `/0`, `/1`, and `/2`; 2026-11-23, lab.
- [Hashes and limitations](../Knowledge/package-resolution.md#source-bindings).
