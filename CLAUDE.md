# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

`mi-criterio` is a personal knowledge architecture repo. It stores context documents that eldaniels pastes into AI conversations to provide full background without re-explaining history. It is not a software project — there are no builds, tests, or deployments.

## Intended Structure

```
mi-criterio/
├── CLAUDE.md                          ← this file
├── perfil_maestro_eldaniels.txt       ← master profile, always updating (main branch)
├── cronograma_intereses.md            ← timeline of interest evolution
└── proyectos/                         ← one file per project lens
    ├── P1_cnc_manufactura.txt
    ├── P2_programacion_desarrollo.txt
    ├── P3_energia_sostenibilidad.txt
    ├── P4_finanzas_inversiones.txt
    ├── P5_geopolitica_economia.txt
    ├── P6_ayuda_futuro.txt
    ├── P7_filosofia_humanidades.txt
    └── P8_ingenieria_ciencia.txt
```

## Git Conventions

- `main` branch holds `perfil_maestro_eldaniels.txt` — the source of truth for full context
- Each `proyectos/P*.txt` file corresponds to a thematic lens that can be used independently
- Commit when a meaningful update is made to any document (career change, new tool adopted, new project started)
- Suggested commit style: `update P3: add geothermal research notes` or `perfil: new job at X`

## Document Roles

| File | Use |
|---|---|
| `perfil_maestro_eldaniels.txt` | Paste at start of any new AI conversation for full context |
| `proyectos/P*.txt` | Paste individually when working in a specific domain |
| `cronograma_intereses.md` | Reference for tracing skill/interest evolution over time |

## Key Interconnections to Maintain

When updating one document, check if related lenses need updating too:

- Finanzas ↔ Geopolítica ↔ Energía (often co-evolve)
- Programación ↔ Finanzas (Excel project is shared)
- CNC ↔ Ingeniería (applied physics, materials)
- Energía ↔ Filosofía (Solarpunk framing)
- Ayuda Futuro ↔ all (career decisions require multiple lenses)
