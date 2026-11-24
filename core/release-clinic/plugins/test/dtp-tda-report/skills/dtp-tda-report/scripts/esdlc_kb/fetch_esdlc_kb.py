#!/usr/bin/env python3
"""
esdlc_kb/fetch_esdlc_kb.py — standalone eSDLC Control Knowledge Base builder/refresher
=======================================================================================

Fetches the bank's Enterprise SDLC (eSDLC) policy content from the ADO wiki
(sc-ado/ESDM/ESDM.wiki) and maintains a local, re-runnable "supplementary
knowledge base" that sits alongside the dtp-tda-report skill.

WHY A STANDALONE SCRIPT (not a one-time copy-paste):
  - The eSDLC wiki is a large, actively-maintained tree (1000+ pages across
    Controls/Guidance/Disciplines/Work-Products/Tools/Appendix). A one-time
    copy would be instantly stale and has no way to tell you WHEN/WHAT changed.
  - Re-running this script periodically (e.g. monthly, or ahead of a TDA
    skill review) lets you compare the live wiki's per-page git commit id
    against the last-known commit id recorded in esdlc_kb_manifest.json —
    the exact same "version drift" pattern dtp-tda-report already uses for
    collector_version vs skill_version.
  - This script NEVER auto-edits the curated ESDLC_CONTROL_REGISTRY.md (the
    "is this control automated by dtp-tda-report?" mapping table) — it only
    refreshes the raw page cache + manifest and flags which pages changed,
    leaving the actual judgement call (does the implemented rule still match
    the control's current wording?) to a human/agent review step.

SCOPE (deliberately NOT a full recursive crawl):
  Only the 14 real "E-SDLC Controls" pages + the Release Compliance
  Pre-Flight Checklist page(s) + the 2 controls-overview landing pages are
  fetched (see IN_SCOPE_PATHS below) — these are the only pages that define
  actual mandatory controls. The much larger Guidance/Disciplines/
  Work-Products/Tools/Appendix sub-trees (850+ pages) are supporting
  reference material the control pages themselves link out to; they are
  out of scope for drift-tracking purposes. Extend IN_SCOPE_PATHS if a new
  control page is added under e-sdlc-controls/ in future.

USAGE:
    python fetch_esdlc_kb.py

Dependencies: Python 3.9+, requests, the existing tda/config.py .env loader
(reused for ADO_TOKEN/ADO_ORGANIZATION/HTTPS_PROXY — no new .env keys needed).

Outputs (all under this script's own directory, scripts/esdlc_kb/):
    raw/<flattened-page-name>.md   — cached raw content of every in-scope page
    esdlc_kb_manifest.json         — path -> {commit_id, commit_date, author, last_fetched}
    ESDLC_CONTROL_REGISTRY.md      — curated control-to-SKILL.md mapping table
                                      (scaffolded on first run only, never
                                      overwritten automatically afterwards)
    esdlc_kb_changes_<date>.md     — written only when a re-run detects that
                                      one or more in-scope pages have a new
                                      commit since the last fetch
"""

from __future__ import annotations

import base64
import json
import os
import pathlib
import sys
from datetime import datetime, timezone

import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Reuse the existing, proven .env loader (ADO_TOKEN / ADO_ORGANIZATION /
# HTTPS_PROXY). It loads .env from the selected Workbench root.
_SCRIPTS_DIR = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_SCRIPTS_DIR))
from tda.config import load_env_file  # noqa: E402

KB_DIR = pathlib.Path(__file__).resolve().parent
RAW_DIR = KB_DIR / "raw"
MANIFEST_PATH = KB_DIR / "esdlc_kb_manifest.json"
REGISTRY_PATH = KB_DIR / "ESDLC_CONTROL_REGISTRY.md"

# The eSDLC wiki lives in a DIFFERENT ADO project (ESDM) to the one
# dtp-tda-report normally talks to (FMQPR) — same org, same ADO_TOKEN (a PAT
# is org-scoped), different project/repo, so this is hardcoded rather than
# read from ADO_PROJECT in .env (which is "FMQPR" and must stay untouched).
ADO_PROJECT = "ESDM"
WIKI_REPO = "ESDM.wiki"

