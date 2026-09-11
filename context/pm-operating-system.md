# ITOM PM Toolkit — Operating System

> Shared rules for **ask-deepu**, **PM Feature Agent**, and **PM Enhancement Agent**.
> Load this file at the start of every PM pipeline run (new or resume).
> **Last updated:** 2026-09-11.
>
> **What is this file?** Single shared rulebook so ask-deepu's wayfinding phase and both pipelines stay consistent (paths, language bar, wayfinding-then-autonomous execution, the consolidated report, retention, quality gates, dense deliverables, resume).

---

## 1. Mission

Produce opinionated, **immediately usable** product work for **OpManager Plus / OpManager Nexus**:
wayfinding → research → analysis → definition → **dense HTML slide deck + Archify diagram + DOCX PRD** → Lovable wireframe prompt → **one consolidated HTML report**.

Agents are **product operators**, not brainstorming chatbots. Prefer one clear recommendation over option menus.

**Audience default:** many reviewers are developers who are **not** specialists in the technology. Write so a competent generalist engineer can follow.

**Deliverable bar:** the slide deck, flowchart, and PRD must be rich enough to present or hand to engineering **without** a cleanup pass. Thin bullet decks are a fail.

---

## 2. Wayfinding Comes First — Always

Before any research step runs, `ask-deepu` interrogates the request itself: does this actually belong in OpManager Plus/Nexus, is it a feature or an enhancement, and what does the rest of the pipeline need locked down before it can run unattended. See `skills/ask-deepu/SKILL.md` for the full interview process — there is no separate wayfinding skill; it's `ask-deepu`'s own first phase.

Wayfinding is the **only** interactive phase in the whole pipeline (Section 8). It concludes one of three ways, and nothing downstream may skip or second-guess this conclusion:

| Conclusion | What happens next |
|---|---|
| **Proceed — Feature** | `.steps/0_wayfinding.md` written; hand off to the feature pipeline, Step 1 = `brainstorm` |
| **Proceed — Enhancement** | `.steps/0_wayfinding.md` written; hand off to the enhancement pipeline, Step 1 = `current-state-analysis` |
| **Stop — Not a fit** | No topic folder created. Explain why plainly and stop. |

Trigger language (`build` / `new feature` vs `enhance` / `improve`) is a starting signal for the mode question — never a substitute for actually asking it. Do **not** mix pipelines in the same topic folder.

---

## 3. Canonical Paths (flat topic folder, one consolidated report, Markdown hidden)

### Workspace root

All paths are relative to the **opened workspace root**. There is no wrapper folder — the topic folder is created **directly** at the workspace root, exactly where the PM was working when they ran `ask-deepu`.

### Feature pipeline

```
[slug]/
├── Progress.md                 ← always visible control plane
├── analysis.html               ← THE deliverable: one navigable HTML, rebuilt after every step
├── architecture.html           ← Archify-rendered flowchart, also embedded inside analysis.html
├── executive-brief.html        ← executive slide deck (frontend-slides, HTML)
├── engineering-brief.html      ← engineering slide deck (frontend-slides, HTML)
├── product-requirements.docx   ← PRD, python-docx
└── .steps/                     ← HIDDEN: markdown source of truth + build scripts (agent edit/resume)
    ├── 0_wayfinding.md
    ├── 1_brainstorm.md
    ├── 2_competitive_analysis.md
    ├── 3_technical_analysis.md
    ├── 4_feature_definition.md
    ├── 5a_executive_presentation.md
    ├── 5b_engineering_presentation.md
    ├── 5c_feature_flowchart.md
    ├── 5d_product_requirements.md
    ├── 6_lovable_wireframe.md
    ├── diagrams/                ← Archify JSON specs (source for the flowchart HTML)
    │   └── flowchart.json
    └── build_docx.py            ← keep after success; regenerates product-requirements.docx
```

### Enhancement pipeline

Same flat pattern, folder named `[slug]-enhancement/`:
- `.steps/*.md` — hidden sources, starting with `0_wayfinding.md`
- `analysis.html` — the one consolidated deliverable
- `architecture.html`, `executive-brief.html`, `engineering-brief.html`, `product-requirements.docx` — same deliverable set as feature mode

### Hard rules

