---
name: deliverables
description: "Step 5 of PM Feature Pipeline: Generate all four deliverable documents — executive slide deck, engineering slide deck, feature flowchart, and PRD — as markdown drafts ready for HTML/DOCX generation."
---

# Step 5 — Deliverable Generation

## Purpose

Generate production-quality content for four deliverables. These are written as structured markdown first (for review), then converted to the actual HTML slide decks, Archify flowchart, and DOCX PRD using the `generate_documents` skill.

**Plain-language bar (DOE) — operating system §7:** dense and jargon-free aren't in tension — density means pulling forward everything real from Steps 1–4 (below), not padding with unexplained technical shorthand. All four drafts' own prose is held to this bar directly; it doesn't inherit plain-language credit from Step 1 just because Step 1 already did the work.

## Dense content bar (mandatory — no thin decks)

PPT drafts and flowchart drafts must be **immediately usable**. They transfer the analysis; they do not vaguely allude to it.

### Pull forward from Steps 1–4 (do not drop)
- Named persona challenges + how each capability solves them
- Competitive gaps we exploit (real competitor names + gap)
- **Full** recommended metric set (split tables/slides; never “key metrics only” if analysis listed more)
- Primary collection method, prerequisites, and **highlight OID/API/path inventory** on engineering + flowchart
- Discovery, polling, alert thresholds, scale limits, risks, phasing, in/out scope
- Concrete numbers from analysis (intervals, limits, severities)

### Executive PPT (5a)
- Strategic but **specific**: named capabilities, segments, metrics targets, competitive facts
- No generic slides that could fit any feature after a rename
- Every slide: actionable bullets, not slogans alone
- Speaker notes may hold extra depth; on-slide content must still stand alone

### Engineering PPT (5b)
- Target **18–25 slides** when needed (prefer more slides over dropped content)
- Required content blocks (add slides/appendix as needed):
  1. Persona-grounded problem
  2. Technology map
  3. Collection method comparison (why primary won)
  4. Collection contract highlights (OID/API/path tables — split across slides)
  5. Full metrics by category (table slides)
  6. Architecture + data flow diagrams
  7. Discovery/onboarding
  8. Polling/error/retry
  9. Data model / retention
  10. Alerting + thresholds
  11. UI surfaces
  12. Scale limits
  13. Risks/dependencies
  14. Phasing
  15. Open eng questions
- **Fail** if metrics or collection contract from Step 3 are missing or reduced to 3 vague bullets

### Flowchart (5c / enhancement 5d)
- Multi-page, followable without the PRD
- Minimum pages/sections: overview, setup/onboarding, discovery, collection pipeline (protocol branches), normalize/store, threshold/alert/notify, failure/retry, EE/probe path if relevant, operator daily loop
- Label decision diamonds with real conditions from analysis
- Annotate important OIDs/endpoints on collection nodes where readable
- **Fail** if only a single 5-box happy path

### PRD (5d / enhancement 5c)
- Already technical; keep density; embed collection contract reference tables

### Placeholders forbidden
No “TBD”, “update later”, “lorem”, or empty speaker-note-only slides for core decisions.

## Input

Read ALL prior step files:
- `[feature-name]/.steps/1_brainstorm.md` — feature understanding and **persona stories/challenges**
- `[feature-name]/.steps/2_competitive_analysis.md` — competitive landscape and **persona challenge coverage**
- `[feature-name]/.steps/3_technical_analysis.md` — technical approach and **persona challenge resolution**
- `[feature-name]/.steps/4_feature_definition.md` — capabilities with **persona challenge traceability**

**Persona stories provide the motivational thread** — the executive PPT opens and closes with them (Slides 2 and 11), the engineering PPT opens with one (Slide 2), and the PRD includes a compact traceability table. Extract the best stories from `1_brainstorm.md` and reference them where needed.

**CRITICAL: The PRD must be technically dense.** Personas motivate the "why" but the PRD's primary value is the "how" and "what exactly." Spend the majority of PRD content on architecture, decision logic, data model, functional requirements, and metrics. Persona sections should be compact reference tables — not multi-paragraph narratives.

## Deliverables

### 5a — Executive Presentation

