#!/usr/bin/env bash
# Parses ## 🔔 Next Action from a case note and syncs tasks to macOS Reminders.
# Only processes files in docs/cases/active/ or docs/cases/followup/.
# Archive is intentionally excluded — never process it.
#
# Due date syntax (appended to task text):
#   @M/D          — due on that date at 08:00
#   @M/D-HH:MM    — due on that date at that time (24-hour)
# Example: - [ ] Call customer @5/15-14:30

FILE="$1"

[[ -z "$FILE" || ! -f "$FILE" ]] && exit 0

# Accept relative paths when run by hand
FILE="$(cd "$(dirname "$FILE")" && pwd)/$(basename "$FILE")"

# Run osascript, and explain the common failure instead of failing silently.
run_osascript() {
  local out err status errfile
  errfile=$(mktemp)
  out=$(osascript 2>"$errfile")
  status=$?
  err=$(cat "$errfile"); rm -f "$errfile"
  if [[ $status -ne 0 ]]; then
    echo "Reminders sync failed: $err" >&2
    if [[ "$err" == *"-1743"* || "$err" == *"Not authorized"* ]]; then
      echo "macOS blocked access to Reminders. Allow it in System Settings → Privacy & Security → Automation (Visual Studio Code → Reminders), then save the note again." >&2
    fi
    exit 1
  fi
  printf '%s' "$out"
}

