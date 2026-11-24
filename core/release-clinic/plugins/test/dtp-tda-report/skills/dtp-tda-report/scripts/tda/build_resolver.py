"""tda/build_resolver.py — Associated build discovery and YAML loading.

Responsibilities:
- Auto-discover associated pipeline build IDs from the release build's
  promotedImageList artifact (preferred)
- Fall back to stream_config.yaml when auto-discovery is disabled or fails
- Load PIT URL templates, Sonar key overrides, and Sonar stream config from
  stream_config.yaml — the single, mandatory source of truth for all
  per-stream configuration

No business/reporting logic lives here.  All ADO HTTP calls go through
tda.http_client.ADOClient.
"""

from __future__ import annotations

import logging
import os
import re
import sys
from functools import lru_cache

import yaml

from tda.config import Config, _find_config_file
from tda.http_client import ADOClient

# A discovered component build whose queueTime predates the release build's
# own queueTime by more than this many days is almost certainly a stale/unrelated
# tag match (e.g. a leftover tag on an old build on a shared branch) rather than
# a genuine release component — see discover_associated_builds().
STALE_BUILD_THRESHOLD_DAYS = 120


def _parse_ado_datetime(ts: str):
    """Parse an ADO ``queueTime``-style ISO8601 timestamp into a datetime.

    Returns None on empty/unparseable input rather than raising — staleness
    detection is a best-effort sanity check, not a hard requirement.
    """
    if not ts:
        return None
    from datetime import datetime
    cleaned = ts.strip()
    if cleaned.endswith('Z'):
        cleaned = cleaned[:-1] + '+00:00'
    # Truncate fractional seconds to microsecond precision (fromisoformat
    # only accepts up to 6 digits; ADO sometimes returns 7).
    if '.' in cleaned:
        head, _, tail = cleaned.partition('.')
        frac, _, tz = tail.partition('+')
        tz = '+' + tz if tz else ''
        if not tz and '-' in tail[1:]:  # negative offset (rare for ADO, but be safe)
            frac, _, tz = tail.partition('-')
            tz = '-' + tz
        cleaned = f"{head}.{frac[:6]}{tz}"
    try:
        return datetime.fromisoformat(cleaned)
    except ValueError:
        return None


def _flag_stale_builds(discovered_builds: dict[str, dict],
                        release_queue_time: str,
                        release_build_id: str,
                        release_pipeline_name: str) -> dict[str, dict]:
    """Flag any build in ``discovered_builds`` whose queueTime predates the
    release build's own queueTime by more than STALE_BUILD_THRESHOLD_DAYS.

    ``discovered_builds`` maps pipeline_name -> {'build_id', 'queue_time'}
    (the release pipeline's own entry, if present, is skipped).

    Returns {pipeline_name: {'build_id', 'queue_time', 'days_older'}}.
    Never raises — staleness detection is a best-effort sanity check.
    """
    stale_pipeline_builds: dict[str, dict] = {}
    release_dt = _parse_ado_datetime(release_queue_time)
    if release_dt is None:
        return stale_pipeline_builds

    for pipeline_name, info in discovered_builds.items():
        if pipeline_name == release_pipeline_name:
            continue
        candidate_dt = _parse_ado_datetime(info.get('queue_time', ''))
        if candidate_dt is None:
            continue
        days_older = (release_dt - candidate_dt).days
        if days_older > STALE_BUILD_THRESHOLD_DAYS:
            stale_pipeline_builds[pipeline_name] = {
                'build_id': info['build_id'],
                'queue_time': info['queue_time'],
                'days_older': days_older,
            }
            print(
                f"        [AutoDiscover] 🚨 STALE BUILD: '{pipeline_name}' build "
                f"{info['build_id']} was queued {days_older} day(s) before the "
                f"release build ({release_build_id}) — likely a stale/unrelated build "
                "match. Verify at the build-confirmation prompt, or pin the correct "
                "build_id under stream_config.yaml's 'builds' map for this pipeline.",
                flush=True,
            )
    return stale_pipeline_builds


# ---------------------------------------------------------------------------
# YAML file helpers
# ---------------------------------------------------------------------------

def _find_yaml(filename: str) -> str | None:
    return _find_config_file(filename)


def _load_yaml(filename: str) -> dict:
    path = _find_yaml(filename)
    if path is None:
        raise FileNotFoundError(
            f"{filename} not found in the workspace root or shipped collector configuration.\n"
            "Set TDA_STREAM_CONFIG to the collector stream configuration file."
        )
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f) or {}


@lru_cache(maxsize=1)
def _load_stream_config_yaml() -> dict:
    """Load stream_config.yaml — the mandatory, single source of truth for
    all per-stream configuration (builds, PIT URLs, Sonar/Genie/regression
    settings). Raises FileNotFoundError if the file is missing. Cached for
    the life of the process since it never changes mid-run.
    """
    return _load_yaml('stream_config.yaml')


def _get_stream_config_entry(release_stream: str) -> dict | None:
    """Return the stream_config.yaml block for this stream, or None if the
    stream has no entry under 'streams' there (caller should raise — there
    is no fallback config file)."""
    return (_load_stream_config_yaml().get('streams') or {}).get(release_stream.upper())


# ---------------------------------------------------------------------------
# Stream config from stream_config.yaml (single source of truth)
# ---------------------------------------------------------------------------

