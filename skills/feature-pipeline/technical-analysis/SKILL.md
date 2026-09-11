---
name: technical-analysis
description: "Step 3 of PM Feature Pipeline: Define the clearest, most opinionated technical implementation path for OpManager Plus. Covers data collection method, metrics, architecture, alerting, and scalability."
---

# Step 3 — Technical Analysis

## Purpose

Define the single best technical implementation path for this feature in OpManager Plus. Be decisive. Recommend ONE primary approach with clear reasoning.

This document must be **engineer-usable**: after reading it, an OpManager developer should know *how* to collect data, *which* OIDs/APIs/paths matter, *what* to store, and *how* to alert — without another research spike for the basics.

## Input

Read:
- `[feature-name]/.steps/1_brainstorm.md`
- `[feature-name]/.steps/2_competitive_analysis.md`
- [context/product-context.md](../../../context/product-context.md)
- Relevant workspace context MDs for the domain (SNMP, REST framework, EE, etc.)

**CRITICAL:** Keep persona challenges from Step 1 front and center. Every technical choice must answer: **does this solve the persona pain in time?**

## Process

### 1. Deep-research ALL viable data collection methods

Do thorough web + context research. For **each** applicable method below, fill the evaluation table (mark N/A only with a one-line why):

| Method | Candidates |
|--------|------------|
| SNMP v1/v2c/v3 | MIBs, OIDs, tables |
| REST / HTTP API | Vendor controllers, cloud APIs |
| gRPC / gNMI / streaming telemetry | Model-driven paths |
| CLI (SSH/Telnet) | Show/display commands |
| Flow (NetFlow/IPFIX/sFlow) | When traffic analytics matter |
| Traps / Syslog / Webhooks | Event-driven |
| Agent / eBPF / packet | When host or packet path is required |
| Other | Redfish, IPMI, proprietary SDK, etc. |

**Score each on:** data richness, reliability, enterprise scale, vendor stability, OpManager engine fit, customer setup pain, security.

**Pick ONE primary.** Fallbacks get a short note — but if a fallback is commonly needed (e.g. SNMP when API license missing), document its contract too at medium depth.

### 2. Collection contract (MANDATORY depth)

For the **primary** method (and close runner-up if customers will split), produce a concrete inventory:

#### If SNMP
- MIB module names (and vendor enterprise IDs when known)
- **OID table** with at least the metrics you recommend:
  | Metric / object | OID (numeric) | MIB object name | Type | Table/scalar | Index notes | Verified? |
- Walk/GETBULK strategy, instance mapping, 32 vs 64-bit counters
- Trap OIDs if eventing is in scope
- Version/auth notes (v3 USM, context)

#### If REST/API
- Base URL pattern, auth (token/OAuth/basic/key), TLS requirements
- **Endpoint inventory:**
  | Metric / resource | Method | Path | Key JSON/XML fields | Pagination | Rate limit notes | Verified? |
- Example response field → metric mapping
- Pagination, filtering, cursor, RBAC scopes
- API versioning / deprecation risk

#### If telemetry / gNMI / gRPC
- Dial-in vs dial-out, encoding (JSON/IETF, proto)
- Sensor/path list mapped to metrics
- Subscription mode (sample/on-change), intervals

#### If CLI
- Exact commands, expected columns, parse fragility, enable-mode needs

#### If flow / trap / syslog
- Template IEs or message patterns, exporters, volume assumptions

**Verified vs Needs lab confirmation:** never invent OIDs/endpoints. If research is incomplete, mark **Needs lab confirmation** and still provide the best-known candidate with source link.

### 3. Complete metrics list

Every metric: definition, why it matters, problem signal/threshold, frequency, collection source ref (OID/endpoint/path).

### 4. Integration architecture

Discovery, polling path, storage, processing, alerting, UI patterns, EE/probe notes.

### 5. Scale and risk

1000+ instances, poller load, DB growth, vendor API limits, licensing.

## Report rebuild (mandatory)

