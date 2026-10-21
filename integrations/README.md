# integrations/

**Looking for setup instructions?** They're in [docs/setup.md](../docs/setup.md).

This folder holds the setup scripts and configuration for optional integrations with other tools. None of them are needed for the core case tracker.

| File | Integration | Purpose |
| ---- | ----------- | ------- |
| `install_schedule.sh` | Jira reminders | Installs or reinstalls the schedule (run via the **⏰ Install Jira Reminders Schedule** task) |
| `com.casework.jira-reminders.plist` | Jira reminders | macOS launchd job template (the installer fills in the repo path) |

See [Jira Reminders](../docs/guide.md#jira-reminders) in the guide.

## Adding an integration

Put its setup scripts and config templates here, add a row to the table above, and document it in `docs/guide.md`. Keep secrets out of this folder: read them from `.env`, which is gitignored. If an integration grows past a couple of files, give it its own subfolder (e.g. `integrations/<name>/`).
