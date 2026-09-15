---
name: ask-deepu
description: "Start the PM pipeline for OpManager Plus: describe a feature idea or an existing-feature improvement. Interrogates fit and mode before running anything, then hands off to the right pipeline."
disable-model-invocation: true
argument-hint: "A feature idea, or an existing feature to improve"
---

# Ask Deepu

The first of two sanctioned interactive checkpoints in the whole pipeline — the second is a short Step 6 opt-in choice, much later, after everything else is done (`pm-shared/context/pm-operating-system.md` §8). Everything between here and that later choice runs without asking the PM anything else — so don't let a wrong assumption slip through here.

## Why the interrogation happens here, not later

A PM's one-line request is not enough to safely run seven unattended pipeline steps against it. Taking a request at face value and assuming it's an OpManager Plus/Nexus feature — even when it describes something that doesn't belong in an ITOM tool at all (a new security product line, a different market, a different buyer) — produces a confident, wrong analysis. This has to be caught *before* research starts, not after.

## Process

1. **Load context first.** This plugin's shared context files live in a sibling skill called `pm-shared`, installed alongside this one — **there is no environment variable involved** (`echo $CLAUDE_PLUGIN_ROOT` or similar comes back empty; don't rely on one). Resolve it directly: take this skill's own **"Base directory for this skill"** path (shown above, no lookup needed) and go up exactly one level — that's the shared parent every installed skill sits in. Then read `<that parent>/pm-shared/context/product-context.md` and `<that parent>/pm-shared/context/CONTEXT.md` — you need the real shape of OpManager Plus/Nexus to judge fit. Resolve once and reuse the literal value for the rest of this run.

2. **Ask the fit question explicitly, don't assume it.** Before anything else, form a real opinion: does this request describe something that extends OpManager Plus/Nexus's actual product surface (network/server/APM/bandwidth/config/firewall/storage observability), or does it describe a different product category entirely (e.g. a standalone security product, a different buyer, a different deployment model)? If you're not confident, that's the first thing to ask the PM about — don't quietly default to "yes, this fits."

3. **Interview in rounds:** ask a batch of numbered questions, wait for real answers, then ask only what their answers newly unblock — don't ask everything at once, and don't ask one thing at a time either. Dispatch research (web search, `product-context.md`) for anything you can find out yourself — never ask the PM something you could look up.

   **Format every question as lettered options (A/B/C/…), not open-ended prose.** A PM answers "B" faster than they compose a paragraph, and named options force you to have actually thought through the real alternatives before asking — "is that right, or something else?" is a weaker question than five concrete possibilities. End each question with a recommended answer, which may combine letters (e.g. "B + A") when the real answer is additive. If a question only has one sane axis, it's fine to have just 2-3 options — the point is concreteness, not a fixed count.

   Cover, in whatever order the conversation naturally raises them:
   - **Fit**: is this an OpManager Plus/Nexus concern, adjacent-but-plausible, or a genuinely different product? If it's a different product, say so plainly and ask whether they still want a pipeline run anyway (e.g. as an integration point, or as an explicit out-of-product-line concept doc) or whether this should stop here.
   - **Product surface**: several modules exist in more than one form — a standalone ManageEngine product (Firewall Analyzer, NetFlow Analyzer, Network Configuration Manager, OpUtils, Applications Manager) *and* an integrated module inside OpManager Nexus. Whenever the request touches one of these, ask explicitly which surface it's for — this pipeline only covers OpManager Plus/Nexus, so a standalone-product answer changes fit, not just scope. Never assume "the Nexus one" by default.
   - **Mode**: feature (net-new) or enhancement (something that already exists gets better)? Use `pm-shared/context/pm-operating-system.md` section 2's trigger language as a starting signal, not the final word.
   - **Concrete definition**: if the request names a broad capability area (e.g. "threat intelligence," "automation," "analytics") rather than a specific mechanism, that phrase covers real, different things — break it into the actual sub-capabilities it could mean (reputation lookups vs. IOC matching vs. CVE correlation vs. attribution, to take one example) and ask which the PM means before researching any of them.
   - **User outcome vs. business driver — ask both, separately.** What does the *user* concretely get to do that they can't today (faster detection, better triage, audit evidence, automated response — these are different scopes with different technical paths)? And separately, what's driving this *for the business* (customer demand, a named competitive gap, a compliance requirement, an internal roadmap move)? Conflating these into one question loses the one that didn't happen to come to mind first.
   - **Internal product-line overlap**: check `pm-shared/context/product-context.md` section 9.1 (ManageEngine ecosystem) for a product that already does something adjacent to this request — Log360 for SIEM/log-compliance, Applications Manager for APM, PAM360 for credentials, etc. If one exists, ask whether this feature is meant to compete with/complement it, position OpManager Plus as a lighter alternative, or stay clearly out of that lane. Skipping this produces a scope that quietly duplicates or contradicts another ManageEngine product.
   - **Positioning**: if this is genuinely new ground (a new capability area, not a small addition), ask how the PM is thinking about it against *external* competitors too — is this meant to match/exceed a specific named competitor, or something else? Name real candidates from `pm-shared/context/product-context.md` section 10 rather than asking abstractly.
   - **Scope boundary**: anything that would make Step 3/4 (technical analysis / feature definition) go down the wrong path if this interview didn't ask now.

4. **Conclude explicitly.** State one of exactly three outcomes:
   - **Proceed — Feature**: net-new, fits the product. Name the slug, hand off to the `ask-deepu-feature` agent.
   - **Proceed — Enhancement**: improves something existing. Name the slug, hand off to the `ask-deepu-enhancement` agent.
   - **Stop — Not a fit**: explain concretely why (which product surface it doesn't match, what it would actually be), and do not create a pipeline run folder. This is a first-class, expected outcome — not a failure.

5. **Write the conclusion.** For a "Proceed" outcome, create `[slug]/.steps/0_wayfinding.md`. This file is the first section of the eventual consolidated report (`analysis.html`) — write it for that reader, not just as an internal note. "Wayfinding" is this skill's own internal name for the process, not something a PM reviewer needs to see, so the file itself never uses that word:

   ```markdown
   # Scope & Requirements

   [1-3 short paragraphs of prose: the fit reasoning (why this belongs in OpManager Plus/Nexus, and on which product surface), the mode and why (feature vs. enhancement), and the positioning answer if this is new ground. This is the only part that reads as a narrative — everything settled during the interview belongs in the table below, not repeated here.]

   ## Decisions Locked

   | Decision | Answer | Why |
   |---|---|---|
   | Mode | Feature / Enhancement | ... |
   | Product surface | ... | ... |
   | Scope | ... | ... |
   | [one row per scoping decision from the interview — anything a later step would otherwise have to re-ask or guess] | | |
   ```

## Completion

After reaching a "Proceed" conclusion, do not pause for approval — hand off immediately to the matching agent (`ask-deepu-feature` or `ask-deepu-enhancement`), which runs Steps 1–5 and document generation back-to-back without further confirmation, then asks one more short question before Step 6 (operating system §8). Say so plainly in your conclusion message so the PM knows what happens next and when to expect the finished consolidated report (`analysis.html`, sitting directly in the topic folder). See `.github/agents/Ask-Deepu-feature.agent.md` / `Ask-Deepu-enhancement.agent.md` for the full workflow each pipeline follows.

For a "Stop" conclusion, end there — no folder, no handoff, just the explanation and (if there's a plausible next step, like "this fits as an integration from a different product") a one-line suggestion of what that would look like.
