---
"deepskill": minor
---

Milestone 3: `unlazy-gates` for the pipeline's Quality Gate checklists.

Vendored a curated, **Solo-mode-only** slice of `unlazy` (v2.1.0, MIT, Leonxlnx) at `skills/unlazy-gates/` — `gate-check.mjs`/`gate-lint.mjs` and their dependencies, a simplified Solo template (`OWNS`/`CWD` dropped, since concurrent-writer coordination never applies to a single continuous sequential session), and the full gate-authoring reference. Deliberately excluded: the Depth Tree, `PLAN.md`, orchestrated/parallel dispatch machinery, and the optional Stop hook — none of it fits this pipeline, and the Stop hook specifically would block a session on unmet gates, which contradicts the never-pause contract below.

Translated each of the 14 pipeline skills' existing "Quality Gate" checklists into a real `.steps/GATES-N.md` ledger: mechanically-checkable items (a persona-story count, a placeholder-text scan, a file existing, `Progress.md` actually updated) become runnable `CHECK:`/`EXPECT:` gates; genuine judgment calls ("plain English," "specific, not generic") stay explicit manual gates, self-attested exactly as they already were. Verified with real traces, not assumed: a runnable gate failing then passing after self-correction, a manual gate correctly carrying no script, and the placeholder-scan gate across a realistic 4-file Step-5 draft set.

**The resolution rule is this repo's own addition, not `unlazy`'s native behavior**: `unlazy`'s own unsatisfiable-gate path is `ABANDON`, which halts with `HANDOFF REQUIRED` — built for a human-supervised session. This pipeline has exactly two sanctioned pause points (wayfinding, the Step 6 opt-in choice); a quality gate is neither. A failing runnable gate gets 2–3 self-correction retries; still-unmet after that gets documented as a stated gap in the step's own output (the same pattern already used for an unavailable screenshot) and the run continues — never abandoned, never paused. Documented in full as `context/pm-operating-system.md` §18.

Also fixed, found while sweeping for consistency: `design-taste` and `unlazy-gates` were both missing from the README's Utilities table despite being vendored the same way as Archify/frontend-slides — an incomplete "vendored in full" listing is exactly the staleness class this repo keeps getting caught by.
