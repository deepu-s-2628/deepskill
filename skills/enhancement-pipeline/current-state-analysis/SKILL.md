---
name: current-state-analysis
description: "Step 1 of Enhancement Pipeline: Deep dive into how a feature currently works in OpManager Plus — what it does, how it's implemented, what data it collects, what UI it exposes, what its limitations are. Use when analyzing an existing feature for enhancement."
---

# Step 1 — Current State Analysis

## Purpose

Before proposing any enhancement, understand the feature as it exists today. Map every touchpoint: discovery, monitoring, alerting, UI, reporting. Identify what works well, what's limited, and what's missing entirely.

## Input

The PM describes an existing feature or area they want to enhance. Examples:
- "I want to improve how discovery rules work — we need more criteria options"
- "Our VMware monitoring is missing some key metrics customers are asking for"
- "The alerting system needs better correlation and deduplication"
- "Wireless monitoring needs deeper access point metrics"

## Process

### 1. Identify the Feature Scope

Pin down exactly what area of OpManager Plus this covers:
- Which module(s) does this feature live in?
- What is the feature's purpose in the product?
- When was this feature likely introduced? Has it evolved significantly?

### 2. Map the Current Implementation

Reference [context/product-context.md](pm-shared/context/product-context.md) for product architecture, then research public docs to go deeper.

**UI accuracy — do not block on this step:**

Understanding the current UI, data layout, or design patterns helps this analysis, but this step runs unattended (operating system §8) — the only sanctioned pause point in the whole pipeline is Step 6's screenshot dependency. So: describe the current UI as accurately as public docs, `product-context.md`, and any screenshots already on hand support, and explicitly note it as an assumption where you're inferring UI details rather than confirming them (e.g. "assumed based on product-context's UI Patterns section — not confirmed against a live screenshot"). Do not stop and wait for screenshots here; that request belongs at Step 6, where the wireframe step actually needs pixel-accurate UI and has the mechanism to pause for it.

You can request additional screenshots at any point during the analysis if you need to see a specific page, dialog, or report. Always explain what you need and why.

**Discovery & Onboarding:**
- How are devices/components for this feature discovered?
- What credentials/protocols are used?
- What device templates apply?
- What discovery rules exist for this area?
- What's the onboarding experience for a new user enabling this feature?

**Monitoring & Data Collection:**
- What protocols collect data? (SNMP, WMI, CLI, API, agent, syslog, traps)
- What specific metrics are monitored? List them.
- What polling intervals are used?
- What thresholds are pre-configured in device templates?
- Are there custom monitor options?

**Alerting & Notifications:**
- What default alarms exist for this feature?
- What severity levels are used?
- Are there feature-specific notification profiles?
- Does alarm suppression or correlation apply here?

**UI & Visualization:**
- What does the snapshot page show for these devices?
- Are there dedicated dashboards or widgets?
- How does this appear in business views, topology maps?
- What graphs/charts are available?

**Reporting:**
- What built-in reports cover this feature?
- Are there scheduled report options?
- What data is available for custom reports?

**Integration Points:**
- Does this feature integrate with add-ons (NCM, NetFlow, Firewall, APM)?
- Is there workflow automation support?
- Any API exposure for this feature?

### 3. Identify Known Limitations

Based on product docs, community forums, and your understanding:
- What common user complaints exist about this feature?
- What workarounds do users employ?
- What feature requests have surfaced in forums or review sites?
- What gaps become obvious when you map the full workflow?

## Output Format

Write to `[feature-name]-enhancement/.steps/1_current_state.md`:

