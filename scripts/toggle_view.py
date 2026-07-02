#!/usr/bin/env python3
"""Toggle files.exclude in settings.json, persisting the exclusion list to .env."""
import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
SETTINGS = ROOT / ".vscode" / "settings.json"
ENV_FILE = ROOT / ".env"

DEFAULT_HIDDEN = {
    "docs/guide.md": True,
    "docs/assets/stylesheets": True,
    "docs/dashboards": True,
    "docs/javascripts": True,
    "docs/stylesheets": True,
    "docs/index.md": True,
    "docs/dashboard.md": True,
    "docs/meetings.md": True,
    "docs/pkb.md": True,
    "docs/markdown.md": True,
}


def read_env():
    if not ENV_FILE.exists():
        return {}
    result = {}
    for line in ENV_FILE.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, _, v = line.partition("=")
            result[k.strip()] = v.strip().strip('"').strip("'")
    return result


def write_env(updates: dict):
    lines = []
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text().splitlines():
            key = line.strip().partition("=")[0].strip()
            if key not in updates:
                lines.append(line)
    for k, v in updates.items():
        lines.append(f"{k}={v}")
    ENV_FILE.write_text("\n".join(lines) + "\n")


env = read_env()
settings = json.loads(SETTINGS.read_text())

currently_hidden = bool(settings.get("files.exclude"))
hide = not currently_hidden

if hide:
    # Restore exclusion list from .env, falling back to the default
    stored = env.get("FILES_EXCLUDE")
    hidden = json.loads(stored) if stored else DEFAULT_HIDDEN
    settings["files.exclude"] = hidden
else:
    # Save current exclusion list to .env before clearing
    current_exclude = settings.get("files.exclude") or DEFAULT_HIDDEN
    settings["files.exclude"] = {}
    write_env({
        "HIDE_CLUTTER": "false",
        "FILES_EXCLUDE": json.dumps(current_exclude),
    })

SETTINGS.write_text(json.dumps(settings, indent=2) + "\n")

if hide:
    write_env({"HIDE_CLUTTER": "true"})

print(f"  HIDE_CLUTTER={str(hide).lower()} → files.exclude {'applied' if hide else 'cleared'}")
