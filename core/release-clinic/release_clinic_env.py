"""Load Release Clinic settings from the selected Workbench root.

Process environment values take precedence over file values.
Default discovery uses this module's source location and ignores the caller's directory.
"""

from __future__ import annotations

import os
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit


_ALIASES = {
    "ADO_TOKEN": "AZURE_DEVOPS_PAT",
    "CONFLUENCE_URL": "CONFLUENCE_BASE_URL",
    "CONFLUENCE_TOKEN": "CONFLUENCE_PAT",
    "SONAR_URL": "SONAR_BASE_URL",
    "SCWIKI_API_KEY": "SCWIKI_TOKEN",
    "SCWIKI_WIKI_NAME": "SCWIKI_WIKI",
    "STREAM_CONFIG_FILE": "STREAM_CONFIG_PATH",
}


def workspace_path(value: str | os.PathLike[str]) -> Path:
    """Resolve a configured path from the selected workspace root."""
    path = Path(value).expanduser()
    return (path if path.is_absolute() else workspace_root() / path).resolve()


def ado_organization(url: str) -> str:
    """Derive an organization or collection name without changing its server URL."""
    parsed = urlsplit(url)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise ValueError("ADO_ORG_URL must be an absolute HTTP or HTTPS organization URL.")
    parts = [unquote(part) for part in parsed.path.split("/") if part]
    if parsed.hostname == "dev.azure.com":
        if not parts:
            raise ValueError("ADO_ORG_URL must include the Azure DevOps organization.")
        return parts[0]
    if parsed.hostname and parsed.hostname.endswith(".visualstudio.com"):
        return parsed.hostname.removesuffix(".visualstudio.com")
    return parts[-1] if parts else parsed.hostname or ""


def workspace_root() -> Path:
    """Return the explicit workspace or the enclosing standalone checkout."""
    configured = os.environ.get("AI_SDLC_WORKSPACE", "").strip()
    if configured:
        root = Path(configured).expanduser()
        if not root.is_absolute():
            raise ValueError("AI_SDLC_WORKSPACE must be an absolute workspace path.")
        if not root.is_dir():
            raise ValueError("AI_SDLC_WORKSPACE must select an existing directory.")
        return root.resolve()
    for root in Path(__file__).resolve().parents:
        if any((root / name).is_file() for name in ("workspace.yaml", "workspace.json")):
            return root
    raise ValueError("Set AI_SDLC_WORKSPACE to the absolute workspace root.")


def load_environment(path: str | os.PathLike[str] | None = None) -> tuple[str | None, list[str]]:
    """Load root settings and return the selected file and applied variable names.

    An explicit file path resolves from the workspace root.
    Missing explicit files fail without selecting a fallback file.
    """
    root = workspace_root()
    selected = path or os.environ.get("AI_SDLC_ENV_FILE", "").strip()
    env_path = Path(selected).expanduser() if selected else root / ".env"
    if not env_path.is_absolute():
        env_path = root / env_path
    env_path = env_path.resolve()
    if not env_path.is_file():
        if selected:
            raise FileNotFoundError(f"Environment file not found: {env_path}")
        file_values = {}
        selected_path = None
    else:
        file_values = _read_environment(env_path)
        selected_path = str(env_path)

    # Resolve aliases from their original source. A process alias must override a file legacy key.
    process_values = dict(os.environ)
    loaded = []
    for key, value in file_values.items():
        if key not in os.environ:
            os.environ[key] = value
            loaded.append(key)
    for target, alias in _ALIASES.items():
        for source in (process_values, file_values):
            if target in source or alias in source:
                os.environ[target] = source[target] if target in source else source[alias]
                break
    for source in (process_values, file_values):
        if not any(name in source for name in ("ADO_ORG_URL", "ADO_ORGANIZATION", "AZURE_DEVOPS_ORG_URL")):
            continue
        if "ADO_ORG_URL" in source:
            url = source["ADO_ORG_URL"].strip().rstrip('/')
            organization = source.get("ADO_ORGANIZATION", "") or (ado_organization(url) if url else "")
        elif "ADO_ORGANIZATION" in source:
            organization = source["ADO_ORGANIZATION"]
            url = f"https://dev.azure.com/{organization}" if organization else ""
        else:
            url = source["AZURE_DEVOPS_ORG_URL"].strip().rstrip('/')
            organization = ado_organization(url) if url else ""
        os.environ["ADO_ORG_URL"] = url
        os.environ["ADO_ORGANIZATION"] = organization
        break

    defaults = {
        "TDA_OUTPUT_DIR": ".workbench/release-clinic/reports",
        "TDA_LOG_DIR": ".workbench/release-clinic/logs",
    }
    for name in ("TDA_STREAM_CONFIG", "TDA_FIELD_CONFIG", "TDA_OUTPUT_DIR", "TDA_LOG_DIR", "TDA_REGISTRY_PATH",
                 "STREAM_CONFIG_FILE", "STREAM_CONFIG_PATH"):
        value = os.environ.get(name, "").strip()
        if not value:
            value = defaults.get(name, "")
        if value:
            os.environ[name] = str(workspace_path(value))

    # Requests checks the lowercase variant first. Preserve an explicit value.
    if "NO_PROXY" in os.environ:
        os.environ.setdefault("no_proxy", os.environ["NO_PROXY"])
    return selected_path, loaded


def _read_environment(env_path: Path) -> dict[str, str]:
    """Read simple dotenv assignments without interpolation or command execution."""
    values = {}
    for line in env_path.read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()
        if line.startswith("export "):
            line = line[7:].lstrip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", key):
            continue
        value = value.strip()
        if len(value) >= 2 and value[0] in ("'", '"'):
            quote = value[0]
            end = value.find(quote, 1)
            if end != -1:
                value = value[1:end]
        else:
            value = re.split(r"\s+#", value, maxsplit=1)[0].rstrip()
        values[key] = value
    return values
