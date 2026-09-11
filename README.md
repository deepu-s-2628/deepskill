# DeepSkill

**Ask Deepu** — an end-to-end product-management pipeline for OpManager Plus, as an installable agent-skills package. Describe a feature or an improvement, and it takes you through research, competitive analysis, technical scoping, and a full deliverable set — decks, a PRD, a flowchart, a wireframe prompt — one reviewable step at a time.

## Installation

```bash
npx skills@latest add deepu-s-2628/deepskill
```

Run it from anywhere — no cloning, no local copy of this repo needed. It fetches directly from GitHub (using the git credentials you already have configured, so this works against a private repo the same as a public one) and walks you through the rest: whether to install for just the current project or globally for every project, and which agent(s) to install for (Claude Code, Codex, Copilot — this repo ships compatibility shims for all three).

Restart your agent afterward.

## Updating an existing install

The `skills` CLI tracks where each installed skill came from, so updating doesn't mean re-running `add` — use its dedicated `update` command instead:

```bash
npx skills@latest update
```

Add `-p` to update only project-scoped skills or `-g` for only global ones, and `-y` to skip the scope prompt. This re-fetches every skill whose source is `deepu-s-2628/deepskill` — `ask-deepu`, all 14 pipeline skills, `wait-what`, Archify, and frontend-slides — straight from `main`, and reports each one it touched. Restart your agent afterward to pick up the changes.

To check what's currently installed (and confirm it really came from this repo) before or after updating:

```bash
npx skills@latest list
```

## Why this exists

The ITOM PM pipeline used to live inside `itom-ai-toolkit`, tangled up with that repo's VS Code extension build. Pulling it out means:

- **It's independent.** Update the pipeline without touching, or being touched by, unrelated toolkit changes.
- **It's install-anywhere.** Every skill ships a Codex-compatible `openai.yaml` shim alongside its `SKILL.md`, and the two orchestrators exist in both Claude subagent and Copilot-agent form.
- **It's plain-language by design.** Every step's output is written in ASD-STE100 Simplified Technical English against a real ubiquitous-language glossary (`context/CONTEXT.md`) — not just "try to keep it simple."

## Getting started

Describe what you want, prefixed with `ask-deepu` (typing `/ask-deepu` shows a greyed-out example prompt to nudge you):

> `/ask-deepu: I want to add Cisco SD-WAN monitoring support`

`ask-deepu` interrogates it first — that's its own job, not a separate step you have to invoke. Before anything else happens: does this actually belong in OpManager Plus/Nexus, is it a net-new feature or an improvement to something existing, and what does the rest of the pipeline need to know. It can conclude the request doesn't fit at all and stop there — that's a first-class outcome, not a failure.

Once that interrogation ("wayfinding") concludes "proceed," the matching pipeline runs every remaining step back-to-back with **no further pauses** through Steps 1–5 and document generation — no `proceed`/`approve` replies needed. Once documents are ready, there's one more short check-in: whether you want the Step 6 wireframe deliverables (the Lovable prompt, a static prototype, both, or neither) at all — a one-time scope question, not a content review. The enhancement pipeline's wireframe step has its own separate, unrelated exception: it'll stop and ask for screenshots if none exist, since that's a real dependency.

Everything lands directly in your workspace, no wrapper folder — a topic folder named after the slug, e.g. `vxlan-monitoring/` (or `vxlan-monitoring-enhancement/`). The files inside it are named for their role, not the slug — same name in every topic folder, same idea as `README.md`, so it's always obvious which one to open first:

```
vxlan-monitoring/
├── Progress.md
├── analysis.html               ← the one consolidated report — start here
├── architecture.html           ← interactive Archify diagram
├── executive-brief.html        ← executive slide deck
├── engineering-brief.html      ← engineering slide deck
├── product-requirements.docx   ← PRD
├── prototype.html              ← static-HTML mockup of the primary screen (only if you opt into Step 6)
└── .steps/                     ← hidden markdown history, kept for resume
```