**File:** `[feature-name]/.steps/5a_executive_presentation.md`
**Audience:** Product Director / Leadership
**Tone:** Strategic, visual, high-level. No deep technical content.
**Slides:** 12-16 (add slides rather than dropping concrete analysis points)

```markdown
# Executive Presentation: [Feature Name]

## Slide 1: Title
- Feature name
- Subtitle: one-line value proposition
- Date, presenter name placeholder

## Slide 2: The Challenge — A Real Story
- Open with the strongest persona story from `1_brainstorm.md` (condensed to 4-5 bullet points)
- Name the person, their role, their company context
- The specific moment where the absence of this feature caused real harm
- The emotional hook: what was at stake, who was affected
- End with: "This is why we need [Feature Name]."
- **This slide should make leadership feel the problem, not just understand it.**

## Slide 3: The Opportunity
- What is this feature in one sentence
- Market context (why now?)
- Key stat or data point that makes this compelling
- Customer demand evidence (how many are asking, revenue at risk)

## Slide 4: Customer Need
- Who is asking for this (reference persona roles)
- What problem they face today
- Impact of not having this (churn risk, lost deals, competitive disadvantage)

## Slide 5: Competitive Landscape
- Visual comparison (simplified matrix or positioning map)
- Who has this, who doesn't, where the gaps are
- Our positioning opportunity

## Slide 6: Our Approach
- How OpManager Plus will implement this
- 3 key differentiators vs. competition
- Why our approach is better

## Slide 7: Key Capabilities
- 4-6 headline capabilities in v1
- Each with a one-line benefit statement
- Visual: icon or screenshot placeholder per capability

## Slide 8: Target Customers
- Which segments benefit most
- Expected adoption profile
- Expansion/upsell opportunity

## Slide 9: Success Metrics
- How we'll measure success
- Target numbers (adoption, retention impact, revenue)

## Slide 10: Timeline & Investment
- High-level phases
- Key milestones
- Resource ask (if applicable)

## Slide 11: The Transformation — Story Revisited
- Return to the persona from Slide 2
- "Now, with [Feature Name], here's how [Persona Name]'s day changes..."
- Show the transformed experience — same scenario, better outcome
- This creates a narrative arc: pain → solution → resolution

## Slide 12: Recommendation & Next Steps
- Clear ask: what you want leadership to approve
- Immediate next steps
- Decision needed by [date]

---
**Design notes:**
- Use ManageEngine brand colors
- Slide 2 is the emotional anchor — a persona quote/callout, not bullets or a diagram
- Slide 11 mirrors Slide 2 — same layout, but showing the "after" story
- Include diagrams on slides 5, 6, 7
- These are reading-first deliverables (async review, handoff), not a speaker-led talk — per frontend-slides' own density framework, aim for its "high density / reading-first" mode (4-8 bullets or structured cards per slide), not its sparse speaker-led one
- Speaker notes included for presenter context

**Layout variety — mandatory.** Never more than 2 consecutive bullet-only slides. Vary layouts by content, using the same vocabulary `generate-documents` renders from (there is no fixed API to call — these are content shapes a frontend-slides deck is authored to, not function names): two-column (problem vs. solution — Slide 3, or comparisons on 6, 8), comparison matrix (competitive — Slide 5), process-flow (approach — Slide 6), icon grid, not a bullet list (capabilities — Slide 7), a single large stat breaking up dense slides (Slide 9), KPI cards (metrics), horizontal timeline (phasing — Slide 10), before/after panels (the transformation slide — Slide 11), quote/callout (persona voice — Slides 2, 11). Use whichever shape actually fits each slide's content — this is the palette, not a rigid per-slide assignment.

- Use accent color/backgrounds on at least 2 non-title slides (section breaks or quote slides)
- KPI cards color-coded by meaning (green=positive, red=risk, blue=neutral)
- Two-column slides get a visual divider and distinct column headers
- Tables get colored headers and alternating row shading
- At least 30% of slides should be non-bullet layouts (diagrams, grids, KPIs, timelines)
```

### 5b — Engineering Presentation

**File:** `[feature-name]/.steps/5b_engineering_presentation.md`
**Audience:** Engineering team
**Tone:** Technically rigorous but accessible. Assume smart engineers who don't know this specific domain.
**Slides:** 18-25 (use more if needed to avoid dropping metrics/OID-API detail)

