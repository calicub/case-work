#!/usr/bin/env zsh
# Installs (or reinstalls) the Jira Reminders launchd schedule.
# Run once per machine via VS Code Task: "⏰ Install Jira Reminders Schedule"

set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
PLIST_SRC="$REPO/setup/com.casework.jira-reminders.plist"
PLIST_DEST="$HOME/Library/LaunchAgents/com.casework.jira-reminders.plist"

# Unload any existing version first (ignore error if not loaded)
launchctl unload "$PLIST_DEST" 2>/dev/null || true

# Stamp the real repo path into the plist
sed "s|REPO_PATH|$REPO|g" "$PLIST_SRC" > "$PLIST_DEST"

# Load it
launchctl load "$PLIST_DEST"

echo ""
echo "✅  Schedule installed."
echo "    Runs at 09:30 and 12:30 every day."
echo "    Logs → /tmp/jira-reminders.log"
echo ""
echo "To uninstall:"
echo "    launchctl unload ~/Library/LaunchAgents/com.casework.jira-reminders.plist"
echo "    rm ~/Library/LaunchAgents/com.casework.jira-reminders.plist"
