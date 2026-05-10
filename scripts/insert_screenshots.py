#!/usr/bin/env python3
"""Find screenshots for the active case note and insert them into the Screenshots section."""

import re
import sys
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).parent.parent
SCREENSHOTS_DIR = ROOT / "docs" / "assets" / "screenshots"
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".webp"}
SECTION = '=== "📸 Screenshots"'


def get_case_number(note_path):
    text = note_path.read_text(encoding="utf-8")
    m = re.search(r"^case_number:\s*(.+)$", text, re.MULTILINE)
    return m.group(1).strip() if m else None


def find_screenshots(case_number):
    """Find matching images at workspace root and already in docs/screenshots/."""
    pat = re.compile(rf"^{re.escape(str(case_number))}[\s\-_]")

    at_root = sorted(
        f for f in ROOT.iterdir()
        if f.is_file() and f.suffix.lower() in IMAGE_EXTS and pat.match(f.name)
    )
    in_dir = sorted(
        f for f in SCREENSHOTS_DIR.iterdir()
        if f.is_file() and f.suffix.lower() in IMAGE_EXTS and pat.match(f.name)
    ) if SCREENSHOTS_DIR.exists() else []

    return at_root, in_dir


def move_screenshots(screenshots):
    """Move images from workspace root to docs/screenshots/, replacing spaces with hyphens."""
    SCREENSHOTS_DIR.mkdir(exist_ok=True)
    moved = []
    for src in screenshots:
        dest = SCREENSHOTS_DIR / src.name.replace(" ", "-")
        src.rename(dest)
        moved.append(dest)
        print(f"  Moved: {src.name}  →  screenshots/{dest.name}")
    return moved


def already_referenced(note_path):
    """Return set of encoded filenames already linked in the Screenshots section."""
    text = note_path.read_text(encoding="utf-8")
    if SECTION not in text:
        return set()
    idx = text.index(SECTION)
    section_text = text[idx:]
    next_h = re.search(r'\n=== "|\n#', section_text[len(SECTION):])
    if next_h:
        section_text = section_text[:next_h.start() + len(SECTION)]
    return set(re.findall(r"screenshots/([^)\s]+)", section_text))


IMG_STYLE = "width:100%;height:180px;object-fit:cover;border-radius:4px;display:block;"
CAP_STYLE = "text-align:center;font-size:0.75rem;opacity:0.6;margin-top:4px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;"
GRID_STYLE = "display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:8px;"


def build_image_block(images):
    lines = [f'    <div style="{GRID_STYLE}">']
    for img in images:
        encoded = quote(img.name)
        lines.append(
            f'    <figure style="margin:0">'
            f'<a href="../../assets/screenshots/{encoded}" target="_blank">'
            f'<img src="../../assets/screenshots/{encoded}" loading="lazy" alt="{img.stem}" style="{IMG_STYLE}"></a>'
            f'<figcaption style="{CAP_STYLE}">{img.stem}</figcaption></figure>'
        )
    lines += ["    </div>", ""]
    return lines


def update_note(note_path, image_lines):
    text = note_path.read_text(encoding="utf-8")
    block = "\n".join(image_lines)

    if SECTION not in text:
        text = text.rstrip() + f"\n\n{SECTION}\n\n{block}\n"
        note_path.write_text(text, encoding="utf-8")
        print(f"  Appended new '{SECTION}' section.")
        return

    idx = text.index(SECTION)
    after = text[idx + len(SECTION):]
    next_h = re.search(r'\n=== "|\n#', after)
    tail = after[next_h.start():] if next_h else ""
    note_path.write_text(
        text[:idx] + SECTION + "\n\n" + block + "\n" + tail,
        encoding="utf-8",
    )
    print(f"  Updated '{SECTION}'.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: insert_screenshots.py <path-to-note.md>")
        sys.exit(1)

    note_path = Path(sys.argv[1])
    if not note_path.exists():
        print(f"❌  File not found: {note_path}")
        sys.exit(1)

    case_number = get_case_number(note_path)
    if not case_number:
        print("❌  Could not read case_number from note frontmatter.")
        sys.exit(1)

    print(f"🔍  Searching for screenshots matching '{case_number}'...")
    at_root, in_dir = find_screenshots(case_number)

    if not at_root and not in_dir:
        print(f"   No screenshots found in {ROOT} or {SCREENSHOTS_DIR}")
        sys.exit(0)

    moved = move_screenshots(at_root)
    all_images = moved + in_dir

    referenced = already_referenced(note_path)
    new_images = [
        img for img in all_images
        if quote(img.name) not in referenced and img.name not in referenced
    ]

    if not new_images:
        print("   All screenshots are already referenced in the note.")
        sys.exit(0)

    print(f"📸  Inserting {len(new_images)} screenshot(s):")
    for img in new_images:
        print(f"  {img.name}")
    update_note(note_path, build_image_block(new_images))
    print("✅  Done.")
