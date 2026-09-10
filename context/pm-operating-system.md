# ITOM PM Toolkit — Operating System

> Shared rules for **PM Feature Agent** and **PM Enhancement Agent**.
> Load this file at the start of every PM pipeline run (new or resume).
> **Last updated:** 2026-08-10.
>
> **What is this file?** Single shared rulebook so Feature and Enhancement pipelines stay consistent (paths, language bar, dual MD→HTML output, retention, quality gates, dense deliverables, resume).

---

## 1. Mission

Produce opinionated, **immediately usable** product work for **OpManager Plus / OpManager Nexus**:
research → analysis → definition → **HTML review drafts** → **dense PPTX/PDF/DOCX** → Lovable wireframe prompt.

Agents are **product operators**, not brainstorming chatbots. Prefer one clear recommendation over option menus.

**Audience default:** many reviewers are developers who are **not** specialists in the technology. Write so a competent generalist engineer can follow.

**Deliverable bar:** PPT, flowchart, and PRD must be rich enough to present or hand to engineering **without** a cleanup pass. Thin bullet decks are a fail.

---

## 2. Pipeline Modes

| Mode | Trigger language | Folder suffix | Step 1 skill |
|------|------------------|---------------|--------------|
| **Feature** (net-new) | build / new feature / add support for | `[slug]/` | `ITOM-PM-brainstorm` |
| **Enhancement** (existing) | enhance / improve / what's missing | `[slug]-enhancement/` | `ITOM-PM-current-state-analysis` |

If intent is ambiguous, ask **one** batch of clarifying questions, then pick a mode and proceed.
Do **not** mix pipelines in the same result folder.

---

## 3. Canonical Paths (HTML visible; Markdown hidden)

### Workspace root
All paths are relative to the **opened workspace root**.

### Feature pipeline
```
ITOM-PM-Result/
└── [slug]/
    ├── STATUS.md                 ← always visible control plane
    ├── .steps/                   ← HIDDEN markdown source of truth (agent edit/resume)
    │   ├── 1_brainstorm.md
    │   ├── 2_competitive_analysis.md
    │   ├── 3_technical_analysis.md
    │   ├── 4_feature_definition.md
    │   ├── 5a_executive_presentation.md
    │   ├── 5b_engineering_presentation.md
    │   ├── 5c_feature_flowchart.md
    │   ├── 5d_product_requirements.md
    │   └── 6_lovable_wireframe.md
    ├── steps/                    ← VISIBLE HTML for human review (open in browser)
    │   ├── 1_brainstorm.html
    │   ├── 2_competitive_analysis.html
    │   ├── 3_technical_analysis.html
    │   ├── 4_feature_definition.html
    │   ├── 5a_executive_presentation.html
    │   ├── 5b_engineering_presentation.html
    │   ├── 5c_feature_flowchart.html
    │   ├── 5d_product_requirements.html
    │   └── 6_lovable_wireframe.html
    └── Generated/                ← binary deliverables + diagrams + build script
        ├── build_documents.py    ← keep after success
        ├── diagrams/
        ├── executive_presentation.pptx
        ├── engineering_presentation.pptx
        ├── feature_flowchart.pdf
        └── product_requirements.docx
```

### Enhancement pipeline
Same pattern under `ITOM-PM-Result/[slug]-enhancement/`:
- `.steps/*.md` — hidden sources
- `steps/*.html` — visible review HTML
- `Generated/` — binaries

### Hard rules
1. **Markdown always under hidden `.steps/`** — never put step `.md` in feature root or in visible `steps/`.
2. **HTML always under visible `steps/`** — every step must produce a browser-openable `.html` with the **same basename** as its `.md`.
3. **Every step is dual-format:** write `.steps/N_name.md` then generate `steps/N_name.html`.
4. **Binaries always under `Generated/`**.
5. **Retention — never delete** `.steps/*.md`, `steps/*.html`, `STATUS.md`, or `Generated/*` (including `build_documents.py`) after PPTX/PDF/DOCX generation.
6. Do not invent alternate layout names (`output/`, `docs/`).
7. Chat summaries should **highlight the HTML path** for reviewers; mention MD only as internal source.

### Convert command
```bash
python "<scripts-dir>/md_to_html.py" \
  "ITOM-PM-Result/[folder]/.steps/1_brainstorm.md" \
  "ITOM-PM-Result/[folder]/steps/1_brainstorm.html"
```
Resolve helper via `**/md_to_html.py` (`scripts/ITOM-PM/` or `assets/scripts/ITOM-PM/`).

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
| Step status | in_progress \| blocked_on_pm \| complete |
| Last updated | [YYYY-MM-DD] |
| Next action | wait_for_proceed \| revise_step_N \| generate_files \| step_N+1 \| done |

## Completed steps
- [x] Step 1 — ... (`.steps/1_….md` → `steps/1_….html`)
- [ ] Step 2 — ...

## Open questions for PM
1. ...

## Key decisions locked
- ...

