#!/usr/bin/env python3
"""Build a compact experience index from packet manifests."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import yaml


def _strings(value):
    return value if isinstance(value, list) and all(isinstance(item, str) for item in value) else []


def build(root: Path) -> tuple[dict, list[str]]:
    errors: list[str] = []
    entries = []
    packets = root / "packets"
    if packets.exists() and not packets.is_dir():
        return {}, ["packets: directory required"]
    for manifest_path in sorted(packets.glob("*/manifest.yaml")) if packets.is_dir() else []:
        try:
            manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, yaml.YAMLError) as error:
            errors.append(f"{manifest_path}: invalid YAML ({error.__class__.__name__})")
            continue
        if not isinstance(manifest, dict):
            errors.append(f"{manifest_path}: mapping required")
            continue
        identifier = manifest.get("id")
        packet = manifest_path.parent
        if not isinstance(identifier, str) or not identifier:
            errors.append(f"{manifest_path}: id required")
            continue
        if any(entry["id"] == identifier for entry in entries):
            errors.append(f"{manifest_path}: duplicate id {identifier}")
            continue
        requires = manifest.get("requires") if isinstance(manifest.get("requires"), dict) else {}
        entries.append({
            "id": identifier,
            "title": manifest.get("title", identifier),
            "domain": manifest.get("domain", "unknown"),
            "status": manifest.get("status", "observed"),
            "applies_when": _strings(manifest.get("applies_when")),
            "tools": _strings(requires.get("tools")),
            "variables": _strings(requires.get("variables")),
            "packet": packet.relative_to(root).as_posix(),
        })
    entries.sort(key=lambda item: (item["domain"], item["id"]))
    return {"schema_version": 1, "experiences": entries}, errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default="assets/experience", help="Experience root")
    parser.add_argument("--output", help="Index path, defaulting to <root>/index.yaml")
    parser.add_argument("--check", action="store_true", help="Check the existing index without writing")
    arguments = parser.parse_args(argv)
    root = Path(arguments.root).expanduser().resolve()
    output = Path(arguments.output).expanduser().resolve() if arguments.output else root / "index.yaml"
    payload, errors = build(root)
    if errors:
        print(json.dumps({"status": "FAILED", "errors": errors}, indent=2))
        return 1
    encoded = yaml.safe_dump(payload, sort_keys=False, allow_unicode=True)
    if arguments.check:
        try:
            current = output.read_text(encoding="utf-8")
        except OSError:
            print(json.dumps({"status": "FAILED", "errors": ["index: file unavailable"]}, indent=2))
            return 1
        if current != encoded:
            print(json.dumps({"status": "FAILED", "errors": ["index: content is stale"]}, indent=2))
            return 1
    else:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(encoded, encoding="utf-8")
    print(json.dumps({"status": "PASSED", "index": str(output), "experiences": len(payload["experiences"])}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
