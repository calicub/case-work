#!/usr/bin/env python3
"""Copy the Details (steps performed) from the Remote Support Note at the cursor to the clipboard."""

import re
import subprocess
import sys
from pathlib import Path

HEADING_PAT = re.compile(r"^\s*### 📓 Remote Support (\d{1,2})/(\d{1,2})")

ORDINAL = {
    1: "1st", 2: "2nd", 3: "3rd", 4: "4th", 5: "5th", 6: "6th", 7: "7th",
    8: "8th", 9: "9th", 10: "10th", 11: "11th", 12: "12th", 13: "13th",
    14: "14th", 15: "15th", 16: "16th", 17: "17th", 18: "18th", 19: "19th",
    20: "20th", 21: "21st", 22: "22nd", 23: "23rd", 24: "24th", 25: "25th",
    26: "26th", 27: "27th", 28: "28th", 29: "29th", 30: "30th", 31: "31st",
}

MONTHS = [
    "", "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]


def format_date(month: int, day: int) -> str:
    return f"{MONTHS[month]} {ORDINAL[day]}"


def find_section(lines, cursor_line):
    cursor_idx = cursor_line - 1
    starts = [(i, l) for i, l in enumerate(lines) if HEADING_PAT.match(l)]
    if not starts:
        return None, None, None

    section_start, heading_line = None, None
    for i, l in reversed(starts):
        if i <= cursor_idx:
            section_start, heading_line = i, l
            break
    if section_start is None:
        section_start, heading_line = starts[0]

    section_end = len(lines)
    for i in range(section_start + 1, len(lines)):
        if re.match(r"^\s*#{1,3} ", lines[i]):
            section_end = i
            break

    return section_start, section_end, heading_line


def parse_details(section_lines):
    details = []
    in_details = False
    for line in section_lines:
        stripped = line.strip()
        if re.match(r"\*\*Details\*\*", stripped):
            in_details = True
            continue
        if in_details:
            if re.match(r"\*\*Action Plan\*\*", stripped):
                break
            m = re.match(r"\s*[-*]\s+(.+)", line)
            if m:
                item = m.group(1).strip()
                if item:
                    details.append(item)
    return details


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: copy_remote_steps.py <path-to-note.md> <cursor-line>")
        sys.exit(1)

    note_path = Path(sys.argv[1])
    cursor_line = int(sys.argv[2])

    if not note_path.exists():
        print(f"❌  File not found: {note_path}")
        sys.exit(1)

    lines = note_path.read_text(encoding="utf-8").splitlines()
    start, end, heading = find_section(lines, cursor_line)

    if start is None:
        print("❌  No Remote Support Note section found near cursor.")
        sys.exit(1)

    m = HEADING_PAT.match(heading)
    month, day = int(m.group(1)), int(m.group(2))
    date_label = format_date(month, day)

    section = lines[start:end]
    admon_start = next(
        (i + 1 for i, l in enumerate(section) if l.strip().startswith("!!! abstract")),
        0,
    )
    details = parse_details(section[admon_start:])

    if not details:
        print("❌  No Details items found in section.")
        sys.exit(1)

    lines_out = [f"--- {date_label} ---"] + [f"+ {d}" for d in details]
    output = "\n".join(lines_out)

    subprocess.run(["pbcopy"], input=output.encode(), check=True)

    print("✅  Copied to clipboard:")
    print()
    print(output)
