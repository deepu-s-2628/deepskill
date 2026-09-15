---
"deepskill": patch
---

README: add migration guidance for anyone who already installed `ask-deepu`/the pipeline skills via `npx skills` before this native-plugin fix shipped. Confirmed empirically: an old flattened `npx skills`-installed skill takes precedence over the new native plugin for a bare `/ask-deepu`, silently reproducing the exact failure this release fixes. Documents the `npx skills@latest remove ... -g -y` cleanup command (verified against the real skill list) and the `/deepskill:ask-deepu` namespaced-invocation fallback for anyone who'd rather not remove anything yet.
