"""Read bounded migration inputs and fetch JSON without retaining credentials.

This optional source adapter supports the inspected matrix and HTTP collection
formats. It neither supplies tenant endpoints nor establishes source authority.
"""

from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
import hashlib
import json
from pathlib import Path
import posixpath
import re
import socket
import ssl
import time
from typing import Any, Mapping
from urllib import error, parse, request
import xml.etree.ElementTree as ET
from zipfile import BadZipFile, ZipFile

from .entitlement_reconciliation import ReconciliationError, split_user_ids


class SourceError(ValueError):
    """A source failed acquisition or validation; its contents are not empty."""

    def __init__(self, code: str, status: int | None = None):
        self.code = code
        self.status = status
        super().__init__(code if status is None else f"{code} (HTTP {status})")


_XML = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
_REL = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
_MAX_INPUT = 32 * 1024 * 1024


def _name(value: Any) -> str:
    return str(value).strip() if value is not None else ""


def _read_zip_xml(archive: ZipFile, name: str) -> ET.Element:
    info = archive.getinfo(name)
    if info.file_size > _MAX_INPUT:
        raise SourceError("MATRIX_TOO_LARGE")
    raw = archive.read(name)
    if b"<!DOCTYPE" in raw.upper() or b"<!ENTITY" in raw.upper():
        raise SourceError("INVALID_MATRIX_XML")
    return ET.fromstring(raw)


def _matrix_rows(path: Path) -> dict[str, dict[int, dict[int, Any]]]:
    """Read shared, inline, numeric, and sparse cells without Excel libraries."""
    try:
        with ZipFile(path) as archive:
            if sum(info.file_size for info in archive.infolist()) > 4 * _MAX_INPUT:
                raise SourceError("MATRIX_TOO_LARGE")
            shared: list[str] = []
            if "xl/sharedStrings.xml" in archive.namelist():
                strings = _read_zip_xml(archive, "xl/sharedStrings.xml")
                shared = [
                    "".join(node.text or "" for node in item.iter(_XML + "t"))
                    for item in strings.findall(_XML + "si")]
            relations = _read_zip_xml(archive, "xl/_rels/workbook.xml.rels")
            targets = {}
            for relation in relations:
                target = relation.attrib.get("Target", "")
                if relation.attrib.get("TargetMode") == "External":
                    continue
                target = target.lstrip("/") if target.startswith("/") else posixpath.normpath("xl/" + target)
                if not target.startswith("xl/") or "/../" in target:
                    raise SourceError("INVALID_MATRIX_RELATIONSHIP")
                targets[relation.attrib["Id"]] = target
            workbook = _read_zip_xml(archive, "xl/workbook.xml")
            sheets = workbook.find(_XML + "sheets")
            if sheets is None:
                raise SourceError("INVALID_MATRIX")
            result: dict[str, dict[int, dict[int, Any]]] = {}
            for sheet in sheets:
                sheet_name = sheet.attrib["name"]
                # Only these sheets participate in this adapter's contract.
                if sheet_name not in {"Application", "Feature", "Entitlement", "EntitlementFeatureAction", "UserEntitlement"}:
                    continue
                target = targets[sheet.attrib[_REL + "id"]]
                tree = _read_zip_xml(archive, target)
                rows: dict[int, dict[int, Any]] = {}
                for row in tree.iter(_XML + "row"):
                    row_number = int(row.attrib["r"])
                    cells = {}
                    for cell in row.findall(_XML + "c"):
                        reference = re.fullmatch(r"([A-Z]+)([1-9][0-9]*)", cell.attrib.get("r", ""))
                        if reference is None:
                            raise SourceError("INVALID_MATRIX_CELL")
                        column = 0
                        for letter in reference.group(1):
                            column = column * 26 + ord(letter) - ord("A") + 1
                        kind = cell.attrib.get("t")
                        value_node = cell.find(_XML + "v")
                        value = value_node.text if value_node is not None else None
                        if kind == "s":
                            value = shared[int(value)]
                        elif kind == "inlineStr":
                            value = "".join(node.text or "" for node in cell.iter(_XML + "t"))
                        elif kind == "b":
                            value = value == "1"
                        elif kind == "e":
                            raise SourceError("MATRIX_CELL_ERROR")
                        elif value is not None and kind not in {"str", "d"}:
                            # Integral numbers remain exact even beyond float precision.
                            number = Decimal(value)
                            if not number.is_finite():
                                raise SourceError("INVALID_MATRIX_NUMBER")
                            value = int(number) if number == number.to_integral_value() else float(number)
                        if cell.find(_XML + "f") is not None and value is None:
                            raise SourceError("MATRIX_FORMULA_WITHOUT_VALUE")
                        cells[column - 1] = value
                    if any(value not in {None, ""} for value in cells.values()):
                        rows[row_number] = cells
                result[sheet_name] = rows
            return result
    except SourceError:
        raise
    except (OSError, BadZipFile, KeyError, ValueError, TypeError, IndexError, InvalidOperation, ET.ParseError) as exc:
        raise SourceError("INVALID_MATRIX") from exc


