#!/usr/bin/env python3
"""Regenerate dashboard tables from case/kb frontmatter."""

import re
import sys
from pathlib import Path
from datetime import datetime

import yaml

BASE = Path(__file__).parent.parent / "docs"

PRIORITY_RANK = {"P1": 0, "P2": 1, "P3": 2, "P4": 3}

CASE_HEADER = (
    "| Priority | Case # | Customer | Status | Note | Created |\n"
    "|----------|--------|----------|--------|------|---------|\n"
)

def parse_frontmatter(path):
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return {}
    fm = {}
    current_key = None
    current_list = None
    for line in match.group(1).splitlines():
        if line.startswith("  - ") and current_list is not None:
            current_list.append(line[4:].strip().strip('"').strip("'"))
        elif ": " in line and not line.startswith(" "):
            current_list = None
            key, _, val = line.partition(": ")
            fm[key.strip()] = val.strip().strip('"').strip("'")
            current_key = key.strip()
        elif line.rstrip().endswith(":") and not line.startswith(" "):
            current_key = line.strip().rstrip(":")
            current_list = []
            fm[current_key] = current_list
    # flatten lists to comma-separated strings for compatibility
    for k, v in fm.items():
        if isinstance(v, list):
            fm[k] = ", ".join(v)
    return fm


def priority_key(entry):
    return PRIORITY_RANK.get(entry.get("priority", ""), 9)


def format_created_date(created):
    if not created:
        return "—"
    date_part = created.split(" ")[0]
    try:
        return datetime.strptime(date_part, "%Y-%m-%d").strftime("%m-%d-%y")
    except ValueError:
        return created


def case_rows(section, link_prefix="../", sort="priority"):
    folder = BASE / section
    if not folder.exists():
        return []
    entries = []
    for f in sorted(folder.glob("*.md")):
        fm = parse_frontmatter(f)
        if fm.get("case_number"):
            fm["_file"] = f.name
            entries.append(fm)
    if sort == "newest":
        entries.sort(key=lambda e: e.get("created", ""), reverse=True)
    else:
        entries.sort(key=priority_key)
    rows = []
    for e in entries:
        num = e.get("case_number", "—")
        link = f"[{num}]({link_prefix}{section}/{e['_file']})"
        rows.append(
            f"| {e.get('priority','—')} | {link} | {e.get('customer','—')} "
            f"| {e.get('status','—')} | {e.get('note','—')} | {format_created_date(e.get('created'))} |"
        )
    return rows



def _tab_block(header, rows):
    if rows:
        lines = (header + "\n".join(rows)).splitlines()
    else:
        lines = ["*No entries.*"]
    return "\n".join("    " + line for line in lines)


def write_combined_dashboard(active, followup, archive):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    tabs = [
        (f"🟢 Active ({len(active)})", CASE_HEADER, active),
        (f"🔄 Follow-up ({len(followup)})", CASE_HEADER, followup),
        ("🗄️ Archive", CASE_HEADER, archive),
    ]
    parts = [f"# 📊 Case Dashboard\n\n*🕐 Updated: {timestamp}*\n"]
    for label, header, rows in tabs:
        parts.append(f'=== "{label}"\n\n{_tab_block(header, rows)}\n')
    (BASE / "dashboard.md").write_text("\n".join(parts), encoding="utf-8")
    total = len(active) + len(followup) + len(archive)
    print(f"  dashboard.md: {total} total entries")


def write_section_dashboard(filename, title, header, rows):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    body = "\n".join(rows) if rows else "*No entries.*"
    (BASE / "dashboards" / filename).write_text(
        f"# {title}\n\n*🕐 Updated: {timestamp}*\n\n{header}{body}\n",
        encoding="utf-8",
    )
    print(f"  {filename}: {len(rows)} entries")

PKB_CONFIG = BASE.parent / "pkb-categories.yaml"
PKB_TEMPLATES = [
    BASE.parent / ".foam" / "templates" / "pkb.md",
    BASE.parent / ".foam" / "templates" / "kb-article.md",
]
IMAGE_EXTS = (".svg", ".png", ".jpg", ".jpeg", ".gif", ".webp")


def load_pkb_config():
    """Read PKB tabs from pkb-categories.yaml. Returns (categories, labels)."""
    if not PKB_CONFIG.exists():
        print(f"  {PKB_CONFIG.name} not found, using a single 'Other' tab")
        return ["Other"], {}
    data = yaml.safe_load(PKB_CONFIG.read_text(encoding="utf-8")) or {}
    other = str(data.get("other_tab") or "Other").strip()
    categories, labels = [], {}
    for item in data.get("categories") or []:
        if isinstance(item, str):
            item = {"name": item}
        name = str(item.get("name", "")).strip()
        if not name:
            continue
        if "," in name or "|" in name:
            sys.exit(f"{PKB_CONFIG.name}: category '{name}' can't contain ',' or '|'")
        categories.append(name)
        icon = str(item.get("icon") or "").strip()
        if icon.lower().endswith(IMAGE_EXTS):
            labels[name] = (
                f'<img src="{icon}" style="height:1em;vertical-align:middle;'
                f'margin-right:4px;"> {name}'
            )
        elif icon:
            labels[name] = f"{icon} {name}"
    categories.append(other)
    return categories, labels


def sync_template_categories():
    """Make the `category` dropdown in the PKB templates match the config."""
    choices = ",".join(PKB_CATEGORIES)
    pattern = re.compile(r"^(category: \$\{\d+\|)[^|}]*(\|\})", re.MULTILINE)
    for path in PKB_TEMPLATES:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        new = pattern.sub(lambda m: f"{m.group(1)}{choices}{m.group(2)}", text)
        if new != text:
            path.write_text(new, encoding="utf-8")
            print(f"  {path.name}: category dropdown updated")


