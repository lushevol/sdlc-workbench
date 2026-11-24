"""service/job_store.py — In-memory job state store.

Tracks the lifecycle of every TDA collection job: pending → running →
complete | failed.  Each job record also accumulates log lines so callers
can inspect progress via GET /tda/jobs/{id}/logs.

Production note:
    Replace the in-memory _store dict with a Redis client to support
    multiple service replicas and job persistence across restarts.
    The public interface (create / get / update_status / append_log) is
    intentionally kept minimal so swapping the backing store requires
    changes only in this module.
"""

from __future__ import annotations

import threading
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional

from service.models import JobStatus, TDAJobRequest


# ---------------------------------------------------------------------------
# Job record
# ---------------------------------------------------------------------------

@dataclass
class JobRecord:
    job_id:       str
    status:       JobStatus
    request:      TDAJobRequest
    submitted_at: datetime
    started_at:   Optional[datetime]   = None
    completed_at: Optional[datetime]   = None
    result_path:  Optional[str]        = None   # server-local path to AutoTDASummary JSON
    error:        Optional[str]        = None
    log_lines:    List[str]            = field(default_factory=list)


# ---------------------------------------------------------------------------
# Store
# ---------------------------------------------------------------------------

class JobStore:
    """Thread-safe in-memory job store.

    All public methods acquire the same lock so records are safe to read and
    write from the ThreadPoolExecutor workers (job_runner.py) and FastAPI
    request handlers (main.py) concurrently.
    """

    def __init__(self) -> None:
        self._store: Dict[str, JobRecord] = {}
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # Write operations
    # ------------------------------------------------------------------

    def create(self, job_id: str, request: TDAJobRequest) -> JobRecord:
        """Insert a new PENDING record and return it."""
        record = JobRecord(
            job_id=job_id,
            status=JobStatus.PENDING,
            request=request,
            submitted_at=datetime.now(tz=timezone.utc),
        )
        with self._lock:
            self._store[job_id] = record
        return record

    def mark_running(self, job_id: str) -> None:
        with self._lock:
            rec = self._store[job_id]
            rec.status     = JobStatus.RUNNING
            rec.started_at = datetime.now(tz=timezone.utc)

    def mark_complete(self, job_id: str, result_path: str) -> None:
        with self._lock:
            rec = self._store[job_id]
            rec.status       = JobStatus.COMPLETE
            rec.result_path  = result_path
            rec.completed_at = datetime.now(tz=timezone.utc)

    def mark_failed(self, job_id: str, error: str) -> None:
        with self._lock:
            rec = self._store[job_id]
            rec.status       = JobStatus.FAILED
            rec.error        = error
            rec.completed_at = datetime.now(tz=timezone.utc)

    def append_log(self, job_id: str, line: str) -> None:
        """Append a single log line.  Silently ignored if job_id is unknown."""
        with self._lock:
            rec = self._store.get(job_id)
            if rec is not None:
                rec.log_lines.append(line)

    # ------------------------------------------------------------------
    # Read operations
    # ------------------------------------------------------------------

    def get(self, job_id: str) -> Optional[JobRecord]:
        with self._lock:
            return self._store.get(job_id)

    def active_count(self) -> int:
        with self._lock:
            return sum(
                1 for r in self._store.values()
                if r.status in (JobStatus.PENDING, JobStatus.RUNNING)
            )
