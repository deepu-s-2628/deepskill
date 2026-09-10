---
name: enhancement-generate-documents
description: "Generate production-quality PPTX, PDF, and DOCX files with professional design for enhancement deliverables. Use when the PM says 'generate files' after approving Step 5 enhancement deliverables."
---

# Generate Enhancement Documents

## Purpose

Generate production-quality deliverable files from the approved Step 5 enhancement markdown drafts. You (the LLM) are the designer — write custom Python code for this specific enhancement that produces visually appealing, professionally designed output.


## Dense binary bar (PPTX / flowchart PDF)

When generating files from Step 5 drafts:

1. **Read Steps 1–4 as well as Step 5** so nothing important is lost if a draft under-specified a slide.
2. Engineering PPTX must include table slides for metrics and collection-contract highlights (OIDs/APIs/paths) from technical analysis.
3. Flowchart PDF must be multi-page with the sections required by the operating system dense-deliverables bar — not a single overview toy diagram.
4. Executive PPTX must include concrete capabilities, competitive facts, and success metrics from prior steps.
5. If a Step 5 draft is thin, **expand content from Steps 1–4** while generating (do not ship a thin deck). Note expansions in chat.
6. Quality fail: decks that still need a human to “fill in the real points.”

## Prerequisites

### Locating the utility scripts

The generation scripts (`generate_pptx.py`, `generate_flowchart.py`, `generate_docx.py`) live at the repo root's `scripts/` directory — relative to this file: `../../../scripts/`.

Install dependencies once via `uv sync` from the repo root (see `scripts/pyproject.toml`).

## MANDATORY: Validate Before Generating

Before writing any code, verify ALL prerequisite **markdown** files exist in `ITOM-PM-Result/[feature-name]-enhancement/.steps/`:

| File | Step |
|------|------|
| `1_current_state.md` | Step 1 — Current State Analysis |
| `2_cross_module_analysis.md` | Step 2 — Cross-Module Analysis |
| `3_competitive_analysis.md` | Step 3 — Competitive Analysis |
| `4_enhancement_findings.md` | Step 4 — Enhancement Findings |
| `5a_executive_presentation.md` | Step 5a — Executive PPT |
| `5b_engineering_presentation.md` | Step 5b — Engineering PPT |
| `5c_enhancement_prd.md` | Step 5c — Enhancement PRD |
| `5d_enhancement_flowchart.md` | Step 5d — Enhancement Flowchart |

**If any file is missing, STOP immediately and tell the PM:**
> "Cannot generate files. Missing: [list missing files]. Please complete these steps first."

Also check that `1_current_state.md` contains persona stories (search for "persona" or "story" or "Meet"). If missing, warn:
> "Warning: No persona stories found in current state analysis. Presentations need persona narratives for Slides 2 and 12."

## CRITICAL: Your Role as Designer

Do NOT just call a generic template script. For each enhancement, you must:
1. **Read the approved content** from Step 5 files (5a–5d)
2. **Design the visuals** — decide what diagrams, charts, layouts, and images best communicate this specific enhancement
3. **Write a custom `build_documents.py`** script in `ITOM-PM-Result/[feature-name]-enhancement/Generated/` that generates all files with tailored visuals
4. **Run it** to produce the final files

Enhancement documents have a unique requirement: they must show **before vs. after** — what exists today and what changes. Use color coding consistently: green=existing/keep, blue=new, orange=modified.

## Process

### 1. Generate Enhancement Flowchart PDF

**This is a real visual flowchart, not Mermaid code in a PDF.**

Write Python code using `graphviz` to render actual flowchart diagrams:
- Translate Mermaid from `5d_enhancement_flowchart.md` into graphviz dot language
- Color coding for enhancement context:
  - **Green** nodes/edges: existing steps (unchanged)
  - **Blue** nodes/edges: new steps (added by enhancement)
  - **Orange** nodes/edges: modified steps (changed by enhancement)
  - **Red**: alert/error paths
- Include before/after comparison diagrams
- Multiple pages: enhanced end-to-end flow, discovery changes, data pipeline, alerting, user workflow
- Professional styling: rounded rectangles, proper spacing, legible fonts
- Export as PDF

Example approach:
```python
from graphviz import Digraph

dot = Digraph('Enhanced Feature Flow', format='pdf')
dot.attr(rankdir='TB', size='11,8', dpi='150')

# Existing steps (green)
dot.node('existing1', 'Current Discovery', style='rounded,filled', fillcolor='#C8E6C9', color='#388E3C')

# Modified steps (orange)
dot.node('modified1', 'Enhanced Polling\n(+new metrics)', style='rounded,filled', fillcolor='#FFF3E0', color='#F57C00', penwidth='3')

# New steps (blue, dashed)
dot.node('new1', 'New Dashboard Widget', style='rounded,filled,dashed', fillcolor='#E3F2FD', color='#1976D2')
```

### 2. Generate Executive Enhancement PPTX

