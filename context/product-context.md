# OpManager Plus (OpManager Nexus) — Product DNA

> **Source:** ManageEngine public documentation, product pages, and help guides.
> **Last updated:** May 2026.
> **PM agents:** Also load [pm-operating-system.md](./pm-operating-system.md) for pipeline paths, Progress.md, quality gates, and resume rules.

---

## 1. What Is It

**OpManager Plus** (rebranded as **OpManager Nexus**) is ManageEngine's unified full-stack observability platform. It combines network monitoring, server monitoring, application performance management, bandwidth analysis, configuration management, IP address management, firewall log management, and storage monitoring into a single on-premises console.

- **Division:** Zoho Corporation → ManageEngine → ITOM (IT Operations Management)
- **Tagline:** "Unified IT operations platform designed to achieve full-stack observability"
- **Target buyers:** NetOps, ITOps, DevOps, SREs, CIOs/CXOs
- **Scale:** 20+ years in market, 15K+ active customers, 190+ countries, 1M+ IT admins
- **Clients:** L'Oréal, NASA, DHL, Siemens, Time Warner Cable, Alcatel-Lucent, Saint-Gobain

### OpManager (standalone) vs OpManager Nexus

| | OpManager | OpManager Nexus (formerly OpManager Plus) |
|---|---|---|
| Focus | Network + Server monitoring | Full-stack observability |
| Add-ons | Sold separately (NetFlow, NCM, Firewall, APM, OpUtils) | All bundled into one product |
| Pricing | From $245 / 25 devices (Standard) | From $1,233 / 50 devices (Professional) |
| APM | Via plug-in | Integrated (Applications Manager) |
| Bandwidth | Via NetFlow Analyzer add-on | Integrated |
| Config mgmt | Via NCM add-on | Integrated |
| IP/Switch port | Via OpUtils add-on | Integrated |
| Firewall logs | Via Firewall Analyzer add-on | Integrated |

---

## 2. Architecture

### 2.1 Deployment Models

- **On-premises** (primary): Windows Server or Linux
- **SaaS/Cloud** (via Site24x7 for cloud-only customers)
- **Hybrid**: On-prem central + cloud probes or mixed

### 2.2 Probe–Central Architecture (Enterprise Edition)

```
┌──────────────────────────────────────────────────────┐
│                   CENTRAL SERVER                     │
│  ┌──────────┐ ┌──────────┐ ┌──────────────────────┐ │
│  │ Web UI   │ │ REST API │ │ Consolidated Reports │ │
│  └──────────┘ └──────────┘ └──────────────────────┘ │
│  ┌─────────────────────────────────────────────────┐ │
│  │           Central Database (PostgreSQL/MSSQL)   │ │
│  └─────────────────────────────────────────────────┘ │
└────────────┬──────────────┬──────────────┬───────────┘
             │              │              │
      ┌──────▼──────┐ ┌────▼────────┐ ┌───▼─────────┐
      │  Probe #1   │ │  Probe #2   │ │  Probe #N   │
      │ (Site A)    │ │ (Site B)    │ │ (Site N)    │
      │ Local DB    │ │ Local DB    │ │ Local DB    │
      │ Polling     │ │ Polling     │ │ Polling     │
      │ Engine      │ │ Engine      │ │ Engine      │
      └──────┬──────┘ └──────┬──────┘ └──────┬──────┘
             │               │               │
        Local devices   Local devices   Local devices
```

- Each **probe** monitors up to ~10,000 devices at its site
- Probes have their own local DB — **100% data integrity** even during WAN outages
- Central server aggregates all probes for unified dashboards, alerts, and reports
- Enterprise Edition scales to **30,000+ devices** or **50,000+ interfaces**
- Supports **High Availability (HA)** with automatic failover

### 2.3 Database

- **PostgreSQL** (bundled, default) or **Microsoft SQL Server** (external)
- Separate databases for device inventory, performance data, events/alarms, reports

### 2.4 Web Server & Client Access

- Embedded web server (Tomcat-based)
- Web UI accessible via browser (no desktop client needed)
- REST API for programmatic access
- Mobile apps: Android, iOS (iPhone + iPad)

---

## 3. Editions & Licensing

