---
name: ask-deepu
description: "Start the PM pipeline for OpManager Plus: describe a feature idea or an existing-feature improvement and this routes you into the right pipeline."
disable-model-invocation: true
---

Run the `wayfind` skill on what the PM just described. Do not guess feature-vs-enhancement or fit-for-product yourself — that is wayfind's entire job, and it's the only step that talks to the PM.

Wayfind concludes one of three ways:

- **Proceed — Feature**: hand off to the `ask-deepu-feature` agent.
- **Proceed — Enhancement**: hand off to the `ask-deepu-enhancement` agent.
- **Stop — Not a fit**: stop here. Do not start a pipeline run.

Once wayfind hands off, the matching agent runs every remaining step back-to-back with no further pauses, and finishes with a single `report.html` under `ITOM-PM-Result/[slug]/`. See `.github/agents/Ask-Deepu-feature.agent.md` / `Ask-Deepu-enhancement.agent.md` for the full workflow each pipeline follows.
