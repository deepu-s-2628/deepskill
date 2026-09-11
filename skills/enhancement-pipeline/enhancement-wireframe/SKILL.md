---
name: enhancement-wireframe
description: "Step 6 of Enhancement Pipeline: Produce a Lovable wireframe prompt that matches the current OpManager Plus design language and incorporates the recommended enhancements from Step 4. Requires screenshots of current UI before generating the prompt."
---

# Step 6 — Enhancement Wireframe Prompt (Lovable)

## Purpose

Generate a Lovable prompt that produces a wireframe/prototype showing the **enhanced** version of an existing feature. Unlike new-feature wireframes (which design from scratch), enhancement wireframes must **match the current OpManager Plus design language exactly** and show only what changes.

## Input

Read all prior steps:
- `[feature-name]-enhancement/.steps/1_current_state.md` — what exists today and **persona challenges**
- `[feature-name]-enhancement/.steps/2_cross_module_analysis.md` — patterns from other modules
- `[feature-name]-enhancement/.steps/3_competitive_analysis.md` — competitive inspiration
- `[feature-name]-enhancement/.steps/4_enhancement_findings.md` — recommended enhancements and persona challenge resolution map
- `[feature-name]-enhancement/.steps/5a_executive_presentation.md` — executive summary of changes
- `[feature-name]-enhancement/.steps/5b_engineering_presentation.md` — technical details of changes
- `[feature-name]-enhancement/.steps/5c_enhancement_prd.md` — full PRD with metrics and requirements
- `[feature-name]-enhancement/.steps/5d_enhancement_flowchart.md` — enhanced flow diagrams

**CRITICAL: Design for the personas.** The enhanced wireframe must visually demonstrate that each persona's challenge is resolved. Walk through each persona's bad-day scenario from Step 1 and verify: does the enhanced UI prevent it? Can they see the right data, get the right alert, find the right screen? If not, the wireframe is incomplete.

## CRITICAL: Screenshot Collection

**You cannot generate the Lovable prompt without screenshots of the current UI.** The wireframe must match the existing design — colors, layout patterns, navigation structure, component styles, typography, spacing.

This is the one sanctioned pause point in the whole pipeline (operating system §8) — every other step runs unattended. If no usable screenshots exist yet, mark `Progress.md` as `blocked_on_pm`, ask exactly what's below, and stop the run there until they're supplied; do not fabricate UI details to keep going, and do not ask for screenshots at any earlier step (current-state-analysis explicitly does not block on this — see its Step 2).

### Step A — Request Initial Screenshots

Ask the PM for screenshots of:

> **I need screenshots of the current UI to match the design in the wireframe. Please share:**
>
> 1. **The main page/snapshot page** for this feature — showing the current layout, widgets, graphs, and data
> 2. **The settings/configuration page** — showing how this feature is currently configured
> 3. **Any relevant dashboard widgets** — showing how data is currently visualized
> 4. **The alarm/alert view** — if this feature has feature-specific alerts visible
>
> Paste or attach the screenshots and I'll analyze the design patterns before generating the wireframe.

### Step B — Analyze Current Design

From the screenshots, extract:

**Layout patterns:**
- Page structure (sidebar + main content? tabs? cards?)
- Grid system (how many columns? card sizes?)
- Navigation pattern (breadcrumbs? tabs? left nav?)
- Header/toolbar layout

**Visual design:**
- Primary colors used (exact hex if determinable, otherwise describe)
- Background colors (page, cards, headers)
- Font sizes and weights visible
- Icon style (outlined? filled? which icon set?)
- Button styles (primary, secondary, text links)
- Table styles (alternating rows? header colors? borders?)

**Component patterns:**
- How are metrics displayed? (large number cards? sparkline charts? gauges?)
- How are status indicators shown? (colored dots? icons? badges?)
- How are graphs rendered? (line charts? area charts? bar charts? time range selector style?)
- How are tables structured? (sortable? filterable? paginated?)
- How are forms/settings laid out? (inline? modal? separate page?)

**Data patterns:**
- What data columns are shown in tables?
- What metrics are shown on the snapshot page?
- What graph types and time ranges are used?
- How are severity levels color-coded?

### Step C — Request Additional Screenshots (If Needed)

If the initial screenshots don't cover all the areas affected by the enhancements, ask for more:

> **I need a few more screenshots to cover the areas that will be enhanced:**
>
> - [Specific page/section needed]
> - [Specific dialog/modal needed]
> - [Specific report/view needed]
>
> This ensures the wireframe accurately represents both what stays the same and what changes.

Do NOT proceed to prompt generation until you have sufficient screenshots to understand the current design.

### Step D — Confirm Design Understanding

Before generating the prompt, confirm with the PM:

> **Here's what I've captured from the current design:**
>
> - **Layout:** [Description]
> - **Color scheme:** [Description]
> - **Key components:** [List]
> - **Data displayed:** [Summary]
>
> **Enhancements I'll incorporate:**
> - [Enhancement 1 — how it modifies the current UI]
> - [Enhancement 2 — what new elements it adds]
> - [Enhancement 3 — what changes in existing elements]
>
> Does this look right? Any corrections before I generate the Lovable prompt?

## Prompt Generation

### Design Matching Rules

The Lovable prompt MUST:

1. **Replicate the existing design language** — same colors, same component patterns, same layout structure
2. **Mark enhanced elements clearly** — use subtle visual indicators (like a colored border or "NEW" badge) to distinguish new/changed elements from existing ones
3. **Preserve all existing data/metrics** — everything currently shown must still be shown
4. **Add new elements in the existing style** — new widgets, metrics, columns must use the same visual patterns as existing ones
5. **Maintain navigation consistency** — new tabs, menu items, or pages follow the existing nav structure

### Lovable Prompt Structure

```markdown
# Enhancement Wireframe: [Feature Name]

## Design System (Match Existing)

### Colors
- Primary: [extracted from screenshots]
- Background: [extracted]
- Card background: [extracted]
- Text primary: [extracted]
- Text secondary: [extracted]
- Status colors: Critical=[color], Warning=[color], OK=[color]
- Accent/highlight: [extracted]

### Typography
- Headings: [observed font, size, weight]
- Body: [observed]
- Metric values: [observed — usually large, bold]
- Table text: [observed]

### Component Library
[Describe each component type observed in screenshots, so Lovable replicates them]
- **Metric card:** [exact description — size, border, shadow, inner layout]
- **Status badge:** [description]
- **Data table:** [header style, row style, sorting indicators]
- **Line chart:** [axis style, legend position, colors used]
- **Button styles:** [primary, secondary, icon-only]
- **Tab bar:** [style, active indicator]
- **Form inputs:** [border style, label position, spacing]

## Pages to Build

### Page 1: [Enhanced Main Page]

**Layout:** [Match existing layout exactly, describe grid]

**Existing elements (keep as-is):**
- [Element 1 — exactly as shown in screenshot]
- [Element 2]

**Enhanced elements (modify from current):**
- [Element] — CHANGE: [what's different — e.g., "add 3 new columns to this table"]
- [Element] — CHANGE: [what's different]

**New elements (add in existing style):**
- [New widget/section] — positioned at [location], styled like [reference existing similar component]
- [New element]

### Page 2: [Enhanced Settings/Configuration]
[Same structure — existing + changes + new]

### Page 3: [New Page If Needed]
[Only if enhancements require a new page — should follow existing page layout patterns]

## Interactive Behavior

### Existing Interactions (Preserve)
- [Interaction that currently exists and must keep working]

### New Interactions
- [New click/hover/filter behavior from enhancements]

## Before/After Summary

| Area | Current | Enhanced | What Changed |
|------|---------|----------|-------------|
| [Section] | [Current state] | [New state] | [Description of change] |

## Persona Scenario Validation

For each persona story from Step 1, verify the enhanced wireframe solves their challenge:

### [Persona Name]'s Scenario
- **Their challenge today:** [One-sentence summary from Step 1 pain story]
- **What failed in the current UI:** [What they couldn't see/do/find]
- **How the enhanced UI solves it:** [Step-by-step — which screen, which new/changed element, what they'd see]
- **Visual proof:** [Which specific widget/table/alert in the wireframe demonstrates the fix]

### [Persona Name]'s Scenario
[Same structure for second persona]

> **If any persona's challenge is NOT visually solvable in the enhanced wireframe, add the missing UI element before finalizing.**
```

## Output Format

Write to `[feature-name]-enhancement/.steps/6_enhancement_wireframe.md`




## Report rebuild (mandatory)

Every step artifact this skill writes must:

1. **Markdown (source of truth, hidden):** `[slug]/.steps/<name>.md`
   - Enhancement mode: `[slug]-enhancement/.steps/<name>.md`
2. **Rebuild the consolidated report** immediately after:
   ```bash
   python "<scripts-dir>/build_report.py" "[slug]/"
   ```
   Resolve helper via `**/build_report.py` (`scripts/`).
3. If this step produced a diagram worth showing, render it with Archify (bundled at `skills/archify/`) to a visible sibling file (e.g. `architecture.html`) and reference it first with a `<!-- diagram: architecture.html -->` marker in the markdown, then rebuild.
4. On revise, rewrite the markdown and rebuild the report again.
5. Final chat summary (end of the whole run) cites the **`analysis.html`** path.
6. **Never delete** `.steps/*.md`, `analysis.html`, or `.steps/build_docx.py` after DOCX/slide-deck/diagram generation.

See `context/pm-operating-system.md` sections 3, 6, and 11–13.


## Quality Gate (before marking complete)

- [ ] Prompt written under correct `.steps/` path, `analysis.html` rebuilt
- [ ] Scope matches Step 4/5 findings (no silent expansion)
- [ ] Screenshots analyzed before drafting (or run correctly marked `blocked_on_pm` if none were available)
- [ ] Paste-ready for Lovable (single coherent prompt)
- [ ] `Progress.md` → `done`



## Completion

After writing the file, display in chat:

---

**Step 6 Complete — Enhancement Wireframe Prompt:**

> **Design matched from:** [N] screenshots analyzed
> **Pages in wireframe:** [N]
> **Existing elements preserved:** [N]
> **Enhanced elements:** [N] modifications to existing UI
> **New elements added:** [N] new components in existing style
>
> The Lovable prompt in `6_enhancement_wireframe.md` matches the current OpManager Plus design language and shows exactly what changes with the enhancements.
>
> **To use:** Copy the prompt into Lovable to generate the prototype.
>
> 🎉 **Enhancement analysis pipeline complete!**

---
