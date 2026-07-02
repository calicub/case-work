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

## 🗂️ Workspaces

Two `.code-workspace` files live in `.vscode/` — open them with **File → Open Workspace from File**.

| File | Name | Shows |
|------|------|-------|
| `case-work-dev.code-workspace` | 📝 Notes (Dev Mode) | Everything — full project tree |
| `case-work-view.code-workspace` | 📖 Case-work (Read/Edit) | `.vscode/` · `docs/assets/` · `docs/cases/` · `docs/meetings/` · `docs/pkb/` · `docs/guide.md` · `docs/tags.md` |

The view workspace hides generated dashboards, config files, scripts, and other non-note content so the Explorer stays focused on case work.

---

## ⌨️ Task Shortcuts

| Task | How to run | What it does |
|------|-----------|--------------|
| **Rebuild Dashboards** | `Ctrl+Shift+B` | Regenerates `dashboard.md` and all four section tables from your note frontmatter |
| **📎 Insert Customer Files** | `Ctrl+Shift+P` → Run Task | Finds files at workspace root matching the case number, moves them to `docs/assets/files/`, inserts links into `## 📎 Customer Files` — also runs automatically on save |
| **📸 Insert Screenshots** | `Ctrl+Shift+P` → Run Task | Finds screenshots at workspace root matching the case number, moves them to `docs/assets/screenshots/`, inserts image blocks into `## 📸 Screenshots` — also runs automatically on save |
| **📌 Append Terminal Block** | `Ctrl+Shift+;` | Reads clipboard and appends a timestamped code block to **🛠️ Steps Taken** in the active case note |
| **🖥️ Start Session Log** | `Ctrl+Shift+P` → Run Task | Starts a `script` recording session — saves everything to `docs/assets/files/casenumber-terminal-session-date.txt` |
| **📋 Copy Support Notes (Salesforce)** | `Ctrl+Shift+P` → Run Task | Converts the Remote Support Note at the cursor to Salesforce plain text and copies it to clipboard |
| **📋 Copy Prior Actions (Salesforce)** | `Ctrl+Shift+P` → Run Task | Copies the steps performed from the Remote Support Note at the cursor, formatted as `--- Month Nth ---` + `+ step` lines |
| **📙 Zensical** | `Ctrl+Shift+P` → Run Task | Starts local server at `http://127.0.0.1:8000` — run once per session, leave it open |
| **🛑 Stop Zensical** | `Ctrl+Shift+P` → Run Task | Kills the Zensical server process |
| **🔔 Sync to Reminders** | Auto on `Cmd+S` | Pushes `▶️ Next Action` tasks to the macOS Reminders "Case Actions" list — active and followup only |
| **📎📸 Insert Assets** | Auto on `Cmd+S` | Runs on every save — picks up any matching files and screenshots at the workspace root and inserts them into the note |
| **⏰ Install Jira Reminders Schedule** | `Ctrl+Shift+P` → Run Task | One-time setup — installs a background schedule that syncs Jira KB/Docs tasks to Reminders at 09:30 and 12:30 daily |
| **🔄 Run Jira Reminders Now** | `Ctrl+Shift+P` → Run Task | Manually triggers the Jira → Reminders sync without waiting for the schedule |
| **🔁 Toggle File Visibility** | `Ctrl+Shift+P` → Run Task | Alternates the Explorer between focused view (hides dashboards, stylesheets, config files) and full view (shows everything) — state is saved to `.env` so it persists across sessions |

!!! warning "Active tab tip"
    The **case note tab must be focused** in VS Code (not the terminal) when running Insert Screenshots, Insert Customer Files, Copy Support Notes, or Append Terminal Block — VS Code passes whichever file is currently active.

---

## 🔔 Reminders Sync

Action items in the **▶️ Next Action** section of any active or follow-up case note are automatically synced to the macOS **Reminders** app whenever you save the file.

