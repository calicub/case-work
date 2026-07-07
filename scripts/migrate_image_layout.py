#!/usr/bin/env python3
"""Migrate case notes from the old grid image layout to the glightbox layout.

The old build_image_block() wrapped each <img> in a
`<a href="..." target="_blank">...</a>` anchor so clicking opened the
full-size image in a new tab. The glightbox plugin (zensical.toml) now
auto-wraps every <img> in a `.glightbox` anchor at build time, so the old
manual anchor is redundant and produces nested <a> tags. This script strips
that wrapper, leaving the bare <img> tag insert_assets.py now generates.

Usage:
    scripts/migrate_image_layout.py            # scan docs/, apply changes
    scripts/migrate_image_layout.py --dry-run  # preview without writing
"""

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS_DIR = ROOT / "docs"

# Matches: <a href="X" target="_blank"><img ... src="X" ...></a>
# Captures the href/src (group 1, must match) and the inner <img> tag (group 2).
OLD_WRAPPER = re.compile(
    r'<a href="([^"]+)" target="_blank">(<img [^>]*src="\1"[^>]*>)</a>'
)


def migrate_text(text):
    return OLD_WRAPPER.subn(r"\2", text)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "path", nargs="?", default=str(DOCS_DIR),
        help="File or directory to migrate (default: docs/)",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Show what would change without writing files",
    )
    args = parser.parse_args()

    target = Path(args.path)
    if not target.exists():
        print(f"❌  Path not found: {target}")
        sys.exit(1)

    md_files = [target] if target.is_file() else sorted(target.rglob("*.md"))

    changed_files = 0
    total_images = 0

    for md in md_files:
        text = md.read_text(encoding="utf-8")
        new_text, count = migrate_text(text)
        if count == 0:
            continue

        changed_files += 1
        total_images += count
        try:
            rel = md.relative_to(ROOT)
        except ValueError:
            rel = md
        print(f"📸  {rel}: {count} image(s){' (dry-run)' if args.dry_run else ''}")

        if not args.dry_run:
            md.write_text(new_text, encoding="utf-8")

    if changed_files == 0:
        print("✅  Nothing to migrate — no old-style image wrappers found.")
    else:
        verb = "Would update" if args.dry_run else "Updated"
        print(f"✅  {verb} {total_images} image(s) across {changed_files} file(s).")


if __name__ == "__main__":
    main()
