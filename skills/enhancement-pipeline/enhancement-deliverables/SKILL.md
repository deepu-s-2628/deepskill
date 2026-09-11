---
name: enhancement-deliverables
description: "Step 5 of Enhancement Pipeline: Generate all four enhancement deliverable documents — executive PPT, engineering PPT, enhancement flowcharts, and enhancement PRD — as markdown drafts ready for PPTX/PDF/DOCX generation."
---

# Step 5 — Enhancement Deliverables (PPTs + Flowchart + PRD)

## Purpose

Produce four documents that fully specify the enhancement: an executive presentation for leadership, an engineering presentation for the dev team, flowcharts showing before/after flows, and a PRD with every detail an engineer needs. These are the bridge between the analysis (Steps 1–4) and the visual wireframe (Step 6).


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

Read ALL prior steps:
- `ITOM-PM-Result/[feature-name]-enhancement/.steps/1_current_state.md` — what exists today and **persona pain stories**
- `ITOM-PM-Result/[feature-name]-enhancement/.steps/2_cross_module_analysis.md` — cross-module patterns and **persona challenge → cross-module solutions**
- `ITOM-PM-Result/[feature-name]-enhancement/.steps/3_competitive_analysis.md` — competitive gaps and **persona challenge coverage**
- `ITOM-PM-Result/[feature-name]-enhancement/.steps/4_enhancement_findings.md` — recommended enhancements with **persona challenge resolution map**

**Persona stories provide the motivational thread** — the executive PPT opens and closes with them (Slides 2 and 12), the engineering PPT opens with one (Slide 2), and the PRD includes a compact traceability table. Extract the best stories from `1_current_state.md` and reference them where needed.

**CRITICAL: The Enhancement PRD must be technically dense.** Personas motivate the "why" but the PRD's primary value is the "how" and "what exactly changes." Spend the majority of PRD content on architecture changes, decision logic, data model modifications, current-vs-enhanced behavior, and metrics. Persona sections should be compact reference tables — not multi-paragraph narratives.

## Deliverables

### 5a — Executive Presentation

**File:** `ITOM-PM-Result/[feature-name]-enhancement/.steps/5a_executive_presentation.md`
**Audience:** Product Director / Leadership
**Tone:** Strategic, visual, high-level. Focus on the business case for enhancing — why now, what impact, what's the competitive risk of NOT doing this.
**Slides:** 12-16 (add slides rather than dropping concrete analysis points)