def load_stream_config(release_stream: str) -> tuple[dict, dict, dict, bool, str, bool, str]:
    """Extract PIT URL template, Sonar key overrides, Sonar stream config,
    genie_enabled flag, regression_run_filter, ado_regression_skip flag, and
    genie_test_management_app_id for the given stream from stream_config.yaml
    (`streams.<STREAM>`) — the single source of truth for stream configuration.

    Raises ValueError if the stream has no entry in stream_config.yaml.
    Returns (pit_links, sonar_key_overrides, sonar_stream_config, genie_enabled,
             regression_run_filter, ado_regression_skip, genie_test_management_app_id).
    """
    stream_key = release_stream.upper()
    stream_cfg = _get_stream_config_entry(release_stream)

    if stream_cfg is None:
        raise ValueError(
            f"Stream '{release_stream}' has no entry under 'streams' in stream_config.yaml. "
            f"Add a 'streams.{stream_key}' block (see FXO or SCM for a template)."
        )

    pit_links: dict[str, str] = {}
    pit_url_template = stream_cfg.get('pit_url')
    if pit_url_template:
        pit_links[stream_key] = str(pit_url_template).strip()
        print(
            f"        [PIT] Loaded URL template for stream '{release_stream}' "
            f"(stream_config.yaml): {pit_links[stream_key]}",
            flush=True,
        )
    else:
        print(
            f"        [PIT] ⚠️  No pit_url for stream '{release_stream}' "
            "in stream_config.yaml.",
            flush=True,
        )

    sonar_key_overrides = {
        str(k).strip(): str(v).strip()
        for k, v in (stream_cfg.get('sonar_keys') or {}).items()
        if k and v
    }
    if sonar_key_overrides:
        print(
            f"        [Sonar] Loaded {len(sonar_key_overrides)} project key override(s) "
            "(stream_config.yaml)",
            flush=True,
        )

    sonar_stream_config = dict(stream_cfg.get('sonar_config') or {})
    if sonar_stream_config:
        print(
            f"        [Sonar] Config for stream '{release_stream}' (stream_config.yaml): "
            f"{sonar_stream_config}",
            flush=True,
        )

    genie_enabled = bool(stream_cfg.get('genie_enabled', True))
    if not genie_enabled:
        print(
            f"        [Genie] Stream '{release_stream}' has genie_enabled: false "
            "(stream_config.yaml) — Genie regression collection will be skipped.",
            flush=True,
        )

    regression_cfg = stream_cfg.get('regression_config') or {}
    regression_run_filter = str(regression_cfg.get('regression_run_filter', '') or '').strip()
    if regression_run_filter:
        print(
            f"        [ADO Regression] regression_run_filter='{regression_run_filter}' "
            "loaded (stream_config.yaml).",
            flush=True,
        )

    ado_regression_skip = bool(regression_cfg.get('skip', False))
    if not genie_enabled and ado_regression_skip:
        print(
            f"        [ADO Regression] skip=true for '{release_stream}' (stream_config.yaml) "
            "— ADO-native regression fetch will be temporarily bypassed "
            "(no regression data collected).",
            flush=True,
        )

    genie_test_management_app_id = str(stream_cfg.get('genie_test_management_app_id', '') or '').strip()
    if genie_test_management_app_id:
        print(
            f"        [Genie Test-Management] app_id='{genie_test_management_app_id}' "
            f"loaded for '{release_stream}' (stream_config.yaml).",
            flush=True,
        )

    return (pit_links, sonar_key_overrides, sonar_stream_config, genie_enabled,
            regression_run_filter, ado_regression_skip, genie_test_management_app_id)


# ---------------------------------------------------------------------------
# Version-to-build resolution (used by auto-discovery)
# ---------------------------------------------------------------------------

