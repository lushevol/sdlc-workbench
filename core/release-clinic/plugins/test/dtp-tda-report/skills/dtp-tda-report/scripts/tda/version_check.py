"""tda/version_check.py — Skill Version Staleness Check (added 2026-10-13).

This repo is vendored/cloned into many consumer application repos via apm
(apm_modules). Once cloned, a consumer's local copy of SKILL.md/AutoTDAScript.py
silently stops tracking the canonical source repo's ongoing updates unless
someone manually re-syncs — the existing Collector/Skill Version Drift Check
only ever compares two LOCAL files against each other, so it can never detect
"you are behind the real upstream latest."

When TDA_CHECK_SKILL_UPDATES=true, this module performs a best-effort,
non-blocking live check against the
canonical repo's stable `main` branch (not the `tdacommit` beta branch) and
prints a loud, hard-to-miss console banner if the locally-installed skill is
out of date. The result is also returned as a dict so the caller can stamp it
into the output JSON (`skill_version_check`) for the HTML report to surface.

Design constraints:
- MUST NOT raise or block the run on any failure (network, auth, parsing) —
  this is a reminder, not a gate.
- Compares `metadata.version` (the field the user asked us to use as the
  reference), not git tags/commits.
"""

from __future__ import annotations

import os
import re
import sys
from datetime import datetime, timezone

# Grace period communicated to the user in the staleness warning/prompt below —
# purely informational text, not an enforced/tracked deadline anywhere in code.
SYNC_GRACE_PERIOD_DAYS = 5

# Canonical source-of-truth repo for this skill. Overridable via env vars in
# case this module is ever vendored somewhere the defaults don't apply.
CANONICAL_ORG     = os.environ.get('CANONICAL_SKILL_ADO_ORG', 'sc-ado')
CANONICAL_PROJECT = os.environ.get('CANONICAL_SKILL_ADO_PROJECT', 'FMQPR')
CANONICAL_REPO    = os.environ.get('CANONICAL_SKILL_REPO', '50665-fm-dtp-qa-utilities')
CANONICAL_PATH    = os.environ.get(
    'CANONICAL_SKILL_PATH',
    'plugins/test/dtp-tda-report/skills/dtp-tda-report/SKILL.md',
)
# Stable releases live on `main`; `tdacommit` carries in-progress/beta work and
# is deliberately NOT what consumer repos should be nudged toward.
CANONICAL_BRANCH  = os.environ.get('CANONICAL_SKILL_BRANCH', 'main')


def read_local_skill_version(skill_md_path: str | None = None) -> str | None:
    """Read `metadata.version` directly from the locally-installed SKILL.md on
    disk (defaults to `skills/dtp-tda-report/SKILL.md`, two directories above
    this file's own location at `skills/dtp-tda-report/scripts/tda/`). Reading
    it live (rather than hardcoding a constant here) means this check
    automatically tracks whatever version is ACTUALLY installed, with nothing
    to remember to bump. Returns None if the file is missing or unparsable.
    """
    path = skill_md_path or os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'SKILL.md')
    path = os.path.normpath(path)
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read(2000)  # frontmatter is always near the top
    except OSError:
        return None
    m = re.search(r'^\s*version:\s*"([^"]+)"', content, re.MULTILINE)
    return m.group(1) if m else None


def parse_version(v: str) -> tuple[int, ...] | None:
    """Parse a dotted version string ('1.10.1') into a comparable int tuple.
    Returns None if the string doesn't look like a dotted-numeric version.
    """
    try:
        parts = tuple(int(p) for p in v.strip().split('.'))
        return parts if parts else None
    except (ValueError, AttributeError):
        return None


