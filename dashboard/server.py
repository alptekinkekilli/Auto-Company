#!/usr/bin/env python3
"""Local dashboard server for Auto Company (Windows + WSL + macOS runtime)."""

from __future__ import annotations

import argparse
import json
import os
import platform
import re
import shlex
import subprocess
import threading
import time
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

import sentry_client

REPO_ROOT = Path(__file__).resolve().parents[1]
DASHBOARD_DIR = Path(__file__).resolve().parent

WINDOWS_STATUS_SCRIPT = REPO_ROOT / "scripts" / "windows" / "status-win.ps1"
WINDOWS_START_SCRIPT = REPO_ROOT / "scripts" / "windows" / "start-win.ps1"
WINDOWS_STOP_SCRIPT = REPO_ROOT / "scripts" / "windows" / "stop-win.ps1"

LINUX_STATUS_SCRIPT = REPO_ROOT / "scripts" / "linux" / "status-linux.sh"
LINUX_NOOP_SCRIPT = REPO_ROOT / "scripts" / "linux" / "noop-action.sh"

MACOS_STATUS_SCRIPT = REPO_ROOT / "scripts" / "macos" / "status-mac.sh"
MACOS_START_SCRIPT = REPO_ROOT / "scripts" / "macos" / "install-daemon.sh"
MACOS_STOP_SCRIPT = REPO_ROOT / "scripts" / "core" / "stop-loop.sh"

LOG_FILE = REPO_ROOT / "logs" / "auto-loop.log"
STATE_FILE = REPO_ROOT / ".auto-loop-state"
CONSENSUS_FILE = REPO_ROOT / "memories" / "consensus.md"
DIRECTIVE_FILE = REPO_ROOT / "memories" / "human-directive.md"
CANDIDATE_REGISTRY_FILE = REPO_ROOT / "memories" / "candidate-registry.md"
ANALYSIS_FILE = REPO_ROOT / "memories" / "analysis-directive.md"
# Operator-editable runtime overrides, sourced by docker-entrypoint.sh on start.
RUNTIME_ENV_FILE = REPO_ROOT / "logs" / "runtime.env"

# Whitelist of NON-SECRET knobs editable from the cockpit Settings panel. Anything
# not listed here is rejected, so the panel can never write secrets to runtime.env.
SETTINGS_SPEC: list[dict[str, str]] = [
    {"key": "ROUTER_ALTERNATE", "type": "bool",
     "label": "Router alternation (Claude↔Codex when both have headroom)"},
    {"key": "WINDOW_BUDGET_USD", "type": "number",
     "label": "Claude 5h window budget (USD, blank = no cap)"},
    {"key": "CODEX_WINDOW_LIMIT", "type": "number",
     "label": "Codex cycles per window (blank = unmetered)"},
    {"key": "MODEL", "type": "text",
     "label": "Claude model (blank = engine default, e.g. claude-haiku-4-5-20251001)"},
    {"key": "CLAUDE_EFFORT", "type": "text",
     "label": "Claude reasoning effort (low / medium / high, blank = default)"},
    {"key": "ENGINE", "type": "text",
     "label": "Primary engine (claude / codex, blank = claude)"},
    {"key": "CODEX_EFFORT", "type": "text",
     "label": "Codex reasoning effort (low / medium / high, blank = codex default)"},
    {"key": "ROUTER_TIER_LADDER", "type": "bool",
     "label": "Tier ladder — round-robin model/effort within the MIN..MAX range (saves tokens)"},
    {"key": "CLAUDE_TIER_LADDER", "type": "text",
     "label": "Claude model ladder, cheapest first (comma-sep), e.g. claude-haiku-4-5-20251001,claude-sonnet-5"},
    {"key": "CODEX_TIER_LADDER", "type": "text",
     "label": "Codex effort ladder, cheapest first (comma-sep), e.g. low,medium"},
    {"key": "LOOP_INTERVAL", "type": "number",
     "label": "Loop interval between cycles (seconds)"},
    {"key": "BUDGET_PAUSE_SECONDS", "type": "number",
     "label": "Pause when budget hit and Codex unavailable (seconds)"},
]
SETTINGS_KEYS = {s["key"] for s in SETTINGS_SPEC}

WINDOWS_HOST = "windows"
MACOS_HOST = "macos"
LINUX_HOST = "linux"


