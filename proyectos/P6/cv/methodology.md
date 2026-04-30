# CV Role Documentation Methodology
**Purpose:** Framework for extracting, structuring, and maintaining master role documentation for adaptive CV tailoring
**Author:** eldaniels
**Version:** v1.0 — April 2026

---

## The Core Idea

A single **master role file** captures everything true and defensible about one job. From that file, tailored CV versions are assembled depending on the target role. Nothing gets invented — everything in any CV version can be traced back to a master file.

This means:
- author can defend every line in an interview
- author can update one file and all variants stay consistent
- author can hand a master file to AI in any future session and continue building

---

## File Structure

```
mi-criterio/proyectos/P6
└── cv/
    ├── roles/
    │   ├── INDEX.md                            ← role tracker, priority, session log
    │   ├── role_encoretools_cnc_programmer.md  ← ✅ v1.0 COMPLETE
    │   ├── role_performance_designs_mexico.md  ← ✅ v1.0 COMPLETE
    │   ├── role_tdi_biomedical.md              ← ✅ v1.0 COMPLETE
    │   ├── role_moldtech_thermoforming.md      ← v0.3 skeleton
    │   ├── role_pap_iteso_entreamigos.md       ← ✅ v1.0 COMPLETE
    │   ├── role_mechanical_automotive_2021.md  ← v0.1 minimal
    │   └── voice_extraction_cnc_manufacturing.md ← archived template
    ├── templates/
    │   ├── cv_infrastructure_template.md        ← tailored CV: infrastructure track
    │   ├── cv_software_template.md              ← tailored CV: software dev track
    │   └── cv_hybrid_template.md               ← tailored CV: hybrid/manufacturing
    ├── companies/
    │   ├── _research_template.md               ← reusable research methodology (v1.0)
    │   ├── [company]_profile.md                ← one file per company: research + profile
    │   ├── continental_energy_efficiency_engineer.md  ← done (REF95136I)
    │   ├── siemens_energy_profile.md           ← in progress (research Part 1 + profile Part 2)
    │   └── bosch_profile.md                    ← empty (research Part 1 + profile Part 2)
    ├── skills_master.md                         ← global skills inventory
    ├── education_master.md                      ← education and certifications
    ├── PerfilCVs_Descripciones.md              ← 4 bilingual profile summaries (ATS-ready)
    └── methodology.md                           ← this file

**Workflow per new company:**
1. Copy `_research_template.md` → `[company]_research.md` — fill via browser session
2. Copy profile template → `[company]_profile.md` — fill via voice session
3. Pick the right CV template from `templates/` — tailor for the vacancy
4. Export PDF → upload to company portal
```

---

## How a Role Session Works

### Step 1 — Open with context
At the start of a new role extraction session, tell to AI:
> "I want to document a past job for my master CV. I'll answer questions. Build the role file using the methodology in `methodology.md`."

Attach any existing role file if expanding a previous session.

### Step 2 — Claude asks structured questions
The interview follows this sequence:

1. **Timeline** — Start date, end date, duration
2. **Company context** — Industry, location, team structure, who you reported to
3. **Role title** — What you were called vs. what you actually did
4. **Two or three main tracks** — Group responsibilities into 2–4 logical clusters
5. **Daily workflow** — What a typical day looked like; what triggered reactive work
6. **Technical specifics** — Tools, languages, hardware, vendors, versions
7. **Key achievements** — What changed because you were there
8. **Collaboration** — Who you worked with, how, how often
9. **Documentation artifacts** — What evidence exists (code, files, photos, emails)
10. **Expansion slots** — What's uncertain or partially remembered (mark for later)

### Step 3 — Recap before writing
Before generating the file, Claude reads back a plain-language summary for confirmation. You correct, add, or approve. Only then does Claude write the markdown.

### Step 4 — Output two files
1. `role_[company]_[dates].md` — the master role document
2. `methodology.md` — this file (updated if the process changed)

---

## Master Role File Structure

Each role file follows this template:

```markdown
# Role: [Title] — [Company] ([Location])
**Period:** [Start] – [End] (≈X months)
**Status:** Completed / Active
**Expansion status:** v1.0 — open for future additions

## Overview
[2–4 sentence summary in first person, past tense]

## Track 1: [Main responsibility cluster]
### [Sub-topic]
- [Bullet: what I did, how, outcome]
<!-- EXPANSION SLOT: [what to add later] -->

## Track 2: [Second responsibility cluster]
...

## Collaboration & Communication
...

## Key Achievements
...

## Tools & Technologies
[Table]

## Documentation Status
[Table: what evidence exists and where]

## Notes for CV Tailoring
- For [role type]: lead with [track], emphasize [skills]
```

---

## Expansion Slots

Throughout the master file, `<!-- EXPANSION SLOT: ... -->` comments mark areas where:
- Memory was incomplete at time of writing
- More detail could be added with effort (e.g., reviewing old photos, code, contacts)
- A future conversation could drill deeper

To expand a role file in a future session:
1. Attach the existing role file
2. Tell Claude: "I want to expand the expansion slots in this file"
3. Claude will ask targeted questions for each slot
4. Revised file is regenerated as v1.1, v1.2, etc.

---

## CV Tailoring Logic

| Target Role | Lead Track | Emphasize | Downplay |
|---|---|---|---|
| IT Infrastructure | Track 2 | Network stability, hardware, troubleshooting | Code complexity |
| Software Development | Track 1 | C#/.NET, AutoCAD API, self-teaching | Hardware ops |
| Hybrid / Manufacturing Tech | Both equal | Dual ownership, manufacturing context | Neither |
| Aerospace / Defense | Both | Regulated environment, reliability outcomes | Learning curve |

The tailored CVs pull from master role files. They do not add claims not present in the master.

---

## Interview Defensibility Rule

> **If it's in a tailored CV, it must be traceable to a master role file. If it's in a master role file, you must be able to speak to it for 2 minutes without notes.**

Before finalizing any CV version, do a quick verbal run-through of each bullet. If you can't explain it naturally, either remove it or add more context to the master file first.

---

## Remaining Roles to Document

- [x] EncoreTools — CNC Programmer (Feb–May 2025) → `role_encoretools_cnc_programmer.md` v1.0 ✅
- [x] TDI Biomedical — CNC Operator (May–Aug 2023) → `role_tdi_biomedical.md` v1.0 COMPLETE ✅
- [ ] MoldTech — Thermoforming Mold Manufacturing (summers 2022 + 2024) → `role_moldtech_thermoforming.md` v0.3 skeleton
- [x] PAP / Entreamigos — Reparación CNC + fab. (Dic 2024 – Ene 2025) → `role_pap_iteso_entreamigos.md` v1.0 COMPLETE ✅
- [ ] Mechanical/Automotive 2021 — first job → `role_mechanical_automotive_2021.md` v0.1 minimal
- [ ] Independent projects (if relevant)

---

## Session Log

| Date | Session | Output |
|---|---|---|
| April 2026 | Mexico role extraction (voice interview) | `role_performance_designs_mexico.md` v1.0 |
| April 19, 2026 | CNC roles voice extraction (~90 min) | `role_encoretools_cnc_programmer.md` v1.0 + skeletons (MoldTech, Automotive) + TDI v1.0 + PAP v1.0 ✅ |
| April 19, 2026 | Format standardization pass | All skeleton files aligned to EncoreTools canonical section order |

---

*methodology.md — v1.0 — April 2026*