**Focus on the business case for the enhancement — why, what changes, what impact.**

**MANDATORY LAYOUT DIVERSITY RULE:** Never use more than 2 consecutive `add_content_slide()` (bullet) slides. At least 30% of slides must be non-bullet layouts. Plan slide types BEFORE writing code:

| Slide | Recommended Method | Why |
|-------|-------------------|-----|
| Title | `add_title_slide()` | Dark background with brand accent |
| Persona Pain (Slide 2) | `add_quote_slide()` | Emotional callout — NOT bullets |
| Current State/Gap | `add_two_column_slide()` | Current vs. Missing split |
| Competitive | `add_comparison_slide()` | Color-coded matrix |
| Quick Wins | `add_before_after_slide()` | Before/after panels |
| Core Improvements | `add_icon_grid_slide()` | 2x3 grid — NOT bullet list |
| Key Impact Stat | `add_stat_slide()` | Single powerful number |
| Success Metrics | `add_kpi_slide()` | Large numbers with color cards |
| Timeline | `add_timeline_slide()` | Horizontal roadmap |
| Transformation (Slide 12) | `add_before_after_slide()` | Before/after with green positive |
| Closing | `add_closing_slide()` | Dark background |

Design slides that include:
- **Before/after comparison visuals** — showing current state vs. enhanced state
- **Competitive gap diagrams** — matrices or positioning maps showing where we close gaps
- **Impact callout cards** — large numbers showing expected improvement
- **Enhancement roadmap timeline** — visual phasing (quick wins → core → strategic)
- **Cross-module benefit diagram** — showing ripple effects

Slide design principles:
- Max 4-5 bullet points per slide, large font
- Use the full slide canvas
- Before/after contrasts should be visual, not just text
- Brand colors: `#0078d4` (blue), `#1a1a2e` (navy), `#28a745` (green), `#fd7e14` (orange)
- **Slide 2 (The Challenge Today):** Use a persona quote callout box with a highlighted background. Use `add_stat_slide()` or a custom callout shape for the persona pain story.
- **Slide 12 (The Transformation):** Mirror Slide 2's layout with green/positive coloring. Use `add_before_after_slide()` to contrast the current pain vs. enhanced outcome.
- **Persona Challenge Resolution:** Render the persona challenge resolution map from Step 4 as a `add_comparison_slide()` with status indicators (✅ Solved / ⚠️ Partial / ❌ Deferred).

### 3. Generate Engineering Enhancement PPTX

**Focus on what changes technically — architecture modifications, new metrics, migration.**

**MANDATORY LAYOUT DIVERSITY RULE:** Same as executive — never more than 2 consecutive bullet slides. Plan:

| Slide | Recommended Method | Why |
|-------|-------------------|-----|
| Title | `add_title_slide()` | Dark background |
| Persona Story (Slide 2) | `add_quote_slide()` | Emotional grounding |
| Current Architecture | `add_image_slide()` | Generated diagram |
| Enhancement Overview | `add_process_flow_slide()` | Connected steps |
| New Metrics | `add_table_slide()` | Split if >8 rows |
| Modified Metrics | `add_two_column_slide()` | Current vs. Enhanced |
| Architecture Changes | `add_before_after_slide()` | Before/after diagrams |
| UI Changes | `add_icon_grid_slide()` | Component overview |
| Scalability | `add_kpi_slide()` | Performance targets |
| Phasing | `add_timeline_slide()` | Roadmap |

Include programmatically generated:
- **Before/after architecture diagrams** — showing existing vs. enhanced data flow
- **New metrics tables** — formatted with categories, thresholds, collection methods
- **Modified component highlights** — color-coded to show what's changed
- **Data model change diagrams** — schema modifications
- **Cross-module reuse diagram** — showing borrowed components

For complex diagrams, generate as PNG with matplotlib/graphviz first, then embed in slides.

### 4. Generate Enhancement PRD DOCX

Professional document with:
- Styled heading hierarchy
- Formatted tables with colored headers
- Current-vs-enhanced comparison tables with color coding
- **Technical Architecture Changes section** (Section 3) with embedded architecture diagram, decision logic changes, data model changes, and integration point changes
- New metrics specification tables
- Embedded diagrams (reuse from engineering PPT)
- Page numbers, headers
- Enhancement scope summary on page 1
- **Persona Challenges section** (Section 2.3) as a COMPACT reference table — not multi-paragraph narratives
- **Persona Challenge Traceability section** (Section 10) as a compact cross-reference table
- **Functional requirement tables** must include "Current Behavior → Enhanced Behavior" columns

### 5. Write and Run the Build Script