def _resolve_builds_for_version(client: ADOClient, version: str,
                                branch_prefix: str = '',
                                release_branch: str = '',
                                extra_project_urls: list[str] | None = None,
                                branch_version_fallback_enabled: bool = False,
                                known_pipeline_names: set[str] | None = None) -> list[dict]:
    """Find ADO pipeline builds for a specific artifact image version.

    Queries the primary ADO project (via client) plus any ``extra_project_urls``
    — needed when component pipelines live in a different ADO project.

    ``branch_version_fallback_enabled`` (opt-in per stream via
    stream_config.yaml's ``branch_version_fallback_enabled: true`` — see
    RULES) additionally:
      - tries a ``release/{major}.{minor}.0`` candidate branch (some
        pipelines — e.g. RULES components — always use a trailing '.0'
        release-train branch regardless of the artifact's actual patch
        version), and
      - adds Strategy 4 below: when no tag strategy matches (because the
        pipeline's builds carry no tags at all), fall back to an UNFILTERED
        branch query and take the newest build by queueTime. This trades
        exact-patch traceability for release-train-level correctness, and is
        only used for streams that explicitly opt in — it never runs for
        streams relying on tag-based correlation (the default).

    ``known_pipeline_names`` — when supplied (the stream's manually-curated
    ``builds:`` map keys in stream_config.yaml), Strategy 4 restricts its
    result to builds whose pipeline (definition) name is in this set. Many
    unrelated pipelines from OTHER teams can share the same release-train
    branch (e.g. 'release/12.0'), so an unfiltered branch query can return
    builds that have nothing to do with this stream at all. Filtering to the
    known pipeline whitelist first is what actually narrows a noisy result
    (e.g. 6 pipelines found) down to just the ones this stream cares about.
    """
    parts = version.split('.')
    major, minor = parts[0], parts[1]  # patch is optional (e.g. '455.0' vs '116.0.3')

    candidate_branches = []
    if release_branch:
        candidate_branches.append(f"refs/heads/{release_branch}")
    if branch_prefix:
        candidate_branches.append(f"refs/heads/release/{branch_prefix}{major}.{minor}")
    candidate_branches.append(f"refs/heads/release/{major}.{minor}")
    if branch_version_fallback_enabled:
        candidate_branches.append(f"refs/heads/release/{major}.{minor}.0")
    # Deduplicate preserving order
    seen: set[str] = set()
    candidate_branches = [c for c in candidate_branches if not (c in seen or seen.add(c))]  # type: ignore[func-returns-value]

    # Version-SPECIFIC candidates only, for Strategy 4 below — deliberately
    # excludes the shared release_branch (e.g. 'release/rules-187.0.0'), which
    # is the same for every version being resolved and is NOT a signal of
    # which version a given build belongs to. Pooling it in would make
    # Strategy 4 converge on "whatever's newest on the shared release branch"
    # for every version, since that branch is almost always the most active.
    version_specific_branches = []
    if branch_prefix:
        version_specific_branches.append(f"refs/heads/release/{branch_prefix}{major}.{minor}")
    version_specific_branches.append(f"refs/heads/release/{major}.{minor}")
    if branch_version_fallback_enabled:
        version_specific_branches.append(f"refs/heads/release/{major}.{minor}.0")
    seen_vs: set[str] = set()
    version_specific_branches = [
        c for c in version_specific_branches if not (c in seen_vs or seen_vs.add(c))  # type: ignore[func-returns-value]
    ]

    def _sort(bl: list[dict]) -> list[dict]:
        bl.sort(key=lambda b: (b.get('definition', {}).get('name', ''), b.get('queueTime', '')))
        return bl

    # For each candidate tag, query ALL candidate branches with server-side tagFilters.
    # This bypasses the $top=200 per-branch limit — ADO filters by tag before applying
    # $top, so we always get matching builds even on very busy shared branches where
    # the relevant build would otherwise fall outside the top-200 window.
    seen_ids: set[int] = set()

    def _tagged_query(tag_key: str) -> list[dict]:
        matched: list[dict] = []
        for branch in candidate_branches:
            for b in client.list_builds_for_branch(
                branch, extra_base_urls=extra_project_urls, tag_filter=tag_key
            ):
                if b['id'] not in seen_ids:
                    seen_ids.add(b['id'])
                    matched.append(b)
        return matched

    # Strategy 1: build-version=X.Y.Z  (preferred — explicit per-component tag)
    exact = _tagged_query(f"build-version={version}")
    if exact:
        return _sort(exact)

    # Strategy 2: release-version=X.Y.Z
    rv = _tagged_query(f"release-version={version}")
    if rv:
        return _sort(rv)

    # Strategy 3: release-version=<release-branch-version>  (e.g. all components
    # tagged with the release-train version regardless of individual image version)
    if release_branch:
        rb_segment = release_branch.split('/')[-1]
        rb_version = rb_segment.split('-', 1)[-1] if '-' in rb_segment else rb_segment
        if rb_version != version:
            rb = _tagged_query(f"release-version={rb_version}")
            if rb:
                return _sort(rb)

    # Strategy 4 (opt-in only): no tags matched anything — this pipeline likely
    # doesn't tag its builds at all. Fall back to an UNFILTERED branch query and
    # take the newest build (by queueTime) as the resolved build. Only engages
    # when the stream has explicitly enabled branch_version_fallback_enabled —
    # every other stream still hard-fails below, exactly as before.
    #
    # IMPORTANT: uses `version_specific_branches` (NOT `candidate_branches`,
    # which also includes the shared `release_branch`). release_branch is the
    # SAME for every version being resolved in this release, so it carries no
    # version-specific signal — pooling it in here would make every version
    # converge on "whatever's newest on the shared release branch" instead of
    # a build that's actually on a branch matching THIS version.
    #
    # Queries ALL version_specific_branches and MERGES the results — does NOT
    # stop at the first branch with any builds. Different component pipelines
    # within the same release train can each follow a different branch-naming
    # convention (e.g. one pipeline builds on 'release/12.0' while another
    # only ever builds on 'release/12.0.0'), so stopping early at whichever
    # candidate branch happens to have *some* builds can miss the true latest
    # build for a pipeline that only builds on a later-priority candidate.
    # Merging first and picking the newest build PER PIPELINE across the
    # combined set guarantees each pipeline's true latest build wins,
    # regardless of which candidate branch it happens to live on.
    if branch_version_fallback_enabled:
        merged_builds: list[dict] = []
        branches_with_builds: list[str] = []
        for branch in version_specific_branches:
            branch_builds = [
                b for b in client.list_builds_for_branch(branch, extra_base_urls=extra_project_urls)
                if b['id'] not in seen_ids
            ]
            if not branch_builds:
                continue
            branches_with_builds.append(branch)
            for b in branch_builds:
                seen_ids.add(b['id'])
                merged_builds.append(b)

        # Narrow to this stream's known pipelines first (if a whitelist was
        # supplied) — a shared release-train branch is often also used by
        # pipelines belonging to OTHER teams/streams, which have nothing to
        # do with this artifact version and would otherwise show up as
        # unrelated "extra pipelines found" noise.
        if known_pipeline_names and merged_builds:
            before_count = len(merged_builds)
            filtered = [
                b for b in merged_builds
                if b.get('definition', {}).get('name', '') in known_pipeline_names
            ]
            dropped = before_count - len(filtered)
            if dropped:
                print(
                    f"        [AutoDiscover] known_pipeline_names filter: dropped {dropped} "
                    f"build(s) from pipeline(s) not in this stream's builds: map.",
                    flush=True,
                )
            merged_builds = filtered

        if merged_builds:
            newest_per_pipeline: dict[str, dict] = {}
            for b in merged_builds:
                pname = b.get('definition', {}).get('name', '')
                existing = newest_per_pipeline.get(pname)
                if existing is None or b.get('queueTime', '') > existing.get('queueTime', ''):
                    newest_per_pipeline[pname] = b
            result = list(newest_per_pipeline.values())
            print(
                f"        [AutoDiscover] branch_version_fallback_enabled: no tag matched "
                f"version {version} — using newest build per pipeline across branch(es) "
                + ', '.join(f"'{b}'" for b in branches_with_builds)
                + f" ({len(result)} pipeline(s): "
                + ', '.join(f"{b['id']}" for b in result)
                + ") as a release-train-level match (not exact-patch-traceable).",
                flush=True,
            )
            return _sort(result)

    # No tag strategy matched — surface a clear diagnostic.
    # Fall back to an unfiltered branch query for diagnostic info only.
    sample_builds: list[dict] = []
    for branch in candidate_branches:
        sample_builds.extend(client.list_builds_for_branch(branch, extra_base_urls=extra_project_urls))
        if len(sample_builds) >= 5:
            break
    sample_tags = '\n'.join(
        f"  build {b['id']}: {b.get('tags', [])}"
        for b in sample_builds[:5]
    )
    tried = ', '.join(f"'{b}'" for b in candidate_branches)
    raise ValueError(
        f"Artifact version {version}: no tag strategy matched any builds on {tried}.\n"
        f"Sample build tags (unfiltered):\n{sample_tags}"
    )


# ---------------------------------------------------------------------------
# Artifactory-based auto-discovery (opt-in per stream, 2026-08-06)
# ---------------------------------------------------------------------------
#
# Alternative to the tag/branch-guessing Strategies 1-4 in
# _resolve_builds_for_version() above. Instead of searching ADO for builds
# matching a tag or branch name, this resolves each promotedImageList helm3
# artifact's build.name/build.number DIRECTLY from Artifactory's build-info
# properties (stamped by JFrogPublishBuildInfo at publish time — see
# governed-templates/steps/jfrog-publish-buildinfo.yml), then looks up the
# exact ADO build via ADOClient.find_build_by_name_and_number(). No tags or
# branch names are guessed anywhere in this path.
#
# Gated by TWO per-stream stream_config.yaml flags, both required:
#   sonar_config.auto_discovery: true            (existing flag)
#   artifactory_build_discovery_enabled: true     (new, this feature)
# Disabled by default for every stream — has zero effect unless a stream
# explicitly opts in to both. Does not touch/replace the existing tag/branch
# strategies, which remain the only discovery path for every other stream.
#
# Docker artifacts are intentionally NOT resolved by this path — the
# Artifactory docker-sc-release_local repo returned 401 (needs an auth token
# not currently configured); only helm3-release_local is queried. If a
# component ONLY publishes a docker image with no helm3/maven counterpart,
# it will not be discovered via this path (open question, pending
# confirmation from the RULES pipeline team on whether every component
# always publishes a helm3/maven artifact alongside its docker image).
#
# Verified manually (2026-08-06, see repo memory) against a real 174-artifact
# RULES promotedImageList.json: all 8 resolved builds matched the existing
# manually-curated stream_config.yaml 'builds:' map for RULES.

