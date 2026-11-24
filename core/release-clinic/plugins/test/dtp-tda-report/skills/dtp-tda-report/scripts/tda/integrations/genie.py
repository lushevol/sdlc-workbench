"""tda/integrations/genie.py — Genie regression scenario results integration."""

from __future__ import annotations

import logging
from collections import Counter, defaultdict

import requests

from tda.config import Config
from tda.http_client import ADOClient, call_with_retries
from tda.call_tracker import tracker as call_tracker


def get_genie_regression_failures(release_id: str,
                                  cfg: Config,
                                  client: ADOClient) -> tuple[dict, list, list, list, list]:
    """Fetch all Genie regression scenarios for this release.

    Returns:
        genie_count           — {'passed': N, 'failed': N}
        failed_scenarios      — [{'name': ..., 'status': ...}]
        tag_split             — [Counter dict of all tags]
        story_tag_split       — [Counter dict filtered to story-link tags]
        story_type_breakdown  — [{'Story WI Id': ..., 'Genie ST Scenarios': N,
                                   'Genie IT Scenarios': N, 'Genie Other Scenarios': N}, ...]
                                 Definitive per-story System Testing vs Integration Testing
                                 scenario counts, computed in this same scan (no extra API
                                 calls). Resolves the ambiguity in story_tag_split, which only
                                 records that a story had *some* ST/IT-tagged scenario without
                                 saying which type.
    """
    client.unset_proxy()
    genie_count = {'passed': 0, 'failed': 0}
    failed_scenarios: list[dict] = []
    master_tag_list: list[str] = []
    per_story_type: dict[str, Counter] = defaultdict(Counter)

    _headers = {"Authorization": f"Bearer {cfg.genie_token}"}
    url = f'{cfg.genie_report_link}?releaseName={release_id}'
    params: dict = {"scenarioIdToSearchAfter": ''}

    for _ in range(100):
        try:
            call_tracker.record('Genie')
            r = call_with_retries(
                lambda: requests.get(
                    url, params=params, headers=_headers, verify=False,
                    timeout=cfg.genie_timeout_seconds,
                ),
                what="getGenieRegressionFailures",
            )
            r.raise_for_status()
        except Exception as e:
            logging.warning("getGenieRegressionFailures: request failed — %s", e)
            break

        data = r.json()
        params['scenarioIdToSearchAfter'] = data.get('scenarioIdToSearchAfter')

        for fragment in data.get('fragments', []):
            name   = fragment['scenario']['name']
            status = fragment['result']['status']
            tags   = fragment.get('tags', [])

            is_st = bool(cfg.genie_st_tags.intersection(tags))
            is_it = bool(cfg.genie_it_tags.intersection(tags))

            if is_st or is_it:
                master_tag_list.extend(tags)

            story_ids = [t[len(cfg.genie_story_link_prefix):] for t in tags
                         if t.startswith(cfg.genie_story_link_prefix)
                         and t[len(cfg.genie_story_link_prefix):].isdigit()]
            for sid in story_ids:
                if is_st:
                    per_story_type[sid]['ST'] += 1
                if is_it:
                    per_story_type[sid]['IT'] += 1
                if not is_st and not is_it:
                    per_story_type[sid]['other'] += 1

            if status == 'passed':
                genie_count['passed'] += 1
            else:
                genie_count['failed'] += 1
                failed_scenarios.append({'name': name, 'status': status})

        if data.get('scenarioIdToSearchAfter') is None:
            break

    element_counts = dict(Counter(master_tag_list))
    story_tag_counts = {
        k: v for k, v in element_counts.items()
        if k.startswith(cfg.genie_story_link_prefix)
    }
    story_type_breakdown = [
        {
            'Story WI Id': sid,
            'Genie ST Scenarios': counts.get('ST', 0),
            'Genie IT Scenarios': counts.get('IT', 0),
            'Genie Other Scenarios': counts.get('other', 0),
        }
        for sid, counts in sorted(per_story_type.items(), key=lambda kv: int(kv[0]) if kv[0].isdigit() else 0)
    ]

    client.set_proxy()
    logging.info(
        "getGenieRegressionFailures: passed=%d failed=%d",
        genie_count['passed'], genie_count['failed'],
    )
    return genie_count, failed_scenarios, [element_counts], [story_tag_counts], story_type_breakdown
