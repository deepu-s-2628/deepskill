---
name: enhancement-findings
description: "Step 4 of Enhancement Pipeline: Synthesize all analysis into a clear, actionable enhancement recommendation with prioritized improvements, impact assessment, and implementation guidance."
---

# Step 4 — Enhancement Findings & Recommendations

## Purpose

Bring together the current state analysis, cross-module insights, and competitive research into one decisive document. The PM should walk away knowing exactly what to enhance, why, in what order, and what the expected impact is.

## Input

Read all prior steps:
- `[feature-name]-enhancement/.steps/1_current_state.md` — what exists today, its limitations, and **persona challenges**
- `[feature-name]-enhancement/.steps/2_cross_module_analysis.md` — internal reuse and consistency opportunities
- `[feature-name]-enhancement/.steps/3_competitive_analysis.md` — competitive gaps and customer demand

**CRITICAL: Persona challenges are the ultimate prioritization filter.** When ranking enhancements, an enhancement that directly solves a persona challenge outranks one that doesn't — even if the latter has more competitive pressure. The persona stories represent real users with real pain. Every recommended enhancement should trace back to either a persona challenge, a competitive gap, or both.

## Process

### 1. Consolidate All Enhancement Opportunities

Merge findings from all three steps into a single list. Remove duplicates. For each enhancement:
- Where did it surface? (internal analysis, cross-module, competitive, customer feedback)
- How many sources support it? (the more sources, the stronger the signal)
- Is it addressing a limitation, a gap, a competitive deficit, or an opportunity?

### 2. Categorize Enhancements

Group them into:

**Quick wins** — small changes, high impact, can be done in a sprint or two:
- Add a missing metric to an existing template
- Add a new criteria option to discovery rules
- Add a threshold that's missing but should obviously be there
- Expose data that's already collected but not shown in the UI

**Core improvements** — meaningful feature upgrades that require design and dev time:
- New monitoring capabilities (new protocols, new device types within the feature)
- UI/UX improvements (new dashboards, better visualization)
- New automation rules or alerting enhancements
- Cross-module integration improvements

**Strategic additions** — larger efforts that change the feature's competitive position:
- ML/AI-powered capabilities (anomaly detection, predictive alerts)
- New data collection methods (streaming telemetry, gRPC)
- Major UX redesigns
- Platform-level changes (new API endpoints, new integration patterns)

### 3. Prioritize with Evidence

For each enhancement, assess:

| Factor | Question |
|--------|----------|
| **Customer demand** | How many users are asking for this? How loud is the signal? |
| **Competitive pressure** | Are competitors ahead? Is this table stakes or differentiator? |
| **Internal consistency** | Does fixing this also fix inconsistencies across modules? |
| **Reuse potential** | Can we leverage existing infrastructure from another module? |
| **Effort** | Low / Medium / High development effort |
| **Impact** | How much does this improve the user's daily workflow? |

### 4. Build the Recommendation

Be opinionated. Don't give the PM a menu of equally weighted options. Recommend:
- What to do first (and why)
- What to bundle together (enhancements that make sense as a release)
- What to defer (and what trigger should bring it back)
- What NOT to do (and why — even if competitors do it)

### 5. Outline Implementation Approach

For the top-priority enhancements, describe:
- What changes to device templates, discovery rules, UI, alerting, reporting
- What existing components to reuse (from cross-module analysis)
- What new components are needed
- What the user experience should look like after the enhancement

## Output Format

Write to `[feature-name]-enhancement/.steps/4_enhancement_findings.md`:

