---
name: feature-definition
description: "Step 4 of PM Feature Pipeline: Define exactly what needs to be built for OpManager Plus — complete feature scope, user flows, settings, dashboards, alerts, and integration points."
---

# Step 4 — Feature Definition

## Purpose

Define exactly what needs to be built. This is the bridge between technical analysis and actual deliverables — it translates technical capability into user-facing product requirements.

## Input

Read all prior step files:
- `ITOM-PM-Result/[feature-name]/.steps/1_brainstorm.md` — feature understanding, target users, and **persona challenges**
- `ITOM-PM-Result/[feature-name]/.steps/2_competitive_analysis.md` — what to match and where to differentiate
- `ITOM-PM-Result/[feature-name]/.steps/3_technical_analysis.md` — how it works technically
- [context/product-context.md](../../../context/product-context.md) — existing product patterns

**CRITICAL: The persona challenges from Step 1 are your acceptance test.** Every must-have capability in v1 should trace back to at least one persona challenge. If a capability doesn't help solve any persona's problem, question whether it belongs in v1. When defining user flows, walk through them as each persona — does this flow prevent the bad scenario from their story?

## Process

### 1. Define Feature Scope

Using inputs from all prior steps, clearly separate:
- **Must-have (v1):** Minimum viable feature that delivers core value
- **Nice-to-have (v1.1):** Meaningful improvements for fast follow-up
- **Future (v2+):** Ambitious extensions to defer

### 2. Map User Flows

For each target user (from Step 1), trace their journey:
- How do they discover this feature exists?
- How do they set it up / onboard?
- How do they use it day-to-day?
- How do they troubleshoot using it?
- How do they configure it to their needs?

### 3. Define Every Screen

For each screen in the feature:
- What is its purpose?
- What data/widgets/tables/charts appear?
- What actions can the user take?
- What drilldowns are available?
- How does it connect to other screens?

### 4. Define Settings & Configuration

What can the user configure?
- Setup wizard steps
- Ongoing settings
- Per-device vs. global settings
- Default values

## Output Format

Write to `ITOM-PM-Result/[feature-name]/.steps/4_feature_definition.md`:

```markdown
# Feature Definition: [Feature Name]

## Feature Scope

### Must-Have (v1) — Launch Requirements
| # | Capability | Description | User Value | Persona Challenge Solved |
|---|-----------|-------------|------------|-------------------------|
| 1 | [Capability] | [What it does] | [Why users need it] | [Which persona story this addresses — e.g., "Priya's blind spot"] |
| 2 | ... | ... | ... | ... |

> **Every v1 capability must trace to at least one persona challenge.** If it doesn't solve a real human problem identified in Step 1, reconsider its priority.

### Nice-to-Have (v1.1) — Fast Follow
| # | Capability | Description | Why Deferred |
|---|-----------|-------------|--------------|
| 1 | [Capability] | [What it does] | [Reason for deferral] |

### Future Considerations (v2+)
| # | Capability | Description | Prerequisite |
|---|-----------|-------------|--------------|
| 1 | [Capability] | [What it does] | [What needs to exist first] |

---

## User Flows

### Flow 1: Discovery & Setup
```
[Step-by-step flow with decision points]
1. User navigates to [location]
2. User clicks [action]
3. System presents [what]
4. User provides [input]
5. System [validates/processes]
6. [Completion state]
```

### Flow 2: Day-to-Day Monitoring
```
[Step-by-step flow]
```

### Flow 3: Troubleshooting / Drill-down
```
[Step-by-step flow]
```

### Flow 4: Configuration / Settings
```
[Step-by-step flow]
```

---

## Screen Definitions

### Screen 1: [Screen Name] (e.g., "SD-WAN Dashboard")
**Purpose:** [What this screen is for]
**Navigation path:** [How to reach it]

**Layout:**
| Section | Content | Interactions |
|---------|---------|-------------|
| [Area] | [What's displayed] | [Click, filter, drill-down actions] |

**Widgets/Components:**
- [Widget 1]: [Description, data shown, visualization type]
- [Widget 2]: [Description]

**Drilldowns:**
- Click [element] → navigates to [destination]

---

### Screen 2: [Screen Name]
[Same structure]

---

### Screen 3: [Screen Name]
[Same structure]

---

## Settings & Configuration

### Initial Setup (First-time Configuration)
| Step | What User Does | What System Does | Required/Optional |
|------|---------------|-----------------|-------------------|
| 1 | [Action] | [Response] | Required |
| 2 | ... | ... | ... |

### Ongoing Settings
| Setting | Location | Default Value | Options | Impact |
|---------|----------|---------------|---------|--------|
| [Setting name] | [Where in UI] | [Default] | [Choices] | [What it affects] |

### Per-Device Settings
| Setting | Default | Override Level | Notes |
|---------|---------|---------------|-------|
| [Setting] | [Default] | Device/Group/Global | [Notes] |

---

## Dashboard & Visualization Requirements

### Summary Dashboard
- **Purpose:** At-a-glance health overview
- **Widgets:**
  - [Widget 1]: [Chart type, metrics, timeframe]
  - [Widget 2]: [Chart type, metrics, timeframe]
  - [Widget 3]: [Table/list, columns, sorting]

### Detail Views
- **Device Detail:** [What appears when drilling into a specific device]
- **Component Detail:** [What appears at component level]
- **Historical View:** [Trend analysis, time range options]

### Topology / Map View (if applicable)
- [What the visual representation shows]
- [Interactive elements]
- [Status indicators]

---

## Alert & Notification Requirements

### Alert Rules (Default)
| Alert Name | Condition | Severity | Default Action | User Configurable |
|-----------|-----------|----------|---------------|-------------------|
| [Name] | [Trigger condition] | Critical/Warning/Info | [Notification method] | Yes/No |

### Notification Options
- Email, SMS, Webhook (standard OpManager channels)
- Custom escalation rules
- Suppression/maintenance window support

---

## Integration Points

### Within OpManager Plus
| Module | Integration Type | Description |
|--------|-----------------|-------------|
| [Module] | [Type] | [How it connects] |

### External Integrations
| System | Integration | Use Case |
|--------|-------------|----------|
| [System] | [How] | [Why] |

---

## Out of Scope (Explicit)
- [Thing that might seem in scope but is NOT]
- [Thing that was discussed but deferred]
- [Thing that belongs to a different module/team]
```




