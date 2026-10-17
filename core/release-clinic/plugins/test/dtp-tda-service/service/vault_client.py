"""service/vault_client.py — HashiCorp Vault credential loader.

Authenticates to Vault using AppRole via direct HTTP (matching the pattern
from AutoTDAScript_Legacy.py) and reads each credential from its own KV path.

Vault layout (per existing dtp-tda-report setup):
    Auth:    POST  /v1/{namespace}/auth/approle/login
    Secrets: GET   /v1/{namespace}/{secret_base_path}/key_store_<name>
             field inside each path matches the key name (e.g. 'ado_token')

Environment variables:
    VAULT_ADDR             — Base URL  (e.g. https://vault-dev.sc.net:8200)
    VAULT_NAMESPACE        — Vault Enterprise namespace  (e.g. ccib)
    HC_ROLE_ID             — AppRole role_id
    HC_SECRET_ID           — AppRole secret_id
    HC_VAULT_AUTH_PATH     — Auth path relative to namespace
                             (default: auth/approle/login)
    HC_VAULT_SECRET_PATH   — Base KV data path
                             (default: 50665/dtpnp/app/kv/data)
    VAULT_DEV_MODE         — Set to 'true' to skip Vault and read from env vars
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass

import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Credentials dataclass
# ---------------------------------------------------------------------------

@dataclass
class Credentials:
    ado_token:         str
    sonar_token:       str
    genie_token:       str
    confluence_token:  str
    confluence_user:   str
    snow_client_id:    str
    snow_client_secret: str   # raw (already decrypted by Vault)
    snow_fernet_key:   str
    snow_blade_key:    str    # Fernet-encrypted SNOW client secret


# ---------------------------------------------------------------------------
# Vault client
# ---------------------------------------------------------------------------

class VaultClient:
    """Reads TDA service credentials from Vault using direct HTTP calls.

    Matches the authentication and secret-reading pattern from the original
    AutoTDAScript_Legacy.py Vault integration.
    """

    def __init__(self) -> None:
        self._addr        = os.environ.get("VAULT_ADDR", "https://vault-dev.sc.net:8200").rstrip("/")
        self._namespace   = os.environ.get("VAULT_NAMESPACE", "ccib")
        self._role_id     = os.environ.get("HC_ROLE_ID", "")
        self._secret_id   = os.environ.get("HC_SECRET_ID", "")
        self._auth_path   = os.environ.get("HC_VAULT_AUTH_PATH", "auth/approle/login")
        self._secret_path = os.environ.get("HC_VAULT_SECRET_PATH", "50665/dtpnp/app/kv/data")
        self._token: str | None = None

        # Proxy-free session for all Vault calls.
        self._session = requests.Session()
        self._session.trust_env = False
        self._session.proxies.clear()
        self._session.verify = False

    # ------------------------------------------------------------------
    # Connection
    # ------------------------------------------------------------------

    def connect(self) -> None:
        """Authenticate to Vault via AppRole and cache the client token."""
        url = f"{self._addr}/v1/{self._namespace}/{self._auth_path}"
        logger.info("Vault: authenticating at %s", url)
        response = self._session.post(
            url,
            json={"role_id": self._role_id, "secret_id": self._secret_id},
            headers={"Content-Type": "application/json"},
        )
        response.raise_for_status()
        self._token = response.json()["auth"]["client_token"]
        logger.info("Vault: authenticated successfully at %s", self._addr)

    @property
    def is_connected(self) -> bool:
        return self._token is not None

    # ------------------------------------------------------------------
    # Credential loading
    # ------------------------------------------------------------------

    def load_credentials(self) -> Credentials:
        """Read all TDA service credentials from Vault and return them.

        When VAULT_DEV_MODE=true, reads directly from environment variables
        instead of Vault.  Use only for local development.
        """
        if os.environ.get("VAULT_DEV_MODE", "false").lower() == "true":
            return self._load_from_env()

        if not self.is_connected:
            self.connect()

        def _read(key_store_name: str, field_name: str) -> str:
            """Fetch one secret from its individual Vault KV path."""
            url = f"{self._addr}/v1/{self._namespace}/{self._secret_path}/{key_store_name}"
            r = self._session.get(
                url,
                headers={"Authorization": f"Bearer {self._token}"},
            )
            if r.status_code == 403:
                raise RuntimeError(
                    f"Permission denied reading Vault secret '{key_store_name}'. "
                    "Ensure the AppRole policy grants read access to "
                    f"'{self._namespace}/{self._secret_path}/*'."
                )
            r.raise_for_status()
            return r.json()["data"]["data"][field_name]

        return Credentials(
            ado_token         = _read("key_store_ado_token",        "ado_token"),
            confluence_token  = _read("key_store_confluence_token", "confluence_token"),
            sonar_token       = _read("key_store_sonar_token",      "sonar_token"),
            snow_client_id    = _read("key_store_client_id",        "client_id"),
            snow_client_secret = _read("key_store_client_secret",   "client_secret"),
            genie_token       = _read("key_store_genie_token",      "genie_token"),
            snow_fernet_key   = _read("key_store_fernet_key",       "fernet_key"),
            snow_blade_key    = _read("key_store_snow_blade_key",   "snow_blade_key"),
            confluence_user   = os.environ.get("USER_EMAIL", ""),
        )

    def _load_from_env(self) -> Credentials:
        """Dev mode: load credentials from os.environ (already populated from .env)."""
        logger.warning(
            "VAULT_DEV_MODE=true — loading credentials from environment variables, not Vault. "
            "Do not use this in production."
        )
        return Credentials(
            ado_token          = os.environ["ADO_TOKEN"],
            sonar_token        = os.environ["SONAR_TOKEN"],
            genie_token        = os.environ["GENIE_TOKEN"],
            confluence_token   = os.environ["CONFLUENCE_TOKEN"],
            confluence_user    = os.environ["USER_EMAIL"],
            snow_client_id     = os.environ.get("CLIENT_ID", ""),
            snow_client_secret = os.environ.get("CLIENT_SECRET", ""),
            snow_fernet_key    = os.environ.get("FERNET_KEY", ""),
            snow_blade_key     = os.environ.get("SNOW_BLADE_KEY", ""),
        )
