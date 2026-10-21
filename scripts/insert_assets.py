#!/usr/bin/env python3
"""Insert customer files and/or screenshots into a case note."""

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).parent.parent
FILES_DIR = ROOT / "docs" / "assets" / "files"
SCREENSHOTS_DIR = ROOT / "docs" / "assets" / "screenshots"
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".webp"}

FILES_SECTION = '=== "📎 Customer Files"'
SCREENSHOTS_SECTION = '=== "📸 Screenshots"'

IMG_STYLE = "width:100%;height:180px;object-fit:cover;border-radius:4px;display:block;"
CAP_STYLE = "text-align:center;font-size:0.75rem;opacity:0.6;margin-top:4px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;"
GRID_STYLE = "display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:8px;"

ICONS = {
    ".pdf":  ":fontawesome-regular-file-pdf:",
    ".doc":  ":fontawesome-regular-file-word:",  ".docx": ":fontawesome-regular-file-word:",
    ".xls":  ":fontawesome-regular-file-excel:", ".xlsx": ":fontawesome-regular-file-excel:", ".csv": ":fontawesome-regular-file-excel:",
    ".png":  ":fontawesome-regular-file-image:", ".jpg":  ":fontawesome-regular-file-image:",
    ".jpeg": ":fontawesome-regular-file-image:", ".gif":  ":fontawesome-regular-file-image:", ".webp": ":fontawesome-regular-file-image:",
    ".zip":  ":fontawesome-solid-file-zipper:",  ".tar":  ":fontawesome-solid-file-zipper:",
    ".gz":   ":fontawesome-solid-file-zipper:",  ".7z":   ":fontawesome-solid-file-zipper:",
    ".txt":  ":fontawesome-regular-file-lines:", ".log":  ":fontawesome-regular-file-lines:",
    ".json": ":fontawesome-regular-file-code:",  ".yaml": ":fontawesome-regular-file-code:",
    ".yml":  ":fontawesome-regular-file-code:",  ".py":   ":fontawesome-regular-file-code:",
    ".sh":   ":fontawesome-regular-file-code:",
}


def get_case_number(note_path):
    text = note_path.read_text(encoding="utf-8")
    m = re.search(r"^case_number:\s*(.+)$", text, re.MULTILINE)
    return m.group(1).strip() if m else None


def already_referenced(note_path, pattern):
    text = note_path.read_text(encoding="utf-8")
    return set(re.findall(pattern, text))


def update_note(note_path, section, block_lines):
    text = note_path.read_text(encoding="utf-8")
    block = "\n".join(block_lines)

    if section not in text:
        text = text.rstrip() + f"\n\n{section}\n\n{block}\n"
        note_path.write_text(text, encoding="utf-8")
        print(f"  Appended new '{section}' section.")
        return

    idx = text.index(section)
    after = text[idx + len(section):]
    next_h = re.search(r'\n=== "|\n#', after)
    tail = after[next_h.start():] if next_h else ""
    note_path.write_text(
        text[:idx] + section + "\n\n" + block + "\n" + tail,
        encoding="utf-8",
    )
    print(f"  Updated '{section}'.")


def clean_name(name):
    """'123456 - Screenshot 12.27.00\u202fPM.png' -> '123456-Screenshot-12.27.00-PM.png'."""
    name = re.sub(r"\s+", "-", name)        # any whitespace, incl. macOS's narrow no-break space
    return re.sub(r"-{2,}", "-", name)       # ' - ' would otherwise become '---'


# --- Files ---