| Edition | Starts At | Key Additions |
|---------|----------|---------------|
| **Standard** | $245 / 25 devices | Basic monitoring, discovery, alerting, dashboards |
| **Professional** | $345 / 25 devices | + Agent-based monitoring, virtual server monitoring, hardware monitoring, workflow automation, AIOps, network path analysis, user management, reports |
| **Enterprise** | $4,595 / 250 devices | + Distributed monitoring (Probe–Central), HA, multi-site alerts |
| **Nexus Professional** | $1,233 / 50 devices | All add-ons bundled (APM, NetFlow, NCM, Firewall, OpUtils) |
| **Nexus Enterprise** | $19,995 / 1,000 devices | Nexus Pro + distributed + HA |

- Licensing is **device-based** (per monitored device count)
- 30-day free trial available for all editions

---

## 4. Feature Modules (Detailed)

### 4.1 Network Management

| Feature | Description |
|---------|-------------|
| **Network Performance Monitoring** | 2,000+ performance metrics, dashboards, instant alerts, intelligent reporting |
| **Router Monitoring** | Errors/discards, voltage, temperature, buffer stats |
| **Switch Monitoring** | Port-wise traffic, switch port mapping to connected devices |
| **WAN RTT Monitoring** | Cisco IP SLA-based WAN link availability, latency, performance |
| **VoIP Monitoring** | VoIP call quality across WAN, jitter, MOS scores |
| **Network Mapping** | Automatic L1/L2 topology maps, pinpoint outages |
| **Interface Monitoring** | ~300 interface templates, bandwidth utilization, errors/discards |
| **Wireless Monitoring** | Access points, WiFi strength, wireless traffic |
| **SD-WAN Monitoring** | SD-WAN link health and performance |
| **BGP Monitoring** | BGP session states, route changes |
| **VPN Monitoring** | VPN tunnel status, throughput |
| **Load Balancer Monitoring** | Health of load balancers |

### 4.2 Server Management

| Feature | Description |
|---------|-------------|
| **Physical Server Monitoring** | Windows, Linux, Solaris, Unix — CPU, memory, disk, processes |
| **VMware Monitoring** | Agentless, 70+ VMware performance monitors (ESXi hosts, VMs, datastores) |
| **Hyper-V Monitoring** | WMI-based, 40+ deep metrics for hosts and guests |
| **Citrix Hypervisor Monitoring** | Hosts, VMs, storage repositories |
| **Nutanix HCI Monitoring** | Hyperconverged infrastructure |
| **Process Monitoring** | Monitor processes via SNMP/WMI/CLI — start/stop, CPU/memory per process |
| **Service Monitoring** | Windows NT services, Linux services (systemd/init) |
| **System Health Monitoring** | CPU, memory, disk utilization via SNMP/WMI/CLI |
| **Hardware Monitoring** | Fan speed, temperature, voltage, power supply (via IPMI, vendor APIs) |

### 4.3 Fault & Performance Management

