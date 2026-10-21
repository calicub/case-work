#!/usr/bin/env python3
"""Add this project's keyboard shortcuts to your VS Code keybindings.json.

VS Code only reads keyboard shortcuts from your user settings, not from a
project folder, so they have to be added there once per Mac.

Safe to run again: shortcuts that are already present are skipped, and the
existing file is backed up to keybindings.json.bak before it is changed.

Usage: install_keybindings.py [path/to/keybindings.json]
"""
import json
import re
import shutil
import sys
from pathlib import Path

DEFAULT_PATH = Path.home() / "Library" / "Application Support" / "Code" / "User" / "keybindings.json"

BINDINGS = [
    {
        "key": "ctrl+shift+;",
        "command": "workbench.action.tasks.runTask",
        "args": "📌 Append Terminal Block",
    },
]


def strip_jsonc(text):
    """Remove // and /* */ comments and trailing commas so the file parses as JSON."""
    out, i, in_str = [], 0, False
    while i < len(text):
        c = text[i]
        if in_str:
            out.append(c)
            if c == "\\":
                out.append(text[i + 1]); i += 1
            elif c == '"':
                in_str = False
        elif c == '"':
            in_str = True; out.append(c)
        elif text.startswith("//", i):
            while i < len(text) and text[i] != "\n":
                i += 1
            continue
        elif text.startswith("/*", i):
            i = text.find("*/", i + 2)
            i = len(text) if i < 0 else i + 2
            continue
        else:
            out.append(c)
        i += 1
    return re.sub(r",(\s*[\]}])", r"\1", "".join(out))


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PATH
    text = path.read_text(encoding="utf-8") if path.exists() else ""

    existing = []
    if text.strip():
        try:
            existing = json.loads(strip_jsonc(text))
        except json.JSONDecodeError as e:
            sys.exit(f"  Couldn't read {path} ({e}). Add the shortcut by hand; see the guide.")
        if not isinstance(existing, list):
            sys.exit(f"  {path} isn't a list of shortcuts. Add the shortcut by hand; see the guide.")

    have = {(b.get("key"), b.get("command"), json.dumps(b.get("args"))) for b in existing if isinstance(b, dict)}
    todo = [b for b in BINDINGS if (b["key"], b["command"], json.dumps(b.get("args"))) not in have]
    if not todo:
        print("  Keyboard shortcuts already set up")
        return

    entries = ",\n".join(
        "\n".join("  " + line for line in json.dumps(b, indent=2, ensure_ascii=False).splitlines())
        for b in todo
    )

    if not text.strip():
        path.parent.mkdir(parents=True, exist_ok=True)
        new = "// Keyboard shortcuts\n[\n" + entries + "\n]\n"
    else:
        # Insert before the closing ] so the user's comments and layout are kept.
        end = text.rstrip().rfind("]")
        if end < 0:
            sys.exit(f"  Couldn't find the end of the list in {path}. Add the shortcut by hand; see the guide.")
        before = text[:end].rstrip()
        needs_comma = bool(existing) and not before.endswith(",")
        new = before + ("," if needs_comma else "") + "\n" + entries + "\n" + text[end:]
        shutil.copyfile(path, path.with_name(path.name + ".bak"))

    json.loads(strip_jsonc(new))  # never write a file VS Code can't read
    path.write_text(new, encoding="utf-8")
    for b in todo:
        print(f"  Added {b['key']} → {b['args']}")


if __name__ == "__main__":
    main()
