---
name: brainstorm
description: "Step 1 of PM Feature Pipeline: Understand a feature idea deeply before any analysis begins. Produces a structured brainstorm document covering what it is, why it matters, and who uses it. Use when starting a new feature analysis for OpManager Plus."
---

# Step 1 — Brainstorm

## Purpose

Understand the feature deeply before any analysis begins. This is the foundation for all later steps.

**Audience bar (DOE):** Many reviewers are developers who are **not** specialists in this technology. Write in **simple English**. Prefer short sentences, everyday words, and easy examples. Define every acronym the first time it appears.

## Input

The PM describes a feature they want to build. Examples:
- "I want to add Cisco SD-WAN monitoring support to OpManager Plus"
- "We need to monitor Kubernetes clusters"
- "Add support for monitoring Palo Alto firewalls"

## Process

### 1. Parse the Feature Request

Identify:
- What technology or capability is being requested?
- Is this a net-new feature or an enhancement to something existing?
  - If enhancement → stop and switch to the **PM Enhancement Agent**
- What is the PM's implicit goal? (competitive parity, customer demand, market expansion, upsell)

### 2. Research the Technology (plain language first)

Use web search, then explain results so a non-specialist developer can follow.

You **must** answer all four before any deep protocol detail:

1. **What is it?** — one plain definition
2. **Why do people use it?** — business / ops drivers (cost, scale, agility, multi-tenant, cloud move, etc.)
3. **What problem does it solve?** — "before vs after" in everyday terms
4. **Easy example** — one concrete scenario (office floors, shipping containers, labeled envelopes, hospital clinics, etc.)

Only after that, lightly note how it works and what can be monitored (APIs, SNMP, CLI, telemetry). Do **not** open with RFC field lists.

**Good framing (VXLAN-style):**
> VXLAN is a way to create a big virtual network on top of a normal IP network. Companies use it so servers in different buildings can act like they sit on the same simple office LAN — without rewiring the physical network. Think of putting letters in identical envelopes so any postal truck can carry them; the envelope is the VXLAN tunnel, the letter is the original network traffic.

**Bad framing:**
> VXLAN encapsulates Layer-2 Ethernet frames in UDP port 4789 with a 24-bit VNI…

### 3. Map to OpManager Plus

Reference [context/product-context.md](../../../context/product-context.md):
- Where does this feature fit?
- Which module would house it?
- Overlap with anything already in the product?
- What existing infrastructure can be reused? (polling, alerts, DB, UI)

Explain module fit in plain language too ("this lives next to our existing network device monitoring, not a brand-new product").

### 4. Craft Persona Stories (with easy examples)

Create 2–3 vivid persona stories. These are **not** Agile user stories. They are short narratives a developer or DOE reviewer can picture.

Each story must:
- **Name the person** — real name, job title, company type, rough scale
- **Show daily reality** — tools, pressures
- **Show a specific failure moment** — time, impact, who noticed
- **Include one easy-to-picture example** of the failure (not only "visibility gap")
- **End with transformation** — "With [capability] in OpManager Plus, …"

These stories are reused in exec/eng decks, PRD, and wireframes.

**Good example:**
> Meet Priya, a Senior Network Engineer at a regional hospital chain with 14 locations. Every Monday she dreads her inbox. Last month the SD-WAN path to a rural clinic got slow for six hours. Nobody knew until a nurse called because telehealth video froze mid-consultation. Priya already watched routers, servers, and apps — but the SD-WAN "virtual roads" between sites were a blind spot. She tracked tunnel status by hand in a spreadsheet after SSH-ing into controllers. By the time she found the bad path, the clinic was on a backup 4G hotspot and had burned its data cap. With SD-WAN monitoring in OpManager Plus, Priya would have seen the path degrade within minutes, gotten an alert before the nurse noticed, and moved traffic to a healthy path.

**Bad example:**
> Network administrators need SD-WAN monitoring to track tunnel health.


## Report rebuild (mandatory)

Every step artifact this skill writes must:

1. **Markdown (source of truth, hidden):** `[slug]/.steps/<name>.md`
   - Enhancement mode: `[slug]-enhancement/.steps/<name>.md`
