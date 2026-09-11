# DeepSkill

**Ask Deepu** — an end-to-end product-management pipeline for OpManager Plus, as an installable agent-skills package. Describe a feature or an improvement, and it takes you through research, competitive analysis, technical scoping, and a full deliverable set — decks, a PRD, a flowchart, a wireframe prompt — one reviewable step at a time.

## Installation

```bash
npx skills@latest add deepu-s-2628/deepskill
```

Run it from anywhere — no cloning, no local copy of this repo needed. It fetches directly from GitHub (using the git credentials you already have configured, so this works against a private repo the same as a public one) and walks you through the rest: whether to install for just the current project or globally for every project, and which agent(s) to install for (Claude Code, Codex, Copilot — this repo ships compatibility shims for all three).

Restart your agent afterward. Re-run the same command after a repo update to pick up new/changed skills.

## Why this exists

The ITOM PM pipeline used to live inside `itom-ai-toolkit`, tangled up with that repo's VS Code extension build. Pulling it out means:

- **It's independent.** Update the pipeline without touching, or being touched by, unrelated toolkit changes.
- **It's install-anywhere.** Every skill ships a Codex-compatible `openai.yaml` shim alongside its `SKILL.md`, and the two orchestrators exist in both Claude subagent and Copilot-agent form.
- **It's plain-language by design.** Every step's output is written in ASD-STE100 Simplified Technical English against a real ubiquitous-language glossary (`context/CONTEXT.md`) — not just "try to keep it simple."

## Getting started

Describe what you want, prefixed with `ask-deepu` (typing `/ask-deepu` shows a greyed-out example prompt to nudge you):

> `/ask-deepu: I want to add Cisco SD-WAN monitoring support`

`ask-deepu` interrogates it first — that's its own job, not a separate step you have to invoke. Before anything else happens: does this actually belong in OpManager Plus/Nexus, is it a net-new feature or an improvement to something existing, and what does the rest of the pipeline need to know. It can conclude the request doesn't fit at all and stop there — that's a first-class outcome, not a failure.

Once that interrogation ("wayfinding") concludes "proceed," the matching pipeline runs every remaining step back-to-back with **no further pauses** — no `proceed`/`approve` replies needed. The one exception: the enhancement pipeline's wireframe step will still stop and ask for screenshots if none exist, since that's a real dependency, not a review gate.

Everything lands directly in your workspace, no wrapper folder — a topic folder named after the slug, e.g. `vxlan-monitoring/` (or `vxlan-monitoring-enhancement/`):

```
vxlan-monitoring/
├── STATUS.md
├── vxlan-monitoring.html                ← the one consolidated report — start here
├── vxlan-monitoring-flowchart.html      ← interactive Archify diagram
├── vxlan-monitoring-exec-slides.html    ← executive slide deck
├── vxlan-monitoring-eng-slides.html     ← engineering slide deck
├── vxlan-monitoring.docx                ← PRD
└── .steps/                              ← hidden markdown history, kept for resume
```

`vxlan-monitoring.html` is a single navigable page with every step's findings, plus a diagram wherever one earns its place over plain text.

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
| `ask-deepu` | Entry point and the only interactive step — interrogates fit, mode, and scope, then hands off to the right pipeline |
| `wait-what` | "That didn't land — re-pitch it simpler" |
| `archify` | Vendored in full (`skills/archify/`) — renders the flowchart and any other diagrams as interactive HTML |
| `frontend-slides` | Vendored in full (`skills/frontend-slides/`) — authors the executive/engineering slide decks as self-contained, animation-capable HTML |

Everything in this repo, including Archify and frontend-slides, is bundled in `skills/` — installing this one package is enough. Nothing here depends on a teammate having a *different*, separately-installed plugin on their machine (operating system §11a) — if that ever changes for something added later, the same rule applies: try it, and degrade gracefully rather than fail the run if it's missing.

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

`v0.1.0` covers: extraction, the glossary, plain-language output, dual-format skills, this release tooling — plus, pulled forward after real testing surfaced they weren't optional: `ask-deepu`'s wayfinding interrogation, Archify diagrams and frontend-slides HTML decks (both fully vendored, replacing PPTX/PDF generation entirely), and the flat topic-folder layout with one consolidated `[slug].html`.

Still planned for `v0.2.0`+:

- A ticket/milestone breakdown stage handing off from PRD to engineering (mattpocock's `to-tickets` pattern, adapted to group tickets into milestones by dependency-free batches)
- Auto-creating tracker issues from that breakdown (currently: markdown/HTML output only, reviewed and entered manually)

## Status

Internal tool, `v0.1.0`, private. Not published to any registry — install directly from this repo via `npx skills add` above.
