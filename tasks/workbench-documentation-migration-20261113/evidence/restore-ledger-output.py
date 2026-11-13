"""Recreate a historical derived ledger from retained source inputs; start no business runner."""
import hashlib
import importlib
import json
from pathlib import Path
import sys

if len(sys.argv) != 5:
    raise SystemExit("usage: restore-ledger-output.py WORKSPACE_ROOT RECEIPT MANIFEST RECOVERED_OUTPUT")
root = Path(sys.argv[1]).resolve()
receipt = json.loads(Path(sys.argv[2]).read_text())
manifest_raw = Path(sys.argv[3]).read_bytes()
assert hashlib.sha256(manifest_raw).hexdigest() == receipt["manifest"]["sha256"], "manifest hash differs"
for code in receipt["generator_sources"]:
    assert hashlib.sha256((root / code["path"]).read_bytes()).hexdigest() == code["sha256"], "generator source differs: " + code["path"]
for source in receipt["source_inputs"]:
    for name in ("source", "binding"):
        if name in source:
            item = source[name]
            assert hashlib.sha256((root / item["path"]).read_bytes()).hexdigest() == item["sha256"], "source input differs: " + item["path"]
sys.path.insert(0, str(root))
build_case_ledger = importlib.import_module("core.review_coverage").build_case_ledger
report = build_case_ledger(json.loads(manifest_raw), root)
raw = (json.dumps(report, indent=2) + "\n").encode("utf8")
assert report["valid"] and report["freshness"] == "CURRENT", "nested source evidence is not current"
assert hashlib.sha256(raw).hexdigest() == receipt["original_output"]["sha256"], "derived output differs"
output = Path(sys.argv[4])
if output.exists():
    raise SystemExit("recovered output already exists")
output.write_bytes(raw)
print(receipt["original_output"]["sha256"])