def ps_quote(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def detect_host_kind(system_name: str | None = None) -> str:
    name = system_name or platform.system()
    if name == "Windows":
        return WINDOWS_HOST
    if name == "Darwin":
        return MACOS_HOST
    if name == "Linux":
        return LINUX_HOST
    raise RuntimeError(
        "Dashboard only supports Windows (WSL), macOS, and Linux/container hosts."
    )


def run_powershell_script(
    script_path: Path, args: list[str] | None = None, timeout: int = 90
) -> dict[str, Any]:
    invocation = f"& {ps_quote(str(script_path))}"
    if args:
        invocation += " " + " ".join(ps_quote(arg) for arg in args)

    cmd = [
        "powershell",
        "-NoProfile",
        "-ExecutionPolicy",
        "Bypass",
        "-Command",
        (
            "$ErrorActionPreference='Stop'; "
            "[Console]::OutputEncoding=[System.Text.Encoding]::UTF8; "
            "$OutputEncoding=[System.Text.Encoding]::UTF8; "
            f"{invocation} *>&1 | Out-String"
        ),
    ]

    start = time.time()
    proc = subprocess.run(
        cmd,
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
    )
    elapsed_ms = int((time.time() - start) * 1000)

    output = (proc.stdout or "").strip()
    error = (proc.stderr or "").strip()
    combined = output
    if error:
        combined = f"{output}\n{error}".strip()

    return {
        "ok": proc.returncode == 0,
        "exitCode": proc.returncode,
        "elapsedMs": elapsed_ms,
        "output": combined,
    }


def run_shell_script(
    script_path: Path, args: list[str] | None = None, timeout: int = 90
) -> dict[str, Any]:
    cmd = ["/bin/bash", str(script_path)]
    if args:
        cmd.extend(args)

    start = time.time()
    proc = subprocess.run(
        cmd,
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
    )
    elapsed_ms = int((time.time() - start) * 1000)

    output = (proc.stdout or "").strip()
    error = (proc.stderr or "").strip()
    combined = output
    if error:
        combined = f"{output}\n{error}".strip()

    return {
        "ok": proc.returncode == 0,
        "exitCode": proc.returncode,
        "elapsedMs": elapsed_ms,
        "output": combined,
    }


def get_host_profile(system_name: str | None = None) -> dict[str, Any]:
    host = detect_host_kind(system_name)
    if host == WINDOWS_HOST:
        return {
            "host": host,
            "runner": run_powershell_script,
            "parser": parse_windows_status_output,
            "status_script": WINDOWS_STATUS_SCRIPT,
            "start_script": WINDOWS_START_SCRIPT,
            "start_args": None,
            "stop_script": WINDOWS_STOP_SCRIPT,
            "stop_args": None,
        }
    if host == LINUX_HOST:
        return {
            "host": host,
            "runner": run_shell_script,
            "parser": parse_macos_status_output,
            "status_script": LINUX_STATUS_SCRIPT,
            "start_script": LINUX_NOOP_SCRIPT,
            "start_args": None,
            "stop_script": LINUX_NOOP_SCRIPT,
            "stop_args": None,
        }
    return {
        "host": host,
        "runner": run_shell_script,
        "parser": parse_macos_status_output,
        "status_script": MACOS_STATUS_SCRIPT,
        "start_script": MACOS_START_SCRIPT,
        "start_args": None,
        "stop_script": MACOS_STOP_SCRIPT,
        "stop_args": ["--pause-daemon"],
    }


def read_text_file(path: Path, fallback: str = "") -> str:
    try:
        raw = path.read_bytes()
    except FileNotFoundError:
        return fallback
    except Exception as exc:  # pragma: no cover - defensive
        return f"(read error: {exc})"

    for enc in ("utf-8", "utf-8-sig", "gb18030", "cp936"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue

    return raw.decode("utf-8", errors="replace")


DIRECTIVE_MAX_CHARS = 20000


def read_directive() -> dict[str, Any]:
    """Parse memories/human-directive.md into a structured payload.

    Returns {present, status, updated, directive}. status is one of
    PENDING / DONE / NONE. The autonomous loop flips PENDING -> DONE after it
    executes the directive, so the dashboard can show whether it was picked up.
    """
    raw = read_text_file(DIRECTIVE_FILE, "")
    if not raw.strip():
        return {"present": False, "status": "NONE", "updated": "", "directive": ""}

    def _section(name: str, to_end: bool = False) -> str:
        # Directive is always the final section, and its body is free-form
        # markdown that may itself contain "## " headings — so for it we must
        # capture to end-of-file (to_end) instead of stopping at the next "## ",
        # which would silently truncate the displayed directive.
        terminator = r"\Z" if to_end else r"(?=^##\s+|\Z)"
        match = re.search(
            rf"^##\s+{name}\s*$\n(.*?){terminator}",
            raw,
            re.MULTILINE | re.DOTALL,
        )
        return match.group(1).strip() if match else ""

    status = (_section("Status") or "PENDING").splitlines()[0].strip().upper()
    if status not in {"PENDING", "DONE"}:
        status = "PENDING"
    return {
        "present": True,
        "status": status,
        "updated": _section("Updated"),
        "directive": _section("Directive", to_end=True),
    }


def write_directive(text: str) -> dict[str, Any]:
    """Write a new PENDING human directive. Overwrites any previous one."""
    clean = text.strip()
    if not clean:
        raise ValueError("directive text is empty")
    if len(clean) > DIRECTIVE_MAX_CHARS:
        raise ValueError(f"directive too long (max {DIRECTIVE_MAX_CHARS} chars)")

    updated = datetime.now(timezone.utc).isoformat()
    body = (
        "# Human Directive\n\n"
        "<!-- Set by the dashboard Director panel. The autonomous loop must\n"
        "     treat a PENDING directive as the top priority for this cycle,\n"
        "     then set Status to DONE once it has been acted on. -->\n\n"
        "## Status\nPENDING\n\n"
        f"## Updated\n{updated}\n\n"
        f"## Directive\n{clean}\n"
    )
    DIRECTIVE_FILE.parent.mkdir(parents=True, exist_ok=True)
    DIRECTIVE_FILE.write_text(body, encoding="utf-8")
    return read_directive()


def _parse_env_file(raw: str) -> dict[str, str]:
    """Parse simple KEY=value lines (ignores blanks/comments)."""
    out: dict[str, str] = {}
    for line in raw.splitlines():
        s = line.strip()
        if not s or s.startswith("#") or "=" not in s:
            continue
        k, _, v = s.partition("=")
        k = k.strip()
        v = v.strip().strip('"').strip("'")
        if k:
            out[k] = v
    return out


def read_ideas() -> dict[str, Any]:
    """Read the live candidate registry (memories/candidate-registry.md) for the Ideas panel.

    The loop stopped maintaining a single docs/research/opportunity-scan.md after the
    discovery-directive rewrite (Cycle 106): per-cycle scans go to cycleNNN-*.md and the
    cumulative, framework-ranked record now lives in the lean candidate-registry.md.
    """
    raw = read_text_file(CANDIDATE_REGISTRY_FILE, "")
    updated = ""
    try:
        if CANDIDATE_REGISTRY_FILE.exists():
            import datetime

            updated = datetime.datetime.fromtimestamp(
                CANDIDATE_REGISTRY_FILE.stat().st_mtime, tz=datetime.timezone.utc
            ).isoformat()
    except OSError:
        pass
    return {"present": bool(raw.strip()), "updated": updated, "markdown": raw}


def read_analysis() -> dict[str, Any]:
    """Read the Opportunity Analyst output (memories/analysis-directive.md) for the Analyst panel."""
    raw = read_text_file(ANALYSIS_FILE, "")
    updated = ""
    try:
        if ANALYSIS_FILE.exists():
            import datetime

            updated = datetime.datetime.fromtimestamp(
                ANALYSIS_FILE.stat().st_mtime, tz=datetime.timezone.utc
            ).isoformat()
    except OSError:
        pass
    return {"present": bool(raw.strip()), "updated": updated, "markdown": raw}


DIRECTIVE_TEMPLATES_DIR = REPO_ROOT / "dashboard" / "directive-templates"
# Copy-to-clipboard directive templates shown as buttons in the Director panel.
# Order + labels here; body text lives in dashboard/directive-templates/*.md.
DIRECTIVE_TEMPLATES = [
    {"id": "hold-and-discover", "label": "Hold + Discover", "file": "01-hold-and-discover.md",
     "hint": "Park a candidate on a named blocker (keep its machine intact) + make discovery the primary activity."},
    {"id": "continuous-discovery", "label": "Discovery", "file": "02-continuous-discovery.md",
     "hint": "No new hold; force continuous discovery + carry the standing blocked/pending register."},
    {"id": "unhold-and-validate", "label": "Un-hold + Validate", "file": "03-unhold-and-validate.md",
     "hint": "A blocker cleared → un-HOLD a candidate + start its human-run cheapest WTP validation."},
    {"id": "select-and-validate", "label": "Select + Validate", "file": "04-select-and-validate.md",
     "hint": "Adopt a candidate (e.g. the Opportunity Analyst pick) + run its cheapest WTP test."},
]


def read_directive_templates() -> dict[str, Any]:
    """Return the Director-panel copy templates (label + hint + full body text)."""
    out = []
    for t in DIRECTIVE_TEMPLATES:
        text = read_text_file(DIRECTIVE_TEMPLATES_DIR / t["file"], "")
        if text.strip():
            out.append({"id": t["id"], "label": t["label"], "hint": t["hint"], "text": text})
    return {"templates": out}


def read_settings() -> dict[str, Any]:
    """Return the Settings-panel spec + current values from logs/runtime.env.

    Only whitelisted keys are surfaced. A missing/blank value means the knob is
    unset (the container falls back to its Coolify env / Dockerfile default).
    """
    current = _parse_env_file(read_text_file(RUNTIME_ENV_FILE, ""))
    values = {s["key"]: current.get(s["key"], "") for s in SETTINGS_SPEC}
    return {
        "present": RUNTIME_ENV_FILE.exists(),
        "path": str(RUNTIME_ENV_FILE),
        "spec": SETTINGS_SPEC,
        "values": values,
        "needsRestart": True,
    }


def write_settings(incoming: dict[str, Any]) -> dict[str, Any]:
    """Write whitelisted KEY=value knobs to logs/runtime.env.

    Rejects any non-whitelisted key (so secrets can never be written here). Keys
    with a blank value are omitted from the file (revert to the default).
    """
    bad = [k for k in incoming if k not in SETTINGS_KEYS]
    if bad:
        raise ValueError(f"unknown setting(s): {', '.join(sorted(bad))}")

    # Preserve any non-whitelisted keys already in the file (e.g. an operator-set
    # COOLIFY_DEPLOY_TOKEN used by the Redeploy button) — the panel only manages the
    # whitelist, it must not wipe other overrides.
    existing_all = _parse_env_file(read_text_file(RUNTIME_ENV_FILE, ""))
    preserved = {k: v for k, v in existing_all.items() if k not in SETTINGS_KEYS}

    lines = [
        "# Auto-Company runtime overrides — sourced by docker-entrypoint.sh on start.",
        "# Managed by the cockpit Settings panel. Non-secret config only.",
        f"# Updated {datetime.now(timezone.utc).isoformat()}",
        "",
    ]
    for k, v in preserved.items():
        lines.append(f"{k}={v}")
    if preserved:
        lines.append("")
    for spec in SETTINGS_SPEC:
        key = spec["key"]
        if key not in incoming:
            # preserve an existing value not included in this write
            existing = _parse_env_file(read_text_file(RUNTIME_ENV_FILE, "")).get(key, "")
            val = existing
        else:
            val = str(incoming[key]).strip()
        if spec["type"] == "bool":
            val = "1" if val in {"1", "true", "True", "on", "yes"} else ("0" if val != "" else "")
        if val == "":
            continue  # unset -> omit -> falls back to container default
        if spec["type"] == "number":
            # keep only a sane numeric-ish token; reject junk
            if not re.fullmatch(r"[0-9]+(?:\.[0-9]+)?", val):
                raise ValueError(f"{key} must be a number, got '{val}'")
        lines.append(f"{key}={val}")

    RUNTIME_ENV_FILE.parent.mkdir(parents=True, exist_ok=True)
    RUNTIME_ENV_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return read_settings()


def trigger_redeploy() -> dict[str, Any]:
    """Trigger a Coolify redeploy so runtime.env changes take effect.

    Needs COOLIFY_APP_UUID (+ COOLIFY_DEPLOY_TOKEN, COOLIFY_URL) in the container
    env. Degrades gracefully with a clear message when not configured, so editing
    settings works even before the deploy webhook is wired.
    """
    uuid = os.environ.get("COOLIFY_APP_UUID", "").strip()
    token = os.environ.get("COOLIFY_DEPLOY_TOKEN", "").strip()
    base = os.environ.get("COOLIFY_URL", "https://app.coolify.io").strip().rstrip("/")
    if not uuid or not token:
        return {
            "ok": False,
            "configured": False,
            "error": "Redeploy not configured. Set COOLIFY_APP_UUID + "
                     "COOLIFY_DEPLOY_TOKEN (deploy-scoped) in the container env.",
        }
    import urllib.error
    import urllib.request

    url = f"{base}/api/v1/deploy?uuid={uuid}&force=false"
    # Cloudflare returns error 1010 (banned browser signature) to urllib's default
    # User-Agent — a browser-like UA is required, not optional. See
    # memories/redeploy-auto-company.md.
    req = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {token}", "User-Agent": "Mozilla/5.0"},
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:  # noqa: S310
            body = resp.read().decode("utf-8", "replace")[:500]
            return {"ok": True, "configured": True, "status": resp.status, "response": body}
    except urllib.error.HTTPError as exc:
        return {"ok": False, "configured": True, "status": exc.code,
                "error": exc.read().decode("utf-8", "replace")[:300]}
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "configured": True, "error": str(exc)}


# --- ccusage integration (optional, prototype) -------------------------------
# ccusage (https://github.com/ryoppippi/ccusage) reads the local agent transcripts
# (~/.claude/projects + Codex sessions under $CODEX_HOME) and prices tokens against a
# cached table. It fills the loop ledger's blind spot: a $ ESTIMATE for Codex (whose
# ChatGPT-auth runs carry no USD) and a per-model Claude/Codex split. NOTE: this is an
# API-EQUIVALENT estimate, not billed spend — the company runs on flat subscriptions.
# Shelled out + cached (CCUSAGE_TTL_SECONDS), refreshed in a background thread so it
# never blocks the /api/status poll. Fails open when ccusage is absent.
_CCUSAGE_CACHE: dict[str, Any] = {"at": 0.0, "data": None}
_CCUSAGE_REFRESHING = {"v": False}
_CCUSAGE_TTL = int(os.environ.get("CCUSAGE_TTL_SECONDS", "600"))


def _ccusage_compute() -> dict[str, Any]:
    cmd_str = os.environ.get("CCUSAGE_CMD", "ccusage")
    days = int(os.environ.get("CCUSAGE_WINDOW_DAYS", "30"))
    since = datetime.fromtimestamp(time.time() - days * 86400, timezone.utc).strftime("%Y%m%d")
    base = shlex.split(cmd_str) + ["daily", "--json", "--since", since]

    def _run(extra: list[str]) -> str | None:
        try:
            proc = subprocess.run(
                base + extra, cwd=str(REPO_ROOT), capture_output=True,
                text=True, encoding="utf-8", errors="replace", timeout=45,
            )
        except Exception:
            return None
        return (proc.stdout or "").strip() or None

    # Try online (fetches/caches pricing); fall back to --offline for air-gapped hosts.
    raw = _run([]) or _run(["--offline"])
    if not raw:
        return {"available": False, "reason": "ccusage not installed / no output"}

    try:
        daily = (json.loads(raw).get("daily") or [])
        model_cost: dict[str, float] = {}
        for day in daily:
            for mb in (day.get("modelBreakdowns") or []):
                name = str(mb.get("modelName", "?"))
                model_cost[name] = model_cost.get(name, 0.0) + float(mb.get("cost", 0) or 0)

        def _is_codex(n: str) -> bool:
            n = n.lower()
            return n.startswith(("gpt", "o1", "o3", "o4")) or "codex" in n

        claude_cost = sum(c for n, c in model_cost.items() if "claude" in n.lower())
        codex_cost = sum(c for n, c in model_cost.items() if _is_codex(n))
        models = sorted(
            ({"name": n, "cost": round(c, 2)} for n, c in model_cost.items()),
            key=lambda m: m["cost"], reverse=True,
        )[:6]
        today = None
        if daily:
            last = daily[-1]
            today = {"date": str(last.get("period", "")),
                     "cost": round(float(last.get("totalCost", 0) or 0), 2)}
        return {
            "available": True,
            "totalCost": round(sum(model_cost.values()), 2),
            "claudeCost": round(claude_cost, 2),
            "codexCost": round(codex_cost, 2),
            "days": len(daily),
            "since": since,
            "today": today,
            "models": models,
        }
    except Exception as exc:  # pragma: no cover - defensive
        return {"available": False, "reason": f"parse error: {exc}"[:120]}


def read_ccusage() -> dict[str, Any]:
    """Return the cached ccusage estimate; refresh in the background when stale.

    Never blocks: the first call returns a pending marker and kicks off a thread;
    later polls pick up the computed result once it lands.
    """
    now = time.time()
    data = _CCUSAGE_CACHE.get("data")
    fresh = data is not None and (now - float(_CCUSAGE_CACHE.get("at", 0))) < _CCUSAGE_TTL
    if not fresh and not _CCUSAGE_REFRESHING["v"]:
        _CCUSAGE_REFRESHING["v"] = True

        def _bg() -> None:
            try:
                result = _ccusage_compute()
                _CCUSAGE_CACHE.update(at=time.time(), data=result)
            finally:
                _CCUSAGE_REFRESHING["v"] = False

        threading.Thread(target=_bg, daemon=True).start()
    return data if data is not None else {"available": False, "reason": "computing"}


def read_engine_runtime() -> dict[str, Any]:
    """The ACTUAL per-cycle routed engine — Runtime State otherwise shows only the base config.

    The loop boots with ENGINE=claude / MODEL=haiku, but the quota-aware router overrides the
    engine every cycle and a round-robin tier ladder picks the model/effort. This parses the
    log's latest [ROUTER]/[TIER] lines + logs/router-state to surface the real active engine,
    model, effort, the tier ladders, the round-robin index, and the next pick.
    """
    text = read_text_file(LOG_FILE, "")
    engine = read_text_file(LOG_FILE.parent / "router-state", "").strip().lower()
    out: dict[str, Any] = {"routedEngine": engine}

    # Tolerant to both the fill-weighted line and the legacy round-robin line.
    tiers = re.findall(
        r"\[TIER\] (\S+).*?Claude=([^\s,\[]+).*?Codex effort=(\w+)", text)
    if tiers:
        mode, cmodel, ceff = tiers[-1]
        out["tierMode"] = mode
        out["claudePick"] = cmodel
        out["codexEffort"] = ceff
        if engine == "codex":
            out["routedModel"] = os.environ.get("CODEX_MODEL", "gpt-5.6-sol")
            out["routedEffort"] = ceff
        else:
            out["routedModel"] = cmodel
            out["routedEffort"] = ""

    routers = re.findall(r"\[ROUTER\] (.+)", text)
    if routers:
        out["routerReason"] = routers[-1].strip()[:180]

    m = re.search(r"Tier ladder:.*?Claude \[([^\]]*)\].*?Codex effort \[([^\]]*)\]", text)
    if m:
        out["claudeLadder"] = [s.strip() for s in m.group(1).split(",") if s.strip()]
        out["codexLadder"] = [s.strip() for s in m.group(2).split(",") if s.strip()]

    mb = re.search(r"Window budget: \$([0-9.]+) per (\d+)s", text)
    if mb:
        out["windowBudget"] = mb.group(1)
    itv = re.findall(r"Interval: (\d+)s", text)
    if itv:
        out["interval"] = itv[-1]

    return out


def read_cost_summary() -> dict[str, Any]:
    """Aggregate cycle cost from auto-loop.log + credit status from ~/.claude.json.

    Cost lines look like: `... [OK] Completed (cost: 2.2577963, subtype: success)`.
    """
    text = read_text_file(LOG_FILE, "")
    costs: list[float] = []
    for m in re.finditer(r"cost:\s*([0-9]+(?:\.[0-9]+)?)\b", text):
        try:
            costs.append(float(m.group(1)))
        except ValueError:
            pass

    credit_reason = ""
    try:
        cj = Path.home() / ".claude.json"
        if cj.exists():
            data = json.loads(cj.read_text(encoding="utf-8"))
            credit_reason = str(data.get("cachedExtraUsageDisabledReason", "") or "")
    except Exception:  # pragma: no cover - defensive
        credit_reason = ""

    window_usd = 0.0
    try:
        ledger = LOG_FILE.parent / "spend-window.log"
        if ledger.exists():
            cutoff = time.time() - int(os.environ.get("WINDOW_SECONDS", "18000"))
            for line in ledger.read_text(encoding="utf-8").splitlines():
                parts = line.split()
                if len(parts) == 2:
                    try:
                        ts, c = float(parts[0]), float(parts[1])
                        if ts >= cutoff:
                            window_usd += c
                    except ValueError:
                        pass
    except Exception:  # pragma: no cover - defensive
        window_usd = 0.0

    # Current routed engine (the loop writes claude|codex to logs/router-state).
    engine = read_text_file(LOG_FILE.parent / "router-state", "").strip().lower() or ""

    # Codex cycles inside the rolling window (each line in codex-window.log is one
    # completed Codex cycle: "<epoch> <count> ..."). Lets the operator SEE Codex is
    # carrying load even though Codex cycles cost $0 (ChatGPT-auth) so windowUsd stays flat.
    codex_window = 0
    try:
        cl = LOG_FILE.parent / "codex-window.log"
        if cl.exists():
            ccut = time.time() - int(os.environ.get("WINDOW_SECONDS", "18000"))
            for line in cl.read_text(encoding="utf-8").splitlines():
                parts = line.split()
                if parts:
                    try:
                        if float(parts[0]) >= ccut:
                            codex_window += 1
                    except ValueError:
                        pass
    except Exception:  # pragma: no cover - defensive
        codex_window = 0

    # Budget offloads to Codex. The router logs "... offloading to Codex"; older builds
    # tagged "[BUDGET-CODEX]". Count both so the counter reflects real offloads.
    budget_offloads = text.count("offloading to Codex") + text.count("[BUDGET-CODEX]")

    return {
        "totalUsd": round(sum(costs), 4),
        "lastUsd": round(costs[-1], 4) if costs else 0.0,
        "cycles": len(costs),
        "creditReason": credit_reason,
        "limitHits": text.count("[LIMIT]"),
        "windowUsd": round(window_usd, 4),
        "windowBudget": os.environ.get("WINDOW_BUDGET_USD", "") or "",
        "fallbackHits": text.count("[FALLBACK]"),
        "budgetPauses": text.count("[BUDGET]"),
        "budgetOffloads": budget_offloads,
        "engine": engine,
        "codexWindow": codex_window,
        "ccusage": read_ccusage(),
    }


def read_tail(path: Path, lines: int = 120) -> str:
    if lines <= 0:
        return ""
    text = read_text_file(path, "")
    if not text:
        return ""
    rows = text.splitlines()
    return "\n".join(rows[-lines:])


def parse_sections(raw: str) -> dict[str, list[str]]:
    section_re = re.compile(r"^=== (.+) ===$")
    sections: dict[str, list[str]] = {}
    current: str | None = None

    for line in raw.splitlines():
        row = line.rstrip("\n")
        match = section_re.match(row.strip())
        if match:
            current = match.group(1)
            sections[current] = []
            continue
        if current is not None:
            sections[current].append(row)

    return sections


def parse_int(value: str | None) -> int | None:
    if not value:
        return None
    value = value.strip()
    return int(value) if value.isdigit() else None


def parse_positive_int(value: str | None, default: int) -> int:
    try:
        parsed = int(value or "")
    except (TypeError, ValueError):
        return default
    return parsed if parsed > 0 else default


def parse_key_values(rows: list[str]) -> dict[str, str]:
    values: dict[str, str] = {}
    for row in rows:
        if "=" not in row:
            continue
        key, value = row.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def blank_parsed() -> dict[str, Any]:
    return {
        "guardian": {"state": "unknown", "pid": None, "raw": ""},
        "autostart": {"state": "unknown", "raw": ""},
        "daemon": {
            "state": "unknown",
            "activeState": "unknown",
            "subState": "unknown",
            "mainPid": None,
            "raw": "",
        },
        "loop": {
            "state": "unknown",
            "pid": None,
            "daemonSummary": "unknown",
            "engine": "",
            "model": "",
            "lastRun": "",
            "errorCount": "",
            "loopCount": "",
            "raw": "",
        },
        "consensusPreview": "",
        "recentLog": "",
    }


def parse_windows_status_output(raw: str) -> dict[str, Any]:
    sections = parse_sections(raw)
    parsed = blank_parsed()

    guardian_rows = sections.get("Windows Guardian", [])
    guardian_line = next(
        (x.strip() for x in guardian_rows if x.strip().startswith("Awake guardian:")),
        "",
    )
    parsed["guardian"]["raw"] = "\n".join(guardian_rows).strip()
    if guardian_line:
        parsed["guardian"]["raw"] = guardian_line
        if "STOPPED" in guardian_line:
            parsed["guardian"]["state"] = "stopped"
        elif "RUNNING" in guardian_line:
            parsed["guardian"]["state"] = "running"
            pid_match = re.search(r"PID (\d+)", guardian_line)
            parsed["guardian"]["pid"] = int(pid_match.group(1)) if pid_match else None

    autostart_rows = sections.get("Windows Autostart Task", [])
    autostart_line = next(
        (x.strip() for x in autostart_rows if x.strip().startswith("Autostart:")),
        "",
    )
    parsed["autostart"]["raw"] = "\n".join(autostart_rows).strip()
    if autostart_line:
        parsed["autostart"]["raw"] = autostart_line
        if "NOT CONFIGURED" in autostart_line:
            parsed["autostart"]["state"] = "not_configured"
        elif "CONFIGURED" in autostart_line:
            parsed["autostart"]["state"] = "configured"

    daemon_rows = sections.get("WSL Daemon (systemd --user)", [])
    parsed["daemon"]["raw"] = "\n".join(daemon_rows).strip()
    daemon_compact = [x.strip() for x in daemon_rows if x.strip()]
    if daemon_compact:
        first = daemon_compact[0]
        lowered = first.lower()
        if "not installed" in lowered:
            parsed["daemon"]["state"] = "not_installed"
        elif first == "active":
            parsed["daemon"]["state"] = "active"
        elif first in {"inactive", "activating", "failed"}:
            parsed["daemon"]["state"] = "inactive"
        for row in daemon_compact:
            if row.startswith("MainPID="):
                parsed["daemon"]["mainPid"] = parse_int(row.split("=", 1)[1])
            elif row.startswith("ActiveState="):
                parsed["daemon"]["activeState"] = row.split("=", 1)[1].strip()
            elif row.startswith("SubState="):
                parsed["daemon"]["subState"] = row.split("=", 1)[1].strip()

    loop_rows = sections.get("Loop Status (scripts/core/monitor.sh)", [])
    if not loop_rows:
        loop_rows = sections.get("Loop Status (monitor.sh)", [])
    loop_status_rows = sections.get("Auto Company Status", [])
    merged_loop_rows = list(loop_rows) + list(loop_status_rows)
    parsed["loop"]["raw"] = "\n".join(merged_loop_rows).strip()
    for row in (x.strip() for x in merged_loop_rows if x.strip()):
        if row.startswith("Loop:"):
            if "NOT RUNNING" in row or "STOPPED" in row:
                parsed["loop"]["state"] = "stopped"
                parsed["loop"]["pid"] = None
            elif "RUNNING" in row:
                parsed["loop"]["state"] = "running"
                pid_match = re.search(r"PID (\d+)", row)
                parsed["loop"]["pid"] = int(pid_match.group(1)) if pid_match else None
        elif row.startswith("Daemon:"):
            parsed["loop"]["daemonSummary"] = row.replace("Daemon:", "", 1).strip()
        elif row.startswith("ENGINE="):
            parsed["loop"]["engine"] = row.split("=", 1)[1].strip()
        elif row.startswith("MODEL="):
            parsed["loop"]["model"] = row.split("=", 1)[1].strip()
        elif row.startswith("LAST_RUN="):
            parsed["loop"]["lastRun"] = row.split("=", 1)[1].strip()
        elif row.startswith("ERROR_COUNT="):
            parsed["loop"]["errorCount"] = row.split("=", 1)[1].strip()
        elif row.startswith("LOOP_COUNT="):
            parsed["loop"]["loopCount"] = row.split("=", 1)[1].strip()

    parsed["consensusPreview"] = "\n".join(sections.get("Latest Consensus", [])).strip()
    parsed["recentLog"] = "\n".join(sections.get("Recent Log", [])).strip()
    return parsed


def parse_macos_status_output(raw: str) -> dict[str, Any]:
    sections = parse_sections(raw)
    parsed = blank_parsed()

    guardian_fields = parse_key_values(sections.get("Guardian", []))
    parsed["guardian"]["state"] = guardian_fields.get("State", "unknown") or "unknown"
    parsed["guardian"]["pid"] = parse_int(guardian_fields.get("Pid"))
    parsed["guardian"]["raw"] = guardian_fields.get("Raw", "")

    daemon_fields = parse_key_values(sections.get("Daemon", []))
    daemon_state = daemon_fields.get("State", "unknown") or "unknown"
    parsed["daemon"]["state"] = daemon_state
    parsed["daemon"]["mainPid"] = parse_int(daemon_fields.get("MainPID"))
    parsed["daemon"]["raw"] = daemon_fields.get("Raw", "")
    parsed["daemon"]["activeState"] = daemon_fields.get("ActiveState", daemon_state)
    parsed["daemon"]["subState"] = daemon_fields.get("SubState", "unknown")

    autostart_fields = parse_key_values(sections.get("Autostart", []))
    parsed["autostart"]["state"] = autostart_fields.get("State", "unknown") or "unknown"
    parsed["autostart"]["raw"] = autostart_fields.get("Raw", "")

    loop_fields = parse_key_values(sections.get("Loop", []))
    parsed["loop"]["state"] = loop_fields.get("State", "unknown") or "unknown"
    parsed["loop"]["pid"] = parse_int(loop_fields.get("Pid"))
    parsed["loop"]["raw"] = "\n".join(sections.get("Loop", [])).strip()
    parsed["loop"]["daemonSummary"] = loop_fields.get("DaemonSummary", "unknown")

    state_file_fields = parse_key_values(sections.get("State File", []))
    parsed["loop"]["engine"] = state_file_fields.get("ENGINE", "")
    parsed["loop"]["model"] = state_file_fields.get("MODEL", "")
    parsed["loop"]["lastRun"] = state_file_fields.get("LAST_RUN", "")
    parsed["loop"]["errorCount"] = state_file_fields.get("ERROR_COUNT", "")
    parsed["loop"]["loopCount"] = state_file_fields.get("LOOP_COUNT", "")

    parsed["consensusPreview"] = "\n".join(sections.get("Latest Consensus", [])).strip()
    parsed["recentLog"] = "\n".join(sections.get("Recent Log", [])).strip()
    return parsed


def read_state_file_pairs() -> dict[str, str]:
    state_text = read_text_file(STATE_FILE, "").strip()
    state_pairs: dict[str, str] = {}
    if state_text:
        for row in state_text.splitlines():
            if "=" in row:
                key, value = row.split("=", 1)
                state_pairs[key.strip()] = value.strip()
    return state_pairs


def run_status_command(system_name: str | None = None) -> dict[str, Any]:
    profile = get_host_profile(system_name)
    runner = profile["runner"]
    return runner(profile["status_script"], timeout=90)


def run_dashboard_action(action: str, system_name: str | None = None) -> dict[str, Any]:
    profile = get_host_profile(system_name)
    if action == "start":
        return profile["runner"](
            profile["start_script"], args=profile["start_args"], timeout=120
        )
    if action == "stop":
        return profile["runner"](
            profile["stop_script"], args=profile["stop_args"], timeout=120
        )
    if action == "refresh":
        return profile["runner"](profile["status_script"], timeout=90)
    raise ValueError(f"Unsupported dashboard action: {action}")


def parse_status_output(raw: str, system_name: str | None = None) -> dict[str, Any]:
    profile = get_host_profile(system_name)
    return profile["parser"](raw)


def gather_status_payload(system_name: str | None = None) -> dict[str, Any]:
    result = run_status_command(system_name)
    parsed = parse_status_output(result["output"], system_name)
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "ok": result["ok"],
        "exitCode": result["exitCode"],
        "elapsedMs": result["elapsedMs"],
        "hostKind": detect_host_kind(system_name),
        "raw": result["output"],
        "parsed": parsed,
        "stateFile": read_state_file_pairs(),
        "consensusHead": read_text_file(CONSENSUS_FILE, "(no consensus file)")[:3000],
        "logTail": read_tail(LOG_FILE, lines=180),
        "directive": read_directive(),
        "cost": read_cost_summary(),
        "router": read_engine_runtime(),
    }


