"""tda/integrations/snow.py — ServiceNow change record integration."""

from __future__ import annotations

import logging
import requests

from tda.config import Config
from tda.call_tracker import tracker as call_tracker


def get_snow_token(cfg: Config) -> str | None:
    payload = {
        "grant_type": "client_credentials",
        "client_id": cfg.snow_client_id,
        "client_secret": cfg.snow_client_secret,
    }
    try:
        call_tracker.record('SNOW')
        r = requests.post(
            cfg.snow_token_endpoint,
            data=payload,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        r.raise_for_status()
        token = r.json().get("access_token")
        if token:
            return token
        logging.warning("SNOW: failed to retrieve access token: %s", r.json())
    except requests.exceptions.RequestException as e:
        logging.warning("SNOW: token request error: %s", e)
    return None


def get_snow_details(change_id: str, cfg: Config) -> dict:
    """Fetch ServiceNow change record fields for the given CHG number.

    Returns a dict {field_name: [values]}.  Empty lists on any error.
    """
    snow_details: dict[str, list] = {field: [] for field in cfg.snow_fields}

    if not cfg.snow_enabled:
        return snow_details

    access_token = get_snow_token(cfg)
    if not access_token:
        return snow_details

    snow_url = (
        f"https://{cfg.snow_instance}/{cfg.snow_api_path.strip('/')}"
        f"?sysparm_query=number={change_id}"
    )
    _headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    try:
        call_tracker.record('SNOW')
        r = requests.get(snow_url, headers=_headers)
        if r.status_code == 200:
            for res in r.json()['result']:
                for key in snow_details:
                    snow_details[key].append(res[key])
        else:
            logging.warning("SNOW: HTTP %s — %s", r.status_code, r.text[:500])
    except requests.exceptions.RequestException as e:
        logging.warning("SNOW: request error: %s", e)
    return snow_details
