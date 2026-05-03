#!/usr/bin/env python3
"""Find customer files for the active case note and insert links into the Customer Files section."""

import re
import sys
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).parent.parent
FILES_DIR = ROOT / "docs" / "files"
SECTION = '=== "📎 Customer Files"'


def get_case_number(note_path):
    text = note_path.read_text(encoding="utf-8")
    m = re.search(r"^case_number:\s*(.+)$", text, re.MULTILINE)
    return m.group(1).strip() if m else None


def find_files(case_number):
    pat = re.compile(rf"^{re.escape(str(case_number))}[\s\-_]")

    at_root = sorted(
        f for f in ROOT.iterdir()
        if f.is_file() and not f.name.startswith(".") and pat.match(f.name)
    )
    in_dir = sorted(
        f for f in FILES_DIR.iterdir()
        if f.is_file() and pat.match(f.name)
    ) if FILES_DIR.exists() else []

    return at_root, in_dir


def move_files(files):
    FILES_DIR.mkdir(exist_ok=True)
    moved = []
    for src in files:
        dest = FILES_DIR / src.name.replace(" ", "-")
        src.rename(dest)
        moved.append(dest)
        print(f"  Moved: {src.name}  →  files/{dest.name}")
    return moved


def already_referenced(note_path):
    text = note_path.read_text(encoding="utf-8")
    if SECTION not in text:
        return set()
    idx = text.index(SECTION)
    section_text = text[idx:]
    next_h = re.search(r'\n=== "', section_text[len(SECTION):])
    if next_h:
        section_text = section_text[:next_h.start() + len(SECTION)]
    return set(re.findall(r"files/([^)\s]+)", section_text))


def build_file_block(files):
    lines = []
    for f in files:
        encoded = quote(f.name)
        lines.append(f"    [{f.name}](../files/{encoded}){{target=_blank}}")
    lines.append("")
    return lines


def update_note(note_path, file_lines):
    text = note_path.read_text(encoding="utf-8")
    block = "\n".join(file_lines)

    if SECTION not in text:
        text = text.rstrip() + f"\n\n{SECTION}\n\n{block}\n"
        note_path.write_text(text, encoding="utf-8")
        print(f"  Appended new '{SECTION}' section.")
        return

    idx = text.index(SECTION)
    after = text[idx + len(SECTION):]
    next_h = re.search(r'\n=== "', after)
    tail = after[next_h.start():] if next_h else ""
    note_path.write_text(
        text[:idx] + SECTION + "\n\n" + block + "\n" + tail,
        encoding="utf-8",
    )
    print(f"  Updated '{SECTION}'.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: insert_files.py <path-to-note.md>")
        sys.exit(1)

    note_path = Path(sys.argv[1])
    if not note_path.exists():
        print(f"❌  File not found: {note_path}")
        sys.exit(1)

    case_number = get_case_number(note_path)
    if not case_number:
        print("❌  Could not read case_number from note frontmatter.")
        sys.exit(1)

    print(f"🔍  Searching for files matching '{case_number}'...")
    at_root, in_dir = find_files(case_number)

    if not at_root and not in_dir:
        print(f"   No files found in {ROOT} or {FILES_DIR}")
        sys.exit(0)

    moved = move_files(at_root)
    all_files = moved + in_dir

    referenced = already_referenced(note_path)
    new_files = [
        f for f in all_files
        if quote(f.name) not in referenced and f.name not in referenced
    ]

    if not new_files:
        print("   All files are already referenced in the note.")
        sys.exit(0)

    print(f"📎  Inserting {len(new_files)} file(s):")
    for f in new_files:
        print(f"  {f.name}")
    update_note(note_path, build_file_block(new_files))
    print("✅  Done.")
