"""service/job_runner.py — Background job executor.

Submits TDA collection jobs to a thread pool so the FastAPI handler returns
immediately (HTTP 202) while the 5-7 minute collection runs asynchronously.

Design decisions:
  - ThreadPoolExecutor rather than asyncio: the tda.* package uses
    blocking requests calls throughout, so true async would require a full
    rewrite.  A thread pool is the minimal-change wrapper.
  - max_workers defaults to 4 so the service can process multiple streams
    concurrently without exhausting the ADO / Confluence rate limits.
  - The executor is created once at application startup (via JobRunner
    attached to app.state) and shut down gracefully on application teardown.
"""

from __future__ import annotations

import logging
from concurrent.futures import ThreadPoolExecutor

from service.job_store import JobStore
from service.models import TDAJobRequest

logger = logging.getLogger(__name__)


class JobRunner:
    """Owns the thread pool and dispatches jobs to runner.run_tda_job()."""

    def __init__(self, store: JobStore, max_workers: int = 4) -> None:
        self._store = store
        self._executor = ThreadPoolExecutor(
            max_workers=max_workers,
            thread_name_prefix="tda-worker",
        )
        self.max_workers = max_workers

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def submit(self, job_id: str, request: TDAJobRequest) -> None:
        """Enqueue a job for execution.  Returns immediately."""
        # Record is already created (PENDING) by the caller before submit().
        logger.info("Submitting job %s (stream=%s release=%s)", job_id, request.stream, request.release_id)
        self._executor.submit(self._execute, job_id, request)

    def shutdown(self, wait: bool = True) -> None:
        """Graceful shutdown — called on application teardown."""
        logger.info("Shutting down job runner (wait=%s)…", wait)
        self._executor.shutdown(wait=wait)

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _execute(self, job_id: str, request: TDAJobRequest) -> None:
        """Worker function — runs in a thread pool thread.

        Imports runner lazily so circular imports are avoided at module load.
        """
        # Import here — runner imports tda.* which does sys.path manipulation
        from service.runner import run_tda_job  # noqa: PLC0415

        record = self._store.get(job_id)
        submitted_at = record.submitted_at if record else None

        self._store.mark_running(job_id)
        log_fn = lambda line: self._store.append_log(job_id, line)  # noqa: E731

        try:
            log_fn(f"[job:{job_id}] Starting TDA collection for {request.stream} / release {request.release_id}")
            result_path = run_tda_job(request, job_id=job_id, submitted_at=submitted_at, log_fn=log_fn)
            self._store.mark_complete(job_id, result_path)
            log_fn(f"[job:{job_id}] Complete — summary written to {result_path}")
            logger.info("Job %s complete — %s", job_id, result_path)
        except Exception as exc:
            error_msg = f"{type(exc).__name__}: {exc}"
            self._store.mark_failed(job_id, error_msg)
            self._append_failure_registry_record(job_id, request, submitted_at, error_msg)
            log_fn(f"[job:{job_id}] FAILED — {error_msg}")
            logger.exception("Job %s failed", job_id)

    def _append_failure_registry_record(self, job_id: str, request: TDAJobRequest,
                                         submitted_at, error_msg: str) -> None:
        """Best-effort portfolio registry write for a failed job.

        No tda_output exists for a failed run, so only request metadata and
        the error message are captured. Never raises — a registry write
        failure must not mask the original job failure.
        """
        try:
            from datetime import datetime, timezone  # noqa: PLC0415
            from service import registry  # noqa: PLC0415
            from service.runner import get_output_dir  # noqa: PLC0415

            rec = self._store.get(job_id)
            started_at = rec.started_at if rec else None
            completed_at = datetime.now(timezone.utc)
            record = registry.build_failure_record(
                job_id=job_id,
                request=request,
                submitted_at=submitted_at,
                started_at=started_at,
                completed_at=completed_at,
                error=error_msg,
            )
            registry.append_record(record, get_output_dir())
        except Exception:
            logger.exception("Failed to write failure registry record for job %s", job_id)

