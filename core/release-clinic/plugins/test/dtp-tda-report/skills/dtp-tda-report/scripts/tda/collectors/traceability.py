"""tda/collectors/traceability.py — Test case ↔ story WI traceability collection.

Discovers which test cases are linked to each story WI and records per-TC
evidence for the traceability matrix.

Thread safety: a module-level lock protects the shared ``unique_test_cases``
dict when running parallel fan-outs (PARALLEL_ENABLED=true).
"""

from __future__ import annotations

import logging
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any

from tda.config import Config
from tda.http_client import ADOClient


_unique_tc_lock = threading.Lock()


# ---------------------------------------------------------------------------
# Low-level helpers
# ---------------------------------------------------------------------------

def get_test_cases_for_work_item(work_item_id: str, client: ADOClient) -> list[dict]:
    """Return the list of test cases linked to a single WI via TestedBy.

    The ADO endpoint returns a single work item object (not a value array).
    We filter its ``relations`` for the "TestedBy" rel attribute, which links
    to Test Case work items.
    """
    try:
        r = client.get('TestCasesForWorkItem', work_item_id)
        wi = r.json()
        relations = wi.get('relations') or []
        test_cases = []
        for rel in relations:
            # Relation type for "Tested By" is "Microsoft.VSTS.Common.TestedBy-Forward"
            rel_type = rel.get('rel', '')
            if 'TestedBy' in rel_type:
                url = rel.get('url', '')
                # Extract TC ID from the URL (last path segment)
                tc_id = url.rstrip('/').split('/')[-1]
                if tc_id.isdigit():
                    test_cases.append({'id': int(tc_id), 'webUrl': url})
        return test_cases
    except Exception as e:
        logging.warning("get_test_cases_for_work_item: WI %s — %s", work_item_id, e)
        return []


# ---------------------------------------------------------------------------
# Per-story traceability
# ---------------------------------------------------------------------------

def get_test_case_details(
    test_cases: list[dict],
    story_item: dict,
    release_id: str,
    cfg: Config,
    client: ADOClient,
    unique_test_cases: dict,
    tc_fields_batch: dict,
) -> list[dict]:
    """Collect traceability facts for one story's test cases.

    ``tc_fields_batch`` is a pre-fetched ``{tc_id: work_item_dict}`` map (from
    ``ADOClient.fetch_work_items_batch``) covering every unique TC referenced
    across all stories in this release. Title/State/Priority/Automated status
    are read from this batch instead of issuing an individual
    ``WorkItemsForRelease`` call per story-TC pair — previously the same TC's
    fields were re-fetched once per story it was linked to (e.g. a TC shared
    across 3 stories triggered 3 identical field fetches).

    Mutates ``unique_test_cases`` in-place (thread-safe via ``_unique_tc_lock``).
    Returns a list of traceability row dicts for the story.
    """
    rows: list[dict] = []
    story_id = story_item['WI Id']

    for tc in test_cases:
        tc_id  = str(tc.get('id', ''))
        tc_ref = str(tc.get('webUrl', ''))

        row: dict[str, Any] = {
            'Story WI Id':   story_id,
            'Story Title':   story_item['WI Title'],
            'TC Id':         tc_id,
            'TC Title':      '',
            'TC State':      '',
            'TC Priority':   '',
            'TC Automated':  '',
            'TC URL':        tc_ref,
            'Run Outcome':   '',
            'Evidence':      '',
        }

        # TC work item fields — from the pre-fetched batch (no per-TC ADO call)
        f = tc_fields_batch.get(tc_id, {}).get('fields', {})
        if f:
            row['TC Title']     = f.get('System.Title', '')
            row['TC State']     = f.get('System.State', '')
            row['TC Priority']  = f.get('Microsoft.VSTS.Common.Priority', '')
            row['TC Automated'] = f.get('Microsoft.VSTS.TCM.AutomationStatus', '')
        else:
            logging.warning("get_test_case_details: TC %s missing from batch fetch", tc_id)

        # Fetch latest run / evidence via the per-TC result approach (test-plans API).
        # No batch API exists for test results, so this remains a per-TC call.
        try:
            res_resp = client.get2('TestResultsForTestCase', release_id, tc_id)
            run_values = res_resp.json().get('value', [])
            if run_values:
                latest = run_values[-1]
                row['Run Outcome'] = latest.get('outcome', '')
                result_detail = client.get2(
                    'TestResultById',
                    str(latest.get('runId', '')),
                    str(latest.get('resultId', '')),
                )
                row['Evidence'] = result_detail.json().get('comment', '')
        except Exception as e:
            logging.warning("get_test_case_details: TC %s run — %s", tc_id, e)

        rows.append(row)

        # Register in the shared unique TC pool
        with _unique_tc_lock:
            if tc_id not in unique_test_cases:
                unique_test_cases[tc_id] = {
                    'TC Id':       tc_id,
                    'TC Title':    row['TC Title'],
                    'TC State':    row['TC State'],
                    'Linked WIs':  [story_id],
                }
            else:
                if story_id not in unique_test_cases[tc_id]['Linked WIs']:
                    unique_test_cases[tc_id]['Linked WIs'].append(story_id)

    return rows


