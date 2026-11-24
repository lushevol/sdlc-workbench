"""Independently reconcile generated report tables with retained run evidence."""
from __future__ import annotations

import argparse
from collections import Counter
import csv
import hashlib
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit


class Tables(HTMLParser):
    def __init__(self):
        super().__init__()
        self.rows, self.links, self.ids = [], [], []
        self.row = self.cell = None

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if "id" in values:
            self.ids.append(values["id"])
        if tag == "a" and "href" in values:
            self.links.append(values["href"])
        if tag == "tr":
            self.row = []
        if tag in ("td", "th"):
            self.cell = []

    def handle_data(self, text):
        if self.cell is not None:
            self.cell.append(text)

    def handle_endtag(self, tag):
        if tag in ("td", "th") and self.row is not None and self.cell is not None:
            self.row.append("".join(self.cell).strip())
            self.cell = None
        if tag == "tr" and self.row is not None:
            self.rows.append(self.row)
            self.row = None


def digest(value):
    raw = value if isinstance(value, bytes) else json.dumps(value, sort_keys=True).encode()
    return hashlib.sha256(raw).hexdigest()


def comparison_items(value):
    if isinstance(value, dict):
        if "baseline_count" in value:
            for kind in ("matched", "missing", "additional"):
                for item in value.get(kind, []):
                    yield tuple(str(part) for part in item)
        for key, child in value.items():
            if key not in ("differences", "matched", "missing", "additional"):
                yield from comparison_items(child)
    elif isinstance(value, list):
        for child in value:
            yield from comparison_items(child)


def markdown_rows(text):
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        line = re.sub(r"\\([\\`*_\[\]{}|#!])", r"\1", line)
        line = html.unescape(line)
        yield [part.strip() for part in line.strip("|").split("|")]


def verify(run_dir, workspace):
    suite = json.loads((run_dir / "result.json").read_text())
    assert suite["mode"] == "replay"
    assert suite["status"] == "INCOMPLETE"
    expected = {
        "ems2-prod-to-ces-uat": (1051, 1049),
        "ems2-prod-to-ems2-uat": (747, 745),
    }
    checks, all_items = [], set()
    for child in suite["checks"]:
        folder = run_dir / child["id"]
        result = json.loads((folder / "result.json").read_text())
        summary = result["summary"]
        assert (summary["discovered_accounts"], summary["unassessed_accounts"]) == expected[child["id"]]
        assert summary["compared_accounts"] == 2
        assert summary["different_accounts"] == 2
        assert summary["functional_profile_coverage_percent"] is None
        assert result["binding"] == json.loads((folder / "binding.json").read_text())
        for name, recorded in result["binding"]["implementation_sha256"].items():
            assert digest((workspace / "core" / name).read_bytes()) == recorded, name
        for path, recorded in result["binding"]["replay_sha256"].items():
            assert digest(Path(path).read_bytes()) == recorded, path
        checkpoints = 0
        for line in (folder / "cases.jsonl").read_text().splitlines():
            case = json.loads(line)
            recorded = case.pop("record_sha256")
            assert digest(case) == recorded
            checkpoints += 1
        assert checkpoints == summary["discovered_accounts"]
        with (folder / "differences.csv").open(newline="") as stream:
            rows = list(csv.DictReader(stream))
        account_key = "account" if "account" in rows[0] else "account_or_entity"
        counts = Counter((r[account_key], r["comparison"], r["kind"]) for r in rows if r["scope"] == "user")
        for user in result["users"]:
            if user["status"] != "DIFFERENT":
                continue
            for comparison in ("effective", "assignments", "profile_grants"):
                for kind in ("missing", "additional"):
                    assert counts[user["user_id"], comparison, kind] == len(user[comparison][kind])
        items = set(comparison_items(result["entitlements"])) | set(comparison_items(result["users"]))
        all_items.update(items)
        checks.append({"id": child["id"], "summary": summary, "checkpoint_hashes_verified": checkpoints,
                       "unique_comparison_tuples": len(items), "report_tables": check_reports(folder, "report", items)})
    combined = check_reports(run_dir, "index", all_items)
    return {"status": "PASSED", "execution_boundary": "Supplied API responses only; no enterprise requests.",
            "checks": checks, "combined_report": combined}


def check_reports(folder, basename, items):
    md = (folder / (basename + ".md")).read_text()
    source = (folder / (basename + ".html")).read_text()
    parsed = Tables()
    parsed.feed(source)
    assert len(set(parsed.ids)) == len(parsed.ids), "Duplicate HTML IDs"
    markdown = list(markdown_rows(md))
    html_index = [set(row) for row in parsed.rows]
    md_index = [set(row) for row in markdown]
    for item in items:
        values = set(item)
        assert any(values.issubset(row) for row in html_index), (basename, "HTML missing tuple", item)
        assert any(values.issubset(row) for row in md_index), (basename, "Markdown missing tuple", item)
    for link in parsed.links:
        parts = urlsplit(link)
        assert not parts.scheme and not parts.netloc, ("Unexpected external report link", link)
        target = folder / unquote(parts.path) if parts.path else folder / (basename + ".html")
        assert target.exists(), ("Missing local report target", target)
        if parts.fragment and not parts.path:
            assert parts.fragment in parsed.ids, ("Missing HTML anchor", link)
    assert "MOCK" in source and "UNASSESSED" in source
    return {"html_rows": len(parsed.rows), "markdown_rows": len(markdown), "unique_tuples_verified": len(items),
            "local_links_verified": len(parsed.links), "markdown_sha256": digest(md.encode()),
            "html_sha256": digest(source.encode())}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", required=True, type=Path)
    parser.add_argument("--workspace", required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(verify(args.run.resolve(), args.workspace.resolve()), indent=2))
