"""tda/config.py — Configuration loading for AutoTDAScript.

Responsibilities:
- Load .env into os.environ (must run first, before any os.environ references)
- Decrypt SNOW credentials via Fernet
- Load ado_field_config.yaml (WI field key lists + extended Genie/story fields)
- Expose all environment-sourced constants as a single Config dataclass

Nothing in this module makes HTTP calls.  It is safe to import in tests with a
mocked environment.
"""

from __future__ import annotations

import base64
import logging
import os
import yaml
from dataclasses import dataclass, field
from functools import lru_cache
from cryptography.fernet import Fernet


# ---------------------------------------------------------------------------
# .env loader — call once at process startup
# ---------------------------------------------------------------------------

def load_env_file(path: str | None = None) -> None:
    """Load a .env file into os.environ.  .env always wins over the shell."""
    env_path = path or os.path.join(os.getcwd(), '.env')
    env_path = os.path.normpath(env_path)
    print(f"[env] Looking for .env at: {env_path}", flush=True)
    if not os.path.exists(env_path):
        # Fallback: look in the scripts/ directory that contains this file,
        # so the script works regardless of which directory it is invoked from.
        script_dir = os.path.dirname(os.path.abspath(__file__))
        fallback = os.path.normpath(os.path.join(script_dir, '..', '.env'))
        if os.path.exists(fallback):
            print(f"[env] ⚠️  Not found in cwd — falling back to: {fallback}", flush=True)
            env_path = fallback
        else:
            print("[env] ❌ Not found — relying on shell environment variables.", flush=True)
            return
    loaded = []
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            key, _, value = line.partition('=')
            val = value.strip()
            # Support quoted values in .env (e.g. TOKEN='abc123').
            if len(val) >= 2 and val[0] == val[-1] and val[0] in ("'", '"'):
                val = val[1:-1]
            os.environ[key.strip()] = val
            loaded.append(key.strip())
    print(f"[env] OK Loaded {len(loaded)} variable(s): {loaded}", flush=True)


# ---------------------------------------------------------------------------
# Per-stream SNOW_ENABLED override (stream_config.yaml)
# ---------------------------------------------------------------------------

@lru_cache(maxsize=1)
def _load_stream_config_yaml() -> dict:
    """Load stream_config.yaml if present (mandatory, stream-centric config
    file). Returns {} when absent, so any stream without an entry there
    transparently falls back to the SNOW_ENABLED environment variable.
    Cached for the life of the process.
    """
    path = _find_config_file('stream_config.yaml')
    if path is None:
        return {}
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f) or {}


def _snow_enabled_for_stream(release_stream: str | None) -> bool:
    """Effective SNOW_ENABLED for this run.

    Priority: stream_config.yaml's ``streams.<STREAM>.snow_enabled`` when
    explicitly set for the given stream, otherwise the SNOW_ENABLED
    environment variable (default 'true'). ``release_stream=None`` (e.g. for
    callers that don't know the stream yet, such as probe scripts) always
    uses the environment variable.
    """
    env_default = os.environ.get('SNOW_ENABLED', 'true').strip().lower() == 'true'
    if not release_stream:
        return env_default
    stream_cfg = (_load_stream_config_yaml().get('streams') or {}).get(release_stream.upper())
    if stream_cfg is not None and 'snow_enabled' in stream_cfg:
        return bool(stream_cfg['snow_enabled'])
    return env_default


def _story_comments_enabled_for_stream(release_stream: str | None) -> bool:
    """Effective story-last-comment fetch flag for this run.

    Controls whether ``get_story_items_in_release`` issues a
    ``CommentByStoryId`` ADO call for every story WI in the release (one
    extra request per story). This is opt-in and **defaults to False** —
    unlike SNOW, there is no environment-variable fallback; a stream must
    explicitly set ``streams.<STREAM>.story_comments_enabled: true`` in
    stream_config.yaml to turn it on. ``release_stream=None`` always
    returns False (disabled).
    """
    if not release_stream:
        return False
    stream_cfg = (_load_stream_config_yaml().get('streams') or {}).get(release_stream.upper())
    if stream_cfg is not None and 'story_comments_enabled' in stream_cfg:
        return bool(stream_cfg['story_comments_enabled'])
    return False