def find_files(case_number):
    pat = re.compile(rf"^{re.escape(str(case_number))}[\s\-_]")
    at_root = sorted(
        f for f in ROOT.iterdir()
        if f.is_file() and not f.name.startswith(".")
        and f.suffix.lower() not in IMAGE_EXTS
        and pat.match(f.name)
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
        dest = FILES_DIR / clean_name(src.name)
        src.rename(dest)
        moved.append(dest)
        print(f"  Moved: {src.name}  →  files/{dest.name}")
    return moved


def build_file_block(files):
    lines = []
    for f in files:
        icon = ICONS.get(f.suffix.lower(), ":fontawesome-regular-file:")
        encoded = quote(f.name)
        lines.append(f"    - {icon} [{f.name}](../../assets/files/{encoded}){{target=_blank}}")
    return lines


def run_files(note_path, case_number):
    print(f"🔍  Searching for files matching '{case_number}'...")
    at_root, in_dir = find_files(case_number)

    if not at_root and not in_dir:
        print(f"   No files found in {ROOT} or {FILES_DIR}")
        return

    moved = move_files(at_root)
    all_files = moved + in_dir

    referenced = already_referenced(note_path, r"files/([^)\s]+)")
    new_files = [
        f for f in all_files
        if quote(f.name) not in referenced and f.name not in referenced
    ]

    if not new_files:
        print("   All files are already referenced in the note.")
        return

    print(f"📎  Inserting {len(new_files)} file(s):")
    for f in new_files:
        print(f"  {f.name}")
    update_note(note_path, FILES_SECTION, build_file_block(new_files))


# --- Screenshots ---

def find_screenshots(case_number):
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
    SCREENSHOTS_DIR.mkdir(exist_ok=True)
    moved = []
    for src in screenshots:
        dest = SCREENSHOTS_DIR / clean_name(src.name)
        src.rename(dest)
        moved.append(dest)
        print(f"  Moved: {src.name}  →  screenshots/{dest.name}")
    return moved


def build_image_block(images):
    # No wrapping anchor on the <img> — the glightbox plugin (zensical.toml)
    # auto-wraps every image in a `.glightbox` anchor at build time.
    lines = [f'    <div style="{GRID_STYLE}">']
    for img in images:
        encoded = quote(img.name)
        lines.append(
            f'    <figure style="margin:0">'
            f'<img src="../../assets/screenshots/{encoded}" loading="lazy" alt="{img.stem}" style="{IMG_STYLE}">'
            f'<figcaption style="{CAP_STYLE}">{img.stem}</figcaption></figure>'
        )
    lines.append("    </div>")
    return lines


def run_screenshots(note_path, case_number):
    print(f"🔍  Searching for screenshots matching '{case_number}'...")
    at_root, in_dir = find_screenshots(case_number)

    if not at_root and not in_dir:
        print(f"   No screenshots found in {ROOT} or {SCREENSHOTS_DIR}")
        return

    moved = move_screenshots(at_root)
    all_images = moved + in_dir

    referenced = already_referenced(note_path, r"screenshots/([^)\s]+)")
    new_images = [
        img for img in all_images
        if quote(img.name) not in referenced and img.name not in referenced
    ]

    if not new_images:
        print("   All screenshots are already referenced in the note.")
        return

    print(f"📸  Inserting {len(new_images)} screenshot(s):")
    for img in new_images:
        print(f"  {img.name}")
    update_note(note_path, SCREENSHOTS_SECTION, build_image_block(new_images))


# --- Entry point ---

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Insert files and/or screenshots into a case note.")
    parser.add_argument("note", help="Path to the case note .md file")
    parser.add_argument("--files", action="store_true", help="Insert customer files only")
    parser.add_argument("--screenshots", action="store_true", help="Insert screenshots only")
    args = parser.parse_args()

    note_path = Path(args.note)
    if not note_path.exists():
        print(f"❌  File not found: {note_path}")
        sys.exit(1)

    case_number = get_case_number(note_path)
    if not case_number:
        print("❌  Could not read case_number from note frontmatter.")
        sys.exit(1)

    # Default: run both if no flags specified
    run_both = not args.files and not args.screenshots

    if args.files or run_both:
        run_files(note_path, case_number)

    if args.screenshots or run_both:
        run_screenshots(note_path, case_number)

    print("✅  Done.")
