#!/usr/bin/env python3
"""Convert the Remote Support Note at the cursor to Salesforce plain text and copy to clipboard."""

import re
import subprocess
import sys
from pathlib import Path

HEADING_PAT = re.compile(r"^\s*### 📓 Remote Support \d{1,2}/\d{1,2}")


def find_section(lines, cursor_line):
    """Return (start, end) indices of the remote support section containing cursor_line (1-based)."""
    cursor_idx = cursor_line - 1
    starts = [i for i, l in enumerate(lines) if HEADING_PAT.match(l)]
    if not starts:
        return None, None

    section_start = None
    for s in reversed(starts):
        if s <= cursor_idx:
            section_start = s
            break
    if section_start is None:
        section_start = starts[0]

    section_end = len(lines)
    for i in range(section_start + 1, len(lines)):
        if re.match(r"^\s*#{1,3} ", lines[i]):
            section_end = i
            break

    return section_start, section_end


def parse_admonition(lines):
    """Extract via, attendees, details, and actions from admonition content lines."""
    via = ""
    attendees = ""
    details = []
    actions = []
    mode = None

    for line in lines:
        stripped = line.strip()

        m = re.match(r"\*\*Remote support via\*\*\s+(.+?)(?:<br>)?$", stripped)
        if m:
            via = m.group(1).strip()
            continue

        m = re.match(r"\*\*Attendees:\*\*\s*(.*?)(?:<br>)?$", stripped)
        if m:
            attendees = m.group(1).strip()
            continue

        if re.match(r"\*\*Details\*\*", stripped):
            mode = "details"
            continue

        if re.match(r"\*\*Action Plan\*\*", stripped):
            mode = "actions"
            continue

        m = re.match(r"\s*[-*]\s+(.+)", line)
        if m and mode:
            item = m.group(1).strip()
            if item:
                (details if mode == "details" else actions).append(item)

    return via, attendees, details, actions


def build_salesforce(via, attendees, details, actions):
    sep = "------------------------------------"
    out = [
        "REMOTE SUPPORT NOTES",
        "",
        sep,
        "",
        f"Remote support via {via}",
        f"Attendees: {attendees}",
        "",
        "",
        "DETAILS",
        sep,
    ]
    for d in details:
        out.append(f"+ {d}")
    out += ["", "ACTION PLAN", sep]
    for a in actions:
        out.append(f"+ {a}")
    out.append("")
    return "\n".join(out)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: copy_salesforce_notes.py <path-to-note.md> <cursor-line>")
        sys.exit(1)

    note_path = Path(sys.argv[1])
    cursor_line = int(sys.argv[2])

    if not note_path.exists():
        print(f"❌  File not found: {note_path}")
        sys.exit(1)

    lines = note_path.read_text(encoding="utf-8").splitlines()
    start, end = find_section(lines, cursor_line)

    if start is None:
        print("❌  No Remote Support Note section found near cursor.")
        sys.exit(1)

    section = lines[start:end]

    admon_start = next(
        (i + 1 for i, l in enumerate(section) if l.strip().startswith("!!! abstract")),
        None,
    )
    if admon_start is None:
        print("❌  Could not find admonition block in section.")
        sys.exit(1)

    via, attendees, details, actions = parse_admonition(section[admon_start:])
    output = build_salesforce(via, attendees, details, actions)

    subprocess.run(["pbcopy"], input=output.encode(), check=True)

    print("✅  Copied to clipboard:")
    print()
    print(output)
