---
"deepskill": patch
---

Fixed the README's "Status" line, which still said `v0.2.0` after `v0.3.0` had already shipped — merging a "Version Packages" PR bumps `package.json`/`plugin.json` but never touches prose elsewhere that names the version. Added the missing `v0.3.0` Roadmap entry, and removed the hardcoded version number from the Status line entirely (points at `.claude-plugin/plugin.json`/`CHANGELOG.md` instead), so this can't silently drift again on the next release.
