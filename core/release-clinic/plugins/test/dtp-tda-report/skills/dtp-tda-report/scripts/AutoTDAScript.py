"""AutoTDAScript_v2.py — slim controller built on the tda.* package.

This is the Phase-6 refactored entry point.  All heavy logic lives in the
tda.* submodules; this file is a ~100-line orchestration shell.

Usage (identical to AutoTDAScript.py):
  python AutoTDAScript_v2.py <release_id> <build_id> <stream> [release_version]
                             [--use-yaml] [--no-batch] [--no-parallel]
"""

import argparse
import json
import logging
import os
import sys
import time

# Force UTF-8 output so emoji/unicode in print() don't crash on cp1252 terminals
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.stderr.reconfigure(encoding='utf-8', errors='replace')

from tda.config import Config, load_env_file, decrypt_snow_credentials
from tda.summarizer import generate_summary
from tda.http_client import ADOClient
from tda.build_resolver import resolve_builds, load_stream_config, derive_pipeline_versions
from tda.result_store import ResultStore
from tda.call_tracker import tracker as call_tracker
from tda.version_check import check_skill_staleness, print_staleness_banner, confirm_staleness_or_exit

from tda.collectors.release import collect_release_data
from tda.collectors.testing import (
    return_test_suites,
    return_test_cases_from_suite,
    populate_test_case_details,
    extract_test_plan_checks,
    extract_test_result_checks,
    get_story_items_in_release,
)
from tda.collectors.traceability import build_traceability