Write markdown to `.steps/<name>.md` (hidden), then rebuild `analysis.html` and, if this step produced a diagram, render it and reference it first with a `<!-- diagram: architecture.html -->` marker. **Full procedure, exact paths, and the rebuild command are in `context/pm-operating-system.md` §§3, 6, 11a — already loaded as mandatory context for every run, so it is not repeated here.** Never delete `.steps/*.md`, `analysis.html`, or `.steps/build_docx.py`.

## Output Format

```markdown
# Technical Analysis: [Feature Name]

## Technical Summary
[5–8 sentences a non-specialist developer can follow. What we monitor, how we collect, why this method won.]

## Recommended Data Collection Method

### Primary: [Method Name]
**Why this wins:**
- …
- …

**How it works:**
[Clear technical explanation]

**Prerequisites:**
- Device-side enablement
- Credentials / RBAC
- Network ports / paths
- Licenses

### Method comparison matrix
| Method | Richness | Scale | Setup pain | OpManager fit | Verdict |
|--------|----------|-------|------------|---------------|---------|
| … | H/M/L | … | … | … | Primary / Fallback / Reject (why) |

### Fallback
> When primary is unavailable: [method]. Use when: [conditions]. Tradeoff: …

---

## Collection contract — [Primary method]

### Inventory (OIDs / APIs / paths)
[Use the appropriate table(s) from Process §2 — must be populated with real researched values]

### Field → metric mapping
| Source field / OID | Internal metric name | Transform | Notes |
|--------------------|----------------------|-----------|-------|

### Polling / subscription design
- Interval defaults and overrides
- Bulk strategy
- Error / retry / timeout
- Partial failure behavior

### Sources for this contract
- [Title](url) — …

---

## Key Metrics & Data Points

### Category: [Name]
| # | Metric | Definition | Why it matters | Problem signal | Freq | Source (OID/API/path) |
|---|--------|------------|----------------|----------------|------|------------------------|
| 1 | | | | | | |

**Total metrics:** N across M categories

---

## Integration Architecture

### Data flow
```
Device → Collection → Normalize → Store → Threshold → UI / Notify
```
(Mermaid or ASCII; include EE probe hop if relevant)

### Discovery mechanism
### Polling configuration
### Data storage & retention
### Correlation with existing OpManager data

---

## Alerting & Threshold Logic

### Critical / Warning tables
### Adaptive threshold candidates
### Dedup / flap / clear behavior

---

## Scalability Considerations

| Scale factor | Impact | Mitigation |
|--------------|--------|------------|
| | | |

**Recommended limits:** devices/probe, poller cost estimate, DB growth.

---

## Dependencies & Risks

| Risk | Prob | Impact | Mitigation |
|------|------|--------|------------|
| | | | |

---

## Persona Challenge Resolution

| Persona challenge | How architecture solves it | Key technical decision |
|-------------------|----------------------------|------------------------|
| | | |

---

## Implementation Complexity Estimate

- Discovery / Polling / Processing / UI / Alerting / Overall

## Open engineering questions
1. …
2. …

## Sources
- [Title](URL) — used for …
```

## Quality Gate (before marking complete)

- [ ] `.steps/3_technical_analysis.md` written, `analysis.html` rebuilt
- [ ] All viable methods evaluated; one primary chosen
- [ ] **Deep collection contract** with concrete OIDs and/or API endpoints/paths (not hand-wavy)
- [ ] Uncertain items labeled Needs lab confirmation + source
- [ ] Metrics complete with source column
- [ ] Scale, EE/probe, security, licensing covered when relevant
- [ ] Persona challenges addressed
- [ ] Sources section present
- [ ] Progress.md updated
- [ ] No implementation source code dumps

## Completion

> **Step 3 Complete — Technical Analysis**
>
> **Primary collection:** [method]
> **Why:** [one sentence]
> **Contract depth:** [N OIDs / N endpoints / paths documented]
> **Metrics:** [N] in [M] categories
> **Source (MD):** `[feature-name]/.steps/3_technical_analysis.md`
>
> Continuing immediately to Step 4 — Feature Definition.