```markdown
# Executive Presentation: [Feature Name] Enhancement

## Slide 1: Title
- "[Feature Name] Enhancement"
- Subtitle: one-line value proposition for the enhancement
- Date, presenter name placeholder

## Slide 2: The Challenge Today — A Real Story
- Open with the strongest persona story from `1_current_state.md` (condensed to 4-5 bullet points)
- Name the person, their role, their company context
- A specific moment where the current feature's limitations caused real pain
- The emotional hook: what workaround failed, who was affected, what was the fallout
- End with: "This is why we need to enhance [Feature Name]."
- **This slide makes leadership feel the urgency, not just see a gap list.**

## Slide 3: Current State & Gap
- What the feature does today (brief)
- Where we're falling short (key limitations)
- Customer impact of these gaps (churn risk, competitive loss, support burden)

## Slide 4: Competitive Pressure
- Visual comparison showing where competitors are ahead on this feature
- Specific capabilities they have that we don't
- Customer feedback/sentiment about our gap

## Slide 5: Enhancement Opportunity
- What we're proposing to change
- 3-4 headline improvements
- Expected outcome for customers

## Slide 6: Key Enhancements — Quick Wins
- Quick wins that can ship fast
- Each with impact statement
- Visual: before/after contrast

## Slide 7: Key Enhancements — Core Improvements
- Major capability upgrades
- Competitive gaps these close
- User workflow improvements

## Slide 8: New Metrics & Capabilities
- Key new metrics being added (not exhaustive — highlight the most impactful)
- New alerting capabilities
- New visualization/dashboard improvements

## Slide 9: Cross-Module Benefits
- How these enhancements benefit other modules
- Reuse opportunities that reduce effort
- Platform-level improvements

## Slide 10: Success Metrics & Expected Impact
- How we'll measure success
- Target improvements (adoption, satisfaction, competitive win rate)
- Before/after user experience comparison

## Slide 11: Phasing & Timeline
- Phase 1: Quick wins — [timeline]
- Phase 2: Core improvements — [timeline]
- Phase 3: Strategic additions — [timeline]

## Slide 12: The Transformation — Story Revisited
- Return to the persona from Slide 2
- "Now, with these enhancements, here's how [Persona Name]'s experience changes..."
- Same scenario, better outcome — the limitation that caused pain is now resolved
- This closes the narrative arc and makes the investment tangible

## Slide 13: Recommendation & Next Steps
- Clear ask: what to approve
- Resource requirements
- Decision needed by [date]

---
**Design notes:**
- Use ManageEngine brand colors
- Slide 2 is the emotional anchor — use a persona quote callout with vivid scenario
- Slide 12 mirrors Slide 2 — same layout, showing the "after" story
- Before/after visuals on slides 6-7
- Competitive comparison visual on slide 4
- Keep text minimal — 4-6 bullets max per slide
- Speaker notes included for context

**SLIDE LAYOUT VARIETY — MANDATORY:**
Every presentation MUST use a mix of slide types. Never use more than 2 consecutive `add_content_slide()` (bullet) slides. Alternate between:
- `add_quote_slide()` — for persona voice on Slides 2 and 12
- `add_two_column_slide()` — for before/after comparisons (Slides 3, 6, 7)
- `add_before_after_slide()` — for enhancement impact visuals (Slides 6-7)
- `add_comparison_slide()` — for competitive landscape (Slide 4)
- `add_kpi_slide()` — for success metrics and impact numbers (Slide 10)
- `add_icon_grid_slide()` — for enhancement capabilities (Slide 5)
- `add_timeline_slide()` — for phasing and roadmap (Slide 11)
- `add_process_flow_slide()` — for approach methodology
- `add_stat_slide()` — for a single powerful statistic between dense slides

**COLOR AND VISUAL RICHNESS:**
- Use accent color backgrounds on at least 2 non-title slides (section breaks or quote slides)
- Use KPI cards with color-coded values (green=improvement, red=risk, blue=neutral)
- Two-column and before/after slides should have colored dividers and headers
- Tables must have colored headers and alternating row shading
- At least 30% of slides should be non-bullet layouts (diagrams, grids, KPIs, timelines)
```

---

### 5b — Engineering Presentation

**File:** `ITOM-PM-Result/[feature-name]-enhancement/.steps/5b_engineering_presentation.md`
**Audience:** Engineering team
**Tone:** Technically detailed. Focus on what changes, what's reused, what's new, and how it integrates with existing architecture.
**Slides:** 18-25 (use more if needed to avoid dropping metrics/OID-API detail)