| Feature | Description |
|---------|-------------|
| **Alarms & Notifications** | Email, SMS alerts with severity-based color coding (Critical/Warning/Attention/Service Down/Clear) |
| **Threshold-Based Alerts** | Static thresholds on any monitored metric with rearm values |
| **Adaptive Thresholds** | ML-learned utilization patterns for auto-generated accurate thresholds |
| **Root Cause Analysis (RCA)** | Centralized view to visualize, analyze, correlate multiple monitor performance |
| **Syslog Monitoring** | Rule-based syslog parsing, alert association |
| **SNMP Trap Monitoring** | Receive and process SNMP traps from devices |
| **Event Log Monitoring** | Windows Event Log rule-based monitoring |
| **IT Workflow Automation** | Automate first-level fault troubleshooting and maintenance tasks (script execution, restart services, etc.) |
| **Notification Profiles** | Configurable notification criteria — who, when, how (email/SMS/webhook/run script) per alarm severity and device group |
| **Alarm Escalation** | Multi-level escalation policies |
| **Alarm Suppression** | Suppress dependent device alarms (e.g., if switch is down, don't alert on all connected devices) |

### 4.4 Storage Management

| Feature | Description |
|---------|-------------|
| **Storage Array Monitoring** | Dell EMC, NetApp, HPE, Hitachi — capacity, IOPS, latency |
| **RAID Management** | Controller health, disk array status, rebuild progress |
| **Tape Library Management** | Status parameters, fault detection |
| **Storage Capacity Forecasting** | Trend analysis for future capacity planning |
| **Fabric Switch Management** | SAN fabric switch discovery and alert on state changes |

### 4.5 AIOps

| Feature | Description |
|---------|-------------|
| **Forecast Reports** | Predict resource exhaustion before it happens |
| **Performance Trend Forecasting** | Usage trend analysis, traffic/resource surge prediction |
| **Adaptive Thresholds** | ML-based threshold learning from historical patterns |
| **Anomaly Detection** | Baselining to detect deviations from normal behavior |

### 4.6 Data Center Management

| Feature | Description |
|---------|-------------|
| **3D Data Center Floor** | Replica of physical data center with racks, real-time device status |
| **Rack Views** | Drill from rack to device snapshot page |
| **Systems Management** | Routers, switches, servers, load balancers — unified view |

### 4.7 Network Visualization

| Feature | Description |
|---------|-------------|
| **Layer 2 Maps** | Auto-discovered L2 topology |
| **Business Views** | Custom maps — department/branch/application groupings |
| **Virtual Topology Maps** | VM → Host → Cluster → Datacenter hierarchy |
| **3D Floor & Rack Views** | Data center physical layout visualization |
| **NOC Views / TV Dashboards** | Large-screen dashboards for operations centers |

### 4.8 Application Performance Management (Nexus only)

| Feature | Description |
|---------|-------------|
| **Code-Level Insights** | Application transaction tracing, bottleneck identification |
| **Distributed Transaction Tracing** | End-to-end request tracing across microservices |
| **Real User Monitoring (RUM)** | User journey through web apps, satisfaction metrics |
| **Apdex Scores** | Application Performance Index tracking |
| **Web Transaction Analysis** | Sessions, AJAX calls, JS errors |

### 4.9 Bandwidth & Traffic Analysis (Nexus / NetFlow Analyzer add-on)

| Feature | Description |
|---------|-------------|
| **NetFlow/sFlow/J-Flow/IPFIX** | Flow-based bandwidth analysis |
| **Top Talkers / Applications** | Identify top bandwidth consumers |
| **Traffic Shaping** | QoS and DSCP analysis |
| **Forensics / Historical** | Flow data retention for troubleshooting |

### 4.10 Network Configuration Management (Nexus / NCM add-on)

| Feature | Description |
|---------|-------------|
| **Configuration Backup** | Scheduled config backups for network devices |
| **Change Management** | Real-time config change tracking via syslog |
| **Config Diff / Compare** | Compare two config versions — same device or across devices |
| **Compliance Auditing** | Check configs against policies (SOX, HIPAA, PCI-DSS, etc.) |

### 4.11 IP & Switch Port Management (Nexus / OpUtils add-on)

| Feature | Description |
|---------|-------------|
| **IP Address Management (IPAM)** | Subnet scanning, IP availability, DNS/DHCP correlation |
| **Switch Port Mapping** | Map ports to connected devices, physical location tracking |
| **Rogue Device Detection** | Detect unauthorized devices on the network |

### 4.12 Firewall Log Management (Nexus / Firewall Analyzer add-on)

| Feature | Description |
|---------|-------------|
| **Security Reports** | Threat analysis from firewall logs |
| **Bandwidth Reports** | Bandwidth usage through firewalls |
| **Compliance Reports** | PCI-DSS, ISO 27001, NIST, SANS |
| **VPN Monitoring** | VPN session monitoring from firewall logs |

---

## 5. Discovery & Configuration System

### 5.1 Device Discovery

- **Discovery Profile**: Bulk discovery via IP range, CSV upload, subnet (CIDR v4/v6), or Active Directory
- **Discovery Schedule**: Automated recurring discovery at specified intervals
- **Interface Discovery**: ~300 interface templates for automatic classification; bulk or individual
- **Discovery Reports**: Email reports after each discovery — total found, successfully added, failures
- **Approve/Ignore**: Discovered devices can be approved for monitoring or ignored (persists across rediscovery)
- **Rediscovery**: Update device properties (RAM, HDD, interface speed) without removing/re-adding
- **Speed**: 5x faster engine — discovers 15,000+ interfaces per minute

### 5.2 Device Templates

- **11,000+ built-in templates** — each contains:
  - System Object ID (sysOID)
  - Device type and vendor classification
  - Pre-configured performance monitors
  - Default threshold values
  - Monitoring intervals
- Auto-associated on discovery based on sysOID match
- Custom templates can be created or imported
- Modify thresholds, monitoring intervals, add/remove monitors per template
- Mass changes: Modify a template → changes apply to ALL devices of that type

### 5.3 Discovery Rule Engine

Automates post-discovery configuration based on device criteria:

**Criteria options** (condition matching on discovered device):
- DNS Name, Category, Type, Service Name, OS, Vendor, Custom Fields, etc.
- Multiple criteria with AND/OR logic

**Available actions** (auto-applied when criteria match):
1. Associate a Process Monitor
2. Associate a Service Monitor
3. Associate a Windows NT Service Monitor
4. Associate a File/Folder/Script Monitor
5. Add the device to a Business View
6. Associate a URL Monitor
7. Associate an Event Log Rule
8. Associate MSSQL Monitors
9. Associate Notification Profiles

**Operational controls**: Edit, Copy As, Enable/Disable, Delete, Re-run on selected devices

### 5.4 Credentials Management

Supported credential types for discovery and monitoring:
- **SNMP v1, v2c, v3** (community strings / USM)
- **WMI** (Windows Management Instrumentation)
- **SSH** (Linux/Unix CLI-based monitoring)
- **Telnet**
- **VMware / ESXi** (vSphere API)
- **Hyper-V** (WMI)
- **Citrix / Xen** credentials
- **IPMI** (hardware health out-of-band)

---

## 6. Data Collection Methods

| Protocol/Method | Use Case | Direction | Port(s) |
|----------------|----------|-----------|---------|
| **SNMP v1/v2c/v3** | Network devices — routers, switches, firewalls, printers, UPS | Poll (GET/WALK) | UDP 161 |
| **SNMP Traps** | Asynchronous event notifications from devices | Push (device → OPM) | UDP 162 |
| **WMI** | Windows servers — CPU, memory, disk, processes, services, event logs | Poll (DCOM/RPC) | TCP 135 + dynamic |
| **SSH/CLI** | Linux/Unix servers, network device CLI scraping | Poll (command execution) | TCP 22 |
| **Telnet** | Legacy network device CLI | Poll | TCP 23 |
| **ICMP (Ping)** | Availability, response time, packet loss | Poll | ICMP |
| **TCP Port** | Service availability (HTTP, SMTP, FTP, DNS, etc.) | Poll | Various |
| **Syslog** | Log events from network devices and servers | Push (device → OPM) | UDP 514 |
| **NetFlow / sFlow / J-Flow / IPFIX** | Bandwidth and traffic analysis | Push (device → OPM) | UDP 2055/6343/9996 |
| **VMware API (vSphere)** | ESXi hosts, VMs, datastores — agentless | Poll (HTTPS) | TCP 443 |
| **Hyper-V (WMI)** | Hyper-V hosts and guests | Poll (WMI) | TCP 135 + dynamic |
| **IPMI** | Hardware health (fan, temp, voltage, PSU) | Poll (out-of-band) | UDP 623 |
| **REST API** | Cloud services, custom monitors, third-party device APIs | Poll (HTTPS) | TCP 443 |
| **Cisco IP SLA** | WAN link quality — latency, jitter, MOS | Poll (SNMP to IP SLA responder) | UDP 161 |
| **Cisco ACI API** | ACI fabric, tenants, EPGs | Poll (HTTPS) | TCP 443 |
| **Agent (ORCA)** | Deep server monitoring — installed on endpoint | Push (agent → OPM) | TCP configurable |

### Custom Monitors

- **SNMP custom monitors**: Import vendor MIB → create monitors from OIDs
- **WMI custom monitors**: Create monitors from WMI queries (Win32 classes, custom namespaces)
- **Script monitors**: Execute scripts (PowerShell, Bash, Python) and parse output as metrics
- **URL monitors**: HTTP/HTTPS response time, status code, content matching
- **File/Folder monitors**: File size, age, existence, count
- **Database monitors**: MSSQL monitors built-in; others via script/JDBC

---

## 7. Alerting & Notification System

### 7.1 Alarm Severities

| Severity | Color | Meaning |
|----------|-------|---------|
| Critical | Red | Immediate action required — threshold severely exceeded or device down |
| Warning | Orange | Approaching problem — threshold crossed warning level |
| Attention | Yellow | Minor issue — informational threshold |
| Service Down | Dark Red | Monitored service is unreachable |
| Clear | Green | Previously raised alarm has been resolved |

### 7.2 Notification Channels

- Email (SMTP)
- SMS (via modem, HTTP gateway, or SMPP)
- Webhooks (HTTP POST to any endpoint)
- Run Script (execute local script on alarm trigger)
- Syslog forward (to SIEM)
- SNMP Trap forward
- Integration-specific: Slack, MS Teams, PagerDuty, ServiceNow ticket creation, Jira, ServiceDesk Plus

### 7.3 Notification Profiles

Each profile defines:
- **Which devices**: All, specific category, business view, or custom criteria
- **Which alarms**: Severity level filter
- **When**: Time window, repeat interval, escalation delay
- **To whom**: User, group, or external system
- **How**: Email, SMS, webhook, script, ticket creation

---

## 8. Dashboards & Reporting

### 8.1 Dashboards

- **200+ built-in widgets** (gauges, charts, maps, top-N, alarm summary, etc.)
- **Custom dashboards**: Drag-and-drop widget placement per user
- **NOC view / TV dashboard**: Auto-rotating, full-screen for operations centers
- **Role-based dashboards**: Different views per user role
- **Business Views**: Custom topology maps representing logical business units

### 8.2 Reports

- **100+ built-in reports**: Availability, performance, health, inventory, top-N, interface, alarm history
- **Scheduled reports**: Auto-email PDF/CSV at configurable intervals
- **Forecast reports**: ML-based future resource utilization prediction
- **Custom reports**: Ad-hoc queries on any collected metric
- **Compliance reports** (via NCM/Firewall add-ons)
- **SLA reports**: Availability SLA compliance tracking

---

## 9. Integrations

### 9.1 ManageEngine Ecosystem

| Product | Integration Type |
|---------|-----------------|
| **ServiceDesk Plus** | Auto-create tickets from alarms |
| **ServiceDesk Plus Cloud** | Cloud-based ticket creation |
| **ServiceDesk Plus MSP** | Multi-client ticket logging |
| **Applications Manager** | APM plug-in for OpManager |
| **NetFlow Analyzer** | Bandwidth/traffic analysis add-on |
| **Network Configuration Manager** | Config backup, change management |
| **Firewall Analyzer** | Firewall log management |
| **OpUtils** | IP address/switch port management |
| **Analytics Plus** | AI-powered analytics and dashboards |
| **Log360** | Log management, SIEM, compliance |
| **PAM360** | Privileged access management for shared credentials |
| **AlarmsOne** | Centralized alert management |

### 9.2 Third-Party Integrations

| Category | Products |
|----------|----------|
| **ITSM / Help Desk** | ServiceNow, Jira Service Management (On-Prem + Cloud), Freshdesk |
| **Collaboration** | Microsoft Teams, Slack |
| **Incident Management** | PagerDuty |
| **SIEM** | Splunk, generic SIEM via UDP/Syslog |
| **Automation** | Ansible |
| **Visualization** | Grafana |
| **AI** | OpenAI (alarm summarization, custom script generation) |
| **Custom** | Webhooks, REST API |

---

## 10. Competitive Landscape

### Direct Competitors

| Competitor | Strengths | Weaknesses vs OpManager |
|-----------|-----------|------------------------|
| **SolarWinds NPM/SAM** | Deep network features, large community | Higher cost, complex pricing (per-element), Orion platform overhead |
| **PRTG Network Monitor** | Easy setup, sensor-based model, free tier | Limited at scale, no built-in config/compliance management |
| **Datadog** | Cloud-native, APM+infra+logs, modern UX | SaaS-only, expensive at scale, no on-prem option |
| **Dynatrace** | AI-driven, full-stack auto-instrumentation | Premium pricing, cloud-first (limited on-prem) |
| **Zabbix** | Open-source, free, highly customizable | Steep learning curve, no vendor support, complex setup |
| **Nagios** | Open-source, massive plugin ecosystem | Dated UI, manual configuration, limited out-of-box |
| **LogicMonitor** | SaaS-based, auto-discovery, good scale | No on-prem, higher cost, limited config management |
| **Auvik** | MSP-focused, L2/L3 auto-mapping | SMB only, no APM, limited enterprise features |
| **Checkmk** | Open-source core, good agent | Limited ecosystem, fewer integrations |
| **New Relic** | Full-stack observability, generous free tier | SaaS-only, consumption pricing unpredictable |
| **Broadcom (CA/DX NetOps)** | Enterprise-grade, carrier-class scale | Very expensive, complex, legacy acquisition |

### OpManager Differentiators

1. **All-in-one on-prem**: Network + Server + APM + Bandwidth + Config + Firewall + IPAM in one product
2. **Price advantage**: ~40% cheaper than buying OpManager + all add-ons separately
3. **11,000+ device templates**: Fastest time-to-monitoring for diverse environments
4. **Probe-Central architecture**: True distributed monitoring with local DB resilience
5. **Low learning curve**: UI praised for simplicity vs. SolarWinds/Zabbix complexity
6. **No per-metric/per-sensor pricing**: Device-based flat pricing, predictable costs

---

## 11. User Personas

| Persona | Role | Uses OpManager For |
|---------|------|--------------------|
| **Network Admin** | Day-to-day network operations | Device health, interface bandwidth, alarm triage, topology maps |
| **System Admin** | Server and VM management | Server CPU/memory/disk, process monitoring, patching windows |
| **NOC Operator** | 24x7 monitoring | NOC dashboards, alarm acknowledgment, escalation |
| **Network Engineer** | Design and troubleshoot | Network path analysis, L2 maps, config comparison, WAN monitoring |
| **IT Manager** | Team oversight, reporting | SLA reports, capacity planning, executive dashboards |
| **CISO / Security** | Compliance and threat visibility | Firewall logs, config compliance, syslog analysis |
| **DevOps / SRE** | Application reliability | APM integration, automated remediation workflows |
| **MSP Technician** | Multi-client management | Per-client dashboards, multi-probe monitoring |

---

## 12. UI Patterns & Conventions

Understanding OpManager's existing UI patterns helps when designing new features:

- **Snapshot Page**: Every device has a snapshot page showing real-time status, monitors, alarms, graphs
- **Tabbed navigation**: Top-level tabs = Home, Inventory, Maps, Alarms, Reports, Settings
- **Inventory lists**: Filterable/sortable tables with columns for status, device name, type, IP, severity
- **Dashboard widgets**: Cards with title + metric value + sparkline graph, drag-and-drop layout
- **Settings hierarchy**: Settings → Discovery, Monitoring, Notifications, Workflow, System, etc.
- **Alarm colors**: Red/Orange/Yellow/Green severity indicator icons and row highlighting
- **Right-click context menus**: On devices in maps for quick actions (ping, trace, snapshot, unmanage)
- **Graphs**: Time-series line charts with zoom (1h/12h/24h/7d/30d range selector)
- **Business Views**: Canvas-based custom map editor with device icons + status overlays
- **3D Views**: WebGL-based data center floor and rack visualization

---

## 13. Technical Internals (for Feature Design)

### 13.1 Monitoring Pipeline

```
Discovery → Device Template Match → Monitors Assigned → Polling Engine Collects →
Data Stored → Thresholds Evaluated → Alarms Raised → Notifications Triggered → Dashboard Updated
```

### 13.2 Polling Intervals

- **Default device poll**: 5 minutes (configurable per device or template: 1 min to 24 hours)
- **Availability (ICMP)**: 3–5 minutes default
- **Interface bandwidth**: 5 minutes default
- **Deep monitors (VMware, SNMP Walk)**: 5–15 minutes
- **Syslog/Trap**: Real-time (event-driven, not polled)

### 13.3 Data Retention

- **Real-time data**: Kept at poll interval granularity for configurable period
- **Hourly averages**: Long-term storage for trend analysis
- **Daily averages**: Multi-year retention
- **Configurable**: Per data type (raw, hourly, daily retention periods)

### 13.4 Supported Device Categories

OpManager classifies discovered devices into categories:
- Routers, Switches, Firewalls, Load Balancers, Wireless Controllers, Access Points
- Windows Servers, Linux Servers, Solaris, AIX, HP-UX, FreeBSD
- ESXi Hosts, vCenter, Hyper-V Hosts, Citrix Hypervisors, Nutanix
- Printers, UPS, Desktops/Workstations
- Storage Arrays, Fiber Channel Switches, Tape Libraries, NAS
- Cisco UCS, Cisco ACI, Cisco Meraki
- Unknown (unclassified devices)

### 13.5 Vendor-Specific Monitoring

| Vendor | Special Support |
|--------|----------------|
| **Cisco** | ACI fabric, Meraki cloud, UCS compute, IP SLA, switch stacks |
| **VMware** | vCenter/ESXi agentless via vSphere API |
| **Microsoft** | Hyper-V via WMI, Windows services/processes/event logs |
| **Fortinet** | FortiGate performance monitoring |
| **Juniper** | Juniper network monitoring |
| **HP/HPE** | Server hardware (iLO), storage arrays |
| **Dell EMC** | Storage arrays, PowerEdge servers (iDRAC) |
| **NetApp** | Storage ONTAP monitoring |
| **IBM** | Server and storage monitoring |

---

## 14. Common Enhancement Areas

These are the areas where feature enhancements (even minor ones) are commonly needed:

### 14.1 Discovery Rules
- Adding new criteria types (e.g., match by custom field, location, subnet)
- New action types (e.g., auto-assign to device group, set maintenance window, apply custom polling interval)
- Bulk rule import/export
- Rule priority/ordering

### 14.2 Device Templates
- New vendor device support (adding sysOIDs and default monitors)
- New metrics for existing templates
- Template inheritance / override hierarchy
- Community-contributed template marketplace

### 14.3 Threshold Configuration
- Per-device threshold overrides without cloning the whole template
- Time-based thresholds (different thresholds for business hours vs off-hours)
- Composite thresholds (alert when CPU > 90% AND memory > 85%)
- Baseline deviation thresholds (alert when metric deviates >2σ from rolling average)

### 14.4 Alerting & Notifications
- Alert correlation (group related alarms into incidents)
- Alert deduplication (suppress repeat alarms within time window)
- Planned maintenance windows (suppress alarms during scheduled work)
- Custom severity levels beyond the 4 built-in ones
- Dynamic escalation based on alarm age or business impact

### 14.5 Dashboards & Visualization
- Custom widget types (embed external URLs, iFrames, custom charts)
- Dashboard templates (shareable dashboard layouts)
- Enhanced topology maps (auto-refresh, animated traffic flow)
- Dark mode / theme customization

### 14.6 Reporting
- Report builder (drag-and-drop custom report creation)
- Cross-module reports (network + server + APM in one report)
- Trend comparison reports (this month vs last month)
- Executive summary auto-generation

### 14.7 Automation & Workflows
- Multi-step remediation workflows (if step 1 fails, try step 2)
- Approval-gated automations (require human approval before executing)
- Integration with CI/CD pipelines
- Runbook automation library

### 14.8 Scale & Performance
- Streaming telemetry (gRPC/gNMI) for modern network devices
- Container/Kubernetes monitoring
- Cloud provider monitoring (AWS, Azure, GCP)
- Edge computing / IoT device monitoring

---

## 15. How to Use This Context

When working on a **new feature**, reference:
- Section 4 (Feature Modules) — understand what exists to avoid duplication
- Section 6 (Data Collection) — decide which protocol fits the new data source
- Section 5 (Discovery & Templates) — understand how devices get onboarded and monitors assigned
- Section 12 (UI Patterns) — maintain consistency with existing product UX
- Section 10 (Competitors) — see what others do and where OpManager can differentiate

When working on an **existing feature enhancement**, reference:
- Section 14 (Common Enhancement Areas) — find your enhancement category
- Section 5.3 (Discovery Rule Engine) — if adding new rules, conditions, or actions
- Section 5.2 (Device Templates) — if adding new monitors, thresholds, or vendor support
- Section 7 (Alerting) — if modifying notification behavior, severities, or escalation
- Section 13 (Technical Internals) — understand polling, data retention, and monitoring pipeline constraints