def check_skill_staleness(client, local_version: str | None = None) -> dict:
    """Compare `local_version` against the canonical repo's `main`-branch
    SKILL.md `metadata.version`. When `local_version` is omitted, it is read
    live from the locally-installed SKILL.md via `read_local_skill_version()`.
    The remote check requires TDA_CHECK_SKILL_UPDATES=true. It is disabled
    by default. Disabled checks retain the result shape and set check_error.
    Never raises. Returns a dict suitable for direct inclusion in the output
    JSON under `skill_version_check`.
    """
    if local_version is None:
        local_version = read_local_skill_version()
    result = {
        'local_version':         local_version,
        'latest_stable_version': None,
        'source_repo':           CANONICAL_REPO,
        'source_branch':         CANONICAL_BRANCH,
        'is_outdated':           False,
        'checked_at':            datetime.now(timezone.utc).isoformat(),
        'check_error':           None,
    }
    if os.environ.get('TDA_CHECK_SKILL_UPDATES', '').strip().lower() != 'true':
        result['check_error'] = 'Disabled. Set TDA_CHECK_SKILL_UPDATES=true to check canonical skill updates.'
        return result
    if local_version is None:
        result['check_error'] = 'Could not read local SKILL.md to determine the installed version.'
        return result
    try:
        remote_version = client.get_remote_skill_version(
            org=CANONICAL_ORG, project=CANONICAL_PROJECT, repo=CANONICAL_REPO,
            path=CANONICAL_PATH, branch=CANONICAL_BRANCH,
        )
    except Exception as e:  # defense-in-depth — get_remote_skill_version already catches internally
        remote_version = None
        result['check_error'] = str(e)

    if remote_version is None:
        if result['check_error'] is None:
            result['check_error'] = 'Could not reach canonical repo or parse its SKILL.md version.'
        return result

    result['latest_stable_version'] = remote_version
    local_tuple  = parse_version(local_version)
    remote_tuple = parse_version(remote_version)
    if local_tuple is not None and remote_tuple is not None and local_tuple < remote_tuple:
        result['is_outdated'] = True
    return result


def print_staleness_banner(result: dict) -> None:
    """Print a loud, impossible-to-miss console banner when the local skill
    is behind the canonical repo's stable `main` branch. No-op (silent,
    single debug line only) when up to date or when the check itself failed —
    a failed check is NOT evidence of staleness and should not alarm the user.
    """
    if result.get('check_error'):
        print(f"[version-check] Skipped: {result['check_error']}", flush=True)
        return
    if not result.get('is_outdated'):
        print(f"[version-check] Skill is up to date (local v{result['local_version']}, "
              f"latest stable v{result['latest_stable_version']}).", flush=True)
        return

    local  = result['local_version']
    latest = result['latest_stable_version']
    repo   = result['source_repo']
    branch = result['source_branch']
    banner = (
        "\n"
        "########################################################################\n"
        "#  WARNING: dtp-tda-report SKILL IS OUT OF DATE                        #\n"
        "########################################################################\n"
        f"#  Local version:          {local:<44}#\n"
        f"#  Latest stable version:  {latest:<44}#\n"
        f"#  Canonical source:       {repo} ({branch} branch){' ' * max(0, 44 - len(repo) - len(branch) - 10)}#\n"
        "#                                                                      #\n"
        "#  Your findings/rules may be missing fixes, new checks, or corrected  #\n"
        "#  severities already shipped upstream. Re-sync this plugin (apm       #\n"
        "#  update / re-clone) before relying on this report for release gate  #\n"
        "#  decisions.                                                         #\n"
        "#                                                                      #\n"
        f"#  Please sync to the latest version within {SYNC_GRACE_PERIOD_DAYS} day(s) to avoid stale    #\n"
        "#  checks and missing updates.                                        #\n"
        "########################################################################\n"
    )
    print(banner, flush=True)


def confirm_staleness_or_exit(result: dict) -> None:
    """When `result['is_outdated']` is True, prompt the user to explicitly
    confirm before the collector continues running on an out-of-date skill.

    No-op (returns immediately) when: the check failed (`check_error` set —
    never gate on a connectivity problem), or the installation is up to date
    or AHEAD of the canonical `main` branch (`is_outdated` is False in both
    cases — see `check_skill_staleness()`).

    Non-interactive sessions (no attached TTY — e.g. piped/redirected input,
    CI runners) cannot be prompted at all; in that case this prints a notice
    and continues automatically rather than hanging indefinitely waiting for
    input that will never arrive. This function does NOT offer any
    download/update mechanism — confirmation only decides whether THIS run
    proceeds.
    """
    if result.get('check_error') or not result.get('is_outdated'):
        return

    if not sys.stdin.isatty():
        print(
            "[version-check] Non-interactive session detected — cannot prompt for "
            "confirmation. Continuing automatically, but please sync this plugin to "
            f"the latest version within {SYNC_GRACE_PERIOD_DAYS} day(s).",
            flush=True,
        )
        return

    prompt = (
        f"\nThis skill is behind the latest version on '{result['source_branch']}' "
        f"(local v{result['local_version']} vs. latest v{result['latest_stable_version']}). "
        f"You must sync to the latest version within {SYNC_GRACE_PERIOD_DAYS} day(s) to avoid "
        "stale checks and missing updates.\n"
        "Continue running with the current (outdated) version anyway? [y/N]: "
    )
    answer = input(prompt).strip().lower()
    if answer not in ('y', 'yes'):
        print("Aborting collector run — please sync to the latest version and try again.", flush=True)
        sys.exit(1)