# See the module docstring's "SCOPE" section for why this list is curated,
# not a full recursive crawl.
IN_SCOPE_PATHS = [
    "/Enterprise-sdlc/e-sdlc-controls.md",
    "/Enterprise-sdlc/esdlc-control-checks-in-ado-pipelines.md",
    "/Enterprise-sdlc/checklist.md",
    "/Enterprise-sdlc/checklist/compliance-checks-preflight-checklist.md",
    "/Enterprise-sdlc/checklist/test-case-review-checkist.md",
    "/Enterprise-sdlc/checklist/test-case-review-checklist.md",
    "/Enterprise-sdlc/e-sdlc-controls/approved-requirements-(functional-and-non_functional).md",
    "/Enterprise-sdlc/e-sdlc-controls/architecture-and-design-sign-off.md",
    "/Enterprise-sdlc/e-sdlc-controls/software-configuration-management.md",
    "/Enterprise-sdlc/e-sdlc-controls/test-environment-management.md",
    "/Enterprise-sdlc/e-sdlc-controls/code-review.md",
    "/Enterprise-sdlc/e-sdlc-controls/unit-testing.md",
    "/Enterprise-sdlc/e-sdlc-controls/test-strategy.md",
    "/Enterprise-sdlc/e-sdlc-controls/secure-by-design.md",
    "/Enterprise-sdlc/e-sdlc-controls/functional-testing.md",
    "/Enterprise-sdlc/e-sdlc-controls/non-functional-testing.md",
    "/Enterprise-sdlc/e-sdlc-controls/pre-deployment-verification.md",
    "/Enterprise-sdlc/e-sdlc-controls/post-deployment-verification.md",
    "/Enterprise-sdlc/e-sdlc-controls/e-sdlc-integrated-training.md",
    "/Enterprise-sdlc/e-sdlc-controls/data.md",
]


def _repo_base(organization: str) -> str:
    return f"https://dev.azure.com/{organization}/{ADO_PROJECT}/_apis/git/repositories/{WIKI_REPO}"


def _build_session(token: str, proxy: str) -> requests.Session:
    session = requests.Session()
    session.headers.update({
        "Authorization": "Basic " + base64.b64encode((":" + token).encode()).decode(),
    })
    if proxy:
        proxy_url = proxy if proxy.startswith(("http://", "https://")) else f"http://{proxy}"
        session.proxies.update({"http": proxy_url, "https": proxy_url})
    return session


def fetch_page_content(session: requests.Session, organization: str, path: str) -> str:
    resp = session.get(
        f"{_repo_base(organization)}/items",
        params={"path": path, "api-version": "7.1"},
        headers={"Accept": "text/plain"},
        verify=False,
        timeout=30,
    )
    resp.raise_for_status()
    return resp.text


def fetch_latest_commit(session: requests.Session, organization: str, path: str) -> dict:
    resp = session.get(
        f"{_repo_base(organization)}/commits",
        params={
            "searchCriteria.itemPath": path,
            "searchCriteria.$top": 1,
            "api-version": "7.1",
        },
        verify=False,
        timeout=30,
    )
    resp.raise_for_status()
    values = (resp.json() or {}).get("value") or []
    if not values:
        return {"commitId": None, "author": None, "date": None}
    c = values[0]
    return {
        "commitId": c.get("commitId"),
        "author": (c.get("author") or {}).get("name"),
        "date": (c.get("author") or {}).get("date"),
    }


def _safe_filename(path: str) -> str:
    trimmed = path.lstrip("/")
    if trimmed.startswith("Enterprise-sdlc/"):
        trimmed = trimmed[len("Enterprise-sdlc/"):]
    return trimmed.replace("/", "__")


def load_manifest() -> dict:
    if MANIFEST_PATH.exists():
        return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    return {}


def save_manifest(manifest: dict) -> None:
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")


