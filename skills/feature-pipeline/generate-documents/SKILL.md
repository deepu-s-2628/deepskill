---
name: generate-documents
description: "Generate production-quality PPTX, PDF, and DOCX files with professional design, embedded diagrams, and visual layouts for OpManager Plus feature documents. Runs automatically right after Step 5's drafts are done — not gated on a PM command."
---

# Generate Documents

## Purpose

Generate production-quality deliverable files with **proper visual design** — not templated bullet dumps. You (the LLM) are the designer. You write custom Python code for each feature that produces visually appealing, professionally designed output.


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

Before writing any code, verify ALL prerequisite **markdown** files exist in `ITOM-PM-Result/[feature-name]/.steps/`:

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

Do NOT just call a generic template script. For each feature, you must:
1. **Read the finished content** from Step 5 files
2. **Design the visuals** — decide what diagrams, charts, layouts, and images best communicate this specific feature
3. **Write a custom `build_documents.py`** script in `ITOM-PM-Result/[feature-name]/Generated/` that generates all files with tailored visuals
4. **Run it** to produce the final files

You have full creative control. Use your understanding of the feature to design diagrams, architecture visuals, comparison charts, and flowcharts that are SPECIFIC to this feature — not generic placeholders.

## Process

### 1. Generate Flowchart PDF

**This is a real visual flowchart, not Mermaid code in a PDF.**

Write Python code using `graphviz` to render actual flowchart diagrams:
- Proper boxes, diamonds (decisions), arrows with labels
- Color coding: green for start/end, blue for processes, orange for decisions, red for alerts
- Multiple pages if needed (overview flow, setup flow, data pipeline, alert flow)
- Professional styling: rounded rectangles, proper spacing, legible fonts
- Export as PDF with multiple pages

Reference the Mermaid logic from `5c_feature_flowchart.md` but render it as a proper visual diagram — translate the Mermaid into graphviz dot language or draw it with matplotlib patches.

Example approach:
```python
from graphviz import Digraph

dot = Digraph('Feature Flow', format='pdf')
dot.attr(rankdir='TB', size='11,8', dpi='150')
dot.attr('node', shape='box', style='rounded,filled', fillcolor='#E3F2FD', fontname='Segoe UI')
dot.attr('edge', fontname='Segoe UI', fontsize='10')

# Design the actual flowchart based on the feature's logic
dot.node('start', 'Device Discovery', shape='oval', fillcolor='#C8E6C9')
dot.node('collect', 'Collect Metrics via API', fillcolor='#E3F2FD')
dot.node('decision', 'Threshold\nExceeded?', shape='diamond', fillcolor='#FFF3E0')
# ... design the full flow
```

### 2. Generate Executive PPTX

**This must be visually compelling for a Product Director presentation.**

**MANDATORY LAYOUT DIVERSITY RULE:** Never use more than 2 consecutive `add_content_slide()` (bullet) slides. At least 30% of slides must be non-bullet layouts. Plan slide types BEFORE writing code:

| Slide | Recommended Method | Why |
|-------|-------------------|-----|
| Title | `add_title_slide()` | Dark background with brand accent |
| Persona Story (Slide 2) | `add_quote_slide()` | Emotional callout — NOT bullets |
| Opportunity/Gap | `add_two_column_slide()` | Problem vs. Solution split |
| Competitive | `add_comparison_slide()` | Color-coded matrix with highlight column |
| Approach | `add_process_flow_slide()` | Connected steps visualization |
| Capabilities | `add_icon_grid_slide()` | 2x3 or 3x3 grid with icons — NOT bullet list |
| Key Stat | `add_stat_slide()` | Single powerful number — use between dense slides |
| Metrics/KPIs | `add_kpi_slide()` | Large numbers with color-coded cards |
| Timeline | `add_timeline_slide()` | Horizontal roadmap with milestone circles |
| Persona Revisited (Slide 11) | `add_before_after_slide()` | Before/after panels with arrow divider |
| Closing | `add_closing_slide()` | Dark background with brand accent |

Design slides that include:
- **Architecture diagrams** — drawn using python-pptx shapes (boxes, arrows, connectors) showing how the feature fits into OpManager Plus
- **Comparison visuals** — matrices, Harvey balls, or color-coded tables for competitive comparison
- **KPI/metric callout cards** — large numbers with icons showing key stats
- **Process flow mini-diagrams** — simplified versions embedded in slides
- **Gradient backgrounds** on key slides, not just flat colors
- **Icon-like shapes** representing concepts (monitor, alert bell, network node)