2. **Rebuild the consolidated report** immediately after:
   ```bash
   python "<scripts-dir>/build_report.py" "[slug]/"
   ```
   Resolve helper via `**/build_report.py` (`scripts/`).
3. If this step produced a diagram worth showing, render it with Archify (bundled at `skills/archify/`) to a visible sibling file (e.g. `architecture.html`) and reference it first with a `<!-- diagram: architecture.html -->` marker in the markdown, then rebuild.
4. On revise, rewrite the markdown and rebuild the report again.
5. Final chat summary (end of the whole run) cites the **`analysis.html`** path.
6. **Never delete** `.steps/*.md`, `analysis.html`, or `.steps/build_docx.py` after DOCX/slide-deck/diagram generation.

See `context/pm-operating-system.md` sections 3, 6, and 11–13.


## Output Format

```markdown
# Feature Brainstorm: [Feature Name]

## Feature Summary
[2–3 short paragraphs in plain language. What are we adding? Who is it for?
Avoid unexplained jargon.]

## Why This Technology Exists
### What is it?
[Simple definition. Define acronyms on first use.]

### Why do people use it?
[3–6 bullets: real-world drivers. Cost, scale, multi-site, cloud, isolation, agility…]

### What problem does it solve?
[Before vs after in everyday terms.]

### Easy example
[One concrete analogy or scenario a non-specialist developer can picture.]

### What we would watch in OpManager Plus (preview only)
[Plain list of the kinds of health signals — not a full metrics design.]

## Why It Matters for OpManager Plus
- **Market demand:** …
- **Competitive pressure:** … (brief — full analysis in Step 2)
- **Product fit:** …
- **Revenue opportunity:** …

## Target Users
| User Role | How They'd Use This Feature | Priority |
|-----------|----------------------------|----------|
| [Role] | [Use case in plain language] | Primary/Secondary |

## Persona Stories

### Story 1: [Name] — [Title] at [Company Type]
[150–200 words. Specific failure moment + easy example + transformation line.]

### Story 2: [Name] — [Title] at [Company Type]
[Different industry/scale/angle.]

### Story 3 (optional): …

> These stories will be reused in presentations, PRD, and marketing. Keep them human and concrete.

## Technology Overview (still plain)
[Short. Key parts in everyday words, then optional one-line note on APIs/SNMP/telemetry.
No RFC dumps.]

## Fit Within OpManager Plus
- **Module:** …
- **Discovery:** …
- **Existing reuse:** …
- **New requirements:** …

## Assumptions & Open Items
[This step runs unattended — wayfinding (Step 0) was the only interactive point. Anything that would otherwise be a question for the PM gets resolved here as a stated, reasonable assumption instead of left open. List each one so a later step or the final report can see what was assumed and revisit it if wrong.]

1. …
2. …
3. …
4. …

## Initial Risks & Considerations
- …
- …

## Sources
- [Title](URL) — why used
```

## Quality Gate (before marking complete)

- [ ] Wrote `.steps/1_brainstorm.md` (not feature root), rebuilt `analysis.html`
- [ ] Plain English throughout; jargon defined on first use
- [ ] **Why This Technology Exists** covers what / why people use it / problem solved / easy example
- [ ] 2–3 named persona stories with concrete failure examples + transformation
- [ ] Module fit / reuse / new requirements filled
- [ ] Open questions noted as assumptions, not batched for the PM (Step 0 wayfinding was the interactive step — this one runs unattended)
- [ ] Sources cited when external claims are made
- [ ] `Progress.md` updated
- [ ] No implementation code
- [ ] No deletion of other pipeline files

## Completion

After writing the markdown and rebuilding `analysis.html`, display a short chat summary, then continue immediately to Step 2 — do not wait for a reply:

---

**Step 1 Complete — Brainstorm Summary:**

> **Feature:** [One-line description in plain English]
> **What the technology is (simple):** [One sentence]
> **Why people use it:** [One sentence]
> **Why it matters for us:** [One sentence on strategic value]
> **Target users:** [2–3 key roles]
> **Assumptions made** (things a human would normally be asked, resolved here instead of blocking):
> 1. …
> 2. …
>
> Continuing immediately to Step 2 — Competitive Analysis.

---

If the PM interrupts with feedback mid-run, revise **only this step** and rebuild the report, then resume the unattended chain from where it left off (operating system §8).
