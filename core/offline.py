"""Prepare and validate dependency bundles for matching, disconnected computers."""

from __future__ import annotations

import argparse
import base64
from dataclasses import dataclass
from email.parser import BytesParser
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import platform
import re
import shutil
import struct
import sys
import sysconfig
import tempfile
from urllib.parse import urlsplit
import zipfile

try:
    from .bootstrap import SetupError, command, npm_command, source_root
except ImportError:  # The source checkout also supports direct script execution.
    _launcher = sys.modules.get("__main__")
    if (getattr(_launcher, "__file__", None)
            and Path(_launcher.__file__).resolve() == Path(__file__).with_name("bootstrap.py").resolve()):
        # Preserve the exception class when the setup launcher itself is __main__.
        SetupError = _launcher.SetupError
        command = _launcher.command
        npm_command = _launcher.npm_command
        source_root = _launcher.source_root
    else:
        from bootstrap import SetupError, command, npm_command, source_root


SCHEMA_VERSION = 1
_SKIP = {"node_modules", "__pycache__", ".git", ".venv", "build", "dist", "coverage", "reports", ".pytest_cache"}
_ROOT_INPUTS = ("pyproject.toml", "setup.py", "MANIFEST.in", "scaffold.json", "package.json", "package-lock.json",
                "setup.cmd", "setup.command", ".env.example")


@dataclass(frozen=True)
class OfflineBundle:
    wheelhouse: Path
    workbench_wheel: Path
    npm_cache: Path | None


def target() -> dict:
    """Identify the interpreter and platform that resolve the binary wheels."""
    cpu = platform.machine().lower()
    cpu = {"amd64": "x64", "x86_64": "x64", "aarch64": "arm64", "i386": "x86", "i686": "x86"}.get(cpu, cpu)
    return {"system": platform.system(), "cpu": cpu, "bits": struct.calcsize("P") * 8,
            "implementation": sys.implementation.name, "python": list(sys.version_info[:2]),
            "abi": sysconfig.get_config_var("SOABI") or "", "platform": sysconfig.get_platform()}


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _files(path: Path):
    """Read regular source files without following links or local package trees."""
    if path.is_symlink():
        raise SetupError("Bundle inputs must not use symbolic links.")
    if path.is_file():
        yield path
    elif path.is_dir():
        for child in sorted(path.iterdir()):
            if child.name in _SKIP or child.name.endswith((".egg-info", ".pyc")) or child.name == ".DS_Store":
                continue
            if child.name == ".env" or child.name.startswith(".env."):
                continue
            yield from _files(child)
    else:
        raise SetupError("Required bundle source inputs are missing.")


