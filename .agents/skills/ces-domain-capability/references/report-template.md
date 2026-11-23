# EMS2 to CES compatibility scan

## Scope

| Repository | Revision | Layer | Inspected roots | Limits |
| --- | --- | --- | --- | --- |
|  |  | UI/shared/BFF/auth/SDK |  |  |

Old contract:

CES source and sample:

Upper-layer source-change constraint:

## Findings

| ID | Category | Disposition | Repository | Source locator | Consequence | Lower-layer action | Owner |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |

For every finding, describe these facts below the table:

- **Observed:** exact source behavior and revision.
- **CES evidence:** field, cardinality, action, or response shape.
- **Old result:** behavior under EMS2.
- **CES result:** behavior under the candidate projection.
- **Preservation limit:** why a lower layer can or cannot preserve the old API.
- **Verification:** test assertion, runtime observation, or `not-observed` limit.

## Coverage

- Repositories searched:
- Files enumerated:
- Candidate matches reviewed:
- Test files reviewed:
- CES samples reviewed:
- Live runtime executed: `no` / `yes`, with environment and limits.

## Decision

State whether zero upper-layer source changes remain credible, which findings block that claim, and the next owner action. Keep unresolved policy separate from implementation defects.
