---
name: wayfind
description: "Interrogate a PM's request before any pipeline runs: does this belong in OpManager Plus/Nexus at all, is it a feature or an enhancement, and what does the pipeline need to know before it can run unattended. Always run this first, before brainstorm or current-state-analysis."
---

# Wayfind

The one and only interactive step. Everything after this runs without asking the PM anything else — so don't let a wrong assumption slip through here.

## Why this exists

A PM's one-line request is not enough to safely run seven unattended pipeline steps against it. Before wayfind existed, `ask-deepu` took the request at face value and assumed it was an OpManager Plus/Nexus feature — even when the request described something that doesn't belong in an ITOM tool at all (a new security product line, a different market, a different buyer). That produced a confident, wrong analysis. Wayfind exists to catch that *before* research starts, not after.

## Process

1. **Load context first.** Read `context/product-context.md` and `context/CONTEXT.md` — you need the real shape of OpManager Plus/Nexus to judge fit.

2. **Ask the fit question explicitly, don't assume it.** Before anything else, form a real opinion: does this request describe something that extends OpManager Plus/Nexus's actual product surface (network/server/APM/bandwidth/config/firewall/storage observability), or does it describe a different product category entirely (e.g. a standalone security product, a different buyer, a different deployment model)? If you're not confident, that's the first thing to ask the PM about — don't quietly default to "yes, this fits."

3. **Interview in rounds**, same discipline as the `grilling` pattern: ask a batch of numbered questions with your recommended answer for each, wait for real answers, then ask only what their answers newly unblock. Dispatch research (web search, `product-context.md`) for anything you can find out yourself — never ask the PM something you could look up.

   Cover, in whatever order the conversation naturally raises them:
   - **Fit**: is this an OpManager Plus/Nexus concern, adjacent-but-plausible, or a genuinely different product? If it's a different product, say so plainly and ask whether they still want a pipeline run anyway (e.g. as an integration point, or as an explicit out-of-product-line concept doc) or whether this should stop here.
   - **Mode**: feature (net-new) or enhancement (something that already exists gets better)? Use `context/pm-operating-system.md` section 2's trigger language as a starting signal, not the final word.
   - **Positioning**: if this is genuinely new ground (a new capability area, not a small addition), ask how the PM is thinking about it — is this meant to compete with a specific class of product, extend an existing module, or something else? This is exactly the kind of question a PM expects to be asked and a pipeline should never skip.
   - **Scope boundary**: anything that would make Step 3/4 (technical analysis / feature definition) go down the wrong path if wayfind didn't ask now.

4. **Conclude explicitly.** State one of exactly three outcomes:
   - **Proceed — Feature**: net-new, fits the product. Names the slug, hands off to the feature pipeline.
   - **Proceed — Enhancement**: improves something existing. Names the slug, hands off to the enhancement pipeline.
   - **Stop — Not a fit**: explain concretely why (which product surface it doesn't match, what it would actually be), and do not create a pipeline run folder. This is a first-class, expected outcome — not a failure.

5. **Write the conclusion.** For a "Proceed" outcome, create `ITOM-PM-Result/[slug]/.steps/0_wayfinding.md` with: the fit reasoning, the mode and why, the positioning answer, and every scoping decision locked during the interview — anything a later step would otherwise have to re-ask or guess. This file is the first section of the eventual consolidated report; write it for that reader, not just as an internal note.

## Completion

After reaching a "Proceed" conclusion, do not pause for approval — hand off immediately to the matching orchestrator (`ask-deepu-feature` or `ask-deepu-enhancement`), which runs every remaining step back-to-back without further confirmation. Wayfind is the only checkpoint; say so plainly in your conclusion message so the PM knows what happens next and when to expect the finished `report.html`.

For a "Stop" conclusion, end there — no folder, no handoff, just the explanation and (if there's a plausible next step, like "this fits as an integration from a different product") a one-line suggestion of what that would look like.