```markdown
# Enhancement Findings & Recommendations: [Feature/Area Name]

## Executive Summary

[One paragraph — max 5 sentences. What did we find? What should we do? What's the expected outcome?]

## Evidence Summary

| Source | # of Enhancements Identified | Strongest Signal |
|--------|------------------------------|-----------------|
| Current State Analysis | [N] | [Top finding] |
| Cross-Module Analysis | [N] | [Top finding] |
| Competitive Analysis | [N] | [Top finding] |
| Customer Feedback | [N] | [Top finding] |
| **Total (deduplicated)** | **[N]** | |

## Recommended Enhancements

### 🟢 Quick Wins (Do Now — Sprint-Level Effort)

| # | Enhancement | Why | Effort | Impact | Persona Challenge Solved |
|---|-------------|-----|--------|--------|-------------------------|
| 1 | [Enhancement] | [Evidence-based reason] | [Low] | [Description of user impact] | [Which persona story this addresses] |
| 2 | ... | ... | ... | ... | ... |

**Bundle recommendation:** [Which quick wins should ship together and why]

---

### 🔵 Core Improvements (Plan for Next Quarter)

| # | Enhancement | Why | Effort | Impact | Persona Challenge Solved |
|---|-------------|-----|--------|--------|-------------------------|
| 1 | [Enhancement] | [Evidence-based reason] | [Medium] | [Description of user impact] | [Which persona story] |
| 2 | ... | ... | ... | ... | ... |

For each core improvement, detail:

#### [Core Improvement 1]: [Name]

**What changes:**
- Discovery: [Changes to discovery rules, templates, credentials]
- Monitoring: [New metrics, polling changes, new protocols]
- Alerting: [New thresholds, alert types, notification changes]
- UI: [New dashboards, widgets, snapshot page changes]
- Reporting: [New reports or report enhancements]

**Reuse from other modules:**
[What existing components from cross-module analysis apply here]

**User experience after enhancement:**
[Describe the improved workflow — what the user sees differently]

**Competitive impact:**
[Which competitive gap does this close or which differentiation does this create]

---

### 🟣 Strategic Additions (Roadmap — Next 2-3 Quarters)

| # | Enhancement | Why | Effort | Impact | Persona Challenge Solved |
|---|-------------|-----|--------|--------|-------------------------|
| 1 | [Enhancement] | [Evidence-based reason] | [High] | [Description of user impact] | [Which persona story or "New capability"] |

---

### ⚪ Not Recommended

| Enhancement | Why Not |
|-------------|---------|
| [Something competitors do that we should NOT copy] | [Reasoning — wrong for our users, too niche, bad ROI] |

## Cross-Module Impact

These enhancements would also benefit other modules if implemented as platform improvements:

| Enhancement | Primary Feature | Also Improves |
|-------------|----------------|---------------|
| [Enhancement] | [This feature] | [Module A, Module B] |

## Success Metrics

How to measure whether the enhancement achieved its goal:

| Enhancement | Success Metric | Target |
|-------------|---------------|--------|
| [Enhancement] | [Metric — e.g., support ticket reduction, adoption rate] | [Target value] |

## Recommended Release Plan

| Phase | Enhancements | Timeline | Theme |
|-------|-------------|----------|-------|
| Phase 1 | Quick wins [list] | [Sprint/Month] | "[Theme name — e.g., Closing the gap]" |
| Phase 2 | Core improvements [list] | [Quarter] | "[Theme name]" |
| Phase 3 | Strategic additions [list] | [Future quarter] | "[Theme name]" |

## Persona Challenge Resolution Map

Final validation that every persona challenge from Step 1 is addressed:

| Persona Challenge | Enhancement(s) That Solve It | Phase | After Enhancement |
|-------------------|-----------------------------|-------|--------------------|
| [Challenge from Story 1 — e.g., "Priya's missed alert on AP failure"] | [Enhancement name(s)] | [Phase 1/2/3] | [How the persona's scenario changes — 1-2 sentences] |
| [Challenge from Story 2] | [Enhancement name(s)] | [Phase] | [Transformed outcome] |

> **If any persona challenge is NOT addressed by the recommended enhancements, flag it explicitly.** Either add an enhancement to cover it, or explain why it's out of scope with a plan for when it will be addressed.
```




## Report rebuild (mandatory)

Every step artifact this skill writes must:

1. **Markdown (source of truth, hidden):** `[slug]/.steps/<name>.md`
   - Enhancement mode: `[slug]-enhancement/.steps/<name>.md`
2. **Rebuild the consolidated report** immediately after:
   ```bash
   python "<scripts-dir>/build_report.py" "[slug]/"
   ```
   Resolve helper via `**/build_report.py` (`scripts/`).
3. If this step produced a diagram worth showing, render it with Archify (bundled at `skills/archify/`) to a visible sibling file (e.g. `[slug]-<name>.html`) and reference it first with a `<!-- diagram: [slug]-<name>.html -->` marker in the markdown, then rebuild.
4. On revise, rewrite the markdown and rebuild the report again.
5. Final chat summary (end of the whole run) cites the **`[slug].html`** path.
6. **Never delete** `.steps/*.md`, `[slug].html`, or `.steps/build_docx.py` after DOCX/slide-deck/diagram generation.

See `context/pm-operating-system.md` sections 3, 6, and 11–13.


## Quality Gate (before marking complete)

- [ ] Path: `[slug]-enhancement/.steps/4_enhancement_findings.md`
- [ ] Prioritized (quick win / core / strategic / not recommended)
- [ ] Each major item traces to persona and/or competitive gap
- [ ] Single recommended first move is clear
- [ ] `STATUS.md` updated



## Completion

After writing the file, display in chat:

---

**Step 4 Complete — Enhancement Findings & Recommendations:**

> **Total enhancements identified:** [N] (deduplicated from all sources)
>
> **🟢 Quick wins:** [N] — ship now, sprint-level effort
> - [Top quick win 1]
> - [Top quick win 2]
>
> **🔵 Core improvements:** [N] — plan for next quarter
> - [Top improvement 1]
> - [Top improvement 2]
>
> **🟣 Strategic additions:** [N] — roadmap items
> - [Top strategic item]
>
> **⚪ Not recommended:** [N] — things competitors do that we should skip
>
> **Recommended first move:** [The single most impactful thing to do first and why]
>
> Full details in `[feature-name]-enhancement/.steps/4_enhancement_findings.md`
>
> Continuing immediately to Step 5 — Enhancement Deliverables.

---
