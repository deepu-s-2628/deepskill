# ITOM PM Toolkit — Operating System

> Shared rules for **wayfind**, **PM Feature Agent**, and **PM Enhancement Agent**.
> Load this file at the start of every PM pipeline run (new or resume).
> **Last updated:** 2026-09-11.
>
> **What is this file?** Single shared rulebook so wayfind and both pipelines stay consistent (paths, language bar, wayfinding-then-autonomous execution, the consolidated report, retention, quality gates, dense deliverables, resume).

---

## 1. Mission

Produce opinionated, **immediately usable** product work for **OpManager Plus / OpManager Nexus**:
wayfind → research → analysis → definition → **dense PPTX/PDF/DOCX** → Lovable wireframe prompt → **one consolidated HTML report**.

Agents are **product operators**, not brainstorming chatbots. Prefer one clear recommendation over option menus.

**Audience default:** many reviewers are developers who are **not** specialists in the technology. Write so a competent generalist engineer can follow.

**Deliverable bar:** PPT, flowchart, and PRD must be rich enough to present or hand to engineering **without** a cleanup pass. Thin bullet decks are a fail.

---

## 2. Wayfinding Comes First — Always

Before any research step runs, the `wayfind` skill interrogates the request: does this actually belong in OpManager Plus/Nexus, is it a feature or an enhancement, and what does the rest of the pipeline need locked down before it can run unattended. See `skills/wayfind/SKILL.md` for the full interview process.

Wayfind is the **only** interactive step in the whole pipeline (Section 8). It concludes one of three ways, and nothing downstream may skip or second-guess this conclusion:

| Conclusion | What happens next |
|---|---|
| **Proceed — Feature** | `.steps/0_wayfinding.md` written; hand off to the feature pipeline, Step 1 = `brainstorm` |
| **Proceed — Enhancement** | `.steps/0_wayfinding.md` written; hand off to the enhancement pipeline, Step 1 = `current-state-analysis` |
| **Stop — Not a fit** | No result folder created. Explain why plainly and stop. |

Trigger language (`build` / `new feature` vs `enhance` / `improve`) is a starting signal for wayfind's mode question — never a substitute for actually asking it. Do **not** mix pipelines in the same result folder.

---

## 3. Canonical Paths (one consolidated report; Markdown hidden)

### Workspace root
All paths are relative to the **opened workspace root**.

### Feature pipeline
```
ITOM-PM-Result/
└── [slug]/
    ├── STATUS.md                 ← always visible control plane
    ├── report.html               ← THE deliverable: one navigable HTML, rebuilt after every step
    ├── .steps/                   ← HIDDEN markdown source of truth (agent edit/resume)
    │   ├── 0_wayfinding.md
    │   ├── 1_brainstorm.md
    │   ├── 2_competitive_analysis.md
    │   ├── 3_technical_analysis.md
    │   ├── 4_feature_definition.md
    │   ├── 5a_executive_presentation.md
    │   ├── 5b_engineering_presentation.md
    │   ├── 5c_feature_flowchart.md
    │   ├── 5d_product_requirements.md
    │   └── 6_lovable_wireframe.md
    └── Generated/                ← binary deliverables + diagrams + build script
        ├── build_documents.py    ← keep after success
        ├── diagrams/              ← Archify-rendered HTML diagrams live here, referenced from .steps/*.md
        ├── executive_presentation.pptx
        ├── engineering_presentation.pptx
        ├── feature_flowchart.pdf
        └── product_requirements.docx
```

### Enhancement pipeline
Same pattern under `ITOM-PM-Result/[slug]-enhancement/`:
- `.steps/*.md` — hidden sources, starting with `0_wayfinding.md`
- `report.html` — the one consolidated deliverable
- `Generated/` — binaries + diagrams

### Hard rules
1. **Markdown always under hidden `.steps/`** — never put step `.md` in the feature root.
2. **There is exactly one visible review artifact per run: `report.html`** at the feature-root level. No per-step HTML files.
3. **After every step**, regenerate the report: `python "<scripts-dir>/build_report.py" "ITOM-PM-Result/[folder]/"`. Never let `report.html` fall behind `.steps/`.
4. **Binaries always under `Generated/`**; Archify diagrams go in `Generated/diagrams/` and get referenced from the relevant step's markdown with a `<!-- diagram: Generated/diagrams/<name>.html -->` marker line — `build_report.py` turns that into an embedded, interactive `<iframe>` in the right section.
5. **Retention — never delete** `.steps/*.md`, `report.html`, `STATUS.md`, or `Generated/*` (including `build_documents.py`) after PPTX/PDF/DOCX generation.
6. Do not invent alternate layout names (`output/`, `docs/`, `steps/`).
7. Chat summaries should **highlight the `report.html` path** for reviewers; mention MD only as internal source.

