---
name: lovable-wireframe
description: "Step 6 of PM Feature Pipeline, opt-in after Step 5's documents are ready: produce a detailed Lovable wireframe prompt and/or a static-HTML prototype.html mockup of the primary screen, per the PM's choice."
---

# Step 6 — Lovable Wireframe Prompt

## Purpose

Produce a comprehensive, ready-to-paste prompt for Lovable that will generate a complete wireframe/prototype of this feature as it would appear inside OpManager Plus.

**This step only runs when the PM has opted into it.** The orchestrator asks once, right after Step 5 and document generation finish, whether the PM wants the Lovable prompt, the static prototype, both, or neither (`pm-shared/context/pm-operating-system.md` §8). Draft the spec below in full regardless of which of A/B/C was chosen — it's the shared source `prototype.html` reuses, so there's no wasted work — but only render `prototype.html` if the choice includes it, and shape the Completion message (below) to what was actually chosen.

## Input

Read all prior step files, particularly:
- `[feature-name]/.steps/1_brainstorm.md` — persona challenges (the wireframe must visually solve these)
- `[feature-name]/.steps/4_feature_definition.md` — screens, user flows, settings
- `[feature-name]/.steps/3_technical_analysis.md` — metrics and data points
- `[feature-name]/.steps/5d_product_requirements.md` — requirements detail
- [context/product-context.md](pm-shared/context/product-context.md) — product UI patterns

**CRITICAL: Design for the personas.** The wireframe should make each persona's challenge obviously solvable. When you define dashboards, think: "If Priya opened this at 6 AM, would she immediately see the degraded SD-WAN tunnel?" When you define alerting UI, think: "Would Marcus get the compliance data he needs from this view?" Walk through each persona's bad-day scenario and ensure the wireframe prevents it.

## Process

### 1. Map Complete Navigation Structure

Define exactly where this feature lives in OpManager Plus's navigation and how users get to every screen.

### 2. Define Every Screen in Full Detail

For each screen:
- Exact layout (header, sidebar, content areas)
- Every widget with its data, chart type, and interactivity
- All tables with columns, sorting, filtering
- All buttons, dropdowns, toggles, and their actions
- Empty states, loading states, error states

### 3. Specify Metrics Display

For each metric shown in the UI:
- Display name, value format, unit
- Visualization type (gauge, line chart, sparkline, number)
- Where it appears (which screen, which widget)
- Color coding / status thresholds

### 4. Define Settings & Configuration Screens

Full detail on every settings page:
- Form fields, labels, validation
- Default values
- Help text / tooltips

### 5. Design Tone Guidance

Give Lovable clear direction on visual style matching OpManager Plus.

## Output Format

Write to `[feature-name]/.steps/6_lovable_wireframe.md`:

```markdown
# Lovable Wireframe Prompt: [Feature Name] for OpManager Plus

## Project Overview
Build a fully navigable wireframe/prototype for the [Feature Name] feature within OpManager Plus, a full-stack IT infrastructure monitoring tool.

## Design System & Visual Guidelines
- **Style:** Enterprise IT monitoring tool — data-dense but clean and scannable
- **Color scheme:** Dark sidebar (#1a1a2e or similar), white/light content area, ManageEngine brand blue (#0078d4) for primary actions
- **Typography:** System fonts, clear hierarchy (large numbers for KPIs, readable tables)
- **Status colors:** Green = healthy/normal, Yellow/Orange = warning, Red = critical, Grey = unknown/inactive
- **Layout pattern:** Left sidebar navigation, top header with breadcrumbs, main content area with configurable dashboard grid
- **Responsive:** Desktop-first (1920x1080 primary), must work at 1366x768

## Global Navigation Changes
[Where this feature appears in the main navigation]
- Sidebar: [Location in nav tree]
- Breadcrumb pattern: Home > [Section] > [Feature] > [Detail]

## Screens to Build

### Screen 1: [Name] — [Purpose]
**URL pattern:** `/[feature]/dashboard`
**Purpose:** [What this screen is for]

**Header:**
- Breadcrumb: [path]
- Page title: [title]
- Action buttons: [list buttons and what they do]

**Layout:** [Describe grid — e.g., "3-column top row of KPI cards, full-width chart below, table at bottom"]

**Components:**
| Component | Position | Type | Data | Interactions |
|-----------|----------|------|------|-------------|
| [Name] | [Grid position] | [Card/Chart/Table/Widget] | [What data it shows] | [Click, hover, filter actions] |

**Table: [Table Name]**
| Column | Data | Sortable | Filterable | Click Action |
|--------|------|----------|-----------|-------------|
| [Col] | [Data] | Yes/No | Yes/No | [Action or none] |

**Empty state:** [What shows when no data]
**Loading state:** [Skeleton/spinner behavior]

---

### Screen 2: [Name]
[Same detailed structure]

---

### Screen 3: [Name]
[Same detailed structure]

---

[Continue for ALL screens]

## Settings & Configuration Screens

### Setup Wizard
**Steps:** [Number of steps]

**Step 1: [Name]**
| Field | Type | Label | Placeholder | Validation | Default | Required |
|-------|------|-------|-------------|-----------|---------|----------|
| [field] | [text/select/toggle/etc] | [Label] | [Placeholder] | [Rules] | [Default] | Yes/No |

**Step 2: [Name]**
[Same format]

### Settings Page
[Full detail on ongoing settings with same field-level format]

## Interactive Elements

### Filters
| Filter | Type | Options | Default | Applies To |
|--------|------|---------|---------|-----------|
| [Filter] | [Dropdown/Date/Toggle] | [Options] | [Default] | [Which data/views] |

### Time Range Selector
- Options: Last 1h, 4h, 12h, 24h, 7d, 30d, Custom
- Default: Last 24h
- Applies to: all charts and tables on the page

### Drill-down Paths
| From | Trigger | To | Context Passed |
|------|---------|------|---------------|
| [Screen] | Click [element] | [Destination screen] | [What data carries over] |

## Metrics Display Specifications
| Metric | Display Name | Format | Unit | Visualization | Location | Thresholds |
|--------|-------------|--------|------|--------------|----------|-----------|
| [metric_id] | [Label] | [number/percentage/bytes] | [unit] | [gauge/line/bar/number] | [Screen > Widget] | [green/yellow/red values] |

## Alerts UI
- Alert banner at top of relevant pages when active alerts exist
- Alert count badge in sidebar navigation
- Alert detail panel: severity, metric, value, threshold, device, timestamp, acknowledge button

## Additional Notes for Lovable
- Use realistic mock data (not lorem ipsum) — generate realistic metric values
- Include hover tooltips on metrics showing definition
- All tables should support pagination (25 rows default)
- Include a "Refresh" button and "Last updated: X minutes ago" timestamp
- Sidebar navigation should show alert count badges
- Support both dark and light theme toggle

## Persona Scenario Validation

For each persona story from Step 1, describe how the wireframe solves their challenge:

### [Persona Name]'s Scenario
- **Their challenge:** [One-sentence summary from brainstorm story]
- **How they'd use this wireframe:** [Step-by-step walkthrough — which screen they'd open, what they'd see, what action they'd take]
- **Where the answer lives:** [Which screen > which widget/table shows the data they need]
- **How fast they'd know:** [Time from problem occurrence to visible alert/indicator in the UI]

### [Persona Name]'s Scenario
[Same structure for second persona]

> **If any persona's challenge is NOT clearly solvable from the wireframe screens, add the missing UI element before finalizing.**
```

## Static Prototype (`prototype.html`)

**Only build this if the PM's Step 6 choice included the prototype (A or C above).** When it did: render **Screen 1** (the primary/dashboard screen already specified above) as a real, self-contained static HTML mockup. This is the "see it now" deliverable; the Lovable prompt above is the "keep iterating" one — when both were chosen, ship both, neither replaces the other.