Create `ITOM-PM-Result/[feature-name]-enhancement/Generated/build_documents.py` that:
1. Resolves the scripts directory (repo root's `scripts/`) and adds it to `sys.path`:
   ```python
   import sys
   SCRIPTS_DIR = "<repo-root>/scripts"
   sys.path.insert(0, SCRIPTS_DIR)
   ```
2. Uses `generate_pptx.PresentationBuilder` for slide creation
3. Uses `generate_flowchart.FlowchartBuilder` for visual flowcharts
4. Uses `generate_docx` utilities for document formatting
5. Reads content from `.steps/` Step 5 markdown files (and backfill from Steps 1–4 when drafts are thin) (5a–5d)
6. Generates intermediate diagram PNGs
7. Assembles all four output files
8. Saves to the Generated/ folder

Then run it:
```bash
cd "ITOM-PM-Result/[feature-name]-enhancement/Generated"
python build_documents.py
```

**Keep `build_documents.py` after success** so the PM can regenerate without rewriting the designer script. Only rewrite it when content or layout must change. Optionally add `Generated/README.md` with the regenerate command and script-path notes.

If unsure of the absolute path, resolve it with `file_search` for `**/generate_pptx.py`.

## Output

```
ITOM-PM-Result/[feature-name]-enhancement/Generated/
├── diagrams/                           ← Intermediate diagram PNGs
│   ├── current_architecture.png
│   ├── enhanced_architecture.png
│   ├── competitive_comparison.png
│   ├── enhancement_roadmap.png
│   └── cross_module_reuse.png
├── build_documents.py                  ← keep for regeneration
├── executive_presentation.pptx
├── engineering_presentation.pptx
├── enhancement_flowchart.pdf
└── enhancement_prd.docx
```



## Dual output: hidden MD + visible HTML (mandatory)

Every step artifact this skill writes must be dual-format:

1. **Markdown (source of truth, hidden):** `ITOM-PM-Result/[slug]/.steps/<name>.md`
   - Enhancement mode: `ITOM-PM-Result/[slug]-enhancement/.steps/<name>.md`
2. **HTML (human review, visible):** `ITOM-PM-Result/[slug]/steps/<name>.html`
   - Same basename; always under visible `steps/` (never put `.md` here).
3. Generate HTML after markdown is final:
   ```bash
   python "<scripts-dir>/md_to_html.py"      "ITOM-PM-Result/[slug]/.steps/<name>.md"      "ITOM-PM-Result/[slug]/steps/<name>.html"
   ```
   Resolve helper via `**/md_to_html.py` (`scripts/`).
4. On revise, regenerate **both**.
5. Chat summary must cite the **HTML path first** (what reviewers open).
6. **Never delete** `.steps/*.md`, `steps/*.html`, or `Generated/build_documents.py` after PPTX/PDF/DOCX generation.

See `context/pm-operating-system.md` sections 3, 6, and 11–13.


## Quality Gate / Checklist (before marking complete)

Before declaring complete, verify:
- [ ] Flowchart PDF has actual visual diagrams with green/blue/orange color coding
- [ ] Executive PPT has before/after visuals (not just bullets)
- [ ] Executive PPT has NO MORE THAN 2 consecutive bullet slides
- [ ] Executive PPT uses at least 4 different slide types (content, two-column, KPI, before-after, comparison, timeline, etc.)
- [ ] Executive PPT Slide 2 has a persona pain story callout (not generic gap list)
- [ ] Executive PPT Slide 12 revisits the same persona with the enhanced outcome
- [ ] Engineering PPT has architecture diagrams showing modifications
- [ ] Engineering PPT has NO MORE THAN 2 consecutive bullet slides
- [ ] Engineering PPT uses at least 4 different slide types
- [ ] Engineering PPT Slide 2 has a persona story grounding the technical work
- [ ] Enhancement PRD includes Technical Architecture Changes section with architecture, decision logic, data model, and integration changes
- [ ] Enhancement PRD Persona Challenges table is compact (one row per challenge, no narratives)
- [ ] New metrics tables are legible and complete
- [ ] Color coding is consistent: green=existing, blue=new, orange=modified
- [ ] All diagrams are specific to THIS enhancement (not generic placeholders)
- [ ] Text is legible (minimum 14pt on slides, 10pt in tables)
- [ ] At least 30% of presentation slides are non-bullet layouts
- [ ] `Generated/build_documents.py` kept for regeneration (not deleted)
- [ ] `STATUS.md` updated after successful generation

- [ ] HTML twin written under visible `steps/`; markdown under hidden `.steps/`
- [ ] Markdown under `.steps/`; HTML under `steps/`; never delete either or Generated artifacts


## Completion

After generating all files, say:

> **Files generated!** Your enhancement deliverables are ready in `ITOM-PM-Result/[feature-name]-enhancement/Generated/`:
> - 📊 `executive_presentation.pptx` — [N] slides with before/after visuals and competitive gap diagrams
> - 📊 `engineering_presentation.pptx` — [N] slides with architecture changes, new metrics tables, and reuse diagrams
> - 📋 `enhancement_flowchart.pdf` — [N]-page visual flowchart with color-coded existing/new/modified steps
> - 📄 `enhancement_prd.docx` — Full enhancement PRD with embedded diagrams
>
>
> Reply **'proceed'** to continue to Step 6 (Wireframe).
