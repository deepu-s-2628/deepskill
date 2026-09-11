---
"deepskill": patch
---

Added an "Updating an existing install" section to the README — the install docs previously only covered a fresh `add`, with no mention of the `skills` CLI's dedicated `update` command (verified against the real CLI: it tracks each installed skill's source and re-fetches from there, so `update` is the right command, not re-running `add`). Also documented `skills list` for checking what's currently installed.
