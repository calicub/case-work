#!/usr/bin/env bash
# Case Work installer for macOS.
#
# Installs what's missing (Homebrew Python, VS Code, extensions), builds the
# project's Python environment, creates your local config, builds the site and
# opens the project in VS Code. Safe to run again at any time; finished steps are skipped.
#
# Usage:
#   ./install.sh              install / repair
#   ./install.sh --upgrade    also upgrade Zensical and the VS Code extensions
#   ./install.sh --yes        don't ask before installing anything
#   ./install.sh --no-open    don't open VS Code at the end

set -euo pipefail

REPO="$(cd "$(dirname "$0")" && pwd)"
cd "$REPO"

EXTENSIONS=(foam.foam-vscode ms-python.python emeraldwalk.RunOnSave)
UPGRADE=false
ASSUME_YES=false
OPEN=true

for arg in "$@"; do
  case "$arg" in
    --upgrade) UPGRADE=true ;;
    --yes|-y)  ASSUME_YES=true ;;
    --no-open) OPEN=false ;;
    -h|--help) sed -n '2,13p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "Unknown option: $arg (see ./install.sh --help)"; exit 2 ;;
  esac
done

# ---------- output helpers ----------
if [[ -t 1 ]]; then B=$'\033[1m'; G=$'\033[32m'; Y=$'\033[33m'; R=$'\033[31m'; N=$'\033[0m'; else B= G= Y= R= N=; fi
step() { printf '\n%s==> %s%s\n' "$B" "$1" "$N"; }
ok()   { printf '  %s✓%s %s\n' "$G" "$N" "$1"; }
warn() { printf '  %s!%s %s\n' "$Y" "$N" "$1"; }
fail() { printf '\n%s✗ %s%s\n' "$R" "$1" "$N" >&2; exit 1; }
confirm() {
  $ASSUME_YES && return 0
  local reply
  read -r -p "  $1 [Y/n] " reply
  [[ -z "$reply" || "$reply" =~ ^[Yy] ]]
}

# ---------- 1. macOS ----------
step "Checking system"
[[ "$(uname)" == "Darwin" ]] || fail "This installer is for macOS. See docs/setup.md for the manual steps."
ok "macOS $(sw_vers -productVersion) ($(uname -m))"

# ---------- 2. Homebrew ----------
step "Homebrew"
if ! command -v brew >/dev/null 2>&1; then
  for p in /opt/homebrew/bin/brew /usr/local/bin/brew; do
    [[ -x "$p" ]] && eval "$("$p" shellenv)" && break
  done
fi
if ! command -v brew >/dev/null 2>&1; then
  warn "Homebrew is not installed."
  confirm "Install Homebrew now? (asks for your Mac password)" || fail "Homebrew is required. Install it from https://brew.sh and run this script again."
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  for p in /opt/homebrew/bin/brew /usr/local/bin/brew; do
    [[ -x "$p" ]] && eval "$("$p" shellenv)" && break
  done
  command -v brew >/dev/null 2>&1 || fail "Homebrew installed, but 'brew' isn't on PATH. Open a new terminal and run this script again."
fi
BREW_PREFIX="$(brew --prefix)"
ok "Homebrew at $BREW_PREFIX"

# Make sure new terminals find Homebrew (and its Python) first.
if ! grep -qs 'brew shellenv' "$HOME/.zprofile" "$HOME/.zshrc"; then
  if confirm "Add Homebrew to your shell startup (~/.zprofile) so new terminals use it?"; then
    printf '\neval "$(%s/bin/brew shellenv)"\n' "$BREW_PREFIX" >> "$HOME/.zprofile"
    ok "Added Homebrew to ~/.zprofile"
  else
    warn "Skipped. New terminals may use macOS's old built-in Python."
  fi
else
  ok "Shell startup already loads Homebrew"
fi

# ---------- 3. Python ----------
step "Python"
PY="$BREW_PREFIX/bin/python3"
if [[ ! -x "$PY" ]]; then
  confirm "Install Python with Homebrew?" || fail "Homebrew Python is required."
  brew install python
fi
ok "$("$PY" --version) at $PY"

