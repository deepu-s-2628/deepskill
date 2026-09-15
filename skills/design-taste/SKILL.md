---
name: design-taste
description: "Design-taste discipline for this repo's own static HTML deliverables (analysis.html today; any future self-contained HTML output). Avoids generic AI-slop defaults, enforces one deliberate accent color, consistent shape/spacing rules, and real accessibility. Reference from build_report.py and any future HTML-generating script — not a page-builder, not invoked directly by a PM."
---

# Design Taste

## Source & attribution

Curated from [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) (`design-taste-frontend` v2, MIT, Copyright 2026 Leonxlnx). **This is not a copy.** That skill's own scope note says it explicitly: *"NOT for dashboards / dense product UI"* — and `analysis.html` is exactly that: a dense, table-heavy report, not a marketing landing page. Most of the source skill's ~1,200 lines are landing-page structure (heroes, bento grids, marquees, scroll-hijacking) and a React/Next.js/Motion/npm-component-library stack that doesn't fit this repo at all — every deliverable here is deliberately self-contained, zero-build-step HTML (see `skills/archify/`, `skills/frontend-slides/`).

What transferred: the genuinely stack-agnostic taste judgment — color restraint, typographic hierarchy, shape/spacing consistency, and the discipline of naming and avoiding generic-AI defaults instead of drifting into them. Rewritten from scratch for plain CSS and this repo's actual content shape (long tables, nested navigation, prose sections), not adapted line-by-line from the source.

**Deliberately left out**, and why:
- All React/Next.js/Motion/GSAP content (Sections 3, 5, 12 of the source) — no framework anywhere in this repo's deliverables.
- Landing-page structure rules (heroes, bento grids, marquees, nav-height caps, scroll cues) — `analysis.html` is a document, not a marketing page; these rules don't have an equivalent here.
- Webfont swaps (the source recommends Geist/Outfit/Satoshi over system fonts) — this repo's HTML must render correctly offline with zero external network calls, the same constraint that keeps Archify and frontend-slides dependency-free. A custom webfont means a network request every viewing; the system-font stack stays.
- Copy/content rules (em-dash bans, generic-name detection, filler-verb bans) — that's a content-voice concern for the pipeline's own 14 skills (ASD-STE100, `wait-what` style), not a CSS/visual-design one. Out of scope here.

## Where this applies

Right now: `pm-shared/scripts/build_report.py`'s CSS, which styles every `analysis.html`. Nothing else in this repo's output currently needs it (Archify and frontend-slides carry their own mature, unrelated style systems — don't apply this skill's rules to their output, see `pm-shared/context/pm-operating-system.md` §11a). A future static-HTML deliverable (e.g. the `prototype.html` from the roadmap's milestone 2) should reference this file the same way.

## The rules

### 1. One deliberate accent color, used identically everywhere

Never default to generic framework blue/purple (`#2563eb`, `#7c3aed` — the "AI blue/purple" tell) just because it's the first thing that renders. Pick one accent and hold it everywhere it appears — links, active states, header rules, callout borders. `analysis.html` uses ManageEngine's own brand blue (`#0078d4`, already the documented brand color in this repo's wireframe skills) rather than an arbitrary blue, so the report reads as *this product's* report, not a generic template. If this skill is ever applied to a second deliverable, pick one accent for that deliverable too and hold it — don't reuse a color inconsistently across unrelated surfaces.

### 2. Shape consistency, documented

Pick a small, explicit corner-radius scale and follow it everywhere — not one radius per element chosen independently. `analysis.html` uses exactly two: 6px for small inline/interactive elements (nav links, inline code), 8px for card-like containers (diagram frames, code blocks). A mixed scale is fine *only* when it's a documented rule like this one, applied consistently — never an unplanned mix.

### 3. Tables: row separators, not a full grid

The single most common "spec sheet" tell in generated documents: every cell boxed (`border: 1px solid` on every `th`/`td`) plus alternating-row zebra striping. It reads as a raw data dump, not an edited document. Prefer: a horizontal rule between rows only (no vertical cell borders), a stronger accent-colored rule under the header row, and at most a very faint zebra tint if the table is long enough that row-tracking genuinely needs it. This repo's reports are table-heavy (metrics, competitive matrices, requirement tables) — this is the highest-leverage single change available.

### 4. A readable measure for prose, full width for everything else

A wide content column (this repo's reports use up to 1400px, deliberately — narrow columns were an earlier, explicitly-reported complaint) is right for tables, headings, and embedded diagrams, but paragraph text at that width is unreadably long-lined. Cap prose elements (`p`) at a readable measure (~65-75 characters, roughly `65ch`) without capping the container itself — tables and diagrams still use the full width; only running text gets a narrower column.

### 5. Real focus states

Every interactive element (nav links, at minimum) needs a visible `:focus-visible` state in the accent color. A CSS file with zero focus styling is a real accessibility gap, not a taste nicety — ship it every time, not as an afterthought.

### 6. Shadows, when used, are tinted — never pure black

A drop shadow used for a touch of elevation (a diagram frame, a code block) should be tinted toward the page's own dark color, at very low opacity — `rgba(15, 23, 42, 0.06)` reads as "printed, lightly raised," a flat `rgba(0,0,0,0.3)` reads as cheap.

### 7. Avoid the obvious AI-slop defaults, on sight

No neon glows, no oversaturated accents, no gradient text on headings, no pure `#000000`/`#ffffff` anywhere (use the existing near-black slate / near-white values already in the palette). None of these need a rule to be enforced mechanically here — just don't reach for them.

## Self-check before calling a style change done

- [ ] One accent color, same hex, used everywhere it appears (links, active nav, header rules, callout borders)
- [ ] One documented corner-radius scale, no ad hoc per-element radius
- [ ] Tables use row separators + an accent header rule, not a full cell grid
- [ ] Prose (`p`) capped to a readable measure; tables/diagrams still use the full container width
- [ ] Every interactive element has a visible `:focus-visible` state
- [ ] No pure black/white, no neon, no gradient text, no unjustified shadow
- [ ] Still renders correctly offline — no external font/asset network calls introduced
