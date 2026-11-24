"""tda/integrations/sonar.py — SonarQube coverage metrics integration."""

from __future__ import annotations

import logging

import requests
from sonarqube import SonarQubeClient

from tda.config import Config
from tda.http_client import ADOClient, call_with_retries
from tda.call_tracker import tracker as call_tracker

_METRICS = [
    'coverage', 'lines_to_cover', 'uncovered_lines', 'line_coverage', 'branch_coverage',
    'new_coverage', 'new_lines_to_cover', 'new_uncovered_lines',
    'new_line_coverage', 'new_branch_coverage',
]


def get_coverage_metrics(pipeline_name: str, sonar_project: str,
                         branch_name: str,
                         cfg: Config, client: ADOClient) -> dict | None:
    """Fetch Sonar coverage metrics for one pipeline.

    Returns the metrics dict (with 'Pipeline' key) on success, or None on failure.
    The caller is responsible for appending the result to the result store.
    """
    sonar = SonarQubeClient(sonarqube_url=cfg.sonar_url, token=cfg.sonar_token, verify=False)
    client.unset_proxy()
    try:
        call_tracker.record('Sonar')
        response = call_with_retries(
            lambda: sonar.measures.get_component_with_specified_measures(
                component=sonar_project,
                branch=branch_name,
                metricKeys=','.join(_METRICS),
            ),
            what=f"get_coverage_metrics[{pipeline_name}]",
        )
        measures = response['component']['measures']
        coverage_metrics: dict = {metric: None for metric in _METRICS}
        for measure in measures:
            metric = measure.get('metric')
            value = (
                measure['period'].get('value')
                if 'period' in measure
                else measure.get('value')
            )
            if metric in coverage_metrics:
                coverage_metrics[metric] = value
        coverage_metrics['Pipeline'] = pipeline_name
        logging.info(
            "get_coverage_metrics: OK pipeline=%s project=%s branch=%s",
            pipeline_name, sonar_project, branch_name,
        )
        return coverage_metrics
    except Exception as e:
        logging.warning(
            "get_coverage_metrics: FAILED pipeline=%s project=%s branch=%s — %s",
            pipeline_name, sonar_project, branch_name, e,
        )
        print(f"        [Sonar] Skipping {pipeline_name} ({sonar_project}@{branch_name}): {e}")
        return None
    finally:
        client.set_proxy()


def get_quality_gate_name(pipeline_name: str, sonar_project: str,
                          cfg: Config, client: ADOClient) -> dict | None:
    """Fetch the SonarQube Quality Gate assigned to one project.

    Calls GET /api/qualitygates/get_by_project directly (the python-sonarqube-api
    SDK is used for coverage metrics elsewhere in this module, but this endpoint
    is queried with a plain requests call for a predictable response shape).

    Returns a dict with 'Pipeline', 'quality_gate_name', 'is_default' on
    success, or None on failure (project key not found, API error, etc — the
    caller should treat None the same way it treats a missing coverage entry).
    """
    client.unset_proxy()
    try:
        call_tracker.record('Sonar')
        response = call_with_retries(
            lambda: requests.get(
                f"{cfg.sonar_url.rstrip('/')}/api/qualitygates/get_by_project",
                params={'project': sonar_project},
                auth=(cfg.sonar_token, ''),
                verify=False,
                timeout=20,
            ),
            what=f"get_quality_gate_name[{pipeline_name}]",
        )
        response.raise_for_status()
        gate = response.json().get('qualityGate', {})
        result = {
            'Pipeline': pipeline_name,
            'quality_gate_name': gate.get('name'),
            'is_default': gate.get('default', False),
        }
        logging.info(
            "get_quality_gate_name: OK pipeline=%s project=%s gate=%s",
            pipeline_name, sonar_project, result['quality_gate_name'],
        )
        return result
    except Exception as e:
        logging.warning(
            "get_quality_gate_name: FAILED pipeline=%s project=%s — %s",
            pipeline_name, sonar_project, e,
        )
        print(f"        [Sonar] Quality gate lookup failed for {pipeline_name} ({sonar_project}): {e}")
        return None
    finally:
        client.set_proxy()


