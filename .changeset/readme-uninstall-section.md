---
"deepskill": patch
---

Added an "Uninstalling" section to the README — there was no documented removal path before, only install/update. `npx skills` has no single "remove everything from this source" flag, so the command names all 22 skills in this package explicitly (verified count, directly from `.claude-plugin/plugin.json` — this repo ships 22 skills, not the 21 stated in earlier session conversation and the separate `deepskill-learning` docs, both of which will be corrected separately). Also documents the interactive picker (`remove` with no arguments) and flags `--all` as removing every installed skill regardless of source, not scoped to this package.