1. **Markdown always under hidden `.steps/`** — never put step `.md` in the topic-folder root.
2. **There is exactly one visible review artifact for the analysis itself: `analysis.html`** at the topic-folder root. No per-step HTML files.
3. **After every step**, regenerate the report: `python "<scripts-dir>/build_report.py" "[slug]/"`. Never let `analysis.html` fall behind `.steps/`. (`build_report.py` derives the output filename from the folder name — it always matches.)
4. **Diagrams are Archify HTML**, visible at the topic-folder root (e.g. `architecture.html`) *and* referenced from the relevant step's markdown with a `<!-- diagram: architecture.html -->` marker line — `build_report.py` turns that into an embedded, interactive `<iframe>` in the right section. There is no PDF flowchart.
5. **Slide decks are HTML** (`frontend-slides`), not PPTX. Two decks — `executive-brief.html` (executive audience) and `engineering-brief.html` (engineering audience) — each self-contained, animation-capable, and openable directly in a browser.
6. **The PRD stays DOCX** (`python-docx`), unchanged from before.
7. **Retention — never delete** `.steps/*.md`, `analysis.html`, `Progress.md`, the deliverable files at the topic-folder root, or `.steps/build_docx.py`.
8. Do not invent alternate layout names (`output/`, `docs/`, `Generated/`, `steps/` without the dot).
9. Chat summaries should **highlight the `analysis.html` path** for reviewers; mention MD only as internal source.

### Report rebuild command

```bash
python "<scripts-dir>/build_report.py" "[slug]/"
```
Resolve helpers via `**/build_report.py` and `**/md_to_html.py` (both live in `scripts/`).

---

## 4. Slug Rules

| Rule | Example |
|------|---------|
| lowercase kebab-case | `vxlan-monitoring` |
| no spaces or underscores | not `VXLAN Monitoring` |
| stable for life of analysis | do not rename mid-pipeline |

Enhancement folders **must** end with `-enhancement`.
If a folder already exists for the same slug, **resume** it — do not create `*-v2` unless the PM asks for a fresh run.

---

## 5. Progress.md (Control Plane)

Create/update `[folder]/Progress.md` at every step boundary.

```markdown
# Progress — [Feature Display Name]

| Field | Value |
|-------|-------|
| Mode | feature \| enhancement |
| Slug | [slug] |
| Folder | [folder]/ |
| Current step | [N] — [name] |
| Step status | running_autonomously \| blocked_on_pm \| complete |
| Last updated | [YYYY-MM-DD] |
| Next action | resolve_blocker \| step_N+1 \| done |

## Completed steps
- [x] Step 0 — Wayfinding (`.steps/0_wayfinding.md`)
- [x] Step 1 — ... (`.steps/1_….md`)
- [ ] Step 2 — ...

## Open questions for PM
1. ... (only ever populated if genuinely blocked — Section 8)

## Key decisions locked
- ... (carried forward from wayfinding, Section 2)

## Risks / blockers
- ...
```

On resume: read `Progress.md`, then all **`.steps/*.md`**, then rebuild `analysis.html` before continuing.

---

## 6. Markdown (hidden source) → consolidated report (visible)

After writing or revising any step's markdown:

1. Save markdown to **`.steps/<name>.md`**. This is the source of truth for edits and for regeneration.
2. Rebuild the report: `python "<scripts-dir>/build_report.py" "[folder]/"`. This regenerates the **whole** `analysis.html` from every `.steps/*.md` file that exists so far — cheap, so do it after every step, not just at the end.
3. If a step produced a diagram worth showing (see Section 11a), render it with Archify to a visible sibling file (e.g. `architecture.html`) and reference it from that step's markdown with a `<!-- diagram: architecture.html -->` marker before rebuilding — `build_report.py` turns it into an embedded, interactive frame.
4. **Never delete** `.steps/*.md` or `analysis.html` after binary/HTML generation.
5. Final chat completion (after the whole run finishes) must cite the **`analysis.html` path**.

If `build_report.py` is unavailable, fall back to `md_to_html.py` per-step and note in chat that the consolidated report couldn't be built — this should not happen in a working checkout.

---

## 7. Plain-language bar (DOE)

Applies hardest to **brainstorm / current-state openers**, and still applies to executive-facing sections.

### Do
- Prefer short sentences and everyday words.
- Define a term the **first** time it appears.
- Use **analogies and concrete examples**.
- Separate **what the technology is** / **why people use it** / **what problem it solves** / **what we monitor**.

### Don’t
- Open Step 1 with RFC field dumps.
- Assume the reader already knows why the technology exists.

### Required technology framing (Feature Step 1)
1. **What is it?**
2. **Why do people use it?**
3. **What problem does it solve?**
4. **Easy example**

---

