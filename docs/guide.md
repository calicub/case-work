---
icon: lucide/book-open
---

# 📖 Setup & Reference Guide

Quick reference for the Foam + Zensical case tracking system.
Keep this tab open in your browser while working in VS Code.

---

## 🧱 Stack

| Tool | Role |
|------|------|
| **Foam** | Note editing, templates, link graph — lives inside VS Code |
| **Zensical** | Renders your markdown as this local website |
| **Python scripts** | Dashboard tables, screenshot insertion — only where Foam/Zensical can't do it natively |

---

## ⌨️ Task Shortcuts

| Task | How to run | What it does |
|------|-----------|--------------|
| **Rebuild Dashboards** | `Ctrl+Shift+B` | Regenerates `dashboard.md` and all four section tables from your note frontmatter |
| **📎 Insert Customer Files** | `Ctrl+Shift+P` → Run Task | Finds files at workspace root matching the case number, moves them to `docs/files/`, inserts links into `## 📎 Customer Files` |
| **📸 Insert Screenshots** | `Ctrl+Shift+P` → Run Task | Finds screenshots at workspace root matching the case number, moves them to `docs/screenshots/`, inserts image blocks into `## 📸 Screenshots` |
| **📌 Append Terminal Block** | `Ctrl+Shift+;` | Reads clipboard and appends a timestamped code block to **🛠️ Steps Taken** in the active case note |
| **🖥️ Start Session Log** | `Ctrl+Shift+P` → Run Task | Starts a `script` recording session — saves everything to `docs/files/casenumber-terminal-session-date.txt` |
| **📋 Copy Support Notes (Salesforce)** | `Ctrl+Shift+P` → Run Task | Converts the Remote Support Note at the cursor to Salesforce plain text and copies it to clipboard |
| **📙 Zensical** | `Ctrl+Shift+P` → Run Task | Starts local server at `http://127.0.0.1:8000` — run once per session, leave it open |
| **🛑 Stop Zensical** | `Ctrl+Shift+P` → Run Task | Kills the Zensical server process |

!!! warning "Active tab tip"
    The **case note tab must be focused** in VS Code (not the terminal) when running Insert Screenshots, Insert Customer Files, Copy Support Notes, or Append Terminal Block — VS Code passes whichever file is currently active.

---

## 🖥️ Terminal Workflows

### Append Terminal Block

Capture a snippet of terminal output directly into **🛠️ Steps Taken**:

```
1. Select the output in the terminal

2. Cmd+C to copy

3. Focus the case note tab in VS Code

4. Ctrl+Shift+; — block is silently inserted:

   ``` title="14:32"
   output here
   ```

5. Switch back to the terminal and continue working
```

### Session Logging

Record an entire terminal session (useful for long cluster investigations):

```
1. Focus the case note tab so VS Code knows which case you're on

2. Ctrl+Shift+P → Run Task → 🖥️ Start Session Log
   A new terminal opens with script recording active

3. Do your work — everything typed and output is captured

4. Type exit to stop recording
   File saved to: docs/files/casenumber-terminal-session-date.txt

5. Run 📎 Insert Customer Files to link the log to the case note
```

!!! note "Session log tip"
    The log file contains raw terminal output including color/escape codes. It is still readable as plain text and opens correctly in a terminal.

---

## 📋 Templates

New note: `Ctrl+Shift+P` → **Foam: Create New Note From Template** → pick a template.
**Type the case/KB number when prompted** — it becomes the filename and auto-fills `case_number`.
Then `Tab` through each field.

=== "🎫 New Case"

    | # | Field | Notes |
    |---|-------|-------|
    | auto | `case_number` | Filled from the filename you typed |
    | **1** | `customer` | Links to the heading — type once, appears in both |
    | **2** | `priority` | Dropdown: P1 / P2 / P3 / P4 |
    | **3** | `status` | Dropdown: Open · In Progress · Pending Customer · Escalated · Resolved |
    | **4** | `note` | One-liner shown in all dashboard tables |
    | **5** | Issue body | Describe the problem |
    | **6** | Next action | First action item |
    | done | Customer Files tab | Cursor lands here; run Insert Customer Files task when ready |

    **Page sections:** 🔍 Description · ▶️ Next Action · 🔄 Follow-up · 🛠️ Steps Taken
    **Attachment tabs (below Steps Taken):** 📎 Customer Files · 📸 Screenshots

=== "🔄 Follow-up"

    | # | Field |
    |---|-------|
    | auto | `case_number` |
    | **1** | `customer` |
    | **2** | `priority` |
    | **3** | `status` |
    | **4** | `follow_up_date` |
    | **5** | `note` |
    | **6** | Context body |
    | **7** | First action item |

=== "📚 KB Update"

    | # | Field |
    |---|-------|
    | auto | `kb_number` |
    | **1** | `title` |
    | **2** | `category` |
    | **3** | `status` (Draft · Review · Published) |
    | **4** | Overview (fills frontmatter `note` and `## 📖 Overview` simultaneously) |
    | **5** | Details body |

---

## 📎 Customer Files Workflow

