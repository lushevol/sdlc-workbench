"""tda/call_tracker.py — lightweight global API call counter / rate tracker.

Tracks how many outbound calls were made to each external system (ADO, SNOW,
Sonar, Genie, Confluence) during a single collector run, plus the first/last
call timestamp per system so an average call rate can be reported at the end
of the run. Thread-safe — safe to call from any ThreadPoolExecutor worker,
since PARALLEL_ENABLED may be true and several collectors can be recording
calls concurrently.

This is a process-wide singleton (``tracker``) rather than something threaded
through every function signature — each real outbound call site only needs
one extra line: ``tracker.record('System')``.
"""

from __future__ import annotations

import threading
import time


class APICallTracker:
    """Thread-safe counter of outbound API calls, grouped by system name."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._counts: dict[str, int] = {}
        self._first_ts: dict[str, float] = {}
        self._last_ts: dict[str, float] = {}
        self._run_start = time.monotonic()

    def reset(self) -> None:
        """Clear all counters and restart the run clock. Call once at the
        start of a collector run so counts/rates reflect this run only."""
        with self._lock:
            self._counts.clear()
            self._first_ts.clear()
            self._last_ts.clear()
            self._run_start = time.monotonic()

    def record(self, system: str) -> None:
        """Record one outbound call to ``system`` (e.g. 'ADO', 'SNOW', 'Sonar',
        'Genie', 'Confluence'). Safe to call from any thread."""
        now = time.monotonic()
        with self._lock:
            self._counts[system] = self._counts.get(system, 0) + 1
            if system not in self._first_ts:
                self._first_ts[system] = now
            self._last_ts[system] = now

    def total_calls(self) -> int:
        with self._lock:
            return sum(self._counts.values())

    def summary_lines(self) -> list[str]:
        """Build the per-system + overall summary as printable lines."""
        with self._lock:
            counts = dict(self._counts)
            first_ts = dict(self._first_ts)
            last_ts = dict(self._last_ts)
            run_start = self._run_start

        now = time.monotonic()
        total_calls = sum(counts.values())
        total_elapsed = max(now - run_start, 1e-9)

        lines: list[str] = []
        lines.append("=" * 75)
        lines.append("  API CALL SUMMARY")
        lines.append("=" * 75)
        if not counts:
            lines.append("  No outbound API calls were tracked during this run.")
            lines.append("=" * 75)
            return lines

        col = f"  {'System':<14} {'Calls':>8} {'Span (s)':>10} {'Avg Rate (calls/s)':>20}"
        lines.append(col)
        lines.append(f"  {'-' * 14} {'-' * 8} {'-' * 10} {'-' * 20}")
        for system in sorted(counts, key=lambda s: -counts[s]):
            n = counts[system]
            span = last_ts[system] - first_ts[system]
            if n > 1 and span > 0:
                rate_str = f"{n / span:.2f}"
            else:
                rate_str = "n/a (1 call)" if n == 1 else "n/a"
            lines.append(f"  {system:<14} {n:>8} {span:>10.1f} {rate_str:>20}")
        lines.append(f"  {'-' * 14} {'-' * 8} {'-' * 10} {'-' * 20}")
        overall_rate = total_calls / total_elapsed
        lines.append(f"  {'TOTAL':<14} {total_calls:>8} {total_elapsed:>10.1f} {overall_rate:>20.2f}")
        lines.append("=" * 75)
        return lines

    def print_summary(self) -> None:
        """Print the summary table to stdout. Call at the end of a run."""
        for line in self.summary_lines():
            print(line, flush=True)


# Process-wide singleton — import this directly at each call site:
#   from tda.call_tracker import tracker as call_tracker
#   call_tracker.record('ADO')
tracker = APICallTracker()