```markdown
# Engineering Presentation: [Feature Name] Enhancement

## Slide 1: Title + Context
- Feature name + "Enhancement"
- One sentence: what's changing and why

## Slide 2: Why This Enhancement Matters — The User's Reality
- Open with a persona story from `1_current_state.md` (pick one showing technical frustration)
- Condensed to 3-4 bullet points: who they are, what limitation hit them, what workaround they use
- This grounds engineers in WHY these changes matter, not just WHAT is changing
- "This is the pain we're eliminating for [Persona Name] and thousands of users like them."

## Slide 3: Current Architecture
- How the feature works today
- Diagram: existing data flow and components
- What we're keeping vs. changing

## Slide 4: Enhancement Overview
- Summary of all changes in one view
- Color-coded: green=keep, blue=new, orange=modify, red=remove
- Scope boundaries

## Slide 5: New Metrics Deep Dive
- Complete table of new metrics being added
- For each: what it measures, collection method, frequency, threshold
- Why each metric matters

## Slide 6: Modified Metrics & Behavior Changes
- What existing metrics are changing
- Current behavior vs. new behavior
- Migration considerations

## Slide 7: Enhanced Architecture Diagram
- Full data flow showing changes
- New components highlighted
- Modified connections marked
- Integration with existing polling engine, DB, UI

## Slide 8-9: Discovery & Collection Changes
- Changes to device discovery rules
- New or modified credential requirements
- Protocol changes
- Enhanced polling logic

## Slide 10: Alerting Enhancements
- New alert types
- Modified thresholds
- New notification capabilities
- Alert correlation changes

## Slide 11: UI/UX Changes
- Pages being modified (before/after description)
- New widgets or views
- Navigation changes
- Dashboard enhancements

## Slide 12: Data Model Changes
- Schema modifications
- New tables/columns
- Migration requirements
- Backward compatibility notes

## Slide 13: Cross-Module Reuse
- Components borrowed from other modules
- How they're adapted for this use
- Effort saved by reusing

## Slide 14: Scalability Impact
- How these changes affect performance at scale
- New load considerations
- Testing requirements

## Slide 15: Phasing Plan
- Phase 1: Quick wins (sprint-level)
- Phase 2: Core improvements (quarter)
- Phase 3: Strategic additions (roadmap)
- Dependencies between phases

## Slide 16: Risks & Open Questions
- Technical risks with mitigation
- Open questions needing engineering input
- Areas requiring spike/investigation

---
**Design notes:**
- Slide 2 is the persona story — design it with an emotional callout, NOT architecture diagrams
- Architecture diagrams on slides 3, 7 (current and enhanced architecture)
- Color coding: green=existing, blue=new, orange=modified
- Metrics tables should be legible (split across slides if needed)
- Include code-level notes in speaker notes where helpful

**SLIDE LAYOUT VARIETY — MANDATORY:**
Same rule as executive PPT — never more than 2 consecutive bullet slides. Use:
- `add_two_column_slide()` — for current-vs-enhanced comparisons (Slides 5-6)
- `add_before_after_slide()` — for architecture changes (Slide 7)
- `add_table_slide()` — for metrics deep dives (split if >8 rows)
- `add_process_flow_slide()` — for data collection pipeline changes
- `add_image_slide()` — for architecture diagrams (Slides 3, 7)
- `add_timeline_slide()` — for phasing plan (Slide 15)
- `add_kpi_slide()` — for scalability and performance targets
- `add_icon_grid_slide()` — for UI component changes (Slide 11)

**COLOR CODING CONSISTENCY:**
- Green (#28A745) = existing/keep
- Blue (#0078D4) = new components
- Orange (#FD7E14) = modified
- Red (#DC3545) = removed/deprecated
- Use these colors consistently in all diagrams, tables, and flow slides
```

---

### 5c — Enhancement PRD

**File:** `ITOM-PM-Result/[feature-name]-enhancement/.steps/5c_enhancement_prd.md`
**Audience:** Engineering, QA, and Design
**Tone:** Precise, comprehensive, unambiguous. This is the source of truth for what gets built.