class DashboardHandler(BaseHTTPRequestHandler):
    def _json(self, payload: dict[str, Any], code: int = 200) -> None:
        raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def _text(
        self, text: str, code: int = 200, content_type: str = "text/plain; charset=utf-8"
    ) -> None:
        raw = text.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def _serve_file(self, path: Path, content_type: str) -> None:
        if not path.exists():
            self._text("Not found", code=404)
            return
        self._text(path.read_text(encoding="utf-8"), content_type=content_type)

    def do_GET(self) -> None:  # noqa: N802
        try:
            self._do_GET()
        except Exception:
            sentry_client.capture_exception(extra={"method": "GET", "path": self.path})
            raise

    def _do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/" or path == "/index.html":
            self._serve_file(DASHBOARD_DIR / "index.html", "text/html; charset=utf-8")
            return
        if path == "/app.js":
            self._serve_file(
                DASHBOARD_DIR / "app.js",
                "application/javascript; charset=utf-8",
            )
            return
        if path == "/styles.css":
            self._serve_file(DASHBOARD_DIR / "styles.css", "text/css; charset=utf-8")
            return
        if path == "/favicon.svg":
            self._serve_file(DASHBOARD_DIR / "favicon.svg", "image/svg+xml")
            return
        if path == "/api/status":
            self._json(gather_status_payload())
            return
        if path == "/api/log-tail":
            qs = parse_qs(parsed.query)
            lines = parse_positive_int(qs.get("lines", ["180"])[0], default=180)
            self._json(
                {
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "lines": lines,
                    "logTail": read_tail(LOG_FILE, lines=lines),
                }
            )
            return
        if path == "/api/ideas":
            self._json(read_ideas())
            return
        if path == "/api/analysis":
            self._json(read_analysis())
            return
        if path == "/api/settings":
            self._json(read_settings())
            return
        if path == "/api/directive-templates":
            self._json(read_directive_templates())
            return

        self._text("Not found", code=404)

    def _read_body(self, limit: int = 64 * 1024) -> bytes:
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            length = 0
        if length <= 0:
            return b""
        return self.rfile.read(min(length, limit))

    def do_POST(self) -> None:  # noqa: N802
        try:
            self._do_POST()
        except Exception:
            sentry_client.capture_exception(extra={"method": "POST", "path": self.path})
            raise

    def _do_POST(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/api/directive":
            self._handle_directive()
            return

        if path == "/api/settings":
            self._handle_settings()
            return

        if path == "/api/redeploy":
            result = trigger_redeploy()
            result["timestamp"] = datetime.now(timezone.utc).isoformat()
            self._json(result, code=HTTPStatus.OK if result.get("ok") else HTTPStatus.BAD_REQUEST)
            return

        if path not in {"/api/action/start", "/api/action/stop", "/api/action/refresh"}:
            self._text("Not found", code=404)
            return

        action = path.rsplit("/", 1)[-1]
        result = run_dashboard_action(action)
        payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "action": action,
            "ok": result["ok"],
            "exitCode": result["exitCode"],
            "elapsedMs": result["elapsedMs"],
            "output": result["output"],
        }
        self._json(payload, code=HTTPStatus.OK if result["ok"] else HTTPStatus.BAD_REQUEST)

    def _handle_directive(self) -> None:
        body = self._read_body()
        text = ""
        try:
            data = json.loads(body.decode("utf-8")) if body else {}
            if isinstance(data, dict):
                text = str(data.get("directive", ""))
        except (ValueError, UnicodeDecodeError):
            text = ""

        try:
            directive = write_directive(text)
        except ValueError as exc:
            self._json(
                {
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "ok": False,
                    "error": str(exc),
                },
                code=HTTPStatus.BAD_REQUEST,
            )
            return

        self._json(
            {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "ok": True,
                "directive": directive,
            }
        )

    def _handle_settings(self) -> None:
        body = self._read_body()
        incoming: dict[str, Any] = {}
        try:
            data = json.loads(body.decode("utf-8")) if body else {}
            if isinstance(data, dict):
                incoming = data.get("values", data) if isinstance(data.get("values", data), dict) else {}
        except (ValueError, UnicodeDecodeError):
            incoming = {}

        try:
            settings = write_settings(incoming)
        except ValueError as exc:
            self._json(
                {
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "ok": False,
                    "error": str(exc),
                },
                code=HTTPStatus.BAD_REQUEST,
            )
            return

        self._json(
            {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "ok": True,
                "settings": settings,
            }
        )

    def log_message(self, fmt: str, *args: Any) -> None:  # noqa: A003
        _ = (fmt, args)


def main() -> None:
    parser = argparse.ArgumentParser(description="Auto Company web dashboard server")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8787)
    args = parser.parse_args()

    try:
        host_kind = detect_host_kind()
    except RuntimeError as exc:
        print(f"[dashboard] {exc}")
        raise SystemExit(1) from exc

    server = ThreadingHTTPServer((args.host, args.port), DashboardHandler)
    print(f"[dashboard] serving on http://{args.host}:{args.port}")
    print(f"[dashboard] repo: {REPO_ROOT}")
    print(f"[dashboard] host: {host_kind}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        print("[dashboard] stopped")


if __name__ == "__main__":
    os.chdir(REPO_ROOT)
    main()
