#!/usr/bin/env python3
"""Compare restored files with exact Git blobs without changing the repository."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import xml.etree.ElementTree as ET


def verify(repository, revision, names, xml=False):
    repository = Path(repository).resolve()
    environment = dict(os.environ, GIT_OPTIONAL_LOCKS="0", GIT_CONFIG_NOSYSTEM="1")

    def git(*arguments):
        result = subprocess.run(
            ["git", "-c", "core.fsmonitor=false", "-C", str(repository), *arguments],
            env=environment, capture_output=True, check=True, timeout=30,
        )
        return result.stdout

    commit = git("rev-parse", "--verify", "--end-of-options", revision + "^{commit}").decode().strip()
    results = []
    for name in names:
        path = Path(name)
        if path.is_absolute() or ".." in path.parts or not path.parts:
            raise ValueError("Use repository-relative paths without parent traversal.")
        path = repository / path
        if path.is_symlink() or not path.resolve().is_relative_to(repository):
            raise ValueError("Use regular files inside the selected repository.")
        original = git("cat-file", "blob", commit + ":" + name)
        current = path.read_bytes()
        matched = current == original
        result = {
            "path": name,
            "status": "PASSED" if matched else "FAILED",
            "historical_sha256": hashlib.sha256(original).hexdigest(),
            "current_sha256": hashlib.sha256(current).hexdigest(),
            "bytes": len(current),
        }
        if xml:
            document = ET.fromstring(current)
            result["xml_root"] = document.tag
            result["diagram_pages"] = len(document.findall("diagram"))
        results.append(result)
    return {"status": "PASSED" if all(item["status"] == "PASSED" for item in results) else "FAILED",
            "source_commit": commit, "files": results}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", default=".")
    parser.add_argument("--revision", required=True)
    parser.add_argument("--xml", action="store_true", help="Also check that current files parse as XML")
    parser.add_argument("paths", nargs="+")
    arguments = parser.parse_args()
    try:
        result = verify(arguments.repository, arguments.revision, arguments.paths, arguments.xml)
    except (OSError, ValueError, subprocess.SubprocessError, ET.ParseError) as error:
        result = {"status": "FAILED", "error_type": type(error).__name__,
                  "reason": "Check the revision, selected file paths, repository access, and XML format."}
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "PASSED" else 1


if __name__ == "__main__":
    sys.exit(main())