_HELM_VERSION_SUFFIX_RE = re.compile(r'-(\d+\.\d+\.\d+)\.tgz$')
# Captures the chart name (filename stem before the version suffix), e.g.
# '50665-dtp-client' from '.../50665-dtp-client-471.0.0.tgz'. Used to ensure
# that two different charts that happen to share the same version number are
# NOT grouped together — grouping must be per-chart, not per-version alone.
_HELM_CHART_NAME_RE  = re.compile(r'/([^/]+)-\d+\.\d+\.\d+\.tgz$')


def _group_helm_paths_by_version(paths: list[str]) -> tuple[dict[str, list[str]], list[str]]:
    """Split helm3 artifact paths into (chart::version -> [paths]) groups, plus a
    list of paths whose version or chart name suffix couldn't be extracted (resolved
    individually, no grouping assumption made for those).

    The group key is ``<chart_name>::<version>`` (not version alone) so that two
    different charts that happen to share the same version string are never bundled
    into the same group. For example, if both ``50665-dtp-client_maven_pipeline``
    and ``50665-dtp-client_npm_pipeline`` publish a ``471.0.0``-versioned artifact,
    they will have different chart names and therefore form separate groups — each
    resolved individually via Artifactory, resulting in two distinct ADO pipeline
    lookups rather than one.
    """
    groups: dict[str, list[str]] = {}
    unmatched: list[str] = []
    for path in paths:
        mv = _HELM_VERSION_SUFFIX_RE.search(path)
        mc = _HELM_CHART_NAME_RE.search(path)
        if mv and mc:
            key = f"{mc.group(1)}::{mv.group(1)}"
            groups.setdefault(key, []).append(path)
        else:
            unmatched.append(path)
    return groups, unmatched


def _resolve_builds_via_artifactory(client: ADOClient,
                                    release_build_id: str,
                                    known_pipeline_names: set[str] | None = None
                                    ) -> tuple[dict, dict, dict, dict]:
    """Resolve associated builds via Artifactory build-info properties instead
    of ADO tag/branch guessing. See module-level comment block above for the
    full design rationale. Returns the same 4-tuple shape as
    discover_associated_builds() so it can be called from the same site.

    Artifacts sharing the same trailing '-<version>.tgz' suffix are grouped
    together before querying Artifactory (same version is assumed to be the
    same originating build) — only the first artifact per group is queried,
    with the last artifact ALSO queried as a spot-check for groups with more
    than one artifact. Any inconsistency falls back to resolving every
    artifact in that group individually rather than trusting the grouping.
    """
    _release_build = client.get('ProjectFromBuild', release_build_id).json()
    release_pipeline_name = _release_build['definition']['name']
    release_queue_time = _release_build.get('queueTime', '')
    discovered_builds: dict[str, dict] = {
        release_pipeline_name: {'build_id': str(release_build_id), 'queue_time': ''}
    }
    discovered_versions: dict[str, list] = {}
    duplicate_pipeline_versions: dict[str, list] = {}

    helm_paths = client.get_promoted_image_artifact_paths(release_build_id, repo='helm3-release_local')
    print(
        f"        [ArtifactoryDiscover] promotedImageList contains {len(helm_paths)} "
        "helm3 artifact(s) (docker entries intentionally skipped — needs Artifactory "
        "auth not currently configured).",
        flush=True,
    )

    groups, unmatched = _group_helm_paths_by_version(helm_paths)
    print(
        f"        [ArtifactoryDiscover] Grouped into {len(groups)} distinct chart+version group(s) "
        f"(+{len(unmatched)} unmatched path(s), resolved individually).",
        flush=True,
    )

    # (build_name, build_number, promoted_image_version) -> artifact paths that
    # resolved to it. Keyed by a synthetic string (not just version) because
    # the SAME version could theoretically resolve to different builds if the
    # spot-check ever finds an inconsistent group (see _resolve_group below) —
    # but the promoted_image_version stored in the tuple (NOT this dict key)
    # is what actually gets used as the discovered_versions key further down,
    # since that's the real artifact version string (e.g. '187.0.24') that
    # derive_pipeline_versions()/Sonar's release/<version> branch construction
    # expects — NOT a build_name#build_number label.
    resolved_pairs: dict[str, tuple[str, str, str, list[str]]] = {}

    def _resolve_group(version: str, paths: list[str]) -> None:
        first_name, first_number = client.get_artifactory_build_info(paths[0])
        if not (first_name and first_number):
            print(f"        [ArtifactoryDiscover] ⚠️  Could not resolve version '{version}' "
                  f"(artifact '{paths[0]}') via Artifactory — skipping.", flush=True)
            return
        consistent = True
        if len(paths) > 1:
            last_name, last_number = client.get_artifactory_build_info(paths[-1])
            if (last_name, last_number) != (first_name, first_number):
                consistent = False
                print(
                    f"        [ArtifactoryDiscover] ⚠️  version '{version}' group INCONSISTENT "
                    f"(first={first_name}#{first_number}, last={last_name}#{last_number}) — "
                    "resolving every artifact in this group individually.",
                    flush=True,
                )
        if consistent:
            resolved_pairs[f"{version}::{first_name}"] = (first_name, first_number, version, paths)
        else:
            for path in paths:
                name, number = client.get_artifactory_build_info(path)
                if name and number:
                    key = f"{version}::{path}"
                    resolved_pairs[key] = (name, number, version, [path])

    for group_key, paths in groups.items():
        # group_key is "<chart_name>::<version>" — extract the plain version for
        # _resolve_group so it correctly keys discovered_versions / log messages.
        _plain_version = group_key.split("::", 1)[1]
        _resolve_group(_plain_version, paths)
    for path in unmatched:
        name, number = client.get_artifactory_build_info(path)
        if name and number:
            # No version could be extracted from this path's suffix — leave
            # version as None rather than inventing a fake one. That pipeline
            # simply won't get a '_pipeline_versions' shortcut entry below and
            # falls back to normal ADO branch-based Sonar resolution instead
            # (same as any pipeline whose version is unknown), which is
            # correct/safe rather than reporting a misleading version string.
            resolved_pairs[f"unmatched::{path}"] = (name, number, None, [path])

    for _key, (build_name, build_number, promoted_version, paths) in resolved_pairs.items():
        build = client.find_build_by_name_and_number(build_name, build_number)
        if not build:
            print(
                f"        [ArtifactoryDiscover] ⚠️  {build_name} #{build_number} "
                "not found in ADO (definition renamed/deleted?) — skipping.",
                flush=True,
            )
            continue
        pipeline_name = build['definition']['name']
        if promoted_version:
            # Keyed by the REAL promotedImageList version (e.g. '187.0.24'),
            # matching the exact contract discover_associated_builds()'s
            # tag/branch path already uses — derive_pipeline_versions() reads
            # this dict's top-level key directly as the pipeline's version
            # for Sonar's release/<version> branch construction.
            discovered_versions.setdefault(promoted_version, []).append({
                'pipeline_name': pipeline_name,
                'build_id': str(build['id']),
                'build_number': build.get('buildNumber', ''),
                'result': build.get('result', ''),
                'source_branch': build.get('sourceBranch', ''),
                'queue_time': build.get('queueTime', ''),
            })
        if pipeline_name == release_pipeline_name:
            continue
        existing = discovered_builds.get(pipeline_name)
        candidate = {'build_id': str(build['id']), 'queue_time': build.get('queueTime', '')}
        if existing is None or candidate['queue_time'] > existing['queue_time']:
            discovered_builds[pipeline_name] = candidate

    if known_pipeline_names:
        extra = set(discovered_builds) - known_pipeline_names - {release_pipeline_name}
        if extra:
            print(
                f"        [ArtifactoryDiscover] ℹ️  Discovered {len(extra)} pipeline(s) not in "
                f"this stream's known 'builds:' map: {sorted(extra)} — new component or rename?",
                flush=True,
            )

    # Secondary sanity net only — this discovery path doesn't guess via tags/
    # branches, so the classic "stale tag match" risk this check was designed
    # for doesn't apply here. Kept anyway since it's cheap and can still catch
    # a genuinely wrong Artifactory-recorded build (e.g. republished artifact).
    stale_pipeline_builds = _flag_stale_builds(
        discovered_builds, release_queue_time, release_build_id, release_pipeline_name
    )

    ordered: dict[str, str] = {release_pipeline_name: discovered_builds.pop(release_pipeline_name)['build_id']}
    for name in sorted(discovered_builds):
        ordered[name] = discovered_builds[name]['build_id']

    logging.info("_resolve_builds_via_artifactory: result=%s", ordered)
    return ordered, discovered_versions, duplicate_pipeline_versions, stale_pipeline_builds