```markdown
# Engineering Presentation: [Feature Name]

## Slide 1: Title + Context
- Feature name
- One sentence: what we're building and why

## Slide 2: Why This Matters — The User's Reality
- Open with a persona story from `1_brainstorm.md` (pick one relevant to engineers — show the technical frustration)
- Condensed to 3-4 bullet points: who they are, what went wrong, what they couldn't do
- This grounds engineers in WHY they're building this, not just WHAT
- "This is the problem we're solving for [Persona Name] and thousands like them."

## Slide 3: Technology Overview
- What is [technology] and how does it work
- Key components and their relationships
- Diagram: architecture of the monitored system

## Slide 4: Data Collection Approach
- Recommended method and why
- What we evaluated and rejected (brief)
- Prerequisites on the monitored device

## Slide 5: Architecture Diagram
- Full data flow: Device → Collection → Processing → Storage → UI
- Where this plugs into existing OpManager architecture
- New components vs. reused components

## Slide 6-7: Metrics Deep Dive
- Complete metrics table by category
- For each: what it is, why it matters, alert threshold
- Collection frequency and rationale

## Slide 8: Discovery & Onboarding
- How devices are discovered
- Classification logic
- Auto-association of monitors

## Slide 9: Polling & Collection Detail
- Technical implementation of the polling mechanism
- Authentication and credential handling
- Error handling and retry logic

## Slide 10: Data Model
- Schema/entity relationship
- How this relates to existing data model
- Storage and retention considerations

## Slide 11: Alerting Logic
- Threshold-based alerts
- Adaptive threshold candidates
- Alert correlation with existing alerts

## Slide 12: UI Components
- Screens to build
- Widgets and visualizations
- Reusable components vs. new development

## Slide 13: Scalability
- Load testing considerations
- Performance targets
- Known limitations at scale

## Slide 14: Dependencies & Risks
- External dependencies
- Technical risks with mitigation plans
- Vendor/protocol risks

## Slide 15: Phasing
- v1 scope (must-have)
- v1.1 fast follow
- v2 future

## Slide 16: Open Questions for Engineering
- Technical decisions that need team input
- Areas needing spike/investigation
- Architecture review topics

---
**Design notes:**
- Slide 2 is the persona story — design it with an emotional callout, NOT architecture diagrams
- Architecture diagrams required on slides 5, 9 (data flow and polling detail)
- Metrics tables should be legible (split across slides if needed)
- Include code-level detail in speaker notes where helpful

**Layout variety — mandatory.** Same rule as the executive deck — never more than 2 consecutive bullet-only slides. Same palette: two-column (metrics comparisons — Slides 6-7), a metrics table (deep dives, split if >8 rows), process-flow (data collection pipeline — Slide 4 or 9), an embedded architecture image (linked from the Archify flowchart, not redrawn — Slides 5, 10), horizontal timeline (phasing — Slide 15), KPI cards (scalability/performance targets), icon grid (UI component overview — Slide 12).

This is a **feature**, not an enhancement — there is no existing/new/modified distinction here (that's an enhancement-pipeline concept, since a net-new feature has nothing prior to compare against). Color by meaning instead: severity/status on metrics and alerting slides, a single consistent accent color for architecture diagrams.
```

### 5c — Feature Flowchart

**File:** `[feature-name]/.steps/5c_feature_flowchart.md`
**Format:** Mermaid diagrams (source material for the Archify flowchart built in `generate-documents`, Section 1 — not a conversion target itself)

```markdown
# Feature Flowchart: [Feature Name]

## Overview Flow
[End-to-end feature flow from setup to daily operation]

​```mermaid
flowchart TD
    A[Start] --> B{...}
    B -->|Yes| C[...]
    B -->|No| D[...]
    ...
​```

## Setup & Onboarding Flow
[Detailed flow for first-time configuration]

​```mermaid
flowchart TD
    ...
​```

## Data Collection Pipeline
[How data flows from device to dashboard]

​```mermaid
flowchart LR
    ...
​```

## Alert Processing Flow
[How alerts are triggered, evaluated, and delivered]

​```mermaid
flowchart TD
    ...
