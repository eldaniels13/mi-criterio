# role_encoretools_cnc_programmer.md
**Version:** 1.0
**Status:** COMPLETE (voice-mode extraction, recommendation letter verified)
**Last updated:** Abr 2026
**Source:** Voice extraction session + recommendation letter PDF (13 mayo 2025)

---

## ROLE IDENTITY

- **Title (official):** Programador CNC
- **Title (ATS-ready):** CNC Programmer & Operator (Full Lifecycle)
- **Worker name (per letter):** José Daniel García Castro
- **Company:** EncoreTools — *Repair Prototyping Manufacturing*
- **Location:** Zapopan, Jalisco, México (area of Mariano Otero & Periférico)
- **Dates:** Mid-February 2025 → May 2025 (~3 months)
- **Employment type:** Formal full-time, 48 hrs/week (08:00–18:00 with 1 hr lunch)
- **Reporting line:**
  - Direct: Shop engineer (~40s, ran the workshop, client-facing, conducted interview) — **name: EXPANSION_SLOT**
  - Indirect: José Luis García de la Torre — General Manager (signed recommendation)

---

## COMPANY CONTEXT

EncoreTools is a **job shop** in Zapopan serving industrial clients (automotive, biomedical adjacent, general manufacturing). Capabilities on the floor included:

- CNC milling (Haas + Fanuc)
- Laser cutting (metal sheets — aluminum, steel with varying carbon content)
- Sand blasting (surface detailing)
- Paint/finish detailing
- DXF file conversion support

Client example documented: **Flex** (Guadalajara) — long-run automotive production of CNC-machined fixtures used in their electrical production line (~3,000 parts/year scope).

---

## HIRING CONTEXT

- **Source:** Recruited via LinkedIn / Indeed contact (employer called phone number listed on profile)
- **Process:** Friday document delivery → interview → Monday start
- **Replaced:** Previous senior operator (top-notch local talent, dismissed due to alcoholism issue) — created the vacancy
- **Exit:** Performance Designs recruited him while still at EncoreTools; ~1 week / 1.5 week handover; left on good terms, ahead of schedule on projects

---

## WHAT HE ACTUALLY DID (full lifecycle ownership)

Daily ownership of **the entire CNC process** — not just operator duties:

1. **Read engineering drawings** with GD&T (Geometric Dimensioning & Tolerancing) specifications, dimensional codes, multi-view plans, material callouts, ISO standards
2. **3D CAD modeling** in **SolidWorks** from 2D manufacturing drawings
3. **CAM programming** using **SolidWorks CAM** — generated full G-code (toolpaths, speeds, feeds, RPM, layering strategies per feature: contour vs. pocket vs. thread vs. face)
4. **Machine setup:** tool loading, diameter verification, tool change operations, work offset zeroing, fixturing
5. **Test runs & automation validation** before committing to production
6. **Production execution** on the machine (operator phase)
7. **Weekly production reporting** to shop engineer (parts/week targets)
8. **Machine care:** wrote custom G-code files for:
   - Daily warm-up routines (lubrication cycles, spindle conditioning)
   - Cleanup routines using coolant system
   - Maintenance cycles
9. **Ad-hoc DXF conversion support** for coworkers (informal, not formal scope)
10. **Emergency response:** rapid setup changes, fixture adaptation, pause/resume long runs

---

## MACHINES

| Machine | Role | Notes |
|---|---|---|
| **Haas** (model TBD) | Primary during learning phase | Newer, more safety interlocks and overload protections — safer for learning |
| **Fanuc** (model TBD) | Adopted during final weeks | Older, less protected, higher damage risk if misused — reserved for experienced operators. Ran long-term Flex automotive fixture production. He transitioned to it after earning trust. |

**Progression:** Starting on Haas → mastering offsets, tool measurement, feed/speed control, collision avoidance → earning Fanuc access → beginning Flex long-run production just before departure.

Acknowledged minor tool breakages during learning (1–2 incidents, tool-level only, no machine damage).

---

## MATERIALS