## 8. Sequential Workflow: Wayfind Interacts, Everything After Runs Unattended

**Wayfind is the only checkpoint.** Once it reaches a "Proceed" conclusion (Section 2), the matching orchestrator runs every remaining step — including document generation (Section 13) and the wireframe prompt — back-to-back with **no pause for approval between steps**. The PM does not need to reply `proceed` at any point after wayfinding.

For each step, in order:
1. Produce the step.
2. Write `.steps/*.md`.
3. Rebuild `analysis.html` (Section 6).
4. Update `Progress.md`.
5. Move immediately to the next step. Do not stop and wait.

### The two real exceptions
- **Hard blocker with no safe default** (e.g. the wireframe step needs real screenshots and none exist, or a step's own quality gate fails and can't be self-corrected): pause, ask the *specific* thing needed, resume the same run once answered. This is a genuine dependency gap, not a review gate.
- **The PM interrupts mid-run** (sends a new message while a run is in progress): stop what you're doing, address what they said, then resume the autonomous chain unless they've asked you to stop for good.

### Special commands (still honored if the PM uses them mid- or post-run)
| PM says | Action |
|---------|--------|
| `redo step N` / feedback on step N | Revise step N only, rebuild the report, then resume the autonomous chain from where it left off |
| `status` / `where are we` | Summarize from `Progress.md` + `.steps/` + `analysis.html` |
| `pause` / `stop` | Stop; leave `Progress.md` accurate so the run can resume later |

There is no `generate files` command to wait for anymore — document generation (Section 13) runs automatically as part of the same unattended chain once Step 5's drafts are done.

---

## 9. Research Bar (Minimum Evidence)

### Every analysis step must
- Use `context/product-context.md`.
- Prefer workspace context files via keyword routing.
- Use **web research** for competitors, vendor tech, protocols, APIs, MIBs/OIDs.
- Cite sources with links in `## Sources`.

### Competitive steps
- ≥4 competitors unless niche exception (state why).
- Table stakes vs differentiators.
- Tie to persona challenges.

### Technical / current-state steps (DEEP)
- Evaluate **all viable collection methods** (SNMP, REST, gRPC/telemetry, CLI, flow, traps/syslog, agent, etc.).
- Pick **one primary** method with rationale; document fallbacks.
- **Deep research required for the primary method** and strong alternatives:
  - **SNMP:** MIB names, concrete OIDs (or OID prefixes), what each returns, tables vs scalars, indexing notes, version caveats.
  - **REST/API:** base paths, key endpoints, auth model, pagination/rate limits, example response fields mapped to metrics.
  - **Telemetry/gRPC/model-driven:** paths/sensors, encodings, dial-in vs dial-out.
  - **CLI:** commands, parse targets, stability risk.
  - **Flow/traps/syslog:** template IDs / message patterns when relevant.
- Label uncertain OIDs/endpoints as **Verified** vs **Needs lab confirmation**.
- Call out EE/probe, scale, licensing, security.
- No implementation source code in PM artifacts.
- Short plain-language recap at top of technical docs.

### Screenshots
- Enhancement UX/wireframes: request real screenshots; never invent contradicting UI.

---

## 10. Persona Standard

Mandatory in Feature Step 1 and Enhancement Step 1.
Each story: name, role, company type, scale, failure moment, easy example, transformation line.
Reuse the same named personas later. Weak generic personas = fail.

---

## 11. Dense deliverables bar (slide decks / flowchart / PRD)

### Principle
Step 5 drafts and the document-generation outputs built from them must **transfer the analysis**, not summarize it into a few vague bullets. A reader who only opens the slide deck or the flowchart should still get the full decision trail.

### Must pull forward from prior steps
- Persona challenges and how each is solved
- Competitive gaps we exploit
- **Every** recommended metric category (not a cherry-picked subset)
- Collection method + prerequisites + key OIDs/API endpoints (engineering deck & flowchart)
- Architecture / data flow / discovery / polling / alert logic
- Scale limits, risks, phasing, open questions
- Explicit in-scope / out-of-scope

### Executive slide deck (HTML, frontend-slides)
- Still strategic, but **not thin**: each slide needs concrete points, numbers, and named capabilities from the analysis.
- Include a competitive snapshot with real differentiators (not “we will monitor better”).
- Capability slides must list the actual v1 capabilities from feature definition.
- Success metrics must be specific and measurable.
- Use frontend-slides' animation and template capabilities deliberately — this is not a PPTX-to-HTML port, it should look and move like a real presentation.

