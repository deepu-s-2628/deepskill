---
name: competitive-analysis
description: "Step 2 of PM Feature Pipeline: Research how competitors implement this feature. Analyze customer sentiment. Identify gaps and opportunities for OpManager Plus. Use when doing competitive intelligence for a feature."
---

# Step 2 — Competitive Analysis

## Purpose

Research how competitors have implemented this feature, what customers think of their implementations, and where OpManager Plus can differentiate.

**Plain-language bar (DOE) — operating system §7:** this step's own written output is held to the same bar Step 1 was, not a lighter one just because it's deeper in the pipeline. "Technical approach: Data collection: [method]" should say what the method actually does for the customer, not just name it — a reader shouldn't need to already know a competitor's product to follow the Competitor Breakdown or the Comparison Matrix.

## Input

Read `[feature-name]/.steps/1_brainstorm.md` for full context on the feature.

**CRITICAL: Extract the persona challenges from Step 1.** Read the Persona Stories section carefully. These are the real human problems your competitive analysis must address. For each competitor you evaluate, explicitly check: **does their implementation solve the challenges described in the persona stories?** If a competitor solves Priya's 3 AM blind spot problem but not Marcus's compliance reporting gap, say so specifically.

## Process

### 1. Identify Relevant Competitors

Not all competitors are relevant for every feature. Select only those that offer this capability or a close equivalent:

**Primary competitors to check:**
- SolarWinds (NPM, NCM, SAM)
- PRTG Network Monitor
- Datadog
- Dynatrace
- Zabbix
- LogicMonitor

**Specialist competitors (check if relevant to the feature):**
- Auvik (cloud-managed networking)
- LiveAction (network performance)
- Kentik (network observability, flow)
- Cisco Crosswork / ThousandEyes
- AppNeta
- Nagios
- LibreNMS

### 2. Research Each Competitor

For each relevant competitor, search the web for:

**Product capability:**
- What exactly do they offer for this feature?
- How deep is their implementation? (basic monitoring vs. full management)
- What data collection method do they use?
- What metrics/data points do they expose?
- How is it configured/set up?
- What does the UI look like? (screenshots if available)

**Customer sentiment** (search G2, Gartner Peer Insights, Reddit, vendor community forums, TrustRadius):
- What do customers love about their implementation?
- What are the pain points, gaps, and complaints?
- What do customers wish it could do that it can't?
- Any migration stories (customers switching away)?

### 3. Synthesize Gaps & Opportunities

Consolidate findings into actionable intelligence for OpManager Plus.

## Output Format

Write to `[feature-name]/.steps/2_competitive_analysis.md`:

```markdown
# Competitive Analysis: [Feature Name]

## Executive Summary
[3-4 sentences: who does this best, where the market gaps are, and what OpManager Plus's opportunity looks like]

## Competitor Breakdown

### [Competitor 1 Name]
**What they offer:**
[Description of their implementation]

**Technical approach:**
- Data collection: [method]
- Coverage depth: [what they monitor]
- Setup complexity: [easy/moderate/complex]

**What customers say:**
- ✅ Praise: [what customers like, with source]
- ❌ Complaints: [what customers dislike, with source]
- 💡 Wishlist: [what customers ask for, with source]

**Key insight:** [One sentence — the most important takeaway for our strategy]

---

### [Competitor 2 Name]
[Same structure]

---

[Repeat for each relevant competitor]

## Competitive Comparison Matrix

| Capability | SolarWinds | PRTG | Datadog | Dynatrace | OpManager Plus (current) |
|-----------|-----------|------|---------|-----------|-------------------------|
| [Capability 1] | ✅/⚠️/❌ | ... | ... | ... | ... |
| [Capability 2] | ... | ... | ... | ... | ... |

Legend: ✅ Full support | ⚠️ Partial/limited | ❌ Not available

## Gap & Opportunity Analysis

### Where Competitors Fall Short
| Gap | Who Has This Problem | Why It Matters | Our Opportunity |
|-----|---------------------|----------------|-----------------|
| [Gap 1] | [Competitors] | [Customer impact] | [What we should do better] |

### Where Competitors Excel (We Must Match)
| Capability | Best-in-class | Why We Can't Skip This |
|-----------|--------------|----------------------|
| [Capability] | [Who does it best] | [Table stakes reason] |

### Differentiation Opportunities
[2-3 specific ways OpManager Plus can be genuinely better, not just "me too". These should be grounded in real customer pain points discovered in the research.]

1. **[Opportunity 1]:** [Description and reasoning]
2. **[Opportunity 2]:** [Description and reasoning]
3. **[Opportunity 3]:** [Description and reasoning]

## Persona Challenge Coverage

Map each persona challenge from Step 1 to competitive findings:

| Persona Challenge (from Brainstorm) | Who Solves It Today | How They Solve It | Gap We Can Exploit |
|-------------------------------------|--------------------|--------------------|--------------------|
| [Challenge from Story 1 — e.g., "Priya's SD-WAN blind spot"] | [Competitor(s) or "Nobody"] | [Their approach] | [Our opportunity] |
| [Challenge from Story 2] | ... | ... | ... |

> **Every persona challenge must appear in this table.** If no competitor solves it, that's a differentiation goldmine. If all competitors solve it, that's table stakes we must match.

## Recommended Strategic Position
[One paragraph: Based on this analysis, should OpManager Plus aim for feature parity, differentiation, or leapfrog? What's the positioning?]

## Sources
- [List all sources consulted with links where available]
```




