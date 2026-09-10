# Ask Deepu — ITOM PM Skills

An end-to-end product-management pipeline for OpManager Plus, as an installable Claude Code plugin. Describe a feature or an improvement, and it takes you through research, competitive analysis, technical scoping, and a full deliverable set — decks, a PRD, a flowchart, a wireframe prompt — one reviewable step at a time.

## Installation

1. Clone this repo somewhere on your machine.
2. Run `./scripts/link-skills.sh` from the repo root.
3. Restart Claude Code.

Re-run step 2 after every `git pull` to pick up new skills.

## Why this exists

The ITOM PM pipeline used to live inside `itom-ai-toolkit`, tangled up with that repo's VS Code extension build. Pulling it out means:

- **It's independent.** Update the pipeline without touching, or being touched by, unrelated toolkit changes.
- **It's install-anywhere.** Every skill ships a Codex-compatible `openai.yaml` shim alongside its `SKILL.md`, and the two orchestrators exist in both Claude subagent and Copilot-agent form.
- **It's plain-language by design.** Every step's output is written in ASD-STE100 Simplified Technical English against a real ubiquitous-language glossary (`context/CONTEXT.md`) — not just "try to keep it simple."

## Getting started

Describe what you want, prefixed with `ask-deepu`:

> `/ask-deepu: I want to add Cisco SD-WAN monitoring support`

`ask-deepu` figures out whether that's a new feature or an improvement to something that already exists, and starts the matching pipeline. Each step pauses for your review (a hidden `.md` source + a visible `.html` file you open in a browser) before moving on.

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
| `ask-deepu` | Entry point — routes to the right pipeline |
| `wait-what` | "That didn't land — re-pitch it simpler" |

## Generating the actual files (PPTX/DOCX/flowchart)

The generators are Python, at `scripts/`. Bootstrap once with [`uv`](https://docs.astral.sh/uv/):

```bash
cd scripts
uv sync
```

## Roadmap

`v0.1.0` is the foundation: extraction, the glossary, plain-language output, dual-format skills, this release tooling. Not yet included, planned for `v0.2.0`+:

- A reusable adaptive-question ("grilling") engine for the brainstorm and current-state-analysis steps
- Archify-based interactive diagrams in place of the static flowchart generator
- A single consolidated, anchor-navigable HTML report per pipeline run
- A ticket/milestone breakdown stage handing off from PRD to engineering

## Status

Internal tool, `v0.1.0`, private. No published package — install via the symlink script above.
