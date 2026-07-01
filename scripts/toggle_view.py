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


env = read_env()
hide = env.get("HIDE_CLUTTER", "true").lower() not in ("false", "0", "no")

settings = json.loads(SETTINGS.read_text())
settings["files.exclude"] = HIDDEN if hide else {}
SETTINGS.write_text(json.dumps(settings, indent=2) + "\n")
print(f"  HIDE_CLUTTER={str(hide).lower()} → files.exclude {'applied' if hide else 'cleared'}")
