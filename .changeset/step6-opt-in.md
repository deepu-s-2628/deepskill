---
"deepskill": minor
---

Step 6 (the Lovable prompt and `prototype.html`) is now opt-in instead of running unconditionally at the end of the autonomous chain. Once Steps 1–5 and document generation finish, the orchestrator asks once — both / just the prompt / just the prototype / neither — before deciding whether Step 6 runs at all, and if so, scoped to exactly what was chosen.

This is a second sanctioned checkpoint, not a reversal of the "wayfinding is the only pause" principle: `pm-operating-system.md` §8 now names both checkpoints explicitly as **scope/consent decisions**, never a content review — nothing about Steps 1–5's analysis or Step 6's own output, once it runs, is ever re-litigated. `Progress.md` gains a new `awaiting_step6_choice` state distinct from `blocked_on_pm` (a real dependency gap, e.g. the enhancement pipeline's screenshot requirement, unrelated to this choice). Propagated across both wireframe skills, both orchestrator agent pairs, the operating-system doc (canonical trees, quality gates, resume protocol, chat contract, non-goals), and the README. Verified `build_report.py` needs no changes — it already tolerates a topic folder with no Step 6 markdown at all — and swept the repo for now-stale "wayfinding is the only interactive step" claims left over in `skills/ask-deepu/SKILL.md` and `skills/feature-pipeline/brainstorm/SKILL.md`.