`analysis.html` is a single navigable page — nested sub-headings and scroll-position highlighting in the left nav — with every step's findings, plus a diagram wherever one earns its place over plain text.

## Reference

### Feature pipeline (`skills/feature-pipeline/`)

| Step | Skill |
|---|---|
| 1 — Brainstorm | `brainstorm` |
| 2 — Competitive Analysis | `competitive-analysis` |
| 3 — Technical Analysis | `technical-analysis` |
| 4 — Feature Definition | `feature-definition` |
| 5 — Deliverable Drafts | `deliverables` |
| 5 (render) — Generate Documents | `generate-documents` |
| 6 — Lovable Wireframe Prompt | `lovable-wireframe` |

### Enhancement pipeline (`skills/enhancement-pipeline/`)

| Step | Skill |
|---|---|
| 1 — Current State Analysis | `current-state-analysis` |
| 2 — Cross-Module Analysis | `cross-module-analysis` |
| 3 — Competitive Analysis | `enhancement-competitive` |
| 4 — Findings | `enhancement-findings` |
| 5 — Deliverable Drafts | `enhancement-deliverables` |
| 5 (render) — Generate Documents | `enhancement-generate-documents` |
| 6 — Lovable Wireframe Prompt | `enhancement-wireframe` |

### Utilities

| Skill | Purpose |
|---|---|
| `ask-deepu` | Entry point and the first of two interactive checkpoints — interrogates fit, mode, and scope, then hands off to the right pipeline |
| `wait-what` | "That didn't land — re-pitch it simpler" |
| `archify` | Vendored in full (`skills/archify/`) — renders the flowchart and any other diagrams as interactive HTML |
| `frontend-slides` | Vendored in full (`skills/frontend-slides/`) — authors the executive/engineering slide decks as self-contained, animation-capable HTML |
| `design-taste` | Curated adaptation (`skills/design-taste/`) — the visual-taste principles behind `analysis.html`'s and `prototype.html`'s styling (operating system §11b) |
| `unlazy-gates` | Curated, Solo-mode-only adaptation (`skills/unlazy-gates/`) — mechanically-verified completion gates for each pipeline step (operating system §18) |

Everything in this repo, including Archify, frontend-slides, design-taste, and unlazy-gates, is bundled in `skills/` — installing this one package is enough. Nothing here depends on a teammate having a *different*, separately-installed plugin on their machine (operating system §11a) — if that ever changes for something added later, the same rule applies: try it, and degrade gracefully rather than fail the run if it's missing.

## Generating the actual files (Archify flowchart / HTML slide decks / DOCX)

