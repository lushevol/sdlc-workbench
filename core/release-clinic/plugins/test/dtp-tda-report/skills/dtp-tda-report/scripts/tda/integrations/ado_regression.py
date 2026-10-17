"""tda/integrations/ado_regression.py â€” ADO-native regression results integration.

Used for streams that do NOT use Genie (genie_enabled=False) but publish their
regression/automation test results to ADO via the Publish Test Results task or
a custom API.  Results appear in the build's "Tests" tab.

Returns the same tuple shape as genie.py so the rest of the pipeline
(result_store, summariser, SKILL) requires no changes:

    (count_dict, failed_scenarios, tag_split, story_tag_split, story_type_breakdown)

The 'genie_source' key is injected into count_dict so the SKILL can annotate
the source correctly.

API flow
--------
For each build_id in build_ids:
  1. GET test/runs?buildId={build_id}&$top=1000  -> all test runs on the build
  2. Filter runs by regression_run_filter        -> keep only regression runs
  3. Read pass/fail counts from the inline payload (includeRunDetails=true).
     Falls back to GET test/runs/{runId}/statistics only when totals are zero.
  4. For failed runs: GET test/runs/{runId}/results -> individual failure names

Results are aggregated across all builds.
"""

from __future__ import annotations

import logging
import time

import requests

from tda.config import Config
from tda.http_client import ADOClient

logger = logging.getLogger(__name__)

# Timeout for the initial test/runs list call per build.
# The ADO test/runs endpoint can be very slow for large builds; a short
# timeout lets us skip unresponsive builds gracefully instead of hanging.
_RUNS_LIST_TIMEOUT = 20   # seconds — raise in stream_config.yaml if needed

# Timeout for per-run statistics / results calls (smaller payloads).
_RUN_DETAIL_TIMEOUT = 30  # seconds


def _ts() -> str:
    """Return a compact HH:MM:SS timestamp string for log lines."""
    return time.strftime('%H:%M:%S')


def _timed_get(client: ADOClient, url: str, label: str, timeout: int = _RUN_DETAIL_TIMEOUT) -> object:
    """Call client.raw_get with a timeout, printing before/after timing."""
    print(f"        [ADO Regression] {_ts()} -> GET {label}  (timeout={timeout}s)", flush=True)
    t0 = time.time()
    resp = client.raw_get(url, timeout=timeout)
    elapsed = time.time() - t0
    print(f"        [ADO Regression] {_ts()} <- {label}  [{elapsed:.1f}s, HTTP {resp.status_code}]",
          flush=True)
    return resp


def _collect_runs_for_build(
    build_id: str,
    pipeline_name: str,
    base_url: str,
    client: ADOClient,
    filter_lower: str,
    regression_run_filter: str,
) -> list[dict]:
    """Return the filtered list of test-run dicts for a single build.

    Returns an empty list on any error so the caller can continue to the
    next build without aborting the whole collection.
    """
    label = f'test/runs?buildId={build_id} ({pipeline_name})'
    url   = (
        f'{base_url}/test/runs'
        f'?buildId={build_id}'
        f'&includeRunDetails=true'
        f'&$top=1000'
        f'&api-version=7.1'
    )
    try:
        resp = _timed_get(client, url, label, timeout=_RUNS_LIST_TIMEOUT)
        resp.raise_for_status()
        all_runs = resp.json().get('value', [])
    except requests.exceptions.Timeout:
        print(
            f"        [ADO Regression] ⚠️  build {build_id} ({pipeline_name}): "
            f"timed out after {_RUNS_LIST_TIMEOUT}s — skipping. "
            "(This build may not publish test results to ADO, or the API is slow.)",
            flush=True,
        )
        return []
    except Exception as exc:
        logger.warning("ado_regression: failed to fetch runs for build %s â€” %s", build_id, exc)
        print(f"        [ADO Regression] âš ï¸  Skipping build {build_id} ({pipeline_name}): {exc}",
              flush=True)
        return []

    if not all_runs:
        print(f"        [ADO Regression] build {build_id} ({pipeline_name}): 0 test runs â€” skipping.",
              flush=True)
        return []

    if filter_lower:
        filtered = [r for r in all_runs if filter_lower in r.get('name', '').lower()]
        print(
            f"        [ADO Regression] build {build_id}: {len(all_runs)} run(s), "
            f"{len(filtered)} matched filter '{regression_run_filter}'.",
            flush=True,
        )
    else:
        filtered = all_runs
        names = ', '.join(f"'{r.get('name', '?')}'" for r in all_runs[:5])
        suffix = f' â€¦ (+{len(all_runs) - 5} more)' if len(all_runs) > 5 else ''
        print(
            f"        [ADO Regression] build {build_id}: {len(all_runs)} run(s): {names}{suffix}",
            flush=True,
        )

    return filtered