### Report rebuild command
```bash
python "<scripts-dir>/build_report.py" "ITOM-PM-Result/[folder]/"
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

## 5. STATUS.md (Control Plane)

Create/update `ITOM-PM-Result/[folder]/STATUS.md` at every step boundary.

```markdown
# STATUS — [Feature Display Name]

| Field | Value |
|-------|-------|
| Mode | feature \| enhancement |
| Slug | [slug] |
| Folder | ITOM-PM-Result/[folder]/ |
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

On resume: read `STATUS.md`, then all **`.steps/*.md`**, then rebuild `report.html` before continuing.

---

## 6. Markdown (hidden source) → consolidated report (visible)

After writing or revising any step's markdown:

1. Save markdown to **`.steps/<name>.md`**. This is the source of truth for edits and for `generate files`.
2. Rebuild the report: `python "<scripts-dir>/build_report.py" "ITOM-PM-Result/[folder]/"`. This regenerates the **whole** `report.html` from every `.steps/*.md` file that exists so far — cheap, so do it after every step, not just at the end.
3. If a step produced a diagram worth showing (see Section 11a), reference it from that step's markdown with a `<!-- diagram: Generated/diagrams/<name>.html -->` marker before rebuilding — `build_report.py` turns it into an embedded, interactive frame.
4. **Never delete** `.steps/*.md` or `report.html` after binary generation.
5. Final chat completion (after the whole run finishes) must cite the **`report.html` path**.

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
3. Rebuild `report.html` (Section 6).
4. Update `STATUS.md`.
5. Move immediately to the next step. Do not stop and wait.

### The two real exceptions
- **Hard blocker with no safe default** (e.g. the wireframe step needs real screenshots and none exist, or a step's own quality gate fails and can't be self-corrected): pause, ask the *specific* thing needed, resume the same run once answered. This is a genuine dependency gap, not a review gate.
- **The PM interrupts mid-run** (sends a new message while a run is in progress): stop what you're doing, address what they said, then resume the autonomous chain unless they've asked you to stop for good.

### Special commands (still honored if the PM uses them mid- or post-run)
| PM says | Action |
|---------|--------|
| `redo step N` / feedback on step N | Revise step N only, rebuild the report, then resume the autonomous chain from where it left off |
| `status` / `where are we` | Summarize from `STATUS.md` + `.steps/` + `report.html` |
| `pause` / `stop` | Stop; leave `STATUS.md` accurate so the run can resume later |

There is no `generate files` command to wait for anymore — document generation (Section 13) runs automatically as part of the same unattended chain once Step 5's drafts are done.

---

## 9. Research Bar (Minimum Evidence)

### Every analysis step must
- Use `context/ITOM-PM/product-context.md`.
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

## 11. Dense deliverables bar (PPT / Flowchart / PRD)

### Principle
Step 5 drafts and the document-generation outputs built from them must **transfer the analysis**, not summarize it into a few vague bullets. A reader who only opens the PPT or flowchart PDF should still get the full decision trail.

### Must pull forward from prior steps
- Persona challenges and how each is solved
- Competitive gaps we exploit
- **Every** recommended metric category (not a cherry-picked subset)
- Collection method + prerequisites + key OIDs/API endpoints (engineering deck & flowchart)
- Architecture / data flow / discovery / polling / alert logic
- Scale limits, risks, phasing, open questions
- Explicit in-scope / out-of-scope

### Executive PPT
- Still strategic, but **not thin**: each slide needs concrete points, numbers, and named capabilities from the analysis.
- Include a competitive snapshot with real differentiators (not “we will monitor better”).
- Capability slides must list the actual v1 capabilities from feature definition.
- Success metrics must be specific and measurable.

### Engineering PPT
- **Detailed and immediately usable** by eng leads.
- Include collection comparison (why primary won).
- Metrics tables split across slides as needed — **do not drop metrics**.
- Dedicated slides for OID/API inventory highlights (or appendix slides).
- Architecture, data model, polling, alerting, scale, risks, phasing, open questions.
- Prefer 18–25 slides when content requires it rather than compressing into vague 12.

