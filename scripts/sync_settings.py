#!/usr/bin/env python3
"""Create or update .vscode/settings.json from .vscode/settings.default.json.

settings.json is gitignored so VS Code, the Toggle File Visibility task and
your own tweaks can change it without blocking `git pull`.

- If settings.json is missing, it is copied from the defaults.
- Otherwise, any top-level setting in the defaults that settings.json lacks is
  added. Settings already in settings.json are never changed.
"""
import json
import shutil
import sys
from pathlib import Path

VSCODE = Path(__file__).parent.parent / ".vscode"
DEFAULTS = VSCODE / "settings.default.json"
SETTINGS = VSCODE / "settings.json"


def ensure_settings(quiet=False):
    if not DEFAULTS.exists():
        return
    if not SETTINGS.exists():
        shutil.copyfile(DEFAULTS, SETTINGS)
        print("  settings.json: created from settings.default.json")
        return
    defaults = json.loads(DEFAULTS.read_text(encoding="utf-8"))
    try:
        settings = json.loads(SETTINGS.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        # Comments or trailing commas: leave the file alone rather than lose them.
        print("  settings.json: has comments or isn't plain JSON, skipped default sync")
        return
    missing = [k for k in defaults if k not in settings]
    if not missing:
        if not quiet:
            print("  settings.json: up to date")
        return
    for key in missing:
        settings[key] = defaults[key]
    SETTINGS.write_text(json.dumps(settings, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"  settings.json: added {', '.join(missing)}")


if __name__ == "__main__":
    ensure_settings()
    sys.exit(0)
