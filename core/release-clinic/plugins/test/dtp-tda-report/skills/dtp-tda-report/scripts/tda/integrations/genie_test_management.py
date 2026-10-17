"""tda/integrations/genie_test_management.py — Genie "test-management" API.

An ALTERNATIVE regression-results source to tda/integrations/genie.py's
scenario-traceability API. Confirmed live (2026-08-04) against a real
release (KDB stream, appId 50285, RWI 12785595):

    GET https://report.genie.cloud.sc.net/api/test-management/
        applications/{application_id}/releases/{release_id}/test-results/_latest

Same Bearer auth (cfg.genie_token) and same "reach it directly, not through
the corporate proxy" pattern as tda/integrations/genie.py.

Response shape (confirmed for the all-PASSED case only — FAILED/other status
values not yet observed in real data):

    {
        "testCaseResults": [
            {
                "testResultId": ..., "testRunId": ..., "testPackId": ...,
                "testCaseId": ..., "name": ...,
                "status": "PASSED",           # only value confirmed so far
                "testType": "AUTOMATED",
                "runStartTime": ..., "runEndTime": ..., "runBy": ...,
                "runMetadata": {"release": ..., "applicationIds": [...], "labels": [...]},
                "requirementRefs": [<ADO Story WI id>, ...],
                "tags": ["@regression", ...],
            },
            ...
        ],
        "continuationTestCaseCursorToSearch": 200   # present when more pages exist
    }

PAGINATION — confirmed 2026-08-06. The next-page cursor is requested via
the GET query param ``testCaseCursorToSearch``, whose value is taken from
the *previous* page's ``continuationTestCaseCursorToSearch`` response field.
The first request omits the param entirely (no cursor yet). The loop
mirrors the `for _ in range(100): ...` pagination loop in
integrations/genie.py: keep requesting while the response keeps returning a
non-null `continuationTestCaseCursorToSearch`, stop once it comes back
null/absent. If a request fails partway through, the partial results
collected so far are kept and `genie_count['pagination_incomplete']` is set
so the truncation is never silently masked as a complete result.

Similarly, only `status == 'PASSED'` is confirmed — anything else (no
observed FAILED example yet) is conservatively treated as a failure below
rather than silently dropped.
"""

from __future__ import annotations

import logging
from collections import Counter, defaultdict

import requests

from tda.config import Config
from tda.http_client import ADOClient, call_with_retries
from tda.call_tracker import tracker as call_tracker


