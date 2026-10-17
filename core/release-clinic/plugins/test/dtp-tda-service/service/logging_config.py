"""service/logging_config.py — File + console logging setup for dtp-tda-service.

Centralises logging configuration so every module that does
``logging.getLogger(__name__)`` (main.py, job_runner.py, runner.py,
registry.py, stream_config.py, vault_client.py, ...) writes to both the
console (as before) and a rotating log file on disk — needed for
troubleshooting once the service is running headless/hosted, where nobody is
watching the console in real time.

Environment variables (all optional):
    TDA_LOG_DIR          — Directory for log files (default: "logs", relative
                            to the current working directory the service is
                            started from).
    TDA_LOG_LEVEL        — Root logging level (default: "INFO").
    TDA_LOG_MAX_BYTES    — Max size in bytes before a log file rotates
                            (default: 10 MiB).
    TDA_LOG_BACKUP_COUNT — Number of rotated backup files to keep
                            (default: 5).

Log file: ``<TDA_LOG_DIR>/dtp-tda-service.log`` (plus
``dtp-tda-service.log.1``, ``.2``, ... once rotation kicks in).

Call ``configure_logging()`` exactly once, at process startup, before any
other module calls ``logging.getLogger(__name__)`` and starts logging —
main.py does this immediately after loading the .env file (so a
``TDA_LOG_DIR`` set only in .env is respected) and before anything else.
"""

from __future__ import annotations

import logging
import os
from logging.handlers import RotatingFileHandler

_LOG_FORMAT = "%(asctime)s  %(levelname)-8s  %(name)s — %(message)s"

_configured = False


def configure_logging() -> str:
    """Configure the root logger with a console handler + rotating file handler.

    Idempotent — calling more than once is a no-op after the first call, so
    it's safe to call defensively from more than one entry point.

    Returns the absolute path to the log file for confirmation/logging by the
    caller.
    """
    global _configured

    log_dir   = os.environ.get("TDA_LOG_DIR", "logs")
    level_str = os.environ.get("TDA_LOG_LEVEL", "INFO").strip().upper()
    level     = getattr(logging, level_str, logging.INFO)

    try:
        max_bytes = int(os.environ.get("TDA_LOG_MAX_BYTES", str(10 * 1024 * 1024)))
    except ValueError:
        max_bytes = 10 * 1024 * 1024
    try:
        backup_count = int(os.environ.get("TDA_LOG_BACKUP_COUNT", "5"))
    except ValueError:
        backup_count = 5

    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.abspath(os.path.join(log_dir, "dtp-tda-service.log"))

    if _configured:
        return log_path

    root = logging.getLogger()
    root.setLevel(level)

    formatter = logging.Formatter(_LOG_FORMAT)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root.addHandler(console_handler)

    file_handler = RotatingFileHandler(
        log_path, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    root.addHandler(file_handler)

    _configured = True
    return log_path