def _po_reprioritization_check_enabled_for_stream(release_stream: str | None) -> bool:
    """Effective post-prioritization Description/AC change check flag for this run.

    Controls whether ``get_story_items_in_release`` issues a
    ``WorkItemUpdates`` (revision history) ADO call for every story WI in the
    release, to detect Description/Acceptance Criteria edits made *after* the
    story transitioned into the 'Prioritized' state (a PO re-prioritization
    governance check). One extra request per story WI. This is opt-in and
    **defaults to False** — like story_comments_enabled, there is no
    environment-variable fallback; a stream must explicitly set
    ``streams.<STREAM>.po_reprioritization_check_enabled: true`` in
    stream_config.yaml to turn it on. ``release_stream=None`` always returns
    False (disabled).
    """
    if not release_stream:
        return False
    stream_cfg = (_load_stream_config_yaml().get('streams') or {}).get(release_stream.upper())
    if stream_cfg is not None and 'po_reprioritization_check_enabled' in stream_cfg:
        return bool(stream_cfg['po_reprioritization_check_enabled'])
    return False


# ---------------------------------------------------------------------------
# SNOW credential decryption
# ---------------------------------------------------------------------------

def decrypt_snow_credentials(release_stream: str | None = None) -> bool:
    """Decrypt the SNOW client secret using Fernet if SNOW is enabled.

    ``release_stream``, when supplied, allows a per-stream override of
    SNOW_ENABLED via stream_config.yaml (``streams.<STREAM>.snow_enabled``).
    Falls back to the SNOW_ENABLED environment variable when the stream has
    no override, or when no stream is supplied.

    Returns True when SNOW is enabled (credentials decrypted and stored in
    os.environ['CLIENT_SECRET']), False when disabled.
    """
    snow_enabled = _snow_enabled_for_stream(release_stream)
    if not snow_enabled:
        print(
            "[SNOW] SNOW disabled for this run — skipping Fernet decryption. "
            "FERNET_KEY, SNOW_BLADE_KEY, CLIENT_ID and CLIENT_SECRET are not required.",
            flush=True,
        )
        return False

    fernet_key = os.environ['FERNET_KEY'].strip().strip("'").strip('"').encode()
    snow_key   = os.environ['SNOW_BLADE_KEY'].strip().strip("'").strip('"').encode()
    fernet     = Fernet(fernet_key)
    os.environ['CLIENT_SECRET'] = fernet.decrypt(snow_key).decode('utf-8')
    print("[SNOW] SNOW enabled for this run — CLIENT_SECRET decrypted successfully.", flush=True)
    return True


# ---------------------------------------------------------------------------
# ADO field config (ado_field_config.yaml)
# ---------------------------------------------------------------------------

