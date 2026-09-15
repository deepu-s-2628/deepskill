# DeepSkill

**Ask Deepu** — an end-to-end product-management pipeline for OpManager Plus, as an installable agent-skills package. Describe a feature or an improvement, and it takes you through research, competitive analysis, technical scoping, and a full deliverable set — decks, a PRD, a flowchart, a wireframe prompt — one reviewable step at a time.

## Installation

One command, works the same way across every agent surface `npx skills` supports — Claude Code, Codex, Grok Build, Cursor, Gemini CLI, and more:

```bash
npx skills@latest add deepu-s-2628/deepskill
```

This installs every skill in this package — the pipeline, `ask-deepu`, `learn-deepu`, Archify, frontend-slides, `design-taste`, `unlazy-gates`, `wait-what` — as independent, flattened packages, each landing as a direct sibling of every other under one common parent directory, regardless of how deeply any of them were nested in this source repo. The pipeline and `learn-deepu` depend on shared files (`context/pm-operating-system.md`, `product-context.md`, `CONTEXT.md`, and the Python generators) — those ship as `skills/pm-shared/`, one more sibling in the same install, so every skill can reach them via a simple, fixed relative path. Restart your agent afterward.

## Updating an existing install

The `skills` CLI tracks where each installed skill came from, so updating doesn't mean re-running `add` — use its dedicated `update` command instead:

```bash
npx skills@latest update
```

Add `-p` to update only project-scoped skills or `-g` for only global ones, and `-y` to skip the scope prompt. This re-fetches every skill whose source is `deepu-s-2628/deepskill` — including `pm-shared` — straight from `main` and reports each one it touched. Restart your agent afterward to pick up the changes.

To check what's currently installed (and confirm it really came from this repo) before or after updating:

```bash
npx skills@latest list      # project-scoped skills (the default)
npx skills@latest list -g   # global skills — use this if you installed with -g,
                             # or if the plain command above says "No project skills found"
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

## Repository structure

This is the repo itself, not a PM run's output (that's under "Getting started" above). Verified against the actual tracked file list, not reconstructed from memory:

```
deepskill/
├── .claude-plugin/
│   └── plugin.json                 ← skill manifest — npx skills reads this to know what to install
├── .github/
│   ├── agents/                     ← Copilot-format orchestrators (mirrors agents/ below)
│   └── workflows/release.yml       ← Changesets release automation
├── agents/                         ← Claude subagent orchestrators
│   ├── ask-deepu-feature.md
│   └── ask-deepu-enhancement.md
├── context/                        ← canonical shared source — mirrored into skills/pm-shared/ at release time
│   ├── pm-operating-system.md      ← the shared rulebook every pipeline skill loads
│   ├── product-context.md          ← OpManager Plus/Nexus product DNA
│   └── CONTEXT.md                  ← ubiquitous-language glossary
├── scripts/                        ← canonical Python generators + release-sync tooling
│   ├── build_report.py, generate_docx.py, md_to_html.py
│   ├── sync-plugin-version.mjs     ← keeps plugin.json's version in step with package.json
│   └── sync-pm-shared.mjs          ← regenerates skills/pm-shared/ from context/ + scripts/
├── skills/
│   ├── ask-deepu/                  ← entry point — the only skill a PM ever invokes directly
│   ├── pm-shared/                  ← generated mirror of context/ + scripts/, installed as a sibling skill
│   ├── learn-deepu/, wait-what/    ← standalone utilities, no relationship to the pipeline
│   ├── archify/, frontend-slides/  ← vendored in full — diagrams and slide decks
│   ├── design-taste/, unlazy-gates/← vendored, curated adaptations — visual taste rules, quality gates
│   ├── feature-pipeline/           ← 7 step skills for net-new work (see Reference below)
│   └── enhancement-pipeline/       ← 7 step skills for improving something that exists
├── .changeset/                     ← pending release notes, consumed by the bot-opened Version Packages PR
├── CHANGELOG.md                    ← generated release history — the actual source of truth
└── README.md                       ← this file
```

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
| 6 — Lovable Prompt + `prototype.html`, opt-in* | `lovable-wireframe` |

### Enhancement pipeline (`skills/enhancement-pipeline/`)

| Step | Skill |
|---|---|
| 1 — Current State Analysis | `current-state-analysis` |
| 2 — Cross-Module Analysis | `cross-module-analysis` |
| 3 — Competitive Analysis | `enhancement-competitive` |
| 4 — Findings | `enhancement-findings` |
| 5 — Deliverable Drafts | `enhancement-deliverables` |
| 5 (render) — Generate Documents | `enhancement-generate-documents` |
| 6 — Lovable Prompt + `prototype.html`, opt-in* | `enhancement-wireframe` |

\* After Step 5's documents are ready, the PM is asked whether they want either, both, or neither of Step 6's deliverables — the only other sanctioned check-in besides wayfinding (operating system §8).

### Utilities

| Skill | Purpose |
|---|---|
| `ask-deepu` | Entry point and the first of two interactive checkpoints — interrogates fit, mode, and scope, then hands off to the right pipeline |
| `wait-what` | "That didn't land — re-pitch it simpler" |
| `learn-deepu` | Standalone, not part of the pipeline — teaches any topic as a real multi-session workspace (lessons, references, progress tracking), grounded in this repo's own OpManager Plus context when the topic is product-related |
| `archify` | Vendored in full (`skills/archify/`) — renders the flowchart and any other diagrams as interactive HTML |
| `frontend-slides` | Vendored in full (`skills/frontend-slides/`) — authors the executive/engineering slide decks as self-contained, animation-capable HTML |
| `design-taste` | Curated adaptation (`skills/design-taste/`) — the visual-taste principles behind `analysis.html`'s and `prototype.html`'s styling (operating system §11b) |
| `unlazy-gates` | Curated, Solo-mode-only adaptation (`skills/unlazy-gates/`) — mechanically-verified completion gates for each pipeline step (operating system §18) |
| `pm-shared` | Not invocable — a shared data package (`skills/pm-shared/`) carrying `context/` and the Python generators, installed alongside every other skill so they can reach it as a sibling directory |

Everything in this repo, including Archify, frontend-slides, design-taste, unlazy-gates, learn-deepu, and `pm-shared`, is bundled in `skills/` — installing this one package is enough. Nothing here depends on a teammate having a *different*, separately-installed plugin on their machine (operating system §11a) — if that ever changes for something added later, the same rule applies: try it, and degrade gracefully rather than fail the run if it's missing.

## Generating the actual files (Archify flowchart / HTML slide decks / DOCX)

The PRD generator is Python, bundled at `skills/pm-shared/scripts/` and resolved by each skill as a sibling directory at runtime. Its dependencies bootstrap themselves automatically, unattended, the first time a run needs them — there's no manual setup step for a PM to run. Archify and frontend-slides need no install step at all — both are pure Node.js/static HTML.

If you're developing on this repo directly rather than running it as an installed plugin, you can bootstrap the same dependencies yourself with [`uv`](https://docs.astral.sh/uv/):

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

## Roadmap

Every shipped change — exact commit links, full reasoning — lives in [`CHANGELOG.md`](CHANGELOG.md), generated by Changesets on every release. This section tracks only what's still ahead; it stopped duplicating shipped history to avoid the exact staleness this repo has already been caught by more than once.

- **Planned.** OpManager Nexus design fidelity for `prototype.html`. Today's mockups apply general good taste (`design-taste`'s principles) but don't know the real product's actual components, layout patterns, or visual language — so a prototype can look tasteful without looking like OpManager Nexus. Needs a new skill or context resource capturing the real design system (navigation shape, card/table/widget patterns, real color tokens, spacing), the same way `product-context.md` already grounds the analysis steps in the real feature catalog.
- **Planned.** A ticket/milestone breakdown stage handing off from PRD to engineering (mattpocock's `to-tickets` pattern, adapted to group tickets into milestones by dependency-free batches).
- **Planned.** Auto-creating tracker issues from that breakdown (currently: markdown/HTML output only, reviewed and entered manually).

## Status

Internal tool, private. Not published to any registry — install directly from this repo via `npx skills add` above. Releases are cut with [Changesets](https://github.com/changesets/changesets): every change lands with a `.changeset/*.md` file, and merging the bot-opened "Version Packages" PR bumps `package.json` and `.claude-plugin/plugin.json` together and updates `CHANGELOG.md`. Current version lives in [`.claude-plugin/plugin.json`](.claude-plugin/plugin.json) / [`CHANGELOG.md`](CHANGELOG.md) — not restated here, so this line can't go stale the way it did through v0.2.0.
