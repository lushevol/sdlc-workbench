"""Compare downloader cancellation against the committed setup baseline."""

import hashlib
import importlib.util
import inspect
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time


root = Path(__file__).resolve().parents[3]
output = Path(__file__).resolve().parent
baseline = subprocess.run(["git", "rev-parse", "b98215fdb"], cwd=root, capture_output=True,
                          text=True, check=True).stdout.strip()
old_source = subprocess.run(["git", "show", f"{baseline}:core/bootstrap.py"], cwd=root,
                            capture_output=True, check=True).stdout

for name, source in (("baseline", old_source), ("candidate", (root / "core/bootstrap.py").read_bytes())):
    with tempfile.TemporaryDirectory(prefix="workbench-timeout-proof-") as temporary:
        folder = Path(temporary)
        script = folder / "bootstrap.py"
        script.write_bytes(source)
        spec = importlib.util.spec_from_file_location("timeout_probe_" + name, script)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        started, completed = folder / "started", folder / "completed"
        child = ("import pathlib,sys,time; pathlib.Path(sys.argv[1]).write_text('started'); "
                 "time.sleep(2.5); pathlib.Path(sys.argv[2]).write_text('continued after cancellation')")
        parent = ("import subprocess,sys,time; "
                  f"subprocess.Popen([sys.executable, '-c', {child!r}, sys.argv[1], sys.argv[2]]); "
                  "time.sleep(60)")
        options = {"seconds": 1}
        if "download" in inspect.signature(module.command).parameters:
            options["download"] = "python"
        began = time.monotonic()
        try:
            module.command([sys.executable, "-c", parent, str(started), str(completed)], folder, **options)
            raise AssertionError("The stalled command must fail.")
        except module.SetupError as error:
            message = str(error)
        elapsed = time.monotonic() - began
        assert started.exists(), "The downloader child must start before cancellation."
        time.sleep(2.6)
        result = {"case": name, "baseline_revision": baseline, "source_sha256": hashlib.sha256(source).hexdigest(),
                  "selected_timeout_seconds": 1, "elapsed_seconds": round(elapsed, 3), "message": message,
                  "child_started": True, "child_continued_after_timeout": completed.exists(),
                  "manual_recovery_guidance": "--offline-bundle PATH" in message,
                  "limits": ["Controlled local process; no public download or company endpoint was contacted.",
                             "Execution proves cancellation on this host only."]}
        (output / (name + "-timeout.json")).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        assert result["child_continued_after_timeout"] == (name == "baseline")
        assert result["manual_recovery_guidance"] == (name == "candidate")
        print(name + ": cancellation assertions passed")
