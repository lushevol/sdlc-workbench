"""Read Eureka application instances through a configured HTTP endpoint."""

from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request

from ..models import Context, Operation, Resource
from .common import BuiltinProvider, ProviderError, object_schema, string_schema, timeout


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request, response, code, message, headers, new_url):
        return None


def _open_request(request: urllib.request.Request, seconds: float):
    return urllib.request.build_opener(_NoRedirect()).open(request, timeout=seconds)


class EurekaDiscoveryProvider(BuiltinProvider):
    id = "discovery.eureka"
    resource_kind = "discovery"
    operations = {"instances": Operation("instances", "Read Eureka application instances.", object_schema({
        "application": string_schema(maximum=256)}))}

    def _invoke(self, operation: str, resource: Resource, arguments: dict, context: Context) -> dict:
        value = resource.config.get("url")
        if not isinstance(value, str) or not value or len(value) > 4096:
            raise ProviderError("INVALID_CONFIGURATION", "The discovery resource needs an HTTP endpoint.")
        parsed = urllib.parse.urlsplit(value)
        if parsed.scheme not in {"http", "https"} or not parsed.hostname or parsed.username or parsed.password or parsed.query or parsed.fragment:
            raise ProviderError("INVALID_CONFIGURATION", "The discovery endpoint URL is invalid.")
        maximum = resource.config.get("max_response_bytes", 2 * 1024 * 1024)
        if isinstance(maximum, bool) or not isinstance(maximum, int) or not 1024 <= maximum <= 10 * 1024 * 1024:
            raise ProviderError("INVALID_CONFIGURATION", "The discovery response bound is invalid.")
        headers = {"Accept": "application/json"}
        token_name = resource.config.get("bearer_token_env")
        if token_name is not None:
            if not isinstance(token_name, str) or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", token_name):
                raise ProviderError("INVALID_CONFIGURATION", "The bearer token environment reference is invalid.")
            token = os.environ.get(token_name)
            if not token:
                raise ProviderError("CREDENTIAL_UNAVAILABLE", "The configured credential is unavailable.")
            if any(character in token for character in "\r\n\x00"):
                raise ProviderError("INVALID_CONFIGURATION", "The configured credential has an invalid format.")
            headers["Authorization"] = "Bearer " + token
        url = value.rstrip("/") + "/apps"
        if "application" in arguments:
            url += "/" + urllib.parse.quote(arguments["application"], safe="")
        request = urllib.request.Request(url, headers=headers, method="GET")
        try:
            with _open_request(request, timeout(context)) as response:
                raw = response.read(maximum + 1)
        except (urllib.error.URLError, TimeoutError, OSError):
            return {"status": "ERROR", "code": "DISCOVERY_UNAVAILABLE", "message": "The discovery endpoint could not supply a response."}
        if len(raw) > maximum:
            raise ProviderError("RESPONSE_TOO_LARGE", "The discovery response exceeds its configured bound.")
        try:
            payload = json.loads(raw)
        except (ValueError, UnicodeError) as error:
            raise ProviderError("INVALID_RESPONSE", "The discovery endpoint did not return valid JSON.") from error
        if not isinstance(payload, dict):
            raise ProviderError("INVALID_RESPONSE", "The discovery response must be a JSON object.")
        if "applications" in payload and isinstance(payload["applications"], dict):
            applications = payload["applications"].get("application", [])
        elif "application" in payload:
            applications = payload["application"]
        else:
            raise ProviderError("INVALID_RESPONSE", "The discovery response has no application collection.")
        if isinstance(applications, dict):
            applications = [applications]
        if not isinstance(applications, list) or any(not isinstance(application, dict) for application in applications):
            raise ProviderError("INVALID_RESPONSE", "The discovery application list is invalid.")
        instances = []
        for application in applications:
            members = application.get("instance", [])
            if isinstance(members, dict):
                members = [members]
            if not isinstance(members, list) or any(not isinstance(member, dict) for member in members):
                raise ProviderError("INVALID_RESPONSE", "The discovery instance list is invalid.")
            instances.extend({**member, "application": application.get("name")} for member in members)
        return {"status": "SUCCEEDED", "applications": applications, "instances": instances, "response_bytes": len(raw)}