```
1. Save the customer's file anywhere at the workspace root, prefixed with the case number:
      123456 - export.csv
      123456 - config.md

2. Focus the case note tab in VS Code

3. Ctrl+Shift+P → Run Task → 📎 Insert Customer Files

4. Script moves the file to docs/files/ and writes this into the note:

      [123456 - export.csv](../files/123456-export.csv)

5. Ctrl+Shift+B → rebuild dashboards → browser auto-reloads
```

---

## 📋 Salesforce Notes Workflow

```
1. Write your remote support note using the `remotenote` snippet

2. Place your cursor anywhere inside the ### 📓 Remote Support block

3. Ctrl+Shift+P → Run Task → 📋 Copy Support Notes (Salesforce)

4. Plain text version is copied to clipboard — paste directly into Salesforce
   A preview is also printed in the terminal panel
```

---

## ✂️ Snippets

Type any prefix in a markdown file and select from the suggestion list (`Ctrl+Space` to force it open).

| Prefix | Name | Inserts |
|--------|------|---------|
| `today` | Date | `#### Month DD` heading with today's date |
| `ustatus` | Update Case Status | Salesforce status dropdown: In-Progress · Waiting-for-Customer · etc. |
| `kbi` | Keyboard Key | `<kbd>key</kbd>` inline tag |
| `casedesc` | Case Description | Quote admonition block for pasting the Salesforce case description |
| `remotenote` | Remote Support Notes | Full remote support session block with via · attendees · details · action plan |

---

## 📸 Screenshot Workflow

```
1. Take screenshot → Automator renames it:  123456 - description.png
                                             saved to case-work/ root

2. Focus the case note tab in VS Code

3. Ctrl+Shift+P → Run Task → 📸 Insert Screenshots

4. Script moves image to docs/screenshots/ and writes this into the note:

   ![123456 - description](../screenshots/123456-description.png){ loading=lazy }
   /// caption
   123456 - description
   ///

5. Ctrl+Shift+B → rebuild dashboards → browser auto-reloads
```

---

## 📊 Dashboard Rules

!!! danger "Do not edit dashboard files by hand"
    `docs/dashboard.md` and everything in `docs/dashboards/` are **auto-generated**.
    Any manual edits will be overwritten the next time you run `Ctrl+Shift+B`.

| Dashboard | Source folder | Sort order |
|-----------|--------------|------------|
| 🟢 Active | `docs/active/` | P1 → P4 |
| 🔄 Follow-up | `docs/followup/` | P1 → P4 |
| 📚 KB Updates | `docs/kb-updates/` | Filename order |
| 🗄️ Archive | `docs/archive/` | P1 → P4 |

Rebuild dashboards after: creating a note · editing frontmatter · archiving a case.

---

## 🗁 Folder Structure

```
case-work/
├── zensical.toml          ← site config (TOML format — not mkdocs.yml)
├── .foam/templates/       ← case.md · followup.md · kb-update.md
├── .vscode/
│   ├── settings.json           ← Foam config, editor settings, markdown snippet support
│   ├── tasks.json              ← all runnable tasks defined here
│   └── case-work.code-snippets ← workspace snippets (remotenote, casedesc, etc.)
├── docs/                  ← Zensical serves everything from here
│   ├── index.md           ← home page
│   ├── dashboard.md       ← tabbed dashboard (auto-generated)
│   ├── guide.md           ← this page
│   ├── dashboards/        ← section tables (auto-generated)
│   ├── active/            ← active case notes
│   ├── followup/          ← follow-up notes
│   ├── kb-updates/        ← KB article notes
│   ├── archive/           ← resolved case notes
│   ├── files/             ← customer-provided files (moved here by script)
│   └── screenshots/       ← case screenshots (moved here by script)
└── scripts/
    ├── dashboard.py              ← regenerates all dashboards
    ├── insert_screenshots.py     ← finds & inserts screenshots
    ├── insert_files.py           ← finds & inserts customer files
    └── copy_salesforce_notes.py  ← converts remote support note to Salesforce plain text
```

---

## 🔧 Environment

```bash
# Zensical is in the project virtual environment — no global install needed
# Tasks use the full path: .venv/bin/zensical and .venv/bin/python3

# To upgrade Zensical:
.venv/bin/pip install --upgrade zensical

# Check current version:
.venv/bin/zensical --version
```

Set VS Code's Python interpreter to `.venv/bin/python3`:
`Ctrl+Shift+P` → **Python: Select Interpreter** → `.venv/bin/python3`

---

## 🔗 Links in Notes

Foam supports both `[[wikilinks]]` and standard `[text](path)` markdown links — both show up in the graph and backlinks panel. This workspace defaults Foam's autocomplete to insert `[text](path)` style links (`foam.completion.link.style: markdown`).

---

## 📝 Quirks & Gotchas

- **`zensical.toml`** — Zensical's config is TOML, not the YAML `mkdocs.yml` used by plain MkDocs
- **Files outside `docs/`** — not served by Zensical; always create case notes via the Foam template so they land in the right folder
- **Screenshots outside `docs/`** — not served; the Insert Screenshots task moves them automatically
- **`${file}` in tasks** — always refers to the active VS Code editor tab, not the last-saved file
