# History scan contract

The scanner emits a bounded JSON review inventory. It records task and session paths, hashes, sizes, headings, and reusable-material signals. It does not copy source content or expose matched values.

Every session scan uses `--past-duration`, which accepts positive values such as `7d`, `1w`, or `24h`. It defaults to `7d` and records the UTC cutoff. Files outside the cutoff are excluded from session inputs. Durable task records remain available for task context.
Default inputs are durable files under `tasks/`. Add explicit `--path` values for retained session exports or another approved history directory. Use `--include-workbench` only when the session state is part of the evidence scope.

The ignored `.workbench/experience/scan-state.json` records each session's latest source fingerprint, latest source time, scan window, and scan time. An unchanged session with the same window is reported as skipped. A changed file, latest timestamp, or duration causes a new scan.

Treat every signal as a search hint. Read the source file and its evidence before using it. A filename, heading, status word, or passing command does not prove a successful domain outcome.

The scanner output is disposable review working state with `review_status: PENDING`. It never creates a packet or changes the experience index. Promote only after the user approves selected candidate IDs, then preserve the review bundle and packet provenance.