def get_new_code_period(pipeline_name: str, sonar_project: str,
                        branch_name: str,
                        cfg: Config, client: ADOClient) -> dict | None:
    """Fetch the authoritative New Code Period actually applied at last analysis.

    Calls GET /api/measures/component with additionalFields=period. This is
    deliberately NOT /api/new_code_periods/show — that endpoint requires
    project 'Administer' permission and returns 403 for the read-only token
    this collector uses. /api/measures/component only requires 'Browse' /
    'Execute Analysis' (the same tier already proven to work for the coverage
    metrics call below), and its `period` field reflects the period that was
    actually applied during the branch's last analysis — arguably even more
    authoritative than the static project-settings lookup.

    This lets the report distinguish between two genuinely different root causes
    of a null/missing `new_coverage` measure, instead of always assuming a missing
    `newCodeReferenceBranch` configuration:

      - `type == 'REFERENCE_BRANCH'`: a reference branch IS configured (its name is
        in `value`) — so a null/zero new_coverage most likely means there were no
        new coverable lines relative to that branch (e.g. a config-only or
        non-code change), not a missing-configuration problem.
      - `type` is one of `'PREVIOUS_VERSION'`, `'NUMBER_OF_DAYS'`, `'SPECIFIC_ANALYSIS'`,
        or the lookup fails entirely (branch not analyzed yet, API error, older
        SonarQube instance without this API): no reference branch is configured —
        the existing "configure newCodeReferenceBranch" CRITICAL finding is the
        correct diagnosis.

    Returns a dict with 'Pipeline', 'type', 'value', 'date' on success, or None
    on failure (the caller should treat None the same way it treats a missing
    coverage/quality-gate entry — fall back to the pre-existing wording).
    """
    client.unset_proxy()
    try:
        call_tracker.record('Sonar')
        response = call_with_retries(
            lambda: requests.get(
                f"{cfg.sonar_url.rstrip('/')}/api/measures/component",
                params={
                    'component': sonar_project,
                    'branch': branch_name,
                    'metricKeys': 'ncloc',
                    'additionalFields': 'period',
                },
                auth=(cfg.sonar_token, ''),
                verify=False,
                timeout=20,
            ),
            what=f"get_new_code_period[{pipeline_name}]",
        )
        response.raise_for_status()
        period = response.json().get('period', {})
        result = {
            'Pipeline': pipeline_name,
            'type':     period.get('mode'),
            'value':    period.get('parameter'),
            'date':     period.get('date'),
        }
        logging.info(
            "get_new_code_period: OK pipeline=%s project=%s branch=%s type=%s value=%s",
            pipeline_name, sonar_project, branch_name, result['type'], result['value'],
        )
        return result
    except Exception as e:
        logging.warning(
            "get_new_code_period: FAILED pipeline=%s project=%s branch=%s — %s",
            pipeline_name, sonar_project, branch_name, e,
        )
        print(f"        [Sonar] New code period lookup failed for {pipeline_name} ({sonar_project}@{branch_name}): {e}")
        return None
    finally:
        client.set_proxy()


_EXCLUSION_KEYS = [
    'sonar.exclusions',
    'sonar.coverage.exclusions',
    'sonar.test.exclusions',
    'sonar.cpd.exclusions',
]


