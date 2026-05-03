#!/usr/bin/env python3
"""Read clipboard and append a fenced code block to the Steps Taken section of the active case note."""

import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

SECTION = "## 🛠️ Steps Taken"
END_PAT = re.compile(r'\n=== "|\n    ## ')


def get_clipboard():
    return subprocess.run(["pbpaste"], capture_output=True, text=True).stdout.strip()


def update_note(note_path, content):
    text = note_path.read_text(encoding="utf-8")

    if SECTION not in text:
        print(f"❌  '{SECTION}' not found in note.")
        sys.exit(1)

    idx = text.index(SECTION)
    after = text[idx + len(SECTION):]
    m = END_PAT.search(after)

    timestamp = datetime.now().strftime("%H:%M")
    lines = [f"    {line}" for line in content.splitlines()]
    block = f'\n\n    ``` title="{timestamp}"\n' + "\n".join(lines) + "\n    ```"

    if m:
        insert_pos = idx + len(SECTION) + m.start()
        text = text[:insert_pos] + block + text[insert_pos:]
    else:
        text = text.rstrip() + block + "\n"

    note_path.write_text(text, encoding="utf-8")
    print(f"✅  Appended terminal block ({len(content.splitlines())} lines) to Steps Taken.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: append_terminal_block.py <path-to-note.md>")
        sys.exit(1)

    note_path = Path(sys.argv[1])
    if not note_path.exists():
        print(f"❌  File not found: {note_path}")
        sys.exit(1)

    content = get_clipboard()
    if not content:
        print("❌  Clipboard is empty.")
        sys.exit(1)

    update_note(note_path, content)