def scaffold_registry() -> str:
    """First-run-only seed of the curated control registry. Content below was
    hand-transcribed from the real e-sdlc-controls.md table (fetched
    2026-10-13) plus a first-pass "is this automated by dtp-tda-report?"
    assessment — review every row before relying on it; this is a starting
    point for human/agent judgement, not an authoritative final mapping.
    """
    return """# eSDLC Control Registry — dtp-tda-report Coverage Mapping

> Curated by hand. This file is **never overwritten automatically** by
> `fetch_esdlc_kb.py` re-runs — only the `raw/` cache and
> `esdlc_kb_manifest.json` are refreshed. When a re-run reports a changed
> page (see `esdlc_kb_changes_<date>.md`), review the affected control
> row(s) below and update this table manually.
>
> Source: https://dev.azure.com/sc-ado/ESDM/_wiki/wikis/ESDM.wiki/29/Enterprise-sdlc
> Scaffolded: 2026-10-13 from the live `e-sdlc-controls.md` page.

| Control Name | Trigger | ADO Implementation | Automated in dtp-tda-report? | Mapped SKILL.md Section | Notes |
|---|---|---|---|---|---|
| Approved Requirements (Functional & Non-Functional) | Release | Automated | ⚠️ Needs Review | — | Story Description/AC quality + PO Reprioritization checks are related but don't fully cover "requirements approved" |
| Architecture and Design Sign-off | Application | Partially Automated | ⚠️ Partial | Application Approvals (Architecture doc) | Covers architecture doc approval/expiry; does not assess design-review *quality* |
| Software Configuration Management | Platform | Automated | ❌ Not covered | — | SCM/branching/repo standards are enforced by the pipeline itself, not by this report |
| Test Environment Management | Platform | Automated | ❌ Not covered | — | Test Environment doc approval/expiry IS covered (see App Approvals); environment *provisioning/config* is not |
| Code Review | Release | Automated | ❌ Not covered | — | Enforced by branch policy/PR process upstream, not assessed by this report |
| Unit Testing | Release | Automated | ✅ Yes | Unit Tests section | Pipeline unit-test pass/fail counts, per SKILL.md |
| Test Strategy | Application | Partially Automated | ⚠️ Partial | Application Approvals (Test Strategy doc) | Doc approval/expiry covered; strategy *content* quality is not assessed |
| Secure by Design | Release | Partially Automated | ❌ Not covered | — | SIA/security sign-off not currently in scope of this report |
| Functional Testing | Release | Automated | ✅ Yes | Manual Test Execution, Story Traceability | Evidence/pass-status gate + traceability checks map closely to this control |
| Non-Functional Testing | Application | Partially Automated | ✅ Yes | PT Governance (PT Plan/Report/PTIA) | Performance testing evidence/approval checks map here |
| Pre-Deployment verification | Release | Automated | ⚠️ Partial | Release Gate Checks, PIT | Some overlap (release-readiness checks); not a 1:1 mapping |
| Post Deployment Verification | Release | Automated | ✅ Yes | PIT Governance | PIT documentation/approval gate maps directly |
| E-SDLC Integrated Training | Squad | Automated | ❌ Not covered | — | Training compliance is outside this report's data sources |
| Data | Release | Partially Automated | ❌ Not covered | — | Not currently assessed |

## Gaps Worth Investigating

Rows marked **❌ Not covered** or **⚠️ Partial/Needs Review** above are candidates for either (a) a new
SKILL.md rule, if ADO/Confluence/Sonar/Genie data already exists to check it automatically, or
(b) an explicit documented exclusion (the control is enforced elsewhere in the pipeline, not
duplicated here) — the Pre-Flight Checklist registry below helps distinguish these two cases,
since several of the "Not covered" controls above (Code Review/SAST, Secrets scanning,
Branch naming) are explicitly enforced as pipeline Hard Stops documented there, not gaps at all.

## Release Compliance Pre-Flight Checklist Cross-Reference

The `/Enterprise-sdlc/checklist/compliance-checks-preflight-checklist.md` page documents the
pipeline's own automated gates (CI Build -> PRE_TEST -> PRE_RELEASE -> Release Approval ->
PRE_PRODUCTION). Several of its Hard Stop items are enforced by the ADO pipeline itself
(secrets scanning, commit-to-work-item linkage, branch naming, SAST, Nexus IQ, Aqua DTA) —
these deliberately do NOT need a dtp-tda-report rule, since they already block the release
pipeline before a release WI is even relevant to this skill. Re-check this cross-reference
whenever the checklist page changes (see `esdlc_kb_changes_*.md`).
"""


