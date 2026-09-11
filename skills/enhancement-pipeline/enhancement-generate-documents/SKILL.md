---
name: enhancement-generate-documents
description: "Generate the enhancement deliverables — an Archify flowchart, executive and engineering HTML slide decks, and a DOCX PRD — with professional design for enhancement work. Runs automatically right after Step 5's drafts are done — not gated on a PM command."
---

# Generate Enhancement Documents

## Purpose

Generate production-quality deliverable files from the finished Step 5 enhancement markdown drafts. You (the LLM) are the designer — you decide what diagrams, slide layouts, and document structure best communicate this specific enhancement, using the tools this repo bundles (Archify, frontend-slides, `generate_docx.py`) rather than a generic template.

## Dense deliverables bar (flowchart / slide decks / PRD)

When generating files from Step 5 drafts:

1. **Read Steps 1–4 as well as Step 5** so nothing important is lost if a draft under-specified content.
2. The engineering deck must include table slides for metrics and collection-contract highlights (OIDs/APIs/paths) from technical analysis.
3. The flowchart must be complete with the sections required by the operating system dense-deliverables bar — not a single overview toy diagram.
4. The executive deck must include concrete capabilities, competitive facts, and success metrics from prior steps.
5. If a Step 5 draft is thin, **expand content from Steps 1–4** while generating (do not ship a thin deck). Note expansions in chat.
6. Quality fail: decks that still need a human to "fill in the real points."

## Prerequisites

### Locating the tools

- **DOCX:** `generate_docx.py` lives at the repo root's `scripts/` directory — relative to this file: `../../../scripts/`. Install its dependencies once via `uv sync` from the repo root (see `scripts/pyproject.toml`).
- **Flowchart diagram:** Archify is bundled at `skills/archify/` (relative to this file: `../../archify/`). Its CLI is `bin/archify.mjs` — resolve it with `**/skills/archify/bin/archify.mjs`. No install step; it's pure Node.js.
- **Slide decks:** frontend-slides is bundled at `skills/frontend-slides/` (relative to this file: `../../frontend-slides/`). Read its `SKILL.md` for templates, animation patterns, and style presets before authoring.

## MANDATORY: Validate Before Generating

Before writing any code, verify ALL prerequisite **markdown** files exist in `[feature-name]-enhancement/.steps/`:

| File | Step |
|------|------|
| `1_current_state.md` | Step 1 — Current State Analysis |
| `2_cross_module_analysis.md` | Step 2 — Cross-Module Analysis |
| `3_competitive_analysis.md` | Step 3 — Competitive Analysis |
| `4_enhancement_findings.md` | Step 4 — Enhancement Findings |
| `5a_executive_presentation.md` | Step 5a — Executive deck |
| `5b_engineering_presentation.md` | Step 5b — Engineering deck |
| `5c_enhancement_prd.md` | Step 5c — Enhancement PRD |
| `5d_enhancement_flowchart.md` | Step 5d — Enhancement Flowchart |

**If any file is missing, STOP immediately and tell the PM:**
> "Cannot generate files. Missing: [list missing files]. Please complete these steps first."

Also check that `1_current_state.md` contains persona stories (search for "persona" or "story" or "Meet"). If missing, warn:
> "Warning: No persona stories found in current state analysis. Slide decks need persona narratives for the challenge and transformation slides."

## CRITICAL: Your Role as Designer

For each enhancement, you must:
1. **Read the finished content** from Step 5 files (5a–5d).
2. **Design the flowchart and decks** — decide what diagrams, charts, and layouts best communicate this specific enhancement.
3. Enhancement documents have a unique requirement: they must show **before vs. after** — what exists today and what changes. Use consistent semantics throughout: **existing/unchanged**, **new**, **modified** — carry this coding into the Archify diagram's node styling and into the slide decks' before/after slides alike.

## Process

### 1. Generate the Enhancement Flowchart (Archify)

Author a JSON spec at `.steps/diagrams/flowchart.json` for Archify's `workflow` type (see `skills/archify/schemas/`), then render:

```bash
node "<archify-dir>/bin/archify.mjs" deliver workflow ".steps/diagrams/flowchart.json" "architecture.html" --quality showcase --json
```

- Translate the Mermaid sketch from `5d_enhancement_flowchart.md` into the spec — this is a fresh authoring pass (new stable IDs, real domain wording), not a literal transcription.
- Mark node/edge state so the diagram visually distinguishes **existing** (unchanged), **new** (added by the enhancement), and **modified** (changed by the enhancement) — Archify's schema supports per-node/edge styling; use it instead of inventing an ad hoc legend.
- Cover: the enhanced end-to-end flow, discovery changes, data pipeline, alerting, user workflow — multiple linked views (`meta.views`) if one flat diagram can't hold all of it legibly.
- Validate before delivering: `node "<archify-dir>/bin/archify.mjs" validate workflow ".steps/diagrams/flowchart.json" --quality showcase --json` must report a showcase pass with 0 errors/warnings. A showcase pass rarely happens on the first attempt — real layout errors (edge/node crossings, label overlaps, desktop-readability failures) are normal on early drafts and come with specific fix suggestions; keep revising the spec and re-validating until it's clean, don't stop or skip the diagram after the first failure.
- Reference the output from `5d_enhancement_flowchart.md` with `<!-- diagram: architecture.html -->` so it embeds into the consolidated report (Section 6).