## Risks / blockers
- ...
```

On resume: read `STATUS.md`, then all **`.steps/*.md`** (HTML is for humans).

---

## 6. Dual output: Markdown (hidden) + HTML (visible)

After writing or revising any step markdown:

1. Save markdown to **`.steps/<name>.md`**.
2. Generate HTML to **`steps/<name>.html`** with `md_to_html.py`.
3. Markdown = source of truth for edits and `generate files`.
4. HTML = what DOE/developers open and review.
5. On revise, regenerate **both**.
6. **Never delete** either after binary generation.
7. Chat completion must cite the **HTML path first**.

If the helper is unavailable, write a simple styled HTML document — prefer the helper.

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

## 8. Sequential Workflow & Approval Gates

1. Produce **one step** at a time.
2. Write `.steps/*.md` **and** `steps/*.html`.
3. Update `STATUS.md`.
4. Post chat summary with **HTML path** (and MD path as source).
5. **PAUSE** for PM review.
6. Proceed only on explicit approval: `proceed`, `approved`, `lgtm`, `continue`.
7. On feedback: revise **only that step** (md+html).

### Special commands
| PM says | Action |
|---------|--------|
| `proceed` / `continue` | Next step |
| `redo step N` / feedback on step N | Revise step N only |
| `generate files` | Doc-gen skill; **do not delete** `.steps/` or `steps/` afterward |
| `status` / `where are we` | Summarize from STATUS + `.steps/` + visible `steps/*.html` |
| `pause` / `stop` | Stop; leave STATUS accurate |

Do **not** auto-run `generate files` or Step 6 without approval.

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
Step 5 drafts and Step “generate files” outputs must **transfer the analysis**, not summarize it into a few vague bullets. A reader who only opens the PPT or flowchart PDF should still get the full decision trail.

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

## 12. Quality Gates (Do Not Mark Step Complete If Failed)

### Global
- [ ] Markdown under **`.steps/`** (hidden)
- [ ] HTML under visible **`steps/`**
- [ ] `STATUS.md` updated
- [ ] Chat summary cites **HTML path** for review
- [ ] No implementation source code in artifacts
- [ ] No deletion of prior `.steps` / `steps` / `Generated` files
- [ ] External claims cited or labeled assumptions
- [ ] Plain language where required (esp. Steps 1–2)

### Feature Step 1 — Brainstorm
- [ ] Plain English; jargon defined on first use
- [ ] What / why people use it / problem / easy example
- [ ] 2–3 named persona stories
- [ ] Module fit + reuse
- [ ] `.steps/1_brainstorm.md` + `steps/1_brainstorm.html`

### Feature Step 2 / Enhancement Step 3 — Competitive
- [ ] ≥4 competitors or exception
- [ ] Persona-challenge matrix
- [ ] Recommended market position
- [ ] md + html paths correct

### Feature Step 3 — Technical
- [ ] All viable collection methods evaluated
- [ ] Single primary method + fallbacks
- [ ] Deep OID/API/telemetry inventory for primary (and major alt if close)
- [ ] Metrics categorized with thresholds/frequency
- [ ] Scale + failure modes + EE/security
- [ ] Persona challenges solved technically
- [ ] Sources cited
- [ ] md + html paths correct

### Feature Step 4 / Enhancement Step 4
- [ ] In-scope vs out-of-scope
- [ ] Persona → capability traceability
- [ ] Decisive phasing
- [ ] md + html paths correct

### Step 5 drafts
- [ ] All four under `.steps/` + HTML twins in `steps/`
- [ ] Exec and eng decks are not near-duplicates
- [ ] Eng deck + flowchart carry full analysis density (metrics, collection contract, flows)
- [ ] No TBD/lorem placeholders
- [ ] PRD testable

### Generate files
- [ ] All prerequisite **`.steps/`** markdown files exist
- [ ] Generators resolved via `**/generate_pptx.py`
- [ ] PPT/flowchart meet dense deliverables bar (section 11)
- [ ] Layout diversity rules met
- [ ] `build_documents.py` kept
- [ ] `.steps/*.md` and `steps/*.html` still present after generation
- [ ] PPTX/PDF/DOCX openable and content-complete

### Step 6 wireframe
- [ ] md in `.steps/`, html in `steps/`
- [ ] Enhancement: screenshots first
- [ ] Paste-ready Lovable prompt
- [ ] Scope matches approval only

---

## 13. Document Generation Rules

1. Validate prerequisites from **`.steps/`**; stop if any Step 5 MD missing.
2. Resolve generators with `file_search` `**/generate_pptx.py`.
3. `pip install -r requirements.txt` if imports fail.
4. Write `Generated/build_documents.py` tailored to this feature.
5. Run it; fix up to 3 times.
6. **Keep** `build_documents.py`.
7. **Do not delete** `.steps/` or `steps/`.
8. Intermediate PNGs under `Generated/diagrams/`.
9. Content must be generated from the full analysis files (Steps 1–5), not from a thin paraphrase.

---

## 14. Resume Protocol

1. List `ITOM-PM-Result/`.
2. Read `STATUS.md`.
3. Read all `.steps/*.md`.
4. Note `steps/*.html` and `Generated/`.
5. Summarize 3–6 bullets; ask next action.

---

## 15. Chat UX Contract

- Keep mid-step narration short; put detail in files.
- End every step with summary + **HTML review path** + required reply keyword.
- Batch questions.
- Be decisive.

---

## 16. Non-Goals

- Production Java/JS implementation code in PM artifacts
- Silent scope expansion after approval
- Auto-cascading later steps after an early rewrite
- Secrets/customer private data in `ITOM-PM-Result/`
- Putting review HTML only in hidden folders
- Putting markdown in the visible `steps/` folder
- Deleting md/html after binary generation
- Thin placeholder PPT/flowcharts