​```

## User Interaction Flow
[How a user navigates and troubleshoots using this feature]

​```mermaid
flowchart TD
    ...
​```
```

### 5d — Product Requirements Document

**File:** `[feature-name]/.steps/5d_product_requirements.md`
**Audience:** Engineering, QA, and Design
**Tone:** Precise, comprehensive, unambiguous

```markdown
# Product Requirements Document: [Feature Name]

## Document Info
| Field | Value |
|-------|-------|
| Author | [PM Name — placeholder] |
| Status | Draft |
| Last Updated | [Date] |
| Version | 1.0 |

## 1. Overview
### 1.1 Feature Summary
[What this feature is and why we're building it]

### 1.2 Objectives
- [Objective 1 — measurable]
- [Objective 2 — measurable]

### 1.3 Background
[Context: market need, customer requests, competitive pressure]

## 2. Target Users & Use Cases
### 2.1 Primary Users
[Who and how they'll use this — table format: Role | Usage | Priority]

### 2.2 Persona Challenges (from Brainstorm)
[Keep this COMPACT — one row per persona challenge, no multi-paragraph narratives]
| Persona | Challenge | Resolution (FR/Capability) |
|---------|-----------|---------------------------|
| [Name, Role] | [One-sentence pain point] | [FR-IDs or capability name that solves it] |

### 2.3 Use Cases
| # | As a... | I want to... | So that... |
|---|---------|-------------|-----------|
| UC-1 | [Role] | [Action] | [Benefit] |

## 3. Technical Architecture
### 3.1 Architecture Overview
[How this feature fits into OpManager Plus architecture. Include a text-based or described diagram showing: data sources → collection layer → processing → storage → UI. Note for `generate-documents`: the DOCX embeds a small `matplotlib`-rendered static image here, not the interactive Archify flowchart HTML — Archify's output can't be embedded as a static picture.]

### 3.2 Data Flow
[End-to-end data flow from monitored device to user-visible output. Step-by-step description of how data moves through the system.]

### 3.3 Decision Logic & Algorithms
[Core logic the feature uses to make decisions — classification rules, severity scoring, correlation logic, threshold evaluation, state machines. This is the "brain" of the feature. Be specific with conditions, formulas, and rules.]

### 3.4 Data Model
[Key entities, relationships, and storage approach. Table format:]
| Entity | Key Fields | Relationships | Retention |
|--------|-----------|---------------|-----------|
| [Entity] | [Fields] | [FK/References] | [Retention policy] |

### 3.5 Integration Points
[How this feature connects to existing OpManager Plus components and external systems]
| Integration | Direction | Protocol | Purpose |
|------------|-----------|----------|---------|
| [System/Module] | Inbound/Outbound/Bidirectional | [REST/SNMP/DB/etc.] | [Why] |

## 4. Functional Requirements
### 4.1 Discovery & Setup
| ID | Requirement | Priority | Acceptance Criteria |
|----|------------|----------|-------------------|
| FR-001 | [Requirement] | P0/P1/P2 | [How to verify] |

### 4.2 Data Collection
[Same table format]

### 4.3 Monitoring & Visualization
[Same table format]

### 4.4 Alerting
[Same table format]

### 4.5 Reporting
[Same table format]

## 5. Metrics Specification
| # | Metric Name | Category | Definition | Collection Method | Frequency | Unit | Alert Threshold | Importance |
|---|------------|----------|-----------|-------------------|-----------|------|-----------------|------------|
| M-001 | [Name] | [Cat] | [Def] | [Method] | [Freq] | [Unit] | [Threshold] | [Why monitor this] |

## 6. Non-Functional Requirements
### 6.1 Performance
- [Response time, throughput targets]

### 6.2 Scalability
- [Max devices, growth expectations]

### 6.3 Security
- [Authentication, encryption, credential storage]

### 6.4 Reliability
- [Failover, data loss tolerance]

## 7. Out of Scope
- [Explicit exclusions]

## 8. Dependencies
| Dependency | Type | Owner | Risk |
|-----------|------|-------|------|
| [Dep] | [Internal/External] | [Team/Vendor] | [Risk level] |

## 9. Persona Challenge Traceability

[Compact cross-reference table — NOT narrative retelling of persona stories]

| Persona Challenge | FR(s) | Metric(s) | Success Criteria |
|-------------------|-------|-----------|------------------|
| [One-line challenge] | [FR-IDs] | [M-IDs] | [Measurable criteria] |

## 10. Success Metrics
| Metric | Target | Measurement Method | Timeframe |
|--------|--------|--------------------|-----------|
| [Metric] | [Target] | [How measured] | [When to evaluate] |

## 11. Open Questions
| # | Question | Owner | Blocking? | Status |
|---|----------|-------|-----------|--------|
| Q-1 | [Question] | [Who answers] | Yes/No | Open |

## 12. Appendix
- Links to competitive analysis
- Links to technical analysis
- Glossary of terms
```