```markdown
# Enhancement PRD: [Feature/Area Name]

## Document Info
| Field | Value |
|-------|-------|
| Author | [PM Name — placeholder] |
| Status | Draft |
| Last Updated | [Date] |
| Version | 1.0 |
| Enhancement Type | Feature Enhancement |

## 1. Executive Summary

[2–3 sentences: what are we enhancing, why, and what's the expected outcome. Reference the enhancement findings.]

## 2. Current State Summary

### 2.1 What Exists Today
[Brief summary from Step 1 — what the feature currently does, how it's monitored, key metrics already collected]

### 2.2 Key Limitations
[Top limitations from Step 1 that this enhancement addresses]

### 2.3 Persona Challenges (from Current State Analysis)
[Keep this COMPACT — one row per persona challenge, no multi-paragraph narratives]
| Persona | Challenge Today | Enhancement(s) That Solve It |
|---------|----------------|------------------------------|
| [Name, Role] | [One-sentence frustration] | [Enhancement name / FR-IDs] |

### 2.4 Competitive Gap
[Brief summary from Step 3 — where competitors are ahead]

## 3. Technical Architecture Changes

### 3.1 Current Architecture
[How the feature currently works architecturally — component diagram or data flow description]

### 3.2 Enhanced Architecture
[What changes in the architecture. Show new components, modified connections, removed elements.]

### 3.3 Decision Logic & Algorithm Changes
[How the feature's core logic changes — classification rules, scoring, correlation, thresholds. Be specific with before/after rules, conditions, and formulas.]

### 3.4 Data Model Changes
| Entity | Change Type | Details | Migration Notes |
|--------|------------|---------|-----------------|
| [Entity] | New/Modified/Removed | [What changes] | [Migration/backward compat] |

### 3.5 Integration Point Changes
| Integration | Change | Current | Enhanced | Protocol |
|------------|--------|---------|----------|----------|
| [System] | New/Modified | [Current behavior] | [Enhanced behavior] | [Protocol] |

## 4. Enhancement Scope

### 4.1 What's Changing
[Explicit list of what is being modified, added, or removed]

| Category | Change Type | Description |
|----------|------------|-------------|
| Discovery | New / Modified / Removed | [What changes in device/component discovery] |
| Metrics | New / Modified | [What new metrics are added or existing ones changed] |
| Alerting | New / Modified | [What new alerts or threshold changes] |
| UI/UX | New / Modified | [What pages, widgets, or views change] |
| Reporting | New / Modified | [What reports are added or enhanced] |
| Integration | New / Modified | [What integration points change] |

### 4.2 What's NOT Changing
[Explicit list of what remains the same — to set clear boundaries]

### 4.3 Out of Scope
[Things that were considered but explicitly excluded from this enhancement]

## 5. New & Modified Metrics

### 5.1 New Metrics
| # | Metric Name | Category | Definition | Collection Method | Protocol | Frequency | Unit | Default Threshold | Why This Metric Matters |
|---|------------|----------|-----------|-------------------|----------|-----------|------|-------------------|------------------------|
| M-NEW-001 | [Name] | [Category] | [What it measures] | [How collected] | [SNMP/WMI/CLI/API] | [Interval] | [Unit] | [Warning/Critical] | [Why users need this] |

### 5.2 Modified Metrics
| # | Metric Name | Current Behavior | New Behavior | Reason for Change |
|---|------------|-----------------|-------------|-------------------|
| M-MOD-001 | [Name] | [What it does now] | [What it will do] | [Why] |

### 5.3 Deprecated Metrics (If Any)
| # | Metric Name | Reason for Deprecation | Migration Path |
|---|------------|----------------------|----------------|
| M-DEP-001 | [Name] | [Why] | [How users transition] |

## 6. Functional Requirements

### 6.1 Discovery & Setup Enhancements
| ID | Requirement | Priority | Current Behavior | Enhanced Behavior | Acceptance Criteria |
|----|------------|----------|-----------------|-------------------|-------------------|
| FR-001 | [Requirement] | P0/P1/P2 | [What happens now] | [What should happen] | [How to verify] |

### 6.2 Monitoring & Data Collection Enhancements
| ID | Requirement | Priority | Current Behavior | Enhanced Behavior | Acceptance Criteria |
|----|------------|----------|-----------------|-------------------|-------------------|
| FR-010 | [Requirement] | P0/P1/P2 | [Now] | [Enhanced] | [Verify] |

### 6.3 Alerting Enhancements
[Same table format — current vs. enhanced]

### 6.4 UI/UX Enhancements
| ID | Requirement | Priority | Page/Component | Current State | Enhanced State | Acceptance Criteria |
|----|------------|----------|----------------|---------------|----------------|-------------------|
| FR-030 | [Requirement] | P0/P1/P2 | [Page] | [Now] | [After] | [Verify] |

### 6.5 Reporting Enhancements
[Same format]

### 6.6 Integration Enhancements
[Same format]

## 7. Cross-Module Reuse

Components from other modules to leverage (from Step 2):

| Component | Source Module | How It's Used There | How We'll Reuse It | Effort Saved |
|-----------|-------------|--------------------|--------------------|-------------|
| [Component] | [Module] | [Current use] | [Our use] | [Est. effort saved] |

## 8. Non-Functional Requirements

### 8.1 Performance
| Requirement | Current | Target | Measurement |
|-------------|---------|--------|-------------|
| [e.g., Polling response time] | [Current value] | [Target value] | [How measured] |

### 8.2 Scalability
- [Max devices/components affected by this enhancement]
- [Expected growth in data volume]
- [Any new scaling constraints]

### 8.3 Backward Compatibility
- [Will existing configurations continue to work?]
- [Migration steps for existing users]
- [Data retention/migration requirements]

## 9. Phasing

| Phase | Enhancements Included | Priority | Timeline | Theme |
|-------|----------------------|----------|----------|-------|
| Phase 1 (Quick Wins) | [List] | P0 | [Sprint/Month] | [Theme] |
| Phase 2 (Core) | [List] | P1 | [Quarter] | [Theme] |
| Phase 3 (Strategic) | [List] | P2 | [Future] | [Theme] |

## 10. Persona Challenge Traceability

[Compact cross-reference table — NOT narrative retelling of persona stories]

| Persona Challenge | Enhancement / FR(s) | Phase | Success Criteria |
|-------------------|--------------------|-------|------------------|
| [One-line challenge] | [Enhancement + FR-IDs] | [Phase] | [Measurable criteria] |

## 11. Success Metrics

| Metric | Current Baseline | Target | Measurement Method | Timeframe |
|--------|-----------------|--------|--------------------|-----------|
| [Metric] | [Current value] | [Target] | [How] | [When] |

## 12. Dependencies

| Dependency | Type | Owner | Risk | Mitigation |
|-----------|------|-------|------|------------|
| [Dep] | Internal/External | [Team] | [Risk level] | [Plan] |

## 13. Open Questions

| # | Question | Owner | Blocking? | Status |
|---|----------|-------|-----------|--------|
| Q-1 | [Question] | [Who] | Yes/No | Open |

## 14. Appendix
- Link to `1_current_state.md`
- Link to `2_cross_module_analysis.md`
- Link to `3_competitive_analysis.md`
- Link to `4_enhancement_findings.md`
- Glossary of terms specific to this feature
```