PKB_CATEGORIES, PKB_TAB_LABELS = load_pkb_config()

PKB_HEADER = (
    "| Title | Tags | Created |\n"
    "| ----- | ---- | ------- |\n"
)


def pkb_rows(category):
    folder = BASE / "pkb"
    if not folder.exists():
        return []
    other = PKB_CATEGORIES[-1]
    known = {c.lower() for c in PKB_CATEGORIES[:-1]}
    entries = []
    for f in sorted(folder.glob("*.md")):
        fm = parse_frontmatter(f)
        file_cat = fm.get("category", "").lower()
        if category == other:
            if file_cat not in known:
                fm["_file"] = f.name
                entries.append(fm)
        elif file_cat == category.lower():
            fm["_file"] = f.name
            entries.append(fm)
    entries.sort(key=lambda e: e.get("created", ""), reverse=True)
    rows = []
    for e in entries:
        title = e.get("title", e["_file"].replace(".md", ""))
        link = f"[{title}](pkb/{e['_file']})"
        tags = e.get("tags", "").strip("[]").replace(",", " ·")
        created = e.get("created", "—")
        rows.append(f"| {link} | {tags} | {created} |")
    return rows


def write_pkb_dashboard():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    parts = [f"# 📓 Knowledge Base\n\n*🕐 Updated: {timestamp}*\n"]
    total = 0
    for category in PKB_CATEGORIES:
        rows = pkb_rows(category)
        total += len(rows)
        block = _tab_block(PKB_HEADER, rows)
        label = PKB_TAB_LABELS.get(category, category)
        parts.append(f'=== "{label} ({len(rows)})"\n\n{block}\n')
    (BASE / "pkb.md").write_text("\n".join(parts), encoding="utf-8")
    print(f"  pkb.md: {total} total entries")


TAG_SCAN_DIRS = [
    ("cases/active",   "cases/active"),
    ("cases/followup", "cases/followup"),
    ("cases/archive",  "cases/archive"),
    ("pkb",            "pkb"),
    ("meetings/1on1",    "meetings/1on1"),
    ("meetings/team",    "meetings/team"),
    ("meetings/general", "meetings/general"),
]


def write_tags_page():
    tag_map = {}
    for rel_dir, link_prefix in TAG_SCAN_DIRS:
        folder = BASE / rel_dir
        if not folder.exists():
            continue
        for f in sorted(folder.glob("*.md")):
            if f.name == "index.md":
                continue
            fm = parse_frontmatter(f)
            raw = fm.get("tags", "").strip("[]")
            if not raw:
                continue
            title = fm.get("title") or fm.get("case_number") or fm.get("kb_number") or f.stem
            for tag in raw.split(","):
                tag = tag.strip().strip('"').strip("'")
                if tag:
                    tag_map.setdefault(tag, []).append((title, f"{link_prefix}/{f.name}"))

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [f"# 🏷️ Tags\n\n*🕐 Updated: {timestamp}*\n"]
    for tag in sorted(tag_map):
        lines.append(f"## `{tag}`\n")
        for title, path in sorted(tag_map[tag]):
            lines.append(f"- [{title}]({path})")
        lines.append("")
    (BASE / "tags.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    total = sum(len(v) for v in tag_map.values())
    print(f"  tags.md: {len(tag_map)} tag(s), {total} reference(s)")


MEETING_SECTIONS = [
    ("1on1",    "🤝 1-on-1s"),
    ("team",    "👥 Team"),
    ("general", "📋 General"),
]


def _meeting_tab_block(subdir):
    folder = BASE / "meetings" / subdir
    notes = sorted(folder.glob("*.md"), reverse=True)
    notes = [n for n in notes if n.name != "index.md"]
    if not notes:
        return "    *No notes yet.*"
    lines = [f"    - [{n.stem}](meetings/{subdir}/{n.name})" for n in notes]
    return "\n".join(lines)


def write_meetings_page():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    parts = [f"# 📅 Meetings\n\n*🕐 Updated: {timestamp}*\n"]
    total = 0
    for subdir, label in MEETING_SECTIONS:
        block = _meeting_tab_block(subdir)
        count = len([
            n for n in (BASE / "meetings" / subdir).glob("*.md")
            if n.name != "index.md"
        ])
        total += count
        parts.append(f'=== "{label} ({count})"\n\n{block}\n')
    (BASE / "meetings.md").write_text("\n".join(parts), encoding="utf-8")
    print(f"  meetings.md: {total} total note(s)")


if __name__ == "__main__":
    print("Rebuilding dashboards...")

    # Combined tabbed dashboard — links relative to docs/
    write_combined_dashboard(
        active=case_rows("cases/active", link_prefix=""),
        followup=case_rows("cases/followup", link_prefix="", sort="newest"),
        archive=case_rows("cases/archive", link_prefix="", sort="newest"),
    )

    # Individual section pages — links relative to docs/dashboards/
    write_section_dashboard("active.md", "🟢 Active Cases", CASE_HEADER, case_rows("cases/active"))
    write_section_dashboard("followup.md", "🔄 Follow-up Cases", CASE_HEADER, case_rows("cases/followup", sort="newest"))
    write_section_dashboard("archive.md", "🗄️ Archived Cases", CASE_HEADER, case_rows("cases/archive", sort="newest"))

    print("Rebuilding meetings page...")
    write_meetings_page()

    print("Rebuilding PKB dashboard...")
    sync_template_categories()
    write_pkb_dashboard()

    print("Rebuilding tags page...")
    write_tags_page()

    print("Done.")
