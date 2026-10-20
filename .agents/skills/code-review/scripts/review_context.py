#!/usr/bin/env python3
"""Collect read-only, content-bound Git review metadata using the standard library."""

from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import os
from pathlib import Path
import shlex
import stat
import subprocess
import sys
from dataclasses import dataclass

MAX_FILE_BYTES = 1024 * 1024


class ContextError(ValueError):
    """A review scope cannot be collected safely. Messages contain no Git output."""


@dataclass
class Entry:
    mode: str
    oid: str
    sha256: str | None = None
    data: bytes | None = None
    size: int = 0
    special: str | None = None


class Git:
    def __init__(self, repo, command):
        try:
            self.command = shlex.split(command or "git")
        except (ValueError, TypeError) as error:
            raise ContextError("Invalid Git command wrapper.") from error
        if not self.command:
            raise ContextError("The Git command wrapper is empty.")
        self.cwd = str(Path(repo).resolve())
        self.env = dict(os.environ, GIT_OPTIONAL_LOCKS="0", GIT_PAGER="cat", LC_ALL="C")
        self.env.pop("GIT_EXTERNAL_DIFF", None)
        # A caller's Git environment must not redirect the requested repository.
        for name in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_COMMON_DIR"):
            self.env.pop(name, None)
        self.prefix = self.command + ["--no-pager", "-c", "core.fsmonitor=false"]
        root = self.run("rev-parse", "--show-toplevel")
        self.cwd = os.fsdecode(root[:-1] if root.endswith(b"\n") else root)
        self.root = Path(self.cwd)
        self.algorithm = self.run("rev-parse", "--show-object-format").strip().decode("ascii")

    def process(self, args, *, stream=False):
        try:
            if stream:
                return subprocess.Popen(self.prefix + list(args), cwd=self.cwd, env=self.env,
                                        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
            return subprocess.run(self.prefix + list(args), cwd=self.cwd, env=self.env,
                                  stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, check=False)
        except (OSError, ValueError) as error:
            raise ContextError("Cannot execute the Git command in the requested repository.") from error

    def run(self, *args, allow_failure=False):
        result = self.process(args)
        if result.returncode and not allow_failure:
            raise ContextError("Git could not collect the requested review scope.")
        return result.stdout if not allow_failure else result

    def resolve(self, revision, *, unborn=False):
        if not isinstance(revision, str) or not revision or "\0" in revision:
            raise ContextError("A revision is missing or invalid.")
        result = self.run("rev-parse", "--verify", "--end-of-options", revision + "^{commit}",
                          allow_failure=True)
        if not result.returncode:
            return result.stdout.strip().decode("ascii")
        if unborn and revision == "HEAD":
            symbolic = self.run("symbolic-ref", "--quiet", "HEAD", allow_failure=True)
            if not symbolic.returncode:
                ref = os.fsdecode(symbolic.stdout.rstrip(b"\n"))
                missing = self.run("show-ref", "--verify", "--quiet", "--", ref, allow_failure=True)
                if missing.returncode == 1:
                    return None
        raise ContextError("Cannot resolve the requested commit revision.")

    def tree(self, revision):
        if revision is None:
            return {}
        entries = {}
        for record in self.run("ls-tree", "-r", "-z", "--full-tree", revision, "--").split(b"\0"):
            if record:
                metadata, path = record.split(b"\t", 1)
                mode, kind, oid = metadata.decode("ascii").split()
                entries[os.fsdecode(path)] = Entry(mode, oid, special="gitlink" if kind == "commit" else None)
        return entries

    def index(self):
        entries = {}
        for record in self.run("ls-files", "--stage", "-z").split(b"\0"):
            if record:
                metadata, path = record.split(b"\t", 1)
                mode, oid, stage = metadata.decode("ascii").split()
                if stage != "0":
                    raise ContextError("Unresolved index conflicts block local review scope collection.")
                entries[os.fsdecode(path)] = Entry(mode, oid, special="gitlink" if mode == "160000" else None)
        return entries

    def blob(self, entry):
        if entry.sha256 is not None or entry.special == "gitlink":
            return
        size = int(self.run("cat-file", "-s", entry.oid).strip())
        process = self.process(("cat-file", "blob", entry.oid), stream=True)
        digest = hashlib.sha256()
        chunks = []
        received = 0
        try:
            while True:
                chunk = process.stdout.read(65536)
                if not chunk:
                    break
                received += len(chunk)
                digest.update(chunk)
                if size <= MAX_FILE_BYTES:
                    chunks.append(chunk)
        finally:
            process.stdout.close()
        if process.wait() or received != size:
            raise ContextError("Git could not read a compared blob.")
        entry.size = size
        entry.sha256 = digest.hexdigest()
        entry.data = b"".join(chunks) if size <= MAX_FILE_BYTES else None
        if entry.mode == "120000":
            entry.special = "symlink"

    def working_entry(self, path, index_entry):
        # Refuse parent links as well as leaf traversal. Symlink payloads use readlink.
        candidate = self.root
        for component in Path(path).parts[:-1]:
            candidate = candidate / component
            try:
                if candidate.is_symlink():
                    raise ContextError("A changed path has a symlink parent; scope collection stopped.")
            except OSError as error:
                raise ContextError("Cannot inspect a compared path.") from error
        candidate = self.root / path
        if index_entry is not None and index_entry.mode == "160000":
            return Entry("160000", index_entry.oid, special="gitlink")
        try:
            details = candidate.lstat()
        except FileNotFoundError:
            return None
        except OSError as error:
            raise ContextError("Cannot inspect a compared path.") from error
        if stat.S_ISLNK(details.st_mode):
            data = os.fsencode(os.readlink(candidate))
            mode, special = "120000", "symlink"
            chunks = [data]
            size = len(data)
            digest = hashlib.sha256(data)
            blob_digest = hashlib.new(self.algorithm, b"blob " + str(size).encode() + b"\0" + data)
        elif stat.S_ISREG(details.st_mode):
            mode, special = ("100755" if details.st_mode & 0o111 else "100644"), None
            size = details.st_size
            digest = hashlib.sha256()
            blob_digest = hashlib.new(self.algorithm, b"blob " + str(size).encode() + b"\0")
            chunks = []
            try:
                flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
                with os.fdopen(os.open(candidate, flags), "rb") as source:
                    before = os.fstat(source.fileno())
                    if (details.st_size, details.st_mtime_ns, details.st_ino) != (before.st_size, before.st_mtime_ns, before.st_ino):
                        raise ContextError("A compared file changed during collection; retry the review.")
                    while True:
                        chunk = source.read(65536)
                        if not chunk:
                            break
                        digest.update(chunk)
                        blob_digest.update(chunk)
                        if size <= MAX_FILE_BYTES:
                            chunks.append(chunk)
                    after = os.fstat(source.fileno())
                if (before.st_size, before.st_mtime_ns, before.st_ino) != (after.st_size, after.st_mtime_ns, after.st_ino):
                    raise ContextError("A compared file changed during collection; retry the review.")
            except OSError as error:
                raise ContextError("Cannot read a compared file without following links.") from error
        elif stat.S_ISDIR(details.st_mode):
            return None
        else:
            raise ContextError("A compared path is not a regular file, symlink, or gitlink.")
        return Entry(mode, blob_digest.hexdigest(), digest.hexdigest(),
                     b"".join(chunks) if size <= MAX_FILE_BYTES else None, size, special)


def _text(entry):
    if entry is None:
        return []
    if entry.special or entry.size > MAX_FILE_BYTES or entry.data is None:
        return None
    if b"\0" in entry.data:
        return None
    try:
        # Git line numbers count LF bytes, not Unicode line separators or lone CR.
        pieces = entry.data.decode("utf-8").split("\n")
        return [piece + "\n" for piece in pieces[:-1]] + ([pieces[-1]] if pieces[-1] else [])
    except UnicodeDecodeError:
        return None


def collect_changes(repo: Path | str, mode="worktree", base=None, head="HEAD", git_command=None):
    """Return metadata and added text lines. Neither result is a cached review verdict."""
    if mode not in {"worktree", "staged", "branch", "range"}:
        raise ContextError("Unsupported review mode.")
    local = mode in {"worktree", "staged"}
    if local and (base is not None or head != "HEAD"):
        raise ContextError("Local review modes compare HEAD; use branch or range for explicit revisions.")
    if not local and base is None:
        raise ContextError("Branch and range review modes require a base revision.")
    git = Git(repo, git_command)
    head_id = git.resolve(head, unborn=local)
    base_id = head_id if local else git.resolve(base)
    comparison_base = base_id
    if mode == "branch":
        comparison_base = git.run("merge-base", base_id, head_id).strip().decode("ascii")
    old = git.tree(comparison_base)
    index = git.index() if local else None
    new = index if local else git.tree(head_id)
    if mode == "staged":
        staged_paths = {os.fsdecode(path) for path in git.run(
            "diff", "--cached", "--name-only", "-z", "--no-ext-diff", "--no-textconv",
            "--ita-invisible-in-index", "--").split(b"\0") if path}
        # Intent-to-add entries belong to worktree scope until their bytes are staged.
        new = {path: entry for path, entry in index.items() if path in old or path in staged_paths}
    if mode == "worktree":
        paths = set(old) | set(index)
        paths.update(os.fsdecode(path) for path in git.run("ls-files", "--others", "--exclude-standard", "-z").split(b"\0") if path)
        new = {}
        for path in sorted(paths):
            entry = git.working_entry(path, index.get(path))
            if entry is not None:
                if path in old and (entry.mode, entry.oid) == (old[path].mode, old[path].oid):
                    entry.data = None  # Do not retain unchanged repository source in memory.
                new[path] = entry
    changed = {}
    for path in old.keys() | new.keys():
        before, after = old.get(path), new.get(path)
        if before is None or after is None or (before.mode, before.oid) != (after.mode, after.oid):
            changed[path] = (before, after)
    # Pair exact-content moves deterministically. Edited moves remain a deletion plus addition.
    deleted = {}
    for path, (before, after) in sorted(changed.items()):
        if after is None:
            deleted.setdefault(before.oid, []).append(path)
    renames = {}
    for path, (before, after) in sorted(changed.items()):
        if before is None and deleted.get(after.oid):
            old_path = deleted[after.oid].pop(0)
            renames[path] = old_path
    old_names = set(renames.values())
    files, added_lines, limitations = [], [], []
    fingerprint = hashlib.sha256()
    identity = {"mode": mode, "head": head_id, "base": base_id, "comparison_base": comparison_base}
    if index is not None:
        identity["index"] = [[path, entry.mode, entry.oid] for path, entry in sorted(index.items())]
    fingerprint.update(json.dumps(identity, sort_keys=True).encode())
    for path in sorted(changed):
        if path in old_names:
            continue
        before, after = changed[path]
        old_path = renames.get(path)
        if old_path is not None:
            before = old[old_path]
        for entry in (before, after):
            if entry is not None:
                git.blob(entry)
        status = "R" if old_path else "A" if before is None else "D" if after is None else "T" if before.mode[:3] != after.mode[:3] else "M"
        payload = {"path": path, "old_path": old_path, "status": status,
                   "before": None if before is None else [before.mode, before.oid, before.sha256],
                   "after": None if after is None else [after.mode, after.oid, after.sha256]}
        fingerprint.update(json.dumps(payload, sort_keys=True, ensure_ascii=True).encode())
        ranges = []
        before_lines, after_lines = _text(before), _text(after)
        binary = any(entry is not None and entry.special is None and entry.size <= MAX_FILE_BYTES and _text(entry) is None for entry in (before, after))
        if before_lines is None and after_lines is not None:
            # An unavailable binary/large/symlink baseline must not hide current added text.
            before_lines = []
        if before_lines is not None and after_lines is not None:
            for tag, _, _, start, end in difflib.SequenceMatcher(None, before_lines, after_lines).get_opcodes():
                if tag in {"insert", "replace"} and start < end:
                    ranges.append([start + 1, end])
                    added_lines.extend({"path": path, "line": number + 1,
                                        "text": after_lines[number].removesuffix("\n")}
                                       for number in range(start, end))
        for entry in (before, after):
            if entry is not None:
                if entry.special:
                    limitations.append(f"{path!r}: {entry.special} content is not scanned or traversed.")
                elif entry.size > MAX_FILE_BYTES:
                    limitations.append(f"{path!r}: content exceeds {MAX_FILE_BYTES} bytes; text analysis is excluded.")
        if binary:
            limitations.append(f"{path!r}: binary or non-UTF-8 content is excluded from text analysis.")
        record = {"path": path, "status": status, "content_sha256": after.sha256 if after else None,
                  "added_ranges": ranges, "binary": binary}
        if old_path is not None:
            record["old_path"] = old_path
        files.append(record)
    if any(entry.mode == "160000" for entry in new.values()):
        limitations.append("Submodule working contents are not inspected; only recorded gitlink changes are compared.")
    if any(before is None for before, after in changed.values()) and any(after is None for before, after in changed.values()):
        limitations.append("Edited renames may be represented as separate deletions and additions; exact-content moves are paired.")
    context = {"schema_version": 1, "mode": mode, "repository": str(git.root), "head": head_id,
               "base": base_id, "comparison_base": comparison_base, "fingerprint": fingerprint.hexdigest(),
               "files": files, "limitations": sorted(set(limitations)), "change_count": len(files)}
    return context, added_lines


def collect_context(repo: Path | str, mode="worktree", base=None, head="HEAD", git_command=None):
    """Return JSON-safe scope metadata without source text."""
    return collect_changes(repo, mode, base, head, git_command)[0]


def main(argv=None):
    class RedactedParser(argparse.ArgumentParser):
        def error(self, message):
            raise ContextError("Invalid review context arguments.")

    parser = RedactedParser(description=__doc__)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--mode", choices=("worktree", "staged", "branch", "range"), default="worktree")
    parser.add_argument("--base")
    parser.add_argument("--head", default="HEAD")
    parser.add_argument("--git-command", help="Argument wrapper, for example 'sc-cli git'. No shell is used.")
    try:
        args = parser.parse_args(argv)
        result = collect_context(args.repo, args.mode, args.base, args.head, args.git_command)
    except (ContextError, OSError, UnicodeError) as error:
        print(str(error) if isinstance(error, ContextError) else "Cannot collect the requested review context.", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=True, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
