---
"deepskill": minor
---

`ask-deepu` now interrogates a request itself before anything else runs: does it actually fit OpManager Plus/Nexus, is it a feature or an enhancement, and what does the pipeline need locked down. This is the only interactive phase — once it concludes "proceed," every remaining step runs unattended with no per-step approval gates (the one exception: the enhancement wireframe step still pauses if screenshots are missing). "Stop — not a fit" is a first-class outcome, not a failure.

Replaced per-step visible HTML with one consolidated, anchor-navigable `report.html` per run, rebuilt after every step via the new `scripts/build_report.py`. Diagrams render through the separate, optional `archify` plugin when it's installed and embed as interactive frames; when it isn't, the same content degrades to a plain table or prose instead of failing the step.

Surfaced by real testing: a request outside OpManager Plus/Nexus's product surface was previously taken at face value and analyzed as if it fit, and results were scattered across a separate HTML file per step instead of one artifact. An earlier version of this fix added a standalone `wayfind` skill; folded directly into `ask-deepu` instead once testing showed the separate-skill invocation was itself unreliable, and its name was one typo away from an unrelated skill (`wayfinder`) that some teammates will have installed from a different plugin.