---

### 5d — Enhancement Flowcharts

**File:** `ITOM-PM-Result/[feature-name]-enhancement/.steps/5d_enhancement_flowchart.md`
**Format:** Mermaid diagrams showing before/after flows

Enhancement flowcharts are different from new feature flowcharts — they must show **what changes** relative to what exists today. Use color/style annotations to distinguish existing steps from new/modified steps.

```markdown
# Enhancement Flowchart: [Feature/Area Name]

## Diagram Legend
- **Solid borders** = Existing steps (unchanged)
- **Dashed borders** = New steps (added by enhancement)
- **Bold borders** = Modified steps (changed by enhancement)
- 🟢 = Existing | 🔵 = New | 🟡 = Modified

## 1. Enhanced End-to-End Flow
[The complete flow after enhancement — showing what exists and what's new/changed]

​```mermaid
flowchart TD
    A[Existing Step 1] --> B[Existing Step 2]
    B --> C["`**Modified Step 3**`"]
    C --> D[New Step 4]:::new
    D --> E[Existing Step 5]

    classDef new stroke-dasharray: 5 5, stroke:#2196F3, stroke-width:2px
    classDef modified stroke:#FF9800, stroke-width:3px
    class D new
    class C modified
​```

## 2. Enhanced Discovery & Setup Flow
[How the setup/onboarding flow changes]

​```mermaid
flowchart TD
    ...
