# deepskill

## 0.8.2

### Patch Changes

- [`0c13841`](https://github.com/deepu-s-2628/deepskill/commit/0c13841e72d620106142e9410986b1a91dc08a77) Thanks [@deepu-s-2628](https://github.com/deepu-s-2628)! - Fixed `ask-deepu` and the whole pipeline being unusable outside a checkout of this repo. `npx skills add` installs each skill as an independent, flattened package with no `context/`/`scripts/` alongside it, so a PM running `/ask-deepu` from a real project folder hit a hard failure looking for files that were never installed. Added a native Claude Code plugin marketplace (`.claude-plugin/marketplace.json`) so `/plugin install deepskill@deepskill` brings the whole repo tree along as one unit, and rewrote every internal reference to `context/`, `scripts/`, and the vendored Archify/frontend-slides/unlazy-gates tools to resolve via `${CLAUDE_PLUGIN_ROOT}` instead of a repo-relative path — works identically whether this is a real plugin install or a local checkout. Python dependency bootstrap (`uv sync`) is now automatic on first use instead of a manual PM-facing step.

- [`e6f2390`](https://github.com/deepu-s-2628/deepskill/commit/e6f2390432e1c3d863531239fcd4113c301c1da0) Thanks [@deepu-s-2628](https://github.com/deepu-s-2628)! - Correct the `$CLAUDE_PLUGIN_ROOT` resolution instructions added in the previous fix — it is not a real environment variable. Confirmed empirically: `echo $CLAUDE_PLUGIN_ROOT` and Python's `os.environ["CLAUDE_PLUGIN_ROOT"]` both come back empty/raise, so the "resolve via Bash" advice previously written into `context/pm-operating-system.md`, both orchestrator agents, and several standalone skills was dead and could strand a real run. Replaced with the mechanism that actually works: Claude Code shows every loaded skill its own resolved "Base directory for this skill" path, and the real plugin root is the nearest ancestor of that path containing `.claude-plugin/plugin.json`. Added a new `context/pm-operating-system.md` §0 documenting this as the authoritative procedure, inlined the same compact procedure into every true entry point (`ask-deepu`, `learn-deepu`, `wait-what`, both orchestrator agents) since they can't yet rely on `pm-operating-system.md` being loaded, and fixed the two generated `.steps/build_docx.py` scripts to receive the literal resolved path directly instead of reading a nonexistent environment variable.

- [`ee070f2`](https://github.com/deepu-s-2628/deepskill/commit/ee070f28aa7c32d2ce316f9c97c14e5fee448027) Thanks [@deepu-s-2628](https://github.com/deepu-s-2628)! - README: add migration guidance for anyone who already installed `ask-deepu`/the pipeline skills via `npx skills` before this native-plugin fix shipped. Confirmed empirically: an old flattened `npx skills`-installed skill takes precedence over the new native plugin for a bare `/ask-deepu`, silently reproducing the exact failure this release fixes. Documents the `npx skills@latest remove ... -g -y` cleanup command (verified against the real skill list) and the `/deepskill:ask-deepu` namespaced-invocation fallback for anyone who'd rather not remove anything yet.

## 0.8.1

### Patch Changes

- [`73569bc`](https://github.com/deepu-s-2628/deepskill/commit/73569bca5fdcd8c714b5c1f6b8bede918bf91d43) Thanks [@deepu-s-2628](https://github.com/deepu-s-2628)! - Fixed the README's "Updating an existing install" section, which listed every bundled skill by name but was missed when `learn-deepu` was added — same staleness pattern caught and fixed twice already tonight (skills list -g, Step 6 reference tables).

## 0.8.0

### Minor Changes

- [`60ec0a8`](https://github.com/deepu-s-2628/deepskill/commit/60ec0a80ab4a60f87d93fd660e3835c36ae3115f) Thanks [@deepu-s-2628](https://github.com/deepu-s-2628)! - Added `learn-deepu`, a standalone teaching utility curated from mattpocock/skills' `teach` (MIT) — a real multi-session learning workspace (`Mission.md`, `lessons/*.html`, `reference/*.html`, `learning-records/`, `assets/`, `Resources.md`, `Notes.md`) for any topic, not just ITOM ones. Checks whether a topic relates to OpManager Plus/Nexus and grounds itself in `context/product-context.md`/`context/CONTEXT.md` when it does, teaches fully generically otherwise. Lessons and reference docs follow `skills/design-taste/SKILL.md`'s styling. Deliberately standalone — not wired into the PM pipeline or any of the 14 pipeline skills.

## 0.7.1

### Patch Changes

- [`3098bbe`](https://github.com/deepu-s-2628/deepskill/commit/3098bbe5cccdd80509e4366e143d1725b89f6d40) Thanks [@deepu-s-2628](https://github.com/deepu-s-2628)! - Fixed the README's `skills list` documentation — it only showed the bare command, which defaults to project scope and reports "No project skills found" for a global install (reproduced live: `npx skills@latest list` after a `-g` install says exactly this and suggests `-g`). Now documents both forms, matching how `update` already documents `-p`/`-g`. Also updated the `update` section's skill list, which was stale since `design-taste` and `unlazy-gates` were vendored.

- [`4cb1263`](https://github.com/deepu-s-2628/deepskill/commit/4cb1263a8fb792f5b83f691a9d31ae9296babde0) Thanks [@deepu-s-2628](https://github.com/deepu-s-2628)! - Fixed stale Step 6 descriptions left over from the `prototype.html` and opt-in changes: README's Feature/Enhancement pipeline reference tables still said "Lovable Wireframe Prompt" only, with no mention of `prototype.html` or that Step 6 is now opt-in; both `lovable-wireframe` and `enhancement-wireframe` skills' own frontmatter `description` had the same gap.

## 0.7.0

### Minor Changes

- [`2cf409e`](https://github.com/deepu-s-2628/deepskill/commit/2cf409e384fa753c1eb67274e6bcbb3692926e5a) Thanks [@deepu-s-2628](https://github.com/deepu-s-2628)! - Milestone 3: `unlazy-gates` for the pipeline's Quality Gate checklists.

  Vendored a curated, **Solo-mode-only** slice of `unlazy` (v2.1.0, MIT, Leonxlnx) at `skills/unlazy-gates/` — `gate-check.mjs`/`gate-lint.mjs` and their dependencies, a simplified Solo template (`OWNS`/`CWD` dropped, since concurrent-writer coordination never applies to a single continuous sequential session), and the full gate-authoring reference. Deliberately excluded: the Depth Tree, `PLAN.md`, orchestrated/parallel dispatch machinery, and the optional Stop hook — none of it fits this pipeline, and the Stop hook specifically would block a session on unmet gates, which contradicts the never-pause contract below.

  Translated each of the 14 pipeline skills' existing "Quality Gate" checklists into a real `.steps/GATES-N.md` ledger: mechanically-checkable items (a persona-story count, a placeholder-text scan, a file existing, `Progress.md` actually updated) become runnable `CHECK:`/`EXPECT:` gates; genuine judgment calls ("plain English," "specific, not generic") stay explicit manual gates, self-attested exactly as they already were. Verified with real traces, not assumed: a runnable gate failing then passing after self-correction, a manual gate correctly carrying no script, and the placeholder-scan gate across a realistic 4-file Step-5 draft set.

  **The resolution rule is this repo's own addition, not `unlazy`'s native behavior**: `unlazy`'s own unsatisfiable-gate path is `ABANDON`, which halts with `HANDOFF REQUIRED` — built for a human-supervised session. This pipeline has exactly two sanctioned pause points (wayfinding, the Step 6 opt-in choice); a quality gate is neither. A failing runnable gate gets 2–3 self-correction retries; still-unmet after that gets documented as a stated gap in the step's own output (the same pattern already used for an unavailable screenshot) and the run continues — never abandoned, never paused. Documented in full as `context/pm-operating-system.md` §18.

  Also fixed, found while sweeping for consistency: `design-taste` and `unlazy-gates` were both missing from the README's Utilities table despite being vendored the same way as Archify/frontend-slides — an incomplete "vendored in full" listing is exactly the staleness class this repo keeps getting caught by.

## 0.6.0

### Minor Changes

- [`e16cc55`](https://github.com/deepu-s-2628/deepskill/commit/e16cc55710d4057b2690c3ff7c713ee3f4db7ca7) Thanks [@deepu-s-2628](https://github.com/deepu-s-2628)! - Step 6 (the Lovable prompt and `prototype.html`) is now opt-in instead of running unconditionally at the end of the autonomous chain. Once Steps 1–5 and document generation finish, the orchestrator asks once — both / just the prompt / just the prototype / neither — before deciding whether Step 6 runs at all, and if so, scoped to exactly what was chosen.

  This is a second sanctioned checkpoint, not a reversal of the "wayfinding is the only pause" principle: `pm-operating-system.md` §8 now names both checkpoints explicitly as **scope/consent decisions**, never a content review — nothing about Steps 1–5's analysis or Step 6's own output, once it runs, is ever re-litigated. `Progress.md` gains a new `awaiting_step6_choice` state distinct from `blocked_on_pm` (a real dependency gap, e.g. the enhancement pipeline's screenshot requirement, unrelated to this choice). Propagated across both wireframe skills, both orchestrator agent pairs, the operating-system doc (canonical trees, quality gates, resume protocol, chat contract, non-goals), and the README. Verified `build_report.py` needs no changes — it already tolerates a topic folder with no Step 6 markdown at all — and swept the repo for now-stale "wayfinding is the only interactive step" claims left over in `skills/ask-deepu/SKILL.md` and `skills/feature-pipeline/brainstorm/SKILL.md`.

## 0.5.0

### Minor Changes

- [`ecb7fed`](https://github.com/deepu-s-2628/deepskill/commit/ecb7fedb94f6893dbe7611b08d4b82f6f3490749) Thanks [@deepu-s-2628](https://github.com/deepu-s-2628)! - Milestone 2 of the taste-skill roadmap: a `prototype.html` deliverable for Step 6, additive alongside the existing Lovable-prompt output — both ship, neither replaces the other. It renders one representative screen (the primary/dashboard screen in feature mode; the enhanced main page, using existing/new/modified color coding, in enhancement mode) as a real, self-contained static HTML mockup, reusing the exact screen spec already drafted for the Lovable prompt rather than researching anything new. Follows `skills/design-taste/SKILL.md` (milestone 1) for its styling — same zero-build-step, zero-framework constraint as every other deliverable in this repo.

  Updated `pm-operating-system.md` (canonical file trees, retention rule, Mission line, §11b, Step 6 quality gate), both orchestrator agent pairs (Step 6 output + Output Structure tree), and the README (Getting Started tree, Roadmap).

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
