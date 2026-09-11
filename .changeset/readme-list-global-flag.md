---
"deepskill": patch
---

Fixed the README's `skills list` documentation — it only showed the bare command, which defaults to project scope and reports "No project skills found" for a global install (reproduced live: `npx skills@latest list` after a `-g` install says exactly this and suggests `-g`). Now documents both forms, matching how `update` already documents `-p`/`-g`. Also updated the `update` section's skill list, which was stale since `design-taste` and `unlazy-gates` were vendored.
