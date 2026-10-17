"""tda/http_client.py — ADO HTTP session, URL routing, and proxy management.

Responsibilities:
- Own the persistent requests.Session (keep-alive, retry adapter, pool)
- Own set_proxy / unset_proxy so proxy lifecycle is in one place
- Expose executeURL / executeURLForMultipleInputs as the single ADO gateway
- Provide _WIResponseAdapter for batch-fetched work item dicts
- Provide _fetch_work_items_batch for bulk ADO WI fetching

All other modules call through this module.  No business logic lives here.
"""

from __future__ import annotations

import io
import json
import logging
import os
import threading
import time
import zipfile

import urllib3
import re

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from tda.config import Config
from tda.call_tracker import tracker as call_tracker


# ---------------------------------------------------------------------------
# Retry helper for non-ADO integrations (Genie, Sonar)
# ---------------------------------------------------------------------------
# tda.integrations.genie and tda.integrations.sonar make bare `requests` /
# third-party-SDK calls to hosts outside ADO, and previously had NO retry
# protection — unlike ADOClient's session above, which mounts a Retry-configured
# HTTPAdapter. A single transient network blip (ConnectionResetError, or a
# corporate-proxy 502 Bad Gateway) would abort the call with no retry, silently
# discarding all results accumulated so far (e.g. Genie's pagination loop).
# call_with_retries() gives those call sites the same retry/backoff protection,
# without requiring control over the transport (works for bare requests.get()
# calls and for third-party SDK calls alike, since it retries around the
# call rather than inside a requests.Session).
_RETRYABLE_EXCEPTIONS = (
    requests.exceptions.ConnectionError,   # includes ProxyError, SSLError subclasses
    requests.exceptions.Timeout,
    requests.exceptions.ChunkedEncodingError,
)

# HTTP status codes that represent transient server-side or gateway failures
# and are worth retrying (502 Bad Gateway, 503 Service Unavailable, 504 Gateway Timeout).
_RETRYABLE_HTTP_STATUSES = {502, 503, 504}


def _is_retryable(exc: Exception) -> bool:
    """Return True if exc should trigger a retry."""
    if isinstance(exc, _RETRYABLE_EXCEPTIONS):
        return True
    if isinstance(exc, requests.exceptions.HTTPError):
        resp = getattr(exc, 'response', None)
        if resp is not None and resp.status_code in _RETRYABLE_HTTP_STATUSES:
            return True
    return False


def call_with_retries(fn, *, attempts: int | None = None, backoff_factor: float | None = None,
                       what: str = "request"):
    """Call fn() with retry/backoff on transient network errors.

    Retries on connection errors (incl. proxy errors), timeouts, chunked
    encoding errors, and transient HTTP gateway errors (502/503/504) — the
    same class of transient failure ADOClient's Retry adapter already protects
    against for ADO calls. Raises the last exception if every attempt fails.

    ``attempts``/``backoff_factor`` default to the HTTP_RETRY_ATTEMPTS /
    HTTP_RETRY_BACKOFF_SECONDS environment variables (read per-call, not
    cached, so a corporate-proxy outage that lasts longer than the original
    hardcoded 3-attempt/short-backoff window can be ridden out by raising
    these in .env without a code change) — falling back to 3 / 1.0 if unset.
    """
    if attempts is None:
        attempts = int(os.environ.get('HTTP_RETRY_ATTEMPTS', '3').strip() or '3')
    if backoff_factor is None:
        backoff_factor = float(os.environ.get('HTTP_RETRY_BACKOFF_SECONDS', '1.0').strip() or '1.0')

    last_exc: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            return fn()
        except Exception as e:
            if not _is_retryable(e):
                raise
            last_exc = e
            if attempt < attempts:
                delay = backoff_factor * (2 ** (attempt - 1))
                logging.warning(
                    "%s: attempt %d/%d failed (%s) — retrying in %.1fs",
                    what, attempt, attempts, e, delay,
                )
                time.sleep(delay)
    raise last_exc


