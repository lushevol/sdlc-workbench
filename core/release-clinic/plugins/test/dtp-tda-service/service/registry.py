"""service/registry.py — Append-only job history registry for portfolio analysis.

Every completed (or failed) TDA collection job appends one compact JSON line
to a JSONL registry file. This is a lightweight, durable substitute for
JobStore (which is in-memory only and lost on restart) — it exists purely so
that a separate offline aggregator (scripts/aggregate_portfolio.py) can later
compute cross-release/cross-stream trends (recurring Genie failures, fragile
stories, Sonar quality-gate mismatches, etc.) without re-parsing every full
AutoTDAResults JSON file.

This module intentionally extracts only RAW/STRUCTURAL facts already present
in the collected data (counts, pass/fail totals, field-completeness, quality
gate names). It does NOT duplicate any of dtp-tda-report/SKILL.md's judgement
based analysis rules (severity classification, gate verdicts, etc.) — trend
computation over these raw facts happens in the aggregator script, which is
run separately by admins.

Thread-safe: safe to call from any ThreadPoolExecutor worker thread. Registry
write failures are logged but never raised — a registry problem must never
fail the underlying job.
"""

from __future__ import annotations

import json
import logging
import os
import threading
from datetime import datetime
from typing import Any, Optional

logger = logging.getLogger(__name__)

_lock = threading.Lock()


# ---------------------------------------------------------------------------
# Path resolution
# ---------------------------------------------------------------------------

def registry_path(output_dir: str) -> str:
    """Resolve the registry file path.

    ``TDA_REGISTRY_PATH`` overrides the default location, which is
    ``<output_dir>/tda_job_registry.jsonl``.
    """
    override = os.environ.get("TDA_REGISTRY_PATH", "").strip()
    if override:
        return override
    return os.path.join(output_dir, "tda_job_registry.jsonl")


def _iso(dt: Optional[datetime]) -> Optional[str]:
    return dt.isoformat() if dt else None


# ---------------------------------------------------------------------------
# Record builders
# ---------------------------------------------------------------------------