_ADO_FIELD_DEFAULTS: dict = {
    'release_wi_keys': [
        'id', 'fields-Custom.ApplicationID',
        'fields-System.State', 'fields-System.Title',
        'fields-Custom.POApproval', 'fields-Custom.TSOApproval',
        'fields-Custom.TSUOApproval', 'fields-Custom.CHGID',
        'fields-Custom.ADOCHGID',
        'fields-Custom.ImpactedCountries', 'fields-Custom.AIGandRollbackdocumentLink',
        'fields-Custom.ReleasePTPlanDocumentLink', 'fields-Custom.ReleasePTReportDocumentLink',
        'fields-Custom.RationaleforNotdoingPerformanceTesting', 'fields-Custom.Testingtypeinscope',
        'fields-Custom.LatestPipelineRuns',
    ],
    'remove_release_level_keys': [
        'Custom.ReleasePTPlanDocumentLink',
        'Custom.ReleasePTReportDocumentLink',
        'Custom.RationaleforNotdoingPerformanceTesting',
        'Custom.Testingtypeinscope',
        'Custom.LatestPipelineRuns',
    ],
    'application_wi_keys': [
        'fields-System.Title', 'fields-System.State',
        'fields-Custom.ApplicationArchitectureApprovalExpiryDate',
        'fields-Custom.ASRMApprovalExpiryDate', 'fields-Custom.NFRApprovalExpiryDate',
        'fields-Custom.TEMApprovalExpiryDate',
        'fields-Custom.TestStrategyApprovalExpiryDate',
    ],
    'bug_wi_keys': [
        'id', 'fields-System.State',
        'fields-Custom.TestPhase', 'fields-Custom.ImpactedEnvironment',
        # Raw text (HTML-stripped, truncated) kept for informational
        # Description/AC quality review — NOT_FOUND gracefully when absent.
        'fields-System.Description',
        'fields-Microsoft.VSTS.Common.AcceptanceCriteria',
    ],
    # Extended fields
    'story_type_field':            'Custom.StoryType',
    'story_application_id_field':  'Custom.ApplicationID',
    'test_type_field':             'Custom.TestType',
    'genie_system_test_tags':      ['@tt_ST', '@tt_st'],
    'genie_integration_test_tags': ['@tt_IT', '@tt_it'],
    'genie_story_link_prefix':     '@AB#',
    'snow_fields':                 ['short_description', 'description', 'type', 'state', 'impact', 'priority', 'risk'],
}


def _find_config_file(filename: str) -> str | None:
    """Search CWD then script directory for a config file. Returns path or None."""
    import sys
    candidates = [
        os.path.join(os.getcwd(), filename),
        os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), filename),
    ]
    return next((p for p in candidates if os.path.exists(p)), None)


def load_ado_field_config() -> dict:
    """Load ado_field_config.yaml, falling back to built-in defaults for any missing section.

    Returns the merged config dict containing all default keys.
    """
    config_file = 'ado_field_config.yaml'
    yaml_path = _find_config_file(config_file)

    if yaml_path is None:
        print(
            f"[ado_field_config] ⚠️  {config_file} not found — using built-in defaults.",
            flush=True,
        )
        return dict(_ADO_FIELD_DEFAULTS)

    with open(yaml_path, 'r', encoding='utf-8') as f:
        cfg = yaml.safe_load(f) or {}

    # For list sections, fall back to defaults when the section is missing/empty
    for section in ('release_wi_keys', 'remove_release_level_keys',
                    'application_wi_keys', 'bug_wi_keys'):
        if not cfg.get(section):
            print(
                f"[ado_field_config] ⚠️  Section '{section}' missing — using built-in default.",
                flush=True,
            )
            cfg[section] = _ADO_FIELD_DEFAULTS[section]

    # Scalar extended fields — fill from defaults when absent
    for key in ('story_type_field', 'story_application_id_field', 'test_type_field',
                'genie_system_test_tags', 'genie_integration_test_tags',
                'genie_story_link_prefix', 'snow_fields'):
        cfg.setdefault(key, _ADO_FIELD_DEFAULTS[key])

    print(f"[ado_field_config] ✅ Loaded from {yaml_path}", flush=True)
    logging.info("load_ado_field_config: loaded from %s", yaml_path)
    return cfg


# ---------------------------------------------------------------------------
# Config dataclass — single source of truth for all run-time constants
# ---------------------------------------------------------------------------