## Report rebuild (mandatory)

Write markdown to `.steps/<name>.md` (hidden), then rebuild `analysis.html` and, if this step produced a diagram, render it and reference it first with a `<!-- diagram: architecture.html -->` marker. **Full procedure, exact paths, and the rebuild command are in `pm-shared/context/pm-operating-system.md` §§3, 6, 11a — already loaded as mandatory context for every run, so it is not repeated here.** Never delete `.steps/*.md`, `analysis.html`, or `.steps/build_docx.py`.

## Quality Gate (before marking complete)

Gate ledger for this step — write `.steps/GATES-5a-5d.md` from `<resolved shared parent>/unlazy-gates/templates/gates-leaf.md` before producing this step's content, one gate per item below. Resolution rule (self-correct on a failed gate, document the gap and continue — never abandon, never pause): `pm-shared/context/pm-operating-system.md` §18.


- [ ] G1: All four Step 5 drafts written under `.steps/` with correct filenames for this pipeline mode
  CHECK: node -e "const fs=require('fs');const f=['.steps/5a_executive_presentation.md','.steps/5b_engineering_presentation.md','.steps/5c_feature_flowchart.md','.steps/5d_product_requirements.md'];process.exit(f.every(p=>fs.existsSync(p))?0:1)"
  EXPECT: (exits zero)
- [ ] G2: Exec and engineering decks are not near-duplicates
  (manual — no command can decide this)
- [ ] G3: Flow content is complete enough to render as real diagrams
  (manual — no command can decide this)
- [ ] G4: No TBD/lorem/fill-in-later placeholders in any of the four drafts
  CHECK: node -e "const fs=require('fs');const f=['.steps/5a_executive_presentation.md','.steps/5b_engineering_presentation.md','.steps/5c_feature_flowchart.md','.steps/5d_product_requirements.md'];process.exit(f.some(p=>/\bTBD\b|\blorem\b|\[fill in\]/i.test(fs.readFileSync(p,'utf8')))?1:0)"
  EXPECT: (exits zero)
- [ ] G5: PRD requirements are testable
  (manual — no command can decide this)
- [ ] G6: Persona traceability retained
  (manual — no command can decide this)
- [ ] G7: `Progress.md` updated (next: document generation)
  CHECK: node -e "const fs=require('fs');process.exit(fs.statSync('Progress.md').mtimeMs>=fs.statSync('.steps/5d_product_requirements.md').mtimeMs?0:1)"
  EXPECT: (exits zero)
## Completion

After producing all four files, display a **summary directly in chat**:

---

**Step 5 Complete — Deliverables Draft Summary:**

> **Executive PPT** (`5a`): [N] slides covering [key topics]
> **Engineering PPT** (`5b`): [N] slides covering [key topics]
> **Flowchart** (`5c`): [N] flow diagrams — [list: setup, data pipeline, alerting, etc.]
> **PRD** (`5d`): [N] functional requirements, [M] metrics defined, [K] open questions
>
> **Key highlights across deliverables:**
> - [Most compelling point for executives]
> - [Key technical decision for engineers]
> - [Most important success metric]
>
> Drafts written under `[feature-name]/.steps/` (`5a`–`5d`), `analysis.html` rebuilt.
> Update `Progress.md` → Step 5 complete, next action `document_generation`.
>
> Continuing immediately into document generation (HTML slide decks, Archify flowchart, DOCX), then Step 6.

---
