# CES frontend migration patches

Full Git diffs, including tests, from each original baseline to its amended delivery commit.
These include the latest optimization. Apply each file in its own repository.

| Repository | Base | Delivery commit | Files | Added / deleted |
| --- | --- | --- | ---: | ---: |
| mfe-base | `4c36f8e14e3d9f178b226000ebbcb41aa611616a` | `10560f39a57e8ce4010cee634f7682559b1a6bdd` | 26 | +846 / -84 |
| mfe-ratan-container | `647e6b3e703e5144ab4b37c4b43aa22a28dfdd07` | `a7e38d048545dd913ae5996a1475980056de18bd` | 11 | +1534 / -26 |

Container's base is the supplied source snapshot. It is not a confirmed PROD revision.
Each delivery branch now has one commit above the listed baseline.
`manifest.json` records file lists, checksums, backup refs, and verification.

## Apply internally

Copy this folder to the internal machine. In each corresponding repository,
start from the listed baseline or review any differences from it, then create a delivery branch:

```sh
git switch -c codex/ces-entitlement-migration
git apply --check /absolute/path/to/mfe-base.diff
git apply --index /absolute/path/to/mfe-base.diff
```

Use `mfe-ratan-container.diff` for the container repository.
The staged patch includes production source and tests; review it and run your owning checks before committing internally.
These are plain `git diff` files for `git apply`, not `git am` mail patches.

Each patch passed `git apply --cached --check` against a temporary index loaded from
its exact baseline. Applying it produced exactly the amended commit's Git tree.
Original working directories were not changed by this verification.

## Validation and remaining gaps

- Base: 515/515 tests in 130 suites; final test-typing correction: 9/9 focused checks; full TypeScript passed.
- Container: 84/84 tests in nine focused suites; selected type check passed. The full container build was not run.
- Controlled browser: 16/16 cases; controlled portal: 4/4 checkpoints. Source hashes match exported source.
- No live CES or deployed upper application verification. Actual logger test mocks transport; remote collection remains unverified.
- Scalar `getUser().role` mapping and CES role-owned writes remain unresolved. Existing UAT logger delivery policy remains.

BFF is unchanged by this squash. The current companion BFF revision is
`95480c0e2563bc2a5a639bca1f22ecedb61936c2` (main baseline
`834b4155232222347220e47139a502ee43a9cbdf`). Its patch is outside this two-UI export.

For detailed behavior and compatibility gaps, see the task's
[adapter review](../../10-change-review-frontend-adapters.md) and
[compatibility audit](../../11-zero-upper-change-audit.md).