```
1. Add tasks under ## ▶️ Next Action using standard checkboxes:

      - [ ] Call customer to confirm reproduction steps
      - [ ] Open engineering ticket
      - [ ] Follow up with customer @5/15          ← due May 15 at 08:00
      - [ ] Submit engineering ticket @5/15-14:30          ← due May 15 at 14:30 (24-hour)

2. Save the file (Cmd+S)
   Tasks appear in a "Case Actions" list in Reminders, prefixed with the case number:
      [02468] Call customer to confirm reproduction steps
      [02468] Follow up with customer              ← due date set; @annotation stripped from title

3. Mark a task done in the note:

      - [x] Call customer to confirm reproduction steps

4. Save again — the matching reminder is marked complete in Reminders
```

**Due date syntax**

| Format | Example | Result |
|--------|---------|--------|
| `@M/D` | `@5/15` | Due May 15, no time set |
| `@M/D-HH:MM` | `@5/15-14:30` | Due May 15 at 14:30 (24-hour) |

The `@` annotation is stripped from the Reminders title — only the task text is shown there. Year is always assumed to be the current year.

!!! info "Scope"
    Only files in `docs/cases/active/` and `docs/cases/followup/` are processed.
    Archive is never touched, regardless of how large it grows.

!!! tip "Duplicate prevention"
    Saving multiple times is safe — the script checks for existing reminders before creating new ones.

---

## 🎫 Jira Reminders

Open KB/Docs tasks assigned to you in Jira are automatically synced to the macOS **Reminders** app twice a day (09:30 and 12:30). Each reminder repeats every 4 days until you mark it complete.

### First-time setup (once per machine)

```
1. Copy the env template and fill in your details:

      cp .env.example .env
      # then open .env and set:
      JIRA_URL=https://your-jira-instance
      JIRA_TOKEN=your-personal-access-token
      JIRA_JQL=assignee = currentUser() AND type = Task AND (status = Open OR status = "In Progress")

   JIRA_JQL is optional — the default query above is used if you leave it out.
   Adjust it if you want to filter by component, project, or other criteria.

2. Ctrl+Shift+P → Run Task → ⏰ Install Jira Reminders Schedule
   You should see: ✅  Schedule installed.

That's it — the schedule survives reboots and runs without VS Code open.
```

!!! warning ".env is gitignored"
    `.env` is never committed. Each teammate creates their own copy from `.env.example`. Pulling updates will never overwrite it.

### What gets synced

Each reminder lands in a **"Jira Tasks"** list in Reminders (created automatically) with:

| Field | Source |
|-------|--------|
| Title | `[KEY-123] Ticket summary` |
| Body note | Key · Created date · Due date · Browse URL |
| Due date | Jira `duedate` field (omitted if not set in Jira) |
| Recurrence | Every 4 days |

### Confirming it works

**Check the log after a scheduled run:**

```bash
cat /tmp/jira-reminders.log
```

A successful run looks like:

```
Fetching Jira tickets…
Found 3 ticket(s). Creating reminders…

  [KB-101] (In Progress) Update LDAP auth guide
    Created: 2026-05-10  |  Due: 2026-06-15
  [KB-88]  (Open) Document new cluster upgrade path
    Created: 2026-04-28  |  Due: not set
  ...
Done — 3 reminder(s) synced to "Jira Tasks".
```

**Check that the schedule is loaded:**

```bash
launchctl list | grep jira-reminders
```

You should see a line like:

```
-   0   com.casework.jira-reminders
```

The middle number is the last exit code — `0` means the last run succeeded. Any non-zero value means it errored; check the log above.

**Trigger a test run immediately:**

```
Ctrl+Shift+P → Run Task → 🔄 Run Jira Reminders Now
```

Output appears in the VS Code terminal panel. Check Reminders.app for a "Jira Tasks" list afterward.

**Common failure reasons:**

| Symptom | Likely cause |
|---------|-------------|
| `HTTP 401` in log | TOKEN is wrong or expired — generate a new PAT in Jira |
| `Failed to reach the server` | Wrong `SERVER_URL` or VPN not connected |
| No log file at all | Schedule not loaded — re-run the Install task |
| Schedule loaded but not firing | Mac was asleep at 09:30/12:30 — launchd will run it at next wake if the window was missed |

**To uninstall the schedule:**

```bash
launchctl unload ~/Library/LaunchAgents/com.casework.jira-reminders.plist
rm ~/Library/LaunchAgents/com.casework.jira-reminders.plist
```

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
   File saved to: docs/assets/files/casenumber-terminal-session-date.txt

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

