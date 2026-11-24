"""Rundeck 5.10 direct-REST client. No API tokens; no third-party dependencies."""
import json
import re
import ssl
import uuid
from http.cookiejar import CookieJar
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlsplit, quote
from urllib.request import Request, build_opener, HTTPCookieProcessor, HTTPRedirectHandler, HTTPSHandler


class RundeckError(Exception):
    pass


class AuthenticationError(RundeckError):
    pass


class SafeRedirectHandler(HTTPRedirectHandler):
    """Never send login credentials or session cookies to another origin."""
    def __init__(self, base_url):
        self.parts = urlsplit(base_url)
        self.context = self.parts.path.rstrip("/")

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        dest = urlsplit(newurl)
        if (dest.scheme, dest.netloc) != (self.parts.scheme, self.parts.netloc):
            raise AuthenticationError("Cross-origin redirect refused")
        # A Rundeck instance may be hosted under /rundeck; reject redirects outside it.
        if self.context and not (dest.path == self.context or dest.path.startswith(self.context + "/")):
            raise AuthenticationError("Redirect escaped Rundeck context path")
        if dest.path.lower().rstrip("/").endswith(("/user/login", "/user/error")):
            raise AuthenticationError("Rundeck redirected to its login/error page")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


class RundeckClient:
    def __init__(self, base_url, username, api_version=46, timeout=20, max_bytes=1048576):
        parsed = urlsplit(base_url)
        if (parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password
                or parsed.query or parsed.fragment or ".." in parsed.path.split("/")):
            raise ValueError("RUNDECK_URL must be a clean HTTPS URL (context path is supported)")
        if not username or not isinstance(username, str):
            raise ValueError("RUNDECK_USER is required")
        if isinstance(api_version, bool) or not 17 <= int(api_version) <= 60:
            raise ValueError("Unexpected Rundeck API version")
        self.base_url = base_url.rstrip("/")
        self.username = username
        self.api_version = int(api_version)
        self.timeout = int(timeout)
        self.max_bytes = int(max_bytes)
        self.context = parsed.path.rstrip("/")
        self.cookies = CookieJar()
        self.http = build_opener(
            HTTPCookieProcessor(self.cookies),
            SafeRedirectHandler(self.base_url),
            HTTPSHandler(context=ssl.create_default_context()),
        )

    def _is_login_path(self, url):
        path = urlsplit(url).path.lower().rstrip("/")
        return any(path.endswith(s) for s in ("/user/login", "/user/error", "/login"))

    def _request(self, relative_url, method="GET", data=None, content_type=None):
        # relative_url is built ONLY by known, typed connector operations.
        headers = {"Accept": "application/json", "Cache-Control": "no-store"}
        if content_type:
            headers["Content-Type"] = content_type
        req = Request(self.base_url + relative_url, data=data, headers=headers, method=method)
        try:
            with self.http.open(req, timeout=self.timeout) as response:
                if self._is_login_path(response.geturl()):
                    raise AuthenticationError("Rundeck redirected the API request to login")
                if response.headers.get_content_type() != "application/json":
                    raise AuthenticationError("API did not return JSON (session or API configuration may be invalid)")
                payload = response.read(self.max_bytes + 1)
                if len(payload) > self.max_bytes:
                    raise RundeckError("Response exceeded configured size limit; narrow your query")
                try:
                    result = json.loads(payload)
                except (ValueError, UnicodeDecodeError) as e:
                    raise RundeckError("Invalid JSON returned by Rundeck") from e
                if isinstance(result, dict) and result.get("error") is True:
                    raise RundeckError("Rundeck returned an API error")
                return result
        except HTTPError as exc:
            if exc.code in (401, 403):
                raise AuthenticationError(f"HTTP {exc.code}: session or permissions denied") from None
            raise RundeckError(f"Rundeck HTTP {exc.code}") from None
        except URLError as exc:
            raise RundeckError("Cannot connect to Rundeck (network, TLS or proxy failure)") from None

    def login(self, password):
        if not password:
            raise AuthenticationError("Password is required")
        form = urlencode({"j_username": self.username, "j_password": password}).encode("utf-8")
        req = Request(self.base_url + "/j_security_check", data=form,
                      headers={"Content-Type": "application/x-www-form-urlencoded"}, method="POST")
        try:
            with self.http.open(req, timeout=self.timeout) as resp:
                if self._is_login_path(resp.geturl()):
                    raise AuthenticationError("Rundeck rejected the username/password")
                if resp.status != 200:
                    raise AuthenticationError("Rundeck did not complete login successfully")
        except HTTPError as exc:
            raise AuthenticationError(f"Login failed: HTTP {exc.code}") from None
        except URLError:
            raise AuthenticationError("Cannot reach Rundeck login (network/TLS error)") from None
        if not any(cookie.name == "JSESSIONID" and not cookie.is_expired() for cookie in self.cookies):
            raise AuthenticationError("Login did not provide an active JSESSIONID cookie")
        # Rundeck 4.8+ rotates JSESSIONID; opener + CookieJar retain changes across redirects.
        # Authorization is tested by each subsequent API request.

    def get(self, path, params=None):
        suffix = "?" + urlencode(params) if params else ""
        return self._request(f"/api/{self.api_version}/{path}{suffix}")

    def run_job(self, job_id, options):
        # Caller must perform policy and local TTY confirmation checks first.
        payload = json.dumps({"options": options}).encode("utf-8")
        return self._request(f"/api/{self.api_version}/job/{self._job_id(job_id)}/run",
                             method="POST", data=payload, content_type="application/json")

    @staticmethod
    def _job_id(job_id):
        try:
            identifier = uuid.UUID(str(job_id))
        except (ValueError, AttributeError, TypeError):
            raise ValueError("Job ID must be a Rundeck UUID") from None
        if str(identifier) != str(job_id).lower():
            raise ValueError("Job ID must be a canonical UUID")
        return str(identifier)

    @staticmethod
    def _execution_id(execution_id):
        if not re.fullmatch(r"\d{1,18}", str(execution_id)):
            raise ValueError("Execution ID must be numeric")
        return str(execution_id)

    @staticmethod
    def _project(project):
        if not isinstance(project, str) or not project or len(project) > 128 or "/" in project:
            raise ValueError("Invalid Rundeck project name")
        return quote(project, safe="")

    def system_info(self):
        return self.get("system/info")

    def projects(self):
        return self.get("projects")

    def jobs(self, project):
        return self.get(f"project/{self._project(project)}/jobs")

    def job_info(self, job_id):
        return self.get(f"job/{self._job_id(job_id)}/info")

    def job_definition(self, job_id):
        return self.get(f"job/{self._job_id(job_id)}", {"format": "json"})

    def executions(self, project, status=None, recent=None, limit=20):
        query = {"max": int(limit), "offset": 0}
        if status:
            if status not in ("running", "succeeded", "failed", "aborted"):
                raise ValueError("Invalid execution status")
            query["statusFilter"] = status
        if recent:
            if not re.fullmatch(r"[1-9]\d{0,3}[snhdwmy]", recent):
                raise ValueError("Invalid --recent; examples: 24h, 7d, 2w")
            query["recentFilter"] = recent
        return self.get(f"project/{self._project(project)}/executions", query)

    def execution(self, execution_id):
        return self.get(f"execution/{self._execution_id(execution_id)}")

    def logs(self, execution_id, lines=100):
        return self.get(f"execution/{self._execution_id(execution_id)}/output",
                        {"lastlines": int(lines)})
