# Test engine entry-point inspection

No critical conclusions require user attention or action.

The [user request](user-input.txt) defines this inquiry.
Repository HEAD: `78141a4eec8040dd0d1ac8a6579b20f612fca0f0`.
The worktree had modified `CLAUDE.md` and untracked `playwright-log.txt`.
This inspection changed neither file. No business test ran.

## Confirmed entry points

| Claim | Class and confidence | Evidence | Limit |
| --- | --- | --- | --- |
| The Robot session suite contains 22 E2E cases. | Inspected implementation; high | [Suite](../../../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/session_renewal.robot), lines 15–136 | Source inspection does not establish passing execution. |
| `--include E2E-15` selects one stable case. | Inspected implementation; high | [Suite](../../../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/session_renewal.robot), lines 94–97 | Setup still requires a prepared target and browser. |
| Long cases require `SESSION_ALLOW_LONG_RUNNING:True`. | Inspected implementation; high | [Gate](../../../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/session_renewal.robot), lines 146–148 | Without opt-in, the gate skips cases. Real expiry can take hours. |
| Session setup requires exact application revisions and a timing profile. | Inspected implementation; high | [Validation](../../../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/support/session.cjs), lines 23–43 | Declared revisions do not bind deployed bytes. |
| Generated UI suites import private environment data and encryption keys. | Inspected implementation; high | [Imports](../../../../repos/testing/ratan-test-engine/Tests/ratan/workspace/ui/__import__.resource), lines 39–46 | Private configuration was not opened. |

The [canonical setup](../../../../repos/testing/ratan-test-engine/docs/WORKBENCH.md#isolated-setup) specifies Python 3.13 and `uv sync --locked --python 3.13`.
The full profile is required for business libraries.
Neither profile installs browser binaries automatically.
The [existing browser installer](../../../../repos/testing/ratan-test-engine/Install/browser.bat), line 4, invokes `rfbrowser init`.
On this macOS checkout, use `.venv/bin/rfbrowser init` when browser initialization is needed.
The wrapper's proxy declarations are machine-specific.
Session browser defaults are visible Chromium with channel `msedge`.
The suite does not start the portal or authentication stack.

The [session execution guide](../../../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/README.md#execution) documents these selections:

```sh
.venv/bin/python -m robot --outputdir .workbench/session-renewal/e2e-15-run-001 --include E2E-15 --variable SESSION_CONFIG:.workbench/session-renewal/config.json Tests/ratan/plugin/ui/session/session_renewal.robot
.venv/bin/python -m robot --outputdir .workbench/session-renewal/quick-run-001 --exclude long-running --exclude diagnostic --variable SESSION_CONFIG:.workbench/session-renewal/config.json Tests/ratan/plugin/ui/session/session_renewal.robot
```

Copy `config.example.json` into the ignored `.workbench/session-renewal/` directory before editing.
Confirm target URL, selectors, expected lifetimes, and both full application Git hashes.
Supply credentials through `SESSION_E2E_USERNAME` and `SESSION_E2E_PASSWORD` in the private process environment.
The example's 900-second expectation needs confirmation against the selected environment.
Robot reports use `--outputdir`. JSON results and screenshots use configuration `artifactDir`.
The `cases/e2e-*.cjs` modules load through the Browser extension. They are not standalone Node runners.

## Existing generated suites

A verified existing selector is `CN-UI-E2E-HOLD-OO1-OO1`.
Its [suite](../../../../repos/testing/ratan-test-engine/Tests/ratan/workspace/ui/CN-UI-E2E-HOLD.robot), lines 18–58, creates cashflows and changes their state.
The following values are examples. Match the prepared private `env_${ENV}_${SECRET}.yaml` file.

```sh
.venv/bin/python -m robot --outputdir .workbench/business-ui/run-001 --variable ENV:uat2 --variable SECRET:secret --variable LANG:0 --test "CN-UI-E2E-HOLD-OO1-OO1" Tests/ratan/workspace/ui/CN-UI-E2E-HOLD.robot
```

Do not regenerate workbooks merely to execute existing suites.
Report upload helpers remain optional. They can upload or remove result files.
The [native observation runner](../../../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/real-world/README.md#execute-cases) uses separate browser configuration and `RW-*` selectors.
It is separate from both Robot and the frontend E2E runner.

## Source identities and performed checks

| Source | SHA-256 |
| --- | --- |
| `docs/WORKBENCH.md` | `1fc1bb142918031aade119696779ec48bb7a4b5db3cb6c79a9e10ddbd42707d6` |
| `Tests/ratan/plugin/ui/session/README.md` | `69b0c8f97459aaae5311a22ea85e5e7276fbeadef9570ec0a1aea8afd38cf7a9` |
| `Tests/ratan/plugin/ui/session/session_renewal.robot` | `27b26a7d9152154e712833ae27ca7b044759b74bb4ab23e4631f338314f07520` |
| `Tests/ratan/plugin/ui/session/config.example.json` | `07279d6b7fdc36a27434ff12f21332e49f8487aec11e6275cfaf058a646fe833` |
| `Tests/ratan/plugin/ui/session/support/session.cjs` | `1c7d5c1157966f01653f8a26069dc90d0c811a430883d8920100ac5fa339b0d5` |
| `Tests/ratan/workspace/ui/__import__.resource` | `a8fe3c80eebb9286747d79c518b52466827c994ca279b84a763facdee7ff48d8` |
| `Tests/ratan/workspace/ui/CN-UI-E2E-HOLD.robot` | `0f3b42b5c9fb85db86317d6554cbe80ea8b0552b5876070908c6efa629dde042` |

`.venv/bin/python -m robot --version` reported Robot 7.2.2 and Python 3.13.14 on macOS.
Robot returned its version-display status, `251`. No suite ran.
`.venv/bin/python scripts/workbench.py --help` succeeded and listed `doctor`, `inventory`, and `parse`.
Commands were checked against current source and documented interfaces.
Target connectivity, credentials, browser launch, and case assertions remain untested.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```
