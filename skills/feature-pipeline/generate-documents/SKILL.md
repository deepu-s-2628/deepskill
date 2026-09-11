---
name: generate-documents
description: "Generate the feature deliverables — an Archify flowchart, executive and engineering HTML slide decks, and a DOCX PRD — with professional design for OpManager Plus feature documents. Runs automatically right after Step 5's drafts are done — not gated on a PM command."
---

# Generate Documents

## Purpose

Generate production-quality deliverable files with **proper visual design** — not templated bullet dumps. You (the LLM) are the designer, using the tools this repo bundles (Archify, frontend-slides, `generate_docx.py`) rather than a generic template.

## Dense deliverables bar (flowchart / slide decks / PRD)

When generating files from Step 5 drafts:

1. **Read Steps 1–4 as well as Step 5** so nothing important is lost if a draft under-specified content.
2. The engineering deck must include table slides for metrics and collection-contract highlights (OIDs/APIs/paths) from technical analysis.
3. The flowchart must be complete with the sections required by the operating system dense-deliverables bar — not a single overview toy diagram.
4. The executive deck must include concrete capabilities, competitive facts, and success metrics from prior steps.
5. If a Step 5 draft is thin, **expand content from Steps 1–4** while generating (do not ship a thin deck). Note expansions in chat.
6. Quality fail: decks that still need a human to “fill in the real points.”

## Prerequisites

### Locating the tools

- **DOCX:** `generate_docx.py` lives at the repo root's `scripts/` directory — relative to this file: `../../../scripts/`. Install its dependencies once via `uv sync` from the repo root (see `scripts/pyproject.toml`).
- **Flowchart diagram:** Archify is bundled at `skills/archify/` (relative to this file: `../../archify/`). Its CLI is `bin/archify.mjs` — resolve it with `**/skills/archify/bin/archify.mjs`. No install step; it's pure Node.js.
- **Slide decks:** frontend-slides is bundled at `skills/frontend-slides/` (relative to this file: `../../frontend-slides/`). Read its `SKILL.md` for templates, animation patterns, and style presets before authoring.

## MANDATORY: Validate Before Generating

Before writing any code, verify ALL prerequisite **markdown** files exist in `[feature-name]/.steps/`:

| File | Step |
|------|------|
| `1_brainstorm.md` | Step 1 — Brainstorm |
| `2_competitive_analysis.md` | Step 2 — Competitive Analysis |
| `3_technical_analysis.md` | Step 3 — Technical Analysis |
| `4_feature_definition.md` | Step 4 — Feature Definition |
| `5a_executive_presentation.md` | Step 5a — Executive PPT |
| `5b_engineering_presentation.md` | Step 5b — Engineering PPT |
| `5c_feature_flowchart.md` | Step 5c — Flowchart |
| `5d_product_requirements.md` | Step 5d — PRD |

**If any file is missing, STOP immediately and tell the PM:**
> "Cannot generate files. Missing: [list missing files]. Please complete these steps first."

Also check that `.steps/1_brainstorm.md` contains persona stories (search for "persona" or "story" or "Meet"). If missing, warn:
> "Warning: No persona stories found in brainstorm. Presentations need persona narratives for Slides 2 and 11."

## CRITICAL: Your Role as Designer

For each feature, you must:
1. **Read the finished content** from Step 5 files.
2. **Design the flowchart and decks** — decide what diagrams, charts, and layouts best communicate this specific feature.

Use your understanding of the feature to design a flowchart and slide decks that are SPECIFIC to this feature — not generic placeholders.

## Process

### 1. Generate the Flowchart (Archify)

Author a JSON spec at `.steps/diagrams/flowchart.json` for Archify's `workflow` type (see `skills/archify/schemas/`), then render:

```bash
node "<archify-dir>/bin/archify.mjs" deliver workflow ".steps/diagrams/flowchart.json" "architecture.html" --quality showcase --json
```

