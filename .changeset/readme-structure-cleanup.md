---
"deepskill": patch
---

README cleanup after a full repo audit (no stale files or orphaned skills found — `plugin.json`'s skill list matches the on-disk tree exactly in both directions, versions consistent across `package.json`/`plugin.json`, no open PRs, no stray branches). Two real fixes: the Roadmap section was a hand-maintained history of every shipped change through `v0.9.0`, fully duplicating what `CHANGELOG.md` already does better and more accurately — trimmed to only the still-unshipped "Planned" items, with a pointer to `CHANGELOG.md` for real history. Added a "Repository structure" section showing the actual repo layout (distinct from the existing topic-folder output structure under "Getting started"), verified against the tracked file list rather than reconstructed from memory.
