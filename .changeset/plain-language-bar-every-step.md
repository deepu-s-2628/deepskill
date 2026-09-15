---
"deepskill": minor
---

The plain-language bar (`pm-operating-system.md` §7) is now the default writing style for every pipeline step's output, not an on-demand fallback a PM has to trigger via `wait-what` after already being confused. Rewrote §7 to state this explicitly and name the connection to `wait-what`'s own "plain words, no unexplained jargon" standard, already coined but only applied to document-generation section intros before.

Closed a real coverage gap: only 3 of 14 pipeline skills referenced this bar at all (`brainstorm`, `generate-documents`, `enhancement-generate-documents`). The other 11 had no connection to it — most notably `current-state-analysis`, which §7 itself names by name as one of the two hardest-apply cases (same weight as `brainstorm`), yet had never actually pointed back to it. Added a short, tailored pointer to each of the 11 remaining pipeline skills — not a templated restatement, but adapted to what each step actually produces (e.g. `technical-analysis` on not assuming the reader knows why an approach was chosen, `deliverables`/`enhancement-deliverables` on the four drafted documents' own prose, `enhancement-wireframe` on describing screen changes the way a persona experiences them).