The PRD generator is Python, at `scripts/`. Bootstrap once with [`uv`](https://docs.astral.sh/uv/):

```bash
cd scripts
uv sync
```

No `uv` on the machine? Fall back to a plain virtualenv:

```bash
cd scripts
python3 -m venv .venv && source .venv/bin/activate
pip install python-docx Pillow matplotlib
```

Archify and frontend-slides need no install step — both are pure Node.js/static HTML, invoked directly from their vendored `skills/` paths.

## Roadmap

`v0.1.0` covered the foundation: extraction, the glossary, plain-language output, dual-format skills, this release tooling.

`v0.2.0` — pulled forward after real testing surfaced they weren't optional: `ask-deepu`'s wayfinding interrogation and the single consolidated `analysis.html` report; Archify and frontend-slides fully vendored under `skills/`, replacing PPTX/PDF generation entirely; the flat topic-folder layout with no `ITOM-PM-Result/` wrapper.

`v0.3.0` — real-usage feedback from a full pipeline run: role-based deliverable filenames (`analysis.html`, `architecture.html`, `executive-brief.html`, `engineering-brief.html`, `product-requirements.docx`) instead of slug-prefixed ones; a real bookmark-linked PRD Table of Contents (no manual Word "Update Field" step); nested report navigation with scroll-position highlighting; mandatory slide-deck navigation at reading-first density; this README's install/update docs.

Unreleased — three sequential milestones (each its own changeset, shipped in this order — the later ones depend on groundwork the earlier ones lay):

1. **Done.** Design taste for `analysis.html`. Curated the stack-agnostic parts of [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) (`design-taste-frontend` v2) into `skills/design-taste/` — its color/typography/shape/spacing discipline and its process of naming and avoiding generic-AI defaults, not its React/Motion/npm-component-library machinery or landing-page structure rules, neither of which fit this repo's zero-build-step static-HTML deliverables — and applied it to the report's styling: one held accent color (ManageEngine brand blue), row-separator tables instead of a full boxed grid, a readable prose measure, real focus states.
2. **Done.** A `prototype.html` deliverable for Step 6. Additive alongside the existing Lovable-prompt output: a real, static-HTML mockup of the primary screen (or, in enhancement mode, the enhanced main page with existing/new/modified coding), rendered using the same design-taste groundwork from milestone 1, for a PM who wants to see the idea fast rather than iterate further in an external tool.
3. **Done.** `unlazy-gates` for the pipeline's Quality Gate checklists. Curated, Solo-mode-only vendor of `unlazy` (`skills/unlazy-gates/` — its Depth Tree, orchestrated/parallel dispatch, and Stop hook all excluded, none of it fits a single-session sequential pipeline) translates each of the 14 skills' checklists into a real `.steps/GATES-N.md` ledger: mechanically-checkable items (a persona-story count, a placeholder-text scan, a file existing) become runnable `CHECK:`/`EXPECT:` gates; genuine judgment calls stay explicit manual gates. A failing gate self-corrects (2–3 retries) or gets documented as a stated gap and the run continues — never `unlazy`'s native abandon/handoff, which would reopen exactly the pause-for-review pattern Section 8 exists to prevent.

Also unreleased, not part of the taste/unlazy sequence above:

- **Done.** Step 6 (the Lovable prompt and `prototype.html`) is opt-in. Once Steps 1–5 and document generation finish, the PM is asked once — both / just the prompt / just the prototype / neither — a second sanctioned check-in alongside wayfinding, reconciled explicitly in `pm-operating-system.md` §8 as a scope/consent decision, never a content review, so it doesn't quietly reopen the "no per-step pauses" contract it sits inside.
- **Planned.** OpManager Nexus design fidelity for `prototype.html`. Milestone 2's mockups apply general good taste (design-taste's principles) but don't know the real product's actual components, layout patterns, or visual language — so a prototype can look tasteful without looking like OpManager Nexus. This needs a new skill or context resource capturing the real design system (navigation shape, card/table/widget patterns, real color tokens, spacing) for `prototype.html` to build against, the same way `product-context.md` already grounds the analysis steps in the real product's feature catalog.

Also still planned, unversioned:

- A ticket/milestone breakdown stage handing off from PRD to engineering (mattpocock's `to-tickets` pattern, adapted to group tickets into milestones by dependency-free batches)
- Auto-creating tracker issues from that breakdown (currently: markdown/HTML output only, reviewed and entered manually)

See `CHANGELOG.md` for the exact, generated release history — this section is a summary, not the source of truth.

## Status

Internal tool, private. Not published to any registry — install directly from this repo via `npx skills add` above. Releases are cut with [Changesets](https://github.com/changesets/changesets): every change lands with a `.changeset/*.md` file, and merging the bot-opened "Version Packages" PR bumps `package.json` and `.claude-plugin/plugin.json` together and updates `CHANGELOG.md`. Current version lives in [`.claude-plugin/plugin.json`](.claude-plugin/plugin.json) / [`CHANGELOG.md`](CHANGELOG.md) — not restated here, so this line can't go stale the way it did through v0.2.0.