- Translate the Mermaid sketch from `5c_feature_flowchart.md` into the spec — this is a fresh authoring pass (new stable IDs, real domain wording), not a literal transcription.
- Cover: overview flow, setup/onboarding, data collection pipeline (with protocol/API branch detail), alerting, failure/retry — multiple linked views (`meta.views`) if one flat diagram can't hold all of it legibly.
- Label every decision node with the real condition from the technical analysis; annotate key OIDs/endpoints on collection nodes where space allows.
- Validate before delivering: `node "<archify-dir>/bin/archify.mjs" validate workflow ".steps/diagrams/flowchart.json" --quality showcase --json` must report a showcase pass with 0 errors/warnings. A showcase pass rarely happens on the first attempt — real layout errors (edge/node crossings, label overlaps, desktop-readability failures) are normal on early drafts and come with specific fix suggestions; keep revising the spec and re-validating until it's clean, don't stop or skip the diagram after the first failure.
- Reference the output from `5c_feature_flowchart.md` with `<!-- diagram: architecture.html -->` so it embeds into the consolidated report (Section 6).

### 2. Generate the Executive Slide Deck (frontend-slides)

**This must be visually compelling for a Product Director presentation.**

Author `executive-brief.html` directly as self-contained HTML, following `skills/frontend-slides/SKILL.md`'s templates and animation patterns. Plan slide types before writing:

| Slide | Content | Why |
|-------|---------|-----|
| Title | — | Sets tone |
| Persona Story | Quote/callout, not bullets | Emotional grounding — must feel human, not data-driven |
| Opportunity/Gap | Two-column | Problem vs. solution |
| Competitive | Comparison matrix, color-coded | Real differentiators |
| Approach | Connected process-flow | How it works, at a glance |
| Capabilities | Icon grid, not a bullet list | v1 capabilities from feature definition |
| Key Stat | Single powerful number | Break up dense slides |
| Metrics/KPIs | KPI cards | Specific, measurable |
| Timeline | Horizontal roadmap | Phasing |
| Persona Revisited | Before/after panels | Mirrors the persona-story slide with the resolved outcome |
| Closing | — | |

Design principles:
- These decks are read async (handoff, review), not presented live — explicitly use frontend-slides' "high density / reading-first" mode (its own SKILL.md §"How dense should the deck feel?"), not its sparse speaker-led default: 4-8 bullets or 4-6 structured cards per slide, self-contained slides that don't need a narrator. Still never more than 2 consecutive bullet-only slides — reach for a table, grid, or comparison layout instead.
- **Navigation is mandatory, not optional polish.** Every deck must ship the full navigation contract from `skills/frontend-slides/html-template.md` — keyboard (arrows, space, page up/down), mouse wheel, and visible on-screen prev/next controls — built directly into the self-contained HTML. Read `html-template.md` in full before authoring; a deck with no way to move to the next slide is incomplete, not just unpolished.
- Diagrams and visuals should be the center of attention on the slides built around them, not an afterthought.
- Use frontend-slides' animation patterns deliberately on the persona and transformation slides.
- The persona-story slide and the persona-revisited slide must use the *same* named persona from Step 1.
- Render the persona challenge traceability table (if in the PRD) as a comparison layout with status indicators showing which challenges are solved.

### 3. Generate the Engineering Slide Deck (frontend-slides)

**This must be technically detailed but visually clear for engineers.**

Author `engineering-brief.html` the same way. Plan:

| Slide | Content |
|-------|---------|
| Title | — |
| Persona Story | Emotional grounding |
| Technology Overview | Concept vs. implementation, two-column |
| Data Collection | Pipeline visualization |
| Architecture | Link/embed the flowchart |
| Metrics | Table (split if >8 rows) |
| Scalability | Performance targets as KPI cards |
| Phasing | Roadmap |
| UI Components | Screen overview grid |

Include:
- **Data flow** — Device → Polling Engine → DB → UI, matching the flowchart.
- **Metric tables** — formatted, with severity indicators.
- **Architecture** — pulled from the same Archify flowchart rather than re-drawn.
- **Scale projections** — a simple chart if the numbers matter (matplotlib PNG embedded, since this is a static presentation asset).

### 4. Generate the PRD (DOCX)

Professional document with:
- Styled heading hierarchy, formatted tables with colored headers.
- Page numbers, headers, and a real Table of Contents (`DocxBuilder.add_table_of_contents()` + `add_heading()` — every heading links automatically, no manual "Update Field" step needed).
- **A short plain-language intro (2-4 sentences, wait-what-style: plain words, no unexplained jargon) before every major section's tables** — Executive Summary, Technical Architecture, Metrics, everything. This document must read as a narrative with supporting tables, not a wall of tables with no framing.
- Metric specification tables with proper formatting.
- **Technical Architecture section** (Section 3) with an embedded architecture image, data flow, decision logic, data model, and integration points. This image is a **simple static diagram rendered with `matplotlib`** purpose-built for the printed page — Archify's output is interactive HTML and isn't meant to be screenshotted into a document; draw a lightweight equivalent instead.
- **Persona Challenges section** (Section 2.2) as a COMPACT reference table — not multi-paragraph narratives.
- **Persona Challenge Traceability section** (Section 9) as a compact cross-reference table.
- **Use Cases table** should be concise — no "Persona Challenge Addressed" column (personas are tracked in Section 9).
- Author metadata defaults to "Deepu S" (`DocxBuilder.add_title_page()`) — no `[PM Name]`-style placeholder ships in the document.

