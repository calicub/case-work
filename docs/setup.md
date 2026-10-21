---
icon: lucide/wrench
---

# 🚀 Setup & Upgrades

---

!!! info "Reading this guide"
    Before the site is running, read this page on GitHub or in VS Code's Markdown preview (`Cmd+Shift+V`). Once it's running, the same page is under **Setup** in the site's top navigation.

## ⚡ Quick Setup (Recommended)

The installer is the easy way to start using Case Work: it does almost everything for you. If you'd rather not run a script, follow the [Manual Setup](#manual-setup) steps below instead. They set up exactly the same things, one at a time.

**1. Get the project.** Open Terminal and run:

```bash
git clone https://github.com/calicub/case-work.git ~/case-work
```

If macOS says `git` needs the **command line developer tools**, click **Install**, wait for it to finish, then run the command again.

**2. Run the installer:**

```bash
cd ~/case-work
./install.sh
```

**What it does:** It asks before installing anything, then:

- installs Homebrew, Homebrew's Python and VS Code if they're missing;
- installs the Foam, Python and Run on Save extensions;
- builds the project's Python environment (`.venv`) with Zensical;
- creates your `.env` and `.vscode/settings.json`;
- builds the site and opens the project folder in VS Code.

It's safe to run again: finished steps are skipped and a broken `.venv` is rebuilt.

**Success looks like:** Every step shows a ✓, and the output ends with `==> Done`.

**3. Finish in VS Code** (the installer opens it):

1. Click **Yes, I trust the authors**.
2. `Cmd+Shift+P` → **Tasks: Run Task** → **🟢 Start Zensical**, then open <http://127.0.0.1:8000>.
3. Using the Reminders sync? Open a case note, run **🔔 Sync Reminders Now** once, and click **Allow** when macOS asks.

To update later, run `./install.sh --upgrade` from the `case-work/` root. Run `./install.sh --help` for all options.

---

## 🛠️ Manual Setup

The same steps the installer runs, one at a time. Use these if the installer stops on an error, or if you want to see exactly what's set up.

### 1. Install Homebrew

Open Terminal and run:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Follow the prompts. When it finishes, run the two `eval` commands it prints at the end to add `brew` to your PATH (they look like `echo '...' >> ~/.zprofile`).

Verify:

```bash
brew --version
```

### 2. Install Python

Use Homebrew to install Python 3:

```bash
brew install python
```

**What it does:** Installs a current Python at `/opt/homebrew/bin/python3`.

Then make sure the shell picks the Homebrew Python instead of Apple's. Add this line to the end of `~/.zshrc`:

```bash
export PATH="/opt/homebrew/bin:$PATH"
```

**What it does:** Puts `/opt/homebrew/bin` at the front of the search path, so `python3` resolves to Homebrew's version before macOS's built-in one (`/usr/bin/python3`, version 3.9.x).

Open a new terminal tab (or run `source ~/.zshrc`), then verify:

```bash
which python3
python3 --version
```

**Success looks like:** `which` prints `/opt/homebrew/bin/python3` and the version is the one Homebrew installed (e.g. `Python 3.15.0`). If you see `/usr/bin/python3` or `3.9.6`, the PATH line is missing or the terminal was not reloaded.

!!! note "System Python"
    macOS ships with a very old Python. Always use the Homebrew-installed `python3`.

!!! tip "Optional aliases"
    `alias python="python3"` and `alias pip="pip3"` in `~/.zshrc` are convenient but not required. The VS Code tasks call `.venv/bin/python3` directly, and an activated venv provides its own `pip`.

### 3. Install VS Code