def get_project_exclusions(pipeline_name: str, sonar_project: str,
                           cfg: Config, client: ADOClient) -> dict | None:
    """Fetch the configured exclusion patterns for one SonarQube project.

    Calls GET /api/settings/values directly (same plain-requests pattern as
    get_quality_gate_name) for the four exclusion-related settings:
    sonar.exclusions, sonar.coverage.exclusions, sonar.test.exclusions,
    sonar.cpd.exclusions.

    Returns a dict with 'Pipeline' plus one key per exclusion setting (each a
    list of patterns, empty if not configured) on success, or None on failure.
    """
    client.unset_proxy()
    try:
        call_tracker.record('Sonar')
        response = call_with_retries(
            lambda: requests.get(
                f"{cfg.sonar_url.rstrip('/')}/api/settings/values",
                params={'component': sonar_project, 'keys': ','.join(_EXCLUSION_KEYS)},
                auth=(cfg.sonar_token, ''),
                verify=False,
                timeout=20,
            ),
            what=f"get_project_exclusions[{pipeline_name}]",
        )
        response.raise_for_status()
        settings = response.json().get('settings', [])
        result = {'Pipeline': pipeline_name}
        for key in _EXCLUSION_KEYS:
            result[key] = []
        for setting in settings:
            key = setting.get('key')
            if key in result:
                result[key] = setting.get('values', [])
        logging.info(
            "get_project_exclusions: OK pipeline=%s project=%s exclusions=%s",
            pipeline_name, sonar_project,
            {k: v for k, v in result.items() if k != 'Pipeline' and v},
        )
        return result
    except Exception as e:
        logging.warning(
            "get_project_exclusions: FAILED pipeline=%s project=%s — %s",
            pipeline_name, sonar_project, e,
        )
        print(f"        [Sonar] Exclusions lookup failed for {pipeline_name} ({sonar_project}): {e}")
        return None
    finally:
        client.set_proxy()


def get_quality_gate_status(pipeline_name: str, sonar_project: str,
                            branch_name: str,
                            cfg: Config, client: ADOClient) -> dict | None:
    """Fetch the Quality Gate pass/fail status for a project + branch.

    Calls GET /api/qualitygates/project_status — a separate endpoint from
    get_quality_gate_name (which only returns the gate's configured name).

    Response shape (SonarQube 9+):
      {
        "projectStatus": {
          "status":     "OK" | "WARN" | "ERROR" | "NONE",
          "conditions": [
            {"status": "OK"|"ERROR", "metricKey": "...", "actualValue": "...",
             "errorThreshold": "...", "comparator": "..."},
            ...
          ]
        }
      }

    Returns a dict with:
      - 'Pipeline':   pipeline_name
      - 'status':     "OK" | "WARN" | "ERROR" | "NONE" | None
      - 'conditions': list of condition dicts (each: metricKey, status,
                      actualValue, errorThreshold) — only failed conditions
                      (status != "OK") are retained to keep output concise
    or None on failure.
    """
    client.unset_proxy()
    try:
        call_tracker.record('Sonar')
        response = call_with_retries(
            lambda: requests.get(
                f"{cfg.sonar_url.rstrip('/')}/api/qualitygates/project_status",
                params={'projectKey': sonar_project, 'branch': branch_name},
                auth=(cfg.sonar_token, ''),
                verify=False,
                timeout=20,
            ),
            what=f"get_quality_gate_status[{pipeline_name}]",
        )
        response.raise_for_status()
        project_status = response.json().get('projectStatus', {})
        status = project_status.get('status')          # "OK", "ERROR", "WARN", "NONE"
        all_conditions = project_status.get('conditions', [])
        # Keep only the failed/warning conditions to avoid verbose output
        failed_conditions = [
            {
                'metricKey':      c.get('metricKey'),
                'status':         c.get('status'),
                'actualValue':    c.get('actualValue'),
                'errorThreshold': c.get('errorThreshold'),
                'comparator':     c.get('comparator'),
            }
            for c in all_conditions
            if c.get('status', 'OK') != 'OK'
        ]
        result = {
            'Pipeline':   pipeline_name,
            'status':     status,
            'conditions': failed_conditions,
        }
        logging.info(
            "get_quality_gate_status: OK pipeline=%s project=%s branch=%s status=%s failed_conditions=%d",
            pipeline_name, sonar_project, branch_name, status, len(failed_conditions),
        )
        return result
    except Exception as e:
        logging.warning(
            "get_quality_gate_status: FAILED pipeline=%s project=%s branch=%s — %s",
            pipeline_name, sonar_project, branch_name, e,
        )
        print(f"        [Sonar] Quality gate status failed for {pipeline_name} ({sonar_project}@{branch_name}): {e}")
        return None
    finally:
        client.set_proxy()