### 5. Write and Run the DOCX Build Script

Write `.steps/build_docx.py` that:
1. Resolves the scripts directory (repo root's `scripts/`) and adds it to `sys.path`:
   ```python
   import sys
   SCRIPTS_DIR = "<repo-root>/scripts"
   sys.path.insert(0, SCRIPTS_DIR)
   ```
2. Imports and uses `generate_docx.DocxBuilder`.
3. Reads content from `.steps/` Step 5 markdown files (and backfill from Steps 1–4 when drafts are thin).
4. Renders the small matplotlib architecture image as an intermediate PNG under `.steps/diagrams/`.
5. Assembles `product-requirements.docx` at the topic-folder root.

Then run it:
```bash
cd "[feature-name]" && python .steps/build_docx.py
```

**Keep `.steps/build_docx.py` after success** so the PM can regenerate without rewriting the designer script. Only rewrite it when content or layout must change.

If unsure of the absolute path, resolve it with `file_search` for `**/generate_docx.py`.

## Output

```
[feature-name]/
├── architecture.html          ← Archify diagram
├── executive-brief.html       ← executive deck (frontend-slides)
├── engineering-brief.html     ← engineering deck (frontend-slides)
├── product-requirements.docx  ← PRD
└── .steps/
    ├── diagrams/flowchart.json  ← Archify source spec
    └── build_docx.py            ← keep for regeneration
```



## Report rebuild (mandatory)

Write markdown to `.steps/<name>.md` (hidden), then rebuild `analysis.html` and, if this step produced a diagram, render it and reference it first with a `<!-- diagram: architecture.html -->` marker. **Full procedure, exact paths, and the rebuild command are in `context/pm-operating-system.md` §§3, 6, 11a — already loaded as mandatory context for every run, so it is not repeated here.** Never delete `.steps/*.md`, `analysis.html`, or `.steps/build_docx.py`.

## Quality Gate / Checklist (before marking complete)

Before declaring complete, verify:
- [ ] Flowchart has real diagram structure (not a toy overview) covering setup, collection with protocol branches, alert, failure
- [ ] Engineering deck includes metrics tables + OID/API/path highlights from technical analysis
- [ ] Executive/Engineering decks are immediately usable (no "fill in later" gaps); content backfilled from Steps 1–4 if needed
- [ ] Executive deck has at least 3 slides with diagrams/visuals (not all bullets)
- [ ] Executive deck has NO MORE THAN 2 consecutive bullet-only slides
- [ ] Executive deck's persona-story slide and persona-revisited slide use the same named persona
- [ ] Engineering deck has architecture and data flow diagrams embedded
- [ ] Engineering deck has NO MORE THAN 2 consecutive bullet-only slides
- [ ] PRD DOCX includes Technical Architecture section with architecture overview, data flow, decision logic, data model, and integration points
- [ ] PRD DOCX Persona Challenges table is compact (one row per challenge, no narratives)
- [ ] All diagrams and slides are specific to THIS feature (not generic placeholders)
- [ ] Color scheme is consistent across all documents
- [ ] `.steps/build_docx.py` and `.steps/diagrams/flowchart.json` kept for regeneration
- [ ] `Progress.md` updated after successful generation


## Completion

After generating all files, say:

> **Files generated!** Your deliverables are ready in `[feature-name]/`:
> - 🗺️ `architecture.html` — interactive Archify flowchart covering setup, data collection, alerting, and user interaction
> - 📊 `executive-brief.html` — executive deck with architecture diagrams and competitive visuals
> - 📊 `engineering-brief.html` — engineering deck with data flow, metrics tables, and scale charts
> - 📄 `product-requirements.docx` — Full PRD with embedded diagrams
>
> Proceed to **Step 6** (Lovable wireframe) when ready.