def build_success_record(job_id: str, request: Any, tda_output: dict,
                          submitted_at: Optional[datetime], started_at: Optional[datetime],
                          completed_at: Optional[datetime], result_path: str) -> dict:
    """Extract compact, aggregator-friendly facts from a completed job's tda_output."""
    story_features = tda_output.get('story_features') or []
    test_results   = tda_output.get('test_result_features') or []
    genie_counts   = tda_output.get('genie_count') or []
    genie_count    = genie_counts[0] if genie_counts else {}
    genie_failures = tda_output.get('genie_failures') or []
    sonar_gates    = tda_output.get('sonar_quality_gates') or []
    unit_tests     = tda_output.get('unit_tests') or []
    release_feats  = tda_output.get('release_features') or []
    release_checks = release_feats[0] if release_feats else {}
    snow_feats     = tda_output.get('snow_features') or []
    snow_checks    = snow_feats[0] if snow_feats else {}

    missing_app_id_ids = [
        s.get('WI Id') for s in story_features if not str(s.get('WI App Id', '')).strip()
    ]
    missing_story_type_ids = [
        s.get('WI Id') for s in story_features if not str(s.get('Automated', '')).strip()
    ]

    genie_passed = genie_count.get('passed', 0)
    genie_failed = genie_count.get('failed', 0)
    genie_total  = genie_passed + genie_failed

    non_standard_gates = [
        g for g in sonar_gates
        if str(g.get('quality_gate_name', '')).strip().lower() != 'esdlc-sonarway-managed'
    ]

    duration = None
    if started_at and completed_at:
        duration = (completed_at - started_at).total_seconds()

    flags = getattr(request, 'flags', None)

    return {
        'schema_version':  1,
        'job_id':          job_id,
        'release_id':      getattr(request, 'release_id', None),
        'release_stream':  (getattr(request, 'stream', '') or '').upper(),
        'build_id':        getattr(request, 'build_id', None),
        'release_version': getattr(request, 'release_version', '') or '',
        'rwi_only':        bool(getattr(flags, 'rwi_only', False)) if flags else False,
        'status':          'complete',
        'error':           None,
        'submitted_at':    _iso(submitted_at),
        'started_at':      _iso(started_at),
        'completed_at':    _iso(completed_at),
        'duration_seconds': duration,
        'result_path':     result_path,
        'counts': {
            'stories':             len(story_features),
            'bugs':                len(tda_output.get('bug_features') or []),
            'test_results':        len(test_results),
            'test_results_failed': sum(
                1 for t in test_results
                if str(t.get('Outcome', '')).strip().lower() not in ('passed', '')
            ),
            'unique_test_cases': len(tda_output.get('unique_test_cases') or []),
            'traceability_rows': len(tda_output.get('traceability') or []),
        },
        'genie': {
            'passed':           genie_passed,
            'failed':           genie_failed,
            'total':            genie_total,
            'fail_rate_pct':    round(100 * genie_failed / genie_total, 1) if genie_total else None,
            'failed_scenarios': [f.get('name') for f in genie_failures if f.get('name')],
        },
        'sonar_quality_gates': {
            'total_pipelines':        len(sonar_gates),
            'non_standard_count':     len(non_standard_gates),
            'non_standard_pipelines': [
                {'pipeline': g.get('Pipeline'), 'quality_gate_name': g.get('quality_gate_name')}
                for g in non_standard_gates
            ],
        },
        'unit_tests_pipeline_count': len(unit_tests),
        'story_field_completeness': {
            'total_stories':            len(story_features),
            'missing_app_id_count':     len(missing_app_id_ids),
            'missing_story_type_count': len(missing_story_type_ids),
            'missing_app_id_wi_ids':     missing_app_id_ids,
            'missing_story_type_wi_ids': missing_story_type_ids,
        },
        'release_state': release_checks.get('System.State', ''),
        'snow_state':    snow_checks.get('state', snow_checks.get('State', '')),
    }


def build_failure_record(job_id: str, request: Any,
                          submitted_at: Optional[datetime], started_at: Optional[datetime],
                          completed_at: Optional[datetime], error: str) -> dict:
    """Compact record for a failed job — no tda_output exists yet, so only
    request metadata and the error message are captured."""
    duration = None
    if started_at and completed_at:
        duration = (completed_at - started_at).total_seconds()

    flags = getattr(request, 'flags', None)

    return {
        'schema_version':  1,
        'job_id':          job_id,
        'release_id':      getattr(request, 'release_id', None),
        'release_stream':  (getattr(request, 'stream', '') or '').upper(),
        'build_id':        getattr(request, 'build_id', None),
        'release_version': getattr(request, 'release_version', '') or '',
        'rwi_only':        bool(getattr(flags, 'rwi_only', False)) if flags else False,
        'status':          'failed',
        'error':           error,
        'submitted_at':    _iso(submitted_at),
        'started_at':      _iso(started_at),
        'completed_at':    _iso(completed_at),
        'duration_seconds': duration,
        'result_path':     None,
    }


# ---------------------------------------------------------------------------
# Append
# ---------------------------------------------------------------------------

def append_record(record: dict, output_dir: str) -> None:
    """Append one JSON line to the registry file. Thread-safe.

    Never raises — a registry write failure is logged but must not fail the
    job it describes.
    """
    path = registry_path(output_dir)
    try:
        parent = os.path.dirname(path)
        if parent:
            os.makedirs(parent, exist_ok=True)
        line = json.dumps(record, default=str)
        with _lock:
            with open(path, 'a', encoding='utf-8') as f:
                f.write(line + '\n')
        logger.info(
            "Registry record appended for job %s (status=%s) -> %s",
            record.get('job_id'), record.get('status'), path,
        )
    except Exception:
        logger.exception("Failed to append registry record for job %s", record.get('job_id'))
