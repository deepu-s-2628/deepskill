---
name: learn-deepu
description: "Teach the user a topic — a technology, a competitor's feature, or anything else — as a real, multi-session learning workspace with lessons, references, and progress tracking. Grounds itself in this repo's own OpManager Plus context when the topic is product-related; teaches generically otherwise."
disable-model-invocation: true
argument-hint: "A technology, feature, or topic you want to learn about"
---

# Learn Deepu

## Source & attribution

Curated from mattpocock/skills' `teach` skill (MIT, Copyright 2026 Matt Pocock). **This is not a copy.** The underlying pedagogical model — Mission, Lessons, Zone of Proximal Development, Reference Documents, Learning Records, reusable Assets, and the fluency-vs-storage-strength distinction — transfers directly and is preserved faithfully, in its own words, for this repo. What changed:
- **Conditional product grounding** (see below) — the source skill is fully topic-agnostic; this adaptation adds a check for whether the topic relates to OpManager Plus/Nexus, and if so, treats `$CLAUDE_PLUGIN_ROOT/context/product-context.md`/`$CLAUDE_PLUGIN_ROOT/context/CONTEXT.md` as primary trusted sources over generic research.
- **File naming** — this repo's own convention (`Mission.md`, `Resources.md`, `Notes.md`), not the source's all-caps (`MISSION.md`, `RESOURCES.md`, `NOTES.md`).
- **Lesson/reference styling** — every HTML file this skill produces follows `$CLAUDE_PLUGIN_ROOT/skills/design-taste/SKILL.md`, not the source's own visual guidance.
- **No satellite format files** — the source points to `MISSION-FORMAT.md`/`RESOURCES-FORMAT.md`/`LEARNING-RECORD-FORMAT.md` alongside itself; those formats are inlined directly below instead, since this is one self-contained skill file, not a multi-file bundle.

## Scope — standalone, not part of the PM pipeline

This is a general-purpose utility, invocable any time, with **no connection to the PM pipeline**. It is never invoked by, and never invokes, any of the 14 pipeline skills, `ask-deepu`, or the orchestrator agents. A PM run and a learning workspace are unrelated concerns that happen to live in the same repo. This is deliberate, not an oversight — wire it into pipeline steps only if real use shows an actual need for that later.

## Conditional product grounding — check this first, every time

Before researching a topic, resolve `$CLAUDE_PLUGIN_ROOT` if not already known this session. **It is not a real environment variable** — `echo $CLAUDE_PLUGIN_ROOT` comes back empty. Resolve it first: take this skill's own **"Base directory for this skill"** path (shown above, no lookup needed) and walk upward until you find the directory containing `.claude-plugin/plugin.json` — that is `$CLAUDE_PLUGIN_ROOT` (full rationale, if useful: `$CLAUDE_PLUGIN_ROOT/context/pm-operating-system.md` §0). Then check whether the topic actually relates to OpManager Plus/Nexus or ITOM concepts — cross-reference `$CLAUDE_PLUGIN_ROOT/context/product-context.md`'s feature catalog and `$CLAUDE_PLUGIN_ROOT/context/CONTEXT.md`'s glossary.

- **If it does** (e.g. "teach me about SNMP," "teach me what Firewall Analyzer does," "teach me about NetFlow"): treat those two files as primary, trusted sources, alongside external research. Use this repo's own already-established canonical terms — don't introduce a competing name for something `CONTEXT.md` already names.
- **If it doesn't** (most topics won't — Rust ownership, yoga, thermodynamics, a new framework): skip `product-context.md`/`CONTEXT.md` entirely and teach exactly as a fully generic teaching skill would. Don't force an ITOM angle onto an unrelated topic.

This check runs once, at the start of a new topic — not per-lesson.

## Philosophy

Real learning needs three things:
- **Knowledge**, from high-quality, high-trust sources — never your own parametric memory alone. Find and cite real sources.
- **Skills**, built through lessons tightly scoped to one tangible win at a time.
- **Wisdom**, which only comes from real-world use outside the lesson — point toward a real community (a forum, a subreddit, a local group) when a question needs it, unless the user says they don't want that.

### Fluency vs. storage strength

Two different things get called "learning":
- **Fluency** — being able to recall something right now, in the moment. Feels like mastery, often isn't durable.
- **Storage strength** — actually retaining it weeks later. This is the real goal.

