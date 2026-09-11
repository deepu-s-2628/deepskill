---
name: enhancement-competitive
description: "Step 3 of Enhancement Pipeline: Focused competitive analysis for an existing feature enhancement. How do competitors handle this specific area? What are they doing better? What are customers saying about their implementations vs ours?"
---

# Step 3 — Enhancement Competitive Analysis

## Purpose

Understand how competitors handle this specific feature area. Unlike the new-feature competitive analysis (which surveys broadly), this is focused: we already have this feature, so we need to know exactly where competitors are ahead of us, where they have the same gaps, and what customers specifically praise or criticize.

## Input

Read:
- `[feature-name]-enhancement/.steps/1_current_state.md` — what we currently do and **persona challenges**
- `[feature-name]-enhancement/.steps/2_cross_module_analysis.md` — internal opportunities

**CRITICAL: The persona challenges from Step 1 are your competitive benchmark.** For each competitor, explicitly check: **would their implementation have prevented the bad scenarios in our persona stories?** If SolarWinds' version would have caught the issue Priya faced, that's a concrete competitive gap we must close. If no competitor solves it either, that's a differentiation opportunity.

## Process

### 1. Select Relevant Competitors

From the competitor list, pick only those that are strong in this specific feature area. Not every competitor matters for every enhancement.

**Competitor pool:**
- SolarWinds (NPM, NCM, SAM, IPAM, NTA)
- PRTG Network Monitor
- Datadog
- Dynatrace
- Zabbix
- LogicMonitor
- Auvik
- Nagios / LibreNMS
- Cisco ThousandEyes / Crosswork
- Kentik
- Checkmk
- New Relic

### 2. Feature-Specific Deep Dive

For each relevant competitor, research:

**Implementation depth:**
- How do they handle this exact feature area?
- What metrics do they monitor that we don't?
- What configuration options do they provide that we lack?
- What UI/UX patterns do they use for this feature?
- What automation or intelligence do they add (auto-thresholds, ML-based, recommendations)?

**Setup & configuration:**
- How easy is it to enable this feature?
- What's the onboarding experience?
- Do they have templates, wizards, or auto-configuration?
- How do their discovery rules or auto-detection compare to ours?

**Where they're specifically better:**
- What do they do in this area that we objectively cannot do today?
- What customer pain points (from our Step 1) have they already solved?
- What UX improvements have they made that we should learn from?

### 3. Customer Sentiment (Feature-Specific)

Search for customer feedback specifically about this feature area:

**Sources to check:**
- G2 reviews mentioning this feature by name
- Gartner Peer Insights with feature-specific comments
- Reddit (r/sysadmin, r/networking, r/msp) threads about this capability
- ManageEngine PitStop community — feature requests and complaints
- Competitor community forums — what do THEIR customers complain about?
- Product comparison articles that focus on this feature