### Engineering slide deck (HTML, frontend-slides)
- **Detailed and immediately usable** by eng leads.
- Include collection comparison (why primary won).
- Metrics tables split across slides as needed — **do not drop metrics**.
- Dedicated slides for OID/API inventory highlights (or appendix slides).
- Architecture, data model, polling, alerting, scale, risks, phasing, open questions.
- Prefer 18–25 slides when content requires it rather than compressing into vague 12.

### Flowchart (Archify HTML)
- Cover: overview, setup/onboarding, discovery, collection pipeline (with protocol/API branch detail), processing/storage, alerting/notification, failure/retry, EE/probe path if relevant, daily operator loop — use Archify's `workflow` diagram type, multiple linked views (`meta.views`) if one flat diagram can't hold all of it legibly.
- Every major decision node labeled with the real condition from analysis.
- Annotate key OIDs/endpoints on collection nodes where space allows.
- Must be followable without reading the PRD.

### Fail conditions
- A slide deck that could apply to any feature with names swapped
- Flowchart with only 5 generic boxes
- Engineering deck missing metrics or collection contract
- “Update later” placeholders, TBD-only slides, or lorem content

---

## 11a. Diagrams and slides: Archify and frontend-slides are first-party, bundled skills

`archify` and `frontend-slides` live inside this repo, at `skills/archify/` and `skills/frontend-slides/` — vendored in full, not separately-installed plugins. They ship with every install of this plugin, so **there is no missing-skill case to degrade from for these two**, and no "try, then fall back to prose" pattern is needed here.