- Aluminum (primary)
- FeC / Acero — steel in various carbon concentrations
- Nylon (plastic, limited use)

---

## SOFTWARE / TECHNICAL STACK

- **SolidWorks** (CAD — 3D modeling from drawings)
- **SolidWorks CAM** (CAM — G-code generation)
- **G-code** (hand-written for maintenance routines, edited generated code)
- **M-code** (machine-level commands, referenced from manuals)
- **DXF** (file format handling, conversion support)

**Reference practice:** Kept machine manuals at workstation for feeds/speeds lookup per material, G/M-code verification.

---

## ACHIEVEMENTS (STAR-format, recruiter-ready)

### 1. Full-lifecycle CNC ownership after senior operator departure
- **S/T:** Previous senior operator dismissed; shop needed CNC programmer + operator to maintain client commitments
- **A:** Took ownership of full workflow (drawing → CAD → CAM → setup → production), combining university SolidWorks training with prior operator experience
- **R:** Sustained production; delivered projects ahead of schedule in final weeks; earned access to second (more sensitive) Fanuc machine for long-run automotive production

### 2. Multi-setup fixturing for oversized carousel tool-holder part
- **S/T:** Part was flat (~1/4" thick) but ~1–2 ft long/wide — exceeded machine envelope for single-setup machining, and held high tolerance requirements
- **A:** Designed a removable/repositionable fixture allowing a two-pass strategy: machine half, unclamp + rotate symmetric part on fixture, re-clamp, machine other half — all while preserving tolerance across setups
- **R:** Part delivered to tolerance; technique became reusable approach for oversized symmetric components

### 3. Internal thread milling optimization
- **S/T:** Internal threads on ~1"-thick part — initial attempts broke the thread-mill tool due to excessive feed rate
- **A:** Systematically characterized feed/speed parameters per thread diameter and material; built personal reference for future jobs
- **R:** Eliminated tool breakage; process repeatable across thread sizes

### 4. Surface-finish optimization via high-RPM / low-feed contouring
- **S/T:** Contour detailing required edge quality that off-the-shelf parameters didn't achieve
- **A:** Applied high-RPM + low-feed strategy for finishing passes on contours
- **R:** Improved edge quality / surface finish on delivered parts

### 5. Custom maintenance G-code scripts
- **S/T:** No standardized daily routine for machine warm-up, lubrication, or cleanup
- **A:** Wrote personal G-code files (.txt with G/M codes) for daily warm-up, lubrication cycling, and coolant-system cleanup
- **R:** Standardized start-of-day and end-of-day routines; improved machine readiness and housekeeping

### 6. Emergency-response production pivots
- **S/T:** Shop occasionally needed urgent small runs (custom adapters, one-off parts) mid-production
- **A:** Paused long-run jobs, rapidly reconfigured setup + fixturing + program, delivered urgent part, restored prior setup
- **R:** Shop treated him as an integrated, responsive operator rather than just a CNC user

---

## RECOMMENDATION LETTER (verified)

**Document on file:** PDF, EncoreTools letterhead, Zapopan Jalisco 13 mayo 2025
**Signed by:** José Luis García de la Torre, Gerente General

**Key attributed qualities (paraphrased for CV use):**
- Outstanding principles and values
- Committed, responsible, faithful in task completion
- Intachable conduct
- Consistently demonstrated concern for improvement, training, and updating knowledge
- Explicit recommendation for future employers

**Usage note:** The letter is strong but generic (no specific project metrics). For international applications, pair it with the technical achievements above rather than relying on the letter alone.

---

## SOFT SKILLS / PROFESSIONAL BEHAVIOR (demonstrated)

- **Autonomous operator:** Sole user of his CNC — full responsibility for production, quality, machine care, safety
- **Safety progression:** Developed proper PPE discipline (gloves, goggles, tool-handling technique) over time
- **Teamwork:** Reciprocal support with shop floor (forklift assistance, material loading, cross-help on DXF conversions)
- **Referral activity:** Brought in a university friend for interview (not hired — experience gap) — kept relationship open with shop post-departure
- **Learning mindset:** Explicitly praised in recommendation letter; demonstrated by studying manuals, optimizing processes, earning Fanuc access

---

## INTERVIEW DEFENSIBILITY — 2-MINUTE VERBAL TEST

If asked *"Walk me through what you did at EncoreTools"* in English:

> At EncoreTools I was the CNC programmer and operator, owning the full pipeline. I read GD&T manufacturing drawings, built the 3D model in SolidWorks, generated the G-code in SolidWorks CAM, and then set up and ran the machine myself — both a Haas and an older Fanuc. I programmed aluminum, steel, and nylon parts, including oversized components that required multi-setup fixturing to hold tolerance, and I wrote my own G-code scripts for daily warm-up and cleanup. I earned access to the second machine as I proved I could handle it without damaging tools. I left after about three months because I was recruited as a C# developer at Performance Designs — with a signed recommendation from the general manager.

**Yes, defensible.** Every claim maps to specific technical actions and can be elaborated.

---

## SKILL TAGS (for CV / LinkedIn / Indeed)

**Machines:** Haas CNC Milling, Fanuc CNC Milling, Laser Cutting (adjacent), Sand Blaster (adjacent)
**Materials:** Aluminum, Steel (FeC, multiple carbon grades), Nylon
**Processes:** CAD → CAM → G-code, Multi-setup fixturing, Internal thread milling, Contour finishing, Machine setup & offsets, Work zeroing, Daily maintenance routines
**Software:** SolidWorks, SolidWorks CAM, G-code/M-code (read & write), DXF
**Standards:** GD&T (ISO), engineering drawing interpretation
**Soft:** Autonomous ownership, emergency response, production scheduling, peer collaboration

---

## EXPANSION SLOTS (to fill in next session or from records)

- [ ] Salary (weekly/monthly at EncoreTools) — not asked in voice session
- [ ] Shop engineer name (direct supervisor)
- [ ] Exact Haas model number
- [ ] Exact Fanuc model number
- [ ] Flex client project: full scope, part name/function, tolerance specs
- [ ] Other client companies served by the job shop
- [ ] Production metrics (parts/week target, actual output, scrap rate if any)
- [ ] Specific dimensional tolerances achieved on carousel part
- [ ] Thread specifications mastered (M-series, imperial, sizes)
- [ ] University friend referral — name, whether this affected professional network
- [ ] Exact end date in May 2025 (letter dated May 13 — likely near this date)

---

## FILE/EVIDENCE INVENTORY

| Item | Status |
|---|---|
| Recommendation letter PDF | ✅ Verified (13 mayo 2025, Gerente General signature) |
| SolidWorks CAD files | ❌ Lost during Linux migration |
| G-code files (custom warmup, cleanup) | ❌ Lost during Linux migration |
| Part photos/video | ❌ Not captured |
| LinkedIn connection with supervisor/GM | ❓ EXPANSION_SLOT — worth attempting |

**Recovery suggestion:** Reach out to José Luis García de la Torre on LinkedIn to re-establish connection (low cost, keeps reference alive for international applications).

---

## CV-READY BULLETS (drop-in)

For **CV_2025_Manufactura** and **CV_2025_Programacion** (EncoreTools bridges both):

> **Programador CNC — EncoreTools, Zapopan (feb–may 2025)**
> - Programación integral CNC (CAD → CAM → setup → producción) en SolidWorks/SolidWorks CAM sobre máquinas Haas y Fanuc; materiales aluminio, acero (FeC) y nylon.
> - Interpretación de planos con GD&T (ISO) y traducción a modelado 3D y código G propio.
> - Solución de fixturing multi-setup para pieza de porta-herramientas tipo carrusel, respetando tolerancia entre amarres.
> - Optimización de roscado interno por fresa y acabado de contorno (alta RPM / bajo avance).
> - Desarrollo de rutinas propias en código G para warm-up, lubricación y limpieza automatizada.
> - Carta de recomendación firmada por Gerente General.

---

*End of file. Version 1.0.*
