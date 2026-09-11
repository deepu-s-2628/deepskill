# deepskill

## 0.4.0

### Minor Changes

- [`0abc4b6`](https://github.com/deepu-s-2628/deepskill/commit/0abc4b685d563513da5064263a0b66899c9e4aa4) Thanks [@deepu-s-2628](https://github.com/deepu-s-2628)! - Milestone 1 of the design-taste/unlazy roadmap: vendored a curated, rewritten-for-this-repo adaptation of [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill)'s stack-agnostic design judgment at `skills/design-taste/`, and applied it to `analysis.html`'s styling via `build_report.py`.

  This is a curated extraction, not a copy — the source skill's own scope note says it explicitly ("NOT for dashboards / dense product UI," which is exactly what a PM analysis report is), and most of its ~1,200 lines are React/Next.js/Motion/npm-component-library machinery or landing-page structure (heroes, bento grids, marquees) that doesn't fit this repo's zero-build-step static-HTML deliverables. What transferred: color restraint, typographic hierarchy, shape/spacing consistency, and the discipline of naming generic-AI defaults instead of drifting into them.

  Concretely, `analysis.html` now uses: one accent color held identically everywhere (ManageEngine brand blue `#0078d4`, already this repo's documented brand color, replacing a generic Tailwind-blue default); a documented two-tier corner-radius scale (was an unplanned 4/6/10px mix); row-separator tables with an accent header rule instead of a full boxed grid with zebra striping (the single most common "AI spec sheet" tell, and the highest-leverage fix given how table-heavy these reports are); a readable ~75ch measure for prose paragraphs while tables and diagrams keep the full 1400px width; and real `:focus-visible` states, previously entirely absent.

  Deliberately kept the system-font stack rather than following the source skill's webfont recommendation (Geist/Outfit/Satoshi) — this repo's HTML must render correctly with zero external network calls, the same constraint that keeps Archify and frontend-slides dependency-free.

- [`a15823d`](https://github.com/deepu-s-2628/deepskill/commit/a15823d7b75c730145ab0d7f379d63b3e132a416) Thanks [@deepu-s-2628](https://github.com/deepu-s-2628)! - Token/file-discipline pass, grilled and verified before implementing (not just a size cleanup):

  **Fixed a real correctness bug found along the way.** `deliverables/SKILL.md` and `enhancement-deliverables/SKILL.md` still instructed the model to design slides around `python-pptx`/`PresentationBuilder` method names (`add_kpi_slide()`, `add_icon_grid_slide()`, etc.) from `generate_pptx.py` — deleted two releases ago when this pipeline moved to frontend-slides. This almost certainly contributed to the earlier "slides are too thin" feedback: the design-notes sections were still steering toward a rigid PPTX function-call model instead of genuine frontend-slides authoring. Rewrote both files' layout-variety guidance in the same content-shape vocabulary `generate-documents`/`enhancement-generate-documents` already use (two-column, comparison matrix, icon grid, KPI cards, before/after panels — described as layouts, not API calls). Also fixed a second bug found in the same pass: existing/new/modified color-coding (an enhancement-only concept) had leaked into the _feature_ pipeline's engineering-deck instructions via copy-paste — removed, since a net-new feature has nothing "existing" to color-code against.

  **Deduped the "Report rebuild" boilerplate.** The same ~19-line procedure was copy-pasted verbatim across all 14 pipeline skills (~266 lines of pure redundancy), duplicating what `pm-operating-system.md` §6 already documents once — and which every step already loads as mandatory context regardless. Replaced with a one-paragraph pointer in each file.

  **Verified the two largest files (`deliverables`, `enhancement-deliverables`, the two biggest `SKILL.md` files installed on this machine) should NOT be split into on-demand references.** Confirmed their four deliverable templates (5a-5d) are unconditionally read in the same Step 5 pass with no cross-template dependencies — splitting a file whose every branch always fires adds tool-call overhead with no token savings (the opposite of what progressive disclosure is for). Left whole; fixed the real defects inside them instead.

  **Added `pm-operating-system.md` §17** codifying this as a standing authoring convention for future skills: don't duplicate what's already mandatory context, only split content that's genuinely conditional, scope directory reads narrowly (matching Archify's own `SKILL.md` discipline), and verify a referenced file/method/format still exists rather than trusting prose that merely reads plausibly.

### Patch Changes

- [`5b5dc58`](https://github.com/deepu-s-2628/deepskill/commit/5b5dc5846782288970e3b6c5e1c5d4947a24e1f2) Thanks [@deepu-s-2628](https://github.com/deepu-s-2628)! - Aligned `md_to_html.py`'s fallback-render CSS with `build_report.py`'s new design-taste styling (milestone 1) — same brand-blue accent, row-separator tables, focus states, and radius scale. This path only runs when `build_report.py` itself is unavailable, but it was left visibly inconsistent (old generic Tailwind blue) after milestone 1 landed.

- [`9f4628b`](https://github.com/deepu-s-2628/deepskill/commit/9f4628b9ee243b15153241b4e1b46fa9bb468d1f) Thanks [@deepu-s-2628](https://github.com/deepu-s-2628)! - Fixed the README's "Status" line, which still said `v0.2.0` after `v0.3.0` had already shipped — merging a "Version Packages" PR bumps `package.json`/`plugin.json` but never touches prose elsewhere that names the version. Added the missing `v0.3.0` Roadmap entry, and removed the hardcoded version number from the Status line entirely (points at `.claude-plugin/plugin.json`/`CHANGELOG.md` instead), so this can't silently drift again on the next release.

- [`1373cb0`](https://github.com/deepu-s-2628/deepskill/commit/1373cb07540393c4d21e6dcf9800daab0b731379) Thanks [@deepu-s-2628](https://github.com/deepu-s-2628)! - Added an "Updating an existing install" section to the README — the install docs previously only covered a fresh `add`, with no mention of the `skills` CLI's dedicated `update` command (verified against the real CLI: it tracks each installed skill's source and re-fetches from there, so `update` is the right command, not re-running `add`). Also documented `skills list` for checking what's currently installed.

## 0.3.0

### Minor Changes

- [`0ae2157`](https://github.com/deepu-s-2628/deepskill/commit/0ae2157ddfae774c058c99b7d47e7a74e83c36a6) Thanks [@deepu-s-2628](https://github.com/deepu-s-2628)! - Second round of real-usage feedback (Firewall Analyzer IP-reputation test run), all implemented:

  **Filenames.** Deliverables are now named for their role, not the slug — `analysis.html`, `architecture.html`, `executive-brief.html`, `engineering-brief.html`, `product-requirements.docx` — the same names in every topic folder, so it's always obvious which to open first. `STATUS.md` is renamed to `Progress.md` (still visible at the topic-folder root).

  **PRD (DOCX).** Author metadata now defaults to "Deepu S" instead of a `[PM Name]` placeholder. The Table of Contents is no longer a Word field that needs a manual "right-click → Update Field" — every heading is bookmarked as it's written and the TOC is filled in with real internal hyperlinks at save time, so it's correct and clickable the moment the file opens. Every major section now opens with a short plain-language intro paragraph instead of jumping straight into tables.

  **Consolidated report (`analysis.html`).** The left nav is now nested — each step's own subsections appear underneath it — with scroll-position highlighting showing which section you're currently reading. The main content column is wider (1400px cap, was 980px). The wayfinding step is renamed "Scope & Requirements" in both the report heading and the nav, and its locked decisions render as a table instead of prose sub-headings.

  **Slide decks.** Both decks now ship full keyboard/mouse-wheel/on-screen navigation (frontend-slides' own template contract, previously not enforced by our instructions) and target frontend-slides' "high density / reading-first" mode (4-8 bullets/cards per slide) instead of its sparse speaker-led default, which is what produced thin one-line slides in testing.

### Patch Changes

- [`cdcdb8d`](https://github.com/deepu-s-2628/deepskill/commit/cdcdb8ddb43555bc5c7e378efe3e8622d6018088) Thanks [@deepu-s-2628](https://github.com/deepu-s-2628)! - Fixed a real version-drift bug: `changeset version` only bumps `package.json`, which left `.claude-plugin/plugin.json` — the manifest that actually matters for the installed plugin — stuck at `0.1.0` after the `0.2.0` release merged. Added `scripts/sync-plugin-version.mjs` and wired it into the `version` npm script so both manifests move together on every future release.

## 0.2.0

### Minor Changes

- [`8eb9f14`](https://github.com/deepu-s-2628/deepskill/commit/8eb9f14187581db50f0d6f6f25c644abbb4e385f) Thanks [@deepu-s-2628](https://github.com/deepu-s-2628)! - Vendored Archify and frontend-slides in full, at `skills/archify/` and `skills/frontend-slides/` — both are now first-party, always-available parts of this plugin, not separately-installed dependencies. PPTX and PDF generation are retired entirely: flowcharts are now interactive Archify HTML, and the executive/engineering presentations are self-contained HTML decks authored with frontend-slides. `generate_pptx.py` and `generate_flowchart.py` are deleted; the PRD stays DOCX, generated the same way as before.

  Removed the `ITOM-PM-Result/` wrapper folder — a PM run's topic folder (`[slug]/` or `[slug]-enhancement/`) now sits directly in the workspace root. Flattened the visible layout inside it: the consolidated report is `[slug].html` (not `report.html`) sitting directly in the topic folder alongside the flowchart, slide decks, and PRD, all visible; `.steps/` stays hidden and now also holds the DOCX build script (`.steps/build_docx.py`) and Archify source specs, kept for resumability.

  Prompted by hands-on use: the nested `ITOM-PM-Result/[slug]/Generated/` structure was confusing to navigate day to day, and generating a PDF/PPTX pipeline alongside an HTML-first report added a second, less capable rendering path for no real benefit once Archify and frontend-slides covered the same ground with more animation and interactivity. Vendoring (rather than depending on the separately-installed `archify` plugin, as the previous release did with a graceful-degrade fallback) was an explicit call: this repo now owns syncing future updates to both tools, in exchange for teammates never needing a second plugin install.

- [`e07bc7d`](https://github.com/deepu-s-2628/deepskill/commit/e07bc7d50241537372a98564b141f9a8c4a42991) Thanks [@deepu-s-2628](https://github.com/deepu-s-2628)! - `ask-deepu` now interrogates a request itself before anything else runs: does it actually fit OpManager Plus/Nexus, is it a feature or an enhancement, and what does the pipeline need locked down. This is the only interactive phase — once it concludes "proceed," every remaining step runs unattended with no per-step approval gates (the one exception: the enhancement wireframe step still pauses if screenshots are missing). "Stop — not a fit" is a first-class outcome, not a failure.

  Replaced per-step visible HTML with one consolidated, anchor-navigable `report.html` per run, rebuilt after every step via the new `scripts/build_report.py`. Diagrams render through the separate, optional `archify` plugin when it's installed and embed as interactive frames; when it isn't, the same content degrades to a plain table or prose instead of failing the step.

  Surfaced by real testing: a request outside OpManager Plus/Nexus's product surface was previously taken at face value and analyzed as if it fit, and results were scattered across a separate HTML file per step instead of one artifact. An earlier version of this fix added a standalone `wayfind` skill; folded directly into `ask-deepu` instead once testing showed the separate-skill invocation was itself unreliable, and its name was one typo away from an unrelated skill (`wayfinder`) that some teammates will have installed from a different plugin.

### Patch Changes

- [`d5cb1ff`](https://github.com/deepu-s-2628/deepskill/commit/d5cb1ff3e791a003f334cd9eb67c8c32e710e17b) Thanks [@deepu-s-2628](https://github.com/deepu-s-2628)! - Added `argument-hint` to `ask-deepu`'s frontmatter, so typing `/ask-deepu` shows a greyed-out example prompt instead of a blank input — matching the pattern already used by mattpocock's own stateful entry-point skills (`loop-me`, `teach`, `handoff`).

- [`1c276f7`](https://github.com/deepu-s-2628/deepskill/commit/1c276f706649080fc2b35f34102133f9ed8cb4ec) Thanks [@deepu-s-2628](https://github.com/deepu-s-2628)! - Fixes surfaced by a real end-to-end run of the feature pipeline against the vendored Archify/frontend-slides tooling and flat layout: a stale "converted to PDF" line in `deliverables/SKILL.md`'s flowchart draft section (PDF generation was already retired), a missing cross-reference explaining that the DOCX's embedded architecture image is a static `matplotlib` render rather than the interactive Archify HTML (added to both `deliverables/SKILL.md` and `enhancement-deliverables/SKILL.md`), and a note on both `generate-documents` skills that an Archify showcase validation pass is expected to take a few iterations, not one shot.

## 0.1.0

Initial release — extracted from `itom-ai-toolkit`. Foundation: pipeline-bucketed skills, `ask-deepu` entry point, ubiquitous-language glossary, dual-format (Claude/Copilot/Codex) skills and agents, Python tooling on `uv`.
