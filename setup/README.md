# setup/

**Looking for setup instructions?** They're in [docs/setup.md](../docs/setup.md).

This folder holds the optional Jira reminders schedule, a macOS launchd job installed by the **⏰ Install Jira Reminders Schedule** task:

| File | Purpose |
| ---- | ------- |
| `install_schedule.sh` | Installs or reinstalls the schedule |
| `com.casework.jira-reminders.plist` | The launchd job template (the installer fills in the repo path) |

See [Jira Reminders](../docs/guide.md#jira-reminders) in the guide.