=== "🤝 1-on-1 Meeting"

    Saved to `docs/meetings/1on1/MM-DD-YY.md`

    | Section | Notes |
    |---------|-------|
    | **1** | First discussion topic |
    | **2** | First action item |

=== "👥 Team Meeting"

    Saved to `docs/meetings/team/MM-DD-YY.md`

    | Section | Notes |
    |---------|-------|
    | **1** | First attendee |
    | **2** | First discussion topic |
    | **3** | First action item |

=== "📋 General Meeting"

    Saved to `docs/meetings/general/MM-DD-YY.md`

    | Section | Notes |
    |---------|-------|
    | **1** | First discussion topic |
    | **2** | First action item |

=== "📓 PKB Note"

    Saved to `docs/pkb/<slug>.md` — type a short descriptive name when prompted (e.g. `ldap-auth-troubleshooting`).

    | # | Field | Notes |
    |---|-------|-------|
    | **1** | `title` | Full readable title |
    | **2** | `category` | Dropdown: Tools · Troubleshooting |
    | **3** | `tags` | Comma-separated: `[kubernetes, ldap]` — see tag conventions below |
    | **4** | Overview | Freeform notes and context |
    | **5–13** | Table rows | KB link · Engineering ticket · Confluence · Doc ref rows |

    **Page sections:** 📝 Overview · 📋 KB Articles · 🔧 Engineering Tickets · 📘 Confluence · 📄 Doc References

---

## 🏷️ Tag Conventions

Tags are set in frontmatter as a YAML list: `tags: [kubernetes, ldap, ssl]`

Apply **both** a product tag and one or more topic tags so notes are findable from either angle.

**Product tags**

| Tag | Covers |
| --- | ------ |
| `kubernetes` | Kubernetes clusters and workloads |
| `linux` | Linux hosts and distributions |
| `tools` | Internal or third-party tools |

**Topic tags (examples — add your own)**

| Tag | Covers |
| --- | ------ |
| `ldap` | LDAP / Active Directory auth |
| `ssl` | SSL / TLS / certificates |
| `high-availability` | HA, clustering, failover |
| `backup` | Backup and restore |
| `api` | REST API usage or issues |
| `performance` | Slow queries, resource usage |
| `upgrade` | Version upgrade procedures |

The **🏷️ Tags** page in the nav aggregates every tagged note across the whole site — PKB notes, cases, and meetings — grouped by tag.

---

## 📎 Customer Files Workflow

```
1. Save the customer's file anywhere at the workspace root, prefixed with the case number:
      123456 - export.csv
      123456 - config.md

2. Focus the case note tab in VS Code and save (Cmd+S)

   → Files are picked up and inserted automatically.
   → Or run manually: Ctrl+Shift+P → Run Task → 📎 Insert Customer Files

3. Script moves the file to docs/assets/files/ and writes this into the note:

      [123456 - export.csv](../../assets/files/123456-export.csv)

4. Ctrl+Shift+B → rebuild dashboards → browser auto-reloads
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
| `cbl` | Code Block (Log) | Titled fenced code block — cursor lands in title, Tab moves to body |
| `cby` | Code Block (YAML) | Same as `cbl` with `yaml` language tag |

!!! tip "Log file language"
    Use `log` or `text` as the language for log snippets — both skip syntax highlighting. `log` may subtly colorize timestamps and error levels depending on the theme.

---

## 🎨 Custom Icons

Icons from any registered set can be used inline in notes with `:set-name:` syntax.
Zensical renders them as inline SVGs — they scale with text and respect the current theme.

### Using icons in notes

```markdown
:k8s-pod: This pod is failing to schedule.
:k8s-svc: Service is exposed on port 443.

