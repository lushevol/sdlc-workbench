"""service/main.py — FastAPI application for dtp-tda-service.

Exposes the TDA data-collection pipeline (Part 1 of dtp-tda-report) as a
REST API with async job execution.  The AutoTDASummary JSON produced by each
job is consumed by the dtp-tda-report Copilot skill (Part 2, unchanged).

Endpoints:
    POST /tda/run                  — Submit a new TDA collection job
    GET  /tda/jobs/{job_id}        — Poll job status
    GET  /tda/jobs/{job_id}/result — Download the AutoTDASummary JSON
    GET  /tda/jobs/{job_id}/logs   — Stream job log lines
    GET  /health                   — Liveness + readiness check

Startup:
    uvicorn service.main:app --host 0.0.0.0 --port 8080

Environment variables:
    See service/server_config.py for the full list.
    WORKER_POOL_SIZE   — Thread pool size for background jobs (default: 4)
    TDA_OUTPUT_DIR     — Directory for JSON output files (default: /tmp/tda-output)
"""

from __future__ import annotations

import logging
import os
from pathlib import Path
import sys
import uuid
from contextlib import asynccontextmanager
from datetime import timezone

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

_VERSION = "1.0.0"


# ---------------------------------------------------------------------------
# .env loader — runs at module import time so Vault env vars (and logging
# config vars like TDA_LOG_DIR) are available before logging is configured
# and before the lifespan function tries to instantiate VaultClient.
#
# Default settings come from the selected Workbench root.
# SERVICE_ENV_FILE remains an explicit file override for existing deployments.
# ---------------------------------------------------------------------------

for _ancestor in Path(__file__).resolve().parents:
    if (_ancestor / "release_clinic_env.py").is_file():
        sys.path.insert(0, str(_ancestor))
        break
from release_clinic_env import load_environment


def _load_service_env() -> tuple[str | None, list[str]]:
    """Load shared root settings before service modules read environment values."""
    return load_environment(os.environ.get("SERVICE_ENV_FILE", "").strip() or None)


_env_path, _env_loaded_keys = _load_service_env()

# Imports follow environment loading because runner reads settings during import.
from service.job_runner import JobRunner
from service.job_store import JobStore
from service.logging_config import configure_logging
from service.models import (
    HealthResponse,
    JobLogsResponse,
    JobStatus,
    JobStatusResponse,
    JobSubmitResponse,
    TDAJobRequest,
)
from service.stream_config import StreamConfigStore
from service.vault_client import VaultClient
import service.runner as _runner

_log_path = configure_logging()
logger = logging.getLogger(__name__)

if _env_path:
    logger.info(".env loaded from %s (%d variable(s): %s)", _env_path, len(_env_loaded_keys), _env_loaded_keys)
else:
    logger.warning(
        "No .env file found — relying entirely on shell environment variables. "
        "Configure .env at AI_SDLC_WORKSPACE or set process environment values."
    )
logger.info("Logging to console + file: %s", _log_path)


