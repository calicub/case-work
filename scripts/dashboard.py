#!/usr/bin/env python3
"""Regenerate dashboard tables from case/kb frontmatter."""

import re
from pathlib import Path
from datetime import datetime

BASE = Path(__file__).parent.parent / "docs"

PRIORITY_RANK = {"P1": 0, "P2": 1, "P3": 2, "P4": 3}

CASE_HEADER = (
    "| Priority | Case # | Customer | Status | Note |\n"
    "|----------|--------|----------|--------|------|\n"
)
KB_HEADER = (
    "| Status | KB # | Title | Category | Note |\n"
    "|--------|------|-------|----------|------|\n"
)


def parse_frontmatter(path):
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return {}
    fm = {}
    for line in match.group(1).splitlines():
        if ": " in line and not line.startswith(" "):
            key, _, val = line.partition(": ")
            fm[key.strip()] = val.strip().strip('"').strip("'")
    return fm


def priority_key(entry):
    return PRIORITY_RANK.get(entry.get("priority", ""), 9)


def case_rows(section, link_prefix="../"):
    folder = BASE / section
    if not folder.exists():
        return []
    entries = []
    for f in sorted(folder.glob("*.md")):
        fm = parse_frontmatter(f)
        if fm.get("case_number"):
            fm["_file"] = f.name
            entries.append(fm)
    entries.sort(key=priority_key)
    rows = []
    for e in entries:
        num = e.get("case_number", "—")
        link = f"[{num}]({link_prefix}{section}/{e['_file']})"
        rows.append(
            f"| {e.get('priority','—')} | {link} | {e.get('customer','—')} "
            f"| {e.get('status','—')} | {e.get('note','—')} |"
        )
    return rows


def kb_rows(link_prefix="../"):
    folder = BASE / "kb-updates"
    if not folder.exists():
        return []
    entries = []
    for f in sorted(folder.glob("*.md")):
        fm = parse_frontmatter(f)
        if fm.get("kb_number"):
            fm["_file"] = f.name
            entries.append(fm)
    rows = []
    for e in entries:
        num = e.get("kb_number", "—")
        link = f"[{num}]({link_prefix}kb-updates/{e['_file']})"
        rows.append(
            f"| {e.get('status','—')} | {link} | {e.get('title','—')} "
            f"| {e.get('category','—')} | {e.get('note','—')} |"
        )
    return rows


def _tab_block(header, rows):
    if rows:
        lines = (header + "\n".join(rows)).splitlines()
    else:
        lines = ["*No entries.*"]
    return "\n".join("    " + line for line in lines)


def write_combined_dashboard(active, followup, kb, archive):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    tabs = [
        (f"🟢 Active ({len(active)})", CASE_HEADER, active),
        (f"🔄 Follow-up ({len(followup)})", CASE_HEADER, followup),
        (f"📚 KB Updates ({len(kb)})", KB_HEADER, kb),
        ("🗄️ Archive", CASE_HEADER, archive),
    ]
    parts = [f"# 📊 Case Dashboard\n\n*🕐 Updated: {timestamp}*\n"]
    for label, header, rows in tabs:
        parts.append(f'=== "{label}"\n\n{_tab_block(header, rows)}\n')
    (BASE / "dashboard.md").write_text("\n".join(parts), encoding="utf-8")
    total = len(active) + len(followup) + len(kb) + len(archive)
    print(f"  dashboard.md: {total} total entries")


def write_section_dashboard(filename, title, header, rows):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    body = "\n".join(rows) if rows else "*No entries.*"
    (BASE / "dashboards" / filename).write_text(
        f"# {title}\n\n*🕐 Updated: {timestamp}*\n\n{header}{body}\n",
        encoding="utf-8",
    )
    print(f"  {filename}: {len(rows)} entries")


PKB_CATEGORIES = ["Tools", "Troubleshooting"]

PKB_HEADER = (
    "| Title | Tags | Created |\n"
    "| ----- | ---- | ------- |\n"
)


def pkb_rows(category):
    folder = BASE / "pkb"
    if not folder.exists():
        return []
    entries = []
    for f in sorted(folder.glob("*.md")):
        fm = parse_frontmatter(f)
        if fm.get("category", "").lower() == category.lower():
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
        parts.append(f'=== "{category} ({len(rows)})"\n\n{block}\n')
    (BASE / "pkb.md").write_text("\n".join(parts), encoding="utf-8")
    print(f"  pkb.md: {total} total entries")


TAG_SCAN_DIRS = [
    ("active",    "active"),
    ("followup",  "followup"),
    ("kb-updates","kb-updates"),
    ("archive",   "archive"),
    ("pkb",       "pkb"),
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
        active=case_rows("active", link_prefix=""),
        followup=case_rows("followup", link_prefix=""),
        kb=kb_rows(link_prefix=""),
        archive=case_rows("archive", link_prefix=""),
    )

    # Individual section pages — links relative to docs/dashboards/
    write_section_dashboard("active.md", "🟢 Active Cases", CASE_HEADER, case_rows("active"))
    write_section_dashboard("followup.md", "🔄 Follow-up Cases", CASE_HEADER, case_rows("followup"))
    write_section_dashboard("archive.md", "🗄️ Archived Cases", CASE_HEADER, case_rows("archive"))
    write_section_dashboard("kb-updates.md", "📚 KB Updates", KB_HEADER, kb_rows())

    print("Rebuilding meetings page...")
    write_meetings_page()

    print("Rebuilding PKB dashboard...")
    write_pkb_dashboard()

    print("Rebuilding tags page...")
    write_tags_page()

    print("Done.")