| Component | Status |
|-----------|--------|
| :k8s-api: API Server | Healthy |
| :k8s-etcd: etcd | Healthy |
| :k8s-node: Node | NotReady |
```

### Available icon sets

=== ":k8s: Kubernetes"

    | Icon | Name | Syntax |
    |------|------|--------|
    | :k8s-pod: | Pod | `:k8s-pod:` |
    | :k8s-deploy: | Deployment | `:k8s-deploy:` |
    | :k8s-svc: | Service | `:k8s-svc:` |
    | :k8s-ns: | Namespace | `:k8s-ns:` |
    | :k8s-node: | Node | `:k8s-node:` |
    | :k8s-etcd: | etcd | `:k8s-etcd:` |
    | :k8s-api: | API Server | `:k8s-api:` |
    | :k8s-kubelet: | Kubelet | `:k8s-kubelet:` |
    | :k8s-sched: | Scheduler | `:k8s-sched:` |
    | :k8s-cm: | ConfigMap | `:k8s-cm:` |
    | :k8s-secret: | Secret | `:k8s-secret:` |
    | :k8s-pv: | PersistentVolume | `:k8s-pv:` |
    | :k8s-pvc: | PersistentVolumeClaim | `:k8s-pvc:` |
    | :k8s-ing: | Ingress | `:k8s-ing:` |
    | :k8s-sa: | ServiceAccount | `:k8s-sa:` |
    | :k8s-ds: | DaemonSet | `:k8s-ds:` |
    | :k8s-sts: | StatefulSet | `:k8s-sts:` |
    | :k8s-rs: | ReplicaSet | `:k8s-rs:` |
    | :k8s-hpa: | HorizontalPodAutoscaler | `:k8s-hpa:` |
    | :k8s-job: | Job | `:k8s-job:` |
    | :k8s-cronjob: | CronJob | `:k8s-cronjob:` |
    | :k8s-sc: | StorageClass | `:k8s-sc:` |
    | :k8s-netpol: | NetworkPolicy | `:k8s-netpol:` |
    | :k8s-crd: | CustomResourceDefinition | `:k8s-crd:` |
    | :k8s-role: | Role | `:k8s-role:` |
    | :k8s-c-role: | ClusterRole | `:k8s-c-role:` |
    | :k8s-rb: | RoleBinding | `:k8s-rb:` |
    | :k8s-crb: | ClusterRoleBinding | `:k8s-crb:` |
    | :k8s-control-plane: | Control Plane | `:k8s-control-plane:` |
    | :k8s-c-m: | Controller Manager | `:k8s-c-m:` |
    | :k8s-c-c-m: | Cloud Controller Manager | `:k8s-c-c-m:` |
    | :k8s-k-proxy: | kube-proxy | `:k8s-k-proxy:` |
    | :k8s-ep: | Endpoint | `:k8s-ep:` |
    | :k8s-vol: | Volume | `:k8s-vol:` |
    | :k8s-quota: | ResourceQuota | `:k8s-quota:` |
    | :k8s-limits: | LimitRange | `:k8s-limits:` |
    | :k8s-psp: | PodSecurityPolicy | `:k8s-psp:` |
    | :k8s-group: | Group | `:k8s-group:` |
    | :k8s-user: | User | `:k8s-user:` |
    | :k8s-logo: | Kubernetes Logo | `:k8s-logo:` |

### Adding a new icon pack

1. Place SVG files in `overrides/.icons/<set-name>/`
   — subdirectories are supported: `overrides/.icons/<set-name>/<sub>/icon.svg` → `:set-name-sub-icon:`
2. Symlinks work — point them at the source SVGs to avoid duplication
3. Restart Zensical (`Ctrl+Shift+B`) — no config changes needed

---

## 📸 Screenshot Workflow

```
1. Take screenshot → Automator renames it:  123456 - description.png
                                             saved to case-work/ root

2. Focus the case note tab in VS Code and save (Cmd+S)

   → Screenshots are picked up and inserted automatically.
   → Or run manually: Ctrl+Shift+P → Run Task → 📸 Insert Screenshots

3. Script moves image to docs/assets/screenshots/ and writes this into the note:

   ![123456 - description](../../assets/screenshots/123456-description.png){ loading=lazy }
   /// caption
   123456 - description
   ///

