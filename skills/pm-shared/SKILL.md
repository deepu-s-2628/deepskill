---
name: pm-shared
description: "Shared data package for the ask-deepu pipeline — not a skill to invoke. Bundles the operating rules, product context, and Python document generators every pipeline skill reads as an installed sibling."
disable-model-invocation: true
---

# pm-shared

This is not a skill you invoke — it exists so `npx skills add` has something to install alongside every other skill in this package. It bundles:

- `context/pm-operating-system.md`, `product-context.md`, `CONTEXT.md` — the shared operating rules and product knowledge every pipeline step and orchestrator loads.
- `scripts/build_report.py`, `generate_docx.py`, `md_to_html.py` — the Python generators that render `analysis.html` and `product-requirements.docx`.

These are generated mirrors of this repo's canonical top-level `context/` and `scripts/` — never edit the copies here directly; edit the top-level originals and run `node scripts/sync-pm-shared.mjs` (wired into every release via `npm run version`).

Every other skill in this package reads from here as an installed sibling: once `npx skills add` installs this repo, `pm-shared` lands as a direct sibling directory of every other installed skill, regardless of how deeply any of them were nested in the source repo. A skill resolves its own installed location (shown to it as "Base directory for this skill"), goes up one level to the shared parent directory, then into `pm-shared/context/...` or `pm-shared/scripts/...`.