# ---------- 4. VS Code ----------
step "VS Code"
CODE=""
if command -v code >/dev/null 2>&1; then
  CODE="$(command -v code)"
elif [[ -x "/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code" ]]; then
  CODE="/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code"
else
  if confirm "Install VS Code with Homebrew?"; then
    brew install --cask visual-studio-code
    CODE="$(command -v code || echo "/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code")"
  fi
fi
if [[ -n "$CODE" && -x "$CODE" ]]; then
  ok "VS Code command at $CODE"
  for ext in "${EXTENSIONS[@]}"; do
    if $UPGRADE; then
      "$CODE" --install-extension "$ext" --force >/dev/null 2>&1 && ok "Extension $ext (updated)" || warn "Couldn't install $ext; install it from the Extensions view"
    else
      "$CODE" --install-extension "$ext" >/dev/null 2>&1 && ok "Extension $ext" || warn "Couldn't install $ext; install it from the Extensions view"
    fi
  done
  # VS Code only reads keyboard shortcuts from user settings, so add ours there.
  if confirm "Add the Ctrl+Shift+; shortcut (Append Terminal Block) to your VS Code keyboard shortcuts?"; then
    "$PY" scripts/install_keybindings.py | sed 's/^  /  ✓ /' || warn "Couldn't add the shortcut; see 'Append Terminal Block' in docs/guide.md to add it by hand"
  else
    warn "Skipped keyboard shortcut. Run the 📌 Append Terminal Block task from Cmd+Shift+P instead"
  fi
else
  warn "VS Code not found. Install it from https://code.visualstudio.com, then run this script again."
fi

# ---------- 5. Project Python environment ----------
step "Project environment (.venv)"
if [[ -x .venv/bin/python3 ]]; then
  VENV_HOME="$(sed -n 's/^home = //p' .venv/pyvenv.cfg 2>/dev/null)"
  if [[ "$VENV_HOME" != "$BREW_PREFIX"* ]] || ! .venv/bin/python3 -c '' 2>/dev/null; then
    warn ".venv was built on a different Python ($VENV_HOME); rebuilding it"
    rm -rf .venv
  fi
fi
if [[ ! -x .venv/bin/python3 ]]; then
  "$PY" -m venv .venv
  ok "Created .venv"
else
  ok ".venv already exists"
fi
PIP_ARGS=(-q install -r requirements.txt)
$UPGRADE && PIP_ARGS=(-q install --upgrade -r requirements.txt)
.venv/bin/python3 -m pip "${PIP_ARGS[@]}" --disable-pip-version-check
ok "$(.venv/bin/zensical --version 2>/dev/null | head -1 | sed 's/^/Zensical /')"

# ---------- 6. Local config ----------
step "Local config"
if [[ -f .env ]]; then
  ok ".env already exists (left unchanged)"
else
  cp .env.example .env
  ok "Created .env from .env.example (add Jira details later if you use it)"
fi
.venv/bin/python3 scripts/sync_settings.py | sed 's/^  /  ✓ /'

# ---------- 7. Build ----------
step "Building the site"
.venv/bin/python3 scripts/dashboard.py >/dev/null
ok "Dashboards, Knowledge Base and Tags pages generated"
if .venv/bin/zensical build >/tmp/case-work-build.log 2>&1; then
  ok "Site builds cleanly"
else
  warn "Site build reported problems; see /tmp/case-work-build.log"
fi

# ---------- Done ----------
step "Done"
cat <<EOF
  Next, in VS Code:
    1. Click "Yes, I trust the authors" when asked.
    2. Cmd+Shift+P → Tasks: Run Task → 🟢 Start Zensical, then open http://127.0.0.1:8000
    3. Cmd+Shift+P → Foam: Create New Note From Template to start a note.

  Using the Reminders sync? Open a case note and run the
  🔔 Sync Reminders Now task once, then click Allow when macOS asks.

  Full guide: docs/setup.md · Run ./install.sh --upgrade later to update.
EOF

if $OPEN && [[ -n "$CODE" && -x "$CODE" ]]; then
  "$CODE" "$REPO"
fi
