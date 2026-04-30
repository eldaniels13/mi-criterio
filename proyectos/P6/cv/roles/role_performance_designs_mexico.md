# Role: IT Infrastructure & Software Development — Performance Designs (Mexico Operations)
**Period:** May 2025 – March 2026 (10 months)
**Location:** Guadalajara, MX (remote collaboration with DeLand, FL, USA)
**Status:** Completed
**Expansion status:** v1.0 — open for future additions

---

## Overview

I was the sole IT and software developer for the Mexico operations of a US-based parachute manufacturing company. During a period of dual-migration (hardware, network interface and enterprise resource planning), I worked independently, developing custom software for the manufacturing floor. I also supported a business systems transition and managed a network infrastructure upgrade.

---

## Track 1: Software Development

### AutoCAD Plugin & Nesting Engine (C# .NET)
- I self-taught C# .NET from near-zero, using Visual Studio 2022 Professional as my primary IDE
- I was responsible for the development of both the front and back end for an open-source nesting engine, and I integrated it with an AutoCAD plugin (netload) to optimise fabric and material cutting layouts used in the manufacturing of parachutes using laser tables.
- My development workflow involved several key stages. Firstly, I received high-level requirements from the Florida team via Microsoft Teams. I then undertook self-directed learning through official documentation and video resources. I also used AI-assisted pattern learning and debugging, and iterative development with progressive code cleanup using VS as the main IDE.
- During my time there, I achieved the functional integration of the plugin within AutoCAD and as standalone app, however, the nesting engine was still under active development when I left, as well as full integration with SQL servers.
- I maintained the codebase with README files and inline documentation. The source code is retained locally on USB storage

### ERP Migration — M2M to Epicor
- I received especial training on Epicor as the company migrated its ERP system from Made2Manage (M2M)
- This was part of a bigger plan to update the business systems at the same time as the infrastructure was being updated

<!-- EXPANSION SLOT: Add specific Epicor modules trained on, training hours, tasks completed -->
<!-- EXPANSION SLOT: Add any data migration tasks or process mapping work if recalled -->

---

## Track 2: IT Infrastructure

### Network Migration — CAT5e to CAT6
- I managed the full CAT5e to CAT6 cabling upgrade across both buildings of the Mexico plant, working alongside third-party contractors
- While the migration phase, the internet was sometimes down for a few hours a week. This was because the system was unstable while it was being updated.
- Once the migration was finished, outages dropped to near-zero. The only remaining failure mode was full external power loss, but compensaded with a self disgn UPS sytem for both sites.

### Internet Continuity — Starlink + UPS Backup System
- I identified the need for a redundant Internet connection independent of the primary ISP
- I designed a backup system using a Starlink antenna paired with few UPS units, ensuring Internet continues working when there is power outages
- Here's how I worked on infrastructure proposals: After the Florida team had given their feedback, the next step would be to work on the final proposal, send it off and get approval, or start the process again. I am happy to tell that the installation was successfully completed.
- The system performed as designed. During full power outages at the plant, Teams communication with the Florida team remained operational via Starlink and UPS

### Access Points & Network Hardware
- I managed hardware upgrades and configuration of wireless access points, migrating to Meraki MR56 units
- I used the Ubiquiti app for client recognition, monitoring and diagnostics
- I performed switch upgrades as new hardware arrived

<!-- EXPANSION SLOT: Add switch models if recalled -->
<!-- EXPANSION SLOT: Add VLAN or segmentation work if applicable -->

### ISP & Firewall Management
- On the job, I gained expirience on ISP-level troubleshooting and firewall configuration basics
- I learned to diagnose connectivity issues at multiple layers: client-side symptoms, DHCP and IP assignment, firewall rule conflicts, and physical cable integrity using Fluke's copper cable tester.

### Troubleshooting Methodology (Self-Developed, Reactive)
My diagnostic sequence for Internet and network outages:
1. Check client-side symptoms on multiple devices (phones, computers, printers) to determine scope
2. Confirm whether the issue was Wi-Fi or Ethernet
3. Inspect physical ISP equipment for status indicators
4. Verify DHCP assignment and IP configuration
5. Check firewall rules for potential blocks
6. Test Ethernet cable integrity using a copper cable testers (pin continuity, length verification and remote location)
7. Use the Ubiquiti app to see what problems there are and manage the network remotely. Also use it to block or restrict certain devices if needed.

> Note: This workflow was developed independently through experience. No formal IT operations methodology was used.

<!-- EXPANSION SLOT: Add any recurring issue patterns or permanent fixes implemented -->

---

## Collaboration & Communication

- I worked mostly on my own, but I'd report to Plant manager in Mexico and work with the IT team in DeLand, Florida, using Microsoft Teams. I had two or three meetings with business ouner for present advaments on the code
- When I first started, the Florida team helped me with complicated technical problems over Teams. After a while, I was able to solve these problems on my own
- Infrastructure proposals and approvals for infrastructure followed a process set via Teams

<!-- EXPANSION SLOT: Add names/titles of Florida contacts if appropriate for references -->

---

## Key Achievements

- Stabilized the Mexico plant network from 2–3 weekly outages to near-zero outages over the first 7 months
- Designed and installed a Starlink + UPS continuity system that kept operations online during full power failures
- Self-taught C# .NET and delivered a functional AutoCAD plugin for manufacturing use — coming from a mechanical engineering and CNC background with no prior professional software development experience
- Managed dual concurrent migrations (CAT5→CAT6 infrastructure, M2M→Epicor ERP) as the sole responsible person on site while working with third-party contractors
- Earned technical credibility and trust from the remote Florida team while working in full autonomy

---

## Tools & Technologies

| Category | Tools |
|---|---|
| Languages | C# (.NET 8) |
| IDE | Visual Studio 2022 Professional |
| CAD | AutoCAD (plugin integration) |
| Network Hardware | Meraki MR56, Ubiquiti switches, CAT6 infrastructure |
| Internet Redundancy | Starlink, UPS |
| ERP | Epicor (training), Made2Manage M2M |
| Communication | Microsoft Teams |
| Diagnostics | Handheld Ethernet cable tester |

<!-- EXPANSION SLOT: Add specific .NET libraries or AutoCAD API namespaces used -->
<!-- EXPANSION SLOT: Add firewall vendor/model if recalled -->

---

## Documentation Status

| Artifact | Status |
|---|---|
| C# source code + READMEs | To Finish and Upload |
| Starlink/UPS proposal documents | ToDo by memory |
| Network migration logs | ToDO by memory |
| Epicor training records | Held by company |
| Teams conversation history | Held by company |

---

## Notes for CV Tailoring

- **For infrastructure/IT roles:** Lead with Track 2. Emphasize network stabilization, Starlink/UPS design, troubleshooting methodology, Meraki/Ubiquiti hardware
- **For software development roles:** Lead with Track 1. Emphasize C# .NET self-teaching, AutoCAD API integration, nesting algorithm development, solo delivery
- **For hybrid/manufacturing tech roles:** Present both tracks equally. Emphasize the manufacturing context (parachute/aerospace), the dual-migration ownership, and the cross-functional autonomy
- **For aerospace/defense roles:** Emphasize the regulated manufacturing environment, hardware upgrade ownership, and infrastructure reliability outcomes

---

*Last updated: April 2026 | Built from voice interview session | v1.0*
*To expand: provide additional recalled details in a new conversation referencing this file*