## Report rebuild (mandatory)

Write markdown to `.steps/<name>.md` (hidden), then rebuild `analysis.html` and, if this step produced a diagram, render it and reference it first with a `<!-- diagram: architecture.html -->` marker. **Full procedure, exact paths, and the rebuild command are in `pm-shared/context/pm-operating-system.md` §§3, 6, 11a — already loaded as mandatory context for every run, so it is not repeated here.** Never delete `.steps/*.md`, `analysis.html`, or `.steps/build_docx.py`.

## Quality Gate (before marking complete)

Gate ledger for this step — write `.steps/GATES-2.md` from `<resolved shared parent>/unlazy-gates/templates/gates-leaf.md` before producing this step's content, one gate per item below. Resolution rule (self-correct on a failed gate, document the gap and continue — never abandon, never pause): `pm-shared/context/pm-operating-system.md` §18.


- [ ] G1: Written at `[slug]/.steps/2_competitive_analysis.md`, `analysis.html` rebuilt
  CHECK: node -e "const fs=require('fs');process.exit(fs.statSync('analysis.html').mtimeMs>=fs.statSync('.steps/2_competitive_analysis.md').mtimeMs?0:1)"
  EXPECT: (exits zero)
- [ ] G2: ≥4 competitors or explicit exception
  CHECK: node -e "const t=require('fs').readFileSync('.steps/2_competitive_analysis.md','utf8');const c=(t.match(/^### .+/gm)||[]).length;process.exit(c>=4||/exception/i.test(t)?0:1)"
  EXPECT: (exits zero)
- [ ] G3: Persona-challenge coverage tied to Step 1 stories
  (manual — no command can decide this)
- [ ] G4: Table stakes vs differentiators clear
  (manual — no command can decide this)
- [ ] G5: Recommended position stated (parity / differentiate / leapfrog)
  CHECK: node -e "process.exit(/parity|differentiate|leapfrog/i.test(require('fs').readFileSync('.steps/2_competitive_analysis.md','utf8'))?0:1)"
  EXPECT: (exits zero)
- [ ] G6: Sources cited with links
  CHECK: node -e "const t=require('fs').readFileSync('.steps/2_competitive_analysis.md','utf8');process.exit(/## Sources[\s\S]*\[.+\]\(http/.test(t)?0:1)"
  EXPECT: (exits zero)
- [ ] G7: `Progress.md` updated
  CHECK: node -e "const fs=require('fs');process.exit(fs.statSync('Progress.md').mtimeMs>=fs.statSync('.steps/2_competitive_analysis.md').mtimeMs?0:1)"
  EXPECT: (exits zero)
## Completion

After writing the file, display a **summary directly in chat**:

---

**Step 2 Complete — Competitive Analysis Summary:**

> **Competitors analyzed:** [List names]
> **Best-in-class:** [Who does it best and what makes them strong]
> **Biggest customer pain points across competitors:**
> - [Pain point 1]
> - [Pain point 2]
> - [Pain point 3]
>
> **Our differentiation opportunity:** [1-2 sentences on where OpManager Plus can win]
>
> **Recommended position:** [Feature parity / Differentiation / Leapfrog]
>
> Full details in `[feature-name]/.steps/2_competitive_analysis.md`
>
> Continuing immediately to Step 3 — Technical Analysis.

---