class ADOClient:
    """Stateful ADO HTTP client.  One instance per TDA run."""

    def __init__(self, cfg: Config) -> None:
        self.cfg = cfg
        self._proxy_ip = cfg.proxy_ip

        retry = Retry(
            total=5,
            connect=3,
            read=2,
            backoff_factor=1.0,
            # 429 added: ADO/TFS returns 429 (or 503) when an identity is throttled by
            # a resource governor (e.g. the 'Concurrency' bucket on on-prem ADO Server
            # instances such as sc-ado). Retrying with backoff instead of failing hard
            # avoids compounding the throttling with an immediate client-side retry storm.
            status_forcelist=[429, 500, 502, 503, 504],
            respect_retry_after_header=True,
            raise_on_status=False,
        )
        self._session = requests.Session()
        self._session.headers.update(cfg.ado_headers)
        self._session.mount('https://', HTTPAdapter(max_retries=retry, pool_maxsize=20))
        self._session.mount('http://',  HTTPAdapter(max_retries=retry, pool_maxsize=20))

        # Cache for list_builds_for_branch — keyed by (branch_name, tag_filter, base_url).
        # Eliminates redundant GetBuilds calls during auto-discovery (same branches
        # queried once per artifact version; typically 10+ versions × 3 candidates).
        self._branch_build_cache: dict[tuple[str, str, str], list[dict]] = {}

        # --- Request throttle ---
        # Enforces a minimum wall-clock interval between ANY two outbound ADO
        # requests made through this client, configurable via ADO_THROTTLE_DELAY_MS
        # in .env (milliseconds; default 0 = disabled/no change in behaviour).
        # Protected by a lock so it is a true GLOBAL min-interval even if
        # PARALLEL_ENABLED=true and multiple threads call in simultaneously —
        # a per-thread delay alone would not actually reduce the peak concurrent
        # request rate seen by ADO, only a shared gate does. Added 2026-07-15
        # as an additional safety measure against the on-prem ADO Server
        # 'Concurrency' resource-governor throttling (see also: reduced
        # ThreadPoolExecutor worker counts and PARALLEL_ENABLED).
        self._throttle_delay = max(0.0, cfg.ado_throttle_delay_ms) / 1000.0
        self._throttle_lock = threading.Lock()
        self._last_request_ts = 0.0

    def _throttle(self) -> None:
        """Block the calling thread until at least ``_throttle_delay`` seconds
        have elapsed since the last ADO request made by ANY thread on this
        client instance. No-op when the delay is 0 (default).

        This is also the single choke point every real outbound ADO HTTP call
        passes through (get/get2/raw_get/raw_post/artifact helpers/branch
        lookup), so it doubles as the call-count/rate tracking hook — one
        line here covers all of them instead of instrumenting each call site.
        """
        call_tracker.record('ADO')
        if self._throttle_delay <= 0:
            return
        with self._throttle_lock:
            now = time.monotonic()
            wait = self._last_request_ts + self._throttle_delay - now
            if wait > 0:
                time.sleep(wait)
            self._last_request_ts = time.monotonic()

    # ------------------------------------------------------------------
    # Proxy helpers
    # ------------------------------------------------------------------

    def set_proxy(self) -> None:
        if self._proxy_ip:
            import os
            # Ensure the proxy URL always has a scheme — requests warns and may
            # silently ignore values without one (e.g. '10.x.x.x:443').
            proxy = self._proxy_ip if self._proxy_ip.startswith(('http://', 'https://')) else f'http://{self._proxy_ip}'
            os.environ['HTTPS_PROXY'] = proxy
            # Also set on the session directly so it is not subject to env-var
            # read-timing or Windows-registry proxy detection quirks.
            self._session.proxies.update({
                'http':  proxy,
                'https': proxy,
            })

    def unset_proxy(self) -> None:
        import os
        os.environ['HTTPS_PROXY'] = ''
        self._session.proxies.clear()

    # ------------------------------------------------------------------
    # HTTP error helper
    # ------------------------------------------------------------------

    def _raise_ado_http_error(self, resp: requests.Response, context: str) -> None:
        try:
            resp.raise_for_status()
        except requests.exceptions.HTTPError as e:
            status = getattr(resp, 'status_code', 'unknown')
            body = (resp.text or '')[:1000]
            if status == 403 and 'VS403463' in body:
                raise RuntimeError(
                    f"{context}: Azure DevOps blocked the request due to Entra Conditional "
                    "Access (VS403463). PAT is present but this device/network/user is not "
                    "allowed by org policy."
                ) from e
            raise

    # ------------------------------------------------------------------
    # URL routing
    # ------------------------------------------------------------------

    def _get_url(self, mapping_link: str, input1: str, input2: str | None = None) -> str:
        base = self.cfg.ado_base_url.rstrip('/')
        mapping: dict[str, str] = {
            'TestRunByPlanId':      f'{base}/test/runs?planId={input1}&api-version=7.1',
            'TestRunsByBuildId':    f'{base}/test/runs?buildId={input1}&includeRunDetails=true&api-version=7.1',
            'TestRunStatistics':    f'{base}/test/runs/{input1}/statistics?api-version=7.1',
            'StoryByReleaseId':     f'{base}/wit/workitems/{input1}?$expand=relations&api-version=7.1',
            'UnitTestByBuild':      f'{base}/test/ResultSummaryByBuild?buildId={input1}&api-version=7.1-preview',
            'BranchFromBuild':      f'{base}/build/builds/{input1}?api-version=7.1',
            'ProjectFromBuild':     f'{base}/build/builds/{input1}?api-version=7.1',
            'TestSuiteFromPlanId':  f'{base}/testplan/plans/{input1}/suites/',
            'TestSuitesForTestPlan':f'{base}/testplan/plans/{input1}/suites/?api-version=7.1',
            'WorkItemsForRelease':  f'{base}/wit/workitems/{input1}?$expand=relations&api-version=7.1',
            'StoryByStoryId':       f'{base}/wit/workitems/{input1}?$expand=relations&api-version=7.1',
            'CommentsForRelease':   f'{base}/wit/workitems/{input1}/comments',
            'TestCasesForWI':       f'{base}/wit/workItems/{input1}?$expand=relations&api-version=7.1',
            'TestCasesForWorkItem': f'{base}/wit/workItems/{input1}?$expand=relations&api-version=7.1',
            'TestCaseDetails':      f'{base}/wit/workitems/{input1}?$expand=relations&api-version=7.1',
            'TestResultByRunId':    f'{base}/test/Runs/{input1}/results?api-version=7.1',
            'TestResultByRunIdWithIterations': f'{base}/test/Runs/{input1}/results?detailsToInclude=Iterations&api-version=7.1',
            'CommentByStoryId':     f'{base}/wit/workItems/{input1}/comments',
            'WorkItemUpdates':      f'{base}/wit/workItems/{input1}/updates?api-version=7.1',
            # Multi-input
            'TestCases':              f'{base}/test/Plans/{input1}/suites/{input2}/testcases?api-version=7.1',
            'TestCasesForTestSuite':  f'{base}/test/Plans/{input1}/suites/{input2}/testcases?api-version=7.1',
            'TestResultsForTestCase': f'{base}/test/runs?planId={input1}&testCaseId={input2}&api-version=7.1',
            'TestResultById':         f'{base}/test/Runs/{input1}/results/{input2}?api-version=7.1-preview.2',
            'TestResultIterations':   f'{base}/test/Runs/{input1}/results/{input2}?detailsToInclude=Iterations&api-version=7.1',
            'TestRunAttachment':       f'{base}/test/Runs/{input1}/attachments?api-version=7.1',
            'TestResultAttachment':   f'{base}/test/Runs/{input1}/results/{input2}/attachments?api-version=7.1',
            'TestResultComment':      f'{base}/test/Runs/{input1}/results/{input2}?api-version=7.1-preview.2',
            'TestResultsByStep':      f'{base}/test/Runs/{input1}/results/{input2}?detailsToInclude=Iterations&api-version=7.1',
        }
        return mapping[mapping_link]

    def get(self, mapping_link: str, input1: str) -> requests.Response:
        """Single-input GET against ADO."""
        self._throttle()
        self.set_proxy()
        url = self._get_url(mapping_link, input1)
        r = self._session.get(url, headers=self.cfg.ado_headers, verify=False)
        self._raise_ado_http_error(r, f"ADO request failed for {mapping_link}")
        return r

    def get2(self, mapping_link: str, input1: str, input2: str) -> requests.Response:
        """Two-input GET against ADO."""
        self._throttle()
        self.set_proxy()
        url = self._get_url(mapping_link, input1, input2)
        r = self._session.get(url, headers=self.cfg.ado_headers, verify=False)
        self._raise_ado_http_error(r, f"ADO request failed for {mapping_link}")
        return r

    def raw_get(self, url: str, *, headers: dict | None = None,
                verify: bool = False, timeout: int = 30) -> requests.Response:
        """Bypass URL routing for arbitrary GET (used by build_resolver)."""
        self._throttle()
        self.set_proxy()
        h = headers or self.cfg.ado_headers
        r = self._session.get(url, headers=h, verify=verify, timeout=timeout)
        self._raise_ado_http_error(r, f"ADO raw GET failed: {url[:120]}")
        return r

    def raw_post(self, url: str, *, json_body: dict | None = None,
                 data=None, headers: dict | None = None,
                 verify: bool = False, timeout: int = 60) -> requests.Response:
        """Arbitrary POST (used by batch fetch and SNOW token)."""
        self._throttle()
        self.set_proxy()
        h = headers or self.cfg.ado_headers
        r = self._session.post(url, json=json_body, data=data,
                               headers=h, verify=verify, timeout=timeout)
        self._raise_ado_http_error(r, f"ADO raw POST failed: {url[:120]}")
        return r

    def get_remote_skill_version(self, *, org: str, project: str, repo: str,
                                  path: str, branch: str) -> str | None:
        """Fetch ``metadata.version`` from a SKILL.md file at a given branch of
        a (possibly different) ADO repo — used by the Skill Version Staleness
        Check (added 2026-10-13) to compare the locally-installed/vendored
        copy of this skill against the canonical source repo's stable branch.

        Best-effort only: returns ``None`` on ANY failure (auth, network, 404,
        unparsable content) rather than raising — this check must never block
        or fail a real report run, it is purely an informational reminder.
        """
        self._throttle()
        self.set_proxy()
        url = (f'https://dev.azure.com/{org}/{project}/_apis/git/repositories/{repo}/items'
               f'?path={path}&versionDescriptor.version={branch}'
               f'&versionDescriptor.versionType=branch&api-version=7.1')
        headers = dict(self.cfg.ado_headers)
        headers['Accept'] = 'text/plain'
        try:
            resp = self._session.get(url, headers=headers, verify=False, timeout=15)
            if resp.status_code != 200:
                return None
            text = resp.text
        except Exception:
            return None
        m = re.search(r'^\s*version:\s*"([^"]+)"', text, re.MULTILINE)
        return m.group(1) if m else None

    def get_test_attachment_content(self, run_id: str, result_id: str,
                                     attachment_id: str) -> bytes:
        """Download the raw byte content of a single test-result attachment.

        Unlike ``get2('TestResultAttachment', ...)`` (which only lists
        attachment metadata — file name, id, size), this fetches the actual
        file bytes for one attachment ID. Used by
        ``tda.collectors.po_approval`` to parse email (.eml/.msg) attachments
        looking for Acceptance Testing PO-approval evidence.
        """
        url = (
            f"{self.cfg.ado_base_url.rstrip('/')}/test/Runs/{run_id}/results/"
            f"{result_id}/attachments/{attachment_id}?api-version=7.1"
        )
        self._throttle()
        self.set_proxy()
        r = self._session.get(url, headers=self.cfg.ado_headers, verify=False, timeout=30)
        self._raise_ado_http_error(r, f"ADO attachment content download failed (attachment {attachment_id})")
        return r.content

    # ------------------------------------------------------------------
    # Batch work item fetch
    # ------------------------------------------------------------------

    def fetch_work_items_batch(self, ids: list[str],
                               chunk_size: int = 200) -> dict[str, dict]:
        """Fetch multiple ADO work items via the workitemsbatch API.

        Returns {str(id): work_item_dict}.  Raises on HTTP errors so the
        caller can decide whether to fall back to sequential fetching.
        """
        url = f"{self.cfg.ado_base_url}wit/workitemsbatch?api-version=7.1"
        id_list = [int(i) for i in ids]
        result: dict[str, dict] = {}
        num_chunks = -(-len(id_list) // chunk_size)
        for chunk_idx in range(num_chunks):
            chunk = id_list[chunk_idx * chunk_size:(chunk_idx + 1) * chunk_size]
            r = self.raw_post(url, json_body={"ids": chunk, "$expand": "relations"})
            for wi in r.json().get('value', []):
                result[str(wi['id'])] = wi
        logging.info(
            "fetch_work_items_batch: fetched %d work items in %d request(s)",
            len(result), num_chunks,
        )
        return result

    # ------------------------------------------------------------------
    # Build artifact helpers (used by build_resolver)
    # ------------------------------------------------------------------

    def get_build_artifact_metadata(self, build_id: str, artifact_name: str) -> dict:
        url = f"{self.cfg.ado_base_url.rstrip('/')}/build/builds/{build_id}/artifacts"
        self._throttle()
        self.set_proxy()
        r = requests.get(
            url,
            params={'artifactName': artifact_name, 'api-version': '7.1'},
            headers=self.cfg.ado_headers, verify=False,
        )
        self._raise_ado_http_error(r, f"ADO artifact metadata failed for '{artifact_name}'")
        return r.json()

    def list_build_artifacts(self, build_id: str) -> list[dict]:
        """List ALL published artifacts on a build (no artifactName filter).

        Used to discover artifact names that vary by pipeline template (e.g.
        'AIG.html' is published by some application pipelines but not others)
        without needing to guess the exact name up front.
        """
        url = f"{self.cfg.ado_base_url.rstrip('/')}/build/builds/{build_id}/artifacts"
        self._throttle()
        self.set_proxy()
        r = requests.get(
            url, params={'api-version': '7.1'},
            headers=self.cfg.ado_headers, verify=False,
        )
        self._raise_ado_http_error(r, f"ADO artifact list failed for build {build_id}")
        return r.json().get('value', [])

    def download_build_artifact_zip(self, build_id: str, artifact_name: str) -> bytes:
        meta = self.get_build_artifact_metadata(build_id, artifact_name)
        download_url = meta['resource']['downloadUrl']
        self._throttle()
        self.set_proxy()
        r = requests.get(download_url, headers=self.cfg.ado_headers, verify=False)
        self._raise_ado_http_error(r, f"ADO artifact download failed for '{artifact_name}'")
        return r.content

    def get_aig_rollback_document(self, build_id: str) -> dict:
        """Fetch the AIG/Rollback installation guide, if published as a build artifact.

        Some application pipelines (e.g. Blade FXO/Credit-style apps) publish
        a self-contained 'AIG.html' artifact on the MASTER release build —
        visible in ADO's UI under the build's custom 'Extensions' tab, but
        also directly downloadable via the standard Build Artifacts API like
        any other artifact (promotedImageList, SBOM, etc). Other applications
        instead link an AIG/Rollback document directly on the Release WI via
        ``Custom.AIGandRollbackdocumentLink`` — that path is handled separately
        in ``extract_release_checks()`` and does not call this method.

        Confirmed live (2026-10-13, build 8979905, 'Blade fxo: Release 106.0.0'):
        the artifact is a zip containing a single '<name>/<name>.html' entry,
        and the installation steps AND rollback steps are both embedded in the
        SAME document (rollback section starts under a heading containing the
        words "THEN FOLLOWING ROLLBACK STEPS").

        Returns a dict (never raises — any failure is captured in 'error' so
        the collector can continue without this optional check):
            {
                'found':        bool,   # artifact exists and was downloaded
                'artifact_name': str | None,
                'content':      str | None,  # full HTML/text content
                'error':        str | None,  # set only on unexpected failure
            }
        Artifact names containing 'aig' (case-insensitive) are treated as
        candidates — matches the observed 'AIG.html' name while tolerating
        minor naming variance across pipeline templates (e.g. 'AIGandRollback').
        """
        try:
            artifacts = self.list_build_artifacts(build_id)
        except Exception as exc:
            return {'found': False, 'artifact_name': None, 'content': None, 'error': str(exc)}

        candidate = next(
            (a['name'] for a in artifacts if 'aig' in a.get('name', '').lower()),
            None,
        )
        if candidate is None:
            return {'found': False, 'artifact_name': None, 'content': None, 'error': None}

        try:
            blob = self.download_build_artifact_zip(build_id, candidate)
            with zipfile.ZipFile(io.BytesIO(blob)) as archive:
                html_names = [n for n in archive.namelist() if n.lower().endswith(('.html', '.htm', '.md'))]
                if not html_names:
                    return {
                        'found': True, 'artifact_name': candidate, 'content': None,
                        'error': f"Artifact '{candidate}' contained no .html/.md file "
                                 f"(entries: {archive.namelist()[:10]})",
                    }
                content = archive.read(html_names[0]).decode('utf-8', errors='replace')
            return {'found': True, 'artifact_name': candidate, 'content': content, 'error': None}
        except Exception as exc:
            return {'found': True, 'artifact_name': candidate, 'content': None, 'error': str(exc)}

    def _download_promoted_image_payload(self, build_id: str) -> dict:
        """Download and parse the raw promotedImageList.json payload for a build.

        Returns the raw dict as published (Artifactory repo name -> list of
        artifact identifiers — image:tag strings for docker-sc-release_local,
        relative paths for helm3-release_local/maven-sc-release_local).
        Shared by extract_promoted_image_versions() (semver-only view) and
        _resolve_builds_via_artifactory() in build_resolver.py (needs the raw
        repo+path structure, not just the version substring).

        Raises ValueError (not the raw json.JSONDecodeError) when the
        extracted file isn't valid JSON — e.g. truncated/blank content, which
        has been observed in practice when the supplied ``build_id`` did not
        actually publish a populated promotedImageList artifact (wrong/stale
        build id, or a build that failed before the promote step ran). The
        raised message includes the build id and a short repr of what was
        actually read, so this is diagnosable directly from the collector's
        console output instead of a bare "Expecting value: line N column M"
        traceback with no further context.
        """
        artifact_zip = self.download_build_artifact_zip(build_id, 'promotedImageList')
        with zipfile.ZipFile(io.BytesIO(artifact_zip)) as archive:
            raw_bytes = archive.read('promotedImageList/promotedImageList.json')
        raw_text = raw_bytes.decode('utf-8', errors='replace')
        try:
            return json.loads(raw_text)
        except json.JSONDecodeError as exc:
            snippet = raw_text[:200].strip() or '(empty)'
            raise ValueError(
                f"promotedImageList.json for build {build_id} is not valid JSON "
                f"({len(raw_bytes)} byte(s) read; content starts with: {snippet!r}). "
                "This usually means the supplied build id did not actually publish a "
                "populated promotedImageList artifact — e.g. a wrong/stale build id, "
                "or a build that failed/was cancelled before the artifact-promotion "
                "step ran. Confirm the build id in ADO's Release Summary -> Published "
                "Artifacts, or supply 'streams.<STREAM>.builds' manually in "
                "stream_config.yaml instead of relying on auto-discovery for this run."
            ) from exc

    def extract_promoted_image_versions(self, build_id: str) -> list[str]:
        """Download promotedImageList artifact and return all semantic versions found."""
        payload = self._download_promoted_image_payload(build_id)
        versions: set[str] = set()
        for images in payload.values():
            for image in images:
                if ':' not in image:
                    continue
                version = image.rsplit(':', 1)[-1].strip()
                if re.fullmatch(r'\d+\.\d+(\.\d+)?', version):
                    versions.add(version)
        if not versions:
            raise ValueError(
                f"promotedImageList artifact on build {build_id} contained no semantic versions."
            )
        return sorted(versions)

    def get_promoted_image_artifact_paths(self, build_id: str, repo: str = 'helm3-release_local') -> list[str]:
        """Return the raw list of artifact paths for one Artifactory repo key
        (default 'helm3-release_local') from the build's promotedImageList
        artifact — e.g. 'fm/51527/dtp-apollo-ans-service-187.0.24.tgz'.

        Used by build_resolver.py's opt-in Artifactory-based discovery path
        (_resolve_builds_via_artifactory(), gated by the per-stream
        'artifactory_build_discovery_enabled' flag). Docker entries
        ('docker-sc-release_local') are deliberately not resolved by that
        path — the Artifactory docker repo requires auth we don't have
        configured (confirmed 401, 2026-08-06).
        """
        payload = self._download_promoted_image_payload(build_id)
        return payload.get(repo, [])

    def get_artifactory_build_info(self, path: str, repo: str = 'helm3-release_local') -> tuple[str | None, str | None]:
        """Look up build.name/build.number for one Artifactory artifact path
        via the build-info properties endpoint.

        Internal SC host — no ADO auth and no corporate proxy needed
        (confirmed live 2026-08-06 for helm3/maven repos). Returns
        (None, None) on any non-200 response or request failure rather than
        raising — a single unresolvable artifact should not abort discovery
        for the rest of the release's artifacts.
        """
        url = f"{self.cfg.artifactory_base_url.rstrip('/')}/{repo}/{path.lstrip('/')}?properties"

        def _do_request():
            return requests.get(url, timeout=15, verify=False, proxies={'http': None, 'https': None})

        try:
            resp = call_with_retries(_do_request, what=f"Artifactory build-info lookup for '{path}'")
        except Exception as exc:
            logging.warning("get_artifactory_build_info: request failed for '%s': %s", path, exc)
            return None, None
        if resp.status_code != 200:
            logging.warning("get_artifactory_build_info: status %s for '%s'", resp.status_code, path)
            return None, None
        props = resp.json().get('properties', {})
        build_name = (props.get('build.name') or [None])[0]
        build_number = (props.get('build.number') or [None])[0]
        return build_name, build_number

    def extract_build_provenance_pipelines(self, build_id: str) -> dict[str, str]:
        """Download the ``build.provenance`` SLSA attestation artifact and return
        ``{buildName: buildNumber}`` for every distinct component pipeline referenced
        in its ``subject`` list.

        Unlike ``promotedImageList`` (image:version pairs, requiring a branch/tag
        search afterward to find the actual build), ``build.provenance`` already
        embeds the exact ``buildName`` (ADO pipeline/definition name) and
        ``buildNumber`` for every published artifact — generated automatically by
        the pipeline template on EVERY build (confirmed present even on builds with
        zero tags, e.g. RULES). Combine with ``find_build_by_name_and_number()`` to
        resolve the real build id deterministically, no tag/branch guessing needed.

        Raises ValueError if the artifact is missing or has no usable subjects.
        """
        artifact_zip = self.download_build_artifact_zip(build_id, 'build.provenance')
        with zipfile.ZipFile(io.BytesIO(artifact_zip)) as archive:
            names = [n for n in archive.namelist() if n.endswith('build.provenance')]
            if not names:
                raise ValueError(
                    f"build.provenance artifact on build {build_id} did not contain a "
                    "'build.provenance' file."
                )
            payload = json.loads(archive.read(names[0]).decode('utf-8'))
        pipelines: dict[str, str] = {}
        for subject in payload.get('subject', []):
            build_name = subject.get('buildName')
            build_number = subject.get('buildNumber')
            if build_name and build_number:
                pipelines[build_name] = build_number
        if not pipelines:
            raise ValueError(
                f"build.provenance artifact on build {build_id} contained no "
                "subjects with both 'buildName' and 'buildNumber'."
            )
        return pipelines

    def find_build_by_name_and_number(self, build_name: str, build_number: str,
                                       extra_base_urls: list[str] | None = None) -> dict | None:
        """Deterministically resolve the exact ADO build for a given pipeline
        (definition) name + buildNumber — the pair recorded in build.provenance.

        No branch/tag guessing involved: looks up the pipeline definition id by
        name, then queries builds for that definition filtered by buildNumber.
        Returns the build dict, or None if the definition or build isn't found
        (tried against ``ado_base_url`` plus any ``extra_base_urls``, in order —
        returns on the first match).
        """
        urls_to_query = [self.cfg.ado_base_url.rstrip('/')] + [
            u.rstrip('/') for u in (extra_base_urls or [])
        ]
        for base in urls_to_query:
            self._throttle()
            self.set_proxy()
            defs_resp = requests.get(
                f"{base}/build/definitions",
                params={'name': build_name, 'api-version': '7.1'},
                headers=self.cfg.ado_headers, verify=False,
            )
            self._raise_ado_http_error(defs_resp, f"ADO build definitions lookup failed for '{build_name}'")
            definitions = defs_resp.json().get('value', [])
            if not definitions:
                continue
            definition_id = definitions[0]['id']

            self._throttle()
            self.set_proxy()
            builds_resp = requests.get(
                f"{base}/build/builds",
                params={
                    'definitions': definition_id,
                    'buildNumber': build_number,
                    'api-version': '7.1',
                },
                headers=self.cfg.ado_headers, verify=False,
            )
            self._raise_ado_http_error(builds_resp, f"ADO builds lookup failed for '{build_name}' #{build_number}")
            builds = builds_resp.json().get('value', [])
            if builds:
                return builds[0]
        return None

    def list_builds_for_branch(self, branch_name: str,
                                extra_base_urls: list[str] | None = None,
                                tag_filter: str = '') -> list[dict]:
        """Return ADO builds for a given branch name.

        Queries ``ado_base_url`` plus any ``extra_base_urls``.

        ``tag_filter`` is forwarded to the ADO API as the ``tagFilters`` parameter
        (server-side AND-filter on build tags).  Using it avoids fetching large
        per-branch result pages when only a specific version tag is needed — the
        ADO API returns only matching builds regardless of branch depth.

        Results are cached per (branch, tag_filter, base_url).
        """
        all_builds: list[dict] = []
        urls_to_query = [self.cfg.ado_base_url.rstrip('/')] + [
            u.rstrip('/') for u in (extra_base_urls or [])
        ]
        for base in urls_to_query:
            cache_key = (branch_name, tag_filter, base)
            if cache_key in self._branch_build_cache:
                all_builds.extend(self._branch_build_cache[cache_key])
                logging.debug(
                    "list_builds_for_branch: cache hit branch='%s' tag='%s' base='%s'",
                    branch_name, tag_filter, base,
                )
                continue
            url = f"{base}/build/builds"
            self.set_proxy()
            try:
                params: dict = {'branchName': branch_name, '$top': 200, 'api-version': '7.1'}
                if tag_filter:
                    params['tagFilters'] = tag_filter
                self._throttle()
                r = requests.get(
                    url,
                    params=params,
                    headers=self.cfg.ado_headers, verify=False, timeout=30,
                )
                self._raise_ado_http_error(r, f"ADO build query failed for branch '{branch_name}' in '{base}'")
                builds = r.json().get('value', [])
                logging.info(
                    "list_builds_for_branch: found %d build(s) on '%s' tag='%s' in '%s'",
                    len(builds), branch_name, tag_filter or '(any)', base,
                )
                self._branch_build_cache[cache_key] = builds
                all_builds.extend(builds)
            except Exception as e:
                logging.warning("list_builds_for_branch: '%s' query failed — %s", base, e)
        return all_builds

    # ------------------------------------------------------------------
    # Build metadata helpers
    # ------------------------------------------------------------------

    def get_branch_from_build(self, build_id: str) -> str:
        r = self.get('BranchFromBuild', build_id)
        return r.json()['sourceBranch'].split('/heads/')[-1]

    def get_project_from_build(self, build_id: str) -> str:
        r = self.get('ProjectFromBuild', build_id)
        return r.json()['repository']['name']

    def get_pipeline_name_from_build(self, build_id: str) -> str:
        r = self.get('ProjectFromBuild', build_id)
        return r.json()['definition']['name']


# ---------------------------------------------------------------------------
# Adapter — lets batch-fetched dicts behave like requests.Response
# ---------------------------------------------------------------------------

class WIResponseAdapter:
    """Wraps a pre-fetched work item dict so it behaves like a requests.Response.

    All existing extract*() functions call .json() — this adapter makes them
    work unchanged whether the WI was fetched individually or in a batch.
    """
    __slots__ = ('_data',)

    def __init__(self, data: dict) -> None:
        self._data = data

    def json(self) -> dict:
        return self._data
