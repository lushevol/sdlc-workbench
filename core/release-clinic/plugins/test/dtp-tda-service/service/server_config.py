"""service/server_config.py — Build tda.config.Config from Vault credentials.

The tda.* package (sourced from dtp-tda-report) uses a Config dataclass that
was originally populated from .env.  This module constructs an equivalent
Config from:
  - Vault credentials (passed in as a Credentials object)
  - Server infrastructure env vars (ADO org URL, Confluence URL, etc.)
  - Per-stream StreamConfig (PIT URLs, Sonar key overrides)

No .env file, no associated_builds.yaml required.

Environment variables consumed here (set by the hosting team at deploy time):
    ADO_ORG_URL          — e.g. https://dev.azure.com/MyOrg
    ADO_PROJECT          — e.g. FMQPR
    CONFLUENCE_URL        — e.g. https://confluence.internal
    CONFLUENCE_SPACE_KEY  — e.g. BLADE
    SNOW_INSTANCE         — e.g. mycompany.service-now.com
    SNOW_API_PATH         — e.g. api/now/table/change_request
    SNOW_TOKEN_ENDPOINT   — e.g. https://mycompany.service-now.com/oauth_token.do
    SNOW_ENABLED          — true | false  (default: true)
    SONAR_URL             — e.g. https://sonar.internal
    GENIE_REPORT_LINK     — Genie API base URL
    PROXY_IP              — Optional corporate proxy (e.g. http://10.x.x.x:8080)
    TDA_OUTPUT_DIR        — Directory for JSON output files (default: /tmp/tda-output)
"""

from __future__ import annotations

import os
import sys
from typing import Optional

from service.vault_client import Credentials
from service.stream_config import StreamConfig

# ---------------------------------------------------------------------------
# Ensure the tda package is importable.
# In the marketplace repo the tda/ package lives under dtp-tda-report/scripts/.
# In a production deployment it should be installed as a package (pip install -e .)
# or placed on PYTHONPATH.  The TDA_PKG_PATH env var allows explicit override.
# ---------------------------------------------------------------------------

_TDA_PKG_PATH = os.environ.get(
    "TDA_PKG_PATH",
    os.path.normpath(
        os.path.join(
            os.path.dirname(__file__),          # service/
            "..", "..",                         # plugins/test/
            "dtp-tda-report",
            "skills", "dtp-tda-report", "scripts",
        )
    ),
)
if _TDA_PKG_PATH not in sys.path:
    sys.path.insert(0, _TDA_PKG_PATH)

from tda.config import Config  # noqa: E402  (must come after sys.path manipulation)


def build_tda_config(
    credentials: Credentials,
    stream_cfg: StreamConfig,
) -> Config:
    """Construct a tda.config.Config suitable for the tda.* collectors.

    All values that previously came from .env are sourced from Vault credentials
    or server infrastructure env vars.  Stream-specific overrides are merged from
    the StreamConfig.
    """
    # Inject credentials into os.environ so that tda.config.Config.from_env()
    # can read them.  We set only the variables actually consumed by Config and
    # the integrations — nothing else is written to the environment.
    # Variable names must match exactly what tda.config.Config.from_env() reads.
    _env_overrides = {
        # Credentials from Vault
        "ADO_TOKEN":             credentials.ado_token,
        "SONAR_TOKEN":           credentials.sonar_token,
        "GENIE_TOKEN":           credentials.genie_token,
        "CONFLUENCE_TOKEN":      credentials.confluence_token,
        "USER_EMAIL":            credentials.confluence_user,
        "CLIENT_ID":             credentials.snow_client_id,
        "FERNET_KEY":            credentials.snow_fernet_key,
        "SNOW_BLADE_KEY":        credentials.snow_blade_key,

        # Infrastructure env vars — names match tda.config.Config.from_env() exactly
        "ADO_ORGANIZATION":      os.environ.get("ADO_ORGANIZATION", "sc-ado"),
        "ADO_PROJECT":           os.environ.get("ADO_PROJECT", "FMQPR"),
        "CONFLUENCE_URL":        os.environ.get("CONFLUENCE_URL", ""),
        "CONFLUENCE_SPACE_KEY":  os.environ.get("CONFLUENCE_SPACE_KEY", "DTP"),
        "SN_INSTANCE":           os.environ.get("SN_INSTANCE", "scbnow01.service-now.com"),
        "SNOW_API_PATH":         os.environ.get("SNOW_API_PATH", "api/x_235492_api_fra_0/api_framework/getapi/getChanges"),
        "SNOW_ENABLED":          os.environ.get("SNOW_ENABLED", "true"),
        "SONAR_URL":             os.environ.get("SONAR_URL", ""),
        "GENIE_REPORT_LINK":     os.environ.get("GENIE_REPORT_LINK", ""),
        "HTTPS_PROXY":           os.environ.get("HTTPS_PROXY", ""),
        "PARALLEL_ENABLED":      os.environ.get("PARALLEL_ENABLED", "true"),
        "ADO_THROTTLE_DELAY_MS": os.environ.get("ADO_THROTTLE_DELAY_MS", "0"),
    }
    for key, value in _env_overrides.items():
        if value:
            os.environ[key] = value

    cfg = Config.from_env()

    # story_comments_enabled has no environment-variable fallback in tda.config
    # (Config.from_env() only picks it up via stream_config.yaml when a
    # release_stream is passed in, which we deliberately don't do here since
    # the service uses its own StreamConfig as the source of truth). Apply the
    # per-stream override explicitly, same pattern as sonar_stream_config below.
    cfg.story_comments_enabled = stream_cfg.story_comments_enabled

    # Apply stream-level Sonar key overrides if provided.
    # These are merged into the sonar_stream_config attribute that
    # build_resolver / collect_release_data expect.
    if stream_cfg.sonar_key_overrides:
        if not hasattr(cfg, "sonar_stream_config"):
            cfg.sonar_stream_config = {}  # type: ignore[attr-defined]
        cfg.sonar_stream_config.update(stream_cfg.sonar_key_overrides)  # type: ignore[attr-defined]

    return cfg