```markdown
# Current State Analysis: [Feature/Area Name]

## Feature Overview
[2-3 paragraphs: What this feature does, where it sits in OpManager Plus, who uses it, and why it exists.]

## Implementation Map

### Discovery & Onboarding
- **Discovery method:** [How devices for this feature are discovered]
- **Credentials required:** [SNMP v1/v2/v3, WMI, SSH, API, etc.]
- **Device templates:** [Which templates apply, how many, what they include]
- **Discovery rules:** [What auto-configuration happens post-discovery]
- **Setup effort:** [Easy/Moderate/Complex — and why]

### Monitoring Coverage
| Metric Category | Metrics Monitored | Protocol | Interval | Threshold |
|----------------|-------------------|----------|----------|-----------|
| [Category] | [Specific metrics] | [SNMP/WMI/etc.] | [5m/10m/etc.] | [Yes/No + values] |

### Alerting
| Alarm | Severity | Trigger Condition | Default Action |
|-------|----------|-------------------|----------------|
| [Alarm name] | [Crit/Warn/etc.] | [Condition] | [Email/SMS/ticket/etc.] |

### UI & Visualization
- **Snapshot page:** [What's shown on device detail page]
- **Dashboards:** [Dedicated widgets/dashboards available]
- **Maps/Topology:** [How it appears in business views, L2 maps]
- **Graphs:** [What time-series data is charted]

### Reporting
- **Built-in reports:** [List available reports]
- **Exportable:** [PDF/CSV/scheduled options]

### Integrations
- **Add-on connections:** [NCM, NetFlow, APM, Firewall — relevance to this feature]
- **Automation:** [Workflow automation support]
- **API:** [REST API endpoints for this feature]

## What Works Well
[List the aspects of the current implementation that are solid and should be preserved]
1. [Strength 1]
2. [Strength 2]
3. [Strength 3]

## Known Limitations
| # | Limitation | Impact | User Workaround (if any) |
|---|-----------|--------|-------------------------|
| 1 | [Limitation] | [Who it affects and how] | [What users do instead] |
| 2 | ... | ... | ... |

## User Feedback Signals
[Evidence from public forums, G2, Gartner, Reddit, ManageEngine community — what do users say about this specific feature area?]
- [Feedback 1 — source]
- [Feedback 2 — source]

## Persona Stories — The Pain Today

These are narrative-driven stories showing the real human impact of the current limitations. They will be used to open presentations, anchor the PRD, and serve as conference/marketing material. Write them at keynote quality — vivid, specific, emotional.

### Story 1: [Persona Name] — [Title] at [Company Type]
[150-200 words. Name this person. Describe their role, company, and team. Tell the story of a specific moment where the current feature's limitations caused real pain — a missed alert because a metric wasn't monitored, a workaround that failed at the worst time, an outage that could have been prevented. Show the frustration, the consequences, and what they wish they had. End with: "If OpManager Plus could [enhancement], [name] would have..."]

### Story 2: [Persona Name] — [Title] at [Company Type]
[Different persona — different company size, industry, or seniority level. Different limitation, different consequence. Perhaps this person is an MSP managing 50 clients, or a CTO who can't get the reports they need for the board.]

> **These stories will be reused in the executive presentation (Slide 2), engineering presentation, PRD, and marketing materials.**

## Initial Enhancement Opportunities
[Based on this analysis alone — before competitive research — what jumps out as obvious improvements?]
1. [Opportunity]
2. [Opportunity]
3. [Opportunity]
```




## Report rebuild (mandatory)

Write markdown to `.steps/<name>.md` (hidden), then rebuild `analysis.html` and, if this step produced a diagram, render it and reference it first with a `<!-- diagram: architecture.html -->` marker. **Full procedure, exact paths, and the rebuild command are in `pm-shared/context/pm-operating-system.md` §§3, 6, 11a — already loaded as mandatory context for every run, so it is not repeated here.** Never delete `.steps/*.md`, `analysis.html`, or `.steps/build_docx.py`.

## Quality Gate (before marking complete)

Gate ledger for this step — write `.steps/GATES-1.md` from `<resolved shared parent>/unlazy-gates/templates/gates-leaf.md` before producing this step's content, one gate per item below. Resolution rule (self-correct on a failed gate, document the gap and continue — never abandon, never pause): `pm-shared/context/pm-operating-system.md` §18.


- [ ] G1: Written at `[slug]-enhancement/.steps/1_current_state.md`
  CHECK: node -e "const fs=require('fs');process.exit(fs.statSync('analysis.html').mtimeMs>=fs.statSync('.steps/1_current_state.md').mtimeMs?0:1)"
  EXPECT: (exits zero)
- [ ] G2: Discovery → monitor → alert → UI → report map complete enough to enhance
  (manual — no command can decide this)
- [ ] G3: Strengths and limitations are specific (not generic)
  (manual — no command can decide this)
- [ ] G4: 2–3 persona pain stories at keynote quality
  CHECK: node -e "const c=(require('fs').readFileSync('.steps/1_current_state.md','utf8').match(/^### Story \d+/gm)||[]).length;console.log(c)"
  EXPECT: a printed count of 2 or 3
- [ ] G5: Screenshot requests made when UI truth is needed
  (manual — no command can decide this)
- [ ] G6: `Progress.md` updated
  CHECK: node -e "const fs=require('fs');process.exit(fs.statSync('Progress.md').mtimeMs>=fs.statSync('.steps/1_current_state.md').mtimeMs?0:1)"
  EXPECT: (exits zero)
## Completion

After writing the file, display in chat:

---

**Step 1 Complete — Current State Analysis:**

> **Feature area:** [Name]
> **Module:** [Where it lives in OpManager Plus]
> **Current metrics monitored:** [Count]
> **Key strengths:** [2-3 bullet points]
> **Key limitations:**
> - [Limitation 1]
> - [Limitation 2]
> - [Limitation 3]
>
> **Early enhancement signals:** [1-2 sentences on what jumps out]
>
> Full details in `[feature-name]-enhancement/.steps/1_current_state.md`
>
> Continuing immediately to Step 2 — Cross-Module Analysis.

---