Slide design principles:
- Max 4-5 bullet points per slide, large font
- Use the full slide canvas — don't crowd everything top-left
- Diagrams should be CENTER of attention on diagram slides
- Use visual hierarchy: title → key visual → supporting text
- Brand colors: `#0078d4` (blue), `#1a1a2e` (navy), `#28a745` (green), `#fd7e14` (orange)
- **Slide 2 (The Challenge):** Use a persona quote callout box with a highlighted background — this slide must feel human, not data-driven. Use `add_stat_slide()` or a custom callout shape for the persona story.
- **Slide 11 (The Transformation):** Mirror Slide 2's layout but with green/positive coloring. Use `add_before_after_slide()` to contrast the pain vs. resolution.
- **Persona Challenge Traceability:** If the PRD includes a persona challenge traceability table, render it as a formatted `add_comparison_slide()` with status indicators showing which challenges are solved.

### 3. Generate Engineering PPTX

**This must be technically detailed but visually clear for engineers.**

**MANDATORY LAYOUT DIVERSITY RULE:** Same as executive — never more than 2 consecutive bullet slides. Plan:

| Slide | Recommended Method | Why |
|-------|-------------------|-----|
| Title | `add_title_slide()` | Dark background |
| Persona Story (Slide 2) | `add_quote_slide()` | Emotional grounding |
| Technology Overview | `add_two_column_slide()` | Concept vs. Implementation |
| Data Collection | `add_process_flow_slide()` | Pipeline visualization |
| Architecture | `add_image_slide()` | Generated architecture diagram |
| Metrics | `add_table_slide()` | Formatted table (split if >8 rows) |
| Scalability | `add_kpi_slide()` | Performance targets as KPI cards |
| Phasing | `add_timeline_slide()` | Horizontal roadmap |
| UI Components | `add_icon_grid_slide()` | Screen overview grid |

Include programmatically generated:
- **Data flow diagrams** — boxes and arrows showing Device → Polling Engine → DB → UI
- **Metric tables** — formatted with alternating colors, severity indicators
- **Architecture diagrams** — showing new components vs. existing (color coded)
- **Protocol sequence diagrams** — showing request/response flow
- **Scale projection charts** — matplotlib bar/line charts embedded as images

For complex diagrams, generate them as PNG with matplotlib/graphviz first, then embed in the slide.

### 4. Generate PRD DOCX

Professional document with:
- Styled heading hierarchy
- Formatted tables with colored headers
- Embedded diagrams (same as engineering PPT, reused)
- Page numbers, headers, table of contents placeholder
- Metric specification tables with proper formatting
- **Technical Architecture section** (Section 3) with embedded architecture diagram, data flow, decision logic, data model, and integration points
- **Persona Challenges section** (Section 2.2) as a COMPACT reference table — not multi-paragraph narratives
- **Persona Challenge Traceability section** (Section 9) as a compact cross-reference table
- **Use Cases table** should be concise — no "Persona Challenge Addressed" column (personas are tracked in Section 9)

### 5. Write and Run the Build Script