def get_test_management_regression_results(release_id: str,
                                           application_id: str,
                                           cfg: Config,
                                           client: ADOClient) -> tuple[dict, list, list, list, list]:
    """Fetch regression test-case results for this release from Genie's
    test-management API (single page only — see module docstring).

    ``application_id`` — the Genie/report application id (NOT necessarily
    the same value as the Release WI's Custom.ApplicationID field, which is
    a free-text ADO description like "RADARS BA-50736" — must come from an
    explicit per-stream ``genie_test_management_app_id`` in
    stream_config.yaml until the two are confirmed to be the same identifier).

    Returns the same 5-tuple shape as
    ``tda.integrations.genie.get_genie_regression_failures`` so callers
    (``tda/collectors/release.py``) don't need separate handling:

        genie_count           — {'passed', 'failed', 'total', 'genie_source',
                                  'pagination_incomplete'}
        failed_scenarios       — [{'name': ..., 'status': ...}]
        tag_split              — [Counter dict of all tags]
        story_tag_split         — [Counter dict of ADO story ids from requirementRefs]
        story_type_breakdown    — [{'Story WI Id', 'Genie ST Scenarios',
                                     'Genie IT Scenarios', 'Genie Other Scenarios'}, ...]
                                  ST/IT split is best-effort from cfg.genie_st_tags/
                                  genie_it_tags intersected with each result's own
                                  `tags` — the one confirmed real sample only carried
                                  a bare "@regression" tag (no @tt_ST/@tt_IT markers),
                                  so most/all stories will land in "Other" until real
                                  ST/IT-tagged data is observed.
    """
    client.unset_proxy()
    genie_count = {
        'passed': 0, 'failed': 0, 'total': 0,
        'genie_source': 'test_management_api',
        'pagination_incomplete': False,
    }
    failed_scenarios: list[dict] = []
    master_tag_list: list[str] = []
    per_story_type: dict[str, Counter] = defaultdict(Counter)

    url = cfg.genie_test_management_url_template.format(
        application_id=application_id, release_id=release_id
    )
    headers = {"Authorization": f"Bearer {cfg.genie_token}"}

    results: list[dict] = []
    cursor = None
    pages_fetched = 0

    for _ in range(100):
        params: dict = {}
        if cursor is not None:
            params['testCaseCursorToSearch'] = cursor

        try:
            call_tracker.record('Genie')
            r = call_with_retries(
                lambda: requests.get(
                    url, params=params, headers=headers, verify=False,
                    timeout=cfg.genie_timeout_seconds,
                ),
                what="getTestManagementRegressionResults",
            )
            r.raise_for_status()
            data = r.json()
        except Exception as e:
            logging.warning("getTestManagementRegressionResults: request failed — %s", e)
            if pages_fetched == 0:
                client.set_proxy()
                genie_count['genie_source'] = 'test_management_api_error'
                return genie_count, failed_scenarios, [dict(Counter())], [{}], []
            genie_count['pagination_incomplete'] = True
            print(
                "        [Genie Test-Management] ⚠️  Pagination request failed after "
                f"{pages_fetched} page(s) — totals below may be INCOMPLETE.",
                flush=True,
            )
            break

        results.extend(data.get('testCaseResults', []))
        pages_fetched += 1
        cursor = data.get('continuationTestCaseCursorToSearch')
        if cursor is None:
            break
    else:
        # Hit the 100-page safety cap while a cursor was still present.
        genie_count['pagination_incomplete'] = True
        logging.warning(
            "getTestManagementRegressionResults: hit the 100-page safety cap with more "
            "pages still remaining (cursor=%s) — totals below are INCOMPLETE.", cursor,
        )
        print(
            "        [Genie Test-Management] ⚠️  Hit 100-page safety cap — "
            "totals below may be INCOMPLETE.",
            flush=True,
        )

    for tc in results:
        name = tc.get('name', tc.get('testCaseId', ''))
        status = str(tc.get('status', '')).upper()
        tags = tc.get('tags', []) or []

        is_st = bool(cfg.genie_st_tags.intersection(tags))
        is_it = bool(cfg.genie_it_tags.intersection(tags))
        if is_st or is_it:
            master_tag_list.extend(tags)
        else:
            master_tag_list.extend(tags)

        story_ids = [str(ref) for ref in (tc.get('requirementRefs') or [])]
        for sid in story_ids:
            if is_st:
                per_story_type[sid]['ST'] += 1
            elif is_it:
                per_story_type[sid]['IT'] += 1
            else:
                per_story_type[sid]['other'] += 1

        if status == 'PASSED':
            genie_count['passed'] += 1
        else:
            genie_count['failed'] += 1
            failed_scenarios.append({'name': name, 'status': status or 'UNKNOWN'})

    genie_count['total'] = genie_count['passed'] + genie_count['failed']

    element_counts = dict(Counter(master_tag_list))
    story_tag_counts = {sid: sum(c.values()) for sid, c in per_story_type.items()}
    story_type_breakdown = [
        {
            'Story WI Id': sid,
            'Genie ST Scenarios': counts.get('ST', 0),
            'Genie IT Scenarios': counts.get('IT', 0),
            'Genie Other Scenarios': counts.get('other', 0),
        }
        for sid, counts in sorted(per_story_type.items(), key=lambda kv: (len(kv[0]), kv[0]))
    ]

    client.set_proxy()
    logging.info(
        "getTestManagementRegressionResults: passed=%d failed=%d pagination_incomplete=%s",
        genie_count['passed'], genie_count['failed'], genie_count['pagination_incomplete'],
    )
    return genie_count, failed_scenarios, [element_counts], [story_tag_counts], story_type_breakdown