# Guard: only active and followup
if [[ "$FILE" != */docs/cases/active/* && "$FILE" != */docs/cases/followup/* ]]; then
  exit 0
fi

# Extract case number from frontmatter
CASE_NUM=$(grep -m1 '^case_number:' "$FILE" | sed 's/case_number:[[:space:]]*//')
[[ -z "$CASE_NUM" ]] && exit 0

CURRENT_YEAR=$(date +%Y)
LIST_NAME="Case Actions"

# Reverse sync: if a reminder for this case was completed in Reminders, mark it done in the note first.
completed_tasks=$(run_osascript << OSEOF
tell application "Reminders"
  if not (exists list "$LIST_NAME") then return ""
  set caseList to list "$LIST_NAME"
  set output to ""
  set prefix to "[$CASE_NUM] "
  repeat with r in (reminders of caseList whose completed is true)
    set n to name of r
    if n starts with prefix then
      set taskName to text ((length of prefix) + 1) thru -1 of n
      set output to output & taskName & "\n"
    end if
  end repeat
  return output
end tell
OSEOF
) || exit 1

if [[ -n "$completed_tasks" ]]; then
  while IFS= read -r task; do
    [[ -z "$task" ]] && continue
    # Match open checkbox lines whose text starts with this task name (ignoring trailing date annotations)
    escaped=$(printf '%s\n' "$task" | sed 's/[][\.*^$(){}/|+?]/\\&/g')
    sed -i '' "s/^\\([[:space:]]*\\)- \\[ \\] \\(${escaped}\\)/\1- [x] \2/" "$FILE"
  done <<< "$completed_tasks"
fi

# Parse ## 🔔 Next Action section (after reverse-sync edits above)
IN_SECTION=0
OPEN_TASKS=()
OPEN_DATES=()
DONE_TASKS=()

while IFS= read -r line; do
  if [[ "$line" =~ ^[[:space:]]*##[[:space:]].*(🔔|▶).*Next[[:space:]]Action ]]; then
    IN_SECTION=1
    continue
  fi
  if [[ $IN_SECTION -eq 1 ]]; then
    [[ "$line" =~ ^[[:space:]]*## ]] && break

    if [[ "$line" =~ ^[[:space:]]*-[[:space:]]\[[[:space:]]\][[:space:]](.+) ]]; then
      raw="${BASH_REMATCH[1]%"${BASH_REMATCH[1]##*[![:space:]]}"}"
      due=""
      if [[ "$raw" =~ @([0-9]{1,2}/[0-9]{1,2}-[0-9]{1,2}:[0-9]{2}) ]]; then
        due="${BASH_REMATCH[1]}"
        raw="${raw/@$due/}"
      elif [[ "$raw" =~ @([0-9]{1,2}/[0-9]{1,2}) ]]; then
        due="${BASH_REMATCH[1]}"
        raw="${raw/@$due/}"
      fi
      raw="${raw%"${raw##*[![:space:]]}"}"
      OPEN_TASKS+=("$raw")
      OPEN_DATES+=("$due")

    elif [[ "$line" =~ ^[[:space:]]*-[[:space:]]\[[xX]\][[:space:]](.+) ]]; then
      raw="${BASH_REMATCH[1]%"${BASH_REMATCH[1]##*[![:space:]]}"}"
      if [[ "$raw" =~ @([0-9]{1,2}/[0-9]{1,2}-[0-9]{1,2}:[0-9]{2}) ]]; then
        raw="${raw/@${BASH_REMATCH[1]}/}"
      elif [[ "$raw" =~ @([0-9]{1,2}/[0-9]{1,2}) ]]; then
        raw="${raw/@${BASH_REMATCH[1]}/}"
      fi
      raw="${raw%"${raw##*[![:space:]]}"}"
      DONE_TASKS+=("$raw")
    fi
  fi
done < "$FILE"

[[ ${#OPEN_TASKS[@]} -eq 0 && ${#DONE_TASKS[@]} -eq 0 ]] && exit 0

# make_date_as <due_str>
# Outputs AppleScript lines that set variable `dueDate` from a M/D or M/D-HH:MM string.
make_date_as() {
  local due="$1"
  local month day hour minute
  if [[ "$due" =~ ^([0-9]{1,2})/([0-9]{1,2})-([0-9]{1,2}):([0-9]{2})$ ]]; then
    month="${BASH_REMATCH[1]}"
    day="${BASH_REMATCH[2]}"
    hour="${BASH_REMATCH[3]}"
    minute="${BASH_REMATCH[4]}"
  elif [[ "$due" =~ ^([0-9]{1,2})/([0-9]{1,2})$ ]]; then
    month="${BASH_REMATCH[1]}"
    day="${BASH_REMATCH[2]}"
    local seconds=$(( 0 ))
    printf '    set dueDate to current date\n'
    printf '    set year of dueDate to %s\n' "$CURRENT_YEAR"
    printf '    set month of dueDate to %s\n' "$month"
    printf '    set day of dueDate to %s\n' "$day"
    return
  else
    echo ""
    return
  fi
  local seconds=$(( hour * 3600 + minute * 60 ))
  printf '    set dueDate to current date\n'
  printf '    set year of dueDate to %s\n' "$CURRENT_YEAR"
  printf '    set month of dueDate to %s\n' "$month"
  printf '    set day of dueDate to %s\n' "$day"
  printf '    set time of dueDate to %s\n' "$seconds"
  return
}

# Build AppleScript
{
  echo "tell application \"Reminders\""
  echo "  if not (exists list \"$LIST_NAME\") then"
  echo "    make new list with properties {name:\"$LIST_NAME\"}"
  echo "  end if"
  echo "  set caseList to list \"$LIST_NAME\""

  for i in "${!OPEN_TASKS[@]}"; do
    task="${OPEN_TASKS[$i]}"
    due="${OPEN_DATES[$i]}"
    title="[$CASE_NUM] $task"
    title="${title//\\/\\\\}"
    title="${title//\"/\\\"}"

    echo "  set t to \"$title\""
    echo "  set taskExists to false"
    echo "  repeat with r in (reminders of caseList)"
    echo "    if name of r is t then set taskExists to true"
    echo "  end repeat"
    echo "  if not taskExists then"

    date_as=$(make_date_as "$due")
    if [[ -n "$date_as" ]]; then
      echo "$date_as"
      echo "    make new reminder in caseList with properties {name:t, completed:false, due date:dueDate}"
    else
      echo "    make new reminder in caseList with properties {name:t, completed:false}"
    fi

    echo "  end if"
  done

  for task in "${DONE_TASKS[@]}"; do
    title="[$CASE_NUM] $task"
    title="${title//\\/\\\\}"
    title="${title//\"/\\\"}"
    echo "  set t to \"$title\""
    echo "  repeat with r in (reminders of caseList)"
    echo "    if name of r is t then set completed of r to true"
    echo "  end repeat"
  done

  echo "end tell"
} | run_osascript
