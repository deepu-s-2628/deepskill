---
"deepskill": minor
---

Vendored Archify and frontend-slides in full, at `skills/archify/` and `skills/frontend-slides/` — both are now first-party, always-available parts of this plugin, not separately-installed dependencies. PPTX and PDF generation are retired entirely: flowcharts are now interactive Archify HTML, and the executive/engineering presentations are self-contained HTML decks authored with frontend-slides. `generate_pptx.py` and `generate_flowchart.py` are deleted; the PRD stays DOCX, generated the same way as before.

Removed the `ITOM-PM-Result/` wrapper folder — a PM run's topic folder (`[slug]/` or `[slug]-enhancement/`) now sits directly in the workspace root. Flattened the visible layout inside it: the consolidated report is `[slug].html` (not `report.html`) sitting directly in the topic folder alongside the flowchart, slide decks, and PRD, all visible; `.steps/` stays hidden and now also holds the DOCX build script (`.steps/build_docx.py`) and Archify source specs, kept for resumability.

Prompted by hands-on use: the nested `ITOM-PM-Result/[slug]/Generated/` structure was confusing to navigate day to day, and generating a PDF/PPTX pipeline alongside an HTML-first report added a second, less capable rendering path for no real benefit once Archify and frontend-slides covered the same ground with more animation and interactivity. Vendoring (rather than depending on the separately-installed `archify` plugin, as the previous release did with a graceful-degrade fallback) was an explicit call: this repo now owns syncing future updates to both tools, in exchange for teammates never needing a second plugin install.