# ---------------------------------------------------------------------------
# Parallel fan-out across all story items
# ---------------------------------------------------------------------------

def build_traceability(story_features: list[dict],
                        release_id: str,
                        cfg: Config,
                        client: ADOClient) -> tuple[list[dict], dict, dict]:
    """Fan out across all story WIs and collect TC traceability data.

    Three phases — avoids redundant per-TC field fetches:
      1. Discover which TCs are linked to each story (``TestCasesForWorkItem``,
         1 call/story — no batch equivalent exists for relation traversal).
      2. Batch-fetch WI fields (Title/State/Priority/Automated/TestType) for
         every UNIQUE TC across all stories in a single ``workitemsbatch`` call,
         instead of re-fetching the same TC's fields once per story it is
         linked to.
      3. Build traceability rows from that batch. Per-TC run outcome/evidence
         still requires an individual call — no batch API exists for test
         results — so that part is unchanged.

    Returns:
        traceability      — flat list of row dicts (one row per story-TC pair)
        unique_test_cases — dict keyed by TC ID
        tc_fields_batch   — {tc_id: work_item_dict} batch result, reusable by
                             populate_test_case_details() to avoid a second
                             identical batch call for the same TC set.
    """
    traceability: list[dict] = []
    unique_test_cases: dict  = {}

    # --- Phase 1: discover linked TCs per story ---
    story_tcs: dict[str, list[dict]] = {}
    if cfg.parallel_enabled:
        with ThreadPoolExecutor(max_workers=5) as ex:
            futures = {
                ex.submit(get_test_cases_for_work_item, s['WI Id'], client): s
                for s in story_features
            }
            for fut in as_completed(futures):
                story = futures[fut]
                try:
                    story_tcs[story['WI Id']] = fut.result()
                except Exception as e:
                    logging.warning(
                        "build_traceability: TC discovery for story %s failed — %s",
                        story.get('WI Id', '?'), e,
                    )
                    story_tcs[story['WI Id']] = []
    else:
        for s in story_features:
            story_tcs[s['WI Id']] = get_test_cases_for_work_item(s['WI Id'], client)

    # --- Phase 2: one batch fetch for every unique TC referenced above ---
    all_tc_ids = sorted({
        str(tc['id']) for tcs in story_tcs.values() for tc in tcs if tc.get('id') is not None
    })
    tc_fields_batch = client.fetch_work_items_batch(all_tc_ids) if all_tc_ids else {}

    # Filter out any "Tested By" linked WIs that are not actually Test Cases.
    # ADO allows the "Tested By" link type to be applied to any WI type, so
    # non-TC items (e.g. User Stories, Tasks) can appear here and must be ignored.
    if tc_fields_batch:
        tc_only_ids = {
            tid for tid, wi in tc_fields_batch.items()
            if wi.get('fields', {}).get('System.WorkItemType', '').lower() == 'test case'
        }
        excluded_ids = set(tc_fields_batch.keys()) - tc_only_ids
        if excluded_ids:
            logging.warning(
                "build_traceability: ignoring %d 'Tested By' linked WI(s) that are not "
                "Test Cases (WI types will differ): %s",
                len(excluded_ids), ", ".join(sorted(excluded_ids)),
            )
        # Strip non-TC entries from both story_tcs and the batch so Phase 3
        # never processes or makes run/evidence calls for them.
        story_tcs = {
            sid: [tc for tc in tcs if str(tc.get('id', '')) in tc_only_ids]
            for sid, tcs in story_tcs.items()
        }
        tc_fields_batch = {k: v for k, v in tc_fields_batch.items() if k in tc_only_ids}

    # --- Phase 3: build traceability rows (still needs per-TC run/evidence call) ---
    def _process_story(story_item: dict) -> list[dict]:
        story_id = story_item['WI Id']
        tcs = story_tcs.get(story_id, [])
        return get_test_case_details(
            tcs, story_item, release_id, cfg, client, unique_test_cases, tc_fields_batch
        )

    if cfg.parallel_enabled:
        with ThreadPoolExecutor(max_workers=5) as ex:
            futures = {ex.submit(_process_story, s): s for s in story_features}
            for fut in as_completed(futures):
                try:
                    traceability.extend(fut.result())
                except Exception as e:
                    story = futures[fut]
                    logging.warning(
                        "build_traceability: story %s failed — %s",
                        story.get('WI Id', '?'), e,
                    )
    else:
        for story_item in story_features:
            traceability.extend(_process_story(story_item))

    return traceability, unique_test_cases, tc_fields_batch