# ---------------------------------------------------------------------------
# Application lifespan (startup / shutdown)
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialise shared resources at startup; tear them down at shutdown."""

    # --- Vault ---
    vault = VaultClient()
    vault.connect()
    app.state.vault = vault

    # --- Stream config ---
    stream_store = StreamConfigStore()
    app.state.stream_store = stream_store

    # --- Job store + runner ---
    job_store = JobStore()
    worker_pool_size = int(os.environ.get("WORKER_POOL_SIZE", "4"))
    job_runner = JobRunner(job_store, max_workers=worker_pool_size)
    app.state.job_store  = job_store
    app.state.job_runner = job_runner

    # Inject shared dependencies into runner module so workers can resolve
    # credentials and stream config without re-loading per job.
    output_dir = os.environ.get("TDA_OUTPUT_DIR", "/tmp/tda-output")
    _runner.configure(vault, stream_store, output_dir)

    logger.info(
        "dtp-tda-service v%s started — %d worker(s), output: %s",
        _VERSION, worker_pool_size, output_dir,
    )

    yield  # Application runs here

    # --- Shutdown ---
    logger.info("Shutting down dtp-tda-service…")
    job_runner.shutdown(wait=True)


# ---------------------------------------------------------------------------
# FastAPI app
# ---------------------------------------------------------------------------

app = FastAPI(
    title="dtp-tda-service",
    version=_VERSION,
    description=(
        "Hosted TDA data-collection service for Blade releases. "
        "Submit a job via POST /tda/run, then poll GET /tda/jobs/{id} "
        "and download the AutoTDASummary JSON when complete."
    ),
    lifespan=lifespan,
)


# ---------------------------------------------------------------------------
# Helper — build absolute URLs for a job
# ---------------------------------------------------------------------------

def _job_urls(request_base: str, job_id: str) -> dict:
    base = request_base.rstrip("/")
    return {
        "poll_url":   f"{base}/tda/jobs/{job_id}",
        "result_url": f"{base}/tda/jobs/{job_id}/result",
        "logs_url":   f"{base}/tda/jobs/{job_id}/logs",
    }


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.post(
    "/tda/run",
    status_code=202,
    response_model=JobSubmitResponse,
    summary="Submit a TDA data-collection job",
    tags=["Jobs"],
)
async def submit_job(request: TDAJobRequest) -> JobSubmitResponse:
    """Accept a TDA collection request and return a job ID immediately.

    The job runs asynchronously (5–7 minutes).  Poll GET /tda/jobs/{job_id}
    for status, then download the result when status == "complete".
    """
    if not request.flags.rwi_only and not request.build_id:
        raise HTTPException(
            status_code=422,
            detail="build_id is required unless flags.rwi_only is true.",
        )

    job_store:  JobStore  = app.state.job_store
    job_runner: JobRunner = app.state.job_runner

    job_id = str(uuid.uuid4())
    record = job_store.create(job_id, request)

    # Build response URLs.  We derive the base URL from the Host header via
    # a placeholder — in production, set a canonical SERVICE_BASE_URL env var.
    base_url = os.environ.get("SERVICE_BASE_URL", "http://localhost:8080")
    urls = _job_urls(base_url, job_id)

    job_runner.submit(job_id, request)

    logger.info(
        "Accepted job %s (stream=%s release=%s build=%s)",
        job_id, request.stream, request.release_id, request.build_id,
    )

    return JobSubmitResponse(
        job_id=job_id,
        status=JobStatus.PENDING,
        stream=request.stream,
        release_id=request.release_id,
        submitted_at=record.submitted_at.isoformat(),
        **urls,
    )


@app.get(
    "/tda/jobs/{job_id}",
    response_model=JobStatusResponse,
    summary="Get job status",
    tags=["Jobs"],
)
async def get_job_status(job_id: str) -> JobStatusResponse:
    """Poll the status of a submitted TDA job."""
    job_store: JobStore = app.state.job_store
    record = job_store.get(job_id)
    if record is None:
        raise HTTPException(status_code=404, detail=f"Job '{job_id}' not found.")

    base_url = os.environ.get("SERVICE_BASE_URL", "http://localhost:8080")
    urls = _job_urls(base_url, job_id)

    result_url = (
        urls["result_url"] if record.status == JobStatus.COMPLETE else None
    )

    return JobStatusResponse(
        job_id=job_id,
        status=record.status,
        stream=record.request.stream,
        release_id=record.request.release_id,
        submitted_at=record.submitted_at.isoformat(),
        started_at=(record.started_at.isoformat() if record.started_at else None),
        completed_at=(record.completed_at.isoformat() if record.completed_at else None),
        error=record.error,
        result_url=result_url,
        logs_url=urls["logs_url"],
    )


@app.get(
    "/tda/jobs/{job_id}/result",
    summary="Download the AutoTDASummary JSON",
    tags=["Jobs"],
)
async def download_result(job_id: str) -> FileResponse:
    """Download the AutoTDASummary JSON once the job is complete.

    The returned file is fed directly into the dtp-tda-report Copilot skill
    (SKILL.md) — the same JSON shape as the locally-run AutoTDAScript.py.
    """
    job_store: JobStore = app.state.job_store
    record = job_store.get(job_id)

    if record is None:
        raise HTTPException(status_code=404, detail=f"Job '{job_id}' not found.")
    if record.status != JobStatus.COMPLETE:
        raise HTTPException(
            status_code=409,
            detail=f"Job '{job_id}' is not yet complete (status: {record.status}).",
        )
    if not record.result_path or not os.path.exists(record.result_path):
        raise HTTPException(
            status_code=500,
            detail=f"Result file not found for job '{job_id}'.",
        )

    filename = os.path.basename(record.result_path)
    return FileResponse(
        path=record.result_path,
        media_type="application/json",
        filename=filename,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@app.get(
    "/tda/jobs/{job_id}/logs",
    response_model=JobLogsResponse,
    summary="Get job log lines",
    tags=["Jobs"],
)
async def get_job_logs(job_id: str) -> JobLogsResponse:
    """Return all log lines accumulated so far for a job.

    Useful for monitoring long-running jobs or diagnosing failures.
    """
    job_store: JobStore = app.state.job_store
    record = job_store.get(job_id)
    if record is None:
        raise HTTPException(status_code=404, detail=f"Job '{job_id}' not found.")

    return JobLogsResponse(
        job_id=job_id,
        status=record.status,
        lines=list(record.log_lines),
    )


@app.get(
    "/health",
    response_model=HealthResponse,
    summary="Liveness and readiness check",
    tags=["Operations"],
)
async def health() -> HealthResponse:
    """Returns 200 when the service is ready to accept jobs."""
    vault: VaultClient  = app.state.vault
    job_store: JobStore = app.state.job_store
    runner: JobRunner   = app.state.job_runner

    return HealthResponse(
        status="ok",
        version=_VERSION,
        vault_connected=vault.is_connected,
        worker_pool_size=runner.max_workers,
        active_jobs=job_store.active_count(),
    )