- **Reuse the spec, don't re-derive it.** Screen 1's layout, components table, and data already exist above — render exactly that screen, with the same widgets, the same table columns, the same realistic mock data (never lorem ipsum, matching "Additional Notes for Lovable" above).
- **Follow `<resolved shared parent>/design-taste/SKILL.md` in full** (sibling skill) — read it before writing this file. In particular: one accent color held everywhere (ManageEngine brand blue, `#0078d4` — the same color already specified in this prompt's own "Color scheme" above, so the prototype and whatever Lovable later builds actually match), row-separator tables (not a full boxed grid + zebra), a documented shape scale, real `:focus-visible` states, no AI-slop defaults.
- **Plain HTML + inline CSS, zero build step, zero framework** — same constraint as every other deliverable in this repo (Archify, frontend-slides, `analysis.html`). A little vanilla JS is fine only for something genuinely interactive the screen needs (e.g. a time-range dropdown that swaps a static mock chart) — this is a mockup demonstrating the idea, not a working app; don't over-build it.
- **Persona-check it**: confirm the same persona validation already done for the Lovable prompt above actually holds for this one rendered screen — if the primary screen alone can't show a persona's challenge being solved, note that plainly rather than silently expanding scope to a second screen.

Write to `[feature-name]/prototype.html` (topic-folder root — a visible deliverable like `architecture.html`/`executive-brief.html`, not `.steps/`; it isn't built from markdown so it sits outside the Report rebuild mechanism below).




## Report rebuild (mandatory)

Write markdown to `.steps/<name>.md` (hidden), then rebuild `analysis.html` and, if this step produced a diagram, render it and reference it first with a `<!-- diagram: architecture.html -->` marker. **Full procedure, exact paths, and the rebuild command are in `pm-shared/context/pm-operating-system.md` §§3, 6, 11a — already loaded as mandatory context for every run, so it is not repeated here.** Never delete `.steps/*.md`, `analysis.html`, or `.steps/build_docx.py`.

## Quality Gate (before marking complete)

Gate ledger for this step — write `.steps/GATES-6.md` from `<resolved shared parent>/unlazy-gates/templates/gates-leaf.md` before producing this step's content, one gate per item below. Resolution rule (self-correct on a failed gate, document the gap and continue — never abandon, never pause): `pm-shared/context/pm-operating-system.md` §18.


- [ ] G1: PM's Step 6 choice (A/B/C from operating system §8) respected exactly — nothing built beyond what was chosen
  (manual — no command can decide this)
- [ ] G2: Spec written under correct `.steps/` path, `analysis.html` rebuilt
  CHECK: node -e "const fs=require('fs');process.exit(fs.statSync('analysis.html').mtimeMs>=fs.statSync('.steps/6_lovable_wireframe.md').mtimeMs?0:1)"
  EXPECT: (exits zero)
- [ ] G3: Scope matches Step 4/5 findings (no silent expansion)
  (manual — no command can decide this)
- [ ] G4: If the Lovable prompt was chosen (A/B): paste-ready (single coherent prompt)
  (manual — no command can decide this)
- [ ] G5: If the prototype was chosen (A/C): `prototype.html` exists at the topic-folder root
  CHECK: node -e "process.exit(require('fs').existsSync('prototype.html')?0:1)"
  EXPECT: (exits zero — only run when the prototype was chosen)
- [ ] G6: `Progress.md` → `done`
  CHECK: node -e "process.exit(/\| Next action \| done/.test(require('fs').readFileSync('Progress.md','utf8'))?0:1)"
  EXPECT: (exits zero)
## Completion

After producing the chosen artifact(s), say (include only the lines matching what was actually chosen):

> **Step 6 complete.**
> [If the Lovable prompt was chosen:] Review `6_lovable_wireframe.md` (hidden under `.steps/`). When ready, copy its content into Lovable's prompt to generate your prototype.
> [If the prototype was chosen:] Open `prototype.html` to see the primary screen now.
>
> **🎉 Feature pipeline complete!** All artifacts are in `[feature-name]/`.
