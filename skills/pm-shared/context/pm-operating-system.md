# ITOM PM Toolkit — Operating System

> Shared rules for **ask-deepu**, **PM Feature Agent**, and **PM Enhancement Agent**.
> Load this file at the start of every PM pipeline run (new or resume).
> **Last updated:** 2026-09-11.
>
> **What is this file?** Single shared rulebook so ask-deepu's wayfinding phase and both pipelines stay consistent (paths, language bar, wayfinding-then-autonomous execution, the consolidated report, retention, quality gates, dense deliverables, resume).

---

## 0. Resolving shared files (read this first)

`context/pm-operating-system.md`, `product-context.md`, `CONTEXT.md`, and the Python generators (`build_report.py`, `generate_docx.py`, `md_to_html.py`) all live in a shared sibling skill called **`pm-shared`** — not inside whichever skill is currently running. `npx skills add` installs every skill in this package as a direct sibling of every other, under one common parent directory, regardless of how deeply any of them were nested in the source repo (a pipeline-bucketed skill like `skills/feature-pipeline/brainstorm/` still installs flat, as a sibling of `pm-shared` — the bucket is dropped). So the path from any skill to shared data is always the same shape, one level up, unconditionally. **There is no environment variable involved anywhere in this** — `os.environ["CLAUDE_PLUGIN_ROOT"]` or similar in a Python script you write (e.g. `.steps/build_docx.py`) will not work.

Resolve the real value this way, once per run:

1. Claude Code (or whatever agent surface is running) shows every loaded skill its own real, resolved installed location as **"Base directory for this skill"** (e.g. `.../skills/ask-deepu` or `.../skills/brainstorm` — installed skills are always one level deep under a common `skills/` parent, regardless of any bucket they lived in inside the source repo).
2. Go up exactly one level from that path — that's the shared parent directory every installed skill sits in.
3. From there, shared files are at `pm-shared/context/<file>` and `pm-shared/scripts/<file>`; other vendored tools are siblings the same way (`archify/...`, `frontend-slides/...`, `unlazy-gates/...`, `design-taste/...`).
4. Treat the resulting absolute path as a literal resolved string for the rest of this run. Substitute it directly wherever `pm-shared/...` appears below and in any pipeline skill, in every `Read`/`python`/`node` invocation, and when writing any generated script — write the literal resolved path there (e.g. `SCRIPTS_DIR = "/Users/.../skills/pm-shared/scripts"`), never an environment variable.
5. Resolve it once — right after wayfinding, or at the start of a resumed session — and reuse that value for the rest of the run. Don't re-derive it every step.

