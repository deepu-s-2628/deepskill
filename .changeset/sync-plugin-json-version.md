---
"deepskill": patch
---

Fixed a real version-drift bug: `changeset version` only bumps `package.json`, which left `.claude-plugin/plugin.json` — the manifest that actually matters for the installed plugin — stuck at `0.1.0` after the `0.2.0` release merged. Added `scripts/sync-plugin-version.mjs` and wired it into the `version` npm script so both manifests move together on every future release.