- **Flowchart / architecture diagrams → Archify.** Use it for anything with real structure worth exploring: architecture/data-flow (Section 9's collection pipeline), the feature flowchart, a before/after comparison for an enhancement. Author a JSON spec under `.steps/diagrams/<name>.json`, render with `node <archify-dir>/bin/archify.mjs deliver <type> <spec.json> architecture.html --quality showcase`, then reference the visible output from the relevant step's markdown with `<!-- diagram: architecture.html -->` (Section 6). Resolve `<archify-dir>` via `**/skills/archify/bin/archify.mjs`.
- **Skip the diagram** and just write it out when a short table or a few sentences say the same thing without asking the reader to parse a shape — e.g. a two-option comparison, a short ordered list of steps. A diagram that doesn't earn more clarity than prose is padding.
- **Slide decks → frontend-slides.** Both the executive and engineering decks (Section 11) are authored as self-contained HTML using `skills/frontend-slides/`'s templates and animation patterns — no PPTX is generated anywhere in this pipeline.
- **License note:** both skills are MIT-licensed. Archify's vendored copy carries `THIRD_PARTY_NOTICES.md` disclosing that a small set of embedded brand-mark icons (used only when a diagram names a real product) carry their own upstream licenses, one of which (Vue.js) is CC-BY-NC-SA-4.0 with a non-commercial, share-alike condition. That notice ships as-is with the vendored copy — do not strip it, and do not use the Vue.js mark for anything beyond identifying the technology in a diagram.

### Standing rule: no hard dependency on an unbundled skill

This still applies to anything **not** vendored into this repo's own `skills/` — added later, or referenced ad hoc. Teammates will have different sets of separately-installed plugins; never assume one is present just because your own machine has it. Every such reference must:
1. Attempt the call, expecting it may not resolve.
2. On failure, degrade to a plain-text/markdown equivalent rather than stopping the step or the run.
3. Never let a failed lookup fall through to invoking a similarly-named but unrelated skill (this is exactly how `wayfind` briefly got confused with an installed-but-unrelated `wayfinder` skill from another plugin, before `wayfind` was folded directly into `ask-deepu` to remove the cross-skill call entirely). When in doubt, prefer inlining the logic into one of this repo's own skills, or vendoring the capability (as done for Archify and frontend-slides), over depending on another plugin's skill by name.

---

## 12. Quality Gates (Do Not Mark Step Complete If Failed)

### Global
- [ ] Markdown under **`.steps/`** (hidden)
- [ ] `analysis.html` rebuilt after this step (Section 6)
- [ ] `Progress.md` updated
- [ ] Chat summary (final, end-of-run) cites the **`analysis.html`** path
- [ ] No implementation source code in artifacts
- [ ] No deletion of prior `.steps/` files or topic-folder deliverables
- [ ] External claims cited or labeled assumptions
- [ ] Plain language where required (esp. Steps 0–2)

### Step 0 — Wayfinding
- [ ] Fit question asked and answered explicitly, not assumed
- [ ] Mode (feature/enhancement) locked with reasoning
- [ ] Positioning question asked if this is genuinely new ground
- [ ] Conclusion is one of exactly three outcomes (Section 2)
- [ ] `.steps/0_wayfinding.md` written (Proceed outcomes only)

### Feature Step 1 — Brainstorm
- [ ] Plain English; jargon defined on first use
- [ ] What / why people use it / problem / easy example
- [ ] 2–3 named persona stories
- [ ] Module fit + reuse
- [ ] `.steps/1_brainstorm.md` written, report rebuilt

### Feature Step 2 / Enhancement Step 3 — Competitive
- [ ] ≥4 competitors or exception
- [ ] Persona-challenge matrix
- [ ] Recommended market position
- [ ] `.steps/` path correct, report rebuilt

### Feature Step 3 — Technical
- [ ] All viable collection methods evaluated
- [ ] Single primary method + fallbacks
- [ ] Deep OID/API/telemetry inventory for primary (and major alt if close)
- [ ] Metrics categorized with thresholds/frequency
- [ ] Scale + failure modes + EE/security
- [ ] Persona challenges solved technically
- [ ] Sources cited
- [ ] `.steps/` path correct, report rebuilt

### Feature Step 4 / Enhancement Step 4
- [ ] In-scope vs out-of-scope
- [ ] Persona → capability traceability
- [ ] Decisive phasing
- [ ] `.steps/` path correct, report rebuilt

### Step 5 drafts
- [ ] All four under `.steps/`
- [ ] Exec and eng decks are not near-duplicates
- [ ] Eng deck + flowchart carry full analysis density (metrics, collection contract, flows)
- [ ] No TBD/lorem placeholders
- [ ] PRD testable

### Document generation (runs automatically once Step 5 is done — Section 8)
- [ ] All prerequisite **`.steps/`** markdown files exist
- [ ] DOCX generator resolved via `**/generate_docx.py`
- [ ] Archify resolved via `**/skills/archify/bin/archify.mjs`
- [ ] Slide decks and flowchart meet the dense deliverables bar (Section 11)
- [ ] `.steps/build_docx.py` kept
- [ ] `.steps/*.md` still present after generation
- [ ] `product-requirements.docx`, `executive-brief.html`, `engineering-brief.html`, `architecture.html` all openable and content-complete

### Step 6 wireframe
- [ ] `.steps/` path correct, report rebuilt
- [ ] Enhancement: screenshots first — this is the one place a real blocker can still pause the run (Section 8)
- [ ] Paste-ready Lovable prompt
- [ ] Scope matches wayfinding conclusion only

---

## 13. Document Generation Rules

Runs automatically as part of the same unattended chain once Step 5's drafts are done — no `generate files` command to wait for.

1. Validate prerequisites from **`.steps/`**; stop and flag as a blocker if any Step 5 MD missing.
2. **Flowchart:** author a JSON spec (`.steps/diagrams/flowchart.json`) per Archify's schema for the `workflow` type, then render it — resolve the CLI with `**/skills/archify/bin/archify.mjs` — to `architecture.html` at the topic-folder root.
3. **Slide decks:** using `skills/frontend-slides/`, author `executive-brief.html` and `engineering-brief.html` directly as self-contained HTML — no build script, no PPTX.
4. **PRD DOCX:** resolve `**/generate_docx.py`; write `.steps/build_docx.py` tailored to this feature, importing `generate_docx.DocxBuilder`. For the PRD's embedded architecture/data-flow image, render a simple static diagram with `matplotlib` (the Archify diagram is interactive HTML, not a static image source — don't try to screenshot it). Run the script to produce `product-requirements.docx`.
5. Fix up to 3 times if generation errors.
6. **Keep** `.steps/build_docx.py` and `.steps/diagrams/*.json` for regeneration.
7. **Do not delete** `.steps/`.
8. Content must be generated from the full analysis files (Steps 1–5), not from a thin paraphrase.
9. Rebuild `analysis.html` afterward (Section 6) — the flowchart gets embedded via its diagram marker; mention the slide decks and DOCX in the report's relevant sections if useful, but they remain separate files, not embedded.

---

## 14. Resume Protocol

There is no single wrapper folder to list — a PM run's topic folder sits directly in the workspace root, named `[slug]/` or `[slug]-enhancement/`.

