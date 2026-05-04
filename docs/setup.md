---
icon: lucide/wrench
---

# 🚀 Setup & Upgrades

---

## 🚀 Initial Setup (New Machine)

Step-by-step setup for a fresh macOS install.

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

Verify:

```bash
python3 --version
```

!!! note "System Python"
    macOS ships with a very old Python. Always use the Homebrew-installed `python3`.

### 3. Install VS Code

Download from [code.visualstudio.com](https://code.visualstudio.com) and drag it to Applications.

Then install the `code` shell command so you can open projects from the terminal:

`Cmd+Shift+P` → **Shell Command: Install 'code' command in PATH**

Install the **Foam** extension:

`Cmd+Shift+X` → search `foam.foam-vscode` → Install

### 4. Clone / Copy the Workspace

```bash
# If starting from a git repo:
git clone <repo-url> ~/case-work

# Or copy your existing workspace folder to ~/case-work
```

Open the workspace in VS Code:

```bash
code ~/case-work
```

### 5. Create the Python Virtual Environment

Run these commands from the `case-work/` root:

```bash
python3 -m venv .venv
```

Activate it (you only need this for manual terminal use — tasks run it automatically):

```bash
source .venv/bin/activate
```

### 6. Install Zensical

With the virtual environment active:

```bash
pip install zensical
```

Verify:

```bash
zensical --version
```

Deactivate when done:

```bash
deactivate
```

### 7. Set the VS Code Python Interpreter

`Ctrl+Shift+P` → **Python: Select Interpreter** → choose `.venv/bin/python3` (it will show the workspace `.venv` path).

This ensures all tasks and scripts use the project virtual environment automatically.

### 8. Verify Everything Works

1. `Ctrl+Shift+P` → Run Task → **📙 Zensical** — should print a URL like `http://127.0.0.1:8000`
2. Open that URL in your browser — you should see the case tracker home page
3. `Ctrl+Shift+B` — should rebuild dashboards with no errors in the terminal panel

!!! tip "Virtual environment tip"
    Never install Zensical or project packages globally with `sudo pip`. Always install inside `.venv` so nothing conflicts with system Python.

---

## 🔄 Upgrading

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
    python3 -m venv .venv
    source .venv/bin/activate
    pip install zensical
    deactivate
    ```
    Then re-point VS Code: `Ctrl+Shift+P` → **Python: Select Interpreter** → `.venv/bin/python3`.

### Zensical

Upgrade Zensical inside the project virtual environment:

```bash
.venv/bin/pip install --upgrade zensical
```

No need to activate the venv first — the full path is enough.

### VS Code

VS Code checks for updates automatically. To trigger a manual check:

`Help` menu → **Check for Updates**

### Foam Extension

`Cmd+Shift+X` → search `foam.foam-vscode` → click **Update** if available.

Or update all extensions at once:

`Cmd+Shift+X` → **...** (top-right menu) → **Update All Extensions**