### 2. Generate the Executive Slide Deck (frontend-slides)

**Focus on the business case for the enhancement — why, what changes, what impact.**

Author `executive-brief.html` directly as self-contained HTML, following `skills/frontend-slides/SKILL.md`'s templates and animation patterns. Plan slide types before writing:

| Slide | Content | Why |
|-------|---------|-----|
| Title | — | Sets tone |
| Persona Pain | Quote/callout, not bullets | Emotional grounding |
| Current State vs. Gap | Two-column | What's missing today |
| Competitive | Comparison matrix | Where we close gaps |
| Quick Wins | Before/after panels | Concrete near-term value |
| Core Improvements | Icon grid, not a bullet list | Capability overview |
| Key Impact Stat | Single large number | Break up dense slides |
| Success Metrics | KPI cards | Specific, measurable |
| Timeline | Horizontal roadmap | Phasing |
| Transformation | Before/after, green/positive | Mirrors the Persona Pain slide with the resolved outcome |
| Closing | — | |

Design principles:
- These decks are read async (handoff, review), not presented live — explicitly use frontend-slides' "high density / reading-first" mode (its own SKILL.md §"How dense should the deck feel?"), not its sparse speaker-led default: 4-8 bullets or 4-6 structured cards per slide, self-contained slides that don't need a narrator. Still never more than 2 consecutive bullet-only slides — reach for a table, grid, or comparison layout instead.
- **Navigation is mandatory, not optional polish.** Every deck must ship the full navigation contract from `skills/frontend-slides/html-template.md` — keyboard (arrows, space, page up/down), mouse wheel, and visible on-screen prev/next controls — built directly into the self-contained HTML. Read `html-template.md` in full before authoring; a deck with no way to move to the next slide is incomplete, not just unpolished.
- Before/after contrasts must be visual (two-panel layout, color-coded), not just paraphrased text.
- Use frontend-slides' animation patterns deliberately on the transformation and impact slides — this is the moment a static bullet deck fails and a real presentation doesn't.
- The persona-pain slide and the transformation slide must revisit the *same* named persona from Step 1.
- Render the persona challenge resolution map from Step 4 as a comparison layout with status indicators (✅ Solved / ⚠️ Partial / ❌ Deferred).

### 3. Generate the Engineering Slide Deck (frontend-slides)

**Focus on what changes technically — architecture modifications, new metrics, migration.**

Author `engineering-brief.html` the same way. Plan:

| Slide | Content |
|-------|---------|
| Title | — |
| Persona Story | Emotional grounding |
| Current Architecture | Link/embed the flowchart's "before" view |
| Enhancement Overview | Process-flow visualization |
| New Metrics | Table (split if >8 rows) |
| Modified Metrics | Current vs. enhanced, two-column |
| Architecture Changes | Before/after diagrams |
| UI Changes | Component overview grid |
| Scalability | Performance targets as KPI cards |
| Phasing | Roadmap |

Include:
- **Before/after architecture** — pull directly from the Archify flowchart's existing/new/modified node coding rather than re-drawing it.
- **New metrics tables** — categories, thresholds, collection methods.
- **Modified component highlights** — color-coded to match the flowchart's semantics.
- **Cross-module reuse** — showing borrowed components (from Step 2).

### 4. Generate the Enhancement PRD (DOCX)

Professional document with:
- Styled heading hierarchy, formatted tables with colored headers.
- A real Table of Contents (`DocxBuilder.add_table_of_contents()` + `add_heading()` — every heading links automatically, no manual "Update Field" step needed).
- **A short plain-language intro (2-4 sentences, wait-what-style: plain words, no unexplained jargon) before every major section's tables** — this document must read as a narrative with supporting tables, not a wall of tables with no framing.
- Current-vs-enhanced comparison tables with color coding matching the flowchart/decks.
- **Technical Architecture Changes section** (Section 3) with an embedded architecture image, decision logic changes, data model changes, and integration point changes. This image is a **simple static diagram rendered with `matplotlib`** purpose-built for the printed page — Archify's output is interactive HTML and isn't meant to be screenshotted into a document; draw a lightweight equivalent instead, using the same existing/new/modified color coding.
- New metrics specification tables.
- Page numbers, headers.
- Enhancement scope summary on page 1.
- **Persona Challenges section** (Section 2.3) as a COMPACT reference table — not multi-paragraph narratives.
- **Persona Challenge Traceability section** (Section 10) as a compact cross-reference table.
- **Functional requirement tables** must include "Current Behavior → Enhanced Behavior" columns.
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
3. Reads content from `.steps/` Step 5 markdown files (5a–5d), and Steps 1–4 for backfill when drafts are thin.
4. Renders the small matplotlib architecture image as an intermediate PNG under `.steps/diagrams/`.
5. Assembles `product-requirements.docx` at the topic-folder root.