# ---------------------------------------------------------------------------
# Version — keep this in sync with the dtp-tda-report SKILL.md metadata.version.
# The collector stamps every JSON output file with this value so the SKILL can
# detect when a user is running an older collector against a newer (or older)
# skill, and warn them to upgrade.
#
# IMPORTANT: bump this whenever SKILL.md's metadata.version is bumped AND the
# change involves new/changed collector output (new tda/ package fields,
# integrations, or config keys) — not just HTML-template/report-writing-rule
# changes confined to SKILL.md itself. See repo memory notes for the full
# history of SKILL.md bumps vs. actual collector code changes.
# ---------------------------------------------------------------------------
COLLECTOR_VERSION = "1.11.0"


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description='AutoTDA data collector — outputs structured JSON for dtp-tda-report skill.'
    )
    parser.add_argument('release_id',     help='ADO Release Work Item ID (e.g. 12347453)')
    parser.add_argument('build_id',       nargs='?', default='',
                        help='ADO Pipeline Build ID (e.g. 9086679). '
                             'Optional when --rwi-only is used.')
    parser.add_argument('release_stream', help='Release stream (e.g. FXO, OMS, RATES, BCF)')
    parser.add_argument('release_version', nargs='?', default='',
                        help='Release version string (e.g. 455.0). When supplied, used directly '
                             'for Sonar branch and PIT URL substitution.')
    parser.add_argument('--use-yaml', action='store_true', default=False,
                        help='Skip auto-discovery; read build IDs from stream_config.yaml.')
    parser.add_argument('--no-batch', action='store_true', default=False,
                        help='Disable bulk work item fetching (Step 4).')
    parser.add_argument('--no-parallel', action='store_true', default=False,
                        help='Disable all parallel threading.')
    parser.add_argument('--rwi-only', action='store_true', default=False,
                        help='Collect only RWI-derived data (release WI, stories, bugs, test plan, '
                             'traceability, SNOW, PIT, PT). Skips build-dependent checks: '
                             'unit tests, Sonar coverage, and Genie regression. '
                             'build_id is not required in this mode.')
    args = parser.parse_args()

    if not args.rwi_only and not args.build_id:
        parser.error('build_id is required unless --rwi-only is specified.')

    # release_stream is needed before bootstrap so decrypt_snow_credentials()/
    # Config.from_env() can apply a per-stream SNOW_ENABLED override from
    # stream_config.yaml (streams.<STREAM>.snow_enabled).
    release_stream = args.release_stream

    # --- Bootstrap ---
    load_env_file()
    decrypt_snow_credentials(release_stream)
    cfg = Config.from_env(release_stream)
    if args.no_parallel:
        cfg.parallel_enabled = False

    client = ADOClient(cfg)
    client.set_proxy()

    # --- Skill Version Staleness Check (2026-10-13) ---
    # This plugin is cloned/vendored into many consumer repos via apm — once
    # cloned, a local copy silently stops tracking the canonical repo's ongoing
    # updates. Best-effort, non-blocking: compares this installation's SKILL.md
    # metadata.version against the canonical repo's stable `main` branch (not
    # the `tdacommit` beta branch) and prints a loud console warning if behind.
    skill_version_check = check_skill_staleness(client)
    print_staleness_banner(skill_version_check)
    # If outdated (never when up to date or ahead), require explicit
    # confirmation before continuing. Non-blocking/no-op if the check itself
    # failed or stdin isn't interactive (see confirm_staleness_or_exit docstring).
    confirm_staleness_or_exit(skill_version_check)

    # Reset the API call tracker so counts/rates reflect only this run —
    # module import happens once per process, but main() may conceptually
    # be re-entered (tests, REPL use), so make the reset explicit here.
    call_tracker.reset()

    release_id             = args.release_id
    supplied_build_id      = args.build_id
    supplied_release_version = args.release_version.strip() if args.release_version else ''
    use_yaml               = args.use_yaml
    rwi_only               = args.rwi_only

    # --- Step 1: resolve associated builds (skipped in --rwi-only mode) ---
    if rwi_only:
        print(f"[1/6] --rwi-only mode: skipping build resolution.", flush=True)
        print(f"      Unit tests, Sonar coverage, and Genie regression will not be collected.", flush=True)
        blade_release_builds      = {}
        associated_builds_source  = 'rwi-only'
        associated_build_versions = {}
        duplicate_pipeline_versions = {}
        stale_pipeline_builds     = {}
        sonar_key_overrides       = {}
        sonar_stream_config       = {}
        # Still load PIT URL template and genie_enabled from YAML — stream config, not build-specific.
        (pit_links, _, _, genie_enabled, regression_run_filter, ado_regression_skip,
         genie_test_management_app_id) = load_stream_config(release_stream)
        resolved_pipeline_versions = {}
    else:
        print(f"[1/6] Resolving associated builds for release build {supplied_build_id}...", flush=True)
        (blade_release_builds,
         associated_builds_source,
         associated_build_versions,
         duplicate_pipeline_versions,
         sonar_key_overrides,
         sonar_stream_config,
         pit_links,
         genie_enabled,
         regression_run_filter,
         ado_regression_skip,
         stale_pipeline_builds,
         genie_test_management_app_id) = resolve_builds(client, release_stream, supplied_build_id, use_yaml,
                                                  release_id=release_id)

        # Per-pipeline version, from whichever source applies to this run:
        # - auto-discovery: derived from promotedImageList metadata (associated_build_versions),
        #   matched against the build_id actually selected for each pipeline.
        # - YAML-loaded builds: explicit "<build_id> <version>" annotations in stream_config.yaml
        #   (sonar_stream_config['_pipeline_versions']).
        # Explicit YAML annotations win if both happen to be present for the same pipeline.
        resolved_pipeline_versions = derive_pipeline_versions(associated_build_versions, blade_release_builds)
        resolved_pipeline_versions.update(sonar_stream_config.get('_pipeline_versions', {}))

        # --- Build confirmation gate (interactive, full mode only) ---
        print()
        print("=" * 75)
        print(f"  ⚠️  PLEASE VERIFY ASSOCIATED BUILDS FOR STREAM: {release_stream}")
        print("=" * 75)
        _source_label = {
            'auto': 'auto-discovered (promotedImageList)',
            'release_field': 'auto-discovered (Custom.LatestPipelineRuns)',
        }.get(associated_builds_source, 'stream_config.yaml')
        print(f"  Source: {_source_label}")
        print()
        if resolved_pipeline_versions:
            print(f"    {'Pipeline':<50} {'Build ID':<14} {'Version'}")
            print(f"    {'─'*50} {'─'*14} {'─'*12}")
            for _name, _bid in blade_release_builds.items():
                _ver = resolved_pipeline_versions.get(_name, '')
                print(f"    {_name:<50} {_bid:<14} {_ver}")
        else:
            for _name, _bid in blade_release_builds.items():
                print(f"    {_name:<50} {_bid}")
        if duplicate_pipeline_versions:
            print()
            print("  ⚠  Duplicate versions resolved per pipeline (newest selected):")
            for _pname, _versions in sorted(duplicate_pipeline_versions.items()):
                print(f"       {_pname}: {', '.join(_versions)}")
        if stale_pipeline_builds:
            print()
            print("  🚨 STALE BUILD WARNING — discovered build predates the release build")
            print("     by an implausible margin. Likely a stale/unrelated tag match, not the")
            print("     true release component. Decide per-build below (default: exclude):")
            for _pname, _info in sorted(stale_pipeline_builds.items()):
                print()
                print(
                    f"       {_pname}: build {_info['build_id']} is "
                    f"{_info['days_older']} day(s) older than the release build"
                )
                try:
                    _keep = input(
                        f"       Keep this build for '{_pname}'? [y/N]: "
                    ).strip().lower()
                except (EOFError, KeyboardInterrupt):
                    _keep = "n"
                if _keep == "y":
                    print(f"       ✅ Keeping '{_pname}' build {_info['build_id']} as supplied.")
                else:
                    blade_release_builds.pop(_pname, None)
                    resolved_pipeline_versions.pop(_pname, None)
                    print(
                        f"       ⏭️  Excluded '{_pname}' — build {_info['build_id']} will NOT be "
                        "collected (no Sonar/unit-test data for this pipeline in this report)."
                    )
            print()
            print("  Updated build list:")
            if resolved_pipeline_versions:
                print(f"    {'Pipeline':<50} {'Build ID':<14} {'Version'}")
                print(f"    {'─'*50} {'─'*14} {'─'*12}")
                for _name, _bid in blade_release_builds.items():
                    _ver = resolved_pipeline_versions.get(_name, '')
                    print(f"    {_name:<50} {_bid:<14} {_ver}")
            else:
                for _name, _bid in blade_release_builds.items():
                    print(f"    {_name:<50} {_bid}")
        print()
        try:
            answer = input("  Confirm builds are correct and continue? [y/N]: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            answer = "n"
        if answer != "y":
            print("\n  ❌ Aborted. Please update stream_config.yaml and re-run.\n")
            sys.exit(1)
        print("\n  ✅ Builds confirmed — proceeding with data collection.\n")

    # --- Step 2 header ---
    print(f"[2/6] Starting full TDA data collection for release {release_id} ({release_stream})...", flush=True)
    store = ResultStore()
    _t_start = time.time()

    # --- Step 3: release WI + all integrations ---
    _t3 = time.time()
    release_data = collect_release_data(
        release_id=release_id,
        supplied_build_id=supplied_build_id,
        release_stream=release_stream,
        blade_release_builds=blade_release_builds,
        sonar_stream_config=sonar_stream_config,
        sonar_key_overrides=sonar_key_overrides,
        pit_links=pit_links,
        supplied_release_version=supplied_release_version,
        cfg=cfg,
        client=client,
        rwi_only=rwi_only,
        genie_enabled=genie_enabled,
        regression_run_filter=regression_run_filter,
        ado_regression_skip=ado_regression_skip,
        genie_test_management_app_id=genie_test_management_app_id,
    )
    store.ingest_release_data(release_data)
    print(f"      [3/6] done in {time.time() - _t3:.1f}s", flush=True)

    # --- Step 4: linked WIs (stories, bugs, test plans, application) ---
    _t4 = time.time()
    work_item_relations = release_data['work_item_relations']
    print(f"  [4/6] Processing {len(work_item_relations)} linked work items...", flush=True)

    wi_ids = [wi['url'].split('workItems/')[-1] for wi in work_item_relations]
    wi_batch = client.fetch_work_items_batch(wi_ids) if (not args.no_batch and wi_ids) else {}

    story_features = get_story_items_in_release(work_item_relations, wi_batch, cfg, client)
    store.story_features.extend(story_features)

    # Application, Bug, Test Plan — dispatched from batch
    from tda.http_client import WIResponseAdapter
    from tda.collectors.release import extract_application_checks, extract_bug_checks
    from tda.build_resolver import _get_stream_config_entry

    _stream_cfg = _get_stream_config_entry(release_stream) or {}
    _app_post_approval_check = bool(
        _stream_cfg.get('application_confluence_post_approval_check_enabled', False)
    )
    if _app_post_approval_check:
        print(
            "  [4/6] application_confluence_post_approval_check_enabled=true — "
            "will check Application WI Confluence links for post-approval edits.",
            flush=True,
        )

    test_plan_ids: list[str] = []
    for wi in work_item_relations:
        wi_id   = wi['url'].split('workItems/')[-1]
        wi_data = wi_batch.get(wi_id) if wi_batch else None
        if wi_data is None:
            wi_data = client.get('WorkItemsForRelease', wi_id).json()
        resp = WIResponseAdapter(wi_data)
        wi_type = wi_data.get('fields', {}).get('System.WorkItemType', '')

        if wi_type == 'Application':
            store.application_features.append(
                extract_application_checks(
                    resp, cfg,
                    client=client if _app_post_approval_check else None,
                    post_approval_check=_app_post_approval_check,
                )
            )
        elif wi_type == 'Bug':
            store.bug_features.append(extract_bug_checks(resp, cfg))
        elif wi_type == 'Test Plan':
            plan_id = str(wi_data.get('id', ''))
            store.test_plan_features.append(extract_test_plan_checks(resp, client))
            test_plan_ids.append(plan_id)

    # Test results for each plan
    for plan_id in test_plan_ids:
        result_rows = extract_test_result_checks(None, plan_id, cfg, client)
        # Filter to only TCs currently in the plan's suites.
        # Run history includes results from TCs that were executed then later
        # removed from the plan — without this filter they surface as CRITICAL
        # missing-evidence findings in the report even though they are no
        # longer in scope for the release.
        try:
            suites = return_test_suites(plan_id, client)
            plan_tcs = return_test_cases_from_suite(plan_id, suites, client)
            active_tc_ids = {str(tc.get('testCase', {}).get('id', '')) for tc in plan_tcs} - {''}
            if active_tc_ids:
                before = len(result_rows)
                result_rows = [r for r in result_rows if r['TestCase Id'] in active_tc_ids]
                removed = before - len(result_rows)
                if removed:
                    logging.info(
                        "plan %s: filtered %d result(s) for TCs removed from plan suites",
                        plan_id, removed,
                    )
        except Exception as e:
            logging.warning(
                "plan %s: could not fetch suite TC list for filtering — %s; "
                "results not filtered (may include orphaned TCs)",
                plan_id, e,
            )
        store.test_result_features.extend(result_rows)

    print(f"      [4/6] done in {time.time() - _t4:.1f}s", flush=True)

    # --- Step 5: traceability ---
    _t5 = time.time()
    print(f"  [5/6] Building traceability for {len(story_features)} stories...", flush=True)
    traceability_rows, unique_tcs, tc_fields_batch = build_traceability(story_features, release_id, cfg, client)
    store.ingest_traceability(traceability_rows, unique_tcs)
    print(f"      [5/6] done in {time.time() - _t5:.1f}s", flush=True)

    # --- Step 5b: populate test_case_details (Custom.TestType per TC) ---
    # Reuses tc_fields_batch from Step 5 (same TC set) instead of a second
    # workitemsbatch fetch for identical data.
    unique_tc_ids = list(unique_tcs.keys())
    if unique_tc_ids:
        store.test_case_details.extend(
            populate_test_case_details(unique_tc_ids, client, cfg, prefetched_batch=tc_fields_batch)
        )

    # --- Step 5c: Acceptance Testing PO-approval email evidence (best-effort) ---
    # Heuristic only — see tda/collectors/po_approval.py module docstring for
    # why this can never definitively prove Product Owner identity. Only
    # examines TCs already classified as Acceptance Testing via Custom.TestType.
    acceptance_tc_ids = [
        d['TC Id'] for d in store.test_case_details
        if d.get('TC TestType') == 'Acceptance Testing'
    ]
    if acceptance_tc_ids:
        tc_to_run_result = {
            row['TestCase Id']: (row['Run Id'], row['Result Id'])
            for row in store.test_result_features
        }
        from tda.collectors.po_approval import analyze_po_approval_evidence
        store.po_approval_evidence.extend(
            analyze_po_approval_evidence(acceptance_tc_ids, tc_to_run_result, cfg, client)
        )

    # --- Step 6: write JSON ---
    print("  [6/6] Writing JSON output...", flush=True)
    _t6 = time.time()
    output_dir  = os.environ.get('TDA_OUTPUT_DIR', './AutoTDAReports')
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f'AutoTDAResults_{release_stream}_{release_id}.json')

    tda_output = store.to_tda_output(
        release_id, release_stream, blade_release_builds,
        pipeline_versions=resolved_pipeline_versions,
        collector_version=COLLECTOR_VERSION,
        ado_organization=cfg.ado_organization,
        ado_project=cfg.ado_project,
    )
    tda_output['skill_version_check'] = skill_version_check
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(tda_output, f, indent=2, default=str)

    summary_file = generate_summary(tda_output, output_dir, release_stream, release_id)

    _t_total = time.time() - _t_start
    print(f"      [6/6] done in {time.time() - _t6:.1f}s", flush=True)
    print()
    print(f"Full TDA data  : {output_file}")
    print(f"Compact summary: {summary_file}")
    print(f"Hand the summary file to the dtp-tda-report skill for faster analysis.")
    _mins, _secs = divmod(int(_t_total), 60)
    print(f"Total time: {_mins}m {_secs}s ({_t_total:.1f}s)")
    print()
    call_tracker.print_summary()


if __name__ == '__main__':
    main()