Build storage strength through **desirable difficulty**: retrieval practice (make them recall, don't just re-show), spacing (revisit across sessions, not all at once), and interleaving related-but-different topics during skills practice. Difficulty is the enemy when acquiring new knowledge (don't overload working memory); difficulty is the tool once building durable skill (effortful recall is what makes it stick).

## The Mission

Every lesson ties back to *why* the user wants to learn this. If `Mission.md` doesn't exist yet, or the reason isn't clear, ask first — a mission-less lesson has no way to judge relevance or what comes next.

`Mission.md` format:
```markdown
# Mission: [Topic]

## Why
[What the user is actually trying to achieve by learning this — a project, a role, curiosity with a real direction.]

## Current level
[Where they're starting from — total beginner, some exposure, rusty.]

## Success looks like
[What being "done," or good enough to stop formal lessons, actually looks like for this mission.]
```

Missions can change as the user's understanding deepens — confirm with them before rewriting `Mission.md`, and add a learning record capturing the change and why.

## Zone of proximal development

Each lesson should feel challenging, not easy and not overwhelming. If the user names an exact next thing, teach that. If not, figure it out: read `learning-records/`, weigh it against the mission, and teach the most relevant thing that's a genuine stretch but not a leap.

## Lessons

The main deliverable. One self-contained HTML file per lesson, saved to `[topic]-learning/lessons/0001-<dash-case-name>.html` (incrementing), styled per `$CLAUDE_PLUGIN_ROOT/skills/design-taste/SKILL.md` — one held accent color, row-separator tables if the lesson has any, a readable prose measure, real focus states, no generic-AI-slop defaults.

- **Short and completable quickly.** Working memory is small; one tangible win per lesson, directly tied to the mission and pitched at the zone of proximal development — not a sprawling reference dump.
- **Cite a primary source** — the single best, most trustworthy resource on this specific point, linked prominently.
- **Cross-link** to other lessons and reference documents via HTML anchors as the workspace grows.
- **End with an invitation to ask follow-up questions** — the agent is the tutor here, not a one-shot document generator.
- For skills (not pure knowledge), build in a **tight feedback loop**: a quiz, a small interactive check, or a concrete real-world step to take and report back on. Quiz answers should be uniform in length/shape — don't let formatting leak the answer.

## Reference documents

Lessons are rarely revisited; reference documents are. Save the compressed, durable essence of what's been taught — a cheat sheet, a glossary, a syntax reference, a quick-lookup table — to `[topic]-learning/reference/<name>.html`, same `design-taste` styling. Once a glossary exists for a topic, stay consistent with it in every later lesson.

## Learning records

`[topic]-learning/learning-records/0001-<dash-case-name>.md` (incrementing) — the non-obvious insights and key decisions from what's been taught so far, loosely like an ADR for the learner's own understanding. Read these before planning what to teach next; they're what makes the zone-of-proximal-development judgment possible across sessions instead of starting cold every time.

## Assets

Shared, reusable lesson components — stylesheets, quiz widgets, diagram helpers — at `[topic]-learning/assets/`. Reuse by default: read what's already there before authoring a new lesson, and build from it. A shared stylesheet is the first asset any topic earns, so a topic's lessons read as one consistent course rather than a pile of one-offs.

## `Resources.md`

A running list of high-quality external sources worth returning to, for either acquiring knowledge or (once fluent) testing it against real practitioners:

```markdown
# Resources: [Topic]

## Primary
- [Title](url) — why this is trustworthy, what it covers

## Communities
- [Name](url) — where real-world practice/feedback happens for this topic
```

## `Notes.md`

A plain scratchpad for anything the user says about how they want to be taught — pace, format preferences, things to avoid — so it's remembered across sessions rather than re-asked.

## Workspace layout

```
[topic]-learning/                 ← directly in the workspace root, e.g. vxlan-learning/
├── Mission.md
├── Resources.md
├── Notes.md
├── lessons/
│   └── 0001-<name>.html
├── reference/
│   └── <name>.html
├── learning-records/
│   └── 0001-<name>.md
└── assets/
    └── (shared stylesheet, widgets, etc.)
```

`-learning` is a deliberately distinct suffix from `-enhancement` (the PM pipeline's own suffix, `$CLAUDE_PLUGIN_ROOT/context/pm-operating-system.md` §3/§4) — a learning workspace must never be mistaken for a PM run, and vice versa.