**What to extract:**
- Direct quotes comparing products on this feature
- Feature requests that indicate gaps in the market
- Praise for specific implementations (what exactly do users love?)
- Frustration patterns (what's broken across the industry?)

### 4. Gap Analysis vs Current State

Compare what competitors offer against our Step 1 findings:
- For each limitation we identified, which competitors have solved it?
- For each strength we identified, do competitors match or exceed it?
- What completely new approaches exist that we haven't considered?

## Output Format

Write to `[feature-name]-enhancement/.steps/3_competitive_analysis.md`:

```markdown
# Enhancement Competitive Analysis: [Feature/Area Name]

## Executive Summary
[3-4 sentences: Where we stand vs competitors on this specific feature. Are we behind, at parity, or ahead? What's the one thing we must address?]

## Competitor Deep Dives

### [Competitor 1]
**Their implementation:**
[How they handle this feature area specifically]

**What they do better than us:**
- [Specific capability we lack]
- [Better UX pattern]
- [Deeper metric coverage]

**What we do better than them:**
- [Our advantage]

**Customer quotes:**
> "[Quote about this feature from their customer]" — [Source]

**Key takeaway:** [One sentence]

---
[Repeat for each relevant competitor]

## Feature-Level Comparison

| Specific Capability | OpManager Plus | [Comp 1] | [Comp 2] | [Comp 3] |
|---------------------|---------------|----------|----------|----------|
| [Capability] | Current state | Their state | Their state | Their state |

Legend: ✅ Strong | ⚠️ Basic/Limited | ❌ Missing | 🌟 Best-in-class

## Our Limitations vs Competitor Solutions

| Our Limitation (from Step 1) | Who Has Solved It | How They Solved It | Effort to Match |
|------------------------------|-------------------|--------------------|-----------------| 
| [Limitation] | [Competitor(s)] | [Their approach] | [Low/Med/High] |

## Customer Sentiment Summary

### What Users Want (Across All Products)
| Demand | Frequency | Who Provides It | Our Status |
|--------|-----------|-----------------|------------|
| [Feature demand] | [Common/Occasional/Rare] | [Competitors] | [Have it/Partial/Missing] |

### Direct Comparison Quotes
> "[Customer comparing OpManager to competitor on this feature]" — [Source]

## Competitive Enhancement Priorities

Based on competitive pressure, rank enhancements by urgency:

| Priority | Enhancement | Competitive Driver | Customer Demand |
|----------|-------------|-------------------|-----------------|
| P0 — Must have | [Enhancement] | [Who's ahead] | [Evidence] |
| P1 — Should have | [Enhancement] | [Market expectation] | [Evidence] |
| P2 — Nice to have | [Enhancement] | [Differentiation play] | [Evidence] |

## Persona Challenge Coverage

Map each persona challenge from Step 1 to competitive findings:

| Persona Challenge (from Step 1) | Who Solves It Today | How They Solve It | Our Gap |
|-------------------------------------|--------------------|--------------------|----------|
| [Challenge from Story 1 — e.g., "Priya's workaround with spreadsheets"] | [Competitor(s) or "Nobody"] | [Their approach] | [What we need to do] |
| [Challenge from Story 2] | ... | ... | ... |

> **Every persona challenge must appear in this table.** Challenges that no competitor solves are differentiation opportunities. Challenges that every competitor solves are table stakes.

## Industry Trends

[What's the direction this feature area is heading across the industry? Any new approaches, technologies, or paradigms emerging?]
```




## Report rebuild (mandatory)

Write markdown to `.steps/<name>.md` (hidden), then rebuild `analysis.html` and, if this step produced a diagram, render it and reference it first with a `<!-- diagram: architecture.html -->` marker. **Full procedure, exact paths, and the rebuild command are in `context/pm-operating-system.md` §§3, 6, 11a — already loaded as mandatory context for every run, so it is not repeated here.** Never delete `.steps/*.md`, `analysis.html`, or `.steps/build_docx.py`.

## Quality Gate (before marking complete)

Gate ledger for this step — write `.steps/GATES-3.md` from `skills/unlazy-gates/templates/gates-leaf.md` before producing this step's content, one gate per item below. Resolution rule (self-correct on a failed gate, document the gap and continue — never abandon, never pause): `context/pm-operating-system.md` §18.


- [ ] G1: Written at `[slug]-enhancement/.steps/3_competitive_analysis.md`
  CHECK: node -e "const fs=require('fs');process.exit(fs.statSync('analysis.html').mtimeMs>=fs.statSync('.steps/3_competitive_analysis.md').mtimeMs?0:1)"
  EXPECT: (exits zero)
- [ ] G2: Focused on our existing feature gaps (not generic market survey only)
  (manual — no command can decide this)
- [ ] G3: Persona challenges used as competitive benchmark
  (manual — no command can decide this)
- [ ] G4: Sources cited
  CHECK: node -e "const t=require('fs').readFileSync('.steps/3_competitive_analysis.md','utf8');process.exit(/## Sources[\s\S]*\[.+\]\(http/.test(t)?0:1)"
  EXPECT: (exits zero)
- [ ] G5: `Progress.md` updated
  CHECK: node -e "const fs=require('fs');process.exit(fs.statSync('Progress.md').mtimeMs>=fs.statSync('.steps/3_competitive_analysis.md').mtimeMs?0:1)"
  EXPECT: (exits zero)
## Completion

After writing the file, display in chat:

---

**Step 3 Complete — Enhancement Competitive Analysis:**

> **Competitors analyzed:** [Names]
> **Our position:** [Behind / At parity / Ahead — on this specific feature]
> **Biggest competitive gap:** [What competitors do that we can't]
> **Biggest customer demand:** [What users are asking for across all products]
>
> **Priority enhancements from competitive pressure:**
> - P0: [Must-have enhancement]
> - P1: [Should-have enhancement]
> - P2: [Nice-to-have enhancement]
>
> Full details in `[feature-name]-enhancement/.steps/3_competitive_analysis.md`
>
> Continuing immediately to Step 4 — Enhancement Findings & Recommendations.

---
