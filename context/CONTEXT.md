# ITOM-PM Ubiquitous Language

One canonical term per concept, for every ITOM-PM skill's output. If a term isn't here, don't invent a new one — check `product-context.md` first, then ask.

> **Status:** drafted from `product-context.md` (v0.1.0). The terms under **Flagged for your ruling** below are genuinely contested or inconsistent in the source material — everything else is settled and safe to use as-is.

## Product & Editions

**OpManager Plus / OpManager Nexus**: the unified full-stack observability product this pipeline plans features for. _Avoid_: "OpManager" alone when you mean the full-stack product — "OpManager" (no suffix) is the standalone network+server product; Plus/Nexus is the superset with all add-ons bundled in.

**Edition**: one of the five licensing tiers (Standard, Professional, Enterprise, Nexus Professional, Nexus Enterprise), each unlocking a different feature/scale ceiling. Device-based pricing, not per-metric or per-sensor.

**Add-on**: a capability sold separately for standalone OpManager (NetFlow Analyzer, Network Configuration Manager, Firewall Analyzer, OpUtils, Applications Manager) that comes bundled into Nexus editions instead.

## Architecture

**Central Server**: the single node hosting the web UI, REST API, consolidated reports, and the central database. Aggregates data from all probes in a distributed deployment.

**Probe**: an Enterprise-Edition collector deployed at a site, monitoring up to ~10,000 local devices with its own local database (so it keeps working through a WAN outage). _Avoid_: "Agent" — a Probe is a site-level collector for many devices; it is not the same thing as the ORCA Agent (see Flagged section).

**High Availability (HA)**: automatic failover for the Central Server, available from Enterprise-tier editions up.

## Discovery & Templates

**Discovery Profile**: the configuration for a bulk discovery run — IP range, CSV upload, subnet (CIDR), or Active Directory source.

**Discovery Schedule**: a recurring, automated trigger for a Discovery Profile to run again at a set interval. _Avoid_ confusing with **Rediscovery** (below) — a schedule triggers new discovery; rediscovery refreshes properties on devices already being monitored.

**Rediscovery**: re-reading a monitored device's properties (RAM, disk, interface speed) without removing and re-adding it.

**Device Template**: a built-in or custom definition (sysOID + vendor/type classification + default monitors + default thresholds + polling interval) that gets auto-associated with a device on discovery. Editing a template changes every device already using it.

**System Object ID (sysOID)**: the SNMP identifier OpManager Plus uses to match a discovered device to a Device Template.

**Discovery Rule Engine**: the post-discovery automation layer — matches discovered devices against criteria (DNS name, category, OS, vendor, custom fields) and auto-applies actions (assign a monitor, add to a Business View, apply a notification profile). _Avoid_ shortening to "discovery rules" when you mean the whole engine — a **Discovery Rule** is one configured rule inside the engine.

## Data Collection

**SNMP**: Simple Network Management Protocol — the primary polling method for network devices (routers, switches, firewalls). v1/v2c/v3.

**SNMP Trap**: an asynchronous, device-pushed event notification over SNMP (as opposed to OpManager Plus polling the device).

**WMI**: Windows Management Instrumentation — the polling method for Windows server metrics (CPU, memory, disk, processes, services, event logs).

**ORCA Agent**: the installed-on-endpoint agent for deep server monitoring, which pushes data to OpManager Plus rather than being polled. _Avoid_ conflating with **Probe** (see Flagged section) — different layer, different direction of data flow.