4. Ctrl+Shift+B → rebuild dashboards → browser auto-reloads
```

---

## 📊 Dashboard Rules

!!! danger "Do not edit dashboard files by hand"
    `docs/dashboard.md` and everything in `docs/dashboards/` are **auto-generated**.
    Any manual edits will be overwritten the next time you run `Ctrl+Shift+B`.

| Dashboard | Source folder | Sort order |
|-----------|--------------|------------|
| 🟢 Active | `docs/cases/active/` | P1 → P4 |
| 🔄 Follow-up | `docs/cases/followup/` | Newest first |
| 🗄️ Archive | `docs/cases/archive/` | Newest first |
| 📅 Meetings | `docs/meetings/*/` | Newest first per type |
| 📓 Knowledge Base | `docs/pkb/` | Newest first per category |

Rebuild dashboards after: creating a note · editing frontmatter · archiving a case · adding a PKB note.

---

## 🗁 Folder Structure

```
case-work/
├── zensical.toml                        ← site config (TOML — not mkdocs.yml)
├── overrides/                           ← Zensical theme overrides
│   └── .icons/                          ← custom icon sets (use as :set-name: in notes)
│       └── k8s/                         ← Kubernetes icons — symlinked from docs/assets/images/kubernetes/
├── .foam/
│   └── templates/                       ← Foam note templates (one per note type)
│       ├── case.md                      ← new support case
│       ├── followup.md                  ← follow-up for an existing case
│       ├── meeting-1on1.md              ← 1-on-1 meeting notes
│       ├── meeting-team.md              ← team meeting notes
│       ├── meeting-general.md           ← general meeting notes
│       └── pkb.md                       ← personal knowledge base article
├── .vscode/
│   ├── settings.json                    ← Foam config, editor settings, snippet support
│   ├── tasks.json                       ← all Ctrl+Shift+P runnable tasks
│   └── case-work.code-snippets          ← workspace snippets (remotenote, casedesc, etc.)
├── scripts/
│   ├── dashboard.py                     ← regenerates all dashboards and index pages
│   ├── insert_assets.py                 ← moves & inserts screenshots and files into case notes (runs on save)
│   ├── append_terminal_block.py         ← appends clipboard as timestamped code block
│   ├── copy_salesforce_notes.py         ← converts remote support note to Salesforce plain text
│   ├── copy_remote_steps.py             ← copies steps performed from remote support note to clipboard
│   ├── sync_reminders.sh               ← syncs ▶️ Next Action tasks to macOS Reminders on save
│   └── toggle_view.py                  ← toggles Explorer between focused and full view via files.exclude
└── docs/                                ← Zensical serves everything from here
    ├── index.md                         ← home page
    ├── dashboard.md                     ← tabbed case dashboard (auto-generated)
    ├── meetings.md                      ← meetings index page (auto-generated)
    ├── pkb.md                           ← knowledge base index (auto-generated)
    ├── tags.md                          ← tag index across all notes (auto-generated)
    ├── guide.md                         ← this page
    ├── setup.md                         ← setup and upgrade instructions
    ├── markdown.md                      ← markdown syntax reference
    ├── cases/                           ← all case lifecycle notes
    │   ├── active/                      ← open cases in progress
    │   ├── followup/                    ← cases awaiting action or response
    │   └── archive/                     ← resolved and closed cases
    ├── dashboards/                      ← per-section dashboard pages (auto-generated)
    │   ├── active.md
    │   ├── followup.md
    │   └── archive.md
    ├── meetings/                        ← meeting notes organised by type
    │   ├── 1on1/                        ← 1-on-1 notes with manager
    │   ├── team/                        ← team meeting notes
    │   └── general/                     ← all other meeting notes
    ├── pkb/                             ← personal KB articles (category set in frontmatter)
    ├── assets/                          ← static assets served by Zensical
    │   ├── files/                       ← customer-provided files (moved here by script)
    │   ├── screenshots/                 ← case screenshots (moved here by script)
    │   ├── images/                      ← site images
    │   └── stylesheets/                 ← custom CSS (extra.css)
    └── javascripts/                     ← custom JavaScript (tabs.js)
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
- **Screenshots and files outside `docs/`** — not served by Zensical; drop them at the workspace root prefixed with the case number and they will be moved to `docs/assets/` automatically on the next save
- **`${file}` in tasks** — always refers to the active VS Code editor tab, not the last-saved file