@dataclass
class Config:
    """All environment-sourced and file-sourced constants for one TDA run.

    Construct via ``Config.from_env()`` after calling ``load_env_file()``.
    """

    # ADO
    ado_token: str
    ado_organization: str
    ado_project: str
    ado_base_url: str
    ado_headers: dict

    # SNOW
    snow_enabled: bool
    snow_instance: str
    snow_api_path: str
    snow_token_endpoint: str
    snow_client_id: str
    snow_client_secret: str
    snow_fields: list

    # Sonar
    sonar_url: str
    sonar_token: str

    # Confluence
    confluence_url: str
    confluence_token: str
    confluence_user: str
    confluence_space_key: str

    # Genie
    genie_token: str
    genie_report_link: str
    genie_st_tags: set
    genie_it_tags: set
    genie_story_link_prefix: str

    # ADO WI field key lists
    release_wi_keys: list
    remove_release_level_keys: list
    application_wi_keys: list
    bug_wi_keys: list
    story_type_field: str
    story_app_id_field: str
    test_type_field: str

    # Proxy
    proxy_ip: str

    # Runtime flags (defaults; overridden from CLI args)
    parallel_enabled: bool = True
    snow_sn_instance: str = ''
    story_comments_enabled: bool = False
    po_reprioritization_check_enabled: bool = False
    ado_throttle_delay_ms: float = 0.0
    genie_timeout_seconds: float = 60.0
    # New Genie "test-management" API (per-stream opt-in, see
    # tda/integrations/genie_test_management.py) — base URL template with
    # {application_id}/{release_id} placeholders. Pagination contract is
    # NOT YET CONFIRMED (see module docstring) so this integration only
    # fetches a single page for now.
    genie_test_management_url_template: str = (
        'https://report.genie.cloud.sc.net/api/test-management/'
        'applications/{application_id}/releases/{release_id}/test-results/_latest'
    )
    # Artifactory build-info properties lookup base URL — used ONLY by the
    # opt-in 'artifactory_build_discovery_enabled' per-stream flag in
    # stream_config.yaml (tda/build_resolver.py's _resolve_builds_via_artifactory()).
    # Internal SC host, no auth/proxy needed for helm3/maven repos (confirmed
    # 2026-08-06) — docker-sc-release_local returns 401 and is intentionally
    # NOT queried by that code path.
    artifactory_base_url: str = 'https://artifactory.global.standardchartered.com/artifactory/api/storage'

    # SC Wiki (optional, future Confluence-replacement integration — see
    # tda/integrations/scwiki.py). Not required by any collector today; empty
    # defaults mean existing .env files without these keys keep working.
    scwiki_url: str = ''
    scwiki_api_key: str = ''
    scwiki_wiki_name: str = 'xwiki'

    @classmethod
    def from_env(cls, release_stream: str | None = None) -> 'Config':
        """Build a Config from the current process environment.

        Call ``load_env_file()`` and ``decrypt_snow_credentials()`` first.
        ``release_stream``, when supplied, allows stream_config.yaml to
        override SNOW_ENABLED for that specific stream (see
        ``_snow_enabled_for_stream``). Must match the value passed to
        ``decrypt_snow_credentials()`` so CLIENT_SECRET decryption and the
        resulting Config agree on whether SNOW is enabled.
        """
        snow_enabled = _snow_enabled_for_stream(release_stream)
        ado_token = os.environ['ADO_TOKEN']
        organization = os.environ['ADO_ORGANIZATION']
        project = os.environ['ADO_PROJECT']
        base_url = f'https://dev.azure.com/{organization}/{project}/_apis/'
        ado_headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic ' + base64.b64encode((':' + ado_token).encode()).decode(),
        }

        field_cfg = load_ado_field_config()

        parallel_env = os.environ.get('PARALLEL_ENABLED', 'true').strip().lower() == 'true'
        try:
            throttle_delay_ms = float(os.environ.get('ADO_THROTTLE_DELAY_MS', '0').strip() or '0')
        except ValueError:
            logging.warning(
                "Config.from_env: ADO_THROTTLE_DELAY_MS='%s' is not a valid number — "
                "defaulting to 0 (throttle disabled).",
                os.environ.get('ADO_THROTTLE_DELAY_MS'),
            )
            throttle_delay_ms = 0.0

        try:
            genie_timeout_seconds = float(os.environ.get('GENIE_TIMEOUT_SECONDS', '60').strip() or '60')
        except ValueError:
            logging.warning(
                "Config.from_env: GENIE_TIMEOUT_SECONDS='%s' is not a valid number — "
                "defaulting to 60.",
                os.environ.get('GENIE_TIMEOUT_SECONDS'),
            )
            genie_timeout_seconds = 60.0

        return cls(
            ado_token=ado_token,
            ado_organization=organization,
            ado_project=project,
            ado_base_url=base_url,
            ado_headers=ado_headers,

            snow_enabled=snow_enabled,
            snow_instance=os.environ.get('SN_INSTANCE', 'scbnow01.service-now.com'),
            snow_api_path=os.environ.get('SNOW_API_PATH', 'api/x_235492_api_fra_0/api_framework/getapi/getChanges'),
            snow_token_endpoint=f"https://{os.environ.get('SN_INSTANCE', 'scbnow01.service-now.com')}/oauth_token.do",
            snow_client_id=os.environ.get('CLIENT_ID', '') if snow_enabled else '',
            snow_client_secret=os.environ.get('CLIENT_SECRET', '') if snow_enabled else '',
            snow_fields=field_cfg.get('snow_fields', _ADO_FIELD_DEFAULTS['snow_fields']),

            sonar_url=os.environ['SONAR_URL'],
            sonar_token=os.environ['SONAR_TOKEN'],

            confluence_url=os.environ['CONFLUENCE_URL'].strip(),
            confluence_token=os.environ['CONFLUENCE_TOKEN'].strip(),
            confluence_user=os.environ.get('USER_EMAIL', '').strip(),
            confluence_space_key=os.environ.get('CONFLUENCE_SPACE_KEY', 'DTP'),

            genie_token=os.environ['GENIE_TOKEN'],
            genie_report_link=os.environ['GENIE_REPORT_LINK'],
            genie_st_tags=set(field_cfg['genie_system_test_tags']),
            genie_it_tags=set(field_cfg['genie_integration_test_tags']),
            genie_story_link_prefix=field_cfg['genie_story_link_prefix'],

            release_wi_keys=field_cfg['release_wi_keys'],
            remove_release_level_keys=field_cfg['remove_release_level_keys'],
            application_wi_keys=field_cfg['application_wi_keys'],
            bug_wi_keys=field_cfg['bug_wi_keys'],
            story_type_field=field_cfg['story_type_field'],
            story_app_id_field=field_cfg['story_application_id_field'],
            test_type_field=field_cfg['test_type_field'],

            proxy_ip=os.environ.get('HTTPS_PROXY', ''),
            parallel_enabled=parallel_env,
            snow_sn_instance=os.environ.get('SN_INSTANCE', 'scbnow01.service-now.com'),
            story_comments_enabled=_story_comments_enabled_for_stream(release_stream),
            po_reprioritization_check_enabled=_po_reprioritization_check_enabled_for_stream(release_stream),
            ado_throttle_delay_ms=throttle_delay_ms,
            genie_timeout_seconds=genie_timeout_seconds,
            genie_test_management_url_template=os.environ.get(
                'GENIE_TEST_MANAGEMENT_URL_TEMPLATE',
                'https://report.genie.cloud.sc.net/api/test-management/'
                'applications/{application_id}/releases/{release_id}/test-results/_latest',
            ),
            artifactory_base_url=os.environ.get(
                'ARTIFACTORY_BASE_URL',
                'https://artifactory.global.standardchartered.com/artifactory/api/storage',
            ),

            scwiki_url=os.environ.get('SCWIKI_URL', '').strip(),
            scwiki_api_key=os.environ.get('SCWIKI_API_KEY', '').strip(),
            scwiki_wiki_name=(os.environ.get('SCWIKI_WIKI_NAME', 'xwiki').strip() or 'xwiki'),
        )