## Dual output: hidden MD + visible HTML (mandatory)

Every step artifact this skill writes must be dual-format:

1. **Markdown (source of truth, hidden):** `ITOM-PM-Result/[slug]/.steps/<name>.md`
   - Enhancement mode: `ITOM-PM-Result/[slug]-enhancement/.steps/<name>.md`
2. **HTML (human review, visible):** `ITOM-PM-Result/[slug]/steps/<name>.html`
   - Same basename; always under visible `steps/` (never put `.md` here).
3. Generate HTML after markdown is final:
   ```bash
   python "<scripts-dir>/md_to_html.py"      "ITOM-PM-Result/[slug]/.steps/<name>.md"      "ITOM-PM-Result/[slug]/steps/<name>.html"
   ```
   Resolve helper via `**/md_to_html.py` (`scripts/`).
4. On revise, regenerate **both**.
5. Chat summary must cite the **HTML path first** (what reviewers open).
6. **Never delete** `.steps/*.md`, `steps/*.html`, or `Generated/build_documents.py` after PPTX/PDF/DOCX generation.

See `context/pm-operating-system.md` sections 3, 6, and 11–13.


## Quality Gate (before marking complete)

- [ ] Path: `ITOM-PM-Result/[slug]/.steps/4_feature_definition.md`
- [ ] Explicit in-scope vs out-of-scope
- [ ] Persona challenge → capability traceability
- [ ] Screens / settings / integrations concrete enough for Step 5–6
- [ ] Phasing decisive (v1 / later)
- [ ] `STATUS.md` updated

- [ ] HTML twin written under visible `steps/`; markdown under hidden `.steps/`
- [ ] Markdown is hidden under `.steps/`; HTML visible under `steps/`; never delete either or Generated artifacts


## Completion

After writing the file, display a **summary directly in chat**:

---

**Step 4 Complete — Feature Definition Summary:**

> **v1 scope:** [N] must-have capabilities
> **Key capabilities:**
> 1. [Capability 1]
> 2. [Capability 2]
> 3. [Capability 3]
> 4. [Capability 4]
>
> **Screens to build:** [List main screens]
> **Integration points:** [Key modules this connects to]
> **Deferred to v1.1:** [2-3 items pushed out]
>
> Full details in `ITOM-PM-Result/[feature-name]/.steps/4_feature_definition.md`
>
> Reply **'proceed'** to continue to Step 5 (Deliverable Generation), or provide feedback.

---
