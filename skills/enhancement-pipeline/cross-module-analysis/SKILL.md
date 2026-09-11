---
name: cross-module-analysis
description: "Step 2 of Enhancement Pipeline: Analyze how the feature relates to other OpManager Plus modules. Find duplication, reusable components, hidden capabilities in other modules that could solve this use case, and inconsistencies."
---

# Step 2 — Cross-Module Analysis

## Purpose

OpManager Plus is a large product with many modules built over 20+ years. Features sometimes exist in one module that could benefit another. Patterns get duplicated inconsistently. A setting in one area solves a problem users report in another area. This step maps those connections.

## Input

Read `[feature-name]-enhancement/.steps/1_current_state.md` for the current state of the feature being enhanced.

**CRITICAL: Extract the persona challenges from Step 1.** Read the "Persona Stories — The Pain Today" section carefully. These are the real user frustrations driving this enhancement. When you find a hidden capability in another module, explicitly check: **does it solve any of the persona challenges?** If Module X has a capability that would have prevented Priya's 3 AM incident, that's a high-priority reuse opportunity.

## Process

### 1. Map Related Modules

Reference [context/product-context.md](../../../context/product-context.md) and identify every module that touches or relates to this feature:

- Which modules collect similar types of data?
- Which modules have similar UI patterns for a related use case?
- Which modules face the same underlying technical challenge?
- Which add-ons (NCM, NetFlow, APM, Firewall Analyzer, OpUtils) are relevant?

### 2. Check for Duplication & Inconsistency

Look for:

**Duplicate functionality:**
- Is the same metric or data point collected in more than one place?
- Are there two different ways to configure the same thing?
- Do different modules handle the same device type differently?

**Inconsistent behavior:**
- Does alerting work differently for similar events across modules?
- Are thresholds configured differently for the same metric in different contexts?
- Does the UI present the same type of data in different formats in different modules?
- Are discovery rules applied inconsistently across device types?

**Missing cross-references:**
- Does Module A collect data that Module B's users need but can't access?
- Are there reports in one module that would be valuable in another?
- Could a dashboard widget from one module solve a gap in another?

### 3. Find Hidden Capabilities

Search for patterns that already exist elsewhere in OpManager Plus that could be applied to the enhancement:

- Is there a similar configuration pattern in another module that we could replicate?
- Does another module already handle a similar workflow that could be extended?
- Are there device template patterns that could be adapted?
- Are there discovery rule actions that exist but aren't available for this feature's device types?
- Does another module's alerting logic solve a problem this feature has?

### 4. Identify Reuse Opportunities

What existing infrastructure can the enhancement leverage:
- Existing polling engine capabilities
- Existing alert correlation/suppression logic
- Existing UI components (widget types, graph types, table layouts)
- Existing report templates
- Existing workflow automation actions
- Existing API endpoints that could be extended

## Output Format

Write to `[feature-name]-enhancement/.steps/2_cross_module_analysis.md`:

```markdown
# Cross-Module Analysis: [Feature/Area Name]

## Related Modules Map

| Module | Relationship | Relevance |
|--------|-------------|-----------|
| [Module name] | [How it connects to this feature] | [High/Medium/Low] |

## Duplication & Inconsistencies Found

### Duplication
| What's Duplicated | Where (Module A) | Where (Module B) | Impact |
|-------------------|-------------------|-------------------|--------|
| [Item] | [Location] | [Location] | [Confusion/maintenance burden/data mismatch] |

### Inconsistencies
| What's Inconsistent | Module A Behavior | Module B Behavior | Which Is Better |
|---------------------|-------------------|-------------------|-----------------|
| [Item] | [How A does it] | [How B does it] | [Recommendation] |

## Hidden Capabilities (Already Exists Elsewhere)

These capabilities exist in other parts of OpManager Plus and could be applied to this feature:

| Capability | Where It Exists | How It Could Help This Feature |
|-----------|----------------|-------------------------------|
| [Capability] | [Module/feature] | [How to apply it here] |

## Reuse Opportunities

### Infrastructure We Can Leverage
| Existing Component | Current Use | How to Reuse for Enhancement |
|-------------------|------------|------------------------------|
| [Component] | [Current purpose] | [Enhancement application] |

### Patterns to Replicate
[Describe 2-3 patterns from other modules that, if applied here, would solve known limitations]

1. **[Pattern name]** (from [Module])
   - How it works there: [Description]
   - How to apply here: [Description]
   - What it solves: [Which limitation from Step 1]

2. **[Pattern name]** (from [Module])
   - How it works there: [Description]
   - How to apply here: [Description]
   - What it solves: [Which limitation from Step 1]

## Cross-Module Enhancement Ideas

Based on this analysis, these enhancements would benefit not just this feature but multiple modules:

| Enhancement | Benefits This Feature | Also Benefits |
|-------------|----------------------|---------------|
| [Enhancement] | [How] | [Which other modules] |

## Consolidation Recommendations

[Are there things that should be unified, merged, or standardized across modules as part of this enhancement?]

1. [Recommendation]
2. [Recommendation]

## Persona Challenge → Cross-Module Solutions

Map each persona challenge from Step 1 to cross-module findings:

| Persona Challenge (from Step 1) | Existing Capability in Another Module | How to Apply It Here | Effort |
|---------------------------------|--------------------------------------|----------------------|--------|
| [Challenge from Story 1] | [What exists and where] | [How to reuse/adapt it] | [Low/Med/High] |
| [Challenge from Story 2] | [What exists or "Nothing found"] | [Build new or adapt] | [Effort] |

> **If a persona challenge is already solved by another module, that's the fastest win. Prioritize these in Step 4.**
```




## Report rebuild (mandatory)

Write markdown to `.steps/<name>.md` (hidden), then rebuild `analysis.html` and, if this step produced a diagram, render it and reference it first with a `<!-- diagram: architecture.html -->` marker. **Full procedure, exact paths, and the rebuild command are in `context/pm-operating-system.md` §§3, 6, 11a — already loaded as mandatory context for every run, so it is not repeated here.** Never delete `.steps/*.md`, `analysis.html`, or `.steps/build_docx.py`.

## Quality Gate (before marking complete)

Gate ledger for this step — write `.steps/GATES-2.md` from `skills/unlazy-gates/templates/gates-leaf.md` before producing this step's content, one gate per item below. Resolution rule (self-correct on a failed gate, document the gap and continue — never abandon, never pause): `context/pm-operating-system.md` §18.


- [ ] G1: Written at `[slug]-enhancement/.steps/2_cross_module_analysis.md`
  CHECK: node -e "const fs=require('fs');process.exit(fs.statSync('analysis.html').mtimeMs>=fs.statSync('.steps/2_cross_module_analysis.md').mtimeMs?0:1)"
  EXPECT: (exits zero)
- [ ] G2: Concrete reuse / duplication / inconsistency findings
  (manual — no command can decide this)
- [ ] G3: Ties back to persona challenges where possible
  (manual — no command can decide this)
- [ ] G4: `Progress.md` updated
  CHECK: node -e "const fs=require('fs');process.exit(fs.statSync('Progress.md').mtimeMs>=fs.statSync('.steps/2_cross_module_analysis.md').mtimeMs?0:1)"
  EXPECT: (exits zero)
## Completion

After writing the file, display in chat:

---

**Step 2 Complete — Cross-Module Analysis:**

> **Modules analyzed:** [Count and names]
> **Duplications found:** [Count]
> **Hidden capabilities to leverage:** [Count]
> **Key finding:** [1-2 sentences — the most impactful cross-module insight]
>
> **Reuse opportunity highlight:** [The single most valuable existing component that can be leveraged]
>
> Full details in `[feature-name]-enhancement/.steps/2_cross_module_analysis.md`
>
> Continuing immediately to Step 3 — Competitive Analysis.

---
