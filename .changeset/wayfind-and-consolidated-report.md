---
"deepskill": minor
---

Add `wayfind`, the mandatory first interactive step: interrogates whether a request actually fits OpManager Plus/Nexus, determines feature vs. enhancement, and locks scope before the rest of the pipeline runs. Once wayfind concludes "proceed," every remaining step runs unattended with no per-step approval gates (the one exception: the enhancement wireframe step still pauses if screenshots are missing). Replaced per-step visible HTML with one consolidated, anchor-navigable `report.html` per run, rebuilt after every step via the new `scripts/build_report.py`, with Archify-rendered diagrams embedded inline where a diagram earns its place over plain text.

Surfaced by real testing: a request outside OpManager Plus/Nexus's product surface was previously taken at face value and analyzed as if it fit, and results were scattered across a separate HTML file per step instead of one artifact.
