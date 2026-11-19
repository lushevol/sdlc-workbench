# History scan contract

The scanner emits a bounded JSON inventory. It records task and session paths, hashes, sizes, headings, and reusable-material signals. It does not copy source content or expose matched values.

Default inputs are durable files under `tasks/`. Add explicit `--path` values for retained session exports or another approved history directory. Use `--include-workbench` only when the session state is part of the evidence scope.

Treat every signal as a search hint. Read the source file and its evidence before using it. A filename, heading, status word, or passing command does not prove a successful domain outcome.

The scanner output is disposable working state. Promote only the selected packet, its provenance, and the task links.
