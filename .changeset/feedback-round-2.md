---
"deepskill": minor
---

Second round of real-usage feedback (Firewall Analyzer IP-reputation test run), all implemented:

**Filenames.** Deliverables are now named for their role, not the slug — `analysis.html`, `architecture.html`, `executive-brief.html`, `engineering-brief.html`, `product-requirements.docx` — the same names in every topic folder, so it's always obvious which to open first. `STATUS.md` is renamed to `Progress.md` (still visible at the topic-folder root).

**PRD (DOCX).** Author metadata now defaults to "Deepu S" instead of a `[PM Name]` placeholder. The Table of Contents is no longer a Word field that needs a manual "right-click → Update Field" — every heading is bookmarked as it's written and the TOC is filled in with real internal hyperlinks at save time, so it's correct and clickable the moment the file opens. Every major section now opens with a short plain-language intro paragraph instead of jumping straight into tables.

**Consolidated report (`analysis.html`).** The left nav is now nested — each step's own subsections appear underneath it — with scroll-position highlighting showing which section you're currently reading. The main content column is wider (1400px cap, was 980px). The wayfinding step is renamed "Scope & Requirements" in both the report heading and the nav, and its locked decisions render as a table instead of prose sub-headings.

**Slide decks.** Both decks now ship full keyboard/mouse-wheel/on-screen navigation (frontend-slides' own template contract, previously not enforced by our instructions) and target frontend-slides' "high density / reading-first" mode (4-8 bullets/cards per slide) instead of its sparse speaker-led default, which is what produced thin one-line slides in testing.