def main() -> None:
    load_env_file()
    organization = os.environ.get("ADO_ORGANIZATION", "sc-ado")
    token = os.environ.get("ADO_TOKEN")
    proxy = os.environ.get("HTTPS_PROXY", "")
    if not token:
        print("[esdlc-kb] ERROR: ADO_TOKEN not found in environment/.env — cannot authenticate.", file=sys.stderr)
        sys.exit(1)

    session = _build_session(token, proxy)

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    manifest = load_manifest()
    new_manifest: dict = {}
    changed_pages: list[tuple[str, dict, dict]] = []
    failed_pages: list[tuple[str, str]] = []

    print(f"[esdlc-kb] Fetching {len(IN_SCOPE_PATHS)} in-scope wiki page(s) from "
          f"{organization}/{ADO_PROJECT}/{WIKI_REPO}...")
    for path in IN_SCOPE_PATHS:
        try:
            commit_info = fetch_latest_commit(session, organization, path)
            content = fetch_page_content(session, organization, path)
        except requests.exceptions.RequestException as e:
            print(f"  [FAIL] {path}: {e}")
            failed_pages.append((path, str(e)))
            continue

        fname = _safe_filename(path)
        (RAW_DIR / fname).write_text(content, encoding="utf-8")

        old_entry = manifest.get(path)
        commit_id = commit_info.get("commitId")
        new_entry = {
            "commit_id": commit_id,
            "commit_date": commit_info.get("date"),
            "commit_author": commit_info.get("author"),
            "last_fetched": datetime.now(timezone.utc).isoformat(),
            "cached_file": fname,
        }
        new_manifest[path] = new_entry

        short_id = (commit_id or "?")[:8]
        if old_entry and old_entry.get("commit_id") != commit_id:
            changed_pages.append((path, old_entry, new_entry))
            old_short = (old_entry.get("commit_id") or "?")[:8]
            print(f"  [CHANGED] {path}  (was {old_short}, now {short_id})")
        elif old_entry is None:
            print(f"  [NEW]     {path}  ({short_id})")
        else:
            print(f"  [OK]      {path}  (unchanged, {short_id})")

    save_manifest(new_manifest)

    if failed_pages:
        print(f"\n[esdlc-kb] WARNING: {len(failed_pages)} page(s) failed to fetch:")
        for p, err in failed_pages:
            print(f"   - {p}: {err}")

    if not REGISTRY_PATH.exists():
        REGISTRY_PATH.write_text(scaffold_registry(), encoding="utf-8")
        print(f"\n[esdlc-kb] Created initial control registry: {REGISTRY_PATH}")
        print("[esdlc-kb] Review every row's 'Automated in dtp-tda-report?' column before "
              "relying on it for gap analysis.")
    elif changed_pages:
        alert_path = KB_DIR / f"esdlc_kb_changes_{datetime.now().strftime('%Y-%m-%d')}.md"
        lines = [
            "# eSDLC Wiki Change Alert",
            "",
            f"Detected {len(changed_pages)} page(s) with a new commit since the last fetch.",
            "ESDLC_CONTROL_REGISTRY.md was NOT modified automatically — review the changed",
            "pages below and update the registry manually if a control's requirements changed.",
            "",
        ]
        for path, old, new in changed_pages:
            lines.append(f"## {path}")
            lines.append(f"- Previous commit: `{old.get('commit_id', '?')}` ({old.get('commit_date', 'unknown date')})")
            lines.append(f"- New commit: `{new.get('commit_id', '?')}` ({new.get('commit_date', 'unknown date')}) "
                          f"by {new.get('commit_author', 'unknown')}")
            lines.append(f"- Raw cache: `raw/{new.get('cached_file')}`")
            lines.append("")
        alert_path.write_text("\n".join(lines), encoding="utf-8")
        print(f"\n[esdlc-kb] {len(changed_pages)} page(s) changed since last fetch — see {alert_path}")
    else:
        print(f"\n[esdlc-kb] No changes detected since last fetch. Registry: {REGISTRY_PATH}")

    print(f"\n[esdlc-kb] Done. {len(new_manifest)} page(s) cached under {RAW_DIR}")


if __name__ == "__main__":
    main()