def read_matrix(path: str | Path) -> dict[str, Any]:
    """Read the inspected seven-sheet conversion format without changing it."""
    path = Path(path)
    rows = _matrix_rows(path)
    required = {"Application": {0: "ITAM_ID", 2: "APPNAME"},
                "Feature": {0: "FEATURENAME"},
                "Entitlement": {0: "ENTITLEMENTNAME", 3: "APPLICATIONNAME"},
                "EntitlementFeatureAction": {0: "ENTITLEMENTNAME", 1: "APPLICATIONNAME", 2: "FEATURENAME", 3: "ACTIONNAME"},
                "UserEntitlement": {0: "USERNAME", 1: "ENTITLEMENTNAME", 4: "APPNAME"}}
    for sheet, headers in required.items():
        if sheet not in rows or any(_name(rows[sheet].get(1, {}).get(index)) != name for index, name in headers.items()):
            raise SourceError("UNSUPPORTED_MATRIX_FORMAT")
    applications = [row for index, row in rows["Application"].items() if index >= 2]
    if len(applications) != 1:
        raise SourceError("MATRIX_APPLICATION_SCOPE")
    app = _name(applications[0].get(2)); itam_id = _name(applications[0].get(0))
    if not app or not itam_id:
        raise SourceError("MATRIX_APPLICATION_SCOPE")
    profiles, grants, assignments, features = set(), set(), set(), set()
    for index, row in rows["Entitlement"].items():
        if index < 2: continue
        profile, scope = _name(row.get(0)), _name(row.get(3))
        if not profile or scope != app:
            raise SourceError("MATRIX_PROFILE_SCOPE")
        profiles.add((app, profile))
    for index, row in rows["Feature"].items():
        if index >= 2:
            feature = _name(row.get(0))
            if not feature: raise SourceError("MATRIX_FEATURE_NAME")
            features.add(feature)
    for index, row in rows["EntitlementFeatureAction"].items():
        if index < 2: continue
        profile, scope, feature, action = (_name(row.get(i)) for i in range(4))
        if not all((profile, feature, action)) or scope != app:
            raise SourceError("MATRIX_GRANT_SCOPE")
        grants.add((app, profile, feature, action))
    try:
        for index, row in rows["UserEntitlement"].items():
            if index < 3: continue
            users = split_user_ids(row.get(0))
            profile, scope = _name(row.get(1)), _name(row.get(4))
            if not users or not profile or scope != app:
                raise SourceError("MATRIX_ASSIGNMENT_SCOPE")
            assignments.update((user, app, profile) for user in users)
    except ReconciliationError as exc:
        raise SourceError("INVALID_MATRIX_IDENTITIES") from exc
    used_profiles = {(scope, profile) for _, scope, profile in assignments}
    grant_profiles = {(scope, profile) for scope, profile, _, _ in grants}
    return {"app": app, "itam_id": itam_id,
            "profiles": [list(value) for value in sorted(profiles)],
            "grants": [list(value) for value in sorted(grants)],
            "assignments": [list(value) for value in sorted(assignments)],
            "users": sorted({row[0] for row in assignments}), "features": sorted(features),
            "missing_profile_definitions": [list(value) for value in sorted(used_profiles - profiles)],
            "missing_profile_grants": [list(value) for value in sorted(used_profiles - grant_profiles)],
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def read_http_example(path: str | Path) -> dict[str, Any]:
    """Read request routing and embedded JSON; deliberately omit all headers."""
    try:
        import yaml
        raw = Path(path).read_bytes()
        if len(raw) > _MAX_INPUT:
            raise SourceError("COLLECTION_TOO_LARGE")
        collection = yaml.safe_load(raw)
        http = collection["http"]
        method, url = http["method"], http["url"]
        if method not in {"GET", "POST"} or not isinstance(url, str):
            raise SourceError("UNSUPPORTED_COLLECTION_REQUEST")
        def data(body):
            if body is None: return None
            if not isinstance(body, dict) or body.get("type") != "json":
                raise SourceError("UNSUPPORTED_COLLECTION_BODY")
            value = body.get("data")
            if isinstance(value, str):
                return json.loads(value) if value.strip() else None
            return value
        examples = collection.get("examples") or []
        example = examples[0] if examples else {}
        response = example.get("response") or {}
        return {"method": method, "url": url, "body": data(http.get("body")),
                "response": data(response.get("body")), "response_status": response.get("status"),
                "example_request_url": (example.get("request") or {}).get("url"),
                "sha256": hashlib.sha256(raw).hexdigest()}
    except SourceError:
        raise
    except ImportError as exc:
        raise SourceError("YAML_DEPENDENCY_UNAVAILABLE") from exc
    except (OSError, KeyError, TypeError, ValueError, AttributeError, yaml.YAMLError) as exc:
        raise SourceError("INVALID_COLLECTION") from exc


def load_root_env(workspace: str | Path) -> dict[str, str]:
    """Reuse the root dotenv contract; process variables override file values."""
    from .doctor import _environment
    environment, check = _environment(Path(workspace))
    if check["status"] != "READY":
        raise SourceError("INVALID_ROOT_ENVIRONMENT")
    return environment


def _redacted_url(url: str) -> str:
    parts = parse.urlsplit(url)
    host = parts.hostname or ""
    if ":" in host: host = "[" + host + "]"
    if parts.port: host += ":" + str(parts.port)
    query = parse.urlencode([(key, "REDACTED") for key, _ in parse.parse_qsl(parts.query, keep_blank_values=True)])
    return parse.urlunsplit((parts.scheme, host, parts.path, query, ""))


class _NoRedirect(request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class JsonHttpClient:
    """Fetch read-only JSON through bounded, verified, credential-private calls."""

    def __init__(self, env: Mapping[str, str], timeout: float = 15, retries: int = 1,
                 allow_http: bool = False, max_response_bytes: int = 16 * 1024 * 1024):
        if timeout <= 0 or retries < 0 or max_response_bytes <= 0:
            raise SourceError("INVALID_HTTP_LIMITS")
        self.env = dict(env); self.timeout = timeout; self.retries = retries
        self.allow_http = allow_http; self.max_response_bytes = max_response_bytes

    def request(self, method: str, url: str, body: Any = None, token_env: str | None = None,
                ca_env: str | None = None) -> dict[str, Any]:
        try:
            parts = parse.urlsplit(url)
            parts.port  # Validate a supplied port before starting acquisition.
            if parts.username is not None or parts.password is not None or not parts.hostname:
                raise SourceError("INVALID_HTTP_URL")
            loopback = parts.hostname.lower() in {"localhost", "127.0.0.1", "::1"}
            if parts.scheme != "https" and not (parts.scheme == "http" and self.allow_http and loopback):
                raise SourceError("HTTPS_REQUIRED")
            if method not in {"GET", "POST"}:
                raise SourceError("UNSUPPORTED_HTTP_METHOD")
            headers = {"Accept": "application/json", "Content-Type": "application/json"}
            if token_env:
                token = self.env.get(token_env, "").strip()
                if not token: raise SourceError("MISSING_CREDENTIAL")
                if "\r" in token or "\n" in token: raise SourceError("INVALID_CREDENTIAL")
                headers["Authorization"] = token if token.lower().startswith(("bearer ", "basic ")) else "Bearer " + token
            cafile = self.env.get(ca_env, "").strip() if ca_env else ""
            cafile = cafile or self.env.get("SSL_CERT_FILE", "").strip() or None
            try:
                context = ssl.create_default_context(cafile=cafile)
            except (OSError, ssl.SSLError) as exc:
                raise SourceError("TLS_CONFIGURATION") from exc
            proxies = {scheme: self.env.get(scheme.upper() + "_PROXY", self.env.get(scheme + "_proxy", ""))
                       for scheme in ("http", "https")}
            proxies = {key: value for key, value in proxies.items() if value}
            no_proxy = self.env.get("NO_PROXY", self.env.get("no_proxy", ""))
            if no_proxy and request.proxy_bypass_environment(parts.hostname, {"no": no_proxy}):
                proxies = {}
            opener = request.build_opener(request.ProxyHandler(proxies), request.HTTPSHandler(context=context), _NoRedirect())
            encoded = json.dumps(body).encode("utf-8") if body is not None else None
            req = request.Request(url, data=encoded, headers=headers, method=method)
        except SourceError:
            raise
        except (ValueError, TypeError) as exc:
            raise SourceError("INVALID_HTTP_REQUEST") from exc
        for attempt in range(self.retries + 1):
            try:
                with opener.open(req, timeout=self.timeout) as response:
                    raw = response.read(self.max_response_bytes + 1)
                    status = response.status
                    if len(raw) > self.max_response_bytes:
                        raise SourceError("RESPONSE_TOO_LARGE", status)
                    try:
                        value = json.loads(raw)
                    except (ValueError, UnicodeError) as exc:
                        raise SourceError("INVALID_JSON_RESPONSE", status) from exc
                    return {"data": value, "status": status,
                            "at": datetime.now(timezone.utc).isoformat(),
                            "url": _redacted_url(url), "sha256": hashlib.sha256(raw).hexdigest()}
            except error.HTTPError as exc:
                status = exc.code
                exc.close()
                if status in {408, 429, 500, 502, 503, 504} and attempt < self.retries:
                    time.sleep(min(0.25 * (2 ** attempt), 2))
                    continue
                raise SourceError("HTTP_ERROR", status) from None
            except SourceError:
                raise
            except (error.URLError, OSError, socket.timeout) as exc:
                reason = getattr(exc, "reason", exc)
                code = "TLS_ERROR" if isinstance(reason, (ssl.SSLError, ssl.CertificateError)) else "NETWORK_ERROR"
                if code == "NETWORK_ERROR" and attempt < self.retries:
                    time.sleep(min(0.25 * (2 ** attempt), 2))
                    continue
                raise SourceError(code) from None
        raise SourceError("NETWORK_ERROR")