# ---------------------------------------------------------------------------
# Auto-discovery
# ---------------------------------------------------------------------------

def discover_associated_builds(client: ADOClient,
                               release_build_id: str,
                               sonar_stream_config: dict | None = None,
                               branch_version_fallback_enabled: bool = False,
                               known_pipeline_names: set[str] | None = None,
                               artifactory_build_discovery_enabled: bool = False) -> tuple[dict, dict, dict, dict]:
    """Auto-discover all component pipeline build IDs from the release build.

    ``sonar_stream_config`` may contain a ``component_ado_projects`` list of
    additional ADO project base URLs to query when component builds live in a
    different project than the release pipeline.  Example in stream_config.yaml:

        RATES:
          sonar_config:
            component_ado_projects:
              - https://dev.azure.com/sc-ado/50665/_apis

    ``branch_version_fallback_enabled`` — opt-in per stream via
    stream_config.yaml's ``branch_version_fallback_enabled: true`` (see
    RULES). Forwarded to ``_resolve_builds_for_version()`` — see its
    docstring for what this changes. Has no effect unless the stream sets it.

    ``known_pipeline_names`` — forwarded to ``_resolve_builds_for_version()``
    to narrow Strategy 4's unfiltered branch query to this stream's own
    pipelines. Has no effect unless branch_version_fallback_enabled is set.

    ``artifactory_build_discovery_enabled`` — opt-in per stream via
    stream_config.yaml's ``artifactory_build_discovery_enabled: true``. When
    set, discovery is delegated ENTIRELY to ``_resolve_builds_via_artifactory()``
    (Artifactory build-info properties, no tag/branch guessing) instead of the
    Strategies 1-4 tag/branch logic below. See that function's docstring and
    the module-level comment block above it for full design rationale.

    Returns:
        builds            — {pipeline_name: build_id_str}
        discovered_versions — {image_version: [metadata_dicts]}
        duplicate_pipeline_versions — {pipeline: [versions]} (when >1 version per pipeline)
        stale_pipeline_builds — {pipeline: {'build_id', 'queue_time', 'days_older'}}
                                (when the discovered build predates the release build's
                                own queueTime by more than STALE_BUILD_THRESHOLD_DAYS —
                                a strong signal of a stale/unrelated tag match)
    """
    if artifactory_build_discovery_enabled:
        return _resolve_builds_via_artifactory(
            client, release_build_id, known_pipeline_names=known_pipeline_names
        )

    extra_project_urls: list[str] = (sonar_stream_config or {}).get(
        'component_ado_projects', []
    )
    if extra_project_urls:
        print(
            f"        [AutoDiscover] Also querying {len(extra_project_urls)} "
            f"extra project(s): {extra_project_urls}",
            flush=True,
        )
    # Single call covers pipeline name + branch + queueTime — ProjectFromBuild
    # and BranchFromBuild both map to the same /build/builds/{id} endpoint.
    _release_build = client.get('ProjectFromBuild', release_build_id).json()
    release_pipeline_name = _release_build['definition']['name']
    release_queue_time = _release_build.get('queueTime', '')
    discovered_builds: dict[str, dict] = {
        release_pipeline_name: {'build_id': str(release_build_id), 'queue_time': ''}
    }
    discovered_versions: dict[str, list] = {}
    duplicate_pipeline_versions: dict[str, list] = {}

    release_branch = _release_build['sourceBranch'].split('/heads/')[-1]
    last_segment = release_branch.split('/')[-1]
    branch_prefix = (last_segment.rsplit('-', 1)[0] + '-') if '-' in last_segment else ''
    logging.info(
        "discover_associated_builds: branch='%s', prefix='%s'",
        release_branch, branch_prefix,
    )
    print(
        f"        [AutoDiscover] Release branch: {release_branch} → "
        f"component branch prefix: '{branch_prefix}'",
        flush=True,
    )

    all_versions = client.extract_promoted_image_versions(release_build_id)
    print(
        f"        [AutoDiscover] promotedImageList contains {len(all_versions)} version(s): "
        + ', '.join(all_versions),
        flush=True,
    )

    for version in all_versions:
        try:
            resolved = _resolve_builds_for_version(
                client, version,
                branch_prefix=branch_prefix,
                release_branch=release_branch,
                extra_project_urls=extra_project_urls,
                branch_version_fallback_enabled=branch_version_fallback_enabled,
                known_pipeline_names=known_pipeline_names,
            )
        except Exception as ver_exc:
            print(
                f"        [AutoDiscover] ⚠️  Could not resolve builds for version {version}: {ver_exc}",
                flush=True,
            )
            logging.warning(
                "discover_associated_builds: skipping version %s — %s", version, ver_exc
            )
            continue
        discovered_versions[version] = []
        for build in resolved:
            pipeline_name = build['definition']['name']
            discovered_versions[version].append({
                'pipeline_name': pipeline_name,
                'build_id': str(build['id']),
                'build_number': build.get('buildNumber', ''),
                'result': build.get('result', ''),
                'source_branch': build.get('sourceBranch', ''),
                'queue_time': build.get('queueTime', ''),
            })
            duplicate_pipeline_versions.setdefault(pipeline_name, []).append(version)
            # Never overwrite the explicitly supplied release pipeline build — it was
            # seeded with queue_time='' so any discovered build of the same pipeline
            # would otherwise displace it with a newer (but potentially wrong) run.
            if pipeline_name == release_pipeline_name:
                continue
            existing = discovered_builds.get(pipeline_name)
            candidate = {'build_id': str(build['id']), 'queue_time': build.get('queueTime', '')}
            if existing is None or candidate['queue_time'] > existing['queue_time']:
                discovered_builds[pipeline_name] = candidate

    # Staleness sanity check: flag any discovered build whose queueTime predates
    # the release build's own queueTime by an implausible margin. This is a
    # strong signal of a stale/unrelated tag match (e.g. a leftover tag on an
    # old build on a shared branch) rather than a genuine release component.
    # We only WARN/flag here — we never silently discard, since there may be
    # no fresher alternative and the caller (AutoTDAScript.py) surfaces this
    # at the interactive build-confirmation gate for a human to verify/abort.
    stale_pipeline_builds = _flag_stale_builds(
        discovered_builds, release_queue_time, release_build_id, release_pipeline_name
    )

    # Build final ordered dict: release pipeline first, then alphabetical
    ordered: dict[str, str] = {release_pipeline_name: discovered_builds.pop(release_pipeline_name)['build_id']}
    for name in sorted(discovered_builds):
        ordered[name] = discovered_builds[name]['build_id']

    duplicate_pipeline_versions = {
        name: sorted(set(versions))
        for name, versions in duplicate_pipeline_versions.items()
        if len(set(versions)) > 1
    }
    logging.info("discover_associated_builds: result=%s", ordered)
    return ordered, discovered_versions, duplicate_pipeline_versions, stale_pipeline_builds


