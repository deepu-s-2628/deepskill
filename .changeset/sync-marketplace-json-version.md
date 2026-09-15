---
"deepskill": patch
---

Fix `scripts/sync-plugin-version.mjs` only syncing `.claude-plugin/plugin.json`'s version from `package.json`, leaving the newly-added `.claude-plugin/marketplace.json` to drift stale after every release (caught immediately after the previous release: `marketplace.json` stayed at `0.8.1` while `package.json`/`plugin.json` moved to `0.8.2`). Now syncs both manifests.
