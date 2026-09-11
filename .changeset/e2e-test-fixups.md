---
"deepskill": patch
---

Fixes surfaced by a real end-to-end run of the feature pipeline against the vendored Archify/frontend-slides tooling and flat layout: a stale "converted to PDF" line in `deliverables/SKILL.md`'s flowchart draft section (PDF generation was already retired), a missing cross-reference explaining that the DOCX's embedded architecture image is a static `matplotlib` render rather than the interactive Archify HTML (added to both `deliverables/SKILL.md` and `enhancement-deliverables/SKILL.md`), and a note on both `generate-documents` skills that an Archify showcase validation pass is expected to take a few iterations, not one shot.