​```

## 3. Enhanced Data Collection Pipeline
[How data collection changes — new metrics, new protocols, modified polling]

​```mermaid
flowchart LR
    ...
​```

## 4. Enhanced Alert Processing Flow
[How alerting changes — new thresholds, new alert types, modified evaluation]

​```mermaid
flowchart TD
    ...
​```

## 5. Enhanced User Workflow
[How the user's daily workflow changes — new views, new actions, modified navigation]

​```mermaid
flowchart TD
    ...
​```

## 6. Before vs. After Comparison

### Before (Current State)
​```mermaid
flowchart LR
    A[Current step] --> B[Current step] --> C[Current step]
​```

### After (Enhanced)
​```mermaid
flowchart LR
    A[Current step] --> B["`**Modified step**`"] --> C[Current step] --> D[New step]:::new
    classDef new stroke-dasharray: 5 5, stroke:#2196F3
    class D new
​```
```




## Report rebuild (mandatory)

Every step artifact this skill writes must:

1. **Markdown (source of truth, hidden):** `ITOM-PM-Result/[slug]/.steps/<name>.md`
   - Enhancement mode: `ITOM-PM-Result/[slug]-enhancement/.steps/<name>.md`
2. **Rebuild the consolidated report** immediately after:
   ```bash
   python "<scripts-dir>/build_report.py" "ITOM-PM-Result/[slug]/"
   ```
   Resolve helper via `**/build_report.py` (`scripts/`).
3. If this step produced a diagram worth showing, reference it first with a `<!-- diagram: Generated/diagrams/<name>.html -->` marker in the markdown, then rebuild.
4. On revise, rewrite the markdown and rebuild the report again.
5. Final chat summary (end of the whole run) cites the **`report.html`** path.
6. **Never delete** `.steps/*.md`, `report.html`, or `Generated/build_documents.py` after PPTX/PDF/DOCX generation.

See `context/pm-operating-system.md` sections 3, 6, and 11–13.


## Quality Gate (before marking complete)

- [ ] All four Step 5 drafts written under `.steps/` with correct filenames for this pipeline mode
- [ ] Exec and engineering decks are not near-duplicates
- [ ] Flow content is complete enough to render as real diagrams
- [ ] PRD requirements are testable
- [ ] Persona traceability retained
- [ ] `STATUS.md` updated (next: `document_generation`)
- [ ] `.steps/` markdown written, `report.html` rebuilt
- [ ] Markdown is hidden under `.steps/`; HTML visible under `steps/`; never delete either or Generated artifacts


## Completion

After producing all four files, display in chat:

---

**Step 5 Complete — Enhancement Deliverables:**

> **Executive PPT** (`5a`): [N] slides covering [key topics]
> **Engineering PPT** (`5b`): [N] slides covering [key topics]
> **Enhancement PRD** (`5c`): [N] functional requirements, [M] new metrics, [K] modified metrics, [J] open questions
> - Scope: [Brief scope summary]
> - Phasing: [N] phases planned
>
> **Enhancement Flowcharts** (`5d`): [N] diagrams
> - [List diagram names — e.g., end-to-end flow, data pipeline, alert processing]
> - Shows existing vs. new vs. modified steps
>
> Drafts written under `ITOM-PM-Result/[feature-name]-enhancement/.steps/` (`5a`–`5d`), `report.html` rebuilt.
> Update `STATUS.md` → Step 5 complete, next action `document_generation`.
>
> Continuing immediately into document generation (PPTX/PDF/DOCX), then Step 6.

---