def get_ado_regression_results(
    build_ids: dict[str, str],
    cfg: Config,
    client: ADOClient,
    regression_run_filter: str = "",
) -> tuple[dict, list, list, list, list]:
    """Fetch ADO-published regression test results across all associated builds.

    Args:
        build_ids:             {pipeline_name: build_id} for all builds associated
                               with the release.  All are queried and results
                               aggregated â€” builds with 0 test runs are skipped.
        cfg:                   TDA Config (for ADO auth).
        client:                ADOClient instance.
        regression_run_filter: Case-insensitive substring to filter run names.
                               Empty string = include ALL test runs on the build.
                               Example: "Regression" keeps only runs whose name
                               contains "Regression".

    Returns:
        count_dict            â€” {'passed': N, 'failed': N, 'total': N,
                                'genie_source': 'ado', 'runs_collected': N,
                                'builds_with_runs': N, 'run_filter': str}
        failed_scenarios      â€” [{'name': str, 'status': str, 'run_name': str,
                                'build_id': str}]
        tag_split             â€” [] (no tag data available from ADO runs)
        story_tag_split       â€” [] (no tag data available from ADO runs)
        story_type_breakdown  â€” [] (no per-story ST/IT scenario data available from ADO runs)
    """
    count_dict: dict = {
        'passed': 0,
        'failed': 0,
        'total': 0,
        'genie_source': 'ado',
        'runs_collected': 0,
        'builds_with_runs': 0,
        'run_filter': regression_run_filter or '(all runs)',
    }
    failed_scenarios: list[dict] = []

    base = client.cfg.ado_base_url.rstrip('/')
    filter_lower = regression_run_filter.lower()

    print(
        f"        [ADO Regression] Querying {len(build_ids)} build(s): "
        + ', '.join(f"{pid}={bid}" for pid, bid in build_ids.items()),
        flush=True,
    )

    for pipeline_name, build_id in build_ids.items():
        target_runs = _collect_runs_for_build(
            build_id, pipeline_name, base, client, filter_lower, regression_run_filter
        )
        if not target_runs:
            continue

        count_dict['builds_with_runs'] += 1

        # --- per-run statistics ---
        for idx, run in enumerate(target_runs, 1):
            run_id   = str(run.get('id', ''))
            run_name = run.get('name', f'Run {run_id}')

            print(
                f"        [ADO Regression] [{pipeline_name}] Run {idx}/{len(target_runs)}: "
                f"'{run_name}' (id={run_id})",
                flush=True,
            )

            # Prefer inline counts from includeRunDetails=true
            run_passed = run.get('passedTests', 0) or 0
            run_total  = run.get('totalTests', 0) or 0
            run_failed = max(
                run_total
                - run_passed
                - (run.get('notApplicableTests', 0) or 0)
                - (run.get('incompleteTests', 0) or 0),
                0,
            )

            # Fallback: statistics endpoint when inline totals are absent
            if run_total == 0:
                print(
                    f"        [ADO Regression] Inline counts missing â€” fetching statistics...",
                    flush=True,
                )
                try:
                    stats_url  = f'{base}/test/runs/{run_id}/statistics?api-version=7.1'
                    stats_resp = _timed_get(client, stats_url,
                                           f'test/runs/{run_id}/statistics',
                                           timeout=_RUN_DETAIL_TIMEOUT)
                    stats_resp.raise_for_status()
                    for stat in stats_resp.json().get('runStatistics', []):
                        outcome = stat.get('outcome', '').lower()
                        cnt     = stat.get('count', 0) or 0
                        if outcome == 'passed':
                            run_passed += cnt
                        elif outcome in ('failed', 'error'):
                            run_failed += cnt
                        run_total += cnt
                except Exception as exc:
                    logger.warning(
                        "ado_regression: stats fetch failed for run %s â€” %s", run_id, exc
                    )
                    print(
                        f"        [ADO Regression] âš ï¸  Statistics unavailable for run {run_id}: {exc}",
                        flush=True,
                    )

            count_dict['passed']         += run_passed
            count_dict['failed']         += run_failed
            count_dict['total']          += run_total
            count_dict['runs_collected'] += 1

            print(
                f"        [ADO Regression] â””â”€ passed={run_passed} failed={run_failed} "
                f"total={run_total}  "
                f"[cumulative: passed={count_dict['passed']} "
                f"failed={count_dict['failed']} total={count_dict['total']}]",
                flush=True,
            )

            # Fetch individual failure names
            if run_failed > 0:
                results_url = f'{base}/test/Runs/{run_id}/results?api-version=7.1'
                try:
                    res_resp = _timed_get(client, results_url,
                                         f'test/Runs/{run_id}/results (failures)',
                                         timeout=_RUN_DETAIL_TIMEOUT)
                    res_resp.raise_for_status()
                    for result in res_resp.json().get('value', []):
                        outcome = result.get('outcome', '').lower()
                        if outcome in ('failed', 'error', 'aborted'):
                            failed_scenarios.append({
                                'name':     result.get('testCaseTitle',
                                                       result.get('automatedTestName',
                                                                  'Unknown')),
                                'status':   outcome,
                                'run_name': run_name,
                                'build_id': build_id,
                            })
                    print(
                        f"        [ADO Regression] {len(failed_scenarios)} total failure(s) so far.",
                        flush=True,
                    )
                except Exception as exc:
                    logger.warning(
                        "ado_regression: could not fetch failure details for run %s â€” %s",
                        run_id, exc,
                    )
                    print(
                        f"        [ADO Regression] âš ï¸  Failure details unavailable for run "
                        f"{run_id}: {exc}",
                        flush=True,
                    )

    print(
        f"        [ADO Regression] âœ… Complete. "
        f"passed={count_dict['passed']} failed={count_dict['failed']} "
        f"total={count_dict['total']} runs={count_dict['runs_collected']} "
        f"builds_with_runs={count_dict['builds_with_runs']}/{len(build_ids)}",
        flush=True,
    )

    return count_dict, failed_scenarios, [], [], []

