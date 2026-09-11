---
"deepskill": patch
---

Aligned `md_to_html.py`'s fallback-render CSS with `build_report.py`'s new design-taste styling (milestone 1) — same brand-blue accent, row-separator tables, focus states, and radius scale. This path only runs when `build_report.py` itself is unavailable, but it was left visibly inconsistent (old generic Tailwind blue) after milestone 1 landed.