Create `ITOM-PM-Result/[feature-name]/Generated/build_documents.py` that:
1. Resolves the scripts directory (repo root's `scripts/`) and adds it to `sys.path`:
   ```python
   import sys
   SCRIPTS_DIR = "<repo-root>/scripts"
   sys.path.insert(0, SCRIPTS_DIR)
   ```
2. Imports and uses `generate_pptx.PresentationBuilder`, `generate_flowchart.FlowchartBuilder`, `generate_docx.DocxBuilder`
3. Reads content from `.steps/` Step 5 markdown files (and backfill from Steps 1–4 when drafts are thin)
4. Generates diagrams as PNG/SVG intermediates
5. Assembles the PPTX files with embedded visuals
6. Creates the flowchart PDF
7. Creates the PRD DOCX with embedded diagrams
8. Saves all to the Generated/ folder

Then run it:
```bash
cd "ITOM-PM-Result/[feature-name]/Generated"
python build_documents.py
```

**Keep `build_documents.py` after success** so the PM can regenerate without rewriting the designer script. Only rewrite it when content or layout must change. Optionally add `Generated/README.md` with the regenerate command and script-path notes.

If unsure of the absolute path, resolve it with `file_search` for `**/generate_pptx.py`.

## Output

```
ITOM-PM-Result/[feature-name]/Generated/
├── diagrams/                    ← Intermediate diagram PNGs
│   ├── architecture.png
│   ├── data_flow.png
│   ├── comparison_matrix.png
│   └── scale_chart.png
├── build_documents.py           ← keep for regeneration
├── executive_presentation.pptx
├── engineering_presentation.pptx
├── feature_flowchart.pdf
└── product_requirements.docx
```



## Report rebuild (mandatory)

Every step artifact this skill writes must:

1. **Markdown (source of truth, hidden):** `ITOM-PM-Result/[slug]/.steps/<name>.md`
   - Enhancement mode: `ITOM-PM-Result/[slug]-enhancement/.steps/<name>.md`
2. **Rebuild the consolidated report** immediately after:
   ```bash
   python "<scripts-dir>/build_report.py" "ITOM-PM-Result/[slug]/"
   ```
   Resolve helper via `**/build_report.py` (`scripts/`).
3. If this step produced a diagram worth showing, reference it first with a `<!-- diagram: Generated/diagrams/<name>.html -->` marker in the markdown, then rebuild.
4. On revise, rewrite the markdown and rebuild the report again.
5. Final chat summary (end of the whole run) cites the **`report.html`** path.
6. **Never delete** `.steps/*.md`, `report.html`, or `Generated/build_documents.py` after PPTX/PDF/DOCX generation.

See `context/pm-operating-system.md` sections 3, 6, and 11–13.


## Quality Gate / Checklist (before marking complete)

Before declaring complete, verify:
- [ ] Flowchart PDF has actual visual diagrams (not code text)
- [ ] Flowchart is multi-page/detail-complete (setup, collection with protocol branches, alert, failure) — not a toy overview
- [ ] Engineering PPTX includes metrics tables + OID/API/path highlights from technical analysis
- [ ] Executive/Engineering PPTX are immediately usable (no "fill in later" gaps); content backfilled from Steps 1–4 if needed
- [ ] Executive PPT has at least 3 slides with diagrams/visuals (not all bullets)
- [ ] Executive PPT has NO MORE THAN 2 consecutive bullet slides
- [ ] Executive PPT uses at least 4 different slide types (content, two-column, KPI, icon-grid, comparison, timeline, etc.)
- [ ] Executive PPT Slide 2 has a persona story callout (not generic problem statement)
- [ ] Executive PPT Slide 11 revisits the same persona with the transformed outcome
- [ ] Engineering PPT has architecture and data flow diagrams embedded
- [ ] Engineering PPT has NO MORE THAN 2 consecutive bullet slides
- [ ] Engineering PPT uses at least 4 different slide types
- [ ] Engineering PPT Slide 2 has a persona story grounding the technical work
- [ ] PRD DOCX includes Technical Architecture section with architecture overview, data flow, decision logic, data model, and integration points
- [ ] PRD DOCX Persona Challenges table is compact (one row per challenge, no narratives)
- [ ] All diagrams are specific to THIS feature (not generic placeholders)
- [ ] Color scheme is consistent across all documents
- [ ] Text is legible (minimum 14pt on slides, 10pt in tables)
- [ ] At least 30% of presentation slides are non-bullet layouts
- [ ] `Generated/build_documents.py` kept for regeneration (not deleted)
- [ ] `STATUS.md` updated after successful generation

- [ ] `.steps/` markdown written, `report.html` rebuilt
- [ ] Markdown under `.steps/`; HTML under `steps/`; never delete either or Generated artifacts


## Completion

After generating all files, say:

> **Files generated!** Your deliverables are ready in `ITOM-PM-Result/[feature-name]/Generated/`:
> - 📊 `executive_presentation.pptx` — [N] slides with architecture diagrams and competitive visuals
> - 📊 `engineering_presentation.pptx` — [N] slides with data flow, metrics tables, and scale charts
> - 📋 `feature_flowchart.pdf` — [N]-page visual flowchart covering setup, data collection, alerting, and user interaction
> - 📄 `product_requirements.docx` — Full PRD with embedded diagrams
>
> Proceed to **Step 6** (Lovable wireframe) when ready.