# ---------------------------------------------------------------------------
# Build discovery from Custom.LatestPipelineRuns (opt-in per stream)
# ---------------------------------------------------------------------------

_VERSION_TAG_RE = re.compile(r'^(?:build|release)-version=(.+)$', re.IGNORECASE)


def discover_builds_from_release_field(client: ADOClient,
                                        release_id: str,
                                        release_build_id: str) -> tuple[dict, dict, dict, dict]:
    """Resolve associated builds by parsing ALL build links out of the Release
    WI's 'Custom.LatestPipelineRuns' field, instead of auto-discovering via a
    single master build's promotedImageList artifact.

    Used only for streams with 'builds_from_latest_pipeline_field: true' in
    stream_config.yaml — i.e. where the Release WI itself already links every
    component's build directly (e.g. SCALE), so there is no single master
    build to expand from via promotedImageList.

    Per extracted build, a version is derived as follows (no promotedImageList
    artifact or branch tag-search involved — just that build's own metadata):
      1. A 'build-version=' / 'release-version=' build tag, if present (same
         convention discover_associated_builds() already searches for).
      2. Otherwise, the branch's own suffix after 'release/' (e.g.
         'release/scale_agg_26.0' -> 'scale_agg_26.0') — matching the same
         convention already used for manually-maintained streams (e.g. SCALE)
         in stream_config.yaml today.
      A pipeline with neither is simply omitted from the returned version map
      (same as an untagged pipeline under normal auto-discovery).

    Returns:
        builds                    — {pipeline_name: build_id_str}
        pipeline_versions         — {pipeline_name: version_str} (only when derived)
        duplicate_pipeline_builds — {pipeline: [build_ids]} (when >1 build for the
                                     same pipeline found in the field; newest
                                     queueTime wins in `builds`)
        stale_pipeline_builds     — {pipeline: {'build_id','queue_time','days_older'}}
                                     (same staleness rule as discover_associated_builds)

    Raises ValueError if no 'buildId=' links are found in the field at all —
    the caller (resolve_builds) falls back to stream_config.yaml on failure,
    same as a failed promotedImageList auto-discovery.
    """
    _release_build = client.get('ProjectFromBuild', release_build_id).json()
    release_pipeline_name = _release_build['definition']['name']
    release_queue_time = _release_build.get('queueTime', '')

    rwi_resp = client.get('WorkItemsForRelease', release_id)
    raw_field = rwi_resp.json().get('fields', {}).get('Custom.LatestPipelineRuns', '') or ''
    found_ids: list[str] = []
    seen_ids: set[str] = set()
    for bid in re.findall(r'buildId=(\d+)', raw_field):
        if bid not in seen_ids:
            seen_ids.add(bid)
            found_ids.append(bid)

    print(
        f"        [AutoDiscover] builds_from_latest_pipeline_field: found {len(found_ids)} "
        f"build link(s) in Custom.LatestPipelineRuns: {', '.join(found_ids) or '(none)'}",
        flush=True,
    )
    if not found_ids:
        raise ValueError(
            "builds_from_latest_pipeline_field: true but no 'buildId=' links were found in "
            "Custom.LatestPipelineRuns on the Release WI."
        )

    discovered_builds: dict[str, dict] = {
        release_pipeline_name: {'build_id': str(release_build_id), 'queue_time': ''}
    }
    pipeline_versions: dict[str, str] = {}
    duplicate_pipeline_builds: dict[str, list] = {}

    for bid in found_ids:
        try:
            build = client.get('ProjectFromBuild', bid).json()
        except Exception as exc:
            print(f"        [AutoDiscover] ⚠️  Could not fetch build {bid}: {exc}", flush=True)
            logging.warning("discover_builds_from_release_field: failed to fetch build %s — %s", bid, exc)
            continue

        pipeline_name = build.get('definition', {}).get('name', '')
        if not pipeline_name:
            continue
        queue_time = build.get('queueTime', '')
        branch = build.get('sourceBranch', '').split('/heads/')[-1]
        tags = build.get('tags', []) or []

        duplicate_pipeline_builds.setdefault(pipeline_name, []).append(str(bid))

        # Never overwrite the explicitly supplied release pipeline build.
        if pipeline_name == release_pipeline_name:
            continue

        existing = discovered_builds.get(pipeline_name)
        candidate = {'build_id': str(bid), 'queue_time': queue_time}
        if existing is not None and candidate['queue_time'] <= existing['queue_time']:
            continue
        discovered_builds[pipeline_name] = candidate

        version = ''
        for tag in tags:
            m = _VERSION_TAG_RE.match(str(tag))
            if m:
                version = m.group(1).strip()
                break
        if not version and branch.startswith('release/'):
            version = branch.split('/', 1)[-1]
        if version:
            pipeline_versions[pipeline_name] = version
        else:
            pipeline_versions.pop(pipeline_name, None)
            print(
                f"        [AutoDiscover] ⚠️  No version tag or 'release/' branch found for "
                f"'{pipeline_name}' (build {bid}, branch '{branch}') — Sonar will fall back to "
                "its default branch_strategy for this pipeline.",
                flush=True,
            )

    # Staleness sanity check (same rule/threshold as discover_associated_builds)
    stale_pipeline_builds = _flag_stale_builds(
        discovered_builds, release_queue_time, release_build_id, release_pipeline_name
    )

    ordered: dict[str, str] = {release_pipeline_name: discovered_builds.pop(release_pipeline_name)['build_id']}
    for name in sorted(discovered_builds):
        ordered[name] = discovered_builds[name]['build_id']

    duplicate_pipeline_builds = {
        name: sorted(set(ids)) for name, ids in duplicate_pipeline_builds.items()
        if len(set(ids)) > 1
    }
    logging.info("discover_builds_from_release_field: result=%s", ordered)
    return ordered, pipeline_versions, duplicate_pipeline_builds, stale_pipeline_builds


