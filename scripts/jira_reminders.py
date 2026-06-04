#!/usr/bin/env python3
"""
Fetch open Jira KB/Docs tasks and create macOS Reminders for each one.

Each reminder is placed in the "Jira Tasks" list with:
  - Due date pulled from the Jira duedate field (or omitted if unset)
  - Body note showing the ticket key, created date, due date, and URL
  - Repeating recurrence every 4 days (FREQ=DAILY;INTERVAL=4) so you
    get a nudge until the ticket is marked complete in Reminders

Usage:
    python3 scripts/jira_reminders.py

Edit the CONFIGURATION block below before first run.
"""

import json
import subprocess
import urllib.parse
import urllib.request
from datetime import datetime
from urllib.error import HTTPError, URLError

# --- CONFIGURATION ---
SERVER_URL = "https://Jira-url"   # Your on-prem Jira base URL (no trailing slash)
TOKEN      = "PAT"                 # Your Personal Access Token

# --- JIRA QUERY ---
JQL = (
    'assignee = currentUser() AND type = Task AND component = "KB/Docs" '
    'AND (status = Open OR status = "In Progress")'
)

LIST_NAME  = "Jira Tasks"
RECURRENCE = "FREQ=DAILY;INTERVAL=4"   # nudge every 4 days


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def jira_get(path: str) -> dict:
    url = f"{SERVER_URL}{path}"
    req = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"},
        method="GET",
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())


def parse_jira_date(date_str: str | None) -> datetime | None:
    """Accept 'YYYY-MM-DD' or 'YYYY-MM-DDTHH:MM:SS.mmm+ZZZZ'."""
    if not date_str:
        return None
    for fmt in ("%Y-%m-%dT%H:%M:%S.%f%z", "%Y-%m-%d"):
        try:
            return datetime.strptime(date_str[:len(fmt) + 5].strip(), fmt)
        except ValueError:
            continue
    return None


def fmt_display(dt: datetime | None) -> str:
    return dt.strftime("%Y-%m-%d") if dt else "not set"


def build_applescript(tickets: list[dict]) -> str:
    lines = [
        'tell application "Reminders"',
        f'  if not (exists list "{LIST_NAME}") then',
        f'    make new list with properties {{name:"{LIST_NAME}"}}',
        "  end if",
        f'  set jiraList to list "{LIST_NAME}"',
    ]

    for t in tickets:
        key         = t["key"]
        summary     = t["summary"].replace("\\", "\\\\").replace('"', '\\"')
        title       = f"[{key}] {summary}"
        url         = f"{SERVER_URL}/browse/{key}"
        body        = (
            f"Key: {key}\\n"
            f"Created: {t['created_display']}\\n"
            f"Due: {t['due_display']}\\n"
            f"URL: {url}"
        )

        lines += [
            f'  set t to "{title}"',
            "  set taskExists to false",
            "  repeat with r in (reminders of jiraList whose completed is false)",
            "    if name of r is t then set taskExists to true",
            "  end repeat",
            "  if not taskExists then",
        ]

        if t["due_dt"]:
            y  = t["due_dt"].year
            mo = t["due_dt"].month
            d  = t["due_dt"].day
            lines += [
                "    set dueDate to current date",
                f"    set year of dueDate to {y}",
                f"    set month of dueDate to {mo}",
                f"    set day of dueDate to {d}",
                "    set time of dueDate to 28800",   # 08:00
                f'    make new reminder in jiraList with properties {{name:t, body:"{body}", completed:false, due date:dueDate, recurrence:"{RECURRENCE}"}}',
            ]
        else:
            lines.append(
                f'    make new reminder in jiraList with properties {{name:t, body:"{body}", completed:false, recurrence:"{RECURRENCE}"}}'
            )

        lines.append("  end if")

    lines.append("end tell")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    encoded_jql = urllib.parse.quote(JQL)
    print("Fetching Jira tickets…")

    try:
        data = jira_get(f"/rest/api/2/search?jql={encoded_jql}&fields=summary,created,duedate")
    except HTTPError as e:
        print(f"HTTP {e.code}: {e.reason}\n{e.read().decode()}")
        return
    except URLError as e:
        print(f"Could not reach Jira — check SERVER_URL or VPN. Reason: {e.reason}")
        return

    issues = data.get("issues", [])
    if not issues:
        print("No matching tickets found.")
        return

    print(f"Found {len(issues)} ticket(s). Creating reminders…\n")

    tickets = []
    for issue in issues:
        fields   = issue.get("fields", {})
        key      = issue["key"]
        summary  = fields.get("summary", "(no summary)")
        created  = parse_jira_date(fields.get("created"))
        due      = parse_jira_date(fields.get("duedate"))
        status   = fields.get("status", {}).get("name", "Unknown")

        print(f"  [{key}] ({status}) {summary}")
        print(f"    Created: {fmt_display(created)}  |  Due: {fmt_display(due)}")

        tickets.append({
            "key":             key,
            "summary":         summary,
            "created_display": fmt_display(created),
            "due_display":     fmt_display(due),
            "due_dt":          due,
        })

    script = build_applescript(tickets)
    result = subprocess.run(["osascript"], input=script, text=True, capture_output=True)

    if result.returncode != 0:
        print(f"\nAppleScript error:\n{result.stderr}")
    else:
        print(f"\nDone — {len(tickets)} reminder(s) synced to \"{LIST_NAME}\".")
        print(f"Each reminder repeats every 4 days until marked complete.")


if __name__ == "__main__":
    main()
