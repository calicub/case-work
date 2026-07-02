#!/usr/bin/env python3
"""Apply AUTO_CLOSE_TERMINAL from .env to tasks.json presentation.close."""
import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
TASKS = ROOT / ".vscode" / "tasks.json"
ENV_FILE = ROOT / ".env"

# Tasks that should never auto-close regardless of the flag
NEVER_CLOSE = {"🖥️ Start Session Log", "⏰ Install Jira Reminders Schedule", "🟢 Start Zensical"}


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
close = env.get("AUTO_CLOSE_TERMINAL", "true").lower() not in ("false", "0", "no")

data = json.loads(TASKS.read_text())
for task in data.get("tasks", []):
    if task.get("label") in NEVER_CLOSE:
        continue
    presentation = task.setdefault("presentation", {})
    if "close" in presentation:
        presentation["close"] = close

TASKS.write_text(json.dumps(data, indent=2) + "\n")
print(f"  AUTO_CLOSE_TERMINAL={str(close).lower()} → terminal close {'enabled' if close else 'disabled'}")