1. If the PM names the slug (or it's obvious from context), go straight to `[slug]/Progress.md` (or the `-enhancement` variant). Do not scan the workspace root — a directory only counts as a PM run if it actually contains both `Progress.md` and `.steps/`.
2. Read `Progress.md`.
3. Read all `.steps/*.md`.
4. Rebuild `analysis.html` (Section 6) so it reflects everything read.
5. Note which topic-folder deliverables already exist so regeneration doesn't start from scratch unnecessarily.
6. If `Progress.md` shows `blocked_on_pm`, summarize the specific blocker and ask for just that. Otherwise resume the autonomous chain from the next step — do not wait for a `proceed`.

If the PM doesn't know the slug and asks what runs exist, it's fine to look for direct child directories of the workspace root that contain both `Progress.md` and `.steps/` — but never treat an unrelated directory as a PM run just because it exists.

---

## 15. Chat UX Contract

- Keep mid-step narration short; put detail in files.
- Wayfinding is the only step that narrates interactively (Section 8) — every step after it just runs, with Progress.md as the source of "where are we" if asked.
- End the whole run with a summary + the **`analysis.html`** path.
- Batch questions (applies to wayfinding; nothing after it asks questions except a genuine blocker).
- Be decisive.

---

## 16. Non-Goals

- Production Java/JS implementation code in PM artifacts
- Silent scope expansion beyond the wayfinding conclusion
- Pausing between steps for review once wayfinding has concluded
- Secrets/customer private data in a PM run's topic folder
- Putting markdown anywhere but hidden `.steps/`
- Per-step HTML files (superseded by the single `analysis.html`)
- PPTX or PDF output of any kind (superseded by HTML slide decks and Archify diagrams)
- Deleting md/deliverables after generation
- Thin placeholder slide decks or flowcharts

---

## 17. Token & File Discipline (skill-authoring convention)

Applies whenever a skill in this repo is written or edited — new skills and edits to the existing 14 alike.

### Don't duplicate content that's already mandatory context

Every pipeline step already loads this file and `product-context.md` in full (Sections 1-16, ~1,000 lines) before it runs. **Never re-state a procedure this file already documents** — point to the section instead (`See context/pm-operating-system.md §6` beats copy-pasting the same three paragraphs into 14 files). The "Report rebuild" procedure in Sections 3, 6, and 11a is the canonical example: every step skill's own "Report rebuild" section is a one-paragraph pointer here, not a restatement — that used to be ~19 duplicated lines × 14 files (~266 lines of pure redundancy) before this section existed.

### Progressive disclosure only pays off for conditional content

A separate `references/*.md` file that's loaded *every single time* the skill runs provides no token savings over inlining it — the agent ends up reading the same total content either way, just across more tool calls. It only pays off when the reference is read on a **branch that doesn't always fire** — see Archify's own `SKILL.md` ("Read only those files... do not read the optional Viewer Runtime reference unless the user asks," "read `references/brand-marks.md` only for an unknown brand") for the pattern done right: bound the default path tightly, defer anything conditional. Before splitting a large `SKILL.md`, check whether the content in question is actually conditional — if every run needs all of it (e.g. Step 5 drafting all four deliverable documents in one continuous pass), splitting adds file-hop overhead for no real savings; the fix there is trimming genuinely dead or redundant content, not fragmenting live content.

### Scope reads narrowly, the way Archify's own SKILL.md does

When a step needs to consult a large directory (schemas, examples, a vendored tool's docs), name the exact file(s) to read, not the whole directory — e.g. "read one matching schema in `schemas/`... read only those files," not "see `schemas/`." Vague scoping invites reading everything in the directory out of caution.

### Verify stale content directly, don't assume it's still correct

A skill file can go quietly wrong when something it depends on changes elsewhere in the repo (a deleted script, a renamed method, a retired format) without the skill's own prose being updated — the file still parses, still reads plausibly, and nothing errors until the model tries to act on a reference that no longer exists. This has happened twice in this repo already: `python-pptx`/`PresentationBuilder` method names (`add_kpi_slide()`, etc.) survived in `deliverables/SKILL.md` and `enhancement-deliverables/SKILL.md` well after `generate_pptx.py` was deleted, and existing/new/modified color-coding (an enhancement-only concept) leaked into the *feature* pipeline's engineering-deck instructions via copy-paste. Both were found by tracing what the instruction actually pointed to, not by re-reading the prose for plausibility. When editing a skill that references another file, tool, or API, confirm that reference still exists and still means what the prose says — don't take a plausible-sounding instruction on faith just because it isn't obviously wrong.
