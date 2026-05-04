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


MEETING_SECTIONS = [
    ("1on1",   "🤝 1-on-1 Meetings"),
    ("team",   "👥 Team Meetings"),
    ("general","📋 General Meetings"),
]


def write_meeting_index(subdir, title):
    folder = BASE / "meetings" / subdir
    folder.mkdir(parents=True, exist_ok=True)
    notes = sorted(folder.glob("*.md"), reverse=True)
    notes = [n for n in notes if n.name != "index.md"]
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [f"# {title}\n", f"*🕐 Updated: {timestamp}*\n"]
    if notes:
        for note in notes:
            stem = note.stem  # e.g. 05-03-26
            lines.append(f"- [{stem}]({note.name})")
    else:
        lines.append("*No notes yet.*")
    (folder / "index.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  meetings/{subdir}/index.md: {len(notes)} note(s)")


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

    print("Rebuilding meeting indexes...")
    for subdir, title in MEETING_SECTIONS:
        write_meeting_index(subdir, title)

    print("Done.")
