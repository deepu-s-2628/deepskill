---
name: ask-deepu
description: "Start the PM pipeline for OpManager Plus: describe a feature idea or an existing-feature improvement and this routes you into the right pipeline."
disable-model-invocation: true
---

Read what the PM just described.

- If it is a net-new capability (something OpManager Plus does not do today), start the **feature pipeline**: run the `ask-deepu-feature` agent.
- If it is an improvement to something that already exists, start the **enhancement pipeline**: run the `ask-deepu-enhancement` agent.

If it is genuinely unclear which one applies, ask one direct question before picking — do not guess silently.

Both agents load `context/pm-operating-system.md` and `context/product-context.md` first, then begin Step 1 immediately. See `.github/agents/Ask-Deepu-feature.agent.md` / `Ask-Deepu-enhancement.agent.md` for the full sequential workflow each pipeline follows.
