# Case Work

A local, Markdown-based workspace for tracking support cases, meeting notes and a personal knowledge base. You write notes in VS Code, and they render as a searchable local website with auto-built dashboards.

Everything lives in plain Markdown files on your machine. There is no server, database or account.

## What it does

- **Case notes** from a template, with priority, status and a one-line summary in frontmatter.
- **Dashboards** for active, follow-up and archived cases, rebuilt from that frontmatter with one shortcut.
- **Personal knowledge base (PKB)** with tabs you define in `pkb-categories.yaml`, plus two templates: a topic overview (PKB Note) and a focused write-up of one issue (KB Article).
- **Meeting notes** for 1-on-1, team and general meetings.
- **Screenshots and customer files**: drop a file in the workspace root with the case number as a prefix, and it is moved and linked into the note when you save.
- **Terminal helpers**: paste clipboard output as a timestamped code block, or record a whole terminal session.
- **macOS Reminders sync** for next-action checklists, plus an optional Jira-to-Reminders sync.
- **Tags page** across every note, plus sortable tables, a screenshot lightbox and Kubernetes icons you can use in notes.

## Built with

| Tool | Role |
| ---- | ---- |
| [VS Code](https://code.visualstudio.com) + [Foam](https://foambubble.github.io/foam/) | Editing, templates, links and the note graph |
| [Zensical](https://zensical.org) | Renders `docs/` as a local website |
| Python 3 | Dashboard and helper scripts |

## Requirements

- macOS (the Reminders sync, scheduler and clipboard helpers use macOS tools; the rest works anywhere VS Code and Python run)
- Python 3 from Homebrew
- VS Code with the Foam, Python and Run on Save extensions

## Quick start

> **Setup guide:** [docs/setup.md](docs/setup.md) has the full step-by-step walkthrough.

```bash
git clone <repo-url> ~/case-work
cd ~/case-work
/opt/homebrew/bin/python3 -m venv .venv
.venv/bin/pip install zensical
cp .env.example .env
.venv/bin/python3 scripts/sync_settings.py
code .vscode/case-work.code-workspace
```

Then in VS Code:

1. Trust the workspace when prompted.
2. Run the **🟢 Start Zensical** task (`Cmd+Shift+P` → **Tasks: Run Task**). It builds the dashboards, then serves the site at <http://127.0.0.1:8000>.
3. After editing notes, `Ctrl+Shift+B` rebuilds the dashboards. The open site reloads by itself.
4. `Cmd+Shift+P` → **Foam: Create New Note From Template** to start your first note.

Daily use, templates, tasks and customization are covered in [docs/guide.md](docs/guide.md).

## Customizing

- **Knowledge base tabs**: edit `pkb-categories.yaml`, then rebuild. The template dropdowns update to match.
- **Templates**: `.foam/templates/`.
- **Snippets**: `.vscode/case-work.code-snippets`.
- **VS Code settings**: edit `.vscode/settings.json`, your own gitignored copy. Defaults live in `.vscode/settings.default.json`; new defaults are added to your copy on each rebuild, and your changes are kept.
- **Site look and navigation**: `zensical.toml`.
- **Personal settings** (Jira, Explorer toggles): `.env` (gitignored).

## Privacy

Your notes stay out of git. Cases, meetings, PKB articles, attachments and generated dashboards are all listed in `.gitignore`, so you can pull updates or share your fork without publishing your work. Check `git status` before you push if you add new folders.

## License

[MIT](LICENSE). You're free to use, modify and redistribute it. Bundled third-party icons and scripts keep their own licenses, listed in [LICENSE](LICENSE).
