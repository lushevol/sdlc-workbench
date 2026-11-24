"""service/models.py — Pydantic request and response models for dtp-tda-service.

All inputs that previously lived in .env, associated_builds.yaml, or CLI args
are now expressed as typed fields on TDAJobRequest.  Credentials never appear
here — they are resolved server-side from Vault.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


# ---------------------------------------------------------------------------
# Valid stream names (mirrors SKILL.md validation table)
# ---------------------------------------------------------------------------

VALID_STREAMS = frozenset(
    {"FXO", "RATES", "RULES", "SCM", "OMS", "XAP", "CREDIT", "BCF", "PLATFORM", "ION"}
)


# ---------------------------------------------------------------------------
# Job flags  (replaces CLI switches and the interactive confirm prompt)
# ---------------------------------------------------------------------------

class TDAFlags(BaseModel):
    """Behavioural flags for a TDA collection run.

    All flags default to the safe/recommended value for a headless service.
    """

    rwi_only: bool = Field(
        default=False,
        description=(
            "Collect only Release WI-derived data (stories, bugs, test plan, "
            "traceability, SNOW, PIT, PT). Skips build-dependent checks: "
            "unit tests, Sonar coverage, and Genie regression. "
            "build_id is not required when this is true."
        ),
    )
    no_batch: bool = Field(
        default=False,
        description="Disable bulk work item fetching. Use when ADO batch API is unavailable.",
    )
    no_parallel: bool = Field(
        default=False,
        description="Disable all parallel threading. Useful for debugging.",
    )
    auto_confirm_builds: bool = Field(
        default=True,
        description=(
            "Always accept the auto-discovered build list without prompting. "
            "Must be true in service mode. Set false only in local-dev mode "
            "where an operator is watching the logs."
        ),
    )
    use_yaml: bool = Field(
        default=False,
        description=(
            "Skip auto-discovery and use the build_overrides map supplied in "
            "the request instead of querying the ADO artifact. "
            "build_overrides must be populated when this is true."
        ),
    )


# ---------------------------------------------------------------------------
# Main request model
# ---------------------------------------------------------------------------

class TDAJobRequest(BaseModel):
    """Everything needed to run one TDA data-collection job.

    Previously spread across .env, associated_builds.yaml, and CLI args.
    Credentials are never included — they are resolved from Vault server-side.
    """

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "release_id": "14765915",
                    "build_id": "13458068",
                    "stream": "RULES",
                    "release_version": "186.0.0",
                    "build_overrides": {
                        "51527-fmdc-releases": "13458068 rules-186.0.0",
                        "51527-dtp-apollo_maven_pipeline": "13289711 186.0.0",
                        "51527-dtp-services_maven_pipeline": "13404172 186.0.0",
                        "51527-dtp-rules-ext_maven_pipeline": "13359176 186.0.0",
                        "51527-dtp-sabre-entitlement_maven_pipeline": "13373336 19.0.0",
                        "50665-dtp-client_maven_pipeline": "13394759 464.0",
                        "50665-dtp-client_npm_pipeline": "13394764 464.0",
                        "51527-dtp-market-data-services_maven_pipeline": "13089570 42.0.0",
                        "51527-apollo-rules-low-latency_maven_pipeline": "13326451 8.0.0",
                    },
                    "flags": {
                        "rwi_only": False,
                        "no_batch": False,
                        "no_parallel": True,
                        "auto_confirm_builds": True,
                        "use_yaml": True,
                    },
                }
            ]
        }
    )

    release_id: str = Field(
        description="ADO Release Work Item ID (e.g. '12347453').",
        examples=["12347453"],
    )
    build_id: Optional[str] = Field(
        default=None,
        description=(
            "ADO Pipeline Build ID for the release build (e.g. '9086679'). "
            "Required unless flags.rwi_only is true."
        ),
        examples=["9086679"],
    )
    stream: str = Field(
        description=f"Release stream. Must be one of: {', '.join(sorted(VALID_STREAMS))}.",
        examples=["RATES"],
    )
    release_version: Optional[str] = Field(
        default="",
        description=(
            "Release version string (e.g. '455.0'). When supplied, used directly "
            "for Sonar branch and PIT URL substitution instead of deriving from build."
        ),
        examples=["455.0"],
    )
    build_overrides: Optional[Dict[str, str]] = Field(
        default=None,
        description=(
            "Explicit pipeline → build-ID mapping. Replaces associated_builds.yaml / "
            "stream_config.yaml's `builds:` section. When provided together with "
            "flags.use_yaml=true, this is the sole source of build IDs (auto-discovery "
            "is skipped entirely). Each value may be a plain build ID ('13458068') or a "
            "'build_id version' annotated string ('13458068 186.0.0') — the optional "
            "trailing version (after a space) is used directly as the Sonar branch "
            "(release/<version>) for that pipeline, same convention as "
            "stream_config.yaml's `builds:` map."
        ),
        examples=[
            {
                "51527-fmdc-releases": "13458068 rules-186.0.0",
                "51527-dtp-apollo_maven_pipeline": "13289711 186.0.0",
                "blade-rates-api": "9086679",
                "blade-rates-ui": "9086700",
            }
        ],
    )
    flags: TDAFlags = Field(default_factory=TDAFlags)

    @field_validator("stream")
    @classmethod
    def validate_stream(cls, v: str) -> str:
        normalised = v.strip().upper()
        if normalised not in VALID_STREAMS:
            raise ValueError(
                f"Invalid stream '{v}'. Must be one of: {', '.join(sorted(VALID_STREAMS))}."
            )
        return normalised

    @field_validator("release_id", "build_id")
    @classmethod
    def strip_whitespace(cls, v: Optional[str]) -> Optional[str]:
        return v.strip() if v else v


# ---------------------------------------------------------------------------
# Job lifecycle enums and state models
# ---------------------------------------------------------------------------

class JobStatus(str, Enum):
    PENDING  = "pending"
    RUNNING  = "running"
    COMPLETE = "complete"
    FAILED   = "failed"


class JobSubmitResponse(BaseModel):
    """Returned immediately (HTTP 202) when a job is accepted."""

    job_id: str
    status: JobStatus = JobStatus.PENDING
    stream: str
    release_id: str
    submitted_at: str
    poll_url: str = Field(description="URL to GET for status updates.")
    result_url: str = Field(description="URL to GET once status == complete.")
    logs_url: str = Field(description="URL to stream job logs.")


class JobStatusResponse(BaseModel):
    """Returned by GET /tda/jobs/{job_id}."""

    job_id: str
    status: JobStatus
    stream: str
    release_id: str
    submitted_at: str
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    error: Optional[str] = None
    result_url: Optional[str] = Field(
        default=None,
        description="Populated only when status == complete.",
    )
    logs_url: str


class JobLogsResponse(BaseModel):
    """Returned by GET /tda/jobs/{job_id}/logs."""

    job_id: str
    status: JobStatus
    lines: List[str]


class HealthResponse(BaseModel):
    status: str = "ok"
    version: str
    vault_connected: bool
    worker_pool_size: int
    active_jobs: int