def source_fingerprint(root: Path) -> str:
    """Cover runtime, connector source, and every declared wheel scaffold input."""
    try:
        manifest = json.loads((root / "scaffold.json").read_text(encoding="utf-8"))
        paths = manifest["paths"]
        if not isinstance(paths, list) or not all(isinstance(item, str) for item in paths):
            raise ValueError
        inputs = {*_ROOT_INPUTS, "core", *paths}
        records = {}
        for relative in sorted(inputs):
            portable = PurePosixPath(relative)
            if portable.is_absolute() or ".." in portable.parts or "\\" in relative or ":" in relative:
                raise ValueError
            for path in _files(root / relative):
                records[path.relative_to(root).as_posix()] = _sha256(path)
        return hashlib.sha256(json.dumps(records, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
    except (OSError, ValueError, KeyError, TypeError):
        raise SetupError("Bundle source inputs could not be checked. Use the complete matching source checkout.") from None


def _lock_tarballs(root: Path) -> dict[str, str]:
    """Reject remote references that can expose credentials or bypass the cache."""
    try:
        lock = json.loads((root / "package-lock.json").read_text(encoding="utf-8"))
        if lock.get("lockfileVersion") != 3 or not isinstance(lock["packages"], dict):
            raise ValueError
        result = {}
        for name, record in lock["packages"].items():
            if not isinstance(record, dict):
                raise ValueError
            if record.get("link"):
                relative = record.get("resolved")
                if not isinstance(relative, str):
                    raise ValueError
                location = PurePosixPath(relative)
                if (location.parts[:3] != ("core", "connectors", "packages") or len(location.parts) != 4
                        or ".." in location.parts or "\\" in relative or ":" in relative
                        or not (root / relative / "package.json").is_file()):
                    raise ValueError
                continue
            if not name.startswith("node_modules/") and "/node_modules/" not in name:
                continue
            url, integrity = record.get("resolved"), record.get("integrity")
            if not isinstance(url, str) or not isinstance(integrity, str):
                raise ValueError
            parsed = urlsplit(url)
            if (parsed.scheme != "https" or not parsed.hostname or parsed.username is not None
                    or parsed.password is not None or parsed.query or parsed.fragment):
                raise ValueError
            _integrity(integrity)
            if url in result and result[url] != integrity:
                raise ValueError
            result[url] = integrity
        if not result:
            raise ValueError
        return result
    except (OSError, ValueError, KeyError, TypeError):
        raise SetupError("The npm lockfile needs HTTPS tarballs, integrity hashes, and credential-free URLs.") from None


def _integrity(value: str) -> tuple[str, bytes]:
    options = {}
    for item in value.split():
        algorithm, encoded = item.split("-", 1)
        if algorithm not in {"sha512", "sha384", "sha256", "sha1"}:
            raise ValueError
        digest = base64.b64decode(encoded, validate=True)
        if len(digest) != hashlib.new(algorithm).digest_size:
            raise ValueError
        options[algorithm] = digest
    for algorithm in ("sha512", "sha384", "sha256", "sha1"):
        if algorithm in options:
            return algorithm, options[algorithm]
    raise ValueError


def _cache_complete(root: Path, cache: Path) -> None:
    for integrity in _lock_tarballs(root).values():
        algorithm, expected = _integrity(integrity)
        key = expected.hex()
        content = cache / "_cacache/content-v2" / algorithm / key[:2] / key[2:4] / key[4:]
        try:
            digest = hashlib.new(algorithm)
            with content.open("rb") as stream:
                for block in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(block)
            if digest.digest() != expected:
                raise ValueError
        except (OSError, ValueError):
            raise SetupError("The offline npm cache is incomplete or corrupt. Prepare a new bundle.") from None


def _wheel_name(path: Path) -> str:
    try:
        with zipfile.ZipFile(path) as archive:
            records = [item for item in archive.infolist() if item.filename.endswith(".dist-info/METADATA")]
            if len(records) != 1 or records[0].file_size > 4 * 1024 * 1024:
                raise ValueError
            metadata = BytesParser().parsebytes(archive.read(records[0]))
        name = metadata.get("Name", "")
        if not name or any(re.search(r"@|(?:https?|git|file|ftp):", item, re.I)
                           for item in metadata.get_all("Requires-Dist", [])):
            raise ValueError
        return re.sub(r"[-_.]+", "-", name).lower()
    except (OSError, ValueError, TypeError, zipfile.BadZipFile, RuntimeError):
        raise SetupError("Bundle wheels need valid metadata without direct URL dependencies.") from None


def _bundle_files(bundle: Path) -> dict[str, dict]:
    records = {}
    for directory, folders, files in os.walk(bundle, followlinks=False):
        for name in [*folders, *files]:
            path = Path(directory) / name
            if path.is_symlink():
                raise SetupError("Offline bundles must not contain symbolic links.")
        for name in files:
            path = Path(directory) / name
            relative = path.relative_to(bundle).as_posix()
            if relative == "manifest.json":
                continue
            if not ((relative.startswith("wheelhouse/") and len(PurePosixPath(relative).parts) == 2
                     and relative.endswith(".whl")) or relative.startswith("npm-cache/_cacache/content-v2/")):
                raise SetupError("The offline bundle contains unexpected files. Prepare a new bundle.")
            if not path.is_file():
                raise SetupError("Offline bundles must contain regular files.")
            records[relative] = {"sha256": _sha256(path), "size": path.stat().st_size}
    return records


def validate_bundle(root: Path, bundle: Path, *, core_only: bool = False) -> OfflineBundle:
    """Check the complete bundle before setup creates or changes any environment."""
    try:
        if bundle.is_symlink() or not bundle.is_dir():
            raise SetupError("Select an existing offline bundle directory without symbolic links.")
        bundle = bundle.resolve()
        manifest_path = bundle / "manifest.json"
        if manifest_path.is_symlink() or manifest_path.stat().st_size > 8 * 1024 * 1024:
            raise ValueError
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest["schema_version"] != SCHEMA_VERSION:
            raise ValueError
        if manifest["target"] != target():
            raise SetupError("The offline bundle needs the same operating system, CPU, Python minor version, and interpreter ABI.")
        if manifest["profile"] != ("core" if core_only else "all"):
            raise SetupError("The offline bundle profile does not match setup. Select the matching profile or prepare another bundle.")
        if manifest["source_fingerprint"] != source_fingerprint(root):
            raise SetupError("The offline bundle does not match this source checkout. Transfer matching source or prepare another bundle.")
        records = _bundle_files(bundle)
        if not isinstance(manifest["files"], dict) or records != manifest["files"]:
            raise SetupError("Offline bundle files are missing or changed. Transfer the complete unchanged bundle.")
        wheels = [bundle / name for name in records if name.startswith("wheelhouse/")]
        workbench = [wheel for wheel in wheels if _wheel_name(wheel) == "ai-sdlc-workbench"]
        if len(workbench) != 1 or manifest["workbench_wheel"] != workbench[0].relative_to(bundle).as_posix():
            raise ValueError
        cache = None if core_only else bundle / "npm-cache"
        if cache is not None:
            _cache_complete(root, cache)
        elif any(name.startswith("npm-cache/") for name in records):
            raise ValueError
        return OfflineBundle(bundle / "wheelhouse", workbench[0], cache)
    except SetupError:
        raise
    except (OSError, ValueError, KeyError, TypeError):
        raise SetupError("The offline bundle manifest is invalid or incomplete. Prepare a new bundle.") from None


def prepare(root: Path, output: Path, *, core_only: bool = False) -> Path:
    """Use approved connected package indexes; never copy an installed environment."""
    root = root.resolve()
    if output.is_symlink() or output.exists():
        raise SetupError("Select a new bundle directory. Existing bundle files are preserved.")
    output = output.absolute()
    try:
        relative = output.resolve().relative_to(root)
        if not relative.parts or relative.parts[0] in {"core", ".agents", "adapters", "docs", "registry", "knowledge", "relationships"}:
            raise SetupError("Create the offline bundle outside the shipped source and scaffold directories.")
    except ValueError:
        pass
    fingerprint = source_fingerprint(root)
    npm = None if core_only else npm_command(root)
    tarballs = {} if core_only else _lock_tarballs(root)
    try:
        output.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="workbench-bundle-", dir=output.parent) as temporary:
            staging = Path(temporary) / "bundle"
            wheelhouse = staging / "wheelhouse"
            wheelhouse.mkdir(parents=True)
            print("Build the Workbench wheel for the matching source checkout.", flush=True)
            if command([sys.executable, "-m", "pip", "wheel", str(root), "--no-deps", "--wheel-dir", str(wheelhouse)], root).returncode:
                raise SetupError("Workbench wheel creation failed. Check approved build package access.")
            wheels = list(wheelhouse.glob("*.whl"))
            if len(wheels) != 1 or _wheel_name(wheels[0]) != "ai-sdlc-workbench":
                raise SetupError("Workbench wheel creation did not produce one supported wheel.")
            wheel = wheels[0]
            packages = [str(wheel) + ("" if core_only else "[release-clinic]")]
            if not core_only and platform.system() == "Windows":
                packages.append("pywin32>=305")
            print("Download binary Python dependencies for this computer's platform and interpreter.", flush=True)
            if command([sys.executable, "-m", "pip", "download", "--only-binary=:all:", "--dest", str(wheelhouse), *packages], root).returncode:
                raise SetupError("Binary dependency download failed. Use approved wheels for this exact platform and Python version.")
            # Reject URL requirements before the isolated, local-only resolution pass.
            for relative in _bundle_files(staging):
                _wheel_name(staging / relative)
            verification = Path(temporary) / "verified-wheels"
            verification.mkdir()
            print("Check the complete Python dependency set without package registry access.", flush=True)
            if command([sys.executable, "-m", "pip", "download", "--no-index", "--find-links", str(wheelhouse),
                        "--only-binary=:all:", "--no-cache-dir", "--dest", str(verification), *packages],
                       root, offline=True).returncode:
                raise SetupError("Offline dependency resolution failed. Required binary wheels are missing or incompatible with this interpreter.")
            if npm:
                print("Cache every locked npm tarball, including other platforms' optional packages.", flush=True)
                cache = Path(temporary) / "npm-download"
                for count, url in enumerate(sorted(tarballs), 1):
                    if count == 1 or count % 25 == 0 or count == len(tarballs):
                        print(f"Cache npm tarball {count}/{len(tarballs)}.", flush=True)
                    if command([*npm, "cache", "add", url, "--cache", str(cache), "--ignore-scripts", "--no-audit", "--no-fund"], root).returncode:
                        raise SetupError("A locked npm tarball could not be cached. Check approved registry access.")
                _cache_complete(root, cache)
                destination = staging / "npm-cache/_cacache/content-v2"
                destination.parent.mkdir(parents=True)
                # Lockfile integrity resolves content directly; request metadata is unnecessary.
                shutil.copytree(cache / "_cacache/content-v2", destination, symlinks=True)
            if source_fingerprint(root) != fingerprint:
                raise SetupError("Source inputs changed during preparation. Prepare another bundle after source changes stop.")
            manifest = {"schema_version": SCHEMA_VERSION, "profile": "core" if core_only else "all", "target": target(),
                        "source_fingerprint": fingerprint, "workbench_wheel": wheel.relative_to(staging).as_posix(),
                        "files": _bundle_files(staging), "integrity_limit": "Hashes detect changes; they do not authenticate a publisher."}
            (staging / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            validate_bundle(root, staging, core_only=core_only)
            if output.exists() or output.is_symlink():
                raise SetupError("The selected output appeared during preparation. Existing files are preserved.")
            staging.rename(output)
        return output.resolve()
    except SetupError:
        raise
    except (OSError, ValueError):
        raise SetupError("Bundle preparation could not finish. Check local paths, permissions, and approved package access.") from None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="operation", required=True)
    commands.add_parser("target", help="Print this Python interpreter's offline bundle target without changing files")
    build = commands.add_parser("prepare", help="Download a bundle on a connected computer matching the target")
    build.add_argument("--output", required=True, type=Path)
    build.add_argument("--core-only", action="store_true")
    options = parser.parse_args(argv)
    if options.operation == "target":
        print(json.dumps(target(), indent=2, sort_keys=True))
        return 0
    try:
        if sys.version_info < (3, 10):
            raise SetupError("Bundle preparation requires Python 3.10 or newer.")
        result = prepare(source_root(), options.output.expanduser(), core_only=options.core_only)
        print("Offline bundle: " + str(result))
        print("Transfer the matching source checkout and complete bundle. Read docs/SETUP.md.")
        return 0
    except SetupError as error:
        print("Bundle preparation incomplete. " + str(error), file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("Bundle preparation interrupted. Existing bundles are preserved.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