def derive_pipeline_versions(discovered_versions: dict, blade_release_builds: dict) -> dict:
    """Turn discover_associated_builds()'s {version: [metadata_dicts]} output
    into a {pipeline_name: version} map, keeping only the version that
    matches the build_id actually selected in ``blade_release_builds`` (so a
    pipeline with multiple resolved versions reports the one actually used,
    not every version it was ever seen at).

    Returns {} when ``discovered_versions`` is empty (e.g. YAML-loaded builds,
    where per-pipeline versions instead come from stream_config.yaml's
    explicit `_pipeline_versions` annotations).
    """
    pipeline_versions: dict[str, str] = {}
    for version, entries in (discovered_versions or {}).items():
        for entry in entries:
            pipeline_name = entry.get('pipeline_name')
            build_id = entry.get('build_id')
            if pipeline_name and blade_release_builds.get(pipeline_name) == build_id:
                pipeline_versions[pipeline_name] = version
    return pipeline_versions


# ---------------------------------------------------------------------------
# YAML-based build loading
# ---------------------------------------------------------------------------

def load_builds_from_yaml(release_stream: str) -> tuple[dict, dict, dict]:
    """Read the ``builds`` map + Sonar config for the given stream from
    stream_config.yaml (`streams.<STREAM>.builds`) — the single source of
    truth for stream configuration.

    Each entry value may be:
      - a plain build ID:                 ``13028582``
      - a build ID with version hint:     ``13028582 185.0.14``

    The optional version string (after the first space) is collected into
    ``sonar_stream_config['_pipeline_versions']`` so the Sonar branch can be
    constructed as ``release/<version>`` without an extra ADO API call.
    This is particularly useful when ``auto_discovery: false``.

    Raises ValueError if the stream has no entry, or no ``builds``, in
    stream_config.yaml.

    Returns:
        builds              — {pipeline_name: build_id_str}
        sonar_key_overrides — {pipeline_name: sonar_project_key}
        sonar_stream_config — raw config dict (Sonar config), with
                              '_pipeline_versions' injected when annotations present
    """
    stream_key = release_stream.upper()
    stream_cfg = _get_stream_config_entry(release_stream)
    if stream_cfg is None:
        raise ValueError(
            f"Stream '{release_stream}' has no entry under 'streams' in stream_config.yaml. "
            f"Add a 'streams.{stream_key}' block with a 'builds' map."
        )

    stream_data = stream_cfg.get('builds') or {}
    if not stream_data:
        raise ValueError(
            f"'streams.{stream_key}.builds' in stream_config.yaml has no entries.\n"
            f"Add entries under 'streams.{stream_key}.builds' in stream_config.yaml."
        )
    builds: dict[str, str] = {}
    pipeline_versions: dict[str, str] = {}
    for k, v in stream_data.items():
        if not k or not v:
            continue
        raw = str(v).strip()
        parts = raw.split(None, 1)   # split on first whitespace only
        builds[str(k).strip()] = parts[0]
        if len(parts) == 2:
            pipeline_versions[str(k).strip()] = parts[1]
    if not builds:
        raise ValueError(
            f"'streams.{stream_key}.builds' in stream_config.yaml has no valid entries."
        )
    logging.info(
        "load_builds_from_yaml: loaded %d build(s) for %s from stream_config.yaml",
        len(builds), release_stream,
    )
    (pit_links, sonar_key_overrides, sonar_stream_config, _genie_enabled, _run_filter,
     _ado_skip, _genie_test_mgmt_app_id) = load_stream_config(release_stream)

    if pipeline_versions:
        sonar_stream_config = dict(sonar_stream_config)  # avoid mutating loaded dict
        sonar_stream_config['_pipeline_versions'] = pipeline_versions
        print(
            f"        [Builds] Version annotations found for {len(pipeline_versions)} "
            f"pipeline(s) — Sonar branches will use release/<version> directly.",
            flush=True,
        )

    return builds, sonar_key_overrides, sonar_stream_config


# ---------------------------------------------------------------------------
# Top-level resolver — attempts auto-discovery then falls back to YAML
# ---------------------------------------------------------------------------