Then run it:
```bash
cd "[feature-name]-enhancement" && python .steps/build_docx.py
```

**Keep `.steps/build_docx.py` after success** so the PM can regenerate without rewriting the designer script. Only rewrite it when content or layout must change.

If unsure of the absolute path, resolve it with `file_search` for `**/generate_docx.py`.

## Output

```
[feature-name]-enhancement/
├── architecture.html          ← Archify diagram (existing/new/modified coding)
├── executive-brief.html       ← executive deck (frontend-slides)
├── engineering-brief.html     ← engineering deck (frontend-slides)
├── product-requirements.docx  ← enhancement PRD
└── .steps/
    ├── diagrams/flowchart.json  ← Archify source spec
    └── build_docx.py            ← keep for regeneration
```


## Report rebuild (mandatory)

Write markdown to `.steps/<name>.md` (hidden), then rebuild `analysis.html` and, if this step produced a diagram, render it and reference it first with a `<!-- diagram: architecture.html -->` marker. **Full procedure, exact paths, and the rebuild command are in `context/pm-operating-system.md` §§3, 6, 11a — already loaded as mandatory context for every run, so it is not repeated here.** Never delete `.steps/*.md`, `analysis.html`, or `.steps/build_docx.py`.

## Quality Gate (before marking complete)

Gate ledger for this step — write `.steps/GATES-5-render.md` from `skills/unlazy-gates/templates/gates-leaf.md` before producing this step's content, one gate per item below. Resolution rule (self-correct on a failed gate, document the gap and continue — never abandon, never pause): `context/pm-operating-system.md` §18.


- [ ] G1: Flowchart has real diagram structure with existing/new/modified coding, not 5 generic boxes
  (manual — no command can decide this)
- [ ] G2: Executive deck has before/after visuals (not just bullets)
  (manual — no command can decide this)
- [ ] G3: Executive deck has NO MORE THAN 2 consecutive bullet-only slides
  (manual — no command can decide this)
- [ ] G4: Executive deck's persona-pain slide and transformation slide revisit the same named persona
  (manual — no command can decide this)
- [ ] G5: Engineering deck has architecture diagrams showing modifications
  (manual — no command can decide this)
- [ ] G6: Engineering deck has NO MORE THAN 2 consecutive bullet-only slides
  (manual — no command can decide this)
- [ ] G7: Enhancement PRD includes Technical Architecture Changes section with architecture, decision logic, data model, and integration changes
  (manual — no command can decide this)
- [ ] G8: Enhancement PRD Persona Challenges table is compact (one row per challenge, no narratives)
  (manual — no command can decide this)
- [ ] G9: New metrics tables are legible and complete
  (manual — no command can decide this)
- [ ] G10: Color coding is consistent everywhere: existing=green, new=blue, modified=orange
  (manual — no command can decide this)
- [ ] G11: All diagrams and slides are specific to THIS enhancement (not generic placeholders)
  (manual — no command can decide this)
- [ ] G12: `.steps/build_docx.py` and `.steps/diagrams/flowchart.json` kept for regeneration
  CHECK: node -e "const fs=require('fs');process.exit(fs.existsSync('.steps/build_docx.py')&&fs.existsSync('.steps/diagrams/flowchart.json')?0:1)"
  EXPECT: (exits zero)
- [ ] G13: All four rendered deliverables exist (`architecture.html`, `executive-brief.html`, `engineering-brief.html`, `product-requirements.docx`)
  CHECK: node -e "const fs=require('fs');process.exit(['architecture.html','executive-brief.html','engineering-brief.html','product-requirements.docx'].every(f=>fs.existsSync(f))?0:1)"
  EXPECT: (exits zero)
- [ ] G14: `Progress.md` updated after successful generation
  CHECK: node -e "const fs=require('fs');process.exit(fs.statSync('Progress.md').mtimeMs>=fs.statSync('product-requirements.docx').mtimeMs?0:1)"
  EXPECT: (exits zero)
## Completion

After generating all files, say:

> **Files generated!** Your enhancement deliverables are ready in `[feature-name]-enhancement/`:
> - 🗺️ `architecture.html` — interactive Archify flowchart with color-coded existing/new/modified steps
> - 📊 `executive-brief.html` — executive deck with before/after visuals and competitive gap diagrams
> - 📊 `engineering-brief.html` — engineering deck with architecture changes, new metrics tables, and reuse diagrams
> - 📄 `product-requirements.docx` — Full enhancement PRD with embedded diagrams
>
> Rebuild `analysis.html`, then continue immediately to Step 6 — Wireframe.
