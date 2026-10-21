#!/usr/bin/env bash
# Take a screenshot for the case note that's open in VS Code and insert it.
#
# Uses macOS's built-in selection tool: drag to capture an area, press Space
# to capture a window, or Esc to cancel. The image is named after the case
# number and handed to insert_assets.py, which moves it into
# docs/assets/screenshots/ and adds it to the note's 📸 Screenshots tab.
#
# Usage: capture_screenshot.sh <case-note.md>

set -euo pipefail

NOTE="${1:-}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

if [[ -z "$NOTE" || ! -f "$NOTE" ]]; then
  echo "❌  Open a case note first (click into it), then run this task again."
  exit 1
fi

CASE_NUM=$(grep -m1 '^case_number:' "$NOTE" | sed 's/^case_number:[[:space:]]*//' | tr -d '\r' || true)
if [[ -z "$CASE_NUM" ]]; then
  echo "❌  '$(basename "$NOTE")' has no case_number, so it isn't a case note. Click into a case note and try again."
  exit 1
fi

DEST="$ROOT/${CASE_NUM}-screenshot-$(date +%Y-%m-%d-%H%M%S).png"

echo "📸  Select an area (drag), press Space for a window, or Esc to cancel..."
# -i interactive selection, -x no camera sound
if ! screencapture -i -x "$DEST"; then
  echo "❌  macOS couldn't take the screenshot. If it asked for Screen Recording access,"
  echo "    allow Visual Studio Code in System Settings → Privacy & Security → Screen & System Audio Recording,"
  echo "    then quit and reopen VS Code."
  exit 1
fi

if [[ ! -f "$DEST" ]]; then
  echo "Cancelled. No screenshot taken."
  exit 0
fi

PY="$ROOT/.venv/bin/python3"
[[ -x "$PY" ]] || PY="python3"
"$PY" "$ROOT/scripts/insert_assets.py" "$NOTE" --screenshots
