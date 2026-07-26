"""Minimal stdlib-only Sentry error reporting for the cockpit dashboard.

The container's dashboard is deliberately stdlib-only (see Dockerfile — "no pip
deps"), so this does not use the official sentry-sdk package. Instead it POSTs
directly to Sentry's legacy Store API via urllib. Best-effort only: any failure
to reach Sentry is swallowed and logged to stderr, never raised into the caller
— monitoring must never be able to take down the cockpit it monitors.

Configuration is read from the environment (set via /app/logs/runtime.env,
exported by docker-entrypoint.sh before the dashboard starts):
  SENTRY_DSN          required — the project DSN from Sentry (Settings > Client Keys)
  SENTRY_ENVIRONMENT  optional — defaults to "production"
  SENTRY_RELEASE      optional — e.g. a git SHA, omitted if unset
"""

from __future__ import annotations

import json
import os
import sys
import traceback
import uuid
from datetime import datetime, timezone
from typing import Any
from urllib.parse import urlparse
from urllib.request import Request, urlopen

_TIMEOUT_SECONDS = 3
_ENVIRONMENT = os.environ.get("SENTRY_ENVIRONMENT", "production")
_RELEASE = os.environ.get("SENTRY_RELEASE", "")


def _parse_dsn(dsn: str) -> tuple[str, str] | None:
    """Return (store_url, public_key), or None if the DSN is missing/malformed."""
    try:
        parsed = urlparse(dsn)
        project_id = parsed.path.strip("/")
        if not (parsed.username and parsed.hostname and project_id):
            return None
        store_url = f"{parsed.scheme}://{parsed.hostname}/api/{project_id}/store/"
        return store_url, parsed.username
    except Exception:
        return None


_PARSED = _parse_dsn(os.environ.get("SENTRY_DSN", "").strip())


def capture_exception(exc: BaseException | None = None, extra: dict[str, Any] | None = None) -> None:
    """Best-effort: report the current (or given) exception to Sentry. Never raises."""
    if _PARSED is None:
        return

    exc_type, exc_value, exc_tb = (
        sys.exc_info() if exc is None else (type(exc), exc, exc.__traceback__)
    )
    if exc_value is None:
        return

    try:
        store_url, public_key = _PARSED
        frames = [
            {"filename": f.filename, "function": f.name, "lineno": f.lineno}
            for f in traceback.extract_tb(exc_tb)
        ]
        event: dict[str, Any] = {
            "event_id": uuid.uuid4().hex,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "platform": "python",
            "logger": "autocompany.cockpit",
            "environment": _ENVIRONMENT,
            "server_name": os.environ.get("HOSTNAME", "auto-company"),
            "exception": {
                "values": [
                    {
                        "type": exc_type.__name__ if exc_type else "Exception",
                        "value": str(exc_value),
                        "stacktrace": {"frames": frames},
                    }
                ]
            },
        }
        if _RELEASE:
            event["release"] = _RELEASE
        if extra:
            event["extra"] = extra

        req = Request(
            store_url,
            data=json.dumps(event).encode("utf-8"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "X-Sentry-Auth": (
                    "Sentry sentry_version=7, sentry_client=autocompany-cockpit/1.0, "
                    f"sentry_key={public_key}"
                ),
            },
        )
        urlopen(req, timeout=_TIMEOUT_SECONDS).close()
    except Exception as report_error:  # noqa: BLE001 - monitoring must never crash the caller
        print(f"[sentry_client] failed to report exception: {report_error}", file=sys.stderr)
