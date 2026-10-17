"""service/stream_config.py — Per-stream server-side configuration.

Replaces the stream-specific sections of associated_builds.yaml that each
team previously maintained locally.  The hosting team manages one central
stream_config.yaml; callers never need to know it exists.

The StreamConfig singleton is loaded once at startup and cached.  To reload
without restarting the service, call StreamConfigStore.reload().
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field
from pathlib import Path
import sys
from typing import Dict, Optional

import yaml

for _ancestor in Path(__file__).resolve().parents:
    if (_ancestor / "release_clinic_env.py").is_file():
        sys.path.insert(0, str(_ancestor))
        break
from release_clinic_env import workspace_path

logger = logging.getLogger(__name__)

# Default path — can be overridden via STREAM_CONFIG_PATH environment variable.
_DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "stream_config.yaml")


# ---------------------------------------------------------------------------
# Per-stream config dataclass
# ---------------------------------------------------------------------------

@dataclass
class StreamConfig:
    """Server-side configuration for one stream.

    Previously lived in per-team associated_builds.yaml files.
    """

    stream: str
    pit_url_template: str = ""
    sonar_key_overrides: Dict[str, str] = field(default_factory=dict)
    ado_field_overrides: Dict[str, str] = field(default_factory=dict)
    genie_enabled: bool = True  # Set to False for streams that do not use Genie regression
    regression_run_filter: str = ""  # Case-insensitive substring to filter ADO test run names (empty = all runs)
    story_comments_enabled: bool = False  # Opt-in: fetch each story WI's last comment (one extra ADO call/story)
    ado_regression_skip: bool = False  # Opt-in: temporarily bypass the ADO-native regression fetch for this stream

    def pit_url(self, version: str) -> str:
        """Substitute {{version}} in the PIT URL template.

        Uses double braces to match tda/integrations/confluence.py's _build_url(),
        which is the function actually used to resolve PIT links for a job
        (via to_pit_links() below). A single-brace {version} template would be
        silently left unresolved in the final URL.
        """
        return self.pit_url_template.replace("{{version}}", version)

    def to_pit_links(self) -> dict:
        """Return the pit_links dict shape expected by tda.build_resolver."""
        return {self.stream: self.pit_url_template}


# ---------------------------------------------------------------------------
# Store
# ---------------------------------------------------------------------------

class StreamConfigStore:
    """Loads and caches per-stream config from stream_config.yaml."""

    def __init__(self, config_path: Optional[str] = None) -> None:
        selected = config_path or os.environ.get("STREAM_CONFIG_FILE") or os.environ.get("STREAM_CONFIG_PATH")
        self._path = str(workspace_path(selected)) if selected else _DEFAULT_CONFIG_PATH
        self._configs: Dict[str, StreamConfig] = {}
        self.reload()

    def reload(self) -> None:
        """(Re-)load stream_config.yaml.  Thread-safe for reads after load."""
        if not os.path.exists(self._path):
            raise FileNotFoundError(
                f"stream_config.yaml not found at '{self._path}'. "
                "Set STREAM_CONFIG_FILE to the correct service configuration location."
            )
        with open(self._path, encoding="utf-8") as f:
            raw = yaml.safe_load(f) or {}

        configs: Dict[str, StreamConfig] = {}
        for stream_name, stream_data in (raw.get("streams") or {}).items():
            configs[stream_name.upper()] = StreamConfig(
                stream=stream_name.upper(),
                pit_url_template=stream_data.get("pit_url_template", ""),
                sonar_key_overrides=stream_data.get("sonar_key_overrides") or {},
                ado_field_overrides=stream_data.get("ado_field_overrides") or {},
                genie_enabled=stream_data.get("genie_enabled", True),
                regression_run_filter=stream_data.get("regression_run_filter", ""),
                story_comments_enabled=stream_data.get("story_comments_enabled", False),
                ado_regression_skip=stream_data.get("ado_regression_skip", False),
            )

        self._configs = configs
        logger.info(
            "StreamConfigStore: loaded %d streams from %s",
            len(configs), self._path,
        )

    def get(self, stream: str) -> StreamConfig:
        """Return the StreamConfig for the given stream name.

        Returns an empty StreamConfig (no PIT URL, no overrides) if the
        stream is not listed — the collector will proceed without those
        optional fields rather than raising.
        """
        cfg = self._configs.get(stream.upper())
        if cfg is None:
            logger.warning(
                "StreamConfigStore: no config found for stream '%s' — using defaults.", stream
            )
            return StreamConfig(stream=stream.upper())
        return cfg

    @property
    def known_streams(self) -> list[str]:
        return list(self._configs.keys())