### Flowchart PDF
- Multiple pages: overview, setup/onboarding, discovery, collection pipeline (with protocol/API branch detail), processing/storage, alerting/notification, failure/retry, EE/probe path if relevant, daily operator loop.
- Every major decision diamond labeled with the real condition from analysis.
- Annotate key OIDs/endpoints on collection nodes where space allows.
- Must be followable without reading the PRD.

### Fail conditions
- PPT that could apply to any feature with names swapped
- Flowchart with only 5 generic boxes
- Engineering deck missing metrics or collection contract
- “Update later” placeholders, TBD-only slides, or lorem content

---

## 11a. Diagrams in the report: Archify vs. plain text

`report.html` can embed real, interactive diagrams — use judgment on when one earns its place:

- **Use Archify** (the `archify` skill) for anything with real structure worth exploring: architecture/data-flow (Section 9's collection pipeline), the feature flowchart, a before/after comparison for an enhancement. Save the rendered HTML to `Generated/diagrams/<name>.html`, then reference it from the relevant step's markdown with `<!-- diagram: Generated/diagrams/<name>.html -->` (Section 6).
- **Skip the diagram** and just write it out when a short table or a few sentences say the same thing without asking the reader to parse a shape — e.g. a two-option comparison, a short ordered list of steps. A diagram that doesn't earn more clarity than prose is padding.
- The flowchart PDF (`generate_flowchart.py`, Section 13) still gets generated separately for the binary deliverables — Archify is for `report.html`, not a replacement for the PDF.

---

## 12. Quality Gates (Do Not Mark Step Complete If Failed)

### Global
- [ ] Markdown under **`.steps/`** (hidden)
- [ ] `report.html` rebuilt after this step (Section 6)
- [ ] `STATUS.md` updated
- [ ] Chat summary (final, end-of-run) cites the **`report.html`** path
- [ ] No implementation source code in artifacts
- [ ] No deletion of prior `.steps` / `Generated` files
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
- [ ] Generators resolved via `**/generate_pptx.py`
- [ ] PPT/flowchart meet dense deliverables bar (section 11)
- [ ] Layout diversity rules met
- [ ] `build_documents.py` kept
- [ ] `.steps/*.md` still present after generation
- [ ] PPTX/PDF/DOCX openable and content-complete

### Step 6 wireframe
- [ ] `.steps/` path correct, report rebuilt
- [ ] Enhancement: screenshots first — this is the one place a real blocker can still pause the run (Section 8)
- [ ] Paste-ready Lovable prompt
- [ ] Scope matches wayfinding conclusion only

---

## 13. Document Generation Rules

Runs automatically as part of the same unattended chain once Step 5's drafts are done — no `generate files` command to wait for.

1. Validate prerequisites from **`.steps/`**; stop and flag as a blocker if any Step 5 MD missing.
2. Resolve generators with `file_search` `**/generate_pptx.py`.
3. `pip install -r requirements.txt` if imports fail.
4. Write `Generated/build_documents.py` tailored to this feature.
5. Run it; fix up to 3 times.
6. **Keep** `build_documents.py`.
7. **Do not delete** `.steps/`.
8. Intermediate PNGs under `Generated/diagrams/`.
9. Content must be generated from the full analysis files (Steps 1–5), not from a thin paraphrase.
10. Rebuild `report.html` afterward (Section 6) — mention the generated binaries in the report's relevant sections if useful, but they remain separate files, not embedded.

---

## 14. Resume Protocol

1. List `ITOM-PM-Result/`.
2. Read `STATUS.md`.
3. Read all `.steps/*.md`.
4. Rebuild `report.html` (Section 6) so it reflects everything read.
5. Note `Generated/`.
6. If `STATUS.md` shows `blocked_on_pm`, summarize the specific blocker and ask for just that. Otherwise resume the autonomous chain from the next step — do not wait for a `proceed`.

---

## 15. Chat UX Contract

- Keep mid-step narration short; put detail in files.
- Wayfinding is the only step that narrates interactively (Section 8) — every step after it just runs, with STATUS.md as the source of "where are we" if asked.
- End the whole run with a summary + the **`report.html`** path.
- Batch questions (applies to wayfinding; nothing after it asks questions except a genuine blocker).
- Be decisive.

---

## 16. Non-Goals

- Production Java/JS implementation code in PM artifacts
- Silent scope expansion beyond the wayfinding conclusion
- Pausing between steps for review once wayfinding has concluded
- Secrets/customer private data in `ITOM-PM-Result/`
- Putting markdown anywhere but hidden `.steps/`
- Per-step HTML files (superseded by the single `report.html`)
- Deleting md/report after binary generation
- Thin placeholder PPT/flowcharts