**Custom Monitor**: a monitor built from a raw collection primitive (an SNMP OID from an imported MIB, a WMI query, a script's parsed output, a URL check, a file/folder check) rather than a built-in Device Template monitor.

## Alerting

**Alarm Severity**: one of five levels — Critical, Warning, Attention, Service Down, Clear — each with a fixed color.

**Threshold**: the value that, when crossed by a monitored metric, raises an alarm. A **Static Threshold** is a fixed value with a rearm value; an **Adaptive Threshold** is ML-learned from historical utilization patterns.

**Notification Profile**: the configuration that decides who gets notified, for which devices/alarms, on what schedule, and by which channel (email, SMS, webhook, script, ticket). See Flagged section — this may be the same feature engineering calls "Alarm Profile."

**Alarm Escalation**: a multi-level policy that notifies further people/systems if an alarm isn't acknowledged in time.

**Alarm Suppression**: suppressing dependent-device alarms when their root cause (e.g. an upstream switch) is already down, so one outage doesn't fan out into dozens of alarms.

**Root Cause Analysis (RCA)**: the centralized correlation view across multiple monitors used to find the actual source of a problem, as opposed to its symptoms.

## Dashboards & Visualization

**Business View**: a canvas-based custom topology map representing a logical business unit (department, branch, application group) — hand-built by a user, with device icons and status overlays. _Avoid_ using "view" generically for this — OpManager Plus has several unrelated "*View" features (see Flagged section).

**NOC View**: an auto-rotating, full-screen dashboard meant for a large screen in an operations center.

**Snapshot Page**: the per-device page showing real-time status, its monitors, its alarms, and its graphs — the default place a user lands when they click into one device.

**3D Data Center Floor**: the WebGL-based physical layout visualization of racks and devices.

## Modules (Nexus-bundled add-on capabilities)

**Applications Manager (APM)**: the application performance module — code-level tracing, distributed transaction tracing, Real User Monitoring, Apdex scores.

**NetFlow Analyzer**: the bandwidth/traffic-analysis module, built on flow protocols (NetFlow/sFlow/J-Flow/IPFIX).

**Network Configuration Manager (NCM)**: the config-backup, change-tracking, and compliance-auditing module for network devices.

**OpUtils**: the IP address management (IPAM) and switch-port-mapping module.

**Firewall Analyzer**: the firewall-log module — security/bandwidth/compliance reporting from firewall logs.

## Sources: Sections referenced

Everything above is drawn from `product-context.md` sections 1–9 and 11–12. Section 10 (Competitive Landscape) and Section 14 (Common Enhancement Areas) contain no additional terms needing definition here — they're comparative/planning content, not vocabulary.

---

## Flagged for your ruling

These are genuinely contested, overloaded, or inconsistent in the source material — I'm not picking a side without you.

1. **Probe vs. Agent** — both are "the thing installed to collect data," but a Probe is a site-level collector for up to 10,000 devices (Enterprise Edition, distributed architecture) while the ORCA Agent is installed per-endpoint for deep server monitoring. Should ITOM-PM output ever call the Agent a "probe" informally, or should these stay strictly separate terms with no interchangeable use at all?

2. **OpManager vs. OpManager Plus vs. OpManager Nexus** — Plus is the old name, Nexus is the current rebrand of the same product tier, and plain "OpManager" is a *different*, narrower standalone product. Which term should new PM pipeline output default to when a PM's request doesn't specify — "OpManager Plus" (matches this pipeline's current skill descriptions) or "OpManager Nexus" (the current market name)?

3. **Enterprise vs. Nexus Enterprise vs. "EE"** — "Enterprise" is a standalone-OpManager edition tier; "Nexus Enterprise" is a separate, pricier Nexus edition; and I've seen "EE" used elsewhere in this codebase (`ee-review` skill) as shorthand for the Probe–Central distributed *architecture*, which isn't strictly tied to either edition name. Should the glossary define "EE" as its own architecture-layer term distinct from both edition names, to stop the three from blurring together?

4. **Notification Profile vs. Alarm Profile** — `product-context.md` calls this feature "Notification Profile" throughout, but another skill in `itom-ai-toolkit` (`alarm-profile-criteria`) refers to "Alarm Profile / Alarm Correlation Rule system." I can't tell from this document alone whether these are the same feature under two names (a real naming drift to fix) or two genuinely different features. Which is it, and which name should ITOM-PM skills use?

5. **"Alarm" vs. "Alert"** — the source document itself switches between the two: the alerting system is titled "Alarms & Notifications" (§4.3) and "Alerting & Notification System" (§7), severities are "Alarm Severities," but the enhancement-areas list uses "Alert Correlation" and "Alert deduplication" (§14.4). Should the glossary standardize fully on "Alarm" as the noun (reserving "Alert"/"Alerting" only for compound system names, as I've done above), or are the two meant to be fully interchangeable?

6. **"View" as a generic word** — Business View, NOC View, Rack View, Virtual Topology Map, and 3D View are five distinct features that all happen to use "view" in casual references. Do you want a hard rule that generic "view" is never used unqualified in ITOM-PM output (always the full feature name), or is that overkill for a first pass?
