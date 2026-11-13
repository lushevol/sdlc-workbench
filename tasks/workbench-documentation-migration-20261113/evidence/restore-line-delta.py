"""Restore exact historical output from a SHA-bound line delta, without rerunning a graph tool."""
import hashlib
import json
from pathlib import Path
import sys

if len(sys.argv) != 4:
    raise SystemExit("usage: restore-line-delta.py RECEIPT BASE_OUTPUT RECOVERED_OUTPUT")
receipt = json.loads(Path(sys.argv[1]).read_text())
base = Path(sys.argv[2]).read_bytes()
assert hashlib.sha256(base).hexdigest() == receipt["base"]["sha256"], "base hash differs"
lines = base.decode("utf8").splitlines(keepends=True)
for op in reversed(receipt["line_edits"]):
    lines[op["base_start_line"]:op["base_end_line"]] = op["insert_text"].splitlines(keepends=True)
restored = "".join(lines).encode("utf8")
assert hashlib.sha256(restored).hexdigest() == receipt["original"]["sha256"], "restored hash differs"
output = Path(sys.argv[3])
if output.exists():
    raise SystemExit("recovered output already exists")
output.write_bytes(restored)
print(receipt["original"]["sha256"])
