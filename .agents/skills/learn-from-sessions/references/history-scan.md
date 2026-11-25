# History scan contract

The scanner emits a bounded JSON review inventory. It records task and session paths, hashes, sizes, headings, and reusable-material signals. It does not copy source content or expose matched values.

Every session scan uses `--past-duration`, which accepts positive values such as `7d`, `1w`, or `24h`. It defaults to `7d` and records the UTC cutoff. Files outside the cutoff are excluded from session inputs. Durable task records remain available for task context.
Default inputs are durable files under `tasks/`. Add explicit `--path` values for retained session exports or another approved history directory. Use `--include-workbench` only when the session state is part of the evidence scope.

The ignored `.workbench/experience/scan-state.json` records each session's latest source fingerprint, latest source time, scan window, and scan time. An unchanged session with the same window is reported as skipped. A changed file, latest timestamp, or duration causes a new scan.

Treat every signal as a search hint. Read the source file and its evidence before using it. A filename, heading, status word, or passing command does not prove a successful domain outcome.

Run from the workspace root:

```sh
python3 .agents/skills/learn-from-sessions/scripts/scan_history.py --workspace . --past-duration 7d --path RETAINED_EXPORT --output .workbench/experience/history.json
```

The scanner output is disposable review working state with `review_status: PENDING`.
It never creates a packet or changes the experience index.
Preserve candidate decisions before packaging selected recipes through [experience-packets.md](experience-packets.md).
Reuse explicit authorization that already selects the candidates and packaging scope.
Otherwise, obtain their approve, reject, or revise decisions.
Keep the review bundle and packet provenance.

Signals include preferences, corrections, exploration, and failed attempts.
These hints do not establish a durable preference, verified explanation, or successful recipe.
A scan-state fingerprint records inventory work only.
If semantic review or its output is missing, inspect the earlier inventory and source despite an unchanged fingerprint.
