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

Describe what you want, prefixed with `ask-deepu`:

> `/ask-deepu: I want to add Cisco SD-WAN monitoring support`

`ask-deepu` hands your request to `wayfind` — the only interactive step. Wayfind interrogates it before anything else happens: does this actually belong in OpManager Plus/Nexus, is it a net-new feature or an improvement to something existing, and what does the rest of the pipeline need to know. It can conclude the request doesn't fit at all and stop there — that's a first-class outcome, not a failure.

Once wayfind concludes "proceed," the matching pipeline runs every remaining step back-to-back with **no further pauses** — no `proceed`/`approve` replies needed. The one exception: the enhancement pipeline's wireframe step will still stop and ask for screenshots if none exist, since that's a real dependency, not a review gate.

Everything lands in one place: `ITOM-PM-Result/[slug]/report.html` — a single navigable page with every step's findings, plus any diagrams rendered as real interactive Archify views where a diagram earns its place over plain text.

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
| `ask-deepu` | Entry point — hands the request to `wayfind` |
| `wayfind` | The only interactive step: interrogates fit, mode, and scope before anything runs unattended |
| `wait-what` | "That didn't land — re-pitch it simpler" |

## Generating the actual files (PPTX/DOCX/flowchart)

The generators are Python, at `scripts/`. Bootstrap once with [`uv`](https://docs.astral.sh/uv/):

```bash
cd scripts
uv sync
```

## Roadmap

`v0.1.0` covers: extraction, the glossary, plain-language output, dual-format skills, this release tooling — plus, pulled forward after real testing surfaced they weren't optional, the `wayfind` interrogation step, Archify diagrams embedded in the report, and the single consolidated `report.html`.

Still planned for `v0.2.0`+:

- A ticket/milestone breakdown stage handing off from PRD to engineering (mattpocock's `to-tickets` pattern, adapted to group tickets into milestones by dependency-free batches)
- Auto-creating tracker issues from that breakdown (currently: markdown/HTML output only, reviewed and entered manually)

## Status

Internal tool, `v0.1.0`, private. Not published to any registry — install directly from this repo via `npx skills add` above.
