"""service/runner.py — Headless TDA orchestration.

This is the service equivalent of AutoTDAScript.py main().

Key differences from the CLI version:
  - No load_env_file() / decrypt_snow_credentials() — credentials come from Vault.
  - No interactive input() prompt — auto_confirm_builds flag replaces it.
  - Accepts a TDAJobRequest object instead of CLI args.
  - Accepts a log_fn callback so log lines are streamed to the job store
    (and surfaced via GET /tda/jobs/{id}/logs) rather than written to stdout.
  - Returns the path to the AutoTDASummary JSON file rather than printing it.

The tda.* package is imported here (not at module level) to avoid import-time
side effects if TDA_PKG_PATH is not yet set when the module is first loaded.
"""

from __future__ import annotations

import json
import logging
import os
import time
from datetime import datetime, timezone
from typing import Callable, Optional

logger = logging.getLogger(__name__)

# Type alias for the log-line callback.
LogFn = Callable[[str], None]


# NOTE (2026-07-16): a service-only _patch_ado_client_proxy() helper used to
# live here, overriding ADOClient.unset_proxy() so it left HTTPS_PROXY set in
# os.environ (forcing Genie/Sonar's bare `requests` calls through the corporate
# proxy). It was removed after confirming the CLI script (AutoTDAScript.py)
# never applied this override and runs reliably — unset_proxy() there fully
# clears HTTPS_PROXY, matching tda/integrations/confluence.py's documented
# intent that Genie/Sonar/Confluence are internal hosts that should be reached
# directly, not via the proxy. The forced-proxy override is the most likely
# cause of the ConnectionResetError/ReadTimeout/ProxyError 502 sequence seen
# when running jobs via the service — removing it makes the service match the
# CLI script's proven-working behavior exactly.


# ---------------------------------------------------------------------------
# Dependency injection container
# ---------------------------------------------------------------------------
# These are set once at application startup (main.py lifespan) and reused
# by every job execution.  Avoids re-loading Vault credentials per job.

_vault_client = None       # VaultClient instance
_stream_store = None       # StreamConfigStore instance
_output_dir: str = os.environ.get("TDA_OUTPUT_DIR", "/tmp/tda-output")


def configure(vault_client, stream_store, output_dir: Optional[str] = None) -> None:
    """Called once from main.py startup to inject shared dependencies."""
    global _vault_client, _stream_store, _output_dir
    _vault_client = vault_client
    _stream_store = stream_store
    if output_dir:
        _output_dir = output_dir
    _write_associated_builds_yaml()


def get_output_dir() -> str:
    """Public accessor for the configured output directory.

    Used by job_runner.py to resolve the registry path when building a
    failure record (no tda_output/output_file is available on failure).
    """
    return _output_dir


