#!/usr/bin/env python3
"""Apply HIDE_CLUTTER from .env to settings.json files.exclude."""
import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
SETTINGS = ROOT / ".vscode" / "settings.json"
ENV_FILE = ROOT / ".env"

HIDDEN = {
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


settings = json.loads(SETTINGS.read_text())

# Detect current state from settings.json and flip it
currently_hidden = bool(settings.get("files.exclude"))
hide = not currently_hidden

settings["files.exclude"] = HIDDEN if hide else {}
SETTINGS.write_text(json.dumps(settings, indent=2) + "\n")

# Persist the new state to .env
env_lines = []
if ENV_FILE.exists():
    for line in ENV_FILE.read_text().splitlines():
        if not line.strip().startswith("HIDE_CLUTTER"):
            env_lines.append(line)
env_lines.append(f'HIDE_CLUTTER={"true" if hide else "false"}')
ENV_FILE.write_text("\n".join(env_lines) + "\n")

print(f"  HIDE_CLUTTER={str(hide).lower()} → files.exclude {'applied' if hide else 'cleared'}")
