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

Reference [context/product-context.md](../../../context/product-context.md) for product architecture, then research public docs to go deeper.

**Request Screenshots:**

If you need to understand the current UI, data layout, or design patterns for this feature, ask the PM for screenshots:

> **To analyze the current implementation accurately, could you share screenshots of:**
> - The main page/snapshot page for this feature
> - The settings or configuration page
> - Any relevant dashboard widgets or views
>
> This helps me document exactly what exists today and what the UI looks like.

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

Write to `ITOM-PM-Result/[feature-name]-enhancement/.steps/1_current_state.md`:

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

- [ ] Path: `ITOM-PM-Result/[slug]-enhancement/.steps/1_current_state.md`
- [ ] Discovery → monitor → alert → UI → report map complete enough to enhance
- [ ] Strengths and limitations are specific (not generic)
- [ ] 2–3 persona pain stories at keynote quality
- [ ] Screenshot requests made when UI truth is needed
- [ ] `STATUS.md` updated

- [ ] `.steps/` markdown written, `report.html` rebuilt
- [ ] Markdown is hidden under `.steps/`; HTML visible under `steps/`; never delete either or Generated artifacts


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
> Full details in `ITOM-PM-Result/[feature-name]-enhancement/.steps/1_current_state.md`
>
> Continuing immediately to Step 2 — Cross-Module Analysis.

---