Download from [code.visualstudio.com](https://code.visualstudio.com) and drag it to Applications.

Then install the `code` shell command so you can open projects from the terminal:

`Cmd+Shift+P` → **Shell Command: Install 'code' command in PATH**

Install the extensions this project uses (`Cmd+Shift+X` → search the ID → Install):

| Extension | ID | Used for |
| --------- | -- | -------- |
| Foam | `foam.foam-vscode` | Note templates, links, graph |
| Python | `ms-python.python` | Selecting the `.venv` interpreter |
| Run on Save | `emeraldwalk.RunOnSave` | Reminders sync and asset insertion when you save a case note |

### 4. Clone / Copy the Project

`git clone` always creates a subfolder named after the repo inside the current directory. To put the project exactly where you want it, pass the target path as the second argument:

```bash
git clone https://github.com/calicub/case-work.git ~/case-work
```

!!! warning "Don't nest the folder"
    Running `git clone <repo-url>` inside an existing folder (e.g. `~/case-work/`) will create `~/case-work/case-work/` — one level deeper than intended. Always specify the full destination path.

Open the project folder in VS Code:

```bash
code ~/case-work
```

### 5. Create the Python Virtual Environment

Run these commands from the `case-work/` root:

```bash
/opt/homebrew/bin/python3 -m venv .venv
```

**What it does:** Creates `.venv/`, a private copy of Python and pip just for this project, so packages never touch the system. Using the full Homebrew path guarantees the venv is built on the right Python even if your PATH is not set up yet.

!!! note "VS Code prompt"
    If VS Code is already open on the project, it may notice the new environment and ask whether to use it for this project. Choose **Yes**. That does the same thing as step 7.

**Success looks like:** Check which Python the venv is based on:

```bash
cat .venv/pyvenv.cfg
```

`home` should be `/opt/homebrew/...` and `version` should match Homebrew's Python. If `home` is `/Library/Developer/CommandLineTools/...` or the version is `3.9.x`, the venv is built on the wrong Python — see [Troubleshooting](#troubleshooting).

Activate it (you only need this for manual terminal use — tasks run it automatically):

```bash
source .venv/bin/activate
```

**Success looks like:** Your prompt gains a `(.venv)` prefix, and `which python3` points inside the project's `.venv/bin/`.

### 6. Install Zensical

With the virtual environment active:

```bash
pip install -r requirements.txt
```

**What it does:** Downloads Zensical (the site generator) and its dependencies into `.venv`.

Verify:

```bash
zensical --version
```

**Success looks like:** A version number prints (e.g. `0.0.71`) with no errors.

Deactivate when done:

```bash
deactivate
```

**Success looks like:** The `(.venv)` prefix disappears from your prompt.

### 7. Set the VS Code Python Interpreter

The project settings already point VS Code at `.venv/bin/python3`, so there's usually nothing to do here. If the status bar shows a different Python, or VS Code asks, choose the project's `.venv`:

`Ctrl+Shift+P` → **Python: Select Interpreter** → `.venv/bin/python3`

### 8. Open the Project in VS Code

Open the `case-work` folder itself in VS Code. Foam, the tasks and the on-save hooks all load from its `.vscode/` folder.

1. Create your VS Code settings, then open the folder:

    ```bash
    cd ~/case-work
    .venv/bin/python3 scripts/sync_settings.py
    code .
    ```

    **What the first command does:** Creates `.vscode/settings.json` from the tracked defaults in `.vscode/settings.default.json`. Your `settings.json` is gitignored, so VS Code prompts, the Toggle File Visibility task and your own tweaks never block `git pull`. Each dashboard rebuild adds any new default settings from future updates and leaves your changes alone.

    Or in VS Code: **File → Open Folder…** → `case-work`.

    **What `code .` does:** Opens the project folder with the settings in `.vscode/settings.json` applied.

2. When VS Code asks **"Do you trust the authors of the files in this folder?"**, choose **Yes, I trust the authors**. Tasks, Run on Save and the Python interpreter are disabled in Restricted Mode.

3. Create your local config from the example:

    ```bash
    cp .env.example .env
    ```

    **What it does:** `.env` holds your personal settings (Jira URL/token, view toggles). It is gitignored, so your values never get committed. Leave the Jira values as-is if you don't use the [Jira reminders](guide.md#jira-reminders).

4. Confirm Foam found the templates: `Cmd+Shift+P` → **Foam: Create New Note From Template**.

    **Success looks like:** The list shows New Case, KB Article, PKB Note and the three meeting templates. Press `Esc` to close it without creating a note.

    When you do create a note, Foam asks for a title with the placeholder *Title of my New Note* (Foam's built-in text, which can't be changed). What you type becomes the file name:

    | Template | Type at the title prompt |
    | -------- | ------------------------ |
    | New Case | The case number, e.g. `00123456` |
    | PKB Note / KB Article | A short name, e.g. `ldap-auth-troubleshooting` |
    | Meetings | Anything. The file is named by today's date |

5. Optional: set your PKB tabs in `pkb-categories.yaml` now. See [Guide → Customizing PKB Tabs](guide.md#customizing-pkb-tabs).

!!! tip "Reopening later"
    Use **File → Open Recent** → `~/case-work`, or run `code ~/case-work`. Open the `case-work` folder itself, not its parent or a subfolder, or the settings, tasks and on-save hooks won't load.

### 9. Verify Everything Works

1. `Ctrl+Shift+P` → **Tasks: Run Task** → **🟢 Start Zensical**. It builds the dashboards first, then starts the local site and prints a URL like `http://127.0.0.1:8000`. Leave this terminal running.
2. Open that URL in your browser. You should see the case tracker home page, and the Dashboard, Meetings, Knowledge Base and Tags pages should all load.
3. `Ctrl+Shift+B` (**Rebuild Dashboards**) should finish with `Done.` in the terminal. The open site picks up the change and reloads by itself.

!!! warning "Don't start the site with `zensical serve` on a new clone"
    The Dashboard, Meetings, Knowledge Base and Tags pages are generated from your notes, so they don't exist until the dashboards are built once. Running `zensical serve` by hand first gives broken links and 404s. The **🟢 Start Zensical** task handles this for you.

To check the same things from a terminal at the `case-work/` root (no activation needed):

```bash
.venv/bin/python3 scripts/dashboard.py
.venv/bin/zensical build
```

**What they do:** The first regenerates the dashboards, Knowledge Base tabs and tags page from your notes. The second builds the full site into `site/`.

**Success looks like:** The first ends with `Done.`; the second prints `No issues found` and `Build finished`.

!!! tip "Using the Reminders sync?"
    macOS asks once for permission before VS Code can add reminders. See [Guide → Reminders Sync](guide.md#reminders-sync) to trigger the prompt and test it.

!!! tip "Virtual environment tip"
    Never install Zensical or project packages globally with `sudo pip`. Always install inside `.venv` so nothing conflicts with system Python.

---

## 🔄 Upgrading

!!! tip "One command"
    `./install.sh --upgrade` from the `case-work/` root upgrades Zensical and the VS Code extensions, and repairs anything missing. The sections below cover upgrading each piece by hand.

### Homebrew

Update Homebrew itself and all installed formulae:

```bash
brew update && brew upgrade
```

Clean up old versions afterward:

```bash
brew cleanup
```

### Python

Upgrade to the latest Homebrew Python:

```bash
brew upgrade python
```

!!! warning "After upgrading Python"
    The `.venv` virtual environment is tied to the Python version it was created with. After a Python upgrade, rebuild the venv:
    ```bash
    rm -rf .venv
    /opt/homebrew/bin/python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    deactivate
    ```
    Then re-point VS Code: `Ctrl+Shift+P` → **Python: Select Interpreter** → `.venv/bin/python3`.

### Zensical

Upgrade Zensical inside the project virtual environment:

```bash
.venv/bin/pip install --upgrade -r requirements.txt
```

No need to activate the venv first — the full path is enough.

### VS Code

VS Code checks for updates automatically. To trigger a manual check:

`Help` menu → **Check for Updates**

### Foam Extension

`Cmd+Shift+X` → search `foam.foam-vscode` → click **Update** if available.

Or update all extensions at once:

`Cmd+Shift+X` → **...** (top-right menu) → **Update All Extensions**

---

## Troubleshooting

### `pip install` fails, or `.venv` looks broken

**Cause:** The `.venv` was built on the wrong Python (usually Apple's 3.9.x from the Command Line Tools), or it was restored from a backup/older machine. A venv is tied to the Python that created it.

**Check:**

```bash
cat .venv/pyvenv.cfg
```

If `home` is not `/opt/homebrew/...`, rebuild it. `.venv` is gitignored, so nothing is lost:

```bash
rm -rf .venv
/opt/homebrew/bin/python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/zensical --version
```

**Success looks like:** A version number prints. Then re-select the interpreter in VS Code (`Ctrl+Shift+P` → **Python: Select Interpreter** → `.venv/bin/python3`).

### `git pull` says local changes to `.vscode/settings.json` would be overwritten

**Cause:** Clones made before `settings.json` became a personal, gitignored file still have it tracked. Any change from VS Code or the Toggle File Visibility task blocks the pull.

**Fix** (run from the `case-work/` root; it keeps your current settings):

```bash
cp .vscode/settings.json /tmp/my-vscode-settings.json
git checkout -- .vscode/settings.json
git pull
cp /tmp/my-vscode-settings.json .vscode/settings.json
.venv/bin/python3 scripts/sync_settings.py
```

**Success looks like:** `git pull` finishes, and `git status` no longer lists `.vscode/settings.json`, now or after future changes.