def _write_associated_builds_yaml() -> None:
    """Write a minimal associated_builds.yaml to CWD from StreamConfigStore data.

    The tda.build_resolver package always tries to read associated_builds.yaml
    from CWD when resolve_builds() is called.  We generate it here from the
    service's stream_config.yaml so no manual file is needed.
    Called once at startup — safe for concurrent job threads since they only read it.
    """
    import yaml  # noqa: PLC0415

    pit_urls = {}
    sonar_keys = {}
    if _stream_store is not None:
        for stream in _stream_store.known_streams:
            cfg = _stream_store.get(stream)
            if cfg.pit_url_template:
                pit_urls[stream] = cfg.pit_url_template
            if cfg.sonar_key_overrides:
                sonar_keys[stream] = cfg.sonar_key_overrides

    data: dict = {"PIT_URLS": pit_urls}
    for stream, keys in sonar_keys.items():
        data[f"{stream}_SONAR_KEYS"] = keys

    dest = os.path.join(os.getcwd(), "associated_builds.yaml")
    with open(dest, "w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False)
    logger.info("associated_builds.yaml written to %s", dest)


# ---------------------------------------------------------------------------
# Main entry point (called from JobRunner._execute)
# ---------------------------------------------------------------------------

def run_tda_job(request, job_id: Optional[str] = None,
                 submitted_at: Optional[datetime] = None,
                 log_fn: Optional[LogFn] = None) -> str:
    """Run a complete TDA data-collection job and return the AutoTDASummary path.

    Parameters
    ----------
    request : TDAJobRequest
        The validated job request from the API.
    job_id : str, optional
        The job's UUID, used only to tag the portfolio registry record.
    submitted_at : datetime, optional
        When the job was originally submitted (for the registry record's
        queue-wait time). Defaults to ``started_at`` when not supplied.
    log_fn : callable, optional
        Called with each progress line.  Defaults to logging.info.

    Returns
    -------
    str
        Absolute path to the AutoTDASummary_<STREAM>_<id>.json file.
    """
    started_at = datetime.now(timezone.utc)

    # Lazy imports — tda.* path must be set before these execute.
    from service.server_config import build_tda_config  # noqa: PLC0415
    from tda.config import decrypt_snow_credentials     # noqa: PLC0415
    from tda.http_client import ADOClient, WIResponseAdapter  # noqa: PLC0415
    from tda.build_resolver import resolve_builds, load_stream_config  # noqa: PLC0415
    from tda.result_store import ResultStore            # noqa: PLC0415
    from tda.summarizer import generate_summary         # noqa: PLC0415
    from tda.collectors.release import (                # noqa: PLC0415
        collect_release_data,
        extract_application_checks,
        extract_bug_checks,
    )
    from tda.collectors.testing import (                # noqa: PLC0415
        return_test_suites,
        return_test_cases_from_suite,
        populate_test_case_details,
        extract_test_plan_checks,
        extract_test_result_checks,
        get_story_items_in_release,
    )
    from tda.collectors.traceability import build_traceability  # noqa: PLC0415
    from tda.call_tracker import tracker as call_tracker         # noqa: PLC0415

    _log = log_fn or (lambda line: logger.info(line))

    release_id      = request.release_id
    release_stream  = request.stream
    supplied_build  = request.build_id or ""
    release_version = (request.release_version or "").strip()
    flags           = request.flags

    _log(f"[1/6] Resolving credentials and stream config for {release_stream}…")

    # --- Credentials + tda Config ---
    credentials   = _vault_client.load_credentials()
    stream_cfg    = _stream_store.get(release_stream)
    cfg           = build_tda_config(credentials, stream_cfg)

    # Decrypt SNOW credentials (populates os.environ['CLIENT_SECRET'] via Fernet).
    decrypt_snow_credentials()

    client = ADOClient(cfg)
    client.set_proxy()

    # Reset the API call tracker so counts/rates reflect only this job — the
    # tracker is a process-wide singleton shared across worker threads, so
    # this must happen before any collector call is made for this job.
    call_tracker.reset()

    # ado_regression_skip is sourced from the service's own StreamConfig (like
    # regression_run_filter below) rather than from resolve_builds()/
    # load_stream_config() — the generated associated_builds.yaml does not
    # carry a GENIE_DISABLED_STREAMS/REGRESSION_CONFIG-style section for it.
    ado_regression_skip = stream_cfg.ado_regression_skip

    # --- Step 1: resolve associated builds ---
    if flags.rwi_only:
        _log("[1/6] --rwi-only mode: skipping build resolution.")
        blade_release_builds     = {}
        associated_builds_source = "rwi-only"
        duplicate_pipeline_versions = {}
        sonar_key_overrides      = {}
        sonar_stream_config      = {}
        pit_links, _, _, _, _, _ = load_stream_config(release_stream)
        genie_enabled            = stream_cfg.genie_enabled
    else:
        _log(f"[1/6] Resolving associated builds for release build {supplied_build}…")

        # Merge any caller-supplied build_overrides into the YAML / auto-discovery flow.
        # When build_overrides is populated and use_yaml is true, it is the authoritative
        # source.  Otherwise it supplements auto-discovery for listed pipelines only.
        if request.build_overrides and flags.use_yaml:
            # Treat build_overrides as the complete associated_builds.yaml equivalent.
            # Each value may be a plain build ID ("13458068") or a "build_id version"
            # annotated string ("13458068 rules-186.0.0"), matching stream_config.yaml's
            # `builds:` schema — split on first whitespace, same as
            # tda.build_resolver.load_builds_from_yaml().
            blade_release_builds: dict[str, str] = {}
            pipeline_versions: dict[str, str] = {}
            for pipeline, raw_value in request.build_overrides.items():
                raw = str(raw_value).strip()
                parts = raw.split(None, 1)   # split on first whitespace only
                blade_release_builds[pipeline] = parts[0]
                if len(parts) == 2:
                    pipeline_versions[pipeline] = parts[1]

            associated_builds_source = "request.build_overrides"
            duplicate_pipeline_versions = {}
            sonar_key_overrides      = stream_cfg.sonar_key_overrides
            sonar_stream_config      = {}
            pit_links                = stream_cfg.to_pit_links()
            genie_enabled            = stream_cfg.genie_enabled
            if pipeline_versions:
                sonar_stream_config['_pipeline_versions'] = pipeline_versions
                _log(
                    f"[1/6] Version annotations found for {len(pipeline_versions)} "
                    f"pipeline(s) — Sonar branches will use release/<version> directly."
                )
            _log(f"[1/6] Using {len(blade_release_builds)} build(s) from request overrides.")
        else:
                try:
                    (blade_release_builds,
                     associated_builds_source,
                     _associated_build_versions,
                     duplicate_pipeline_versions,
                     sonar_key_overrides,
                     sonar_stream_config,
                     pit_links,
                     genie_enabled,
                     _run_filter,
                     _ado_regression_skip) = resolve_builds(client, release_stream, supplied_build,
                                                     use_yaml=False)
                except (ValueError, FileNotFoundError) as exc:
                    raise RuntimeError(
                        f"Build auto-discovery failed for build_id='{supplied_build}' "
                        f"(stream={release_stream}): {exc}\n\n"
                        "This means the supplied build_id does not have a 'promotedImageList' "
                        "artifact, so the service cannot auto-discover the associated pipeline "
                        "build IDs.\n\n"
                        "SOLUTION: Re-submit the job with explicit 'build_overrides' mapping "
                        "each pipeline name to its build ID, e.g.:\n"
                        '  "build_overrides": {\n'
                        '    "blade-rates-api": "9086679",\n'
                        '    "blade-rates-ui": "9086700"\n'
                        '  }\n\n'
                        "You can find the pipeline build IDs in the Azure DevOps pipeline runs "
                        "for this release."
                    ) from exc
        # auto_confirm_builds is always True in service mode (no operator present).
        if not flags.auto_confirm_builds:
            _log("[1/6] WARN: auto_confirm_builds=false in service mode — proceeding anyway.")

    _log(f"[2/6] Starting TDA data collection for release {release_id} ({release_stream})…")
    store   = ResultStore()
    t_start = time.time()

    # --- Step 3: release WI + all integrations ---
    _log("[3/6] Collecting release WI, approvals, unit tests, Sonar, regression, PIT…")
    t3 = time.time()
    release_data = collect_release_data(
        release_id=release_id,
        supplied_build_id=supplied_build,
        release_stream=release_stream,
        blade_release_builds=blade_release_builds,
        sonar_stream_config=sonar_stream_config,
        sonar_key_overrides=sonar_key_overrides,
        pit_links=pit_links,
        supplied_release_version=release_version,
        cfg=cfg,
        client=client,
        rwi_only=flags.rwi_only,
        genie_enabled=genie_enabled,
        regression_run_filter=stream_cfg.regression_run_filter,
        ado_regression_skip=ado_regression_skip,
    )
    store.ingest_release_data(release_data)
    _log(f"[3/6] Done in {time.time() - t3:.1f}s")

    # --- Step 4: linked WIs (stories, bugs, test plans, application) ---
    work_item_relations = release_data.get("work_item_relations", [])
    _log(f"[4/6] Processing {len(work_item_relations)} linked work items…")
    t4 = time.time()

    wi_ids  = [wi["url"].split("workItems/")[-1] for wi in work_item_relations]
    wi_batch = (
        client.fetch_work_items_batch(wi_ids)
        if (not flags.no_batch and wi_ids)
        else {}
    )

    story_features = get_story_items_in_release(work_item_relations, wi_batch, cfg, client)
    store.story_features.extend(story_features)

    test_plan_ids: list[str] = []
    for wi in work_item_relations:
        wi_id   = wi["url"].split("workItems/")[-1]
        wi_data = wi_batch.get(wi_id) if wi_batch else None
        if wi_data is None:
            wi_data = client.get("WorkItemsForRelease", wi_id).json()
        resp    = WIResponseAdapter(wi_data)
        wi_type = wi_data.get("fields", {}).get("System.WorkItemType", "")

        if wi_type == "Application":
            store.application_features.append(extract_application_checks(resp, cfg))
        elif wi_type == "Bug":
            store.bug_features.append(extract_bug_checks(resp, cfg))
        elif wi_type == "Test Plan":
            plan_id = str(wi_data.get("id", ""))
            store.test_plan_features.append(extract_test_plan_checks(resp, client))
            test_plan_ids.append(plan_id)

    for plan_id in test_plan_ids:
        result_rows = extract_test_result_checks(None, plan_id, cfg, client)
        store.test_result_features.extend(result_rows)

    _log(f"[4/6] Done in {time.time() - t4:.1f}s")

    # --- Step 5: traceability ---
    _log(f"[5/6] Building traceability for {len(story_features)} stories…")
    t5 = time.time()
    traceability_rows, unique_tcs, tc_fields_batch = build_traceability(story_features, release_id, cfg, client)
    store.ingest_traceability(traceability_rows, unique_tcs)
    _log(f"[5/6] Done in {time.time() - t5:.1f}s")

    # Reuses tc_fields_batch from build_traceability() (same TC set) instead of
    # issuing a second, identical workitemsbatch fetch for the same data.
    unique_tc_ids = list(unique_tcs.keys())
    if unique_tc_ids:
        store.test_case_details.extend(
            populate_test_case_details(unique_tc_ids, client, cfg, prefetched_batch=tc_fields_batch)
        )

    # --- Step 6: write JSON ---
    _log("[6/6] Writing JSON output…")
    t6 = time.time()
    os.makedirs(_output_dir, exist_ok=True)

    output_file = os.path.join(
        _output_dir, f"AutoTDAResults_{release_stream}_{release_id}.json"
    )
    tda_output = store.to_tda_output(release_id, release_stream, blade_release_builds)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(tda_output, f, indent=2, default=str)

    summary_path = generate_summary(tda_output, _output_dir, release_stream, release_id)

    t_total = time.time() - t_start
    mins, secs = divmod(int(t_total), 60)
    _log(f"[6/6] Done in {time.time() - t6:.1f}s")
    _log(f"Full results : {output_file}")
    _log(f"Summary      : {summary_path}")
    _log(f"Total time   : {mins}m {secs}s")

    for line in call_tracker.summary_lines():
        _log(line)

    # --- Portfolio registry (best-effort, must never fail the job) ---
    try:
        from service import registry  # noqa: PLC0415
        completed_at = datetime.now(timezone.utc)
        record = registry.build_success_record(
            job_id=job_id or "",
            request=request,
            tda_output=tda_output,
            submitted_at=submitted_at or started_at,
            started_at=started_at,
            completed_at=completed_at,
            result_path=summary_path,
        )
        registry.append_record(record, _output_dir)
    except Exception:
        logger.exception("Failed to write portfolio registry record for job %s", job_id)

    return summary_path