def resolve_builds(client: ADOClient, release_stream: str,
                   release_build_id: str, use_yaml: bool,
                   release_id: str | None = None) -> tuple[dict, str, dict, dict, dict, dict, dict, bool, str, bool, dict, str]:
    """Resolve associated builds, returning everything the controller needs.

    ``release_id`` (the Release WI id) is only required when the stream has
    'builds_from_latest_pipeline_field: true' in stream_config.yaml — it is
    used to fetch Custom.LatestPipelineRuns off the Release WI. It is unused
    for every other stream/path.

    Returns:
        builds                   — {pipeline_name: build_id_str}
        source                   — 'auto' | 'release_field' | 'yaml'
        discovered_versions      — {image_version: [metadata_dicts]}; {} for the
                                   'release_field' and 'yaml' paths
        duplicate_pipeline_versions — {pipeline: [versions_or_build_ids]}
        sonar_key_overrides
        sonar_stream_config
        pit_links                — {STREAM: url_template}
        genie_enabled            — bool (False when stream is in GENIE_DISABLED_STREAMS)
        regression_run_filter    — str (empty = all ADO test runs; substring = filter by run name)
        ado_regression_skip      — bool (True to temporarily bypass the ADO-native regression fetch)
        stale_pipeline_builds    — {pipeline: {'build_id','queue_time','days_older'}}; always {}
                                   for the YAML-loaded path (no discovery/queueTime data there)
        genie_test_management_app_id — str (empty when unset); per-stream opt-in Genie
                                   test-management API application id (stream_config.yaml)
    """
    # Load stream config first (needed for auto_discovery flag)
    (pit_links, sonar_keys, sonar_cfg, genie_enabled, regression_run_filter,
     ado_regression_skip, genie_test_management_app_id) = load_stream_config(release_stream)
    auto_error: Exception | None = None

    stream_cfg_entry = _get_stream_config_entry(release_stream) or {}
    use_release_field_builds = bool(stream_cfg_entry.get('builds_from_latest_pipeline_field', False))
    branch_version_fallback_enabled = bool(stream_cfg_entry.get('branch_version_fallback_enabled', False))
    # Opt-in Artifactory-based discovery (2026-08-06) — requires BOTH this flag
    # AND sonar_config.auto_discovery: true (checked further below, same gate
    # as the existing tag/branch auto-discovery path). See
    # discover_associated_builds()/_resolve_builds_via_artifactory() docstrings.
    artifactory_build_discovery_enabled = bool(stream_cfg_entry.get('artifactory_build_discovery_enabled', False))
    # Whitelist of this stream's own pipeline names (the manually-curated
    # 'builds:' map keys) — used by Strategy 4's branch fallback to filter
    # out unrelated pipelines from other teams that happen to share the same
    # release-train branch. Only meaningful when branch_version_fallback_enabled.
    # NOTE: `.get('builds', {})` is NOT safe here — if a stream's `builds:` key
    # is present but empty (e.g. every entry commented out), YAML parses it as
    # `None`, not `{}`. `.get(key, default)` only substitutes `default` when the
    # key is ABSENT, so a `builds: None` value silently defeats the `{}`
    # fallback and crashes `.keys()` with AttributeError. Use `... or {}` instead.
    known_pipeline_names: set[str] | None = set((stream_cfg_entry.get('builds') or {}).keys()) or None

    if use_yaml:
        auto_error = RuntimeError("--use-yaml flag supplied — skipping auto-discovery.")
        logging.info("resolve_builds: --use-yaml; bypassing auto-discovery.")
        print("        [Builds] --use-yaml: using stream_config.yaml builds.", flush=True)
    elif use_release_field_builds:
        if not release_build_id or not release_id:
            auto_error = RuntimeError(
                "builds_from_latest_pipeline_field: true requires both release_id and a "
                "release build_id to be supplied."
            )
        else:
            try:
                builds, pipeline_versions, dupe_builds, stale_builds = discover_builds_from_release_field(
                    client, release_id, release_build_id
                )
                sonar_cfg = dict(sonar_cfg)  # avoid mutating the loaded config dict
                if pipeline_versions:
                    sonar_cfg['_pipeline_versions'] = {
                        **sonar_cfg.get('_pipeline_versions', {}), **pipeline_versions
                    }
                return (builds, 'release_field', {}, dupe_builds, sonar_keys, sonar_cfg,
                        pit_links, genie_enabled, regression_run_filter, ado_regression_skip,
                        stale_builds, genie_test_management_app_id)
            except Exception as exc:
                auto_error = exc
                logging.warning("builds_from_latest_pipeline_field discovery failed: %s", exc)
                print(
                    f"        [Builds] ⚠️  builds_from_latest_pipeline_field discovery failed: {exc}\n"
                    "        [Builds] Falling back to stream_config.yaml builds.",
                    flush=True,
                )
    elif release_build_id:
        if not sonar_cfg.get('auto_discovery', True):
            auto_error = RuntimeError(
                f"auto_discovery disabled for '{release_stream}' in stream_config.yaml."
            )
        else:
            try:
                builds, version_map, dupe_versions, stale_builds = discover_associated_builds(
                    client, release_build_id, sonar_stream_config=sonar_cfg,
                    branch_version_fallback_enabled=branch_version_fallback_enabled,
                    known_pipeline_names=known_pipeline_names,
                    artifactory_build_discovery_enabled=artifactory_build_discovery_enabled,
                )
                return (builds, 'auto', version_map, dupe_versions, sonar_keys, sonar_cfg,
                        pit_links, genie_enabled, regression_run_filter, ado_regression_skip,
                        stale_builds, genie_test_management_app_id)
            except Exception as exc:
                auto_error = exc
                logging.warning("Auto-discovery failed: %s", exc)
                print(
                    f"        [Builds] ⚠️  Auto-discovery failed: {exc}\n"
                    "        [Builds] Falling back to stream_config.yaml builds.",
                    flush=True,
                )

    # YAML fallback
    try:
        builds, sonar_keys2, sonar_cfg2 = load_builds_from_yaml(release_stream)
        # Re-read pit_links from yaml (load_builds_from_yaml reloads via load_stream_config)
        (pit_links2, _, _, genie_enabled2, regression_run_filter2, ado_regression_skip2,
         genie_test_management_app_id2) = load_stream_config(release_stream)
        return (builds, 'yaml', {}, {}, sonar_keys2, sonar_cfg2, pit_links2, genie_enabled2,
                regression_run_filter2, ado_regression_skip2, {}, genie_test_management_app_id2)
    except Exception as yaml_error:
        if auto_error is not None:
            raise RuntimeError(
                f"Auto-discovery failed: {auto_error}\n\nYAML fallback failed: {yaml_error}"
            ) from yaml_error
        raise