Every other reference in this repo to "resolve shared files" points back to this section rather than repeating the procedure (Section 17's token-discipline convention).

---

## 1. Mission

Produce opinionated, **immediately usable** product work for **OpManager Plus / OpManager Nexus**:
wayfinding → research → analysis → definition → **dense HTML slide deck + Archify diagram + DOCX PRD** → **one consolidated HTML report**, with an optional Lovable wireframe prompt + static prototype the PM can request once everything else is ready.

Agents are **product operators**, not brainstorming chatbots. Prefer one clear recommendation over option menus.

**Audience default:** many reviewers are developers who are **not** specialists in the technology. Write so a competent generalist engineer can follow.

**Deliverable bar:** the slide deck, flowchart, and PRD must be rich enough to present or hand to engineering **without** a cleanup pass. Thin bullet decks are a fail.

---

## 2. Wayfinding Comes First — Always

Before any research step runs, `ask-deepu` interrogates the request itself: does this actually belong in OpManager Plus/Nexus, is it a feature or an enhancement, and what does the rest of the pipeline need locked down before it can run unattended. See `skills/ask-deepu/SKILL.md` for the full interview process — there is no separate wayfinding skill; it's `ask-deepu`'s own first phase.

Wayfinding is the **first** of two sanctioned interactive checkpoints in the whole pipeline (Section 8) — the second comes after Step 5 and document generation, asking only whether the PM wants the optional Step 6 wireframe deliverables. Wayfinding itself concludes one of three ways, and nothing downstream may skip or second-guess this conclusion:

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
├── prototype.html              ← static-HTML mockup of the primary screen (Step 6, opt-in — §8; design-taste §11b)
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
    ├── GATES-N.md               ← per-step unlazy-gates ledger (§18), one per step, e.g. GATES-3.md
    ├── diagrams/                ← Archify JSON specs (source for the flowchart HTML)
    │   └── flowchart.json
    └── build_docx.py            ← keep after success; regenerates product-requirements.docx
```

### Enhancement pipeline

Same flat pattern, folder named `[slug]-enhancement/`:
- `.steps/*.md` — hidden sources, starting with `0_wayfinding.md`
- `analysis.html` — the one consolidated deliverable
- `architecture.html`, `executive-brief.html`, `engineering-brief.html`, `product-requirements.docx` — same deliverable set as feature mode; `prototype.html` and `.steps/6_*.md` only exist if the PM opts into Step 6 (§8)

### Hard rules

1. **Markdown always under hidden `.steps/`** — never put step `.md` in the topic-folder root.
2. **There is exactly one visible review artifact for the analysis itself: `analysis.html`** at the topic-folder root. No per-step HTML files.
3. **After every step**, regenerate the report: `python "<resolved shared parent>/pm-shared/scripts/build_report.py" "[slug]/"`. Never let `analysis.html` fall behind `.steps/`. (`build_report.py` derives the output filename from the folder name — it always matches.)
4. **Diagrams are Archify HTML**, visible at the topic-folder root (e.g. `architecture.html`) *and* referenced from the relevant step's markdown with a `<!-- diagram: architecture.html -->` marker line — `build_report.py` turns that into an embedded, interactive `<iframe>` in the right section. There is no PDF flowchart.
5. **Slide decks are HTML** (`frontend-slides`), not PPTX. Two decks — `executive-brief.html` (executive audience) and `engineering-brief.html` (engineering audience) — each self-contained, animation-capable, and openable directly in a browser.
6. **The PRD stays DOCX** (`python-docx`), unchanged from before.
7. **Retention — never delete** `.steps/*.md`, `analysis.html`, `Progress.md`, the deliverable files at the topic-folder root (including `prototype.html`, when the PM opted into it), `.steps/build_docx.py`, or `.steps/GATES-N.md` (§18) — a gate ledger is evidence of what was checked, not scratch work.
8. Do not invent alternate layout names (`output/`, `docs/`, `Generated/`, `steps/` without the dot).
9. Chat summaries should **highlight the `analysis.html` path** for reviewers; mention MD only as internal source.

### Report rebuild command

`build_report.py` and `md_to_html.py` both live in the sibling `pm-shared` skill's `scripts/` — resolve the shared parent directory per Section 0 above if not already known this session, then substitute the literal resolved path everywhere below.

```bash
python "<resolved shared parent>/pm-shared/scripts/build_report.py" "[slug]/"
```
No glob search needed — the location is fixed once resolved.

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
| Next action | resolve_blocker \| step_N+1 \| awaiting_step6_choice \| done |

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
2. Rebuild the report: `python "<resolved shared parent>/pm-shared/scripts/build_report.py" "[folder]/"`. This regenerates the **whole** `analysis.html` from every `.steps/*.md` file that exists so far — cheap, so do it after every step, not just at the end.
3. If a step produced a diagram worth showing (see Section 11a), render it with Archify to a visible sibling file (e.g. `architecture.html`) and reference it from that step's markdown with a `<!-- diagram: architecture.html -->` marker before rebuilding — `build_report.py` turns it into an embedded, interactive frame.
4. **Never delete** `.steps/*.md` or `analysis.html` after binary/HTML generation.
5. Final chat completion (after the whole run finishes) must cite the **`analysis.html` path**.

If `build_report.py` is unavailable at the resolved `pm-shared/scripts/`, fall back to `md_to_html.py` per-step and note in chat that the consolidated report couldn't be built — this should not happen on a real install.

---

## 7. Plain-language bar (DOE) — the default writing style for every step, not an on-demand fallback

This is the same bar `wait-what` re-pitches to when a PM has to ask for one — "plain words, no unexplained jargon," already named that way in `generate-documents`/`enhancement-generate-documents`. The point of this section is that a PM should never need to invoke `wait-what` in the first place: every step's own written output — not just Step 1, not just executive sections — is held to this bar as it's produced, not corrected after the fact. Applies **hardest** to brainstorm/current-state openers (the reader has the least context there), and still applies in full to every other step's prose, every deliverable draft, and every generated document's section framing.

### Do
- Prefer short sentences and everyday words.
- Define a term the **first** time it appears.
- Use **analogies and concrete examples**.
- Separate **what the technology is** / **why people use it** / **what problem it solves** / **what we monitor**.
- Use this repo's own canonical terms from `CONTEXT.md` — don't introduce a competing name for something already named there.

### Don’t
- Open Step 1 with RFC field dumps.
- Assume the reader already knows why the technology exists.
- Let a later step (competitive analysis, technical analysis, findings, deliverable drafts) drift back into unexplained jargon just because Step 1 already did the plain-language work — each step's own output is judged against this bar independently, not inherited from an earlier step.

### Required technology framing (Feature Step 1)
1. **What is it?**
2. **Why do people use it?**
3. **What problem does it solve?**
4. **Easy example**

---

## 8. Sequential Workflow: Two Sanctioned Checkpoints, Everything Else Runs Unattended

**Two points in the whole pipeline are deliberate, sanctioned checkpoints — every other step runs unattended.** Both are **scope or consent decisions**, never a content review: nothing about Steps 1–5's actual analysis, or Step 6's actual output once it runs, gets re-litigated at either checkpoint.

1. **Wayfinding** (Section 2), before anything runs: does this request even belong in OpManager Plus/Nexus, and in what mode. Concludes "Proceed"/"Stop".
2. **The Step 6 choice**, after Step 5 and document generation finish: does the PM want the optional wireframe deliverables at all. Ask exactly this, in the same lettered-option style as wayfinding:

   > **Analysis and documents are ready:** `analysis.html`, `architecture.html`, `executive-brief.html`, `engineering-brief.html`, `product-requirements.docx`. Would you like the Step 6 wireframe deliverables too?
   >
   > A. Both — the Lovable prompt and a static prototype (Recommended)
   > B. Just the Lovable prompt
   > C. Just the static prototype
   > D. Neither — I'm done here

   - **A/B/C**: run Step 6 (`lovable-wireframe`/`enhancement-wireframe`), scoped to only the artifact(s) chosen. The enhancement pipeline's screenshot-blocking pause (an unplanned exception, below) still applies independently whenever the choice includes anything that needs it — it is not part of this checkpoint.
   - **D**: set `Progress.md`'s `Next action` to `done` immediately. No Step 6 skill runs; `.steps/6_*.md` and `prototype.html` simply don't exist for this run.
   - While waiting for this answer, `Progress.md`'s `Next action` reads `awaiting_step6_choice` (Section 5).

Once either checkpoint resolves toward doing more work, everything from there runs unattended, for each step, in order:
1. Produce the step.
2. Write `.steps/*.md`.
3. Rebuild `analysis.html` (Section 6).
4. Update `Progress.md`.
5. Move immediately to the next step. Do not stop and wait.

### The two real exceptions (unplanned — distinct from the two sanctioned checkpoints above)
- **Hard blocker with no safe default** (e.g. the wireframe step needs real screenshots and none exist, or a step's own quality gate fails and can't be self-corrected): pause, ask the *specific* thing needed, resume the same run once answered. This is a genuine dependency gap, not a review gate.
- **The PM interrupts mid-run** (sends a new message while a run is in progress): stop what you're doing, address what they said, then resume the autonomous chain unless they've asked you to stop for good.

### Special commands (still honored if the PM uses them mid- or post-run)
| PM says | Action |
|---------|--------|
| `redo step N` / feedback on step N | Revise step N only, rebuild the report, then resume the autonomous chain from where it left off |
| `status` / `where are we` | Summarize from `Progress.md` + `.steps/` + `analysis.html` |
| `pause` / `stop` | Stop; leave `Progress.md` accurate so the run can resume later |

There is no `generate files` command to wait for anymore — document generation (Section 13) runs automatically as part of the same unattended chain once Step 5's drafts are done, right up to the Step 6 choice above.

---

## 9. Research Bar (Minimum Evidence)

### Every analysis step must
- Use `pm-shared/context/product-context.md` (resolve the shared parent per Section 0).
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

- **Flowchart / architecture diagrams → Archify.** Use it for anything with real structure worth exploring: architecture/data-flow (Section 9's collection pipeline), the feature flowchart, a before/after comparison for an enhancement. Author a JSON spec under `.steps/diagrams/<name>.json`, render with `node "<resolved shared parent>/archify/bin/archify.mjs" deliver <type> <spec.json> architecture.html --quality showcase`, then reference the visible output from the relevant step's markdown with `<!-- diagram: architecture.html -->` (Section 6).
- **Skip the diagram** and just write it out when a short table or a few sentences say the same thing without asking the reader to parse a shape — e.g. a two-option comparison, a short ordered list of steps. A diagram that doesn't earn more clarity than prose is padding.
- **Slide decks → frontend-slides.** Both the executive and engineering decks (Section 11) are authored as self-contained HTML using `skills/frontend-slides/`'s templates and animation patterns — no PPTX is generated anywhere in this pipeline.
- **License note:** both skills are MIT-licensed. Archify's vendored copy carries `THIRD_PARTY_NOTICES.md` disclosing that a small set of embedded brand-mark icons (used only when a diagram names a real product) carry their own upstream licenses, one of which (Vue.js) is CC-BY-NC-SA-4.0 with a non-commercial, share-alike condition. That notice ships as-is with the vendored copy — do not strip it, and do not use the Vue.js mark for anything beyond identifying the technology in a diagram.

### Standing rule: no hard dependency on an unbundled skill

This still applies to anything **not** vendored into this repo's own `skills/` — added later, or referenced ad hoc. Teammates will have different sets of separately-installed plugins; never assume one is present just because your own machine has it. Every such reference must:
1. Attempt the call, expecting it may not resolve.
2. On failure, degrade to a plain-text/markdown equivalent rather than stopping the step or the run.
3. Never let a failed lookup fall through to invoking a similarly-named but unrelated skill (this is exactly how `wayfind` briefly got confused with an installed-but-unrelated `wayfinder` skill from another plugin, before `wayfind` was folded directly into `ask-deepu` to remove the cross-skill call entirely). When in doubt, prefer inlining the logic into one of this repo's own skills, or vendoring the capability (as done for Archify and frontend-slides), over depending on another plugin's skill by name.

---

## 11b. Design taste for `analysis.html`

`build_report.py`'s CSS follows `skills/design-taste/SKILL.md` — a curated, rewritten-for-this-repo adaptation of the stack-agnostic taste judgment from [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill), not a copy of it (that skill's own React/Motion/npm machinery, and its landing-page structure rules, don't apply to a self-contained static-HTML report). Read that file for the full rationale and rule set; the short version: one accent color held identically everywhere (ManageEngine brand blue, `#0078d4`), a documented two-tier corner-radius scale, row-separator tables instead of a full boxed grid, a readable measure for prose while tables/diagrams keep the full width, and real `:focus-visible` states.

This applies to `analysis.html`'s own styling, and to `prototype.html` (Step 6's static-HTML wireframe, milestone 2 — feature mode picks its own accent per §11b rule 1, enhancement mode's colors come from the extracted current design instead, per `enhancement-wireframe/SKILL.md`) — never to Archify's or frontend-slides' output, which carry their own mature, unrelated style systems (Section 11a).

---

## 12. Quality Gates (Do Not Mark Step Complete If Failed)

The checklists below are the substance of every step's quality bar — what has to be true before a step counts as done. Each of the 14 pipeline skills expresses its own step-specific list here as a real `unlazy-gates` ledger (`.steps/GATES-N.md`), not just prose: a mechanically-checkable item becomes a runnable `CHECK:`/`EXPECT:` gate, a genuine judgment call stays a manual gate — see each skill's own "Quality Gate" section for its exact ledger, and Section 18 for the resolution rule (self-correct on a failed gate, document the gap and continue if it still fails — **never abandon, never pause the run**). The lists below stay the readable summary of what those ledgers check; Section 18 documents the mechanism itself.

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
- [ ] DOCX generator resolved at `pm-shared/scripts/generate_docx.py` (resolved shared parent)
- [ ] Archify resolved at `archify/bin/archify.mjs` (resolved shared parent)
- [ ] Slide decks and flowchart meet the dense deliverables bar (Section 11)
- [ ] `.steps/build_docx.py` kept
- [ ] `.steps/*.md` still present after generation
- [ ] `product-requirements.docx`, `executive-brief.html`, `engineering-brief.html`, `architecture.html` all openable and content-complete

### Step 6 opt-in choice (Section 8)
- [ ] PM asked the A/B/C/D question exactly once, after document generation, before Step 6 might run
- [ ] Chosen scope (both / prompt only / prototype only / neither) respected exactly — no silent expansion or contraction
- [ ] If "neither": `Progress.md` → `done`, no Step 6 skill invoked, `.steps/6_*.md`/`prototype.html` correctly absent

### Step 6 wireframe (only applies when the PM opted in — Section 8)
- [ ] `.steps/` path correct, report rebuilt
- [ ] Enhancement: screenshots first — this is one of the two unplanned exceptions that can still pause the run (Section 8), unrelated to the opt-in choice above
- [ ] If the Lovable prompt was chosen: paste-ready
- [ ] If the prototype was chosen: `prototype.html` written at the topic-folder root, follows `skills/design-taste/SKILL.md` (Section 11b)
- [ ] Scope matches wayfinding conclusion only

---

## 13. Document Generation Rules

Runs automatically as part of the same unattended chain once Step 5's drafts are done — no `generate files` command to wait for.

0. **Bootstrap Python deps once, unattended, if needed.** Resolve the shared parent per Section 0, then check whether `pm-shared/scripts` has its dependencies installed (e.g. a `.venv` present or `python -c "import docx"` succeeding). If not, run `uv sync` inside `pm-shared/scripts` (fall back to `python3 -m venv .venv && source .venv/bin/activate && pip install python-docx Pillow matplotlib` if `uv` isn't available). This is a transparent first-run step — never pause or ask the PM about it.
1. Validate prerequisites from **`.steps/`**; stop and flag as a blocker if any Step 5 MD missing.
2. **Flowchart:** author a JSON spec (`.steps/diagrams/flowchart.json`) per Archify's schema for the `workflow` type, then render it — with `<resolved shared parent>/archify/bin/archify.mjs` — to `architecture.html` at the topic-folder root.
3. **Slide decks:** using `<resolved shared parent>/frontend-slides/`, author `executive-brief.html` and `engineering-brief.html` directly as self-contained HTML — no build script, no PPTX.
4. **PRD DOCX:** using `<resolved shared parent>/pm-shared/scripts/generate_docx.py`, write `.steps/build_docx.py` tailored to this feature, importing `generate_docx.DocxBuilder` (add the literal resolved `pm-shared/scripts` path to the Python path so the import resolves — write it as a literal string in the generated script, never an environment variable). For the PRD's embedded architecture/data-flow image, render a simple static diagram with `matplotlib` (the Archify diagram is interactive HTML, not a static image source — don't try to screenshot it). Run the script to produce `product-requirements.docx`.
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
6. If `Progress.md` shows `blocked_on_pm`, summarize the specific blocker and ask for just that. If it shows `awaiting_step6_choice`, do not re-run Steps 1–5 — they're already complete — just re-surface the same A/B/C/D question from Section 8 and wait. Otherwise resume the autonomous chain from the next step — do not wait for a `proceed`.

If the PM doesn't know the slug and asks what runs exist, it's fine to look for direct child directories of the workspace root that contain both `Progress.md` and `.steps/` — but never treat an unrelated directory as a PM run just because it exists.

---

## 15. Chat UX Contract

- Keep mid-step narration short; put detail in files.
- Wayfinding and the Step 6 choice are the only two points that narrate interactively (Section 8) — every other step just runs, with Progress.md as the source of "where are we" if asked.
- End the whole run with a summary + the **`analysis.html`** path.
- Batch questions (applies to wayfinding and the Step 6 choice; nothing else asks questions except a genuine blocker).
- Be decisive.

---

## 16. Non-Goals

- Production Java/JS implementation code in PM artifacts
- Silent scope expansion beyond the wayfinding conclusion
- Pausing between steps to review a step's *content* once wayfinding has concluded — the Step 6 choice (Section 8) is not this: it's a one-time scope question about whether an entirely optional later deliverable should run at all, never a re-litigation of Steps 1–5's or Step 6's own output
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

---

## 18. Verified Quality Gates (`unlazy-gates`)

`skills/unlazy-gates/` is a curated, **Solo-mode-only** adaptation of `unlazy` (vendored in full — see that skill's own `SKILL.md` for exclusions and attribution), giving Section 12's per-step checklists a mechanically-checkable form instead of a self-reported one. A mechanically-checkable item (a count, a presence/absence check, a file that must exist) becomes a runnable `CHECK:`/`EXPECT:` gate; a genuine qualitative judgment (plain language, no unexplained jargon) stays a manual gate, self-attested exactly as it already was.

### Per step

1. Before producing the step's content, write `.steps/GATES-N.md` (`N` = the step number) from `<resolved shared parent>/unlazy-gates/templates/gates-leaf.md`, one gate per item in that step's Section 12 checklist.
2. Produce the step's content.
3. `node "<resolved shared parent>/unlazy-gates/scripts/gate-check.mjs" --approve .steps/GATES-N.md` (first run) or `--status`/plain re-run (later checks). Lint first with `gate-lint.mjs` if authoring a new ledger from scratch.

### The resolution rule — never `unlazy`'s native `ABANDON`/handoff

This pipeline has exactly two sanctioned pause points (Section 8); a quality gate is neither of them, so a failing gate is never a reason to stop or hand off:

1. **A failing runnable gate**: revise the specific failing content and re-check. Bound to **2–3 retries**.
2. **Still unmet after retries**: do not abandon, do not pause. Note the specific gap in that step's own `.steps/*.md` output as a stated assumption/limitation — the same pattern `current-state-analysis/SKILL.md` already uses when a screenshot isn't available — and move on to the next step. A documented gap is an honest, complete step; a silently-dropped gate is not.
3. **Manual gates** are never mechanically resolved — they're the explicit, single-outcome version of what Section 12's checklists already asked for.

Never install `unlazy`'s optional Stop hook (`scripts/install-hooks.mjs`, deliberately excluded from the vendored copy) — it exists to block a session on unmet gates, which directly contradicts the rule above.

### Retention

`.steps/GATES-N.md` is retained same as every other `.steps/` file (Section 3, hard rule 7) — it's evidence of what was checked and how, not scratch work to clean up after the step completes.
